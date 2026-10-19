# 全面回歸驗收證明 · 把已過審的心法前往聚魂與聚魂前往心法雙分支合進主線 (t_d80cea6d)

## 1. 任務背景與驗收目標
將已由測試小婷（`sideqa`）完成獨立驗收審查並通過的心法招式前往聚魂殿堂與聚魂殿堂前往心法招式雙快捷分支乾淨合併至 main 主線：
1. **t_e6e9756b**：`SkillDialog` 心法招式底欄新增『前往聚魂』快捷果凍按鈕連動聚魂殿堂（分支 `origin/agent/20261019-skill-dialog-soul-hall-shortcut-t_e6e9756b`，commit `99e31c5ee`）
2. **t_cb73d5ff**：`MobileLobby` 聚魂殿堂底欄新增『前往心法』快捷果凍按鈕聯動 `SkillDialog`（分支 `origin/agent/20261019-soul-hall-skill-shortcut-t_cb73d5ff`，commit `0d8cbcb6d`）

### 功能特性與 UI 規範：
- **MobileLobby 聚魂殿堂前往心法 (`BtnGoSkill`)**：
  - 樣式：多巴胺天藍色盤 `#38A0FF`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`（2px）與深色字 `#1F1A3A`
  - 尺寸：140x52px（熱區 >= 48px，高度 52px，符合手遊人體工學）
  - 連動：點擊發射 `skill_requested` 信號並播放 UI 音效，順暢開啟 `SkillDialog` 心法招式彈窗
- **SkillDialog 前往聚魂 (`BtnGoSoulHall`)**：
  - 樣式：多巴胺金黃色盤 `#FFD028`、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`（2px）與深色字 `#1F1A3A`
  - 尺寸：140x50px（熱區 >= 48px，高度 50px，符合手遊人體工學）
  - 連動：點擊發射 `soul_hall_requested`、`go_soul_hall` 與 `closed` 信號，順暢關閉心法彈窗並切換至大廳聚魂殿堂分頁 (`Tab.SOUL_HALL`)
- **雙向閉環流轉**：
  - 大廳聚魂殿堂點擊『前往心法』直通招式心法彈窗，招式心法點擊『前往聚魂』安全關閉彈窗並切回聚魂殿堂，形成順暢的雙向閉環操作。
- **六語系對齊**：
  - `soul_hall.btn_go_skill`：繁中 `前往心法`、簡中 `前往心法`、英文 `To Skills`、日文 `心法へ`、韓文 `심법으로`、西文 `A Habilidades`
  - `skill.btn_go_soul_hall`：繁中 `前往聚魂`、簡中 `前往聚魂`、英文 `To Soul Hall`、日文 `聚魂殿へ`、韓文 `집혼전으로`、西文 `A Salón de Almas`
- **100% 零系統 Emoji**，完全遵循手遊人體工學與設計規範，採用開源粉圓體（Open-Huninn）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **心法前往聚魂單元測試** | `godot --path game --headless -s scripts/ui/test_skill_dialog_soul_hall_shortcut.gd` | 熱區>=48px、金黃色盤、信號與六語系全過 (TEST_SKILL_DIALOG_SOUL_HALL_SHORTCUT_OK) | **PASS** |
| **聚魂前往心法單元測試** | `godot --path game --headless -s scripts/ui/test_soul_hall_skill_shortcut.gd` | 熱區>=48px、天藍色盤、信號與六語系全過 (TEST_SOUL_HALL_SKILL_SHORTCUT_OK) | **PASS** |
| **雙快捷主線合併回歸測試** | `xvfb-run -a godot --path game --rendering-driver opengl3 --audio-driver Dummy -s scripts/ui/test_batch_soul_hall_skill_shortcuts_t_d80cea6d.gd` | 雙快捷熱區、樣式、大廳雙向閉環連動、六語系全檢驗通過 (TEST_BATCH_SOUL_HALL_SKILL_SHORTCUTS_OK) | **PASS** |
| **無頭冒煙測試** | `godot --headless --path game --quit-after 3` | 0 SCRIPT ERROR / 0 Crash | **PASS** |
| **素材與名詞規範檢查** | `clock-check /opt/side/bravesoul-game` | 缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留 | **PASS** |

---

## 3. 實機截圖存證清單
截圖檔案置於 `proofs/t_d80cea6d/` 與 `docs/proofs/t_d80cea6d/`（真 Framebuffer 渲染 1280x720，每張 201KB ~ 382KB，SHA256 均獨立無重複）：
1. `proof_01_zh_TW_soul_hall_to_skill.png` (SHA256: `e3f3191ab8c9bf78611b1e60e48c5f5589b0e990e30d0a1117d771e553a27dce`)：MobileLobby 聚魂殿堂底欄『前往心法』天藍色立體果凍按鈕實機截圖。
2. `proof_02_zh_TW_skill_to_soul_hall_loop.png` (SHA256: `9c5b79d4be8d4e6a6f7e77c5a5de0bc2d031353940ca5160771e62c1394adef7`)：連動開啟 SkillDialog 心法招式彈窗，底欄展示『前往聚魂』金黃色立體果凍按鈕實機截圖。
3. `proof_03_zh_TW_dual_shortcuts.png` (SHA256: `ec6d24877892fcf542d12585b15b9adee97a249ed85bbff3e4c9522f15b6d305`)：繁體中文（zh_TW）雙向按鈕文字對照存證。
4. `proof_04_zh_CN_dual_shortcuts.png` (SHA256: `21f165d6f6a7230cbf96a42ca74be5ccd8b86514a09c565d7f44ef294dbf88a5`)：簡體中文（zh_CN）雙向按鈕文字對照存證。
5. `proof_05_en_dual_shortcuts.png` (SHA256: `0d304599dc229c030377a3f6b98858be7b6e127f86613f9b800339fe62be496b`)：英文語系（en）雙向按鈕文字對照存證。
6. `proof_06_ja_dual_shortcuts.png` (SHA256: `e332beecff384e774e0366e86be602f6d75b3d388c813a8dc8e4d1b31e6de26c`)：日文語系（ja）雙向按鈕文字對照存證。
7. `proof_07_ko_dual_shortcuts.png` (SHA256: `8892236549b29d8f8fab0554619e5d20ff7c05714429410c0d29e3172025b769`)：韓文語系（ko）雙向按鈕文字對照存證。
8. `proof_08_es_dual_shortcuts.png` (SHA256: `9c1578113e3fdde9e1317f59bbfcfc43e405c615f471eaa8d5cfcba2ad2dc13e`)：西班牙語系（es）雙向按鈕文字對照存證。
