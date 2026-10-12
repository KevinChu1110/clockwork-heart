# 全面回歸驗收證明 · MapleInventory 探索背包消耗品即時使用效果結算合進主線後的全站回歸驗收 (t_6d8496ba)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）開發、測試小婷（`sideqa`）完成獨立驗收審查、並由工程師阿翔（`sideworker2`）執行主線合併（卡號 `t_6d8496ba`，分支 `agent/20261011-maple-inventory-consumable-use-t_3bb0fb3b`）之功能：
- `inventory-consumable-use`（t_3bb0fb3b）：MapleInventory 探索背包支援消耗品即時使用效果結算與恢復浮動提示

在合併至 `origin/main` 後，由工程師阿翔在 `main` 主線執行全機制回歸測試、自動化單元測試、無頭引擎冒煙測試、六語系驗證、真實 OpenGL3 實機渲染截圖存證，確認無任何 SCRIPT ERROR、無破圖、零系統 Emoji，並將 `docs/PROJECTS.json` 項目狀態正式更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **消耗品使用專用單元測試** | `TEST_FILTER=test_maple_inventory_consumable_use ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_CONSUMABLE_OK`） | **PASS** |
| **探索背包全套相關測試** | `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 12/12 全部通過（batch_sell, capacity, chips, consumable_use, diff, dismantle, equip, equipped, test_maple_inventory, lock, shortcuts, sort 全部通過） | **PASS** |
| **全站道具背包整合測試** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 13/13 全部通過（test_inventory_item_i18n + 12 支背包單元測試） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，拒絕虛假圖片。
- [x] **獨立 Proof 目錄**：所有實機全景圖與特寫圖存證於 `proofs/t_6d8496ba/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 消耗品使用按鈕 (`BtnUseConsumable`)：薄荷綠果凍厚底按鈕（#4ED86A，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）。
  - 生命恢復結算閉環：受傷狀態選取 hp_s 扣除 1 瓶並即時回復 25 HP，右側數量即時刷新為 '×2'。
  - 恢復浮動提示：使用後彈出 `ConsumableFloatingToast`，水平居中於頂部分隔線上方，顯示「+25 HP」綠色多巴胺高對比字體，平滑淡出。
  - 生命已滿安全防護：滿血時恢復消耗品按鈕適應性置灰 (disabled=true)，文案顯示「生命已滿」，防止無效浪費；非恢復類消耗品（星屑碎）仍維持啟用可正常使用。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼斷言，UI 元素全面清除系統 emoji，採用純淨手繪/向量圖示與粉圓體文字。
- [x] **多語系即時在地化切換**：繁中 (zh_TW)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es)、簡中 (zh_CN) 動態切換無需重啟，無缺詞漏詞，英文語系無 CJK 殘留。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-consumable-use` 更新為『已上線』並推向遠端。

---

## 4. 存證截圖清單 (proofs/t_6d8496ba/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_consumable_selected_damaged_hp_ready_zh_tw.png` | 受傷狀態 (HP 20/50) 選取 hp_s，右側詳情欄呈現薄荷綠果凍厚底按鈕『使用』（高 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | **PASS** |
| 02 | `proof_02_consumable_use_floating_toast_heal_green.png` | 點擊『使用』後，彈出恢復浮動提示卡片（`ConsumableFloatingToast`）與飄字 '+25 HP'，詳情數量即時更新為 x2 | ✓ | ✓ | ✓ | **PASS** |
| 03 | `proof_03_consumable_selected_full_hp_disabled_zh_tw.png` | 角色生命已滿 (HP 50/50) 選取恢復類消耗品 (hp_s)，按鈕適應性置灰顯示『生命已滿』，防止無效浪費 | ✓ | ✓ | ✓ | **PASS** |
| 04 | `proof_04_consumable_non_heal_dust_crumb_usable.png` | 角色生命已滿選取非恢復類消耗品 (dust_crumb)，按鈕正常啟用顯示『使用』，可獲取星屑 | ✓ | ✓ | ✓ | **PASS** |
| 05 | `proof_05_consumable_full_hp_en.png` | 英文語系 (en) 滿血選取恢復消耗品：按鈕文案為『HP Full』，全介面零中文殘留，排版整齊 | ✓ | ✓ | ✓ | **PASS** |
| 06 | `proof_06_consumable_full_hp_ja.png` | 日文語系 (ja) 滿血選取恢復消耗品：按鈕文案為『HP満タン』，日文字形渲染清晰無穿模 | ✓ | ✓ | ✓ | **PASS** |
| 07 | `proof_07_consumable_full_hp_ko.png` | 韓文語系 (ko) 滿血選取恢復消耗品：按鈕文案為『HP 가득 참』，韓文字形渲染清晰工整 | ✓ | ✓ | ✓ | **PASS** |
| 08 | `proof_08_consumable_full_hp_es.png` | 西班牙文語系 (es) 滿血選取恢復消耗品：按鈕文案為『Salud llena』，歐美語系排版符合手遊規範 | ✓ | ✓ | ✓ | **PASS** |
