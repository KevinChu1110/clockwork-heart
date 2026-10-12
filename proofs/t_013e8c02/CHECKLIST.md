# 實機驗收證明 · MapleInventory 探索背包支援快捷欄綁定狀態膠囊顯示與一鍵卸下快捷鍵 (t_013e8c02)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）負責之需求卡號 `t_013e8c02`：
- `inventory-hotbar-toggle`：MapleInventory 探索背包支援快捷欄綁定狀態膠囊顯示與一鍵卸下快捷鍵
- 驗收項目：
  1. 檢查 `GameState.hotbar`：若該道具已綁定於快捷欄（槽位 0~7），於明細面板顯示天藍底（#38A0FF）『快捷欄 1』或『快捷欄 2』標籤膠囊（字級 14~16px 加粗，深藍紫描邊 outline 3px，白色文字，零 Emoji）。
  2. 原「放到快捷欄」按鈕動態切換文案與樣式：未綁定顯示天藍底『放到快捷欄』，已綁定切換為珊瑚粉果凍厚底按鈕『從快捷欄卸下』。
  3. 點擊卸下時，清空 `GameState.hotbar` 對應槽位，發出 `remove_hotbar` 信號，觸發 Toast 提示『已從快捷欄卸下：XX』並即時刷新主畫面快捷欄與背包按鈕狀態。
  4. 支援六語系（`ui_hotbar_slot_capsule` / `ui_remove_hotbar`）、按鈕熱區 >= 48px (實際 52px)、果凍厚底 5px、無 13px 以下小字、零 Emoji。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **快捷欄膠囊與雙向切換單元測試** | `TEST_FILTER=test_maple_inventory_hotbar_toggle ./tools/run_tests.sh` | 1/1 全部通過（`MAPLE_INVENTORY_HOTBAR_TOGGLE_OK`） | **PASS** |
| **探索背包全套單元測試** | `TEST_FILTER=test_maple_inventory ./tools/run_tests.sh` | 13/13 全部通過（batch_sell, capacity, chips, consumable_use, diff, dismantle, equip, equipped, test_maple_inventory, hotbar_toggle, lock, shortcuts, sort 全部通過） | **PASS** |
| **全站道具背包整合測試** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 14/14 全部通過（test_inventory_item_i18n + 13 支背包單元測試） | **PASS** |
| **素材與軟連結檢查** | `clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **真實 OpenGL3 渲染存證**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機截圖，8 張截圖 SHA256 全部唯一。
- [x] **獨立 Proof 目錄**：所有實機全景圖存證於 `proofs/t_013e8c02/` 獨立目錄，不污染其他任務。
- [x] **手遊人體工學與多巴胺視覺規範**：
  - 快捷欄切換按鈕 (`BtnHotbarToggle`)：高度 52px >= 48px，果凍厚底 5px，圓角 18px，字級 18px >= 16px。
  - 未綁定：天藍底（#38A0FF），深藍紫邊框（#1F1A3A），文字『放到快捷欄』。
  - 已綁定：珊瑚粉底（#FF5E8A），深藍紫邊框（#1F1A3A），文字『從快捷欄卸下』。
  - 快捷欄標籤膠囊 (`HotbarCapsule`)：天藍底（#38A0FF），深藍紫描邊（#1F1A3A），3px 厚底，圓角 10px，白字加粗帶深藍紫描邊，字級 14px。
  - 卸下浮動提示 (`HotbarFloatingToast`)：米白暖底（#FFFDF8），深藍紫描邊（#1F1A3A），4px 厚底，圓角 18px，深色文字 20px，平滑浮現淡出。
- [x] **零系統原生 Emoji**：經視覺審查與程式碼遍歷檢查，全畫面 100% 零系統原生 Emoji。
- [x] **六語系即時在地化切換**：繁中 (zh_TW)、簡中 (zh_CN)、英文 (en)、日文 (ja)、韓文 (ko)、西文 (es) 動態切換無需重啟，無缺詞漏詞，英文語系無 CJK 殘留。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-hotbar-toggle` 更新為『測試中』。

---

## 4. 存證截圖清單 (proofs/t_013e8c02/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_hotbar_unbound_assign_btn_sky_zh_tw.png` | 選取未綁定消耗品 (hp_s)：右側詳情欄膠囊隱藏，按鈕呈現天藍果凍厚底『放到快捷欄』（高 52px，厚底 5px，圓角 18px，字級 18px） | ✓ | ✓ | ✓ | **PASS** |
| 02 | `proof_02_hotbar_bound_slot1_capsule_pink_btn_zh_tw.png` | 綁定至槽位 0：名稱右側呈現天藍底『快捷欄 1』標籤膠囊（字級 14px，深藍紫描邊），按鈕切換為珊瑚粉『從快捷欄卸下』 | ✓ | ✓ | ✓ | **PASS** |
| 03 | `proof_03_hotbar_bound_slot2_capsule_zh_tw.png` | 道具處於槽位 1：名稱右側標籤膠囊動態識別為天藍底『快捷欄 2』，按鈕維持『從快捷欄卸下』 | ✓ | ✓ | ✓ | **PASS** |
| 04 | `proof_04_hotbar_unbind_toast_zh_tw.png` | 點擊『從快捷欄卸下』：彈出米白浮動提示『已從快捷欄卸下：微光潤滑油』，膠囊即時隱藏，按鈕切換回『放到快捷欄』 | ✓ | ✓ | ✓ | **PASS** |
| 05 | `proof_05_hotbar_bound_en.png` | 英文語系 (en)：呈現天藍底『Hotbar 1』膠囊與珊瑚粉『Remove from Hotbar』按鈕，全介面零中文殘留 | ✓ | ✓ | ✓ | **PASS** |
| 06 | `proof_06_hotbar_bound_ja.png` | 日文語系 (ja)：呈現天藍底『ショートカット 1』膠囊與珊瑚粉『ショートカットから解除』按鈕，日文字形工整無穿模 | ✓ | ✓ | ✓ | **PASS** |
| 07 | `proof_07_hotbar_bound_ko.png` | 韓文語系 (ko)：呈現天藍底『단축칸 1』膠囊與珊瑚粉『단축칸에서 해제』按鈕，韓文字形清晰無溢出 | ✓ | ✓ | ✓ | **PASS** |
| 08 | `proof_08_hotbar_bound_es.png` | 西班牙文語系 (es)：呈現天藍底『Acceso rápido 1』膠囊與珊瑚粉『Quitar de acceso rápido』按鈕，排版完美符合手遊規範 | ✓ | ✓ | ✓ | **PASS** |
