# トラブルシューティング集

過去に発生したエラー・問題と対処法のリファレンス。

---

## 1. production.csv 関連

### ❌ 文字化け（絵文字が ?? になる）

**症状：**
- production.csv の text_with_emoji 列が `??????` だらけ
- recorder 実行で「絵文字が認識されない」

**原因：**
- Excel で開いて保存すると `cp932`（Shift-JIS系）に変換される
- 絵文字（🥵🫣 等）は cp932 に存在しないため `??` に化ける

**対処法：**
- ❌ Excel で開かない
- ✅ VS Code / メモ帳++ / `python` で開く
- ✅ approved_candidate の編集は `approve.py` を使う

```bash
# 文字化けが起きた場合の復旧
python -c "
import csv
rows = list(csv.DictReader(open('production.csv', encoding='cp932')))
# 絵文字列が ?? の場合は grok_bridge process で再生成
"
```

最善は、**最初から `approve.py` 経由で承認**する運用。

---

### ❌ PermissionError on CSV write

**症状：**
- `PermissionError: [Errno 13] Permission denied: 'production.csv'`

**原因：**
- production.csv を Excel やテキストエディタで開いたままにしている

**対処法：**
- ファイルを閉じてから再実行
- 編集中に他プロセスで書き込まないルールにする

---

## 2. GPU 関連

### ❌ CUDA out of memory

**症状：**
- `RuntimeError: CUDA out of memory. Tried to allocate ...`

**原因：**
- 動画生成 / 別の TTS / Stable Diffusion 等と並列実行
- バッチサイズが大きすぎる

**対処法：**

1. **他の GPU 使用プロセスを止める**
   ```bash
   # 一括停止
   taskkill /F /IM python.exe
   ```

2. **バッチサイズを下げる**（学習時）
   ```bash
   --batch-size 2 --gradient-accumulation-steps 4
   ```

3. **gradient checkpointing を有効化**（フル学習のみ。LoRAでは caption 非対応バグあり）

---

### ⚠️ GPU を独占するルール

| 処理 | GPU使用量 |
|------|---------|
| 動画生成 | フル使用 |
| TTS 推論（recorder） | フル使用 |
| LoRA 学習 | フル使用 |
| 画像生成（SD） | フル使用 |

→ **同時に2つは走らせない**。Claude セッション中も「動画やってる」と言われたら recorder は止める判断。

---

## 3. recorder 関連

### ❌ status=pending のまま全行 fail

**症状：**
- 全行が `gen_fail` になる
- ログに `infer.py: error` の連続

**確認手順：**

1. 単発で infer.py が動くか確認
   ```bash
   D:/irodori/emoji/.venv/Scripts/python.exe D:/irodori/emoji/infer.py \
     --hf-checkpoint Aratako/Irodori-TTS-500M-v2-VoiceDesign \
     --codec-repo Aratako/Semantic-DACVAE-Japanese-32dim \
     --text "テスト" --caption "若い女性が話している。" \
     --no-ref --output-wav test.wav
   ```

2. **エラーパターン別対処：**

| エラー | 原因 | 対処 |
|--------|------|------|
| FileNotFoundError on .safetensors | チェックポイント未DL | `huggingface-cli login` 後にHF経由で再取得 |
| latent_dim mismatch | codec-repo を指定し忘れ | `Aratako/Semantic-DACVAE-Japanese-32dim` を必須指定 |
| empty text | text_with_emoji が空 | grok_bridge process を再実行 |

---

### ⚠️ `--codec-repo` 必須

VoiceDesign モデルは `latent_dim=32` の codec を使う。**指定しないと latent_dim 不一致でエラー**。

```bash
# 必須オプション
--codec-repo Aratako/Semantic-DACVAE-Japanese-32dim
```

---

## 4. Whisper 誤認識への対応

### ⚠️ 漢字が間違って書き起こされる

**よくあるケース：**
- 「子宮」→ 「視点」「資金」
- 「淫紋」→ 「印鑑」
- 「霊山」→ 「礼讃」「歴山」
- 「番人」→ 「半人」

**対処法：**

1. **書き起こし後に CSV 目視チェック**（学習用データ作成時）
2. **文字化け検出：**
   ```python
   # おかしい文字パターンの検出
   import csv
   for row in csv.DictReader(open('manifest_raw.csv', encoding='utf-8-sig')):
       if any(c in row['text'] for c in '視点 資金 印鑑'):
           print(f"要確認: {row['file_name']}: {row['text']}")
   ```

3. **どうしてもの場合は手動修正**

LoRA 学習素材なら多少の誤認識は許容OK（声質を学ぶだけだから）。

---

## 5. ffmpeg / torchcodec 関連

### ❌ libtorchcodec_core8.dll Could not load

**症状：**
- `OSError: Could not load this library: ... libtorchcodec_core{4,5,6,7,8}.dll`
- `dataset_tools.py slice` や `prepare_manifest.py` が落ちる

**原因：**
- FFmpeg 8.0 と torchcodec の互換性問題（PyTorch 2.11.0 環境）

**対処法：**

1. **`dataset_tools.py slice` の代わり**：
   - `D:/irodori/agents/docs/lora_training_guide.md` の librosa スライサーを使用

2. **`prepare_manifest.py` の代わり**：
   - `D:/irodori/emoji/custom_prepare_manifest.py` を使用

3. **完全に直したい場合：**
   - FFmpeg を 5.x or 6.x にダウングレード（推奨しない）
   - torchcodec をアップグレード（互換版が出るまで待ち）

---

### ❌ ffmpeg が見つからない（MP3変換時）

