#!/usr/bin/env python3
"""MA/ミキシングエージェント - 承認済み音声をシーン/作品単位で結合"""
import csv
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import soundfile as sf

PROJECTS_DIR = Path("D:/irodori/projects")

# デフォルト設定
LINE_SILENCE_SEC = 0.8     # セリフ間の無音（秒）
SCENE_SILENCE_SEC = 2.0    # シーン間の無音（秒）
SAMPLE_RATE = 48000         # 出力サンプルレート


def copy_approved(project_name: str) -> int:
    """approved_candidate に基づいて候補を approved/ フォルダにコピーする"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / "audio"
    approved_dir = project_dir / "approved"

    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    copied = 0
    for row in rows:
        approved_c = row.get("approved_candidate", "").strip()
        if not approved_c:
            continue

        scene_id = row["scene_id"]
        line_id = row["line_id"]
        candidate = int(approved_c)

        src = audio_dir / scene_id / f"{line_id}_{candidate:03d}.wav"
        dst_dir = approved_dir / scene_id
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / f"{line_id}.wav"

        if not src.exists():
            print(f"[warn] ソースが見つかりません: {src}")
            continue

        # コピー（soundfileで読み書きして統一）
        data, sr = sf.read(str(src))
        sf.write(str(dst), data, sr)
        copied += 1

    print(f"[ok] {copied}ファイルを approved/ にコピーしました")
    return copied


def auto_approve_first(project_name: str) -> int:
    """全ての qc_pass 行で候補1を自動承認する（テスト用）"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"

    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    count = 0
    for row in rows:
        if row.get("status") == "qc_pass" and not row.get("approved_candidate", "").strip():
            row["approved_candidate"] = "1"
            row["status"] = "approved"
            count += 1

    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[ok] {count}行を自動承認しました（候補1）")
    return count


def concat_scenes(project_name: str, line_silence: float = LINE_SILENCE_SEC,
                  scene_silence: float = SCENE_SILENCE_SEC) -> list[str]:
    """承認済み音声をシーン単位で結合する"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    approved_dir = project_dir / "approved"
    master_dir = project_dir / "master"
    master_dir.mkdir(parents=True, exist_ok=True)

    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # シーンごとにグループ化
    scenes = {}
    for row in rows:
        if row.get("status") != "approved":
            continue
        scene_id = row["scene_id"]
        if scene_id not in scenes:
            scenes[scene_id] = []
        scenes[scene_id].append(row)

    if not scenes:
        print("[warn] approved のセリフがありません")
        return []

    scene_files = []
    all_audio = []

    for scene_id in sorted(scenes.keys()):
        scene_rows = scenes[scene_id]
        scene_audio = []

        for i, row in enumerate(scene_rows):
            line_id = row["line_id"]
            wav_path = approved_dir / scene_id / f"{line_id}.wav"

            if not wav_path.exists():
                print(f"[warn] {scene_id}/{line_id}.wav が見つかりません")
                continue

            data, sr = sf.read(str(wav_path))
            if len(data.shape) > 1:
                data = data.mean(axis=1)
            scene_audio.append(data)

            # セリフ間無音（最後のセリフ以外）
            if i < len(scene_rows) - 1:
                silence = np.zeros(int(sr * line_silence))
                scene_audio.append(silence)

        if scene_audio:
            scene_concat = np.concatenate(scene_audio)
            scene_path = master_dir / f"{scene_id}.wav"
            sf.write(str(scene_path), scene_concat, sr)
            scene_files.append(str(scene_path))
            duration = len(scene_concat) / sr
            print(f"[ok] {scene_id}.wav ({duration:.1f}秒, {len(scene_rows)}行)")

            all_audio.append(scene_concat)
            # シーン間無音
            all_audio.append(np.zeros(int(sr * scene_silence)))

    # 全シーン結合
    if all_audio:
        # 最後のシーン間無音を除去
        if len(all_audio) > 1:
            all_audio = all_audio[:-1]
        full = np.concatenate(all_audio)
        full_path = master_dir / "full_work.wav"
        sf.write(str(full_path), full, sr)
        full_duration = len(full) / sr
        print(f"\n[ok] full_work.wav ({full_duration:.1f}秒, 全{sum(len(v) for v in scenes.values())}行)")
        scene_files.append(str(full_path))

    return scene_files


def run_ma(project_name: str) -> list[str]:
    """MA全工程を実行する"""
    print(f"=== MAエージェント ===")

    # 1. 承認済み音声をコピー
    copied = copy_approved(project_name)
    if copied == 0:
        print("[info] 承認済み音声がありません")
        return []

    # 2. シーン結合 + 全体結合
    files = concat_scenes(project_name)

    print(f"\n{'='*50}")
    print(f"MA完了！出力: D:/irodori/projects/{project_name}/master/")
    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ma_agent.py <project_name>            -- MA実行")
        print("  python ma_agent.py <project_name> --auto      -- 自動承認+MA実行")
        sys.exit(1)

    project_name = sys.argv[1]
    auto = "--auto" in sys.argv

    if auto:
        auto_approve_first(project_name)
        copy_approved(project_name)

    run_ma(project_name)
