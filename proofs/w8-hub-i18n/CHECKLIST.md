# W8 Hub 殼玩家可見字六語系送審檢核清單 (w8-hub-i18n)

## 任務資訊
- 卡號：`t_c3ee61e9`
- 標題：🎮 遊戲開發｜W8 Hub 殼玩家可見字六語系
- 負責人：阿翔（sideworker2）
- 審查員：小婷（sideqa）

## 規範遵從檢核
- [x] **0-QA23**：OUT_DIR 嚴格限定為 `proofs/w8-hub-i18n/`，絕不覆蓋其它卡片 proof。
- [x] **0-QA24**：日文漢字（如「玩具の山の縁」、「初回クリアと掃討」、「進行ガイド」等）對齊 `game/data/i18n/content/ja/` 既定譯名。
- [x] **0-QA25**：開著 W8 Hub 介面即時動態切換語系，全畫面（Banner、Info、按鈕、Hint、Daily 事件）連動刷新無延遲。
- [x] **零系統 Emoji**：按鈕、提示、橫幅全面無 emoji。
- [x] **不改數值**：未修改任何戰鬥與經濟數值平衡。
- [x] **不產圖**：未產生無授權圖片資產。
- [x] **不推 main**：代碼保留於專案 worktree 分支 `wt/t_c3ee61e9`。

## 節點與 Key 查表對應表

