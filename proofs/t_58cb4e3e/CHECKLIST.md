# WindupDailyDialog 冒險委託每日上發條新增『前往戰力』快捷果凍按鈕連動 PowerStatDialog 驗收存證 (t_58cb4e3e)

## 任務目標
1. 在 `WindupDailyDialog` (`game/scripts/ui/windup_daily_dialog.gd`) 每日委託完成狀態下（底部按鈕列中），新增『前往戰力』(`BtnGoPowerStat`) 快捷果凍按鈕。
2. 點擊後發射 `power_stat_requested` 與 `closed` 訊號並自動關閉彈窗 (`queue_free()`)，大廳 `MobileLobby` (`game/scripts/ui/mobile_lobby.gd`) 接到後平滑連動開啟 `PowerStatDialog` 戰力屬性總覽。
3. 按鈕尺寸與視覺規範：
   - 位於 `FootButtons` 底部按鈕列，與『離開委託』、『前往出征』/『前往停擺巨偶』並列。
   - 按鈕高度 52px (>= 50px 手機端熱區)，熱區寬度 >= 120px (實測 160~180px)。
   - 多巴胺天藍色盤 (`COLOR_SKY` `#38A0FF`)，立體果凍厚底 5px，圓角 20px (18~20px)，深藍紫描邊 (`#1F1A3A`)，字級 16px 開源粉圓體，100% 零系統 Emoji。
4. 提供存取器 `get_power_stat_button()` 與 `get_go_power_stat_button()`。
5. 支援六語系 i18n 即時刷新（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），歐美語系零 CJK 殘留。
6. 撰寫單元與整合測試 `test_windup_power_stat_shortcut.gd`，在非 headless (xvfb) 下產出實機截圖存證，執行 `clock-check` 確認無警告。
7. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，每日委託底部按鈕列四按鈕『離開委託』、『前往戰力』、『前往出征』、『前往停擺巨偶』並列間距合理，文字完整無穿框，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 160x52px（熱區 >= 48px），文字採白色加深藍紫描邊 #1F1A3A（outline_size 4）搭配天藍底 #38A0FF，多巴胺立體厚底 5px，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /opt/side/bravesoul-game` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 3~6 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_windup_power_stat_shortcut`、`test_windup_daily`、`test_windup_daily_i18n`、`test_windup_to_colossus` 等測試全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 發射 `closed` 與 `power_stat_requested` 訊號並關閉委託彈窗，大廳連動開啟 `PowerStatDialog`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 每日委託點擊『前往戰力』直達戰力屬性總覽，無卡死、無破圖。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全（zh_TW: 前往戰力, zh_CN: 前往战力, en: Go to Stats, ja: 戦力詳細へ, ko: 전투력으로 이동, es: Ir a Estadísticas），英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `windup-power-stat-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261014-windup-power-stat-t_58cb4e3e` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_windup_daily_completed_btn_go_power_stat_zh_TW.png` | 繁中委託完成狀態：底欄四按鈕並列，天藍果凍按鈕『前往戰力』(160x52px) 正常顯示 | 1280x720 | `333555540a5d24f0` |
| 02 | `proof_02_click_go_power_stat_opens_power_stat_dialog.png` | 點擊前往戰力：直通開啟 PowerStatDialog 戰力屬性總覽，底層無遮罩殘留 | 1280x720 | `c0505b10743450d1` |
| 03 | `proof_locale_zh_TW_windup_power_stat_btn.png` | 繁中語系切換刷新：『前往戰力』 | 1280x720 | `9505c5d1743602ef` |
| 04 | `proof_locale_zh_CN_windup_power_stat_btn.png` | 簡中語系切換刷新：『前往战力』 | 1280x720 | `da210aef8dbac104` |
| 05 | `proof_locale_en_windup_power_stat_btn.png` | 英文語系切換刷新："Go to Stats"，零 CJK 殘留 | 1280x720 | `e32935bc5fa6e7a0` |
| 06 | `proof_locale_ja_windup_power_stat_btn.png` | 日文語系切換刷新：『戦力詳細へ』 | 1280x720 | `5d4209145ae094b9` |
| 07 | `proof_locale_ko_windup_power_stat_btn.png` | 韓文語系切換刷新：『전투력으로 이동』 | 1280x720 | `d37faff125167251` |
| 08 | `proof_locale_es_windup_power_stat_btn.png` | 西文語系切換刷新："Ir a Estadísticas"，零 CJK 殘留 | 1280x720 | `7bb323fcb5bdaa8f` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：Exit 0

# 3. 功能單元與整合測試
godot --path game --headless -s res://scripts/ui/test_windup_power_stat_shortcut.gd
# 輸出：TEST_WINDUP_POWER_STAT_SHORTCUT_OK (Exit 0)

# 4. 關聯單元測試
godot --path game --headless -s res://scripts/systems/test_windup_daily.gd
# 輸出：WINDUP_DAILY_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_windup_daily_i18n.gd
# 輸出：WINDUP_DAILY_I18N_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_windup_to_colossus.gd
# 輸出：TEST_WINDUP_TO_COLOSSUS_OK (Exit 0)

# 5. 實機渲染截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_windup_power_stat_shortcut.gd
# 輸出：8 張獨立唯一截圖成功產出，雜湊無碰撞 (Exit 0)
```
