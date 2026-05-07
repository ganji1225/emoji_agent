#!/usr/bin/env python3
"""
pdf_extract.py - デジタルPDFからクリーンテキストを抽出

使い方:
  # 1ファイル
  python pdf_extract.py document.pdf

  # 複数ファイル
  python pdf_extract.py doc1.pdf doc2.pdf

  # フォルダ内の全PDFを一括処理
  python pdf_extract.py D:/path/to/folder/

オプション:
  --output-dir       出力先フォルダ（デフォルト: D:/irodori/projects/transcripts）
  --output-alongside ソースファイルと同じフォルダに出力（--output-dir より優先）

出力:
  {output_dir}/{ファイル名}.txt  ← Grok に渡してアレンジしてもらう用
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

DEFAULT_OUTPUT_DIR = "D:/irodori/projects/transcripts"


def clean_text(text: str) -> str:
    """抽出テキストのクリーニング"""
    # 連続する空白を1つに
    text = re.sub(r"[ \t　]+", " ", text)
    # 3行以上の連続空行を2行に
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 行頭・行末の空白除去
    lines = [line.strip() for line in text.splitlines()]
    # 空行のみの連続を1つに圧縮
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
    """PDFからテキストを抽出して .txt に保存"""
    import pdfplumber

    print(f"[処理中] {pdf_path.name}")

    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text.append(text)
            if i % 10 == 0 or i == total:
                print(f"  {i}/{total} ページ処理済み", end="\r")

    print()  # 改行

    combined = "\n\n".join(all_text)
    cleaned  = clean_text(combined)

    dest_dir = pdf_path.parent if output_alongside else output_dir
    out_path = dest_dir / (pdf_path.stem + ".txt")
    out_path.write_text(cleaned, encoding="utf-8")

    line_count = cleaned.count("\n") + 1
    char_count  = len(cleaned)
    print(f"  → {total}ページ / {line_count}行 / {char_count}文字 / 保存: {out_path}")
    return out_path


def collect_pdf_files(inputs: list[str]) -> list[Path]:
    """引数からPDFファイルのリストを収集"""
    files = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files.extend(sorted(p.glob("**/*.pdf")))
        elif p.is_file() and p.suffix.lower() == ".pdf":
            files.append(p)
        else:
            print(f"[スキップ] {inp}（PDFファイルではないか存在しない）")
    # 重複除去
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser(description="デジタルPDFからクリーンテキストを抽出")
    parser.add_argument("inputs", nargs="+", help="PDFファイルまたはフォルダのパス")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="出力先フォルダ")
    parser.add_argument("--output-alongside", action="store_true", help="ソースファイルと同じフォルダに出力")
    args = parser.parse_args()

    output_dir = None
    if not args.output_alongside:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    files = collect_pdf_files(args.inputs)
    if not files:
        print("処理対象のPDFファイルが見つからなかったわ。")
        sys.exit(1)

    print(f"対象ファイル: {len(files)} 件")
    if args.output_alongside:
        print("出力先: 各ソースファイルと同じフォルダ")
    else:
        print(f"出力先: {output_dir}")
    print()

    results = []
    for pdf_path in files:
        try:
            out = extract_pdf(pdf_path, output_dir, args.output_alongside)
            results.append((pdf_path.name, True))
        except Exception as e:
            print(f"  [エラー] {e}")
            results.append((pdf_path.name, False))

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
