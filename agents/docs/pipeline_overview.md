# 繝代う繝励Λ繧､繝ｳ蜈ｨ菴薙ぎ繧､繝・
R-18 蜷御ｺｺ髻ｳ螢ｰ蛻ｶ菴懊ヱ繧､繝励Λ繧､繝ｳ縺ｮ蜈ｨ菴灘ワ縲よ眠隕丞盾逕ｻ繝｡繝ｳ繝舌・縺梧怙蛻昴↓隱ｭ繧荳蜀翫・
---

## 0. 縺薙・繧ｷ繧ｹ繝・Β縺ｯ菴輔ｒ縺吶ｋ縺・
**繧ｴ繝ｼ繝ｫ**・壻ｽ懷刀繧ｳ繝ｳ繧ｻ繝励ヨ縺九ｉ邏榊刀髻ｳ螢ｰ・・AV/MP3・峨∪縺ｧ縲，laude Code 荳翫・繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝磯｣謳ｺ縺ｧ蜊願・蜍募宛菴懊☆繧九・
**謚陦薙せ繧ｿ繝・け**・・- TTS: Emoji-TTS・・ratako/Irodori-TTS-500M-v2-VoiceDesign 縺ｮ繝輔か繝ｼ繧ｯ・・- 蜿ｰ譛ｬ逕滓・: Grok・亥､夜ΚLLM縲ヽ-18繝・く繧ｹ繝域球蠖難ｼ・- 繝・ぅ繝ｬ繧ｯ繧ｷ繝ｧ繝ｳ繝ｻ蜿朱鹸繝ｻQC繝ｻMA: Claude 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・
**Claude蛻ｶ髯舌→縺ｮ蛻・ｊ蛻・￠**・・- Claude 縺ｯ R-18 繝・く繧ｹ繝・*縺昴・繧ゅ・**繧呈嶌縺九↑縺・- 莨∫判繝ｻ蜿朱鹸貍泌・繝ｻQC繝ｻMA 縺ｯ Claude
- R-18 繧ｻ繝ｪ繝輔・ Grok 縺ｫ螟匁ｳｨ縲，laude 縺悟燕蠕悟・逅・☆繧・
---

## 1. 繝代う繝励Λ繧､繝ｳ蜈ｨ菴灘峙

```
[0. 莨∫判]
  繝励Ο繝・Η繝ｼ繧ｵ繝ｼ ﾃ・Claude
  菴懷刀繧ｳ繝ｳ繧ｻ繝励ヨ 竊・grok_prompt.md / project_brief.json
        竊・[Grok: 蜿ｰ譛ｬ逕滓・]
  繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺・Grok 縺ｫ繝励Ο繝ｳ繝励ヨ繧呈ｸ｡縺励※螳溯｡・  竊・response.json・亥床譛ｬJSON・・        竊・[1. 閼壽悽蜃ｦ逅・ (script-pipeline 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・
  grok_bridge validate 竊・process 竊・casting apply
  竊・production.csv・井ｸｭ螟ｮ繝・・繧ｿ・・        竊・[2. 蜿朱鹸] (recorder 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・
  GPU 縺ｧ infer.py 繧貞・陦後↓蟇ｾ縺怜ｮ溯｡・  竊・audio/{scene}/{line_id}_{c01,c02,c03}.wav
        竊・[3. QC] (qc-reviewer 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・
  髻ｳ螢ｰ髟ｷ繝ｻRMS繝ｻ辟｡髻ｳ繝ｻ繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ閾ｪ蜍輔メ繧ｧ繝・け
  竊・qc_report.csv + approvals_template.json・域耳螂ｨ蛟呵｣懶ｼ・        竊・[繝励Ο繝・Η繝ｼ繧ｵ繝ｼ: 荳ｻ隕ｳ蛻､螳咯
  approvals_template.json 繧堤ｷｨ髮・ｼ亥呵｣懃分蜿ｷ螟画峩・・        竊・[4. 謇ｿ隱榊渚譏] (approve.py 繧ｹ繧ｯ繝ｪ繝励ヨ)
  approved_candidate 蛻励ｒ production.csv 縺ｫ譖ｸ縺崎ｾｼ縺ｿ
        竊・[5. MA/繝溘く繧ｷ繝ｳ繧ｰ] (ma-master 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・
  ma_agent.py 縺ｧ邨仙粋繝ｻ譛ｫ蟆ｾ辟｡髻ｳ繝医Μ繝
  竊・master/scene_XX.wav + master/full_work.wav
        竊・[螳梧・蜩‐
  邏榊刀髻ｳ螢ｰ・・AV / 莉ｻ諢上〒 MP3・・```