| UI 節點路徑 | 原始繁中文案 | 查表 Key (ContentLoc / Loc) | 刷新機制 | en 譯文 | ja 譯文 |
|---|---|---|---|---|---|
| `Banner` (Phase.ONBOARD) | 玩具堆邊緣 · 新手引導 | `玩具堆邊緣 · 新手引導` / `w8.hub.banner_onboard` | `_refresh_banner()` | Toy-pile Edge · Novice Guide | 玩具の山の縁 · 初心者ガイド |
| `Banner` (Phase.SOUL) | 玩具堆邊緣 · 聚魂抽取 | `玩具堆邊緣 · 聚魂抽取` / `w8.hub.banner_soul` | `_refresh_banner()` | Toy-pile Edge · Soul Drawing | 玩具の山の縁 · 魂寄せガチャ |
| `Banner` (Phase.CHAPTER) | 玩具堆邊緣 · 首通與掃蕩 · 發條 %d/%d | `玩具堆邊緣 · 首通與掃蕩 · 發條 %d/%d` / `w8.hub.banner_chapter` | `_refresh_banner()` | Toy-pile Edge · First Clear & Sweep · Wind-up %d/%d | 玩具の山の縁 · 初回クリアと掃討 · ぜんまい %d/%d |
| `ChapterPanel/Info` | 章節「玩具堆邊緣」\n金幣 %d · 聚魂券 %d · 等級 %d\n發條 %d/%d · 今日掃蕩 %d | `章節「玩具堆邊緣」\n金幣 %d · 聚魂券 %d · 等級 %d\n發條 %d/%d · 今日掃蕩 %d` / `w8.hub.chapter_info` | `_refresh_chapter_info()` | Chapter "Toy-pile Edge"\nGold %d · Soul Tickets %d · Level %d\nWind-up %d/%d · Sweeps Today %d | 章「玩具の山の縁」\nゴールド %d · 魂寄せ券 %d · レベル %d\nぜんまい %d/%d · 今日の掃討 %d |
| `ChapterPanel/ButtonRow/BtnFirstClear` | 首通 玩具堆邊緣 | `首通 玩具堆邊緣` / `w8.hub.btn_first_clear` | `_refresh_chapter_buttons()` | First Clear: Toy-pile Edge | 初回クリア 玩具の山の縁 |
| `ChapterPanel/ButtonRow/BtnSweep` | 掃蕩 玩具堆邊緣 | `掃蕩 玩具堆邊緣` / `w8.hub.btn_sweep` | `_refresh_chapter_buttons()` | Sweep: Toy-pile Edge | 掃討 玩具の山の縁 |
| `ChapterPanel/ButtonRow/BtnSimRegen` | 等 8 分（模擬回復） | `等 8 分（模擬回復）` / `w8.hub.btn_sim_regen` | `_refresh_chapter_buttons()` | Wait 8 min (Sim Regen) | 8分待機（回復シミュレーション） |
| `ChapterPanel/ButtonRow/BtnGotoSoul` | 前往聚魂 | `前往聚魂` / `w8.hub.btn_goto_soul` | `_refresh_chapter_buttons()` | Go to Soul Draw | 魂寄せへ |
| `ChapterPanel/Hint` | 引導流程：新手引導 → 聚魂抽取 → 章節挑戰。日常發條每日一選，漏天不補。 | `引導流程：新手引導 → 聚魂抽取 → 章節挑戰。日常發條每日一選，漏天不補。` / `w8.hub.hint` | `_refresh_chapter_hint()` | Guide Flow: Novice Guide → Soul Drawing → Chapter Challenge. Daily wind-up once per day; missed days cannot be made up. | 進行ガイド：初心者ガイド → 魂寄せガチャ → 章チャレンジ。デイリーぜんまいは1日1回、逃した日は補填されません。 |
| `Toast` / 回饋 | 新手引導完成，前往聚魂 | `新手引導完成，前往聚魂` / `w8.hub.toast_onboard_done` | `_flash()` | Novice guide complete, proceeding to soul drawing | 初心者ガイド完了、魂寄せへ進みます |
| `Toast` / 回饋 | 前往玩具堆邊緣 | `前往玩具堆邊緣` / `w8.hub.toast_goto_outskirts` | `_flash()` | Proceeding to Toy-pile Edge | 玩具の山の縁へ進みます |
| `Toast` / 回饋 | 需先首通，或發條／掃蕩次數不足 | `需先首通，或發條／掃蕩次數不足` / `w8.hub.err_need_first_clear` | `_flash()` | Must first clear, or insufficient wind-up/sweeps | 初回クリアが必要、またはぜんまい／掃討回数が不足しています |
| `Toast` / 回饋 | 首通失敗：%s | `首通失敗：%s` / `w8.hub.err_first_clear_fail` | `_flash()` | First clear failed: %s | 初回クリア失敗：%s |
| `Toast` / 回饋 | 掃蕩失敗：%s | `掃蕩失敗：%s` / `w8.hub.err_sweep_fail` | `_flash()` | Sweep failed: %s | 掃討失敗：%s |
| `Toast` / 回饋 | 日常發條失敗：%s | `日常發條失敗：%s` / `w8.hub.err_daily_fail` | `_flash()` | Daily wind-up failed: %s | デイリーぜんまい失敗：%s |

## 實機存證產物
- `proofs/w8-hub-i18n/proof_01_w8_hub_chapter_en.png` (en 全景截圖)
- `proofs/w8-hub-i18n/crops/crop_01_w8_hub_chapter_en.png` (en 特寫截圖)
- `proofs/w8-hub-i18n/proof_02_w8_hub_chapter_ja.png` (ja 全景截圖)
- `proofs/w8-hub-i18n/crops/crop_02_w8_hub_chapter_ja.png` (ja 特寫截圖)
- `proofs/w8-hub-i18n/proof_03_w8_hub_chapter_zh_TW.png` (zh_TW 對照全景截圖)
- `proofs/w8-hub-i18n/crops/crop_03_w8_hub_chapter_zh_TW.png` (zh_TW 對照特寫截圖)

## 測試通過狀態
- `godot --path game --headless -s res://scripts/systems/wave8/test_w8_hub.gd` -> `W8_HUB_OK` 通過
- `godot --path game --headless -s res://scripts/systems/wave8/test_w8_hub_i18n.gd` -> `TEST_W8_HUB_I18N_OK` 通過
