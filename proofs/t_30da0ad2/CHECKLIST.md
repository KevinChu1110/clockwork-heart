# 全面回歸驗收證明 · 鐵匠鐵屑拆解快捷與背包機芯校準快捷雙分支合進主線 (t_30da0ad2)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩項重要養成跳轉閉環分支：
1. **`forge-scrap-shortcut`（t_2e0eeb9f）**：分支 `origin/agent/20261012-forge-scrap-shortcut-t_2e0eeb9f`
   - ForgeDialog 天宮鐵匠機芯五槽部位面板頂部新增『鐵屑持有膠囊』（IronScrapCapsule 與 IronScrapLabel）
   - 即時讀取玩家持有鐵屑與校準消耗，鐵屑充足時顯示「鐵屑：XX（每次消耗 5）」
   - 鐵屑不足（< 5）時呈現珊瑚粉警告色階，顯現『前往拆解』薄荷綠立體果凍按鈕（BtnGoDismantle，高 48px，字級 16px，零 Emoji）
   - 點擊按鈕發出 `dismantle_requested` 信號，大廳 MobileLobby 連動關閉鐵匠並直通開啟 MapleInventory 背包且自動切換至機芯分類 Chip ('core')
2. **`inventory-core-calibrate-shortcut`（t_a9ea5a87）**：分支 `origin/agent/20261012-maple-inventory-calibrate-shortcut-t_a9ea5a87`
   - MapleInventory 探索背包機芯部件詳情面板底部新增『前往校準』金黃立體果凍按鈕（BtnGoCalibrate，高 52px >= 48px，字級 18px >= 16px，零 Emoji）
   - 選取已裝備且剩餘校準次數 > 0 之機芯時按鈕高亮可用；未裝備或校準次數已達上限時正確置灰禁用
   - 點擊按鈕發射 `calibrate_requested` 信號，連動關閉探索背包並直通開啟天宮鐵匠 ForgeDialog

由工程師阿宏（`sideworker`）在 `main` 主線執行雙分支無衝突乾淨整併（Merge commits: `ce18daaad`, `2f86b109e`），執行全站無頭冒煙測試、單元測試、forge / inventory / core 全套回歸測試、公開官網 live 檢測與素材檢查，並透過 `/root/project_status.py` 同步將兩項目更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **鐵匠鐵屑拆解單元測試** | `godot --path game --headless -s scripts/ui/test_forge_dialog_scrap_shortcut.gd` | `TEST_FORGE_DIALOG_SCRAP_SHORTCUT_OK`，按鈕規格、充足/不足切換、信號連動、六語系全綠 | **PASS** |
| **背包機芯校準單元測試** | `godot --path game --headless -s scripts/ui/test_maple_inventory_calibrate_shortcut.gd` | `MAPLE_INVENTORY_CALIBRATE_SHORTCUT_OK`，9 階段驗證（按鈕規格、裝備防護、上限防護、信號連動、六語系、截圖雜湊互異）全綠 | **PASS** |
| **鐵匠系統回歸測試** | `TEST_FILTER=forge ./tools/run_tests.sh` | 10/10 PASS（全部通過） | **PASS** |
| **探索背包回歸測試** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 17/17 PASS（全部通過） | **PASS** |
| **機芯系統回歸測試** | `TEST_FILTER=core ./tools/run_tests.sh` | 17/17 PASS（全部通過） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表 (proofs/t_30da0ad2/)
所有截圖皆以真實 OpenGL3 渲染驅動於 1280×720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，15 張 SHA256 各自獨立：

### A. ForgeDialog 鐵屑膠囊與前往拆解快捷（6 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `forge_scrap_01_sufficient_capsule_zh_TW.png` | 鐵屑充足 (scrap=24) 膠囊米黃底色「鐵屑：24（每次消耗 5）」，前往拆解按鈕安全隱藏 | 1280×720 | `4638ee285545f8555282505f776dd9b85556952507acbd694957c851eb9958d7` |
| `forge_scrap_02_insufficient_warning_dismantle_btn_zh_TW.png` | 鐵屑不足 (scrap=2) 珊瑚粉警告色階「鐵屑：2（每次消耗 5）」，顯現『前往拆解』薄荷綠果凍按鈕 | 1280×720 | `386831f9ce968974c74ab92129c56e5b6e8bd7dd6d5a13d2553dc0ef0aa00552` |
| `forge_scrap_03_click_dismantle_opens_maple_inventory_chip_zh_TW.png` | 點擊『前往拆解』直通連動開啟 MapleInventory 背包並切換至機芯分類 Chip ('core') | 1280×720 | `56718ea830acf6fc741707f93d78e1f5d2b9232882650b714281341299210c4f` |
| `forge_scrap_04_en.png` | 英文語系 (en) Iron Scrap: 2 (Cost 5) 與 Dismantle 按鈕，零 CJK 殘留 | 1280×720 | `02da3a67be6c8b9f8c71cba738f0c5bb055bf0013e89b154c4b479df6ea4f702` |
| `forge_scrap_05_ja.png` | 日文語系 (ja) 鉄くず：2（消費 5）與 分解へ 按鈕 | 1280×720 | `677f9f2354c2019e218fa8f6efb51d0127c11d1e3a6e12d13c9d6c99bff75c8e` |
| `forge_scrap_06_ko.png` | 韓文語系 (ko) 고철: 2 (소모 5) 與 분해하러 가기 按鈕 | 1280×720 | `5e7a2246b7cc560c40246c9b6f0c7089ac176094e0d37806955845840d62bf11` |

