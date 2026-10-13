# 驗收清單：GemWorkshopDialog 手藝工坊新增『前往背包』快捷按鈕連動探索背包寶石頁籤 (t_3693a5bb)

## 1. 任務核心驗收標準對齊
- [x] **GemWorkshopDialog 底部按鈕列新增『前往背包』立體果凍按鈕 (BtnGoInventory)**：
  - 在 `game/scripts/ui/gem_workshop_dialog.gd` 底部操作列 `foot_row` 新增『前往背包』果凍按鈕（`BtnGoInventory`）。
  - 熱區尺寸嚴格符合手機端人體工學規範（`custom_minimum_size = Vector2(170, 50)`，高度 >= 48px，熱區 >= 48px）。
  - 配色採多巴胺天藍色立體果凍厚底風格（`COLOR_SKY` `#38A0FF`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A`、底部立體厚底 5px、圓角 18px、陰影 6px），文字為白色粉圓體（18px >= 16px）加深色厚描邊 4px，零系統 Emoji。
- [x] **信號發射與雙向跳轉閉環連動**：
  - 宣告並提供 `signal inventory_requested()` 信號。
  - 提供 `get_go_inventory_button() -> Button` 按鈕存取器。
  - 點擊按鈕後發射 `inventory_requested` 信號，並調用 `MobileLobby.open_maple_inventory("gem")`，連動關閉工坊彈窗且開啟探索背包 `MapleInventory`。
  - `MapleInventory` 自動切換至『寶石』分類 Chip（cid: 'gem'），展示所有寶石道具與庫存容量狀態。
  - 背包點擊前往工坊快捷按鈕即可返回工坊，形成「工坊合成/鑲嵌 → 前往背包檢視所有素材與庫存」的雙向跳轉閉環。
- [x] **雙分頁操作一致性**：
  - 手藝工坊「寶石熔煉與合成」分頁（Tab.SMELT）與「寶石櫃盤點檢視」分頁（Tab.CASE_INSPECT）下，底部『前往背包』快捷按鈕均常駐可見且正常點擊。
- [x] **六語系即時在地化切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六大語系即時切換與即時刷新。
  - 各語系按鈕文字精確對齊：
    - `zh_TW`: "前往背包"
    - `zh_CN`: "前往背包"
    - `en`: "Go to Inventory" (零 CJK)
    - `ja`: "インベントリへ進む"
    - `ko`: "인벤토리로 이동"
    - `es`: "Ir al Inventario" (零 CJK)
  - 歐美語系 (en, es) 零 CJK 漢字殘留，全語系零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=test_gem_workshop_go_inventory ./tools/run_tests.sh`：1/1 PASS（100% 全綠，`TEST_GEM_WORKSHOP_GO_INVENTORY_OK`，exit code 0）。
  - 覆蓋點：按鈕熱區與尺寸規格、立體厚底與大圓角、信號發射與存取器、雙分頁可見性、六語系即時切換與零 CJK/零 Emoji、MobileLobby 雙向平滑切換閉環。
- **工坊與背包快捷全套測試**：
  - `TEST_FILTER=workshop ./tools/run_tests.sh`：5/5 PASS（全數通過，無任何回歸破壞）。
    - `test_bag_workshop_shortcut`: PASS
    - `test_forge_workshop_shortcut`: PASS
    - `test_gem_workshop`: PASS
    - `test_gem_workshop_go_inventory`: PASS
    - `test_gem_workshop_i18n`: PASS
- **無頭冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3693a5bb/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_3693a5bb/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_gem_workshop_smelt_tab_zh_TW.png` | 繁中手藝工坊熔煉分頁，展示『前往背包』天藍色立體果凍按鈕（170x50px） | `836c4ed11a53da91765828cdc150077e410dd6ad163f7bc6db88e521b3a538ec` |
| `proof_02_gem_workshop_case_tab_zh_TW.png` | 繁中手藝工坊寶石櫃分頁，孔位卡、六維加成面板、15 格盤點小卡與『前往背包』按鈕 | `60c3204fc7dcf190a74298f47d1d19fa7aa339adbb1c1f1059263383ce9cb326` |
| `proof_03_click_go_inventory_opens_maple_inventory_gem_chip_zh_TW.png` | 點擊『前往背包』後連動開啟 MapleInventory 並自動切換至『寶石』分類 Chip (cid: 'gem')，展示寶石道具與容量狀態 | `3a7e1d8bc29510400a666866e8029e83cc3be429e4c1350bef7eb8cc197b0501` |
| `proof_04_gem_workshop_en.png` | 英文語系 (en) Go to Inventory 按鈕與介面，零 CJK 殘留 | `45025e8109f6be5fe89d9b6fb4c75fe5944dc121ff5a8d7357da81a6072abb8f` |
| `proof_05_gem_workshop_ja.png` | 日文語系 (ja) インベントリへ進む 按鈕與介面 | `928c28a8a4c28af971e6c73bdf8426b2fa3bd03540852ff6e0724c64fb6a4303` |
| `proof_06_gem_workshop_ko.png` | 韓文語系 (ko) 인벤토리로 이동 按鈕與介面 | `d142c3666796ff390367852fb538f92b734baea14a6f011ef8c10f4e1fe3a76b` |
| `proof_07_gem_workshop_es.png` | 西班牙文語系 (es) Ir al Inventario 按鈕與介面，零 CJK 殘留 | `a3a3f3e7fefe5b8b8a84f47002ac5251a25dce67b84a3ef583da060825206b6e` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中熔煉頁、寶石櫃頁、連動背包寶石頁籤、英/日/韓/西語系切換截圖齊全，包含正確按鈕、高亮 Chip、道具狀態，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（25~35 幀），無時序競爭，無頭測試 `1/1 PASS`。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：按鈕位於彈窗底部 `foot_row`，三顆按鈕總寬 542px，完美納入 710px 內容區，無穿透無溢出。
- [x] **互動元件佈局尺寸與熱區**：`BtnGoInventory` 尺寸設為 170x50px，熱區符合手遊防誤觸規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 18px 加粗，深藍紫描邊 4px，達成零小字（>= 16px）。
- [x] **零系統 Emoji**：按鈕全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：各語系名稱嚴格對齊既有定義，無任何淘汰用詞。
