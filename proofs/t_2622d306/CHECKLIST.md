# 驗收查核表 (CHECKLIST) · ShopDialog 前往工坊快捷按鈕 (t_2622d306)

## 驗收項目逐項檢查

- [x] **按鈕規格樣式**：
  - [x] 節點名稱為 `BtnGoWorkshop`。
  - [x] 按鈕尺寸 `140x50px`，滿足 `>= 50px` 高度與手機端熱區規範。
  - [x] 底色多巴胺暖橘色盤 `#FFA010`，邊框深藍紫 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
  - [x] 果凍厚底 `5px`，圓角 `18px`，字級 `16px` 開源粉圓體 (Open Huninn)。
  - [x] 100% 零系統 Emoji 與特殊符號。
- [x] **點擊聯動與訊號**：
  - [x] 發射 `workshop_requested` 訊號與 `go_workshop` 訊號。
  - [x] 安全關閉 `ShopDialog`（發射 `closed` 訊號，無遮罩殘留）。
  - [x] `MobileLobby` 監聽並連動開啟 `GemWorkshopDialog` (`open_gem_workshop()`)。
  - [x] 流暢切換至手藝工坊介面。
- [x] **存取器**：
  - [x] `get_go_workshop_button() -> Button` 與 `get_workshop_button() -> Button`。
- [x] **六語系在地化**：
  - [x] `zh_TW`: 前往工坊
  - [x] `zh_CN`: 前往工坊
  - [x] `en`: To Workshop
  - [x] `ja`: 工房へ
  - [x] `ko`: 공방으로
  - [x] `es`: Al Taller
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 12 個檔案均已更新。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_shop_dialog_workshop_shortcut.gd` 全部 PASS (exit 0)。
  - [x] 7 張實機截圖完整產出且 SHA256 唯一無重複。
  - [x] 視覺檢驗通過，無穿模、無遮罩殘留、無文字溢出、零 CJK 殘留。

