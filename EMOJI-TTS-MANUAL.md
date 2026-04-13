# Emoji-TTS (Irodori-TTS フォーク版) 導入・操作マニュアル

**このみお姉さんのTTSディレクターズガイド - プロダクション版**

---

## 目次

1. [概要 - 本家との違い](#概要---本家との違い)
2. [環境構成](#環境構成)
3. [Web UI の使い方（7つのタブ）](#web-ui-の使い方7つのタブ)
4. [CLI での使い方](#cli-での使い方)
5. [感情プリセットの活用](#感情プリセットの活用)
6. [データセット作成ワークフロー](#データセット作成ワークフロー)
7. [LoRA ファインチューニング](#lora-ファインチューニング)
8. [フルファインチューニング](#フルファインチューニング)
9. [モデルマージ](#モデルマージ)
10. [絵文字スタイルコントロール一覧](#絵文字スタイルコントロール一覧)
11. [よりよい音声を作るためのコツ](#よりよい音声を作るためのコツ)
12. [トラブルシューティング](#トラブルシューティング)

---

## 概要 - 本家との違い

このEmoji-TTSは [iron-mukakin](https://github.com/iron-mukakin/Emoji-TTS) によるフォーク版で、本家Irodori-TTSに大幅な機能追加がされてるわ。

### 本家 vs フォーク版 比較

| 機能 | 本家 Irodori-TTS | Emoji-TTS フォーク版 |
|------|-----------------|---------------------|
| 推論（CLI/Gradio） | あり | あり |
| 感情プリセット | なし | **5種（普通/力強い/静か/明るい/ヒソヒソ）** |
| 複数候補同時生成 | あり | あり（**最大8候補**） |
| LoRAファインチューニング | 設定ファイル手動 | **GUI対応・Resume/EMA/Early Stopping** |
| フルファインチューニング | あり | あり（**GUI対応**） |
| データセットツール | なし | **音声スライス・Whisper文字起こし・LLM絵文字アノテーション** |
| モデルマージ | なし | **Weighted Average/SLERP/Task Arithmetic/部分マージ/LoRA注入** |
| チェックポイント変換 | あり | あり（**GUI対応**） |
| デフォルトモデル | v2 (500M) | **v1 (500M)** ※v2も使用可能 |
| ライセンス（重量） | MIT | **非商用のみ** |

### 重要な注意点

- **モデル重みは非商用ライセンス**よ。商用利用には注意してね
- デフォルトは `Aratako/Irodori-TTS-500M`（v1）を使うわ
- v2モデル (`Aratako/Irodori-TTS-500M-v2`) もHFリポIDを指定すれば使えるわよ

---

## 環境構成

```
D:\irodori\
  emoji\                      ← Emoji-TTS フォーク版
    .venv\                    ← Python 3.10 仮想環境
    gradio_app.py             ← All-in-One Web UI（7タブ）
    infer.py                  ← CLI推論
    train.py                  ← フルファインチューニング
    lora_train.py             ← LoRAトレーニング
    dataset_tools.py          ← データセットツール
    merge.py                  ← モデルマージ
    prepare_manifest.py       ← マニフェスト作成
    start_webui.bat           ← ワンクリック起動
    configs/                  ← トレーニング設定
    checkpoints/              ← モデル保存先
    lora/                     ← LoRAアダプター
    data/                     ← マニフェスト・ラテント
    outputs/                  ← 生成音声
    gradio_outputs/           ← Gradio出力
    logs/                     ← 学習ログ
```

### 起動方法

`start_webui.bat` をダブルクリック → http://localhost:7863

---

## Web UI の使い方（7つのタブ）

### タブ1: 推論（Inference）

メインの音声生成タブよ。

**基本操作：**
1. モデルをロード（初回は自動ダウンロード）
2. テキストを入力
3. （任意）リファレンス音声をアップロード
4. 感情プリセットを選択 or スライダーで調整
5. 生成ボタンを押す

**感情プリセット：**
| プリセット | 効果 | 適したシーン |
|-----------|------|-------------|
| Normal | 標準的な読み上げ | ナレーション全般 |
| Powerful | 力強く、はっきりと | 叫び、怒り、決意 |
| Quiet | 静かで落ち着いた | ささやき、内緒話 |
| Bright | 明るく元気に | 楽しいシーン、挨拶 |
| Hushed | ヒソヒソ声 | 秘密の会話、ASMR |

**スタイルスライダー：**
- テキスト表現力：テキストへの忠実度（高い＝感情豊か）
- 感情の強さ：プリセットの効き具合
- 話者の忠実度：リファレンス音声への類似度
- 表現のバリエーション：生成のランダムさ

**LoRAアダプターの適用：**
- LoRAパスにアダプターフォルダを指定
- スケール（0.0〜2.0）で効き具合を調整

### タブ2: マニフェスト作成（Prepare Manifest）

音声データをDACVAEラテントに変換し、トレーニング用JSONLマニフェストを生成するわ。

**対応形式：**
- ローカルCSV（audiofolderフォーマット）
- ローカルJSONL
- HuggingFace Datasets

### タブ3: トレーニング（学習）

フルファインチューニング。RTX 4090なら快適よ♪

**おすすめ設定（RTX 4090/24GB）：**
- バッチサイズ: 4〜8
- 精度: bf16
- オプティマイザ: muon
- 勾配蓄積: 2

### タブ4: LoRAトレーニング

軽量なアダプター学習。少ないデータ・短時間でキャラの声を学習できるわ。

**ターゲットモジュール：**
- 基本: `wq,wk,wv,wo`（アテンション層のみ）
- 拡張: `wq,wk,wv,wo,wk_text,wv_text,wk_speaker,wv_speaker,w1,w2,w3`

**推奨パラメータ：**
- LoRA rank: 16
- Alpha: 32.0
- Dropout: 0.05
- ステップ数: 500〜3000（データ量による）

### タブ5: データセット作成（Dataset作成）

**スライス（Slice）：**
長い音声ファイルを無音区間で自動分割するわ。
- 最小/最大秒数を指定
- 無音検出の閾値調整可能

**キャプション（Caption）：**
Whisperで自動文字起こし。
- モデルサイズ: tiny〜large-v3
- 言語: 日本語自動検出
- CSV or JSONL出力

**パイプライン：**
スライス → キャプション を一括実行

**絵文字キャプション（Emoji Caption）：**
LLMで音響特徴量から絵文字アノテーションを自動付与。これが超便利！
- 対応API: LM Studio / Groq / OpenAI / Together AI
- ピッチ、エネルギー、話速、MFCC等を解析してLLMに渡す

### タブ6: チェックポイント変換

- `.pt` → `.safetensors` 変換
- LoRAの学習用 → 推論用 変換

### タブ7: モデルマージ

**マージ方式：**
| 方式 | 説明 | 向いてるケース |
|------|------|--------------|
| Weighted Average | 単純な加重平均 | 2モデルのブレンド |
| SLERP | 球面線形補間（ノルム保持） | 品質重視のマージ |
| Task Arithmetic | ベースモデル＋差分合成 | 複数の特化モデル合成 |

**部分マージ：**
レイヤーグループ（text/speaker/diffusion/io）ごとに異なるマージ方式を適用可能。

**LoRA注入：**
ドナーモデルの差分をベースに注入。スケール調整可能。

---

## CLI での使い方

### 推論

```bash
cd D:/irodori/emoji

# リファレンス音声あり
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M \
  --text "😊今日はとっても楽しい一日でした！" \
  --ref-wav path/to/reference.wav \
  --output-wav outputs/sample.wav

# リファレンスなし
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M \
  --text "こんにちは" \
  --no-ref \
  --output-wav outputs/sample.wav

# v2モデルを使う場合
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v2 \
  --text "こんにちは" \
  --no-ref \
  --output-wav outputs/sample_v2.wav

# LoRAアダプター適用
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M \
  --text "セリフ" \
  --ref-wav ref.wav \
  --lora-path lora/my_adapter \
  --lora-scale 1.0 \
  --output-wav outputs/lora_sample.wav

# 複数候補生成
.venv/Scripts/python.exe infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M \
  --text "セリフ" \
  --no-ref \
  --num-candidates 5 \
  --output-wav outputs/multi.wav
```

### データセットツール

```bash
# 音声スライス
.venv/Scripts/python.exe dataset_tools.py slice \
  --input path/to/long_audio.wav \
  --output path/to/sliced/

# Whisper文字起こし
.venv/Scripts/python.exe dataset_tools.py caption \
  --input path/to/sliced/ \
  --output-manifest path/to/manifest.csv \
  --format csv --model medium --language ja

# スライス→キャプション一括
.venv/Scripts/python.exe dataset_tools.py pipeline \
  --input path/to/long_audio.wav \
  --slice-output path/to/sliced/ \
  --output-manifest path/to/manifest.jsonl

# 絵文字キャプション（LM Studio使用）
.venv/Scripts/python.exe dataset_tools.py emoji_caption \
  --csv path/to/metadata.csv \
  --wav-dir path/to/wavs/ \
  --api lm_studio \
  --lm-studio-url http://localhost:1234
```

### LoRAトレーニング

```bash
.venv/Scripts/python.exe lora_train.py \
  --base-model checkpoints/model.safetensors \
  --manifest data/train_manifest.jsonl \
  --output-dir lora/my_character \
  --lora-rank 16 --lora-alpha 32.0 \
  --max-steps 1000
```

---

## 感情プリセットの活用

フォーク版最大の特徴の一つ！ボタン一つでCFGパラメータが最適化されるわ。

### プリセット使い分けガイド

**Normal（通常）：** ナレーション、説明文、日常会話
```
テキスト例：「今日の天気は晴れです。気温は25度でしょう。」
```

**Powerful（力強い）：** 怒り、決意、叫び、緊迫シーン
```
テキスト例：「😠絶対に許さない！😱逃げて！」
```

**Quiet（静か）：** 内省、独白、落ち着いたシーン
```
テキスト例：「😌そうね…⏸️あの日のことを、思い出していたの。」
```

**Bright（明るい）：** 挨拶、楽しい場面、元気キャラ
```
テキスト例：「😊おはよう！😆今日もいい天気だね！」
```

**Hushed（ヒソヒソ）：** 秘密話、ASMR、耳打ち
```
テキスト例：「👂ねぇ…⏸️あのね…🤭内緒なんだけど…」
```

---

## データセット作成ワークフロー

同人音声制作でオリジナルキャラの声を学習させたい場合の手順よ。

### ステップ1: 音声素材の準備

- 高品質WAVファイルを用意（48kHz/24bit推奨）
- ノイズが少ない収録環境で
- 1話者あたり最低50セグメント（できれば100以上）

### ステップ2: スライス

Web UIの「Dataset作成」タブ → Slice で長尺音声を分割

### ステップ3: キャプション

同じタブのCaption でWhisper文字起こし → CSV出力

### ステップ4: 絵文字アノテーション（任意だけど推奨）

Emoji Caption タブで、LLMにテキスト＋音響特徴から絵文字を自動付与。
感情表現のあるデータセットになって品質UP！

### ステップ5: マニフェスト作成

「Prepare Manifest」タブでDACVAEラテント変換＋JSONL生成

### ステップ6: LoRAトレーニング

少量データなら「LoRA Training」タブ。
50件程度のデータでもRTX 4090なら30分〜1時間で学習できるわ。

---

## 絵文字スタイルコントロール一覧

（本家Irodori-TTSと共通、全38種）

### 効果音・呼吸系
| 絵文字 | 効果 |
|--------|------|
| 👂 | 囁き、耳元の音 |
| 😮‍💨 | 吐息、溜息、寝息 |
| 🌬️ | 息切れ、荒い息遣い |
| 😮 | 息をのむ |
| 👅 | 舐める音、咀嚼音、水音 |
| 💋 | リップノイズ |
| 🥤 | 唾を飲み込む音 |
| 🤧 | 咳き込み、くしゃみ |
| 😒 | 舌打ち |
| 👌 | 相槌 |
| 🥱 | あくび |
| 🎵 | 鼻歌 |
| 🥵 | 喘ぎ、うめき声 |

### 感情・話し方系
| 絵文字 | 効果 |
|--------|------|
| 🤭 | くすくす笑い |
| 😏 | からかう、甘える |
| 🥺 | 声を震わせて |
| 🫶 | 優しく |
| 😭 | 嗚咽、泣き声 |
| 😱 | 悲鳴、叫び |
| 😪 | 眠そう |
| 😰 | 慌てて、どもり |
| 😆 | 喜び |
| 😠 | 怒り、拗ね |
| 😲 | 驚き |
| 😖 | 苦しげ |
| 😟 | 心配そう |
| 🫣 | 恥ずかしそう |
| 🙄 | 呆れ |
| 😊 | 楽しい |
| 🙏 | 懇願 |
| 🥴 | 酔っ払い |
| 🤐 | 口を塞がれて |
| 😌 | 安堵 |
| 🤔 | 疑問 |

### スピード・エフェクト系
| 絵文字 | 効果 |
|--------|------|
| ⏸️ | 間、沈黙 |
| ⏩ | 早口 |
| 🐢 | ゆっくり |
| 📢 | エコー、リバーブ |
| 📞 | 電話越しの音 |

---

## よりよい音声を作るためのコツ

### テキスト入力

1. **難しい漢字はひらがな/カタカナに変換**
2. **句読点を適切に入れる**（自然な間が生まれる）
3. **⏸️ で明示的に間を作る**
4. **長文は分割して生成**（品質安定）

### 感情表現の演出テクニック

```
# 段階的な感情変化
「😊ふふっ、あのね。⏸️🫣実は…ちょっと、言いにくいんだけど…😰えっと…🥺好きです。」

# 怒りから悲しみへの転換
「😠なんでそんなこと言うの！⏸️😭…ひどい…」

# ASMR系
「👂ねぇ…⏸️💋🤭ふふっ…⏸️👂聞こえてる？」

# 酔っ払い
「🥴えへへぇ〜🤭もう一杯⏸️飲んじゃおっかなぁ〜🎵」
```

### 複数候補で選ぶ

- `--num-candidates 5` で5パターン生成
- seedを固定して比較するのもアリ
- Web UIなら最大8候補を同時生成

### LoRAのコツ

- **rank 16** で十分なことが多い
- **50〜100件** のデータがあれば実用レベル
- 過学習に注意（Early Stopping推奨）
- EMAチェックポイントの方が品質が安定しやすい

---

## トラブルシューティング

### ポートが被る

```bash
# ポート番号を変えて起動
python gradio_app.py --server-port 7870
```

### CUDA out of memory

```bash
# bf16精度に切り替え（Web UIでも設定可能）
--model-precision bf16 --codec-precision bf16
```

### 初回起動が遅い

モデル（約2GB）をHugging Faceからダウンロードするため。2回目以降はキャッシュ済みで高速。

### venv再構築

```bash
cd D:/irodori/emoji
rm -rf .venv
C:/Users/ganji/AppData/Local/Programs/Python/Python310/python.exe -m venv .venv
.venv/Scripts/pip.exe install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
.venv/Scripts/pip.exe install "dacvae @ git+https://github.com/facebookresearch/dacvae" \
  "datasets>=3.0.0" "gradio>=5.0.0" "huggingface-hub>=0.34.0,<1.0" \
  "llvmlite>=0.40.0" "numba>=0.57.0" "peft>=0.18.0" "pyyaml>=6.0" \
  "safetensors>=0.7.0" "soundfile>=0.12.0" "sentencepiece>=0.1.99,<0.2" \
  "torchcodec>=0.10.0" "transformers<5" "tqdm>=4.67.3" "wandb>=0.17.0" "pandas>=2.3.3"
```

---

## クイックリファレンス

```bash
# === Web UI（全機能） → http://localhost:7863 ===
cd D:/irodori/emoji
.venv/Scripts/python.exe gradio_app.py --server-port 7863

# === CLI推論（リファレンスあり） ===
.venv/Scripts/python.exe infer.py --hf-checkpoint Aratako/Irodori-TTS-500M --text "テキスト" --ref-wav ref.wav --output-wav outputs/out.wav

# === CLI推論（リファレンスなし） ===
.venv/Scripts/python.exe infer.py --hf-checkpoint Aratako/Irodori-TTS-500M --text "テキスト" --no-ref --output-wav outputs/out.wav

# === LoRAトレーニング ===
.venv/Scripts/python.exe lora_train.py --base-model checkpoints/model.safetensors --manifest data/manifest.jsonl --output-dir lora/my_run --lora-rank 16 --max-steps 1000
```
