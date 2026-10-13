# 全面回歸驗收證明 · 手藝工坊前往背包與戰力總覽前往鍛造雙分支合進主線 (t_169405f8)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之兩項重要養成跳轉閉環分支：
1. **`gem-workshop-go-inventory`（t_3693a5bb）**：分支 `agent/20261012-gem-workshop-go-inventory-t_3693a5bb`（commit `8afb7ccd0`）
   - GemWorkshopDialog 手藝工坊新增『前往背包』天藍色立體果凍按鈕（`BtnGoInventory`，尺寸 170x50px，熱區 >= 48px，字級 18px >= 16px，圓角 18px，厚底 5px，深藍紫描邊 2px，零 Emoji）
   - 熔煉分頁與寶石櫃分頁雙分頁均維持常駐可見，佈局穩固
   - 點擊按鈕發射 `inventory_requested` 信號，大廳 `MobileLobby` 連動關閉工坊並直通開啟 `MapleInventory` 探索背包，且自動切換至寶石分類 Chip（`gem`）
   - 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換無缺漏，歐美語系零 CJK 殘留
2. **`power-stat-weapon-forge-shortcut`（t_7716e1d4）**：分支 `agent/20261012-power-stat-forge-shortcut-t_7716e1d4`（commit `02afd7fd0`）
   - PowerStatDialog 戰力屬性總覽三欄武器卡片標題列新增『前往鍛造』金黃立體果凍按鈕（`BtnGoForge`，尺寸 96x48px，高度 >= 48px，熱區 >= 48px，字級 14px，厚底 5px，零 Emoji）
   - 與寶石卡片『前往工坊』、心法卡片『前往心法』、戰魂卡片『前往聚魂』、機芯卡片『前往校準』形成完整的五大養成直通閉環
   - 點擊按鈕發射 `forge_requested` 與 `closed` 信號，大廳 `MobileLobby` 連動關閉戰力總覽並直通開啟天宮鐵匠 `ForgeDialog`
   - 支援六語系（zh_TW, zh_CN, en, ja, ko, es）即時切換，歐美語系零 CJK 殘留

由工程師阿宏（`sideworker`）在 `main` 主線執行雙分支無衝突乾淨整併（Merge commits: `e5479aaaa`, `b3fbda7af`），執行全套無頭冒煙測試、專屬單元測試、workshop / power_stat / inventory / forge 全套回歸測試、公開官網 live 檢測與素材檢查，並透過 `/root/project_status.py` 同步將兩項目更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **手藝工坊前往背包單元測試** | `godot --path game --headless -s scripts/ui/test_gem_workshop_go_inventory.gd` | `TEST_GEM_WORKSHOP_GO_INVENTORY_OK`，按鈕規格、信號發射、雙分頁可見性、六語系、雙向跳轉閉環全綠 | **PASS** |
| **戰力總覽前往鍛造單元測試** | `godot --path game --headless -s scripts/ui/test_power_stat_weapon_forge_shortcut.gd` | `TEST_POWER_STAT_WEAPON_FORGE_SHORTCUT_OK`，按鈕規格、六語系、信號連動、大廳開啟 ForgeDialog 全綠 | **PASS** |
| **手藝工坊系統回歸測試** | `TEST_FILTER=workshop ./tools/run_tests.sh` | 5/5 PASS（全部通過） | **PASS** |
| **戰力總覽系統回歸測試** | `TEST_FILTER=power_stat ./tools/run_tests.sh` | 6/6 PASS（全部通過） | **PASS** |
| **探索背包系統回歸測試** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 18/18 PASS（全部通過） | **PASS** |
| **天宮鐵匠系統回歸測試** | `TEST_FILTER=forge ./tools/run_tests.sh` | 11/11 PASS（全部通過） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表 (proofs/t_169405f8/)
所有截圖皆以真實 OpenGL3 渲染驅動於 1280×720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，14 張 SHA256 各自獨立：

