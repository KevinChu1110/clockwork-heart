# WardrobeDialog 前往儲能庫快捷果凍按鈕驗收存證 (t_933567fb)

## 1. 驗收標準檢驗
- [x] 按鈕存在於 WardrobeDialog 底部操作列 (actions_hbox)，名稱為 `BtnGoVault`
- [x] 尺寸熱區 >= 48px（實裝 105x50px，符合手機人體工學）
- [x] 符合多巴胺亮色盤規範：金黃底色 `#FFD028`、圓角 18px、厚底 5px、深藍紫描邊與文字 `#1F1A3A`
- [x] 零系統 Emoji，使用粉圓體 (Open-Huninn)
- [x] 點擊後發射 `vault_requested` / `go_vault` 訊號並關閉衣櫥彈窗
- [x] 大廳接收訊號後即時開啟發條儲能庫 `ClockworkVaultDialog`
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es

## 2. 實機截圖存證清單
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_vault.png`: SHA256 `fdd631ae825213194bf42864eb1436a6f428133fc82b91bd782b4495d526c73c`
- `proof_02_zh_TW_vault_opened_from_wardrobe.png`: SHA256 `075f5d9ddbbf93c06d7d9642036b7aaa20097875f0abe50a93e02049a4f674b0`
- `proof_03_zh_CN_wardrobe_btn_go_vault.png`: SHA256 `cccfea6e629f5695e7a87892a0bc2e25971c85e9e9afcb1b43f3d02a9d61c358`
- `proof_04_en_wardrobe_btn_go_vault.png`: SHA256 `512acdc72b02eee7463fd5a6c5b84e876a447df011fe000ab1ac1cb388520791`
- `proof_05_ja_wardrobe_btn_go_vault.png`: SHA256 `4e36d352e1ad3cab405c1e9240047a17934b216a9826282be7465c1b76567158`
- `proof_06_ko_wardrobe_btn_go_vault.png`: SHA256 `1adc1da7fbb38c0650e4cb1792c58c3610b1e296d0454049662ef5e3f57e2257`
- `proof_07_es_wardrobe_btn_go_vault.png`: SHA256 `244113c2b966840aadfc50d6eebe8cad4852594f6d8d200534508725b19099d0`
