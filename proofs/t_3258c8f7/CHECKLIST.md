# 《發條之心》手藝工坊 GemWorkshopDialog 寶石櫃新增『一鍵鑲嵌』果凍按鈕連動 GemSystem 查驗清單與驗收報告 (t_3258c8f7)

- **審查卡號**：`t_3258c8f7`
- **對應模組**：`GemWorkshopDialog` (`game/scripts/ui/gem_workshop_dialog.gd`)、`GemSystem` (`game/scripts/systems/gem_system.gd`)
- **審查標準**：完全遵循多巴胺鮮亮高飽和色盤、手遊人體工學規範、0-QA5 / 0-QA26 / 0-QA28（六語系無缺詞、零Emoji、真實 OpenGL3 Framebuffer 截圖存證）

---

## 1. 核心驗收標準對齊

| 項目 | 規範標準 | 實作情況 | 驗收結果 |
|---|---|---|---|
| **一鍵鑲嵌立體果凍按鈕** | 位於寶石櫃檢視分頁（`Tab.CASE_INSPECT`）標題列或頂部加成列，尺寸 >= 120x48px，熱區 >= 48px，薄荷綠果凍厚底 5px，深藍紫描邊 2px，圓角 16px，零Emoji | `BtnAutoSocket`：`custom_minimum_size = Vector2(130, 50)`，薄荷綠立體果凍厚底 5px（`COLOR_MINT` #4ED86A）、圓角 16px、深藍紫描邊 2px（`COLOR_BORDER` #1F1A3A）、字級 16px 粉圓體，零 Emoji | **合格 (PASS)** |
| **連動 GemSystem.auto_socket()** | 點擊後呼叫 `GemSystem.auto_socket()`，自動將庫存最高級寶石填入全身裝備空孔，絕不覆蓋已鑲嵌寶石 | 點擊 `BtnAutoSocket` 觸發 `_on_auto_socket_pressed()`，呼叫 `GemSystem.auto_socket()`，依高階優先與部位相性自動鑲嵌空孔 | **合格 (PASS)** |
| **原地即時刷新孔位與六維面板** | 原地刷新孔位卡片、六維加成面板與寶石庫存網格，並提示訊息 | 自動呼叫 `_refresh_case_view()` 原地重建孔位卡片（更新為已鑲嵌狀態）、重算全身六維總加成（暴擊、攻擊%、命中、生命%、防禦%、迴避），並更新 15 格庫存網格與 `MsgLabel` | **合格 (PASS)** |
| **六語系即時在地化切換** | 支援 zh_TW, zh_CN, en, ja, ko, es 六語系即時切換，粉圓體字級 >= 16px，無缺詞，歐美語系零 CJK 殘留 | 六語系精確對齊：繁中「一鍵鑲嵌」、簡中「一键镶嵌」、英文「Quick Socket」、日文「一括装着」、韓文「일괄 장착」、西文「Engarzar Todo」，切換即時生效且零 CJK 殘留 | **合格 (PASS)** |
| **防呆回饋機制** | 全孔位已滿或無可用寶石時提供精準且友善的提示 | 全孔位已填滿時提示「目前穿戴裝備皆已鑲嵌寶石，無閒置空孔。」；背包無寶石提示「背包沒有可鑲嵌的寶石。」 | **合格 (PASS)** |
| **無頭單元測試與回歸測試** | 附專屬無頭單元測試腳本，既有測試無回歸破壞 | `test_gem_workshop_auto_socket.gd` (PASS)、`test_gem_workshop.gd` (PASS)、`test_gem_workshop_i18n.gd` (PASS)、`test_gem_system.gd` (PASS)、`test_gem_auto_fuse.gd` (PASS) | **合格 (PASS)** |

---

## 2. 實機 Framebuffer 截圖存證清單 (OpenGL3, 1280x720)

