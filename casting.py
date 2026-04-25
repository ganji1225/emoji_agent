#!/usr/bin/env python3
"""キャスティングエージェント - シーンごとのキャプション（声質）設定"""
import csv
import json
import sys
from pathlib import Path

PROJECTS_DIR = Path("D:/irodori/projects")


def apply_captions(project_name: str) -> str:
    """captions.json の scene_mapping に基づいて production.csv の caption/cfg列を設定する"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    captions_json = project_dir / "captions.json"

    if not prod_csv.exists():
        print(f"[error] production.csv が見つかりません: {prod_csv}")
        return ""
    if not captions_json.exists():
        print(f"[error] captions.json が見つかりません: {captions_json}")
        return ""

    # captions.json 読み込み
    with open(captions_json, "r", encoding="utf-8") as f:
        captions_data = json.load(f)

    profiles = captions_data.get("profiles", {})
    scene_mapping = captions_data.get("scene_mapping", {})

    if not scene_mapping:
        print("[warn] scene_mapping が空です。captions.json を編集してください。")
        print("  利用可能なプロファイル:")
        for name, prof in profiles.items():
            print(f"    - {name}: {prof['caption'][:40]}...")
        return ""

    # production.csv 読み込み
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # caption/cfg列を設定
    updated_count = 0
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
            # LoRA はプロファイルで指定された場合のみ書き込む（指定なしは空のまま）
            if "lora_path" in prof:
                row["lora_path"] = prof.get("lora_path", "")
                row["lora_scale"] = str(prof.get("lora_scale", 1.0)) if prof.get("lora_path") else ""
            updated_count += 1
        else:
            if scene_id not in unmapped_scenes:
                unmapped_scenes.add(scene_id)

    # 書き戻し
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[ok] キャプションを適用しました ({updated_count}/{len(rows)}行)")
    if unmapped_scenes:
        print(f"[warn] マッピングされていないシーン: {', '.join(sorted(unmapped_scenes))}")
        print("  captions.json の scene_mapping に追加してください。")

    return str(prod_csv)


def show_profiles(project_name: str):
    """利用可能なキャプションプロファイルを表示する"""
    project_dir = PROJECTS_DIR / project_name
    captions_json = project_dir / "captions.json"

    if not captions_json.exists():
        print(f"[error] captions.json が見つかりません")
        return

    with open(captions_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles = data.get("profiles", {})
    mapping = data.get("scene_mapping", {})

    print("=== キャプションプロファイル ===")
    for name, prof in profiles.items():
        print(f"\n[{name}]")
        print(f"  caption: {prof['caption']}")
        print(f"  cfg: text={prof.get('cfg_text', 3.0)} caption={prof.get('cfg_caption', 3.0)} speaker={prof.get('cfg_speaker', 5.0)}")
        print(f"  steps: {prof.get('num_steps', 40)}")

    print(f"\n=== シーンマッピング ===")
    if mapping:
        for scene, profile in sorted(mapping.items()):
            print(f"  {scene} → {profile}")
    else:
        print("  (未設定)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python casting.py apply <project_name>   -- キャプション適用")
        print("  python casting.py show <project_name>     -- プロファイル表示")
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]

    if cmd == "apply":
        apply_captions(project_name)
    elif cmd == "show":
        show_profiles(project_name)
    else:
        print(f"Unknown command: {cmd}")
