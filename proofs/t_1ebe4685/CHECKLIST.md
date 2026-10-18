# 驗收清單 · ForgeDialog 天宮鐵匠底欄新增『前往稱號』快捷果凍按鈕聯動 TitleWallDialog (t_1ebe4685)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoTitleWall` 位於 `act_row` 底欄，尺寸 140x50px（>= 115x50px，熱區 >= 48px），多巴胺金黃底色 `#FFD028`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`，16px 粉圓體，100% 零系統 Emoji。
- [x] **彈窗排版與捲動**：底欄按鈕列封裝於 `ActionScroll`（ScrollContainer，橫向捲動支援），彈窗維持標準 750px 置中卡片，全視窗無溢出、無截斷。
- [x] **存取器與訊號**：提供 `get_go_title_wall_button()` 與 `get_action_scroll()` 存取器，點擊發射 `title_wall_requested` 與 `go_title_wall` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `ForgeDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 無縫開啟 `TitleWallDialog` 稱號牆。
- [x] **雙向閉環**：稱號牆關閉後可順暢返回 `ForgeDialog` 裝備鍛造彈窗。
- [x] **六語系支援**：`ContentLoc` 與 `Loc` 雙向 12 個字典鍵值完全對齊（`forge.btn_go_title_wall`），繁中、簡中、英文、日文、韓文、西文即時切換無誤：
  - 繁體中文 (zh_TW)：前往稱號
  - 簡體中文 (zh_CN)：前往称号
  - 英文 (en)：To Titles
  - 日文 (ja)：称号へ
  - 韓文 (ko)：칭호로 이동
  - 西班牙文 (es)：Ir a Títulos
- [x] **自動檢查**：`clock-check` 通過（✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）。
- [x] **單元與整合測試**：`test_forge_dialog_title_wall_shortcut.gd` (PASS_OK)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 實機畫面截圖（xvfb-run），SHA256 獨立完整，經 Vision 審查合格。遵守 review.md 第 1104 條與第 16 條。

## 存證截圖清單
1. `proof_01_zh_TW_forge_dialog_btn_go_title_wall.png` (SHA256: `fe1585c75e814b53...`) - 繁中天宮鐵匠底欄 BtnGoTitleWall 快捷按鈕高解析畫面
2. `proof_02_click_btn_go_title_wall_opens_title_wall_dialog.png` (SHA256: `e54bbe98748b8a77...`) - 點擊 BtnGoTitleWall 後安全關閉鐵匠並連動開啟 TitleWallDialog 稱號牆彈窗
3. `proof_03_title_wall_dialog_loop_back_to_forge.png` (SHA256: `b4956d0c4ed9df01...`) - 稱號牆彈窗關閉返回天宮鐵匠彈窗之雙向閉環驗證
4. `proof_04_zh_CN_forge_dialog_btn_go_title_wall.png` (SHA256: `03747ee2ae5e22dc...`) - 簡體中文即時切換「前往称号」驗證
5. `proof_05_en_forge_dialog_btn_go_title_wall.png` (SHA256: `cdd2ebe0d5c90706...`) - 英文即時切換「To Titles」驗證
6. `proof_06_ja_forge_dialog_btn_go_title_wall.png` (SHA256: `3155ca691ed1d98e...`) - 日文即時切換「称号へ」驗證
7. `proof_07_ko_forge_dialog_btn_go_title_wall.png` (SHA256: `a3f9352d945908d1...`) - 韓文即時切換「칭호로 이동」驗證
8. `proof_08_es_forge_dialog_btn_go_title_wall.png` (SHA256: `43e8edbab1f3d5ac...`) - 西班牙文即時切換「Ir a Títulos」驗證
