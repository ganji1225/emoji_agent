# 納品前品質チェックリスト

完成音声を納品・配布する前に必ず確認する項目集。

---

## 0. このチェックリストの使い方

- 各セクションの ☐ を上から順に確認
- 1つでも NG があれば該当する対処法に従って修正
- 全部 ✅ になってから納品

---

## 1. ファイル存在チェック

### ☐ master/full_work.wav が存在する
```bash
ls -la D:/irodori/projects/{name}/master/full_work.wav
```

### ☐ シーン別ファイルが想定通りある
```bash
ls D:/irodori/projects/{name}/master/*.wav | wc -l
```
→ 期待値：シーン数 + 1（full_work.wav 含む）

### ☐ MP3 が必要なら mp3/ フォルダにある（オプション）
```bash
ls D:/irodori/projects/{name}/mp3/
```

---

## 2. 行数チェック

### ☐ production.csv で approved 行数 = 期待行数
```python
import csv
rows = list(csv.DictReader(open('D:/irodori/projects/{name}/production.csv', encoding='utf-8-sig')))
approved = [r for r in rows if r['approved_candidate']]
print(f'approved: {len(approved)}行')
```

### ☐ approved/ フォルダのファイル数が一致
```bash
find D:/irodori/projects/{name}/approved -name "*.wav" | wc -l
```
→ approved 行数と一致すること

---

## 3. 音声長チェック

### ☐ full_work.wav の総時間が企画書通り
```python
import soundfile as sf
info = sf.info('D:/irodori/projects/{name}/master/full_work.wav')
print(f'{info.duration/60:.1f}分')
```

### ☐ 各シーンの時間が極端に短くない
- 1セリフ平均 5〜8秒
- 50行のシーンで4〜6分が標準

### ☐ 個々のセリフファイルに 0.5秒未満が無い
```python
import soundfile as sf, glob
for f in glob.glob('D:/irodori/projects/{name}/approved/**/*.wav', recursive=True):
    d = sf.info(f).duration
    if d < 0.5:
        print(f'⚠️ {f}: {d:.2f}秒')
```

---

## 4. 音質チェック

### ☐ qc_report.csv で qc_fail 行が無い（or 全部 done）
```python
import csv
from collections import Counter
rows = list(csv.DictReader(open('D:/irodori/projects/{name}/qc_report.csv', encoding='utf-8-sig')))
print(Counter(r['qc_result'] for r in rows))
```

### ☐ クリッピング（peak ≥ 0.99）が approved に含まれてない
qc_report.csv で peak_value > 0.99 の行を確認。該当があれば別候補に切り替え。

### ☐ 無音判定（RMS < 0.001）が approved に含まれてない
qc_report.csv で rms_energy が極端に低い行をチェック。

### ☐ ノイズ・かすれが目立つ箇所が無い
**手動確認**：full_work.wav を最初から最後まで通しで聴く。

---

## 5. テキストチェック

### ☐ Whisper 誤認識・文字化けが残ってない
production.csv の text_raw をざっと確認：
```python
import csv
for r in csv.DictReader(open('production.csv', encoding='utf-8-sig')):
    txt = r['text_raw']
    if '？？' in txt or '？' * 3 in txt:
        print(f'⚠️ {r["scene_id"]}/{r["line_id"]}: {txt}')
```

### ☐ セリフ内容に誤読・誤変換が無い
- 「子宮」→「視点」のような Whisper 由来の誤認識
- 同音異義語の混入

### ☐ 想定したセリフ順序になってる
script_with_emoji.txt を順に確認：
```bash
cat D:/irodori/projects/{name}/script_with_emoji.txt
```

---

## 6. シーン構成チェック

### ☐ シーン区切りの無音（2.0秒）が入っている
full_work.wav を聴いてシーン切り替わり点で違和感がないか。

### ☐ セリフ間の無音（0.8秒）が自然
連続して聞くと早すぎる/遅すぎる場合は LINE_SILENCE_SEC を調整。

### ☐ 末尾の無音が長すぎない
**ma_agent.py が `trim_trailing_silence()` で自動カット**するが、念のため確認。

---

## 7. 声質一貫性チェック

### ☐ 同じシーン内で声質がブレてない
- candidate ガチャで全然違う声が混ざることがある
- 特に強度の高いシーン（CFG=7+）で発生しがち

### ☐ シーン間で声質が極端に変わってない
- caption が変わると声質も変わる（意図的なら OK）
- 意図せず変わってる場合は caption の整合性を確認

### ☐ LoRA を使った場合：scale が安定範囲（0.5〜1.5）
LoRA scale が 2.0 超で発散するリスクあり。

---

## 8. ファイル形式チェック

### ☐ サンプルレート 48kHz
```python
import soundfile as sf
info = sf.info('D:/irodori/projects/{name}/master/full_work.wav')
assert info.samplerate == 48000, f'sr={info.samplerate}'
```

### ☐ ビット深度 16bit / 24bit / float（用途による）
納品先の要件に合わせる。

### ☐ MP3 の場合：適切なビットレート
- 配布用：VBR qscale 2（≒190kbps、ma_agent.py のデフォ）
- 高音質：320kbps CBR

---

## 9. メタデータ・著作権

### ☐ ファイル名に日本語/特殊記号が無い
配布時の互換性のため、ASCII のみ推奨：
```
✅ scene_01.wav  scene_02.wav  full_work.wav
❌ シーン①.wav  本編.wav
```

### ☐ 学習素材の権利確認
- LoRA 学習に使った素材：自分の声 / 商用OK素材 / 配布OK素材のみ
- ゼロショット参照音声：同上

### ☐ Irodori-TTS のライセンス遵守
- コードは MIT
- **モデル重みは商用利用禁止**（Aratako/Irodori-TTS-500M-v2 のライセンス参照）

---

## 10. バックアップ

### ☐ 完成版の WAV を別場所にコピー
```bash
cp D:/irodori/projects/{name}/master/full_work.wav D:/backup/{name}_v1_final.wav
```

### ☐ production.csv も保存
再現性確保のため、生成時の CSV を残す。

### ☐ project_brief.json と grok_prompt.md も保存
将来の続編 / リテイク用。

---

## 11. 最終リスニング

### ☐ ヘッドホンで通しで聴く
- スピーカーでは見逃すノイズが分かる
- 左右バランス（モノラルなら関係なし）

### ☐ 別端末でも聴く
- スマホ・別 PC で再生確認
- 環境差で違和感が出ないか

### ☐ 第三者の耳でチェック（可能なら）
自分は聴き慣れて気づかなくなる現象あり。

---

## 12. NGがあった場合の対処早見表

| NG項目 | 対処 |
|-------|------|
| 行数不足 | production.csv の status と approved_candidate を確認、不足分を追加収録 |
| ノイズ・かすれ | 別 candidate に切り替え or リテイク |
| Whisper誤認識 | text_raw を修正 → 再生成 |
| 声質ブレ | caption / CFG / guidance_mode を再調整 |
| 無音長すぎ | ma_agent.py の LINE_SILENCE_SEC / SCENE_SILENCE_SEC を調整 |
| サンプルレート違い | infer.py の codec-repo が正しいか確認 |

---

## 13. チェック完了テンプレート

すべて ✅ になったら、以下を記録：

```
=== 納品チェック完了 ===
プロジェクト名: {project_name}
納品日: {YYYY-MM-DD}
完成版: {file_name}.wav
総時間: {分}
行数: {N}
チェック実施者: {ダーリン}
✅ 全項目クリア
```

---

**最終更新: 2026-04-25**
