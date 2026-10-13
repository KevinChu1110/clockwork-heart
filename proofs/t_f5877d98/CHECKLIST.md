# 驗收查核表：探索背包選取當前穿戴裝備切換「已穿戴」置灰按鈕與專屬膠囊提示 (t_f5877d98)

- **關聯任務**：`t_f5877d98`（🎮 遊戲開發｜探索背包選取當前穿戴裝備切換「已穿戴」置灰按鈕與專屬膠囊提示）
- **關聯專案項目**：`inventory-equipped-state`（探索背包當前裝備狀態辨識與已穿戴按鈕置灰）
- **工程師**：阿翔（sideworker2）
- **分支**：`agent/20261011-inventory-equipped-state-t_f5877d98`

---

## 1. 驗收項目清單

| 編號 | 項目 | 驗收標準 | 狀態 | 驗證方式 |
|---|---|---|---|---|
| 01 | 已裝備武器狀態切換 | 選取當前裝備武器時，按鈕切換為『已穿戴』且 disabled=true 置灰防重複點擊；差額膠囊切換為『穿戴中』（專屬藍底 #3870B2，白字 #FFFFFF 高對比）；屬性預覽正常呈現（攻擊 +N） | PASS | 單元測試斷言 + 實機畫面檢視 |
| 02 | 已裝備防具狀態切換 | 選取當前裝備防具時，按鈕切換為『已穿戴』且 disabled=true 置灰防重複點擊；差額膠囊切換為『穿戴中』（專屬藍底 #3870B2，白字 #FFFFFF）；屬性預覽正常呈現（防禦 +N） | PASS | 單元測試斷言 + 實機畫面檢視 |
| 03 | 未裝備裝備正常操作與差額 | 選取未裝備武器/防具時，按鈕正常顯示『立即裝備』且 disabled=false 可點擊；差額膠囊正常呈現升/降/持平比對數值（+N 攻擊/防禦、-N 攻擊/防禦、--） | PASS | 單元測試斷言 + 實機畫面檢視 |
| 04 | 穿戴中專屬膠囊規格 | 膠囊圓角 13px (pill shape)，白字加粗高對比，自適應字級防溢出，無重疊無截字 | PASS | 單元測試 StyleBox 斷言 + Vision 視覺複檢 |
| 05 | 六語系即時切換無缺詞 | 支援 zh_TW, zh_CN, en, ja, ko, es 動態無缺詞（已穿戴/已穿戴/Equipped/装備済み/장착됨/Equipado、穿戴中/穿戴中/Equipped/装備中/장착 중/Equipado） | PASS | 單元測試迴圈切換驗證 + 實機截圖存證 |
| 06 | 零系統 Emoji | 全畫面無作業系統原生 Emoji 字符，無破圖、無溢出 | PASS | Unicode 碼位過濾斷言與 Vision 視覺審查 |
| 07 | 回歸測試與工具檢查 | 既有 5 支背包測試全綠，新增 `test_maple_inventory_equipped.gd` 通過，`clock-check` 0 缺失 | PASS | 6 支測試全綠，clock-check 通過 |

---

## 2. 實機截圖存證清單 (proofs/t_f5877d98/)

所有截圖均拆分等待步驟獨立渲染，SHA256 彼此完全相異，尺寸為 1280×720，零黑屏零遮擋：

| 編號 | 檔名 | 說明 | 尺寸 | SHA256 | 驗收結果 |
|---|---|---|---|---|---|
| 01 | `proof_01_equipped_weapon_btn_capsule.png` | 選取已穿戴武器「鏽劍」：按鈕切換為置灰『已穿戴』(disabled=true)，差額膠囊切換為專屬藍底『穿戴中』(#3870B2)，屬性預覽顯示「攻擊 +4」 | 1280×720 | `270cbcf75e27911c707dc8943a18d018aa3d4fe5a6617fb3a6c1bd70ce8b407c` | 合格 (PASS) |
| 02 | `proof_02_equipped_armor_btn_capsule.png` | 選取已穿戴防具「騎士胸甲」：按鈕切換為置灰『已穿戴』(disabled=true)，差額膠囊切換為專屬藍底『穿戴中』(#3870B2)，屬性預覽顯示「防禦 +7 · 生命 +20」 | 1280×720 | `18ff761cc845263af930e2e7222a736cc398a2c11ea27552656d0486aa4bc539` | 合格 (PASS) |
| 03 | `proof_03_unequipped_weapon_diff.png` | 選取未穿戴武器「微末之刃」：按鈕呈現亮橘色『立即裝備』(disabled=false)，差額膠囊呈現綠色『+5 攻擊』(#1E7538)，屬性預覽顯示「攻擊 +9」 | 1280×720 | `57d56e01d2daf42f0cff3ecc81e80f6fb360ecd7dea68db4a5e9d338dd3de7f8` | 合格 (PASS) |
| 04 | `proof_04_unequipped_armor_diff.png` | 選取未穿戴防具「灰燼甲片」：按鈕呈現亮橘色『立即裝備』(disabled=false)，差額膠囊呈現灰色『-4 防禦』(#7A7090)，屬性預覽顯示「防禦 +3」 | 1280×720 | `1a6bef0533d0c3dd4afca8dc947366c3d52a02d897751ac570c59c58c4ce2b7c` | 合格 (PASS) |
| 05 | `proof_05_six_locales_en.png` | 英文語系 (en) 驗收：選取已穿戴武器呈現置灰按鈕『Equipped』與膠囊『Equipped』，零 emoji，排版工整無溢出 | 1280×720 | `a14583ac97cbc8c68c891e4c44077852ff3fb8e7e5e682d0a14fc2846a23c3c5` | 合格 (PASS) |
| 06 | `proof_06_six_locales_ja.png` | 日文語系 (ja) 驗收：選取已穿戴武器呈現置灰按鈕『装備済み』與膠囊『装備中』，零 emoji，排版工整無溢出 | 1280×720 | `2ab42b6a780b82bf8deb97ec6b93e9bacf4b99e166abd813412fd0ef1f4ee464` | 合格 (PASS) |

---

## 3. 單元測試與回歸驗證

- `test_maple_inventory_equipped.gd`：PASS（`MAPLE_INVENTORY_EQUIPPED_OK`）
- `test_maple_inventory_diff.gd`：PASS（`MAPLE_INVENTORY_DIFF_OK`）
- `test_maple_inventory_equip.gd`：PASS（`MAPLE_INVENTORY_EQUIP_OK`）
- `test_maple_inventory.gd`：PASS（`MAPLE_INVENTORY_OK`）
- `test_maple_inventory_sort.gd`：PASS（`MAPLE_INVENTORY_SORT_OK`）
- `test_maple_inventory_chips.gd`：PASS（`MAPLE_INVENTORY_CHIPS_OK`）
- `smoke headless quit-after 3`：PASS（0 SCRIPT ERROR）
- `clock-check /opt/side/bravesoul-game`：✅ 全過（素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）