所有截圖皆為 OpenGL3 渲染驅動於 1280x720 下真實 Framebuffer 輸出，經 SHA256 驗證彼此獨立無重複：

| 編號 | 檔案名稱 | 截圖內容說明 | 破圖檢核 | Emoji檢核 | 截字檢核 | SHA256 前綴 | 狀態 |
|---|---|---|---|---|---|---|---|
| 01 | `proof_01_gem_workshop_case_tab_zh_TW.png` | 繁中 (zh_TW) 寶石櫃檢視分頁：薄荷綠果凍『一鍵鑲嵌』按鈕（`BtnAutoSocket`，130x50px）、孔位卡片（未鑲嵌狀態）、六維加成面板與 15 格盤點網格 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `12878443063a` | 合格 (PASS) |
| 02 | `proof_02_click_auto_socket_success.png` | 點擊『一鍵鑲嵌』後，武器自動鑲入黃2、防具鑲入紅1，六維加成面板即時提升，`MsgLabel` 顯示綠色成功提示 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `defea441f6ff` | 合格 (PASS) |
| 03 | `proof_03_auto_socket_full_feedback.png` | 全身孔位填滿後再次點擊一鍵鑲嵌，`MsgLabel` 顯示橘色防呆提示「目前穿戴裝備皆已鑲嵌寶石，無閒置空孔。」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `52b63625f803` | 合格 (PASS) |
| 04 | `proof_04_gem_workshop_auto_socket_zh_CN.png` | 簡體中文語系 (zh_CN) 下 `BtnAutoSocket` 顯示「一键镶嵌」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `799a55ac4cb9` | 合格 (PASS) |
| 05 | `proof_05_gem_workshop_auto_socket_en.png` | 英文語系 (en) 下 `BtnAutoSocket` 顯示「Quick Socket」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `52c05ce01be4` | 合格 (PASS) |
| 06 | `proof_06_gem_workshop_auto_socket_ja.png` | 日文語系 (ja) 下 `BtnAutoSocket` 顯示「一括装着」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `c1fb3b26d18f` | 合格 (PASS) |
| 07 | `proof_07_gem_workshop_auto_socket_ko.png` | 韓文語系 (ko) 下 `BtnAutoSocket` 顯示「일괄 장착」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `1cc84197b134` | 合格 (PASS) |
| 08 | `proof_08_gem_workshop_auto_socket_es.png` | 西班牙文語系 (es) 下 `BtnAutoSocket` 顯示「Engarzar Todo」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `0294fca24a21` | 合格 (PASS) |

---

## 3. 常見退回自查核對 (clock-review-checklist.md)

- [x] **截圖存證對齊驗收項目與完整互動過程**：截圖涵蓋初始寶石櫃、點擊一鍵鑲嵌成功填入寶石、六維數值原地提升、全滿防呆提示、六語系即時切換，所有 8 張截圖 SHA256 獨立唯一。
- [x] **單元測試防 flaky**：專屬測試 `test_gem_workshop_auto_socket.gd` 充分等待節點就緒（15~30 幀），斷言涵蓋按鈕尺寸、字級、數值刷新、防呆分支與六語系，`TEST_GEM_WORKSHOP_AUTO_SOCKET_OK` (PASS)。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：`BtnAutoSocket` 整合於寶石櫃盤點標題列，彈窗符合 750x580 橫屏規範，全螢幕 Scrim 正常發揮，零穿透重疊。
- [x] **互動元件佈局尺寸與熱區**：`BtnAutoSocket` custom_minimum_size = (130, 50)，點擊熱區符合手遊規範 (>= 48px)。
- [x] **字級規範**：按鈕字體大小 16px 粉圓體，深藍紫描邊 4px，全彈窗零 13px 以下小字。
- [x] **零系統 Emoji**：按鈕、提示全域無 Unicode 系統 Emoji。
- [x] **全站零退化與回歸測試**：既有寶石工坊與寶石系統相關單元測試全數跑綠。
