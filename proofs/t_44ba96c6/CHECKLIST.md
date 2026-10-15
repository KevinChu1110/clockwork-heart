# WindupDailyDialog 冒險委託每日上發條新增『前往儲能庫』快捷果凍按鈕連動 ClockworkVaultDialog 驗收存證 (t_44ba96c6)

## 任務目標
1. 在 `WindupDailyDialog` (`game/scripts/ui/windup_daily_dialog.gd`) 每日委託完成狀態下（底部按鈕列中），新增『前往儲能庫』(`BtnGoVault`) 快捷果凍按鈕。
2. 點擊後發射 `vault_requested` 與 `closed` 訊號並自動關閉彈窗 (`queue_free()`)，大廳 `MobileLobby` (`game/scripts/ui/mobile_lobby.gd`) 接到後平滑連動開啟 `ClockworkVaultDialog` 發條儲能庫放置收益彈窗。
3. 按鈕尺寸與視覺規範：
   - 位於 `FootButtons` 底部按鈕列，與『離開委託』、『前往戰力』、『前往背包』、『前往出征』/『前往停擺巨偶』並列。
   - 按鈕高度 52px (>= 50px 手機端熱區)，熱區寬度 >= 120px (實測 120~130px)。
   - 多巴胺天藍色盤 (`COLOR_SKY` `#38A0FF`)，立體果凍厚底 5px，圓角 18px，深藍紫描邊 (`#1F1A3A`)，字級 16px 開源粉圓體，100% 零系統 Emoji。
4. 提供存取器 `get_vault_button()` 與 `get_go_vault_button()`。
5. 支援六語系 i18n 即時刷新（`zh_TW`: 「前往儲能庫」, `zh_CN`: 「前往储能库」, `en`: 「To Vault」, `ja`: 「貯蔵庫へ」, `ko`: 「저장고로 이동」, `es`: 「Ir a Bóveda」），歐美語系零 CJK 殘留。
6. 撰寫單元與整合測試 `test_windup_daily_vault_shortcut.gd`，在非 headless (xvfb) 下產出實機截圖存證，執行 `clock-check` 確認無警告。
7. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態為「測試中」。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，每日委託底部按鈕列六按鈕『離開委託』、『前往戰力』、『前往背包』、『前往儲能庫』、『前往出征』、『前往停擺巨偶』並列間距合理，文字完整無穿框，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoVault` 尺寸 120x52px（未選巨偶 130x52px，熱區 >= 48px），文字採白色加深藍紫描邊 #1F1A3A（outline_size 4）搭配天藍底 #38A0FF，多巴胺立體厚底 5px，圓角 18px，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /opt/side/bravesoul-game` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏、無殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 3~8 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_windup_daily_vault_shortcut`、`test_windup_daily`、`test_windup_daily_i18n`、`test_windup_daily_inventory_shortcut`、`test_windup_power_stat_shortcut`、`test_windup_to_colossus` 及 8 項儲能庫測試全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoVault` 發射 `closed` 與 `vault_requested` 訊號並關閉委託彈窗，大廳連動開啟 `ClockworkVaultDialog`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 每日委託點擊『前往儲能庫』直達發條儲能庫放置收益彈窗，放置金幣與零件鐵屑收益狀態齊全，無卡死、無破圖。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全（zh_TW: 前往儲能庫, zh_CN: 前往储能库, en: To Vault, ja: 貯蔵庫へ, ko: 저장고로 이동, es: Ir a Bóveda），英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `windup-vault-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261015-windup-daily-vault-shortcut-t_44ba96c6` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_windup_daily_completed_btn_go_vault_zh_TW.png` | 繁中委託完成狀態：底欄六按鈕並列，天藍果凍按鈕『前往儲能庫』(120x52px) 正常顯示 | 1280x720 | `b7fe619bccdf5d3dd269a191091e81a7581b412c92ab0f944ff1f2d67fa29c50` |
| 02 | `proof_02_click_go_vault_opens_clockwork_vault_dialog.png` | 點擊前往儲能庫：直通開啟 ClockworkVaultDialog 放置收益彈窗，底層無遮罩殘留 | 1280x720 | `e983d097009f316188ee172fd85331bcb7f5bef572f6fa152060282134ab07d8` |
| 03 | `proof_locale_zh_TW_windup_vault_btn.png` | 繁中語系切換刷新：『前往儲能庫』 | 1280x720 | `625f9e9ddfb9e72611ce9612e7ce5f9b877615b1324eb0f1933d14dffbec3671` |
| 04 | `proof_locale_zh_CN_windup_vault_btn.png` | 簡中語系切換刷新：『前往储能库』 | 1280x720 | `8242a02b352c5e65431014cc21156a257adbd9226dc702d00dfe519046b164e2` |
| 05 | `proof_locale_en_windup_vault_btn.png` | 英文語系切換刷新："To Vault"，零 CJK 殘留 | 1280x720 | `f5c90a79ab5652f12d470c951400cabaed0dc4482e433287b8f9f3e2ca0abaef` |
| 06 | `proof_locale_ja_windup_vault_btn.png` | 日文語系切換刷新：『貯蔵庫へ』 | 1280x720 | `fe8136549950f9a34943219ed5aecb71f93718e3a0d72df4eb3bf56dd5010d5e` |
| 07 | `proof_locale_ko_windup_vault_btn.png` | 韓文語系切換刷新：『저장고로 이동』 | 1280x720 | `513c7974afd573336d49ec40746328a67ec932adf9c4c01b52ede49ec0935095` |
| 08 | `proof_locale_es_windup_vault_btn.png` | 西文語系切換刷新："Ir a Bóveda"，零 CJK 殘留 | 1280x720 | `a910316a17a36f02c61c40f66c4eb24aa25385a28606f8974861bf63b33a2cf7` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 功能單元與整合測試
godot --path game --headless -s res://scripts/ui/test_windup_daily_vault_shortcut.gd
# 輸出：TEST_WINDUP_DAILY_VAULT_SHORTCUT_OK (Exit 0)

# 3. 關聯單元與語系測試
TEST_FILTER=test_windup ./tools/run_tests.sh
# 輸出：TESTS PASSED (6/6) (test_windup_daily, test_windup_daily_i18n, test_windup_daily_inventory_shortcut, test_windup_daily_vault_shortcut, test_windup_power_stat_shortcut, test_windup_to_colossus)

# 4. 儲能庫相關測試迴歸
TEST_FILTER=vault ./tools/run_tests.sh
# 輸出：TESTS PASSED (8/8)

# 5. 實機渲染截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_windup_daily_vault_shortcut.gd
# 輸出：8 張獨立唯一截圖成功產出，雜湊無碰撞 (Exit 0)
```
