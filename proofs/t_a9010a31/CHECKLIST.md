# 驗收查核表 · t_a9010a31

## 任務
🎮 遊戲開發｜MapleInventory 探索背包底欄新增『前往稱號』快捷果凍按鈕連動 TitleWallDialog

## 驗收標準對照
- [x] **按鈕規格與樣式**：`BtnGoTitleWall` 位於 `GridBottomBar` 底欄，尺寸 120x48px（熱區 >= 48px），多巴胺天藍色盤 `#38A0FF`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`，果凍厚底 5px，圓角 18px，開源粉圓體 16px。
- [x] **0-UI1 零系統 Emoji**：100% 零系統 Emoji，純淨文字排版。
- [x] **訊號與連動**：點擊發射 `go_title_wall` 與 `title_wall_requested` 訊號，同時發射 `closed` 訊號安全關閉背包（無殘留遮罩），大廳連動開啟 `TitleWallDialog`。
- [x] **雙向快捷閉環**：關閉 `TitleWallDialog` 後可流暢重新開啟 `MapleInventory`。
- [x] **0-QA28 六語系即時切換**：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 全部完成字典對齊，英文與西班牙語系零 CJK 殘留。
- [x] **0-QA26 真實 Framebuffer 渲染存證**：透過 `xvfb-run -a godot` 擷取真實畫面，8 張截圖 SHA256 全部獨立唯一，無黑屏、無文字穿框。
- [x] **單元與回歸測試**：`test_maple_inventory_title_wall_shortcut.gd` (PASS)、`test_title_wall_inventory_shortcut.gd` (PASS)。
- [x] **clock-check**：`clock-check t_a9010a31` 零警告，完全通過 (✅ 全過)。

## 實機截圖存證清單 (SHA256)
- `proof_01_zh_TW_maple_inventory_btn_go_title_wall.png`: SHA256 `854dafc6578d4640f6caa12f02211826c5b58c0b43843c813d9600ff0b2602fa`
- `proof_02_zh_TW_click_go_title_wall_opens_title_wall_dialog.png`: SHA256 `96a6af4f38d79300cafe5a793da6f374b8477fa61f3461c8b2b56058a8dc9d93`
- `proof_08_loop_back_to_maple_inventory.png`: SHA256 `85f20a782eb33de2f2dafe14a5448c2faa7cfe28e8a5ece6ebef545c800448bd`
- `proof_03_zh_CN_maple_inventory_btn_go_title_wall.png`: SHA256 `2f65ddf306e9ded1a1b3baf3f5e282bab7a081e4276d3fe7477fa4ba144cd8c1`
- `proof_04_en_maple_inventory_btn_go_title_wall.png`: SHA256 `b0a370991d3dcc3c75a528d6af4a18aa436eb2ed8625c95c90dc2c6f38324a91`
- `proof_05_ja_maple_inventory_btn_go_title_wall.png`: SHA256 `0a43c08e60a682caef2181e2c20841d1fe1f9b3ad4fab755dce072c8fa3d62aa`
- `proof_06_ko_maple_inventory_btn_go_title_wall.png`: SHA256 `19ea0e9cac6a08ee9affb14644d3bc730aa07eb74b0adedeb1d302da06814007`
- `proof_07_es_maple_inventory_btn_go_title_wall.png`: SHA256 `25bc02d1bd88e3bfa3135701cc1b809566b0fa0c97197cf65deea4f8613ea6dc`
