# 全面回歸驗收證明 · 把已過審的衣櫥前往背包與背包前往衣櫥雙分支合進主線回歸 (t_ac821efb)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成獨立審查驗收並簽核通過）之衣櫥與背包雙向快捷功能分支：
1. **`wardrobe-inventory-shortcut`（t_a1e49461）**：分支 `agent/20261016-wardrobe-inventory-shortcut-t_a1e49461`
   - `WardrobeDialog` 換裝衣櫥彈窗底欄按鈕列（`actions_hbox`）新增『前往背包』(`BtnGoInventory`) 快捷果凍按鈕
   - 規格：暖橘色盤 `#FFA010` (COLOR_ORANGE)、立體厚底 5px、圓角 18px、尺寸 105x50px（符合人體工學熱區 >= 48px 防誤觸規範）、100% 零系統 Emoji、開源粉圓體字型、深藍紫描邊 `#1F1A3A`
   - 連動：點擊後發出 `go_inventory` 與 `inventory_requested` 訊號並關閉衣櫥彈窗，大廳平滑開啟 `MapleInventory` 探索背包，無殘留遮罩
   - 存取器：`get_go_inventory_button() -> Button`、`get_inventory_button() -> Button`
   - 六語系支援：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 字典齊全
2. **`inventory-wardrobe-shortcut`（t_edd1109c）**：分支 `agent/20261016-inventory-wardrobe-shortcut-t_edd1109c`
   - `MapleInventory` 探索背包底欄快捷列（`GridBottomBar`）新增『前往衣櫥』(`BtnGoWardrobe`) 快捷果凍按鈕
   - 規格：暖橘色盤 `#FFA010` (COLOR_ORANGE)、立體厚底 5px、圓角 18px、尺寸 120x48px（符合熱區 >= 48px）、100% 零系統 Emoji、開源粉圓體字型、深藍紫描邊 `#1F1A3A`
   - 連動：點擊後發出 `go_wardrobe` 與 `wardrobe_requested` 訊號並關閉背包視窗，大廳平滑開啟 `WardrobeDialog` 換裝衣櫥彈窗，無殘留遮罩
   - 存取器：`get_go_wardrobe_button() -> Button`、`get_bag_go_wardrobe_button() -> Button`、`get_wardrobe_button() -> Button`
   - 六語系支援：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 字典齊全

由工程師阿宏（`sideworker`）在主線執行雙分支乾淨合併，解決多語系字典與 `PROJECTS.json` 衝突，執行全套無頭冒煙測試、關聯模組單元測試、官網 live 檢測與素材檢查，並透過 `project_status.py` 同步將兩項功能與合併維運項目標記為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **衣櫥前往背包單元測試** | `TEST_TIMEOUT=240 TEST_FILTER=test_wardrobe_inventory_shortcut ./tools/run_tests.sh` | PASS (1/1: TEST_WARDROBE_INVENTORY_SHORTCUT_OK) | **PASS** |
| **背包前往衣櫥單元測試** | `TEST_TIMEOUT=240 TEST_FILTER=test_maple_inventory_wardrobe_shortcut ./tools/run_tests.sh` | PASS (1/1: TEST_MAPLE_INVENTORY_WARDROBE_SHORTCUT_OK) | **PASS** |
| **雙快捷按鈕合併回歸測試** | `xvfb-run -a godot --path game --rendering-driver opengl3 --audio-driver Dummy -s res://scripts/ui/test_wardrobe_inventory_dual_shortcuts_regression.gd` | 規格、樣式、訊號、大廳連動、雙向閉環、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **衣櫥相關全套單元測試 (5支)** | `TEST_TIMEOUT=240 TEST_FILTER=test_wardrobe ./tools/run_tests.sh` | 全部 5 支測試 PASS (shortcut, title_wall, shop, power_stat, i18n) | **PASS** |
| **程式與素材合規檢查** | `clock-check /opt/side/bravesoul-game` | ✅ 全過：素材 0 缺 .import、0 軟連結、語系 key 齊全、無退役名詞（直接在 main 上做提示因本單為合併主線維運單） | **PASS** |