---

## 2. 繝励Ο繧ｸ繧ｧ繧ｯ繝医ヵ繧ｩ繝ｫ繝讒矩

```
E:/irodori/projects/{project_name}/
  project_brief.json         竊・菴懷刀莨∫判譖ｸ
  grok_prompt.md             竊・Grok 縺ｸ縺ｮ萓晞ｼ譁・  grok/
    response.json            竊・Grok 縺九ｉ霑斐▲縺ｦ縺阪◆蜿ｰ譛ｬJSON
  production.csv             竊・荳ｭ螟ｮ繝・・繧ｿ・亥・繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝亥・譛会ｼ・  qc_report.csv              竊・QC 邨先棡
  approvals_template.json    竊・QC謗ｨ螂ｨ蛟呵｣懶ｼ井ｺｺ髢薙′邱ｨ髮・ｼ・  audio/
    {scene_id}/
      line_001_001.wav       竊・蛟呵｣・
      line_001_002.wav       竊・蛟呵｣・
      line_001_003.wav       竊・蛟呵｣・
      ...
  approved/
    {scene_id}/
      line_001.wav           竊・謇ｿ隱肴ｸ医∩・亥呵｣懊°繧・譛ｬ繧ｳ繝斐・・・      ...
  master/
    {scene_id}.wav           竊・繧ｷ繝ｼ繝ｳ邨仙粋貂医∩
    full_work.wav            竊・蜈ｨ繧ｷ繝ｼ繝ｳ邨仙粋貂医∩
  mp3/                        竊・--mp3 繧ｪ繝励す繝ｧ繝ｳ譎ゅ・縺ｿ
    *.mp3
```

---

## 3. 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝域ｧ区・

### project-orchestrator・医ョ繧｣繝ｬ繧ｯ繧ｿ繝ｼ・・- **蠖ｹ蜑ｲ**・壼・菴鍋ｵｱ諡ｬ縲Ａinit / script / record / qc / master / full` 縺ｮ蜷・せ繝・・繧ｸ繧貞他縺ｳ蜃ｺ縺・- **繝｢繝・Ν**・嘖onnet
- **莠ｺ髢謎ｻ句・繝昴う繝ｳ繝・*縺ｧ蛛懈ｭ｢・哦rok螳溯｡・/ approved_candidate 蜈･蜉・
### script-pipeline・郁・譛ｬ蜃ｦ逅・ｼ・- **蠖ｹ蜑ｲ**・喩rok/response.json 竊・production.csv 螟画鋤
- **蜀・Κ蜻ｼ縺ｳ蜃ｺ縺・*・啻grok_bridge validate` 竊・`grok_bridge process` 竊・`casting apply`
- **繝｢繝・Ν**・嘖onnet

### recorder・亥庶骭ｲ・・- **蠖ｹ蜑ｲ**・嗔roduction.csv 縺ｮ `status=pending` 陦後ｒ蜈ｨ驛ｨ髻ｳ螢ｰ逕滓・
- **GPU 謗剃ｻ・*・壻ｻ悶・GPU蜃ｦ逅・ｼ亥虚逕ｻ逕滓・遲会ｼ峨→荳ｦ蛻礼ｦ∵ｭ｢
- **繝｢繝・Ν**・喇aiku・郁ｻｽ驥上ち繧ｹ繧ｯ・・
### qc-reviewer・亥刀雉ｪ繝√ぉ繝・け・・- **蠖ｹ蜑ｲ**・嘔c_agent.py 螳溯｡・竊・qc_report.csv 逕滓・ 竊・謗ｨ螂ｨ蛟呵｣懊ｒ謠千､ｺ
- **蜑ｯ逕｣迚ｩ**・啻approvals_template.json`・・C謗ｨ螂ｨ蛟呵｣懷・繧奇ｼ・- **繝｢繝・Ν**・嘖onnet

### ma-master・域怙邨ゆｻ穂ｸ翫￡・・- **蠖ｹ蜑ｲ**・啾pproved 陦後ｒ邨仙粋 竊・繧ｷ繝ｼ繝ｳ蛻･WAV + full_work.wav 逕滓・
- **蜑ｯ讖溯・**・壽忰蟆ｾ辟｡髻ｳ閾ｪ蜍輔ヨ繝ｪ繝縲｀P3螟画鋤
- **繝｢繝・Ν**・喇aiku

