# 全面回歸驗收證明 · 把已過審的衣櫥前往儲能庫與儲能庫前往衣櫥雙分支合進主線 (t_e3ccf785)

## 1. 任務背景與驗收目標
將已由測試小婷（`sideqa`）完成獨立驗收審查並通過的衣櫥前往儲能庫與儲能庫前往衣櫥雙快捷分支乾淨合併至 main 主線：
1. **t_933567fb**：`WardrobeDialog` 衣櫥換裝彈窗底欄新增『前往儲能庫』快捷果凍按鈕聯動 `ClockworkVaultDialog`（分支 `agent/20261018-wardrobe-vault-shortcut-t_933567fb`）
2. **t_5f8d2190**：`ClockworkVaultDialog` 發條儲能庫放置收益底欄新增『前往衣櫥』快捷果凍按鈕聯動 `WardrobeDialog`（分支 `agent/20261018-vault-wardrobe-shortcut-t_5f8d2190`）

### 功能特性與 UI 規範：
- **WardrobeDialog 前往儲能庫 (`BtnGoVault`)**：
  - 樣式：多巴胺金黃色盤 `#FFD028`（`COLOR_GOLD`）、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`（`COLOR_BORDER` 2px）與深色字 `#1F1A3A`
  - 尺寸：112x50px（熱區 >= 105x48px，高度 >= 50px，符合手遊人體工學）
  - 連動：點擊發射 `vault_requested`、`go_vault` 與 `closed` 信號，順暢關閉衣櫥換裝彈窗並直通呼起 `ClockworkVaultDialog`
- **ClockworkVaultDialog 前往衣櫥 (`BtnGoWardrobe`)**：
  - 樣式：多巴胺暖橘色盤 `#FFA010`（`COLOR_ORANGE`）、圓角 18px、底厚 5px、深藍紫描邊 `#1F1A3A`（`COLOR_BORDER` 2px）與深色字 `#1F1A3A`
  - 尺寸：105x52px（熱區 >= 105x48px，高度 >= 50px，符合手遊人體工學）
  - 連動：點擊發射 `wardrobe_requested`、`go_wardrobe` 與 `closed` 信號，順暢關閉儲能庫彈窗並直通呼起 `WardrobeDialog`
- **雙向閉環流轉**：
  - 衣櫥換裝點擊『前往儲能庫』直通發條儲能庫彈窗，發條儲能庫點擊『前往衣櫥』即刻返回衣櫥換裝彈窗，形成順暢的雙向閉環操作。
- **六語系對齊**：
  - `wardrobe.btn_go_vault` / `wardrobe.go_vault`：繁中 `前往儲能庫`、簡中 `前往储能库`、英文 `To Vault`、日文 `貯蔵庫へ`、韓文 `저장고로 이동`、西文 `Ir a Bóveda`
  - `vault.btn_go_wardrobe` / `vault.go_wardrobe`：繁中 `前往衣櫥`、簡中 `前往衣橱`、英文 `To Wardrobe`、日文 `衣装部屋へ`、韓文 `의상실로`、西文 `Al Armario`
- **100% 零系統 Emoji**，完全遵循手遊人體工學與設計規範，採用開源粉圓體（Open-Huninn）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **衣櫥前往儲能庫單元測試** | `godot --path game --headless -s res://scripts/ui/test_wardrobe_vault_shortcut.gd` | 熱區>=48px、金黃色盤、信號與六語系全過 (TEST_WARDROBE_VAULT_SHORTCUT_OK) | **PASS** |
| **儲能庫前往衣櫥單元測試** | `godot --path game --headless -s res://scripts/ui/test_clockwork_vault_wardrobe_shortcut.gd` | 熱區>=48px、暖橘色盤、信號與六語系全過 (TEST_CLOCKWORK_VAULT_WARDROBE_SHORTCUT_OK) | **PASS** |
| **雙快捷主線合併回歸測試** | `xvfb-run -a godot --path game --resolution 1280x720 -s res://scripts/ui/test_batch_wardrobe_vault_shortcuts_t_e3ccf785.gd` | 雙快捷熱區、樣式、大廳雙向閉環連動、六語系全檢驗通過 (TEST_BATCH_WARDROBE_VAULT_SHORTCUTS_OK) | **PASS** |
| **無頭冒煙測試** | `godot --headless --path game --quit-after 3` | 0 SCRIPT ERROR / 0 Crash | **PASS** |
| **素材與名詞規範檢查** | `clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e3ccf785/bravesoul-game` | 缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留 | **PASS** |

