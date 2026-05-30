# 邏榊刀蜑榊刀雉ｪ繝√ぉ繝・け繝ｪ繧ｹ繝・
螳梧・髻ｳ螢ｰ繧堤ｴ榊刀繝ｻ驟榊ｸ・☆繧句燕縺ｫ蠢・★遒ｺ隱阪☆繧矩・岼髮・・
---

## 0. 縺薙・繝√ぉ繝・け繝ｪ繧ｹ繝医・菴ｿ縺・婿

- 蜷・そ繧ｯ繧ｷ繝ｧ繝ｳ縺ｮ 笘・繧剃ｸ翫°繧蛾・↓遒ｺ隱・- 1縺､縺ｧ繧・NG 縺後≠繧後・隧ｲ蠖薙☆繧句ｯｾ蜃ｦ豕輔↓蠕薙▲縺ｦ菫ｮ豁｣
- 蜈ｨ驛ｨ 笨・縺ｫ縺ｪ縺｣縺ｦ縺九ｉ邏榊刀

---

## 1. 繝輔ぃ繧､繝ｫ蟄伜惠繝√ぉ繝・け

### 笘・master/full_work.wav 縺悟ｭ伜惠縺吶ｋ
```bash
ls -la E:/irodori/projects/{name}/master/full_work.wav
```

