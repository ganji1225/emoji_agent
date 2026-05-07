#!/usr/bin/env python3
"""
transcribe.py - 音声ファイルからテキストを文字起こし

使い方:
  # 1ファイル
  python transcribe.py audio.wav

  # 複数ファイル
  python transcribe.py audio1.wav audio2.mp3

  # フォルダ内の全WAV/MP3
  python transcribe.py D:/path/to/folder/

オプション:
  --output-dir       出力先フォルダ（デフォルト: D:/irodori/projects/transcripts）
  --output-alongside ソースファイルと同じフォルダに出力（--output-dir より優先）
  --model            Whisperモデル（デフォルト: large-v3）
  --device           cuda または cpu（デフォルト: cuda）

出力:
  {output_dir}/{ファイル名}.txt  ← Grok に渡してアレンジしてもらう用
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SUPPORTED_EXT = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
DEFAULT_OUTPUT_DIR = "D:/irodori/projects/transcripts"


def transcribe_file(audio_path: Path, model, output_dir: Path | None, output_alongside: bool) -> Path:
    """1ファイルを文字起こしして .txt で保存"""
    print(f"[処理中] {audio_path.name}")

    segments, info = model.transcribe(
        str(audio_path),
        language="ja",
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )

    lines = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            lines.append(text)

    dest_dir = audio_path.parent if output_alongside else output_dir
    out_path = dest_dir / (audio_path.stem + ".txt")
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"  → {len(lines)} 行 / 保存: {out_path}")
    return out_path


def collect_audio_files(inputs: list[str]) -> list[Path]:
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            for ext in SUPPORTED_EXT:
                files.extend(sorted(p.rglob(f"*{ext}")))
        elif p.is_file() and p.suffix.lower() in SUPPORTED_EXT:
            files.append(p)
        else:
            print(f"[スキップ] {inp}（対応外 or 存在しない）")
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser(description="音声ファイルからテキストを文字起こし")
    parser.add_argument("inputs", nargs="+", help="音声ファイルまたはフォルダのパス")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="出力先フォルダ")
    parser.add_argument("--output-alongside", action="store_true", help="ソースファイルと同じフォルダに出力")
    parser.add_argument("--model", default="large-v3", help="Whisperモデル名")
    parser.add_argument("--device", default="cuda", help="cuda または cpu")
    args = parser.parse_args()

    output_dir = None
    if not args.output_alongside:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_audio_files(args.inputs)
    if not files:
        print("処理対象の音声ファイルが見つからなかったわ。")
        sys.exit(1)

    print(f"対象ファイル: {len(files)} 件")
    if args.output_alongside:
        print("出力先: 各ソースファイルと同じフォルダ")
    else:
        print(f"出力先: {output_dir}")
    print()

    print(f"Whisperモデル読み込み中... ({args.model})")
    from faster_whisper import WhisperModel
    compute_type = "float16" if args.device == "cuda" else "int8"
    model = WhisperModel(args.model, device=args.device, compute_type=compute_type)
    print("準備完了\n")

    results = []
    for audio_path in files:
        try:
            out = transcribe_file(audio_path, model, output_dir, args.output_alongside)
            results.append((audio_path.name, True))
        except Exception as e:
            print(f"  [エラー] {e}")
            results.append((audio_path.name, False))

    print()
    print("=" * 50)
    ok = sum(1 for _, s in results if s)
    ng = sum(1 for _, s in results if not s)
    print(f"完了: {ok} 件 / エラー: {ng} 件")
    print()
    print("次のステップ:")
    print("  出力された .txt を Grok に渡してアレンジしてもらってちょうだい♪")


if __name__ == "__main__":
    main()
