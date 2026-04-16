# TTS Production Knowledge Base
_Auto-updated: 2026-04-16 | Total findings: 14 | Sources: 4 articles_


## Caption Design (キャプション設計)

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

### WAV→MP3変換はffmpeg VBR qscale:a 2（約190kbps）が最適
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Params: ffmpeg_qscale=2, approx_bitrate=190kbps
- Confidence: high


## Voice Quality (声質改善)

### 難読漢字はTTS誤読の原因。重要な単語はひらがなで書く
- Source: [Irodori-TTSのキャプション設計で声質を操る方法](https://zenn.dev/ojisan_ai_lab/articles/post-20260411-nu5cku)
- Date: 2026-04-11
- Confidence: high

### 33種類の感情絵文字が声質に影響: 😊楽しげ 😠怒り 😰パニック 🥺不安 😭泣き 😱恐怖 😪眠い 😆大笑い 😲驚き 🙏懇願
- Source: [Irodori-TTS EMOJI_ANNOTATIONS.md - 公式絵文字アノテーション](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign/blob/main/EMOJI_ANNOTATIONS.md)
- Date: 2026-03-24
- Params: total_emojis=33
- Confidence: high