---

## 4. 荳ｭ螟ｮ繝・・繧ｿ螂醍ｴ・ｼ嗔roduction.csv

**蜈ｨ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝磯俣縺ｮ繝・・繧ｿ蜿励￠貂｡縺励・蜚ｯ荳縺ｮ逵溷ｮ・*縲・xcel 縺ｧ髢九°縺ｪ縺・％縺ｨ・・p932縺ｧ邨ｵ譁・ｭ怜喧縺托ｼ峨・
| 蛻怜錐 | 險ｭ螳夊・| 隱ｬ譏・|
|------|--------|------|
| scene_id | script-pipeline | 繧ｷ繝ｼ繝ｳID |
| line_id | script-pipeline | 陦栗D・・ine_001...・・|
| speaker | script-pipeline | 隧ｱ閠・錐 |
| emotion_note | script-pipeline | 諢滓ュ繝｡繝｢ |
| text_raw | script-pipeline | 蜈・ユ繧ｭ繧ｹ繝・|
| text_with_emoji | script-pipeline | 邨ｵ譁・ｭ玲諺蜈･貂医∩繝・く繧ｹ繝・|
| caption | casting | VoiceDesign 繧ｭ繝｣繝励す繝ｧ繝ｳ |
| cfg_text | casting | CFG 繝・く繧ｹ繝医せ繧ｱ繝ｼ繝ｫ |
| cfg_caption | casting | CFG 繧ｭ繝｣繝励す繝ｧ繝ｳ繧ｹ繧ｱ繝ｼ繝ｫ |
| cfg_speaker | casting | CFG 繧ｹ繝斐・繧ｫ繝ｼ繧ｹ繧ｱ繝ｼ繝ｫ |
| cfg_guidance_mode | casting | independent / joint / alternating |
| num_steps | casting | 繧ｹ繝・ャ繝玲焚・域耳螂ｨ40・・|
| num_candidates | recorder | 逕滓・蛟呵｣懈焚・医ョ繝輔か3・・|
| seed | recorder | 菴ｿ逕ｨ繧ｷ繝ｼ繝会ｼ亥・迴ｾ諤ｧ遒ｺ菫晢ｼ・|
| lora_path | casting/謇句虚 | LoRA 繧｢繝繝励ち繝代せ・育ｩｺ=荳堺ｽｿ逕ｨ・・|
| lora_scale | casting/謇句虚 | LoRA 驕ｩ逕ｨ蠑ｷ蠎ｦ・医ョ繝輔か1.0・・|
| status | recorder/qc/莠ｺ髢・| pending / generated / qc_pass / qc_fail / approved / done |
| approved_candidate | 莠ｺ髢・| 謇ｿ隱榊呵｣懃分蜿ｷ・・-based・・|
| notes | 莉ｻ諢・| 蛯呵・|

**status 縺ｮ驕ｷ遘ｻ・・*
```
pending 竊・generated 竊・qc_pass 竊・approved 竊・done
                 竊・              qc_fail・亥・骭ｲ・・```

---

## 5. 莠ｺ髢薙′繧・ｋ縺薙→ / 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝医′繧・ｋ縺薙→

### 莠ｺ髢難ｼ医・繝ｭ繝・Η繝ｼ繧ｵ繝ｼ・峨・蠖ｹ蜑ｲ
- **莨∫判**・壻ｽ懷刀繧ｳ繝ｳ繧ｻ繝励ヨ繝ｻ繧ｭ繝｣繝ｩ險ｭ螳壹・繧ｷ繝ｼ繝ｳ讒区・繧呈ｱｺ繧√ｋ
- **Grok 螳溯｡・*・喩rok_prompt.md 繧・Grok 縺ｫ貂｡縺励※蜿ｰ譛ｬ逕滓・
- **繧ｷ繝ｼ繝ｳ蠑ｷ蠎ｦ縺ｮ遒ｺ隱・*・嗔roduction.csv 縺ｮ caption 繧貞ｿ・ｦ√↓蠢懊§縺ｦ隱ｿ謨ｴ
- **髻ｳ螢ｰ隧ｦ閨ｴ**・壼呵｣懊ｒ閨ｴ縺・※驕ｸ螳夲ｼ・pprovals_template.json 繧堤ｷｨ髮・ｼ・- **GPU 邂｡逅・*・壼虚逕ｻ逕滓・遲峨→荳ｦ蛻励↓縺励↑縺・愛譁ｭ

