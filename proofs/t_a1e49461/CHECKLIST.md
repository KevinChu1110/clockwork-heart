# WardrobeDialog 前往背包快捷果凍按鈕驗收存證 (t_a1e49461)

## 1. 驗收標準檢驗
- [x] 按鈕存在於 WardrobeDialog 底部操作列 (actions_hbox)，名稱為 `BtnGoInventory`
- [x] 尺寸熱區 >= 48px（實裝 105x50px，符合手機人體工學）
- [x] 符合多巴胺亮色盤規範：暖橘底色 `#FFA010`、圓角 18px、厚底 5px、深藍紫描邊與文字 `#1F1A3A`
- [x] 零系統 Emoji，使用粉圓體 (Open-Huninn)
- [x] 點擊後發射 `go_inventory` / `inventory_requested` 訊號並關閉衣櫥彈窗
- [x] 大廳接收訊號後即時開啟探索背包 `MapleInventory`
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es

## 2. 實機截圖存證清單
