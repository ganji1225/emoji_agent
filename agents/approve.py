#!/usr/bin/env python3
"""承認候補設定スクリプト - approvals_template.json を production.csv に反映する

使い方:
  python approve.py <project_name>
  python approve.py <project_name> --json path/to/approvals.json

approvals_template.json の形式:
  {
    "s1_ev3/line_001": 2,
    "s1_ev3/line_002": 1,
    ...
  }
  ※ キーは "scene_id/line_id"、値は候補番号（1始まりの整数）
"""
import csv
import json
import sys
from pathlib import Path

import os
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("D:/irodori/projects")


def apply_approvals(project_name: str, json_path: Path) -> None:
    csv_path = PROJECTS_DIR / project_name / "production.csv"

    if not csv_path.exists():
        print(f"[error] production.csv が見つかりません: {csv_path}")
        sys.exit(1)

    # 承認JSONを読み込む
    approvals: dict = json.loads(json_path.read_text(encoding="utf-8"))
    if not approvals:
        print("[warn] approvals_template.json が空です。処理を中断します。")
        sys.exit(0)

    # production.csv を読み込む
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    fieldnames = list(rows[0].keys())

    # キー "scene_id/line_id" → row のマップを作成
    row_map: dict = {f"{r['scene_id']}/{r['line_id']}": r for r in rows}

    print(f"=== approve.py ===")
    print(f"プロジェクト: {project_name}")
    print(f"承認JSON: {json_path}")
    print(f"承認対象: {len(approvals)}行")
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
        print(f"  [OK] {key} → 候補{candidate}")

    # production.csv を書き戻す（utf-8-sig を維持）
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"{'='*50}")
    print(f"承認設定完了！")
    print(f"  更新: {updated}行")
    if skipped:
        print(f"  スキップ（見つからず）: {skipped}行")
        for k in not_found:
            print(f"    - {k}")
    print(f"  production.csv: {csv_path}")
    print()
    print(f"次のステップ:")
    print(f"  python D:/irodori/agents/ma_agent.py {project_name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python approve.py <project_name> [--json path/to/approvals.json]")
        sys.exit(1)

    project_name = sys.argv[1]

    # --json オプションの解析
    json_path = None
    if "--json" in sys.argv:
        idx = sys.argv.index("--json")
        if idx + 1 < len(sys.argv):
            json_path = Path(sys.argv[idx + 1])
        else:
            print("[error] --json の後にパスを指定してください")
            sys.exit(1)
    else:
        json_path = PROJECTS_DIR / project_name / "approvals_template.json"

    if not json_path.exists():
        print(f"[error] 承認JSONが見つかりません: {json_path}")
        print(f"  先に qc-reviewer を実行して approvals_template.json を生成してください。")
        sys.exit(1)

    apply_approvals(project_name, json_path)


if __name__ == "__main__":
    main()
