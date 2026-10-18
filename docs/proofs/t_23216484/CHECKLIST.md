# 驗收清單 · TitleWallDialog 稱號牆底欄新增『前往工坊』快捷果凍按鈕連動 GemWorkshopDialog (t_23216484)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoWorkshop` 位於 `ButtonRow` 底欄，尺寸 150x52px（寬 >= 120px，高 >= 50px，熱區 >= 48px），多巴胺薄荷綠底色 `#4ED86A`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`，18px 粉圓體，100% 零 Emoji。
- [x] **存取器與訊號**：提供 `get_go_workshop_button()` 與 `get_workshop_button()` 存取器，發射 `workshop_requested` 與 `go_workshop` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `TitleWallDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 開啟 `GemWorkshopDialog` 手藝工坊。
- [x] **雙向閉環**：手藝工坊視窗關閉後可順暢返回 `TitleWallDialog`。
- [x] **六語系支援**：`ContentLoc` 與 `Loc` 字典齊全（`title_wall.btn_go_workshop` 與 `title_wall.go_workshop`），繁中、簡中、英文、日文、韓文、西文即時切換無誤：
  - 繁體中文 (zh_TW)：前往工坊
  - 簡體中文 (zh_CN)：前往工坊
  - 英文 (en)：Go to Workshop
  - 日文 (ja)：工房へ進む
  - 韓文 (ko)：공방으로 이동
  - 西班牙文 (es)：Ir al Taller
- [x] **自動檢查**：`clock-check` 通過，0 缺漏素材、0 軟連結、0 舊名詞。
- [x] **單元與回歸測試**：`test_title_wall_dialog_workshop_shortcut.gd` (PASS_OK)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 真實 Framebuffer 畫面截圖，SHA256 獨立完整。

## 存證截圖檔案
1. `proof_01_zh_TW_title_wall_with_btn_go_workshop.png` - 繁中稱號牆底欄 BtnGoWorkshop 快捷按鈕高解析實機畫面
2. `proof_02_zh_TW_workshop_opened_from_title_wall.png` - 點擊 BtnGoWorkshop 後安全關閉稱號牆並連動開啟手藝工坊視窗
3. `proof_03_zh_CN_title_wall_btn_go_workshop.png` - 簡體中文即時切換「前往工坊」驗證
4. `proof_04_en_title_wall_btn_go_workshop.png` - 英文即時切換「Go to Workshop」驗證
5. `proof_05_ja_title_wall_btn_go_workshop.png` - 日文即時切換「工房へ進む」驗證
6. `proof_06_ko_title_wall_btn_go_workshop.png` - 韓文即時切換「공방으로 이동」驗證
7. `proof_07_es_title_wall_btn_go_workshop.png` - 西班牙文即時切換「Ir al Taller」驗證
8. `proof_08_loop_back_to_title_wall.png` - 手藝工坊關閉返回稱號牆之雙向閉環驗證
