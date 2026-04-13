#!/usr/bin/env python3
"""脚本処理エージェント - Grokの生台本（JSON/CSV/TXT）を絵文字付きproduction.csvに変換
サンドイッチ方式: 感情強度に応じて prefix + テキスト + suffix で絵文字を配置
"""
import csv
import json
import re
import sys
from pathlib import Path

PROJECTS_DIR = Path("D:/irodori/projects")

# ============================================================
# 感情キーワード → 絵文字マッピング（全タグマッチ方式）
# ============================================================
EMOTION_EMOJI_MAP = [
    # 効果音・息遣い系
    (r"囁き|ささやき|耳元|ひそひそ|ウィスパー", "👂"),
    (r"吐息|溜息|ため息|寝息", "😮\u200d💨"),
    (r"喘ぎ\(強\)|喘ぎ（強）", "🥵"),
    (r"喘ぎ\(弱\)|喘ぎ（弱）", "🥵"),
    (r"喘ぎ|あえぎ|荒い息|うめき", "🥵"),
    (r"息切れ|荒い息遣い|はぁはぁ", "😮\u200d💨"),
    (r"息をのむ|ハッ", "😮"),
    (r"舐め|ぺろ|ちゅぱ|水音", "👅"),
    (r"リップ|キス|唇|ちゅ", "💋"),
    # 感情・話し方系
    (r"笑い|くすくす|ふふ|クスッ|含み笑", "🤭"),
    (r"甘え", "😏"),
    (r"からかう|からかい|いたずら|小悪魔", "😏"),
    (r"恥ずかし|照れ|もじもじ|テレ|恥じらい", "🫣"),
    (r"震え|おどおど|自信な", "🥺"),
    (r"泣き|泣く|嗚咽|涙声", "😭"),
    (r"悲鳴|叫び|絶叫|キャー", "😱"),
    (r"怒り|怒る|不満|イライラ|拗ね", "😠"),
    (r"驚き|びっくり|えっ", "😲"),
    (r"優し|穏やか|慈しみ", "🫶"),
    (r"眠い|だるい|まどろみ|寝起き", "😪"),
    (r"慌て|パニック|どもり|焦", "😰"),
    (r"喜び|嬉し|楽し|ウキウキ", "😆"),
    (r"懇願|お願い|頼む", "🙏"),
    (r"酔|ほろ酔い", "🥴"),
    (r"口を塞|くぐもっ", "🤐"),
    (r"安堵|ほっ|満足|安心", "😌"),
    (r"疑問|不思議|首かしげ", "🤔"),
    (r"苦し|痛|うぅ", "😖"),
    (r"心配|不安そう", "😟"),
    (r"呆れ|やれやれ", "🙄"),
    (r"放心|虚脱|朦朧|脱力", "😌"),
    (r"拒絶|拒否", "😱"),
    (r"屈辱|崩壊", "😭"),
    (r"絶望", "😭"),
    (r"絶頂", "😱"),
    (r"動揺", "😰"),
    (r"恐怖", "😱"),
    (r"強がり", "😤"),
    (r"自信|威圧|挑発", "😤"),
    (r"抵抗", "😖"),
    (r"困惑", "😖"),
    # エフェクト
    (r"💦|汗|濡", "💦"),
    # 広い感情（最後）
    (r"明るい|元気|ハキハキ", "😊"),
    (r"日常|普通|通常|ナレーション", ""),
]

# ============================================================
# 感情強度の判定キーワード
# ============================================================
INTENSITY_STRONG = {
    "喘ぎ(強)", "喘ぎ（強）", "絶頂", "叫び", "嗚咽", "荒い息遣い",
    "崩壊", "絶叫", "連続絶頂",
}
INTENSITY_MEDIUM = {
    "喘ぎ(弱)", "喘ぎ（弱）", "恥じらい", "困惑", "動揺", "恐怖",
    "抵抗", "拒絶", "屈辱", "絶望",
}
INTENSITY_EXTREME = {
    "出産", "全穴同時", "連続絶頂", "妊娠",
}


