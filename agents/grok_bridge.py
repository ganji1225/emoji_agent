#!/usr/bin/env python3
"""Grokブリッジエージェント - Grok↔パイプライン間のワークフロー管理

標準ワークフロー:
  1. init     : プロジェクトにgrok/フォルダを作成、指示書テンプレートを配置
  2. prepare  : project_brief.json → grok/prompt.md を生成
  3. validate : grok/response.json のバリデーション
  4. process  : grok/response.json → production.csv → キャプション適用
  5. status   : 現在の進捗を表示
"""
import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("D:/irodori/projects")
AGENTS_DIR = Path("D:/irodori/agents")
TEMPLATE_DIR = AGENTS_DIR / "templates"


# ============================================================
# 1. init: grok/ フォルダとテンプレートを配置
# ============================================================
def init_grok_workspace(project_name: str) -> None:
    """プロジェクトにgrok/フォルダを作成し、指示書テンプレートを配置する"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    grok_dir.mkdir(parents=True, exist_ok=True)

    # テンプレートをコピー
    template_src = TEMPLATE_DIR / "grok_prompt_template.md"
    if template_src.exists():
        dest = grok_dir / "prompt_template.md"
        if not dest.exists():
            shutil.copy2(template_src, dest)
            print(f"[ok] テンプレート配置: {dest}")
        else:
            print(f"[skip] テンプレート既存: {dest}")
    else:
        print(f"[warn] テンプレートが見つかりません: {template_src}")

    # 空の response.json プレースホルダ
    response_file = grok_dir / "response.json"
    if not response_file.exists():
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        print(f"[ok] レスポンスファイル作成: {response_file}")

    print(f"\n[ok] Grokワークスペース初期化完了: {grok_dir}")
    print(f"\n次のステップ:")
    print(f"  1. grok/prompt_template.md をカスタマイズして grok/prompt.md を作成")
    print(f"  2. Grokに prompt.md を渡してJSON出力を取得")
    print(f"  3. 出力を grok/response.json に保存")
    print(f"  4. python grok_bridge.py validate {project_name}")


# ============================================================
# 2. prepare: project_brief.json → grok/prompt.md
# ============================================================
def prepare_prompt(project_name: str) -> None:
    """project_brief.json が存在すれば planner.py で指示書を生成し grok/ に配置"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    grok_dir.mkdir(parents=True, exist_ok=True)

    brief_path = project_dir / "project_brief.json"
    if not brief_path.exists():
        print(f"[info] project_brief.json が無いため、テンプレートから直接編集してください")
        print(f"  テンプレート: {grok_dir / 'prompt_template.md'}")
        return

    # planner.py の generate_grok_prompt を呼ぶ
    sys.path.insert(0, str(AGENTS_DIR))
    from planner import generate_grok_prompt
    generate_grok_prompt(project_dir)

    # 生成された grok_prompt.md を grok/ にもコピー
    src = project_dir / "grok_prompt.md"
    if src.exists():
        dest = grok_dir / "prompt.md"
        shutil.copy2(src, dest)
        print(f"[ok] 指示書を grok/ にコピー: {dest}")


# ============================================================
# 3. validate: Grokの出力JSONをバリデーション
# ============================================================
REQUIRED_FIELDS = {"scene_id", "line_id", "speaker", "emotion_tags", "text_raw"}
OPTIONAL_FIELDS = {"emoji_suggestion"}
VALID_EMOTIONS = {
    "自信", "威圧", "挑発", "動揺", "恐怖", "絶望", "強がり", "驚き", "怒り",
    "照れ", "恥じらい", "困惑", "もじもじ",
    "甘え", "囁き", "からかう", "優しい",
    "吐息", "喘ぎ", "喘ぎ(弱)", "喘ぎ(強)", "息切れ", "荒い息遣い",
    "泣き", "嗚咽", "涙声",
    "絶頂", "叫び", "悲鳴", "苦しい", "崩壊",
    "放心", "脱力", "朦朧", "虚脱", "安堵",
    "舌打ち", "唾を飲む", "リップ", "あくび",
    "拒絶", "屈辱", "抵抗", "懇願",
}

