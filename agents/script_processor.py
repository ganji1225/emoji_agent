#!/usr/bin/env python3
"""閼壽悽蜃ｦ逅・お繝ｼ繧ｸ繧ｧ繝ｳ繝・- Grok縺ｮ逕溷床譛ｬ・・SON/CSV/TXT・峨ｄ繧ｲ繝ｼ繝繝・く繧ｹ繝・.md)繧・邨ｵ譁・ｭ嶺ｻ倥″production.csv縺ｫ螟画鋤縺吶ｋ縲・繧ｵ繝ｳ繝峨う繝・メ譁ｹ蠑・ 諢滓ュ蠑ｷ蠎ｦ縺ｫ蠢懊§縺ｦ prefix + 繝・く繧ｹ繝・+ suffix 縺ｧ邨ｵ譁・ｭ励ｒ驟咲ｽｮ
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("E:/irodori/projects")

# ============================================================
# 諢滓ュ繧ｭ繝ｼ繝ｯ繝ｼ繝・竊・邨ｵ譁・ｭ励・繝・ヴ繝ｳ繧ｰ・亥・繧ｿ繧ｰ繝槭ャ繝∵婿蠑擾ｼ・# ============================================================
EMOTION_EMOJI_MAP = [
    # 蜉ｹ譫憺浹繝ｻ諱ｯ驕｣縺・ｳｻ
    (r"蝗√″|縺輔＆繧・″|閠ｳ蜈ポ縺ｲ縺昴・縺掟繧ｦ繧｣繧ｹ繝代・", "曹"),
    (r"蜷先・|貅懈・|縺溘ａ諱ｯ|蟇晄・", "舒\u200d暢"),
    (r"蝟倥℃\(蠑ｷ\)|蝟倥℃・亥ｼｷ・・, "･ｵ"),
    (r"蝟倥℃\(蠑ｱ\)|蝟倥℃・亥ｼｱ・・, "･ｵ"),
    (r"蝟倥℃|縺ゅ∴縺旨闕偵＞諱ｯ|縺・ａ縺・, "･ｵ"),
    (r"諱ｯ蛻・ｌ|闕偵＞諱ｯ驕｣縺л縺ｯ縺√・縺・, "舒\u200d暢"),
    (r"諱ｯ繧偵・繧|繝上ャ", "舒"),
    (r"闊舌ａ|縺ｺ繧鋼縺｡繧・・|豌ｴ髻ｳ", "槽"),
    (r"繝ｪ繝・・|繧ｭ繧ｹ|蜚・縺｡繧・, "昼"),
    (r"蜥ｳ|縺上＠繧・∩|繧ｴ繝斈繧ｳ繝・, "､ｧ"),
    (r"蝴･荳弓縺斐￥繧掛鬟ｲ縺ｿ霎ｼ|縺舌・縺｣", "･､"),
    (r"繧ｨ繧ｳ繝ｼ|繝ｪ繝舌・繝翻髻ｿ縺楯縺薙□縺ｾ", "討"),
    (r"髮ｻ隧ｱ雜翫＠|髮ｻ隧ｱ蜿｣|蜿苓ｩｱ蝎ｨ", "到"),
    (r"繧・▲縺上ｊ|荳∝ｯｧ縺ｫ|蝎帙∩邱繧－荳隱樔ｸ隱・, "世"),
    (r"譌ｩ蜿｣|縺ｾ縺上＠縺溘※|荳豌励↓|遏｢邯吶℃譌ｩ", "竢ｩ"),
    # 諢滓ュ繝ｻ隧ｱ縺玲婿邉ｻ
    (r"隨代＞|縺上☆縺上☆|縺ｵ縺ｵ|繧ｯ繧ｹ繝ポ蜷ｫ縺ｿ隨・, "､ｭ"),
    (r"逕倥∴", "・"),
    (r"縺九ｉ縺九≧|縺九ｉ縺九＞|縺・◆縺壹ｉ|蟆乗が鬲・, "・"),
    (r"諱･縺壹°縺慾辣ｧ繧芸繧ゅ§繧ゅ§|繝・Ξ|諱･縺倥ｉ縺・, "ｫ｣"),
    (r"髴・∴|縺翫←縺翫←|閾ｪ菫｡縺ｪ", "･ｺ"),
    (r"豕｣縺鋼豕｣縺楯蝸壼朕|豸吝｣ｰ", "亊"),
    (r"謔ｲ魑ｴ|蜿ｫ縺ｳ|邨ｶ蜿ｫ|繧ｭ繝｣繝ｼ", "亞"),
    (r"諤偵ｊ|諤偵ｋ|荳肴ｺ|繧､繝ｩ繧､繝ｩ|諡励・", "丐"),
    (r"鬩壹″|縺ｳ縺｣縺上ｊ|縺医▲", "亟"),
    (r"蜆ｪ縺慾遨上ｄ縺弓諷医＠縺ｿ", "ｫｶ"),
    (r"逵縺л縺繧九＞|縺ｾ縺ｩ繧阪∩|蟇晁ｵｷ縺・, "亂"),
    (r"諷後※|繝代ル繝・け|縺ｩ繧ゅｊ|辟ｦ", "于"),
    (r"蝟懊・|螫峨＠|讌ｽ縺慾繧ｦ繧ｭ繧ｦ繧ｭ", "・"),
    (r"諛・｡・縺企｡倥＞|鬆ｼ繧", "剌"),
    (r"驟培縺ｻ繧埼・縺・, "･ｴ"),
    (r"蜿｣繧貞｡桍縺上＄繧ゅ▲", "､・),
    (r"螳牙ｵ|縺ｻ縺｣|貅雜ｳ|螳牙ｿ・, "・"),
    (r"逍大撫|荳肴晁ｭｰ|鬥悶°縺励￡", "､・),
    (r"闍ｦ縺慾逞斈縺・≦", "・"),
    (r"蠢・・|荳榊ｮ峨◎縺・, "弌"),
    (r"蜻・ｌ|繧・ｌ繧・ｌ", "刋"),
    (r"謾ｾ蠢ポ陌夊┳|譛ｦ譛ｧ|閼ｱ蜉・, "・"),
    (r"諡堤ｵｶ|諡貞凄", "亞"),
    (r"螻郁ｾｱ|蟠ｩ螢・, "亊"),
    (r"邨ｶ譛・, "亊"),
    (r"邨ｶ鬆・, "亞"),
    (r"蜍墓昭", "于"),
    (r"諱先・, "亞"),
    (r"蠑ｷ縺後ｊ", "丶"),
    (r"閾ｪ菫｡|螽∝悸|謖醍匱", "丶"),
    (r"謚ｵ謚・, "・"),
    (r"蝗ｰ諠・, "・"),
    # 繧ｨ繝輔ぉ繧ｯ繝・    (r"懲|豎慾豼｡", "懲"),
    # 蠎・＞諢滓ュ・域怙蠕鯉ｼ・    (r"譏弱ｋ縺л蜈・ｰ慾繝上く繝上く", "・"),
    (r"譌･蟶ｸ|譎ｮ騾嘶騾壼ｸｸ|繝翫Ξ繝ｼ繧ｷ繝ｧ繝ｳ", ""),
]

# ============================================================
# 諢滓ュ蠑ｷ蠎ｦ縺ｮ蛻､螳壹く繝ｼ繝ｯ繝ｼ繝・# ============================================================
INTENSITY_STRONG = {
    "蝟倥℃(蠑ｷ)", "蝟倥℃・亥ｼｷ・・, "邨ｶ鬆・, "蜿ｫ縺ｳ", "蝸壼朕", "闕偵＞諱ｯ驕｣縺・,
    "蟠ｩ螢・, "邨ｶ蜿ｫ", "騾｣邯夂ｵｶ鬆・,
}
INTENSITY_MEDIUM = {
    "蝟倥℃(蠑ｱ)", "蝟倥℃・亥ｼｱ・・, "諱･縺倥ｉ縺・, "蝗ｰ諠・, "蜍墓昭", "諱先・,
    "謚ｵ謚・, "諡堤ｵｶ", "螻郁ｾｱ", "邨ｶ譛・,
}
INTENSITY_EXTREME = {
    "蜃ｺ逕｣", "蜈ｨ遨ｴ蜷梧凾", "騾｣邯夂ｵｶ鬆・, "螯雁ｨ",
}


def classify_intensity(emotion_tags: list[str]) -> str:
    """諢滓ュ繧ｿ繧ｰ繝ｪ繧ｹ繝医°繧牙ｼｷ蠎ｦ繝ｬ繝吶Ν繧貞愛螳壹☆繧・""
    tag_set = set(emotion_tags)
    if tag_set & INTENSITY_EXTREME:
        return "extreme"
    # 蠑ｷ縺・ち繧ｰ縺・蛟倶ｻ･荳・or 蠑ｷ縺・ち繧ｰ + 荳ｭ繧ｿ繧ｰ = strong
    strong_count = len(tag_set & INTENSITY_STRONG)
    medium_count = len(tag_set & INTENSITY_MEDIUM)
    if strong_count >= 2:
        return "strong"
    if strong_count >= 1 and medium_count >= 1:
        return "strong"
    if strong_count >= 1:
        return "medium"
    if medium_count >= 1:
        return "medium"
    return "weak"


