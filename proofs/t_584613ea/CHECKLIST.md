# 驗收自查清單 · TitleWallDialog 稱號牆新增『前往商城』快捷果凍按鈕連動 ShopDialog (t_584613ea)

## 任務基本資訊
- **卡號**：`t_584613ea`
- **負責人**：阿翔（`sideworker2`）
- **工作分支**：`agent/20261015-title-wall-shop-shortcut-t_584613ea`
- **審查員**：小婷（`sideqa`）

---

## 驗收規範自查項目

### 1. 按鈕規格與多巴胺視覺
- [x] **按鈕識別**：節點名稱為 `BtnGoShop`，在 `title_wall_dialog.gd` 中位於底部操作按鈕列 `ButtonRow`（`foot`）。
- [x] **規格與熱區**：
  - 尺寸熱區：`custom_minimum_size` 設定為寬 150px、高 52px（滿足手遊熱區 >= 48px、高度 >= 50px 人因規格）。
  - 色盤樣式：多巴胺暖橘色盤 `#FFA010`（`COLOR_ORANGE`），深藍紫描邊 `#1F1A3A`（`COLOR_BORDER`），文字白色 `#FFFFFF`（深藍紫描邊 2px）。
  - 果凍立體厚底：底邊厚底 5px，圓角 18px，字級 18px 開源粉圓體（Open Huninn）。
- [x] **零系統 Emoji**：按鈕文字無任何原生 Emoji。

### 2. 點擊連動與大廳直通
- [x] **訊號與存取器**：提供 `shop_requested` 訊號與 `get_go_shop_button()` 存取器。
- [x] **點擊連動**：點擊 `BtnGoShop` 發射 `shop_requested` 訊號並安全關閉 `TitleWallDialog`（`closed` 訊號、`visible = false`、`_on_close()`）。
- [x] **無遮罩殘留**：關閉稱號牆時立即隱藏與釋放全螢幕半透明遮罩，底層無殘留黑屏或遮罩疊加。
- [x] **大廳直通**：`MobileLobby.open_title_wall_dialog()` 監聽 `shop_requested` 訊號，連動開啟 `ShopDialog`（`MobileLobby.open_shop()`）。

### 3. 六語系 i18n 完整支援
- [x] **字典完整性**：於 `game/data/i18n/content/<lang>/ui.json` 與 `game/data/i18n/<lang>.json` 補齊六語系鍵值：
  - `title_wall.btn_go_shop`:
    - `zh_TW`: `前往商城`
    - `zh_CN`: `前往商城`
    - `en`: `To Shop`
    - `ja`: `ショップへ`
    - `ko`: `상점으로 이동`
    - `es`: `Ir a Tienda`
- [x] **即時切換**：`Loc.locale_changed` / `_update_ui_texts()` 在語系變更時即時刷新按鈕文字。

---

## 審查常見退回自查（對照 checklist）
- **實機截圖與 UI 排版**：✅ 已於 1280x720 橫屏環境實機渲染，按鈕高度 52px（>= 50px）、文字 18px，排版留白充足無切字或遮蔽，無遮罩殘留。
- **點擊熱區**：✅ BtnGoShop 寬 150px、高 52px，符合 >= 48px 與高度 >= 50px 手機端標準。
- **測試穩定性 (Flaky 防護)**：✅ 測試腳本精準控制幀數，手動推進等待幀保證 UI 與語系渲染完成，無頭與虛擬桌面環境皆綠。
- **無頭測試防護**：✅ 截圖比對防護 `DisplayServer.get_name() != "headless"`，確保 `run_tests.sh` 穩定跑綠。
- **工作區乾淨**：✅ 所有檔案均已 commit 至 `agent/20261015-title-wall-shop-shortcut-t_584613ea`。
- **專案狀態**：✅ 已使用 `project_status.py` 將 `title-wall-shop-shortcut` 更新為「測試中」。

---

## 實機截圖存證清單 (proofs/t_584613ea/)
| 檔案名稱 | 說明 | SHA256 雜湊 (前 16 碼) |
|---|---|---|
| `proof_01_zh_TW_title_wall_with_btn_go_shop.png` | 繁中稱號牆底部操作列新增暖橘色「前往商城」果凍按鈕 | `14bd95fd26125a28` |
| `proof_02_zh_TW_shop_opened_from_title_wall.png` | 點擊前往商城後安全關閉稱號牆無遮罩殘留，直通開啟商城彈窗 ShopDialog | `8790fb3e506a1c34` |
| `proof_03_zh_CN_title_wall_btn_go_shop.png` | 簡中語系 称号墙 與 前往商城 按鈕 | `c9bcd89c11fe3341` |
| `proof_04_en_title_wall_btn_go_shop.png` | 英文語系 Achievements · Title Wall 與 To Shop 按鈕 | `05573190c404864e` |
| `proof_05_ja_title_wall_btn_go_shop.png` | 日文語系 実績 · 称号の壁 與 ショップへ 按鈕 | `b8214588f1819a86` |
| `proof_06_ko_title_wall_btn_go_shop.png` | 韓文語系 업적 · 칭호의 벽 與 상점으로 이동 按鈕 | `e6a6892022e31241` |
| `proof_07_es_title_wall_btn_go_shop.png` | 西文語系 Logros · Muro de títulos 與 Ir a Tienda 按鈕 | `deb0e5e93bb3edfd` |
