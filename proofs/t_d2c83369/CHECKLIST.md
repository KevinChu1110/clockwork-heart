# WardrobeDialog 前往鍛造快捷果凍按鈕驗收存證 (t_d2c83369)

## 1. 驗收標準檢驗
- [x] 按鈕存在於 WardrobeDialog 底部操作列 (actions_hbox)，名稱為 `BtnGoForge`
- [x] 尺寸熱區 >= 48px（實裝 105x50px，符合手機人體工學）
- [x] 符合多巴胺亮色盤規範：天藍底色 `#38A0FF`、圓角 18px、厚底 5px、深藍紫描邊與文字 `#1F1A3A`
- [x] 零系統 Emoji，使用粉圓體 (Open-Huninn)
- [x] 點擊後發射 `forge_requested` / `go_forge` 訊號並關閉衣櫥彈窗
- [x] 大廳接收訊號後即時開啟天宮鐵匠 `ForgeDialog`
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es

## 2. 實機截圖存證清單
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_forge.png`: SHA256 `beb3d1a2658d25ee011f56e5c4a7d3e19ed5cac28c7262b2e8f6d9ea6eb995df`
- `proof_02_zh_TW_forge_opened_from_wardrobe.png`: SHA256 `17cd3373a5ff5df613c092ff2f03c9b171af356a107d0947af40af7e8de8d400`
- `proof_03_zh_CN_wardrobe_btn_go_forge.png`: SHA256 `51a3c95bd57b3d1bd500338233b1dca45f9a1f17738ec01f6919a2607a8e6194`
- `proof_04_en_wardrobe_btn_go_forge.png`: SHA256 `b39b1a2f439a9864d92659de4a6eb8a53c5caf23fdd632b2b825cc492e4922e0`
- `proof_05_ja_wardrobe_btn_go_forge.png`: SHA256 `5b787600b15de6687abd853e0858f6b129021d85968ac0b1597bdebb2f45309e`
- `proof_06_ko_wardrobe_btn_go_forge.png`: SHA256 `2db6fd015ec8b26182ef2e9f1f56a16a378bcd18f0ffe55966f703af2840e099`
- `proof_07_es_wardrobe_btn_go_forge.png`: SHA256 `e9bd1aa2cd2a941d59ae98abf01cb739bc88790f110bef319239eb034f7845eb`
