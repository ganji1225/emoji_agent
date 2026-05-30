# 繧ｯ繧､繝・け繧ｹ繧ｿ繝ｼ繝・
**蛻晄律縺ｫ縺薙ｌ繧定ｪｭ繧√・縲√∪縺・菴懷刀菴懊ｌ繧・*譛遏ｭ繧ｬ繧､繝峨・隧ｳ邏ｰ縺ｯ莉悶・繝峨く繝･繝｡繝ｳ繝医↓莉ｻ縺帙※縲∵怙蟆城剞縺ｮ豬√ｌ縺縺醍､ｺ縺吶・
---

## 0. 蜑肴署

- Windows 迺ｰ蠅・- `E:/irodori/` 縺ｫ繝ｪ繝昴ず繝医Μ荳蠑上′驟咲ｽｮ貂医∩
- Emoji-TTS 縺ｮ `.venv` 讒狗ｯ画ｸ医∩
- GPU・・RAM 12GB+ 謗ｨ螂ｨ・・
---

## 1. 繝励Ο繧ｸ繧ｧ繧ｯ繝井ｽ懈・・・蛻・ｼ・
### 1-1. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺・Claude 縺ｫ菴懷刀繧ｳ繝ｳ繧ｻ繝励ヨ繧剃ｼ昴∴繧・```
萓・ 縲檎曝縲・ｳｻ縺ｮ閠ｳ縺九″髻ｳ螢ｰ繧剃ｽ懊ｊ縺溘＞縲ゅす繝ｼ繝ｳ縺ｯ3縺､縲∝粋險・0蛻・￥繧峨＞縲・```

### 1-2. Claude 縺・grok_prompt.md 縺ｨ project_brief.json 繧堤函謌・- `E:/irodori/projects/{project_name}/grok_prompt.md`
- `E:/irodori/projects/{project_name}/project_brief.json`

---

## 2. 蜿ｰ譛ｬ菴懈・・亥､夜Κ Grok 縺ｧ20縲・0蛻・ｼ・
### 2-1. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺・grok_prompt.md 繧・Grok 縺ｫ貂｡縺・- Grok 蜈ｬ蠑上し繧､繝育ｭ峨〒 grok_prompt.md 縺ｮ蜀・ｮｹ繧呈兜縺偵ｋ
- Grok 縺・response.json 蠖｢蠑上〒蜿ｰ譛ｬ繧定ｿ斐☆

### 2-2. 蜿励￠蜿悶▲縺・JSON 繧帝・鄂ｮ
```
E:/irodori/projects/{project_name}/grok/response.json
```

### 2-3. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺悟・螳ｹ遒ｺ隱・- 繧ｻ繝ｪ繝輔′諠ｳ螳夐壹ｊ縺・- emoji_suggestion 縺・3 蛟九★縺､縺上ｉ縺・≠繧九°・亥ｰ代↑縺代ｌ縺ｰ Claude 縺ｫ菫ｮ豁｣萓晞ｼ・・
---

## 3. 閼壽悽蜃ｦ逅・ｼ・laude 縺ｫ萓晞ｼ縲・蛻・ｼ・
繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺・Claude 縺ｫ萓晞ｼ・・> 縲鶏project_name} 縺ｮ grok_bridge 繧呈ｵ√＠縺ｦ縲・
Claude 縺瑚｣上〒螳溯｡後☆繧句・螳ｹ・・```bash
python E:/irodori/agents/grok_bridge.py validate {project_name}
python E:/irodori/agents/grok_bridge.py process {project_name}
```

竊・`production.csv` 逕滓・螳御ｺ・
---

## 4. 繧ｭ繝｣繝励す繝ｧ繝ｳ遒ｺ隱搾ｼ・蛻・ｼ・
production.csv 縺ｮ `caption` / `cfg_text` / `cfg_guidance_mode` 蛻励′閾ｪ蜍戊ｨｭ螳壹＆繧後ｋ縲・豌励↓縺ｪ繧九す繝ｼ繝ｳ縺後≠繧後・謇句虚縺ｧ隱ｿ謨ｴ蜿ｯ閭ｽ・・`caption_design_guide.md`](./caption_design_guide.md) 蜿ら・・峨・
**騾壼ｸｸ縺ｯ縺昴・縺ｾ縺ｾ谺｡縺ｸ縲・*

---

## 5. 髻ｳ螢ｰ逕滓・・・PU 縺ｧ30蛻・・譎る俣・・
### 5-0. ・医が繝励す繝ｧ繝ｳ・鵜oRA 縺ｧ蝗ｺ螳壹・螢ｰ繧剃ｽｿ縺・ｴ蜷・蝓ｺ譛ｬ縺ｯ LoRA 謖・ｮ壹↑縺励〒騾ｲ繧√※ OK縲ら音螳壹く繝｣繝ｩ縺ｮ LoRA 繧貞・陦後↓驕ｩ逕ｨ縺励◆縺・ｴ蜷茨ｼ・
```bash
# 蜈ｨ陦後↓ LoRA 驕ｩ逕ｨ
python E:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 遒ｺ隱・python E:/irodori/agents/set_lora.py {project_name} --show

