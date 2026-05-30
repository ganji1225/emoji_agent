#!/usr/bin/env python3
"""謇ｿ隱榊呵｣懆ｨｭ螳壹せ繧ｯ繝ｪ繝励ヨ - approvals_template.json 繧・production.csv 縺ｫ蜿肴丐縺吶ｋ

菴ｿ縺・婿:
  python approve.py <project_name>
  python approve.py <project_name> --json path/to/approvals.json

approvals_template.json 縺ｮ蠖｢蠑・
  {
    "s1_ev3/line_001": 2,
    "s1_ev3/line_002": 1,
    ...
  }
  窶ｻ 繧ｭ繝ｼ縺ｯ "scene_id/line_id"縲∝､縺ｯ蛟呵｣懃分蜿ｷ・・蟋九∪繧翫・謨ｴ謨ｰ・・"""
import csv
import json
import sys
from pathlib import Path

import os
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")


def apply_approvals(project_name: str, json_path: Path) -> None:
    csv_path = PROJECTS_DIR / project_name / "production.csv"

    if not csv_path.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {csv_path}")
        sys.exit(1)

    # 謇ｿ隱巷SON繧定ｪｭ縺ｿ霎ｼ繧
    approvals: dict = json.loads(json_path.read_text(encoding="utf-8"))
    if not approvals:
        print("[warn] approvals_template.json 縺檎ｩｺ縺ｧ縺吶ょ・逅・ｒ荳ｭ譁ｭ縺励∪縺吶・)
        sys.exit(0)

    # production.csv 繧定ｪｭ縺ｿ霎ｼ繧
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    fieldnames = list(rows[0].keys())

    # 繧ｭ繝ｼ "scene_id/line_id" 竊・row 縺ｮ繝槭ャ繝励ｒ菴懈・
    row_map: dict = {f"{r['scene_id']}/{r['line_id']}": r for r in rows}

    print(f"=== approve.py ===")
    print(f"繝励Ο繧ｸ繧ｧ繧ｯ繝・ {project_name}")
    print(f"謇ｿ隱巷SON: {json_path}")
    print(f"謇ｿ隱榊ｯｾ雎｡: {len(approvals)}陦・)
    print()

    updated = 0
    skipped = 0
    not_found = []

    for key, candidate in approvals.items():
        if key not in row_map:
            not_found.append(key)
            skipped += 1
            continue

        row = row_map[key]
        row["approved_candidate"] = str(int(candidate))
        row["status"] = "approved"
        updated += 1
        print(f"  [OK] {key} 竊・蛟呵｣悳candidate}")

    # production.csv 繧呈嶌縺肴綾縺呻ｼ・tf-8-sig 繧堤ｶｭ謖・ｼ・    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"{'='*50}")
    print(f"謇ｿ隱崎ｨｭ螳壼ｮ御ｺ・ｼ・)
    print(f"  譖ｴ譁ｰ: {updated}陦・)
    if skipped:
        print(f"  繧ｹ繧ｭ繝・・・郁ｦ九▽縺九ｉ縺夲ｼ・ {skipped}陦・)
        for k in not_found:
            print(f"    - {k}")
    print(f"  production.csv: {csv_path}")
    print()
    print(f"谺｡縺ｮ繧ｹ繝・ャ繝・")
    print(f"  python E:/irodori/agents/ma_agent.py {project_name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python approve.py <project_name> [--json path/to/approvals.json]")
        sys.exit(1)

    project_name = sys.argv[1]

    # --json 繧ｪ繝励す繝ｧ繝ｳ縺ｮ隗｣譫・    json_path = None
    if "--json" in sys.argv:
        idx = sys.argv.index("--json")
        if idx + 1 < len(sys.argv):
            json_path = Path(sys.argv[idx + 1])
        else:
            print("[error] --json 縺ｮ蠕後↓繝代せ繧呈欠螳壹＠縺ｦ縺上□縺輔＞")
            sys.exit(1)
    else:
        json_path = PROJECTS_DIR / project_name / "approvals_template.json"

    if not json_path.exists():
        print(f"[error] 謇ｿ隱巷SON縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {json_path}")
        print(f"  蜈医↓ qc-reviewer 繧貞ｮ溯｡後＠縺ｦ approvals_template.json 繧堤函謌舌＠縺ｦ縺上□縺輔＞縲・)
        sys.exit(1)

    apply_approvals(project_name, json_path)


if __name__ == "__main__":
    main()
