#!/usr/bin/env python3
"""
pdf_extract.py - 繝・ず繧ｿ繝ｫPDF縺九ｉ繧ｯ繝ｪ繝ｼ繝ｳ繝・く繧ｹ繝医ｒ謚ｽ蜃ｺ

菴ｿ縺・婿:
  # 1繝輔ぃ繧､繝ｫ
  python pdf_extract.py document.pdf

  # 隍・焚繝輔ぃ繧､繝ｫ
  python pdf_extract.py doc1.pdf doc2.pdf

  # 繝輔か繝ｫ繝蜀・・蜈ｨPDF繧剃ｸ諡ｬ蜃ｦ逅・  python pdf_extract.py D:/path/to/folder/

繧ｪ繝励す繝ｧ繝ｳ:
  --output-dir       蜃ｺ蜉帛・繝輔か繝ｫ繝・医ョ繝輔か繝ｫ繝・ E:/irodori/projects/transcripts・・  --output-alongside 繧ｽ繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝縺ｫ蜃ｺ蜉幢ｼ・-output-dir 繧医ｊ蜆ｪ蜈茨ｼ・
蜃ｺ蜉・
  {output_dir}/{繝輔ぃ繧､繝ｫ蜷閤.txt  竊・Grok 縺ｫ貂｡縺励※繧｢繝ｬ繝ｳ繧ｸ縺励※繧ゅｉ縺・畑
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_OUTPUT_DIR = "E:/irodori/projects/transcripts"


def clean_text(text: str) -> str:
    """謚ｽ蜃ｺ繝・く繧ｹ繝医・繧ｯ繝ｪ繝ｼ繝九Φ繧ｰ"""
    # 騾｣邯壹☆繧狗ｩｺ逋ｽ繧・縺､縺ｫ
    text = re.sub(r"[ \t縲]+", " ", text)
    # 3陦御ｻ･荳翫・騾｣邯夂ｩｺ陦後ｒ2陦後↓
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 陦碁ｭ繝ｻ陦梧忰縺ｮ遨ｺ逋ｽ髯､蜴ｻ
    lines = [line.strip() for line in text.splitlines()]
    # 遨ｺ陦後・縺ｿ縺ｮ騾｣邯壹ｒ1縺､縺ｫ蝨ｧ邵ｮ
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return "\n".join(result).strip()


def extract_pdf(pdf_path: Path, output_dir: Path | None, output_alongside: bool) -> Path:
    """PDF縺九ｉ繝・く繧ｹ繝医ｒ謚ｽ蜃ｺ縺励※ .txt 縺ｫ菫晏ｭ・""
    import pdfplumber

    print(f"[蜃ｦ逅・ｸｭ] {pdf_path.name}")

    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text.append(text)
            if i % 10 == 0 or i == total:
                print(f"  {i}/{total} 繝壹・繧ｸ蜃ｦ逅・ｸ医∩", end="\r")

    print()  # 謾ｹ陦・
    combined = "\n\n".join(all_text)
    cleaned  = clean_text(combined)

    dest_dir = pdf_path.parent if output_alongside else output_dir
    out_path = dest_dir / (pdf_path.stem + ".txt")
    out_path.write_text(cleaned, encoding="utf-8")

    line_count = cleaned.count("\n") + 1
    char_count  = len(cleaned)
    print(f"  竊・{total}繝壹・繧ｸ / {line_count}陦・/ {char_count}譁・ｭ・/ 菫晏ｭ・ {out_path}")
    return out_path


def collect_pdf_files(inputs: list[str]) -> list[Path]:
    """蠑墓焚縺九ｉPDF繝輔ぃ繧､繝ｫ縺ｮ繝ｪ繧ｹ繝医ｒ蜿朱寔"""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(sorted(p.glob("**/*.pdf")))
        elif p.is_file() and p.suffix.lower() == ".pdf":
            files.append(p)
        else:
            print(f"[繧ｹ繧ｭ繝・・] {inp}・・DF繝輔ぃ繧､繝ｫ縺ｧ縺ｯ縺ｪ縺・°蟄伜惠縺励↑縺・ｼ・)
    # 驥崎､・勁蜴ｻ
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser(description="繝・ず繧ｿ繝ｫPDF縺九ｉ繧ｯ繝ｪ繝ｼ繝ｳ繝・く繧ｹ繝医ｒ謚ｽ蜃ｺ")
    parser.add_argument("inputs", nargs="+", help="PDF繝輔ぃ繧､繝ｫ縺ｾ縺溘・繝輔か繝ｫ繝縺ｮ繝代せ")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="蜃ｺ蜉帛・繝輔か繝ｫ繝")
    parser.add_argument("--output-alongside", action="store_true", help="繧ｽ繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝縺ｫ蜃ｺ蜉・)
    args = parser.parse_args()

    output_dir = None
    if not args.output_alongside:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_pdf_files(args.inputs)
    if not files:
        print("蜃ｦ逅・ｯｾ雎｡縺ｮPDF繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｉ縺ｪ縺九▲縺溘ｏ縲・)
        sys.exit(1)

    print(f"蟇ｾ雎｡繝輔ぃ繧､繝ｫ: {len(files)} 莉ｶ")
    if args.output_alongside:
        print("蜃ｺ蜉帛・: 蜷・た繝ｼ繧ｹ繝輔ぃ繧､繝ｫ縺ｨ蜷後§繝輔か繝ｫ繝")
    else:
        print(f"蜃ｺ蜉帛・: {output_dir}")
    print()

    results = []
    for pdf_path in files:
        try:
            out = extract_pdf(pdf_path, output_dir, args.output_alongside)
            results.append((pdf_path.name, True))
        except Exception as e:
            print(f"  [繧ｨ繝ｩ繝ｼ] {e}")
            results.append((pdf_path.name, False))

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
