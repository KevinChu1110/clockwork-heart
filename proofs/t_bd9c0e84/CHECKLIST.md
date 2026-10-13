# 驗收查核表：MapleInventory 探索背包支援選取裝備立即裝備與動態按鈕文案 (t_bd9c0e84)

- **關聯任務**：`t_bd9c0e84`（🎮 遊戲開發｜MapleInventory 探索背包支援選取裝備立即裝備與動態按鈕文案）
- **關聯專案項目**：`inventory-equip-direct`（MapleInventory 探索背包支援選取裝備立即裝備與動態按鈕文案）
- **工程師**：阿宏（sideworker）
- **分支**：`agent/20261011-inventory-equip-direct-t_bd9c0e84`

---

## 1. 驗收項目清單

| 編號 | 項目 | 驗收標準 | 狀態 | 驗證方式 |
|---|---|---|---|---|
| 01 | 右側操作按鈕適應性文案 | 消耗品顯示『使用』、素材顯示『賣出』、裝備類顯示『立即裝備』、重要物品顯示『重要物品』且禁用、未選取顯示『使用 / 賣出』且禁用 | PASS | 單元測試斷言 + 實機畫面檢視 |
| 02 | 立即裝備與換裝連動 | 選取裝備點擊『立即裝備』呼叫 `EquipmentSystem.equip`，並雙向發射 `MapleInventory.equipment_changed` 與 `EquipmentSystem.equipment_changed` 信號 | PASS | 單元測試信號監聽與入槽斷言 |
| 03 | 多巴胺視覺與尺寸規範 | 按鈕高度 52px（>= 48px 手機熱區標準）、圓角 18px、果凍厚底 5px，裝備採暖橘 #FFA010、消耗品/素材採薄荷綠 #4ED86A、重要物品採灰底 #E8E4EC | PASS | 單元測試 StyleBoxFlat 與 Vision 視覺複檢 |
| 04 | 六語系即時切換 | 支援 zh_TW, zh_CN, en, ja, ko, es 動態無缺詞（使用/Use/使う/사용/Usar、賣出/出售/Sell/売却/판매/Vender、立即裝備/立即装备/Equip Now/今すぐ装備/즉시 장착/Equipar ahora、重要物品/Key Item/重要アイテム/중요 아이템/Objeto clave） | PASS | 單元測試迴圈遍歷切換驗證 |
| 05 | 零系統 Emoji | 全畫面無作業系統原生 Emoji 字符，無破圖、無截字溢出 | PASS | Unicode 碼位過濾斷言與 Vision 視覺審查 |
| 06 | 回歸測試與工具檢查 | `run_tests.sh` 既有 maple 測試全綠，`clock-check` 0 缺失 | PASS | 4 支測試全綠，clock-check 通過 |

---

## 2. 實機截圖存證清單 (proofs/t_bd9c0e84/)

所有截圖均拆分等待步驟獨立渲染，SHA256 彼此完全相異，尺寸為 1280×720，零黑屏零遮擋：

| 編號 | 檔名 | 說明 | 尺寸 | SHA256 | 驗收結果 |
|---|---|---|---|---|---|
| 01 | `proof_01_consumable_use.png` | 選取「高純潤滑油」(hp_m) 消耗品：右側按鈕動態呈現『使用』、薄荷綠果凍厚底按鈕 | 1280×720 | `efe806a368e43307ebe41391552f03d78648a95e8291df59bf18fd870cb9533e` | 合格 (PASS) |
| 02 | `proof_02_material_sell.png` | 選取「鍛造鐵屑」(iron_scrap) 素材：右側按鈕動態呈現『賣出』、薄荷綠果凍厚底按鈕 | 1280×720 | `34ab37faf9e5adeb381b90012692b41e6f147920729f3a429e1b1480e47a469d` | 合格 (PASS) |
| 03 | `proof_03_equip_now.png` | 選取「鏽劍」(rusty_blade) 裝備類：右側按鈕動態呈現『立即裝備』、暖橘果凍厚底按鈕 | 1280×720 | `ef06bc945ce09f7d9342f390d63150f514e71f5d93b9d70fb5a6c4263dd45736` | 合格 (PASS) |
| 04 | `proof_04_key_item_disabled.png` | 選取「鏽劍（紀念）」(key_rusty) 重要物品：右側按鈕呈現『重要物品』、禁用灰底樣式 | 1280×720 | `e2c273e124bbcd9194b31034b3d45bea8dab86498221bf0bd9332df2b5230641` | 合格 (PASS) |
| 05 | `proof_05_six_locales_equip_en.png` | 英文語系 (en) 選取裝備類呈現『Equip Now』、標題與分類頁籤完整在地化 | 1280×720 | `987e272c8899eae32ffa23222675867855f5e9c3bdea7efb70ec713b93e5cb6b` | 合格 (PASS) |
| 06 | `proof_06_unselected_empty.png` | 未選取道具時之預設狀態：按鈕禁用、顯示『使用 / 賣出』 | 1280×720 | `bb001b7e2263da44e2a57ced18ab60b5c055aedbb27ae72a6575337c227113ce` | 合格 (PASS) |

---

## 3. 單元測試與回歸驗證

- `test_maple_inventory_equip.gd`：PASS（`MAPLE_INVENTORY_EQUIP_OK`）
- `test_maple_inventory.gd`：PASS（`MAPLE_INVENTORY_OK`）
- `test_maple_inventory_sort.gd`：PASS（`MAPLE_INVENTORY_SORT_OK`）
- `test_maple_inventory_chips.gd`：PASS（`MAPLE_INVENTORY_CHIPS_OK`）
- `test_inventory_item_i18n.gd`：PASS（`INVENTORY_ITEM_I18N_OK`）
- `clock-check /opt/side/bravesoul-game`：✅ 全過（素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）
