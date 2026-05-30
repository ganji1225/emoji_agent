#!/usr/bin/env python3
"""Grok繝悶Μ繝・ず繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・- Grok竊斐ヱ繧､繝励Λ繧､繝ｳ髢薙・繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ邂｡逅・
讓呎ｺ悶Ρ繝ｼ繧ｯ繝輔Ο繝ｼ:
  1. init     : 繝励Ο繧ｸ繧ｧ繧ｯ繝医↓grok/繝輔か繝ｫ繝繧剃ｽ懈・縲∵欠遉ｺ譖ｸ繝・Φ繝励Ξ繝ｼ繝医ｒ驟咲ｽｮ
  2. prepare  : project_brief.json 竊・grok/prompt.md 繧堤函謌・  3. validate : grok/response.json 縺ｮ繝舌Μ繝・・繧ｷ繝ｧ繝ｳ
  4. process  : grok/response.json 竊・production.csv 竊・繧ｭ繝｣繝励す繝ｧ繝ｳ驕ｩ逕ｨ
  5. status   : 迴ｾ蝨ｨ縺ｮ騾ｲ謐励ｒ陦ｨ遉ｺ
"""
import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")
AGENTS_DIR = Path("E:/irodori/agents")
TEMPLATE_DIR = AGENTS_DIR / "templates"


# ============================================================
# 1. init: grok/ 繝輔か繝ｫ繝縺ｨ繝・Φ繝励Ξ繝ｼ繝医ｒ驟咲ｽｮ
# ============================================================
def init_grok_workspace(project_name: str) -> None:
    """繝励Ο繧ｸ繧ｧ繧ｯ繝医↓grok/繝輔か繝ｫ繝繧剃ｽ懈・縺励∵欠遉ｺ譖ｸ繝・Φ繝励Ξ繝ｼ繝医ｒ驟咲ｽｮ縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    grok_dir.mkdir(parents=True, exist_ok=True)

    # 繝・Φ繝励Ξ繝ｼ繝医ｒ繧ｳ繝斐・
    template_src = TEMPLATE_DIR / "grok_prompt_template.md"
    if template_src.exists():
        dest = grok_dir / "prompt_template.md"
        if not dest.exists():
            shutil.copy2(template_src, dest)
            print(f"[ok] 繝・Φ繝励Ξ繝ｼ繝磯・鄂ｮ: {dest}")
        else:
            print(f"[skip] 繝・Φ繝励Ξ繝ｼ繝域里蟄・ {dest}")
    else:
        print(f"[warn] 繝・Φ繝励Ξ繝ｼ繝医′隕九▽縺九ｊ縺ｾ縺帙ｓ: {template_src}")

    # 遨ｺ縺ｮ response.json 繝励Ξ繝ｼ繧ｹ繝帙Ν繝
    response_file = grok_dir / "response.json"
    if not response_file.exists():
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        print(f"[ok] 繝ｬ繧ｹ繝昴Φ繧ｹ繝輔ぃ繧､繝ｫ菴懈・: {response_file}")

    print(f"\n[ok] Grok繝ｯ繝ｼ繧ｯ繧ｹ繝壹・繧ｹ蛻晄悄蛹門ｮ御ｺ・ {grok_dir}")
    print(f"\n谺｡縺ｮ繧ｹ繝・ャ繝・")
    print(f"  1. grok/prompt_template.md 繧偵き繧ｹ繧ｿ繝槭う繧ｺ縺励※ grok/prompt.md 繧剃ｽ懈・")
    print(f"  2. Grok縺ｫ prompt.md 繧呈ｸ｡縺励※JSON蜃ｺ蜉帙ｒ蜿門ｾ・)
    print(f"  3. 蜃ｺ蜉帙ｒ grok/response.json 縺ｫ菫晏ｭ・)
    print(f"  4. python grok_bridge.py validate {project_name}")


# ============================================================
# 2. prepare: project_brief.json 竊・grok/prompt.md
# ============================================================
def prepare_prompt(project_name: str) -> None:
    """project_brief.json 縺悟ｭ伜惠縺吶ｌ縺ｰ planner.py 縺ｧ謖・､ｺ譖ｸ繧堤函謌舌＠ grok/ 縺ｫ驟咲ｽｮ"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    grok_dir.mkdir(parents=True, exist_ok=True)

    brief_path = project_dir / "project_brief.json"
    if not brief_path.exists():
        print(f"[info] project_brief.json 縺檎┌縺・◆繧√√ユ繝ｳ繝励Ξ繝ｼ繝医°繧臥峩謗･邱ｨ髮・＠縺ｦ縺上□縺輔＞")
        print(f"  繝・Φ繝励Ξ繝ｼ繝・ {grok_dir / 'prompt_template.md'}")
        return

    # planner.py 縺ｮ generate_grok_prompt 繧貞他縺ｶ
    sys.path.insert(0, str(AGENTS_DIR))
    from planner import generate_grok_prompt
    generate_grok_prompt(project_dir)

    # 逕滓・縺輔ｌ縺・grok_prompt.md 繧・grok/ 縺ｫ繧ゅさ繝斐・
    src = project_dir / "grok_prompt.md"
    if src.exists():
        dest = grok_dir / "prompt.md"
        shutil.copy2(src, dest)
        print(f"[ok] 謖・､ｺ譖ｸ繧・grok/ 縺ｫ繧ｳ繝斐・: {dest}")


