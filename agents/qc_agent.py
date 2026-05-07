#!/usr/bin/env python3
"""品質チェック（QC）エージェント - 生成音声の技術的品質を自動チェック"""
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

# QC基準
QC_THRESHOLDS = {
    "min_duration_sec": 0.5,
    "max_duration_sec": 30.0,
    "min_rms": 0.001,           # 無音検出
    "max_peak": 0.99,           # クリッピング検出
    "max_leading_silence": 0.5, # 先頭無音の許容秒数
    "silence_threshold": 0.005, # 無音判定のRMS閾値
}


def analyze_wav(wav_path: str) -> dict:
    """1つのWAVファイルを分析する"""
    try:
        data, sr = sf.read(wav_path)
    except Exception as e:
        return {"error": str(e)}

    if len(data.shape) > 1:
        data = data.mean(axis=1)  # ステレオ→モノラル

    duration = len(data) / sr
    rms = float(np.sqrt(np.mean(data ** 2)))
    peak = float(np.max(np.abs(data)))

    # 先頭無音の検出
    frame_size = int(sr * 0.02)  # 20ms frame
    leading_silence = 0.0
    for i in range(0, len(data) - frame_size, frame_size):
        frame_rms = np.sqrt(np.mean(data[i:i+frame_size] ** 2))
        if frame_rms > QC_THRESHOLDS["silence_threshold"]:
            break
        leading_silence += 0.02

    # 末尾無音の検出
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
    """分析結果からQC判定を行う。(result, notes) を返す"""
    if "error" in analysis:
        return "qc_fail", f"読み込みエラー: {analysis['error']}"

    notes = []
    result = "qc_pass"

    dur = analysis["duration_sec"]
    if dur < QC_THRESHOLDS["min_duration_sec"]:
        notes.append(f"音声が短すぎる({dur:.1f}s)")
        result = "qc_fail"
    elif dur > QC_THRESHOLDS["max_duration_sec"]:
        notes.append(f"音声が長すぎる({dur:.1f}s)")
        result = "qc_fail"

    if analysis["rms_energy"] < QC_THRESHOLDS["min_rms"]:
        notes.append(f"無音またはほぼ無音(RMS={analysis['rms_energy']:.5f})")
        result = "qc_fail"

    if analysis["peak_value"] > QC_THRESHOLDS["max_peak"]:
        notes.append(f"クリッピング(peak={analysis['peak_value']:.4f})")
        result = "qc_warn" if result != "qc_fail" else result

    if analysis["leading_silence_sec"] > QC_THRESHOLDS["max_leading_silence"]:
        notes.append(f"先頭無音が長い({analysis['leading_silence_sec']:.1f}s)")
        result = "qc_warn" if result != "qc_fail" else result

    return result, "; ".join(notes) if notes else "OK"


def run_qc(project_name: str) -> dict:
    """プロジェクトの全生成音声をQCする"""
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"
    audio_dir = project_dir / "audio"
    qc_report_path = project_dir / "qc_report.csv"

    if not prod_csv.exists():
        print(f"[error] production.csv が見つかりません")
        return {}

    # CSV 読み込み
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # generated の行を抽出
    generated = [(i, row) for i, row in enumerate(rows) if row.get("status") == "generated"]
    if not generated:
        print("[info] QC対象の行がありません（status=generated がない）")
        return {}

    print(f"=== QCエージェント ===")
    print(f"QC対象: {len(generated)}行")

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
                    "qc_result": "qc_fail", "qc_notes": "ファイル不在"
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

        # 行レベルの判定
        line_results = [r["qc_result"] for r in qc_rows if r["scene_id"] == scene_id and r["line_id"] == line_id]
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

    # QCレポート書き出し
    qc_fieldnames = ["scene_id", "line_id", "candidate", "file_path",
                     "duration_sec", "rms_energy", "peak_value",
                     "leading_silence_sec", "trailing_silence_sec",
                     "qc_result", "qc_notes"]
    with open(qc_report_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=qc_fieldnames)
        writer.writeheader()
        writer.writerows(qc_rows)

    # production.csv 書き戻し
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # approvals_template.json 書き出し（QC推奨候補が入った承認テンプレート）
    import json
    approvals_path = project_dir / "approvals_template.json"
    with open(approvals_path, "w", encoding="utf-8") as f:
        json.dump(best_candidates, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"QC完了！")
    print(f"  合格: {pass_count}  不合格: {fail_count}")
    print(f"  QCレポート: {qc_report_path}")
    print(f"  承認テンプレート: {approvals_path}")
    print(f"\n次のステップ:")
    print(f"  1. audio/ フォルダで音声を確認し approvals_template.json の数字を編集")
    print(f"  2. python D:/irodori/agents/approve.py {project_dir.name}")

    return {"pass": pass_count, "warn": warn_count, "fail": fail_count}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qc_agent.py <project_name>")
        sys.exit(1)
    run_qc(sys.argv[1])
