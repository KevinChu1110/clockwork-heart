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
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_inventory.png`: SHA256 `45bca5b2c08515a8e6c1bddd033750ba8c3c5cc9b2ad1e793e74bcd4d20a0b85`
- `proof_02_zh_TW_inventory_opened_from_wardrobe.png`: SHA256 `5ce0afb4ae640a17619636806d8d8ac7cb79ecc5aa59116d48418d7032e6dc94`
- `proof_03_zh_CN_wardrobe_btn_go_inventory.png`: SHA256 `6cf79de6fc57b1044b0bf595a5b67057df59d34e94e64c6348f6272e6ff1d91b`
- `proof_04_en_wardrobe_btn_go_inventory.png`: SHA256 `b1eb0294f1e7e4da34e9bb4b9759f43bd6c5a5ff67a55827d84be6fb6d5350b6`
- `proof_05_ja_wardrobe_btn_go_inventory.png`: SHA256 `046fd20e12cc1629331f557536e306491ffb538c62b508f273eafc04ec15b478`
- `proof_06_ko_wardrobe_btn_go_inventory.png`: SHA256 `58578a57ded72871f82e9f59a5c07ae47b4127352b45df289728533c93dcfd9b`
- `proof_07_es_wardrobe_btn_go_inventory.png`: SHA256 `ef48ed85b91828b19b4844b91f1e9315d2c22c92d95b0a656b2c14c8202c843a`
