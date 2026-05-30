# 繝医Λ繝悶Ν繧ｷ繝･繝ｼ繝・ぅ繝ｳ繧ｰ髮・
驕主悉縺ｫ逋ｺ逕溘＠縺溘お繝ｩ繝ｼ繝ｻ蝠城｡後→蟇ｾ蜃ｦ豕輔・繝ｪ繝輔ぃ繝ｬ繝ｳ繧ｹ縲・
---

## 1. production.csv 髢｢騾｣

### 笶・譁・ｭ怜喧縺托ｼ育ｵｵ譁・ｭ励′ ?? 縺ｫ縺ｪ繧具ｼ・
**逞・憾・・*
- production.csv 縺ｮ text_with_emoji 蛻励′ `??????` 縺繧峨￠
- recorder 螳溯｡後〒縲檎ｵｵ譁・ｭ励′隱崎ｭ倥＆繧後↑縺・・
**蜴溷屏・・*
- Excel 縺ｧ髢九＞縺ｦ菫晏ｭ倥☆繧九→ `cp932`・・hift-JIS邉ｻ・峨↓螟画鋤縺輔ｌ繧・- 邨ｵ譁・ｭ暦ｼ芋衍ｵｫ｣ 遲会ｼ峨・ cp932 縺ｫ蟄伜惠縺励↑縺・◆繧・`??` 縺ｫ蛹悶￠繧・
**蟇ｾ蜃ｦ豕包ｼ・*
- 笶・Excel 縺ｧ髢九°縺ｪ縺・- 笨・VS Code / 繝｡繝｢蟶ｳ++ / `python` 縺ｧ髢九￥
- 笨・approved_candidate 縺ｮ邱ｨ髮・・ `approve.py` 繧剃ｽｿ縺・
```bash
# 譁・ｭ怜喧縺代′襍ｷ縺阪◆蝣ｴ蜷医・蠕ｩ譌ｧ
python -c "
import csv
rows = list(csv.DictReader(open('production.csv', encoding='cp932')))
# 邨ｵ譁・ｭ怜・縺・?? 縺ｮ蝣ｴ蜷医・ grok_bridge process 縺ｧ蜀咲函謌・"
```

譛蝟・・縲・*譛蛻昴°繧・`approve.py` 邨檎罰縺ｧ謇ｿ隱・*縺吶ｋ驕狗畑縲・
---

### 笶・PermissionError on CSV write

**逞・憾・・*
- `PermissionError: [Errno 13] Permission denied: 'production.csv'`

**蜴溷屏・・*
- production.csv 繧・Excel 繧・ユ繧ｭ繧ｹ繝医お繝・ぅ繧ｿ縺ｧ髢九＞縺溘∪縺ｾ縺ｫ縺励※縺・ｋ

**蟇ｾ蜃ｦ豕包ｼ・*
- 繝輔ぃ繧､繝ｫ繧帝哩縺倥※縺九ｉ蜀榊ｮ溯｡・- 邱ｨ髮・ｸｭ縺ｫ莉悶・繝ｭ繧ｻ繧ｹ縺ｧ譖ｸ縺崎ｾｼ縺ｾ縺ｪ縺・Ν繝ｼ繝ｫ縺ｫ縺吶ｋ

---

## 2. GPU 髢｢騾｣

### 笶・CUDA out of memory

**逞・憾・・*
- `RuntimeError: CUDA out of memory. Tried to allocate ...`

**蜴溷屏・・*
- 蜍慕判逕滓・ / 蛻･縺ｮ TTS / Stable Diffusion 遲峨→荳ｦ蛻怜ｮ溯｡・- 繝舌ャ繝√し繧､繧ｺ縺悟､ｧ縺阪☆縺弱ｋ

**蟇ｾ蜃ｦ豕包ｼ・*

1. **莉悶・ GPU 菴ｿ逕ｨ繝励Ο繧ｻ繧ｹ繧呈ｭ｢繧√ｋ**
   ```bash
   # 荳諡ｬ蛛懈ｭ｢
   taskkill /F /IM python.exe
   ```

2. **繝舌ャ繝√し繧､繧ｺ繧剃ｸ九￡繧・*・亥ｭｦ鄙呈凾・・   ```bash
   --batch-size 2 --gradient-accumulation-steps 4
   ```

3. **gradient checkpointing 繧呈怏蜉ｹ蛹・*・医ヵ繝ｫ蟄ｦ鄙偵・縺ｿ縲・oRA縺ｧ縺ｯ caption 髱槫ｯｾ蠢懊ヰ繧ｰ縺ゅｊ・・
---

