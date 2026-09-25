# 《發條之心》探索性 QA 第三十四輪 查驗清單與缺陷報告 (Round 34 Checklist)

- **測試日期**：2026-09-26
- **測試員**：小婷（側案·測試 sideqa）
- **關聯卡號**：`t_cff8dfc0`
- **關聯前置任務**：
  - `t_2d2c11cb`（衣櫥「星紋斗篷」、「無外裝 (裸機素體)」六語系落地與彈窗標題按鈕語系修復）
  - `t_9409c5c5`（創角頂部「首發／擴充」分頁與底部「確認選擇 · 踏上旅途／返回」按鈕六語系落地）
- **存檔目錄**：`/opt/side/bravesoul-game/proofs/qa_round34/`

---

## 一、 實機截圖核驗清單（每張全景圖：破圖／emoji／截字／模糊／語系一致性）

依據規範（review.md 0-QA15、0-QA17、0-QA23、0-QA24、0-QA25），全數實機截圖規格為 1280x720，MD5 經查核 100% 獨立無覆蓋：

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零系統Emoji | 零截字 | 高清立繪 | 審核結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_wardrobe_frog_astral_zh_TW.png` | 衣櫥 蛙選星紋斗篷（zh_TW 全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 02 | `proof_02_wardrobe_frog_astral_en.png` | 衣櫥 蛙選星紋斗篷（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 03 | `proof_03_wardrobe_frog_astral_ja.png` | 衣櫥 蛙選星紋斗篷（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 04 | `proof_04_wardrobe_frog_bare_zh_TW.png` | 衣櫥 蛙選裸像素體（zh_TW 全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 05 | `proof_05_wardrobe_frog_bare_en.png` | 衣櫥 蛙選裸像素體（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 06 | `proof_06_wardrobe_frog_bare_ja.png` | 衣櫥 蛙選裸像素體（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 07 | `proof_07_creation_launch_zh_TW.png` | 創角首發分頁（zh_TW 白金兔全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 08 | `proof_08_creation_launch_en.png` | 創角首發分頁（en 英文 白金兔全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 09 | `proof_09_creation_launch_ja.png` | 創角首發分頁（ja 日文 白金兔全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 10 | `proof_10_creation_expansion_zh_TW.png` | 創角擴充分頁（zh_TW 瓷韻熊貓全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 11 | `proof_11_creation_expansion_en.png` | 創角擴充分頁（en 英文 瓷韻熊貓全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 12 | `proof_12_creation_expansion_ja.png` | 創角擴充分頁（ja 日文 瓷韻熊貓全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 13 | `proof_13_lobby_dock_zh_TW.png` | 手遊大廳與 Dock（zh_TW 全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 14 | `proof_14_lobby_dock_en.png` | 手遊大廳與 Dock（en 英文全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 發現背景漏翻 |
| 15 | `proof_15_lobby_dock_ja.png` | 手遊大廳與 Dock（ja 日文全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 發現背景漏翻 |

### 局部特寫 Crops 驗證清單（`proofs/qa_round34/crops/`）
- `crop_wardrobe_title_{zh_TW,en,ja}.png`：衣櫥彈窗大標題與副標題即時翻譯特寫。
- `crop_wardrobe_cards_{zh_TW,en,ja}.png`：衣櫥外裝卡片（星紋斗篷／裸像素體）多語系卡片文字特寫。
- `crop_wardrobe_actions_{zh_TW,en,ja}.png`：衣櫥底部操作按鈕（還原預設、隨機、確認換裝）多語系特寫。
- `crop_creation_tabs_{zh_TW,en,ja}.png`：創角頂部「首發／擴充」分頁標籤多語系特寫。
- `crop_creation_actions_{zh_TW,en,ja}.png`：創角底部操作按鈕（確認選擇 · 踏上旅途／返回）多語系特寫。
- `crop_dock_{zh_TW,en,ja}.png`：底部 Dock 五大入口多語系連動特寫。

---

## 二、 專項查核重點結果

### 1. 衣櫥六語系落地與素體展示（proof_01 ~ proof_06）
- **星紋斗篷（Astral Cape）多語系**：
  - zh_TW：卡片顯示「星紋斗篷」，左側 512 預覽為藍金琺瑯星紋斗篷。
  - en：卡片顯示「Astral Cape」，大標題 `Clockwork Wardrobe · Hero Outfits`。
  - ja：卡片顯示「星紋のマント」，大標題 `ゼンマイ衣装棚・英雄の着替え`。
  - 均帶有金色選用框與選中標記（`✓ 已選用` / `✓ Selected` / `✓ 選択中`）。
- **裸像素體（Bare Frame）外觀與多語系**：
  - zh_TW：卡片顯示「無外裝 (裸機素體)」，左側 512 預覽無斗篷無圍裙，露出完整綠金機械素體與發條關節。
  - en：卡片顯示「No Costume (Bare Frame)」，選取狀態為 `✔ Selected`。
  - ja：卡片顯示「衣装なし (素体)」，選取狀態為 `✔ 選択中`。
- **彈窗標題與按鈕修復**：
  - 徹底解決了 Round 33 發現的標題與按鈕硬編碼繁中問題，底部按鈕均已隨語系動態切換：
    - zh_TW: 還原預設｜隨機｜確認換裝 · 套用新外觀
    - en: Reset｜Random｜Confirm Outfit · Apply New Look
    - ja: デフォルトに戻す｜ランダム｜着替え確認・新しい外見を適用

### 2. 創角首發／擴充分頁與確認按鈕（proof_07 ~ proof_12）
- **頂部雙 Tab 分頁**：
  - zh_TW：「首發」「擴充」
  - en：「Launch」「Expansion」
  - ja：「初期」「拡張」
  - 點擊分頁即時切換高亮底色與下機種族清單，首發 5 族與擴充 8 族各自獨立、無溢出無空卡。
- **底部操作按鈕**：
  - zh_TW：「確認選擇 · 踏上旅途」「返回」
  - en：「Confirm Selection · Begin Journey」「Back」
  - ja：「選択確認 · 旅立ち」「戻る」
  - 100% 完整翻譯，按鈕尺寸熱區與間距均符合規範。
- **角色立繪**：
  - 白金兔（首發）與瓷韻熊貓（擴充）512 高清人偶合成無缺件、無破圖、零殘留 Emoji。

### 3. 大廳頂欄與底部 Dock 連動查核（0-QA25 檢查，proof_13 ~ proof_15）
- **連動一致性**：
  - 玩家切換語言後，大廳頂部（商城／設置）、左側四大入口、底部五大 Dock 標籤皆能動態連動切換：
    - zh_TW: 商城 / 設置 / 天宮鐵匠 / 手藝工坊 / 演武競技 / 冒險委託 / 發條新村 / 冒險背包
    - en: Shop / Settings / Celestial Blacksmith / Craft Workshop / Martial Arena / Adventure Bounties / Cogwheel Hamlet / Adventure Bag
    - ja: ショップ / 設定 / 天宮の鍛冶屋 / 工芸工房 / 演武競技 / 冒険依頼 / ぜんまい新村 / 冒險バッグ
  - 0-QA25 規範（彈窗切換語言時大廳背景同步換語系）合格通過。

### 4. 日／韓漢字翻譯規範核實（0-QA24 規範）
- 日文環境下角色名「碧箸蛙」、職業「忍者」、建築「聚魂殿」在 `game/data/i18n/content/ja/ui.json` 中本即以漢字收錄（`"碧箸蛙": "碧箸蛙"`），符合 0-QA24「沿用漢字的既定譯名不誤判為漏翻」之標準。

### 5. 截圖目錄獨立性核驗（0-QA23 規範）
- 截圖腳本 `tools/capture_qa_round34.gd` 將輸出嚴格限定於 `proofs/qa_round34/` 與 `proofs/qa_round34/crops/`，完全未寫入或覆蓋其他任務的 proof 目錄。

---

## 三、 探索性發現之缺陷報告（什麼輸入 → 什麼壞掉）
*註：依任務規範「若還有玩家可見漏翻，CHECKLIST 寫『什麼輸入→什麼壞掉』；本單不修，由製作人另開單」。*

### 【缺陷 1】大廳右側玩家當前裝備欄部件名稱在非繁中語系下存在漏翻（仍顯示繁中）
- **觸發輸入**：
  1. 切換語言至英文（en）或日文（ja）。
  2. 進入手遊主大廳（`MobileLobby`），檢視右上方角色當前裝備清單（`Weapon`、`Clockwork`、`Curio` 槽位）。
- **壞掉現象**：
  - 裝備清單中的部件標籤（如 `Outfit` / `Weapon` / `Clockwork` / `Curio`）已成功翻譯。
  - 第一項外裝「`Spring Forest Courier Overalls`」已翻譯。
  - 但其餘三項裝備名稱**仍顯示為繁體中文**（見 `proof_14_lobby_dock_en.png`、`proof_15_lobby_dock_ja.png`，以及衣櫥背景露出處）：
    - 武器槽：仍顯示「**碧葉旋刃機關鏢**」
    - 發條槽：仍顯示「**雙蝶翼同心圓黃銅發條鑰匙**」
    - 奇玩槽：仍顯示「**微型發條荷葉浮空傘**」
- **根本原因**：
  大廳裝備欄直接讀取自 `GameState` 玩家初始裝備之物件名稱，該物件名稱在資料表或顯示層尚未呼叫 `Loc.t()` 進行本地化映射。
- **修復建議**：
  於 `mobile_lobby.gd` 的裝備顯示邏輯中（或裝備資料庫）補充六語系詞條映射。

### 【缺陷 2】創角紙娃娃展示介面（`paperdoll_select_demo.tscn`）種族名稱與槽位控制項未接入 i18n
- **觸發輸入**：
  1. 切換語言至英文（en）或日文（ja）。
  2. 進入創角紙娃娃選擇介面（`paperdoll_select_demo`）。
- **壞掉現象**：
  - 本輪修復的頂部分頁（Launch / Expansion、初期 / 拡張）與底部按鈕（Confirm Selection · Begin Journey / Back 等）已成功翻譯。
  - 但種族橫條卡片名稱（「白金兔」、「靈尾狐」、「烈焰虎」等）以及右側槽位標題（「外裝服飾槽」、「軀體塗裝槽」、「手持武器槽」）、狀態列（「7 大槽位狀態：512 高清合成就緒」）**仍顯示繁體中文**（見 `proof_08`、`proof_09`、`proof_11`、`proof_12`）。
- **根本原因**：
  `t_9409c5c5` 任務範疇專注於頂部分頁與底部確認鈕的六語系落地，`paperdoll_select_demo.gd` 內部的種族標籤與槽位控制器文字採用了硬編碼中文，尚未納入全量 i18n 清單。
- **修復建議**：
  建議製作人後續開單為 `paperdoll_select_demo.gd` 之種族名稱卡片與槽位描述文字接入 `Loc.t()`。

---

## 四、 驗收指令執行紀錄

- `godot --path game --headless --quit-after 3`：**0 SCRIPT ERROR**（通過）。
- `TEST_FILTER=wardrobe ./tools/run_tests.sh`：**3/3 PASSED**（含 `test_paperdoll_wardrobe_save`、`test_wardrobe_thumbnails`、`test_wardrobe_i18n`）。
- `TEST_FILTER=creation ./tools/run_tests.sh`：**5/5 PASSED**（含 `test_paperdoll_creation_breathe`、`test_character_creation_flow`、`test_creation_race_tabs`、`test_creation_stage_no_128_fallback`、`test_creation_tabs_i18n`）。
- **Vision 逐張審查**：全數 15 張實機全景截圖與特寫裁剪均已親自由 Vision 模型完成視覺審驗與缺陷定位。