def classify_intensity(emotion_tags: list[str]) -> str:
    """感情タグリストから強度レベルを判定する"""
    tag_set = set(emotion_tags)
    if tag_set & INTENSITY_EXTREME:
        return "extreme"
    # 強いタグが2個以上 or 強いタグ + 中タグ = strong
    strong_count = len(tag_set & INTENSITY_STRONG)
    medium_count = len(tag_set & INTENSITY_MEDIUM)
    if strong_count >= 2:
        return "strong"
    if strong_count >= 1 and medium_count >= 1:
        return "strong"
    if strong_count >= 1:
        return "medium"
    if medium_count >= 1:
        return "medium"
    return "weak"


def emotion_to_emojis_all(emotion: str) -> list[str]:
    """感情テキストから全マッチする絵文字をリストで返す（重複排除）"""
    if not emotion:
        return []
    emojis = []
    seen = set()
    # スペースまたはカンマで分割して各タグを処理
    tags = re.split(r"[,、\s]+", emotion.strip())
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        for pattern, emoji in EMOTION_EMOJI_MAP:
            if re.search(pattern, tag):
                if emoji and emoji not in seen:
                    emojis.append(emoji)
                    seen.add(emoji)
                break
    return emojis


def build_sandwich(text: str, emojis: list[str], intensity: str) -> str:
    """テスト結果に基づいたサンドイッチ方式で絵文字を配置する

    聴き比べテスト結果（2026-04-13）:
      弱: B_sandwich（prefix 2-3, suffix 1）が最適
      中: B_sandwich or C_prefix_多（prefix 2-4, suffix 0-1）
      強: D_sandwich_多（prefix 3-5, suffix 2-3）が圧勝
      極限: D_sandwich_多 最大盛り
    """
    if not emojis:
        return text

    if intensity == "weak":
        # B_sandwich: prefix 2-3, suffix 1
        prefix = "".join(emojis[:3])
        suffix = emojis[-1] if len(emojis) >= 2 else ""
    elif intensity == "medium":
        # B_sandwich〜C_prefix_多: prefix 2-4, suffix 0-1
        prefix = "".join(emojis[:4])
        suffix = emojis[-1] if len(emojis) >= 3 else ""
    elif intensity == "strong":
        # D_sandwich_多: prefix all, suffix 2-3
        prefix = "".join(emojis)
        suffix_emojis = emojis[-3:] if len(emojis) >= 3 else emojis[-2:]
        # suffix は prefix と少し違う組み合わせで着地を表現
        suffix = "".join(suffix_emojis)
        # 💦 を suffix に追加（強い感情の余韻）
        if "💦" not in suffix:
            suffix += "💦"
    else:  # extreme
        # D_sandwich_多 最大盛り
        prefix = "".join(emojis)
        suffix_emojis = emojis[-3:] if len(emojis) >= 3 else emojis
        suffix = "".join(suffix_emojis) + "💦"

    result = f"{prefix} {text}"
    if suffix:
        result += f" {suffix}"
    return result


def normalize_text(text: str) -> str:
    """テキストを正規化する（TTS向け）"""
    text = text.strip()
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"。{2,}", "。", text)
    text = text.strip("「」『』\"")
    # Grokが埋め込んだ絵文字を除去（text_rawはクリーンに保つ）
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U00002702-\U000027B0"  # dingbats
        "\U0000FE00-\U0000FE0F"  # variation selectors
        "\U0000200D"             # zero width joiner
        "\U00002640-\U00002642"  # gender symbols
        "\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub("", text).strip()


