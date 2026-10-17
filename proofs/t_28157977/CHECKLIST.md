# 驗收清單 · ForgeDialog 天宮鐵匠底欄新增『前往衣櫥』快捷果凍按鈕連動 WardrobeDialog (t_28157977)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoWardrobe` 位於 `act_row` 底欄，尺寸 140x50px（>= 115x50px，熱區 >= 48px），多巴胺金黃底色 `#FFD028`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`，16px 粉圓體，100% 零 Emoji。
- [x] **存取器與訊號**：提供 `get_go_wardrobe_button()` 存取器，發射 `wardrobe_requested` 與 `go_wardrobe` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `ForgeDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 開啟 `WardrobeDialog`。
- [x] **雙向閉環**：衣櫥換裝視窗關閉後可順暢返回 `ForgeDialog`。
- [x] **六語系支援**：`ContentLoc` 字典齊全（`forge.btn_go_wardrobe` 與 `ui.btn_go_wardrobe`），繁中、簡中、英文、日文、韓文、西文即時切換無誤。
- [x] **自動檢查**：`clock-check` 通過，0 缺漏素材、0 軟連結、0 舊名詞。
- [x] **單元與回歸測試**：`test_forge_dialog_wardrobe_shortcut.gd` (PASS_OK)、`test_forge_dialog_*` (7/7 PASS)、`test_batch_*` (8/8 PASS)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 實機畫面截圖，SHA256 獨立完整。