### 笘・繧ｷ繝ｼ繝ｳ蛻･繝輔ぃ繧､繝ｫ縺梧Φ螳夐壹ｊ縺ゅｋ
```bash
ls E:/irodori/projects/{name}/master/*.wav | wc -l
```
竊・譛溷ｾ・､・壹す繝ｼ繝ｳ謨ｰ + 1・・ull_work.wav 蜷ｫ繧・・
### 笘・MP3 縺悟ｿ・ｦ√↑繧・mp3/ 繝輔か繝ｫ繝縺ｫ縺ゅｋ・医が繝励す繝ｧ繝ｳ・・```bash
ls E:/irodori/projects/{name}/mp3/
```

---

## 2. 陦梧焚繝√ぉ繝・け

### 笘・production.csv 縺ｧ approved 陦梧焚 = 譛溷ｾ・｡梧焚
```python
import csv
rows = list(csv.DictReader(open('E:/irodori/projects/{name}/production.csv', encoding='utf-8-sig')))
approved = [r for r in rows if r['approved_candidate']]
print(f'approved: {len(approved)}陦・)
```

### 笘・approved/ 繝輔か繝ｫ繝縺ｮ繝輔ぃ繧､繝ｫ謨ｰ縺御ｸ閾ｴ
```bash
find E:/irodori/projects/{name}/approved -name "*.wav" | wc -l
```
竊・approved 陦梧焚縺ｨ荳閾ｴ縺吶ｋ縺薙→

---

## 3. 髻ｳ螢ｰ髟ｷ繝√ぉ繝・け

### 笘・full_work.wav 縺ｮ邱乗凾髢薙′莨∫判譖ｸ騾壹ｊ
```python
import soundfile as sf
info = sf.info('E:/irodori/projects/{name}/master/full_work.wav')
print(f'{info.duration/60:.1f}蛻・)
```

### 笘・蜷・す繝ｼ繝ｳ縺ｮ譎る俣縺梧･ｵ遶ｯ縺ｫ遏ｭ縺上↑縺・- 1繧ｻ繝ｪ繝募ｹｳ蝮・5縲・遘・- 50陦後・繧ｷ繝ｼ繝ｳ縺ｧ4縲・蛻・′讓呎ｺ・
### 笘・蛟九・・繧ｻ繝ｪ繝輔ヵ繧｡繧､繝ｫ縺ｫ 0.5遘呈悴貅縺檎┌縺・```python
import soundfile as sf, glob
for f in glob.glob('E:/irodori/projects/{name}/approved/**/*.wav', recursive=True):
    d = sf.info(f).duration
    if d < 0.5:
        print(f'笞・・{f}: {d:.2f}遘・)
```

---

## 4. 髻ｳ雉ｪ繝√ぉ繝・け

### 笘・qc_report.csv 縺ｧ qc_fail 陦後′辟｡縺・ｼ・r 蜈ｨ驛ｨ done・・```python
import csv
from collections import Counter
rows = list(csv.DictReader(open('E:/irodori/projects/{name}/qc_report.csv', encoding='utf-8-sig')))
print(Counter(r['qc_result'] for r in rows))
```

### 笘・繧ｯ繝ｪ繝・ヴ繝ｳ繧ｰ・・eak 竕･ 0.99・峨′ approved 縺ｫ蜷ｫ縺ｾ繧後※縺ｪ縺・qc_report.csv 縺ｧ peak_value > 0.99 縺ｮ陦後ｒ遒ｺ隱阪りｩｲ蠖薙′縺ゅｌ縺ｰ蛻･蛟呵｣懊↓蛻・ｊ譖ｿ縺医・
### 笘・辟｡髻ｳ蛻､螳夲ｼ・MS < 0.001・峨′ approved 縺ｫ蜷ｫ縺ｾ繧後※縺ｪ縺・qc_report.csv 縺ｧ rms_energy 縺梧･ｵ遶ｯ縺ｫ菴弱＞陦後ｒ繝√ぉ繝・け縲・
### 笘・繝弱う繧ｺ繝ｻ縺九☆繧後′逶ｮ遶九▽邂・園縺檎┌縺・**謇句虚遒ｺ隱・*・喃ull_work.wav 繧呈怙蛻昴°繧画怙蠕後∪縺ｧ騾壹＠縺ｧ閨ｴ縺上・
---

## 5. 繝・く繧ｹ繝医メ繧ｧ繝・け

### 笘・Whisper 隱､隱崎ｭ倥・譁・ｭ怜喧縺代′谿九▲縺ｦ縺ｪ縺・production.csv 縺ｮ text_raw 繧偵＊縺｣縺ｨ遒ｺ隱搾ｼ・```python
import csv
for r in csv.DictReader(open('production.csv', encoding='utf-8-sig')):
    txt = r['text_raw']
    if '・滂ｼ・ in txt or '・・ * 3 in txt:
        print(f'笞・・{r["scene_id"]}/{r["line_id"]}: {txt}')
```

### 笘・繧ｻ繝ｪ繝募・螳ｹ縺ｫ隱､隱ｭ繝ｻ隱､螟画鋤縺檎┌縺・- 縲悟ｭ仙ｮｮ縲坂・縲瑚ｦ也せ縲阪・繧医≧縺ｪ Whisper 逕ｱ譚･縺ｮ隱､隱崎ｭ・- 蜷碁浹逡ｰ鄒ｩ隱槭・豺ｷ蜈･

### 笘・諠ｳ螳壹＠縺溘そ繝ｪ繝暮・ｺ上↓縺ｪ縺｣縺ｦ繧・script_with_emoji.txt 繧帝・↓遒ｺ隱搾ｼ・```bash
cat E:/irodori/projects/{name}/script_with_emoji.txt
```

---

## 6. 繧ｷ繝ｼ繝ｳ讒区・繝√ぉ繝・け

### 笘・繧ｷ繝ｼ繝ｳ蛹ｺ蛻・ｊ縺ｮ辟｡髻ｳ・・.0遘抵ｼ峨′蜈･縺｣縺ｦ縺・ｋ
full_work.wav 繧定・縺・※繧ｷ繝ｼ繝ｳ蛻・ｊ譖ｿ繧上ｊ轤ｹ縺ｧ驕募柱諢溘′縺ｪ縺・°縲・
### 笘・繧ｻ繝ｪ繝暮俣縺ｮ辟｡髻ｳ・・.8遘抵ｼ峨′閾ｪ辟ｶ
騾｣邯壹＠縺ｦ閨槭￥縺ｨ譌ｩ縺吶℃繧・驕・☆縺弱ｋ蝣ｴ蜷医・ LINE_SILENCE_SEC 繧定ｪｿ謨ｴ縲・
### 笘・譛ｫ蟆ｾ縺ｮ辟｡髻ｳ縺碁聞縺吶℃縺ｪ縺・**ma_agent.py 縺・`trim_trailing_silence()` 縺ｧ閾ｪ蜍輔き繝・ヨ**縺吶ｋ縺後∝ｿｵ縺ｮ縺溘ａ遒ｺ隱阪・
---

## 7. 螢ｰ雉ｪ荳雋ｫ諤ｧ繝√ぉ繝・け

### 笘・蜷後§繧ｷ繝ｼ繝ｳ蜀・〒螢ｰ雉ｪ縺後ヶ繝ｬ縺ｦ縺ｪ縺・- candidate 繧ｬ繝√Ε縺ｧ蜈ｨ辟ｶ驕輔≧螢ｰ縺梧ｷｷ縺悶ｋ縺薙→縺後≠繧・- 迚ｹ縺ｫ蠑ｷ蠎ｦ縺ｮ鬮倥＞繧ｷ繝ｼ繝ｳ・・FG=7+・峨〒逋ｺ逕溘＠縺後■

### 笘・繧ｷ繝ｼ繝ｳ髢薙〒螢ｰ雉ｪ縺梧･ｵ遶ｯ縺ｫ螟峨ｏ縺｣縺ｦ縺ｪ縺・- caption 縺悟､峨ｏ繧九→螢ｰ雉ｪ繧ょ､峨ｏ繧具ｼ域э蝗ｳ逧・↑繧・OK・・- 諢丞峙縺帙★螟峨ｏ縺｣縺ｦ繧句ｴ蜷医・ caption 縺ｮ謨ｴ蜷域ｧ繧堤｢ｺ隱・
### 笘・LoRA 繧剃ｽｿ縺｣縺溷ｴ蜷茨ｼ嘖cale 縺悟ｮ牙ｮ夂ｯ・峇・・.5縲・.5・・LoRA scale 縺・2.0 雜・〒逋ｺ謨｣縺吶ｋ繝ｪ繧ｹ繧ｯ縺ゅｊ縲・
---

## 8. 繝輔ぃ繧､繝ｫ蠖｢蠑上メ繧ｧ繝・け

### 笘・繧ｵ繝ｳ繝励Ν繝ｬ繝ｼ繝・48kHz
```python
import soundfile as sf
info = sf.info('E:/irodori/projects/{name}/master/full_work.wav')
assert info.samplerate == 48000, f'sr={info.samplerate}'
```

### 笘・繝薙ャ繝域ｷｱ蠎ｦ 16bit / 24bit / float・育畑騾斐↓繧医ｋ・・邏榊刀蜈医・隕∽ｻｶ縺ｫ蜷医ｏ縺帙ｋ縲・
### 笘・MP3 縺ｮ蝣ｴ蜷茨ｼ夐←蛻・↑繝薙ャ繝医Ξ繝ｼ繝・- 驟榊ｸ・畑・啖BR qscale 2・遺薗190kbps縲［a_agent.py 縺ｮ繝・ヵ繧ｩ・・- 鬮倬浹雉ｪ・・20kbps CBR

---

## 9. 繝｡繧ｿ繝・・繧ｿ繝ｻ闡嶺ｽ懈ｨｩ

### 笘・繝輔ぃ繧､繝ｫ蜷阪↓譌･譛ｬ隱・迚ｹ谿願ｨ伜捷縺檎┌縺・驟榊ｸ・凾縺ｮ莠呈鋤諤ｧ縺ｮ縺溘ａ縲、SCII 縺ｮ縺ｿ謗ｨ螂ｨ・・```
笨・scene_01.wav  scene_02.wav  full_work.wav
笶・繧ｷ繝ｼ繝ｳ竭.wav  譛ｬ邱ｨ.wav
```

### 笘・蟄ｦ鄙堤ｴ譚舌・讓ｩ蛻ｩ遒ｺ隱・- LoRA 蟄ｦ鄙偵↓菴ｿ縺｣縺溽ｴ譚撰ｼ夊・蛻・・螢ｰ / 蝠・畑OK邏譚・/ 驟榊ｸグK邏譚舌・縺ｿ
- 繧ｼ繝ｭ繧ｷ繝ｧ繝・ヨ蜿ら・髻ｳ螢ｰ・壼酔荳・
### 笘・Irodori-TTS 縺ｮ繝ｩ繧､繧ｻ繝ｳ繧ｹ驕ｵ螳・- 繧ｳ繝ｼ繝峨・ MIT
- **繝｢繝・Ν驥阪∩縺ｯ蝠・畑蛻ｩ逕ｨ遖∵ｭ｢**・・ratako/Irodori-TTS-500M-v2 縺ｮ繝ｩ繧､繧ｻ繝ｳ繧ｹ蜿ら・・・
---

## 10. 繝舌ャ繧ｯ繧｢繝・・

### 笘・螳梧・迚医・ WAV 繧貞挨蝣ｴ謇縺ｫ繧ｳ繝斐・
```bash
cp E:/irodori/projects/{name}/master/full_work.wav D:/backup/{name}_v1_final.wav
```

### 笘・production.csv 繧ゆｿ晏ｭ・蜀咲樟諤ｧ遒ｺ菫昴・縺溘ａ縲∫函謌先凾縺ｮ CSV 繧呈ｮ九☆縲・
### 笘・project_brief.json 縺ｨ grok_prompt.md 繧ゆｿ晏ｭ・蟆・擂縺ｮ邯夂ｷｨ / 繝ｪ繝・う繧ｯ逕ｨ縲・
---

## 11. 譛邨ゅΜ繧ｹ繝九Φ繧ｰ

### 笘・繝倥ャ繝峨・繝ｳ縺ｧ騾壹＠縺ｧ閨ｴ縺・- 繧ｹ繝斐・繧ｫ繝ｼ縺ｧ縺ｯ隕矩・☆繝弱う繧ｺ縺悟・縺九ｋ
- 蟾ｦ蜿ｳ繝舌Λ繝ｳ繧ｹ・医Δ繝弱Λ繝ｫ縺ｪ繧蛾未菫ゅ↑縺暦ｼ・
### 笘・蛻･遶ｯ譛ｫ縺ｧ繧り・縺・- 繧ｹ繝槭・繝ｻ蛻･ PC 縺ｧ蜀咲函遒ｺ隱・- 迺ｰ蠅・ｷｮ縺ｧ驕募柱諢溘′蜃ｺ縺ｪ縺・°

### 笘・隨ｬ荳芽・・閠ｳ縺ｧ繝√ぉ繝・け・亥庄閭ｽ縺ｪ繧会ｼ・閾ｪ蛻・・閨ｴ縺肴・繧後※豌励▼縺九↑縺上↑繧狗樟雎｡縺ゅｊ縲・
---

## 12. NG縺後≠縺｣縺溷ｴ蜷医・蟇ｾ蜃ｦ譌ｩ隕玖｡ｨ

| NG鬆・岼 | 蟇ｾ蜃ｦ |
|-------|------|
| 陦梧焚荳崎ｶｳ | production.csv 縺ｮ status 縺ｨ approved_candidate 繧堤｢ｺ隱阪∽ｸ崎ｶｳ蛻・ｒ霑ｽ蜉蜿朱鹸 |
| 繝弱う繧ｺ繝ｻ縺九☆繧・| 蛻･ candidate 縺ｫ蛻・ｊ譖ｿ縺・or 繝ｪ繝・う繧ｯ |
| Whisper隱､隱崎ｭ・| text_raw 繧剃ｿｮ豁｣ 竊・蜀咲函謌・|
| 螢ｰ雉ｪ繝悶Ξ | caption / CFG / guidance_mode 繧貞・隱ｿ謨ｴ |
| 辟｡髻ｳ髟ｷ縺吶℃ | ma_agent.py 縺ｮ LINE_SILENCE_SEC / SCENE_SILENCE_SEC 繧定ｪｿ謨ｴ |
| 繧ｵ繝ｳ繝励Ν繝ｬ繝ｼ繝磯＆縺・| infer.py 縺ｮ codec-repo 縺梧ｭ｣縺励＞縺狗｢ｺ隱・|

---

## 13. 繝√ぉ繝・け螳御ｺ・ユ繝ｳ繝励Ξ繝ｼ繝・
縺吶∋縺ｦ 笨・縺ｫ縺ｪ縺｣縺溘ｉ縲∽ｻ･荳九ｒ險倬鹸・・
```
=== 邏榊刀繝√ぉ繝・け螳御ｺ・===
繝励Ο繧ｸ繧ｧ繧ｯ繝亥錐: {project_name}
邏榊刀譌･: {YYYY-MM-DD}
螳梧・迚・ {file_name}.wav
邱乗凾髢・ {蛻・
陦梧焚: {N}
繝√ぉ繝・け螳滓命閠・ {繝繝ｼ繝ｪ繝ｳ}
笨・蜈ｨ鬆・岼繧ｯ繝ｪ繧｢
```

---

**譛邨よ峩譁ｰ: 2026-04-25**
