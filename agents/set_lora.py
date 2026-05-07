#!/usr/bin/env python3
"""LoRA 設定スクリプト - production.csv の lora_path / lora_scale 列を一括設定する

使い方:
  # 全行に適用
  python set_lora.py <project_name> --lora <lora_name_or_path> [--scale 1.0]

  # 特定シーンだけ適用
  python set_lora.py <project_name> --lora <lora_name_or_path> --scenes scene_01,scene_02

  # 特定 status の行だけ適用（デフォルトは全 status 対象）
  python set_lora.py <project_name> --lora <lora_name_or_path> --status pending

  # クリア（LoRA 解除）
  python set_lora.py <project_name> --clear
  python set_lora.py <project_name> --clear --scenes scene_01

  # 現在の設定を確認
  python set_lora.py <project_name> --show

LoRA 名の解決ルール:
  1. 絶対パス（D:/... または C:/...）→ そのまま
  2. ディレクトリが存在する相対パス → 絶対パスに変換
  3. それ以外 → 'D:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema' を試す
"""
import csv
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("D:/irodori/projects")
LORA_BASE_DIR = Path("D:/irodori/emoji/lora")


def resolve_lora_path(lora_arg: str) -> str:
    """LoRA 引数を絶対パスに解決する"""
    p = Path(lora_arg)

    # 絶対パスならそのまま
    if p.is_absolute() and p.exists():
        return str(p).replace("\\", "/")

    # 相対パスでも存在すれば絶対化
    if p.exists():
        return str(p.resolve()).replace("\\", "/")

    # デフォルト探索: D:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema
    candidate = LORA_BASE_DIR / lora_arg / "lora_checkpoint_final_ema"
    if candidate.exists():
        return str(candidate).replace("\\", "/")

    # 名前だけ指定で final_ema を探す
    candidate2 = LORA_BASE_DIR / lora_arg
    if candidate2.exists() and (candidate2 / "lora_checkpoint_final_ema").exists():
        return str(candidate2 / "lora_checkpoint_final_ema").replace("\\", "/")

    print(f"[error] LoRA が見つかりません: {lora_arg}")
    print(f"  試したパス:")
    print(f"    {p}")
    print(f"    {candidate}")
    sys.exit(1)


def show_settings(project_name: str) -> None:
    """現在の LoRA 設定状況を表示"""
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    if not csv_path.exists():
        print(f"[error] production.csv が見つかりません: {csv_path}")
        sys.exit(1)

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    if not rows:
        print("[info] production.csv が空です")
        return

    has_lora_field = "lora_path" in rows[0]
    if not has_lora_field:
        print("[warn] このプロジェクトの production.csv には lora_path 列がありません")
        print("       grok_bridge process を再実行すると追加されます")
        return

    # 集計
    from collections import Counter
    lora_counter: Counter = Counter()
    scenes_with_lora: dict = {}
    for r in rows:
        lp = (r.get("lora_path") or "").strip()
        ls = (r.get("lora_scale") or "").strip()
        key = f"{lp}|scale={ls}" if lp else "(none)"
        lora_counter[key] += 1
        if lp:
            scenes_with_lora.setdefault(r["scene_id"], []).append(r["line_id"])

    print(f"=== LoRA 設定状況 ({project_name}) ===")
    print(f"全行数: {len(rows)}")
    for key, count in lora_counter.most_common():
        print(f"  {count}行: {key}")
    if scenes_with_lora:
        print()
        print(f"LoRA 適用シーン:")
        for s, lines in sorted(scenes_with_lora.items()):
            print(f"  {s}: {len(lines)}行")


def apply_settings(
    project_name: str,
    lora_path: str | None,
    lora_scale: float,
    target_scenes: set | None,
    target_status: str | None,
    clear: bool,
) -> None:
    """LoRA 設定を一括適用する"""
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    if not csv_path.exists():
        print(f"[error] production.csv が見つかりません: {csv_path}")
        sys.exit(1)

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    if not rows:
        print("[error] production.csv が空です")
        sys.exit(1)

    fieldnames = list(rows[0].keys())

    # lora_path / lora_scale 列が無い場合は追加
    if "lora_path" not in fieldnames:
        # 適切な位置（seed の後）に挿入
        if "seed" in fieldnames:
            idx = fieldnames.index("seed") + 1
            fieldnames.insert(idx, "lora_path")
            fieldnames.insert(idx + 1, "lora_scale")
        else:
            fieldnames.append("lora_path")
            fieldnames.append("lora_scale")
        for r in rows:
            r.setdefault("lora_path", "")
            r.setdefault("lora_scale", "")
        print(f"[info] lora_path / lora_scale 列を追加しました")

    # 適用
    updated = 0
    skipped = 0
    for r in rows:
        # シーン絞り込み
        if target_scenes is not None and r["scene_id"] not in target_scenes:
            skipped += 1
            continue
        # ステータス絞り込み
        if target_status is not None and r.get("status") != target_status:
            skipped += 1
            continue

        if clear:
            r["lora_path"] = ""
            r["lora_scale"] = ""
        else:
            r["lora_path"] = lora_path or ""
            r["lora_scale"] = str(lora_scale) if lora_path else ""
        updated += 1

    # 書き戻し
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    action = "クリア" if clear else "設定"
    print(f"=== LoRA {action} 完了 ===")
    print(f"  更新: {updated}行 / スキップ: {skipped}行")
    if not clear:
        print(f"  lora_path: {lora_path}")
        print(f"  lora_scale: {lora_scale}")
    if target_scenes:
        print(f"  対象シーン: {sorted(target_scenes)}")
    if target_status:
        print(f"  対象 status: {target_status}")
    print()
    print(f"次のステップ:")
    print(f"  python D:/irodori/agents/recorder.py {project_name}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_name = sys.argv[1]
    args = sys.argv[2:]

    # --show で確認
    if "--show" in args:
        show_settings(project_name)
        return

    # 引数解析
    clear = "--clear" in args
    lora_arg = None
    scale = 1.0
    target_scenes = None
    target_status = None

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--lora" and i + 1 < len(args):
            lora_arg = args[i + 1]
            i += 2
        elif a == "--scale" and i + 1 < len(args):
            scale = float(args[i + 1])
            i += 2
        elif a == "--scenes" and i + 1 < len(args):
            target_scenes = {s.strip() for s in args[i + 1].split(",") if s.strip()}
            i += 2
        elif a == "--status" and i + 1 < len(args):
            target_status = args[i + 1].strip()
            i += 2
        elif a == "--clear":
            i += 1
        else:
            i += 1

    # バリデーション
    if not clear and not lora_arg:
        print("[error] --lora または --clear のどちらかを指定してください")
        print("使い方: python set_lora.py <project_name> --lora <name> [--scale 1.0]")
        sys.exit(1)

    # LoRA パス解決
    lora_path = None
    if not clear:
        lora_path = resolve_lora_path(lora_arg)
        print(f"[info] LoRA path: {lora_path}")

    apply_settings(
        project_name=project_name,
        lora_path=lora_path,
        lora_scale=scale,
        target_scenes=target_scenes,
        target_status=target_status,
        clear=clear,
    )


if __name__ == "__main__":
    main()
