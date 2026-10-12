# 全面回歸驗收證明 · 探索背包四大強化與戰力總覽戰魂快捷合進主線後的全機制回歸驗收 (t_a85555ab)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）與阿翔（`sideworker2`）開發、測試小婷（`sideqa`）完成獨立驗收審查、並由主管老周完成主線合併（卡號 `t_4736857f`，merge commit `9752e956`）之五大功能分支：
1. `inventory-equip-direct`（t_bd9c0e84）：探索背包選取裝備支援立即裝備與動態按鈕文案
2. `inventory-stat-comparison`（t_cdb04bcb）：探索背包選取裝備支援戰力差額比對膠囊與屬性預覽
3. `inventory-equipped-state`（t_f5877d98）：探索背包當前裝備狀態辨識與已穿戴按鈕置灰
4. `inventory-lock-toggle`（t_73dedb6c）：探索背包支援裝備鎖定與解鎖防誤賣
5. `power-stat-soul-shortcut`（t_102be271）：PowerStatDialog 戰力屬性總覽新增戰魂共鳴卡片與前往聚魂快捷按鈕

在合併至 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全機制回歸測試、自動化靜態與動態檢查、多語系驗證、真實 OpenGL3 實機截圖存證，並將 `docs/PROJECTS.json` 項目狀態正式更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **立即裝備單元測試** | `TEST_FILTER=test_maple_inventory_equip ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_EQUIP_OK`） | **PASS** |
| **戰力差額比對測試** | `TEST_FILTER=test_maple_inventory_diff ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_DIFF_OK`） | **PASS** |
| **已穿戴狀態置灰測試** | `TEST_FILTER=test_maple_inventory_equipped ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_EQUIPPED_OK`） | **PASS** |
| **裝備鎖定切換測試** | `TEST_FILTER=test_maple_inventory_lock ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_LOCK_OK`） | **PASS** |
| **探索背包核心與分類測試** | `TEST_FILTER=maple_inventory ./tools/run_tests.sh` | 7/7 通過（chips, diff, equip, equipped, core, lock, sort 全部通過） | **PASS** |
| **戰魂共鳴與快捷按鈕測試** | `TEST_FILTER=test_power_stat_soul_shortcut ./tools/run_tests.sh` | 1/1 通過（`TEST_POWER_STAT_SOUL_SHORTCUT_OK`） | **PASS** |
| **戰力屬性總覽全套測試** | `TEST_FILTER=power_stat ./tools/run_tests.sh` | 4/4 通過（equip_shortcut, dialog, shortcuts, soul_shortcut 全部通過） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，拒絕虛假圖片。
- [x] **獨立 Proof 目錄**：所有實機全景圖與特寫圖存證於 `proofs/t_a85555ab/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 探索背包操作按鈕：高度 52px（>= 48px），立體果凍厚底 5px，圓角 18px。
  - 差額比對膠囊：圓角 13px pill shape，綠色升攻/升防 (#1E7538)，灰色降/平 (#7A7090)，專屬藍底穿戴中 (#3870B2)，白字高對比度。
  - 裝備鎖定防誤賣：未鎖定灰色膠囊，已鎖定金黃膠囊 (#D49B20)，詳情面板紅橘色高能提示「裝備已鎖定無法出售」。
  - 戰魂共鳴卡片：雙欄 CoreGrid (columns = 2)，四大核心（齒、甲、簧、衡）卡片格高度 >= 48px。
  - 前往聚魂按鈕：88x36px，熱區 >= 48px，珊瑚粉 (#FF5E8A) 果凍厚底 4px。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼斷言，UI 元素全面清除系統 emoji，採用純淨手繪/向量圖示與粉圓體文字。
- [x] **六語系即時在地化切換**：繁中 (zh_TW)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es)、簡中 (zh_CN) 動態切換無需重啟，無缺詞漏詞。
- [x] **大廳流暢連動**：點擊「前往聚魂」快捷按鈕後，彈窗自動關閉，大廳流暢無縫切換至聚魂殿堂（Tab.SOUL_HALL）。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將五大項目皆更新為『已上線』並推向遠端。

---

## 4. 存證截圖清單 (proofs/t_a85555ab/)

1. `proof_01_maple_inventory_equip_direct_zh_tw.png` — 探索背包選取未穿戴裝備，顯示暖橘『立即裝備』果凍按鈕與屬性預覽
2. `proof_02_maple_inventory_diff_capsule_up.png` — 探索背包選取高攻擊裝備，顯示綠色差額比對膠囊『+5 攻擊』(#1E7538)
3. `proof_03_maple_inventory_equipped_state_grey.png` — 探索背包選取當前穿戴裝備，操作按鈕動態置灰『已穿戴』(disabled=true) 與藍底『穿戴中』膠囊 (#3870B2)
4. `proof_04_maple_inventory_lock_unlocked_state.png` — 探索背包選取未鎖定裝備，顯示灰底『未鎖定』膠囊與『鎖定』按鈕
5. `proof_05_maple_inventory_lock_locked_state.png` — 探索背包裝備鎖定後，顯示金黃『已鎖定』膠囊與『解鎖』按鈕，並於詳情面板標註『裝備已鎖定無法出售』防誤賣提示
6. `proof_06_maple_inventory_en_locale.png` — 英文語系 (en) 下探索背包介面：Equipped 置灰、Locked 狀態、No Emoji
7. `proof_07_power_stat_soul_resonance_zh_tw.png` — PowerStatDialog 戰力屬性總覽：第四大戰力支柱『戰魂共鳴』雙欄卡片（齒、甲、簧、衡四大核心）與『前往聚魂』珊瑚粉果凍按鈕
8. `proof_08_power_stat_soul_resonance_en.png` — 英文語系 (en) 下 PowerStatDialog 戰力屬性總覽：Soul Resonance 卡片與 Go to Soul Draw 快捷按鈕
9. `proof_09_power_stat_jump_to_soul_hall.png` — 大廳無縫連動跳轉：點擊前往聚魂後，大廳切換至聚魂殿堂 (Tab.SOUL_HALL)
