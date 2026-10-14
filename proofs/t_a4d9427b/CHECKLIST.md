# 驗收自查清單 · TitleWallDialog 稱號牆新增『前往戰力』快捷果凍按鈕連動 PowerStatDialog (t_a4d9427b)

## 任務基本資訊
- **卡號**：`t_a4d9427b`
- **負責人**：阿宏（`sideworker`）
- **工作分支**：`agent/20261013-title-wall-power-stat-shortcut-t_a4d9427b`
- **審查員**：小婷（`sideqa`）

---

## 驗收規範自查項目

### 1. 按鈕規格與多巴胺視覺
- [x] **按鈕識別**：節點名稱為 `BtnGoPowerStat`，在 `title_wall_dialog.gd` 中位於底部按鈕列 `ButtonRow`（`foot`）。
- [x] **規格與熱區**：
  - 尺寸熱區：`custom_minimum_size` 設定為寬 160px、高 52px（滿足高度 >= 50px 手機端人因規格）。
  - 色盤樣式：天藍色盤 `#38A0FF`（`COLOR_SKY`），深藍紫描邊 `#1F1A3A`（`COLOR_BORDER`），文字深藍紫 `#1F1A3A`（`COLOR_TEXT_DARK`）。
  - 果凍立體厚底：底邊厚底 5px，圓角 18px，字級 18px 開源粉圓體（Open Huninn）。
- [x] **零系統 Emoji**：按鈕文字無任何原生 Emoji。

### 2. 點擊連動與雙向閉環
- [x] **訊號與存取器**：提供 `power_stat_requested` 訊號與 `get_go_power_stat_button()` 存取器。
- [x] **點擊連動**：點擊 `BtnGoPowerStat` 發射 `power_stat_requested` 訊號並安全關閉 `TitleWallDialog`（`closed` 訊號、`visible = false`、`queue_free()`）。
- [x] **無遮罩殘留**：關閉稱號牆時立即隱藏與釋放全螢幕半透明遮罩，底層無殘留黑屏或遮罩疊加。
- [x] **大廳直通**：`MobileLobby.open_title_wall_dialog()` 監聽 `power_stat_requested` 訊號，連動開啟 `PowerStatDialog`（`MobileLobby.open_power_stat_dialog()`）。
- [x] **雙向閉環**：與戰力屬性總覽的『前往稱號』按鈕形成雙向閉環（稱號牆 ⇄ 戰力總覽自由切換）。

### 3. 六語系 i18n 完整支援
- [x] **字典完整性**：於 `game/data/i18n/content/<lang>/ui.json` 與 `game/data/i18n/<lang>.json` 補齊六語系鍵值：
  - `title_wall.btn_go_power_stat`:
    - `zh_TW`: `前往戰力`
    - `zh_CN`: `前往战力`
    - `en`: `Go to Stats`
    - `ja`: `戦力詳細へ`
    - `ko`: `전투력으로 이동`
    - `es`: `Ir a Estadísticas`
  - 亦提供直接字串鍵 `"前往戰力"` 之六語系映射。
- [x] **即時切換**：`Loc.locale_changed` 在語系變更時即時刷新按鈕文字。

---

## 審查常見退回自查（對照 checklist）
- **實機截圖與 UI 排版**：✅ 已於 1280x720 橫屏環境實機渲染，按鈕高度 52px、文字 18px，排版留白充足無切字或遮蔽，無遮罩殘留。
- **點擊熱區**：✅ BtnGoPowerStat 寬 160px、高 52px，符合 >= 50px 手機端標準。
- **測試穩定性 (Flaky 防護)**：✅ 測試腳本精準控制幀數，手動推進等待幀保證 UI 與語系渲染完成，無頭與虛擬桌面環境皆綠。
- **無頭測試防護**：✅ 截圖比對防護 `DisplayServer.get_name() != "headless"`，確保 `run_tests.sh` 穩定跑綠。
- **工作區乾淨**：✅ 所有檔案均已 commit 至 `agent/20261013-title-wall-power-stat-shortcut-t_a4d9427b`。
- **專案狀態**：✅ 已使用 `project_status.py` 將 `title-wall-power-stat-shortcut` 更新為「測試中」。

---

## 實機截圖存證清單 (proofs/t_a4d9427b/)
| 檔案名稱 | 說明 | SHA256 雜湊 (前 16 碼) |
|---|---|---|
| `proof_01_zh_TW_title_wall_with_btn_go_power_stat.png` | 繁中稱號牆底部操作列新增天藍色「前往戰力」果凍按鈕 | `094c3f49852e76ad` |
| `proof_02_zh_TW_power_stat_opened_from_title_wall.png` | 點擊前往戰力後安全關閉稱號牆無遮罩殘留，直通開啟戰力屬性總覽 | `e22922b51e789e74` |
| `proof_03_zh_TW_loop_back_to_title_wall.png` | 從戰力總覽點擊「前往稱號」閉環返回稱號牆視窗 | `c9c5f9a047f0f6e7` |
| `proof_04_en_title_wall_power_stat_btn.png` | 英文語系 Achievements · Title Wall 與 Go to Stats 按鈕 | `f27cbe445605114c` |
| `proof_05_ja_title_wall_power_stat_btn.png` | 日文語系 実績 · 称号の壁 與 戦力詳細へ 按鈕 | `a88cc1ad75d31325` |
| `proof_06_ko_title_wall_power_stat_btn.png` | 韓文語系 업적 · 칭호의 벽 與 전투력으로 이동 按鈕 | `07753d26f58b4944` |

六張截圖雜湊彼此相異，無重複畫面。

---

## clock-check 檢查結果
```
📍 分支：agent/20261013-title-wall-power-stat-shortcut-t_a4d9427b
🖼️ 新增／修改的素材 0 個，缺 .import 0 個

✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞
```