---

## 3. 實機截圖存證清單 (1280x720 OpenGL3，真實 Framebuffer 渲染)

### (1) 雙快捷合併後完整回歸存證 (`proofs/t_ac821efb/` 與 `docs/proofs/t_ac821efb/`, 6 張)
1. `proof_01_wardrobe_dialog_with_btn_go_inventory.png` (SHA256: `74dae0b81222cf6b1b2fcb6855ed80cbaa4718b2c5e3366e691372a9722da887`)：繁體中文換裝衣櫥彈窗底欄展示暖橘立體果凍按鈕『前往背包』(`BtnGoInventory`)
2. `proof_02_wardrobe_click_go_inventory_opens_maple_inventory.png` (SHA256: `833e477e7ab778b7bc69aa328b48f8e8570c89bb3bed51a808d191f20732ce69`)：點擊前往背包安全關閉衣櫥彈窗並直通開啟 `MapleInventory` 探索背包
3. `proof_03_maple_inventory_with_btn_go_wardrobe.png` (SHA256: `4109d15e86be6215ed89faf2109c62af1929cfc4e24c5497f428a934bdfeb42f`)：繁體中文探索背包底欄展示暖橘立體果凍按鈕『前往衣櫥』(`BtnGoWardrobe`)
4. `proof_04_inventory_click_go_wardrobe_opens_wardrobe_dialog.png` (SHA256: `9d4be712334a26da68abd71f4259d749d013546f61adeae0debd0496ab48ce08`)：點擊前往衣櫥安全關閉背包視窗並直通連動開啟 `WardrobeDialog`（完成雙向閉環連動驗證）
5. `proof_05_wardrobe_inventory_locale_ja.png` (SHA256: `2fdb8562db12168f8fea2b94781369c8a72652bc6367b4e0897deb79ff057dcf`)：日文語系衣櫥彈窗展示，按鈕文本 `バッグへ` 正常顯示
6. `proof_06_inventory_wardrobe_locale_en.png` (SHA256: `b9b5bb968719025e1af379fcd94f7d1c92577b9a944cc23e6a476ad7f9cb6120`)：英文語系探索背包視窗展示，按鈕文本 `To Wardrobe` 正常顯示，零 CJK 殘留

---

## 4. 專案狀態更新（docs/PROJECTS.json）
透過 `/root/project_status.py` 完成三項專案狀態推進：
- `wardrobe-inventory-shortcut`：`測試中` → `已上線`（雙分支合進 main 並完成全套回歸驗收 (t_ac821efb)）
- `inventory-wardrobe-shortcut`：`測試中` → `已上線`（雙分支合進 main 並完成全套回歸驗收 (t_ac821efb)）
- `merge-wardrobe-inventory`：`開發中` → `已上線`（雙分支合進 main 並完成全套回歸驗收 (t_ac821efb)）

---

## 5. 驗收標準對照 CHECKLIST
- [x] **無退役名詞、無缺 .import、路徑正常**：`clock-check /opt/side/bravesoul-game` 通過
- [x] **0 SCRIPT ERROR**：無頭引擎冒煙測試通過 (exit 0)
- [x] **無語系衝突與死 key**：六語系 12 處字典全數齊全
- [x] **相關測試全綠**：test_wardrobe_inventory_shortcut, test_maple_inventory_wardrobe_shortcut, test_wardrobe_inventory_dual_shortcuts_regression, test_wardrobe (5/5)
- [x] **存證截圖與查核表齊備**：`proofs/t_ac821efb/` 6 張實機截圖與 `CHECKLIST.md`、`docs/proofs/t_ac821efb.md`
- [x] **遵守 review.md 規範**：雙分支完整乾淨合併，無任何功能退化或衝突
