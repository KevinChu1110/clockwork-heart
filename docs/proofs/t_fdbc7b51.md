# 全面回歸驗收證明 · 把已過審的手藝工坊前往心法與心法前往工坊雙分支合進主線 (t_fdbc7b51)

## 1. 任務背景與驗收目標
將已由測試小婷（`sideqa`）完成獨立驗收審查並通過的手藝工坊前往心法與心法前往工坊雙快捷分支乾淨合併至 main 主線：
1. **t_096b6592**：`GemWorkshopDialog` 手藝工坊底欄新增『前往心法』快捷果凍按鈕聯動心法招式 `SkillDialog`（分支 `agent/20261017-gem-workshop-skill-shortcut-t_096b6592`）
2. **t_d748c5d4**：`SkillDialog` 心法招式底欄新增『前往工坊』快捷果凍按鈕聯動手藝工坊 `GemWorkshopDialog`（分支 `agent/20261017-skill-dialog-workshop-shortcut-t_d748c5d4`）

### 功能特性與 UI 規範：
- **GemWorkshopDialog 前往心法 (`BtnGoSkill`)**：
  - 樣式：多巴胺天藍色盤 `#38A0FF`、圓角 18px、底厚 5px、深藍紫文字與描邊 `#1F1A3A`
  - 尺寸：130x50px（熱區 >= 48px）
  - 連動：點擊發射 `skill_requested` 與 `go_skill` 信號，順暢關閉工坊彈窗並呼起 `SkillDialog`
- **SkillDialog 前往工坊 (`BtnGoWorkshop`)**：
  - 樣式：多巴胺薄荷綠色盤 `#4ED86A`、圓角 18px、底厚 5px、深藍紫文字與描邊 `#1F1A3A`
  - 尺寸：140x50px（熱區 >= 140x48px）
  - 連動：點擊發射 `workshop_requested` 與 `go_workshop` 信號，順暢關閉心法彈窗並呼起 `GemWorkshopDialog`
- **雙向閉環流轉**：
  - 手藝工坊點擊『前往心法』直通心法招式，心法招式點擊『前往工坊』即刻返回手藝工坊，形成流暢的雙向閉環操作，且關閉工坊可順暢返回心法。
- **六語系對齊**：
  - `gem_workshop.btn_go_skill` / `ui.btn_go_skill`：繁中 `前往心法`、簡中 `前往心法`、英文 `Go to Skills`、日文 `心法へ進む`、韓文 `심법으로 이동`、西文 `Ir a Habilidades`
  - `skill.btn_go_workshop` / `ui.btn_go_workshop`：繁中 `前往工坊`、簡中 `前往工坊`、英文 `Go to Workshop`、日文 `工房へ進む`、韓文 `공방으로 이동`、西文 `Ir al Taller`
- **100% 零系統 Emoji**，完全遵循手遊人體工學與設計規範。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **工坊前往心法單元測試** | `godot --headless -s scripts/ui/test_gem_workshop_skill_shortcut.gd` | 熱區>=48px、天藍色盤、信號與六語系全過 (TEST_GEM_WORKSHOP_SKILL_SHORTCUT_OK) | **PASS** |
| **心法前往工坊單元測試** | `godot --headless -s scripts/ui/test_skill_dialog_workshop_shortcut.gd` | 熱區>=48px、薄荷綠色盤、信號與六語系全過 (TEST_SKILL_DIALOG_WORKSHOP_SHORTCUT_OK) | **PASS** |
| **雙快捷主線合併回歸測試** | `xvfb-run -a godot --path game -s scripts/ui/test_batch_dual_shortcuts_t_fdbc7b51.gd` | 雙快捷熱區、樣式、大廳雙向閉環連動、六語系全檢驗通過 (TEST_BATCH_DUAL_SHORTCUTS_REGRESSION_OK) | **PASS** |
| **既有四快捷回歸測試** | `godot --headless -s scripts/ui/test_batch_shortcuts_regression.gd` | 背包/商城/稱號/工坊四快捷連動通過 (TEST_BATCH_SHORTCUTS_REGRESSION_OK) | **PASS** |
| **上一批雙快捷回歸測試** | `godot --headless -s scripts/ui/test_batch_dual_shortcuts_t_beb52071.gd` | 心法與鍛造雙向閉環測試通過 (TEST_BATCH_DUAL_SHORTCUTS_REGRESSION_OK) | **PASS** |
| **無頭冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR / 0 Crash | **PASS** |
| **素材與名詞規範檢查** | `clock-check /opt/side/bravesoul-game` | 缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留 (1 direct on main warning acknowledged for ops merge task) | **PASS** |

---

## 3. 實機截圖存證清單
截圖檔案置於 `proofs/t_fdbc7b51/`、`docs/proofs/t_fdbc7b51/` 與看板附件中（SHA256 均獨立無重複）：
1. `proof_01_gem_workshop_btn_go_skill.png` (SHA256: `e817e3d9c17edb73...`)：GemWorkshopDialog 底欄『前往心法』果凍按鈕（天藍色盤 `#38A0FF`、熱區 130x50px）。
2. `proof_02_skill_dialog_btn_go_workshop.png` (SHA256: `311d10c8d497fd6f...`)：SkillDialog 底欄『前往工坊』果凍按鈕（薄荷綠色盤 `#4ED86A`、熱區 140x50px）。
3. `proof_03_lobby_gem_workshop.png` (SHA256: `388f5b7ecf3f0b10...`)：大廳直通開啟 GemWorkshopDialog 手藝工坊彈窗。
4. `proof_04_lobby_gem_workshop_to_skill.png` (SHA256: `21f127adfa784a1a...`)：點擊『前往心法』順暢開啟 SkillDialog 心法招式彈窗。
5. `proof_05_lobby_skill_to_gem_workshop_returned.png` (SHA256: `c81638a5b3cb0ac3...`)：點擊『前往工坊』順暢返回 GemWorkshopDialog，形成雙向互通閉環。

---

## 4. 專案狀態更新（docs/PROJECTS.json）
透過 `/root/project_status.py` 完成專案狀態推進至『已上線』：
- `gem-workshop-skill-shortcut`：`已上線`（GemWorkshopDialog 手藝工坊底欄新增前往心法快捷果凍按鈕連動 SkillDialog）
- `skill-workshop-shortcut`：`已上線`（SkillDialog 心法招式底欄新增前往工坊快捷果凍按鈕連動 GemWorkshopDialog）
- `merge-gem-workshop-skill-shortcuts`：`已上線`（已完成雙分支主線合併、單元與全面回歸測試全綠 (t_fdbc7b51)）
