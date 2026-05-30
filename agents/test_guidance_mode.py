#!/usr/bin/env python3
"""guidance_mode 豈碑ｼ・ユ繧ｹ繝医せ繧ｯ繝ｪ繝励ヨ

Emoji-TTS 縺ｮ `--guidance-mode` 繝代Λ繝｡繝ｼ繧ｿ縺ｫ縺ｯ 3縺､縺ｮ蛟､縺後≠繧・
  - independent (繝・ヵ繧ｩ繝ｫ繝・: text 縺ｨ speaker 縺ｮCFG繧堤峡遶矩←逕ｨ
  - joint: text 縺ｨ speaker 縺ｮCFG繧堤ｵｱ蜷磯←逕ｨ
  - alternating: 繧ｹ繝・ャ繝励＃縺ｨ縺ｫ莠､莠偵↓驕ｩ逕ｨ

3繝｢繝ｼ繝・ﾃ・蜷後§ seed 縺ｧ逕滓・縺励※閨ｴ縺肴ｯ斐∋繧九◆繧√・繧ｹ繧ｯ繝ｪ繝励ヨ縲・
菴ｿ縺・婿:
  python agents/test_guidance_mode.py <project_name> <scene_id> <line_id>

萓・
  python agents/test_guidance_mode.py hakuu_game_voices s2_mid line_001

蜃ｺ蜉・
  audio/{scene_id}/{line_id}_gm-{mode}_001~003.wav
"""
import csv
import os
import subprocess
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")
EMOJI_PYTHON = "E:/irodori/emoji/.venv/Scripts/python.exe"
INFER_PY = "E:/irodori/emoji/infer.py"

GUIDANCE_MODES = ["independent", "joint", "alternating"]

# 豈碑ｼ・ｒ蜈ｬ蟷ｳ縺ｫ縺吶ｋ縺溘ａ蝗ｺ螳・seed
TEST_SEED = "12345"


def run_test(project_name: str, scene_id: str, line_id: str):
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))

    # 蟇ｾ雎｡陦後ｒ讀懃ｴ｢
    target = None
    for r in rows:
        if r["scene_id"] == scene_id and r["line_id"] == line_id:
            target = r
            break

    if not target:
        print(f"[error] {scene_id}/{line_id} 縺・production.csv 縺ｫ隕九▽縺九ｊ縺ｾ縺帙ｓ")
        sys.exit(1)

    text = target["text_with_emoji"]
    caption = target["caption"]
    cfg_text = target["cfg_text"]
    cfg_caption = target["cfg_caption"]
    cfg_speaker = target["cfg_speaker"]
    num_steps = target["num_steps"]

    out_dir = PROJECTS_DIR / project_name / "audio" / scene_id
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== guidance_mode 豈碑ｼ・ユ繧ｹ繝・===")
    print(f"蟇ｾ雎｡: {scene_id}/{line_id}")
    print(f"繝・く繧ｹ繝・ {text}")
    print(f"caption: {caption}")
    print(f"seed: {TEST_SEED}, num_steps: {num_steps}")
    print()

    for mode in GUIDANCE_MODES:
        print(f"--- {mode} ---")
        out_path = out_dir / f"{line_id}_gm-{mode}.wav"
        cmd = [
            EMOJI_PYTHON, INFER_PY,
            "--hf-checkpoint", "Aratako/Irodori-TTS-500M-v2-VoiceDesign",
            "--codec-repo", "Aratako/Semantic-DACVAE-Japanese-32dim",
            "--text", text,
            "--caption", caption,
            "--no-ref",
            "--seed", TEST_SEED,
            "--num-steps", num_steps,
            "--num-candidates", "3",
            "--cfg-scale-text", cfg_text,
            "--cfg-scale-caption", cfg_caption,
            "--cfg-scale-speaker", cfg_speaker,
            "--cfg-guidance-mode", mode,
            "--model-precision", "bf16",
            "--output-wav", str(out_path),
            "--no-show-timings",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            print(f"  OK: {line_id}_gm-{mode}_001~003.wav 逕滓・螳御ｺ・)
        else:
            print(f"  FAIL: {result.stderr[-300:]}")
        print()

    print(f"蜃ｺ蜉帛・: {out_dir}")
    print(f"\n閨ｴ縺肴ｯ斐∋繝昴う繝ｳ繝・")
    print(f"  - independent: 讓呎ｺ悶Ｕext/speaker 繧堤峡遶矩←逕ｨ")
    print(f"  - joint: 邨ｱ蜷磯←逕ｨ縲ょ｣ｰ雉ｪ螟牙喧縺梧而縺医ａ縺ｫ縺ｪ繧句だ蜷托ｼ・)
    print(f"  - alternating: 莠､莠帝←逕ｨ縲ゅΜ繧ｺ繝諢溘ｄ謚第恕縺ｫ驕輔＞縺悟・繧九°")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python test_guidance_mode.py <project_name> <scene_id> <line_id>")
        print("萓・ python test_guidance_mode.py hakuu_game_voices s2_mid line_001")
        sys.exit(1)

    run_test(sys.argv[1], sys.argv[2], sys.argv[3])
