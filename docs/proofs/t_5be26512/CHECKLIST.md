# 驗收清單 · GemWorkshopDialog 手藝工坊底欄新增『前往稱號』快捷果凍按鈕連動 TitleWallDialog (t_5be26512)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoTitleWall` 位於 `foot_row` 底欄，尺寸 130x50px（寬 >= 120px，高 >= 50px，熱區 >= 48px），多巴胺金黃底色 `#FFD028`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`，16px 粉圓體，100% 零 Emoji。
- [x] **存取器與訊號**：提供 `get_go_title_wall_button()`、`get_title_wall_button()` 與 `get_btn_go_title_wall()` 存取器，發射 `title_wall_requested` 與 `go_title_wall` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `GemWorkshopDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 開啟 `TitleWallDialog` 稱號牆。
- [x] **雙向閉環**：手藝工坊與稱號牆互通流暢。
- [x] **六語系支援**：`ContentLoc` 與 `Loc` 字典齊全（`gem_workshop.btn_go_title_wall` 與 `gem_workshop.go_title_wall`），繁中、簡中、英文、日文、韓文、西文即時切換無誤：
  - 繁體中文 (zh_TW)：前往稱號
  - 簡體中文 (zh_CN)：前往称号
  - 英文 (en)：To Titles
  - 日文 (ja)：称号へ
  - 韓文 (ko)：칭호로 이동
  - 西班牙文 (es)：Ir a Títulos
- [x] **自動檢查**：`clock-check` 通過，0 缺漏素材、0 軟連結、0 舊名詞。
- [x] **單元與回歸測試**：`test_gem_workshop_title_wall_shortcut.gd` (PASS_OK)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 真實 Framebuffer 畫面截圖，SHA256 獨立完整。

## 存證截圖檔案
1. `proof_01_zh_TW_gem_workshop_btn_go_title_wall.png` - 繁中手藝工坊底欄 BtnGoTitleWall 快捷按鈕高解析實機畫面
2. `proof_02_zh_TW_gem_workshop_case_tab_title_wall_btn.png` - 寶石櫃盤點分頁下 BtnGoTitleWall 快捷按鈕常駐顯示
3. `proof_03_zh_TW_title_wall_opened_from_gem_workshop.png` - 點擊 BtnGoTitleWall 後安全關閉手藝工坊並連動開啟 TitleWallDialog 稱號牆
4. `proof_04_zh_CN_gem_workshop_btn_go_title_wall.png` - 簡體中文即時切換「前往称号」驗證
5. `proof_05_en_gem_workshop_btn_go_title_wall.png` - 英文即時切換「To Titles」驗證
6. `proof_06_ja_gem_workshop_btn_go_title_wall.png` - 日文即時切換「称号へ」驗證
7. `proof_07_ko_gem_workshop_btn_go_title_wall.png` - 韓文即時切換「칭호로 이동」驗證
8. `proof_08_es_gem_workshop_btn_go_title_wall.png` - 西班牙文即時切換「Ir a Títulos」驗證
