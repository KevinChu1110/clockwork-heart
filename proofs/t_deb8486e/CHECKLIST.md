# 大廳聚魂殿堂新增『前往戰力』快捷果凍按鈕驗收存證 (t_deb8486e)

## 任務目標
1. 在 `mobile_lobby.gd` 的聚魂殿堂分頁（`_build_soul_hall_tab`）底欄按鈕列，在既有一鍵吸收、一鍵配置、一鍵卸下、前往背包旁，新增『前往戰力』（`BtnGoPowerStat`）金黃色立體果凍按鈕。
2. 按鈕規格：熱區 140x52px（>= 50px），金黃色盤 #FFD028，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊聯動：調用 `open_power_stat_dialog()` 直通戰力屬性總覽，與戰力總覽的『前往聚魂』形成完整雙向閉環。
4. 提供 `get_soul_hall_go_power_stat_btn()` 存取器。
5. 支援六語系 i18n 即時切換（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），新增 `soul_hall.btn_go_power_stat` 鍵值：
   - 繁中：前往戰力
   - 簡中：前往战力
   - en：Go to Stats
   - ja：戦力詳細へ
   - ko：전투력으로 이동
   - es：Ir a Estadísticas
6. 遵守 review.md 規範，撰寫單元與整合測試 `test_soul_hall_power_stat_shortcut.gd` 覆蓋樣式、點擊聯動、六語系即時切換。
7. 執行 `clock-check` 確保無警告，非 headless 截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，底欄六大按鈕間距合理無擁擠穿模，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 140x52px（熱區 >= 50px），文字採深藍紫 #1F1A3A 搭配金黃色底 #FFD028，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複）。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game()`，時序等待幀數精準控制在 6 幀，穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_soul_hall_power_stat_shortcut`、`test_soul_hall_unequip_all`、`test_gem_workshop_power_stat_shortcut`、`test_forge_power_stat_shortcut`、`test_power_stat_shortcuts` 等測試全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 開啟 `PowerStatDialog`，戰力總覽點擊『前往聚魂』安全關閉總覽彈窗釋放無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與雙向閉環 | ✅ 已檢查 | 聚魂殿底欄點擊『前往戰力』開啟戰力總覽；戰力總覽點擊『前往聚魂』返回聚魂殿，閉環流暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已新增 `soul-hall-power-stat-shortcut` 並更新狀態為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261014-soul-hall-power-stat-shortcut-t_deb8486e` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_soul_hall_btn_go_power_stat.png` | 繁中聚魂殿分頁：底欄展示金黃色立體果凍按鈕『前往戰力』(140x52px) | 1280x720 | `972a4cef06d452a6ee0a62a6a0aa6f881abf4729815a6f3d065098ea87785800` |
| 02 | `proof_02_zh_TW_power_stat_dialog_opened.png` | 點擊前往戰力：直通開啟 PowerStatDialog 戰力屬性總覽彈窗 | 1280x720 | `3f0807a42530e4b752aee1a6bec216b22fc138a52edfc2ff5fc79c01a8430308` |
| 03 | `proof_03_zh_TW_loop_back_to_soul_hall.png` | 雙向閉環：從戰力總覽點擊『前往聚魂』安全關閉總覽返回聚魂殿堂 | 1280x720 | `0c64a28f7589b5e085625b9ad4f4a381a064c8e783e24adbc2b309ffa81b5db8` |
| 04 | `proof_04_zh_CN_soul_hall_power_stat_btn.png` | 簡中語系：按鈕文字「前往战力」，零 Emoji | 1280x720 | `e4363be215882a4536d505260cf5b41db54999af53346a78f787f5de47f47122` |
| 05 | `proof_05_en_soul_hall_power_stat_btn.png` | 英文語系：按鈕文字 "Go to Stats"，零 CJK 殘留 | 1280x720 | `6fab5a9516b1da645ed2ccaf2981a968c06d4e03465db893f4c3e96a2aec9a8b` |
| 06 | `proof_06_ja_soul_hall_power_stat_btn.png` | 日文語系：按鈕文字「戦力詳細へ」 | 1280x720 | `6027aaf8492a020506dfbcdf39a2289fad6ff04cef240f2eea88bf0063553601` |
| 07 | `proof_07_ko_soul_hall_power_stat_btn.png` | 韓文語系：按鈕文字「전투력으로 이동」 | 1280x720 | `9abb04e2dd3440d1ead46ffbe8104d61e1bb9bf39a468cc1153e6ce1c23a731b` |
| 08 | `proof_08_es_soul_hall_power_stat_btn.png` | 西文語系：按鈕文字 "Ir a Estadísticas"，零 CJK 殘留 | 1280x720 | `d584dead476b0b734a8874aa7cc4ffcf76b76deeb50492bcb6fc4bb90d5335d6` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check t_deb8486e
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：Exit 0

# 3. 功能單元與整合測試
godot --path game --headless -s res://scripts/ui/test_soul_hall_power_stat_shortcut.gd
# 輸出：TEST_SOUL_HALL_POWER_STAT_SHORTCUT_OK (Exit 0)

# 4. 關聯單元與雙向迴歸測試
godot --path game --headless -s res://scripts/ui/test_soul_hall_unequip_all.gd
# 輸出：TEST_SOUL_HALL_UNEQUIP_ALL_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_power_stat_shortcuts.gd
# 輸出：TEST_POWER_STAT_SHORTCUTS_OK (Exit 0)

# 5. 實機渲染截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 --audio-driver Dummy -s res://scripts/ui/test_soul_hall_power_stat_shortcut.gd
# 輸出：8 張獨立唯一截圖成功產出，雜湊無碰撞
```
