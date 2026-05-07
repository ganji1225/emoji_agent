# LoRA 学習ガイド（Irodori-TTS / Emoji-TTS）

参照音声から「固定の声」を作るための LoRA ファインチューニング手順。
2026-04-25 に voice_ganyu_v1 を作成した時の知見ベース。

---

## 0. 概要

### LoRA で何ができるか
- 数十本の参照音声から **キャラ固有の声** を学習
- ベースモデル（Aratako/Irodori-TTS-500M-v2-VoiceDesign）に **6.4MB の小さな差分アダプタ** を作る
- 推論時に `--lora-path` で読み込むだけで適用可能
- `--lora-scale 0.0〜2.0` でベース声寄り or LoRA寄りに調整できる

### ゼロショット参照音声 vs LoRA

| 観点 | ゼロショット（--ref-wav） | LoRA |
|------|------------------------|------|
| 必要素材 | 参照音声1本 | 学習用音声 50本前後 |
| 学習時間 | 不要 | 30〜60分 |
| 一貫性 | △ ガチャ要素強い | ◎ ほぼ固定 |
| ストレージ | 0 | ~6MB（アダプタのみ） |

「同じ声で量産したい」なら **LoRA一択**。

---

## 1. 前提環境

### ハードウェア
- **VRAM 16GB 以上推奨**（RTX 4060 Ti / 5060 Ti クラス）
- **batch_size=2 + gradient_accumulation=4** が安全圏（実効バッチ=8）

### 必須ライブラリ
```bash
# Emoji-TTS の venv に必要
pip install peft faster-whisper librosa soundfile torch
```

### モデルチェックポイント
- ベース: `D:/irodori/emoji/checkpoints/Aratako_Irodori-TTS-500M-v2-VoiceDesign/model.safetensors`
- コーデック: `Aratako/Semantic-DACVAE-Japanese-32dim`（HuggingFace から自動DL）

### `lora_train.py` の修正済みバージョンが必要
2026-04-25 時点でフォーク版に **VoiceDesign 対応バグが7件** あり、`D:/irodori/emoji/lora_train.py` を修正済み。詳細は §6 トラブルシューティング を参照。

---

## 2. パイプライン全体図

```
[音声素材].wav
    ↓ ① スライス（librosa独自）
[2〜12秒のセグメント].wav × N本
    ↓ ② Whisper キャプション
metadata.csv（file_name, text, caption）
    ↓ ③ DACVAE 潜在変換
manifest.jsonl + latents/*.pt
    ↓ ④ LoRA 学習
lora_checkpoint_final_ema/
    ↓ ⑤ 推論で読み込み
完成音声.wav
```

---

## 3. データ準備

### Step 1: 音声素材の置き場所
```
D:/irodori/emoji/input/{voice_name}/*.wav
```

**素材の目安：**
| 観点 | 推奨 |
|------|------|
| 合計時間 | 5〜30分 |
| 1ファイル長 | 何分でも可（後でスライス） |
| サンプルレート | 48kHz推奨（自動でリサンプル） |
| バリエーション | 平静・喜怒哀楽が混ざってると◎ |

### Step 2: 作業ディレクトリ作成
```bash
mkdir -p D:/irodori/emoji/data/{voice_name}/slices
mkdir -p D:/irodori/emoji/data/{voice_name}/latents
```

### Step 3: スライス（librosa 独自スクリプト）

**注意：** Emoji-TTS の `dataset_tools.py slice` は torchcodec を使うが、**FFmpeg 8.0 環境では動作しない**。代替として以下を実行：

```python
# librosa_slicer.py（インラインで実行可）
import os, glob
import numpy as np, soundfile as sf, librosa

INPUT_DIR = 'D:/irodori/emoji/input/{voice_name}'
OUTPUT_DIR = 'D:/irodori/emoji/data/{voice_name}/slices'
MIN_SEC = 2.0
MAX_SEC = 12.0
TOP_DB = 35  # 無音判定（dB）

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

    # 12秒超: 無音区間で分割
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

print(f'スライス出力: {total_out}本')
```

### Step 4: Whisper でキャプション生成

```bash
cd D:/irodori/emoji && .venv/Scripts/python.exe dataset_tools.py caption \
  --input data/{voice_name}/slices \
  --output-manifest data/{voice_name}/manifest_raw.csv \
  --format csv \
  --model large-v3 \
  --language ja \
  --voice-design \
  --voice-design-caption "{キャラの声を表現するキャプション文}" \
  --device cuda
```

