# 驗收自查清單 · 稱號牆前往戰力與心法前往戰力快捷雙分支合併主線回歸 (t_de763658)

## 任務基本資訊
- **卡號**：`t_de763658`
- **負責人**：阿翔（`sideworker2`）
- **合併分支**：
  1. `origin/agent/20261013-title-wall-power-stat-shortcut-t_a4d9427b`（TitleWallDialog 稱號牆新增前往戰力快捷果凍按鈕連動 PowerStatDialog）
  2. `origin/agent/20261013-skill-power-stat-shortcut-t_d703bf0e`（SkillDialog 心法招式底欄新增前往戰力快捷果凍按鈕聯動 PowerStatDialog）
- **目標分支**：`main`
- **審查員**：小婷（`sideqa`）

---

## 自查項目（對照 review.md 與 clock-review-checklist 規範）

### 1. 分支整合成效與衝突解決
- [x] 雙分支全數乾淨合併至 main，無未解衝突標記。
- [x] 多語系字典（`game/data/i18n/` 與 `game/data/i18n/content/*/ui.json`）衝突透過雙向鍵值補齊完美融合，六語系鍵值齊全（`title_wall.btn_go_power_stat`、`skill.btn_go_power_stat`、`前往戰力` 等）。
- [x] `docs/PROJECTS.json` 項目定義完整對齊，並透過 `project_status.py` 規範更新狀態。

### 2. 測試與驗證結果
- [x] **無頭引擎冒煙測試**：`godot --path game --headless --quit-after 3` 退出碼 0，0 SCRIPT ERROR。
- [x] **稱號牆前往戰力單元測試**：`test_title_wall_power_stat_shortcut.gd` PASS（TEST_TITLE_WALL_POWER_STAT_SHORTCUT_OK）。
- [x] **心法招式前往戰力單元測試**：`test_skill_power_stat_shortcut.gd` PASS（TEST_SKILL_POWER_STAT_SHORTCUT_OK）。
- [x] **關聯回歸測試集**：
  - `test_power_stat_title_shortcut.gd` PASS（TEST_POWER_STAT_TITLE_SHORTCUT_OK）
  - `test_title_unequip.gd` PASS（TEST_TITLE_UNEQUIP_OK）
  - `test_power_stat_core_shortcut.gd` PASS（POWER_STAT_CORE_SHORTCUT_OK）
  - `test_title_wall_i18n.gd` PASS（TEST_TITLE_WALL_I18N_OK）
  - `test_skill_i18n.gd` PASS（TEST_SKILL_I18N_OK）
  - `test_title_equip_lobby.gd` PASS（TEST_TITLE_EQUIP_LOBBY_OK）
  - `test_lobby_skill_dialog_btn.gd` PASS（LOBBY_SKILL_DIALOG_BTN_TEST_OK）
- [x] **公開官網與舊名詞檢查**：`clock-check --live` 確認官網 14 頁全開、0 舊名詞。
- [x] **素材與軟連結檢查**：`clock-check /opt/side/bravesoul-game` 確認 0 缺 .import、0 軟連結。

### 3. 手遊人因與視覺規範
- [x] **零系統 Emoji**：TitleWallDialog 前往戰力、SkillDialog 前往戰力按鈕均無原生 Emoji。
- [x] **果凍按鈕規格**：按鈕尺寸熱區均 >= 48px（稱號牆 160x52px，心法 160x50px），圓角 18px，底厚 5px，描邊 #1F1A3A，多巴胺鮮亮色盤（稱號牆天藍 #38A0FF、心法金黃 #FFD028）。
- [x] **字級規範**：按鈕文字均 >= 16px，無碎小文字，採用開源粉圓體。
- [x] **六語系在地化**：zh_TW, zh_CN, en, ja, ko, es 均即時切換生效，歐美語系零 CJK。
- [x] **視覺模型自檢**：經 Vision Analyze 逐項確認，按鈕無破圖、無溢出、無文字穿框。

### 4. 專案狀態同步
- [x] 使用 `python3 /root/project_status.py` 同步更新 `PROJECTS.json`：
  - `title-wall-power-stat-shortcut`：已上線
  - `skill-power-stat-shortcut`：已上線
