# 《發條之心》ShopDialog 商城彈窗底部新增前往聚魂與前往鍛造快捷果凍按鈕 驗收檢查清單 (t_29493bde)

## 任務背景與目標
- **任務編號**：t_29493bde
- **功能描述**：
  1. 在 `ShopDialog`（`shop_dialog.gd`）商城彈窗底部 `FooterBar`，在既有『前往背包』按鈕旁新增『前往聚魂』（`BtnGoSoulHall`）與『前往鍛造』（`BtnGoForge`）立體果凍按鈕，三按鈕居中並列。
  2. 按鈕規格：熱區高度 52px（>= 50px，符合手機觸控熱區 >= 48px 規範），寬度 160px（150~160px 規範），果凍厚底 5px，圓角 18px，字級 17px 開源粉圓體（OpenHuninn），零系統 Emoji。
     - `BtnGoInventory`：薄荷綠 `#4ED86A`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
     - `BtnGoSoulHall`：珊瑚粉 `#FF5E8A`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
     - `BtnGoForge`：金黃色 `#FFD028`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
  3. 點擊連動：
     - 點擊 `BtnGoSoulHall` 發射 `go_soul_hall` 與 `soul_hall_requested` 訊號，安全關閉商城彈窗，連動大廳切換至聚魂殿堂（`MobileLobby.open_soul_hall()`）。
     - 點擊 `BtnGoForge` 發射 `go_forge` 與 `forge_requested` 訊號，安全關閉商城彈窗，連動大廳開啟天宮鐵匠（`MobileLobby.open_forge()`）。
  4. 提供存取器 `get_go_inventory_button()`, `get_go_soul_hall_button()`, `get_go_forge_button()`。
  5. 支援六語系 i18n 即時切換（zh_TW, zh_CN, en, ja, ko, es），新增鍵值：
     - `shop.btn_go_soul_hall`（繁中：前往聚魂，簡中：前往聚魂，en：Go to Soul Hall，ja：聚魂殿へ進む，ko：혼령전으로 이동，es：Ir a Sala de Almas）
     - `shop.btn_go_forge`（繁中：前往鍛造，簡中：前往锻造，en：Go to Forge，ja：鍛冶屋へ進む，ko：대장간으로 이동，es：Ir a la Forja）
  6. 撰寫自動化單元與整合測試 `test_shop_shortcuts.gd` 並產出 8 張真實 OpenGL3 實機截圖存證至 `proofs/t_29493bde/`，驗證 SHA256 互異獨立。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | 三按鈕尺寸皆為 `Vector2(160, 52)`，高度 52px >= 50px，熱區充足；字級 17px，彈窗卡片寬度 750px、高度 580px 居中於 720px 畫面，無溢出無遮擋。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 彈窗底部 `FooterBar` 居中並列三顆果凍按鈕（前往背包、前往聚魂、前往鍛造），左右間距 12px，全寬 504px < 750px，留白充足，各語系文字完整無穿框。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 全語系下按鈕純淨文字渲染，零 Unicode 系統 Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 薄荷綠 `#4ED86A`、珊瑚粉 `#FF5E8A`、金黃 `#FFD028`，深藍紫描邊 `#1F1A3A`，厚底 5px，圓角 18px，視覺標準完全對齊。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run godot` 產生 8 張真實 Framebuffer 截圖，8 張 SHA256 互異獨立（0 重複）。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試覆蓋按鈕規格、六語系即時切換、點擊聚魂直達、點擊鍛造直達、彈窗銷毀、大廳開啟與哨兵 `TEST_SHOP_SHORTCUTS_OK`。 |
| **程式與邏輯** | 跳轉與子模式參數有效對齊、無縫連動聚魂殿堂與鐵匠 | ✅ 已檢查 | 點擊 `BtnGoSoulHall` 直達 `open_soul_hall()`，點擊 `BtnGoForge` 直達 `open_forge()`，且安全清理 `ShopDialog` 避免殘留遮罩。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全齊全，世界觀名詞完全符合，零「今日村莊」等舊詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check .` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_29493bde/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_shop_three_shortcuts_zh_TW.png` | 商城彈窗底部展示三果凍按鈕並列（前往背包、前往聚魂、前往鍛造，繁中） | `c87b0b287c72aaaf` | PASS，居中並列，綠/粉/黃三色鮮明，文字與描邊清晰，留白合理，零 Emoji |
| `proof_02_shop_shortcuts_en.png` | 三快捷按鈕即時切換為英文 `Go to Inventory`, `Go to Soul Hall`, `Go to Forge` | `095c2265828fd586` | PASS，純英文字體排版完整，零 CJK 殘留，零 Emoji |
| `proof_03_shop_shortcuts_ja.png` | 三快捷按鈕即時切換為日文 `インベントリへ進む`, `聚魂殿へ進む`, `鍛冶屋へ進む` | `aec1d8fa3700cbae` | PASS，日文顯示完整無缺字，零 Emoji |
| `proof_04_shop_shortcuts_ko.png` | 三快捷按鈕即時切換為韓文 `인벤토리로 이동`, `혼령전으로 이동`, `대장간으로 이동` | `72386108eac1ceaf` | PASS，韓文顯示完整無缺字，零 Emoji |
| `proof_05_shop_shortcuts_es.png` | 三快捷按鈕即時切換為西文 `Ir al Inventario`, `Ir a Sala de Almas`, `Ir a la Forja` | `3841dee870a7e45b` | PASS，西文顯示完整無缺字，零 CJK 殘留，零 Emoji |
| `proof_06_shop_shortcuts_zh_CN.png` | 三快捷按鈕即時切換為簡中 `前往背包`, `前往聚魂`, `前往锻造` | `f68f8b0a28084683` | PASS，簡體中文顯示正確，零 Emoji |
| `proof_07_click_go_soul_hall_opens_soul_hall.png` | 點擊前往聚魂即時關閉商城彈窗並直達聚魂殿堂（Tab.SOUL_HALL） | `d04a93f9beaf24b3` | PASS，商城彈窗已完全關閉，聚魂殿堂導航高亮選中，封靈罐四階主介面清晰顯示，動線閉環 |
| `proof_08_click_go_forge_opens_forge_dialog.png` | 點擊前往鍛造即時關閉商城彈窗並直達天宮鐵匠彈窗（ForgeDialog） | `a8ebf29054830512` | PASS，商城彈窗已完全關閉，天宮鐵匠彈窗正常開啟，裝備與機芯鍛造動線閉環 |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元與整合測試**：`godot --path game --headless -s res://scripts/ui/test_shop_shortcuts.gd` -> **PASS (`TEST_SHOP_SHORTCUTS_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game -s res://scripts/ui/test_shop_shortcuts.gd` -> **PASS (8 獨立雜湊截圖)**
- **既有測試回歸**：
  - `test_shop_inventory_shortcut.gd` -> **PASS (`TEST_SHOP_INVENTORY_SHORTCUT_OK`)**
  - `test_shop_dialog.gd` -> **PASS (`SHOP_DIALOG_OK`)**
  - `test_soul_hall_inventory_shortcut.gd` -> **PASS (`SOUL_HALL_INVENTORY_SHORTCUT_TEST_OK`)**
- **自動合規檢查**：`clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_29493bde/bravesoul-game` -> **PASS (✅ 全過)**