---

## 3. 實機截圖存證清單
截圖檔案置於 `proofs/t_e3ccf785/` 與 `docs/proofs/t_e3ccf785/`（8 張實機截圖 SHA256 均獨立無重複）：
1. `proof_01_zh_TW_wardrobe_to_vault.png` (SHA256: `e8cfb5a72d10f54dfda8be3cfc4465477fde5a8e554a7dece599e5544ee67953`)：點擊 WardrobeDialog 底欄『前往儲能庫』果凍按鈕後，大廳直通連動呼起 ClockworkVaultDialog 實機截圖。
2. `proof_02_zh_TW_vault_to_wardrobe_loop.png` (SHA256: `cda15e8f82c0cb7b29f566b93c1b8801dbba8230179fc3a7263197ba4d08680e`)：在連動呼起之 ClockworkVaultDialog 點擊『前往衣櫥』果凍按鈕後，順暢返回呼起 WardrobeDialog 達成雙向閉環實機截圖。
3. `proof_03_zh_TW_dual_shortcuts.png` (SHA256: `8e117ff8a2afcdbe9aebac0aab7cc22edf8b5170220a163136ab5682ba66cc6a`)：繁體中文 (zh_TW) 雙快捷果凍按鈕對照檢驗實機截圖。
4. `proof_04_zh_CN_dual_shortcuts.png` (SHA256: `08a252ddcd1ec3748d0ebdebedc15c71b70e739614a9d62d14827917349a66ff`)：簡體中文 (zh_CN) 雙快捷果凍按鈕對照檢驗實機截圖。
5. `proof_05_en_dual_shortcuts.png` (SHA256: `5d66e13b21f6570b2493e151826ac12c1d22b57b0e1f390f036456eeab1b0f92`)：英文 (en) 雙快捷果凍按鈕對照檢驗實機截圖。
6. `proof_06_ja_dual_shortcuts.png` (SHA256: `8eb08ab843463c5769b0327bd866c0abd8a15bed1ea51b2200f24028385a09e7`)：日文 (ja) 雙快捷果凍按鈕對照檢驗實機截圖。
7. `proof_07_ko_dual_shortcuts.png` (SHA256: `160d3129116fe9ffae9c65fff733bb7b169fec4020984eea4be5492b7b0cec6c`)：韓文 (ko) 雙快捷果凍按鈕對照檢驗實機截圖。
8. `proof_08_es_dual_shortcuts.png` (SHA256: `f22b915601945a9b07ce6008ff47dbc5396b710e9a30881194fc1c17093c0d75`)：西班牙文 (es) 雙快捷果凍按鈕對照檢驗實機截圖。

---

## 4. 專案狀態更新（docs/PROJECTS.json）
透過 `/root/project_status.py` 完成專案狀態推進至『已上線』：
- `wardrobe-vault-shortcut`：`已上線`（WardrobeDialog 衣櫥換裝彈窗新增前往儲能庫快捷果凍按鈕連動 ClockworkVaultDialog 已過審合進主線）
- `vault-wardrobe-shortcut`：`已上線`（ClockworkVaultDialog 發條儲能庫放置收益新增前往衣櫥快捷果凍按鈕連動 WardrobeDialog 已過審合進主線）
- `merge-wardrobe-vault-shortcuts`：`已上線`（已完成雙分支主線合併、單元與回歸測試全綠 (t_e3ccf785)）
