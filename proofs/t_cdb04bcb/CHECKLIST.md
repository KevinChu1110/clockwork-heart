# 驗收查核表：MapleInventory 探索背包選取裝備支援戰力差額比對膠囊與屬性預覽 (t_cdb04bcb)

- **關聯任務**：`t_cdb04bcb`（🎮 遊戲開發｜MapleInventory 探索背包選取裝備支援戰力差額比對膠囊與屬性預覽）
- **關聯專案項目**：`inventory-stat-comparison`（MapleInventory 探索背包選取裝備支援戰力差額比對膠囊與屬性預覽）
- **工程師**：阿翔（sideworker2）
- **分支**：`agent/20261011-inventory-power-diff-t_cdb04bcb`

---

## 1. 驗收項目清單

| 編號 | 項目 | 驗收標準 | 狀態 | 驗證方式 |
|---|---|---|---|---|
| 01 | 武器屬性預覽與差額比對膠囊 | 選取武器呈現「攻擊 +N」與攻擊力差額膠囊。升攻綠色膠囊 #1E7538（文案『+N 攻擊』）、降攻灰色膠囊 #7A7090（文案『-N 攻擊』）、持平灰色膠囊 #7A7090（文案『--』） | PASS | 單元測試斷言 + 實機畫面檢視 |
| 02 | 防具屬性預覽與差額比對膠囊 | 選取防具呈現「防禦 +N」與防禦力差額膠囊。升防綠色膠囊 #1E7538（文案『+N 防禦』）、降防灰色膠囊 #7A7090（文案『-N 防禦』）、持平灰色膠囊 #7A7090（文案『--』） | PASS | 單元測試斷言 + 實機畫面檢視 |
| 03 | 非裝備類與未選取隱藏 | 消耗品、素材、重要道具與未選取狀態時，屬性預覽列與差額膠囊列完全隱藏 (`visible = false`) | PASS | 單元測試狀態斷言 |
| 04 | 膠囊規格與視覺人體工學 | 差額膠囊圓角 13px (pill shape)，白字加粗高對比，自適應字級防溢出，無重疊無截字 | PASS | 單元測試 StyleBox 斷言 + Vision 視覺複檢 |
| 05 | 六語系即時切換 | 支援 zh_TW, zh_CN, en, ja, ko, es 動態無缺詞（攻擊/攻击/Attack/攻撃/공격/Ataque、防禦/防御/DEF/防御/방어/DEF） | PASS | 單元測試迴圈切換驗證 + 實機截圖存證 |
| 06 | 零系統 Emoji | 全畫面無作業系統原生 Emoji 字符，無破圖、無溢出 | PASS | Unicode 碼位過濾斷言與 Vision 視覺審查 |
| 07 | 回歸測試與工具檢查 | 既有 4 支背包測試全綠，新增 `test_maple_inventory_diff.gd` 通過，`clock-check` 0 缺失 | PASS | 5 支測試全綠，clock-check 通過 |

---

## 2. 實機截圖存證清單 (proofs/t_cdb04bcb/)

所有截圖均拆分等待步驟獨立渲染，SHA256 彼此完全相異，尺寸為 1280×720，零黑屏零遮擋：

| 編號 | 檔名 | 說明 | 尺寸 | SHA256 | 驗收結果 |
|---|---|---|---|---|---|
| 01 | `proof_01_weapon_diff_up.png` | 武器升攻比對：選取「微末之刃」(atk 9)，相較當前裝備「鏽劍」(atk 4) 呈現「攻擊 +9」與「+5 攻擊」升攻綠色膠囊 (#1E7538) | 1280×720 | `8a63efba0f61b3dc706a7fc39e8b8428140ebd2443c6ea2540e2591f1cbc2936` | 合格 (PASS) |
| 02 | `proof_02_weapon_diff_down.png` | 武器降攻比對：選取「鏽劍」(atk 4)，相較當前裝備「微末之刃」(atk 9) 呈現「攻擊 +4」與「-5 攻擊」降攻灰色膠囊 (#7A7090) | 1280×720 | `d38e94bfa7fced71d949b7dfdc3474c72ae4fe8784e523ab77a426569cbef2fb` | 合格 (PASS) |
| 03 | `proof_03_armor_diff_up.png` | 防具升防比對：選取「騎士殘甲」(def 7)，相較當前裝備「灰燼甲片」(def 3) 呈現「防禦 +7」與「+4 防禦」升防綠色膠囊 (#1E7538) | 1280×720 | `19e047359af152ddaf9fdcd5f0e76a35ae1019c6ae95922859603aebe6590468` | 合格 (PASS) |
| 04 | `proof_04_armor_diff_down.png` | 防具降防比對：選取「灰燼甲片」(def 3)，相較當前裝備「騎士殘甲」(def 7) 呈現「防禦 +3」與「-4 防禦」降防灰色膠囊 (#7A7090) | 1280×720 | `a286b889e69e2aa019e67f7924f3ff64677172a4da193f67fb811ce2be284305` | 合格 (PASS) |
| 05 | `proof_05_six_locales_en.png` | 英文語系 (en) 驗收：選取武器呈現「Attack +9」與「+5 Attack」綠色膠囊，標題、頁籤與分類全在地化且自適應縮放無穿框 | 1280×720 | `59bbd7289d03454d176a6599b65085375edbb980fef3fcf180bc2d46162f2322` | 合格 (PASS) |
| 06 | `proof_06_diff_equal_capsule.png` | 裝備同攻武器選取呈現持平「--」灰色膠囊 (#7A7090)，消耗品/素材/重要道具正確隱藏膠囊列 | 1280×720 | `ee0be7c6963a0d172253aa5851d0eba7eeb5fc8051eca70c631b083221ea861c` | 合格 (PASS) |

---

## 3. 單元測試與回歸驗證

- `test_maple_inventory_diff.gd`：PASS（`MAPLE_INVENTORY_DIFF_OK`）
- `test_maple_inventory_equip.gd`：PASS（`MAPLE_INVENTORY_EQUIP_OK`）
- `test_maple_inventory.gd`：PASS（`MAPLE_INVENTORY_OK`）
- `test_maple_inventory_sort.gd`：PASS（`MAPLE_INVENTORY_SORT_OK`）
- `test_maple_inventory_chips.gd`：PASS（`MAPLE_INVENTORY_CHIPS_OK`）
- `clock-check /opt/side/bravesoul-game`：✅ 全過（素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）
