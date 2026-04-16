#!/usr/bin/env python3
"""ナレッジコレクター - Irodori-TTS/Emoji-TTS の制作ノウハウを自動収集

Web上の記事・投稿からTTS音声品質向上に有用なノウハウを収集し、
パイプラインへの反映提案を生成する。

標準ワークフロー:
  1. search   : WebSearch で URL を収集
  2. fetch    : WebFetch で記事内容を抽出
  3. filter   : 品質スコアリング・フィルタ
  4. report   : レポート生成（knowledge_base.md + daily CSV）
  5. propose  : パイプライン更新提案を生成
  6. status   : 収集統計を表示
  7. run      : 全パイプライン一括実行

注意:
  WebSearch/WebFetch は Claude MCP ツールであり、Pythonから直接呼べない。
  このスクリプトは **状態管理・データ永続化** を担当し、
  Web操作はスケジュールされた Claude セッションが実行する。
  Claude セッションがこのスクリプトの関数を呼び出す形で連携する。
"""
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

AGENTS_DIR = Path("D:/irodori/agents")
KNOWLEDGE_DIR = AGENTS_DIR / "knowledge"
DAILY_DIR = KNOWLEDGE_DIR / "daily"

KB_INDEX_PATH = KNOWLEDGE_DIR / "kb_index.json"
SEEN_URLS_PATH = KNOWLEDGE_DIR / "seen_urls.json"
KB_MD_PATH = KNOWLEDGE_DIR / "knowledge_base.md"
PENDING_UPDATES_PATH = KNOWLEDGE_DIR / "pending_updates.json"

JST = timezone(timedelta(hours=9))

# ============================================================
# 検索クエリ（曜日ローテーション）
# ============================================================
SEARCH_QUERIES = {
    0: [  # 月曜: コア製品
        '"Irodori-TTS" キャプション設計',
        '"Irodori-TTS" cfg パラメータ 調整',
        '"Irodori-TTS" 音声品質 コツ',
    ],
    1: [  # 火曜: フォーク
        '"Emoji-TTS" 絵文字 音声',
        '"Emoji-TTS" 感情表現 テクニック',
        'Emoji-TTS caption voice quality',
    ],
    2: [  # 水曜: VoiceDesign
        '"VoiceDesign TTS" 声質',
        'Irodori-TTS VoiceDesign caption 設計',
        '"Semantic-DACVAE" 音声合成',
    ],
    3: [  # 木曜: テクニック
        '日本語TTS 絵文字 音声品質 Irodori',
        'TTS キャプション 感情表現 テクニック',
        'text-to-speech emoji emotion Japanese',
    ],
    4: [  # 金曜: コミュニティ
        'Irodori-TTS site:x.com',
        'Irodori-TTS site:zenn.dev',
        'Irodori-TTS site:note.com',
        'Emoji-TTS site:qiita.com',
    ],
    5: [  # 土曜: 広めTTS
        '日本語音声合成 CFG チューニング',
        'TTS caption design emotional voice cfg',
        '音声合成 キャプション 行動描写 声質',
    ],
    6: [  # 日曜: キャッチオール
        'Irodori-TTS OR Emoji-TTS 2026',
        'irodori-tts 使い方 コツ ノウハウ',
        'Aratako Irodori TTS tips',
    ],
}

# 対象ドメイン
HIGH_AUTHORITY_DOMAINS = {
    "zenn.dev", "note.com", "qiita.com", "github.com",
    "huggingface.co", "x.com",
}
BLOCKED_DOMAINS = {"amazon.co.jp", "youtube.com", "wikipedia.org", "booth.pm"}

# カテゴリ定義
CATEGORIES = [
    "caption_design",      # キャプション設計
    "emoji_technique",     # 絵文字テクニック
    "cfg_tuning",          # CFG値チューニング
    "audio_postprocess",   # 音声後処理
    "voice_quality",       # 声質改善
    "training_tips",       # 学習・LoRA関連
]


