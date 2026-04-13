#!/usr/bin/env python3
"""絵文字の量×位置テスト - 同じセリフで prefix / sandwich / heavy 比較"""
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PYTHON = "D:/irodori/emoji/.venv/Scripts/python.exe"
INFER = "D:/irodori/emoji/infer.py"
OUTPUT_DIR = Path("D:/irodori/tests/emoji_position_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# VoiceDesign 白雨キャプション（クール・低めの声）
CAPTION = "若い女性が、クールで低めの落ち着いた声で、芯の強さを持って話している。"

# テストケース: 3段階の感情強度 × 4パターンの絵文字配置
TEST_CASES = [
    # ===== 軽い感情（scene_01: 自信・威圧）=====
    {
        "name": "light",
        "base_text": "さあ……来なさい！　この誇りを、砕いてみせるといいわ！",
        "caption": CAPTION,
        "cfg_text": 3.0, "cfg_caption": 3.0,
        "patterns": {
            "A_prefix_少": "😤 さあ……来なさい！　この誇りを、砕いてみせるといいわ！",
            "B_sandwich": "😤💪 さあ……来なさい！　この誇りを、砕いてみせるといいわ！ 😤",
            "C_prefix_多": "😤💪😠 さあ……来なさい！　この誇りを、砕いてみせるといいわ！",
            "D_sandwich_多": "😤💪😠 さあ……来なさい！　この誇りを、砕いてみせるといいわ！ 💪😤",
        }
    },
    # ===== 中程度（scene_03: 喘ぎ(弱)・恥じらい）=====
    {
        "name": "medium",
        "base_text": "やだ……まんこが勝手に締まって……触手ちんぽを咥え込んでる……恥ずかしい……！",
        "caption": "若い女性が、恥ずかしそうに息を乱しながら、抵抗しつつも感じている声で話している。",
        "cfg_text": 6.0, "cfg_caption": 6.0,
        "patterns": {
            "A_prefix_少": "🥵 やだ……まんこが勝手に締まって……触手ちんぽを咥え込んでる……恥ずかしい……！",
            "B_sandwich": "🥵😖 やだ……まんこが勝手に締まって……触手ちんぽを咥え込んでる……恥ずかしい……！ 🫣",
            "C_prefix_多": "🥵😖🫣💦 やだ……まんこが勝手に締まって……触手ちんぽを咥え込んでる……恥ずかしい……！",
            "D_sandwich_多": "🥵😖🫣 やだ……まんこが勝手に締まって……触手ちんぽを咥え込んでる……恥ずかしい……！ 🥵💦",
        }
    },
    # ===== 強い感情（scene_04: 絶頂・喘ぎ(強)）=====
    {
        "name": "heavy",
        "base_text": "お゛ほぉおっ……お゛ほおおっ……子宮に熱い媚毒がどぷどぷ中出しされて……パンパンに孕んじゃう……！",
        "caption": "若い女性が、感情が限界に達して、声を抑えられずに叫んでいる。",
        "cfg_text": 8.0, "cfg_caption": 8.0,
        "patterns": {
            "A_prefix_少": "🥵 お゛ほぉおっ……お゛ほおおっ……子宮に熱い媚毒がどぷどぷ中出しされて……パンパンに孕んじゃう……！",
            "B_sandwich": "🥵😮\u200d💨💦 お゛ほぉおっ……お゛ほおおっ……子宮に熱い媚毒がどぷどぷ中出しされて……パンパンに孕んじゃう……！ 😭",
            "C_prefix_多": "🥵😮\u200d💨💦😭 お゛ほぉおっ……お゛ほおおっ……子宮に熱い媚毒がどぷどぷ中出しされて……パンパンに孕んじゃう……！",
            "D_sandwich_多": "🥵😮\u200d💨💦 お゛ほぉおっ……お゛ほおおっ……子宮に熱い媚毒がどぷどぷ中出しされて……パンパンに孕んじゃう……！ 😭🥵💦",
        }
    },
]

SEED = 42
NUM_CANDIDATES = 1
NUM_STEPS = 30
CFG_SPEAKER = 5.0


def run_test():
    total = sum(len(tc["patterns"]) for tc in TEST_CASES)
    count = 0
    results = []

    print("=" * 60)
    print("絵文字の量×位置 比較テスト")
    print(f"テストケース: {len(TEST_CASES)}段階 × 4パターン = {total}本")
    print("=" * 60)

    for tc in TEST_CASES:
        name = tc["name"]
        caption = tc["caption"]
        cfg_text = tc["cfg_text"]
        cfg_caption = tc["cfg_caption"]

        print(f"\n{'='*50}")
        print(f"感情レベル: {name}")
        print(f"ベーステキスト: {tc['base_text'][:40]}...")
        print(f"CFG: text={cfg_text}, caption={cfg_caption}")
        print(f"{'='*50}")

        for pattern_name, text in tc["patterns"].items():
            count += 1
            filename = f"{name}_{pattern_name}.wav"
            output_path = OUTPUT_DIR / filename

            print(f"\n[{count}/{total}] {pattern_name}")
            print(f"  テキスト: {text[:60]}...")

            cmd = [
                PYTHON, INFER,
                "--hf-checkpoint", "Aratako/Irodori-TTS-500M-v2-VoiceDesign",
                "--codec-repo", "Aratako/Semantic-DACVAE-Japanese-32dim",
                "--text", text,
                "--caption", caption,
                "--no-ref",
                "--seed", str(SEED),
                "--num-steps", str(NUM_STEPS),
                "--num-candidates", str(NUM_CANDIDATES),
                "--cfg-scale-text", str(cfg_text),
                "--cfg-scale-caption", str(cfg_caption),
                "--cfg-scale-speaker", str(CFG_SPEAKER),
                "--model-precision", "bf16",
                "--output-wav", str(output_path),
                "--no-show-timings",
            ]

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            try:
                start = time.time()
                proc = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=180,
                    env=env, encoding="utf-8", errors="replace"
                )
                elapsed = time.time() - start

                if proc.returncode == 0 and output_path.exists():
                    size_kb = output_path.stat().st_size / 1024
                    print(f"  -> [OK] {elapsed:.1f}s, {size_kb:.0f}KB")
                    results.append({
                        "level": name, "pattern": pattern_name,
                        "file": filename, "time": f"{elapsed:.1f}s",
                        "size_kb": f"{size_kb:.0f}", "status": "OK"
                    })
                else:
                    print(f"  -> [FAIL] {proc.stderr[-200:]}")
                    results.append({
                        "level": name, "pattern": pattern_name,
                        "file": filename, "status": "FAIL"
                    })
            except subprocess.TimeoutExpired:
                print(f"  -> [TIMEOUT]")
                results.append({
                    "level": name, "pattern": pattern_name,
                    "file": filename, "status": "TIMEOUT"
                })

    # レポート出力
    print("\n" + "=" * 60)
    print("テスト結果サマリー")
    print("=" * 60)

    report_lines = [
        "# 絵文字の量×位置 比較テスト結果",
        f"日時: 2026-04-13",
        f"シード: {SEED}",
        f"モデル: VoiceDesign (Aratako/Irodori-TTS-500M-v2-VoiceDesign)",
        "",
        "## パターン説明",
        "| パターン | 説明 |",
        "|---|---|",
        "| A_prefix_少 | 絵文字1個を前方のみ |",
        "| B_sandwich | 絵文字2-3個を前後に配置（サンドイッチ） |",
        "| C_prefix_多 | 絵文字3-5個を全て前方に配置 |",
        "| D_sandwich_多 | 絵文字5個以上を前後に多めに配置 |",
        "",
        "## 結果",
        "| レベル | パターン | ファイル | 生成時間 | サイズ | 状態 |",
        "|---|---|---|---|---|---|",
    ]

    for r in results:
        report_lines.append(
            f"| {r['level']} | {r['pattern']} | {r['file']} | "
            f"{r.get('time', '-')} | {r.get('size_kb', '-')}KB | {r['status']} |"
        )

    report_lines.extend([
        "",
        "## 聴き比べチェックポイント",
        "- [ ] 感情の「入り」（冒頭の表現力）",
        "- [ ] 感情の「出」（末尾の余韻・着地）",
        "- [ ] 全体の感情強度（弱・中・強の差が出ているか）",
        "- [ ] 不自然なノイズ・アーティファクト",
        "- [ ] 間（ま）の自然さ",
        "",
        "## 音声ファイル場所",
        f"`{OUTPUT_DIR}`",
    ])

    report_path = OUTPUT_DIR / "EMOJI_POSITION_TEST_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\nレポート: {report_path}")
    print(f"音声ファイル: {OUTPUT_DIR}")

    for r in results:
        status_icon = "✅" if r["status"] == "OK" else "❌"
        print(f"  {status_icon} {r['level']}/{r['pattern']}: {r['status']}")


if __name__ == "__main__":
    run_test()
