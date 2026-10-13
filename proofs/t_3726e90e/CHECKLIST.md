# 《發條之心》MapleInventory 探索背包戰魂素材新增『前往聚魂』快捷按鈕連動大廳聚魂殿驗收報告 (t_3726e90e)

- **關聯任務**：`t_3726e90e`（🎮 遊戲開發｜MapleInventory 探索背包戰魂素材新增『前往聚魂』快捷按鈕連動大廳聚魂殿）
- **實作者**：阿翔（`sideworker2`）
- **審查者**：小婷（`sideqa`）
- **分支**：`agent/20261013-inventory-soul-shortcut-t_3726e90e`

---

## 1. 任務背景與驗收目標
在探索背包 `MapleInventory`（`game/scripts/ui/maple_inventory.gd`）右側詳情欄中，實作戰魂養成快捷閉環：
1. **新增『前往聚魂』快捷果凍按鈕（BtnGoSoul）**：
   - 金黃色 `#FFD028`，深藍紫文字與描邊 `#1F1A3A`，底邊 5px，圓角 18px，按鈕高度 52px（>= 48px），字級 18px。
2. **選取戰魂素材時顯示與互斥性**：
   - 選取戰魂素材（`windup_fragment`、`soul_crystal` 等）時顯示 `BtnGoSoul`。
   - 與『前往鍛造』（`BtnGoForge`）、『前往工坊』（`BtnGoWorkshop`）、『前往校準』（`BtnGoCalibrate`）嚴格互斥隱藏，保持面板乾淨與單一視覺重心。
3. **選取一般裝備、素材、消耗品時**：
   - 選取裝備時僅顯示『前往鍛造』；選取一般素材/寶石時僅顯示『前往工坊』；選取機芯時僅顯示『前往校準』；未選取或消耗品時均隱藏。
4. **訊號發射與大廳連動跳轉**：
   - 點擊發射 `go_soul_hall_requested` 訊號並支援 `open_soul_hall()` 直通大廳聚魂殿堂分頁（`Tab.SOUL_HALL`），平滑關閉背包。
5. **六語系支援**：
   - 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時動態切換，歐美語系零 CJK 殘留，零系統 Emoji。
6. **實機驗證與存證**：
   - 通過無頭冒煙測試 0 報錯，通過 `test_maple_inventory_soul_shortcut.gd` 自動化單元測試，實機 OpenGL3 渲染存證至 `proofs/t_3726e90e/`，SHA256 獨立不重複。

---

## 2. 實機存證截圖清單 (proofs/t_3726e90e/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_soul_fragment_selected_btn_go_soul_zh_tw.png` | 選取戰魂素材【發條碎片】時，右側詳情面板顯示金黃果凍厚底按鈕『前往聚魂』（`BtnGoSoul`，高度 52px，厚底 5px，圓角 18px，字級 18px，金黃 #FFD028 / 深藍紫 #1F1A3A） | ✓ | ✓ | ✓ | `daf4568411b4` | **PASS** |
| 02 | `proof_02_maple_inv_soul_shortcut_en.png` | 英文語系 (en) 選取戰魂素材展示：按鈕文字為『Go to Soul Draw』，零中文殘留，多巴胺配色鮮亮 | ✓ | ✓ | ✓ | `26368ee09a71` | **PASS** |
| 03 | `proof_03_maple_inv_soul_shortcut_ja.png` | 日文語系 (ja) 選取戰魂素材展示：按鈕文字為『魂寄せへ』，排版工整無溢出 | ✓ | ✓ | ✓ | `6bef4fd0c2b4` | **PASS** |
| 04 | `proof_04_maple_inv_soul_shortcut_ko.png` | 韓文語系 (ko) 選取戰魂素材展示：按鈕文字為『영혼 뽑기로 이동』，排版工整無溢出 | ✓ | ✓ | ✓ | `fb8164be7e27` | **PASS** |
| 05 | `proof_05_maple_inv_soul_shortcut_es.png` | 西文語系 (es) 選取戰魂素材展示：按鈕文字為『Ir a extracción de almas』，排版工整無溢出 | ✓ | ✓ | ✓ | `53ddab50802e` | **PASS** |
| 06 | `proof_06_click_btn_go_soul_opens_soul_hall.png` | 點擊『前往聚魂』後成功發射 `go_soul_hall_requested` 訊號，自動平滑關閉背包並無縫直達大廳『聚魂殿堂』分頁（Tab.SOUL_HALL） | ✓ | ✓ | ✓ | `b6b36baa82e7` | **PASS** |

---

## 3. 六語系字典對齊驗證

| 鍵值 / 按鈕 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) |
|---|---|---|---|---|---|---|
| **BtnGoSoul** | 前往聚魂 | 前往聚魂 | Go to Soul Draw | 魂寄せへ | 영혼 뽑기로 이동 | Ir a extracción de almas |

---

## 4. 自動化測試執行紀錄

| 測試腳本 / 指令 | 驗證項目 | 結果 | 報錯數 |
|---|---|:---:|:---:|
| `godot --path game --headless --quit-after 3` | 無頭引擎冒煙測試 | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_soul_shortcut ./tools/run_tests.sh` | 專用單元測試（按鈕規格、互斥性、訊號發送、連動大廳聚魂殿、六語系、零 Emoji） | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_shortcuts ./tools/run_tests.sh` | 原有鍛造與工坊快捷按鈕迴歸測試 | **PASS** | 0 SCRIPT ERROR |
| `TEST_FILTER=test_maple_inventory_calibrate_shortcut ./tools/run_tests.sh` | 原有機芯校準快捷按鈕迴歸測試 | **PASS** | 0 SCRIPT ERROR |
| `clock-check /opt/side/bravesoul-game` | 素材、路徑、語系 key、舊名詞自動審查工具 | **PASS** | 0 警告 |
| `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_maple_inventory_soul_shortcut.gd` | 真實 OpenGL3 實機渲染存證截圖與 SHA256 驗證 | **PASS** | 6 獨立截圖 |
