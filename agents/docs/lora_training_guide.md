# LoRA 蟄ｦ鄙偵ぎ繧､繝会ｼ・rodori-TTS / Emoji-TTS・・
蜿ら・髻ｳ螢ｰ縺九ｉ縲悟崋螳壹・螢ｰ縲阪ｒ菴懊ｋ縺溘ａ縺ｮ LoRA 繝輔ぃ繧､繝ｳ繝√Η繝ｼ繝九Φ繧ｰ謇矩・・2026-04-25 縺ｫ voice_ganyu_v1 繧剃ｽ懈・縺励◆譎ゅ・遏･隕九・繝ｼ繧ｹ縲・
---

## 0. 讎りｦ・
### LoRA 縺ｧ菴輔′縺ｧ縺阪ｋ縺・- 謨ｰ蜊∵悽縺ｮ蜿ら・髻ｳ螢ｰ縺九ｉ **繧ｭ繝｣繝ｩ蝗ｺ譛峨・螢ｰ** 繧貞ｭｦ鄙・- 繝吶・繧ｹ繝｢繝・Ν・・ratako/Irodori-TTS-500M-v2-VoiceDesign・峨↓ **6.4MB 縺ｮ蟆上＆縺ｪ蟾ｮ蛻・い繝繝励ち** 繧剃ｽ懊ｋ
- 謗ｨ隲匁凾縺ｫ `--lora-path` 縺ｧ隱ｭ縺ｿ霎ｼ繧縺縺代〒驕ｩ逕ｨ蜿ｯ閭ｽ
- `--lora-scale 0.0縲・.0` 縺ｧ繝吶・繧ｹ螢ｰ蟇・ｊ or LoRA蟇・ｊ縺ｫ隱ｿ謨ｴ縺ｧ縺阪ｋ

### 繧ｼ繝ｭ繧ｷ繝ｧ繝・ヨ蜿ら・髻ｳ螢ｰ vs LoRA

| 隕ｳ轤ｹ | 繧ｼ繝ｭ繧ｷ繝ｧ繝・ヨ・・-ref-wav・・| LoRA |
|------|------------------------|------|
| 蠢・ｦ∫ｴ譚・| 蜿ら・髻ｳ螢ｰ1譛ｬ | 蟄ｦ鄙堤畑髻ｳ螢ｰ 50譛ｬ蜑榊ｾ・|
| 蟄ｦ鄙呈凾髢・| 荳崎ｦ・| 30縲・0蛻・|
| 荳雋ｫ諤ｧ | 笆ｳ 繧ｬ繝√Ε隕∫ｴ蠑ｷ縺・| 笳・縺ｻ縺ｼ蝗ｺ螳・|
| 繧ｹ繝医Ξ繝ｼ繧ｸ | 0 | ~6MB・医い繝繝励ち縺ｮ縺ｿ・・|

縲悟酔縺伜｣ｰ縺ｧ驥冗肇縺励◆縺・阪↑繧・**LoRA荳謚・*縲・
---

## 1. 蜑肴署迺ｰ蠅・
### 繝上・繝峨え繧ｧ繧｢
- **VRAM 16GB 莉･荳頑耳螂ｨ**・・TX 4060 Ti / 5060 Ti 繧ｯ繝ｩ繧ｹ・・- **batch_size=2 + gradient_accumulation=4** 縺悟ｮ牙・蝨擾ｼ亥ｮ溷柑繝舌ャ繝・8・・
### 蠢・医Λ繧､繝悶Λ繝ｪ
```bash
# Emoji-TTS 縺ｮ venv 縺ｫ蠢・ｦ・pip install peft faster-whisper librosa soundfile torch
```

### 繝｢繝・Ν繝√ぉ繝・け繝昴う繝ｳ繝・- 繝吶・繧ｹ: `E:/irodori/emoji/checkpoints/Aratako_Irodori-TTS-500M-v2-VoiceDesign/model.safetensors`
- 繧ｳ繝ｼ繝・ャ繧ｯ: `Aratako/Semantic-DACVAE-Japanese-32dim`・・uggingFace 縺九ｉ閾ｪ蜍疋L・・
### `lora_train.py` 縺ｮ菫ｮ豁｣貂医∩繝舌・繧ｸ繝ｧ繝ｳ縺悟ｿ・ｦ・2026-04-25 譎らせ縺ｧ繝輔か繝ｼ繧ｯ迚医↓ **VoiceDesign 蟇ｾ蠢懊ヰ繧ｰ縺・莉ｶ** 縺ゅｊ縲～E:/irodori/emoji/lora_train.py` 繧剃ｿｮ豁｣貂医∩縲りｩｳ邏ｰ縺ｯ ﾂｧ6 繝医Λ繝悶Ν繧ｷ繝･繝ｼ繝・ぅ繝ｳ繧ｰ 繧貞盾辣ｧ縲・
---

