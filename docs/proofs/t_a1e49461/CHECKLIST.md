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
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_inventory.png`: SHA256 `ccc7d1afc069c2a9b1f691793c32f5407710d871b2785b730915d7f1f16c250b`
- `proof_02_zh_TW_inventory_opened_from_wardrobe.png`: SHA256 `8ed587d355cc0f119e7e67e70133d6988394cc0b2590c19fa32bf27af133df96`
- `proof_03_zh_CN_wardrobe_btn_go_inventory.png`: SHA256 `fb3ce3cccffbc7ad8f5da7f26d3e032d7b91b68a0c827ae42abbd33124eadc17`
- `proof_04_en_wardrobe_btn_go_inventory.png`: SHA256 `e1f281735f2e16cf26d7676d8fb4c755ba4b72ab7ade94d79fbf466331ff5243`
- `proof_05_ja_wardrobe_btn_go_inventory.png`: SHA256 `2d8e75846a9db0bb41e34df291b4262dfe35c8f680f88306dafdf17ddfca6fdb`
- `proof_06_ko_wardrobe_btn_go_inventory.png`: SHA256 `656c1308b1ed8b3125f3375b9a083c1f30b896a2a55db002bbf68a243b54452d`
- `proof_07_es_wardrobe_btn_go_inventory.png`: SHA256 `4f6a7327f361b0c83eee5e4c1ca9a9fb03e0763ba12ccea16921ff52fb447883`
