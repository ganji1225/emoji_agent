#!/usr/bin/env python3
"""繧ｭ繝｣繧ｹ繝・ぅ繝ｳ繧ｰ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・- 繧ｷ繝ｼ繝ｳ縺斐→縺ｮ繧ｭ繝｣繝励す繝ｧ繝ｳ・亥｣ｰ雉ｪ・芽ｨｭ螳・""
import csv
import json
import sys
from pathlib import Path

PROJECTS_DIR = Path("E:/irodori/projects")


def apply_captions(project_name: str) -> str:
    """captions.json 縺ｮ scene_mapping 縺ｫ蝓ｺ縺･縺・※ production.csv 縺ｮ caption/cfg蛻励ｒ險ｭ螳壹☆繧・""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    captions_json = project_dir / "captions.json"

    if not prod_csv.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {prod_csv}")
        return ""
    if not captions_json.exists():
        print(f"[error] captions.json 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {captions_json}")
        return ""

    # captions.json 隱ｭ縺ｿ霎ｼ縺ｿ
    with open(captions_json, "r", encoding="utf-8") as f:
        captions_data = json.load(f)

    profiles = captions_data.get("profiles", {})
    scene_mapping = captions_data.get("scene_mapping", {})

    if not scene_mapping:
        print("[warn] scene_mapping 縺檎ｩｺ縺ｧ縺吶Ｄaptions.json 繧堤ｷｨ髮・＠縺ｦ縺上□縺輔＞縲・)
        print("  蛻ｩ逕ｨ蜿ｯ閭ｽ縺ｪ繝励Ο繝輔ぃ繧､繝ｫ:")
        for name, prof in profiles.items():
            print(f"    - {name}: {prof['caption'][:40]}...")
        return ""

    # production.csv 隱ｭ縺ｿ霎ｼ縺ｿ
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # caption/cfg蛻励ｒ險ｭ螳・    updated_count = 0
    unmapped_scenes = set()
    for row in rows:
        scene_id = row.get("scene_id", "")
        profile_name = scene_mapping.get(scene_id)

        if profile_name and profile_name in profiles:
            prof = profiles[profile_name]
            row["caption"] = prof.get("caption", "")
            row["cfg_text"] = str(prof.get("cfg_text", 3.0))
            row["cfg_caption"] = str(prof.get("cfg_caption", 3.0))
            row["cfg_speaker"] = str(prof.get("cfg_speaker", 5.0))
            row["cfg_guidance_mode"] = prof.get("cfg_guidance_mode", "alternating")
            row["num_steps"] = str(prof.get("num_steps", 40))
            # LoRA 縺ｯ繝励Ο繝輔ぃ繧､繝ｫ縺ｧ謖・ｮ壹＆繧後◆蝣ｴ蜷医・縺ｿ譖ｸ縺崎ｾｼ繧・域欠螳壹↑縺励・遨ｺ縺ｮ縺ｾ縺ｾ・・            if "lora_path" in prof:
                row["lora_path"] = prof.get("lora_path", "")
                row["lora_scale"] = str(prof.get("lora_scale", 1.0)) if prof.get("lora_path") else ""
            updated_count += 1
        else:
            if scene_id not in unmapped_scenes:
                unmapped_scenes.add(scene_id)

    # 譖ｸ縺肴綾縺・    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[ok] 繧ｭ繝｣繝励す繝ｧ繝ｳ繧帝←逕ｨ縺励∪縺励◆ ({updated_count}/{len(rows)}陦・")
    if unmapped_scenes:
        print(f"[warn] 繝槭ャ繝斐Φ繧ｰ縺輔ｌ縺ｦ縺・↑縺・す繝ｼ繝ｳ: {', '.join(sorted(unmapped_scenes))}")
        print("  captions.json 縺ｮ scene_mapping 縺ｫ霑ｽ蜉縺励※縺上□縺輔＞縲・)

    return str(prod_csv)


def show_profiles(project_name: str):
    """蛻ｩ逕ｨ蜿ｯ閭ｽ縺ｪ繧ｭ繝｣繝励す繝ｧ繝ｳ繝励Ο繝輔ぃ繧､繝ｫ繧定｡ｨ遉ｺ縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    captions_json = project_dir / "captions.json"

    if not captions_json.exists():
        print(f"[error] captions.json 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ")
        return

    with open(captions_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles = data.get("profiles", {})
    mapping = data.get("scene_mapping", {})

    print("=== 繧ｭ繝｣繝励す繝ｧ繝ｳ繝励Ο繝輔ぃ繧､繝ｫ ===")
    for name, prof in profiles.items():
        print(f"\n[{name}]")
        print(f"  caption: {prof['caption']}")
        print(f"  cfg: text={prof.get('cfg_text', 3.0)} caption={prof.get('cfg_caption', 3.0)} speaker={prof.get('cfg_speaker', 5.0)}")
        print(f"  steps: {prof.get('num_steps', 40)}")

    print(f"\n=== 繧ｷ繝ｼ繝ｳ繝槭ャ繝斐Φ繧ｰ ===")
    if mapping:
        for scene, profile in sorted(mapping.items()):
            print(f"  {scene} 竊・{profile}")
    else:
        print("  (譛ｪ險ｭ螳・")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python casting.py apply <project_name>   -- 繧ｭ繝｣繝励す繝ｧ繝ｳ驕ｩ逕ｨ")
        print("  python casting.py show <project_name>     -- 繝励Ο繝輔ぃ繧､繝ｫ陦ｨ遉ｺ")
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]

    if cmd == "apply":
        apply_captions(project_name)
    elif cmd == "show":
        show_profiles(project_name)
    else:
        print(f"Unknown command: {cmd}")
