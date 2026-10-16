# 全面回歸驗收證明 · 把已過審的商城前往儲能庫、委託前往商城與商城前往委託三分支合進主線 (t_fa68c3d2)

## 1. 任務背景與驗收目標
將已通過測試審查（測試小婷 `sideqa` 完成獨立審查驗收並簽核通過）之三個快捷功能分支乾淨合併至 main 主線：
1. **`shop-vault-shortcut` (t_53a8b616)**：分支 `agent/20261016-shop-dialog-vault-shortcut-t_53a8b616` (commit 5ffd9b04b)
   - `ShopDialog` (商城彈窗) 底欄新增『前往儲能庫』(`BtnGoVault`) 快捷果凍按鈕連動 `ClockworkVaultDialog`
   - 規格：多巴胺金黃色盤 `#FFD028`、立體厚底 5px、圓角 18px、尺寸 140x50px（熱區 >= 48px 防誤觸）、100% 零系統 Emoji、開源粉圓體字型、深藍紫描邊與文字 `#1F1A3A`
   - 存取器：`get_go_vault_button()`、信號：`vault_requested`、`go_vault`
2. **`windup-shop-shortcut` (t_18b92637)**：分支 `agent/20261016-windup-daily-shop-shortcut-t_18b92637` (commit fe2ee9df4)
   - `WindupDailyDialog` (冒險委託每日上發條) 底欄新增『前往商城』(`BtnGoShop`) 快捷果凍按鈕連動 `ShopDialog`
   - 規格：多巴胺暖橘色盤 `#FFA010`、立體厚底 5px、圓角 18px、尺寸 98x52px（熱區 >= 48px 防誤觸）、100% 零系統 Emoji、開源粉圓體字型、深藍紫描邊與文字 `#1F1A3A`
   - 存取器：`get_go_shop_button()`、信號：`shop_requested`、`go_shop`
3. **`shop-windup-shortcut` (t_ec3adc60)**：分支 `agent/20261016-shop-dialog-daily-shortcut-t_ec3adc60` (commit 67673ccf7)
   - `ShopDialog` (商城彈窗) 底欄新增『前往委託』(`BtnGoWindupDaily`) 快捷果凍按鈕連動 `WindupDailyDialog`
   - 規格：多巴胺暖橘色盤 `#FFA010`、立體厚底 5px、圓角 18px、尺寸 150x50px（熱區 >= 48px 防誤觸）、100% 零系統 Emoji、開源粉圓體字型、深藍紫描邊與文字 `#1F1A3A`
   - 存取器：`get_go_windup_daily_button()`、信號：`windup_daily_requested`、`go_windup_daily`

由工程師阿宏（`sideworker`）在主線執行三分支乾淨合併，解決多語系字典與 `PROJECTS.json` 衝突，執行全套專屬測試與主線批次回歸測試，並透過 `project_status.py` 同步將三項功能與本合併任務標記為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---|
| **商城前往儲能庫單元測試** | `./tools/run_tests.sh (filter: test_shop_dialog_vault_shortcut.gd)` | PASS (TEST_SHOP_VAULT_SHORTCUT_OK) | **PASS** |
| **委託前往商城單元測試** | `./tools/run_tests.sh (filter: test_windup_daily_shop_shortcut.gd)` | PASS (TEST_WINDUP_DAILY_SHOP_SHORTCUT_OK) | **PASS** |
| **商城前往委託單元測試** | `./tools/run_tests.sh (filter: test_shop_dialog_daily_shortcut.gd)` | PASS (TEST_SHOP_DAILY_SHORTCUT_OK) | **PASS** |
| **商城基準單元測試** | `./tools/run_tests.sh (filter: test_shop_dialog.gd)` | PASS (SHOP_DIALOG_OK) | **PASS** |
| **委託各快捷回歸測試** | `./tools/run_tests.sh (filter: test_windup_power_stat_shortcut / test_windup_daily_inventory_shortcut / test_windup_daily_vault_shortcut)` | 全數 PASS | **PASS** |
| **主線三快捷批次回歸測試** | `./tools/run_tests.sh (filter: test_batch_three_shortcuts_t_fa68c3d2.gd)` | 規格、樣式、訊號、熱區、六語系即時切換全部 PASS (TEST_BATCH_THREE_SHORTCUTS_REGRESSION_OK) | **PASS** |
| **無頭冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR / 0 Crash | **PASS** |
| **程式與素材合規檢查** | `clock-check /opt/side/bravesoul-game` | 缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留 | **PASS** |

---

## 3. 實機截圖存證清單
存證檔案置於 `proofs/t_fa68c3d2/` 與 `docs/proofs/t_fa68c3d2/`：
1. `01_shop_with_btn_go_vault.png`：ShopDialog 商城底欄展示多巴胺金黃果凍按鈕『前往儲能庫』(`BtnGoVault`)。
2. `02_vault_opened_from_shop.png`：從 ShopDialog 點擊『前往儲能庫』順暢直通開啟 ClockworkVaultDialog 發條儲能庫放置收益視窗。
3. `03_windup_daily_with_btn_go_shop.png`：WindupDailyDialog 冒險委託底欄展示多巴胺暖橘果凍按鈕『前往商城』(`BtnGoShop`)。
4. `04_shop_opened_from_windup_daily.png`：從 WindupDailyDialog 點擊『前往商城』順暢連動開啟 ShopDialog。
5. `05_shop_with_btn_go_windup_daily.png`：ShopDialog 商城底欄展示多巴胺暖橘果凍按鈕『前往委託』(`BtnGoWindupDaily`)。
6. `06_windup_daily_opened_from_shop.png`：從 ShopDialog 點擊『前往委託』順暢直通開啟 WindupDailyDialog。
7. `07_loop_back_to_shop_dialog.png`：雙向閉環流暢返回 ShopDialog 商城彈窗，無任何遮罩殘留或死拍。

---

## 4. 專案狀態更新（docs/PROJECTS.json）
透過 `/root/project_status.py` 完成四項專案狀態推進至『已上線』：
- `shop-vault-shortcut`：`測試中` → `已上線`
- `windup-shop-shortcut`：`測試中` → `已上線`
- `shop-windup-shortcut`：`測試中` → `已上線`
- `merge-shop-vault-windup-shortcuts`：`草稿` → `已上線`