# ============================================================
# 3. validate: Grok縺ｮ蜃ｺ蜉妍SON繧偵ヰ繝ｪ繝・・繧ｷ繝ｧ繝ｳ
# ============================================================
REQUIRED_FIELDS = {"scene_id", "line_id", "speaker", "emotion_tags", "text_raw"}
OPTIONAL_FIELDS = {"emoji_suggestion"}
VALID_EMOTIONS = {
    "閾ｪ菫｡", "螽∝悸", "謖醍匱", "蜍墓昭", "諱先・, "邨ｶ譛・, "蠑ｷ縺後ｊ", "鬩壹″", "諤偵ｊ",
    "辣ｧ繧・, "諱･縺倥ｉ縺・, "蝗ｰ諠・, "繧ゅ§繧ゅ§",
    "逕倥∴", "蝗√″", "縺九ｉ縺九≧", "蜆ｪ縺励＞",
    "蜷先・", "蝟倥℃", "蝟倥℃(蠑ｱ)", "蝟倥℃(蠑ｷ)", "諱ｯ蛻・ｌ", "闕偵＞諱ｯ驕｣縺・,
    "豕｣縺・, "蝸壼朕", "豸吝｣ｰ",
    "邨ｶ鬆・, "蜿ｫ縺ｳ", "謔ｲ魑ｴ", "闍ｦ縺励＞", "蟠ｩ螢・,
    "謾ｾ蠢・, "閼ｱ蜉・, "譛ｦ譛ｧ", "陌夊┳", "螳牙ｵ",
    "闊梧遠縺｡", "蜚ｾ繧帝｣ｲ繧", "繝ｪ繝・・", "縺ゅ￥縺ｳ",
    "諡堤ｵｶ", "螻郁ｾｱ", "謚ｵ謚・, "諛・｡・,
}

