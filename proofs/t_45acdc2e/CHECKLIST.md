# 驗收查核清單 CHECKLIST · SkillDialog 心法招式底欄新增『前往鍛造』快捷果凍按鈕聯動天宮鐵匠 (t_45acdc2e)

> 驗收執行人：發條之心·工程師 阿宏 (`sideworker`)  
> 驗收分支：`agent/20261017-skill-dialog-forge-shortcut-t_45acdc2e`

---

## 1. 介面與規格驗收

- [x] **按鈕規格與命名**：
  - 按鈕節點命名為 `BtnGoForge`，位於 SkillDialog 底部操作按鈕列 (`BottomBar`)。
  - 按鈕尺寸 `140x50px`，熱區規格 `>= 140x48px`（高度 50px），符合手遊人體工學防誤觸規範。
  - 在 BottomBar 中緊鄰『前往背包』(`BtnGoInventory`，idx 2) 與『前往商城』(`BtnGoShop`，idx 4)。
- [x] **色彩與果凍視覺風格**：
  - 採用多巴胺金黃色盤 `COLOR_GOLD` (`#FFD028`)，立體果凍厚底 5px，大圓角 18px，深藍紫描邊 `#1F1A3A`。
  - 字級 16px 開源粉圓體（Open Huninn），深藍紫字帶微描邊，視覺對比清晰。
  - 100% 徹底清除系統 Emoji，無廉價感。
- [x] **訊號與連動機制**：
  - 提供 `forge_requested` 與 `go_forge` 雙訊號，並提供 `get_go_forge_button()` 與 `get_forge_button()` 存取器。
  - 點擊按鈕安全發射 `closed` 與跳轉訊號，順暢關閉 SkillDialog（無遮罩與彈窗殘留）。
  - 大廳 `MobileLobby` 接收訊號直通開啟 `ForgeDialog` 天宮鐵匠彈窗。
- [x] **雙向閉環流轉**：
  - 關閉 `ForgeDialog` 可順暢返回 `SkillDialog` 心法招式介面，形成雙向操作閉環。
- [x] **六語系即時切換**：
  - 繁中 `zh_TW`：`前往鍛造`
  - 簡中 `zh_CN`：`前往锻造`
  - 英文 `en`：`Go to Forge`
  - 日文 `ja`：`鍛造へ進む`
  - 韓文 `ko`：`단조로 이동`
  - 西文 `es`：`Ir a Forja`
  - 12 處多語系字典完全對齊（`ui.json` 與 `<locale>.json`）。

---

## 2. 測試與存證截圖

- [x] **專屬單元與整合測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_forge_shortcut.gd --headless`，輸出 `PASS_OK` 與 `TEST_SKILL_DIALOG_FORGE_SHORTCUT_OK`。
- [x] **無頭冒煙測試**：
  - 執行 `godot --path game --headless --quit-after 3`，0 SCRIPT ERROR / 0 Crash。
- [x] **關聯回歸測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_shop_shortcut.gd --headless`，全部通過。
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_inventory_shortcut.gd --headless`，全部通過。
  - 執行 `godot --path game -s res://scripts/ui/test_skill_power_stat_shortcut.gd --headless`，全部通過。
- [x] **實機渲染截圖存證**（`xvfb-run` 獨立截圖）：
  - `proof_01_zh_TW_skill_dialog_btn_go_forge.png` (SHA256: 43bd2181f4fbbd03...)：繁中介面與金黃色 BtnGoForge
  - `proof_02_zh_TW_forge_dialog_opened.png` (SHA256: 083bdb8edb85592a...)：直通連動開啟天宮鐵匠 ForgeDialog 視窗
  - `proof_03_zh_CN_skill_dialog_btn_go_forge.png` (SHA256: db4ab90364e66ec4...)：簡體中文
  - `proof_04_en_skill_dialog_btn_go_forge.png` (SHA256: 3c4579e604f44182...)：英文
  - `proof_05_ja_skill_dialog_btn_go_forge.png` (SHA256: 69b5d13fe572d927...)：日文
  - `proof_06_ko_skill_dialog_btn_go_forge.png` (SHA256: c64e06d304f68b6d...)：韓文
  - `proof_07_es_skill_dialog_btn_go_forge.png` (SHA256: 7af529724f34220e...)：西文
  - 所有存證截圖雜湊互不相同，零同幀重複。
