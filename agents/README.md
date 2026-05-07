# irodori 音声制作パイプライン（emoji_agent）

R-18 同人音声作品を半自動制作するための **Claude Code エージェント + Python ツールキット**。
[Emoji-TTS](https://github.com/iron-mukakin/Emoji-TTS) をエンジンとして利用し、
企画・台本処理・収録・QC・MA までを統合管理する。

---

## 📁 構成

```
agents/
  ├─ docs/                     # 📚 ドキュメント（必読）
  │   ├─ pipeline_overview.md      # 全体パイプライン解説
  │   ├─ quickstart.md             # 初日に1作品作る最短ガイド
  │   ├─ caption_design_guide.md   # キャプション設計のコツ
  │   ├─ emoji_pattern_reference.md # 絵文字パターン辞典
  │   ├─ lora_training_guide.md    # LoRA で固定の声を作る
  │   ├─ troubleshooting.md        # よくあるエラーと対処
  │   └─ quality_checklist.md      # 納品前チェックリスト
  │
  ├─ knowledge/                # 🧠 ナレッジコレクター収集データ
  │   ├─ kb_index.json
  │   ├─ knowledge_base.md
  │   ├─ pending_updates.json
  │   ├─ rejection_feedback.json
  │   ├─ seen_urls.json
  │   └─ daily/                # 日次収集レポート
  │
  ├─ templates/                # テンプレート群
  │   └─ grok_prompt_template.md
  │
  ├─ # 🛠️ パイプラインスクリプト
  ├─ project_manager.py        # プロジェクトフォルダ管理
  ├─ planner.py                # 企画支援
  ├─ grok_bridge.py            # Grok JSON → production.csv
  ├─ script_processor.py       # 絵文字挿入・スクリプト変換
  ├─ casting.py                # キャプション割当
  ├─ recorder.py               # 音声生成（GPU）
  ├─ qc_agent.py               # 品質チェック
  ├─ approve.py                # 承認候補反映
  ├─ ma_agent.py               # シーン結合・MP3変換
  ├─ set_lora.py               # LoRA 設定管理
  ├─ test_guidance_mode.py     # guidance_mode 比較テスト
  ├─ knowledge_collector.py    # ナレッジ自動収集
  ├─ download_konomi_voices.py # 学習素材ダウンロード補助
  │
  ├─ # ⚙️ 設定
  ├─ default_captions.json     # キャプションプロファイル + LoRA紐付け
  └─ emoji_patterns.json       # 絵文字パターンライブラリ
```

---

## 🎯 主な特徴

- **Claude Code エージェント連携**: project-orchestrator / script-pipeline / recorder / qc-reviewer / ma-master
- **production.csv による中央データ契約**: 全エージェント間の唯一の真実
- **LoRA 対応**: シーン別・キャラ別 LoRA 切り替えをパイプラインで管理
- **VoiceDesign キャプション設計**: CFG値 / guidance_mode / 絵文字パターンの最適解を内蔵
- **自動 QC + 承認フロー**: utf-8 維持で文字化けゼロ

---

## 🚀 クイックスタート

詳細は [`docs/quickstart.md`](./docs/quickstart.md) を参照。

```bash
# 1. プロジェクト作成（Claude と対話）
# 2. Grok で台本生成 → response.json 配置
# 3. 脚本処理
python grok_bridge.py validate {project_name}
python grok_bridge.py process {project_name}

# 4. （オプション）LoRA 適用
python set_lora.py {project_name} --lora voice_ganyu_v1 --scale 1.0

# 5. 音声生成
python recorder.py {project_name}

# 6. QC + 承認
python qc_agent.py {project_name}
# → audio/ を試聴 → approvals_template.json を編集
python approve.py {project_name}

# 7. MA 最終出力
python ma_agent.py {project_name} --mp3
```

---

## 🔗 関連リポジトリ

- **エンジン**: [Emoji-TTS フォーク](https://github.com/iron-mukakin/Emoji-TTS) — Irodori-TTS フォーク
- **個人バックアップ（エンジン+LoRA）**: `ganji1225/emoji`（private）

---

## 📋 想定環境

- Windows 11
- Python 3.10
- GPU: VRAM 12GB+ 推奨
- Emoji-TTS が `D:/irodori/emoji/` に配置済み
- プロジェクトフォルダ: `D:/irodori/projects/{project_name}/`

---

## 📝 ライセンス

private リポジトリ。個人利用前提。

---

**最終更新: 2026-04-26**
