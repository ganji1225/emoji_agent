#!/usr/bin/env python3
"""企画エージェント - 作品企画書とGrok用プロンプトを生成"""
import json
import sys
from pathlib import Path

PROJECTS_DIR = Path("D:/irodori/projects")


def generate_grok_prompt(project_dir: Path) -> str:
    """project_brief.json からGrok用プロンプトを生成する"""
    brief_path = project_dir / "project_brief.json"
    if not brief_path.exists():
        raise FileNotFoundError(f"project_brief.json が見つかりません: {brief_path}")

    with open(brief_path, "r", encoding="utf-8") as f:
        brief = json.load(f)

    # キャラクター情報の組み立て
    chars_text = ""
    for ch in brief.get("characters", []):
        chars_text += f"""
### {ch['name']}
- 年齢: {ch.get('age', '不明')}
- 性格: {ch.get('personality', '')}
- 口調: {ch.get('speech_style', '')}
- 体の特徴: {ch.get('body_features', '')}
- 関係性: {ch.get('relationship', '')}
"""

    # シーン構成の組み立て
    scenes_text = ""
    for sc in brief.get("scenes", []):
        scenes_text += f"""
### {sc['scene_id']}: {sc.get('title', '')}
- 概要: {sc.get('description', '')}
- 雰囲気・感情の流れ: {sc.get('mood', '')}
- 目安セリフ数: {sc.get('estimated_lines', '?')}行
"""

    total_lines = brief.get("line_count_target", 50)

    speakers = ', '.join(ch['name'] for ch in brief.get('characters', []))

    prompt = f"""# 台本生成依頼

## 作品概要
- タイトル: {brief.get('title', '無題')}
- ジャンル: {brief.get('genre', '')}
- 目安尺: {brief.get('duration_target', '10分')}
- 方向性: {brief.get('direction_notes', '')}

## 登場人物
{chars_text}

## シーン構成
{scenes_text}

## 出力形式

**必ずJSON形式で出力してください。** CSV形式は使わないでください。

以下のJSON配列形式で出力してください:

```json
[
  {{
    "scene_id": "scene_01",
    "line_id": 1,
    "speaker": "{speakers}",
    "emotion_tags": "自信,威圧",
    "text_raw": "セリフテキスト",
    "emoji_suggestion": ""
  }}
]
```

### 各フィールドの説明

| フィールド | 説明 |
|---|---|
| `scene_id` | シーン区切り（scene_01, scene_02, ...） |
| `line_id` | シーン内の連番（1, 2, 3...） |
| `speaker` | 話者名（{speakers}） |
| `emotion_tags` | 感情タグ（カンマ区切り。下記ガイド参照） |
| `text_raw` | セリフテキスト（絵文字を含めない素のテキスト） |
| `emoji_suggestion` | 絵文字の提案（任意。サンドイッチ形式で前後に配置。下記参照） |

### emoji_suggestion の書き方

音声合成エンジンは**テキストの前後に絵文字を配置する「サンドイッチ方式」**で感情表現を制御します。
感情が強い場面では、前後に多くの絵文字を配置するほど感情表現が豊かになります。

**配置ルール:**
- 弱い感情: `"😤💪 テキスト 😤"` （前2-3個、後1個）
- 中程度: `"🥵😖🫣 テキスト 🫣"` （前2-4個、後0-1個）
- 強い感情: `"🥵😮‍💨💦 テキスト 😭💦"` （前3-5個、後2-3個）
- 極限状態: `"🥵😱😮‍💨💦🫃😭 テキスト 😱💦🥵"` （前5-8個、後2-3個）

**推奨絵文字パターン（場面別）:**

| 場面 | 前方（prefix） | 後方（suffix） |
|---|---|---|
| 低く太い喘ぎ（お゛ほぉ系） | 🥵😮‍💨💦 | 😭 |
| 恥ずかしい喘ぎ（ん゛ほぉ系） | 🫣🥵😰 | 💦 |
| 短く鋭い絶叫（あ゛あっ系） | 😱🥵💦 | 😱💦 |
| 甘く長い喘ぎ（はぁん系） | 🥵🙏💦 | 😌 |
| 懇願（孕ませて系） | 🙏🥵😭 | 💦 |
| 事後・放心 | 🥵😌💦 | 😌 |
| 泣きイキ | 😭🥵💦 | 😱 |
| 耳元囁き | 👂🥵😮‍💨 | 💋 |

`emoji_suggestion` は空欄でもOKです（その場合、emotion_tagsから自動生成します）。


## emotion_tags の使い方ガイド

シーンに応じて以下の感情タグをemotion_tags列に記述してください。
音声合成エンジンがこのタグをもとに声の演技を制御します。

【基本感情】自信, 威圧, 挑発, 動揺, 恐怖, 絶望, 強がり, 驚き, 怒り
【恥じらい系】照れ, 恥じらい, 困惑, もじもじ
【甘え・親密系】甘え, 囁き, からかう, 優しい
【息遣い系】吐息, 喘ぎ, 喘ぎ(弱), 喘ぎ(強), 息切れ, 荒い息遣い
【泣き系】泣き, 嗚咽, 涙声
【極限系】絶頂, 叫び, 悲鳴, 苦しい
【事後系】放心, 脱力, 朦朧, 虚脱, 安堵
【効果音系】舌打ち, 唾を飲む, リップ, あくび

※ 複数の感情を「,」で組み合わせ（例: 「恐怖,強がり」「喘ぎ(弱),困惑」）

### 重要：感情の強度と複数タグの使い方

感情表現が強い状態（喘ぎ、絶頂、叫び、嗚咽など）では、**emotion_tags に複数の感情タグをカンマ区切りで積極的に組み合わせてください**。
タグが多いほど音声合成時の感情表現が豊かになります。

**具体例：**
- 弱い感情状態 → タグ1〜2個: `"困惑"` `"動揺,恐怖"`
- 中程度の感情状態 → タグ2〜3個: `"喘ぎ(弱),困惑,恥じらい"` `"恐怖,強がり,涙声"`
- 強い感情状態 → タグ3〜4個: `"喘ぎ(強),息切れ,荒い息遣い"` `"絶頂,叫び,喘ぎ(強),嗚咽"`
- 極限状態 → タグ4個以上: `"絶頂,叫び,喘ぎ(強),荒い息遣い,嗚咽"`

**特に激しい場面では、1つのemotion_tagsに3個以上のタグを使うことを推奨します。**

## 注意事項
- 総セリフ数は約{total_lines}行を目安にしてください
- **必ずJSON配列形式で出力してください**（CSVではなく）
- text_raw にはセリフのみ記述してください（絵文字は含めない。絵文字はemoji_suggestionに書く）
- 1行に1セリフのみ（地の文・ト書きは不要）
- emotion_tags には上記ガイドの感情タグを使って記述してください
- 難読漢字は避け、ひらがな・カタカナを活用してください
- 句読点は適切に入れてください
- 「…」（三点リーダー）は躊躇や余韻の表現に使ってください
- セリフは自然な話し言葉で書いてください
- 内心の独白は（括弧）で表現してください（例: （これは……瘴気？））
"""

    # grok_prompt.md を保存
    prompt_path = project_dir / "grok_prompt.md"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"[ok] Grok用プロンプトを生成しました: {prompt_path}")
    print(f"  総セリフ目安: {total_lines}行")
    print(f"  シーン数: {len(brief.get('scenes', []))}")
    return str(prompt_path)