## 2. 繝代う繝励Λ繧､繝ｳ蜈ｨ菴灘峙

```
[髻ｳ螢ｰ邏譚疹.wav
    竊・竭 繧ｹ繝ｩ繧､繧ｹ・・ibrosa迢ｬ閾ｪ・・[2縲・2遘偵・繧ｻ繧ｰ繝｡繝ｳ繝・.wav ﾃ・N譛ｬ
    竊・竭｡ Whisper 繧ｭ繝｣繝励す繝ｧ繝ｳ
metadata.csv・・ile_name, text, caption・・    竊・竭｢ DACVAE 貎懷惠螟画鋤
manifest.jsonl + latents/*.pt
    竊・竭｣ LoRA 蟄ｦ鄙・lora_checkpoint_final_ema/
    竊・竭､ 謗ｨ隲悶〒隱ｭ縺ｿ霎ｼ縺ｿ
螳梧・髻ｳ螢ｰ.wav
```

---

## 3. 繝・・繧ｿ貅門ｙ

### Step 1: 髻ｳ螢ｰ邏譚舌・鄂ｮ縺榊ｴ謇
```
E:/irodori/emoji/input/{voice_name}/*.wav
```

**邏譚舌・逶ｮ螳会ｼ・*
| 隕ｳ轤ｹ | 謗ｨ螂ｨ |
|------|------|
| 蜷郁ｨ域凾髢・| 5縲・0蛻・|
| 1繝輔ぃ繧､繝ｫ髟ｷ | 菴募・縺ｧ繧ょ庄・亥ｾ後〒繧ｹ繝ｩ繧､繧ｹ・・|
| 繧ｵ繝ｳ繝励Ν繝ｬ繝ｼ繝・| 48kHz謗ｨ螂ｨ・郁・蜍輔〒繝ｪ繧ｵ繝ｳ繝励Ν・・|
| 繝舌Μ繧ｨ繝ｼ繧ｷ繝ｧ繝ｳ | 蟷ｳ髱吶・蝟懈貞凍讌ｽ縺梧ｷｷ縺悶▲縺ｦ繧九→笳・|

### Step 2: 菴懈･ｭ繝・ぅ繝ｬ繧ｯ繝医Μ菴懈・
```bash
mkdir -p E:/irodori/emoji/data/{voice_name}/slices
mkdir -p E:/irodori/emoji/data/{voice_name}/latents
```

