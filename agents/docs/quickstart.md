# クイックスタート

**初日にこれを読めば、まず1作品作れる**最短ガイド。
詳細は他のドキュメントに任せて、最小限の流れだけ示す。

---

## 0. 前提

- Windows 環境
- `D:/irodori/` にリポジトリ一式が配置済み
- Emoji-TTS の `.venv` 構築済み
- GPU（VRAM 12GB+ 推奨）

---

## 1. プロジェクト作成（5分）

### 1-1. プロデューサーが Claude に作品コンセプトを伝える
```
例: 「甘々系の耳かき音声を作りたい。シーンは3つ、合計10分くらい」
```

### 1-2. Claude が grok_prompt.md と project_brief.json を生成
- `D:/irodori/projects/{project_name}/grok_prompt.md`
- `D:/irodori/projects/{project_name}/project_brief.json`

---

## 2. 台本作成（外部 Grok で20〜30分）

### 2-1. プロデューサーが grok_prompt.md を Grok に渡す
- Grok 公式サイト等で grok_prompt.md の内容を投げる
- Grok が response.json 形式で台本を返す

### 2-2. 受け取った JSON を配置
```
D:/irodori/projects/{project_name}/grok/response.json
```

### 2-3. プロデューサーが内容確認
- セリフが想定通りか
- emoji_suggestion が 3 個ずつくらいあるか（少なければ Claude に修正依頼）

---

## 3. 脚本処理（Claude に依頼、3分）

プロデューサーが Claude に依頼：
> 「{project_name} の grok_bridge を流して」

Claude が裏で実行する内容：
```bash
python D:/irodori/agents/grok_bridge.py validate {project_name}
python D:/irodori/agents/grok_bridge.py process {project_name}
```

→ `production.csv` 生成完了

---

## 4. キャプション確認（5分）

production.csv の `caption` / `cfg_text` / `cfg_guidance_mode` 列が自動設定される。
気になるシーンがあれば手動で調整可能（[`caption_design_guide.md`](./caption_design_guide.md) 参照）。

**通常はそのまま次へ。**

---

## 5. 音声生成（GPU で30分〜1時間）

### 5-0. （オプション）LoRA で固定の声を使う場合
基本は LoRA 指定なしで進めて OK。特定キャラの LoRA を全行に適用したい場合：

```bash
# 全行に LoRA 適用
python D:/irodori/agents/set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 確認
python D:/irodori/agents/set_lora.py {project_name} --show

# 解除
python D:/irodori/agents/set_lora.py {project_name} --clear
```

LoRA を作る方法は [`lora_training_guide.md`](./lora_training_guide.md) 参照。

### 5-1. CLI で実行（GPU 排他のため Claude チャットからは推奨しない）
```bash
cd D:/irodori
python agents/recorder.py {project_name}
```

→ `D:/irodori/projects/{project_name}/audio/{scene_id}/line_XXX_001~003.wav` が生成される（行数 × 3候補）

**目安：**
- 50行で約 10〜15 分
- 100行で約 20〜30 分
- 大規模な作品なら昼休み or 夜中に走らせる

---

## 6. QC + 承認（試聴含めて1〜2時間）

### 6-1. Claude に依頼：
> 「qc-reviewer 走らせて」

→ `qc_report.csv` と `approvals_template.json` が生成される

### 6-2. 音声を試聴
```
D:/irodori/projects/{project_name}/audio/{scene_id}/
```
WAV プレイヤーで聴き比べ（候補1, 2, 3）

### 6-3. approvals_template.json を編集
```json
{
  "scene_01/line_001": 2,    ← QC推奨
  "scene_01/line_002": 3,    ← 自分が好きな候補に変更
  ...
}
```

**ポイント：** QC推奨が良ければ何もしなくてOK。違うと思った行だけ数字を変える。

### 6-4. 承認反映
```bash
python D:/irodori/agents/approve.py {project_name}
```

---

## 7. MA / 最終出力（5〜10分）

プロデューサーが Claude に依頼：
> 「ma-master 走らせて」

または直接：
```bash
python D:/irodori/agents/ma_agent.py {project_name}

# MP3 も同時に書き出す場合
python D:/irodori/agents/ma_agent.py {project_name} --mp3
```

### 出力ファイル
```
D:/irodori/projects/{project_name}/master/
  scene_01.wav
  scene_02.wav
  ...
  full_work.wav    ← これが完成版
```

---

## 8. 納品前の最終チェック

[`quality_checklist.md`](./quality_checklist.md) に従って確認：

- [ ] full_work.wav の長さが想定通り
- [ ] 全シーンが含まれている（行数確認）
- [ ] ノイズ・クリッピングなし
- [ ] 無音区間が長すぎない（先頭/末尾/シーン間）
- [ ] 文字化けセリフが残ってない（QC段階で除去済みのはず）

---

## 9. 困ったら

| 状況 | 参照先 |
|------|-------|
| 全体像を再確認したい | [`pipeline_overview.md`](./pipeline_overview.md) |
| 声が思った通りにならない | [`caption_design_guide.md`](./caption_design_guide.md) |
| 絵文字パターンを変えたい | [`emoji_pattern_reference.md`](./emoji_pattern_reference.md) |
| エラーが出た | [`troubleshooting.md`](./troubleshooting.md) |
| 固定の声を作りたい | [`lora_training_guide.md`](./lora_training_guide.md) |

---

## 10. 1作品の所要時間目安

| フェーズ | 時間 |
|---------|------|
| 企画 + Grok 台本生成 | 30分〜1時間 |
| 脚本処理 + キャプション設定 | 5〜10分 |
| 収録（GPU生成） | 行数 × 12秒 |
| QC + 試聴 + 承認 | 1〜2時間 |
| MA + 最終出力 | 10分 |
| **合計（50行作品）** | **3〜4時間** |

---

## 11. やってはいけないこと TOP 5

1. ❌ **production.csv を Excel で開いて保存** → 絵文字が文字化け
2. ❌ **GPU 処理（動画/SD）と recorder の並列実行** → CUDA OOM
3. ❌ **approved_candidate を直接 production.csv に手書き** → `approve.py` 経由必須
4. ❌ **emoji_suggestion を 4 個以上 + CFG 7.0** → ノイズ多発
5. ❌ **Claude に R-18 セリフを直接書かせる** → 拒否される。Grok 担当

---

**最終更新: 2026-04-25**
