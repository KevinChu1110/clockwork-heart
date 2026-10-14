# BattleDefeatDialog 戰敗結算新增『前往戰力』快捷果凍按鈕驗收存證 (t_2cf9d674)

## 任務目標
1. 在 `BattleDefeatDialog`（`game/scripts/battle/battle_defeat_dialog.gd`）底部操作列新增『前往戰力』（`BtnGoPowerStat`）天藍色立體果凍按鈕，引導戰敗玩家一鍵直通 `PowerStatDialog` 檢視戰力診斷、六維屬性、戰魂共鳴與機芯強度。
2. 按鈕規格樣式：
   - 節點名稱為 `BtnGoPowerStat`，掛載於底欄操作列（`BottomActions`）。
   - 高度 52px，寬度 130px（熱區 >= 48px）。
   - 天藍色盤 `#38A0FF`，深藍紫描邊 `#1F1A3A`，文字高對比奶油白 `#FFFDF8` 帶深色描邊。
   - 立體果凍厚底（bottom border 6px >= 5px），圓角 20px。
   - 零系統 Emoji，零禁止符號。
3. 點擊連動與訊號：
   - 發射 `power_stat_requested` 訊號與執行 `on_power_stat` 回調。
   - 安全銷毀彈窗（`queue_free()`），無遮罩殘留或舊彈窗遮擋。
   - 正確調起 `PowerStatDialog` 戰力屬性總覽視窗（`BattleView.open_power_stat_dialog()` / `MobileLobby.open_power_stat_dialog()`）。
4. 存取器：
   - `get_go_power_stat_button() -> Button`。
   - `get_go_power_stat_button_text() -> String`。
   - `get_power_stat_button() -> Button`。
5. 六語系多國語言動態即時切換：
   - 繁中 (zh_TW)：前往戰力
   - 簡中 (zh_CN)：前往战力
   - 英文 (en)：Go to Stats（零 CJK 殘留）
   - 日文 (ja)：戦力詳細へ
   - 韓文 (ko)：전투력으로 이동
   - 西班牙文 (es)：Ir a Estadísticas（零 CJK 殘留）
   - 全語系零系統 Emoji。
6. 單元與整合測試：
   - 新增 `game/scripts/battle/test_battle_defeat_power_stat_shortcut.gd`，覆蓋按鈕實例、層級、尺寸厚底、信號發射、PowerStatDialog 調起、六語系即時切換與零 CJK/零 Emoji。
   - 迴歸測試 `test_battle_defeat_diagnostic.gd`、`test_battle_defeat_retry.gd`、`test_battle_defeat_i18n.gd` 全綠通過。
7. 執行 `clock-check` 零警告，完全通過。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複查，5 個按鈕排版整齊無重疊、無截字、邊界充足。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 130x52px（>= 48px），天藍色底 #38A0FF 搭配奶油白 #FFFDF8 與深描邊，對比度高。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | `clock-check` 驗證 0 缺 .import，0 軟連結。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 7 張截圖均由 `xvfb-run opengl3` 渲染，SHA256 雜湊互不相同，完整存證。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試先初始化 Autoload 與 reset_new_game，等待幀數充足，無時序競爭。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | 4 支測試全部 PASS（power_stat_shortcut, diagnostic, retry, i18n）。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 後執行 `queue_free()`，且安全調起 `PowerStatDialog`。 |
| **程式與邏輯** | 畫面跳轉與雙向閉環 | ✅ 已檢查 | 點擊『前往戰力』可開啟 `PowerStatDialog` 檢視六維屬性與機芯，關閉後無殘留。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系翻譯對齊，en/es 零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已將 `battle-defeat-power-stat-shortcut` 更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案提交至 `agent/20261014-battle-defeat-power-stat-shortcut-t_2cf9d674` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_battle_defeat_five_buttons_zh_TW.png` | 繁中戰敗結算彈窗：展示底欄五按鈕（復活、再次挑戰、前往整頓、前往戰力、結束戰鬥）與戰力診斷卡 | 1280x720 | `be6d878d92839b5d14d4bf4085fb5f1e12449494086381d5e595f983c8a2528c` |
| 02 | `proof_02_battle_defeat_power_stat_en.png` | 英文語系：BtnGoPowerStat 顯示 \"Go to Stats\"，零 CJK 殘留 | 1280x720 | `d5d237c79f3ad186c618fc2ab404f3cafe61eab41a2df56ad64cf0842e6e09df` |
| 03 | `proof_03_battle_defeat_power_stat_ja.png` | 日文語系：BtnGoPowerStat 顯示 \"戦力詳細へ\" | 1280x720 | `bafc9713446761bc9693903eaf7c4d91d3536698955255e609905cace24609e4` |
| 04 | `proof_04_battle_defeat_power_stat_ko.png` | 韓文語系：BtnGoPowerStat 顯示 \"전투력으로 이동\" | 1280x720 | `30d745f34c83a3f45292c1b736de2fa02cd4d1c17c1992a20b3049dd48234c50` |
| 05 | `proof_05_battle_defeat_power_stat_es.png` | 西文語系：BtnGoPowerStat 顯示 \"Ir a Estadísticas\"，零 CJK 殘留 | 1280x720 | `d30332c9ebf4e1155a5db79e1318e55aeeb38252bb514077fe1b76a24c763c79` |
| 06 | `proof_06_battle_defeat_power_stat_zh_CN.png` | 簡中語系：BtnGoPowerStat 顯示 \"前往战力\" | 1280x720 | `bbfa5b6f3e479752b50c7a8b07c35f70a1817bf96b491babe232f87e37837134` |
| 07 | `proof_07_click_go_power_stat_opens_power_stat_dialog.png` | 點擊前往戰力：戰敗結算彈窗銷毀，成功調起 PowerStatDialog 戰力屬性總覽視窗 | 1280x720 | `e609cf2c2a0b4eb7eea03117229eab44c0c406051bbe74de132113e6a452fe9e` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2cf9d674/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：Exit 0

# 3. 本功能單元與整合測試
godot --path game --headless -s scripts/battle/test_battle_defeat_power_stat_shortcut.gd
# 輸出：TEST_BATTLE_DEFEAT_POWER_STAT_SHORTCUT_OK (Exit 0)

# 4. 戰敗結算關聯迴歸測試
godot --path game --headless -s scripts/battle/test_battle_defeat_diagnostic.gd
godot --path game --headless -s scripts/battle/test_battle_defeat_retry.gd
godot --path game --headless -s scripts/battle/test_battle_defeat_i18n.gd
# 輸出：全數 PASS (Exit 0)

# 5. 實機渲染截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_battle_defeat_power_stat_proof.gd
# 輸出：7 張獨立唯一截圖成功產出，雜湊無碰撞
```
