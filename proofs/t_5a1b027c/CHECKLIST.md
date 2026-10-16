# 全面回歸驗收存證 · 把已過審的儲能庫前往委託與稱號牆前往背包雙分支合進主線 (t_5a1b027c)

## 任務目標
1. 將通過測試審查（測試小婷 `sideqa` 完成獨立審查簽核通過）之兩張快捷功能分支合併進 `main` 主線：
   - `agent/20261015-clockwork-vault-windup-shortcut-t_e54083c8` (ClockworkVaultDialog 前往委託快捷果凍按鈕聯動 WindupDailyDialog)
   - `agent/20261015-title-wall-inventory-shortcut-t_e56c4603` (TitleWallDialog 前往背包快捷果凍按鈕聯動探索背包 MapleInventory)
2. 解決多語系字典與專案狀態衝突，確保 main 分支乾淨 merge 兩個分支，無任何衝突與遺漏。
3. 執行全域自動化測試與回歸：
   - `clock-check /opt/side/bravesoul-game` 確認無缺 .import、0 軟連結、語系 key 齊全、無退役名詞。
   - `godot --path game --headless --quit-after 3` 零 SCRIPT ERROR (exit 0)。
   - 相關單元與回歸測試全綠（`test_clockwork_vault` 3/3、`test_title_wall` 5/5、`test_lobby` 15/15、`test_windup` 7/7、`test_maple_inventory` 18/18、`test_vault_title_dual_shortcuts_regression.gd` 全數跑綠）。
4. 更新 `docs/PROJECTS.json`：
   - `vault-windup-shortcut`：`測試中` → `已上線`
   - `title-wall-inventory-shortcut`：`測試中` → `已上線`
   - `merge-vault-title-shortcuts`：`草稿` → `已上線`
5. 實機截圖存證於 `proofs/t_5a1b027c/`（6 張 1280x720 獨立唯一截圖）。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經渲染驗證，ClockworkVaultDialog 與 TitleWallDialog 底欄快捷按鈕正常呈現，排版合理、文字無穿框、無遮擋。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoWindup` (115x52px) 與 `BtnGoInventory` (150x52px) 高度皆為 52px (>= 48px)，熱區充足；字級 16~18px 開源粉圓體加深藍紫描邊，對比度充足且 100% 零系統 Emoji。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 經 `clock-check` 確認，工作區無軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 6 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經檢驗無黑屏、無遮罩殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化執行 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 10~20 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_clockwork_vault` (3/3)、`test_title_wall` (5/5)、`test_lobby` (15/15)、`test_windup` (7/7)、`test_maple_inventory` (18/18) 測試全綠，`test_vault_title_dual_shortcuts_regression.gd` 成功輸出哨兵並通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoWindup` 或 `BtnGoInventory` 皆能順利發射對應請求訊號並安全關閉原彈窗，大廳平滑開啟目標彈窗。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 分別測試由儲能庫前往每日委託（WindupDailyDialog）與由稱號牆前往探索背包（MapleInventory），彈窗連動跳轉順暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系（zh_TW, zh_CN, en, ja, ko, es）字典皆齊備，英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `vault-windup-shortcut` 與 `title-wall-inventory-shortcut` 以及維運項目已透過更新推進至「已上線」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 乾淨合併雙分支，所有檔案完整 commit。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_clockwork_vault_with_btn_go_windup.png` | 繁中發條儲能庫：底欄六按鈕並列，暖橘色『前往委託』快捷按鈕正常顯示 | 1280x720 | `e5174da13d9525a70ae8fd4655676946f7c1bca42c4e84f71c57a6e45be39d24` |
| 02 | `proof_02_vault_click_go_windup_opens_windup_daily.png` | 點擊前往委託：直通開啟 WindupDailyDialog 冒險委託彈窗，底層無遮罩殘留 | 1280x720 | `f5a748a37939c0c930106c3084a3c0d62d857438d409e28a8f834892f497e289` |
| 03 | `proof_03_title_wall_with_btn_go_inventory.png` | 繁名稱號牆：底欄新增薄荷綠『前往背包』快捷果凍按鈕正常顯示 | 1280x720 | `476d2c9b8be6584d621f339ee20eb67e83cf1b837f09eb45b2d1be1e1706d2d6` |
| 04 | `proof_04_title_wall_click_go_inventory_opens_maple_inventory.png` | 點擊前往背包：直通開啟 MapleInventory 探索背包，底層無遮罩殘留 | 1280x720 | `ca0ac1e61f53d5c8504d12f859c217984ce421190c9bb2de06867db929b4c21e` |
| 05 | `proof_05_vault_windup_locale_ja.png` | 日文語系儲能庫展示：按鈕文本『日課へ』正常顯示 | 1280x720 | `0c59ad32f11e15f524fe7a168acde9ef2c2932510c941b61cef16879a77bc56b` |
| 06 | `proof_06_title_wall_inventory_locale_en.png` | 英文語系稱號牆展示：按鈕文本 \"To Inventory\" 正常顯示，零 CJK 殘留 | 1280x720 | `7ed4021434fb1f1cd0029416391481d8e0d315bf05d7ca6674727bcf74797e81` |
