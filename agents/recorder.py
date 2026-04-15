#!/usr/bin/env python3
"""収録エージェント - production.csv に基づいて infer.py で音声を一括生成"""
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

PROJECTS_DIR = Path("D:/irodori/projects")
PYTHON = str(Path("D:/irodori/emoji/.venv/Scripts/python.exe"))
INFER = str(Path("D:/irodori/emoji/infer.py"))

# VoiceDesign モデル設定
VOICEDESIGN_CONFIG = {
    "hf_checkpoint": "Aratako/Irodori-TTS-500M-v2-VoiceDesign",
    "codec_repo": "Aratako/Semantic-DACVAE-Japanese-32dim",  # 必須！latent_dim=32
}

# v1 モデル設定（リファレンス音声モード用）
V1_CONFIG = {
    "hf_checkpoint": "Aratako/Irodori-TTS-500M",
    "codec_repo": "facebook/dacvae-watermarked",  # latent_dim=128
}

MAX_RETRIES = 2
TIMEOUT_SEC = 180


def record_project(project_name: str, model: str = "voicedesign", dry_run: bool = False, audio_subdir: str = "audio") -> dict:
    """production.csv の pending 行を順に音声生成する"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / audio_subdir

    if not prod_csv.exists():
        print(f"[error] production.csv が見つかりません: {prod_csv}")
        return {}

    # モデル設定
    config = VOICEDESIGN_CONFIG if model == "voicedesign" else V1_CONFIG
    print(f"=== 収録エージェント ===")
    print(f"モデル: {config['hf_checkpoint']}")
    print(f"コーデック: {config['codec_repo']}")
    print()

    # CSV 読み込み
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # pending の行を抽出
    pending = [(i, row) for i, row in enumerate(rows) if row.get("status") == "pending"]
    if not pending:
        print("[info] 生成待ちの行がありません（全てpending以外）")
        return {"total": 0, "generated": 0}

    print(f"生成対象: {len(pending)}/{len(rows)}行")
    if dry_run:
        print("[dry-run] 実際の生成はスキップします")
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
        num_steps = int(row.get("num_steps") or 30)
        cfg_text = float(row.get("cfg_text") or 3.0)
        cfg_caption = float(row.get("cfg_caption") or 3.0)
        cfg_speaker = float(row.get("cfg_speaker") or 5.0)
        seed = row.get("seed", "").strip()

        # 出力ディレクトリ
        scene_dir = audio_dir / scene_id
        scene_dir.mkdir(parents=True, exist_ok=True)
        output_wav = str(scene_dir / f"{line_id}.wav")

        print(f"\n[{idx+1}/{len(pending)}] {scene_id}/{line_id}: {text[:35]}...")

        # コマンド組み立て
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
            "--model-precision", "bf16",
            "--output-wav", output_wav,
            "--no-show-timings",
        ]

        # VoiceDesign: caption追加
        if model == "voicedesign" and caption:
            cmd.extend(["--caption", caption])
            cmd.extend(["--cfg-scale-caption", str(cfg_caption)])

        # seed指定
        if seed:
            cmd.extend(["--seed", seed])

        # 実行（リトライ付き）
        success = False
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

                # seed抽出
                for line in proc.stdout.split("\n"):
                    if "used_seed" in line:
                        used_seed = line.split(":")[-1].strip()

                # 成功判定
                if num_candidates == 1:
                    success = proc.returncode == 0 and Path(output_wav).exists()
                else:
                    # 複数候補: {stem}_001.wav 等
                    stem = Path(output_wav).stem
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

        # CSV更新
        rows[row_idx]["status"] = "generated" if success else "gen_fail"
        rows[row_idx]["seed"] = used_seed

        if success:
            generated += 1
        else:
            failed += 1

    # CSV書き戻し
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total_elapsed = time.time() - total_start
    print(f"\n{'='*50}")
    print(f"収録完了！")
    print(f"  成功: {generated}/{len(pending)}")
    print(f"  失敗: {failed}/{len(pending)}")
    print(f"  所要時間: {total_elapsed:.0f}秒 ({total_elapsed/60:.1f}分)")
    print(f"  音声フォルダ: {audio_dir}")

    return {"total": len(pending), "generated": generated, "failed": failed}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python recorder.py <project_name>                          -- VoiceDesignで生成")
        print("  python recorder.py <project_name> --model v1               -- v1モデルで生成")
        print("  python recorder.py <project_name> --dry-run                -- ドライラン（実行せず確認）")
        print("  python recorder.py <project_name> --audio-dir audio_agent  -- 出力先フォルダ指定")
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
