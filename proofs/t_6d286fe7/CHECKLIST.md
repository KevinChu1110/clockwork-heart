# 驗收查核表 (CHECKLIST) · ShopDialog 前往戰力快捷按鈕 (t_6d286fe7)

## 驗收項目逐項檢查

- [x] **按鈕規格樣式**：
  - [x] 節點名稱為 `BtnGoPowerStat`。
  - [x] 按鈕尺寸 `140x50px`，滿足 `>= 48px` 手機端熱區。
  - [x] 底色薄荷綠色盤 `#4ED86A`，邊框深藍紫 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
  - [x] 果凍厚底 `5px`，圓角 `18px`，字級 `16px` 開源粉圓體。
  - [x] 零系統 Emoji。
- [x] **點擊聯動與訊號**：
  - [x] 發射 `power_stat_requested` 訊號。
  - [x] 安全關閉 `ShopDialog`（發射 `closed` 訊號，無遮罩殘留）。
  - [x] `MobileLobby` 監聽並連動開啟 `PowerStatDialog`。
  - [x] 直通戰力屬性總覽。
- [x] **存取器**：
  - [x] `get_go_power_stat_button() -> Button`。
- [x] **六語系在地化**：
  - [x] `zh_TW`: 前往戰力
  - [x] `zh_CN`: 前往战力
  - [x] `en`: Go to Stats
  - [x] `ja`: 戦力詳細へ
  - [x] `ko`: 전투력으로 이동
  - [x] `es`: Ir a Estadísticas
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 均已更新。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_shop_power_stat_shortcut.gd` 全部 PASS。
  - [x] `clock-check` 零警告，完全通過。
  - [x] 7 張實機截圖完整產出且 SHA256 唯一無重複。
  - [x] Vision 視覺複檢通過，無穿模、無遮罩殘留、無文字溢出。
