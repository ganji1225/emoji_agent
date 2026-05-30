#!/usr/bin/env python3
"""LoRA 險ｭ螳壹せ繧ｯ繝ｪ繝励ヨ - production.csv 縺ｮ lora_path / lora_scale 蛻励ｒ荳諡ｬ險ｭ螳壹☆繧・
菴ｿ縺・婿:
  # 蜈ｨ陦後↓驕ｩ逕ｨ
  python set_lora.py <project_name> --lora <lora_name_or_path> [--scale 1.0]

  # 迚ｹ螳壹す繝ｼ繝ｳ縺縺鷹←逕ｨ
  python set_lora.py <project_name> --lora <lora_name_or_path> --scenes scene_01,scene_02

  # 迚ｹ螳・status 縺ｮ陦後□縺鷹←逕ｨ・医ョ繝輔か繝ｫ繝医・蜈ｨ status 蟇ｾ雎｡・・  python set_lora.py <project_name> --lora <lora_name_or_path> --status pending

  # 繧ｯ繝ｪ繧｢・・oRA 隗｣髯､・・  python set_lora.py <project_name> --clear
  python set_lora.py <project_name> --clear --scenes scene_01

  # 迴ｾ蝨ｨ縺ｮ險ｭ螳壹ｒ遒ｺ隱・  python set_lora.py <project_name> --show

LoRA 蜷阪・隗｣豎ｺ繝ｫ繝ｼ繝ｫ:
  1. 邨ｶ蟇ｾ繝代せ・・:/... 縺ｾ縺溘・ C:/...・俄・ 縺昴・縺ｾ縺ｾ
  2. 繝・ぅ繝ｬ繧ｯ繝医Μ縺悟ｭ伜惠縺吶ｋ逶ｸ蟇ｾ繝代せ 竊・邨ｶ蟇ｾ繝代せ縺ｫ螟画鋤
  3. 縺昴ｌ莉･螟・竊・'E:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema' 繧定ｩｦ縺・"""
import csv
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")
LORA_BASE_DIR = Path("E:/irodori/emoji/lora")


def resolve_lora_path(lora_arg: str) -> str:
    """LoRA 蠑墓焚繧堤ｵｶ蟇ｾ繝代せ縺ｫ隗｣豎ｺ縺吶ｋ"""
    p = Path(lora_arg)

    # 邨ｶ蟇ｾ繝代せ縺ｪ繧峨◎縺ｮ縺ｾ縺ｾ
    if p.is_absolute() and p.exists():
        return str(p).replace("\\", "/")

    # 逶ｸ蟇ｾ繝代せ縺ｧ繧ょｭ伜惠縺吶ｌ縺ｰ邨ｶ蟇ｾ蛹・    if p.exists():
        return str(p.resolve()).replace("\\", "/")

    # 繝・ヵ繧ｩ繝ｫ繝域爾邏｢: E:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema
    candidate = LORA_BASE_DIR / lora_arg / "lora_checkpoint_final_ema"
    if candidate.exists():
        return str(candidate).replace("\\", "/")

    # 蜷榊燕縺縺第欠螳壹〒 final_ema 繧呈爾縺・    candidate2 = LORA_BASE_DIR / lora_arg
    if candidate2.exists() and (candidate2 / "lora_checkpoint_final_ema").exists():
        return str(candidate2 / "lora_checkpoint_final_ema").replace("\\", "/")

    print(f"[error] LoRA 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {lora_arg}")
    print(f"  隧ｦ縺励◆繝代せ:")
    print(f"    {p}")
    print(f"    {candidate}")
    sys.exit(1)


