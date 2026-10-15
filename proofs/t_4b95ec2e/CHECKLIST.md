# 驗收查核表 (CHECKLIST) · WardrobeDialog 前往稱號快捷按鈕 (t_4b95ec2e)

## 驗收項目逐項檢查

- [x] **按鈕規格樣式**：
  - [x] 節點名稱為 `BtnGoTitleWall`。
  - [x] 按鈕尺寸 `105x50px`，滿足 `>= 48px` 手機端熱區規範。
  - [x] 底色暖橘色盤 `#FFA010` (COLOR_ORANGE)，邊框深藍紫 `#1F1A3A` (COLOR_BORDER)，文字深藍紫 `#1F1A3A`。
  - [x] 果凍厚底 `5px`，圓角 `18px`，字級 `16px` 開源粉圓體。
  - [x] 100% 徹底清除遊戲內系統 Emoji（零系統 Emoji）。
- [x] **點擊連動與訊號**：
  - [x] 點擊發射 `title_wall_requested` 訊號。
  - [x] 安全關閉 `WardrobeDialog`（發射 `closed` 訊號，無遮罩殘留）。
  - [x] `MobileLobby` (mobile_lobby.gd) 監聽 `title_wall_requested` 並連動開啟 `TitleWallDialog`。
  - [x] 直通稱號牆彈窗。
- [x] **存取器**：
  - [x] `get_go_title_wall_button() -> Button`。
  - [x] `get_title_wall_button() -> Button`。
- [x] **六語系在地化**：
  - [x] `zh_TW`: 前往稱號
  - [x] `zh_CN`: 前往称号
  - [x] `en`: Go to Titles
  - [x] `ja`: 称号一覧へ
  - [x] `ko`: 칭호로 이동
  - [x] `es`: Ir a Títulos
  - [x] `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處均已同步支援 `wardrobe.go_title_wall` / `wardrobe.btn_go_title_wall`。
- [x] **測試與存證**：
  - [x] 單元與整合測試 `test_wardrobe_title_wall_shortcut.gd` 全部 PASS (`TEST_WARDROBE_TITLE_WALL_SHORTCUT_OK`)。
  - [x] 關聯測試 `test_wardrobe_shop_shortcut.gd`、`test_shop_wardrobe_shortcut.gd`、`test_wardrobe_power_stat_shortcut.gd`、`test_power_stat_wardrobe_card.gd`、`test_wardrobe_i18n.gd`、`test_title_wall_power_stat_shortcut.gd` 全數 PASS。
  - [x] `clock-check` 自動化檢查通過（無語系死 key、無退役詞、素材正常）。
  - [x] 7 張實機截圖完整產出且 SHA256 唯一無重複：
    - `proof_01_zh_TW_wardrobe_dialog_with_btn_go_title_wall.png` (162954678ccbd28e5f53a54a19628c7d20c06ff7569c194a8e726857e726349c)
    - `proof_02_zh_TW_title_wall_dialog_opened_from_wardrobe.png` (ef5dc2eeca585ec4e2e1d78d742ed4de7adcf623f8f82a1754b6ecc7161d9a23)
    - `proof_03_zh_TW_wardrobe_closed_clean.png` (92afc677f9955e9474258dd0dc7d3b95e19893f2bbc699dca9fec409ee650b76)
    - `proof_04_en_wardrobe_title_wall_btn.png` (990e43429ba337cdb19c7aae31765938f0bc7d85c1ccf6374ce65a6960c85bc5)
    - `proof_05_ja_wardrobe_title_wall_btn.png` (a713c7eb1cc958cfd2ffd53e4fdd05482d503ada27eb4635725268f35c9c84a8)
    - `proof_06_ko_wardrobe_title_wall_btn.png` (6f9eca881763ae488f48cedbf67059b5de695888e4c253d2ba206b8b7e5b9ab9)
    - `proof_07_es_wardrobe_title_wall_btn.png` (7121ff18eddcf772e46f2613a2ed4221b008fdea86d9dd3d24eb7584652174c6)
  - [x] 符合 review.md 第 0-OPS 與 UI 規範。
