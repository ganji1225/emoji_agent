#!/usr/bin/env python3
"""莨∫判繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・- 菴懷刀莨∫判譖ｸ縺ｨGrok逕ｨ繝励Ο繝ｳ繝励ヨ繧堤函謌・""
import json
import sys
from pathlib import Path

PROJECTS_DIR = Path("E:/irodori/projects")


def generate_grok_prompt(project_dir: Path) -> str:
    """project_brief.json 縺九ｉGrok逕ｨ繝励Ο繝ｳ繝励ヨ繧堤函謌舌☆繧・""
    brief_path = project_dir / "project_brief.json"
    if not brief_path.exists():
        raise FileNotFoundError(f"project_brief.json 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: {brief_path}")

    with open(brief_path, "r", encoding="utf-8") as f:
        brief = json.load(f)

    # 繧ｭ繝｣繝ｩ繧ｯ繧ｿ繝ｼ諠・ｱ縺ｮ邨・∩遶九※
    chars_text = ""
    for ch in brief.get("characters", []):
        chars_text += f"""
### {ch['name']}
- 蟷ｴ鮨｢: {ch.get('age', '荳肴・')}
- 諤ｧ譬ｼ: {ch.get('personality', '')}
- 蜿｣隱ｿ: {ch.get('speech_style', '')}
- 菴薙・迚ｹ蠕ｴ: {ch.get('body_features', '')}
- 髢｢菫よｧ: {ch.get('relationship', '')}
"""

    # 繧ｷ繝ｼ繝ｳ讒区・縺ｮ邨・∩遶九※
    scenes_text = ""
    for sc in brief.get("scenes", []):
        scenes_text += f"""
### {sc['scene_id']}: {sc.get('title', '')}
- 讎りｦ・ {sc.get('description', '')}
- 髮ｰ蝗ｲ豌励・諢滓ュ縺ｮ豬√ｌ: {sc.get('mood', '')}
- 逶ｮ螳峨そ繝ｪ繝墓焚: {sc.get('estimated_lines', '?')}陦・"""

    total_lines = brief.get("line_count_target", 50)

    speakers = ', '.join(ch['name'] for ch in brief.get('characters', []))

    prompt = f"""# 蜿ｰ譛ｬ逕滓・萓晞ｼ

## 菴懷刀讎りｦ・- 繧ｿ繧､繝医Ν: {brief.get('title', '辟｡鬘・)}
- 繧ｸ繝｣繝ｳ繝ｫ: {brief.get('genre', '')}
- 逶ｮ螳牙ｰｺ: {brief.get('duration_target', '10蛻・)}
- 譁ｹ蜷第ｧ: {brief.get('direction_notes', '')}

## 逋ｻ蝣ｴ莠ｺ迚ｩ
{chars_text}

## 繧ｷ繝ｼ繝ｳ讒区・
{scenes_text}

## 蜃ｺ蜉帛ｽ｢蠑・
**蠢・★JSON蠖｢蠑上〒蜃ｺ蜉帙＠縺ｦ縺上□縺輔＞縲・* CSV蠖｢蠑上・菴ｿ繧上↑縺・〒縺上□縺輔＞縲・
莉･荳九・JSON驟榊・蠖｢蠑上〒蜃ｺ蜉帙＠縺ｦ縺上□縺輔＞:

```json
[
  {{
    "scene_id": "scene_01",
    "line_id": 1,
    "speaker": "{speakers}",
    "emotion_tags": "閾ｪ菫｡,螽∝悸",
    "text_raw": "繧ｻ繝ｪ繝輔ユ繧ｭ繧ｹ繝・,
    "emoji_suggestion": ""
  }}
]
```

### 蜷・ヵ繧｣繝ｼ繝ｫ繝峨・隱ｬ譏・
| 繝輔ぅ繝ｼ繝ｫ繝・| 隱ｬ譏・|
|---|---|
| `scene_id` | 繧ｷ繝ｼ繝ｳ蛹ｺ蛻・ｊ・・cene_01, scene_02, ...・・|
| `line_id` | 繧ｷ繝ｼ繝ｳ蜀・・騾｣逡ｪ・・, 2, 3...・・|
| `speaker` | 隧ｱ閠・錐・・speakers}・・|
| `emotion_tags` | 諢滓ュ繧ｿ繧ｰ・医き繝ｳ繝槫玄蛻・ｊ縲ゆｸ玖ｨ倥ぎ繧､繝牙盾辣ｧ・・|
| `text_raw` | 繧ｻ繝ｪ繝輔ユ繧ｭ繧ｹ繝茨ｼ育ｵｵ譁・ｭ励ｒ蜷ｫ繧√↑縺・ｴ縺ｮ繝・く繧ｹ繝茨ｼ・|
| `emoji_suggestion` | 邨ｵ譁・ｭ励・謠先｡茨ｼ井ｻｻ諢上ゅし繝ｳ繝峨う繝・メ蠖｢蠑上〒蜑榊ｾ後↓驟咲ｽｮ縲ゆｸ玖ｨ伜盾辣ｧ・・|

### emoji_suggestion 縺ｮ譖ｸ縺肴婿

髻ｳ螢ｰ蜷域・繧ｨ繝ｳ繧ｸ繝ｳ縺ｯ**繝・く繧ｹ繝医・蜑榊ｾ後↓邨ｵ譁・ｭ励ｒ驟咲ｽｮ縺吶ｋ縲後し繝ｳ繝峨う繝・メ譁ｹ蠑上・*縺ｧ諢滓ュ陦ｨ迴ｾ繧貞宛蠕｡縺励∪縺吶・諢滓ュ縺悟ｼｷ縺・ｴ髱｢縺ｧ縺ｯ縲∝燕蠕後↓螟壹￥縺ｮ邨ｵ譁・ｭ励ｒ驟咲ｽｮ縺吶ｋ縺ｻ縺ｩ諢滓ュ陦ｨ迴ｾ縺瑚ｱ翫°縺ｫ縺ｪ繧翫∪縺吶・
**驟咲ｽｮ繝ｫ繝ｼ繝ｫ:**
- 蠑ｱ縺・─諠・ `"丶潮 繝・く繧ｹ繝・丶"` ・亥燕2-3蛟九∝ｾ・蛟具ｼ・- 荳ｭ遞句ｺｦ: `"･ｵ・ｫ｣ 繝・く繧ｹ繝・ｫ｣"` ・亥燕2-4蛟九∝ｾ・-1蛟具ｼ・- 蠑ｷ縺・─諠・ `"･ｵ舒窶昨汳ｨ懲 繝・く繧ｹ繝・亊懲"` ・亥燕3-5蛟九∝ｾ・-3蛟具ｼ・- 讌ｵ髯千憾諷・ `"･ｵ亞舒窶昨汳ｨ懲ｫ・沽ｭ 繝・く繧ｹ繝・亞懲･ｵ"` ・亥燕5-8蛟九∝ｾ・-3蛟具ｼ・
**謗ｨ螂ｨ邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ・亥ｴ髱｢蛻･・・**

| 蝣ｴ髱｢ | 蜑肴婿・・refix・・| 蠕梧婿・・uffix・・|
|---|---|---|
| 菴弱￥螟ｪ縺・迄縺趣ｼ医♀繧帙⊇縺臥ｳｻ・・| ･ｵ舒窶昨汳ｨ懲 | 亊 |
| 諱･縺壹°縺励＞蝟倥℃・医ｓ繧帙⊇縺臥ｳｻ・・| ｫ｣･ｵ于 | 懲 |
| 遏ｭ縺城強縺・ｵｶ蜿ｫ・医≠繧帙≠縺｣邉ｻ・・| 亞･ｵ懲 | 亞懲 |
| 逕倥￥髟ｷ縺・迄縺趣ｼ医・縺√ｓ邉ｻ・・| ･ｵ剌懲 | ・ |
| 諛・｡假ｼ亥ｭ輔∪縺帙※邉ｻ・・| 剌･ｵ亊 | 懲 |
| 莠句ｾ後・謾ｾ蠢・| ･ｵ・懲 | ・ |
| 豕｣縺阪う繧ｭ | 亊･ｵ懲 | 亞 |
| 閠ｳ蜈・宦縺・| 曹･ｵ舒窶昨汳ｨ | 昼 |

`emoji_suggestion` 縺ｯ遨ｺ谺・〒繧０K縺ｧ縺呻ｼ医◎縺ｮ蝣ｴ蜷医‘motion_tags縺九ｉ閾ｪ蜍慕函謌舌＠縺ｾ縺呻ｼ峨・

## emotion_tags 縺ｮ菴ｿ縺・婿繧ｬ繧､繝・
繧ｷ繝ｼ繝ｳ縺ｫ蠢懊§縺ｦ莉･荳九・諢滓ュ繧ｿ繧ｰ繧弾motion_tags蛻励↓險倩ｿｰ縺励※縺上□縺輔＞縲・髻ｳ螢ｰ蜷域・繧ｨ繝ｳ繧ｸ繝ｳ縺後％縺ｮ繧ｿ繧ｰ繧偵ｂ縺ｨ縺ｫ螢ｰ縺ｮ貍疲橿繧貞宛蠕｡縺励∪縺吶・
縲仙渕譛ｬ諢滓ュ縲題・菫｡, 螽∝悸, 謖醍匱, 蜍墓昭, 諱先・ 邨ｶ譛・ 蠑ｷ縺後ｊ, 鬩壹″, 諤偵ｊ
縲先▼縺倥ｉ縺・ｳｻ縲醍・繧・ 諱･縺倥ｉ縺・ 蝗ｰ諠・ 繧ゅ§繧ゅ§
縲千曝縺医・隕ｪ蟇・ｳｻ縲醍曝縺・ 蝗√″, 縺九ｉ縺九≧, 蜆ｪ縺励＞
縲先・驕｣縺・ｳｻ縲大瑞諱ｯ, 蝟倥℃, 蝟倥℃(蠑ｱ), 蝟倥℃(蠑ｷ), 諱ｯ蛻・ｌ, 闕偵＞諱ｯ驕｣縺・縲先ｳ｣縺咲ｳｻ縲第ｳ｣縺・ 蝸壼朕, 豸吝｣ｰ
縲先･ｵ髯千ｳｻ縲醍ｵｶ鬆・ 蜿ｫ縺ｳ, 謔ｲ魑ｴ, 闍ｦ縺励＞
縲蝉ｺ句ｾ檎ｳｻ縲第叛蠢・ 閼ｱ蜉・ 譛ｦ譛ｧ, 陌夊┳, 螳牙ｵ
縲仙柑譫憺浹邉ｻ縲題・謇薙■, 蜚ｾ繧帝｣ｲ繧, 繝ｪ繝・・, 縺ゅ￥縺ｳ

窶ｻ 隍・焚縺ｮ諢滓ュ繧偵・縲阪〒邨・∩蜷医ｏ縺幢ｼ井ｾ・ 縲梧＄諤・蠑ｷ縺後ｊ縲阪悟迄縺・蠑ｱ),蝗ｰ諠代搾ｼ・
### 驥崎ｦ・ｼ壽─諠・・蠑ｷ蠎ｦ縺ｨ隍・焚繧ｿ繧ｰ縺ｮ菴ｿ縺・婿

諢滓ュ陦ｨ迴ｾ縺悟ｼｷ縺・憾諷具ｼ亥迄縺弱∫ｵｶ鬆ゅ∝将縺ｳ縲∝履蜥ｽ縺ｪ縺ｩ・峨〒縺ｯ縲・*emotion_tags 縺ｫ隍・焚縺ｮ諢滓ュ繧ｿ繧ｰ繧偵き繝ｳ繝槫玄蛻・ｊ縺ｧ遨肴･ｵ逧・↓邨・∩蜷医ｏ縺帙※縺上□縺輔＞**縲・繧ｿ繧ｰ縺悟､壹＞縺ｻ縺ｩ髻ｳ螢ｰ蜷域・譎ゅ・諢滓ュ陦ｨ迴ｾ縺瑚ｱ翫°縺ｫ縺ｪ繧翫∪縺吶・
**蜈ｷ菴謎ｾ具ｼ・*
- 蠑ｱ縺・─諠・憾諷・竊・繧ｿ繧ｰ1縲・蛟・ `"蝗ｰ諠・` `"蜍墓昭,諱先・`
- 荳ｭ遞句ｺｦ縺ｮ諢滓ュ迥ｶ諷・竊・繧ｿ繧ｰ2縲・蛟・ `"蝟倥℃(蠑ｱ),蝗ｰ諠・諱･縺倥ｉ縺・` `"諱先・蠑ｷ縺後ｊ,豸吝｣ｰ"`
- 蠑ｷ縺・─諠・憾諷・竊・繧ｿ繧ｰ3縲・蛟・ `"蝟倥℃(蠑ｷ),諱ｯ蛻・ｌ,闕偵＞諱ｯ驕｣縺・` `"邨ｶ鬆・蜿ｫ縺ｳ,蝟倥℃(蠑ｷ),蝸壼朕"`
- 讌ｵ髯千憾諷・竊・繧ｿ繧ｰ4蛟倶ｻ･荳・ `"邨ｶ鬆・蜿ｫ縺ｳ,蝟倥℃(蠑ｷ),闕偵＞諱ｯ驕｣縺・蝸壼朕"`

**迚ｹ縺ｫ豼縺励＞蝣ｴ髱｢縺ｧ縺ｯ縲・縺､縺ｮemotion_tags縺ｫ3蛟倶ｻ･荳翫・繧ｿ繧ｰ繧剃ｽｿ縺・％縺ｨ繧呈耳螂ｨ縺励∪縺吶・*

## 1陦後・繝・く繧ｹ繝磯㍼繧ｬ繧､繝会ｼ・TS譛驕ｩ蛹厄ｼ・
髻ｳ螢ｰ蜷域・縺ｧ縺ｯ**1陦後≠縺溘ｊ15縲・0譁・ｭ・*縺梧怙驕ｩ縺ｧ縺吶・髟ｷ縺・そ繝ｪ繝輔・諢丞袖縺ｮ蛹ｺ蛻・ｊ縺ｧ蛻・牡縺励※縺上□縺輔＞縲・
| 遞ｮ鬘・| 譁・ｭ玲焚 | 萓・|
|---|---|---|
| 遏ｭ縺・渚蠢懊・蜿ｫ縺ｳ | 5縲・5譁・ｭ・| `縺上▲窶ｦ窶ｦ・～ `謾ｾ縺励※窶ｦ窶ｦ・～ |
| 騾壼ｸｸ縺ｮ逋ｺ隧ｱ | 15縲・0譁・ｭ・| 騾壼ｸｸ縺ｮ繧ｻ繝ｪ繝・|
| 髟ｷ繧√・迢ｬ逋ｽ | 40縲・0譁・ｭ・| ・域峡蠑ｧ縺ｮ蜀・ｿ・峡逋ｽ・・|
| **NG: 髟ｷ縺吶℃** | 60譁・ｭ苓ｶ・| 竊・蠢・★2陦後↓蛻・牡 |

**蛻・牡縺ｮ繧ｳ繝・**
- 諢滓ュ縺悟､峨ｏ繧九・繧､繝ｳ繝医〒蛻・牡縺吶ｋ
- 縲娯ｦ窶ｦ縲阪・蠕後′閾ｪ辟ｶ縺ｪ蛹ｺ蛻・ｊ
- 螢ｰ縺ｫ蜃ｺ縺咏匱隧ｱ縺ｨ・亥・蠢・・迢ｬ逋ｽ・峨・蛻･縺ｮ陦後↓縺吶ｋ
- 蝟倥℃螢ｰ縺ｯ遏ｭ縺丞・繧区婿縺碁浹螢ｰ縺ｮ繝ｪ繧｢繝ｪ繝・ぅ縺御ｸ翫′繧・
## 豕ｨ諢丈ｺ矩・- 邱上そ繝ｪ繝墓焚縺ｯ邏кtotal_lines}陦後ｒ逶ｮ螳峨↓縺励※縺上□縺輔＞
- **蠢・★JSON驟榊・蠖｢蠑上〒蜃ｺ蜉帙＠縺ｦ縺上□縺輔＞**・・SV縺ｧ縺ｯ縺ｪ縺擾ｼ・- text_raw 縺ｫ縺ｯ繧ｻ繝ｪ繝輔・縺ｿ險倩ｿｰ縺励※縺上□縺輔＞・育ｵｵ譁・ｭ励・蜷ｫ繧√↑縺・らｵｵ譁・ｭ励・emoji_suggestion縺ｫ譖ｸ縺擾ｼ・- 1陦後↓1繧ｻ繝ｪ繝輔・縺ｿ・亥慍縺ｮ譁・・繝域嶌縺阪・荳崎ｦ・ｼ・- emotion_tags 縺ｫ縺ｯ荳願ｨ倥ぎ繧､繝峨・諢滓ュ繧ｿ繧ｰ繧剃ｽｿ縺｣縺ｦ險倩ｿｰ縺励※縺上□縺輔＞
- **1陦後≠縺溘ｊ15縲・0譁・ｭ励ｒ逶ｮ螳峨↓縺励※縺上□縺輔＞**・磯聞縺・ｴ蜷医・蛻・牡・・- 髮｣隱ｭ貍｢蟄励・驕ｿ縺代√・繧峨′縺ｪ繝ｻ繧ｫ繧ｿ繧ｫ繝翫ｒ豢ｻ逕ｨ縺励※縺上□縺輔＞
- 蜿･隱ｭ轤ｹ縺ｯ驕ｩ蛻・↓蜈･繧後※縺上□縺輔＞
- 縲娯ｦ縲搾ｼ井ｸ臥せ繝ｪ繝ｼ繝繝ｼ・峨・霄願ｺ・ｄ菴咎渊縺ｮ陦ｨ迴ｾ縺ｫ菴ｿ縺｣縺ｦ縺上□縺輔＞
- 繧ｻ繝ｪ繝輔・閾ｪ辟ｶ縺ｪ隧ｱ縺苓ｨ闡峨〒譖ｸ縺・※縺上□縺輔＞
- 蜀・ｿ・・迢ｬ逋ｽ縺ｯ・域峡蠑ｧ・峨〒陦ｨ迴ｾ縺励※縺上□縺輔＞・井ｾ・ ・医％繧後・窶ｦ窶ｦ逖ｴ豌暦ｼ滂ｼ会ｼ・"""

    # grok_prompt.md 繧剃ｿ晏ｭ・    prompt_path = project_dir / "grok_prompt.md"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"[ok] Grok逕ｨ繝励Ο繝ｳ繝励ヨ繧堤函謌舌＠縺ｾ縺励◆: {prompt_path}")
    print(f"  邱上そ繝ｪ繝慕岼螳・ {total_lines}陦・)
    print(f"  繧ｷ繝ｼ繝ｳ謨ｰ: {len(brief.get('scenes', []))}")
    return str(prompt_path)


def create_brief_template(project_dir: Path) -> str:
    """project_brief.json 縺ｮ繝・Φ繝励Ξ繝ｼ繝医ｒ菴懈・縺吶ｋ"""
    template = {
        "title": "",
        "genre": "",
        "duration_target": "10蛻・,
        "line_count_target": 50,
        "characters": [
            {
                "name": "",
                "age": "",
                "personality": "",
                "speech_style": "",
                "body_features": "",
                "relationship": ""
            }
        ],
        "scenes": [
            {
                "scene_id": "scene_01",
                "title": "",
                "description": "",
                "mood": "",
                "estimated_lines": 15
            },
            {
                "scene_id": "scene_02",
                "title": "",
                "description": "",
                "mood": "",
                "estimated_lines": 25
            }
        ],
        "direction_notes": ""
    }

    brief_path = project_dir / "project_brief.json"
    with open(brief_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"[ok] 莨∫判譖ｸ繝・Φ繝励Ξ繝ｼ繝医ｒ菴懈・縺励∪縺励◆: {brief_path}")
    return str(brief_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python planner.py template <project_name>  -- 繝・Φ繝励Ξ繝ｼ繝井ｽ懈・")
        print("  python planner.py generate <project_name>  -- Grok繝励Ο繝ｳ繝励ヨ逕滓・")
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]
    project_dir = PROJECTS_DIR / project_name

    if not project_dir.exists():
        print(f"[error] 繝励Ο繧ｸ繧ｧ繧ｯ繝医′蟄伜惠縺励∪縺帙ｓ: {project_dir}")
        print("蜈医↓ project_manager.py init 縺ｧ菴懈・縺励※縺上□縺輔＞")
        sys.exit(1)

    if cmd == "template":
        create_brief_template(project_dir)
    elif cmd == "generate":
        generate_grok_prompt(project_dir)
    else:
        print(f"Unknown command: {cmd}")
