#!/usr/bin/env python3
"""邨ｵ譁・ｭ励・驥湘嶺ｽ咲ｽｮ繝・せ繝・- 蜷後§繧ｻ繝ｪ繝輔〒 prefix / sandwich / heavy 豈碑ｼ・""
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PYTHON = "E:/irodori/emoji/.venv/Scripts/python.exe"
INFER = "E:/irodori/emoji/infer.py"
OUTPUT_DIR = Path("E:/irodori/tests/emoji_position_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# VoiceDesign 逋ｽ髮ｨ繧ｭ繝｣繝励す繝ｧ繝ｳ・医け繝ｼ繝ｫ繝ｻ菴弱ａ縺ｮ螢ｰ・・CAPTION = "闍･縺・･ｳ諤ｧ縺後√け繝ｼ繝ｫ縺ｧ菴弱ａ縺ｮ關ｽ縺｡逹縺・◆螢ｰ縺ｧ縲∬官縺ｮ蠑ｷ縺輔ｒ謖√▲縺ｦ隧ｱ縺励※縺・ｋ縲・

# 繝・せ繝医こ繝ｼ繧ｹ: 3谿ｵ髫弱・諢滓ュ蠑ｷ蠎ｦ ﾃ・4繝代ち繝ｼ繝ｳ縺ｮ邨ｵ譁・ｭ鈴・鄂ｮ
TEST_CASES = [
    # ===== 霆ｽ縺・─諠・ｼ・cene_01: 閾ｪ菫｡繝ｻ螽∝悸・・====
    {
        "name": "light",
        "base_text": "縺輔≠窶ｦ窶ｦ譚･縺ｪ縺輔＞・√縺薙・隱・ｊ繧偵∫輔＞縺ｦ縺ｿ縺帙ｋ縺ｨ縺・＞繧擾ｼ・,
        "caption": CAPTION,
        "cfg_text": 3.0, "cfg_caption": 3.0,
        "patterns": {
            "A_prefix_蟆・: "丶 縺輔≠窶ｦ窶ｦ譚･縺ｪ縺輔＞・√縺薙・隱・ｊ繧偵∫輔＞縺ｦ縺ｿ縺帙ｋ縺ｨ縺・＞繧擾ｼ・,
            "B_sandwich": "丶潮 縺輔≠窶ｦ窶ｦ譚･縺ｪ縺輔＞・√縺薙・隱・ｊ繧偵∫輔＞縺ｦ縺ｿ縺帙ｋ縺ｨ縺・＞繧擾ｼ・丶",
            "C_prefix_螟・: "丶潮丐 縺輔≠窶ｦ窶ｦ譚･縺ｪ縺輔＞・√縺薙・隱・ｊ繧偵∫輔＞縺ｦ縺ｿ縺帙ｋ縺ｨ縺・＞繧擾ｼ・,
            "D_sandwich_螟・: "丶潮丐 縺輔≠窶ｦ窶ｦ譚･縺ｪ縺輔＞・√縺薙・隱・ｊ繧偵∫輔＞縺ｦ縺ｿ縺帙ｋ縺ｨ縺・＞繧擾ｼ・潮丶",
        }
    },
    # ===== 荳ｭ遞句ｺｦ・・cene_03: 蝟倥℃(蠑ｱ)繝ｻ諱･縺倥ｉ縺・ｼ・====
    {
        "name": "medium",
        "base_text": "繧・□窶ｦ窶ｦ縺ｾ繧薙％縺悟享謇九↓邱縺ｾ縺｣縺ｦ窶ｦ窶ｦ隗ｦ謇九■繧薙⊃繧貞徴縺郁ｾｼ繧薙〒繧銀ｦ窶ｦ諱･縺壹°縺励＞窶ｦ窶ｦ・・,
        "caption": "闍･縺・･ｳ諤ｧ縺後∵▼縺壹°縺励◎縺・↓諱ｯ繧剃ｹｱ縺励↑縺後ｉ縲∵慣謚励＠縺､縺､繧よ─縺倥※縺・ｋ螢ｰ縺ｧ隧ｱ縺励※縺・ｋ縲・,
        "cfg_text": 6.0, "cfg_caption": 6.0,
        "patterns": {
            "A_prefix_蟆・: "･ｵ 繧・□窶ｦ窶ｦ縺ｾ繧薙％縺悟享謇九↓邱縺ｾ縺｣縺ｦ窶ｦ窶ｦ隗ｦ謇九■繧薙⊃繧貞徴縺郁ｾｼ繧薙〒繧銀ｦ窶ｦ諱･縺壹°縺励＞窶ｦ窶ｦ・・,
            "B_sandwich": "･ｵ・ 繧・□窶ｦ窶ｦ縺ｾ繧薙％縺悟享謇九↓邱縺ｾ縺｣縺ｦ窶ｦ窶ｦ隗ｦ謇九■繧薙⊃繧貞徴縺郁ｾｼ繧薙〒繧銀ｦ窶ｦ諱･縺壹°縺励＞窶ｦ窶ｦ・・ｫ｣",
            "C_prefix_螟・: "･ｵ・ｫ｣懲 繧・□窶ｦ窶ｦ縺ｾ繧薙％縺悟享謇九↓邱縺ｾ縺｣縺ｦ窶ｦ窶ｦ隗ｦ謇九■繧薙⊃繧貞徴縺郁ｾｼ繧薙〒繧銀ｦ窶ｦ諱･縺壹°縺励＞窶ｦ窶ｦ・・,
            "D_sandwich_螟・: "･ｵ・ｫ｣ 繧・□窶ｦ窶ｦ縺ｾ繧薙％縺悟享謇九↓邱縺ｾ縺｣縺ｦ窶ｦ窶ｦ隗ｦ謇九■繧薙⊃繧貞徴縺郁ｾｼ繧薙〒繧銀ｦ窶ｦ諱･縺壹°縺励＞窶ｦ窶ｦ・・･ｵ懲",
        }
    },
    # ===== 蠑ｷ縺・─諠・ｼ・cene_04: 邨ｶ鬆ゅ・蝟倥℃(蠑ｷ)・・====
    {
        "name": "heavy",
        "base_text": "縺翫・縺ｻ縺峨♀縺｣窶ｦ窶ｦ縺翫・縺ｻ縺翫♀縺｣窶ｦ窶ｦ蟄仙ｮｮ縺ｫ辭ｱ縺・ｪ壽ｯ偵′縺ｩ縺ｷ縺ｩ縺ｷ荳ｭ蜃ｺ縺励＆繧後※窶ｦ窶ｦ繝代Φ繝代Φ縺ｫ蟄輔ｓ縺倥ｃ縺・ｦ窶ｦ・・,
        "caption": "闍･縺・･ｳ諤ｧ縺後∵─諠・′髯千阜縺ｫ驕斐＠縺ｦ縲∝｣ｰ繧呈椛縺医ｉ繧後★縺ｫ蜿ｫ繧薙〒縺・ｋ縲・,
        "cfg_text": 8.0, "cfg_caption": 8.0,
        "patterns": {
            "A_prefix_蟆・: "･ｵ 縺翫・縺ｻ縺峨♀縺｣窶ｦ窶ｦ縺翫・縺ｻ縺翫♀縺｣窶ｦ窶ｦ蟄仙ｮｮ縺ｫ辭ｱ縺・ｪ壽ｯ偵′縺ｩ縺ｷ縺ｩ縺ｷ荳ｭ蜃ｺ縺励＆繧後※窶ｦ窶ｦ繝代Φ繝代Φ縺ｫ蟄輔ｓ縺倥ｃ縺・ｦ窶ｦ・・,
            "B_sandwich": "･ｵ舒\u200d暢懲 縺翫・縺ｻ縺峨♀縺｣窶ｦ窶ｦ縺翫・縺ｻ縺翫♀縺｣窶ｦ窶ｦ蟄仙ｮｮ縺ｫ辭ｱ縺・ｪ壽ｯ偵′縺ｩ縺ｷ縺ｩ縺ｷ荳ｭ蜃ｺ縺励＆繧後※窶ｦ窶ｦ繝代Φ繝代Φ縺ｫ蟄輔ｓ縺倥ｃ縺・ｦ窶ｦ・・亊",
            "C_prefix_螟・: "･ｵ舒\u200d暢懲亊 縺翫・縺ｻ縺峨♀縺｣窶ｦ窶ｦ縺翫・縺ｻ縺翫♀縺｣窶ｦ窶ｦ蟄仙ｮｮ縺ｫ辭ｱ縺・ｪ壽ｯ偵′縺ｩ縺ｷ縺ｩ縺ｷ荳ｭ蜃ｺ縺励＆繧後※窶ｦ窶ｦ繝代Φ繝代Φ縺ｫ蟄輔ｓ縺倥ｃ縺・ｦ窶ｦ・・,
            "D_sandwich_螟・: "･ｵ舒\u200d暢懲 縺翫・縺ｻ縺峨♀縺｣窶ｦ窶ｦ縺翫・縺ｻ縺翫♀縺｣窶ｦ窶ｦ蟄仙ｮｮ縺ｫ辭ｱ縺・ｪ壽ｯ偵′縺ｩ縺ｷ縺ｩ縺ｷ荳ｭ蜃ｺ縺励＆繧後※窶ｦ窶ｦ繝代Φ繝代Φ縺ｫ蟄輔ｓ縺倥ｃ縺・ｦ窶ｦ・・亊･ｵ懲",
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
    print("邨ｵ譁・ｭ励・驥湘嶺ｽ咲ｽｮ 豈碑ｼ・ユ繧ｹ繝・)
    print(f"繝・せ繝医こ繝ｼ繧ｹ: {len(TEST_CASES)}谿ｵ髫・ﾃ・4繝代ち繝ｼ繝ｳ = {total}譛ｬ")
    print("=" * 60)

    for tc in TEST_CASES:
        name = tc["name"]
        caption = tc["caption"]
        cfg_text = tc["cfg_text"]
        cfg_caption = tc["cfg_caption"]

        print(f"\n{'='*50}")
        print(f"諢滓ュ繝ｬ繝吶Ν: {name}")
        print(f"繝吶・繧ｹ繝・く繧ｹ繝・ {tc['base_text'][:40]}...")
        print(f"CFG: text={cfg_text}, caption={cfg_caption}")
        print(f"{'='*50}")

        for pattern_name, text in tc["patterns"].items():
            count += 1
            filename = f"{name}_{pattern_name}.wav"
            output_path = OUTPUT_DIR / filename

            print(f"\n[{count}/{total}] {pattern_name}")
            print(f"  繝・く繧ｹ繝・ {text[:60]}...")

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

    # 繝ｬ繝昴・繝亥・蜉・    print("\n" + "=" * 60)
    print("繝・せ繝育ｵ先棡繧ｵ繝槭Μ繝ｼ")
    print("=" * 60)

    report_lines = [
        "# 邨ｵ譁・ｭ励・驥湘嶺ｽ咲ｽｮ 豈碑ｼ・ユ繧ｹ繝育ｵ先棡",
        f"譌･譎・ 2026-04-13",
        f"繧ｷ繝ｼ繝・ {SEED}",
        f"繝｢繝・Ν: VoiceDesign (Aratako/Irodori-TTS-500M-v2-VoiceDesign)",
        "",
        "## 繝代ち繝ｼ繝ｳ隱ｬ譏・,
        "| 繝代ち繝ｼ繝ｳ | 隱ｬ譏・|",
        "|---|---|",
        "| A_prefix_蟆・| 邨ｵ譁・ｭ・蛟九ｒ蜑肴婿縺ｮ縺ｿ |",
        "| B_sandwich | 邨ｵ譁・ｭ・-3蛟九ｒ蜑榊ｾ後↓驟咲ｽｮ・医し繝ｳ繝峨う繝・メ・・|",
        "| C_prefix_螟・| 邨ｵ譁・ｭ・-5蛟九ｒ蜈ｨ縺ｦ蜑肴婿縺ｫ驟咲ｽｮ |",
        "| D_sandwich_螟・| 邨ｵ譁・ｭ・蛟倶ｻ･荳翫ｒ蜑榊ｾ後↓螟壹ａ縺ｫ驟咲ｽｮ |",
        "",
        "## 邨先棡",
        "| 繝ｬ繝吶Ν | 繝代ち繝ｼ繝ｳ | 繝輔ぃ繧､繝ｫ | 逕滓・譎る俣 | 繧ｵ繧､繧ｺ | 迥ｶ諷・|",
        "|---|---|---|---|---|---|",
    ]

    for r in results:
        report_lines.append(
            f"| {r['level']} | {r['pattern']} | {r['file']} | "
            f"{r.get('time', '-')} | {r.get('size_kb', '-')}KB | {r['status']} |"
        )

    report_lines.extend([
        "",
        "## 閨ｴ縺肴ｯ斐∋繝√ぉ繝・け繝昴う繝ｳ繝・,
        "- [ ] 諢滓ュ縺ｮ縲悟・繧翫搾ｼ亥・鬆ｭ縺ｮ陦ｨ迴ｾ蜉幢ｼ・,
        "- [ ] 諢滓ュ縺ｮ縲悟・縲搾ｼ域忰蟆ｾ縺ｮ菴咎渊繝ｻ逹蝨ｰ・・,
        "- [ ] 蜈ｨ菴薙・諢滓ュ蠑ｷ蠎ｦ・亥ｼｱ繝ｻ荳ｭ繝ｻ蠑ｷ縺ｮ蟾ｮ縺悟・縺ｦ縺・ｋ縺具ｼ・,
        "- [ ] 荳崎・辟ｶ縺ｪ繝弱う繧ｺ繝ｻ繧｢繝ｼ繝・ぅ繝輔ぃ繧ｯ繝・,
        "- [ ] 髢難ｼ医∪・峨・閾ｪ辟ｶ縺・,
        "",
        "## 髻ｳ螢ｰ繝輔ぃ繧､繝ｫ蝣ｴ謇",
        f"`{OUTPUT_DIR}`",
    ])

    report_path = OUTPUT_DIR / "EMOJI_POSITION_TEST_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n繝ｬ繝昴・繝・ {report_path}")
    print(f"髻ｳ螢ｰ繝輔ぃ繧､繝ｫ: {OUTPUT_DIR}")

    for r in results:
        status_icon = "笨・ if r["status"] == "OK" else "笶・
        print(f"  {status_icon} {r['level']}/{r['pattern']}: {r['status']}")


if __name__ == "__main__":
    run_test()
