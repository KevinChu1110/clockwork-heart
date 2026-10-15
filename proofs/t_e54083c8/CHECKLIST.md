# ClockworkVaultDialog 發條儲能庫放置收益彈窗新增『前往委託』快捷果凍按鈕連動 WindupDailyDialog 驗收存證 (t_e54083c8)

## 任務目標
1. 在 `ClockworkVaultDialog` (`game/scripts/ui/clockwork_vault_dialog.gd`) 發條儲能庫放置收益彈窗底欄按鈕列中，新增多巴胺果凍厚底按鈕『前往委託』(`BtnGoWindup`)。
2. 建立發條儲能庫放置收益與每日冒險委託上發條 (`WindupDailyDialog`) 的雙向互通閉環（與 `WindupDailyDialog` 的 `BtnGoVault` 對應）。
3. 按鈕尺寸與視覺規範：
   - 位於底部按鈕列，與『一鍵領取』(`ClaimButton`)、『雙倍領取』(`DoubleClaimButton`)、『前往鍛造』(`BtnGoForge`)、『前往背包』(`BtnGoInventory`)、『前往戰力』(`BtnGoPowerStat`) 六按鈕完整並列。
   - 按鈕高度 52px (>= 50px 手機端熱區)，熱區寬度 115px (>= 48px)。
   - 多巴胺暖橘色盤 (`COLOR_ORANGE` `#FFA010`)，立體果凍厚底 5px，圓角 18px，深藍紫描邊 (`#1F1A3A`)，字級 16px 開源粉圓體，100% 零系統 Emoji。
4. 訊號與跳轉聯動：
   - `ClockworkVaultDialog` 宣告 `signal windup_requested()` 與 `signal go_windup()`。
   - 點擊 `BtnGoWindup` 發射訊號並自動關閉儲能庫彈窗 (`queue_free()`)，大廳 `MobileLobby` 監聽訊號並平滑連動開啟 `WindupDailyDialog`。
   - 提供存取器 `get_go_windup_button()` 與 `get_windup_button()`。
5. 支援六語系 i18n 即時刷新：
   - `zh_TW`: 「前往委託」
   - `zh_CN`: 「前往委托」
   - `en`: 「To Daily」
   - `ja`: 「日課へ」
   - `ko`: 「일일 의뢰로 이동」
   - `es`: 「Ir a Encargos」
   - 歐美語系零 CJK 殘留，全語系 100% 零系統 Emoji。
6. 撰寫單元與整合測試 `test_clockwork_vault_windup_shortcut.gd`，在非 headless (xvfb) 下產出 8 張實機截圖存證，執行 `clock-check` 確認無警告。
7. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態為「測試中」。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，底欄六按鈕『一鍵領取』、『雙倍領取』、『前往委託』、『前往鍛造』、『前往背包』、『前往戰力』並列間距合理，文字完整無穿框，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoWindup` 尺寸 115x52px（熱區 >= 48px），文字採深藍紫 #1F1A3A 搭配暖橘底 #FFA010，多巴胺立體厚底 5px，圓角 18px，高對比清晰易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /opt/side/bravesoul-game` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏、無殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化設置 1280x720 分辨率，時序等待幀數控制在 2~3 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_clockwork_vault_windup_shortcut`、`test_clockwork_vault_power_stat_shortcut`、`test_idle_clockwork_vault`、`test_vault_double_claim`、`test_windup_daily_vault_shortcut` 全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoWindup` 發射 `closed` 與 `windup_requested` 訊號並關閉儲能庫彈窗，大廳連動開啟 `WindupDailyDialog`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 發條儲能庫點擊『前往委託』直達冒險委託每日上發條彈窗，委託事件與選項齊全，雙向互通閉環達成，無卡死、無破圖。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全（zh_TW: 前往委託, zh_CN: 前往委托, en: To Daily, ja: 日課へ, ko: 일일 의뢰로 이동, es: Ir a Encargos），英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `vault-windup-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261015-clockwork-vault-windup-shortcut-t_e54083c8` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_vault_six_buttons_zh_TW.png` | 繁中儲能庫底欄六按鈕齊全並列：暖橘果凍按鈕『前往委託』(115x52px) 正常顯示 | 1280x720 | `8c72d6d17dcd20a9e6fb0671fd818d28a13a2312279dfc9fc222c890330dee5a` |
| 02 | `proof_02_click_go_windup_opens_windup_daily_dialog.png` | 點擊前往委託：直通開啟 WindupDailyDialog 冒險委託彈窗，底層無遮罩殘留 | 1280x720 | `9be93841f3a7cc15c28aa48785448e3a95715d9e66eeee0b17436f2c7e04ecd0` |
| 03 | `proof_03_locale_zh_TW_vault_windup_btn.png` | 繁中語系切換刷新：『前往委託』 | 1280x720 | `a34e396cf3ac1b0026025700f389da439e1782cb7b071d44d2f52a778a0dd5af` |
| 04 | `proof_04_locale_zh_CN_vault_windup_btn.png` | 簡中語系切換刷新：『前往委托』 | 1280x720 | `9f0ae19e5aa5a002c3e4acb8a0487418e91864b4ed14da82b2b64135542d083b` |
| 05 | `proof_05_locale_en_vault_windup_btn.png` | 英文語系切換刷新：\"To Daily\"，零 CJK 殘留 | 1280x720 | `6fc6d69add6b4f650066ff48ef7e0d99a953472a0fdd70427d138a07cd9777fb` |
| 06 | `proof_06_locale_ja_vault_windup_btn.png` | 日文語系切換刷新：『日課へ』 | 1280x720 | `909a3636ce6a635ae30368e0b44fc1b35257ef5bb54869ddf0e7285adaeed11b` |
| 07 | `proof_07_locale_ko_vault_windup_btn.png` | 韓文語系切換刷新：『일일 의뢰로 이동』 | 1280x720 | `1dfd0e3c95a82d2b6c6b0e5d72eb77d4d5ab2f30510060013dc1197d3b002b58` |
| 08 | `proof_08_locale_es_vault_windup_btn.png` | 西文語系切換刷新：\"Ir a Encargos\"，零 CJK 殘留 | 1280x720 | `834bd0c67d8ae181d720f0d1ff5760d0bf754676c6d0cc7f19b44beccc3f540f` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 功能單元與整合測試
godot --path game --headless -s res://scripts/ui/test_clockwork_vault_windup_shortcut.gd
# 輸出：TEST_CLOCKWORK_VAULT_WINDUP_SHORTCUT_OK (Exit 0)

# 3. 實機渲染截圖存證
xvfb-run -a godot --path game --audio-driver Dummy -s res://scripts/ui/test_clockwork_vault_windup_shortcut.gd
# 輸出：8 張獨立唯一截圖成功產出，雜湊無碰撞 (Exit 0)

# 4. 相關彈窗迴歸測試
godot --path game --headless -s res://scripts/ui/test_clockwork_vault_power_stat_shortcut.gd
godot --path game --headless -s res://scripts/ui/test_idle_clockwork_vault.gd
godot --path game --headless -s res://scripts/ui/test_vault_double_claim.gd
godot --path game --headless -s res://scripts/ui/test_windup_daily_vault_shortcut.gd
# 輸出：全數 PASS (Exit 0)
```