### 笞・・GPU 繧堤峡蜊縺吶ｋ繝ｫ繝ｼ繝ｫ

| 蜃ｦ逅・| GPU菴ｿ逕ｨ驥・|
|------|---------|
| 蜍慕判逕滓・ | 繝輔Ν菴ｿ逕ｨ |
| TTS 謗ｨ隲厄ｼ・ecorder・・| 繝輔Ν菴ｿ逕ｨ |
| LoRA 蟄ｦ鄙・| 繝輔Ν菴ｿ逕ｨ |
| 逕ｻ蜒冗函謌撰ｼ・D・・| 繝輔Ν菴ｿ逕ｨ |

竊・**蜷梧凾縺ｫ2縺､縺ｯ襍ｰ繧峨○縺ｪ縺・*縲・laude 繧ｻ繝・す繝ｧ繝ｳ荳ｭ繧ゅ悟虚逕ｻ繧・▲縺ｦ繧九阪→險繧上ｌ縺溘ｉ recorder 縺ｯ豁｢繧√ｋ蛻､譁ｭ縲・
---

## 3. recorder 髢｢騾｣

### 笶・status=pending 縺ｮ縺ｾ縺ｾ蜈ｨ陦・fail

**逞・憾・・*
- 蜈ｨ陦後′ `gen_fail` 縺ｫ縺ｪ繧・- 繝ｭ繧ｰ縺ｫ `infer.py: error` 縺ｮ騾｣邯・
**遒ｺ隱肴焔鬆・ｼ・*

1. 蜊倡匱縺ｧ infer.py 縺悟虚縺上°遒ｺ隱・   ```bash
   E:/irodori/emoji/.venv/Scripts/python.exe E:/irodori/emoji/infer.py \
     --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
     --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
     --text "繝・せ繝・ --caption "闍･縺・･ｳ諤ｧ縺瑚ｩｱ縺励※縺・ｋ縲・ \
     --no-ref --output-wav test.wav
   ```

2. **繧ｨ繝ｩ繝ｼ繝代ち繝ｼ繝ｳ蛻･蟇ｾ蜃ｦ・・*

| 繧ｨ繝ｩ繝ｼ | 蜴溷屏 | 蟇ｾ蜃ｦ |
|--------|------|------|
| FileNotFoundError on .safetensors | 繝√ぉ繝・け繝昴う繝ｳ繝域悴DL | `huggingface-cli login` 蠕後↓HF邨檎罰縺ｧ蜀榊叙蠕・|
| latent_dim mismatch | codec-repo 繧呈欠螳壹＠蠢倥ｌ | `Aratako/Semantic-DACVAE-Japanese-32dim` 繧貞ｿ・域欠螳・|
| empty text | text_with_emoji 縺檎ｩｺ | grok_bridge process 繧貞・螳溯｡・|

---

### 笞・・`--codec-repo` 蠢・・
VoiceDesign 繝｢繝・Ν縺ｯ `latent_dim=32` 縺ｮ codec 繧剃ｽｿ縺・・*謖・ｮ壹＠縺ｪ縺・→ latent_dim 荳堺ｸ閾ｴ縺ｧ繧ｨ繝ｩ繝ｼ**縲・
```bash
# 蠢・医が繝励す繝ｧ繝ｳ
--codec-repo Aratako/Semantic-DACVAE-Japanese-32dim
```

---

## 4. Whisper 隱､隱崎ｭ倥∈縺ｮ蟇ｾ蠢・
### 笞・・貍｢蟄励′髢馴＆縺｣縺ｦ譖ｸ縺崎ｵｷ縺薙＆繧後ｋ

**繧医￥縺ゅｋ繧ｱ繝ｼ繧ｹ・・*
- 縲悟ｭ仙ｮｮ縲坂・ 縲瑚ｦ也せ縲阪瑚ｳ・≡縲・- 縲梧ｷｫ邏九坂・ 縲悟魂髑代・- 縲碁怺螻ｱ縲坂・ 縲檎､ｼ隶・阪梧ｭｴ螻ｱ縲・- 縲檎分莠ｺ縲坂・ 縲悟濠莠ｺ縲・
**蟇ｾ蜃ｦ豕包ｼ・*

1. **譖ｸ縺崎ｵｷ縺薙＠蠕後↓ CSV 逶ｮ隕悶メ繧ｧ繝・け**・亥ｭｦ鄙堤畑繝・・繧ｿ菴懈・譎ゑｼ・2. **譁・ｭ怜喧縺第､懷・・・*
   ```python
   # 縺翫°縺励＞譁・ｭ励ヱ繧ｿ繝ｼ繝ｳ縺ｮ讀懷・
   import csv
   for row in csv.DictReader(open('manifest_raw.csv', encoding='utf-8-sig')):
       if any(c in row['text'] for c in '隕也せ 雉・≡ 蜊ｰ髑・):
           print(f"隕∫｢ｺ隱・ {row['file_name']}: {row['text']}")
   ```

