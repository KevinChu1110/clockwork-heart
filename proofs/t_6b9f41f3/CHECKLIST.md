# 《發條之心》MapleInventory 探索背包一鍵出售未鎖定素材與金幣結算驗收報告 (t_6b9f41f3)

- **關聯任務**：`t_6b9f41f3`（🎮 遊戲開發｜MapleInventory 探索背包支援一鍵出售未鎖定素材與金幣結算浮動提示）
- **實作者**：阿宏（`sideworker`）
- **審查者**：小婷（`sideqa`）
- **分支**：`agent/20261011-maple-inventory-batch-sell-t_6b9f41f3`

---

## 1. 任務背景與驗收目標
在探索背包 `MapleInventory`（`game/scripts/ui/maple_inventory.gd`）右側詳情欄與素材分類中，實作素材一鍵批次出售與金幣結算浮動提示：
1. **『素材』Chip 分類或選取素材時顯示按鈕**：
   - 切換至『素材』分類（不論是否有選取道具）或選取素材類道具時，右側詳情欄呈現多巴胺薄荷綠果凍厚底按鈕『一鍵出售素材』（`BtnBatchSellMaterials`）。
   - 切換至其他分類（`equip`, `consumable`, `gem`）或選取裝備／消耗品時，按鈕嚴格隱藏（`visible == false`）。
2. **安全過濾未鎖定素材與金幣結算**：
   - 點擊後安全過濾所有未鎖定之素材物品，計算總價值並一次性出售轉換為金幣。
   - 保留已鎖定之素材物品（如 `wolf_fang`）完好不被出售。
   - 彈出金幣結算浮動提示（`GoldFloatingToast` / `GoldToastLabel`）與飄字，並同步通知大廳 HUD 與日誌。
3. **多巴胺亮色盤與手遊人體工學規範**：
   - 薄荷綠 `#4ED86A`、深藍紫描邊 `#1F1A3A`（邊框 2px、果凍厚底 5px）、圓角 18px。
   - 按鈕高度 52px（>= 48px），粉圓體字級 18px（>= 16px）。
   - 零系統原生 Emoji。
4. **六語系支援**：
   - 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時在地化切換，歐美語系零 CJK 殘留。
5. **單元測試與實機存證**：
   - 附單元測試 `test_maple_inventory_batch_sell.gd`，涵蓋按鈕樣式、分類顯示、鎖定保留、金幣結算、無可賣防護、六語系切換、零 Emoji 檢查。
   - 真實 OpenGL3 實機渲染存證截圖至 `proofs/t_6b9f41f3/`，SHA256 獨立不重複。

---

## 2. 實機存證截圖清單 (proofs/t_6b9f41f3/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_material_category_batch_sell_btn.png` | 切換至『素材』Chip 分類時，右側詳情欄呈現薄荷綠果凍厚底按鈕『一鍵出售素材』（`BtnBatchSellMaterials`，高 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `abe7254a973c` | **PASS** |
| 02 | `proof_02_maple_inv_material_selected_batch_sell_btn.png` | 選取素材【鐵屑】時，右側詳情面板呈現『一鍵出售素材』與『前往工坊』快捷按鈕，無縫連動 | ✓ | ✓ | ✓ | `d8f9a6322037` | **PASS** |
| 03 | `proof_03_maple_inv_batch_sell_floating_gold_toast.png` | 點擊一鍵出售後，彈出金幣結算浮動提示卡片（`GoldFloatingToast`）與飄字，顯示售出 14 件與獲得 108 金幣 | ✓ | ✓ | ✓ | `0cc201172c50` | **PASS** |
| 04 | `proof_04_maple_inv_batch_sell_completed_locked_retained.png` | 出售完成後背包狀態：未鎖定素材全數清除，已鎖定之素材【棘輪尖齒】完好保留未被誤售，詳情正確展示 | ✓ | ✓ | ✓ | `ec048839f8f4` | **PASS** |
| 05 | `proof_05_maple_inv_batch_sell_en_locale.png` | 英文語系 (en) 素材分類展示：按鈕文案為『Quick-Sell Materials』，全介面零中文殘留，排版整齊 | ✓ | ✓ | ✓ | `2be0afac3684` | **PASS** |
| 06 | `proof_06_maple_inv_batch_sell_ja_locale.png` | 日文語系 (ja) 素材分類展示：按鈕文案為『素材を一括売却』，日文字形渲染清晰無穿模 | ✓ | ✓ | ✓ | `a4b824c93d0c` | **PASS** |

---

## 3. 六語系字典對齊驗證

| 鍵值 / 按鈕 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) |
|---|---|---|---|---|---|---|
| **一鍵出售素材** | 一鍵出售素材 | 一键出售素材 | Quick-Sell Materials | 素材を一括売却 | 재료 일괄 판매 | Vender materiales |
| **賣出材料 %d 件 · 金 +%d** | 賣出材料 %d 件 · 金 +%d | 出售材料 %d 件 · 金 +%d | Sold %d materials · gold +%d | 素材を %d 個売却 · 金 +%d | 재료 %d개 판매 · 골드 +%d | Vendiste %d materiales · oro +%d |
| **沒有可賣的材料。** | 沒有可賣的材料。 | 没有可出售的材料。 | No sellable materials. | 売却できる素材がありません。 | 판매할 수 있는 재료가 없습니다. | No hay materiales para vender. |

---

## 4. 自動化測試執行紀錄

| 測試腳本 / 指令 | 驗證項目 | 結果 | 報錯數 |
|---|---|:---:|:---:|
| `godot --path game --headless --quit-after 3` | 無頭引擎冒煙測試 | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_batch_sell ./tools/run_tests.sh` | 專用單元測試（樣式規格、分類切換、鎖定過濾、金幣累加、安全防護、六語系、零 Emoji） | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 探索背包 11 支單元測試迴歸（batch_sell, capacity, chips, diff, dismantle, equip, equipped, lock, sort, shortcuts 等） | **PASS** (11/11) | 0 SCRIPT ERROR |
| `/root/bin/clock-check /opt/side/bravesoul-game` | 素材、路徑、語系 key、舊名詞自動審查工具 | **PASS** | 0 警告 |
| `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_maple_inventory_batch_sell.gd` | 真實 OpenGL3 實機渲染存證截圖與 SHA256 驗證 | **PASS** | 6 獨立截圖 |
