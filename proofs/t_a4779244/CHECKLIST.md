# 驗收自查清單 · TitleWallDialog 稱號牆新增『前往衣櫥』快捷果凍按鈕連動 WardrobeDialog (t_a4779244)

## 任務基本資訊
- **卡號**：`t_a4779244`
- **負責人**：阿翔（`sideworker2`）
- **工作分支**：`agent/20261015-title-wall-wardrobe-shortcut-t_a4779244`
- **審查員**：小婷（`sideqa`）

---

## 驗收規範自查項目

### 1. 按鈕規格與多巴胺視覺
- [x] **按鈕識別**：節點名稱為 `BtnGoWardrobe`，在 `title_wall_dialog.gd` 中位於底部操作按鈕列 `ButtonRow`（`foot`）。
- [x] **規格與熱區**：
  - 尺寸熱區：`custom_minimum_size` 設定為寬 150px、高 48px（滿足手遊熱區 >= 48px 人因規格）。
  - 色盤樣式：多巴胺暖橘色盤 `#FFA010`（`COLOR_ORANGE`），深藍紫描邊 `#1F1A3A`（`COLOR_BORDER`），文字白色 `#FFFFFF`（深藍紫描邊 2px）。
  - 果凍立體厚底：底邊厚底 5px，圓角 18px，字級 18px 開源粉圓體（Open Huninn）。
- [x] **零系統 Emoji**：按鈕文字無任何原生 Emoji。

### 2. 點擊連動與大廳直通
- [x] **訊號與存取器**：提供 `wardrobe_requested` 訊號與 `get_go_wardrobe_button()` 存取器。
- [x] **點擊連動**：點擊 `BtnGoWardrobe` 發射 `wardrobe_requested` 訊號並安全關閉 `TitleWallDialog`（`closed` 訊號、`visible = false`、`queue_free()`）。
- [x] **無遮罩殘留**：關閉稱號牆時立即隱藏與釋放全螢幕半透明遮罩，底層無殘留黑屏或遮罩疊加。
- [x] **大廳直通**：`MobileLobby.open_title_wall_dialog()` 監聽 `wardrobe_requested` 訊號，連動開啟 `WardrobeDialog`（`MobileLobby.open_wardrobe()`）。

### 3. 六語系 i18n 完整支援
- [x] **字典完整性**：於 `game/data/i18n/content/<lang>/ui.json` 與 `game/data/i18n/<lang>.json` 補齊六語系鍵值：
  - `title_wall.btn_go_wardrobe`:
    - `zh_TW`: `前往衣櫥`
    - `zh_CN`: `前往衣橱`
    - `en`: `Go to Wardrobe`
    - `ja`: `衣装部屋へ`
    - `ko`: `의상실로 이동`
    - `es`: `Ir al Armario`
- [x] **即時切換**：`Loc.locale_changed` / `_update_ui_texts()` 在語系變更時即時刷新按鈕文字。

---

## 審查常見退回自查（對照 checklist）
- **實機截圖與 UI 排版**：✅ 已於 1280x720 橫屏環境實機渲染，按鈕高度 48px、文字 18px，排版留白充足無切字或遮蔽，無遮罩殘留。
- **點擊熱區**：✅ BtnGoWardrobe 寬 150px、高 48px，符合 >= 48px 手機端標準。
- **測試穩定性 (Flaky 防護)**：✅ 測試腳本精準控制幀數，手動推進等待幀保證 UI 與語系渲染完成，無頭與虛擬桌面環境皆綠。
- **無頭測試防護**：✅ 截圖比對防護 `DisplayServer.get_name() != "headless"`，確保 `run_tests.sh` 穩定跑綠。
- **工作區乾淨**：✅ 所有檔案均已 commit 至 `agent/20261015-title-wall-wardrobe-shortcut-t_a4779244`。
- **專案狀態**：✅ 已使用 `project_status.py` 將 `title-wall-wardrobe-shortcut` 更新為「測試中」。

---

## 實機截圖存證清單 (proofs/t_a4779244/)
| 檔案名稱 | 說明 | SHA256 雜湊 (前 16 碼) |
|---|---|---|
| `proof_01_zh_TW_title_wall_with_btn_go_wardrobe.png` | 繁中稱號牆底部操作列新增暖橘色「前往衣櫥」果凍按鈕 | `d208668df6b0a425` |
| `proof_02_zh_TW_wardrobe_opened_from_title_wall.png` | 點擊前往衣櫥後安全關閉稱號牆無遮罩殘留，直通開啟衣櫥換裝彈窗 | `3943f85936121ff6` |
| `proof_03_zh_CN_title_wall_btn_go_wardrobe.png` | 簡中語系 称号墙 與 前往衣橱 按鈕 | `71083a66b08fafa7` |
| `proof_04_en_title_wall_btn_go_wardrobe.png` | 英文語系 Achievements · Title Wall 與 Go to Wardrobe 按鈕 | `ad12072d959aab92` |
| `proof_05_ja_title_wall_btn_go_wardrobe.png` | 日文語系 実績 · 称号の壁 與 衣装部屋へ 按鈕 | `c9ffd48e7424f6a1` |
| `proof_06_ko_title_wall_btn_go_wardrobe.png` | 韓文語系 업적 · 칭호의 벽 與 의상실로 이동 按鈕 | `ebe844b047e1cadf` |
| `proof_07_es_title_wall_btn_go_wardrobe.png` | 西文語系 Logros · Muro de títulos 與 Ir al Armario 按鈕 | `c03fae56ab702f55` |