def validate_response(project_name: str) -> dict:
    """grok/response.json をバリデーションし、問題点を報告する"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    response_path = grok_dir / "response.json"

    # script_raw_grok.json からも読み込み可能（後方互換）
    if not response_path.exists():
        alt_path = project_dir / "script_raw_grok.json"
        if alt_path.exists():
            response_path = alt_path
            print(f"[info] grok/response.json が無いため {alt_path.name} を使用")
        else:
            print(f"[error] レスポンスファイルが見つかりません")
            print(f"  期待パス: {response_path}")
            print(f"  代替パス: {alt_path}")
            return {"valid": False}

    with open(response_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"[error] JSON配列ではありません（型: {type(data).__name__}）")
        return {"valid": False}

    if len(data) == 0:
        print(f"[warn] JSONが空です。Grokの出力を response.json に貼り付けてください")
        return {"valid": False, "empty": True}

    errors = []
    warnings = []
    scenes = set()
    emotion_counter = {}

    for i, entry in enumerate(data):
        line_label = f"行{i+1}"

        # 必須フィールドチェック
        for field in REQUIRED_FIELDS:
            if field not in entry or not str(entry[field]).strip():
                errors.append(f"{line_label}: 必須フィールド '{field}' が空です")

        # scene_id チェック
        sid = entry.get("scene_id", "")
        scenes.add(sid)

        # emotion_tags チェック
        tags_str = entry.get("emotion_tags", "")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        for tag in tags:
            emotion_counter[tag] = emotion_counter.get(tag, 0) + 1
            if tag not in VALID_EMOTIONS:
                warnings.append(f"{line_label}: 未定義の感情タグ '{tag}'")

        # テキスト長チェック
        text = entry.get("text_raw", "")
        if len(text) > 60:
            warnings.append(f"{line_label}: テキストが長い ({len(text)}文字): {text[:40]}...")
        if len(text) < 3:
            warnings.append(f"{line_label}: テキストが短すぎ ({len(text)}文字)")

        # emoji_suggestion チェック
        emoji = entry.get("emoji_suggestion", "")
        if emoji and text not in emoji:
            warnings.append(f"{line_label}: emoji_suggestion にテキストが含まれていません")

    # レポート
    print(f"\n{'='*50}")
    print(f"バリデーション結果: {response_path.name}")
    print(f"{'='*50}")
    print(f"  総行数: {len(data)}")
    print(f"  シーン数: {len(scenes)}")
    print(f"  エラー: {len(errors)}件")
    print(f"  警告: {len(warnings)}件")

    emoji_filled = sum(1 for e in data if e.get("emoji_suggestion", "").strip())
    print(f"  emoji_suggestion 記入率: {emoji_filled}/{len(data)} ({emoji_filled/len(data)*100:.0f}%)")

    if errors:
        print(f"\n[エラー]")
        for e in errors[:10]:
            print(f"  ❌ {e}")
        if len(errors) > 10:
            print(f"  ... 他 {len(errors)-10} 件")

    if warnings:
        print(f"\n[警告]")
        for w in warnings[:15]:
            print(f"  ⚠️  {w}")
        if len(warnings) > 15:
            print(f"  ... 他 {len(warnings)-15} 件")

    # 感情タグ分布
    print(f"\n  感情タグ TOP10:")
    sorted_emotions = sorted(emotion_counter.items(), key=lambda x: -x[1])
    for tag, count in sorted_emotions[:10]:
        marker = "" if tag in VALID_EMOTIONS else " ⚠️未定義"
        print(f"    {tag}: {count}回{marker}")

    is_valid = len(errors) == 0
    print(f"\n{'✅ バリデーション通過' if is_valid else '❌ エラーあり — 修正が必要です'}")

    return {
        "valid": is_valid,
        "total": len(data),
        "scenes": len(scenes),
        "errors": len(errors),
        "warnings": len(warnings),
        "emoji_fill_rate": emoji_filled / len(data) if data else 0,
    }


# ============================================================
# 4. process: response.json → production.csv → キャプション適用
# ============================================================
def process_response(project_name: str, num_candidates: int = 1) -> None:
    """Grok出力をパイプラインに通してproduction.csvを生成する

    処理フロー:
      1. grok/response.json → script_raw.json にコピー
      2. script_processor.py で production.csv を生成
      3. captions.json が存在すればキャプション自動適用
    """
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"

    # レスポンスファイルを探す
    response_path = grok_dir / "response.json"
    if not response_path.exists():
        alt_path = project_dir / "script_raw_grok.json"
        if alt_path.exists():
            response_path = alt_path
        else:
            print(f"[error] Grok出力が見つかりません")
            return

    # バリデーション
    result = validate_response(project_name)
    if not result.get("valid"):
        print(f"\n[abort] バリデーションエラーのため処理を中止します")
        return

    # script_raw.json にコピー（script_processor が読む標準パス）
    dest = project_dir / "script_raw.json"
    shutil.copy2(response_path, dest)
    print(f"\n[ok] {response_path.name} → script_raw.json コピー")

    # script_processor.py で production.csv 生成
    sys.path.insert(0, str(AGENTS_DIR))
    from script_processor import process_script
    csv_path = process_script(project_name)

    if not csv_path:
        print(f"[error] production.csv の生成に失敗しました")
        return

    # キャプション自動適用
    captions_path = project_dir / "captions.json"
    if captions_path.exists():
        _apply_captions(project_dir, captions_path, num_candidates)
    else:
        print(f"\n[info] captions.json が無いため、キャプションは未設定です")
        print(f"  casting.py または手動で設定してください")

    print(f"\n{'='*50}")
    print(f"パイプライン処理完了！")
    print(f"  production.csv: {project_dir / 'production.csv'}")
    print(f"\n次のステップ:")
    print(f"  python recorder.py {project_name}  -- 音声生成")


def _apply_captions(project_dir: Path, captions_path: Path, num_candidates: int = 1) -> None:
    """captions.json の intensity_profiles を production.csv に適用する"""
    with open(captions_path, "r", encoding="utf-8") as f:
        captions = json.load(f)

    profiles = captions.get("intensity_profiles", {})
    if not profiles:
        print(f"[warn] captions.json に intensity_profiles がありません")
        return

    prod_csv = project_dir / "production.csv"
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    stats = {}
    for row in rows:
        notes = row.get("notes", "")
        m = re.search(r"intensity=(\w+)", notes)
        intensity = m.group(1) if m else "medium"

        profile = profiles.get(intensity, profiles.get("medium", {}))
        row["caption"] = profile.get("caption", "")
        row["cfg_text"] = str(profile.get("cfg_text", 3.0))
        row["cfg_caption"] = str(profile.get("cfg_caption", 3.0))
        row["cfg_speaker"] = str(profile.get("cfg_speaker", 5.0))
        row["num_steps"] = str(profile.get("num_steps", 30))
        row["num_candidates"] = str(num_candidates)

        stats[intensity] = stats.get(intensity, 0) + 1

    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[ok] キャプション適用: {len(rows)}行")
    for k, v in sorted(stats.items()):
        p = profiles.get(k, {})
        print(f"  {k}: {v}行 (cfg_text={p.get('cfg_text')}, cfg_caption={p.get('cfg_caption')})")
    print(f"  num_candidates={num_candidates}")


# ============================================================
# 5. status: プロジェクトの Grok ワークフロー進捗
# ============================================================
def show_status(project_name: str) -> None:
    """Grokワークフローの進捗を表示する"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"

    print(f"\n{'='*50}")
    print(f"Grokワークフロー状況: {project_name}")
    print(f"{'='*50}")

    checks = [
        ("grok/フォルダ", grok_dir.exists()),
        ("grok/prompt.md (指示書)", (grok_dir / "prompt.md").exists() or (project_dir / "grok_prompt.md").exists()),
        ("grok/response.json", _check_response(grok_dir / "response.json") or _check_response(project_dir / "script_raw_grok.json")),
        ("production.csv", (project_dir / "production.csv").exists()),
        ("captions.json", (project_dir / "captions.json").exists()),
    ]

    for label, ok in checks:
        status = "✅" if ok else "⬜"
        print(f"  {status} {label}")

    # production.csv の状態
    prod_csv = project_dir / "production.csv"
    if prod_csv.exists():
        with open(prod_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        status_counts = {}
        for r in rows:
            s = r.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        print(f"\n  production.csv 行数: {len(rows)}")
        for s, c in sorted(status_counts.items()):
            print(f"    {s}: {c}行")

    # audio フォルダチェック
    for audio_name in ["audio", "audio_grok", "audio_agent"]:
        audio_dir = project_dir / audio_name
        if audio_dir.exists():
            wav_count = len(list(audio_dir.rglob("*.wav")))
            print(f"\n  {audio_name}/: {wav_count} wavファイル")


def _check_response(path: Path) -> bool:
    """レスポンスファイルが存在し、空でないか"""
    if not path.exists():
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return isinstance(data, list) and len(data) > 0
    except Exception:
        return False


# ============================================================
# CLI
# ============================================================
USAGE = """Grok Bridge - Grok↔パイプライン ワークフロー管理

Usage:
  python grok_bridge.py init     <project>                    -- grok/フォルダ初期化
  python grok_bridge.py prepare  <project>                    -- 指示書生成 (project_brief.json → grok/prompt.md)
  python grok_bridge.py validate <project>                    -- Grok出力バリデーション
  python grok_bridge.py process  <project> [--candidates N]   -- パイプライン処理 (response.json → production.csv)
  python grok_bridge.py status   <project>                    -- 進捗確認

標準ワークフロー:
  1. init     → grok/ フォルダとテンプレートを配置
  2. prepare  → project_brief.json から指示書を生成 (または手動で grok/prompt.md を作成)
  3. (人間)   → Grokに指示書を渡し、JSON出力を grok/response.json に保存
  4. validate → JSONのバリデーション
  5. process  → production.csv 生成 + キャプション適用
  6. (収録)   → python recorder.py <project> で音声生成
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]

    if cmd == "init":
        init_grok_workspace(project_name)
    elif cmd == "prepare":
        prepare_prompt(project_name)
    elif cmd == "validate":
        validate_response(project_name)
    elif cmd == "process":
        num_candidates = 3
        if "--candidates" in sys.argv:
            idx = sys.argv.index("--candidates")
            if idx + 1 < len(sys.argv):
                num_candidates = int(sys.argv[idx + 1])
        process_response(project_name, num_candidates=num_candidates)
    elif cmd == "status":
        show_status(project_name)
    else:
        print(f"Unknown command: {cmd}")
        print(USAGE)
        sys.exit(1)