def show_settings(project_name: str) -> None:
    """迴ｾ蝨ｨ縺ｮ LoRA 險ｭ螳夂憾豕√ｒ陦ｨ遉ｺ"""
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    if not csv_path.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {csv_path}")
        sys.exit(1)

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    if not rows:
        print("[info] production.csv 縺檎ｩｺ縺ｧ縺・)
        return

    has_lora_field = "lora_path" in rows[0]
    if not has_lora_field:
        print("[warn] 縺薙・繝励Ο繧ｸ繧ｧ繧ｯ繝医・ production.csv 縺ｫ縺ｯ lora_path 蛻励′縺ゅｊ縺ｾ縺帙ｓ")
        print("       grok_bridge process 繧貞・螳溯｡後☆繧九→霑ｽ蜉縺輔ｌ縺ｾ縺・)
        return

    # 髮・ｨ・    from collections import Counter
    lora_counter: Counter = Counter()
    scenes_with_lora: dict = {}
    for r in rows:
        lp = (r.get("lora_path") or "").strip()
        ls = (r.get("lora_scale") or "").strip()
        key = f"{lp}|scale={ls}" if lp else "(none)"
        lora_counter[key] += 1
        if lp:
            scenes_with_lora.setdefault(r["scene_id"], []).append(r["line_id"])

    print(f"=== LoRA 險ｭ螳夂憾豕・({project_name}) ===")
    print(f"蜈ｨ陦梧焚: {len(rows)}")
    for key, count in lora_counter.most_common():
        print(f"  {count}陦・ {key}")
    if scenes_with_lora:
        print()
        print(f"LoRA 驕ｩ逕ｨ繧ｷ繝ｼ繝ｳ:")
        for s, lines in sorted(scenes_with_lora.items()):
            print(f"  {s}: {len(lines)}陦・)


def apply_settings(
    project_name: str,
    lora_path: str | None,
    lora_scale: float,
    target_scenes: set | None,
    target_status: str | None,
    clear: bool,
) -> None:
    """LoRA 險ｭ螳壹ｒ荳諡ｬ驕ｩ逕ｨ縺吶ｋ"""
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    if not csv_path.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {csv_path}")
        sys.exit(1)

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    if not rows:
        print("[error] production.csv 縺檎ｩｺ縺ｧ縺・)
        sys.exit(1)

    fieldnames = list(rows[0].keys())

    # lora_path / lora_scale 蛻励′辟｡縺・ｴ蜷医・霑ｽ蜉
    if "lora_path" not in fieldnames:
        # 驕ｩ蛻・↑菴咲ｽｮ・・eed 縺ｮ蠕鯉ｼ峨↓謖ｿ蜈･
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
        print(f"[info] lora_path / lora_scale 蛻励ｒ霑ｽ蜉縺励∪縺励◆")

    # 驕ｩ逕ｨ
    updated = 0
    skipped = 0
    for r in rows:
        # 繧ｷ繝ｼ繝ｳ邨槭ｊ霎ｼ縺ｿ
        if target_scenes is not None and r["scene_id"] not in target_scenes:
            skipped += 1
            continue
        # 繧ｹ繝・・繧ｿ繧ｹ邨槭ｊ霎ｼ縺ｿ
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

    # 譖ｸ縺肴綾縺・    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    action = "繧ｯ繝ｪ繧｢" if clear else "險ｭ螳・
    print(f"=== LoRA {action} 螳御ｺ・===")
    print(f"  譖ｴ譁ｰ: {updated}陦・/ 繧ｹ繧ｭ繝・・: {skipped}陦・)
    if not clear:
        print(f"  lora_path: {lora_path}")
        print(f"  lora_scale: {lora_scale}")
    if target_scenes:
        print(f"  蟇ｾ雎｡繧ｷ繝ｼ繝ｳ: {sorted(target_scenes)}")
    if target_status:
        print(f"  蟇ｾ雎｡ status: {target_status}")
    print()
    print(f"谺｡縺ｮ繧ｹ繝・ャ繝・")
    print(f"  python E:/irodori/agents/recorder.py {project_name}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_name = sys.argv[1]
    args = sys.argv[2:]

    # --show 縺ｧ遒ｺ隱・    if "--show" in args:
        show_settings(project_name)
        return

    # 蠑墓焚隗｣譫・    clear = "--clear" in args
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

    # 繝舌Μ繝・・繧ｷ繝ｧ繝ｳ
    if not clear and not lora_arg:
        print("[error] --lora 縺ｾ縺溘・ --clear 縺ｮ縺ｩ縺｡繧峨°繧呈欠螳壹＠縺ｦ縺上□縺輔＞")
        print("菴ｿ縺・婿: python set_lora.py <project_name> --lora <name> [--scale 1.0]")
        sys.exit(1)

    # LoRA 繝代せ隗｣豎ｺ
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
