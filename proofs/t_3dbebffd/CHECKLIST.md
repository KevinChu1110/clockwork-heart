# 《發條之心》MapleInventory 探索背包即時容量進度膠囊顯示與格子滿載提示驗收報告 (t_3dbebffd)

- **關聯任務**：`t_3dbebffd`（🎮 遊戲開發｜MapleInventory 探索背包支援即時容量進度膠囊顯示與格子滿載提示）
- **實作者**：阿宏（`sideworker`）
- **審查者**：小婷（`sideqa`）
- **分支**：`agent/20261011-inventory-capacity-t_3dbebffd`

---

## 1. 任務背景與驗收目標
在探索背包 `MapleInventory`（`game/scripts/ui/maple_inventory.gd`）左側物品格子區底部一鍵整理按鈕旁：
1. **新增『容量進度膠囊』顯示元件（`_capacity_capsule` 與 `_capacity_label`）**：
   - 即時顯示當前背包已佔用格子數與總容量（例如『容量 12/24』），讓玩家能即時掌握空間。
   - 隨物品增減、整理或分類切換即時更新數據。
2. **滿載狀態自動色階切換與提示（>= 24）**：
   - 當物品佔用格數達到上限（>= 24）時，膠囊樣式自動切換為珊瑚粉/暖橘警示色階（珊瑚粉底 `#FF5E8A`、深藍紫描邊 `#1F1A3A`、暖橘光暈），字色轉為白色深描邊。
   - 滿載狀態下選取物品時，於操作提示標籤（`_tip`）與詳情卡片（`_detail`）同步提示『背包空間已滿』。
   - 扣減道具回到未滿載狀態（如 23/24）時，自動切回奶油白底解除警示。
3. **多巴胺亮色盤與手遊人體工學規範**：
   - 膠囊背景奶油白 `#FFFDF8`（`COLOR_BG_CREAM`）、深藍紫描邊 `#1F1A3A` (2px)、圓角 16px。
   - 粉圓體字級 16px（>= 16px）、膠囊尺寸 120x48px（高度 >= 48px），與右側「一鍵整理」按鈕協調居中排版。
   - 全程零系統原生 Emoji。
4. **六語系支援**：
   - 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換（`ui.json` 詞條同步），歐美語系零 CJK 殘留。
5. **單元測試與實機存證**：
   - 建立專用單元測試 `game/scripts/ui/test_maple_inventory_capacity.gd`。
   - 透過真實 OpenGL3 實機渲染存證 6 張截圖至 `proofs/t_3dbebffd/`，SHA256 全數獨立不重複。

---

## 2. 實機存證截圖清單 (proofs/t_3dbebffd/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_capacity_normal_zh_TW.png` | 正常容量狀態 (12/24)：左下角膠囊奶油白底、深藍紫描邊，清楚顯示『容量 12/24』，與右側一鍵整理按鈕協調排版 | ✓ | ✓ | ✓ | `9fcaf5e17555` | **PASS** |
| 02 | `proof_02_maple_inv_capacity_chip_filter.png` | 分類頁籤切換：切換至【裝備】Chip，膠囊即時動態更新為裝備格數『容量 4/24』 | ✓ | ✓ | ✓ | `547f7210e7ff` | **PASS** |
| 03 | `proof_03_maple_inv_capacity_full_warning_coral.png` | 滿載狀態 (24/24)：格數達上限，膠囊自動切換為珊瑚粉底 (#FF5E8A) 暖橘光暈警示色階，白字高對比顯示『容量 24/24』 | ✓ | ✓ | ✓ | `eb7ee62203de` | **PASS** |
| 04 | `proof_04_maple_inv_capacity_full_item_selected_tip.png` | 滿載選取物品提示：選中武器時，操作提示標籤與詳情卡片均高亮提示『背包空間已滿』 | ✓ | ✓ | ✓ | `f91730a11e16` | **PASS** |
| 05 | `proof_05_maple_inv_capacity_en_locale.png` | 英文語系 (en) 滿載展示：膠囊顯示『Capacity 24/24』，提示『Backpack is full』，100% 零 CJK 殘留 | ✓ | ✓ | ✓ | `fa5876961da5` | **PASS** |
| 06 | `proof_06_maple_inv_capacity_ja_locale.png` | 日語語系 (ja) 滿載展示：膠囊顯示『容量 24/24』，提示『バッグの空きがありません』，漢字常用規範對齊 | ✓ | ✓ | ✓ | `23009795aa2f` | **PASS** |

---

## 3. 六語系字典對齊驗證

| 鍵值 / 詞條 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) |
|---|---|---|---|---|---|---|
| **容量 %d/%d** | 容量 %d/%d | 容量 %d/%d | Capacity %d/%d | 容量 %d/%d | 용량 %d/%d | Capacidad %d/%d |
| **容量** | 容量 | 容量 | Capacity | 容量 | 용량 | Capacidad |
| **背包空間已滿** | 背包空間已滿 | 背包空间已满 | Backpack is full | バッグの空きがありません | 가방 공간이 가득 찼습니다 | Espacio de mochila lleno |

---

## 4. 自動化測試執行紀錄

| 測試腳本 / 指令 | 驗證項目 | 結果 | 報錯數 |
|---|---|:---:|:---:|
| `godot --path game --headless --quit-after 3` | 無頭引擎冒煙測試 | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_capacity ./tools/run_tests.sh` | 專用單元測試（規格尺寸、容量計算、分類連動、滿載色階切換、扣減恢復、六語系、零 Emoji） | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 探索背包全套 10 支單元測試（capacity, chips, diff, dismantle, equip, equipped, lock, shortcuts, sort 等） | **PASS** (10/10) | 0 SCRIPT ERROR |
| `clock-check /opt/side/bravesoul-game` | 素材、路徑、語系 key、舊名詞自動審查工具 | **PASS** | 0 警告 |
| `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_maple_inventory_capacity.gd` | 真實 OpenGL3 實機渲染存證截圖與 SHA256 驗證 | **PASS** | 6 獨立截圖 |