# ============================================================
# データ管理
# ============================================================
def _load_json(path: Path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_kb_index() -> dict:
    default = {
        "_updated": "",
        "_total_articles": 0,
        "_categories": {c: 0 for c in CATEGORIES},
        "articles": [],
    }
    return _load_json(KB_INDEX_PATH, default)


def save_kb_index(data: dict):
    data["_updated"] = datetime.now(JST).isoformat()
    data["_total_articles"] = len(data.get("articles", []))
    # カテゴリ集計
    cat_counts = {c: 0 for c in CATEGORIES}
    for art in data.get("articles", []):
        for cat in art.get("categories", []):
            if cat in cat_counts:
                cat_counts[cat] += 1
    data["_categories"] = cat_counts
    _save_json(KB_INDEX_PATH, data)


def load_seen_urls() -> dict:
    return _load_json(SEEN_URLS_PATH, {})


def save_seen_urls(data: dict):
    _save_json(SEEN_URLS_PATH, data)


def load_pending_updates() -> dict:
    return _load_json(PENDING_UPDATES_PATH, {"pending_updates": []})


def save_pending_updates(data: dict):
    _save_json(PENDING_UPDATES_PATH, data)


def get_today_str() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d")


def content_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ============================================================
# 1. search: URL収集結果を登録する
# ============================================================
def get_todays_queries() -> list[str]:
    """今日の曜日に対応する検索クエリを返す"""
    weekday = datetime.now(JST).weekday()
    return SEARCH_QUERIES.get(weekday, SEARCH_QUERIES[0])


def register_urls(urls: list[dict]) -> dict:
    """WebSearch の結果URLを seen_urls.json に登録する

    Args:
        urls: [{"url": "https://...", "title": "記事タイトル", "snippet": "概要"}]

    Returns:
        {"new": N, "skipped": N, "blocked": N}
    """
    seen = load_seen_urls()
    today = get_today_str()

    stats = {"new": 0, "skipped": 0, "blocked": 0}

    for item in urls:
        url = item.get("url", "").strip()
        if not url:
            continue

        # ブロックドメインチェック
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace("www.", "")
        if any(bd in domain for bd in BLOCKED_DOMAINS):
            stats["blocked"] += 1
            continue

        # 重複チェック
        if url in seen:
            seen[url]["last_checked"] = today
            stats["skipped"] += 1
            continue

        # 新規登録
        seen[url] = {
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "first_seen": today,
            "last_checked": today,
            "status": "pending_fetch",
            "content_hash": "",
        }
        stats["new"] += 1

    save_seen_urls(seen)
    print(f"[search] 新規: {stats['new']}, スキップ: {stats['skipped']}, ブロック: {stats['blocked']}")
    return stats


# ============================================================
# 2. fetch: 記事内容を kb_index に登録する
# ============================================================
def register_article(article_data: dict) -> bool:
    """WebFetch で抽出した記事データを kb_index.json に登録する

    Args:
        article_data: {
            "url": "https://...",
            "title": "記事タイトル",
            "summary": "1-2文の要約",
            "categories": ["caption_design", "cfg_tuning"],
            "extracted_knowhow": [
                {
                    "type": "caption_technique",
                    "finding": "具体的な発見",
                    "params": {"cfg_caption": 5.0},
                    "confidence": "high",
                    "actionable": true
                }
            ],
            "relevance_indicators": {
                "mentions_irodori": true,
                "mentions_emoji_tts": false,
                "has_specific_params": true,
                "has_comparison": false,
                "has_caption_examples": true
            },
            "publish_date": "2026-04-11",
            "full_text": "記事の全文（ハッシュ計算用）"
        }

    Returns:
        True if registered, False if duplicate/rejected
    """
    kb = load_kb_index()
    seen = load_seen_urls()
    today = get_today_str()

    url = article_data.get("url", "")
    full_text = article_data.get("full_text", article_data.get("summary", ""))
    c_hash = content_hash(full_text)

    # 重複チェック（content hash）
    for existing in kb.get("articles", []):
        if existing.get("content_hash") == c_hash:
            print(f"[fetch] 重複スキップ（content hash一致）: {url}")
            return False
        if existing.get("url") == url:
            print(f"[fetch] 重複スキップ（URL一致）: {url}")
            return False

    # 記事ID生成
    article_count = len(kb.get("articles", []))
    article_id = f"art_{today.replace('-', '')}_{article_count + 1:03d}"

    # 関連性スコア計算
    indicators = article_data.get("relevance_indicators", {})
    relevance = _compute_relevance(indicators)

    # 品質スコア計算
    quality = _compute_quality(article_data)

    # 統合スコア
    combined = 0.6 * relevance + 0.4 * quality

    article = {
        "id": article_id,
        "url": url,
        "title": article_data.get("title", ""),
        "source_type": _detect_source_type(url),
        "discovered_date": today,
        "fetch_date": today,
        "categories": article_data.get("categories", []),
        "relevance_score": round(relevance, 2),
        "quality_score": round(quality, 2),
        "combined_score": round(combined, 2),
        "content_hash": c_hash,
        "summary": article_data.get("summary", ""),
        "extracted_knowhow": article_data.get("extracted_knowhow", []),
        "publish_date": article_data.get("publish_date", ""),
        "excluded": combined < 0.5,
        "exclusion_reason": "combined_score < 0.5" if combined < 0.5 else None,
    }

    kb.setdefault("articles", []).append(article)
    save_kb_index(kb)

    # seen_urls 更新
    if url in seen:
        seen[url]["status"] = "fetched"
        seen[url]["content_hash"] = c_hash
        save_seen_urls(seen)

    status = "除外" if article["excluded"] else "採用"
    print(f"[fetch] {status} (score={combined:.2f}): {article_data.get('title', url)[:50]}")
    return not article["excluded"]


def _compute_relevance(indicators: dict) -> float:
    """関連性スコアを計算（0.0-1.0）"""
    score = 0.0
    if indicators.get("mentions_irodori"):
        score += 0.25
    if indicators.get("mentions_emoji_tts"):
        score += 0.15
    if indicators.get("has_specific_params"):
        score += 0.20
    if indicators.get("has_caption_examples"):
        score += 0.20
    if indicators.get("has_comparison"):
        score += 0.20
    return min(score, 1.0)


def _compute_quality(article_data: dict) -> float:
    """品質スコアを計算（0.0-1.0）"""
    score = 0.0
    indicators = article_data.get("relevance_indicators", {})
    knowhow = article_data.get("extracted_knowhow", [])

    # 具体的パラメータを含む
    if indicators.get("has_specific_params"):
        score += 0.25

    # 新規テクニック（knowhow にactionable=trueがある）
    actionable_count = sum(1 for k in knowhow if k.get("actionable"))
    if actionable_count > 0:
        score += 0.25

    # Before/After比較あり
    if indicators.get("has_comparison"):
        score += 0.20

    # 鮮度
    pub_date = article_data.get("publish_date", "")
    if pub_date:
        try:
            pub = datetime.strptime(pub_date, "%Y-%m-%d").replace(tzinfo=JST)
            days_old = (datetime.now(JST) - pub).days
            if days_old <= 7:
                score += 0.15
            elif days_old <= 30:
                score += 0.10
            elif days_old <= 90:
                score += 0.05
        except ValueError:
            pass

    # ドメイン権威
    url = article_data.get("url", "")
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace("www.", "")
    if any(d in domain for d in HIGH_AUTHORITY_DOMAINS):
        score += 0.15

    return min(score, 1.0)


def _detect_source_type(url: str) -> str:
    if "x.com" in url or "twitter.com" in url:
        return "tweet"
    if "github.com" in url:
        return "github"
    if "huggingface.co" in url:
        return "huggingface"
    if any(d in url for d in ["zenn.dev", "note.com", "qiita.com"]):
        return "blog"
    return "web"


# ============================================================
# 3. filter: スコアに基づくフィルタリング
# ============================================================
def filter_articles(threshold: float = 0.5) -> dict:
    """kb_index の記事をスコアでフィルタリングし直す"""
    kb = load_kb_index()
    stats = {"total": 0, "passed": 0, "excluded": 0}

    for article in kb.get("articles", []):
        stats["total"] += 1
        combined = article.get("combined_score", 0)
        if combined >= threshold:
            article["excluded"] = False
            article["exclusion_reason"] = None
            stats["passed"] += 1
        else:
            article["excluded"] = True
            article["exclusion_reason"] = f"combined_score {combined:.2f} < {threshold}"
            stats["excluded"] += 1

    save_kb_index(kb)
    print(f"[filter] 合計: {stats['total']}, 採用: {stats['passed']}, 除外: {stats['excluded']}")
    return stats


# ============================================================
# 4. report: knowledge_base.md + daily CSV 生成
# ============================================================
def generate_report(target_date: str = None) -> str:
    """knowledge_base.md を再生成し、daily CSV を出力する"""
    kb = load_kb_index()
    today = target_date or get_today_str()

    # --- knowledge_base.md 生成 ---
    included = [a for a in kb.get("articles", []) if not a.get("excluded")]
    included.sort(key=lambda a: a.get("combined_score", 0), reverse=True)

    lines = [
        f"# TTS Production Knowledge Base",
        f"_Auto-updated: {today} | Total findings: {_count_knowhow(included)} | Sources: {len(included)} articles_\n",
    ]

    # knowhow を type でカテゴリ分類（重複なし）
    cat_map = {
        "caption_technique": "caption_design",
        "caption_design": "caption_design",
        "emoji_technique": "emoji_technique",
        "cfg_tuning": "cfg_tuning",
        "audio_postprocess": "audio_postprocess",
        "voice_quality": "voice_quality",
        "training_tips": "training_tips",
    }
    cat_labels = {
        "caption_design": "Caption Design (キャプション設計)",
        "emoji_technique": "Emoji Technique (絵文字テクニック)",
        "cfg_tuning": "CFG Tuning (CFGチューニング)",
        "audio_postprocess": "Audio Post-Processing (音声後処理)",
        "voice_quality": "Voice Quality (声質改善)",
        "training_tips": "Training Tips (学習・LoRA)",
    }

    # カテゴリごとに knowhow を集約
    cat_knowhow: dict[str, list] = {c: [] for c in CATEGORIES}
    for art in included:
        for kh in art.get("extracted_knowhow", []):
            if not kh.get("actionable"):
                continue
            kh_cat = cat_map.get(kh.get("type", ""), "voice_quality")
            cat_knowhow[kh_cat].append((art, kh))

    for category in CATEGORIES:
        items = cat_knowhow[category]
        if not items:
            continue

        lines.append(f"\n## {cat_labels.get(category, category)}\n")

        for art, kh in items:
            lines.append(f"### {kh.get('finding', 'N/A')[:80]}")
            lines.append(f"- Source: [{art.get('title', 'N/A')}]({art.get('url', '')})")
            if art.get("publish_date"):
                lines.append(f"- Date: {art['publish_date']}")
            if kh.get("params"):
                params_str = ", ".join(f"{k}={v}" for k, v in kh["params"].items())
                lines.append(f"- Params: {params_str}")
            lines.append(f"- Confidence: {kh.get('confidence', 'N/A')}")
            lines.append("")

    md_content = "\n".join(lines)
    with open(KB_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    # --- daily CSV 生成 ---
    csv_path = DAILY_DIR / f"{today}.csv"
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    today_articles = [a for a in included if a.get("discovered_date") == today]

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "url", "categories", "combined_score",
                         "summary", "knowhow_count", "publish_date"])
        for art in today_articles:
            writer.writerow([
                art.get("id", ""),
                art.get("title", ""),
                art.get("url", ""),
                ",".join(art.get("categories", [])),
                art.get("combined_score", 0),
                art.get("summary", "")[:100],
                len([k for k in art.get("extracted_knowhow", []) if k.get("actionable")]),
                art.get("publish_date", ""),
            ])

    print(f"[report] knowledge_base.md 生成 ({len(included)}記事, {_count_knowhow(included)} findings)")
    print(f"[report] daily CSV 生成: {csv_path} ({len(today_articles)}記事)")
    return str(csv_path)