def emotion_to_emojis_all(emotion: str) -> list[str]:
    """諢滓ュ繝・く繧ｹ繝医°繧牙・繝槭ャ繝√☆繧狗ｵｵ譁・ｭ励ｒ繝ｪ繧ｹ繝医〒霑斐☆・磯㍾隍・賜髯､・・""
    if not emotion:
        return []
    emojis = []
    seen = set()
    # 繧ｹ繝壹・繧ｹ縺ｾ縺溘・繧ｫ繝ｳ繝槭〒蛻・牡縺励※蜷・ち繧ｰ繧貞・逅・    tags = re.split(r"[,縲―s]+", emotion.strip())
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        for pattern, emoji in EMOTION_EMOJI_MAP:
            if re.search(pattern, tag):
                if emoji and emoji not in seen:
                    emojis.append(emoji)
                    seen.add(emoji)
                break
    return emojis


def build_sandwich(text: str, emojis: list[str], intensity: str, stacking: bool = False) -> str:
    """繝・せ繝育ｵ先棡縺ｫ蝓ｺ縺･縺・◆繧ｵ繝ｳ繝峨う繝・メ譁ｹ蠑上〒邨ｵ譁・ｭ励ｒ驟咲ｽｮ縺吶ｋ

    閨ｴ縺肴ｯ斐∋繝・せ繝育ｵ先棡・・026-04-13 + 2026-04-15・・
      蠑ｱ: prefix 2, suffix 1 縺梧怙驕ｩ
      荳ｭ: prefix 2-3, suffix 1 縺悟ｮ牙ｮ・      蠑ｷ: prefix 3, suffix 2 縺梧怙驕ｩ・・蛟倶ｻ･荳翫・繝弱う繧ｺ蠅暦ｼ・      讌ｵ髯・ prefix 3, suffix 2・域э蝗ｳ逧・↓繝弱う繧ｺ繧貞・繧後◆縺・ｴ蜷医・縺ｿ4蛟具ｼ・
    驥崎ｦ√↑逋ｺ隕具ｼ・026-04-15 閨ｴ縺肴ｯ斐∋・・
      - 邨ｵ譁・ｭ・-3蛟九′諢滓ュ蟷・′螟ｧ縺阪￥螳牙ｮ・      - 4蛟倶ｻ･荳翫・荳崎・辟ｶ縺ｪ髻ｳ螢ｰ繧・ヮ繧､繧ｺ縺悟｢怜刈
      - 邨ｵ譁・ｭ玲焚縺悟､壹＞縺ｨ蜷先・繝ｻ螢ｰ縺ｫ縺ｪ繧峨↑縺・浹螢ｰ縺悟｢励∴繧・
    繧ｹ繧ｿ繝・く繝ｳ繧ｰ繝・け繝九ャ繧ｯ・亥・蠑拾MOJI_ANNOTATIONS.md 2026-03-24遒ｺ隱搾ｼ・
      stacking=True 縺ｮ蝣ｴ蜷医∫ｵｵ譁・ｭ励ｒ2蝗樣㍾縺ｭ縺ｦ蜉ｹ譫懊ｒ蠑ｷ隱ｿ縺吶ｋ
      萓・ 曹 竊・曹曹 縺ｧ繧医ｊ蠑ｷ縺・宦縺榊柑譫・      窶ｻ 邱乗焚3蛟倶ｻ･蜀・・繝ｫ繝ｼ繝ｫ繧堤ｶｭ謖√☆繧九◆繧・prefix 繧貞榊刈縺吶ｋ
    """
    if not emojis:
        return text

    # 繧ｹ繧ｿ繝・く繝ｳ繧ｰ繝・け繝九ャ繧ｯ: 邨ｵ譁・ｭ・蛟九・蝣ｴ蜷医↓2蝗樣㍾縺ｭ縺ｦ蜉ｹ譫懷ｼｷ隱ｿ
    # 萓・ [曹] 竊・prefix="曹曹", suffix="" (邱乗焚2蛟九〒繝ｫ繝ｼ繝ｫ蜀・
    if stacking and len(emojis) == 1:
        prefix = emojis[0] * 2
        suffix = ""
        result = f"{prefix} {text}"
        return result

    if intensity == "weak":
        # prefix 2, suffix 1
        prefix = "".join(emojis[:2])
        suffix = emojis[-1] if len(emojis) >= 2 else ""
    elif intensity == "medium":
        # prefix 2-3, suffix 1
        prefix = "".join(emojis[:3])
        suffix = emojis[-1] if len(emojis) >= 2 else ""
    elif intensity == "strong":
        # prefix 3, suffix 2・井ｸ企剞蜴ｳ螳茨ｼ・        prefix = "".join(emojis[:3])
        suffix_emojis = emojis[-2:] if len(emojis) >= 2 else emojis[-1:]
        suffix = "".join(suffix_emojis)
        if "懲" not in suffix:
            suffix += "懲"
    else:  # extreme
        # prefix 4, suffix 4・・026-04-22 閨ｴ縺肴ｯ斐∋: 4+4 ﾃ・CFG=6 縺ｧ諢滓ュ陦ｨ迴ｾ竊代・縺九☆繧梧椛蛻ｶ・・        # CFG縺ｯcaptions.json縺ｧ6.0繧定ｨｭ螳壹☆繧九％縺ｨ・・.0竊・.0・・        e = (emojis * 4)[:8]  # 8蛟句・縺ｫ諡｡蠑ｵ・育ｵｵ譁・ｭ励′雜ｳ繧翫↑縺代ｌ縺ｰ郢ｰ繧願ｿ斐＠・・        prefix = "".join(e[:4])
        suffix = "".join(e[4:8])

    result = f"{prefix} {text}"
    if suffix:
        result += f" {suffix}"
    return result


def normalize_text(text: str) -> str:
    """繝・く繧ｹ繝医ｒ豁｣隕丞喧縺吶ｋ・・TS蜷代￠・・""
    text = text.strip()
    text = re.sub(r"\.{3,}", "窶ｦ", text)
    text = re.sub(r"縲・2,}", "縲・, text)
    text = text.strip("縲後阪弱十"")
    # Grok縺悟沂繧∬ｾｼ繧薙□邨ｵ譁・ｭ励ｒ髯､蜴ｻ・・ext_raw縺ｯ繧ｯ繝ｪ繝ｼ繝ｳ縺ｫ菫昴▽・・    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U00002702-\U000027B0"  # dingbats
        "\U0000FE00-\U0000FE0F"  # variation selectors
        "\U0000200D"             # zero width joiner
        "\U00002640-\U00002642"  # gender symbols
        "\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text).strip()
    # 貍｢蟄苓ｪｭ縺ｿ髢馴＆縺・ｯｾ遲・ TTS 縺瑚ｪ､隱ｭ縺励ｄ縺吶＞蜊倩ｪ槭ｒ縺ｲ繧峨′縺ｪ/繧ｫ繧ｿ繧ｫ繝翫↓螟画鋤
    text = _fix_kanji_reading(text)
    return text


# TTS隱､隱ｭ縺励ｄ縺吶＞貍｢蟄・竊・縺ｲ繧峨′縺ｪ/繧ｫ繧ｿ繧ｫ繝雁､画鋤繝・・繝悶Ν
# 蜿り・ https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku
KANJI_FIX_MAP = [
    (r"莉頑律", "縺阪ｇ縺・),
    (r"譏ｨ譌･", "縺阪・縺・),
    (r"譏取律", "縺ゅ＠縺・),
    (r"荳莠ｺ", "縺ｲ縺ｨ繧・),
    (r"莠御ｺｺ", "縺ｵ縺溘ｊ"),
    (r"螟ｧ莠ｺ", "縺翫→縺ｪ"),
    (r"荳頑焔", "縺倥ｇ縺・★"),
    (r"荳区焔", "縺ｸ縺・),
    (r"髮鷹ｭ・, "繧ｶ繧ｳ"),
    (r"逖ｴ豌・, "縺励ｇ縺・″"),
    (r"髴雁ｱｱ", "繧後＞縺悶ｓ"),
    (r"逡ｪ莠ｺ", "縺ｰ繧薙↓繧・),
    (r"陝ｲ", "繧縺・),
    (r"雍・, "縺ｫ縺・),
    (r"闍怜ｺ・, "縺ｪ縺医←縺・),
    (r"蟄ｵ蛹・, "縺ｵ縺・),
    (r"阡・, "縺､繧・),
    (r"郢ｭ", "縺ｾ繧・),
    (r"蟐夊脈", "縺ｳ繧・￥"),
    (r"陷倩屁", "縺上ｂ"),
]


def _fix_kanji_reading(text: str) -> str:
    """TTS 縺瑚ｪ､隱ｭ縺励ｄ縺吶＞貍｢蟄励ｒ縺ｲ繧峨′縺ｪ/繧ｫ繧ｿ繧ｫ繝翫↓螟画鋤縺吶ｋ"""
    for kanji, reading in KANJI_FIX_MAP:
        text = text.replace(kanji, reading)
    return text


# ============================================================
# 髢難ｼ医∪・峨・閾ｪ蜍墓諺蜈･
# ============================================================
def insert_pause_markers(text: str, max_pauses: int = 2) -> str:
    """蜿･隱ｭ轤ｹ繧・娯ｦ窶ｦ縲阪・菴咲ｽｮ縺ｫ 竢ｸ・擾ｼ磯俣・峨・繝ｼ繧ｫ繝ｼ繧呈諺蜈･縺吶ｋ

    蜿り・ Irodori-TTS 縺ｧ縺ｯ莉･荳九・邨ｵ譁・ｭ励′迚ｹ谿雁柑譫懊→縺励※讖溯・縺吶ｋ・亥・蠑拾MOJI_ANNOTATIONS遒ｺ隱肴ｸ医∩・・      竢ｸ・・= 髢薙・豐磯ｻ呻ｼ域─諠・・螟峨ｏ繧顔岼縺ｮ逶ｴ蜑阪↓謖ｿ蜈･・・      竢ｩ = 譌ｩ蜿｣繝ｻ縺ｾ縺上＠縺溘※繧具ｼ域・縺ｦ繝ｻ闊亥･ｮ繧ｷ繝ｼ繝ｳ縺ｫ・・      世 = 繧・▲縺上ｊ繝ｻ荳∝ｯｧ縺ｫ・亥剱縺ｿ邱繧√ｋ繧医≧縺ｪ隱槭ｊ縺九￠縺ｫ・・
    Args:
        text: 蟇ｾ雎｡繝・く繧ｹ繝・        max_pauses: 1陦後≠縺溘ｊ縺ｮ譛螟ｧ竢ｸ・乗諺蜈･謨ｰ・医ョ繝輔か繝ｫ繝・・・            - 0: 謖ｿ蜈･縺ｪ縺・            - 2: 繝・ヵ繧ｩ繝ｫ繝医よ─諠・・螟峨ｏ繧顔岼2邂・園縺ｫ邨槭ｋ・域耳螂ｨ・・            - 騾｣邯壼・逕滓凾縺ｯ繧ｻ繝ｪ繝輔′髟ｷ縺乗─縺倥ｋ縺溘ａ繝・ヵ繧ｩ繝ｫ繝・縺梧怙驕ｩ
            - 閨ｴ縺肴ｯ斐∋繝輔ぅ繝ｼ繝峨ヰ繝・け(2026-04-17): 竢ｸ・丞､夂畑縺ｧ髟ｷ縺輔′豌励↓縺ｪ繧・    """
    if max_pauses == 0:
        return text

    count = 0
    result = []
    # 縲娯ｦ窶ｦ縲阪〒蛻・牡縺励※蜃ｦ逅・    parts = re.split(r"(窶ｦ窶ｦ)", text)
    for i, part in enumerate(parts):
        if part == "窶ｦ窶ｦ":
            # 譛ｫ蟆ｾ・域ｬ｡縺ｮ繝代・繝医′遨ｺ or 縲鯉ｼ峨搾ｼ峨・繧ｹ繧ｭ繝・・
            next_part = parts[i + 1] if i + 1 < len(parts) else ""
            if next_part and not next_part.startswith("・・) and count < max_pauses:
                result.append("窶ｦ窶ｦ 竢ｸ・・")
                count += 1
            else:
                result.append("窶ｦ窶ｦ")
        else:
            result.append(part)
    return "".join(result)


# ============================================================
# 繝・く繧ｹ繝亥・螳ｹ縺九ｉ諢滓ュ繧定・蜍墓耳螳壹☆繧・# ============================================================
EMOTION_INFERENCE_RULES = [
    # 讌ｵ髯千ｳｻ・亥━蜈茨ｼ・    (r"繧薙・縺ｻ繧斈縺翫・縺ｻ繧斈縺ｯ繧帙ｓ繧斈縺舌・縺翫・|縺ゅ・縺ｲ繧斈繧薙・縺翫・", "蝟倥℃(蠑ｷ),邨ｶ鬆・闕偵＞諱ｯ驕｣縺・),
    (r"縺ゅ・縺ゅ・|縺ｯ繧帙≠繧斈縺ゅ・縺翫・", "蝟倥℃(蠑ｷ),蜿ｫ縺ｳ,蝸壼朕"),
    (r"繧､繧ｭ迢・螢翫ｌ縺毫螢翫＠縺ｦ|貅ｶ縺代ｋ|貅ｶ縺代■繧ポ縺ｶ縺｣螢・, "邨ｶ鬆・蜿ｫ縺ｳ,蝟倥℃(蠑ｷ),蟠ｩ螢・),
    (r"繧､繝・■繧・≧|繧､縺｣縺｡繧ポ繧､繧ｭ縺昴≧|繧､繧ｯ", "邨ｶ鬆・蜿ｫ縺ｳ,蝟倥℃(蠑ｷ)"),
    (r"蟄輔∪縺帙※|蟄輔∩縺溘＞|逕｣縺ｾ縺帙※|逕｣縺ｿ縺溘＞", "邨ｶ鬆・蝸壼朕,諛・｡・),
    # 蠑ｷ縺・ｳｻ
    (r"繧薙≠縺－繧薙♀縺榎縺ゅ＝縺－縺翫♂縺・, "蝟倥℃(蠑ｷ),邨ｶ鬆・),
    (r"豌玲戟縺｡縺・＞.*豁｢縺ｾ繧榎蠢ｫ讌ｽ.*貅ｺ繧芸蠢ｫ讌ｽ.*譛鬮・, "蝟倥℃(蠑ｷ),邨ｶ鬆・陌夊┳"),
    (r"蟄仙ｮｮ.*逍ｼ|蟄仙ｮｮ.*逞呎肇|蟄仙ｮｮ.*邱縺ｾ", "蝟倥℃(蠑ｷ),諱･縺倥ｉ縺・),
    (r"縺翫∪繧薙％.*繝偵け繝偵け|縺翫∪繧薙％.*縺ｳ縺上・縺・, "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"豈堺ｹｳ.*蝎ｴ|豈堺ｹｳ.*謳ｾ|荵ｳ鬥・*蜷ｸ", "蝟倥℃(蠑ｷ),諱･縺倥ｉ縺・),
    (r"蜊ｵ.*繝代Φ繝代Φ|縺願・.*閹ｨ|縺願・.*繝代Φ繝代Φ", "邨ｶ鬆・蝟倥℃(蠑ｷ),蝸壼朕"),
    # 荳ｭ遞句ｺｦ
    (r"縺ｯ縺・*縺ｯ縺－縺ｯ縺√ｓ", "蝟倥℃(蠑ｱ),闕偵＞諱ｯ驕｣縺・),
    (r"繧薙▲.*縺ｯ縺－縺ゅｓ縺｣", "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"豌玲戟縺｡縺・＞|豌玲戟縺｡謔ｪ縺・*豌玲戟縺｡縺・, "蝟倥℃(蠑ｱ),蝗ｰ諠・),
    (r"雖後↑縺ｮ縺ｫ.*豌玲戟縺｡|雖・*縺ｧ繧・, "蝗ｰ諠・諱･縺倥ｉ縺・),
    (r"諱･縺壹°縺慾諱･縺壹°縺・, "諱･縺倥ｉ縺・),
    (r"辭ｱ縺・*菴倒菴・*辭ｱ縺л辭ｱ縺上※", "蝟倥℃(蠑ｱ),蝗ｰ諠・),
    (r"諢帶ｶｲ|豼｡繧芸縺舌■繧・縺ｬ繧九〓繧弓縺ｬ繧・, "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"繧ゅ▲縺ｨ.*谺ｲ縺慾繧ゅ▲縺ｨ.*縺励※|繧ゅ▲縺ｨ.*迥ｯ", "蝟倥℃(蠑ｷ),逕倥∴,諛・｡・),
    (r"隱・ｊ.*縺・ｉ縺ｪ縺л隱・ｊ.*縺ｩ縺・〒繧・逡ｪ莠ｺ.*繧ゅ≧", "邨ｶ譛・陌夊┳"),
    (r"謌ｻ繧翫◆縺上↑縺л謌ｻ繧後↑縺л莠ｺ髢薙§繧・, "陌夊┳,謾ｾ蠢・),
    # 蠑ｱ縺・ｳｻ
    (r"繧・ａ縺ｦ|髮｢縺励※|髮｢繧後↑縺輔＞|謾ｾ縺励※", "諱先・諡堤ｵｶ"),
    (r"縺励∪縺｣縺毫縺ｾ縺壹＞", "鬩壹″,諱先・),
    (r"諤悶＞|諱舌ｍ縺・, "諱先・),
    (r"雖・*繧・□|繧・□", "諱先・諡堤ｵｶ"),
    (r"蜉帙′.*蜈･繧峨↑縺л蜍輔￠縺ｪ縺л蜍輔°縺ｪ縺л謚ｵ謚励〒縺阪↑縺・, "邨ｶ譛・諱先・),
    (r"繧ゅ≧.*縺繧－繧ゅ≧.*髯千阜", "邨ｶ譛・蝟倥℃(蠑ｱ)"),
    (r"縺ｾ縺.*雋縺掃縺ｾ縺.*謌ｦ縺医ｋ|謚ｵ謚・*縺吶ｋ", "蠑ｷ縺後ｊ"),
    # 莠句ｾ檎ｳｻ
    (r"豌ｸ驕縺ｫ.*迥ｯ縺輔ｌ|豌ｸ驕縺ｫ.*貅ｺ繧芸縺壹▲縺ｨ.*蠢ｫ讌ｽ", "謾ｾ蠢・陌夊┳,逕倥∴"),
    (r"繧ゅ≧.*縺・＞縺九↑|繧ゅ≧.*縺・＞縺九ｂ", "謾ｾ蠢・陌夊┳"),
    (r"螢翫ｌ縺溽ｬ代∩|陌壹ｍ縺ｪ逶ｮ", "謾ｾ蠢・陌夊┳"),
    # 霄ｫ菴灘渚蠢懃ｳｻ・亥ｼｱ縲應ｸｭ縺ｮ陬懷ｮ鯉ｼ・    (r"縺翫∪繧薙％|縺ｾ繧薙％|蟄仙ｮｮ|繧ｯ繝ｪ", "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"荵ｳ鬥翻豈堺ｹｳ|荵ｳ|閭ｸ.*蜷ｸ", "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"邊俶ｶｲ|縺ｬ繧－縺ｬ繧弓縺ｹ縺｡繧・, "蝗ｰ諠・諱･縺倥ｉ縺・),
    (r"蟐夊脈|蟐壽ｯ竹逕倥＞.*豸ｲ|蛻・ｳ梧ｶｲ", "蝗ｰ諠・蝟倥℃(蠑ｱ)"),
    (r"蠢ｫ讌ｽ|豌玲戟縺｡縺・＞|豌玲戟縺｡繧・, "蝟倥℃(蠑ｱ),蝗ｰ諠・),
    (r"逍ｼ|縺・★|繝偵け繝偵け|縺ｳ縺上・縺楯逞呎肇", "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"豼｡繧芸諢帶ｶｲ|縺舌■繧・縺倥ｅ繧・, "蝟倥℃(蠑ｱ),諱･縺倥ｉ縺・),
    (r"隗ｦ謇弓阡倒蟷ｼ陌ｫ|陜ｿ|蜊ｵ", "諱先・蝗ｰ諠・),
    (r"騾吶＞|邨｡縺ｿ|蟾ｻ縺鋼蜷ｸ縺・ｻ・蛹・∩霎ｼ", "諱先・蝗ｰ諠・),
    (r"鬟ｲ縺ｾ縺輔ｌ|豕ｨ縺手ｾｼ|豬√＠霎ｼ", "諱先・蝗ｰ諠・),
    (r"縺雁ｰｻ|繧｢繝翫Ν|蟆ｻ遨ｴ", "諱･縺倥ｉ縺・蝗ｰ諠・),
    (r"闍怜ｺ掛郢∵ｮ翻閧芽｢弓蝎ｨ.*縺ｪ繧・, "邨ｶ譛・陌夊┳"),
    (r"閹ｨ繧榎繝代Φ繝代Φ|縺・▲縺ｱ縺・, "蝟倥℃(蠑ｷ),諱･縺倥ｉ縺・),
    (r"蜃ｺ蜿｣.*隕九∴|縺ゅ→蟆代＠|繧ゅ≧蟆代＠", "辟ｦ繧・蠑ｷ縺後ｊ"),
    (r"雖芸繧・□|縺薙ｓ縺ｪ縺ｮ", "諱先・諡堤ｵｶ"),
    (r"窶ｦ窶ｦ縺｣|縺上▲|縺ゅ▲", "鬩壹″,蜍墓昭"),
    # 繝輔か繝ｼ繝ｫ繝舌ャ繧ｯ
    (r"窶ｦ窶ｦ", "蜍墓昭"),
]


def infer_emotion_from_text(text: str) -> str:
    """繝・く繧ｹ繝亥・螳ｹ縺九ｉ諢滓ュ繧ｿ繧ｰ繧定・蜍墓耳螳壹☆繧・""
    for pattern, emotion in EMOTION_INFERENCE_RULES:
        if re.search(pattern, text):
            return emotion
    return "譌･蟶ｸ"


def load_game_text(filepath: Path) -> list[dict]:
    """繧ｲ繝ｼ繝繝・く繧ｹ繝茨ｼ・md・峨ｒ隗｣譫舌＠縺ｦ繧ｻ繝ｪ繝輔ｒ謚ｽ蜃ｺ縺吶ｋ

    蟇ｾ雎｡陦・
      - ・域峡蠑ｧ縺ｮ迢ｬ逋ｽ・俄・ 謗｡逕ｨ
      - 縲檎匱隧ｱ繧ｻ繝ｪ繝輔坂・ 謗｡逕ｨ・域峡蠑ｧ繧帝勁蜴ｻ・・    髯､螟冶｡・
      - # 繧ｻ繧ｯ繧ｷ繝ｧ繝ｳ繝倥ャ繝 竊・scene_id 縺ｨ縺励※蛻ｩ逕ｨ
      - 縲先ｼ泌・謖・､ｺ縲代燭G縲鯛・ 髯､螟・      - 笘・ヱ繝ｩ繝｡繝ｼ繧ｿ 竊・髯､螟・      - 窶披忍ND窶披・竊・髯､螟・      - --- 竊・髯､螟・      - 繝翫Ξ繝ｼ繧ｷ繝ｧ繝ｳ・亥慍縺ｮ譁・ｼ俄・ 髯､螟・      - 遨ｺ陦・竊・髯､螟・    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []
    current_scene = "scene_01"
    scene_count = 0

    for line in lines:
        l = line.strip()
        if not l:
            continue

        # 繧ｻ繧ｯ繧ｷ繝ｧ繝ｳ繝倥ャ繝 竊・scene_id 譖ｴ譁ｰ
        section_match = re.match(r'^#{1,3}\s+(.+)$', l)
        if section_match:
            section_name = section_match.group(1)
            # scene_id 繧堤函謌撰ｼ・1-mid 竊・s1_mid, S2-ev1 竊・s2_ev1 etc.・・            sid = re.search(r'(S\d+[-_]\w+)', section_name)
            if sid:
                scene_count += 1
                current_scene = sid.group(1).lower().replace('-', '_')
            elif re.search(r'Stage\s*\d', section_name):
                # Stage 繝倥ャ繝縺ｯ繧ｹ繧ｭ繝・・・亥ｭ舌そ繧ｯ繧ｷ繝ｧ繝ｳ縺ｧ scene_id 繧定ｨｭ螳夲ｼ・                pass
            continue

        # 髯､螟冶｡・        if l.startswith('縲・) or l.startswith('笘・) or l.startswith('窶披・) or l == '---':
            continue

        # 迢ｬ逋ｽ: ・・..・・        monologue_match = re.match(r'^・・.+)・・', l)
        if monologue_match:
            text = monologue_match.group(1)
            # 髟ｷ縺・｡後・蛻・牡・・0譁・ｭ苓ｶ・ｼ・            sub_lines = _split_long_text(text, max_len=55)
            for sub in sub_lines:
                emotion = infer_emotion_from_text(sub)
                rows.append({
                    "scene_id": current_scene,
                    "speaker": "逋ｽ髮ｨ",
                    "emotion_tags": emotion,
                    "text_raw": f"・・sub}・・,
                    "line_type": "迢ｬ逋ｽ",
                })
            continue

        # 逋ｺ隧ｱ: 縲・..縲・        speech_match = re.match(r'^縲・.+?)縲・$', l)
        if speech_match:
            text = speech_match.group(1)
            sub_lines = _split_long_text(text, max_len=55)
            for sub in sub_lines:
                emotion = infer_emotion_from_text(sub)
                rows.append({
                    "scene_id": current_scene,
                    "speaker": "逋ｽ髮ｨ",
                    "emotion_tags": emotion,
                    "text_raw": sub,
                    "line_type": "逋ｺ隧ｱ",
                })
            continue

        # 縺昴ｌ莉･螟悶・繝翫Ξ繝ｼ繧ｷ繝ｧ繝ｳ 竊・繧ｹ繧ｭ繝・・

    return rows


def _split_long_text(text: str, max_len: int = 55) -> list[str]:
    """髟ｷ縺・ユ繧ｭ繧ｹ繝医ｒ驕ｩ蛻・↑菴咲ｽｮ縺ｧ蛻・牡縺吶ｋ"""
    if len(text) <= max_len:
        return [text]

    result = []
    # 縲娯ｦ窶ｦ縲阪〒蛻・牡繧定ｩｦ縺ｿ繧・    parts = re.split(r'(窶ｦ窶ｦ)', text)
    current = ""
    for i, part in enumerate(parts):
        if part == "窶ｦ窶ｦ":
            current += part
            # 谺｡縺ｮ繝代・繝医→蜷医ｏ縺帙※髟ｷ縺吶℃繧九↑繧峨√％縺薙〒蛻・ｋ
            remaining = "".join(parts[i+1:]) if i+1 < len(parts) else ""
            if len(current) >= max_len * 0.4 and remaining:
                result.append(current.strip())
                current = ""
        else:
            if len(current + part) > max_len and current:
                result.append(current.strip())
                current = part
            else:
                current += part

    if current.strip():
        result.append(current.strip())

    # 蛻・牡縺ｧ縺阪↑縺九▲縺溷ｴ蜷医・縺昴・縺ｾ縺ｾ霑斐☆
    return result if result else [text]


def load_json(filepath: Path) -> list[dict]:
    """JSON蠖｢蠑上・蜿ｰ譛ｬ繧定ｪｭ縺ｿ霎ｼ繧"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "lines" in data:
        return data["lines"]
    return []


def load_csv(filepath: Path) -> list[dict]:
    """CSV蠖｢蠑上・蜿ｰ譛ｬ繧定ｪｭ縺ｿ霎ｼ繧"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_txt(filepath: Path) -> list[dict]:
    """繝励Ξ繝ｼ繝ｳ繝・く繧ｹ繝亥ｽ｢蠑上ｒ隱ｭ縺ｿ霎ｼ繧・育ｩｺ陦後〒繧ｷ繝ｼ繝ｳ蛹ｺ蛻・ｊ・・""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    rows = []
    scene_num = 1
    for line in lines:
        line = line.strip()
        if not line:
            scene_num += 1
            continue
        rows.append({
            "scene_id": f"scene_{scene_num:02d}",
            "speaker": "繧ｭ繝｣繝ｩ",
            "emotion_note": "譌･蟶ｸ",
            "text_raw": line,
        })
    return rows


def process_script(project_name: str, ignore_grok_emoji: bool = False,
                    use_pause_markers: bool = True) -> str:
    """蜿ｰ譛ｬ繝輔ぃ繧､繝ｫ繧定ｪｭ縺ｿ霎ｼ繧薙〒 production.csv 繧堤函謌舌☆繧・
    蟇ｾ蠢懷ｽ｢蠑擾ｼ亥━蜈磯・ｼ・
      1. script_raw.json  (謗ｨ螂ｨ: Grok JSON蜃ｺ蜉・
      2. script_raw.csv
      3. script_raw.txt

    Args:
        project_name: 繝励Ο繧ｸ繧ｧ繧ｯ繝亥錐
        ignore_grok_emoji: True 縺ｮ蝣ｴ蜷医；rok 縺ｮ emoji_suggestion 繧堤┌隕悶＠
            繝代う繝励Λ繧､繝ｳ縺ｮ build_sandwich() 縺ｧ邨ｵ譁・ｭ励ｒ蜀肴ｧ狗ｯ峨☆繧九・            謾ｹ蝟・＆繧後◆繝代う繝励Λ繧､繝ｳ・育ｵｵ譁・ｭ・-3蛟句宛髯舌√せ繧ｿ繝・く繝ｳ繧ｰ遲会ｼ峨ｒ
            Grok迚医ョ繝ｼ繧ｿ縺ｫ驕ｩ逕ｨ縺吶ｋ髫帙↓菴ｿ逕ｨ縲・        use_pause_markers: True 縺ｮ蝣ｴ蜷医√娯ｦ窶ｦ縲堺ｽ咲ｽｮ縺ｫ 竢ｸ・・繧定・蜍墓諺蜈･縺吶ｋ
    """
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"

    raw_json = project_dir / "script_raw.json"
    raw_csv = project_dir / "script_raw.csv"
    raw_txt = project_dir / "script_raw.txt"

    # 隱ｭ縺ｿ霎ｼ縺ｿ
    rows = []
    if raw_json.exists():
        rows = load_json(raw_json)
        print(f"[ok] script_raw.json 繧定ｪｭ縺ｿ霎ｼ縺ｿ縺ｾ縺励◆ ({len(rows)}陦・")
    elif raw_csv.exists():
        rows = load_csv(raw_csv)
        print(f"[ok] script_raw.csv 繧定ｪｭ縺ｿ霎ｼ縺ｿ縺ｾ縺励◆ ({len(rows)}陦・")
    elif raw_txt.exists():
        rows = load_txt(raw_txt)
        print(f"[ok] script_raw.txt 繧定ｪｭ縺ｿ霎ｼ縺ｿ縺ｾ縺励◆ ({len(rows)}陦・")
    else:
        print(f"[error] 蜿ｰ譛ｬ繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {project_dir}")
        print(f"  蟇ｾ蠢懷ｽ｢蠑・ script_raw.json / script_raw.csv / script_raw.txt")
        return ""

    if not rows:
        print("[error] 蜿ｰ譛ｬ縺檎ｩｺ縺ｧ縺・)
        return ""

    # production.csv 縺ｫ螟画鋤
    prod_rows = []
    scene_line_counts = {}
    stats = {"weak": 0, "medium": 0, "strong": 0, "extreme": 0}

    for row in rows:
        scene_id = row.get("scene_id", "scene_01").strip()
        scene_line_counts[scene_id] = scene_line_counts.get(scene_id, 0) + 1
        line_num = scene_line_counts[scene_id]

        # 繝・く繧ｹ繝亥叙蠕暦ｼ・SON: text_raw, CSV: text / text_raw・・        text_raw_orig = row.get("text_raw", row.get("text", ""))
        text_raw = normalize_text(text_raw_orig)

        # 諢滓ュ繧ｿ繧ｰ蜿門ｾ暦ｼ・SON: emotion_tags / emotion_note, CSV: emotion / emotion_note・・        emotion = row.get("emotion_tags",
                  row.get("emotion_note",
                  row.get("emotion", "")))

        # Grok縺ｮ邨ｵ譁・ｭ玲署譯医′縺ゅｌ縺ｰ繝槭・繧ｸ逕ｨ縺ｫ菫晄戟
        grok_emoji = row.get("emoji_suggestion", "")

        # 諢滓ュ繧ｿ繧ｰ繧偵ヱ繝ｼ繧ｹ
        tags = [t.strip() for t in re.split(r"[,縲―s]+", emotion.strip()) if t.strip()]

        # 蠑ｷ蠎ｦ蛻､螳・        intensity = classify_intensity(tags)
        stats[intensity] += 1

        # 邨ｵ譁・ｭ怜､画鋤
        emojis = emotion_to_emojis_all(emotion)

        # 竢ｸ・・髢薙・繝ｼ繧ｫ繝ｼ縺ｮ閾ｪ蜍墓諺蜈･
        if use_pause_markers:
            text_raw = insert_pause_markers(text_raw)

        # 邨ｵ譁・ｭ励し繝ｳ繝峨う繝・メ讒狗ｯ・        if grok_emoji and not ignore_grok_emoji:
            # Grok邨ｵ譁・ｭ玲署譯医ｒ縺昴・縺ｾ縺ｾ菴ｿ逕ｨ・・moji_suggestion縺ｯ譌｢縺ｫ繧ｵ繝ｳ繝峨う繝・メ貂医∩・・            text_with_emoji = grok_emoji
        else:
            # 繝代う繝励Λ繧､繝ｳ縺ｧ蜀肴ｧ狗ｯ会ｼ域隼蝟・沿: 邨ｵ譁・ｭ・-3蛟句宛髯舌√せ繧ｿ繝・く繝ｳ繧ｰ遲会ｼ・            text_with_emoji = build_sandwich(text_raw, emojis, intensity)

        prod_rows.append({
            "scene_id": scene_id,
            "line_id": f"line_{line_num:03d}",
            "speaker": row.get("speaker", "").strip(),
            "emotion_note": emotion,
            "text_raw": text_raw,
            "text_with_emoji": text_with_emoji,
            "caption": "",
            "cfg_text": "",
            "cfg_caption": "",
            "cfg_speaker": "",
            "cfg_guidance_mode": "",
            "num_steps": "",
            "num_candidates": "3",
            "seed": "",
            "lora_path": "",
            "lora_scale": "",
            "status": "pending",
            "approved_candidate": "",
            "notes": f"intensity={intensity}",
        })

    # 譖ｸ縺榊・縺・    fieldnames = list(prod_rows[0].keys())
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)

    # 繝励Ξ繝ｼ繝ｳ繝・く繧ｹ繝医ｂ蜃ｺ蜉幢ｼ井ｺｺ髢鍋｢ｺ隱咲畑・・    txt_path = project_dir / "script_with_emoji.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        current_scene = ""
        for row in prod_rows:
            if row["scene_id"] != current_scene:
                current_scene = row["scene_id"]
                f.write(f"\n=== {current_scene} ===\n")
            intensity_mark = row["notes"].replace("intensity=", "")
            f.write(f"[{intensity_mark}][{row['emotion_note']}] {row['text_with_emoji']}\n")

    print(f"\n[ok] production.csv 繧堤函謌舌＠縺ｾ縺励◆ ({len(prod_rows)}陦・")
    print(f"[ok] script_with_emoji.txt 繧堤函謌舌＠縺ｾ縺励◆・育｢ｺ隱咲畑・・)

    # 繧ｵ繝槭Μ繝ｼ
    scenes = sorted(set(r["scene_id"] for r in prod_rows))
    print(f"\n  繧ｷ繝ｼ繝ｳ謨ｰ: {len(scenes)}")
    for s in scenes:
        count = sum(1 for r in prod_rows if r["scene_id"] == s)
        print(f"    {s}: {count}陦・)

    print(f"\n  蠑ｷ蠎ｦ蛻・ｸ・")
    print(f"    蠑ｱ (B_sandwich):     {stats['weak']}陦・)
    print(f"    荳ｭ (B/C譁ｹ蠑・:        {stats['medium']}陦・)
    print(f"    蠑ｷ (D_sandwich_螟・:  {stats['strong']}陦・)
    print(f"    讌ｵ髯・(D譛螟ｧ逶帙ｊ):    {stats['extreme']}陦・)

    return str(prod_csv)


def process_game_text(project_name: str, game_text_paths: list[str]) -> str:
    """繧ｲ繝ｼ繝繝・く繧ｹ繝・.md)繧定ｧ｣譫舌＠縺ｦ production.csv 繧堤函謌舌☆繧・
    Args:
        project_name: 繝励Ο繧ｸ繧ｧ繧ｯ繝亥錐
        game_text_paths: 繧ｲ繝ｼ繝繝・く繧ｹ繝医ヵ繧｡繧､繝ｫ縺ｮ繝代せ繝ｪ繧ｹ繝・    """
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    prod_csv = project_dir / "production.csv"

    all_rows = []
    for path_str in game_text_paths:
        filepath = Path(path_str)
        if not filepath.exists():
            print(f"[error] 繝輔ぃ繧､繝ｫ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {filepath}")
            continue
        rows = load_game_text(filepath)
        source_name = filepath.stem
        # rows 縺ｫ source 諠・ｱ繧定ｿｽ蜉
        for r in rows:
            r["source"] = source_name
        all_rows.extend(rows)
        print(f"[ok] {filepath.name} 竊・{len(rows)}陦梧歓蜃ｺ・育峡逋ｽ: {sum(1 for r in rows if r.get('line_type')=='迢ｬ逋ｽ')}, 逋ｺ隧ｱ: {sum(1 for r in rows if r.get('line_type')=='逋ｺ隧ｱ')}・・)

    if not all_rows:
        print("[error] 髻ｳ螢ｰ蛹門ｯｾ雎｡縺ｮ陦後′縺ゅｊ縺ｾ縺帙ｓ")
        return ""

    # production.csv 縺ｫ螟画鋤
    prod_rows = []
    scene_line_counts = {}
    stats = {"weak": 0, "medium": 0, "strong": 0, "extreme": 0}

    for row in all_rows:
        scene_id = row.get("scene_id", "scene_01")
        scene_line_counts[scene_id] = scene_line_counts.get(scene_id, 0) + 1
        line_num = scene_line_counts[scene_id]

        text_raw = row.get("text_raw", "")
        emotion = row.get("emotion_tags", "")

        tags = [t.strip() for t in re.split(r"[,縲―s]+", emotion.strip()) if t.strip()]
        intensity = classify_intensity(tags)
        stats[intensity] += 1

        emojis = emotion_to_emojis_all(emotion)
        text_with_emoji = build_sandwich(text_raw, emojis, intensity)

        prod_rows.append({
            "scene_id": scene_id,
            "line_id": f"line_{line_num:03d}",
            "speaker": row.get("speaker", "逋ｽ髮ｨ"),
            "emotion_note": emotion,
            "text_raw": text_raw,
            "text_with_emoji": text_with_emoji,
            "caption": "",
            "cfg_text": "",
            "cfg_caption": "",
            "cfg_speaker": "",
            "cfg_guidance_mode": "",
            "num_steps": "",
            "num_candidates": "3",
            "seed": "",
            "lora_path": "",
            "lora_scale": "",
            "status": "pending",
            "approved_candidate": "",
            "notes": f"intensity={intensity},type={row.get('line_type', '')},src={row.get('source', '')}",
        })

    # 譖ｸ縺榊・縺・    fieldnames = list(prod_rows[0].keys())
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)

    # 繝励Ξ繝ｼ繝ｳ繝・く繧ｹ繝亥・蜉・    txt_path = project_dir / "script_with_emoji.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        current_scene = ""
        for row in prod_rows:
            if row["scene_id"] != current_scene:
                current_scene = row["scene_id"]
                f.write(f"\n=== {current_scene} ===\n")
            notes = row["notes"]
            intensity_mark = ""
            if "intensity=" in notes:
                intensity_mark = notes.split("intensity=")[1].split(",")[0]
            f.write(f"[{intensity_mark}][{row['emotion_note']}] {row['text_with_emoji']}\n")

    print(f"\n[ok] production.csv 繧堤函謌舌＠縺ｾ縺励◆ ({len(prod_rows)}陦・")
    print(f"[ok] script_with_emoji.txt 繧堤函謌舌＠縺ｾ縺励◆・育｢ｺ隱咲畑・・)

    # 繧ｵ繝槭Μ繝ｼ
    scenes = sorted(set(r["scene_id"] for r in prod_rows))
    print(f"\n  繧ｷ繝ｼ繝ｳ謨ｰ: {len(scenes)}")
    for s in scenes:
        count = sum(1 for r in prod_rows if r["scene_id"] == s)
        print(f"    {s}: {count}陦・)

    print(f"\n  蠑ｷ蠎ｦ蛻・ｸ・")
    print(f"    蠑ｱ (B_sandwich):     {stats['weak']}陦・)
    print(f"    荳ｭ (B/C譁ｹ蠑・:        {stats['medium']}陦・)
    print(f"    蠑ｷ (D_sandwich_螟・:  {stats['strong']}陦・)
    print(f"    讌ｵ髯・(D譛螟ｧ逶帙ｊ):    {stats['extreme']}陦・)

    return str(prod_csv)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python script_processor.py <project_name> [--ignore-grok-emoji] [--no-pause]")
        print("    蜿ｰ譛ｬ蠖｢蠑・ script_raw.json (謗ｨ螂ｨ) / script_raw.csv / script_raw.txt")
        print("    --ignore-grok-emoji: Grok縺ｮemoji_suggestion繧堤┌隕悶＠繝代う繝励Λ繧､繝ｳ縺ｧ蜀肴ｧ狗ｯ・)
        print("    --no-pause: 竢ｸ・城俣繝槭・繧ｫ繝ｼ縺ｮ閾ｪ蜍墓諺蜈･繧堤┌蜉ｹ蛹・)
        print()
        print("  python script_processor.py --game <project_name> <file1.md> [file2.md ...]")
        print("    繧ｲ繝ｼ繝繝・く繧ｹ繝郁ｧ｣譫舌Δ繝ｼ繝・ .md 繝輔ぃ繧､繝ｫ縺九ｉ迢ｬ逋ｽ繝ｻ逋ｺ隧ｱ繧呈歓蜃ｺ")
        sys.exit(1)

    if sys.argv[1] == "--game":
        if len(sys.argv) < 4:
            print("Usage: python script_processor.py --game <project_name> <file1.md> [file2.md ...]")
            sys.exit(1)
        project_name = sys.argv[2]
        game_files = sys.argv[3:]
        process_game_text(project_name, game_files)
    else:
        project_name = sys.argv[1]
        ignore_grok = "--ignore-grok-emoji" in sys.argv
        use_pause = "--no-pause" not in sys.argv
        process_script(project_name, ignore_grok_emoji=ignore_grok,
                       use_pause_markers=use_pause)
