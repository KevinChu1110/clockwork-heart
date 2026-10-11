# MapleInventory 探索背包新增一鍵整理功能與果凍按鈕 驗收查驗清單 (t_604b6c45)

## 任務目標
1. 在探索背包彈窗（`maple_inventory.gd`）左側物品格子區（4×6）底部新增金黃果凍厚底按鈕『一鍵整理』(`BtnSortItems`，尺寸 120x48px，熱區 >= 48px，果凍底 5px)。
2. 點擊後調用背包物品排序邏輯（依裝備/寶石/消耗品/材料分類優先序及品質降序排列），即時刷新格子顯示並播放反饋，支援六語系在地化文字，零系統 Emoji。
3. 背包左側底部顯示居中的『一鍵整理』按鈕，點擊後物品格子依類別整齊重新排列，無卡頓無破圖。
4. 編寫 `test_maple_inventory_sort.gd` 驗證一鍵整理按鈕點擊後背包物品順序重排、介面即時刷新與六語系無缺詞，無 SCRIPT ERROR，產出實機截圖存證。

## 查驗項目與執行結果

### 1. 程式碼與功能實作
- [x] `BtnSortItems` 按鈕節點：於 `maple_inventory.gd` 左側物品欄網格底部以 `HBoxContainer` 水平置中，尺寸設定為 `Vector2(120, 48)`（熱區 >= 48px）。
- [x] 金黃果凍厚底按鈕樣式：採用多巴胺色盤 `COLOR_GOLD` (`#FFD028`)，深藍紫描邊 `COLOR_BORDER` (`#1F1A3A`)，果凍底厚度 5px（`border_width_bottom = 5`），pressed 態 2px 厚底彈性反饋，hover 態柔和金黃。
- [x] 物品分類排序演算法：
  - 分類優先序：1. 裝備（weapon / equipment）→ 2. 寶石（gem）→ 3. 消耗品（consumable）→ 4. 材料（material）→ 5. 其他/重要道具（key）。
  - 同類別依品質降序排列：5. 秘寶/神話 → 4. 極品/史詩 → 3. 上品/稀有 → 2. 良品/優秀 → 1. 凡品/普通（包含 tier / level 數值降序）。
  - 同品質以 ID 字母升序確保穩定性。
- [x] 即時刷新與反饋：點擊按鈕調用 `sort_items()`，即時觸發按鈕縮放脈衝與格子高亮反饋動畫、呼叫 `AudioManager.play_ui()`、重新計算格子資料並即時刷新 `_cells`，保留選取並連動詳情卡。
- [x] 六語系在地化文字支援：`ui.json` 與 `<locale>.json` 補齊 zh_TW（一鍵整理）、zh_CN（一键整理）、en（Auto-Sort）、ja（一括整理）、ko（자동 정리）、es（Organizar），動態切換 `Loc.locale_changed` 即時生效，零系統 Emoji。

### 2. 實機渲染存證截圖 (1280x720)
| 截圖檔名 | 說明 | 規格與狀態 | SHA256 雜湊值 |
|---|---|---|---|
| `proof_01_inventory_before_sort.png` | 探索背包整理前未排序狀態（展示打亂道具、底部居中 BtnSortItems） | 1280x720 PNG | `38169f5dc7949971875f6bd4acbe48d1a99ab02417bf2bb308d3f9da45360c29` |
| `proof_02_inventory_after_sort.png` | 點擊一鍵整理後排序狀態（裝備→寶石→消耗品→材料整齊排列，選取連動詳情） | 1280x720 PNG | `2b6ff2176f331aca0f49a815046649f5adfa4b8bcc33534237823236cba16785` |
| `proof_03_inventory_sort_en.png` | 英文語系介面動態即時切換（Auto-Sort 按鈕與全英文介面無缺詞） | 1280x720 PNG | `4fb5e6ff111b2b8b36ba1fb1dd97053774ade99ff6b03e0d7ceae710f8d481a9` |

### 3. 無頭測試與合規斷言
- [x] `test_maple_inventory_sort.gd`：驗證 BtnSortItems 尺寸/樣式/熱區、六語系即時切換無缺詞、打亂道具排序依裝備/寶石/消耗品/材料及品質降序排列、點擊即時連動刷新，全數 PASS（`MAPLE_INVENTORY_SORT_OK`）。
- [x] `test_maple_inventory.gd`：既有探索背包多巴胺 UI 規格測試全數 PASS（`MAPLE_INVENTORY_OK`）。
- [x] `test_inventory_item_i18n.gd`：既有背包道具名稱與說明六語系測試全數 PASS（`INVENTORY_ITEM_I18N_OK`）。
- [x] `godot --path game --headless --quit-after 3`：冒煙測試 0 報錯、0 SCRIPT ERROR。
- [x] `clock-check t_604b6c45`：結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。