def _count_knowhow(articles: list) -> int:
    return sum(
        len([k for k in a.get("extracted_knowhow", []) if k.get("actionable")])
        for a in articles
    )


# ============================================================
# 5. propose: パイプライン更新提案を生成
# ============================================================
def generate_proposals() -> list[dict]:
    """採用済み記事から、パイプラインへの変更提案を生成する

    この関数は Claude が呼び出し、knowhow の内容に基づいて
    具体的な提案を pending_updates.json に追記する。
    """
    kb = load_kb_index()
    included = [a for a in kb.get("articles", []) if not a.get("excluded")]

    pending = load_pending_updates()
    existing_ids = {u.get("source_article") for u in pending.get("pending_updates", [])}

    new_proposals = []
    today = get_today_str()

    for art in included:
        if art["id"] in existing_ids:
            continue

        for kh in art.get("extracted_knowhow", []):
            if not kh.get("actionable"):
                continue

            proposal = _knowhow_to_proposal(art, kh, today)
            if proposal:
                new_proposals.append(proposal)

    if new_proposals:
        pending.setdefault("pending_updates", []).extend(new_proposals)
        save_pending_updates(pending)

    print(f"[propose] 新規提案: {len(new_proposals)}件")
    return new_proposals


def _knowhow_to_proposal(article: dict, knowhow: dict, today: str) -> dict | None:
    """knowhow を pipeline 更新提案に変換する"""
    kh_type = knowhow.get("type", "")
    params = knowhow.get("params", {})

    # キャプション関連
    if kh_type in ("caption_technique", "caption_design") or "caption" in kh_type:
        return {
            "id": f"upd_{today.replace('-', '')}_{article['id']}",
            "target": "default_captions.json",
            "operation": "review_caption_technique",
            "data": {
                "finding": knowhow.get("finding", ""),
                "params": params,
            },
            "source_article": article["id"],
            "source_url": article.get("url", ""),
            "confidence": knowhow.get("confidence", "medium"),
            "status": "pending_review",
            "created": today,
        }

    # CFG関連
    if "cfg" in kh_type:
        return {
            "id": f"upd_{today.replace('-', '')}_{article['id']}",
            "target": "default_captions.json",
            "operation": "review_cfg_values",
            "data": {
                "finding": knowhow.get("finding", ""),
                "params": params,
            },
            "source_article": article["id"],
            "source_url": article.get("url", ""),
            "confidence": knowhow.get("confidence", "medium"),
            "status": "pending_review",
            "created": today,
        }

    # 絵文字関連
    if "emoji" in kh_type:
        return {
            "id": f"upd_{today.replace('-', '')}_{article['id']}",
            "target": "emoji_patterns.json",
            "operation": "review_emoji_pattern",
            "data": {
                "finding": knowhow.get("finding", ""),
                "params": params,
            },
            "source_article": article["id"],
            "source_url": article.get("url", ""),
            "confidence": knowhow.get("confidence", "medium"),
            "status": "pending_review",
            "created": today,
        }

    # 音声後処理関連
    if "postprocess" in kh_type or "audio" in kh_type:
        return {
            "id": f"upd_{today.replace('-', '')}_{article['id']}",
            "target": "ma_agent.py",
            "operation": "review_postprocess_technique",
            "data": {
                "finding": knowhow.get("finding", ""),
                "params": params,
            },
            "source_article": article["id"],
            "source_url": article.get("url", ""),
            "confidence": knowhow.get("confidence", "medium"),
            "status": "pending_review",
            "created": today,
        }

    return None