### Step 3: 繧ｹ繝ｩ繧､繧ｹ・・ibrosa 迢ｬ閾ｪ繧ｹ繧ｯ繝ｪ繝励ヨ・・
**豕ｨ諢擾ｼ・* Emoji-TTS 縺ｮ `dataset_tools.py slice` 縺ｯ torchcodec 繧剃ｽｿ縺・′縲・*FFmpeg 8.0 迺ｰ蠅・〒縺ｯ蜍穂ｽ懊＠縺ｪ縺・*縲ゆｻ｣譖ｿ縺ｨ縺励※莉･荳九ｒ螳溯｡鯉ｼ・
```python
# librosa_slicer.py・医う繝ｳ繝ｩ繧､繝ｳ縺ｧ螳溯｡悟庄・・import os, glob
import numpy as np, soundfile as sf, librosa

INPUT_DIR = 'E:/irodori/emoji/input/{voice_name}'
OUTPUT_DIR = 'E:/irodori/emoji/data/{voice_name}/slices'
MIN_SEC = 2.0
MAX_SEC = 12.0
TOP_DB = 35  # 辟｡髻ｳ蛻､螳夲ｼ・B・・
os.makedirs(OUTPUT_DIR, exist_ok=True)
files = sorted(glob.glob(f'{INPUT_DIR}/*.wav'))

total_out = 0
for f in files:
    data, sr = sf.read(f)
    if data.ndim > 1: data = data.mean(axis=1)
    duration = len(data) / sr
    base = os.path.splitext(os.path.basename(f))[0]

    if duration < MIN_SEC:
        continue
    if duration <= MAX_SEC:
        sf.write(f'{OUTPUT_DIR}/{base}_001.wav', data, sr)
        total_out += 1
        continue

    # 12遘定ｶ・ 辟｡髻ｳ蛹ｺ髢薙〒蛻・牡
    intervals = librosa.effects.split(data, top_db=TOP_DB, frame_length=2048, hop_length=512)
    segments = []
    cur_start, cur_end = None, None
    for s, e in intervals:
        if cur_start is None:
            cur_start, cur_end = s, e
        else:
            seg_dur = (e - cur_start) / sr
            gap_dur = (s - cur_end) / sr
            if seg_dur > MAX_SEC:
                segments.append((cur_start, cur_end))
                cur_start, cur_end = s, e
            elif gap_dur > 0.6:
                cur_dur = (cur_end - cur_start) / sr
                if cur_dur >= MIN_SEC:
                    segments.append((cur_start, cur_end))
                    cur_start, cur_end = s, e
                else:
                    cur_end = e
            else:
                cur_end = e
    if cur_start is not None:
        cur_dur = (cur_end - cur_start) / sr
        if cur_dur >= MIN_SEC:
            segments.append((cur_start, cur_end))

    valid_segs = []
    for s, e in segments:
        d = (e - s) / sr
        if d < MIN_SEC: continue
        if d <= MAX_SEC:
            valid_segs.append((s, e))
        else:
            n = int(np.ceil(d / MAX_SEC))
            step = (e - s) // n
            for i in range(n):
                ss = s + i * step
                ee = s + (i+1) * step if i < n-1 else e
                if (ee - ss) / sr >= MIN_SEC:
                    valid_segs.append((ss, ee))

    for i, (s, e) in enumerate(valid_segs):
        pad = int(sr * 0.03)
        s_pad = max(0, s - pad)
        e_pad = min(len(data), e + pad)
        sf.write(f'{OUTPUT_DIR}/{base}_{i+1:03d}.wav', data[s_pad:e_pad], sr)
        total_out += 1

print(f'繧ｹ繝ｩ繧､繧ｹ蜃ｺ蜉・ {total_out}譛ｬ')
```

### Step 4: Whisper 縺ｧ繧ｭ繝｣繝励す繝ｧ繝ｳ逕滓・

```bash
cd E:/irodori/emoji && .venv/Scripts/python.exe dataset_tools.py caption \
  --input data/{voice_name}/slices \
  --output-manifest data/{voice_name}/manifest_raw.csv \
  --format csv \
  --model large-v3 \
  --language ja \
  --voice-design \
  --voice-design-caption "{繧ｭ繝｣繝ｩ縺ｮ螢ｰ繧定｡ｨ迴ｾ縺吶ｋ繧ｭ繝｣繝励す繝ｧ繝ｳ譁・" \
  --device cuda
```

**voice-design-caption 縺ｮ萓具ｼ・*
- 關ｽ縺｡逹縺・◆螂ｳ諤ｧ: `"遨上ｄ縺九〒蜆ｪ縺励＞闍･縺・･ｳ諤ｧ縺後∬誠縺｡逹縺・◆髱吶°縺ｪ螢ｰ縺ｧ荳∝ｯｧ縺ｫ隧ｱ縺励※縺・ｋ縲・`
- 蜈・ｰ励↑蟆大･ｳ: `"譏弱ｋ縺丞・豌励↑蟆大･ｳ縺後√・縺阪・縺阪→繧医￥騾壹ｋ螢ｰ縺ｧ隧ｱ縺励※縺・ｋ縲・`
- 繧ｯ繝ｼ繝ｫ縺ｪ螟ｧ莠ｺ: `"繧ｯ繝ｼ繝ｫ縺ｧ遏･逧・↑螂ｳ諤ｧ縺後∽ｽ弱ａ縺ｮ關ｽ縺｡逹縺・◆螢ｰ縺ｧ豺｡縲・→隧ｱ縺励※縺・ｋ縲・`

