#!/usr/bin/env python3
"""guidance_mode 比較テストスクリプト

Emoji-TTS の `--guidance-mode` パラメータには 3つの値がある:
  - independent (デフォルト): text と speaker のCFGを独立適用
  - joint: text と speaker のCFGを統合適用
  - alternating: ステップごとに交互に適用

3モード × 同じ seed で生成して聴き比べるためのスクリプト。

使い方:
  python agents/test_guidance_mode.py <project_name> <scene_id> <line_id>

例:
  python agents/test_guidance_mode.py hakuu_game_voices s2_mid line_001

出力:
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

PROJECTS_DIR = Path("D:/irodori/projects")
EMOJI_PYTHON = "D:/irodori/emoji/.venv/Scripts/python.exe"
INFER_PY = "D:/irodori/emoji/infer.py"

GUIDANCE_MODES = ["independent", "joint", "alternating"]

# 比較を公平にするため固定 seed
TEST_SEED = "12345"


def run_test(project_name: str, scene_id: str, line_id: str):
    csv_path = PROJECTS_DIR / project_name / "production.csv"
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))

    # 対象行を検索
    target = None
    for r in rows:
        if r["scene_id"] == scene_id and r["line_id"] == line_id:
            target = r
            break

    if not target:
        print(f"[error] {scene_id}/{line_id} が production.csv に見つかりません")
        sys.exit(1)

    text = target["text_with_emoji"]
    caption = target["caption"]
    cfg_text = target["cfg_text"]
    cfg_caption = target["cfg_caption"]
    cfg_speaker = target["cfg_speaker"]
    num_steps = target["num_steps"]

    out_dir = PROJECTS_DIR / project_name / "audio" / scene_id
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== guidance_mode 比較テスト ===")
    print(f"対象: {scene_id}/{line_id}")
    print(f"テキスト: {text}")
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
            print(f"  OK: {line_id}_gm-{mode}_001~003.wav 生成完了")
        else:
            print(f"  FAIL: {result.stderr[-300:]}")
        print()

    print(f"出力先: {out_dir}")
    print(f"\n聴き比べポイント:")
    print(f"  - independent: 標準。text/speaker を独立適用")
    print(f"  - joint: 統合適用。声質変化が控えめになる傾向？")
    print(f"  - alternating: 交互適用。リズム感や抑揚に違いが出るか")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python test_guidance_mode.py <project_name> <scene_id> <line_id>")
        print("例: python test_guidance_mode.py hakuu_game_voices s2_mid line_001")
        sys.exit(1)

    run_test(sys.argv[1], sys.argv[2], sys.argv[3])