def create_brief_template(project_dir: Path) -> str:
    """project_brief.json のテンプレートを作成する"""
    template = {
        "title": "",
        "genre": "",
        "duration_target": "10分",
        "line_count_target": 50,
        "characters": [
            {
                "name": "",
                "age": "",
                "personality": "",
                "speech_style": "",
                "body_features": "",
                "relationship": ""
            }
        ],
        "scenes": [
            {
                "scene_id": "scene_01",
                "title": "",
                "description": "",
                "mood": "",
                "estimated_lines": 15
            },
            {
                "scene_id": "scene_02",
                "title": "",
                "description": "",
                "mood": "",
                "estimated_lines": 25
            }
        ],
        "direction_notes": ""
    }

    brief_path = project_dir / "project_brief.json"
    with open(brief_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"[ok] 企画書テンプレートを作成しました: {brief_path}")
    return str(brief_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python planner.py template <project_name>  -- テンプレート作成")
        print("  python planner.py generate <project_name>  -- Grokプロンプト生成")
        sys.exit(1)

    cmd = sys.argv[1]
    project_name = sys.argv[2]
    project_dir = PROJECTS_DIR / project_name

    if not project_dir.exists():
        print(f"[error] プロジェクトが存在しません: {project_dir}")
        print("先に project_manager.py init で作成してください")
        sys.exit(1)

    if cmd == "template":
        create_brief_template(project_dir)
    elif cmd == "generate":
        generate_grok_prompt(project_dir)
    else:
        print(f"Unknown command: {cmd}")