# ============================================================
# 6. status: 収集統計表示
# ============================================================
def show_status():
    """収集状況を表示する"""
    kb = load_kb_index()
    seen = load_seen_urls()
    pending = load_pending_updates()

    total = len(kb.get("articles", []))
    included = len([a for a in kb.get("articles", []) if not a.get("excluded")])
    excluded = total - included
    knowhow_count = _count_knowhow([a for a in kb.get("articles", []) if not a.get("excluded")])

    print(f"\n{'='*50}")
    print(f"ナレッジコレクター状況")
    print(f"{'='*50}")
    print(f"  URL登録数: {len(seen)}")
    print(f"  記事数: {total} (採用: {included}, 除外: {excluded})")
    print(f"  ノウハウ数: {knowhow_count}")
    print(f"  保留中の提案: {len(pending.get('pending_updates', []))}件")

    # カテゴリ分布
    cats = kb.get("_categories", {})
    if any(v > 0 for v in cats.values()):
        print(f"\n  カテゴリ分布:")
        for cat, count in cats.items():
            if count > 0:
                print(f"    {cat}: {count}")

    # 直近5記事
    articles = kb.get("articles", [])
    if articles:
        recent = sorted(articles, key=lambda a: a.get("discovered_date", ""), reverse=True)[:5]
        print(f"\n  直近の記事:")
        for a in recent:
            status = "除外" if a.get("excluded") else "採用"
            print(f"    [{status}] {a.get('title', 'N/A')[:40]} (score={a.get('combined_score', 0):.2f})")

    # daily ファイル
    daily_files = sorted(DAILY_DIR.glob("*.csv"))
    if daily_files:
        print(f"\n  日次レポート: {len(daily_files)}件 (最新: {daily_files[-1].stem})")

    # knowledge_base.md
    if KB_MD_PATH.exists():
        size = KB_MD_PATH.stat().st_size
        print(f"  knowledge_base.md: {size/1024:.1f}KB")


