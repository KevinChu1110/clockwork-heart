# 驗收自查清單 · 稱號卸下與商城背包快捷雙分支合併與主線回歸 (t_97107a4e)

## 任務基本資訊
- **卡號**：`t_97107a4e`
- **負責人**：阿翔（`sideworker2`）
- **合併分支**：
  1. `origin/agent/20261013-title-unequip-t_71a3c58d`（TitleWallDialog 稱號牆新增『卸下稱號』果凍按鈕與連動安全防護，Commit: `4bccffd38`）
  2. `origin/agent/20261013-shop-inventory-shortcut-t_6821e62c`（ShopDialog 商城彈窗底部新增『前往背包』快捷果凍按鈕連動探索背包，Commit: `9a193d060`，Merge commit: `5af79dec1`）
- **目標分支**：`main`
- **審查員**：小婷（`sideqa`）

---

## 自查項目（對照 review.md 規範）

### 1. 分支整合成效與衝突解決
- [x] 雙分支全數乾淨合併至 main，無未解衝突標記。
- [x] 多語系字典（`game/data/i18n/` 與 `game/data/i18n/content/*/ui.json`）衝突透過工具腳本與雙向注入完美融合，六語系鍵值齊全（`卸下稱號`、`shop.btn_go_inventory`、`前往背包`）。
- [x] `docs/PROJECTS.json` 項目定義完整對齊，無遺漏。

### 2. 測試與驗證結果
- [x] **無頭引擎冒煙測試**：`godot --path game --headless --quit-after 3` 退出碼 0，0 SCRIPT ERROR。
- [x] **稱號卸下單元測試**：`test_title_unequip.gd` PASS（TEST_TITLE_UNEQUIP_OK）。
- [x] **商城前往背包快捷單元測試**：`test_shop_inventory_shortcut.gd` PASS（TEST_SHOP_INVENTORY_SHORTCUT_OK）。
- [x] **稱號佩戴與大廳連動單元測試**：`test_title_equip_lobby.gd` PASS（TEST_TITLE_EQUIP_LOBBY_OK）。
- [x] **商城基礎彈窗單元測試**：`test_shop_dialog.gd` PASS（SHOP_DIALOG_OK）。
- [x] **關聯回歸測試集**：`test_title_wall_i18n.gd` PASS、`test_energy_lack_shop_shortcut.gd` PASS。
- [x] **公開官網與舊名詞檢查**：`clock-check --live` 確認官網 14 頁全開、0 舊名詞。
- [x] **素材與軟連結檢查**：`clock-check /opt/side/bravesoul-game` 確認 0 缺 .import、0 軟連結。

### 3. 手遊人因與視覺規範
- [x] **零系統 Emoji**：TitleWallDialog 卸下稱號按鈕、ShopDialog 前往背包按鈕均無原生 Emoji。
- [x] **果凍按鈕規格**：按鈕高度均 >= 50px（52px），圓角 18px，底厚 5px，描邊 #1F1A3A，多巴胺鮮亮色盤（珊瑚粉 #FF5E8A、薄荷綠 #4ED86A）。
- [x] **字級規範**：按鈕文字均 >= 16px（17~18px），無碎小文字。
- [x] **六語系在地化**：zh_TW, zh_CN, en, ja, ko, es 均即時切換生效，歐美語系零 CJK。

### 4. 專案狀態同步
- [x] 使用 `python3 /root/project_status.py` 同步更新 `PROJECTS.json`：
  - `title-wall-unequip`：已上線
  - `shop-inventory-shortcut`：已上線
  - `merge-title-shop-shortcuts`：已上線