**症状：**
- `ma_agent.py --mp3` で `[error] ffmpeg が見つかりません`

**対処法：**
```bash
# winget でインストール
winget install Gyan.FFmpeg

# PATH 通っているか確認
which ffmpeg
ffmpeg -version
```

---

## 6. LoRA 学習関連

### ❌ ModelConfig got unexpected keyword 'max_caption_len'

**修正済み**（lora_train.py 2026-04-25 修正版）。
詳細は [`lora_training_guide.md`](./lora_training_guide.md) §6 バグ① 参照。

### ❌ LatentTextDataset got unexpected keyword 'latent_patch_size'

**修正済み**（lora_train.py 2026-04-25 修正版）。
詳細は [`lora_training_guide.md`](./lora_training_guide.md) §6 バグ② 参照。

### ❌ caption_input_ids and caption_mask are required

**修正済み**（lora_train.py 2026-04-25 修正版）。
詳細は [`lora_training_guide.md`](./lora_training_guide.md) §6 バグ③④ 参照。

### ❌ checkpointed() got unexpected keyword 'caption_state'

**回避策**：`--grad-checkpoint` を**使わない**。
詳細は [`lora_training_guide.md`](./lora_training_guide.md) §6 バグ⑤ 参照。

---

## 7. ma-master 関連

### ❌ approved 音声ファイルが存在しない

**症状：**
- `[warn] ソースが見つかりません: audio/scene_01/line_001_002.wav`

**原因：**
- approved_candidate に指定した候補番号のファイルが無い
- audio/ フォルダ内のファイル名が想定と違う

**対処法：**

1. **ファイルの存在を確認：**
   ```bash
   ls D:/irodori/projects/{project_name}/audio/{scene_id}/
   ```

2. **production.csv の approved_candidate を確認：**
   ```python
   import csv
   for r in csv.DictReader(open('production.csv', encoding='utf-8-sig')):
       if r['approved_candidate']:
           print(f"{r['scene_id']}/{r['line_id']}: c{r['approved_candidate']}")
   ```

3. **不一致の行を再生成 or approved_candidate を修正**

---

### ❌ master/full_work.wav が短い

**症状：**
- 期待時間より短い結合音声

**原因：**
- 一部の行で承認が漏れている
- status が approved になってない

**対処法：**

```bash
python -c "
import csv
from collections import Counter
rows = list(csv.DictReader(open('production.csv', encoding='utf-8-sig')))
print(Counter(r['status'] for r in rows))
print(f'approved with candidate: {sum(1 for r in rows if r[\"approved_candidate\"])}')"
```

→ approved 行数 = approved_candidate 入力済み行数 でないと結合に含まれない。

---

## 8. grok_bridge 関連

### ❌ JSONDecodeError on response.json

**症状：**
- `JSONDecodeError: Expecting ',' delimiter: line N column M`

**原因：**
- Grok 出力でカンマ抜け / 引用符ミス
- 行間に余計な空白行

**対処法：**

1. **VS Code で response.json を開く** → エラー位置がハイライトされる
2. **よくある修正：**
   - オブジェクト間のカンマ抜け
   - `"` の閉じ忘れ
   - 末尾のカンマ余分

---

### ⚠️ emoji_suggestion が短すぎる

**症状：**
- Grok が `🥵 ... 💦` のように prefix/suffix が1個ずつしか入ってない

**対処法：**
- プロデューサーに「3個ずつに調整して」と頼む（手動編集）
- または `script_processor.py` の `build_sandwich()` で再構築

---

## 9. 承認フロー関連

### ⚠️ approvals_template.json に新規行が含まれてない

**症状：**
- 後から追加した行が approvals_template.json に出てこない

**原因：**
- qc-reviewer は status=generated の行だけを QC する
- 既に approved/done になってる行は再 QC されない

**対処法：**

```bash
# 新規行だけ qc_agent を再実行
python D:/irodori/agents/qc_agent.py {project_name}
```

→ approvals_template.json は **status=generated の行だけ** で書き換わる（既存 approved 行は残る）。

---

## 10. その他

### ⚠️ Grok 実行時の R-18 弾かれ

**症状：**
- Grok から「規制対象」「内容を変えて」と返ってくる

**対処法：**
- grok_prompt.md の表現を婉曲化
- 「フィクションの音声制作」「成人向け同人」を明記
- それでもダメなら別 LLM（Claude では不可）

---

### 💡 Whisper のモデル選択

| モデル | 精度 | 速度 | 用途 |
|--------|------|------|------|
| tiny | ★ | ⚡⚡⚡⚡ | 試験用 |
| base | ★★ | ⚡⚡⚡ | 軽量 |
| small | ★★★ | ⚡⚡ | バランス |
| medium | ★★★★ | ⚡ | 標準推奨 |
| **large-v3** | ★★★★★ | 🐢 | **本番推奨** |

LoRA 学習素材は **large-v3** 一択。

---

## 11. 困った時の確認手順

1. **production.csv の status 分布を確認**
   ```python
   from collections import Counter
   import csv
   rows = list(csv.DictReader(open('production.csv', encoding='utf-8-sig')))
   print(Counter(r['status'] for r in rows))
   ```

2. **audio/ フォルダのファイル数を確認**
   ```bash
   find D:/irodori/projects/{name}/audio -name "*.wav" | wc -l
   ```

3. **エラーログを最後まで読む**（最初のエラーじゃなく最後のエラーが原因）

4. **このドキュメントの該当節を検索**

5. **Claude（姉さん）に投げる**

---

**最終更新: 2026-04-25**