3. **縺ｩ縺・＠縺ｦ繧ゅ・蝣ｴ蜷医・謇句虚菫ｮ豁｣**

LoRA 蟄ｦ鄙堤ｴ譚舌↑繧牙､壼ｰ代・隱､隱崎ｭ倥・險ｱ螳ｹOK・亥｣ｰ雉ｪ繧貞ｭｦ縺ｶ縺縺代□縺九ｉ・峨・
---

## 5. ffmpeg / torchcodec 髢｢騾｣

### 笶・libtorchcodec_core8.dll Could not load

**逞・憾・・*
- `OSError: Could not load this library: ... libtorchcodec_core{4,5,6,7,8}.dll`
- `dataset_tools.py slice` 繧・`prepare_manifest.py` 縺瑚誠縺｡繧・
**蜴溷屏・・*
- FFmpeg 8.0 縺ｨ torchcodec 縺ｮ莠呈鋤諤ｧ蝠城｡鯉ｼ・yTorch 2.11.0 迺ｰ蠅・ｼ・
**蟇ｾ蜃ｦ豕包ｼ・*

1. **`dataset_tools.py slice` 縺ｮ莉｣繧上ｊ**・・   - `E:/irodori/agents/docs/lora_training_guide.md` 縺ｮ librosa 繧ｹ繝ｩ繧､繧ｵ繝ｼ繧剃ｽｿ逕ｨ

2. **`prepare_manifest.py` 縺ｮ莉｣繧上ｊ**・・   - `E:/irodori/emoji/custom_prepare_manifest.py` 繧剃ｽｿ逕ｨ

3. **螳悟・縺ｫ逶ｴ縺励◆縺・ｴ蜷茨ｼ・*
   - FFmpeg 繧・5.x or 6.x 縺ｫ繝繧ｦ繝ｳ繧ｰ繝ｬ繝ｼ繝会ｼ域耳螂ｨ縺励↑縺・ｼ・   - torchcodec 繧偵い繝・・繧ｰ繝ｬ繝ｼ繝会ｼ井ｺ呈鋤迚医′蜃ｺ繧九∪縺ｧ蠕・■・・
---

### 笶・ffmpeg 縺瑚ｦ九▽縺九ｉ縺ｪ縺・ｼ・P3螟画鋤譎ゑｼ・
**逞・憾・・*
- `ma_agent.py --mp3` 縺ｧ `[error] ffmpeg 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ`

**蟇ｾ蜃ｦ豕包ｼ・*
```bash
# winget 縺ｧ繧､繝ｳ繧ｹ繝医・繝ｫ
winget install Gyan.FFmpeg

# PATH 騾壹▲縺ｦ縺・ｋ縺狗｢ｺ隱・which ffmpeg
ffmpeg -version
```

---

## 6. LoRA 蟄ｦ鄙帝未騾｣

### 笶・ModelConfig got unexpected keyword 'max_caption_len'

**菫ｮ豁｣貂医∩**・・ora_train.py 2026-04-25 菫ｮ豁｣迚茨ｼ峨・隧ｳ邏ｰ縺ｯ [`lora_training_guide.md`](./lora_training_guide.md) ﾂｧ6 繝舌げ竭 蜿ら・縲・
### 笶・LatentTextDataset got unexpected keyword 'latent_patch_size'

**菫ｮ豁｣貂医∩**・・ora_train.py 2026-04-25 菫ｮ豁｣迚茨ｼ峨・隧ｳ邏ｰ縺ｯ [`lora_training_guide.md`](./lora_training_guide.md) ﾂｧ6 繝舌げ竭｡ 蜿ら・縲・
### 笶・caption_input_ids and caption_mask are required

**菫ｮ豁｣貂医∩**・・ora_train.py 2026-04-25 菫ｮ豁｣迚茨ｼ峨・隧ｳ邏ｰ縺ｯ [`lora_training_guide.md`](./lora_training_guide.md) ﾂｧ6 繝舌げ竭｢竭｣ 蜿ら・縲・
### 笶・checkpointed() got unexpected keyword 'caption_state'

