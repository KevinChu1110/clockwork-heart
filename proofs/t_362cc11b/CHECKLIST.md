# 驗收項目自檢表（t_362cc11b: MapleInventory 探索背包支援分類頁籤 Chip 列）

## 1. 規格與功能檢查
- [x] 格子區上方配置 5 枚 Chip 按鈕：『全部』、『裝備』、『消耗品』、『素材』、『寶石』
- [x] 按鈕熱區高度達標：custom_minimum_size.y = 42px（>= 40px）
- [x] 按鈕圓角樣式：StyleBoxFlat set_corner_radius_all(15)（符合 14~16px 規範）
- [x] 深藍紫描邊：border_color COLOR_BORDER (#1F1A3A)
- [x] 零系統 Emoji 檢查：全介面文字 0 系統 Emoji
- [x] 預設選中『全部』，顯示所有道具；切換至對應分類時即時過濾：
  - 『裝備』：僅顯示 weapon / equip / equipment
  - 『消耗品』：僅顯示 consumable
  - 『素材』：僅顯示 material
  - 『寶石』：僅顯示 gem / jewel
- [x] 切換分類時若當前選取道具不在該分類中，重設選取狀態為空字串，右側面板顯示預設提示，操作按鈕 disabled
- [x] 六語系即時切換無缺詞：zh_TW（全部/裝備/消耗品/素材/寶石）、zh_CN（全部/装备/消耗品/素材/宝石）、en（All/Equipment/Consumable/Material/Gem）、ja（全部/装備/消耗品/素材/宝石）、ko（전체/장비/소모품/소재/보석）、es（Todo/Equipo/Consumible/Material/Gema）

## 2. 測試與存證
- [x] 單元測試 test_maple_inventory_chips.gd：通過（MAPLE_INVENTORY_CHIPS_OK）
- [x] 既有測試回歸 test_maple_inventory.gd：通過（MAPLE_INVENTORY_OK）
- [x] 既有測試回歸 test_maple_inventory_sort.gd：通過（MAPLE_INVENTORY_SORT_OK）
- [x] 語系測試回歸 test_inventory_item_i18n.gd：通過（INVENTORY_ITEM_I18N_OK）
- [x] 無頭冒煙測試 godot --path game --headless --quit-after 3：0 錯誤、0 SCRIPT ERROR
- [x] 實機截圖存證：
  - proofs/t_362cc11b/proof_01_chips_all.png（SHA256: 38e0b563...）
  - proofs/t_362cc11b/proof_02_chips_equip.png（SHA256: aba1f084...）
  - proofs/t_362cc11b/proof_03_chips_consumable.png（SHA256: 18b24495...）
  - proofs/t_362cc11b/proof_04_chips_en.png（SHA256: 6bb29694...）
- [x] 實機截圖無重複（SHA256 均不相同），經 Vision 審查版面完整無破圖