def load_json(filepath: Path) -> list[dict]:
    """JSON形式の台本を読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "lines" in data:
        return data["lines"]
    return []


def load_csv(filepath: Path) -> list[dict]:
    """CSV形式の台本を読み込む"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_txt(filepath: Path) -> list[dict]:
    """プレーンテキスト形式を読み込む（空行でシーン区切り）"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    rows = []
    scene_num = 1
    for line in lines:
        line = line.strip()
        if not line:
            scene_num += 1
            continue
        rows.append({
            "scene_id": f"scene_{scene_num:02d}",
            "speaker": "キャラ",
            "emotion_note": "日常",
            "text_raw": line,
        })
    return rows


def process_script(project_name: str) -> str:
    """台本ファイルを読み込んで production.csv を生成する

    対応形式（優先順）:
      1. script_raw.json  (推奨: Grok JSON出力)
      2. script_raw.csv
      3. script_raw.txt
    """
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"

    raw_json = project_dir / "script_raw.json"
    raw_csv = project_dir / "script_raw.csv"
    raw_txt = project_dir / "script_raw.txt"

    # 読み込み
    rows = []
    if raw_json.exists():
        rows = load_json(raw_json)
        print(f"[ok] script_raw.json を読み込みました ({len(rows)}行)")
    elif raw_csv.exists():
        rows = load_csv(raw_csv)
        print(f"[ok] script_raw.csv を読み込みました ({len(rows)}行)")
    elif raw_txt.exists():
        rows = load_txt(raw_txt)
        print(f"[ok] script_raw.txt を読み込みました ({len(rows)}行)")
    else:
        print(f"[error] 台本ファイルが見つかりません: {project_dir}")
        print(f"  対応形式: script_raw.json / script_raw.csv / script_raw.txt")
        return ""

    if not rows:
        print("[error] 台本が空です")
        return ""

    # production.csv に変換
    prod_rows = []
    scene_line_counts = {}
    stats = {"weak": 0, "medium": 0, "strong": 0, "extreme": 0}

    for row in rows:
        scene_id = row.get("scene_id", "scene_01").strip()
        scene_line_counts[scene_id] = scene_line_counts.get(scene_id, 0) + 1
        line_num = scene_line_counts[scene_id]

        # テキスト取得（JSON: text_raw, CSV: text / text_raw）
        text_raw_orig = row.get("text_raw", row.get("text", ""))
        text_raw = normalize_text(text_raw_orig)

        # 感情タグ取得（JSON: emotion_tags / emotion_note, CSV: emotion / emotion_note）
        emotion = row.get("emotion_tags",
                  row.get("emotion_note",
                  row.get("emotion", "")))

        # Grokの絵文字提案があればマージ用に保持
        grok_emoji = row.get("emoji_suggestion", "")

        # 感情タグをパース
        tags = [t.strip() for t in re.split(r"[,、\s]+", emotion.strip()) if t.strip()]

        # 強度判定
        intensity = classify_intensity(tags)
        stats[intensity] += 1

        # 絵文字変換
        emojis = emotion_to_emojis_all(emotion)

        # Grok絵文字提案があればそちらを優先
        if grok_emoji:
            text_with_emoji = f"{grok_emoji} {text_raw}"
        else:
            text_with_emoji = build_sandwich(text_raw, emojis, intensity)

        prod_rows.append({
            "scene_id": scene_id,
            "line_id": f"line_{line_num:03d}",
            "speaker": row.get("speaker", "").strip(),
            "emotion_note": emotion,
            "text_raw": text_raw,
            "text_with_emoji": text_with_emoji,
            "caption": "",
            "cfg_text": "",
            "cfg_caption": "",
            "cfg_speaker": "",
            "num_steps": "",
            "num_candidates": "3",
            "seed": "",
            "status": "pending",
            "approved_candidate": "",
            "notes": f"intensity={intensity}",
        })

    # 書き出し
    fieldnames = list(prod_rows[0].keys())
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)

    # プレーンテキストも出力（人間確認用）
    txt_path = project_dir / "script_with_emoji.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        current_scene = ""
        for row in prod_rows:
            if row["scene_id"] != current_scene:
                current_scene = row["scene_id"]
                f.write(f"\n=== {current_scene} ===\n")
            intensity_mark = row["notes"].replace("intensity=", "")
            f.write(f"[{intensity_mark}][{row['emotion_note']}] {row['text_with_emoji']}\n")

    print(f"\n[ok] production.csv を生成しました ({len(prod_rows)}行)")
    print(f"[ok] script_with_emoji.txt を生成しました（確認用）")

    # サマリー
    scenes = sorted(set(r["scene_id"] for r in prod_rows))
    print(f"\n  シーン数: {len(scenes)}")
    for s in scenes:
        count = sum(1 for r in prod_rows if r["scene_id"] == s)
        print(f"    {s}: {count}行")

    print(f"\n  強度分布:")
    print(f"    弱 (B_sandwich):     {stats['weak']}行")
    print(f"    中 (B/C方式):        {stats['medium']}行")
    print(f"    強 (D_sandwich_多):  {stats['strong']}行")
    print(f"    極限 (D最大盛り):    {stats['extreme']}行")

    return str(prod_csv)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_processor.py <project_name>")
        print("  台本形式: script_raw.json (推奨) / script_raw.csv / script_raw.txt")
        sys.exit(1)
    process_script(sys.argv[1])