### Step 5: audiofolder 蠖｢蠑上↓謨ｴ蠖｢

```bash
cp data/{voice_name}/manifest_raw.csv data/{voice_name}/slices/metadata.csv
```

### Step 6: DACVAE 貎懷惠螟画鋤・・orchcodec 繝舌う繝代せ迚茨ｼ・
`E:/irodori/emoji/custom_prepare_manifest.py` 繧剃ｽｿ縺・ｼ医％縺ｮ繧ｹ繧ｯ繝ｪ繝励ヨ縺ｯ2026-04-25縺ｫ菴懈・縲》orchcodec/HF datasets 繧堤ｵ檎罰縺励↑縺・ｰ｡譏鍋沿・峨・
```bash
cd E:/irodori/emoji && .venv/Scripts/python.exe custom_prepare_manifest.py \
  --csv data/{voice_name}/manifest_raw.csv \
  --audio-dir data/{voice_name}/slices \
  --output-manifest data/{voice_name}/manifest.jsonl \
  --latent-dir data/{voice_name}/latents \
  --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
  --device cuda
```

### Step 7: manifest.jsonl 縺ｮ繝代せ遒ｺ隱・
`latent_path` 縺・**manifest.jsonl 縺ｨ蜷後§繝・ぅ繝ｬ繧ｯ繝医Μ縺九ｉ縺ｮ逶ｸ蟇ｾ繝代せ** 縺ｫ縺ｪ縺｣縺ｦ縺・ｋ縺狗｢ｺ隱阪Ａdata/{voice_name}/latents/...` 縺ｮ繧医≧縺ｪ髫主ｱ､縺悟性縺ｾ繧後※縺・ｋ蝣ｴ蜷医・縲～latents/{filename}.pt` 縺縺代↓菫ｮ豁｣縺吶ｋ縲・
---

## 4. LoRA 蟄ｦ鄙・
### 繧ｳ繝槭Φ繝会ｼ域耳螂ｨ繝代Λ繝｡繝ｼ繧ｿ・・
```bash
cd E:/irodori/emoji && .venv/Scripts/python.exe lora_train.py \
  --base-model checkpoints/Aratako_Irodori-TTS-500M-v2-VoiceDesign/model.safetensors \
  --manifest data/{voice_name}/manifest.jsonl \
  --output-dir lora/voice_{voice_name}_v1 \
  --lora-rank 16 \
  --lora-alpha 32.0 \
  --lora-dropout 0.05 \
  --max-steps 3000 \
  --warmup-steps 300 \
  --stable-steps 2100 \
  --batch-size 2 \
  --gradient-accumulation-steps 4 \
  --optimizer muon \
  --lr 0.0003 \
  --precision bf16 \
  --device cuda \
  --save-every 500 \
  --log-every 50
```

### 笞・・驥崎ｦ√↑豕ｨ諢冗せ

| 鬆・岼 | 險ｭ螳・| 逅・罰 |
|------|------|------|
| `--grad-checkpoint` | **菴ｿ繧上↑縺・* | VoiceDesign繝｢繝・Ν縺ｮ caption 蠑墓焚縺ｨ髱樔ｺ呈鋤 |
| `--batch-size` | **2** | grad_checkpoint 縺ｪ縺励□縺ｨ VRAM 菴呵｣輔′蠢・ｦ・|
| `--gradient-accumulation-steps` | **4** | 螳溷柑繝舌ャ繝√ｒ 8 縺ｫ菫昴▽ |
| `--max-steps` | **3000** | 50莉ｶ蜑榊ｾ後・繝・・繧ｿ縺ｧ驕ｩ蛻・ょ､壹☆縺弱ｋ縺ｨ驕主ｭｦ鄙・|

### 蟄ｦ鄙剃ｸｭ縺ｮ謖・ｨ・- 蛻晄悄 loss: 0.85縲・.95
- 邨ら乢 loss: 0.45縲・.55 遞句ｺｦ縺ｾ縺ｧ荳九′繧後・蟄ｦ鄙呈・蜉・- 騾溷ｺｦ: RTX 5060 Ti 縺ｧ 1.7 steps/sec縲・000 step = 邏・0蛻・
### 蜃ｺ蜉帙ヵ繧｡繧､繝ｫ
```
lora/voice_{voice_name}_v1/
  笏懌楳 lora_checkpoint_0000500_ema/
  笏懌楳 lora_checkpoint_0001000_ema/
  笏懌楳 lora_checkpoint_0001500_ema/
  笏懌楳 lora_checkpoint_0002000_ema/
  笏懌楳 lora_checkpoint_0002500_ema/
  笏懌楳 lora_checkpoint_0003000_ema/
  笏披楳 lora_checkpoint_final_ema/   竊・縺薙ｌ繧剃ｽｿ縺・```

