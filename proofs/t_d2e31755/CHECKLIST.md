# 全面回歸驗收證明 · MapleInventory 探索背包一鍵出售素材合進主線後的全站回歸驗收 (t_d2e31755 / t_1524faa0)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）開發、測試小婷（`sideqa`）完成獨立驗收審查、並由主管老周完成主線合併（卡號 `t_d2e31755`，merge commit `c94dc0ac`）之功能分支：
- `inventory-batch-sell-materials`（t_6b9f41f3）：MapleInventory 探索背包支援一鍵出售未鎖定素材與金幣結算浮動提示

在合併至 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全機制回歸測試、自動化單元測試、無頭引擎冒煙測試、六語系驗證、真實 OpenGL3 實機渲染截圖存證，確認無任何 SCRIPT ERROR、無破圖、零系統 Emoji，並將 `docs/PROJECTS.json` 項目狀態正式更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **一鍵出售專用單元測試** | `TEST_FILTER=test_maple_inventory_batch_sell ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_BATCH_SELL_OK`） | **PASS** |
| **探索背包全套相關測試** | `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 11/11 全部通過（batch_sell, capacity, chips, diff, dismantle, equip, equipped, test_maple_inventory, lock, shortcuts, sort 全部通過） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，拒絕虛假圖片。
- [x] **獨立 Proof 目錄**：所有實機全景圖與特寫圖存證於 `proofs/t_d2e31755/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 一鍵出售素材按鈕 (`BtnBatchSellMaterials`)：薄荷綠果凍厚底按鈕（#4ED86A，邊框 #1F1A3A，厚底 5px，圓角 18px，高度 52px >= 48px，字級 18px）。
  - 分類與選取連動：切換至『素材』分類時顯示；全部分類下選取素材時顯示；切換至裝備、消耗品、寶石分類時嚴格隱藏。
  - 金幣結算浮動提示：結算後彈出 `GoldFloatingToast`，水平居中於頂部分隔線上方，顯示「賣出材料 14 件 · 金 +108」，平滑淡出。
  - 安全鎖定過濾：已鎖定之素材（如 `wolf_fang x5`）完好保留未被誤售，僅未鎖定素材被出售並累加金幣。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼斷言，UI 元素全面清除系統 emoji，採用純淨手繪/向量圖示與粉圓體文字。
- [x] **多語系即時在地化切換**：繁中 (zh_TW)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es)、簡中 (zh_CN) 動態切換無需重啟，無缺詞漏詞，英文語系無 CJK 殘留。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-batch-sell-materials` 更新為『已上線』並推向遠端。

---

## 4. 存證截圖清單 (proofs/t_d2e31755/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_maple_inv_batch_sell_material_category_zh_tw.png` | 切換至『素材』Chip 分類時，右側詳情欄呈現薄荷綠果凍厚底按鈕『一鍵出售素材』（高 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | `607485164433` | **PASS** |
| 02 | `proof_02_maple_inv_batch_sell_material_selected_detail.png` | 選取素材【鐵屑】時，右側詳情面板呈現『一鍵出售素材』與『前往工坊』雙快捷按鈕，無縫連動 | ✓ | ✓ | ✓ | `ea28a7259d91` | **PASS** |
| 03 | `proof_03_maple_inv_batch_sell_floating_gold_toast.png` | 點擊一鍵出售後，彈出金幣結算浮動提示卡片（`GoldFloatingToast`）與飄字，居中顯示售出 14 件與獲得 108 金幣 | ✓ | ✓ | ✓ | `8fc08836b140` | **PASS** |
| 04 | `proof_04_maple_inv_batch_sell_completed_locked_retained.png` | 出售完成後背包狀態：未鎖定素材全數清除，已鎖定之素材【棘輪尖齒】完好保留未被誤售，詳情正確展示 | ✓ | ✓ | ✓ | `66e6d8d2a0e5` | **PASS** |
| 05 | `proof_05_maple_inv_batch_sell_en_locale.png` | 英文語系 (en) 素材分類展示：按鈕文案為『Quick-Sell Materials』，全介面零中文殘留，排版整齊 | ✓ | ✓ | ✓ | `26ca590bde15` | **PASS** |
| 06 | `proof_06_maple_inv_batch_sell_ja_locale.png` | 日文語系 (ja) 素材分類展示：按鈕文案為『素材を一括売却』，日文字形渲染清晰無穿模 | ✓ | ✓ | ✓ | `d40b14416bd1` | **PASS** |
| 07 | `proof_07_maple_inv_batch_sell_ko_locale.png` | 韓文語系 (ko) 素材分類展示：按鈕文案為『재료 일괄 판매』，韓文字形渲染清晰工整 | ✓ | ✓ | ✓ | `ed4da3949a88` | **PASS** |
| 08 | `proof_08_maple_inv_batch_sell_es_locale.png` | 西班牙文語系 (es) 素材分類展示：按鈕文案為『Vender materiales』，歐美語系排版符合手遊規範 | ✓ | ✓ | ✓ | `e7ef0ecf0b37` | **PASS** |