**voice-design-caption の例：**
- 落ち着いた女性: `"穏やかで優しい若い女性が、落ち着いた静かな声で丁寧に話している。"`
- 元気な少女: `"明るく元気な少女が、はきはきとよく通る声で話している。"`
- クールな大人: `"クールで知的な女性が、低めの落ち着いた声で淡々と話している。"`

### Step 5: audiofolder 形式に整形

```bash
cp data/{voice_name}/manifest_raw.csv data/{voice_name}/slices/metadata.csv
```

### Step 6: DACVAE 潜在変換（torchcodec バイパス版）

`D:/irodori/emoji/custom_prepare_manifest.py` を使う（このスクリプトは2026-04-25に作成、torchcodec/HF datasets を経由しない簡易版）。

```bash
cd D:/irodori/emoji && .venv/Scripts/python.exe custom_prepare_manifest.py \
  --csv data/{voice_name}/manifest_raw.csv \
  --audio-dir data/{voice_name}/slices \
  --output-manifest data/{voice_name}/manifest.jsonl \
  --latent-dir data/{voice_name}/latents \
  --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
  --device cuda
```

### Step 7: manifest.jsonl のパス確認

`latent_path` が **manifest.jsonl と同じディレクトリからの相対パス** になっているか確認。`data/{voice_name}/latents/...` のような階層が含まれている場合は、`latents/{filename}.pt` だけに修正する。

---

## 4. LoRA 学習

### コマンド（推奨パラメータ）

```bash
cd D:/irodori/emoji && .venv/Scripts/python.exe lora_train.py \
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

### ⚠️ 重要な注意点

| 項目 | 設定 | 理由 |
|------|------|------|
| `--grad-checkpoint` | **使わない** | VoiceDesignモデルの caption 引数と非互換 |
| `--batch-size` | **2** | grad_checkpoint なしだと VRAM 余裕が必要 |
| `--gradient-accumulation-steps` | **4** | 実効バッチを 8 に保つ |
| `--max-steps` | **3000** | 50件前後のデータで適切。多すぎると過学習 |

### 学習中の指標
- 初期 loss: 0.85〜0.95
- 終盤 loss: 0.45〜0.55 程度まで下がれば学習成功
- 速度: RTX 5060 Ti で 1.7 steps/sec、3000 step = 約30分

### 出力ファイル
```
lora/voice_{voice_name}_v1/
  ├─ lora_checkpoint_0000500_ema/
  ├─ lora_checkpoint_0001000_ema/
  ├─ lora_checkpoint_0001500_ema/
  ├─ lora_checkpoint_0002000_ema/
  ├─ lora_checkpoint_0002500_ema/
  ├─ lora_checkpoint_0003000_ema/
  └─ lora_checkpoint_final_ema/   ← これを使う
```

---

## 5. 推論で使う

### 単発生成

```bash
cd D:/irodori/emoji && .venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
  --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
  --text "セリフテキスト" \
  --caption "声のキャラ説明文" \
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

### `--lora-scale` の調整目安

| スケール | 効果 |
|---------|------|
| 0.0 | LoRA 無効化（ベース声のみ） |
| 0.5 | ベース寄り、LoRA はうっすら |
| 1.0 | 標準。学習通りの声 |
| 1.5 | LoRA 強調。声質固定が強い |
| 2.0 以上 | ノイズ・崩壊リスク高い |

---

## 6. トラブルシューティング（2026-04-25 で発生した実績）

### バグ① `max_caption_len` got an unexpected keyword
**症状:** `TypeError: ModelConfig.__init__() got an unexpected keyword argument 'max_caption_len'`
**原因:** VoiceDesign の safetensors metadata に `max_caption_len` (TrainConfig フィールド) が混入
**修正:** `lora_train.py` `_load_base_model()` の `_INF_KEYS` に `max_caption_len` を追加し、`fields(ModelConfig)` でフィルタ

### バグ② `latent_patch_size` 引数が無い
**症状:** `TypeError: LatentTextDataset.__init__() got an unexpected keyword argument 'latent_patch_size'`
**原因:** dataset.py のAPI変更（`latent_patch_size` 引数が削除）
**修正:** `lora_train.py` の `LatentTextDataset(...)` 3箇所から `latent_patch_size=...` を削除

### バグ③ caption_tokenizer が必須
**症状:** `TypeError: TTSCollator.__init__() missing 1 required positional argument: 'caption_tokenizer'`
**修正:** VoiceDesign 用に `PretrainedTextTokenizer.from_pretrained()` で caption tokenizer を構築して渡す

