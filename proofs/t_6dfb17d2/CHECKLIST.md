# 驗收查核清單 CHECKLIST · ForgeDialog 天宮鐵匠底欄新增『前往心法』快捷果凍按鈕連動 SkillDialog (t_6dfb17d2)

> 驗收執行人：發條之心·工程師 阿翔 (`sideworker2`)  
> 驗收分支：`agent/20261017-forge-dialog-skill-shortcut-t_6dfb17d2`

---

## 1. 介面與規格驗收

- [x] **按鈕規格與命名**：
  - 按鈕節點命名為 `BtnGoSkill`，位於 ForgeDialog 底部操作按鈕列 (`act_row`)。
  - 按鈕尺寸 `140x50px`，熱區規格 `>= 140x48px`（高度 50px），符合手遊人體工學防誤觸規範。
- [x] **色彩與果凍視覺風格**：
  - 採用多巴胺天藍色盤 `COLOR_SKY` (`#38A0FF`)，立體果凍厚底 5px，大圓角 18px，深藍紫描邊 `#1F1A3A`。
  - 字級 16px 開源粉圓體（Open Huninn），深藍紫字帶描邊，視覺對比清晰。
  - 100% 徹底清除系統 Emoji，無廉價感。
- [x] **訊號與連動機制**：
  - 提供 `skill_requested` 與 `go_skill` 雙訊號，並提供 `get_go_skill_button()` 存取器。
  - 點擊按鈕安全發射 `closed` 與跳轉訊號，順暢關閉 ForgeDialog（無遮罩與彈窗殘留）。
  - 大廳 `MobileLobby` 接收訊號直通開啟 `SkillDialog` 心法招式彈窗。
- [x] **雙向閉環流轉**：
  - 心法彈窗關閉後順暢返回 `ForgeDialog`，形成雙向操作閉環。
- [x] **六語系即時切換**：
  - 繁中 `zh_TW`：`前往心法`
  - 簡中 `zh_CN`：`前往心法`
  - 英文 `en`：`Go to Skills`
  - 日文 `ja`：`心法へ進む`
  - 韓文 `ko`：`심법으로 이동`
  - 西文 `es`：`Ir a Habilidades`
  - 12 處多語系字典完全對齊（`ui.json` 與 `<locale>.json`），切換語系動態即時刷新。

---

## 2. 測試與存證截圖

- [x] **專屬單元與整合測試**：
  - 執行 `godot --path game -s res://scripts/ui/test_forge_dialog_skill_shortcut.gd --headless`，輸出 `PASS_OK: TEST_FORGE_DIALOG_SKILL_SHORTCUT_OK 全部測試通過！`。
- [x] **無頭冒煙測試**：
  - 執行 `godot --path game --headless --quit-after 3`，0 SCRIPT ERROR / 0 Crash。
- [x] **clock-check 自動化檢查**：
  - 執行 `clock-check .`，全數通過：0 缺 .import、0 軟連結、語系 key 齊全、0 舊名詞。
- [x] **實機渲染截圖存證**（`xvfb-run` 獨立截圖）：
  - `proof_01_zh_TW_forge_dialog_btn_go_skill.png` (SHA256: ddef57adca46715d...)：繁中介面與天藍色 BtnGoSkill。
  - `proof_02_click_btn_go_skill_opens_skill_dialog.png` (SHA256: 0060818260a29ae3...)：直通開啟 SkillDialog 心法招式彈窗。
  - `proof_03_skill_dialog_loop_back_to_forge.png` (SHA256: 169e996a4a006c9c...)：返回 ForgeDialog 雙向閉環與第 2 槽位互動狀態。
  - `proof_04_zh_CN_forge_dialog_btn_go_skill.png` (SHA256: 3972ddd0bea4f03a...)：簡體中文『前往心法』。
  - `proof_05_en_forge_dialog_btn_go_skill.png` (SHA256: e4dc0d4177cc998f...)：英文『Go to Skills』。
  - `proof_06_ja_forge_dialog_btn_go_skill.png` (SHA256: 439559bdda60487d...)：日文『心法へ進む』。
  - `proof_07_ko_forge_dialog_btn_go_skill.png` (SHA256: ee7534319ec519cd...)：韓文『심법으로 이동』。
  - `proof_08_es_forge_dialog_btn_go_skill.png` (SHA256: 052f089a455a59aa...)：西文『Ir a Habilidades』。
  - 所有存證截圖雜湊互不相同，零同幀重複。
