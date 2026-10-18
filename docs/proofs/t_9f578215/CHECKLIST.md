# 驗收清單 · ForgeDialog 天宮鐵匠底欄新增『前往儲能庫』快捷果凍按鈕連動 ClockworkVaultDialog (t_9f578215)

## 驗收項目自查
- [x] **按鈕節點與樣式**：`BtnGoVault` 位於 `act_row` 底欄，尺寸 140x50px（>= 115x50px，熱區 >= 48px），多巴胺金黃底色 `#FFD028`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`，16px 粉圓體，100% 零 Emoji。
- [x] **存取器與訊號**：提供 `get_go_vault_button()` 存取器，發射 `vault_requested` 與 `go_vault` 訊號。
- [x] **連動與安全性**：點擊後安全關閉 `ForgeDialog`（發射 `closed` 訊號無遮罩殘留），連動 `MobileLobby` 開啟 `ClockworkVaultDialog`。
- [x] **雙向閉環**：發條儲能庫視窗關閉後可順暢返回 `ForgeDialog`（支援 `forge_requested` / `_on_go_forge_pressed`）。
- [x] **六語系支援**：`ContentLoc` 與 `Loc` 字典齊全（`forge.btn_go_vault` 與 `ui.btn_go_vault`），繁中、簡中、英文、日文、韓文、西文即時切換無誤：
  - 繁體中文 (zh_TW)：前往儲能庫
  - 簡體中文 (zh_CN)：前往储能库
  - 英文 (en)：To Vault
  - 日文 (ja)：貯蔵庫へ
  - 韓文 (ko)：저장고로 이동
  - 西班牙文 (es)：Ir a Bóveda
- [x] **自動檢查**：`clock-check` 通過，0 缺漏素材、0 軟連結、0 舊名詞。
- [x] **單元與回歸測試**：`test_forge_dialog_vault_shortcut.gd` (PASS_OK)、`test_vault_forge_shortcut.gd` (PASS_OK)、無頭冒煙測試 (PASS)。
- [x] **實機存證截圖**：8 張 OpenGL3 實機畫面截圖，SHA256 獨立完整。

## 存證截圖檔案
1. `proof_01_zh_TW_forge_dialog_btn_go_vault.png` - 繁中天宮鐵匠底欄 BtnGoVault 快捷按鈕高解析畫面
2. `proof_02_click_btn_go_vault_opens_clockwork_vault_dialog.png` - 點擊 BtnGoVault 後安全關閉鐵匠並連動開啟發條儲能庫放置收益視窗
3. `proof_03_vault_dialog_loop_back_to_forge.png` - 發條儲能庫彈窗關閉返回天宮鐵匠彈窗之雙向閉環驗證
4. `proof_04_zh_CN_forge_dialog_btn_go_vault.png` - 簡體中文即時切換「前往储能库」驗證
5. `proof_05_en_forge_dialog_btn_go_vault.png` - 英文即時切換「To Vault」驗證
6. `proof_06_ja_forge_dialog_btn_go_vault.png` - 日文即時切換「貯蔵庫へ」驗證
7. `proof_07_ko_forge_dialog_btn_go_vault.png` - 韓文即時切換「저장고로 이동」驗證
8. `proof_08_es_forge_dialog_btn_go_vault.png` - 西班牙文即時切換「Ir a Bóveda」驗證
