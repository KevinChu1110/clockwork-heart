# 驗收查核清單 CHECKLIST · SkillDialog 心法招式底欄新增『前往衣櫥』快捷果凍按鈕聯動 WardrobeDialog (t_10bea025)

> 驗收執行人：發條之心·工程師 阿翔 (`sideworker2`)  
> 驗收分支：`agent/20261018-skill-wardrobe-shortcut-t_10bea025`

---

## 1. 介面與規格驗收

- [x] **按鈕規格與命名**：
  - 按鈕節點命名為 `BtnGoWardrobe`，位於 SkillDialog 底部操作按鈕列 (`BottomBar`)。
  - 按鈕尺寸 `140x50px`，熱區規格 `>= 140x48px`（高度 50px），符合手遊人體工學防誤觸規範。
  - 在 BottomBar 中與『前往背包』(`BtnGoInventory`)、『前往鍛造』(`BtnGoForge`)、『前往商城』(`BtnGoShop`)、『前往工坊』(`BtnGoWorkshop`) 並列。
- [x] **色彩與果凍視覺風格**：
  - 採用多巴胺金黃色盤 `COLOR_GOLD` (`#FFD028`)，立體果凍厚底 5px，大圓角 16px，深藍紫描邊 `#1F1A3A` 2px。
  - 字級 16px 開源粉圓體（Open Huninn），深藍紫字帶微描邊，視覺對比清晰。
  - 100% 徹底清除系統 Emoji，無廉價感。
- [x] **訊號與連動機制**：
  - 提供 `wardrobe_requested` 與 `go_wardrobe` 雙訊號，並提供 `get_go_wardrobe_button()` 與 `get_wardrobe_button()` 存取器。
  - 點擊按鈕安全發射 `closed` 與跳轉訊號，順暢關閉 SkillDialog（無遮罩與彈窗殘留）。
  - 大廳 `MobileLobby` 接收訊號直通開啟 `WardrobeDialog` 衣櫥換裝彈窗。
- [x] **雙向閉環流轉**：
  - 關閉 `WardrobeDialog` 可順暢返回 `SkillDialog` 心法招式介面，形成雙向操作閉環。
- [x] **六語系即時切換**：
  - 繁中 `zh_TW`：`前往衣櫥`
  - 簡中 `zh_CN`：`前往衣橱`
  - 英文 `en`：`Go to Wardrobe`
  - 日文 `ja`：`衣装部屋へ`
  - 韓文 `ko`：`의상실로 이동`
  - 西文 `es`：`Ir al Armario`
  - 12 處多語系字典完全對齊（`ui.json` 與 `<locale>.json`），歐美語系零 CJK 殘留與零 Emoji。

---

## 2. 測試與存證截圖

- [x] **專屬單元與整合測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_skill_wardrobe_shortcut.gd --headless`，輸出 `PASS_OK` 與 `TEST_SKILL_WARDROBE_SHORTCUT_OK`。
- [x] **無頭冒煙測試**：
  - 執行 `godot --path game --headless --quit-after 3`，0 SCRIPT ERROR / 0 Crash。
- [x] **關聯回歸測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_workshop_shortcut.gd --headless`，全部通過。
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_forge_shortcut.gd --headless`，全部通過。
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_shop_shortcut.gd --headless`，全部通過。
  - 執行 `godot --path game -s res://scripts/ui/test_skill_dialog_inventory_shortcut.gd --headless`，全部通過。
- [x] **實機渲染截圖存證**（`xvfb-run` 獨立截圖，零重複 SHA256）：
  - `proof_01_zh_TW_skill_dialog_btn_go_wardrobe.png` (SHA256: `bab35a326de19a21...`)：繁中介面與金黃色 BtnGoWardrobe
  - `proof_02_zh_TW_wardrobe_dialog_opened.png` (SHA256: `e282cb05a5ef28b2...`)：直通連動開啟大廳 WardrobeDialog 視窗
  - `proof_03_zh_TW_skill_dialog_btn_go_wardrobe.png` (SHA256: `9cef91c8dc5469dc...`)：繁體中文
  - `proof_04_zh_CN_skill_dialog_btn_go_wardrobe.png` (SHA256: `d0d5158f192faec2...`)：簡體中文
  - `proof_05_en_skill_dialog_btn_go_wardrobe.png` (SHA256: `dea355a5077edc67...`)：英文
  - `proof_06_ja_skill_dialog_btn_go_wardrobe.png` (SHA256: `92612b942c171f62...`)：日文
  - `proof_07_ko_skill_dialog_btn_go_wardrobe.png` (SHA256: `922e68698a8c90d0...`)：韓文
  - `proof_08_es_skill_dialog_btn_go_wardrobe.png` (SHA256: `9c53ff2d03f3cf5b...`)：西文
  - `proof_09_locales_btn_go_wardrobe.png` (SHA256: `bbb7b731128dc832...`)：多語系切換後畫面
  - 所有存證截圖雜湊互不相同，零同幀重複。
