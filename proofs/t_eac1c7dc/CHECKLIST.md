# 全面回歸驗收證明 · MapleInventory 機芯替換與大廳機芯一鍵配置雙分支合進主線後的全站回歸驗收 (t_eac1c7dc)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩項重要功能分支：
1. **`inventory-core-category-replace`（t_ba3e60c1）**：分支 `agent/20261012-maple-inventory-core-replace-t_ba3e60c1`
   - MapleInventory 探索背包支援機芯分類頁籤 Chip 列（id=`core`，熱區 >= 40px，金黃選取高亮）
   - 選取機芯部件顯示專屬槽位膠囊（CoreSlotCapsule）與八色階標籤膠囊（CoreTierCapsule）
   - 替換機芯按鈕（BtnReplaceCore，高 52px >= 48px，立體果凍厚底 5px，圓角 18px）
   - 直通連動 CoreReplaceDialog 比較確認彈窗，支援即時數值/色階對比、取消回調與確認替換
   - 確認替換時同步 GameState.core_slots、發出 core_replaced 訊號、刷新背包與大廳戰力
2. **`lobby-core-auto-equip`（t_791dc011）**：分支 `agent/20261012-lobby-core-auto-equip-t_791dc011`
   - 大廳角色頁五大機芯槽位支援一鍵配置最高戰力機芯（BtnCoreAutoEquip，熱區 >= 48px，果凍厚底）
   - 點擊一鍵配置自動換上背包內最高戰力機芯，頂部戰力即時刷新，彈出「戰力提升 +XX！」飄字
   - 最佳狀態下再次點擊一鍵配置，彈出「目前已是最佳機芯配置！」防呆提示
   - 六語系（zh_TW, zh_CN, en, ja, ko, es）動態切換支援，零 Emoji，零 13px 以下小字

由工程師阿宏（`sideworker`）在 `main` 主線執行雙分支無衝突合併（Merge commits: `61813d0e`, `efe1651e`），解決 i18n 語系檔衝突，執行全套無頭冒煙測試、全套 core / maple_inventory / lobby 單元測試、官網 live 檢測與素材檢查，並透過 `project_status.py` 同步將兩項目更新為『已上線』推向 `origin/main`。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|\
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **機芯系統全套測試** | `TEST_FILTER=core ./tools/run_tests.sh` | 15/15 全部通過（`test_lobby_core_auto_equip`, `test_maple_inventory_core_replace` 等） | **PASS** |
| **探索背包全套單元測試** | `TEST_FILTER=maple_inventory ./tools/run_tests.sh` | 14/14 全部通過（100% 綠燈覆蓋） | **PASS** |
| **大廳機芯專屬測試** | `TEST_FILTER=lobby_core ./tools/run_tests.sh` | 2/2 通過（`test_lobby_core_auto_equip`, `test_lobby_core_replace_dialog`） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_eac1c7dc/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_char_core_slots_auto_equip_btn_zh_tw.png` | 大廳角色頁五大機芯槽位與一鍵配置按鈕 (BtnCoreAutoEquip) | 1280×720 | `d5a990188439d62fc572456166eae67adba55f785a8ea5c90b4c2e18681ca74a` |
| `proof_02_char_core_auto_equipped_power_boost_zh_tw.png` | 一鍵配置後高階機芯全數換上、飄字戰力提升提示與即時屬性刷新 | 1280×720 | `4bbdfc288b8d88f2846a6cb0a25eaaacd98c1e3f37b335e5b284b9db98b7e88c` |
| `proof_03_maple_inventory_core_chip_filtered_zh_tw.png` | MapleInventory 探索背包點選機芯分類 Chip，過濾顯示未裝備機芯部件與八色階標籤 | 1280×720 | `6a6b8779a542917cc52390f7a70c1103a8fddad7c6b5d704b7092a25dc7eae36` |
| `proof_04_maple_inventory_core_replace_dialog_zh_tw.png` | MapleInventory 選取機芯點擊替換機芯，直通連動 CoreReplaceDialog 比較確認彈窗 | 1280×720 | `b438fc699672dee9ef088d33302aa7b06d4524ed151fb1ae481171b82ce09cbf` |
| `proof_05_maple_inventory_core_en.png` | 英文語系驗證：MapleInventory Core chip, Swap Core button, slot capsules | 1280×720 | `91f16868ac1453889b80091f9bfc7432aab419d57abef3973ad170686a49a98a` |
| `proof_06_lobby_core_replace_dialog_ja.png` | 日文語系驗證：大廳角色頁機芯槽位與 CoreReplaceDialog 比較確認彈窗 (コア入替) | 1280×720 | `b44cf22d333df75f701b3f59cbb5a9721d0ca7f8a5bfd3996645e8cee60b0f10` |

*註：6 張截圖 SHA256 互不相同，零重複，各語系渲染及時序等待皆符合手遊人因與視覺規範。*

---

## 4. 規範查核與審驗結論

- [x] **雙分支乾淨合併至 main**：依序合併 `61813d0e` 與 `efe1651e`，i18n 多語系鍵值完整整合，無遺漏。
- [x] **零系統原生 Emoji**：全面遵循規範，清除系統 emoji，採用粉圓體與質感果凍厚底按鈕。
- [x] **手遊人因工程與按鈕熱區**：
  - 一鍵配置按鈕高度 52px >= 48px，果凍厚底 5px，圓角 18px。
  - 替換機芯按鈕熱區 >= 48px，消除 13px 以下微小文字（升級為 14~16px 加粗帶深色描邊）。
- [x] **多語系即時在地化切換**：六語系（zh_TW, zh_CN, en, ja, ko, es）完整對齊，無缺失。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `inventory-core-category-replace` 與 `lobby-core-auto-equip` 更新為『已上線』，並推向 `origin/main`。
