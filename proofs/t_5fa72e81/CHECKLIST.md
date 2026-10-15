# 全面回歸驗收存證 · 把已過審的每日委託前往背包與前往儲能庫雙分支合進主線 (t_5fa72e81)

## 任務目標
1. 將通過測試審查（測試小婷 `sideqa` 完成獨立審查簽核通過）之兩張每日委託快捷功能分支合併進 `main` 主線：
   - `agent/20261015-windup-daily-inventory-shortcut-t_ca80ffb9` (WindupDailyDialog 前往背包快捷果凍按鈕聯動探索背包 MapleInventory)
   - `agent/20261015-windup-daily-vault-shortcut-t_44ba96c6` (WindupDailyDialog 前往儲能庫快捷果凍按鈕聯動發條儲能庫 ClockworkVaultDialog)
2. 解決多語系字典與專案狀態衝突，確保 main 分支乾淨 merge 兩個分支，無任何衝突與遺漏。
3. 執行全域自動化測試與回歸：
   - `clock-check /opt/side/bravesoul-game` 確認無缺 .import、0 軟連結、語系 key 齊全、無退役名詞。
   - `godot --path game --headless --quit-after 3` 零 SCRIPT ERROR (exit 0)。
   - 相關單元與回歸測試全綠（`test_windup_daily_inventory_shortcut.gd`、`test_windup_daily_vault_shortcut.gd`、`test_windup_daily_dual_shortcuts.gd`、`test_windup` 9/9 支全數跑綠）。
4. 更新 `docs/PROJECTS.json`：
   - `windup-inventory-shortcut`：`測試中` → `已上線`
   - `windup-vault-shortcut`：`測試中` → `已上線`
   - `merge-windup-shortcuts`：`草稿` → `已上線`
5. 實機截圖存證存證於 `proofs/t_5fa72e81/`（9 張 1280x720 獨立唯一截圖）。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經渲染驗證，每日委託底欄按鈕列在完成狀態下，『離開委託』、『前往戰力』、『前往背包』、『前往儲能庫』、『前往出征』、『前往停擺巨偶』並列呈現，間距合理、文字無穿框、無遮擋。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoInventory` (120x52px) 與 `BtnGoVault` (120x52px) 高度皆為 52px (>= 50px)，熱區充足；字級 16px 開源粉圓體加深藍紫描邊，對比度充足且 100% 零系統 Emoji。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 經 `clock-check` 確認，工作區無軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 9 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經檢驗無黑屏、無遮罩殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化執行 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 3~8 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_windup` 相關 9 支測試全綠，`test_windup_daily_dual_shortcuts.gd` 成功輸出哨兵並通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoInventory` 或 `BtnGoVault` 皆能順利發射對應請求訊號與 `closed` 訊號，彈窗安全銷毀 (`queue_free()`)，大廳平滑開啟目標彈窗。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 分別測試前往探索背包（MapleInventory）與前往發條儲能庫（ClockworkVaultDialog），彈窗連動跳轉順暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系（zh_TW, zh_CN, en, ja, ko, es）字典皆齊備，英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `windup-inventory-shortcut` 與 `windup-vault-shortcut` 以及維運項目已透過 `project_status.py` 推進至「已上線」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 乾淨合併雙分支，所有檔案完整 commit。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_windup_daily_completed_dual_shortcuts_zh_TW.png` | 繁中委託完成狀態：底欄六按鈕並列，前往背包與前往儲能庫雙果凍按鈕並列正常顯示 | 1280x720 | `7106fd950a2f54f234d4286ddac814505b62ba2eb7608ad4daa5293375eaf825` |
| 02 | `proof_02_click_go_inventory_opens_maple_inventory.png` | 點擊前往背包：直通開啟 MapleInventory 探索背包，底層無遮罩殘留 | 1280x720 | `e6137fae5e0fd6a52cdd798eaf0a9bfbc01aa05acf2bc6742ffcb62ad5a639f1` |
| 03 | `proof_03_click_go_vault_opens_clockwork_vault.png` | 點擊前往儲能庫：直通開啟 ClockworkVaultDialog 放置收益彈窗，底層無遮罩殘留 | 1280x720 | `997552549bd2fbb7f0d8092d6a9ff279248e88aec67db4b18e8ab9799aab0651` |
| 04 | `proof_locale_zh_TW_dual_shortcuts.png` | 繁中語系切換刷新：『前往背包』與『前往儲能庫』 | 1280x720 | `7d5243085fd9df91dccb1035deec99e0866405f1b12077bcf0fa6420d5df729a` |
| 05 | `proof_locale_zh_CN_dual_shortcuts.png` | 簡中語系切換刷新：『前往背包』與『前往储能库』 | 1280x720 | `258c9f7a952392e5af5d357c636737d9b07905a9cf729eac9ed538af6e606092` |
| 06 | `proof_locale_en_dual_shortcuts.png` | 英文語系切換刷新：\"To Inventory\" 與 \"To Vault\"，零 CJK 殘留 | 1280x720 | `7a3f3da142c80ca03ab3a91a5e39dc6fa6805b7bffdac827049627d56d47e21f` |
| 07 | `proof_locale_ja_dual_shortcuts.png` | 日文語系切換刷新：『バッグへ』與『貯蔵庫へ』 | 1280x720 | `5d3bf25074ab2ba72ef2ddf8e7b34391d2f2e0720176d71f9f753f3d347f4333` |
| 08 | `proof_locale_ko_dual_shortcuts.png` | 韓文語系切換刷新：『가방으로 이동』與『저장고로 이동』 | 1280x720 | `497cc62726347276023a1224fef5784b30360c97e7177535b825f2e9868a23a2` |
| 09 | `proof_locale_es_dual_shortcuts.png` | 西文語系切換刷新：\"Ir a Mochila\" 與 \"Ir a Bóveda\"，零 CJK 殘留 | 1280x720 | `fa5daaf159488dc8b91996e0b39414d68611e72d32d60e8c7393c1ed93f581be` |
