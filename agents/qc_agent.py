#!/usr/bin/env python3
"""蜩∬ｳｪ繝√ぉ繝・け・・C・峨お繝ｼ繧ｸ繧ｧ繝ｳ繝・- 逕滓・髻ｳ螢ｰ縺ｮ謚陦鍋噪蜩∬ｳｪ繧定・蜍輔メ繧ｧ繝・け"""
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

# QC蝓ｺ貅・QC_THRESHOLDS = {
    "min_duration_sec": 0.5,
    "max_duration_sec": 30.0,
    "min_rms": 0.001,           # 辟｡髻ｳ讀懷・
    "max_peak": 0.99,           # 繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ讀懷・
    "max_leading_silence": 0.5, # 蜈磯ｭ辟｡髻ｳ縺ｮ險ｱ螳ｹ遘呈焚
    "silence_threshold": 0.005, # 辟｡髻ｳ蛻､螳壹・RMS髢ｾ蛟､
}


def analyze_wav(wav_path: str) -> dict:
    """1縺､縺ｮWAV繝輔ぃ繧､繝ｫ繧貞・譫舌☆繧・""
    try:
        data, sr = sf.read(wav_path)
    except Exception as e:
        return {"error": str(e)}

    if len(data.shape) > 1:
        data = data.mean(axis=1)  # 繧ｹ繝・Ξ繧ｪ竊偵Δ繝弱Λ繝ｫ

    duration = len(data) / sr
    rms = float(np.sqrt(np.mean(data ** 2)))
    peak = float(np.max(np.abs(data)))

    # 蜈磯ｭ辟｡髻ｳ縺ｮ讀懷・
    frame_size = int(sr * 0.02)  # 20ms frame
    leading_silence = 0.0
    for i in range(0, len(data) - frame_size, frame_size):
        frame_rms = np.sqrt(np.mean(data[i:i+frame_size] ** 2))
        if frame_rms > QC_THRESHOLDS["silence_threshold"]:
            break
        leading_silence += 0.02

    # 譛ｫ蟆ｾ辟｡髻ｳ縺ｮ讀懷・
    trailing_silence = 0.0
    for i in range(len(data) - frame_size, 0, -frame_size):
        frame_rms = np.sqrt(np.mean(data[i:i+frame_size] ** 2))
        if frame_rms > QC_THRESHOLDS["silence_threshold"]:
            break
        trailing_silence += 0.02

    return {
        "duration_sec": round(duration, 2),
        "rms_energy": round(rms, 5),
        "peak_value": round(peak, 4),
        "leading_silence_sec": round(leading_silence, 2),
        "trailing_silence_sec": round(trailing_silence, 2),
        "sample_rate": sr,
    }


def judge_quality(analysis: dict) -> tuple[str, str]:
    """蛻・梵邨先棡縺九ｉQC蛻､螳壹ｒ陦後≧縲・result, notes) 繧定ｿ斐☆"""
    if "error" in analysis:
        return "qc_fail", f"隱ｭ縺ｿ霎ｼ縺ｿ繧ｨ繝ｩ繝ｼ: {analysis['error']}"

    notes = []
    result = "qc_pass"

    dur = analysis["duration_sec"]
    if dur < QC_THRESHOLDS["min_duration_sec"]:
        notes.append(f"髻ｳ螢ｰ縺檎洒縺吶℃繧・{dur:.1f}s)")
        result = "qc_fail"
    elif dur > QC_THRESHOLDS["max_duration_sec"]:
        notes.append(f"髻ｳ螢ｰ縺碁聞縺吶℃繧・{dur:.1f}s)")
        result = "qc_fail"

    if analysis["rms_energy"] < QC_THRESHOLDS["min_rms"]:
        notes.append(f"辟｡髻ｳ縺ｾ縺溘・縺ｻ縺ｼ辟｡髻ｳ(RMS={analysis['rms_energy']:.5f})")
        result = "qc_fail"

    if analysis["peak_value"] > QC_THRESHOLDS["max_peak"]:
        notes.append(f"繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ(peak={analysis['peak_value']:.4f})")
        result = "qc_warn" if result != "qc_fail" else result

    if analysis["leading_silence_sec"] > QC_THRESHOLDS["max_leading_silence"]:
        notes.append(f"蜈磯ｭ辟｡髻ｳ縺碁聞縺・{analysis['leading_silence_sec']:.1f}s)")
        result = "qc_warn" if result != "qc_fail" else result

    return result, "; ".join(notes) if notes else "OK"


def run_qc(project_name: str) -> dict:
    """繝励Ο繧ｸ繧ｧ繧ｯ繝医・蜈ｨ逕滓・髻ｳ螢ｰ繧嘆C縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / "audio"
    qc_report_path = project_dir / "qc_report.csv"

    if not prod_csv.exists():
        print(f"[error] production.csv 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ")
        return {}

    # CSV 隱ｭ縺ｿ霎ｼ縺ｿ
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # generated 縺ｮ陦後ｒ謚ｽ蜃ｺ
    generated = [(i, row) for i, row in enumerate(rows) if row.get("status") == "generated"]
    if not generated:
        print("[info] QC蟇ｾ雎｡縺ｮ陦後′縺ゅｊ縺ｾ縺帙ｓ・・tatus=generated 縺後↑縺・ｼ・)
        return {}

    print(f"=== QC繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・===")
    print(f"QC蟇ｾ雎｡: {len(generated)}陦・)

    qc_rows = []
    pass_count = 0
    warn_count = 0
    fail_count = 0
    best_candidates = {}  # { "scene_id/line_id": candidate_num }

    for idx, (row_idx, row) in enumerate(generated):
        scene_id = row["scene_id"]
        line_id = row["line_id"]
        num_candidates = int(row.get("num_candidates") or 3)

        scene_dir = audio_dir / scene_id
        best_candidate = None
        best_rms = 0

        for c in range(1, num_candidates + 1):
            wav_name = f"{line_id}_{c:03d}.wav"
            wav_path = scene_dir / wav_name

            if not wav_path.exists():
                qc_rows.append({
                    "scene_id": scene_id, "line_id": line_id, "candidate": c,
                    "file_path": str(wav_path), "duration_sec": 0,
                    "rms_energy": 0, "peak_value": 0,
                    "leading_silence_sec": 0, "trailing_silence_sec": 0,
                    "qc_result": "qc_fail", "qc_notes": "繝輔ぃ繧､繝ｫ荳榊惠"
                })
                continue

            analysis = analyze_wav(str(wav_path))
            result, notes = judge_quality(analysis)

            qc_rows.append({
                "scene_id": scene_id, "line_id": line_id, "candidate": c,
                "file_path": str(wav_path),
                "duration_sec": analysis.get("duration_sec", 0),
                "rms_energy": analysis.get("rms_energy", 0),
                "peak_value": analysis.get("peak_value", 0),
                "leading_silence_sec": analysis.get("leading_silence_sec", 0),
                "trailing_silence_sec": analysis.get("trailing_silence_sec", 0),
                "qc_result": result,
                "qc_notes": notes,
            })

            if result in ("qc_pass", "qc_warn"):
                rms = analysis.get("rms_energy", 0)
                if rms > best_rms:
                    best_rms = rms
                    best_candidate = c

        # 陦後Ξ繝吶Ν縺ｮ蛻､螳・        line_results = [r["qc_result"] for r in qc_rows if r["scene_id"] == scene_id and r["line_id"] == line_id]
        if "qc_pass" in line_results or "qc_warn" in line_results:
            rows[row_idx]["status"] = "qc_pass"
            pass_count += 1
        else:
            rows[row_idx]["status"] = "qc_fail"
            fail_count += 1

        if best_candidate is not None:
            best_candidates[f"{scene_id}/{line_id}"] = best_candidate

        status_emoji = "OK" if rows[row_idx]["status"] == "qc_pass" else "NG"
        print(f"  [{status_emoji}] {scene_id}/{line_id} (best=c{best_candidate})")

    # QC繝ｬ繝昴・繝域嶌縺榊・縺・    qc_fieldnames = ["scene_id", "line_id", "candidate", "file_path",
                     "duration_sec", "rms_energy", "peak_value",
                     "leading_silence_sec", "trailing_silence_sec",
                     "qc_result", "qc_notes"]
    with open(qc_report_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=qc_fieldnames)
        writer.writeheader()
        writer.writerows(qc_rows)

    # production.csv 譖ｸ縺肴綾縺・    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # approvals_template.json 譖ｸ縺榊・縺暦ｼ・C謗ｨ螂ｨ蛟呵｣懊′蜈･縺｣縺滓価隱阪ユ繝ｳ繝励Ξ繝ｼ繝茨ｼ・    import json
    approvals_path = project_dir / "approvals_template.json"
    with open(approvals_path, "w", encoding="utf-8") as f:
        json.dump(best_candidates, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"QC螳御ｺ・ｼ・)
    print(f"  蜷域ｼ: {pass_count}  荳榊粋譬ｼ: {fail_count}")
    print(f"  QC繝ｬ繝昴・繝・ {qc_report_path}")
    print(f"  謇ｿ隱阪ユ繝ｳ繝励Ξ繝ｼ繝・ {approvals_path}")
    print(f"\n谺｡縺ｮ繧ｹ繝・ャ繝・")
    print(f"  1. audio/ 繝輔か繝ｫ繝縺ｧ髻ｳ螢ｰ繧堤｢ｺ隱阪＠ approvals_template.json 縺ｮ謨ｰ蟄励ｒ邱ｨ髮・)
    print(f"  2. python E:/irodori/agents/approve.py {project_dir.name}")

    return {"pass": pass_count, "warn": warn_count, "fail": fail_count}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qc_agent.py <project_name>")
        sys.exit(1)
    run_qc(sys.argv[1])