### Claude 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝医・蠖ｹ蜑ｲ
- **邨ｵ譁・ｭ玲諺蜈･**・啼motion_tags 縺九ｉ邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ繧定・蜍暮∈謚・- **繧ｭ繝｣繝励す繝ｧ繝ｳ蜑ｲ蠖・*・壹す繝ｼ繝ｳ蠑ｷ蠎ｦ縺ｫ蠢懊§縺・CFG 蛟､繝ｻguidance_mode 驕ｩ逕ｨ
- **髻ｳ螢ｰ逕滓・**・喨nfer.py 繧貞・陦後↓蟇ｾ縺励※螳溯｡・- **QC**・壽橿陦捺欠讓呻ｼ・MS繝ｻ辟｡髻ｳ繝ｻ繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ・峨・閾ｪ蜍募愛螳・- **MA**・壹す繝ｼ繝ｳ邨仙粋繝ｻ譛ｫ蟆ｾ辟｡髻ｳ繝医Μ繝繝ｻMP3螟画鋤

---

## 6. 蜈ｸ蝙狗噪縺ｪ菴懈･ｭ繝輔Ο繝ｼ・・菴懷刀縺ｮ豬√ｌ・・
### Day 1: 莨∫判 + 蜿ｰ譛ｬ
1. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ・壻ｽ懷刀繧ｳ繝ｳ繧ｻ繝励ヨ繧・Claude 縺ｨ逶ｸ隲・2. Claude・喩rok_prompt.md 縺ｨ project_brief.json 繧堤函謌・3. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ・哦rok 縺ｫ grok_prompt.md 繧呈ｸ｡縺励※ response.json 繧貞叙蠕・4. response.json 繧・`E:/irodori/projects/{name}/grok/` 縺ｫ驟咲ｽｮ

### Day 1縲・: 閼壽悽蜃ｦ逅・+ 蜿朱鹸
5. Claude・・cript-pipeline・会ｼ嗔roduction.csv 逕滓・
6. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ・嗔roduction.csv 縺ｮ caption 繧貞ｿ・ｦ√↓蠢懊§縺ｦ遒ｺ隱・7. Claude・・ecorder・会ｼ哦PU 縺ｧ蜈ｨ陦檎函謌撰ｼ郁｡梧焚 ﾃ・12遘堤ｨ句ｺｦ・・
### Day 2: QC + 謇ｿ隱・8. Claude・・c-reviewer・会ｼ嘔c_report.csv + approvals_template.json 逕滓・
9. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ・啾udio/ 繝輔か繝ｫ繝縺ｮ髻ｳ螢ｰ繧定・縺・※ approvals_template.json 繧堤ｷｨ髮・10. 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ・啻python agents/approve.py {project_name}` 螳溯｡・
### Day 2: MA + 邏榊刀
11. Claude・・a-master・会ｼ嗄aster/full_work.wav 逕滓・
12. 蠢・ｦ√↑繧・`--mp3` 縺ｧ MP3 繧よ嶌縺榊・縺・13. 邏榊刀

**謇隕∵凾髢鍋岼螳会ｼ・0陦・ﾃ・3蛟呵｣・= 150繝輔ぃ繧､繝ｫ縺ｧ荳ｸ2譌･・郁ｩｦ閨ｴ縺ｫ譎る俣縺九°繧具ｼ・*

---

## 7. 髢｢騾｣繝峨く繝･繝｡繝ｳ繝・
| 逕ｨ騾・| 繝峨く繝･繝｡繝ｳ繝・|
|------|-------------|
| 縺ｨ縺ｫ縺九￥1菴懷刀菴懊ｊ縺溘＞ | [`quickstart.md`](./quickstart.md) |
| 蜿ｰ譛ｬ縺ｮ繧ｭ繝｣繝励す繝ｧ繝ｳ險ｭ險・| [`caption_design_guide.md`](./caption_design_guide.md) |
| 邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ縺ｮ驕ｸ縺ｳ譁ｹ | [`emoji_pattern_reference.md`](./emoji_pattern_reference.md) |
| 邏榊刀蜑阪・繝√ぉ繝・け | [`quality_checklist.md`](./quality_checklist.md) |
| LoRA 縺ｧ蝗ｺ螳壹・螢ｰ繧剃ｽ懊ｋ | [`lora_training_guide.md`](./lora_training_guide.md) |
| 蝗ｰ縺｣縺滓凾 | [`troubleshooting.md`](./troubleshooting.md) |

---

**譛邨よ峩譁ｰ: 2026-04-25**