---

## 5. 謗ｨ隲悶〒菴ｿ縺・
### 蜊倡匱逕滓・

```bash
cd E:/irodori/emoji && .venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
  --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
  --text "繧ｻ繝ｪ繝輔ユ繧ｭ繧ｹ繝・ \
  --caption "螢ｰ縺ｮ繧ｭ繝｣繝ｩ隱ｬ譏取枚" \
  --no-ref \
  --num-steps 40 \
  --num-candidates 3 \
  --cfg-scale-text 5.0 \
  --cfg-scale-caption 5.0 \
  --cfg-scale-speaker 5.0 \
  --cfg-guidance-mode alternating \
  --lora-path lora/voice_{voice_name}_v1/lora_checkpoint_final_ema \
  --lora-scale 1.0 \
  --model-precision bf16 \
  --output-wav outputs/test.wav \
  --no-show-timings
```

### `--lora-scale` 縺ｮ隱ｿ謨ｴ逶ｮ螳・
| 繧ｹ繧ｱ繝ｼ繝ｫ | 蜉ｹ譫・|
|---------|------|
| 0.0 | LoRA 辟｡蜉ｹ蛹厄ｼ医・繝ｼ繧ｹ螢ｰ縺ｮ縺ｿ・・|
| 0.5 | 繝吶・繧ｹ蟇・ｊ縲´oRA 縺ｯ縺・▲縺吶ｉ |
| 1.0 | 讓呎ｺ悶ょｭｦ鄙帝壹ｊ縺ｮ螢ｰ |
| 1.5 | LoRA 蠑ｷ隱ｿ縲ょ｣ｰ雉ｪ蝗ｺ螳壹′蠑ｷ縺・|
| 2.0 莉･荳・| 繝弱う繧ｺ繝ｻ蟠ｩ螢翫Μ繧ｹ繧ｯ鬮倥＞ |

---