**蝗樣∩遲・*・啻--grad-checkpoint` 繧・*菴ｿ繧上↑縺・*縲・隧ｳ邏ｰ縺ｯ [`lora_training_guide.md`](./lora_training_guide.md) ﾂｧ6 繝舌げ竭､ 蜿ら・縲・
---

## 7. ma-master 髢｢騾｣

### 笶・approved 髻ｳ螢ｰ繝輔ぃ繧､繝ｫ縺悟ｭ伜惠縺励↑縺・
**逞・憾・・*
- `[warn] 繧ｽ繝ｼ繧ｹ縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ: audio/scene_01/line_001_002.wav`

**蜴溷屏・・*
- approved_candidate 縺ｫ謖・ｮ壹＠縺溷呵｣懃分蜿ｷ縺ｮ繝輔ぃ繧､繝ｫ縺檎┌縺・- audio/ 繝輔か繝ｫ繝蜀・・繝輔ぃ繧､繝ｫ蜷阪′諠ｳ螳壹→驕輔≧

**蟇ｾ蜃ｦ豕包ｼ・*

1. **繝輔ぃ繧､繝ｫ縺ｮ蟄伜惠繧堤｢ｺ隱搾ｼ・*
   ```bash
   ls E:/irodori/projects/{project_name}/audio/{scene_id}/
   ```

2. **production.csv 縺ｮ approved_candidate 繧堤｢ｺ隱搾ｼ・*
   ```python
   import csv
   for r in csv.DictReader(open('production.csv', encoding='utf-8-sig')):
       if r['approved_candidate']:
           print(f"{r['scene_id']}/{r['line_id']}: c{r['approved_candidate']}")
   ```

3. **荳堺ｸ閾ｴ縺ｮ陦後ｒ蜀咲函謌・or approved_candidate 繧剃ｿｮ豁｣**

---

### 笶・master/full_work.wav 縺檎洒縺・
**逞・憾・・*
- 譛溷ｾ・凾髢薙ｈ繧顔洒縺・ｵ仙粋髻ｳ螢ｰ

**蜴溷屏・・*
- 荳驛ｨ縺ｮ陦後〒謇ｿ隱阪′貍上ｌ縺ｦ縺・ｋ
- status 縺・approved 縺ｫ縺ｪ縺｣縺ｦ縺ｪ縺・
**蟇ｾ蜃ｦ豕包ｼ・*

```bash
python -c "
import csv
from collections import Counter
rows = list(csv.DictReader(open('production.csv', encoding='utf-8-sig')))
print(Counter(r['status'] for r in rows))
print(f'approved with candidate: {sum(1 for r in rows if r[\"approved_candidate\"])}')"
```

竊・approved 陦梧焚 = approved_candidate 蜈･蜉帶ｸ医∩陦梧焚 縺ｧ縺ｪ縺・→邨仙粋縺ｫ蜷ｫ縺ｾ繧後↑縺・・
---

## 8. grok_bridge 髢｢騾｣

### 笶・JSONDecodeError on response.json

**逞・憾・・*
- `JSONDecodeError: Expecting ',' delimiter: line N column M`

**蜴溷屏・・*
- Grok 蜃ｺ蜉帙〒繧ｫ繝ｳ繝樊栢縺・/ 蠑慕畑隨ｦ繝溘せ
- 陦碁俣縺ｫ菴呵ｨ医↑遨ｺ逋ｽ陦・
**蟇ｾ蜃ｦ豕包ｼ・*

1. **VS Code 縺ｧ response.json 繧帝幕縺・* 竊・繧ｨ繝ｩ繝ｼ菴咲ｽｮ縺後ワ繧､繝ｩ繧､繝医＆繧後ｋ
2. **繧医￥縺ゅｋ菫ｮ豁｣・・*
   - 繧ｪ繝悶ず繧ｧ繧ｯ繝磯俣縺ｮ繧ｫ繝ｳ繝樊栢縺・   - `"` 縺ｮ髢峨§蠢倥ｌ
   - 譛ｫ蟆ｾ縺ｮ繧ｫ繝ｳ繝樔ｽ吝・

---

### 笞・・emoji_suggestion 縺檎洒縺吶℃繧・
**逞・憾・・*
- Grok 縺・`･ｵ ... 懲` 縺ｮ繧医≧縺ｫ prefix/suffix 縺・蛟九★縺､縺励°蜈･縺｣縺ｦ縺ｪ縺・
**蟇ｾ蜃ｦ豕包ｼ・*
- 繝励Ο繝・Η繝ｼ繧ｵ繝ｼ縺ｫ縲・蛟九★縺､縺ｫ隱ｿ謨ｴ縺励※縲阪→鬆ｼ繧・域焔蜍慕ｷｨ髮・ｼ・- 縺ｾ縺溘・ `script_processor.py` 縺ｮ `build_sandwich()` 縺ｧ蜀肴ｧ狗ｯ・
---

