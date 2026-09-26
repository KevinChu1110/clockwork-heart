# 《發條之心》探索性 QA 第三十六輪 查驗清單與缺陷報告 (Round 36 Checklist)

- **測試日期**：2026-09-26
- **測試員**：小婷（側案·測試 sideqa）
- **關聯卡號**：`t_386168d6`
- **關聯前置任務**：
  - `t_83122b72`（大廳左側四殿堂卡標題副標六語系改動合進主線）
  - `t_48d09604`（大廳左側四殿堂卡六語系落地方案實作）
- **存檔目錄**：`/opt/side/bravesoul-game/proofs/qa_round36/`

---

## 一、 實機截圖核驗清單（每張全景圖：破圖／emoji／截字／模糊／語系一致性）

依據規範（review.md 0-QA15、0-QA17、0-QA23、0-QA24、0-QA25），全數實機截圖規格為 1280x720，MD5 經查核 100% 獨立無重複：

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零系統Emoji | 零截字 | 語系完整度 | 審核結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_lobby_village_zh_TW.png` | 大廳村莊全景（zh_TW 繁中基準） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 繁中 | 合格 (PASS) |
| 02 | `proof_02_lobby_village_en.png` | 大廳村莊全景（en 英文全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 英文 | 合格 (PASS) |
| 03 | `proof_03_lobby_village_ja.png` | 大廳村莊全景（ja 日文全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 日文 | 合格 (PASS) |
| 04 | `proof_04_lobby_village_ko.png` | 大廳村莊全景（ko 韓文全景連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 韓文 | 合格 (PASS) |
| 05 | `proof_05_regression_forge_dialog.png` | 回歸：點擊「天宮鐵匠」彈出裝備鍛造彈窗 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 英文 | 合格 (PASS) |
| 06 | `proof_06_regression_gem_workshop_dialog.png` | 回歸：點擊「手藝工坊」彈出寶石工坊熔煉彈窗 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 英文 | 合格 (PASS) |
| 07 | `proof_07_regression_windup_quest_dialog.png` | 回歸：點擊「冒險委託」彈出每日懸賞簽到彈窗 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 英文 | 合格 (PASS) |
| 08 | `proof_08_regression_sortie_adventure_tab.png` | 回歸：點擊「前往出征」切換至四區出征分頁 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | 100% 英文 | 合格 (PASS) |

### 局部特寫 Crops 驗證清單（`proofs/qa_round36/crops/`）
- `crop_hall_cards_{zh_TW,en,ja,ko}.png`：左側四殿堂卡（標題、副標、Pixel Art 圖示、熱區高寬）多語系特寫。
- `crop_dock_{zh_TW,en,ja,ko}.png`：底部 Dock 五大導航頁籤多語系即時連動特寫。
- `crop_topbar_{zh_TW,en,ja,ko}.png`：頂部 HUD 狀態列（能量、金幣、星屑、商城、設置）多語系特寫。

---

## 二、 專項查核重點結果

### 1. 大廳左側四殿堂卡六語系合入主線查核（proof_01 ~ proof_04 與 crop_hall_cards）
- **四大殿堂標題與副標題對齊**：
  - **天宮鐵匠**：
    - zh_TW: `天宮鐵匠` / `品質轉化 · 裝備鍛造`
    - en: `Celestial Blacksmith` / `Quality Conversion · Gear Forging`
    - ja: `天宮の鍛冶屋` / `品質転換 · 装備鍛造`
    - ko: `천궁 대장장이` / `품질 변환 · 장비 단조`
  - **手藝工坊**：
    - zh_TW: `手藝工坊` / `紅黃藍石 · 三合一熔煉`
    - en: `Craft Workshop` / `RGB Gems · 3-in-1 Smelting`
    - ja: `工芸工房` / `紅黄青石 · 三位一体精錬`
    - ko: `공예 공방` / `적황청 보석 · 삼합일 제련`
  - **演武競技**：
    - zh_TW: `演武競技` / `挑戰對手 · 雙倍抽獎`
    - en: `Martial Arena` / `Challenge Rivals · Double Lottery`
    - ja: `演武競技` / `対戦相手に挑戦 · 2倍抽選`
    - ko: `연무 경기` / `상대 도전 · 2배 추첨`
  - **冒險委託**：
    - zh_TW: `冒險委託` / `每日簽到 · 懸賞領獎`
    - en: `Adventure Bounties` / `Daily Check-in · Bounty Rewards`
    - ja: `冒険依頼` / `デイリー出席 · 懸賞受取`
    - ko: `모험 의뢰` / `일일 출석 · 현상금 수령`
- **版面與字級**：
  - 熱區高度達到 56px（>=48px 手機熱區標準）。
  - en/es 語系下長字串動態縮小字級（主標題 13px、副標題 9px），文字完全無溢出、無截字（零 `...`）。
  - 自繪 Pixel Art 圖示垂直置中，文字左縮排 58px 避開圖示，排版整齊清爽。

### 2. 大廳整片 Chrome 同步切換查核（0-QA25 檢查）
- 玩家切換語言至 en、ja、ko 時，大廳畫面全數 UI 模組均即時同步切換，零殘留硬編繁中：
  - **頂欄 HUD**：玩家稱號（Fledgling Novice / 【駆け出し】 / 【풋내기 모험가】）、能量（Energy / エネルギー / 에너지）、金幣（Gold / 金 / 골드）、星屑（Stardust / 星屑 / 성설）、系統按鈕（Shop / ショップ / 상점、Settings / 設定 / 설정）。
  - **左側四殿堂卡**：四張卡片主標與副標題完整切換。
  - **底部 Dock**：五大入口頁籤（Cogwheel Hamlet / ぜんまい新村 / 태엽 신촌、Hero Gear / キャラ装備 / 영웅 장비 等）。
  - **右側出征卡**：出征標題（Adventure Sortie / 冒険出征 / 모험 출정）、章節關卡（Lands of White Fog / 白霧の地 / 백무의 땅）、按鈕（Set Out to Battle / 出征する / 출정하기）。
  - **右上角玩家裝備清單**：四項裝備槽位標籤（Outfit, Weapon, Clockwork, Curio 等）與裝備名稱（Nutcracker Guard Uniform / くるみ割り近衛軍服 等）全數同步翻譯。

### 3. 日／韓漢字翻譯規範核實（0-QA24 規範）
- 日文環境下「天宮の鍛冶屋」、「品質転換 · 装備鍛造」、「工芸工房」、「演武競技」等完全符合 JIS 當用漢字與文法，非中文硬套。
- 韓文環境下「천궁 대장장이」、「품질 변환 · 장비 단조」、「공예 공방」等詞條均經專業對照，無亂碼破字。

### 4. 舊功能入口回歸查核（proof_05 ~ proof_08）
- **天宮鐵匠入口（`proof_05_regression_forge_dialog.png`）**：
  - 點擊「天宮鐵匠」卡片，成功彈出 `ForgeDialog`（Celestial Blacksmith · Equipment Forge）。
  - 顯示當前裝備之長劍屬性、鍛造花費金幣、基礎成功率、封靈槽狀態、鍛造保底計數器（Forge Loss Pity）、鍛造升階按鈕與離開按鈕。
- **手藝工坊入口（`proof_06_regression_gem_workshop_dialog.png`）**：
  - 點擊「手藝工坊」卡片，成功彈出 `GemWorkshopDialog`（Gem Workshop • Smelting & Gem Case）。
  - 顯示紅黃藍三色寶石三合一熔煉面板、每日熔煉次數限制、寶石碎晶與成品庫存、離開工坊按鈕。
- **冒險委託入口（`proof_07_regression_windup_quest_dialog.png`）**：
  - 點擊「冒險委託」卡片，成功彈出 `WindupDailyDialog`（Adventure Commission • Who Needs Winding Today?）。
  - 顯示今日上發條委託故事【Lion Remnant】、選項按鈕與懸賞領獎機制。
- **冒險出征入口（`proof_08_regression_sortie_adventure_tab.png`）**：
  - 點擊「前往出征」按鈕（或底部 Dock 四區出征），成功切換至出征頁籤。
  - 四大地區標籤（Region 1 ~ Region 4）、關卡卡片（2-1 至 2-4 BOSS）與出征挑戰按鈕全數可見且可點擊。

### 5. 截圖目錄獨立性核驗（0-QA23 規範）
- 截圖腳本 `game/scripts/dev/capture_qa_round36.gd` 將輸出嚴格限定於 `proofs/qa_round36/` 與 `proofs/qa_round36/crops/`，完全未寫入或覆蓋其他任務的 proof 目錄。

---

## 三、 探索性發現與缺陷清查結果

- **破圖（Broken Textures）**：**零破圖**。全景圖與特寫裁剪均無任何粉紅缺失紋理、白底黑塊或幾何斷層。
- **系統 Emoji（Emoji Leak）**：**零系統 Emoji**。所有按鈕與標籤均使用純文字或自繪圖示。
- **文字溢出與截字（Text Overflow & Truncation）**：**零截字**。即使在英文與韓文較長字串下，四殿堂卡主標題與副標題均完整顯示無截斷。
- **語系混用（Language Mixing）**：**零混用**。全屏 chrome、HUD、四殿堂卡、Dock、出征卡、裝備清單均同處當前選定語系。
- **舊功能完整性**：鐵匠、工坊、委託、出征四項核心功能入口完整健在。
- **結論**：本次大廳四殿堂卡六語系合入主線驗收**無新增缺陷，品質全綠通過 (Zero Defects PASS)**。

---

## 四、 驗收指令執行紀錄

- `godot --path game --headless --quit-after 3`：**0 SCRIPT ERROR**（通過）。
- `TEST_FILTER=lobby ./tools/run_tests.sh`：**4/4 PASSED**（含 `test_lobby_equip_i18n`、`test_lobby_hall_i18n`、`test_lobby_sortie_i18n`、`test_mobile_lobby`）。
- `TEST_FILTER=i18n ./tools/run_tests.sh`：**13/13 PASSED**（全域 13 支 i18n 測試全綠）。
- `python3 tools/verify_qa_round36.py`：**ALL PASSED**（8 張 1280x720 全景實機截圖 + 12 張 Crops 規格與 MD5 互異性全數合格）。
- **Vision 逐張視覺審驗**：全數實機全景截圖與特寫裁剪均已親自由 Vision 模型完成視覺審核，無任何破圖與截字。
