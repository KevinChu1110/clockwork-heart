# WardrobeDialog 前往心法快捷果凍按鈕驗收存證 (t_d81cf274)

## 1. 驗收標準檢驗
- [x] 按鈕存在於 WardrobeDialog 底部操作列 (actions_hbox)，名稱為 `BtnGoSkill`
- [x] 尺寸熱區 >= 48px（實裝 105x52px，符合手機人體工學）
- [x] 符合多巴胺亮色盤規範：珊瑚粉底色 `#FF5E8A`、圓角 16px、厚底 5px、深藍紫描邊與文字 `#1F1A3A`
- [x] 零系統 Emoji，使用粉圓體 (Open-Huninn)
- [x] 點擊後發射 `skill_requested` / `go_skill` 訊號並關閉衣櫥彈窗
- [x] 大廳接收訊號後即時開啟招式心法彈窗 `SkillDialog`
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es

## 2. 實機截圖存證清單
- `proof_01_zh_TW_wardrobe_dialog_with_btn_go_skill.png`: SHA256 `147155a5d008073c1d1c75cc40f8d9427dd83b175b3423309c66d679f79b1ee2`
- `proof_02_zh_TW_skill_dialog_opened_from_wardrobe.png`: SHA256 `6619a614fdf69a715e0476b8b4f2b44757de2a0e178184cb39ec2fcae1efc5fc`
- `proof_03_zh_CN_wardrobe_btn_go_skill.png`: SHA256 `25f179fc45025f52d7bbf47c6a6eb2bcc7d0fd04d0410a0243950281b13e4939`
- `proof_04_en_wardrobe_btn_go_skill.png`: SHA256 `3d26313f589a9ebc53d11a93ab7634d6ed5cb6c2911e0c3330867b9e3795a215`
- `proof_05_ja_wardrobe_btn_go_skill.png`: SHA256 `7bb1baaee7084f0843b4169798387d01d0c1bbbfdd66dd29425788989a370aaf`
- `proof_06_ko_wardrobe_btn_go_skill.png`: SHA256 `d92133ad550f79342ec05e3d0b7aa681096b9dfbe6388d296597ce28e82109a0`
- `proof_07_es_wardrobe_btn_go_skill.png`: SHA256 `8f9fc2f7f62cc47b1d5ebe7121a51166a54db9c01ad2cb5ceac707f74615677b`
