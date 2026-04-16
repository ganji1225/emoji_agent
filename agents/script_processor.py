#!/usr/bin/env python3
"""脚本処理エージェント - Grokの生台本（JSON/CSV/TXT）やゲームテキスト(.md)を
絵文字付きproduction.csvに変換する。
サンドイッチ方式: 感情強度に応じて prefix + テキスト + suffix で絵文字を配置
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_DIR = Path("D:/irodori/projects")

# ============================================================
# 感情キーワード → 絵文字マッピング（全タグマッチ方式）
# ============================================================
EMOTION_EMOJI_MAP = [
    # 効果音・息遣い系
    (r"囁き|ささやき|耳元|ひそひそ|ウィスパー", "👂"),
    (r"吐息|溜息|ため息|寝息", "😮\u200d💨"),
    (r"喘ぎ\(強\)|喘ぎ（強）", "🥵"),
    (r"喘ぎ\(弱\)|喘ぎ（弱）", "🥵"),
    (r"喘ぎ|あえぎ|荒い息|うめき", "🥵"),
    (r"息切れ|荒い息遣い|はぁはぁ", "😮\u200d💨"),
    (r"息をのむ|ハッ", "😮"),
    (r"舐め|ぺろ|ちゅぱ|水音", "👅"),
    (r"リップ|キス|唇|ちゅ", "💋"),
    (r"咳|くしゃみ|ゴホ|コホ", "🤧"),
    (r"嚥下|ごくり|飲み込|ぐびっ", "🥤"),
    (r"エコー|リバーブ|響く|こだま", "📢"),
    (r"電話越し|電話口|受話器", "📞"),
    (r"ゆっくり|丁寧に|噛み締め|一語一語", "🐢"),
    (r"早口|まくしたて|一気に|矢継ぎ早", "⏩"),
    # 感情・話し方系
    (r"笑い|くすくす|ふふ|クスッ|含み笑", "🤭"),
    (r"甘え", "😏"),
    (r"からかう|からかい|いたずら|小悪魔", "😏"),
    (r"恥ずかし|照れ|もじもじ|テレ|恥じらい", "🫣"),
    (r"震え|おどおど|自信な", "🥺"),
    (r"泣き|泣く|嗚咽|涙声", "😭"),
    (r"悲鳴|叫び|絶叫|キャー", "😱"),
    (r"怒り|怒る|不満|イライラ|拗ね", "😠"),
    (r"驚き|びっくり|えっ", "😲"),
    (r"優し|穏やか|慈しみ", "🫶"),
    (r"眠い|だるい|まどろみ|寝起き", "😪"),
    (r"慌て|パニック|どもり|焦", "😰"),
    (r"喜び|嬉し|楽し|ウキウキ", "😆"),
    (r"懇願|お願い|頼む", "🙏"),
    (r"酔|ほろ酔い", "🥴"),
    (r"口を塞|くぐもっ", "🤐"),
    (r"安堵|ほっ|満足|安心", "😌"),
    (r"疑問|不思議|首かしげ", "🤔"),
    (r"苦し|痛|うぅ", "😖"),
    (r"心配|不安そう", "😟"),
    (r"呆れ|やれやれ", "🙄"),
    (r"放心|虚脱|朦朧|脱力", "😌"),
    (r"拒絶|拒否", "😱"),
    (r"屈辱|崩壊", "😭"),
    (r"絶望", "😭"),
    (r"絶頂", "😱"),
    (r"動揺", "😰"),
    (r"恐怖", "😱"),
    (r"強がり", "😤"),
    (r"自信|威圧|挑発", "😤"),
    (r"抵抗", "😖"),
    (r"困惑", "😖"),
    # エフェクト
    (r"💦|汗|濡", "💦"),
    # 広い感情（最後）
    (r"明るい|元気|ハキハキ", "😊"),
    (r"日常|普通|通常|ナレーション", ""),
]

# ============================================================
# 感情強度の判定キーワード
# ============================================================
INTENSITY_STRONG = {
    "喘ぎ(強)", "喘ぎ（強）", "絶頂", "叫び", "嗚咽", "荒い息遣い",
    "崩壊", "絶叫", "連続絶頂",
}
INTENSITY_MEDIUM = {
    "喘ぎ(弱)", "喘ぎ（弱）", "恥じらい", "困惑", "動揺", "恐怖",
    "抵抗", "拒絶", "屈辱", "絶望",
}
INTENSITY_EXTREME = {
    "出産", "全穴同時", "連続絶頂", "妊娠",
}


def classify_intensity(emotion_tags: list[str]) -> str:
    """感情タグリストから強度レベルを判定する"""
    tag_set = set(emotion_tags)
    if tag_set & INTENSITY_EXTREME:
        return "extreme"
    # 強いタグが2個以上 or 強いタグ + 中タグ = strong
    strong_count = len(tag_set & INTENSITY_STRONG)
    medium_count = len(tag_set & INTENSITY_MEDIUM)
    if strong_count >= 2:
        return "strong"
    if strong_count >= 1 and medium_count >= 1:
        return "strong"
    if strong_count >= 1:
        return "medium"
    if medium_count >= 1:
        return "medium"
    return "weak"


def emotion_to_emojis_all(emotion: str) -> list[str]:
    """感情テキストから全マッチする絵文字をリストで返す（重複排除）"""
    if not emotion:
        return []
    emojis = []
    seen = set()
    # スペースまたはカンマで分割して各タグを処理
    tags = re.split(r"[,、\s]+", emotion.strip())
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue
        for pattern, emoji in EMOTION_EMOJI_MAP:
            if re.search(pattern, tag):
                if emoji and emoji not in seen:
                    emojis.append(emoji)
                    seen.add(emoji)
                break
    return emojis


def build_sandwich(text: str, emojis: list[str], intensity: str, stacking: bool = False) -> str:
    """テスト結果に基づいたサンドイッチ方式で絵文字を配置する

    聴き比べテスト結果（2026-04-13 + 2026-04-15）:
      弱: prefix 2, suffix 1 が最適
      中: prefix 2-3, suffix 1 が安定
      強: prefix 3, suffix 2 が最適（4個以上はノイズ増）
      極限: prefix 3, suffix 2（意図的にノイズを入れたい場合のみ4個）

    重要な発見（2026-04-15 聴き比べ）:
      - 絵文字2-3個が感情幅が大きく安定
      - 4個以上は不自然な音声やノイズが増加
      - 絵文字数が多いと吐息・声にならない音声が増える

    スタッキングテクニック（公式EMOJI_ANNOTATIONS.md 2026-03-24確認）:
      stacking=True の場合、絵文字を2回重ねて効果を強調する
      例: 👂 → 👂👂 でより強い囁き効果
      ※ 総数3個以内のルールを維持するため prefix を倍加する
    """
    if not emojis:
        return text

    # スタッキングテクニック: 絵文字1個の場合に2回重ねて効果強調
    # 例: [👂] → prefix="👂👂", suffix="" (総数2個でルール内)
    if stacking and len(emojis) == 1:
        prefix = emojis[0] * 2
        suffix = ""
        result = f"{prefix} {text}"
        return result

    if intensity == "weak":
        # prefix 2, suffix 1
        prefix = "".join(emojis[:2])
        suffix = emojis[-1] if len(emojis) >= 2 else ""
    elif intensity == "medium":
        # prefix 2-3, suffix 1
        prefix = "".join(emojis[:3])
        suffix = emojis[-1] if len(emojis) >= 2 else ""
    elif intensity == "strong":
        # prefix 3, suffix 2（上限厳守）
        prefix = "".join(emojis[:3])
        suffix_emojis = emojis[-2:] if len(emojis) >= 2 else emojis[-1:]
        suffix = "".join(suffix_emojis)
        if "💦" not in suffix:
            suffix += "💦"
    else:  # extreme
        # prefix 3, suffix 2 + 💦
        prefix = "".join(emojis[:3])
        suffix_emojis = emojis[-2:] if len(emojis) >= 2 else emojis
        suffix = "".join(suffix_emojis) + "💦"

    result = f"{prefix} {text}"
    if suffix:
        result += f" {suffix}"
    return result


def normalize_text(text: str) -> str:
    """テキストを正規化する（TTS向け）"""
    text = text.strip()
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"。{2,}", "。", text)
    text = text.strip("「」『』\"")
    # Grokが埋め込んだ絵文字を除去（text_rawはクリーンに保つ）
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U00002702-\U000027B0"  # dingbats
        "\U0000FE00-\U0000FE0F"  # variation selectors
        "\U0000200D"             # zero width joiner
        "\U00002640-\U00002642"  # gender symbols
        "\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text).strip()
    # 漢字読み間違い対策: TTS が誤読しやすい単語をひらがな/カタカナに変換
    text = _fix_kanji_reading(text)
    return text


# TTS誤読しやすい漢字 → ひらがな/カタカナ変換テーブル
# 参考: https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku
KANJI_FIX_MAP = [
    (r"今日", "きょう"),
    (r"昨日", "きのう"),
    (r"明日", "あした"),
    (r"一人", "ひとり"),
    (r"二人", "ふたり"),
    (r"大人", "おとな"),
    (r"上手", "じょうず"),
    (r"下手", "へた"),
    (r"雑魚", "ザコ"),
    (r"瘴気", "しょうき"),
    (r"霊山", "れいざん"),
    (r"番人", "ばんにん"),
    (r"蟲", "むし"),
    (r"贄", "にえ"),
    (r"苗床", "なえどこ"),
    (r"孵化", "ふか"),
    (r"蔓", "つる"),
    (r"繭", "まゆ"),
    (r"媚薬", "びやく"),
    (r"蜘蛛", "くも"),
]


def _fix_kanji_reading(text: str) -> str:
    """TTS が誤読しやすい漢字をひらがな/カタカナに変換する"""
    for kanji, reading in KANJI_FIX_MAP:
        text = text.replace(kanji, reading)
    return text


# ============================================================
# 間（ま）の自動挿入
# ============================================================
def insert_pause_markers(text: str) -> str:
    """句読点や「……」の位置に ⏸️（間）マーカーを挿入する

    参考: Irodori-TTS では以下の絵文字が特殊効果として機能する（公式EMOJI_ANNOTATIONS確認済み）
      ⏸️ = 間・沈黙（感情の変わり目の直前に挿入）
      ⏩ = 早口・まくしたてる（慌て・興奮シーンに）
      🐢 = ゆっくり・丁寧に（噛み締めるような語りかけに）
    """
    # 「……」の後に間を挿入（ただし末尾は除く）
    text = re.sub(r"……(?!$)(?!）)", "…… ⏸️ ", text)
    return text


# ============================================================
# テキスト内容から感情を自動推定する
# ============================================================
EMOTION_INFERENCE_RULES = [
    # 極限系（優先）
    (r"ん゛ほ゛|お゛ほ゛|は゛ん゛|ぐ゛お゛|あ゛ひ゛|ん゛お゛", "喘ぎ(強),絶頂,荒い息遣い"),
    (r"あ゛あ゛|は゛あ゛|あ゛お゛", "喘ぎ(強),叫び,嗚咽"),
    (r"イキ狂|壊れた|壊して|溶ける|溶けちゃ|ぶっ壊", "絶頂,叫び,喘ぎ(強),崩壊"),
    (r"イッちゃう|イっちゃ|イキそう|イク", "絶頂,叫び,喘ぎ(強)"),
    (r"孕ませて|孕みたい|産ませて|産みたい", "絶頂,嗚咽,懇願"),
    # 強い系
    (r"んあぁ|んおぉ|あぁぁ|おぉお", "喘ぎ(強),絶頂"),
    (r"気持ちいい.*止まら|快楽.*溺れ|快楽.*最高", "喘ぎ(強),絶頂,虚脱"),
    (r"子宮.*疼|子宮.*痙攣|子宮.*締ま", "喘ぎ(強),恥じらい"),
    (r"おまんこ.*ヒクヒク|おまんこ.*びくびく", "喘ぎ(弱),恥じらい"),
    (r"母乳.*噴|母乳.*搾|乳首.*吸", "喘ぎ(強),恥じらい"),
    (r"卵.*パンパン|お腹.*膨|お腹.*パンパン", "絶頂,喘ぎ(強),嗚咽"),
    # 中程度
    (r"はぁ.*はぁ|はぁん", "喘ぎ(弱),荒い息遣い"),
    (r"んっ.*はぁ|あんっ", "喘ぎ(弱),恥じらい"),
    (r"気持ちいい|気持ち悪い.*気持ちい", "喘ぎ(弱),困惑"),
    (r"嫌なのに.*気持ち|嫌.*でも", "困惑,恥じらい"),
    (r"恥ずかし|恥ずかし", "恥じらい"),
    (r"熱い.*体|体.*熱い|熱くて", "喘ぎ(弱),困惑"),
    (r"愛液|濡れ|ぐちょ|ぬるぬる|ぬめ", "喘ぎ(弱),恥じらい"),
    (r"もっと.*欲し|もっと.*して|もっと.*犯", "喘ぎ(強),甘え,懇願"),
    (r"誇り.*いらない|誇り.*どうでも|番人.*もう", "絶望,虚脱"),
    (r"戻りたくない|戻れない|人間じゃ", "虚脱,放心"),
    # 弱い系
    (r"やめて|離して|離れなさい|放して", "恐怖,拒絶"),
    (r"しまった|まずい", "驚き,恐怖"),
    (r"怖い|恐ろし", "恐怖"),
    (r"嫌.*やだ|やだ", "恐怖,拒絶"),
    (r"力が.*入らない|動けない|動かない|抵抗できない", "絶望,恐怖"),
    (r"もう.*だめ|もう.*限界", "絶望,喘ぎ(弱)"),
    (r"まだ.*負け|まだ.*戦える|抵抗.*する", "強がり"),
    # 事後系
    (r"永遠に.*犯され|永遠に.*溺れ|ずっと.*快楽", "放心,虚脱,甘え"),
    (r"もう.*いいかな|もう.*いいかも", "放心,虚脱"),
    (r"壊れた笑み|虚ろな目", "放心,虚脱"),
    # 身体反応系（弱〜中の補完）
    (r"おまんこ|まんこ|子宮|クリ", "喘ぎ(弱),恥じらい"),
    (r"乳首|母乳|乳|胸.*吸", "喘ぎ(弱),恥じらい"),
    (r"粘液|ぬめ|ぬる|べちゃ", "困惑,恥じらい"),
    (r"媚薬|媚毒|甘い.*液|分泌液", "困惑,喘ぎ(弱)"),
    (r"快楽|気持ちいい|気持ちよ", "喘ぎ(弱),困惑"),
    (r"疼|うず|ヒクヒク|びくびく|痙攣", "喘ぎ(弱),恥じらい"),
    (r"濡れ|愛液|ぐちょ|じゅわ", "喘ぎ(弱),恥じらい"),
    (r"触手|蔓|幼虫|蝿|卵", "恐怖,困惑"),
    (r"這い|絡み|巻き|吸い付|包み込", "恐怖,困惑"),
    (r"飲まされ|注ぎ込|流し込", "恐怖,困惑"),
    (r"お尻|アナル|尻穴", "恥じらい,困惑"),
    (r"苗床|繁殖|肉袋|器.*なる", "絶望,虚脱"),
    (r"膨ら|パンパン|いっぱい", "喘ぎ(強),恥じらい"),
    (r"出口.*見え|あと少し|もう少し", "焦り,強がり"),
    (r"嫌|やだ|こんなの", "恐怖,拒絶"),
    (r"……っ|くっ|あっ", "驚き,動揺"),
    # フォールバック
    (r"……", "動揺"),
]


def infer_emotion_from_text(text: str) -> str:
    """テキスト内容から感情タグを自動推定する"""
    for pattern, emotion in EMOTION_INFERENCE_RULES:
        if re.search(pattern, text):
            return emotion
    return "日常"


def load_game_text(filepath: Path) -> list[dict]:
    """ゲームテキスト（.md）を解析してセリフを抽出する

    対象行:
      - （括弧の独白）→ 採用
      - 「発話セリフ」→ 採用（括弧を除去）
    除外行:
      - # セクションヘッダ → scene_id として利用
      - 【演出指示】【CG】→ 除外
      - ★パラメータ → 除外
      - ——END—— → 除外
      - --- → 除外
      - ナレーション（地の文）→ 除外
      - 空行 → 除外
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    rows = []
    current_scene = "scene_01"
    scene_count = 0

    for line in lines:
        l = line.strip()
        if not l:
            continue

        # セクションヘッダ → scene_id 更新
        section_match = re.match(r'^#{1,3}\s+(.+)$', l)
        if section_match:
            section_name = section_match.group(1)
            # scene_id を生成（S1-mid → s1_mid, S2-ev1 → s2_ev1 etc.）
            sid = re.search(r'(S\d+[-_]\w+)', section_name)
            if sid:
                scene_count += 1
                current_scene = sid.group(1).lower().replace('-', '_')
            elif re.search(r'Stage\s*\d', section_name):
                # Stage ヘッダはスキップ（子セクションで scene_id を設定）
                pass
            continue

        # 除外行
        if l.startswith('【') or l.startswith('★') or l.startswith('——') or l == '---':
            continue

        # 独白: （...）
        monologue_match = re.match(r'^（(.+)）$', l)
        if monologue_match:
            text = monologue_match.group(1)
            # 長い行は分割（60文字超）
            sub_lines = _split_long_text(text, max_len=55)
            for sub in sub_lines:
                emotion = infer_emotion_from_text(sub)
                rows.append({
                    "scene_id": current_scene,
                    "speaker": "白雨",
                    "emotion_tags": emotion,
                    "text_raw": f"（{sub}）",
                    "line_type": "独白",
                })
            continue

        # 発話: 「...」
        speech_match = re.match(r'^「(.+?)」?$', l)
        if speech_match:
            text = speech_match.group(1)
            sub_lines = _split_long_text(text, max_len=55)
            for sub in sub_lines:
                emotion = infer_emotion_from_text(sub)
                rows.append({
                    "scene_id": current_scene,
                    "speaker": "白雨",
                    "emotion_tags": emotion,
                    "text_raw": sub,
                    "line_type": "発話",
                })
            continue

        # それ以外はナレーション → スキップ

    return rows


