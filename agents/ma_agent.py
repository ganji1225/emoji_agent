#!/usr/bin/env python3
"""MA/繝溘く繧ｷ繝ｳ繧ｰ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・- 謇ｿ隱肴ｸ医∩髻ｳ螢ｰ繧偵す繝ｼ繝ｳ/菴懷刀蜊倅ｽ阪〒邨仙粋"""
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

PROJECTS_DIR = Path("E:/irodori/projects")

# 繝・ヵ繧ｩ繝ｫ繝郁ｨｭ螳・LINE_SILENCE_SEC = 0.8     # 繧ｻ繝ｪ繝暮俣縺ｮ辟｡髻ｳ・育ｧ抵ｼ・SCENE_SILENCE_SEC = 2.0    # 繧ｷ繝ｼ繝ｳ髢薙・辟｡髻ｳ・育ｧ抵ｼ・SAMPLE_RATE = 48000         # 蜃ｺ蜉帙し繝ｳ繝励Ν繝ｬ繝ｼ繝・
# Trailing silence trimming・亥盾閠・ Emoji-TTS README, 2026-04-21・・TRIM_TAIL_THRESHOLD = 0.005  # RMS縺後％繧御ｻ･荳九ｒ辟｡髻ｳ縺ｨ縺ｿ縺ｪ縺・TRIM_TAIL_FRAME_MS = 20      # 辟｡髻ｳ蛻､螳壹・遯薙し繧､繧ｺ・医Α繝ｪ遘抵ｼ・TRIM_TAIL_KEEP_SEC = 0.10    # 譛ｫ蟆ｾ縺ｫ谿九☆閾ｪ辟ｶ縺ｪ菴咎渊・育ｧ抵ｼ・

def trim_trailing_silence(data: np.ndarray, sr: int,
                          threshold: float = TRIM_TAIL_THRESHOLD,
                          frame_ms: int = TRIM_TAIL_FRAME_MS,
                          keep_sec: float = TRIM_TAIL_KEEP_SEC) -> np.ndarray:
    """髻ｳ螢ｰ繝・・繧ｿ縺ｮ譛ｫ蟆ｾ辟｡髻ｳ繧偵ヨ繝ｪ繝縺吶ｋ・・lattening heuristic・・
    譛ｫ蟆ｾ縺九ｉ蠕後ｍ縺ｫ蜷代°縺｣縺ｦRMS繧定ｨ域ｸｬ縺励》hreshold 繧定ｶ・∴繧句慍轤ｹ縺ｾ縺ｧ繧ｫ繝・ヨ縲・    閾ｪ辟ｶ縺ｪ菴咎渊繧呈ｮ九☆縺溘ａ keep_sec 蛻・・辟｡髻ｳ繧呈忰蟆ｾ縺ｫ谿九☆縲・    """
    if len(data) == 0:
        return data

    frame_size = max(1, int(sr * frame_ms / 1000))
    # 譛ｫ蟆ｾ縺九ｉ騾・髄縺阪↓襍ｰ譟ｻ
    last_voice_idx = 0
    for i in range(len(data) - frame_size, 0, -frame_size):
        frame = data[i:i + frame_size]
        rms = float(np.sqrt(np.mean(frame ** 2)))
        if rms > threshold:
            last_voice_idx = i + frame_size
            break

    if last_voice_idx == 0:
        return data  # 蜈ｨ驛ｨ辟｡髻ｳ・育焚蟶ｸ・俄・ 縺昴・縺ｾ縺ｾ霑斐☆

    # 菴咎渊繧堤｢ｺ菫・    keep_samples = int(sr * keep_sec)
    end_idx = min(len(data), last_voice_idx + keep_samples)
    return data[:end_idx]


