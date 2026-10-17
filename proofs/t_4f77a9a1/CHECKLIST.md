# 驗收清單 · GemWorkshopDialog 手藝工坊底欄新增『前往衣櫥』快捷果凍按鈕連動 WardrobeDialog (t_4f77a9a1)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoWardrobe` 位於 `foot_row` 底欄，尺寸 130x50px（熱區 >= 48px），多巴胺暖橘底色 `#FFA010`、圓角 16px、底厚 5px、深藍紫描邊 2px `#1F1A3A`，16px 粉圓體，100% 零 Emoji。
- [x] **存取器與訊號**：提供 `get_go_wardrobe_button()` 存取器，發射 `wardrobe_requested` 與 `go_wardrobe` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `GemWorkshopDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 開啟 `WardrobeDialog`。
- [x] **常駐可見性**：切換熔煉與寶石櫃分頁，`BtnGoWardrobe` 保持常駐正常顯示。
- [x] **六語系支援**：`ContentLoc` 字典齊全（`gem_workshop.btn_go_wardrobe` 與 `ui.btn_go_wardrobe`），繁中、簡中、英文、日文、韓文、西文即時切換無誤。
- [x] **自動檢查**：`clock-check` 通過，0 缺漏素材、0 軟連結、0 舊名詞。
- [x] **單元與回歸測試**：`test_gem_workshop_wardrobe_shortcut.gd` (PASS_OK)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 實機畫面截圖，SHA256 獨立完整無重複。