### B. MapleInventory 機芯詳情前往校準快捷（9 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `inv_calibrate_01_core_equipped_calibratable_zh_tw.png` | 選取已裝備且剩餘校準次數>0之機芯，BtnGoCalibrate 金黃立體果凍按鈕高亮可用 | 1280×720 | `a668a08a75545dd07404a3e3483a3ec5e999dae7733f42611d92da12e05cd988` |
| `inv_calibrate_02_core_unequipped_disabled.png` | 選取未裝備機芯部件，BtnGoCalibrate 正確置灰禁用 (disabled=true) 防誤操作 | 1280×720 | `1eb902a11337a453f2e2b6adabe2348615e89caeca2bc2b892a2eca40b9e52fb` |
| `inv_calibrate_03_core_maxed_disabled.png` | 選取已裝備但校準次數已滿上限之機芯，按鈕置灰禁用 (disabled=true) | 1280×720 | `737d7ce26457f96b195bdcfeb70b49901f0ddfdacb12bb277376c84079a0c387` |
| `inv_calibrate_04_forge_dialog_opened.png` | 點擊『前往校準』發射信號，背包關閉且直通開啟天宮鐵匠 ForgeDialog | 1280×720 | `4374da41c38ad939a2e911f69c4c8a9b071cabe302548dc879fa9d75f569a828` |
| `inv_calibrate_05_zh_CN.png` | 簡體中文語系 (zh_CN) 前往校准 按鈕展示 | 1280×720 | `466873715fafe8985526483317f29e1254c30d9bb407d3f1283606144af78754` |
| `inv_calibrate_06_en.png` | 英文語系 (en) Calibrate 按鈕展示，零 CJK 殘留 | 1280×720 | `61e87f5d5b7e1cc06e14a17b238f52546c39d7b20b8a714eeab27b2f5c6bcbec` |
| `inv_calibrate_07_ja.png` | 日文語系 (ja) 較正へ 按鈕展示 | 1280×720 | `d3710e4e317636b2c3793f5db8e3149576b05bd1273eca6506b285082334178a` |
| `inv_calibrate_08_ko.png` | 韓文語系 (ko) 교정하러 가기 按鈕展示 | 1280×720 | `61c82b4d81c6e9819909620b47b36ee23dbd45b2d09f35d90405ce788795428b` |
| `inv_calibrate_09_es.png` | 西班牙文語系 (es) Calibrar 按鈕展示，零 CJK 殘留 | 1280×720 | `f0f9e0e37e6cf97cf721abc31a49670ebf6c40e8e971dabea7555655963b8024` |

---

## 4. 規範查核與審驗結論
- [x] **雙分支乾淨合入 main**：Merge commits `ce18daaad` 與 `2f86b109e`，無任何未解衝突。
- [x] **零系統原生 Emoji**：全面遵循規範，清除系統 emoji，採用粉圓體與質感多巴胺立體果凍厚底按鈕。
- [x] **手遊人因工程與按鈕熱區**：
  - 前往拆解按鈕高度 48px >= 48px，字級 16px >= 16px。
  - 前往校準按鈕高度 52px >= 48px，字級 18px >= 16px。
- [x] **安全防護機制完整**：鐵屑充足安全隱藏、未裝備與已達上限置灰防呆。
- [x] **六語系在地化切換**：zh_TW, zh_CN, en, ja, ko, es 完整對齊，歐美語系零 CJK 殘留。
- [x] **專案進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `forge-scrap-shortcut` 與 `inventory-core-calibrate-shortcut` 標記為『已上線』。
