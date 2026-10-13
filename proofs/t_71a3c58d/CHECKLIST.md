# 驗收自查清單 · TitleWallDialog 稱號牆新增『卸下稱號』果凍按鈕與連動安全防護 (t_71a3c58d)

## 任務基本資訊
- **卡號**：`t_71a3c58d`
- **負責人**：阿宏（`sideworker`）
- **工作分支**：`agent/20261013-title-unequip-t_71a3c58d`
- **審查員**：小婷（`sideqa`）

---

## 驗收規範自查項目

### 1. 按鈕規格與多巴胺視覺
- [x] **按鈕識別**：節點名稱固定為 `BtnUnequipTitle`，置於底部操作列（`ButtonRow`）。
- [x] **點擊熱區與尺寸**：`custom_minimum_size` 設定為寬 160px、高 52px（滿足高度 >= 50px、熱區 >= 48px 手機端人因規格）。
- [x] **多巴胺亮色厚底**：珊瑚粉色盤 `#FF5E8A`（`COLOR_PINK`），圓角 18px，底邊厚底 5px，深藍紫描邊 `#1F1A3A`（`COLOR_BORDER`），底邊陰影 5px。
- [x] **字級與排版**：字級設定為 18px（滿足 >= 16px 規範，零碎小字），自適應粉圓體字型。
- [x] **零系統 Emoji**：按鈕、標籤與文字無任何原生 Emoji。

### 2. 安全防呆機制
- [x] **預設置灰防呆**：當玩家當前未佩戴特殊稱號（即當前佩戴為預設「初出茅廬」或空字串）時，按鈕安全置灰（`disabled = true`）。
- [x] **置灰外觀保護**：置灰狀態使用柔和灰米色底板 `#D6CFC7`、深灰描邊 `#A89E90`、字體色 `#8C827A`，文字描邊歸零避免黑框，防止無效點擊。
- [x] **動態啟用**：當玩家點擊佩戴特殊稱號（如「看破者」或「以劍抵爪」）後，按鈕立即解除置灰（`disabled = false`），恢復亮色立體果凍外觀。

### 3. 卸下邏輯與連動閉環
- [x] **點擊卸下**：點擊按鈕觸發 `_on_unequip_pressed()` 與 `unequip_title()`，播放 UI 點擊音效。
- [x] **訊號發射**：成功發射 `title_unequipped` 訊號。
- [x] **GameState 重設**：呼叫 `GameState.set_equipped_title("")` 安全重設為預設「初出茅廬」，並觸發 `equipped_title_changed("初出茅廬")`。
- [x] **稱號卡片復原**：原佩戴稱號金黃光框與「✓ 佩戴中」標籤消失，恢復為「已解鎖」暖橘厚底卡片。
- [x] **大廳頭頂名牌連動**：大廳 `_hero_title_tag` 藉由 `equipped_title_changed` 監聽，即時更新文字回歸「【初出茅廬】」（或當前語系之預設稱號名牌）。
- [x] **按鈕重新置灰**：卸下完成後，按鈕重新回到置灰防呆狀態。

### 4. 六語系 i18n 完整支援
- [x] **字典完整性**：於 `game/data/i18n/content/<lang>/ui.json` 與 `game/data/i18n/<lang>.json` 補齊六語系「卸下稱號」鍵值：
  - `zh_TW`: `卸下稱號`
  - `zh_CN`: `卸下称号`
  - `en`: `Unequip Title`
  - `ja`: `称号を外す`
  - `ko`: `칭호 해제`
  - `es`: `Desequipar título`
- [x] **即時切換**：`_update_ui_texts()` 在語系變更時即時刷新按鈕文字與置灰狀態，無 CJK 漏翻殘留。

---

## 審查常見退回自查（對照 checklist）
- **實機截圖與 UI 排版**：✅ 已於 1280x720 橫屏環境實機渲染，按鈕高度 52px、文字 18px，排版留白充足無切字或遮蔽。
- **點擊熱區**：✅ BtnUnequipTitle 寬 160px、高 52px，符合 >= 48px 手機端標準。
- **測試穩定性 (Flaky 防護)**：✅ 測試腳本精準控制幀數，手動推進等待幀保證 UI 與語系渲染完成，無頭與虛擬桌面環境皆綠。
- **無頭測試防護**：✅ 截圖比對防護 `DisplayServer.get_name() != "headless"`，確保 `run_tests.sh` 穩定跑綠。
- **工作區乾淨**：✅ 所有檔案均已 commit 至 `agent/20261013-title-unequip-t_71a3c58d`，工作區無 untracked 或 modified 檔案。
- **專案狀態**：✅ 已使用 `project_status.py` 將 `title-wall-unequip` 更新為「測試中」。

---

## 實機截圖存證清單 (proofs/t_71a3c58d/)
| 檔案名稱 | 說明 | SHA256 雜湊 (前 16 碼) |
|---|---|---|
| `proof_01_zh_TW_title_wall_disabled_default.png` | 繁中稱號牆預設初出茅廬，按鈕安全置灰防呆 | `fdaedd3040631672` |
| `proof_02_zh_TW_title_wall_equipped_special.png` | 繁中稱號牆佩戴特殊稱號，按鈕高亮啟用、卡片金框佩戴中 | `61d6d29124886075` |
| `proof_03_zh_TW_title_wall_after_unequip.png` | 點擊卸下稱號後，卡片復原已解鎖、按鈕重新置灰 | `ee93d96185e8d669` |
| `proof_04_zh_TW_lobby_after_unequip.png` | 大廳頭頂稱號名牌即時同步回歸【初出茅廬】 | `c31df8a5c01af96b` |
| `proof_05_en_title_wall_unequip.png` | 英文語系 Unequip Title 按鈕支援與卸下置灰驗證 | `192d6482ef328659` |
| `proof_06_ja_title_wall_unequip.png` | 日文語系 称号を外す 按鈕支援與卸下置灰驗證 | `7cf40badc331c10d` |

六張截圖雜湊彼此相異，無重複或假存證。
