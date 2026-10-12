# 全面回歸驗收證明 · 探索背包快捷欄卸下與大廳機芯替換彈窗雙分支合進主線後的全站回歸驗收 (t_8d640837)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩項重要功能分支：
1. **`inventory-hotbar-toggle`（t_013e8c02）**：分支 `agent/20261012-maple-inventory-hotbar-toggle-t_013e8c02`
   - MapleInventory 探索背包支援快捷欄綁定狀態膠囊顯示（天藍底 #38A0FF『快捷欄 1/2』）
   - 一鍵卸下快捷鍵與動態按鈕（未綁定天藍底『放到快捷欄』／已綁定珊瑚粉底 #FF5E8A『從快捷欄卸下』）
   - 雙向同步 GameState.hotbar、浮動飄字提示（HotbarFloatingToast『已從快捷欄卸下：XX』）與六語系支援
2. **`lobby-core-replace-compare`（t_f800a6fa）**：分支 `agent/20261012-lobby-core-replace-dialog-t_f800a6fa`
   - 大廳角色頁五大機芯槽位點擊更換裝備時連動彈出 CoreReplaceDialog 比較確認彈窗
   - 攻/防/血/色階/階級即時對比計算、確認替換時同步 GameState.core_slots 與大廳頂部戰力
   - 清除 5347 行等 13px 以下小字（改為 14~16px 加粗，深藍紫描邊，零小字）、六語系動態即時切換

由工程師阿翔（`sideworker2`）在 `main` 主線執行雙分支無衝突合併（Merge commits: `0c9e129f`, `7cce95bf`），解決 i18n 語系檔衝突，執行全套無頭冒煙測試、全套背包與大廳單元測試、官網 live 檢測與素材檢查，並透過 `project_status.py` 同步將兩項目更新為『已上線』推向 `origin/main`。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **快捷欄綁定與卸下測試** | `TEST_FILTER=hotbar ./tools/run_tests.sh` | 2/2 通過（`test_hotbar_dopamine`, `test_maple_inventory_hotbar_toggle`） | **PASS** |
| **機芯替換與比較測試** | `TEST_FILTER=core_replace ./tools/run_tests.sh` | 3/3 通過（`test_core_replace_compare`, `test_equip_core_replace`, `test_lobby_core_replace_dialog`） | **PASS** |
| **探索背包全套單元測試** | `TEST_FILTER=maple_inventory ./tools/run_tests.sh` | 13/13 全部通過（100% 綠燈覆蓋） | **PASS** |
| **大廳主介面全套測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 13/13 全部通過（100% 綠燈覆蓋） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論

- [x] **雙分支乾淨合併至 main**：依序合併 `0c9e129f` 與 `7cce95bf`，i18n 多語系鍵值完整整合，無遺漏。
- [x] **零系統原生 Emoji**：全面遵循規範，清除系統 emoji，採用粉圓體與質感果凍厚底按鈕。
- [x] **手遊人因工程與按鈕熱區**：
  - 快捷欄卸下按鈕高度 52px >= 48px，果凍厚底 5px，圓角 18px。
  - 機芯替換彈窗按鈕熱區 >= 48px，消除 13px 以下微小文字（升級為 14~16px 加粗帶深色描邊）。
- [x] **多語系即時在地化切換**：六語系（zh_TW, zh_CN, en, ja, ko, es）完整對齊，無缺失。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-hotbar-toggle` 與 `lobby-core-replace-compare` 更新為『已上線』，並推向 `origin/main`（HEAD: `52b5ba3d`）。
