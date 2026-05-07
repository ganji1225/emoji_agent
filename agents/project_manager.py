#!/usr/bin/env python3
"""プロジェクト管理エージェント - フォルダ構造の初期化と進捗管理"""
import json
import csv
import sys
from pathlib import Path

PROJECTS_DIR = Path("D:/irodori/projects")
PRODUCTION_CSV_COLUMNS = [
    "scene_id", "line_id", "speaker", "emotion_note",
    "text_raw", "text_with_emoji", "caption",
    "cfg_text", "cfg_caption", "cfg_speaker", "num_steps",
    "num_candidates", "seed", "status", "approved_candidate", "notes"
]


def init_project(project_name: str) -> Path:
    """プロジェクトフォルダを初期化する"""
    project_dir = PROJECTS_DIR / project_name
    if project_dir.exists():
        print(f"[warn] プロジェクト '{project_name}' は既に存在します: {project_dir}")
        return project_dir

    # フォルダ構造を作成
    dirs = [
        project_dir,
        project_dir / "audio",
        project_dir / "approved",
        project_dir / "master",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 空の production.csv をヘッダー付きで作成
    csv_path = project_dir / "production.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(PRODUCTION_CSV_COLUMNS)

    # デフォルトキャプションライブラリをコピー
    captions_path = project_dir / "captions.json"
    default_captions = Path(__file__).parent / "default_captions.json"
    if default_captions.exists():
        with open(default_captions, "r", encoding="utf-8") as f:
            captions_data = json.load(f)
        # scene_mapping は空で初期化（プロジェクトごとに設定）
        captions_data["scene_mapping"] = {}
        # _comment, _updated は除去
        captions_data.pop("_comment", None)
        captions_data.pop("_updated", None)
    else:
        captions_data = {
            "profiles": {
                "日常会話": {
                    "caption": "若い女性が、リラックスした自然な口調で、明るく話している。",
                    "cfg_text": 3.0, "cfg_caption": 3.0, "cfg_speaker": 5.0, "num_steps": 40
                }
            },
            "scene_mapping": {}
        }
    with open(captions_path, "w", encoding="utf-8") as f:
        json.dump(captions_data, f, ensure_ascii=False, indent=2)

    print(f"[ok] プロジェクト '{project_name}' を作成しました")
    print(f"  フォルダ: {project_dir}")
    print(f"  production.csv: {csv_path}")
    print(f"  captions.json: {captions_path}")
    return project_dir


def show_progress(project_name: str) -> dict:
    """プロジェクトの進捗を表示する"""
    project_dir = PROJECTS_DIR / project_name
    csv_path = project_dir / "production.csv"

    if not csv_path.exists():
        print(f"[error] production.csv が見つかりません: {csv_path}")
        return {}

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)
    if total == 0:
        print("[info] production.csv にデータがありません")
        return {"total": 0}

    status_counts = {}
    for row in rows:
        s = row.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    scenes = sorted(set(row.get("scene_id", "") for row in rows))

    print(f"=== プロジェクト '{project_name}' 進捗 ===")
    print(f"総セリフ数: {total}")
    print(f"シーン数: {len(scenes)} ({', '.join(scenes)})")
    print(f"ステータス別:")
    for status, count in sorted(status_counts.items()):
        pct = count / total * 100
        print(f"  {status}: {count}/{total} ({pct:.0f}%)")

    return {"total": total, "scenes": scenes, "status_counts": status_counts}


def list_projects() -> list[str]:
    """既存プロジェクト一覧を表示する"""
    if not PROJECTS_DIR.exists():
        print("[info] プロジェクトフォルダが存在しません")
        return []

    projects = [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]
    if not projects:
        print("[info] プロジェクトはまだありません")
    else:
        print(f"=== プロジェクト一覧 ({len(projects)}件) ===")
        for p in sorted(projects):
            csv_path = PROJECTS_DIR / p / "production.csv"
            status = "✅" if csv_path.exists() else "⚠️"
            print(f"  {status} {p}")
    return projects


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python project_manager.py init <project_name>")
        print("  python project_manager.py progress <project_name>")
        print("  python project_manager.py list")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        init_project(sys.argv[2])
    elif cmd == "progress":
        show_progress(sys.argv[2])
    elif cmd == "list":
        list_projects()
    else:
        print(f"Unknown command: {cmd}")