def validate_response(project_name: str) -> dict:
    """grok/response.json 繧偵ヰ繝ｪ繝・・繧ｷ繝ｧ繝ｳ縺励∝撫鬘檎せ繧貞ｱ蜻翫☆繧・""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"
    response_path = grok_dir / "response.json"

    # script_raw_grok.json 縺九ｉ繧りｪｭ縺ｿ霎ｼ縺ｿ蜿ｯ閭ｽ・亥ｾ梧婿莠呈鋤・・    if not response_path.exists():
        alt_path = project_dir / "script_raw_grok.json"
        if alt_path.exists():
            response_path = alt_path
            print(f"[info] grok/response.json 縺檎┌縺・◆繧・{alt_path.name} 繧剃ｽｿ逕ｨ")
        else:
            print(f"[error] 繝ｬ繧ｹ繝昴Φ繧ｹ繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ")
            print(f"  譛溷ｾ・ヱ繧ｹ: {response_path}")
            print(f"  莉｣譖ｿ繝代せ: {alt_path}")
            return {"valid": False}

    with open(response_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"[error] JSON驟榊・縺ｧ縺ｯ縺ゅｊ縺ｾ縺帙ｓ・亥梛: {type(data).__name__}・・)
        return {"valid": False}

    if len(data) == 0:
        print(f"[warn] JSON縺檎ｩｺ縺ｧ縺吶・rok縺ｮ蜃ｺ蜉帙ｒ response.json 縺ｫ雋ｼ繧贋ｻ倥￠縺ｦ縺上□縺輔＞")
        return {"valid": False, "empty": True}

    errors = []
    warnings = []
    scenes = set()
    emotion_counter = {}

    for i, entry in enumerate(data):
        line_label = f"陦鶏i+1}"

        # 蠢・医ヵ繧｣繝ｼ繝ｫ繝峨メ繧ｧ繝・け
        for field in REQUIRED_FIELDS:
            if field not in entry or not str(entry[field]).strip():
                errors.append(f"{line_label}: 蠢・医ヵ繧｣繝ｼ繝ｫ繝・'{field}' 縺檎ｩｺ縺ｧ縺・)

        # scene_id 繝√ぉ繝・け
        sid = entry.get("scene_id", "")
        scenes.add(sid)

        # emotion_tags 繝√ぉ繝・け
        tags_str = entry.get("emotion_tags", "")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        for tag in tags:
            emotion_counter[tag] = emotion_counter.get(tag, 0) + 1
            if tag not in VALID_EMOTIONS:
                warnings.append(f"{line_label}: 譛ｪ螳夂ｾｩ縺ｮ諢滓ュ繧ｿ繧ｰ '{tag}'")

        # 繝・く繧ｹ繝磯聞繝√ぉ繝・け
        text = entry.get("text_raw", "")
        if len(text) > 60:
            warnings.append(f"{line_label}: 繝・く繧ｹ繝医′髟ｷ縺・({len(text)}譁・ｭ・: {text[:40]}...")
        if len(text) < 3:
            warnings.append(f"{line_label}: 繝・く繧ｹ繝医′遏ｭ縺吶℃ ({len(text)}譁・ｭ・")

        # emoji_suggestion 繝√ぉ繝・け
        emoji = entry.get("emoji_suggestion", "")
        if emoji and text not in emoji:
            warnings.append(f"{line_label}: emoji_suggestion 縺ｫ繝・く繧ｹ繝医′蜷ｫ縺ｾ繧後※縺・∪縺帙ｓ")

    # 繝ｬ繝昴・繝・    print(f"\n{'='*50}")
    print(f"繝舌Μ繝・・繧ｷ繝ｧ繝ｳ邨先棡: {response_path.name}")
    print(f"{'='*50}")
    print(f"  邱剰｡梧焚: {len(data)}")
    print(f"  繧ｷ繝ｼ繝ｳ謨ｰ: {len(scenes)}")
    print(f"  繧ｨ繝ｩ繝ｼ: {len(errors)}莉ｶ")
    print(f"  隴ｦ蜻・ {len(warnings)}莉ｶ")

    emoji_filled = sum(1 for e in data if e.get("emoji_suggestion", "").strip())
    print(f"  emoji_suggestion 險伜・邇・ {emoji_filled}/{len(data)} ({emoji_filled/len(data)*100:.0f}%)")

    if errors:
        print(f"\n[繧ｨ繝ｩ繝ｼ]")
        for e in errors[:10]:
            print(f"  笶・{e}")
        if len(errors) > 10:
            print(f"  ... 莉・{len(errors)-10} 莉ｶ")

    if warnings:
        print(f"\n[隴ｦ蜻馨")
        for w in warnings[:15]:
            print(f"  笞・・ {w}")
        if len(warnings) > 15:
            print(f"  ... 莉・{len(warnings)-15} 莉ｶ")

    # 諢滓ュ繧ｿ繧ｰ蛻・ｸ・    print(f"\n  諢滓ュ繧ｿ繧ｰ TOP10:")
    sorted_emotions = sorted(emotion_counter.items(), key=lambda x: -x[1])
    for tag, count in sorted_emotions[:10]:
        marker = "" if tag in VALID_EMOTIONS else " 笞・乗悴螳夂ｾｩ"
        print(f"    {tag}: {count}蝗桀marker}")

    is_valid = len(errors) == 0
    print(f"\n{'笨・繝舌Μ繝・・繧ｷ繝ｧ繝ｳ騾夐℃' if is_valid else '笶・繧ｨ繝ｩ繝ｼ縺ゅｊ 窶・菫ｮ豁｣縺悟ｿ・ｦ√〒縺・}")

    return {
        "valid": is_valid,
        "total": len(data),
        "scenes": len(scenes),
        "errors": len(errors),
        "warnings": len(warnings),
        "emoji_fill_rate": emoji_filled / len(data) if data else 0,
    }


# ============================================================
# 4. process: response.json 竊・production.csv 竊・繧ｭ繝｣繝励す繝ｧ繝ｳ驕ｩ逕ｨ
# ============================================================
def process_response(project_name: str, num_candidates: int = 1) -> None:
    """Grok蜃ｺ蜉帙ｒ繝代う繝励Λ繧､繝ｳ縺ｫ騾壹＠縺ｦproduction.csv繧堤函謌舌☆繧・
    蜃ｦ逅・ヵ繝ｭ繝ｼ:
      1. grok/response.json 竊・script_raw.json 縺ｫ繧ｳ繝斐・
      2. script_processor.py 縺ｧ production.csv 繧堤函謌・      3. captions.json 縺悟ｭ伜惠縺吶ｌ縺ｰ繧ｭ繝｣繝励す繝ｧ繝ｳ閾ｪ蜍暮←逕ｨ
    """
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"

    # 繝ｬ繧ｹ繝昴Φ繧ｹ繝輔ぃ繧､繝ｫ繧呈爾縺・    response_path = grok_dir / "response.json"
    if not response_path.exists():
        alt_path = project_dir / "script_raw_grok.json"
        if alt_path.exists():
            response_path = alt_path
        else:
            print(f"[error] Grok蜃ｺ蜉帙′隕九▽縺九ｊ縺ｾ縺帙ｓ")
            return

    # 繝舌Μ繝・・繧ｷ繝ｧ繝ｳ
    result = validate_response(project_name)
    if not result.get("valid"):
        print(f"\n[abort] 繝舌Μ繝・・繧ｷ繝ｧ繝ｳ繧ｨ繝ｩ繝ｼ縺ｮ縺溘ａ蜃ｦ逅・ｒ荳ｭ豁｢縺励∪縺・)
        return

    # script_raw.json 縺ｫ繧ｳ繝斐・・・cript_processor 縺瑚ｪｭ繧讓呎ｺ悶ヱ繧ｹ・・    dest = project_dir / "script_raw.json"
    shutil.copy2(response_path, dest)
    print(f"\n[ok] {response_path.name} 竊・script_raw.json 繧ｳ繝斐・")

    # script_processor.py 縺ｧ production.csv 逕滓・
    sys.path.insert(0, str(AGENTS_DIR))
    from script_processor import process_script
    csv_path = process_script(project_name)

    if not csv_path:
        print(f"[error] production.csv 縺ｮ逕滓・縺ｫ螟ｱ謨励＠縺ｾ縺励◆")
        return

    # 繧ｭ繝｣繝励す繝ｧ繝ｳ閾ｪ蜍暮←逕ｨ
    captions_path = project_dir / "captions.json"
    if captions_path.exists():
        _apply_captions(project_dir, captions_path, num_candidates)
    else:
        print(f"\n[info] captions.json 縺檎┌縺・◆繧√√く繝｣繝励す繝ｧ繝ｳ縺ｯ譛ｪ險ｭ螳壹〒縺・)
        print(f"  casting.py 縺ｾ縺溘・謇句虚縺ｧ險ｭ螳壹＠縺ｦ縺上□縺輔＞")

    print(f"\n{'='*50}")
    print(f"繝代う繝励Λ繧､繝ｳ蜃ｦ逅・ｮ御ｺ・ｼ・)
    print(f"  production.csv: {project_dir / 'production.csv'}")
    print(f"\n谺｡縺ｮ繧ｹ繝・ャ繝・")
    print(f"  python recorder.py {project_name}  -- 髻ｳ螢ｰ逕滓・")


def _apply_captions(project_dir: Path, captions_path: Path, num_candidates: int = 1) -> None:
    """captions.json 縺ｮ intensity_profiles 繧・production.csv 縺ｫ驕ｩ逕ｨ縺吶ｋ"""
    with open(captions_path, "r", encoding="utf-8") as f:
        captions = json.load(f)

    profiles = captions.get("intensity_profiles", {})
    if not profiles:
        print(f"[warn] captions.json 縺ｫ intensity_profiles 縺後≠繧翫∪縺帙ｓ")
        return

    prod_csv = project_dir / "production.csv"
    with open(prod_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    stats = {}
    for row in rows:
        notes = row.get("notes", "")
        m = re.search(r"intensity=(\w+)", notes)
        intensity = m.group(1) if m else "medium"

        profile = profiles.get(intensity, profiles.get("medium", {}))
        row["caption"] = profile.get("caption", "")
        row["cfg_text"] = str(profile.get("cfg_text", 3.0))
        row["cfg_caption"] = str(profile.get("cfg_caption", 3.0))
        row["cfg_speaker"] = str(profile.get("cfg_speaker", 5.0))
        row["cfg_guidance_mode"] = profile.get("cfg_guidance_mode", "alternating")
        row["num_steps"] = str(profile.get("num_steps", 40))
        # LoRA 縺ｯ繝励Ο繝輔ぃ繧､繝ｫ縺ｧ謖・ｮ壹＆繧後◆蝣ｴ蜷医・縺ｿ譖ｸ縺崎ｾｼ繧・域欠螳壹↑縺励・遨ｺ縺ｮ縺ｾ縺ｾ・・        if "lora_path" in profile:
            row["lora_path"] = profile.get("lora_path", "")
            row["lora_scale"] = str(profile.get("lora_scale", 1.0)) if profile.get("lora_path") else ""
        row["num_candidates"] = str(num_candidates)

        stats[intensity] = stats.get(intensity, 0) + 1

    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[ok] 繧ｭ繝｣繝励す繝ｧ繝ｳ驕ｩ逕ｨ: {len(rows)}陦・)
    for k, v in sorted(stats.items()):
        p = profiles.get(k, {})
        print(f"  {k}: {v}陦・(cfg_text={p.get('cfg_text')}, cfg_caption={p.get('cfg_caption')})")
    print(f"  num_candidates={num_candidates}")


# ============================================================
# 5. status: 繝励Ο繧ｸ繧ｧ繧ｯ繝医・ Grok 繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ騾ｲ謐・# ============================================================
def show_status(project_name: str) -> None:
    """Grok繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ縺ｮ騾ｲ謐励ｒ陦ｨ遉ｺ縺吶ｋ"""
    project_dir = PROJECTS_DIR / project_name
    grok_dir = project_dir / "grok"

    print(f"\n{'='*50}")
    print(f"Grok繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ迥ｶ豕・ {project_name}")
    print(f"{'='*50}")

    checks = [
        ("grok/繝輔か繝ｫ繝", grok_dir.exists()),
        ("grok/prompt.md (謖・､ｺ譖ｸ)", (grok_dir / "prompt.md").exists() or (project_dir / "grok_prompt.md").exists()),
        ("grok/response.json", _check_response(grok_dir / "response.json") or _check_response(project_dir / "script_raw_grok.json")),
        ("production.csv", (project_dir / "production.csv").exists()),
        ("captions.json", (project_dir / "captions.json").exists()),
    ]

    for label, ok in checks:
        status = "笨・ if ok else "筮・
        print(f"  {status} {label}")

    # production.csv 縺ｮ迥ｶ諷・    prod_csv = project_dir / "production.csv"
    if prod_csv.exists():
        with open(prod_csv, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        status_counts = {}
        for r in rows:
            s = r.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        print(f"\n  production.csv 陦梧焚: {len(rows)}")
        for s, c in sorted(status_counts.items()):
            print(f"    {s}: {c}陦・)

    # audio 繝輔か繝ｫ繝繝√ぉ繝・け
    for audio_name in ["audio", "audio_grok", "audio_agent"]:
        audio_dir = project_dir / audio_name
        if audio_dir.exists():
            wav_count = len(list(audio_dir.rglob("*.wav")))
            print(f"\n  {audio_name}/: {wav_count} wav繝輔ぃ繧､繝ｫ")


def _check_response(path: Path) -> bool:
    """繝ｬ繧ｹ繝昴Φ繧ｹ繝輔ぃ繧､繝ｫ縺悟ｭ伜惠縺励∫ｩｺ縺ｧ縺ｪ縺・°"""
    if not path.exists():
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return isinstance(data, list) and len(data) > 0
    except Exception:
        return False


# ============================================================
# CLI
# ============================================================
USAGE = """Grok Bridge - Grok竊斐ヱ繧､繝励Λ繧､繝ｳ 繝ｯ繝ｼ繧ｯ繝輔Ο繝ｼ邂｡逅・
Usage:
  python grok_bridge.py init     <project>                    -- grok/繝輔か繝ｫ繝蛻晄悄蛹・  python grok_bridge.py prepare  <project>                    -- 謖・､ｺ譖ｸ逕滓・ (project_brief.json 竊・grok/prompt.md)
  python grok_bridge.py validate <project>                    -- Grok蜃ｺ蜉帙ヰ繝ｪ繝・・繧ｷ繝ｧ繝ｳ
  python grok_bridge.py process  <project> [--candidates N]   -- 繝代う繝励Λ繧､繝ｳ蜃ｦ逅・(response.json 竊・production.csv)
  python grok_bridge.py status   <project>                    -- 騾ｲ謐礼｢ｺ隱・
