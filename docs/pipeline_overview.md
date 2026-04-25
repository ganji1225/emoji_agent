# パイプライン全体ガイド

R-18 同人音声制作パイプラインの全体像。新規参画メンバーが最初に読む一冊。

---

## 0. このシステムは何をするか

**ゴール**：作品コンセプトから納品音声（WAV/MP3）まで、Claude Code 上のエージェント連携で半自動制作する。

**技術スタック**：
- TTS: Emoji-TTS（Aratako/Irodori-TTS-500M-v2-VoiceDesign のフォーク）
- 台本生成: Grok（外部LLM、R-18テキスト担当）
- ディレクション・収録・QC・MA: Claude エージェント

**Claude制限との切り分け**：
- Claude は R-18 テキスト**そのもの**を書かない
- 企画・収録演出・QC・MA は Claude
- R-18 セリフは Grok に外注、Claude が前後処理する

---

## 1. パイプライン全体図

```
[0. 企画]
  プロデューサー × Claude
  作品コンセプト → grok_prompt.md / project_brief.json
        ↓
[Grok: 台本生成]
  プロデューサーが Grok にプロンプトを渡して実行
  → response.json（台本JSON）
        ↓
[1. 脚本処理] (script-pipeline エージェント)
  grok_bridge validate → process → casting apply
  → production.csv（中央データ）
        ↓
[2. 収録] (recorder エージェント)
  GPU で infer.py を全行に対し実行
  → audio/{scene}/{line_id}_{c01,c02,c03}.wav
        ↓
[3. QC] (qc-reviewer エージェント)
  音声長・RMS・無音・クリッピング自動チェック
  → qc_report.csv + approvals_template.json（推奨候補）
        ↓
[プロデューサー: 主観判定]
  approvals_template.json を編集（候補番号変更）
        ↓
[4. 承認反映] (approve.py スクリプト)
  approved_candidate 列を production.csv に書き込み
        ↓
[5. MA/ミキシング] (ma-master エージェント)
  ma_agent.py で結合・末尾無音トリム
  → master/scene_XX.wav + master/full_work.wav
        ↓
[完成品]
  納品音声（WAV / 任意で MP3）
```

---

## 2. プロジェクトフォルダ構造

```
D:/irodori/projects/{project_name}/
  project_brief.json         ← 作品企画書
  grok_prompt.md             ← Grok への依頼文
  grok/
    response.json            ← Grok から返ってきた台本JSON
  production.csv             ← 中央データ（全エージェント共有）
  qc_report.csv              ← QC 結果
  approvals_template.json    ← QC推奨候補（人間が編集）
  audio/
    {scene_id}/
      line_001_001.wav       ← 候補1
      line_001_002.wav       ← 候補2
      line_001_003.wav       ← 候補3
      ...
  approved/
    {scene_id}/
      line_001.wav           ← 承認済み（候補から1本コピー）
      ...
  master/
    {scene_id}.wav           ← シーン結合済み
    full_work.wav            ← 全シーン結合済み
  mp3/                        ← --mp3 オプション時のみ
    *.mp3
```

---

## 3. エージェント構成

### project-orchestrator（ディレクター）
- **役割**：全体統括。`init / script / record / qc / master / full` の各ステージを呼び出す
- **モデル**：sonnet
- **人間介入ポイント**で停止：Grok実行 / approved_candidate 入力

### script-pipeline（脚本処理）
- **役割**：grok/response.json → production.csv 変換
- **内部呼び出し**：`grok_bridge validate` → `grok_bridge process` → `casting apply`
- **モデル**：sonnet

### recorder（収録）
- **役割**：production.csv の `status=pending` 行を全部音声生成
- **GPU 排他**：他のGPU処理（動画生成等）と並列禁止
- **モデル**：haiku（軽量タスク）

### qc-reviewer（品質チェック）
- **役割**：qc_agent.py 実行 → qc_report.csv 生成 → 推奨候補を提示
- **副産物**：`approvals_template.json`（QC推奨候補入り）
- **モデル**：sonnet

### ma-master（最終仕上げ）
- **役割**：approved 行を結合 → シーン別WAV + full_work.wav 生成
- **副機能**：末尾無音自動トリム、MP3変換
- **モデル**：haiku

---