def copy_approved(project_name: str, audio_subdir: str = "audio") -> int:
    """approved_candidate 縺ｫ蝓ｺ縺･縺・※蛟呵｣懊ｒ approved/ 繝輔か繝ｫ繝縺ｫ繧ｳ繝斐・縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / audio_subdir
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
            print(f"[warn] 繧ｽ繝ｼ繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {src}")
            continue

        # 繧ｳ繝斐・・・oundfile縺ｧ隱ｭ縺ｿ譖ｸ縺阪＠縺ｦ邨ｱ荳・・        data, sr = sf.read(str(src))
        sf.write(str(dst), data, sr)
        row["status"] = "approved"  # 繧ｹ繝・・繧ｿ繧ｹ繧・approved 縺ｫ譖ｴ譁ｰ
        copied += 1

    # CSV 譖ｸ縺肴綾縺・    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[ok] {copied}繝輔ぃ繧､繝ｫ繧・approved/ 縺ｫ繧ｳ繝斐・縺励∪縺励◆")
    return copied


def auto_approve_first(project_name: str) -> int:
    """蜈ｨ縺ｦ縺ｮ qc_pass 陦後〒蛟呵｣・繧定・蜍墓価隱阪☆繧具ｼ医ユ繧ｹ繝育畑・・""
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

    print(f"[ok] {count}陦後ｒ閾ｪ蜍墓価隱阪＠縺ｾ縺励◆・亥呵｣・・・)
    return count


def concat_scenes(project_name: str, line_silence: float = LINE_SILENCE_SEC,
                  scene_silence: float = SCENE_SILENCE_SEC) -> list[str]:
    """謇ｿ隱肴ｸ医∩髻ｳ螢ｰ繧偵す繝ｼ繝ｳ蜊倅ｽ阪〒邨仙粋縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    approved_dir = project_dir / "approved"
    master_dir = project_dir / "master"
    master_dir.mkdir(parents=True, exist_ok=True)

    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 繧ｷ繝ｼ繝ｳ縺斐→縺ｫ繧ｰ繝ｫ繝ｼ繝怜喧
    scenes = {}
    for row in rows:
        if row.get("status") != "approved":
            continue
        scene_id = row["scene_id"]
        if scene_id not in scenes:
            scenes[scene_id] = []
        scenes[scene_id].append(row)

    if not scenes:
        print("[warn] approved 縺ｮ繧ｻ繝ｪ繝輔′縺ゅｊ縺ｾ縺帙ｓ")
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
                print(f"[warn] {scene_id}/{line_id}.wav 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ")
                continue

            data, sr = sf.read(str(wav_path))
            if len(data.shape) > 1:
                data = data.mean(axis=1)
            # 蜷・そ繝ｪ繝輔・譛ｫ蟆ｾ辟｡髻ｳ繧偵ヨ繝ｪ繝・郁・辟ｶ縺ｪ菴咎渊縺縺第ｮ九☆・・            data = trim_trailing_silence(data, sr)
            scene_audio.append(data)

            # 繧ｻ繝ｪ繝暮俣辟｡髻ｳ・域怙蠕後・繧ｻ繝ｪ繝穂ｻ･螟厄ｼ・            if i < len(scene_rows) - 1:
                silence = np.zeros(int(sr * line_silence))
                scene_audio.append(silence)

        if scene_audio:
            scene_concat = np.concatenate(scene_audio)
            scene_path = master_dir / f"{scene_id}.wav"
            sf.write(str(scene_path), scene_concat, sr)
            scene_files.append(str(scene_path))
            duration = len(scene_concat) / sr
            print(f"[ok] {scene_id}.wav ({duration:.1f}遘・ {len(scene_rows)}陦・")

            all_audio.append(scene_concat)
            # 繧ｷ繝ｼ繝ｳ髢鍋┌髻ｳ
            all_audio.append(np.zeros(int(sr * scene_silence)))

    # 蜈ｨ繧ｷ繝ｼ繝ｳ邨仙粋
    if all_audio:
        # 譛蠕後・繧ｷ繝ｼ繝ｳ髢鍋┌髻ｳ繧帝勁蜴ｻ
        if len(all_audio) > 1:
            all_audio = all_audio[:-1]
        full = np.concatenate(all_audio)
        full_path = master_dir / "full_work.wav"
        sf.write(str(full_path), full, sr)
        full_duration = len(full) / sr
        print(f"\n[ok] full_work.wav ({full_duration:.1f}遘・ 蜈ｨ{sum(len(v) for v in scenes.values())}陦・")
        scene_files.append(str(full_path))

    return scene_files


def wav_to_mp3(project_name: str, source_dir: str = "master") -> list[str]:
    """WAV繝輔ぃ繧､繝ｫ繧樽P3縺ｫ螟画鋤縺吶ｋ・磯・蟶・畑・・
    蜿り・ https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku
    ffmpeg VBR qscale:a 2 竕・190kbps
    """
    import subprocess
    import shutil

    if not shutil.which("ffmpeg"):
        print("[error] ffmpeg 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縲１ATH 縺ｫ ffmpeg 繧定ｿｽ蜉縺励※縺上□縺輔＞")
        return []

    project_dir = PROJECTS_DIR / project_name
    src_dir = project_dir / source_dir
    mp3_dir = project_dir / "mp3"
    mp3_dir.mkdir(parents=True, exist_ok=True)

    wav_files = sorted(src_dir.glob("*.wav"))
    if not wav_files:
        print(f"[warn] {src_dir} 縺ｫ WAV 繝輔ぃ繧､繝ｫ縺後≠繧翫∪縺帙ｓ")
        return []

    mp3_files = []
    for wav_path in wav_files:
        mp3_path = mp3_dir / f"{wav_path.stem}.mp3"
        cmd = [
            "ffmpeg", "-y", "-i", str(wav_path),
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            str(mp3_path),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # 繝輔ぃ繧､繝ｫ繧ｵ繧､繧ｺ陦ｨ遉ｺ
                wav_size = wav_path.stat().st_size / 1024 / 1024
                mp3_size = mp3_path.stat().st_size / 1024 / 1024
                ratio = mp3_size / wav_size * 100 if wav_size > 0 else 0
                print(f"[ok] {wav_path.name} 竊・{mp3_path.name} ({wav_size:.1f}MB 竊・{mp3_size:.1f}MB, {ratio:.0f}%)")
                mp3_files.append(str(mp3_path))
            else:
                print(f"[error] {wav_path.name}: {result.stderr[-100:]}")
        except Exception as e:
            print(f"[error] {wav_path.name}: {e}")

    print(f"\n[ok] MP3螟画鋤螳御ｺ・ {len(mp3_files)}/{len(wav_files)}繝輔ぃ繧､繝ｫ 竊・{mp3_dir}")
    return mp3_files


def run_ma(project_name: str, export_mp3: bool = False,
           audio_subdir: str = "audio") -> list[str]:
    """MA蜈ｨ蟾･遞九ｒ螳溯｡後☆繧・""
    print(f"=== MA繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・===")
    if audio_subdir != "audio":
        print(f"髻ｳ螢ｰ繧ｽ繝ｼ繧ｹ: {audio_subdir}/")

    # 1. 謇ｿ隱肴ｸ医∩髻ｳ螢ｰ繧偵さ繝斐・
    copied = copy_approved(project_name, audio_subdir=audio_subdir)
    if copied == 0:
        print("[info] 謇ｿ隱肴ｸ医∩髻ｳ螢ｰ縺後≠繧翫∪縺帙ｓ")
        return []

    # 2. 繧ｷ繝ｼ繝ｳ邨仙粋 + 蜈ｨ菴鍋ｵ仙粋
    files = concat_scenes(project_name)

    # 3. MP3螟画鋤・医が繝励す繝ｧ繝ｳ・・    if export_mp3:
        mp3_files = wav_to_mp3(project_name)
        files.extend(mp3_files)

    print(f"\n{'='*50}")
    print(f"MA螳御ｺ・ｼ∝・蜉・ E:/irodori/projects/{project_name}/master/")
    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ma_agent.py <project_name>              -- MA螳溯｡・)
        print("  python ma_agent.py <project_name> --auto        -- 閾ｪ蜍墓価隱・MA螳溯｡・)
        print("  python ma_agent.py <project_name> --mp3         -- MA螳溯｡・MP3譖ｸ縺榊・縺・)
        print("  python ma_agent.py <project_name> --mp3-only    -- MP3螟画鋤縺ｮ縺ｿ")
        sys.exit(1)

    project_name = sys.argv[1]
    auto = "--auto" in sys.argv
    export_mp3 = "--mp3" in sys.argv
    mp3_only = "--mp3-only" in sys.argv
    audio_subdir = "audio"
    if "--audio-dir" in sys.argv:
        idx = sys.argv.index("--audio-dir")
        if idx + 1 < len(sys.argv):
            audio_subdir = sys.argv[idx + 1]

    if mp3_only:
        wav_to_mp3(project_name)
    else:
        if auto:
            auto_approve_first(project_name)
            copy_approved(project_name, audio_subdir=audio_subdir)

        run_ma(project_name, export_mp3=export_mp3, audio_subdir=audio_subdir)