# 隗｣髯､
python E:/irodori/agents/set_lora.py {project_name} --clear
```

LoRA 繧剃ｽ懊ｋ譁ｹ豕輔・ [`lora_training_guide.md`](./lora_training_guide.md) 蜿ら・縲・
### 5-1. CLI 縺ｧ螳溯｡鯉ｼ・PU 謗剃ｻ悶・縺溘ａ Claude 繝√Ε繝・ヨ縺九ｉ縺ｯ謗ｨ螂ｨ縺励↑縺・ｼ・```bash
cd E:/irodori
python agents/recorder.py {project_name}
```

竊・`E:/irodori/projects/{project_name}/audio/{scene_id}/line_XXX_001~003.wav` 縺檎函謌舌＆繧後ｋ・郁｡梧焚 ﾃ・3蛟呵｣懶ｼ・
**逶ｮ螳会ｼ・*
- 50陦後〒邏・10縲・5 蛻・- 100陦後〒邏・20縲・0 蛻・- 螟ｧ隕乗ｨ｡縺ｪ菴懷刀縺ｪ繧画仂莨代∩ or 螟應ｸｭ縺ｫ襍ｰ繧峨○繧・
---

## 6. QC + 謇ｿ隱搾ｼ郁ｩｦ閨ｴ蜷ｫ繧√※1縲・譎る俣・・
### 6-1. Claude 縺ｫ萓晞ｼ・・> 縲繋c-reviewer 襍ｰ繧峨○縺ｦ縲・
竊・`qc_report.csv` 縺ｨ `approvals_template.json` 縺檎函謌舌＆繧後ｋ

### 6-2. 髻ｳ螢ｰ繧定ｩｦ閨ｴ
```
E:/irodori/projects/{project_name}/audio/{scene_id}/
```
WAV 繝励Ξ繧､繝､繝ｼ縺ｧ閨ｴ縺肴ｯ斐∋・亥呵｣・, 2, 3・・
### 6-3. approvals_template.json 繧堤ｷｨ髮・```json
{
  "scene_01/line_001": 2,    竊・QC謗ｨ螂ｨ
  "scene_01/line_002": 3,    竊・閾ｪ蛻・′螂ｽ縺阪↑蛟呵｣懊↓螟画峩
  ...
}
```

**繝昴う繝ｳ繝茨ｼ・* QC謗ｨ螂ｨ縺瑚憶縺代ｌ縺ｰ菴輔ｂ縺励↑縺上※OK縲る＆縺・→諤昴▲縺溯｡後□縺第焚蟄励ｒ螟峨∴繧九・
### 6-4. 謇ｿ隱榊渚譏
```bash
python E:/irodori/agents/approve.py {project_name}
```

---

## 7. MA / 譛邨ょ・蜉幢ｼ・縲・0蛻・ｼ・
繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺・Claude 縺ｫ萓晞ｼ・・> 縲稽a-master 襍ｰ繧峨○縺ｦ縲・
縺ｾ縺溘・逶ｴ謗･・・```bash
python E:/irodori/agents/ma_agent.py {project_name}

