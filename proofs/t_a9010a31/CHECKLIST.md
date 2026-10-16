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
