#!/usr/bin/env python3
"""蜿朱鹸繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・- production.csv 縺ｫ蝓ｺ縺･縺・※ infer.py 縺ｧ髻ｳ螢ｰ繧剃ｸ諡ｬ逕滓・"""
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")
PYTHON = str(Path("E:/irodori/emoji/.venv/Scripts/python.exe"))
INFER = str(Path("E:/irodori/emoji/infer.py"))

# VoiceDesign 繝｢繝・Ν險ｭ螳・VOICEDESIGN_CONFIG = {
    "hf_checkpoint": "Aratako/Irodori-TTS-500M-v2-VoiceDesign",
    "codec_repo": "Aratako/Semantic-DACVAE-Japanese-32dim",  # 蠢・茨ｼ〕atent_dim=32
}

# v1 繝｢繝・Ν險ｭ螳夲ｼ医Μ繝輔ぃ繝ｬ繝ｳ繧ｹ髻ｳ螢ｰ繝｢繝ｼ繝臥畑・・V1_CONFIG = {
    "hf_checkpoint": "Aratako/Irodori-TTS-500M",
    "codec_repo": "facebook/dacvae-watermarked",  # latent_dim=128
}

MAX_RETRIES = 2
TIMEOUT_SEC = 180


def record_project(project_name: str, model: str = "voicedesign", dry_run: bool = False, audio_subdir: str = "audio") -> dict:
    """production.csv 縺ｮ pending 陦後ｒ鬆・↓髻ｳ螢ｰ逕滓・縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / audio_subdir

    if not prod_csv.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {prod_csv}")
        return {}

    # 繝｢繝・Ν險ｭ螳・    config = VOICEDESIGN_CONFIG if model == "voicedesign" else V1_CONFIG
    print(f"=== 蜿朱鹸繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・===")
    print(f"繝｢繝・Ν: {config['hf_checkpoint']}")
    print(f"繧ｳ繝ｼ繝・ャ繧ｯ: {config['codec_repo']}")
    print()

    # CSV 隱ｭ縺ｿ霎ｼ縺ｿ
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # pending 縺ｮ陦後ｒ謚ｽ蜃ｺ
    pending = [(i, row) for i, row in enumerate(rows) if row.get("status") == "pending"]
    if not pending:
        print("[info] 逕滓・蠕・■縺ｮ陦後′縺ゅｊ縺ｾ縺帙ｓ・亥・縺ｦpending莉･螟厄ｼ・)
        return {"total": 0, "generated": 0}

    print(f"逕滓・蟇ｾ雎｡: {len(pending)}/{len(rows)}陦・)
    if dry_run:
        print("[dry-run] 螳滄圀縺ｮ逕滓・縺ｯ繧ｹ繧ｭ繝・・縺励∪縺・)
        for _, row in pending:
            print(f"  {row['scene_id']}/{row['line_id']}: {row['text_with_emoji'][:40]}")
        return {"total": len(pending), "generated": 0, "dry_run": True}

    generated = 0
    failed = 0
    total_start = time.time()

    for idx, (row_idx, row) in enumerate(pending):
        scene_id = row["scene_id"]
        line_id = row["line_id"]
        text = row["text_with_emoji"]
        caption = row.get("caption", "")
        num_candidates = int(row.get("num_candidates") or 3)
        num_steps = int(row.get("num_steps") or 40)
        cfg_text = float(row.get("cfg_text") or 3.0)
        cfg_caption = float(row.get("cfg_caption") or 3.0)
        cfg_speaker = float(row.get("cfg_speaker") or 5.0)
        cfg_guidance_mode = (row.get("cfg_guidance_mode") or "alternating").strip()
        lora_path = (row.get("lora_path") or "").strip()
        lora_scale_raw = (row.get("lora_scale") or "").strip()
        lora_scale = float(lora_scale_raw) if lora_scale_raw else 1.0
        seed = row.get("seed", "").strip()

        # 蜃ｺ蜉帙ョ繧｣繝ｬ繧ｯ繝医Μ
        scene_dir = audio_dir / scene_id
        scene_dir.mkdir(parents=True, exist_ok=True)
        output_wav = str(scene_dir / f"{line_id}.wav")

        print(f"\n[{idx+1}/{len(pending)}] {scene_id}/{line_id}: {text[:35]}...")

        # 繧ｳ繝槭Φ繝臥ｵ・∩遶九※
        cmd = [
            PYTHON, INFER,
            "--hf-checkpoint", config["hf_checkpoint"],
            "--codec-repo", config["codec_repo"],
            "--text", text,
            "--no-ref",
            "--num-steps", str(num_steps),
            "--num-candidates", str(num_candidates),
            "--cfg-scale-text", str(cfg_text),
            "--cfg-scale-speaker", str(cfg_speaker),
            "--cfg-guidance-mode", cfg_guidance_mode,
            "--model-precision", "bf16",
            "--output-wav", output_wav,
            "--no-show-timings",
        ]

        # VoiceDesign: caption霑ｽ蜉
        if model == "voicedesign" and caption:
            cmd.extend(["--caption", caption])
            cmd.extend(["--cfg-scale-caption", str(cfg_caption)])

        # seed謖・ｮ・        if seed:
            cmd.extend(["--seed", seed])

        # LoRA 謖・ｮ夲ｼ・ora_path 縺瑚ｨｭ螳壹＆繧後※縺・ｋ陦後・縺ｿ・・        if lora_path:
            cmd.extend(["--lora-path", lora_path])
            cmd.extend(["--lora-scale", str(lora_scale)])

        # 螳溯｡鯉ｼ医Μ繝医Λ繧､莉倥″・・        success = False
        used_seed = ""
        for attempt in range(MAX_RETRIES + 1):
            try:
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"

                start = time.time()
                proc = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=TIMEOUT_SEC,
                    env=env, encoding="utf-8", errors="replace"
                )
                elapsed = time.time() - start

                # seed謚ｽ蜃ｺ
                for line in proc.stdout.split("\n"):
                    if "used_seed" in line:
                        used_seed = line.split(":")[-1].strip()

                # 謌仙粥蛻､螳・                if num_candidates == 1:
                    success = proc.returncode == 0 and Path(output_wav).exists()
                else:
                    # 隍・焚蛟呵｣・ {stem}_001.wav 遲・                    stem = Path(output_wav).stem
                    parent = Path(output_wav).parent
                    first_candidate = parent / f"{stem}_001.wav"
                    success = proc.returncode == 0 and first_candidate.exists()

                if success:
                    print(f"  -> [OK] {elapsed:.1f}s (seed={used_seed})")
                    break
                else:
                    if attempt < MAX_RETRIES:
                        print(f"  -> [RETRY {attempt+1}] {proc.stderr[-150:]}")
                    else:
                        print(f"  -> [FAIL] {proc.stderr[-200:]}")

            except subprocess.TimeoutExpired:
                if attempt < MAX_RETRIES:
                    print(f"  -> [TIMEOUT RETRY {attempt+1}]")
                else:
                    print(f"  -> [TIMEOUT FAIL]")

            except Exception as e:
                print(f"  -> [ERROR] {e}")
                break

        # CSV譖ｴ譁ｰ
        rows[row_idx]["status"] = "generated" if success else "gen_fail"
        rows[row_idx]["seed"] = used_seed

        if success:
            generated += 1
        else:
            failed += 1

    # CSV譖ｸ縺肴綾縺・    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total_elapsed = time.time() - total_start
    print(f"\n{'='*50}")
    print(f"蜿朱鹸螳御ｺ・ｼ・)
    print(f"  謌仙粥: {generated}/{len(pending)}")
    print(f"  螟ｱ謨・ {failed}/{len(pending)}")
    print(f"  謇隕∵凾髢・ {total_elapsed:.0f}遘・({total_elapsed/60:.1f}蛻・")
    print(f"  髻ｳ螢ｰ繝輔か繝ｫ繝: {audio_dir}")

    return {"total": len(pending), "generated": generated, "failed": failed}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python recorder.py <project_name>                          -- VoiceDesign縺ｧ逕滓・")
        print("  python recorder.py <project_name> --model v1               -- v1繝｢繝・Ν縺ｧ逕滓・")
        print("  python recorder.py <project_name> --dry-run                -- 繝峨Λ繧､繝ｩ繝ｳ・亥ｮ溯｡後○縺夂｢ｺ隱搾ｼ・)
        print("  python recorder.py <project_name> --audio-dir audio_agent  -- 蜃ｺ蜉帛・繝輔か繝ｫ繝謖・ｮ・)
        sys.exit(1)

    project_name = sys.argv[1]
    model = "voicedesign"
    dry_run = False
    audio_subdir = "audio"

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        elif args[i] == "--audio-dir" and i + 1 < len(args):
            audio_subdir = args[i + 1]
            i += 2
        else:
            i += 1

    record_project(project_name, model=model, dry_run=dry_run, audio_subdir=audio_subdir)
