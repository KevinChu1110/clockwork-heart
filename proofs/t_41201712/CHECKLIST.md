# 驗收查核清單 CHECKLIST · ForgeDialog 天宮鐵匠底欄新增『前往背包』快捷果凍按鈕聯動 MapleInventory (t_41201712)

> 驗收執行人：發條之心·工程師 阿翔 (`sideworker2`)  
> 驗收分支：`agent/20261017-forge-dialog-inventory-shortcut-t_41201712`

---

## 1. 介面與規格驗收

- [x] **按鈕規格與命名**：
  - 按鈕節點命名為 `BtnGoInventory`，位於 ForgeDialog 底部操作按鈕列 (`act_row`)。
  - 按鈕尺寸 `115x50px`，熱區規格 `>= 48px`（高度 50px），符合手遊人體工學防誤觸規範。
- [x] **色彩與果凍視覺風格**：
  - 採用多巴胺天藍色盤 `COLOR_SKY` (`#38A0FF`)，立體果凍厚底 5px，大圓角 18px，深藍紫描邊 `#1F1A3A`。
  - 字級 16px 開源粉圓體（Open Huninn），深藍紫字帶描邊，視覺對比清晰。
  - 100% 徹底清除系統 Emoji，無廉價感。
- [x] **訊號與連動機制**：
  - 提供 `inventory_requested` 與 `go_inventory` 雙訊號，並提供 `get_go_inventory_button()` 存取器。
  - 點擊按鈕安全發射 `closed` 與跳轉訊號，順暢關閉 ForgeDialog（無遮罩與彈窗殘留）。
  - 大廳 `MobileLobby` 接收訊號直通開啟 `MapleInventory` 探索背包彈窗。
- [x] **雙向閉環流轉**：
  - 在探索背包中點擊『前往鍛造』(`BtnBagGoForge`) 可順暢關閉背包並返回 `ForgeDialog`，形成雙向操作閉環。
- [x] **六語系即時切換**：
  - 繁中 `zh_TW`：`前往背包`
  - 簡中 `zh_CN`：`前往背包`
  - 英文 `en`：`Go to Inventory`
  - 日文 `ja`：`インベントリへ進む`
  - 韓文 `ko`：`인벤토리로 이동`
  - 西文 `es`：`Ir al Inventario`
  - 12 處多語系字典完全對齊（`ui.json` 與 `<locale>.json`）。

---

## 2. 測試與存證截圖

- [x] **專屬單元與整合測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_forge_dialog_inventory_shortcut.gd --headless`，輸出 `TEST_FORGE_DIALOG_INVENTORY_SHORTCUT_OK`。
- [x] **無頭冒煙測試**：
  - 執行 `godot --path game --headless --quit-after 3`，0 SCRIPT ERROR / 0 Crash。
- [x] **關聯回歸測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_forge_shop_shortcut.gd --headless`，全部通過。
- [x] **實機渲染截圖存證**（`xvfb-run` 獨立截圖）：
  - `proof_01_zh_TW_forge_dialog_btn_go_inventory.png` (SHA256: 774e67b658a2ae05...)：繁中介面與天藍色 BtnGoInventory
  - `proof_02_click_btn_go_inventory_opens_maple_inventory.png` (SHA256: 9a56221ab2ea3dc4...)：直通開啟 MapleInventory 探索背包彈窗
  - `proof_03_maple_inventory_loop_back_to_forge.png` (SHA256: bc895b2920ee7d33...)：點擊前往鍛造返回 ForgeDialog 雙向閉環
  - `proof_04_zh_CN_forge_dialog_btn_go_inventory.png` (SHA256: 6f5a9b432634c405...)：簡體中文
  - `proof_05_en_forge_dialog_btn_go_inventory.png` (SHA256: c40474dbc211880c...)：英文
  - `proof_06_ja_forge_dialog_btn_go_inventory.png` (SHA256: b2606ef8beff6548...)：日文
  - `proof_07_ko_forge_dialog_btn_go_inventory.png` (SHA256: 6ec37bd8ad013842...)：韓文
  - `proof_08_es_forge_dialog_btn_go_inventory.png` (SHA256: e1f4e1ececc6af1e...)：西文
  - 所有存證截圖雜湊互不相同，零同幀重複。