# ============================================================
# 7. Slack通知用サマリー生成
# ============================================================
def generate_slack_summary(target_date: str = None) -> str:
    """Slack #tts チャンネルに送信するサマリーテキストを生成する"""
    kb = load_kb_index()
    pending = load_pending_updates()
    today = target_date or get_today_str()

    today_articles = [
        a for a in kb.get("articles", [])
        if a.get("discovered_date") == today and not a.get("excluded")
    ]

    if not today_articles:
        return f"*TTS Knowledge Collector ({today})*\n新規記事: 0件\n今日は有用な記事が見つかりませんでした。"

    # TOP3
    top3 = sorted(today_articles, key=lambda a: a.get("combined_score", 0), reverse=True)[:3]
    today_proposals = [
        p for p in pending.get("pending_updates", [])
        if p.get("created") == today
    ]

    lines = [
        f"*TTS Knowledge Collector ({today})*",
        f"新規記事: {len(today_articles)}件 | 提案: {len(today_proposals)}件",
        "",
    ]

    for i, art in enumerate(top3, 1):
        lines.append(f"*{i}. {art.get('title', 'N/A')[:50]}*")
        lines.append(f"   Score: {art.get('combined_score', 0):.2f} | {', '.join(art.get('categories', []))}")
        lines.append(f"   {art.get('summary', '')[:80]}")
        lines.append(f"   <{art.get('url', '')}|記事を読む>")
        lines.append("")

    if today_proposals:
        lines.append("*パイプライン更新提案:*")
        for p in today_proposals[:3]:
            lines.append(f"  - [{p.get('target', '')}] {p.get('data', {}).get('finding', '')[:60]}")

    return "\n".join(lines)