### A. GemWorkshopDialog 手藝工坊前往背包快捷（7 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_gem_workshop_smelt_tab_zh_TW.png` | 熔煉分頁 (zh_TW)，展示『前往背包』天藍立體果凍按鈕 (BtnGoInventory, 170x50px) | 1280×720 | `836c4ed11a53da91765828cdc150077e410dd6ad163f7bc6db88e521b3a538ec` |
| `proof_02_gem_workshop_case_tab_zh_TW.png` | 寶石櫃分頁 (zh_TW)，孔位卡片、六維加成面板、15 格盤點小卡與『前往背包』按鈕維持可見 | 1280×720 | `60c3204fc7dcf190a74298f47d1d19fa7aa339adbb1c1f1059263383ce9cb326` |
| `proof_03_click_go_inventory_opens_maple_inventory_gem_chip_zh_TW.png` | 點擊『前往背包』直通連動開啟 MapleInventory 背包並自動切換至寶石分類 Chip ('gem') | 1280×720 | `08067b40d62533d0f89587d97030c1395d83cc5cfba39fcc2fcb1f5c6f5de919` |
| `proof_04_gem_workshop_en.png` | 英文語系 (en) Go to Inventory 按鈕與介面展示，零 CJK 殘留 | 1280×720 | `45025e8109f6be5fe89d9b6fb4c75fe5944dc121ff5a8d7357da81a6072abb8f` |
| `proof_05_gem_workshop_ja.png` | 日文語系 (ja) インベントリへ進む 按鈕與介面展示 | 1280×720 | `928c28a8a4c28af971e6c73bdf8426b2fa3bd03540852ff6e0724c64fb6a4303` |
| `proof_06_gem_workshop_ko.png` | 韓文語系 (ko) 인벤토리로 이동 按鈕與介面展示 | 1280×720 | `d142c3666796ff390367852fb538f92b734baea14a6f011ef8c10f4e1fe3a76b` |
| `proof_07_gem_workshop_es.png` | 西班牙文語系 (es) Ir al Inventario 按鈕與介面展示，零 CJK 殘留 | 1280×720 | `a3a3f3e7fefe5b8b8a84f47002ac5251a25dce67b84a3ef583da060825206b6e` |

### B. PowerStatDialog 戰力總覽武器卡片前往鍛造快捷（7 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_power_stat_weapon_forge_shortcut_zh_tw.png` | 繁中 (zh_TW) 戰力總覽武器卡片標題列展示 BtnGoForge 前往鍛造金黃果凍按鈕（96x48px，字級 14px） | 1280×720 | `9dc5352be8e1f173b95ec312ccb2b55d948f4bc0df59bc9a6055badaf9c796d9` |
| `proof_02_power_stat_weapon_forge_shortcut_zh_cn.png` | 簡中 (zh_CN) 戰力總覽武器卡片『前往锻造』按鈕展示 | 1280×720 | `6b26c9812087c6e2fa8ed3eb1cb0ad72b2656419ab1db9b89d79084e7945b7fc` |
| `proof_03_power_stat_weapon_forge_shortcut_en.png` | 英文 (en) 戰力總覽武器卡片『Go to Forge』按鈕展示，零 CJK 殘留 | 1280×720 | `2bf40c262ea85b59e8d1d8378adb84aadfd21a06e091018ac3783881914cf05a` |
| `proof_04_power_stat_weapon_forge_shortcut_ja.png` | 日文 (ja) 戰力總覽武器卡片『鍛造へ進む』按鈕展示 | 1280×720 | `fd8c5bc873d6c62a901b724100225a3050ecb974b924df6d71b00a6eae87393b` |
| `proof_05_power_stat_weapon_forge_shortcut_ko.png` | 韓文 (ko) 戰力總覽武器卡片『단조로 이동』按鈕展示 | 1280×720 | `e7b5fea007ed2d3f2508f53e3da564ca0b498247cb75ba5a9c97e9f26d093df3` |
| `proof_06_power_stat_weapon_forge_shortcut_es.png` | 西文 (es) 戰力總覽武器卡片『Ir a Forja』按鈕展示，零 CJK 殘留 | 1280×720 | `17789bedacf77b552d404966bf838d71daa8d8fb5ea7483471436cec08b7fd09` |
| `proof_07_click_forge_shortcut_opens_forge_dialog.png` | 點擊前往鍛造按鈕後成功連動關閉戰力總覽並直通開啟天宮鐵匠 ForgeDialog 實機畫面 | 1280×720 | `cfae62f84cba38f3b7b157eb4bef13cd86263b453c86b10df5ee5b53f783f93c` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證對齊驗收項目與完整互動過程**：共 14 張真實 OpenGL3 實機截圖，涵蓋手藝工坊前往背包、跳轉 MapleInventory 寶石分類、戰力總覽前往鍛造、跳轉天宮鐵匠 ForgeDialog，及多語系完整切換；14 張 SHA256 各自獨立無重複。
- [x] **單元與回歸測試穩定防 flaky**：專屬測試無頭全綠，四項系統回歸測試 40/40 PASS（workshop 5/5, power_stat 6/6, inventory 18/18, forge 11/11），時序無競爭。
- [x] **UI 排版與邊界規範**：
  - 手藝工坊『前往背包』按鈕為 170x50px，熱區 >= 48px，字級 18px >= 16px，圓角 18px，天藍果凍厚底 5px。
  - 戰力總覽『前往鍛造』按鈕為 96x48px，熱區 >= 48px，字級 14px，圓角 14px，金黃果凍厚底 5px。
  - 全域零系統 Emoji，全面採用粉圓體與高飽和度多巴胺配色。
- [x] **名稱與用詞規範**：各語系鍵值與名詞嚴格對齊既有規範，無舊名詞（霧隱村／今日村莊／白霧村 零殘留）。
- [x] **專案進度同步**：`docs/PROJECTS.json` 透過 `/root/project_status.py` 將 `gem-workshop-go-inventory` 與 `power-stat-weapon-forge-shortcut` 標記為『已上線』。
