# 驗收自查清單 · 手藝工坊與天宮鐵匠前往戰力快捷雙分支合併主線回歸 (t_56ee3721)

## 任務基本資訊
- **卡號**：`t_56ee3721`
- **負責人**：阿翔（`sideworker2`）
- **合併分支**：
  1. `agent/20261014-gem-workshop-power-stat-shortcut-t_69e139d8`（GemWorkshopDialog 手藝工坊新增前往戰力快捷果凍按鈕連動 PowerStatDialog）
  2. `agent/20261014-forge-power-stat-shortcut-t_a7b67508`（ForgeDialog 天宮鐵匠底欄新增前往戰力快捷果凍按鈕聯動 PowerStatDialog）
- **目標分支**：`main`
- **審查員**：小婷（`sideqa`）

---

## 自查項目（對照 review.md 與 clock-review-checklist 規範）

### 1. 分支整合成效與衝突解決
- [x] 雙分支全數乾淨合併至 main，無未解衝突標記。
- [x] 多語系字典（`game/data/i18n/` 與 `game/data/i18n/content/*/ui.json`）衝突透過雙向鍵值補齊完美融合，六語系鍵值齊全（`gem_workshop.btn_go_power_stat`、`forge.btn_go_power_stat`、`前往戰力` 等），並校正各語系對齊（ja: 鍛造へ進む, ko: 단조로 이동, es: Ir a Forja）。
- [x] `docs/PROJECTS.json` 項目定義完整對齊，並透過 `project_status.py` 規範更新狀態。

### 2. 測試與驗證結果
- [x] **無頭引擎冒煙測試**：`godot --path game --headless --quit-after 3` 退出碼 0，0 SCRIPT ERROR。
- [x] **手藝工坊前往戰力單元測試**：`test_gem_workshop_power_stat_shortcut.gd` PASS（TEST_GEM_WORKSHOP_POWER_STAT_SHORTCUT_OK）。
- [x] **天宮鐵匠前往戰力單元測試**：`test_forge_power_stat_shortcut.gd` PASS（TEST_FORGE_POWER_STAT_SHORTCUT_OK）。
- [x] **關聯回歸測試集**：
  - `test_power_stat_weapon_forge_shortcut.gd` PASS（TEST_POWER_STAT_WEAPON_FORGE_SHORTCUT_OK）
  - `test_weapon_swap_forge_shortcut.gd` PASS（TEST_WEAPON_SWAP_FORGE_SHORTCUT_OK）
  - `test_forge_workshop_shortcut.gd` PASS（TEST_FORGE_WORKSHOP_SHORTCUT_OK）
  - `test_gem_workshop_go_inventory.gd` PASS（TEST_GEM_WORKSHOP_GO_INVENTORY_OK）
  - `test_gem_workshop_i18n.gd` PASS（TEST_GEM_WORKSHOP_I18N_OK）
  - `test_forge_i18n.gd` PASS（TEST_FORGE_I18N_OK）
  - `test_power_stat_shortcuts.gd` PASS（TEST_POWER_STAT_SHORTCUTS_OK）
  - `test_power_stat_dialog.gd` PASS（TEST_POWER_STAT_DIALOG_OK）
  - `test_shop_shortcuts.gd` PASS（TEST_SHOP_SHORTCUTS_OK）
  - `test_shop_dialog.gd` PASS（SHOP_DIALOG_OK）
- [x] **公開官網與舊名詞檢查**：`clock-check --live` 確認官網 14 頁全開、0 舊名詞。
- [x] **素材與軟連結檢查**：`clock-check /opt/side/bravesoul-game` 確認 0 缺 .import、0 軟連結。

### 3. 手遊人因與視覺規範
- [x] **零系統 Emoji**：GemWorkshopDialog 前往戰力、ForgeDialog 前往戰力按鈕均無原生 Emoji。
- [x] **果凍按鈕規格**：按鈕尺寸熱區均 >= 48px（手藝工坊 145x50px，天宮鐵匠 145x50px），圓角 18px，底厚 5px，描邊 #1F1A3A，多巴胺天藍色盤 #38A0FF。
- [x] **字級規範**：按鈕文字均 >= 16px，無碎小文字，採用開源粉圓體。
- [x] **六語系在地化**：zh_TW, zh_CN, en, ja, ko, es 均即時切換生效，歐美語系零 CJK。
- [x] **雙向閉環**：手藝工坊 ↔ 戰力總覽、天宮鐵匠 ↔ 戰力總覽 雙向跳轉無遮罩殘留。

### 4. 專案狀態同步
- [x] 使用 `python3 /root/project_status.py` 同步更新 `PROJECTS.json`：
  - `gem-workshop-power-stat-shortcut`：已上線
  - `forge-power-stat-shortcut`：已上線