## 4. 中央データ契約：production.csv

**全エージェント間のデータ受け渡しの唯一の真実**。Excel で開かないこと（cp932で絵文字化け）。

| 列名 | 設定者 | 説明 |
|------|--------|------|
| scene_id | script-pipeline | シーンID |
| line_id | script-pipeline | 行ID（line_001...） |
| speaker | script-pipeline | 話者名 |
| emotion_note | script-pipeline | 感情メモ |
| text_raw | script-pipeline | 元テキスト |
| text_with_emoji | script-pipeline | 絵文字挿入済みテキスト |
| caption | casting | VoiceDesign キャプション |
| cfg_text | casting | CFG テキストスケール |
| cfg_caption | casting | CFG キャプションスケール |
| cfg_speaker | casting | CFG スピーカースケール |
| cfg_guidance_mode | casting | independent / joint / alternating |
| num_steps | casting | ステップ数（推奨40） |
| num_candidates | recorder | 生成候補数（デフォ3） |
| seed | recorder | 使用シード（再現性確保） |
| lora_path | casting/手動 | LoRA アダプタパス（空=不使用） |
| lora_scale | casting/手動 | LoRA 適用強度（デフォ1.0） |
| status | recorder/qc/人間 | pending / generated / qc_pass / qc_fail / approved / done |
| approved_candidate | 人間 | 承認候補番号（1-based） |
| notes | 任意 | 備考 |

**status の遷移：**
```
pending → generated → qc_pass → approved → done
                 ↓
              qc_fail（再録）
```

---

## 5. 人間がやること / エージェントがやること

### 人間（プロデューサー）の役割
- **企画**：作品コンセプト・キャラ設定・シーン構成を決める
- **Grok 実行**：grok_prompt.md を Grok に渡して台本生成
- **シーン強度の確認**：production.csv の caption を必要に応じて調整
- **音声試聴**：候補を聴いて選定（approvals_template.json を編集）
- **GPU 管理**：動画生成等と並列にしない判断

### Claude エージェントの役割
- **絵文字挿入**：emotion_tags から絵文字パターンを自動選択
- **キャプション割当**：シーン強度に応じた CFG 値・guidance_mode 適用
- **音声生成**：infer.py を全行に対して実行
- **QC**：技術指標（RMS・無音・クリッピング）の自動判定
- **MA**：シーン結合・末尾無音トリム・MP3変換

---

## 6. 典型的な作業フロー（1作品の流れ）

### Day 1: 企画 + 台本
1. プロデューサー：作品コンセプトを Claude と相談
2. Claude：grok_prompt.md と project_brief.json を生成
3. プロデューサー：Grok に grok_prompt.md を渡して response.json を取得
4. response.json を `D:/irodori/projects/{name}/grok/` に配置

### Day 1〜2: 脚本処理 + 収録
5. Claude（script-pipeline）：production.csv 生成
6. プロデューサー：production.csv の caption を必要に応じて確認
7. Claude（recorder）：GPU で全行生成（行数 × 12秒程度）

### Day 2: QC + 承認
8. Claude（qc-reviewer）：qc_report.csv + approvals_template.json 生成
9. プロデューサー：audio/ フォルダの音声を聴いて approvals_template.json を編集
10. プロデューサー：`python agents/approve.py {project_name}` 実行

### Day 2: MA + 納品
11. Claude（ma-master）：master/full_work.wav 生成
12. 必要なら `--mp3` で MP3 も書き出し
13. 納品

**所要時間目安：50行 × 3候補 = 150ファイルで丸2日（試聴に時間かかる）**

---

## 7. 関連ドキュメント

| 用途 | ドキュメント |
|------|-------------|
| とにかく1作品作りたい | [`quickstart.md`](./quickstart.md) |
| 台本のキャプション設計 | [`caption_design_guide.md`](./caption_design_guide.md) |
| 絵文字パターンの選び方 | [`emoji_pattern_reference.md`](./emoji_pattern_reference.md) |
| 納品前のチェック | [`quality_checklist.md`](./quality_checklist.md) |
| LoRA で固定の声を作る | [`lora_training_guide.md`](./lora_training_guide.md) |
| 困った時 | [`troubleshooting.md`](./troubleshooting.md) |

---

**最終更新: 2026-04-25**
