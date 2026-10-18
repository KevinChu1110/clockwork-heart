# WardrobeDialog 前往工坊快捷果凍按鈕驗收存證 (t_ee1a4077)

## 1. 驗收標準檢驗
- [x] 按鈕存在於 WardrobeDialog 底部操作列 (actions_hbox)，名稱為 `BtnGoWorkshop`
- [x] 尺寸熱區 >= 48px（實裝 105x50px，符合手機人體工學）
- [x] 符合多巴胺亮色盤規範：薄荷綠底色 `#4ED86A`、圓角 16px、厚底 5px、深藍紫描邊與文字 `#1F1A3A`
- [x] 零系統 Emoji，使用粉圓體 (Open-Huninn)
- [x] 點擊後發射 `workshop_requested` / `go_workshop` 訊號並關閉衣櫥彈窗
- [x] 大廳接收訊號後即時開啟手藝工坊 `GemWorkshopDialog`
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es

## 2. 實機截圖存證清單
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_workshop.png`: SHA256 `4f986eeca923b0ac40d567620e0b0b4fe7e19d7f881005da9340ebc161fc38e1`
- `proof_02_zh_TW_gem_workshop_opened_from_wardrobe.png`: SHA256 `f950627532742e12cdab30c192391f48fa28978fb4f308e412eea82a3f395658`
- `proof_03_zh_CN_wardrobe_btn_go_workshop.png`: SHA256 `3d542bdcb01738b1d97f00a80a73e5579e25a28b3978fb3cd5bf7e687ab9e572`
- `proof_04_en_wardrobe_btn_go_workshop.png`: SHA256 `58af0a1ce75531323eebc73fb780c66f3dce0528c8b5313b3ca37877b932a198`
- `proof_05_ja_wardrobe_btn_go_workshop.png`: SHA256 `309fa731c659464babb2edc7e8c9b2c00d33f9110380715e02f036f8b4077f87`
- `proof_06_ko_wardrobe_btn_go_workshop.png`: SHA256 `198d6e0979f18bdcaacb431b9dccd0229f3c91cdb7bc0d9577b39068b59a6e09`
- `proof_07_es_wardrobe_btn_go_workshop.png`: SHA256 `01bab4fa48ef4940cd7c1aaac3a8d4c73a8bd9958d27d4bdd0a5555179b41c32`