# ============================================================
# 8. Claude セッション用: WebFetch プロンプト生成
# ============================================================
def get_fetch_prompt() -> str:
    """WebFetch に渡す記事内容抽出プロンプトを返す"""
    return """この記事からTTS音声生成に関する技術的なノウハウを抽出してください。
以下のJSON形式で回答してください:

{
  "title": "記事タイトル",
  "summary": "1-2文の要約（実用テクニックに焦点）",
  "categories": ["caption_design", "emoji_technique", "cfg_tuning", "audio_postprocess", "voice_quality", "training_tips"],
  "extracted_knowhow": [
    {
      "type": "caption_technique|emoji_technique|cfg_tuning|audio_postprocess|voice_quality|training_tips",
      "finding": "具体的な発見内容",
      "params": {"パラメータ名": 値},
      "confidence": "high|medium|low",
      "actionable": true
    }
  ],
  "relevance_indicators": {
    "mentions_irodori": true/false,
    "mentions_emoji_tts": true/false,
    "has_specific_params": true/false,
    "has_comparison": true/false,
    "has_caption_examples": true/false
  },
  "publish_date": "YYYY-MM-DD or null"
}

対象TTS: Irodori-TTS, Emoji-TTS, VoiceDesign TTS のみ。
インストール手順、ライセンス、一般概要は無視。
具体的なパラメータ値やテクニックを重点的に抽出。"""


