# irodori 髻ｳ螢ｰ蛻ｶ菴懊ヱ繧､繝励Λ繧､繝ｳ・・moji_agent・・
R-18 蜷御ｺｺ髻ｳ螢ｰ菴懷刀繧貞濠閾ｪ蜍募宛菴懊☆繧九◆繧√・ **Claude Code 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝・+ Python 繝・・繝ｫ繧ｭ繝・ヨ**縲・[Emoji-TTS](https://github.com/iron-mukakin/Emoji-TTS) 繧偵お繝ｳ繧ｸ繝ｳ縺ｨ縺励※蛻ｩ逕ｨ縺励・莨∫判繝ｻ蜿ｰ譛ｬ蜃ｦ逅・・蜿朱鹸繝ｻQC繝ｻMA 縺ｾ縺ｧ繧堤ｵｱ蜷育ｮ｡逅・☆繧九・
---

## 刀 讒区・

```
agents/
  笏懌楳 docs/                     # 答 繝峨く繝･繝｡繝ｳ繝茨ｼ亥ｿ・ｪｭ・・  笏・  笏懌楳 pipeline_overview.md      # 蜈ｨ菴薙ヱ繧､繝励Λ繧､繝ｳ隗｣隱ｬ
  笏・  笏懌楳 quickstart.md             # 蛻晄律縺ｫ1菴懷刀菴懊ｋ譛遏ｭ繧ｬ繧､繝・  笏・  笏懌楳 caption_design_guide.md   # 繧ｭ繝｣繝励す繝ｧ繝ｳ險ｭ險医・繧ｳ繝・  笏・  笏懌楳 emoji_pattern_reference.md # 邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ霎槫・
  笏・  笏懌楳 lora_training_guide.md    # LoRA 縺ｧ蝗ｺ螳壹・螢ｰ繧剃ｽ懊ｋ
  笏・  笏懌楳 troubleshooting.md        # 繧医￥縺ゅｋ繧ｨ繝ｩ繝ｼ縺ｨ蟇ｾ蜃ｦ
  笏・  笏披楳 quality_checklist.md      # 邏榊刀蜑阪メ繧ｧ繝・け繝ｪ繧ｹ繝・  笏・  笏懌楳 knowledge/                # ｧ 繝翫Ξ繝・ず繧ｳ繝ｬ繧ｯ繧ｿ繝ｼ蜿朱寔繝・・繧ｿ
  笏・  笏懌楳 kb_index.json
  笏・  笏懌楳 knowledge_base.md
  笏・  笏懌楳 pending_updates.json
  笏・  笏懌楳 rejection_feedback.json
  笏・  笏懌楳 seen_urls.json
  笏・  笏披楳 daily/                # 譌･谺｡蜿朱寔繝ｬ繝昴・繝・  笏・  笏懌楳 templates/                # 繝・Φ繝励Ξ繝ｼ繝育ｾ､
  笏・  笏披楳 grok_prompt_template.md
  笏・  笏懌楳 # 屏・・繝代う繝励Λ繧､繝ｳ繧ｹ繧ｯ繝ｪ繝励ヨ
  笏懌楳 project_manager.py        # 繝励Ο繧ｸ繧ｧ繧ｯ繝医ヵ繧ｩ繝ｫ繝邂｡逅・  笏懌楳 planner.py                # 莨∫判謾ｯ謠ｴ
  笏懌楳 grok_bridge.py            # Grok JSON 竊・production.csv
  笏懌楳 script_processor.py       # 邨ｵ譁・ｭ玲諺蜈･繝ｻ繧ｹ繧ｯ繝ｪ繝励ヨ螟画鋤
  笏懌楳 casting.py                # 繧ｭ繝｣繝励す繝ｧ繝ｳ蜑ｲ蠖・  笏懌楳 recorder.py               # 髻ｳ螢ｰ逕滓・・・PU・・  笏懌楳 qc_agent.py               # 蜩∬ｳｪ繝√ぉ繝・け
  笏懌楳 approve.py                # 謇ｿ隱榊呵｣懷渚譏
  笏懌楳 ma_agent.py               # 繧ｷ繝ｼ繝ｳ邨仙粋繝ｻMP3螟画鋤
  笏懌楳 set_lora.py               # LoRA 險ｭ螳夂ｮ｡逅・  笏懌楳 test_guidance_mode.py     # guidance_mode 豈碑ｼ・ユ繧ｹ繝・  笏懌楳 knowledge_collector.py    # 繝翫Ξ繝・ず閾ｪ蜍募庶髮・  笏懌楳 download_konomi_voices.py # 蟄ｦ鄙堤ｴ譚舌ム繧ｦ繝ｳ繝ｭ繝ｼ繝芽｣懷勧
  笏・  笏懌楳 # 笞呻ｸ・險ｭ螳・  笏懌楳 default_captions.json     # 繧ｭ繝｣繝励す繝ｧ繝ｳ繝励Ο繝輔ぃ繧､繝ｫ + LoRA邏蝉ｻ倥￠
  笏披楳 emoji_patterns.json       # 邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ繝ｩ繧､繝悶Λ繝ｪ
```

---

## 識 荳ｻ縺ｪ迚ｹ蠕ｴ

- **Claude Code 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝磯｣謳ｺ**: project-orchestrator / script-pipeline / recorder / qc-reviewer / ma-master
- **production.csv 縺ｫ繧医ｋ荳ｭ螟ｮ繝・・繧ｿ螂醍ｴ・*: 蜈ｨ繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝磯俣縺ｮ蜚ｯ荳縺ｮ逵溷ｮ・- **LoRA 蟇ｾ蠢・*: 繧ｷ繝ｼ繝ｳ蛻･繝ｻ繧ｭ繝｣繝ｩ蛻･ LoRA 蛻・ｊ譖ｿ縺医ｒ繝代う繝励Λ繧､繝ｳ縺ｧ邂｡逅・- **VoiceDesign 繧ｭ繝｣繝励す繝ｧ繝ｳ險ｭ險・*: CFG蛟､ / guidance_mode / 邨ｵ譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ縺ｮ譛驕ｩ隗｣繧貞・阡ｵ
- **閾ｪ蜍・QC + 謇ｿ隱阪ヵ繝ｭ繝ｼ**: utf-8 邯ｭ謖√〒譁・ｭ怜喧縺代ぞ繝ｭ

---

## 噫 繧ｯ繧､繝・け繧ｹ繧ｿ繝ｼ繝・
隧ｳ邏ｰ縺ｯ [`docs/quickstart.md`](./docs/quickstart.md) 繧貞盾辣ｧ縲・
```bash
# 1. 繝励Ο繧ｸ繧ｧ繧ｯ繝井ｽ懈・・・laude 縺ｨ蟇ｾ隧ｱ・・# 2. Grok 縺ｧ蜿ｰ譛ｬ逕滓・ 竊・response.json 驟咲ｽｮ
# 3. 閼壽悽蜃ｦ逅・python grok_bridge.py validate {project_name}
python grok_bridge.py process {project_name}

# 4. ・医が繝励す繝ｧ繝ｳ・鵜oRA 驕ｩ逕ｨ
python set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 5. 髻ｳ螢ｰ逕滓・
python recorder.py {project_name}

# 6. QC + 謇ｿ隱・python qc_agent.py {project_name}
# 竊・audio/ 繧定ｩｦ閨ｴ 竊・approvals_template.json 繧堤ｷｨ髮・python approve.py {project_name}

# 7. MA 譛邨ょ・蜉・python ma_agent.py {project_name} --mp3
```

---

## 迫 髢｢騾｣繝ｪ繝昴ず繝医Μ

- **繧ｨ繝ｳ繧ｸ繝ｳ**: [Emoji-TTS 繝輔か繝ｼ繧ｯ](https://github.com/iron-mukakin/Emoji-TTS) 窶・Irodori-TTS 繝輔か繝ｼ繧ｯ
- **蛟倶ｺｺ繝舌ャ繧ｯ繧｢繝・・・医お繝ｳ繧ｸ繝ｳ+LoRA・・*: `ganji1225/emoji`・・rivate・・
---

## 搭 諠ｳ螳夂腸蠅・
- Windows 11
- Python 3.10
- GPU: VRAM 12GB+ 謗ｨ螂ｨ
- Emoji-TTS 縺・`E:/irodori/emoji/` 縺ｫ驟咲ｽｮ貂医∩
- 繝励Ο繧ｸ繧ｧ繧ｯ繝医ヵ繧ｩ繝ｫ繝: `E:/irodori/projects/{project_name}/`

---

## 統 繝ｩ繧､繧ｻ繝ｳ繧ｹ

private 繝ｪ繝昴ず繝医Μ縲ょ倶ｺｺ蛻ｩ逕ｨ蜑肴署縲・
---

**譛邨よ峩譁ｰ: 2026-04-26**
