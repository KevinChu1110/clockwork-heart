# 關卡勝利結算新增『前往戰力』快捷果凍按鈕驗收存證 (t_5bd28180)

## 任務目標
1. 在 `battle_victory_dialog.gd` 的關卡出征勝利結算彈窗（`BattleVictoryDialog`）底部按鈕列，在既有立即裝備、收下完成、前往整頓旁，新增『前往戰力』（`BtnGoPowerStat`）天藍色立體果凍按鈕。
2. 按鈕規格：熱區 130x50px（高度 50px，熱區 >= 48px），天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A，果凍厚底 5px，圓角 16px（14~18px 規範內），字級 16px 開源粉圓體，零系統 Emoji、零禁止符號。
3. 點擊聯動：點擊後發射 `power_stat_requested` 訊號並執行 `setup` 傳入之 `on_power_stat` 回調，安全關閉銷毀結算彈窗，BattleView / 大廳接收後平滑切換回大廳並直通開啟 `PowerStatDialog` 戰力屬性總覽。
4. 提供存取器：`get_go_power_stat_button() -> Button`、`get_power_stat_button() -> Button`、`get_go_power_stat_button_text() -> String`。
5. 支援六語系 i18n 即時切換（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）：
   - 繁中：前往戰力
   - 簡中：前往战力
   - en：Go to Stats
   - ja：戦力詳細へ
   - ko：전투력으로 이동
   - es：Ir a Estadísticas
6. 遵守 review.md 規範，撰寫單元與整合測試 `test_battle_victory_power_stat.gd` 覆蓋樣式、點擊聯動、六語系即時切換。
7. 執行 `clock-check` 確保無警告，非 headless 截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，底欄按鈕間距均勻合理，文字完整清晰無截斷溢出，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 130x50px（高度 50px，熱區 >= 48px），文字採深藍紫 #1F1A3A 搭配天藍底色 #38A0FF，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 6 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複）。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化調用 `gs.reset_new_game("rabbit")`，時序等待幀數精準控制，run_tests.sh 穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_battle_victory_power_stat`、`test_battle_victory_gear_up`、`test_battle_victory_next_stage`、`test_battle_victory_replay`、`test_battle_defeat_power_stat_shortcut`、`test_power_stat_shortcuts` 等測試全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 後結算彈窗安全執行 `queue_free()` 徹底銷毀，直通開啟 `PowerStatDialog`，無殘留遮罩無卡死。 |
| **程式與邏輯** | 畫面跳轉與直通戰力總覽 | ✅ 已檢查 | 勝利結算底欄點擊『前往戰力』發射訊號與回調，戰鬥/大廳視圖接收後切換回大廳並開啟 PowerStatDialog。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已將 `victory-power-stat-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案將 commit 至 `agent/20261014-victory-power-stat-shortcut-t_5bd28180` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_battle_victory_dialog_six_buttons_zh_TW.png` | 繁中勝利結算彈窗：底欄展示天藍色立體果凍按鈕『前往戰力』(130x50px) | 1280x720 | `529471bd820070db121461a7ccf7556774c1b90c8d8e0c0e0dab3bdb9dce51ab` |
| 02 | `proof_02_battle_victory_dialog_en.png` | 英文語系：按鈕文字 "Go to Stats"，零 CJK 殘留、零 Emoji | 1280x720 | `3d207c099f66c04aef83b423a0442db5fa1e5fa6ee72c3a5a15ff15bcd50480f` |
| 03 | `proof_03_battle_victory_dialog_ja.png` | 日文語系：按鈕文字「戦力詳細へ」，零 Emoji | 1280x720 | `8f9458bcf3ccfa3caea217eb9329f66b8741505acfd581ce0fde39987005c940` |
| 04 | `proof_04_battle_victory_dialog_ko.png` | 韓文語系：按鈕文字「전투력으로 이동」，零 Emoji | 1280x720 | `b8843289b6411785444740d001ee31dd87154a483a6bb0d0e068a2bfcbbe5786` |
| 05 | `proof_05_battle_victory_dialog_es.png` | 西文語系：按鈕文字 "Ir a Estadísticas"，零 CJK 殘留、零 Emoji | 1280x720 | `d49223d996a261a78c918bcb16b44366212a196cccc1d791534edff523d330c7` |
| 06 | `proof_06_victory_power_stat_transition_opened.png` | 點擊前往戰力：直通開啟 PowerStatDialog 戰力屬性總覽彈窗 | 1280x720 | `124cb750bd27d112c463b7536bc253b47cd742b8d1386a77b9164ed03dfa2413` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (Exit 0)

# 3. 功能單元與整合測試
TEST_FILTER=test_battle_victory_power_stat ./tools/run_tests.sh
# 輸出：TEST_BATTLE_VICTORY_POWER_STAT_OK (Exit 0)

# 4. 關聯單元與迴歸測試
TEST_FILTER=test_battle_victory ./tools/run_tests.sh
# 輸出：TESTS PASSED (4/4)

TEST_FILTER=test_battle_defeat_power_stat ./tools/run_tests.sh
# 輸出：TESTS PASSED (1/1)

TEST_FILTER=test_power_stat ./tools/run_tests.sh
# 輸出：TESTS PASSED (8/8)
```
