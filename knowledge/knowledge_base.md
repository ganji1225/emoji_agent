# TTS Production Knowledge Base
_Auto-updated: 2026-04-25 | Total findings: 77 | Sources: 19 articles_


## Caption Design (キャプション設計)

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

### 三点リーダーは文脈の雰囲気を保持するが、絵文字は台詞化する傾向。効果は文脈依存的
- Source: [絵文字で感情表現ができる合成音声Irodori-TTSを使ってみた](https://note.com/totchira/n/n1b9eb0c64080)
- Date: 2026-02-27
- Params: context_sensitivity=high
- Confidence: medium

### 難しい漢字はひらがなに変換してから入力すると安定する
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: input_preprocessing=kanji_to_hiragana_conversion
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

### Irodori-TTSは絵文字によるスタイル制御（感情・SE等）機能を搭載し、テキストに絵文字を挿入するだけでアニメキャラ風の感情表現が可能
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: supported_features=['emotion_control', 'sound_effects']
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

### Emoji caption feature extracts acoustic features (pitch, energy, speech rate, MF
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

### Independent CFG guidance: cfg-scale-text=3.0, cfg-scale-speaker=5.0 as defaults.
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: cfg_scale_text_default=3.0, cfg_scale_speaker_default=5.0, guidance_modes=['independent', 'joint', 'alternating'], cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: high

### WAV→MP3変換はffmpeg VBR qscale:a 2（約190kbps）が最適
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Params: ffmpeg_qscale=2, approx_bitrate=190kbps
- Confidence: high


## Audio Post-Processing (音声後処理)

### Trailing silence trimming via flattening heuristic enabled by default (trim-tail
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: trim_tail=True, method=flattening_heuristic
- Confidence: medium

### テキストファイルを行ごとに読み込み、Gradioで順序的に一括音声生成処理を実行。1行1セリフのtxtファイル形式。
- Source: [Irodori-TTSで音声を一括生成する](https://note.com/aiaicreate/n/n61b29f9810a8)
- Date: 2026-04-16
- Params: input_format=txt (1行1セリフ), output_naming=セリフそのまままたはプレフィックス+連番, ui_component=Gradio file upload + batch processing button
- Confidence: high


## Voice Quality (声質改善)

### ゼロショット音声クローンはリファレンス音声の話者特性をMioTTSより正確に再現。参照音声なしでも使用可能。
- Source: [「Irodori-TTS」を試す](https://zenn.dev/kun432/scraps/87d7776909e4d9)
- Date: 2025-03-22
- Params: ref_wav_required=False, zero_shot_clone=supported, vram_usage_gb=7.7, compared_model=MioTTS
- Confidence: medium

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

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: cfg_scale_text=3.0, cfg_scale_speaker=5.0, num_steps=40
- Confidence: N/A

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: ref_normalize_db=-16.0, max_ref_seconds=30.0
- Confidence: N/A

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: tail_std_threshold=0.05, tail_mean_threshold=0.1
- Confidence: N/A

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Params: model_precision=bf16, codec_precision=fp32
- Confidence: N/A

### N/A
- Source: [【多様な感情表現】Irodori TTSサンプル＆導入解説](https://note.com/seal309midorin/n/nb3fa17b52deb)
- Date: 2026-04-21
- Confidence: N/A

### 制御精度は完全ではないが、マスタリングにより多様な音声合成が可能。絵文字を組み合わせることで複合効果を生成できる
- Source: [Irodori-TTS-500M Emoji Annotations Guide](https://huggingface.co/Aratako/Irodori-TTS-500M/blob/main/EMOJI_ANNOTATIONS.md)
- Params: control_accuracy=imperfect, combination_effect=supported
- Confidence: medium

### Multi-candidate generation (1-8 candidates) with truncation-factor parameter and
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

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2-VoiceDesign · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- Date: 2026-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2-VoiceDesign · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- Date: 2026-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2-VoiceDesign · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- Date: 2026-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2-VoiceDesign · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- Date: 2026-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2-VoiceDesign · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign)
- Date: 2026-01-01
- Confidence: N/A

### 難読漢字はTTS誤読の原因。重要な単語はひらがなで書く
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### 33種類の感情絵文字が声質に影響: 😊楽しげ 😠怒り 😰パニック 🥺不安 😭泣き 😱恐怖 😪眠い 😆大笑い 😲驚き 🙏懇願
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: total_emojis=33
- Confidence: high

### N/A
- Source: [GitHub - Aratako/Irodori-TTS: A Flow Matching-based TTS Model](https://github.com/Aratako/Irodori-TTS)
- Date: 2025-01-01
- Params: num_steps=40, cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### N/A
- Source: [GitHub - Aratako/Irodori-TTS: A Flow Matching-based TTS Model](https://github.com/Aratako/Irodori-TTS)
- Date: 2025-01-01
- Confidence: N/A

### N/A
- Source: [GitHub - Aratako/Irodori-TTS: A Flow Matching-based TTS Model](https://github.com/Aratako/Irodori-TTS)
- Date: 2025-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2 · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2)
- Date: 2026-01-01
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2 · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2)
- Date: 2026-01-01
- Params: training_steps_multiplier=2.5
- Confidence: N/A

### N/A
- Source: [Aratako/Irodori-TTS-500M-v2 · Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2)
- Date: 2026-01-01
- Params: vae_dim=32, sample_rate=48kHz
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: cfg_scale_text=3.0, cfg_scale_speaker=5.0, guidance_mode=independent, cfg_min_t=0.5, cfg_max_t=1.0
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: lora_scale_range=0.0-2.0, lora_scale_default=1.0
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Params: max_candidates=8
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Confidence: N/A

### N/A
- Source: [GitHub - iron-mukakin/Emoji-TTS: Irodori-TTSのフォーク](https://github.com/iron-mukakin/Emoji-TTS)
- Date: 2025-01-01
- Confidence: N/A


## Training Tips (学習・LoRA)

### V2モデルはコーデックを日本語専用版（Semantic-DACVAE-Japanese-32dim）に切り替え、学習ステップをV1比で2.5倍増加、データフィル
- Source: [テキストに絵文字入れるだけ アニメキャラ風の感情表現ができる日本語TTSirodoriTTS_V2](https://note.com/jscdisk/n/n6352441b050f)
- Date: 2026-04-08
- Params: codec_v2=Semantic-DACVAE-Japanese_32dim, training_multiplier=2.5
- Confidence: high

### Default fine-tuning config: batch_size=4, gradient_accumulation=2, optimizer=muo
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: batch_size=4, gradient_accumulation_steps=2, optimizer=muon, learning_rate=0.0003, max_steps=3000, warmup_steps=300, stable_steps=2100, lr_scheduler=wsd, precision=bf16
- Confidence: high

### LoRA fine-tuning: rank=16, alpha=32.0, dropout=0.05, target_modules=wq,wk,wv,wo
- Source: [Emoji-TTS README - Flow Matching TTS with Emotion Control (iron-mukakin fork)](https://github.com/iron-mukakin/Emoji-TTS/blob/main/README.md)
- Params: lora_rank=16, lora_alpha=32.0, lora_dropout=0.05, target_modules=wq,wk,wv,wo
- Confidence: high
