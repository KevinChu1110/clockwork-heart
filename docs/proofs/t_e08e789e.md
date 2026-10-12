# 全面回歸驗收證明 · PowerStatDialog 機芯快捷與 MapleInventory 機芯拆解回收雙分支合進主線後的全站回歸驗收 (t_e08e789e)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩大重要功能分支：
1. **`power-stat-core-shortcut`（t_f6bb0eb2）**：分支 `agent/20261012-power-stat-core-shortcut-t_f6bb0eb2`
   - PowerStatDialog 戰力屬性總覽新增機芯部件卡片（CorePartCard）與五大槽位展示
   - 新增『前往校準』快捷按鈕（BtnGoCalibrate，88x36px，熱區 >= 48px，暖橘果凍厚底 4px）
   - 點擊發射 calibrate_requested 信號並自動連動大廳開啟天宮鐵匠校準（ForgeDialog）
   - 六語系在地化支援（前往校準 / 机芯部件 / Calibrate / 較正へ / 교정하러 가기 / Calibrar）
2. **`inventory-core-dismantle-recycle`（t_00903732）**：分支 `agent/20261012-maple-inventory-core-dismantle-t_00903732`
   - MapleInventory 探索背包支援選取機芯拆解回收（BtnDismantle，高 52px >= 48px）
   - 嚴格安全防護：已裝備於五大槽位機芯（is_selected_item_equipped()）切換為禁用『已裝備無法拆解』，嚴防誤拆
   - 依 CoreSystem 八色階標準產出鐵屑（灰1、白2、橘3、藍4、紫5、金6、綠8、紅10），拆解後背包即時扣除並刷新容量
   - 六語系完整在地化支援與零系統 Emoji 規範

由工程師阿翔（`sideworker2`）在 `main` 主線執行雙分支無衝突合併（Merge commits: `7dd61d45`, `045c9fc3`），解決 i18n 語系檔與 PROJECTS.json 衝突，執行全套無頭冒煙測試、全套單元測試、官網 live 檢測與素材檢查，並透過 `project_status.py` 同步將兩項目更新為『已上線』推向 `origin/main`。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **戰力機芯快捷單元測試** | `godot --path game --headless -s scripts/ui/test_power_stat_core_shortcut.gd` | 全部測試通過（按鈕熱區、CoreSystem讀取、六語系、大廳連動） | **PASS** |
| **機芯拆解回收單元測試** | `godot --path game --headless -s scripts/ui/test_maple_inventory_core_dismantle.gd` | 全部測試通過（八色階鐵屑計算、已裝備防護、容量刷新、六語系） | **PASS** |
| **機芯替換回歸單元測試** | `godot --path game --headless -s scripts/ui/test_maple_inventory_core_replace.gd` | 全部測試通過（機芯 Chip 列、CoreReplaceDialog 彈窗與屬性刷新） | **PASS** |
| **機芯一鍵配置回歸測試** | `godot --path game --headless -s scripts/ui/test_lobby_core_auto_equip.gd` | 全部測試通過（五槽一鍵換裝、戰力即時刷新） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_power_stat_core_shortcut_zh_tw.png` | PowerStatDialog 戰力屬性總覽機芯部件卡片與前往校準按鈕 (繁中) | 1280×720 | `30fd8499e96963f0bb9949af69faa292302fd04b5b1dd04ae344a8f7dba1c5e5` |
| `proof_02_power_stat_core_shortcut_en.png` | PowerStatDialog 英文語系 Core Part 卡片與 Calibrate 按鈕 | 1280×720 | `ddb16b76fe1dd70f2898b92951c49de736fc4fe723ad5e28a328ad7222131a9c` |
| `proof_03_lobby_forge_integration.png` | 大廳點擊前往校準後成功連動開啟天宮鐵匠校準 (ForgeDialog) | 1280×720 | `4165a43afea2168ea82da8477ed4791d95e441669c0cabc8dcd36710655fa2a4` |
| `proof_04_core_equipped_protected_zh_tw.png` | MapleInventory 選取已裝備機芯禁用安全防護（已裝備無法拆解） | 1280×720 | `74c6f3a5a4899d10d92089b616a6b1e52e255bd9a7f09cac69ad5ea3b1d95b1f` |
| `proof_05_core_unequipped_ready_dismantle_zh_tw.png` | MapleInventory 選取未裝備機芯啟用拆解回收按鈕 (52px果凍厚底) | 1280×720 | `a985083403d0743ac4c388ebca236e841ebdf36327ccc17fabd2ca09e6f65ba3` |
| `proof_06_core_dismantled_scrap_gained_zh_tw.png` | 機芯拆解回收成功獲得鐵屑、容量更新與飄字反饋 | 1280×720 | `57ad96579f45bc7b9acd061ec23d0df341c68ea7144cb233dd45b8e76250d941` |
| `proof_07_core_dismantle_en.png` | 英文語系驗證：Equipped (Cannot Dismantle) 與 Dismantle 按鈕 | 1280×720 | `821070e13e02b1843c253de511c9767db5e5f54dde36c35e3da55a2f4ade9101` |
| `proof_08_core_dismantle_ja.png` | 日文語系驗證：装備中（分解不可）與分解回収按鈕 | 1280×720 | `be923065f1e488ee3522809ed4807f53f6ad16a79a2d38f4dcc9413823f8df3a` |

*註：8 張截圖 SHA256 互不相同，零重複，各語系渲染及時序等待皆符合手遊人因與視覺規範。*

---

## 4. 規範查核與審驗結論

- [x] **雙分支乾淨合併至 main**：依序合併 `7dd61d45` 與 `045c9fc3`，i18n 多語系鍵值完整整合，無遺漏。
- [x] **零系統原生 Emoji**：全面遵循規範，清除系統 emoji，採用粉圓體與質感果凍厚底按鈕。
- [x] **手遊人因工程與按鈕熱區**：
  - 前往校準按鈕熱區 >= 48px，果凍厚底 4px。
  - 機芯拆解按鈕高度 52px >= 48px，果凍厚底 5px，圓角 18px。
- [x] **安全防護機制**：已裝備於五大機芯槽位之部件絕對禁止拆解，按鈕置灰提示。
- [x] **多語系即時在地化切換**：六語系（zh_TW, zh_CN, en, ja, ko, es）完整對齊，無缺失。
- [x] **項目進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `power-stat-core-shortcut` 與 `inventory-core-dismantle-recycle` 更新為『已上線』，並推向 `origin/main`。
