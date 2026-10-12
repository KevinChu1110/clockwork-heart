# 全面回歸驗收證明 · MapleInventory 探索背包裝備拆解回收功能合進主線後的全站回歸驗收 (t_a36f9bb8)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）開發、測試小婷（`sideqa`）完成獨立驗收審查、並由主管老周完成主線合併（卡號 `t_de857c1c`，merge commit `611260b8`）之功能分支：
- `inventory-dismantle-recycle`（t_783e312b）：MapleInventory 探索背包選取裝備支援拆解回收與安全防護

在合併至 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全機制回歸測試、自動化單元測試、無頭引擎冒煙測試、多語系驗證、真實 OpenGL3 實機截圖存證，確認無任何 SCRIPT ERROR、無破圖、零系統 Emoji，並將 `docs/PROJECTS.json` 項目狀態正式更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **拆解核心系統單元測試** | `TEST_FILTER=test_equipment_dismantle ./tools/run_tests.sh` | 1/1 通過（`EQUIPMENT_DISMANTLE_OK`） | **PASS** |
| **背包機芯拆解單元測試** | `TEST_FILTER=test_bag_core_dismantle ./tools/run_tests.sh` | 1/1 通過（`TEST_BAG_CORE_DISMANTLE_OK`） | **PASS** |
| **背包拆解按鈕單元測試** | `TEST_FILTER=test_bag_dismantle_btn ./tools/run_tests.sh` | 1/1 通過（`TEST_BAG_DISMANTLE_BTN_OK`） | **PASS** |
| **裝備寶石詳情與拆解測試** | `TEST_FILTER=test_bag_gem_detail_and_dismantle ./tools/run_tests.sh` | 1/1 通過（`TEST_BAG_GEM_DETAIL_AND_DISMANTLE_OK`） | **PASS** |
| **探索背包拆解全套單元測試** | `TEST_FILTER=test_maple_inventory_dismantle ./tools/run_tests.sh` | 1/1 通過（`MAPLE_INVENTORY_DISMANTLE_OK`，18 步全機制驗證） | **PASS** |
| **探索背包全套相關測試** | `TEST_FILTER=maple_inventory ./tools/run_tests.sh` | 9/9 全部通過（chips, diff, dismantle, equip, equipped, core, lock, sort 全部通過） | **PASS** |
| **全拆解相關測試組** | `TEST_FILTER=dismantle ./tools/run_tests.sh` | 5/5 全部通過 | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，拒絕虛假圖片。
- [x] **獨立 Proof 目錄**：所有實機全景圖與特寫圖存證於 `proofs/t_a36f9bb8/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 探索背包拆解按鈕：高度 52px（>= 48px），立體果凍厚底 5px，圓角 18px，熱區充足。
  - 按鈕樣式：正常狀態為高飽和珊瑚粉 (#FF5E8A) 搭配深色厚描邊 (#1F1A3A)；置灰禁用狀態為淡灰紫底 (#E8E4EC) 搭配紫灰邊框 (#9E96AF) 與字色 (#7A7090)。
  - 防誤拆防護：已鎖定裝備動態置灰並顯示『已鎖定無法拆解』，詳情面板標註橘紅色提示『裝備已鎖定無法出售』；已穿戴裝備動態置灰並顯示『已穿戴無法拆解』。
  - 鑲嵌寶石返還：拆解裝備時返還鐵屑與金幣，鑲嵌寶石（如紅寶石 Lv.1）安全退回 GemSystem，無被吞或損壞風險。
  - 非裝備道具安全保護：選取消耗品與素材時，拆解按鈕自動安全隱藏，維持原快捷欄操作按鈕。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼斷言，UI 元素全面清除系統 emoji，採用純淨手繪/向量圖示與粉圓體文字。
- [x] **多語系即時在地化切換**：繁中 (zh_TW)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es)、簡中 (zh_CN) 動態切換無需重啟，無缺詞漏詞。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-dismantle-recycle` 更新為『已上線』並推向遠端。

---

## 4. 存證截圖清單 (proofs/t_a36f9bb8/)

1. `proof_01_dismantle_ready_zh_tw.png` — 繁中語系下選取未穿戴未鎖定裝備 (rusty_blade)，顯示珊瑚粉果凍厚底按鈕『拆解回收』（高度 52px、厚底 5px、圓角 18px）
2. `proof_02_dismantle_locked_protected.png` — 選取已鎖定裝備 (ash_mail)，按鈕動態置灰『已鎖定無法拆解』(disabled=true)，詳情面板標註『裝備已鎖定無法出售』
3. `proof_03_dismantle_equipped_protected.png` — 選取已穿戴裝備 (meager_edge)，按鈕動態置灰『已穿戴無法拆解』(disabled=true)
4. `proof_04_dismantle_success_and_refund.png` — 拆解成功、鐵屑與金幣回收、鑲嵌寶石安全返還至背包，裝備乾淨自背包移除
5. `proof_05_dismantle_i18n_en.png` — 英文語系 (en) 選取未穿戴裝備，顯示『Dismantle』果凍按鈕，零 Emoji，多巴胺高飽和
6. `proof_06_dismantle_i18n_en_locked.png` — 英文語系 (en) 選取已鎖定裝備，顯示『Locked (Cannot Dismantle)』置灰保護按鈕
7. `proof_07_dismantle_consumables_shortcuts.png` — 選取消耗品 (hp_s)，拆解按鈕安全隱藏，維持原快捷欄按鈕『放到快捷欄』