讓呎ｺ悶Ρ繝ｼ繧ｯ繝輔Ο繝ｼ:
  1. init     竊・grok/ 繝輔か繝ｫ繝縺ｨ繝・Φ繝励Ξ繝ｼ繝医ｒ驟咲ｽｮ
  2. prepare  竊・project_brief.json 縺九ｉ謖・､ｺ譖ｸ繧堤函謌・(縺ｾ縺溘・謇句虚縺ｧ grok/prompt.md 繧剃ｽ懈・)
  3. (莠ｺ髢・   竊・Grok縺ｫ謖・､ｺ譖ｸ繧呈ｸ｡縺励゛SON蜃ｺ蜉帙ｒ grok/response.json 縺ｫ菫晏ｭ・  4. validate 竊・JSON縺ｮ繝舌Μ繝・・繧ｷ繝ｧ繝ｳ
  5. process  竊・production.csv 逕滓・ + 繧ｭ繝｣繝励す繝ｧ繝ｳ驕ｩ逕ｨ
  6. (蜿朱鹸)   竊・python recorder.py <project> 縺ｧ髻ｳ螢ｰ逕滓・
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]

    if cmd == "init":
        init_grok_workspace(project_name)
    elif cmd == "prepare":
        prepare_prompt(project_name)
    elif cmd == "validate":
        validate_response(project_name)
    elif cmd == "process":
        num_candidates = 3
        if "--candidates" in sys.argv:
            idx = sys.argv.index("--candidates")
            if idx + 1 < len(sys.argv):
                num_candidates = int(sys.argv[idx + 1])
        process_response(project_name, num_candidates=num_candidates)
    elif cmd == "status":
        show_status(project_name)
    else:
        print(f"Unknown command: {cmd}")
        print(USAGE)
        sys.exit(1)