## 6. 繝医Λ繝悶Ν繧ｷ繝･繝ｼ繝・ぅ繝ｳ繧ｰ・・026-04-25 縺ｧ逋ｺ逕溘＠縺溷ｮ溽ｸｾ・・
### 繝舌げ竭 `max_caption_len` got an unexpected keyword
**逞・憾:** `TypeError: ModelConfig.__init__() got an unexpected keyword argument 'max_caption_len'`
**蜴溷屏:** VoiceDesign 縺ｮ safetensors metadata 縺ｫ `max_caption_len` (TrainConfig 繝輔ぅ繝ｼ繝ｫ繝・ 縺梧ｷｷ蜈･
**菫ｮ豁｣:** `lora_train.py` `_load_base_model()` 縺ｮ `_INF_KEYS` 縺ｫ `max_caption_len` 繧定ｿｽ蜉縺励～fields(ModelConfig)` 縺ｧ繝輔ぅ繝ｫ繧ｿ

### 繝舌げ竭｡ `latent_patch_size` 蠑墓焚縺檎┌縺・**逞・憾:** `TypeError: LatentTextDataset.__init__() got an unexpected keyword argument 'latent_patch_size'`
**蜴溷屏:** dataset.py 縺ｮAPI螟画峩・・latent_patch_size` 蠑墓焚縺悟炎髯､・・**菫ｮ豁｣:** `lora_train.py` 縺ｮ `LatentTextDataset(...)` 3邂・園縺九ｉ `latent_patch_size=...` 繧貞炎髯､

### 繝舌げ竭｢ caption_tokenizer 縺悟ｿ・・**逞・憾:** `TypeError: TTSCollator.__init__() missing 1 required positional argument: 'caption_tokenizer'`
**菫ｮ豁｣:** VoiceDesign 逕ｨ縺ｫ `PretrainedTextTokenizer.from_pretrained()` 縺ｧ caption tokenizer 繧呈ｧ狗ｯ峨＠縺ｦ貂｡縺・
### 繝舌げ竭｣ caption_input_ids 縺梧ｸ｡縺｣縺ｦ縺ｪ縺・**逞・憾:** `ValueError: caption_input_ids and caption_mask are required when caption conditioning is enabled.`
**菫ｮ豁｣:** 蟄ｦ鄙偵Ν繝ｼ繝励〒 `batch["caption_ids"]` / `batch["caption_mask"]` 繧貞叙繧雁・縺励※ `model()` 縺ｫ貂｡縺・
### 繝舌げ竭､ gradient_checkpoint 縺ｧ caption 髱槫ｯｾ蠢・**逞・憾:** `TypeError: ... checkpointed() got an unexpected keyword argument 'caption_state'`
**蝗樣∩遲・** `--grad-checkpoint` 繧・*菴ｿ繧上↑縺・*縲ゆｻ｣繧上ｊ縺ｫ `batch_size=2 / gradient-accumulation=4` 縺ｧ蟇ｾ蠢・
### 繝舌げ竭･ torchcodec 縺・FFmpeg 8 縺ｨ髱樔ｺ呈鋤
**逞・憾:** `OSError: Could not load this library: ... libtorchcodec_core8.dll`
**蝗樣∩遲・** `dataset_tools.py slice` 縺ｯ菴ｿ繧上★ **librosa 迢ｬ閾ｪ繧ｹ繝ｩ繧､繧ｵ繝ｼ** 繧剃ｽｿ縺・～prepare_manifest.py` 繧ゆｽｿ繧上★ **`custom_prepare_manifest.py`** 繧剃ｽｿ縺・
### 繝舌げ竭ｦ manifest 縺ｮ latent_path 縺御ｺ碁㍾邨仙粋
**逞・憾:** `FileNotFoundError: ...\data\ganyu_v1\data\ganyu_v1\latents\xxx.pt`
**蜴溷屏:** prepare_manifest 螳溯｡梧凾縺ｫ逶ｸ蟇ｾ繝代せ縺ｧ謖・ｮ壹☆繧九→繝代せ縺御ｺ碁㍾邨仙粋縺輔ｌ繧・**菫ｮ豁｣:** manifest.jsonl 縺ｮ `latent_path` 繧・`latents/{filename}.pt` 縺縺代・逶ｸ蟇ｾ繝代せ縺ｫ譖ｸ縺肴鋤縺医ｋ

---

## 7. 繝輔ぃ繧､繝ｫ謨ｴ逅・
### 荳ｭ髢薙メ繧ｧ繝・け繝昴う繝ｳ繝医・蜑企勁
蟄ｦ鄙貞ｮ御ｺ・ｾ後～lora_checkpoint_final_ema` 莉･螟悶・騾壼ｸｸ荳崎ｦ・ｼ・
```bash
rm -rf E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0000500_ema \
       E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0001000_ema \
       E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0001500_ema \
       E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0002000_ema \
       E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0002500_ema \
       E:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0003000_ema
```

**谿九☆逅・罰縺後≠繧句ｴ蜷茨ｼ・*
- 驕主ｭｦ鄙偵′逍代ｏ縺励＞ 竊・荳ｭ逶､・・500step・峨→豈碑ｼ・＠縺溘＞
- A/B 繝・せ繝医＠縺溘＞ 竊・蜷・せ繝・ャ繝励ｒ荳ｦ縺ｹ縺ｦ閨ｴ縺肴ｯ斐∋

### 繧ｹ繝ｩ繧､繧ｹ繝ｻ貎懷惠繝輔ぃ繧､繝ｫ
蟄ｦ鄙偵′螳御ｺ・＠縺ｦ LoRA 縺悟撫鬘後↑縺丞虚縺・※縺・ｌ縺ｰ縲√せ繝ｩ繧､繧ｹ縺ｨ貎懷惠繧ょ炎髯､蜿ｯ・亥・蟄ｦ鄙偵☆繧区凾縺ｯ縺ｾ縺滉ｽ懊ｊ逶ｴ縺暦ｼ会ｼ・
```bash
# 螳ｹ驥城ｼ霑ｫ縺励※縺九ｉ豸医☆縺ｧ蜊∝・
rm -rf E:/irodori/emoji/data/{voice_name}/
```

---

## 8. 繝代う繝励Λ繧､繝ｳ縺ｸ縺ｮ邨・∩霎ｼ縺ｿ・亥ｮ溯｣・ｸ医∩ 2026-04-25・・
production.csv 縺ｫ `lora_path` / `lora_scale` 蛻励′霑ｽ蜉縺輔ｌ縺ｦ縺翫ｊ縲〉ecorder.py 縺瑚・蜍慕噪縺ｫ隱ｭ縺ｿ蜿悶▲縺ｦ infer.py 縺ｫ貂｡縺吶・*Claude 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝育ｵ檎罰 / CLI 逶ｴ謗･螳溯｡後←縺｡繧峨〒繧る←逕ｨ縺輔ｌ繧・*縲・
### 菴ｿ縺・婿 A: set_lora.py 縺ｧ荳諡ｬ險ｭ螳夲ｼ域耳螂ｨ・・
```bash
# 蜈ｨ陦後↓驕ｩ逕ｨ
python E:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 迚ｹ螳壹す繝ｼ繝ｳ縺縺・python E:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scenes scene_01,scene_02

# 迚ｹ螳・status 縺ｮ陦後□縺・python E:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --status pending

# 隗｣髯､
python E:/irodori/agents/set_lora.py {project_name} --clear

# 迴ｾ蝨ｨ縺ｮ險ｭ螳夂｢ｺ隱・python E:/irodori/agents/set_lora.py {project_name} --show
```

LoRA 蜷阪・隗｣豎ｺ・・1. 邨ｶ蟇ｾ繝代せ謖・ｮ・竊・縺昴・縺ｾ縺ｾ
2. 蜷榊燕縺ｮ縺ｿ謖・ｮ・竊・`E:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema` 繧定・蜍墓爾邏｢

### 菴ｿ縺・婿 B: default_captions.json 繝励Ο繝輔ぃ繧､繝ｫ縺ｧ邏蝉ｻ倥￠

```json
"譌･蟶ｸ莨夊ｩｱ_逕倬岑": {
  "caption": "遨上ｄ縺九〒蜆ｪ縺励＞闍･縺・･ｳ諤ｧ縺後∬誠縺｡逹縺・◆髱吶°縺ｪ螢ｰ縺ｧ荳∝ｯｧ縺ｫ隧ｱ縺励※縺・ｋ縲・,
  "cfg_text": 3.0,
  "cfg_caption": 3.0,
  "cfg_speaker": 5.0,
  "cfg_guidance_mode": "joint",
  "num_steps": 40,
  "lora_path": "E:/irodori/emoji/lora/voice_ganyu_v1/lora_checkpoint_final_ema",
  "lora_scale": 1.0
}
```

竊・casting apply / grok_bridge process 譎ゅ↓閾ｪ蜍輔〒 production.csv 縺ｫ譖ｸ縺崎ｾｼ縺ｾ繧後ｋ縲・
### 襍ｷ蜍慕ｵ瑚ｷｯ縺ｫ髢｢繧上ｉ縺夐←逕ｨ縺輔ｌ繧・
- 笨・Claude 繧ｨ繝ｼ繧ｸ繧ｧ繝ｳ繝茨ｼ・ecorder・臥ｵ檎罰
- 笨・CLI 逶ｴ謗･・・python recorder.py {project_name}`・・
蛻､譁ｭ縺ｯ production.csv 縺ｮ `lora_path` 蛻・邂・園縺ｫ髮・ｴ・＆繧後※縺・ｋ縺溘ａ縲∬ｵｷ蜍慕ｵ瑚ｷｯ繧貞撫繧上★蜷後§蜍穂ｽ懊↓縺ｪ繧九・
---

## 9. 蜿り・ｳ・侭

- [Emoji-TTS README_ja.md](E:/irodori/emoji/README_ja.md)
- [HuggingFace - Aratako/Irodori-TTS-500M-v2-VoiceDesign](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- [PEFT (Parameter-Efficient Fine-Tuning)](https://github.com/huggingface/peft)

---

**譛邨よ峩譁ｰ: 2026-04-25 / 蛻晉沿菴懈・: voice_ganyu_v1 蛻ｶ菴懈凾**
