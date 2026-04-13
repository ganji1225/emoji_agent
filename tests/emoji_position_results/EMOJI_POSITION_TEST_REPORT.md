# 絵文字の量×位置 比較テスト結果
日時: 2026-04-13
シード: 42
モデル: VoiceDesign (Aratako/Irodori-TTS-500M-v2-VoiceDesign)

## パターン説明
| パターン | 説明 |
|---|---|
| A_prefix_少 | 絵文字1個を前方のみ |
| B_sandwich | 絵文字2-3個を前後に配置（サンドイッチ） |
| C_prefix_多 | 絵文字3-5個を全て前方に配置 |
| D_sandwich_多 | 絵文字5個以上を前後に多めに配置 |

## 生成結果
| レベル | パターン | ファイル | 生成時間 | サイズ | 状態 |
|---|---|---|---|---|---|
| light | A_prefix_少 | light_A_prefix_少.wav | 105.1s | 623KB | OK |
| light | B_sandwich | light_B_sandwich.wav | 18.9s | 716KB | OK |
| light | C_prefix_多 | light_C_prefix_多.wav | 17.5s | 623KB | OK |
| light | D_sandwich_多 | light_D_sandwich_多.wav | 16.3s | 716KB | OK |
| medium | A_prefix_少 | medium_A_prefix_少.wav | 17.0s | 784KB | OK |
| medium | B_sandwich | medium_B_sandwich.wav | 16.8s | 784KB | OK |
| medium | C_prefix_多 | medium_C_prefix_多.wav | 16.6s | 1065KB | OK |
| medium | D_sandwich_多 | medium_D_sandwich_多.wav | 16.3s | 1440KB | OK |
| heavy | A_prefix_少 | heavy_A_prefix_少.wav | 16.7s | 911KB | OK |
| heavy | B_sandwich | heavy_B_sandwich.wav | 17.5s | 1046KB | OK |
| heavy | C_prefix_多 | heavy_C_prefix_多.wav | 14.8s | 1046KB | OK |
| heavy | D_sandwich_多 | heavy_D_sandwich_多.wav | 17.9s | 1440KB | OK |

## 聴き比べ結果（ユーザー評価）

### 感情の「入り」（冒頭の表現力）
- light: B_sandwich = C_prefix_多 > A_prefix_少 = D_sandwich_多
- medium: D_sandwich_多 > C_prefix_多 > B_sandwich > A_prefix_少
- heavy: D_sandwich_多 > C_prefix_多 > B_sandwich > A_prefix_少

### 感情の「出」（末尾の余韻・着地）
- light: D_sandwich_多 = B_sandwich > C_prefix_多 > A_prefix_少
- medium: D_sandwich_多 > B_sandwich > C_prefix_多 > A_prefix_少
- heavy: D_sandwich_多 > B_sandwich > C_prefix_多 > A_prefix_少

### 全体の感情強度
- light: D_sandwich_多 = B_sandwich > C_prefix_多 > A_prefix_少
- medium: D_sandwich_多 > C_prefix_多 > B_sandwich > A_prefix_少
- heavy: D_sandwich_多 > B_sandwich > C_prefix_多 > A_prefix_少

### 不自然なノイズ・アーティファクト（多い順 = 悪い順）
- light: D_sandwich_多 > C_prefix_多 > B_sandwich > A_prefix_少
- medium: D_sandwich_多 > C_prefix_多 > B_sandwich > A_prefix_少
- heavy: D_sandwich_多 > C_prefix_多 > B_sandwich = A_prefix_少

### 間（ま）の自然さ
- light: B_sandwich = D_sandwich_多 > C_prefix_多 > A_prefix_少
- medium: C_prefix_多 = B_sandwich > D_sandwich_多 > A_prefix_少
- heavy: D_sandwich_多 > B_sandwich > C_prefix_多 > A_prefix_少

## 結論：最適パターン

| 感情レベル | 推奨パターン | 理由 |
|---|---|---|
| **弱（日常・自信・威圧）** | **B_sandwich** | 表現力◎ ノイズ少 間◎ lightで総合1位 |
| **中（恥じらい・喘ぎ弱）** | **B_sandwich / C_prefix_多** | 間が自然でノイズ控えめ |
| **強（絶頂・叫び）** | **D_sandwich_多** | 圧倒的表現力、ノイズは激しい場面で許容 |
| **極限（連続絶頂・出産）** | **D_sandwich_多（最大盛り）** | 全指標で最高、ノイズも演技の一部 |

→ script_processor.py に反映済み（build_sandwich関数で自動制御）

## 音声ファイル場所
`D:\irodori\tests\emoji_position_results`