# MP3 繧ょ酔譎ゅ↓譖ｸ縺榊・縺吝ｴ蜷・python E:/irodori/agents/ma_agent.py {project_name} --mp3
```

### 蜃ｺ蜉帙ヵ繧｡繧､繝ｫ
```
E:/irodori/projects/{project_name}/master/
  scene_01.wav
  scene_02.wav
  ...
  full_work.wav    竊・縺薙ｌ縺悟ｮ梧・迚・```

---

## 8. 邏榊刀蜑阪・譛邨ゅメ繧ｧ繝・け

[`quality_checklist.md`](./quality_checklist.md) 縺ｫ蠕薙▲縺ｦ遒ｺ隱搾ｼ・
- [ ] full_work.wav 縺ｮ髟ｷ縺輔′諠ｳ螳夐壹ｊ
- [ ] 蜈ｨ繧ｷ繝ｼ繝ｳ縺悟性縺ｾ繧後※縺・ｋ・郁｡梧焚遒ｺ隱搾ｼ・- [ ] 繝弱う繧ｺ繝ｻ繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ縺ｪ縺・- [ ] 辟｡髻ｳ蛹ｺ髢薙′髟ｷ縺吶℃縺ｪ縺・ｼ亥・鬆ｭ/譛ｫ蟆ｾ/繧ｷ繝ｼ繝ｳ髢難ｼ・- [ ] 譁・ｭ怜喧縺代そ繝ｪ繝輔′谿九▲縺ｦ縺ｪ縺・ｼ・C谿ｵ髫弱〒髯､蜴ｻ貂医∩縺ｮ縺ｯ縺夲ｼ・
---

## 9. 蝗ｰ縺｣縺溘ｉ

| 迥ｶ豕・| 蜿ら・蜈・|
|------|-------|
| 蜈ｨ菴灘ワ繧貞・遒ｺ隱阪＠縺溘＞ | [`pipeline_overview.md`](./pipeline_overview.md) |
| 螢ｰ縺梧昴▲縺滄壹ｊ縺ｫ縺ｪ繧峨↑縺・| [`caption_design_guide.md`](./caption_design_guide.md) |
| 邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ繧貞､峨∴縺溘＞ | [`emoji_pattern_reference.md`](./emoji_pattern_reference.md) |
| 繧ｨ繝ｩ繝ｼ縺悟・縺・| [`troubleshooting.md`](./troubleshooting.md) |
| 蝗ｺ螳壹・螢ｰ繧剃ｽ懊ｊ縺溘＞ | [`lora_training_guide.md`](./lora_training_guide.md) |

---

## 10. 1菴懷刀縺ｮ謇隕∵凾髢鍋岼螳・
| 繝輔ぉ繝ｼ繧ｺ | 譎る俣 |
|---------|------|
| 莨∫判 + Grok 蜿ｰ譛ｬ逕滓・ | 30蛻・・譎る俣 |
| 閼壽悽蜃ｦ逅・+ 繧ｭ繝｣繝励す繝ｧ繝ｳ險ｭ螳・| 5縲・0蛻・|
| 蜿朱鹸・・PU逕滓・・・| 陦梧焚 ﾃ・12遘・|
| QC + 隧ｦ閨ｴ + 謇ｿ隱・| 1縲・譎る俣 |
| MA + 譛邨ょ・蜉・| 10蛻・|
| **蜷郁ｨ茨ｼ・0陦御ｽ懷刀・・* | **3縲・譎る俣** |

---

## 11. 繧・▲縺ｦ縺ｯ縺・￠縺ｪ縺・％縺ｨ TOP 5

1. 笶・**production.csv 繧・Excel 縺ｧ髢九＞縺ｦ菫晏ｭ・* 竊・邨ｵ譁・ｭ励′譁・ｭ怜喧縺・2. 笶・**GPU 蜃ｦ逅・ｼ亥虚逕ｻ/SD・峨→ recorder 縺ｮ荳ｦ蛻怜ｮ溯｡・* 竊・CUDA OOM
3. 笶・**approved_candidate 繧堤峩謗･ production.csv 縺ｫ謇区嶌縺・* 竊・`approve.py` 邨檎罰蠢・・4. 笶・**emoji_suggestion 繧・4 蛟倶ｻ･荳・+ CFG 7.0** 竊・繝弱う繧ｺ螟夂匱
5. 笶・**Claude 縺ｫ R-18 繧ｻ繝ｪ繝輔ｒ逶ｴ謗･譖ｸ縺九○繧・* 竊・諡貞凄縺輔ｌ繧九・rok 諡・ｽ・
---

**譛邨よ峩譁ｰ: 2026-04-25**
