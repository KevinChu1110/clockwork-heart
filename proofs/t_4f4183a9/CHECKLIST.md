# 木人樁試招結算新增『前往戰力』快捷果凍按鈕驗收存證 (t_4f4183a9)

## 任務目標
1. 在 `dummy_settlement_dialog.gd` 的木人樁試招結算數據卡（`DummySettlementDialog`）底部按鈕列中，在既有再次試招、調整心法與完成試招之間，新增『前往戰力』（`BtnGoPowerStat`）多巴胺立體厚底果凍按鈕。
2. 按鈕規格：熱區 150x50px（高度 50px，熱區 >= 48px），天藍多巴胺色盤 #38A0FF，深藍紫描邊 2px #1F1A3A，文字深藍紫 #1F1A3A，立體果凍厚底 5px（3~5px 規範內），圓角 14px（12~14px 規範內），字級 18px 開源粉圓體，100% 徹底清除系統 Emoji、零禁止符號。
3. 點擊連動：點擊後發出 `go_power_stat` 與 `power_stat_requested` 訊號，並執行 `setup` 傳入之 `on_power_stat` 回調，安全關閉銷毀結算彈窗，BattleView / 大廳接收後平滑直通開啟 `PowerStatDialog` 戰力屬性總覽。
4. 提供存取器：`get_go_power_stat_button() -> Button`、`get_power_stat_button() -> Button`、`get_go_power_stat_button_text() -> String`、`get_go_power_stat_text() -> String`。
5. 支援六語系 i18n 即時切換（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）：
   - zh_TW：前往戰力
   - zh_CN：前往战力
   - en：View Power
   - ja：戦力へ
   - ko：전투력 보기
   - es：Ver Poder
6. 遵守 review.md 規範，撰寫無頭測試 `test_dummy_settlement_go_power_stat.gd` 覆蓋樣式、點擊連動、六語系即時切換與 BattleView 整合。
7. 執行 `clock-check` 確保無警告，OpenGL3 實機截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，底欄四顆按鈕間距均勻合理，文字完整清晰無截斷溢出，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 150x50px（高度 50px，熱區 >= 48px），文字採深藍紫 #1F1A3A 搭配天藍底色 #38A0FF，高對比易讀，無節點坍塌。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 7 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複）。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化調用 `gs.reset_new_game("rabbit")`，時序等待幀數精準控制，run_tests.sh 穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_dummy_settlement_go_power_stat`、`test_dummy_settlement_dialog`、`test_dummy_settlement_i18n`、`test_dummy_settlement_record`、`test_dummy_settlement_skills` 全綠通過 (5/5)。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 後結算彈窗安全執行 `queue_free()` 徹底銷毀，直通開啟 `PowerStatDialog`，無殘留遮罩無卡死。 |
| **程式與邏輯** | 畫面跳轉與直通戰力總覽 | ✅ 已檢查 | 木人樁結算底欄點擊『前往戰力』發射訊號與回調，BattleView 接收後平滑開啟 PowerStatDialog。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全（zh_TW: 前往戰力, zh_CN: 前往战力, en: View Power, ja: 戦力へ, ko: 전투력 보기, es: Ver Poder），英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已將 `dummy-settlement-power-stat` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案完整 commit 至 `agent/20261014-dummy-settlement-power-stat-t_4f4183a9` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_dummy_settlement_dialog_zh_TW.png` | 繁中木人樁試招結算：底欄展示四按鈕，包含天藍色立體果凍按鈕『前往戰力』(150x50px) | 1280x720 | `311c2829af9e15a01e9fc1175861f6eaad2001eaf576e1e9474f780d278f589d` |
| 02 | `proof_02_dummy_settlement_dialog_zh_CN.png` | 簡中語系：按鈕文字「前往战力」，零 Emoji | 1280x720 | `7d26d0ad6095ad37ee3864a11fd197f25267bd93a9112823a3cf154e0494a1ba` |
| 03 | `proof_03_dummy_settlement_dialog_en.png` | 英文語系：按鈕文字 "View Power"，零 CJK 殘留、零 Emoji | 1280x720 | `86d168c3eaa9eed8f4267b0b600ee432df9fca06f91b8e3f20deff9b13f48c70` |
| 04 | `proof_04_dummy_settlement_dialog_ja.png` | 日文語系：按鈕文字「戦力へ」，零 Emoji | 1280x720 | `9f2af98060654b70d4633f7b51a9e1c26e5d68c58ea57e3be1c6a500d8dd7d6b` |
| 05 | `proof_05_dummy_settlement_dialog_ko.png` | 韓文語系：按鈕文字「전투력 보기」，零 Emoji | 1280x720 | `21366cae993f15a0f44a6bd178a31616be017e78dc951187d82013c466a2f475` |
| 06 | `proof_06_dummy_settlement_dialog_es.png` | 西文語系：按鈕文字 "Ver Poder"，零 CJK 殘留、零 Emoji | 1280x720 | `fef039c0f272e3ba029dfb497062b351d9794b216d5474fce60efc2a3a0069af` |
| 07 | `proof_07_dummy_settlement_power_stat_opened.png` | 點擊前往戰力：直通開啟 PowerStatDialog 戰力屬性總覽彈窗 | 1280x720 | `4decd676f161c06003da22085b33bf065fdeac315f52ac395903b2710cd3967b` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /opt/side/bravesoul-game/.worktrees/t_4f4183a9
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (Exit 0)

# 3. 功能單元與整合測試
TEST_FILTER=test_dummy_settlement_go_power_stat ./tools/run_tests.sh
# 輸出：TEST_DUMMY_SETTLEMENT_GO_POWER_STAT_OK (Exit 0)

# 4. 關聯單元與迴歸測試
TEST_FILTER=dummy_settlement ./tools/run_tests.sh
# 輸出：TESTS PASSED (5/5)
```