### バグ④ caption_input_ids が渡ってない
**症状:** `ValueError: caption_input_ids and caption_mask are required when caption conditioning is enabled.`
**修正:** 学習ループで `batch["caption_ids"]` / `batch["caption_mask"]` を取り出して `model()` に渡す

### バグ⑤ gradient_checkpoint で caption 非対応
**症状:** `TypeError: ... checkpointed() got an unexpected keyword argument 'caption_state'`
**回避策:** `--grad-checkpoint` を**使わない**。代わりに `batch_size=2 / gradient-accumulation=4` で対応

### バグ⑥ torchcodec が FFmpeg 8 と非互換
**症状:** `OSError: Could not load this library: ... libtorchcodec_core8.dll`
**回避策:** `dataset_tools.py slice` は使わず **librosa 独自スライサー** を使う、`prepare_manifest.py` も使わず **`custom_prepare_manifest.py`** を使う

### バグ⑦ manifest の latent_path が二重結合
**症状:** `FileNotFoundError: ...\data\ganyu_v1\data\ganyu_v1\latents\xxx.pt`
**原因:** prepare_manifest 実行時に相対パスで指定するとパスが二重結合される
**修正:** manifest.jsonl の `latent_path` を `latents/{filename}.pt` だけの相対パスに書き換える

---

## 7. ファイル整理

### 中間チェックポイントの削除
学習完了後、`lora_checkpoint_final_ema` 以外は通常不要：

```bash
rm -rf D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0000500_ema \
       D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0001000_ema \
       D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0001500_ema \
       D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0002000_ema \
       D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0002500_ema \
       D:/irodori/emoji/lora/voice_{voice_name}_v1/lora_checkpoint_0003000_ema
```

**残す理由がある場合：**
- 過学習が疑わしい → 中盤（1500step）と比較したい
- A/B テストしたい → 各ステップを並べて聴き比べ

### スライス・潜在ファイル
学習が完了して LoRA が問題なく動いていれば、スライスと潜在も削除可（再学習する時はまた作り直し）：

```bash
# 容量逼迫してから消すで十分
rm -rf D:/irodori/emoji/data/{voice_name}/
```

---

## 8. パイプラインへの組み込み（実装済み 2026-04-25）

production.csv に `lora_path` / `lora_scale` 列が追加されており、recorder.py が自動的に読み取って infer.py に渡す。**Claude エージェント経由 / CLI 直接実行どちらでも適用される**。

### 使い方 A: set_lora.py で一括設定（推奨）

```bash
# 全行に適用
python D:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 特定シーンだけ
python D:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scenes scene_01,scene_02

# 特定 status の行だけ
python D:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --status pending

# 解除
python D:/irodori/agents/set_lora.py {project_name} --clear

# 現在の設定確認
python D:/irodori/agents/set_lora.py {project_name} --show
```

LoRA 名の解決：
1. 絶対パス指定 → そのまま
2. 名前のみ指定 → `D:/irodori/emoji/lora/{name}/lora_checkpoint_final_ema` を自動探索

### 使い方 B: default_captions.json プロファイルで紐付け

```json
"日常会話_甘雨": {
  "caption": "穏やかで優しい若い女性が、落ち着いた静かな声で丁寧に話している。",
  "cfg_text": 3.0,
  "cfg_caption": 3.0,
  "cfg_speaker": 5.0,
  "cfg_guidance_mode": "joint",
  "num_steps": 40,
  "lora_path": "D:/irodori/emoji/lora/voice_ganyu_v1/lora_checkpoint_final_ema",
  "lora_scale": 1.0
}
```

→ casting apply / grok_bridge process 時に自動で production.csv に書き込まれる。

### 起動経路に関わらず適用される

- ✅ Claude エージェント（recorder）経由
- ✅ CLI 直接（`python recorder.py {project_name}`）

判断は production.csv の `lora_path` 列1箇所に集約されているため、起動経路を問わず同じ動作になる。

---

## 9. 参考資料

- [Emoji-TTS README_ja.md](D:/irodori/emoji/README_ja.md)
- [HuggingFace - Aratako/Irodori-TTS-500M-v2-VoiceDesign](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- [PEFT (Parameter-Efficient Fine-Tuning)](https://github.com/huggingface/peft)

---

**最終更新: 2026-04-25 / 初版作成: voice_ganyu_v1 制作時**