## 9. 謇ｿ隱阪ヵ繝ｭ繝ｼ髢｢騾｣

### 笞・・approvals_template.json 縺ｫ譁ｰ隕剰｡後′蜷ｫ縺ｾ繧後※縺ｪ縺・
**逞・憾・・*
- 蠕後°繧芽ｿｽ蜉縺励◆陦後′ approvals_template.json 縺ｫ蜃ｺ縺ｦ縺薙↑縺・
**蜴溷屏・・*
- qc-reviewer 縺ｯ status=generated 縺ｮ陦後□縺代ｒ QC 縺吶ｋ
- 譌｢縺ｫ approved/done 縺ｫ縺ｪ縺｣縺ｦ繧玖｡後・蜀・QC 縺輔ｌ縺ｪ縺・
**蟇ｾ蜃ｦ豕包ｼ・*

```bash
# 譁ｰ隕剰｡後□縺・qc_agent 繧貞・螳溯｡・python E:/irodori/agents/qc_agent.py {project_name}
```

竊・approvals_template.json 縺ｯ **status=generated 縺ｮ陦後□縺・* 縺ｧ譖ｸ縺肴鋤繧上ｋ・域里蟄・approved 陦後・谿九ｋ・峨・
---

## 10. 縺昴・莉・
### 笞・・Grok 螳溯｡梧凾縺ｮ R-18 蠑ｾ縺九ｌ

**逞・憾・・*
- Grok 縺九ｉ縲瑚ｦ丞宛蟇ｾ雎｡縲阪悟・螳ｹ繧貞､峨∴縺ｦ縲阪→霑斐▲縺ｦ縺上ｋ

**蟇ｾ蜃ｦ豕包ｼ・*
- grok_prompt.md 縺ｮ陦ｨ迴ｾ繧貞ｩ画峇蛹・- 縲後ヵ繧｣繧ｯ繧ｷ繝ｧ繝ｳ縺ｮ髻ｳ螢ｰ蛻ｶ菴懊阪梧・莠ｺ蜷代￠蜷御ｺｺ縲阪ｒ譏手ｨ・- 縺昴ｌ縺ｧ繧ゅム繝｡縺ｪ繧牙挨 LLM・・laude 縺ｧ縺ｯ荳榊庄・・
---

### 庁 Whisper 縺ｮ繝｢繝・Ν驕ｸ謚・
| 繝｢繝・Ν | 邊ｾ蠎ｦ | 騾溷ｺｦ | 逕ｨ騾・|
|--------|------|------|------|
| tiny | 笘・| 笞｡笞｡笞｡笞｡ | 隧ｦ鬨鍋畑 |
| base | 笘・・ | 笞｡笞｡笞｡ | 霆ｽ驥・|
| small | 笘・・笘・| 笞｡笞｡ | 繝舌Λ繝ｳ繧ｹ |
| medium | 笘・・笘・・ | 笞｡ | 讓呎ｺ匁耳螂ｨ |
| **large-v3** | 笘・・笘・・笘・| 世 | **譛ｬ逡ｪ謗ｨ螂ｨ** |

LoRA 蟄ｦ鄙堤ｴ譚舌・ **large-v3** 荳謚槭・
---

## 11. 蝗ｰ縺｣縺滓凾縺ｮ遒ｺ隱肴焔鬆・
1. **production.csv 縺ｮ status 蛻・ｸ・ｒ遒ｺ隱・*
   ```python
   from collections import Counter
   import csv
   rows = list(csv.DictReader(open('production.csv', encoding='utf-8-sig')))
   print(Counter(r['status'] for r in rows))
   ```

2. **audio/ 繝輔か繝ｫ繝縺ｮ繝輔ぃ繧､繝ｫ謨ｰ繧堤｢ｺ隱・*
   ```bash
   find E:/irodori/projects/{name}/audio -name "*.wav" | wc -l
   ```

3. **繧ｨ繝ｩ繝ｼ繝ｭ繧ｰ繧呈怙蠕後∪縺ｧ隱ｭ繧**・域怙蛻昴・繧ｨ繝ｩ繝ｼ縺倥ｃ縺ｪ縺乗怙蠕後・繧ｨ繝ｩ繝ｼ縺悟次蝗・・
4. **縺薙・繝峨く繝･繝｡繝ｳ繝医・隧ｲ蠖鍋ｯ繧呈､懃ｴ｢**

5. **Claude・亥ｧ峨＆繧難ｼ峨↓謚輔￡繧・*

---

**譛邨よ峩譁ｰ: 2026-04-25**
