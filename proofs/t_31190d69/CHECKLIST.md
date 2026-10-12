# 《發條之心》MapleInventory 探索背包前往鍛造與前往工坊快捷跳轉驗收報告 (t_31190d69)

- **關聯任務**：`t_31190d69`（🎮 遊戲開發｜MapleInventory 探索背包選取裝備與素材支援前往鍛造與前往工坊快捷跳轉）
- **實作者**：阿宏（`sideworker`）
- **審查者**：小婷（`sideqa`）
- **分支**：`agent/20261011-inventory-shortcuts-t_31190d69`

---

## 1. 任務背景與驗收目標
在探索背包 `MapleInventory`（`game/scripts/ui/maple_inventory.gd`）右側詳情欄中，實作養成閉環快捷跳轉：
1. **選取裝備（weapon / armor / equip）時**：
   - 詳情欄提供多巴胺暖橘立體厚底按鈕『前往鍛造』（`BtnGoForge`）。
   - 點擊發送 `forge_requested` 訊號並支援直通開啟天宮鐵匠彈窗 `ForgeDialog`，平滑關閉背包。
2. **選取寶石或素材（gem / material）時**：
   - 詳情欄提供多巴胺薄荷綠立體厚底按鈕『前往工坊』（`BtnGoWorkshop`）。
   - 點擊發送 `workshop_requested` 訊號並支援直通開啟手藝工坊彈窗 `GemWorkshopDialog`，平滑關閉背包。
3. **未選取或選取消耗品／重要道具時**：
   - 兩快捷按鈕嚴格隱藏（`visible == false`），維持原有版面與快捷欄按鈕。
4. **多巴胺亮色盤與手遊人體工學規範**：
   - 按鈕高度 52px（>= 50px），熱區 >= 48px，立體果凍厚底 5px，圓角 18px，粉圓體字級 18px（>= 18px）。
   - 零系統原生 Emoji。
5. **六語系支援**：
   - 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時切換，歐美語系零 CJK 殘留。
6. **實機驗證與存證**：
   - 通過 `test_maple_inventory_shortcuts.gd` 單元測試（10 項全綠），實機 OpenGL3 渲染存證至 `proofs/t_31190d69/`，SHA256 獨立不重複。

---

## 2. 實機存證截圖清單 (proofs/t_31190d69/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_weapon_selected_forge_btn.png` | 選取裝備【鏽劍】時，右側詳情面板顯示暖橘果凍厚底按鈕『前往鍛造』（`BtnGoForge`，高度 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `f3cc47b80644` | **PASS** |
| 02 | `proof_02_maple_inv_material_selected_workshop_btn.png` | 選取素材【鐵屑】時，右側詳情面板顯示薄荷綠果凍厚底按鈕『前往工坊』（`BtnGoWorkshop`，高度 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `a78d42d3f768` | **PASS** |
| 03 | `proof_03_maple_inv_consumable_hidden_shortcuts.png` | 選取消耗品【微光潤滑油】時，『前往鍛造』與『前往工坊』按鈕嚴格隱藏，維持原快捷欄按鈕『放到快捷欄』 | ✓ | ✓ | ✓ | `0228344aa8b9` | **PASS** |
| 04 | `proof_04_maple_inv_forge_dialog_opened.png` | 點擊『前往鍛造』後成功發射 `forge_requested` 訊號，自動平滑關閉背包並無縫彈出天宮鐵匠 `ForgeDialog` | ✓ | ✓ | ✓ | `867ca6fb7529` | **PASS** |
| 05 | `proof_05_maple_inv_gem_workshop_opened.png` | 點擊『前往工坊』後成功發射 `workshop_requested` 訊號，自動平滑關閉背包並無縫彈出手藝工坊 `GemWorkshopDialog` | ✓ | ✓ | ✓ | `0944298514f8` | **PASS** |
| 06 | `proof_06_maple_inv_shortcuts_i18n_locales.png` | 英文語系 (en) 選取裝備展示：按鈕文字為『Go to Forge』，所有按鈕與 UI 標籤無中文殘留，排版工整 | ✓ | ✓ | ✓ | `91543d9cf1de` | **PASS** |

---

## 3. 六語系字典對齊驗證

| 鍵值 / 按鈕 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) |
|---|---|---|---|---|---|---|
| **BtnGoForge** | 前往鍛造 | 前往锻造 | Go to Forge | 鍛造へ進む | 단조로 이동 | Ir a Forja |
| **BtnGoWorkshop** | 前往工坊 | 前往工坊 | Go to Workshop | 工房へ進む | 공방으로 이동 | Ir al Taller |

---

## 4. 自動化測試執行紀錄

| 測試腳本 / 指令 | 驗證項目 | 結果 | 報錯數 |
|---|---|:---:|:---:|
| `godot --path game --headless --quit-after 3` | 無頭引擎冒煙測試 | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_shortcuts ./tools/run_tests.sh` | 專用單元測試（按鈕樣式、狀態切換、訊號發送、連動開啟、六語系、零 Emoji） | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 探索背包 9 支單元測試（chips, diff, dismantle, equip, equipped, lock, sort, shortcuts 等） | **PASS** (9/9) | 0 SCRIPT ERROR |
| `clock-check /opt/side/bravesoul-game` | 素材、路徑、語系 key、舊名詞自動審查工具 | **PASS** | 0 警告 |
| `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_maple_inventory_shortcuts.gd` | 真實 OpenGL3 實機渲染存證截圖與 SHA256 驗證 | **PASS** | 6 獨立截圖 |
