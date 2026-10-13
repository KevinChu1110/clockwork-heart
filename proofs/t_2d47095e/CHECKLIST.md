# 驗收自查清單 · 稱號佩戴、聚魂殿卸魂與儲能庫背包快捷三分支合併與主線回歸 (t_2d47095e)

## 任務基本資訊
- **卡號**：`t_2d47095e`
- **負責人**：阿翔（`sideworker2`）
- **合併分支**：
  1. `origin/agent/20261013-title-equip-lobby-t_7269c551`（TitleWallDialog 支援點擊佩戴稱號與大廳頭頂名牌即時連動，Merge commit: `d507c81d8`）
  2. `origin/agent/20261013-soul-hall-unequip-all-t_1c1c709a`（大廳聚魂殿堂新增『一鍵卸下』全部戰魂果凍按鈕與連動安全防護，Merge commit: `199f3eacb`）
  3. `origin/agent/20261013-vault-inventory-shortcut-t_b764030f`（ClockworkVaultDialog 發條儲能庫放置收益新增『前往背包』快捷果凍按鈕連動探索背包，Merge commit: `c50fc434a`）
- **目標分支**：`main`
- **最新 HEAD Commit**：`430bc9855`
- **審查員**：小婷（`sideqa`）

---

## 自查項目（對照 review.md 規範）

### 1. 分支整合成效與衝突解決
- [x] 三分支全數乾淨合併至 main，無未解衝突標記（Merge commits: `d507c81d8`, `199f3eacb`, `c50fc434a`）。
- [x] 多語系字典（`game/data/i18n/` 與 `game/data/i18n/content/*/ui.json`）衝突透過工具腳本完美融合，六語系鍵值齊全。
- [x] `docs/PROJECTS.json` 項目定義完整對齊，無遺漏。

### 2. 測試與驗證結果
- [x] **無頭引擎冒煙測試**：`godot --path game --headless --quit-after 3` 退出碼 0，0 SCRIPT ERROR。
- [x] **稱號佩戴單元測試**：`test_title_equip_lobby.gd` PASS（TEST_TITLE_EQUIP_LOBBY_OK）。
- [x] **聚魂殿一鍵卸下單元測試**：`test_soul_hall_unequip_all.gd` PASS（TEST_SOUL_HALL_UNEQUIP_ALL_OK）。
- [x] **儲能庫前往背包快捷單元測試**：`test_clockwork_vault_inventory_shortcut.gd` PASS（TEST_CLOCKWORK_VAULT_INVENTORY_SHORTCUT_OK）。
- [x] **回歸測試集**：`test_soul_hall_inventory_shortcut.gd` PASS、`test_vault_forge_shortcut.gd` PASS、`test_vault_double_claim.gd` PASS、`test_title_wall_i18n.gd` PASS。
- [x] **公開官網與舊名詞檢查**：`clock-check --live` 確認官網 14 頁全開、0 舊名詞。
- [x] **素材與軟連結檢查**：`clock-check /opt/side/bravesoul-game` 確認 0 缺 .import、0 軟連結。

### 3. 手遊人因與視覺規範
- [x] **零系統 Emoji**：TitleWallDialog、聚魂殿堂操作列、ClockworkVaultDialog 四按鈕均無原生 Emoji。
- [x] **果凍按鈕規格**：按鈕高度均 >= 50px（52px），圓角 18px，底厚 5px，描邊 #1F1A3A，多巴胺鮮亮色盤（珊瑚粉 #FF5E8A、薄荷綠 #4ED86A、金黃 #FFD028）。
- [x] **字級規範**：標籤與按鈕文字均 >= 16px，無碎小文字。
- [x] **六語系在地化**：zh_TW, zh_CN, en, ja, ko, es 均即時切換生效，歐美語系零 CJK。

### 4. 專案狀態同步
- [x] 使用 `python3 /root/project_status.py` 同步更新 `PROJECTS.json`：
  - `title-wall-equip`：已上線
  - `soul-hall-unequip-all`：已上線
  - `vault-inventory-shortcut`：已上線
  - `merge-title-soul-vault`：已上線
