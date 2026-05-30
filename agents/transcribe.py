#!/usr/bin/env python3
"""
transcribe.py - 髻ｳ螢ｰ繝輔ぃ繧､繝ｫ縺九ｉ繝・く繧ｹ繝医ｒ譁・ｭ苓ｵｷ縺薙＠

菴ｿ縺・婿:
  # 1繝輔ぃ繧､繝ｫ
  python transcribe.py audio.wav

  # 隍・焚繝輔ぃ繧､繝ｫ
  python transcribe.py audio1.wav audio2.mp3

  # 繝輔か繝ｫ繝蜀・・蜈ｨWAV/MP3
  python transcribe.py D:/path/to/folder/

繧ｪ繝励す繝ｧ繝ｳ:
  --output-dir       蜃ｺ蜉帛・繝輔か繝ｫ繝・医ョ繝輔か繝ｫ繝・ E:/irodori/projects/transcripts・・  --output-alongside 繧ｽ繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝縺ｫ蜃ｺ蜉幢ｼ・-output-dir 繧医ｊ蜆ｪ蜈茨ｼ・  --model            Whisper繝｢繝・Ν・医ョ繝輔か繝ｫ繝・ large-v3・・  --device           cuda 縺ｾ縺溘・ cpu・医ョ繝輔か繝ｫ繝・ cuda・・
蜃ｺ蜉・
  {output_dir}/{繝輔ぃ繧､繝ｫ蜷閤.txt  竊・Grok 縺ｫ貂｡縺励※繧｢繝ｬ繝ｳ繧ｸ縺励※繧ゅｉ縺・畑
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
DEFAULT_OUTPUT_DIR = "E:/irodori/projects/transcripts"


def transcribe_file(audio_path: Path, model, output_dir: Path | None, output_alongside: bool) -> Path:
    """1繝輔ぃ繧､繝ｫ繧呈枚蟄苓ｵｷ縺薙＠縺励※ .txt 縺ｧ菫晏ｭ・""
    print(f"[蜃ｦ逅・ｸｭ] {audio_path.name}")

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

    print(f"  竊・{len(lines)} 陦・/ 菫晏ｭ・ {out_path}")
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
            print(f"[繧ｹ繧ｭ繝・・] {inp}・亥ｯｾ蠢懷､・or 蟄伜惠縺励↑縺・ｼ・)
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser(description="髻ｳ螢ｰ繝輔ぃ繧､繝ｫ縺九ｉ繝・く繧ｹ繝医ｒ譁・ｭ苓ｵｷ縺薙＠")
    parser.add_argument("inputs", nargs="+", help="髻ｳ螢ｰ繝輔ぃ繧､繝ｫ縺ｾ縺溘・繝輔か繝ｫ繝縺ｮ繝代せ")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="蜃ｺ蜉帛・繝輔か繝ｫ繝")
    parser.add_argument("--output-alongside", action="store_true", help="繧ｽ繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝縺ｫ蜃ｺ蜉・)
    parser.add_argument("--model", default="large-v3", help="Whisper繝｢繝・Ν蜷・)
    parser.add_argument("--device", default="cuda", help="cuda 縺ｾ縺溘・ cpu")
    args = parser.parse_args()

    output_dir = None
    if not args.output_alongside:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_audio_files(args.inputs)
    if not files:
        print("蜃ｦ逅・ｯｾ雎｡縺ｮ髻ｳ螢ｰ繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｉ縺ｪ縺九▲縺溘ｏ縲・)
        sys.exit(1)

    print(f"蟇ｾ雎｡繝輔ぃ繧､繝ｫ: {len(files)} 莉ｶ")
    if args.output_alongside:
        print("蜃ｺ蜉帛・: 蜷・た繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝")
    else:
        print(f"蜃ｺ蜉帛・: {output_dir}")
    print()

    print(f"Whisper繝｢繝・Ν隱ｭ縺ｿ霎ｼ縺ｿ荳ｭ... ({args.model})")
    from faster_whisper import WhisperModel
    compute_type = "float16" if args.device == "cuda" else "int8"
    model = WhisperModel(args.model, device=args.device, compute_type=compute_type)
    print("貅門ｙ螳御ｺ・n")

    results = []
    for audio_path in files:
        try:
            out = transcribe_file(audio_path, model, output_dir, args.output_alongside)
            results.append((audio_path.name, True))
        except Exception as e:
            print(f"  [繧ｨ繝ｩ繝ｼ] {e}")
            results.append((audio_path.name, False))

    print()
    print("=" * 50)
    ok = sum(1 for _, s in results if s)
    ng = sum(1 for _, s in results if not s)
    print(f"螳御ｺ・ {ok} 莉ｶ / 繧ｨ繝ｩ繝ｼ: {ng} 莉ｶ")
    print()
    print("谺｡縺ｮ繧ｹ繝・ャ繝・")
    print("  蜃ｺ蜉帙＆繧後◆ .txt 繧・Grok 縺ｫ貂｡縺励※繧｢繝ｬ繝ｳ繧ｸ縺励※繧ゅｉ縺｣縺ｦ縺｡繧・≧縺縺・飭")


if __name__ == "__main__":
    main()
