# 驗收查核表 (CHECKLIST) · WardrobeDialog 前往商城快捷按鈕 (t_879da174)

## 驗收項目逐項檢查

- [x] **按鈕規格樣式**：
  - [x] 節點名稱為 `BtnGoShop`。
  - [x] 按鈕尺寸 `105x50px`，滿足 `>= 48px` 手機端熱區規範。
  - [x] 底色暖橘色盤 `#FFA010` (COLOR_ORANGE)，邊框深藍紫 `#1F1A3A` (COLOR_BORDER)，文字深藍紫 `#1F1A3A`。
  - [x] 果凍厚底 `5px`，圓角 `18px`，字級 `16px` 開源粉圓體。
  - [x] 100% 徹底清除遊戲內系統 Emoji（零系統 Emoji）。
- [x] **點擊連動與訊號**：
  - [x] 點擊發射 `shop_requested` 訊號。
  - [x] 安全關閉 `WardrobeDialog`（發射 `closed` 訊號，無遮罩殘留）。
  - [x] `MobileLobby` (mobile_lobby.gd) 監聽 `shop_requested` 並連動開啟 `ShopDialog`。
  - [x] 直通商城彈窗。
- [x] **存取器**：
  - [x] `get_go_shop_button() -> Button`。
  - [x] `get_shop_button() -> Button`。
- [x] **六語系在地化**：
  - [x] `zh_TW`: 前往商城
  - [x] `zh_CN`: 前往商城
  - [x] `en`: Go to Shop
  - [x] `ja`: ショップへ
  - [x] `ko`: 상점으로
  - [x] `es`: Ir a la tienda
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處均已同步支援 `wardrobe.go_shop` / `wardrobe.btn_go_shop`。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_wardrobe_shop_shortcut.gd` 全部 PASS (`TEST_WARDROBE_SHOP_SHORTCUT_OK`)。
  - [x] `clock-check` 自動化檢查通過（無語系死 key、無退役詞、素材正常）。
  - [x] 7 張實機截圖完整產出且 SHA256 唯一無重複。
  - [x] 符合 review.md 第 0-OPS 與 UI 規範。
