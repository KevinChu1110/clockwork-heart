# 驗收清單：大廳角色頁五大機芯槽位點擊更換支援 CoreReplaceDialog 比較確認彈窗連動 (t_f800a6fa)

## 1. 任務核心驗收標準對齊
- [x] **大廳角色頁五大機芯槽位顯示與熱區**：
  - 在 `mobile_lobby.gd` 的角色頁（`_char_layer`, `Tab.CHARACTER`）增加「機芯五槽配置」橫向列（`CoreSlotsRow`）。
  - 五大槽位（`mainspring`, `chassis`, `escapement`, `gear_train`, `soul_core`）對齊 `SpriteDB.CORE_SLOT_DEFS` 與既有規格。
  - 每個槽位均具備獨立 `SlotButton`，點擊熱區寬高 >= 48px（實測 88x50px），高對比圓角果凍厚底樣式。
  - 零系統 Emoji，使用官方粉圓體與高對比深藍紫描邊。
- [x] **CoreReplaceDialog 比較確認彈窗連動**：
  - 點擊角色頁機芯槽位或背包未裝備機芯卡片，連動彈出多巴胺風格 `CoreReplaceDialog`（`CompareLayer`）。
  - 顯示當前槽位已裝備機芯與預計替換機芯的屬性對比（攻/防/血/色階/階級）。
  - 彈窗尺寸嚴格符合 740~760px（740x440），右上關閉按鈕（52x52 >= 48px），操作按鈕（`BtnCancelReplace`, `BtnConfirmReplace` 寬高 210x52 >= 48px）。
- [x] **取消替換行為**：
  - 點擊「取消替換」或右上「✕」：彈窗關閉，GameState.core_slots 與 CoreSystem 槽位保持原樣，新部件留在背包中。
- [x] **確認替換行為與即時刷新**：
  - 點擊「確認替換」：更新 GameState.core_slots 與 CoreSystem，舊件退回背包、新件裝上槽位。
  - 發出 `core_replaced(norm_slot, target_new_part)` 訊號。
  - 觸發 Toast 提示：`已成功替換裝備至【%s】槽位！`。
  - 即時刷新大廳戰力（`_power_label`, `_char_power_badge`）與五大機芯槽外觀（色階即時更新為對應色票與階級文字）。
- [x] **清除 5347 行等 13px 以下小字**：
  - 5347 行 `ActionLabel`（更換裝備）由 12px 改為 14px 加粗，深藍紫描邊（`COLOR_BORDER` outline_size=2）。
  - 角色頁相關標籤（`_char_weapon_sub_label`, `_weapon_slot_hint_label`, `_char_power_badge`, `_char_level_badge`, 屬性卡）全面改為 14~16px 加粗，深藍紫描邊，達成零 13px 以下小字。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 即時切換，語言切換無時序競爭與文字重疊。
  - en、es 下 100% 零中文 CJK 殘留（經 Vision 模型複檢驗證通過）。
  - ja 下色階正確使用青階，無藍字。

---

## 2. 測試與驗證結果
- **單元測試**：
  - `TEST_FILTER=test_lobby_core_replace_dialog ./tools/run_tests.sh`：1/1 PASS（100% 全綠）
  - `TEST_FILTER=test_lobby_bag_core_list ./tools/run_tests.sh`：1/1 PASS（既有背包機芯測試相容通過）
  - `TEST_FILTER=test_equip_core_replace ./tools/run_tests.sh`：1/1 PASS（既有整備替換測試相容通過）
  - `TEST_FILTER=test_core_replace_compare ./tools/run_tests.sh`：1/1 PASS（既有勝利替換測試相容通過）
  - `TEST_FILTER=test_mobile_lobby ./tools/run_tests.sh`：1/1 PASS（大廳全套功能測試通過）
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f800a6fa/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_f800a6fa/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_char_core_slots_zh_TW.png` | 繁中大廳角色頁五大機芯槽位（CoreSlotsRow），字級 >= 14px，熱區 >= 48px | `7b3093ab9be20054311fcf4b3e2b94c256f92f069e4a372eccd81510aa692b49` |
| `proof_02_core_replace_dialog_zh_TW.png` | 繁中 CoreReplaceDialog 比較確認彈窗（白階 vs 金階，攻防血對比） | `c6e8f8c6e499257e821810186600881c8a9a2ba70436f1ebbeb466b14ec1701f` |
| `proof_03_core_replaced_combat_power_refreshed_zh_TW.png` | 確認替換後大廳槽位刷新為金階、戰力更新為 42、頂部 Toast 提示呈現 | `b89b3a631ac08839837eacf7528f23cb2eaefe3d2bf5434c476163c292a12329` |
| `proof_04_char_core_slots_en.png` | 英文大廳角色頁五大機芯槽位（5 Core Slots Configuration，零中文殘留） | `21af7b33e9e80a70c0e14a016c6dd2e60440a6c59f65a96bc5a7e137939fb221` |
| `proof_05_core_replace_dialog_en.png` | 英文 CoreReplaceDialog 比較確認彈窗（零中文殘留，高對比按鈕） | `21259e715ee4c9bf634170a4526e99610204a7a17e46fcfc6a3f5fbe5e4c6242` |
| `proof_06_core_replace_dialog_ja.png` | 日文 CoreReplaceDialog 比較確認彈窗（日文在地化正常，零中文殘留） | `91685a24cb525cae217655a030a7cdcc71812b626b32a94844b0447a7e19d2c3` |
| `proof_07_core_bag_action_label_14px.png` | 背包機芯卡片 5347 行 ActionLabel 更換裝備為 14px 加粗，深藍紫描邊 | `17b5d1d32f13517ac2beb9cb656fcfda432b2daa549bbdbf9e7ad355afafed49` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含槽位列、比較彈窗、確認後戰力與外觀刷新、背包卡片，各圖 SHA256 皆不同。
- [x] **單元測試穩定防 flaky**：等待幀數充足（15~25 幀），無時序競爭，無頭測試 `1/1 PASS`。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：`CompareLayer` z-index 設為 95，`Toast` z-index 設為 100，彈窗與提示層次分明無穿透。
- [x] **互動元件佈局尺寸與熱區**：槽位卡片按鈕 88x50px、彈窗按鈕 210x52px，全部符合手遊規範（>= 48px）。
- [x] **字級規範**：清除 5347 行等 13px 以下小字，全數改為 14~16px 加粗，深藍紫描邊。
- [x] **零系統 Emoji**：介面全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：五大槽位名稱與八色階名稱嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `lobby-core-replace-compare` 標記為測試中。
