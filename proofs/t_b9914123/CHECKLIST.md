# 驗收自查清單 · 商城聚魂鍛造快捷與戰力稱號卡片雙分支合併主線回歸 (t_b9914123)

## 任務基本資訊
- **卡號**：`t_b9914123`
- **負責人**：阿翔（`sideworker2`）
- **合併分支**：
  1. `origin/agent/20261013-shop-shortcuts-t_29493bde-v2`（ShopDialog 商城彈窗底部新增前往聚魂與前往鍛造快捷果凍按鈕）
  2. `origin/agent/20261013-power-stat-title-shortcut-t_931b088a`（PowerStatDialog 戰力屬性總覽新增稱號卡片與前往稱號牆快捷按鈕）
- **目標分支**：`main`
- **審查員**：小婷（`sideqa`）

---

## 自查項目（對照 review.md 規範）

### 1. 分支整合成效與衝突解決
- [x] 雙分支全數乾淨合併至 main，無未解衝突標記。
- [x] 多語系字典（`game/data/i18n/` 與 `game/data/i18n/content/*/ui.json`）衝突透過工具腳本與雙向注入完美融合，六語系鍵值齊全（`shop.btn_go_soul_hall`、`shop.btn_go_forge`、`power_stat.title_card`、`power_stat.btn_go_title_wall`、`power_stat.title_desc` 等）。
- [x] `docs/PROJECTS.json` 項目定義完整對齊，並透過 `project_status.py` 規範更新狀態。

### 2. 測試與驗證結果
- [x] **無頭引擎冒煙測試**：`godot --path game --headless --quit-after 3` 退出碼 0，0 SCRIPT ERROR。
- [x] **商城聚魂鍛造快捷單元測試**：`test_shop_shortcuts.gd` PASS（TEST_SHOP_SHORTCUTS_OK）。
- [x] **戰力總覽稱號快捷單元測試**：`test_power_stat_title_shortcut.gd` PASS（TEST_POWER_STAT_TITLE_SHORTCUT_OK）。
- [x] **關聯回歸測試集**：
  - `test_shop_inventory_shortcut.gd` PASS（TEST_SHOP_INVENTORY_SHORTCUT_OK）
  - `test_power_stat_core_shortcut.gd` PASS（POWER_STAT_CORE_SHORTCUT_OK）
  - `test_title_unequip.gd` PASS（TEST_TITLE_UNEQUIP_OK）
- [x] **公開官網與舊名詞檢查**：`clock-check --live` 確認官網 14 頁全開、0 舊名詞。
- [x] **素材與軟連結檢查**：`clock-check /opt/side/bravesoul-game` 確認 0 缺 .import、0 軟連結。

### 3. 手遊人因與視覺規範
- [x] **零系統 Emoji**：ShopDialog 前往聚魂／前往鍛造、PowerStatDialog 稱號卡片／前往稱號按鈕均無原生 Emoji。
- [x] **果凍按鈕規格**：按鈕尺寸熱區均 >= 48px（商城 160x52px，戰力 110x48px），圓角 16~18px，底厚 4~5px，描邊 #1F1A3A，多巴胺鮮亮色盤（聚魂珊瑚粉 #FF5E8A、鍛造金黃 #FFD028、稱號天藍 #38A0FF）。
- [x] **字級規範**：按鈕文字均 >= 16px，無碎小文字，採用開源粉圓體。
- [x] **六語系在地化**：zh_TW, zh_CN, en, ja, ko, es 均即時切換生效，歐美語系零 CJK。

### 4. 專案狀態同步
- [x] 使用 `python3 /root/project_status.py` 同步更新 `PROJECTS.json`：
  - `shop-soul-forge-shortcuts`：已上線
  - `power-stat-title-shortcut`：已上線
