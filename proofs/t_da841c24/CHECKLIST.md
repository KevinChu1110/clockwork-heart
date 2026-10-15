# 驗收查核表 (CHECKLIST) · 衣櫥換裝前往商城與商城前往衣櫥雙分支合進主線回歸驗收 (t_da841c24)

## 驗收項目逐項檢查

- [x] **雙向快捷按鈕規格與樣式**：
  - [x] `WardrobeDialog`：底欄操作區具備 `BtnGoShop` 前往商城果凍按鈕（熱區 105x50px >= 48px、暖橘 `#FFA010`、深藍紫描邊與文字 `#1F1A3A`、果凍厚底 5px、圓角 18px、開源粉圓體字型、100% 零系統 Emoji）。
  - [x] `ShopDialog`：底欄具備 `BtnGoWardrobe` 前往衣櫥果凍按鈕（熱區 140x48px >= 48px、暖橘 `#FFA010`、深藍紫描邊與文字 `#1F1A3A`、果凍厚底 5px、圓角 18px、開源粉圓體字型、100% 零系統 Emoji）。
- [x] **訊號發射與大廳連動跳轉**：
  - [x] `WardrobeDialog` 點擊發射 `shop_requested`，關閉衣櫥彈窗並連動 `MobileLobby` 直通開啟 `ShopDialog`，無殘留遮罩。
  - [x] `ShopDialog` 點擊發射 `wardrobe_requested` 與 `go_wardrobe`，安全銷毀商城彈窗並連動 `MobileLobby` 直通開啟 `WardrobeDialog`，無殘留遮罩。
- [x] **存取器支援**：
  - [x] `WardrobeDialog` 具備 `get_go_shop_button() -> Button` 與 `get_shop_button() -> Button`。
  - [x] `ShopDialog` 具備 `get_go_wardrobe_button() -> Button`。
- [x] **六語系在地化 (12 處字典全齊)**：
  - [x] `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系在 `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 完整對齊支援。
  - [x] 即時語系切換正常，無缺失 key、無預設未翻譯殘留。
- [x] **自動化測試與無頭冒煙測試**：
  - [x] `test_wardrobe_shop_shortcut`：1/1 PASS。
  - [x] `test_shop_wardrobe_shortcut`：1/1 PASS。
  - [x] `test_wardrobe` 全套：4/4 PASS。
  - [x] `test_shop` 全套：5/5 PASS。
  - [x] `test_lobby` 全套：15/15 PASS。
  - [x] 無頭引擎冒煙測試 (`godot --path game --headless --quit-after 3`)：exit 0，0 SCRIPT ERROR。
- [x] **合規與發佈標準檢驗**：
  - [x] `clock-check .`：無退役名詞、無缺失 import、無語系死 key。
  - [x] `clock-check --live`：官網 14 頁正常打得開，無退役名詞。
  - [x] 符合 review.md 第 0-OPS 相關規範。
- [x] **實機截圖與存證**：
  - [x] 共 14 張實機截圖存證於 `proofs/t_da841c24/`，SHA256 均獨立唯一。
