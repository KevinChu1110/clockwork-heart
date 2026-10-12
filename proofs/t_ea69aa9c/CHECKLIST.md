# 全面回歸驗收證明 · MapleInventory 探索背包前往鍛造與工坊快捷跳轉合進主線後的全站回歸驗收 (t_ea69aa9c)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）開發、測試小婷（`sideqa`）完成獨立驗收審查、並由主管老周完成主線合併（卡號 `t_5c4c087c`，merge commit `5887b74f`）之功能分支：
- `inventory-shortcuts`（t_31190d69）：MapleInventory 探索背包選取裝備與素材支援前往鍛造與前往工坊快捷跳轉

在合併至 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全機制回歸測試、自動化單元測試、無頭引擎冒煙測試、六語系驗證、真實 OpenGL3 實機渲染截圖存證，確認無任何 SCRIPT ERROR、無破圖、零系統 Emoji，並將 `docs/PROJECTS.json` 項目狀態正式更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **快捷跳轉專用單元測試** | `TEST_FILTER=test_maple_inventory_shortcuts ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_SHORTCUTS_OK`） | **PASS** |
| **探索背包全套相關測試** | `TEST_FILTER=maple_inventory ./tools/run_tests.sh` | 9/9 全部通過（chips, diff, dismantle, equip, equipped, lock, shortcuts, sort 全部通過） | **PASS** |
| **鍛造相關測試組** | `TEST_FILTER=forge ./tools/run_tests.sh` | 8/8 全部通過（forge_dialog_auto_forge, forge_i18n, forge_workshop_shortcut 等） | **PASS** |
| **工坊相關測試組** | `TEST_FILTER=workshop ./tools/run_tests.sh` | 4/4 全部通過（gem_workshop, gem_workshop_i18n 等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，拒絕虛假圖片。
- [x] **獨立 Proof 目錄**：所有實機全景圖與特寫圖存證於 `proofs/t_ea69aa9c/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 前往鍛造按鈕 (`BtnGoForge`)：暖橘果凍厚底按鈕（#FFA010，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）。
  - 前往工坊按鈕 (`BtnGoWorkshop`)：薄荷綠果凍厚底按鈕（#4ED86A，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）。
  - 狀態自動切換：選取裝備顯示『前往鍛造』並隱藏『前往工坊』；選取素材/寶石顯示『前往工坊』並隱藏『前往鍛造』；選取消耗品/重要道具雙按鈕嚴格隱藏，維持原快捷欄按鈕。
  - 無縫連動跳轉：點擊『前往鍛造』發射 `forge_requested` 訊號並直通開啟 `ForgeDialog`，平滑關閉背包；點擊『前往工坊』發射 `workshop_requested` 訊號並直通開啟 `GemWorkshopDialog`，平滑關閉背包。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼斷言，UI 元素全面清除系統 emoji，採用純淨手繪/向量圖示與粉圓體文字。
- [x] **多語系即時在地化切換**：繁中 (zh_TW)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es)、簡中 (zh_CN) 動態切換無需重啟，無缺詞漏詞，英文語系無 CJK 殘留。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-shortcuts` 更新為『已上線』並推向遠端。

---

## 4. 存證截圖清單 (proofs/t_ea69aa9c/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_weapon_selected_forge_btn.png` | 選取裝備【鏽劍】時，右側詳情面板顯示暖橘果凍厚底按鈕『前往鍛造』（`BtnGoForge`，高度 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `a7702bcacc58` | **PASS** |
| 02 | `proof_02_maple_inv_material_selected_workshop_btn.png` | 選取素材【鐵屑】時，右側詳情面板顯示薄荷綠果凍厚底按鈕『前往工坊』（`BtnGoWorkshop`，高度 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `28c660094b1f` | **PASS** |
| 03 | `proof_03_maple_inv_consumable_hidden_shortcuts.png` | 選取消耗品【微光潤滑油】時，『前往鍛造』與『前往工坊』按鈕嚴格隱藏，維持原快捷欄按鈕『放到快捷欄』 | ✓ | ✓ | ✓ | `1a1abeb8d4b0` | **PASS** |
| 04 | `proof_04_maple_inv_forge_dialog_opened.png` | 點擊『前往鍛造』後成功發射 `forge_requested` 訊號，自動平滑關閉背包並無縫彈出天宮鐵匠 `ForgeDialog` | ✓ | ✓ | ✓ | `ff1e2748147a` | **PASS** |
| 05 | `proof_05_maple_inv_gem_workshop_opened.png` | 點擊『前往工坊』後成功發射 `workshop_requested` 訊號，自動平滑關閉背包並無縫彈出手藝工坊 `GemWorkshopDialog` | ✓ | ✓ | ✓ | `0944298514f8` | **PASS** |
| 06 | `proof_06_maple_inv_shortcuts_i18n_en.png` | 英文語系 (en) 選取裝備展示：按鈕文字為『Go to Forge』，所有按鈕與 UI 標籤無中文殘留，排版工整 | ✓ | ✓ | ✓ | `e84db6199fa7` | **PASS** |