# ============================================================
# CLI
# ============================================================
USAGE = """ナレッジコレクター - TTS制作ノウハウ自動収集

Usage:
  python knowledge_collector.py search                      -- 今日の検索クエリを表示
  python knowledge_collector.py fetch                       -- 未取得URLの一覧を表示
  python knowledge_collector.py filter [--threshold 0.5]    -- 品質フィルタリング
  python knowledge_collector.py report [--date YYYY-MM-DD]  -- レポート生成
  python knowledge_collector.py propose                     -- パイプライン更新提案を生成
  python knowledge_collector.py status                      -- 収集統計表示
  python knowledge_collector.py queries                     -- 今日の検索クエリ一覧

注意:
  WebSearch/WebFetch は Claude MCP ツールです。
  このスクリプトは状態管理を担当し、Web操作はClaudeセッションが実行します。
  毎日9:00のスケジュールタスクで自動実行されます。
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "search" or cmd == "queries":
        queries = get_todays_queries()
        weekday_names = ["月", "火", "水", "木", "金", "土", "日"]
        weekday = datetime.now(JST).weekday()
        print(f"\n今日（{weekday_names[weekday]}曜日）の検索クエリ:")
        for q in queries:
            print(f"  - {q}")
        print(f"\n合計: {len(queries)}クエリ")

    elif cmd == "fetch":
        seen = load_seen_urls()
        pending = [(url, info) for url, info in seen.items()
                   if info.get("status") == "pending_fetch"]
        print(f"\n未取得URL: {len(pending)}件")
        for url, info in pending[:10]:
            print(f"  {info.get('title', url)[:50]}")
            print(f"    {url}")

    elif cmd == "filter":
        threshold = 0.5
        if "--threshold" in sys.argv:
            idx = sys.argv.index("--threshold")
            if idx + 1 < len(sys.argv):
                threshold = float(sys.argv[idx + 1])
        filter_articles(threshold)

    elif cmd == "report":
        target_date = None
        if "--date" in sys.argv:
            idx = sys.argv.index("--date")
            if idx + 1 < len(sys.argv):
                target_date = sys.argv[idx + 1]
        generate_report(target_date)

    elif cmd == "propose":
        generate_proposals()

    elif cmd == "status":
        show_status()

    else:
        print(f"Unknown command: {cmd}")
        print(USAGE)
        sys.exit(1)