def _split_long_text(text: str, max_len: int = 55) -> list[str]:
    """長いテキストを適切な位置で分割する"""
    if len(text) <= max_len:
        return [text]

    result = []
    # 「……」で分割を試みる
    parts = re.split(r'(……)', text)
    current = ""
    for i, part in enumerate(parts):
        if part == "……":
            current += part
            # 次のパートと合わせて長すぎるなら、ここで切る
            remaining = "".join(parts[i+1:]) if i+1 < len(parts) else ""
            if len(current) >= max_len * 0.4 and remaining:
                result.append(current.strip())
                current = ""
        else:
            if len(current + part) > max_len and current:
                result.append(current.strip())
                current = part
            else:
                current += part

    if current.strip():
        result.append(current.strip())

    # 分割できなかった場合はそのまま返す
    return result if result else [text]


def load_json(filepath: Path) -> list[dict]:
    """JSON形式の台本を読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "lines" in data:
        return data["lines"]
    return []


def load_csv(filepath: Path) -> list[dict]:
    """CSV形式の台本を読み込む"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_txt(filepath: Path) -> list[dict]:
    """プレーンテキスト形式を読み込む（空行でシーン区切り）"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    rows = []
    scene_num = 1
    for line in lines:
        line = line.strip()
        if not line:
            scene_num += 1
            continue
        rows.append({
            "scene_id": f"scene_{scene_num:02d}",
            "speaker": "キャラ",
            "emotion_note": "日常",
            "text_raw": line,
        })
    return rows


def process_script(project_name: str, ignore_grok_emoji: bool = False,
                    use_pause_markers: bool = True) -> str:
    """台本ファイルを読み込んで production.csv を生成する

    対応形式（優先順）:
      1. script_raw.json  (推奨: Grok JSON出力)
      2. script_raw.csv
      3. script_raw.txt

    Args:
        project_name: プロジェクト名
        ignore_grok_emoji: True の場合、Grok の emoji_suggestion を無視し
            パイプラインの build_sandwich() で絵文字を再構築する。
            改善されたパイプライン（絵文字2-3個制限、スタッキング等）を
            Grok版データに適用する際に使用。
        use_pause_markers: True の場合、「……」位置に ⏸️ を自動挿入する
    """
    project_dir = PROJECTS_DIR / project_name
    prod_csv = project_dir / "production.csv"

    raw_json = project_dir / "script_raw.json"
    raw_csv = project_dir / "script_raw.csv"
    raw_txt = project_dir / "script_raw.txt"

    # 読み込み
    rows = []
    if raw_json.exists():
        rows = load_json(raw_json)
        print(f"[ok] script_raw.json を読み込みました ({len(rows)}行)")
    elif raw_csv.exists():
        rows = load_csv(raw_csv)
        print(f"[ok] script_raw.csv を読み込みました ({len(rows)}行)")
    elif raw_txt.exists():
        rows = load_txt(raw_txt)
        print(f"[ok] script_raw.txt を読み込みました ({len(rows)}行)")
    else:
        print(f"[error] 台本ファイルが見つかりません: {project_dir}")
        print(f"  対応形式: script_raw.json / script_raw.csv / script_raw.txt")
        return ""

    if not rows:
        print("[error] 台本が空です")
        return ""

    # production.csv に変換
    prod_rows = []
    scene_line_counts = {}
    stats = {"weak": 0, "medium": 0, "strong": 0, "extreme": 0}

    for row in rows:
        scene_id = row.get("scene_id", "scene_01").strip()
        scene_line_counts[scene_id] = scene_line_counts.get(scene_id, 0) + 1
        line_num = scene_line_counts[scene_id]

        # テキスト取得（JSON: text_raw, CSV: text / text_raw）
        text_raw_orig = row.get("text_raw", row.get("text", ""))
        text_raw = normalize_text(text_raw_orig)

        # 感情タグ取得（JSON: emotion_tags / emotion_note, CSV: emotion / emotion_note）
        emotion = row.get("emotion_tags",
                  row.get("emotion_note",
                  row.get("emotion", "")))

        # Grokの絵文字提案があればマージ用に保持
        grok_emoji = row.get("emoji_suggestion", "")

        # 感情タグをパース
        tags = [t.strip() for t in re.split(r"[,、\s]+", emotion.strip()) if t.strip()]

        # 強度判定
        intensity = classify_intensity(tags)
        stats[intensity] += 1

        # 絵文字変換
        emojis = emotion_to_emojis_all(emotion)

        # ⏸️ 間マーカーの自動挿入
        if use_pause_markers:
            text_raw = insert_pause_markers(text_raw)

        # 絵文字サンドイッチ構築
        if grok_emoji and not ignore_grok_emoji:
            # Grok絵文字提案をそのまま使用（emoji_suggestionは既にサンドイッチ済み）
            text_with_emoji = grok_emoji
        else:
            # パイプラインで再構築（改善版: 絵文字2-3個制限、スタッキング等）
            text_with_emoji = build_sandwich(text_raw, emojis, intensity)

        prod_rows.append({
            "scene_id": scene_id,
            "line_id": f"line_{line_num:03d}",
            "speaker": row.get("speaker", "").strip(),
            "emotion_note": emotion,
            "text_raw": text_raw,
            "text_with_emoji": text_with_emoji,
            "caption": "",
            "cfg_text": "",
            "cfg_caption": "",
            "cfg_speaker": "",
            "num_steps": "",
            "num_candidates": "3",
            "seed": "",
            "status": "pending",
            "approved_candidate": "",
            "notes": f"intensity={intensity}",
        })

    # 書き出し
    fieldnames = list(prod_rows[0].keys())
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)

    # プレーンテキストも出力（人間確認用）
    txt_path = project_dir / "script_with_emoji.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        current_scene = ""
        for row in prod_rows:
            if row["scene_id"] != current_scene:
                current_scene = row["scene_id"]
                f.write(f"\n=== {current_scene} ===\n")
            intensity_mark = row["notes"].replace("intensity=", "")
            f.write(f"[{intensity_mark}][{row['emotion_note']}] {row['text_with_emoji']}\n")

    print(f"\n[ok] production.csv を生成しました ({len(prod_rows)}行)")
    print(f"[ok] script_with_emoji.txt を生成しました（確認用）")

    # サマリー
    scenes = sorted(set(r["scene_id"] for r in prod_rows))
    print(f"\n  シーン数: {len(scenes)}")
    for s in scenes:
        count = sum(1 for r in prod_rows if r["scene_id"] == s)
        print(f"    {s}: {count}行")

    print(f"\n  強度分布:")
    print(f"    弱 (B_sandwich):     {stats['weak']}行")
    print(f"    中 (B/C方式):        {stats['medium']}行")
    print(f"    強 (D_sandwich_多):  {stats['strong']}行")
    print(f"    極限 (D最大盛り):    {stats['extreme']}行")

    return str(prod_csv)


def process_game_text(project_name: str, game_text_paths: list[str]) -> str:
    """ゲームテキスト(.md)を解析して production.csv を生成する

    Args:
        project_name: プロジェクト名
        game_text_paths: ゲームテキストファイルのパスリスト
    """
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    prod_csv = project_dir / "production.csv"

    all_rows = []
    for path_str in game_text_paths:
        filepath = Path(path_str)
        if not filepath.exists():
            print(f"[error] ファイルが見つかりません: {filepath}")
            continue
        rows = load_game_text(filepath)
        source_name = filepath.stem
        # rows に source 情報を追加
        for r in rows:
            r["source"] = source_name
        all_rows.extend(rows)
        print(f"[ok] {filepath.name} → {len(rows)}行抽出（独白: {sum(1 for r in rows if r.get('line_type')=='独白')}, 発話: {sum(1 for r in rows if r.get('line_type')=='発話')}）")

    if not all_rows:
        print("[error] 音声化対象の行がありません")
        return ""

    # production.csv に変換
    prod_rows = []
    scene_line_counts = {}
    stats = {"weak": 0, "medium": 0, "strong": 0, "extreme": 0}

    for row in all_rows:
        scene_id = row.get("scene_id", "scene_01")
        scene_line_counts[scene_id] = scene_line_counts.get(scene_id, 0) + 1
        line_num = scene_line_counts[scene_id]

        text_raw = row.get("text_raw", "")
        emotion = row.get("emotion_tags", "")

        tags = [t.strip() for t in re.split(r"[,、\s]+", emotion.strip()) if t.strip()]
        intensity = classify_intensity(tags)
        stats[intensity] += 1

        emojis = emotion_to_emojis_all(emotion)
        text_with_emoji = build_sandwich(text_raw, emojis, intensity)

        prod_rows.append({
            "scene_id": scene_id,
            "line_id": f"line_{line_num:03d}",
            "speaker": row.get("speaker", "白雨"),
            "emotion_note": emotion,
            "text_raw": text_raw,
            "text_with_emoji": text_with_emoji,
            "caption": "",
            "cfg_text": "",
            "cfg_caption": "",
            "cfg_speaker": "",
            "num_steps": "",
            "num_candidates": "3",
            "seed": "",
            "status": "pending",
            "approved_candidate": "",
            "notes": f"intensity={intensity},type={row.get('line_type', '')},src={row.get('source', '')}",
        })

    # 書き出し
    fieldnames = list(prod_rows[0].keys())
    with open(prod_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)

    # プレーンテキスト出力
    txt_path = project_dir / "script_with_emoji.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        current_scene = ""
        for row in prod_rows:
            if row["scene_id"] != current_scene:
                current_scene = row["scene_id"]
                f.write(f"\n=== {current_scene} ===\n")
            notes = row["notes"]
            intensity_mark = ""
            if "intensity=" in notes:
                intensity_mark = notes.split("intensity=")[1].split(",")[0]
            f.write(f"[{intensity_mark}][{row['emotion_note']}] {row['text_with_emoji']}\n")

    print(f"\n[ok] production.csv を生成しました ({len(prod_rows)}行)")
    print(f"[ok] script_with_emoji.txt を生成しました（確認用）")

    # サマリー
    scenes = sorted(set(r["scene_id"] for r in prod_rows))
    print(f"\n  シーン数: {len(scenes)}")
    for s in scenes:
        count = sum(1 for r in prod_rows if r["scene_id"] == s)
        print(f"    {s}: {count}行")

    print(f"\n  強度分布:")
    print(f"    弱 (B_sandwich):     {stats['weak']}行")
    print(f"    中 (B/C方式):        {stats['medium']}行")
    print(f"    強 (D_sandwich_多):  {stats['strong']}行")
    print(f"    極限 (D最大盛り):    {stats['extreme']}行")

    return str(prod_csv)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python script_processor.py <project_name> [--ignore-grok-emoji] [--no-pause]")
        print("    台本形式: script_raw.json (推奨) / script_raw.csv / script_raw.txt")
        print("    --ignore-grok-emoji: Grokのemoji_suggestionを無視しパイプラインで再構築")
        print("    --no-pause: ⏸️間マーカーの自動挿入を無効化")
        print()
        print("  python script_processor.py --game <project_name> <file1.md> [file2.md ...]")
        print("    ゲームテキスト解析モード: .md ファイルから独白・発話を抽出")
        sys.exit(1)

    if sys.argv[1] == "--game":
        if len(sys.argv) < 4:
            print("Usage: python script_processor.py --game <project_name> <file1.md> [file2.md ...]")
            sys.exit(1)
        project_name = sys.argv[2]
        game_files = sys.argv[3:]
        process_game_text(project_name, game_files)
    else:
        project_name = sys.argv[1]
        ignore_grok = "--ignore-grok-emoji" in sys.argv
        use_pause = "--no-pause" not in sys.argv
        process_script(project_name, ignore_grok_emoji=ignore_grok,
                       use_pause_markers=use_pause)
