#!/usr/bin/env python3
"""繝励Ο繧ｸ繧ｧ繧ｯ繝育ｮ｡逅・お繝ｼ繧ｸ繧ｧ繝ｳ繝・- 繝輔か繝ｫ繝讒矩縺ｮ蛻晄悄蛹悶→騾ｲ謐礼ｮ｡逅・""
import json
import csv
import sys
from pathlib import Path

PROJECTS_DIR = Path("E:/irodori/projects")
PRODUCTION_CSV_COLUMNS = [
    "scene_id", "line_id", "speaker", "emotion_note",
    "text_raw", "text_with_emoji", "caption",
    "cfg_text", "cfg_caption", "cfg_speaker", "num_steps",
    "num_candidates", "seed", "status", "approved_candidate", "notes"
]


def init_project(project_name: str) -> Path:
    """繝励Ο繧ｸ繧ｧ繧ｯ繝医ヵ繧ｩ繝ｫ繝繧貞・譛溷喧縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    if project_dir.exists():
        print(f"[warn] 繝励Ο繧ｸ繧ｧ繧ｯ繝・'{project_name}' 縺ｯ譌｢縺ｫ蟄伜惠縺励∪縺・ {project_dir}")
        return project_dir

    # 繝輔か繝ｫ繝讒矩繧剃ｽ懈・
    dirs = [
        project_dir,
        project_dir / "audio",
        project_dir / "approved",
        project_dir / "master",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 遨ｺ縺ｮ production.csv 繧偵・繝・ム繝ｼ莉倥″縺ｧ菴懈・
    csv_path = project_dir / "production.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(PRODUCTION_CSV_COLUMNS)

    # 繝・ヵ繧ｩ繝ｫ繝医く繝｣繝励す繝ｧ繝ｳ繝ｩ繧､繝悶Λ繝ｪ繧偵さ繝斐・
    captions_path = project_dir / "captions.json"
    default_captions = Path(__file__).parent / "default_captions.json"
    if default_captions.exists():
        with open(default_captions, "r", encoding="utf-8") as f:
            captions_data = json.load(f)
        # scene_mapping 縺ｯ遨ｺ縺ｧ蛻晄悄蛹厄ｼ医・繝ｭ繧ｸ繧ｧ繧ｯ繝医＃縺ｨ縺ｫ險ｭ螳夲ｼ・        captions_data["scene_mapping"] = {}
        # _comment, _updated 縺ｯ髯､蜴ｻ
        captions_data.pop("_comment", None)
        captions_data.pop("_updated", None)
    else:
        captions_data = {
            "profiles": {
                "譌･蟶ｸ莨夊ｩｱ": {
                    "caption": "闍･縺・･ｳ諤ｧ縺後√Μ繝ｩ繝・け繧ｹ縺励◆閾ｪ辟ｶ縺ｪ蜿｣隱ｿ縺ｧ縲∵・繧九￥隧ｱ縺励※縺・ｋ縲・,
                    "cfg_text": 3.0, "cfg_caption": 3.0, "cfg_speaker": 5.0, "num_steps": 40
                }
            },
            "scene_mapping": {}
        }
    with open(captions_path, "w", encoding="utf-8") as f:
        json.dump(captions_data, f, ensure_ascii=False, indent=2)

    print(f"[ok] 繝励Ο繧ｸ繧ｧ繧ｯ繝・'{project_name}' 繧剃ｽ懈・縺励∪縺励◆")
    print(f"  繝輔か繝ｫ繝: {project_dir}")
    print(f"  production.csv: {csv_path}")
    print(f"  captions.json: {captions_path}")
    return project_dir


def show_progress(project_name: str) -> dict:
    """繝励Ο繧ｸ繧ｧ繧ｯ繝医・騾ｲ謐励ｒ陦ｨ遉ｺ縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    csv_path = project_dir / "production.csv"

    if not csv_path.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {csv_path}")
        return {}

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)
    if total == 0:
        print("[info] production.csv 縺ｫ繝・・繧ｿ縺後≠繧翫∪縺帙ｓ")
        return {"total": 0}

    status_counts = {}
    for row in rows:
        s = row.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    scenes = sorted(set(row.get("scene_id", "") for row in rows))

    print(f"=== 繝励Ο繧ｸ繧ｧ繧ｯ繝・'{project_name}' 騾ｲ謐・===")
    print(f"邱上そ繝ｪ繝墓焚: {total}")
    print(f"繧ｷ繝ｼ繝ｳ謨ｰ: {len(scenes)} ({', '.join(scenes)})")
    print(f"繧ｹ繝・・繧ｿ繧ｹ蛻･:")
    for status, count in sorted(status_counts.items()):
        pct = count / total * 100
        print(f"  {status}: {count}/{total} ({pct:.0f}%)")

    return {"total": total, "scenes": scenes, "status_counts": status_counts}


def list_projects() -> list[str]:
    """譌｢蟄倥・繝ｭ繧ｸ繧ｧ繧ｯ繝井ｸ隕ｧ繧定｡ｨ遉ｺ縺吶ｋ"""
    if not PROJECTS_DIR.exists():
        print("[info] 繝励Ο繧ｸ繧ｧ繧ｯ繝医ヵ繧ｩ繝ｫ繝縺悟ｭ伜惠縺励∪縺帙ｓ")
        return []

    projects = [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]
    if not projects:
        print("[info] 繝励Ο繧ｸ繧ｧ繧ｯ繝医・縺ｾ縺縺ゅｊ縺ｾ縺帙ｓ")
    else:
        print(f"=== 繝励Ο繧ｸ繧ｧ繧ｯ繝井ｸ隕ｧ ({len(projects)}莉ｶ) ===")
        for p in sorted(projects):
            csv_path = PROJECTS_DIR / p / "production.csv"
            status = "笨・ if csv_path.exists() else "笞・・
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
