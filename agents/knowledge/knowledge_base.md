# TTS Production Knowledge Base
_Auto-updated: 2026-05-30 | Total findings: 148 | Sources: 38 articles_


## Caption Design (キャプション設計)

### VoiceDesign版では参照音声なしで、声の説明文（例：『落ち着いた女性の声で、やわらかく自然に』）を入力することで声質・感情・話し方を指定可能。描写的なキャプションで話者性を制御。
- Source: [【ローカルAI音声革命】Irodori-TTSがかなりヤバい。日本語音声生成は"絵文字で感情を操る時代"へ](https://note.com/fuma_ai_lab/n/nef8cb249ccdf)
- Date: 2026-05-05
- Params: examples=落ち着いた女性の声で自然に / 低めの男性が疲れた優しい雰囲気 / 若い女性が困惑しながら小さな声で
- Confidence: high

### 音声指示テキストに明るく元気に・落ち着いた声でなど演技指示を記述。英語指示の方が安定する傾向
- Source: [日本語最強クラスの音声生成「Irodori-TTS」絵文字で感情まで操れる神ツール](https://note.com/aaafrog/n/n2021733405ad)
- Date: 2026-04-06
- Params: stability=英語指示がより安定
- Confidence: high

### 全角「？」使用時にmio-tts-cppで不自然な音声生成が発生。半角「?」への変換で改善確認
- Source: [ローカルで動かせる日本語TTSをいろいろ試す（その３）](https://zenn.dev/megyo9/articles/548448f7c8fc83)
- Date: 2026-03-22
- Params: system=mio-tts-cpp, problematic_character=fullwidth_question_mark, solution=halfwidth_conversion
- Confidence: high

### 漢字読み方の精度向上のため、ひらがな入力を推奨。確実な発音制御が必要な箇所では特に有効。
- Source: [「声をテキストで作る時代」が来た——Irodori-TTS（彩りTTS）がヤバすぎる件](https://note.com/gensnotes/n/na48b222358c4)
- Date: 2026-04-17
- Params: input_format=hiragana, use_case=accurate_pronunciation
- Confidence: high

### テキストのみで声色を指定可能。例：「落ち着いた30代女性の声で、低めに、囁く雰囲気」で音声生成。参照音声不要。
- Source: [「声をテキストで作る時代」が来た——Irodori-TTS（彩りTTS）がヤバすぎる件](https://note.com/gensnotes/n/na48b222358c4)
- Date: 2026-04-17
- Params: age=30, gender=female, tone=whisper
- Confidence: high

### VoiceDesignでは『落ち着いた女性の声で、近い距離感でやわらかく自然に読み上げてください』のような自然文キャプションでスタイルを直接指定でき、参照音声不要。
- Source: [Irodori-TTS v3とv2 VoiceDesignを試す](https://zenn.dev/kun432/scraps/b83b0406b067bb)
- Date: 2026-05-17
- Confidence: high

### 三点リーダーは文脈の雰囲気を保持するが、絵文字は台詞化する傾向。効果は文脈依存的
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: context_sensitivity=high
- Confidence: medium

### VoiceDesignのキャプションは音響指定だけでなく『一生懸命』『ドジっ子っぽく』『時々慌てる』といった行動・性格描写を含めると、無個性な声から個性的な声に大きく変化する。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Confidence: high

### 1文に『声の高さ』『年齢感』『話し方』『感情』のうち最低3要素を盛り込む。長さは1-2文がベスト。『幼い』と『若い』では声の印象が大きく異なるため語彙選択も重要。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Params: min_elements=3, ideal_sentences=1-2
- Confidence: high

### 確定キャプション例『少し高めの声の少女が、一生懸命だけど少しドジっ子っぽく話している。穏やかだけど時々慌てる』+ seed値1234で再現可能なキャラ声が確立した。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Params: seed=1234
- Confidence: high

### 重要なテキストはひらがな/カタカナで記述することでAIの漢字読み間違いを回避できる。安定生成のために事前変換しておく。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Confidence: high

### 難しい漢字はひらがなに変換してから入力すると安定する
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: input_preprocessing=kanji_to_hiragana_conversion
- Confidence: high

### Voice Designで声の高さや話し方を記述可能。感情指示は効果が限定的なため、読み上げ文章側のプロンプト（絵文字）で対応するのが現実的
- Source: [【彩】Irodori-TTS 解説](https://note.com/417__/n/n7c25cf9a04c2)
- Date: 2026-05-08
- Confidence: medium

### VoiceDesign版で自然言語による声指定が可能。『明るい女性の声』のような言語表現で声質をテキスト記述制御。参照音声なしでの声質指定に対応。
- Source: [Irodori-TTS の考察｜日本語特化ローカル AI 音声合成](https://hatohato.jp/blog/core/single.php?id=1032)
- Date: 2026-05-04
- Params: method=自然言語記述, example=明るい女性の声
- Confidence: high

### VoiceDesignモデル(irodori-tts-500m-v2-voicedesign)ではCaption/Style Promptフィールドで年齢・性別・感情などのメタデータを組み込み、より精密な音声生成が実現される。
- Source: [【TTS】Irodori-TTS-v2の簡単な使い方など](https://local-llm.memo.wiki/d/%A1%DATTS%A1%DBIrodori-TTS-v2%A4%CE%B4%CA%C3%B1%A4%CA%BB%C8%A4%A4%CA%FD%A4%CA%A4%C9)
- Date: 2026-04-17
- Params: model=irodori-tts-500m-v2-voicedesign, field=Caption / Style Prompt
- Confidence: high

### VoiceDesign版では『Caption / Style Prompt』欄に声の性別や声質を日本語で説明するプロンプトを入力。例：『高飛車なお嬢様のような、若い女性話者』と指定すると対応するボイスが生成される。
- Source: [日本語音声AI「Irodori-TTS」の導入方法・使い方](https://kurokumasoft.com/2026/04/28/irodori-tts/)
- Date: 2026-04-28
- Params: field_name=Caption / Style Prompt, example_prompt=高飛車なお嬢様のような、若い女性話者
- Confidence: high

### 生理音・音声特性制御: 👂(囁き)、😮‍💨(吐息)、⏸️(沈黙)、🥤(嚥下音)、🤧(咳)など細かい音響要素を個別制御
- Source: [EMOJI_ANNOTATIONS.md - Irodori-TTS-500M-v2 Emoji Control Guide](https://huggingface.co/Aratako/Irodori-TTS-500M-v2/blob/main/EMOJI_ANNOTATIONS.md)
- Params: whisper=👂, breath=😮‍💨, pause=⏸️, swallow=🥤, cough=🤧
- Confidence: high

### キャプションに行動描写（一生懸命・たどたどしい等）を加えると、声質にハリやテンポ変化が生まれる
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### 年齢表現で声質をコントロール: 幼い女の子=高く舌足らず / 少女=中間 / 若い女性=大人っぽく
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### キャプションエンジニアリングで細かいNSFW系音声制御も対応可能
- Source: [絵文字で感情表現ができるIrodori-TTSの使い方](https://note.com/aiaicreate/n/n958873db85eb)
- Date: 2026-03-18
- Confidence: medium


## Emoji Technique (絵文字テクニック)

### 入力テキストに絵文字を直接埋め込むことで発話スタイル・感情表現・音声効果を制御可能。対応絵文字は公式ドキュメント参照。
- Source: [「Irodori-TTS」を試す](https://zenn.dev/kun432/scraps/87d7776909e4d9)
- Date: 2025-03-22
- Params: emoji_control=supported, style_dimensions=emotion_expression, voice_effects, speech_style
- Confidence: high

### v3で確認された絵文字例：😭（泣く）、🤧（病気）、👂（囁き）、😮‍💨（息遣い）。複合絵文字（ZWJ含む）も対応
- Source: [Irodori-TTS-500M-v3: 公式モデルカード](https://huggingface.co/Aratako/Irodori-TTS-500M-v3)
- Date: 2026-01-01
- Params: verified_emojis=['😭', '🤧', '👂', '😮\u200d💨']
- Confidence: high

### 絵文字キャプションは音響特徴量抽出後LLM APIで自動生成。38種の絵文字（囁き・笑い・喘ぎ・早口など）で声のスタイルを自然言語アノテーション可能
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: emoji_count=38, supported_apis=['lm_studio', 'groq', 'openai', 'together']
- Confidence: high

### テキストに絵文字を挿入することで感情が音声に反映。😊で楽しげに、😭で泣き声、😠で怒り表現が実現
- Source: [日本語最強クラスの音声生成「Irodori-TTS」絵文字で感情まで操れる神ツール](https://note.com/aaafrog/n/n2021733405ad)
- Date: 2026-04-06
- Params: emoji_meaning=😊=楽しげ、😭=嗚咽・悲しみ、😠=怒り・不満
- Confidence: high

### Irodori-TTSは絵文字で感情を表現できるが、複数の絵文字連続（👂😮‍💨👂😮‍💨）による囁き声指定は困難
- Source: [ローカルで動かせる日本語TTSをいろいろ試す（その３）](https://zenn.dev/megyo9/articles/548448f7c8fc83)
- Date: 2026-03-22
- Params: system=Irodori-TTS, emotion_marker=emoji, limitation=compound_emoji_sequences
- Confidence: high

### 絵文字を読み上げテキストに挿入することで感情と効果音を制御。例：😊で笑い声、🔥で苛立った感じ。
- Source: [「声をテキストで作る時代」が来た——Irodori-TTS（彩りTTS）がヤバすぎる件](https://note.com/gensnotes/n/na48b222358c4)
- Date: 2026-04-17
- Params: emoji_smile=laugh_effect, emoji_fire=angry_tone
- Confidence: high

### 絵文字には全体効果型（👂で囁き声化）と単体音声型（🤭で含み笑い）の2種類が存在
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: emoji_👂=全体的に囁き声効果, emoji_🤭=単体で笑い声を出力
- Confidence: high

### 複数絵文字（🤭🤭🤭）の使用で複数人会話表現に変換される可能性がある
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: emoji_count=3以上で複数音声化傾向
- Confidence: medium

### 感情変化の『直前』に絵文字を配置すると自然な表現になる。😊嬉しい・😰慌てる・🥺落ち込み・😲驚き・🤔分析・😌安堵・⏸️沈黙・⏩早口の8種を使い分け。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Confidence: high

### Irodori-TTSは絵文字によるスタイル制御（感情・SE等）機能を搭載し、テキストに絵文字を挿入するだけでアニメキャラ風の感情表現が可能
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: supported_features=['emotion_control', 'sound_effects']
- Confidence: high

### 感情表現制御に40種類以上の絵文字をテキスト中に挿入することで、感情ニュアンスを反映させる仕様。日本語ユーザーの絵文字利用習慣を活かしたインターフェース設計。
- Source: [Irodori-TTS の考察｜日本語特化ローカル AI 音声合成](https://hatohato.jp/blog/core/single.php?id=1032)
- Date: 2026-05-04
- Params: emoji_count=40種以上, integration_method=テキスト内埋め込み
- Confidence: high

### テキストに絵文字を含めると、その絵文字に合ったボイスが生成される。例：喜びの感情は✨📦💖🌈😭、恐怖は😱👤💦😨👁️💀などの絵文字を含めることで表現が可能。
- Source: [日本語音声AI「Irodori-TTS」の導入方法・使い方](https://kurokumasoft.com/2026/04/28/irodori-tts/)
- Date: 2026-04-28
- Params: emotion_emoji_set_joy=✨📦💖🌈😭, emotion_emoji_set_fear=😱👤💦😨👁️💀
- Confidence: high

### Irodori-TTSは42種類の絵文字をサポートしており、各絵文字が特定の音声効果や感情表現をトリガーする
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: supported_emojis=42, emoji_repetition_effect=複数使用で効果強調可能
- Confidence: high

### 呼吸・息遣い系制御：👂(囁き)、😮‍💨(吐息)、🌬️(息切れ)、🥱(あくび)で息遣いの質感を変更可能
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: whisper_emoji=👂, breath_emoji=😮‍💨, heavy_breathing_emoji=🌬️, yawn_emoji=🥱
- Confidence: high

### 感情表現制御：😆(喜び)、😠(怒り)、😭(悲しみ)、😱(恐怖)、😊(楽しい)など多様な感情パターンに対応
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: joy_emoji=😆, anger_emoji=😠, sadness_emoji=😭, fear_emoji=😱, cheerful_emoji=😊
- Confidence: high

### 話速制御：⏩(早口)、🐢(ゆっくり)で話速を調整。その他⏸️(沈黙/間)で強調効果を生成
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: fast_speaking_emoji=⏩, slow_speaking_emoji=🐢, pause_emoji=⏸️
- Confidence: high

### 音声加工効果：📢(エコー・リバーブ)、📞(電話越し/スピーカー越し)で音声を空間的に加工可能
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: echo_reverb_emoji=📢, phone_speaker_emoji=📞
- Confidence: high

### 口腔音・咀嚼音：👅(舐める音/咀嚼)、💋(リップノイズ)、🥤(嚥下音)、🤧(咳/鼻すすり)で細かい音声テクスチャーを制御
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: licking_chewing_emoji=👅, lip_smack_emoji=💋, swallow_emoji=🥤, cough_emoji=🤧
- Confidence: high

### Emoji caption feature extracts acoustic features (pitch, energy, speech rate, MFCC delta, ZCR) and calls LLM API to anno
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: emoji_types=38, acoustic_features=['pitch', 'energy', 'speech_rate', 'mfcc_delta', 'zcr']
- Confidence: high

### 33種類の絵文字により音響効果と感情表現を制御。各絵文字が特定の音声特性（囁き、呼吸音、喘ぎ、泣き声など）を生成
- Source: [EMOJI_ANNOTATIONS.md - Irodori-TTS-500M-v2 Emoji Control Guide](https://huggingface.co/Aratako/Irodori-TTS-500M-v2/blob/main/EMOJI_ANNOTATIONS.md)
- Params: emoji_count=33, control_dimensions=['sound_effects', 'speaking_style', 'emotional_expression'], effectiveness=imperfect but learnable
- Confidence: high

### 同じ絵文字を複数回使用することで効果を強調・増幅できる（stackable emoji control）
- Source: [EMOJI_ANNOTATIONS.md - Irodori-TTS-500M-v2 Emoji Control Guide](https://huggingface.co/Aratako/Irodori-TTS-500M-v2/blob/main/EMOJI_ANNOTATIONS.md)
- Params: technique=emoji_repetition, effect=emphasis_amplification
- Confidence: high

### ⏸️=間（沈黙）、⏩=早口として機能。感情の変わり目の直前に絵文字を挿入
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### 👂で囁き・耳元効果、😮‍💨で吐息・溜息・寝息、📢でエコー・リバーブ効果
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: proximity=👂, breathing=😮‍💨, echo=📢
- Confidence: high

### ⏩で早口、🐢でゆっくり話法を制御可能
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: fast=⏩, slow=🐢
- Confidence: high

### 👅で舐める音・咀嚼音、💋でリップノイズ、🤧で咳・くしゃみ、🥤で嚥下音
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: licking=👅, lip=💋, cough=🤧, swallow=🥤
- Confidence: high

### 📞で電話越し音質、🤐で口塞ぎ、😰でどもり効果
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: phone=📞, muffled=🤐, stutter=😰
- Confidence: high

### 同じ絵文字を複数回使用するとその効果が強調される（スタッキングテクニック）
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: technique=emoji_repetition
- Confidence: high

### 📢絵文字でエコーとリバーブを追加可能。音声に空間的な響きを付与して劇的な表現効果を生成
- Source: [Irodori-TTS-500M-v3 絵文字アノテーション完全ガイド](https://huggingface.co/Aratako/Irodori-TTS-500M-v3/blob/main/EMOJI_ANNOTATIONS.md)
- Params: emoji=📢, effect=echo_reverb
- Confidence: high

### 😰絵文字で慌て・緊張・どもりといった心理状態を反映した不安定な音声生成が可能。キャラクター演技の幅を拡げる
- Source: [Irodori-TTS-500M-v3 絵文字アノテーション完全ガイド](https://huggingface.co/Aratako/Irodori-TTS-500M-v3/blob/main/EMOJI_ANNOTATIONS.md)
- Params: emoji=😰
- Confidence: medium

### 😭と😱で泣き声と悲鳴という極限の感情表現を区別可能。ドラマチックな演技シーンで感情の深さを制御
- Source: [Irodori-TTS-500M-v3 絵文字アノテーション完全ガイド](https://huggingface.co/Aratako/Irodori-TTS-500M-v3/blob/main/EMOJI_ANNOTATIONS.md)
- Params: emoji_sob=😭, emoji_scream=😱
- Confidence: high

### 📖絵文字でナレーション・独白・モノローグといった客観的な叙述表現を指定可能。語り手スタイルを分離できる
- Source: [Irodori-TTS-500M-v3 絵文字アノテーション完全ガイド](https://huggingface.co/Aratako/Irodori-TTS-500M-v3/blob/main/EMOJI_ANNOTATIONS.md)
- Params: emoji=📖
- Confidence: high

### テキスト内に絵文字を挿入することで、その絵文字に応じた感情表現が音声に反映される。例：😊で明るく弾む声、😢で悲しみをたたえた震える声に変化する。
- Source: [【無料】声優不要！？神AI「Irodori-TTS」がヤバすぎて草生える件](https://library.libecity.com/articles/01KNFP7SDC3ZW1HRJFASXF81BX)
- Date: 2026-04-06
- Params: emoji_joy=😊, emoji_sad=😢, reference=EMOJI_ANNOTATIONS.md
- Confidence: high

### WebUI上で絵文字を入力することで声の感情表現が変化する実践確認
- Source: [Irodori-TTSを実際に動かしてみた！感情絵文字で声に表情をつける面白さ](https://note.com/sugerpowder/n/n1c182e6f0ea1)
- Date: 2026-04-07
- Confidence: high

### 絵文字による感情表現コントロールが可能。テキスト入力層で効果を制御。
- Source: [絵文字で感情表現ができるIrodori-TTSの使い方](https://note.com/aiaicreate/n/n958873db85eb)
- Date: 2026-03-18
- Confidence: high


## CFG Tuning (CFGチューニング)

### モデル精度をfloat32からbf16に設定することで推論時間を約58%削減（1.786秒→0.733秒）。
- Source: [「Irodori-TTS」を試す](https://zenn.dev/kun432/scraps/87d7776909e4d9)
- Date: 2025-03-22
- Params: model_precision=bf16, codec_precision=bf16, speed_improvement=58%, baseline_time_ms=1786, optimized_time_ms=733
- Confidence: high

### CFGスケール推奨値：テキスト条件3.0、話者条件5.0。独立・結合・交互の3つのガイダンスモードから選択可能。デフォルトステップ数は40で1～120の範囲で調整可
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: cfg_scale_text=3.0, cfg_scale_speaker=5.0, num_steps_default=40, guidance_modes=['independent', 'joint', 'alternating']
- Confidence: high

### Sway Samplingで推論を約5倍高速化（483.6ms→98.8ms）。--num-steps 6 --t-schedule-mode sway --sway-coeff -1.0 を指定。品質低下とのトレードオフあり。
- Source: [Irodori-TTS v3とv2 VoiceDesignを試す](https://zenn.dev/kun432/scraps/b83b0406b067bb)
- Date: 2026-05-17
- Params: num_steps=6, t_schedule_mode=sway, sway_coeff=-1.0
- Confidence: high

### v3は出力長を自動推定するため --seconds 指定が不要に。--duration-scale で倍率調整可能（>1で長く、<1で短く）。v2の固定30秒問題を解決。
- Source: [Irodori-TTS v3とv2 VoiceDesignを試す](https://zenn.dev/kun432/scraps/b83b0406b067bb)
- Date: 2026-05-17
- Params: duration_scale_default=1.0
- Confidence: high

### CFG Scale Textのデフォルト値は3。値を大きくするとテキスト指示への準拠性が強くなるが、不自然になる可能性がある。VoiceDesignではCFG Scale Captionデフォルト値4でスタイル指定の効果を調整。
- Source: [【TTS】Irodori-TTS-v2の簡単な使い方など](https://local-llm.memo.wiki/d/%A1%DATTS%A1%DBIrodori-TTS-v2%A4%CE%B4%CA%C3%B1%A4%CA%BB%C8%A4%A4%CA%FD%A4%CA%A4%C9)
- Date: 2026-04-17
- Params: cfg_scale_text_default=3, cfg_scale_caption_default=4, cfg_scale_speaker_default=5, cfg_guidance_modes=['independent', 'joint', 'alternating']
- Confidence: high

### CFG independent モードがデフォルト推奨。各条件（text/caption/speaker）が独自無条件分岐を持ち最も柔軟だが、バッチサイズ増でVRAM消費増。CFG-activeステップでは通常3倍のNFE。
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: cfg_guidance_mode=independent
- Confidence: high

### CFGスケール公式デフォルト値: text=3.0, caption=3.0, speaker=5.0。発音が弱いときはtextスケールを『わずかに』増加させる。話者類似性が弱いときはspeakerスケールを調整。
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: cfg_scale_text=3.0, cfg_scale_caption=3.0, cfg_scale_speaker=5.0
- Confidence: high

### CFG時間範囲は cfg-min-t=0.5, cfg-max-t=1.0 がデフォルト。拡散プロセスの特定段階のみにガイダンスを適用することで品質と速度のバランスを取る。
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: high

### Sway Sampling推奨設定: t-schedule-mode=sway, sway-coeff=-1.0。ノイズ側に計算スケジュール解像度を割く設計。低ステップ数（6〜10）での品質改善に効く。
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: t_schedule_mode=sway, sway_coeff=-1.0, num_steps_range=6-10
- Confidence: high

### v2-duration-controlで短発話のRTFが大幅改善。推定式 est = len(text)/4.5 + 1.0 を使用するため、同一テキストでも+42%音声長になりRTF算出方式に注意が必要。
- Source: [Irodori-TTS の WaveEx x duration-control を Mac MPS で 4 条件比較](https://zenn.dev/yoshitetsu/articles/6376a9a2204ffb)
- Date: 2026-05-13
- Params: duration_estimate=len(text)/4.5 + 1.0
- Confidence: high

### Independent CFG guidance: cfg-scale-text=3.0, cfg-scale-speaker=5.0 as defaults. Guidance modes: independent, joint, alt
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: cfg_scale_text_default=3.0, cfg_scale_speaker_default=5.0, guidance_modes=['independent', 'joint', 'alternating'], cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: high

### WAV→MP3変換はffmpeg VBR qscale:a 2（約190kbps）が最適
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Params: ffmpeg_qscale=2, approx_bitrate=190kbps
- Confidence: high


## Audio Post-Processing (音声後処理)

### v3でSilentCipherを統合し、生成出力に堅牢な不可視音声透かしを自動適用。責任あるAI利用を推進する仕組み
- Source: [Irodori-TTS-500M-v3: 公式モデルカード](https://huggingface.co/Aratako/Irodori-TTS-500M-v3)
- Date: 2026-01-01
- Params: watermarking_tech=SilentCipher
- Confidence: high

### 改行分割生成は3モード選択可：全文同時生成・改行ごと個別出力・改行ごと無音区間（0.1～3.0秒）挟んで連結
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: silence_duration_range=0.1-3.0秒
- Confidence: high

### 音声前処理ツールはSilero VAD（音声活動検出）で長尺音声分割し、Whisper（tiny～large-v3選択可）で字幕化。自動的にLLMで絵文字アノテーション付与
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: vad_threshold=0.5, whisper_models=['tiny', 'base', 'small', 'medium', 'large-v3']
- Confidence: high

### 日本語の漢字読み精度が同規模TTSより弱く、複雑な漢字はひらがなやカタカナへの事前変換が推奨される。生成後のテイク選別は画像生成AIのように複数生成から最良を選ぶ方式が現実的。
- Source: [【ローカルAI音声革命】Irodori-TTSがかなりヤバい。日本語音声生成は"絵文字で感情を操る時代"へ](https://note.com/fuma_ai_lab/n/nef8cb249ccdf)
- Date: 2026-05-05
- Params: kanji_handling=複雑な漢字は事前にひらがな・カタカナ変換, generation_strategy=複数テイク生成して最良を選別
- Confidence: medium

### DiTとDACVAEを非同時実行するパイプライン設計でメモリを再利用しVRAM占有を最小化。Lite版運用ではこの設計が画像生成AIとの共存可否を決める。
- Source: [1GBのVRAMで動く次世代音声合成 Irodori-TTS-Lite](https://note.com/humble_bobcat51/n/ne4c7a419c97f)
- Date: 2026-05-19
- Confidence: medium

### WaveEx併用は wall-clock 13.3%短縮の効果はあるが、duration-controlではTaylor外挿の誤差が増幅して聴感品質が低下する。安定品質優先ならlinear_30が最良。
- Source: [Irodori-TTS の WaveEx x duration-control を Mac MPS で 4 条件比較](https://zenn.dev/yoshitetsu/articles/6376a9a2204ffb)
- Date: 2026-05-13
- Params: steps=6, nfe=40, speedup_pct=13.3
- Confidence: high

### Irodori-TTS-ServerはOpenAI互換 POST /v1/audio/speech エンドポイント。wav/mp3/flac/opus/aac/pcm の6形式に対応し、長文テキストは自動で分割されて処理される。
- Source: [Irodori-TTS-Serverを試す](https://zenn.dev/kun432/scraps/27a96c1a3d3f7e)
- Date: 2026-05-15
- Params: endpoint=/v1/audio/speech, formats=wav,mp3,flac,opus,aac,pcm
- Confidence: high

### Trailing silence trimming via flattening heuristic enabled by default (trim-tail: True) to clean generated audio.
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: trim_tail=True, method=flattening_heuristic
- Confidence: medium

### テキストファイルを行ごとに読み込み、Gradioで順序的に一括音声生成処理を実行。1行1セリフのtxtファイル形式。
- Source: [Irodori-TTSで音声を一括生成する](https://note.com/aiaicreate/n/n61b29f9810a8)
- Date: 2026-04-16
- Params: input_format=txt (1行1セリフ), output_naming=セリフそのまままたはプレフィックス+連番, ui_component=Gradio file upload + batch processing button
- Confidence: high

### DAC VAEの推論時にウォーターマーク処理をバイパス(model.decoder.alpha=0.0設定)することで、ファインチューニングされたモデルの性能を最大化できる。正規化(-16.0dB)と振幅制御も重要。
- Source: [Semantic-DACVAE-Japanese: Audio VAE for Japanese Speech](https://huggingface.co/Aratako/Semantic-DACVAE-Japanese)
- Params: watermark_alpha=0.0, normalization_db=-16.0
- Confidence: high


## Voice Quality (声質改善)

### ゼロショット音声クローンはリファレンス音声の話者特性をMioTTSより正確に再現。参照音声なしでも使用可能。
- Source: [「Irodori-TTS」を試す](https://zenn.dev/kun432/scraps/87d7776909e4d9)
- Date: 2025-03-22
- Params: ref_wav_required=False, zero_shot_clone=supported, vram_usage_gb=7.7, compared_model=MioTTS
- Confidence: medium

### v3の構成は約500Mパラメータで、テキストエンコーダ・参照潜在エンコーダ・拡散トランスフォーマ・Duration Predictorの4コンポーネント。音声コーデックはSemantic-DACVAE-Japanese-32dim（48kH
- Source: [Irodori-TTS-500M-v3: 公式モデルカード](https://huggingface.co/Aratako/Irodori-TTS-500M-v3)
- Date: 2026-01-01
- Params: total_params=500M, audio_codec=DACVAE-32dim, audio_quality_khz=48
- Confidence: high

### WebUIに5つのプリセット感情（ノーマル・力強く・おとなしく・明るく・ひそやかに）を搭載。テキスト表現力・感情の強さ・話者密着度・表現振幅を手動調整可能
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: presets=['normal', 'powerful', 'subtle', 'bright', 'quiet']
- Confidence: high

### 1実行で最大8候補を同時生成し別ファイルで自動保存。推論品質の比較検証に有効でseed制御で再現性も支援
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: max_candidates=8
- Confidence: high

### スピーカーライブラリ機能：参照WAVをspeakers/{name}/に登録（ref.wav・ref.pt・profile.json）してセッション間で再利用可能な話者プロファイル化
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: storage_path=speakers/{name}/
- Confidence: high

### v2では音声VAEがSemantic-DACVAE-Japanese-32dimに変更され、学習ステップ数が2.5倍に増加。テキスト前処理・データフィルタリング改善で日本語音声生成品質が向上。
- Source: [【ローカルAI音声革命】Irodori-TTSがかなりヤバい。日本語音声生成は"絵文字で感情を操る時代"へ](https://note.com/fuma_ai_lab/n/nef8cb249ccdf)
- Date: 2026-05-05
- Params: model_size=500M parameters, vae_architecture=Semantic-DACVAE-Japanese-32dim, training_steps_improvement=2.5x
- Confidence: high

### 複数回生成で当たり音声を引ける実用レベルの品質を実現。ガチャ要素あり。
- Source: [日本語最強クラスの音声生成「Irodori-TTS」絵文字で感情まで操れる神ツール](https://note.com/aaafrog/n/n2021733405ad)
- Date: 2026-04-06
- Params: consistency=ガチャ要素あり（試行必要）
- Confidence: high

### mio-tts-cppは感情表現の自動品質が高く生成速度も優秀だが、感情指定オプションなし
- Source: [ローカルで動かせる日本語TTSをいろいろ試す（その３）](https://zenn.dev/megyo9/articles/548448f7c8fc83)
- Date: 2026-03-22
- Params: system=mio-tts-cpp, strength=generation_speed, limitation=no_emotion_control
- Confidence: high

### 48kHz出力品質でCD（44.1kHz）を上回る解像度。日本語イントネーション精度が優秀。
- Source: [「声をテキストで作る時代」が来た——Irodori-TTS（彩りTTS）がヤバすぎる件](https://note.com/gensnotes/n/na48b222358c4)
- Date: 2026-04-17
- Params: sample_rate=48000, ref_standard=44100
- Confidence: high

### 参照音声のlatent表現を prepare_reference スクリプトで事前計算しておくと推論時 124.8ms→0.5ms（約250倍）に削減できる。バッチ生成時に有効。
- Source: [Irodori-TTS v3とv2 VoiceDesignを試す](https://zenn.dev/kun432/scraps/b83b0406b067bb)
- Date: 2026-05-17
- Params: prepare_reference_ms_before=124.8, after=0.5
- Confidence: high

### 「音質はガチャ次第」、同じテキスト・同じSeed値なら再現性あり
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: seed_consistency=identical seed = identical voice quality, generation_time=RTX4070で2～3秒
- Confidence: high

### 従来困難だった音声効果（唾音、泣き声、欠伸、リップノイズ）が対応絵文字で生成可能
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: supported_effects=['crying', 'swallowing', 'yawning', 'lip_noise']
- Confidence: high

### seed値は『声のレシピ番号』。有望キャプションが見つかったらseed値を10パターン試して微調整するのがおすすめ。同じキャプション+seedで完全再現可能。
- Source: [20回試行して見つけた、AIキャラの推し声の作り方](https://note.com/ojisan_ai_lab/n/n870c6f00a4d1)
- Date: 2026-04-11
- Params: seed_trials=10
- Confidence: high

### Irodori-TTSはDiT型でFlow Matching方式を採用し、画像生成と数学的に同じアプローチ。Steps、CFG、KV関連パラメータが主要な調整対象
- Source: [【彩】Irodori-TTS 解説](https://note.com/417__/n/n7c25cf9a04c2)
- Date: 2026-05-08
- Params: latent_dimension=32
- Confidence: high

### Voice Cloneでは10秒程度の音声から声を再現可能だが、入力音声はクリアである必要があり、ノイズが含まれると再現度が低下する
- Source: [【彩】Irodori-TTS 解説](https://note.com/417__/n/n7c25cf9a04c2)
- Date: 2026-05-08
- Params: sample_duration_seconds=10
- Confidence: high

### 動画ナレーションなど事前音声生成が可能な用途に最適。ストリーミング非対応だが生成速度は十分
- Source: [【彩】Irodori-TTS 解説](https://note.com/417__/n/n7c25cf9a04c2)
- Date: 2026-05-08
- Confidence: high

### Flow Matching方式のアーキテクチャで500Mパラメータの軽量設計を採用。GPU環境では5秒音声を3秒で生成、CPU処理では90秒。リアルタイム生成に対応可能な性能水準。
- Source: [Irodori-TTS の考察｜日本語特化ローカル AI 音声合成](https://hatohato.jp/blog/core/single.php?id=1032)
- Date: 2026-05-04
- Params: architecture=Flow Matching, parameters=500M, gpu_latency_sec=3, cpu_latency_sec=90
- Confidence: high

### Num Stepsパラメータ(デフォルト40)を増やすと生成品質が向上するが、処理時間が増加。ステップ数の調整でスピードと品質のトレードオフを制御可能。
- Source: [【TTS】Irodori-TTS-v2の簡単な使い方など](https://local-llm.memo.wiki/d/%A1%DATTS%A1%DBIrodori-TTS-v2%A4%CE%B4%CA%C3%B1%A4%CA%BB%C8%A4%A4%CA%FD%A4%CA%A4%C9)
- Date: 2026-04-17
- Params: num_steps_default=40, num_candidates_default=1
- Confidence: high

### Reference Audio機能でボイスクローニングが可能。Voicevoxで生成した音声をReference Audioとして使用し、特定のボイススタイルを参考にしながらテキスト音声合成を実行できる。
- Source: [【TTS】Irodori-TTS-v2の簡単な使い方など](https://local-llm.memo.wiki/d/%A1%DATTS%A1%DBIrodori-TTS-v2%A4%CE%B4%CA%C3%B1%A4%CA%BB%C8%A4%A4%CA%FD%A4%CA%A4%C9)
- Date: 2026-04-17
- Params: feature=Reference Audio Upload, compatible_sources=['Voicevox']
- Confidence: high

### 参照音声なしの場合、生成ボイスの性別や声質がランダムに決定される。対照的にVoiceDesign版ではキャプションにより声の特性を明示的に制御できる。
- Source: [日本語音声AI「Irodori-TTS」の導入方法・使い方](https://kurokumasoft.com/2026/04/28/irodori-tts/)
- Date: 2026-04-28
- Params: default_behavior=random_voice, controlled_behavior=caption_specified
- Confidence: high

### パラメータ: cfg_scale_text=3.0, cfg_scale_speaker=5.0, num_steps=40
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: cfg_scale_text=3.0, cfg_scale_speaker=5.0, num_steps=40
- Confidence: N/A

### パラメータ: cfg_min_t=0.5, cfg_max_t=1.0
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### パラメータ: ref_normalize_db=-16.0, max_ref_seconds=30.0
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: ref_normalize_db=-16.0, max_ref_seconds=30.0
- Confidence: N/A

### パラメータ: tail_std_threshold=0.05, tail_mean_threshold=0.1
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: tail_std_threshold=0.05, tail_mean_threshold=0.1
- Confidence: N/A

### パラメータ: model_precision=bf16, codec_precision=fp32
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: model_precision=bf16, codec_precision=fp32
- Confidence: N/A

### speaker-kv-scale を 1.0以上に設定で話者同一性を実験的に強化できる。speaker-kv-min-t デフォルト0.9。参照音声から声質が乖離する場合に有効。
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: speaker_kv_scale_min=1.0, speaker_kv_min_t=0.9
- Confidence: medium

### 高速化レシピ: num-steps削減 + context-kv-cache有効 + decode-mode=batch。VRAM削減レシピ: decode-mode=sequential + num-candidates=1 + fp32
- Source: [Irodori-TTS 公式推論パラメータドキュメント](https://github.com/Aratako/Irodori-TTS/blob/main/docs/parameters.md)
- Date: 2026-05-18
- Params: speed_decode_mode=batch, vram_decode_mode=sequential
- Confidence: high

### Irodori-TTS-Liteの4-bit量子化でディスク容量がFP32 1888MBから279MBへ約7倍圧縮。エンドツーエンドVRAMは988.7MBで1GB未満を実現し、画像生成AIと並行稼働可能。
- Source: [1GBのVRAMで動く次世代音声合成 Irodori-TTS-Lite](https://note.com/humble_bobcat51/n/ne4c7a419c97f)
- Date: 2026-05-19
- Params: disk_mb_fp32=1888, disk_mb_int4=279, vram_mb=988.7
- Confidence: high

### Triton FusedInt4Linearカーネル利用でFP32比+約80msのレイテンシ増、実測473msで実用パフォーマンス。要件はCUDA Compute Capability 8.0以上（RTX 30シリーズ以降）。
- Source: [1GBのVRAMで動く次世代音声合成 Irodori-TTS-Lite](https://note.com/humble_bobcat51/n/ne4c7a419c97f)
- Date: 2026-05-19
- Params: latency_ms=473, cuda_cc_min=8.0
- Confidence: high

### ref-wav未指定時はモデル既定声で生成されるためspeaker similarity評価外となる。キャラクター声を維持するならLoRA fine-tuneが本命。
- Source: [Irodori-TTS の WaveEx x duration-control を Mac MPS で 4 条件比較](https://zenn.dev/yoshitetsu/articles/6376a9a2204ffb)
- Date: 2026-05-13
- Confidence: medium

### RTX4090実測：curlで約0.473秒、OpenAI SDKで約0.995秒。SDK経由のオーバーヘッドが約500ms上乗せされる点に注意。
- Source: [Irodori-TTS-Serverを試す](https://zenn.dev/kun432/scraps/27a96c1a3d3f7e)
- Date: 2026-05-15
- Params: latency_curl_s=0.473, latency_sdk_s=0.995
- Confidence: high

### 制御精度は完全ではないが、マスタリングにより多様な音声合成が可能。絵文字を組み合わせることで複合効果を生成できる
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: control_accuracy=imperfect, combination_effect=supported
- Confidence: medium

### Multi-candidate generation (1-8 candidates) with truncation-factor parameter and score rescaling (k and sigma parameters
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: max_candidates=8, truncation_factor=optional, score_rescaling_params=['k', 'sigma']
- Confidence: high

### 話速制御: ⏩(高速)、🐢(低速)により合成音声のテンポを明確に変更可能
- Source: [EMOJI_ANNOTATIONS.md - Irodori-TTS-500M-v2 Emoji Control Guide](https://huggingface.co/Aratako/Irodori-TTS-500M-v2/blob/main/EMOJI_ANNOTATIONS.md)
- Params: fast_emoji=⏩, slow_emoji=🐢, characteristics=['rapid-fire speech', 'slow speech']
- Confidence: high

### 音響環境の模擬: 📢(エコー/リバーブ)、📞(電話/スピーカー経由)により合成音声の音響特性を変更
- Source: [EMOJI_ANNOTATIONS.md - Irodori-TTS-500M-v2 Emoji Control Guide](https://huggingface.co/Aratako/Irodori-TTS-500M-v2/blob/main/EMOJI_ANNOTATIONS.md)
- Params: echo_reverb_emoji=📢, phone_speaker_emoji=📞, effect_type=acoustic_environment
- Confidence: high

### 難読漢字はTTS誤読の原因。重要な単語はひらがなで書く
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### 33種類の感情絵文字が声質に影響: 😊楽しげ 😠怒り 😰パニック 🥺不安 😭泣き 😱恐怖 😪眠い 😆大笑い 😲驚き 🙏懇願
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: total_emojis=33
- Confidence: high

### パラメータ: num_steps=40, cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Source: [GitHub - Aratako/Irodori-TTS: A Flow Matching-based TTS Model](https://github.com/Aratako/Irodori-TTS)
- Date: 2025-01-01
- Params: num_steps=40, cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### パラメータ: training_steps_multiplier=2.5
- Source: [Aratako/Irodori-TTS-500M-v2 · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2)
- Date: 2026-01-01
- Params: training_steps_multiplier=2.5
- Confidence: N/A

### パラメータ: vae_dim=32, sample_rate=48kHz
- Source: [Aratako/Irodori-TTS-500M-v2 · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2)
- Date: 2026-01-01
- Params: vae_dim=32, sample_rate=48kHz
- Confidence: N/A

### パラメータ: cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### パラメータ: lora_scale_range=0.0-2.0, lora_scale_default=1.0
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: lora_scale_range=0.0-2.0, lora_scale_default=1.0
- Confidence: N/A

### パラメータ: max_candidates=8
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: max_candidates=8
- Confidence: N/A

### GPU不要で動作し、数秒程度のセリフなら2〜3秒で出力完了する爆速生成性能。リアルタイム用途に対応可能なレベル。
- Source: [【無料】声優不要！？神AI「Irodori-TTS」がヤバすぎて草生える件](https://library.libecity.com/articles/01KNFP7SDC3ZW1HRJFASXF81BX)
- Date: 2026-04-06
- Params: gpu_required=False, latency_sec=2-3
- Confidence: high

### WavLM意味抽出(semantic distillation)を統合することで、日本語音声の自然性と主観的品質が向上する。Emilia-YODASデータセットでUTMOSv2スコアが2.28から2.48へ改善された。
- Source: [Semantic-DACVAE-Japanese: Audio VAE for Japanese Speech](https://huggingface.co/Aratako/Semantic-DACVAE-Japanese)
- Params: metric=UTMOSv2, baseline_score=2.2841, improved_score=2.4812
- Confidence: high


## Training Tips (学習・LoRA)

### v3はv2から可変長学習に移行しDuration Predictorを新規導入。訓練効率が向上し推論時のReal-Time Factor（RTF）が改善された。固定長学習制約が解除
- Source: [Irodori-TTS-500M-v3: 公式モデルカード](https://huggingface.co/Aratako/Irodori-TTS-500M-v3)
- Date: 2026-01-01
- Params: training_mode=variable-length, new_component=Duration Predictor
- Confidence: high

### LoRA学習デフォルト設定：ランク16、アルファ32.0、ドロップアウト0.05。ターゲットモジュールはwq,wk,wv,woが推奨
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: lora_rank=16, lora_alpha=32.0, lora_dropout=0.05, target_modules=['wq', 'wk', 'wv', 'wo']
- Confidence: high

### LoRA学習推奨設定（約50件サンプル、RTX 5060 Ti 16GB想定）：バッチ4、勾配蓄積2、warmup300、安定2100、max3000ステップ。bf16精度で学習時間30～60分
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: batch_size=4, gradient_accumulation_steps=2, warmup_steps=300, max_steps=3000, precision=bf16
- Confidence: high

### マニフェストはJSONL形式で出力。text・latent_path・speaker_id・num_framesが必須フィールド。v2/v3はlatent_dims=32、v1は128
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: format=JSONL, latent_dims_v3=32, latent_dims_v1=128
- Confidence: high

### モデルマージ手法は3種類：Weighted Average・SLERP・Task Arithmetic。テキスト/話者/拡散/IO層のグループ別部分マージ対応
- Source: [Emoji-TTS（Irodori-TTSフォーク版）日本語README](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README_ja.md)
- Params: merge_methods=['weighted_average', 'slerp', 'task_arithmetic']
- Confidence: high

### V2モデルはコーデックを日本語専用版（Semantic-DACVAE-Japanese-32dim）に切り替え、学習ステップをV1比で2.5倍増加、データフィルタリングを厳格化
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: codec_v2=Semantic-DACVAE-Japanese_32dim, training_multiplier=2.5
- Confidence: high

### Irodori-TTSのLoRA学習において、フォーク版のEmoji-TTSを使用する方が実装上より利用しやすい傾向がある。フォーク版はインターフェースや統合面で改善が施されている。
- Source: [Irodori-TTSのLoRA配布｜852話](https://note.com/852wa/n/n7a4955dc6754)
- Date: 2026-04-21
- Params: framework=Irodori-TTS fork (Emoji-TTS)
- Confidence: medium

### LoRAモデルのファイル構成は loraフォルダに学習データセット名（例: 43ch）のフォルダごと配置する形式で管理する。複数声色の管理が効率化される。
- Source: [Irodori-TTSのLoRA配布｜852話](https://note.com/852wa/n/n7a4955dc6754)
- Date: 2026-04-21
- Params: directory_structure=lora/<character_name>/
- Confidence: high

### Speaker Inversion: 話者エンコーダ入力ではなく speaker_state（最終話者状態ベクトル）側を直接最適化する。これによりベースモデル能力を壊さずに軽量で声を学習可能。
- Source: [Irodori-TTSを使って音声ファイルよりも軽い埋め込みだけで声を学習する](https://zenn.dev/platina/articles/speaker-inversion)
- Date: 2026-05-19
- Params: target_layer=speaker_state
- Confidence: high

### 16トークンの埋め込みベクトルを直接学習する設計で、LoRA rank4 (17Mパラメータ) と比べて12Kパラメータ（約1/1000）に削減できる。トークン数で表現力を制御。
- Source: [Irodori-TTSを使って音声ファイルよりも軽い埋め込みだけで声を学習する](https://zenn.dev/platina/articles/speaker-inversion)
- Date: 2026-05-19
- Params: num_tokens=16, params_count=12000
- Confidence: high

### FP32 16トークン埋め込みのファイルサイズは49KBで、5秒無圧縮WAV約500KBの1/10。VRAM 3.2GB（LoRA比12%削減）、学習時間30%削減と効率的。
- Source: [Irodori-TTSを使って音声ファイルよりも軽い埋め込みだけで声を学習する](https://zenn.dev/platina/articles/speaker-inversion)
- Date: 2026-05-19
- Params: file_size_kb=49, vram_gb=3.2, time_reduction_pct=30
- Confidence: high

### サーバ側でLoRAアダプターを動的ロード可能。キャラごとに異なるLoRAを切替えながら同一サーバで運用するパイプラインに有効。
- Source: [Irodori-TTS-Serverを試す](https://zenn.dev/kun432/scraps/27a96c1a3d3f7e)
- Date: 2026-05-15
- Confidence: high

### Default fine-tuning config: batch_size=4, gradient_accumulation=2, optimizer=muon, learning_rate=3e-4, max_steps=3000, w
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: batch_size=4, gradient_accumulation_steps=2, optimizer=muon, learning_rate=0.0003, max_steps=3000, warmup_steps=300, stable_steps=2100, lr_scheduler=wsd, precision=bf16
- Confidence: high

### LoRA fine-tuning: rank=16, alpha=32.0, dropout=0.05, target_modules=wq,wk,wv,wo
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: lora_rank=16, lora_alpha=32.0, lora_dropout=0.05, target_modules=wq,wk,wv,wo
- Confidence: high

### 言語固有のVAEモデルは対象言語のデータセットで明示的にファインチューニングすることで、オリジナルベースモデルより優れた再構成品質が得られる。
- Source: [Semantic-DACVAE-Japanese: Audio VAE for Japanese Speech](https://huggingface.co/Aratako/Semantic-DACVAE-Japanese)
- Params: base_model=facebook/dacvae-watermarked, language=Japanese, training_approach=semantic_distillation
- Confidence: high
