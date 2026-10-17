# 全面回歸驗收證明 · 把已過審的 EnergyLackDialog 前往儲能庫快捷分支合進主線 (t_8f1f5cf3)

## 1. 任務背景與驗收目標
將已由測試小婷（`sideqa`）完成獨立驗收審查並通過的 `energy-lack-vault-shortcut` (t_f267916e) 分支乾淨合併至 main 主線：
- **分支名**：`agent/20261016-energy-lack-vault-shortcut-t_f267916e` (commit `b41b291a0`)
- **功能內容**：在 `EnergyLackDialog`（能量不足彈窗）底欄操作按鈕區新增『前往儲能庫』(`BtnGoVault`) 快捷果凍按鈕，點擊發射 `vault_requested` 與 `closed` 信號，連動大廳順暢開啟 `ClockworkVaultDialog`（發條儲能庫放置收益彈窗），與儲能庫底部的前往委託／商城／鍛造等按鈕形成完整的雙向閉環流轉。
- **UI 規範**：
  - 陽光童話·多巴胺金黃色盤 `#FFD028`
  - 立體果凍厚底 6px、圓角 20px、深藍紫描邊 `#1F1A3A`
  - 尺寸 125x52px（按鈕熱區 >= 48px 防誤觸）
  - 100% 徹底清除系統 Emoji，使用開源粉圓體字型
- **六語系對齊**：
  - 繁中 `zh_TW`：`前往儲能庫`
  - 簡中 `zh_CN`：`前往储能库`
  - 英文 `en`：`To Vault`
  - 日文 `ja`：`貯蔵庫へ`
  - 韓文 `ko`：`저장고로 이동`
  - 西文 `es`：`Ir a Bóveda`

由工程師阿翔（`sideworker2`）在主線執行合併，解決六語系字典與 `PROJECTS.json` 衝突，執行專案測試與關聯回歸測試，並將 `PROJECTS.json` 中對應項目標記為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---|
| **專屬快捷單元測試** | `godot --headless -s res://scripts/ui/test_energy_lack_vault_shortcut.gd` | 五按鈕並列、StyleBox、熱區>=48px、零Emoji、六語系動態刷新、大廳連動開啟 ClockworkVaultDialog 全過 (TEST_ENERGY_LACK_VAULT_SHORTCUT_OK) | **PASS** |
| **能量不足前往商城單元測試** | `godot --headless -s res://scripts/ui/test_energy_lack_shop_shortcut.gd` | PASS (TEST_ENERGY_LACK_SHOP_SHORTCUT_OK) | **PASS** |
| **能量不足前往戰力單元測試** | `godot --headless -s res://scripts/ui/test_energy_lack_power_stat_shortcut.gd` | PASS (TEST_ENERGY_LACK_POWER_STAT_SHORTCUT_OK) | **PASS** |
| **能量不足六語系單元測試** | `godot --headless -s res://scripts/ui/test_energy_lack_i18n.gd` | PASS (TEST_ENERGY_LACK_I18N_OK) | **PASS** |
| **儲能庫系列關聯測試** | `TEST_FILTER=vault ./tools/run_tests.sh` | 13/13 支全部通過 | **PASS** |
| **大廳系列關聯測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 18/18 支全部通過 | **PASS** |
| **無頭冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR / 0 Crash | **PASS** |
| **程式與素材合規檢查** | `clock-check /root/.../repo` | 缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留（1 項 main 線直接維運警告已確認） | **PASS** |

---

## 3. 實機截圖存證清單
截圖檔案置於 `proofs/t_8f1f5cf3/`：
1. `proof_01_energy_lack_five_buttons_zh_TW.png`：EnergyLackDialog 底欄並列五顆果凍按鈕（廣告、儲能庫、商城、戰力、稍後再來），繁中文案『前往儲能庫』。
2. `proof_02_energy_lack_btn_go_vault_en.png`：英文語系即時刷新為『To Vault』。
3. `proof_03_energy_lack_btn_go_vault_ja.png`：日文語系即時刷新為『貯蔵庫へ』。
4. `proof_04_energy_lack_btn_go_vault_ko.png`：韓文語系即時刷新為『저장고로 이동』。
5. `proof_05_energy_lack_btn_go_vault_es.png`：西文語系即時刷新為『Ir a Bóveda』。
6. `proof_06_click_btn_go_vault_opens_clockwork_vault_dialog.png`：點擊 BtnGoVault 順暢關閉能量不足彈窗並開啟 ClockworkVaultDialog。

---

## 4. 專案狀態更新（docs/PROJECTS.json）
透過 `/root/project_status.py` 完成兩項專案狀態推進至『已上線』：
- `energy-lack-vault-shortcut`：`草稿` → `已上線`（備註：EnergyLackDialog 前往儲能庫快捷按鈕已合併至 main 並完成全套回歸驗收 (t_8f1f5cf3)）
- `merge-energy-lack-vault-shortcut`：`草稿` → `已上線`（備註：EnergyLackDialog 前往儲能庫快捷分支已合併至 main 主線並完成回歸驗收 (t_8f1f5cf3)）
