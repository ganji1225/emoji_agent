# Irodori-TTS 導入・操作マニュアル

**このみお姉さんのTTSディレクターズガイド**

---

## 目次

1. [概要](#概要)
2. [環境構成](#環境構成)
3. [基本の使い方 - v2（リファレンス音声モード）](#基本の使い方---v2リファレンス音声モード)
4. [基本の使い方 - VoiceDesign（テキストで声をデザイン）](#基本の使い方---voicedesignテキストで声をデザイン)
5. [Gradio Web UI で使う](#gradio-web-ui-で使う)
6. [絵文字スタイルコントロール一覧](#絵文字スタイルコントロール一覧)
7. [パラメータチューニングガイド](#パラメータチューニングガイド)
8. [よりよい音声を作るためのコツ](#よりよい音声を作るためのコツ)
9. [トラブルシューティング](#トラブルシューティング)

---

## 概要

**Irodori-TTS** は日本語テキストから高品質な音声を合成するTTSモデルよ。

### 2つのモデルの違い

| 項目 | v2（リファレンスモード） | VoiceDesign（キャプションモード） |
|------|--------------------------|----------------------------------|
| フォルダ | `irodori-tts-v2` | `irodori-tts-voicedesign` |
| HFモデル | `Aratako/Irodori-TTS-500M-v2` | `Aratako/Irodori-TTS-500M-v2-VoiceDesign` |
| 声の指定方法 | 参照音声ファイル（WAV）を渡す | テキストで声の特徴を記述する |
| 用途 | 特定の声を再現したい場合 | リファレンス音声なしで多様な声を作りたい場合 |
| 対応言語 | 日本語のみ | 日本語のみ |
| 音質 | 48kHz | 48kHz |

---

## 環境構成

```
D:\irodori\
  irodori-tts-v2\           ← リファレンス音声モード
    .venv\                  ← Python 3.10 仮想環境
    infer.py                ← CLI推論スクリプト
    gradio_app.py           ← Web UI
    outputs\                ← 生成音声の出力先
  irodori-tts-voicedesign\  ← VoiceDesignモード
    .venv\                  ← Python 3.10 仮想環境
    infer.py                ← CLI推論スクリプト
    gradio_app_voicedesign.py ← Web UI
    outputs\                ← 生成音声の出力先
```

### venv の有効化（コマンドプロンプト）

```cmd
:: v2（リファレンスモード）
D:\irodori\irodori-tts-v2\.venv\Scripts\activate.bat

:: VoiceDesign
D:\irodori\irodori-tts-voicedesign\.venv\Scripts\activate.bat
```

### venv の有効化（PowerShell）

```powershell
# v2（リファレンスモード）
D:\irodori\irodori-tts-v2\.venv\Scripts\Activate.ps1

# VoiceDesign
D:\irodori\irodori-tts-voicedesign\.venv\Scripts\Activate.ps1
```

### venv の有効化（Git Bash / bash）

```bash
# v2（リファレンスモード）
source D:/irodori/irodori-tts-v2/.venv/Scripts/activate

# VoiceDesign
source D:/irodori/irodori-tts-voicedesign/.venv/Scripts/activate
```

---

## 基本の使い方 - v2（リファレンス音声モード）

### リファレンス音声あり（ゼロショットボイスクローニング）

参照音声の声色を真似て音声を生成するわ。

```bash
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2 \
  --text "今日はいい天気ですね。お散歩に行きましょう。" \
  --ref-wav path/to/reference.wav \
  --output-wav outputs/sample.wav
```

### リファレンスなし

```bash
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2 \
  --text "今日はいい天気ですね。" \
  --no-ref \
  --output-wav outputs/sample_noref.wav
```

### 絵文字でスタイルを制御

```bash
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2 \
  --text "😊今日はとっても楽しい一日でした！🤭えへへっ" \
  --no-ref \
  --output-wav outputs/happy_sample.wav
```

### 複数候補を一度に生成

```bash
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2 \
  --text "おはようございます。" \
  --no-ref \
  --num-candidates 5 \
  --output-wav outputs/candidate.wav
```

→ `candidate_001.wav` ～ `candidate_005.wav` が生成される

---

## 基本の使い方 - VoiceDesign（テキストで声をデザイン）

リファレンス音声がなくても、テキストで声の特徴を指定できるのがVoiceDesignの強みよ！

### 基本的な使い方

```bash
cd D:/irodori/irodori-tts-voicedesign
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
  --text "今日はいい天気ですね。" \
  --caption "落ち着いた女性の声で、近い距離感でやわらかく自然に読み上げてください。" \
  --no-ref \
  --output-wav outputs/gentle_female.wav
```

### キャプション例（いろいろな声）

```bash
# 元気な少女
--caption "明るくハキハキした少女の声で、楽しそうに話してください。"

# 渋い男性
--caption "低い声の中年男性が、落ち着いた口調でゆっくりと話している。"

# ささやき声
--caption "若い女性が、耳元で囁くように小さな声で話している。"

# 怒った声
--caption "男性が苛立ちを隠せない様子で、強い口調で話している。"

# ナレーション調
--caption "プロのナレーターが、はっきりとした発音で聞き取りやすく読み上げている。"
```

### 絵文字との組み合わせ

```bash
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
  --text "😰え、えっと…🥺ごめんなさい…😭" \
  --caption "若い女性が、自信なさげに震える声で話している。" \
  --no-ref \
  --output-wav outputs/nervous_girl.wav
```

---

## Gradio Web UI で使う

WebブラウザベースのUIで簡単に操作できるわよ♪

### v2（リファレンスモード）

```bash
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe gradio_app.py --server-name 0.0.0.0 --server-port 7860
```

→ ブラウザで `http://localhost:7860` を開く

### VoiceDesign

```bash
cd D:/irodori/irodori-tts-voicedesign
.venv/Scripts/python.exe gradio_app_voicedesign.py --server-name 0.0.0.0 --server-port 7861
```

→ ブラウザで `http://localhost:7861` を開く

---

## 絵文字スタイルコントロール一覧

テキスト中に絵文字を挿入すると、発話スタイルや効果音を制御できるの。
**繰り返し入力するほど効果が強くなる**わよ！

### 効果音・呼吸系

| 絵文字 | 効果 | 使い方のコツ |
|--------|------|-------------|
| 👂 | 囁き、耳元の音 | ASMRっぽい音声に |
| 😮‍💨 | 吐息、溜息、寝息 | セリフの前後に入れると自然 |
| 🌬️ | 息切れ、荒い息遣い | 運動後や緊張シーンに |
| 😮 | 息をのむ | 驚きの直前に |
| 👅 | 舐める音、咀嚼音、水音 | ASMR向け |
| 💋 | リップノイズ | 唇の音 |
| 🥤 | 唾を飲み込む音 | 緊張シーンに |
| 🤧 | 咳き込み、くしゃみ、鼻をすする | 風邪キャラに |
| 😒 | 舌打ち | 不満表現に |
| 👌 | 相槌、頷く音 | 会話の合間に |
| 🥱 | あくび | 眠そうなシーンに |
| 🎵 | 鼻歌 | 楽しいシーンの雰囲気作りに |

### 感情・話し方系

| 絵文字 | 効果 | 使い方のコツ |
|--------|------|-------------|
| 🤭 | くすくす笑い | セリフの合間に入れると自然な笑い |
| 😏 | からかうように、甘えるように | イタズラっぽい口調に |
| 🥺 | 声を震わせて、自信なさげ | おねだりや泣きそうな声に |
| 🫶 | 優しく | 温かいセリフに |
| 😭 | 嗚咽、泣き声 | 悲しいシーンに |
| 😱 | 悲鳴、叫び | ホラーや驚愕シーンに |
| 😪 | 眠そうに、気だるげに | 寝起きキャラに |
| 😰 | 慌てて、動揺、どもり | パニックシーンに |
| 😆 | 喜びながら | 楽しいセリフに |
| 😠 | 怒り、不満げ、拗ねながら | ツンデレシーンに最適 |
| 😲 | 驚き、感嘆 | 「えっ!?」の直前に |
| 😖 | 苦しげに | 痛みや苦悩の表現に |
| 😟 | 心配そうに | 不安なセリフに |
| 🫣 | 恥ずかしそうに、照れながら | 告白シーンなどに |
| 🙄 | 呆れたように | ツッコミに |
| 😊 | 楽しげに、嬉しそうに | 明るいセリフ全般に |
| 🙏 | 懇願するように | 「お願い！」に |
| 🥴 | 酔っ払って | 酔いどれキャラに |
| 🤐 | 口を塞がれて | くぐもった声に |
| 😌 | 安堵、満足げ | ほっとしたシーンに |
| 🤔 | 疑問の声 | 考え中のシーンに |
| 🥵 | 喘ぎ、うめき声 | 疲労や極限状態に |

### スピード・エフェクト系

| 絵文字 | 効果 | 使い方のコツ |
|--------|------|-------------|
| ⏸️ | 間、沈黙 | セリフの途中に「間」を入れたい時 |
| ⏩ | 早口、まくしたてる | 焦ってるセリフに |
| 🐢 | ゆっくりと | 落ち着いたナレーションに |
| 📢 | エコー、リバーブ | 広い空間の雰囲気に |
| 📞 | 電話越しの音 | 通話シーンに |

---

## パラメータチューニングガイド

### よく使うパラメータ

| パラメータ | デフォルト | 説明 | おすすめ範囲 |
|-----------|-----------|------|-------------|
| `--num-steps` | 40 | サンプリングステップ数 | 20-60（多いほど高品質だが遅い） |
| `--cfg-scale-text` | 3.0 | テキストガイダンス強度 | 1.0-5.0 |
| `--cfg-scale-caption` | 3.0 | キャプションガイダンス強度（VoiceDesign） | 1.0-5.0 |
| `--cfg-scale-speaker` | 5.0 | スピーカーガイダンス強度 | 3.0-8.0 |
| `--seed` | ランダム | シード値（再現性） | 固定値で結果固定 |
| `--model-precision` | fp32 | モデル精度 | bf16で高速化 |

### パフォーマンス最適化

RTX 4090（24GB VRAM）での推奨設定：

```bash
# 高速モード（品質をわずかに犠牲にして速度UP）
--model-precision bf16 --num-steps 25

# 高品質モード（じっくり生成）
--model-precision fp32 --num-steps 60

# 複数候補から選びたい場合
--num-candidates 5 --model-precision bf16 --decode-mode batch
```

### リファレンス音声のコツ（v2）

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `--max-ref-seconds` | 30.0 | リファレンス音声の最大秒数 |
| `--ref-normalize-db` | -16.0 | 音量正規化（dB） |

---

## よりよい音声を作るためのコツ

### テキスト入力のポイント

1. **難しい漢字はひらがな・カタカナに変換する**
   - 悪い例：「紫陽花が咲いた」→ 読み間違える可能性あり
   - 良い例：「あじさいが咲いた」

2. **句読点を適切に入れる**
   - 自然な間（ま）が生まれて聞きやすくなる

3. **⏸️ で明示的に間を作る**
   - 「それは⏸️とても大切なことです」

4. **長いテキストは分割する**
   - 1文ずつ生成して後で結合する方が品質が安定しやすい

### キャプション（VoiceDesign）のポイント

1. **具体的に書く**
   - 悪い例：「いい声で」
   - 良い例：「20代の女性が、少し低めの落ち着いた声で、マイクに近い距離感で話している」

2. **矛盾する指示を避ける**
   - 悪い例：「元気で暗い声」→ 結果が不安定に

3. **距離感を指定すると効果的**
   - 「耳元で」「遠くから」「マイクに近い距離で」

4. **感情+声質+話し方のセットで指定する**
   - 例：「若い女性の高い声で、恥ずかしそうにもじもじしながら、小さな声で話している」

### 絵文字の使い方のポイント

1. **セリフの該当箇所の直前に置く**
   - 「😊ありがとう！」→ 笑顔混じりの「ありがとう」

2. **繰り返すと効果が強まる**
   - 「😭😭😭もうダメ…」→ より激しい泣き声

3. **組み合わせも可能**
   - 「🥺😰えっと…その…」→ 不安げでどもる

4. **効果は完璧ではない**
   - 文脈によって効果が弱い場合がある。何パターンか生成して選ぶのがおすすめ

### 音声選びのコツ

- `--num-candidates 5` で複数候補を生成し、一番良いものを選ぶ
- `--seed` を固定して他のパラメータを微調整すると比較しやすい
- CFGスケールを上げすぎると不自然になるので注意

---

## トラブルシューティング

### 「CUDA out of memory」エラーが出る

```bash
# bf16精度に切り替える
--model-precision bf16 --codec-precision bf16

# 候補数を減らす
--num-candidates 1

# デコードモードを変更
--decode-mode sequential
```

### 漢字の読み間違い

難しい漢字はひらがな/カタカナに置き換えてね。モデルの漢字読み精度はやや弱め。

### 音声の末尾にノイズが入る

末尾トリミングはデフォルトで有効（`--trim-tail`）。閾値を調整する場合：

```bash
--tail-std-threshold 0.03 --tail-mean-threshold 0.08
```

### 初回実行が遅い

初回はHugging Faceからモデルをダウンロードするため時間がかかるわ。
2回目以降はキャッシュされるから速くなるわよ♪

### venvの再構築が必要な場合

```bash
# 古いvenvを削除して作り直す
rm -rf .venv
C:/Users/ganji/AppData/Local/Programs/Python/Python310/python.exe -m venv .venv
.venv/Scripts/pip.exe install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
.venv/Scripts/pip.exe install "dacvae @ git+https://github.com/facebookresearch/dacvae" \
  "datasets>=3.0.0" "gradio>=5.0.0" "huggingface-hub>=0.34.0,<1.0" \
  "llvmlite>=0.40.0" "numba>=0.57.0" "peft>=0.18.0" "pyyaml>=6.0" \
  "safetensors>=0.7.0" "soundfile>=0.12.0" "sentencepiece>=0.1.99,<0.2" \
  "torchcodec>=0.10.0" "transformers<5" "tqdm>=4.67.3" "wandb>=0.17.0"
```

---

## クイックリファレンス

### 最短コマンド（コピペ用）

```bash
# === v2: リファレンス音声あり ===
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe infer.py --hf-checkpoint Aratako/Irodori-TTS-500M-v2 --text "こんにちは" --ref-wav ref.wav --output-wav outputs/out.wav

# === v2: リファレンスなし ===
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe infer.py --hf-checkpoint Aratako/Irodori-TTS-500M-v2 --text "こんにちは" --no-ref --output-wav outputs/out.wav

# === VoiceDesign ===
cd D:/irodori/irodori-tts-voicedesign
.venv/Scripts/python.exe infer.py --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign --text "こんにちは" --caption "優しい女性の声で話してください。" --no-ref --output-wav outputs/out.wav

# === Web UI (v2) ===
cd D:/irodori/irodori-tts-v2
.venv/Scripts/python.exe gradio_app.py --server-port 7860

# === Web UI (VoiceDesign) ===
cd D:/irodori/irodori-tts-voicedesign
.venv/Scripts/python.exe gradio_app_voicedesign.py --server-port 7861
```
