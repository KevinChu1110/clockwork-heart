# 驗收查核表 (CHECKLIST) · ShopDialog 前往稱號快捷按鈕 (t_982b471c)

## 驗收項目逐項檢查

- [x] **按鈕規格樣式**：
  - [x] 節點名稱為 `BtnGoTitleWall`。
  - [x] 按鈕尺寸 `140x50px`，滿足 `>= 50px` 高度與手機端熱區規範。
  - [x] 底色多巴胺天藍色盤 `#38A0FF`，邊框深藍紫 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
  - [x] 果凍厚底 `5px`，圓角 `18px`，字級 `16px` 開源粉圓體 (Open Huninn)。
  - [x] 100% 零系統 Emoji 與特殊符號。
- [x] **點擊聯動與訊號**：
  - [x] 發射 `title_wall_requested` 訊號與 `go_title_wall` 訊號。
  - [x] 安全關閉 `ShopDialog`（發射 `closed` 訊號，無遮罩殘留）。
  - [x] `MobileLobby` 監聽並連動開啟 `TitleWallDialog`。
  - [x] 流暢切換至成就稱號牆介面。
- [x] **存取器**：
  - [x] `get_go_title_wall_button() -> Button`。
- [x] **六語系在地化**：
  - [x] `zh_TW`: 前往稱號
  - [x] `zh_CN`: 前往称号
  - [x] `en`: To Titles
  - [x] `ja`: 称号へ
  - [x] `ko`: 칭호로 이동
  - [x] `es`: Ir a Títulos
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 12 個檔案均已更新。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_shop_dialog_title_wall_shortcut.gd` 全部 PASS。
  - [x] `clock-check .` 零警告，完全通過。
  - [x] 7 張實機截圖完整產出且 SHA256 唯一無重複。
  - [x] 視覺檢驗通過，無穿模、無遮罩殘留、無文字溢出。
