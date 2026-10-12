# 驗收清單：大廳角色頁五大機芯槽位支援一鍵配置最高戰力機芯與即時屬性刷新 (t_791dc011)

## 1. 任務核心驗收標準對齊
- [x] **大廳角色頁一鍵配置果凍按鈕 (BtnCoreAutoEquip)**：
  - 在 `mobile_lobby.gd` 的角色頁（`Tab.CHARACTER`）機芯五槽標題列（`c_hdr`）新增「一鍵配置」果凍按鈕（`BtnCoreAutoEquip`）。
  - 熱區尺寸嚴格符合手機端人體工學（`custom_minimum_size = Vector2(104, 48)`，熱區 >= 48px）。
  - 配色採《塔塔冒險隊》薄荷綠果凍厚底風格（`COLOR_MINT` `#4ED86A`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A`、底部立體厚底 5px、圓角 16px、陰影 5px），字體使用開源粉圓體（Open Huninn 14px，加粗，深藍紫加深描邊），零系統 Emoji。
- [x] **自動比對背包機芯綜合戰力與一鍵配置邏輯**：
  - 在 `core_system.gd` 實作 `calculate_part_power(part)`：考量各部位實質攻防血（血量折算）、暴擊（x2.0）、爆傷（x1.0）、校準評分與色階權重，精確計算機芯綜合戰力。
  - 在 `core_system.gd` 實作 `auto_equip_best_cores()`：五大槽位（`mainspring`, `chassis`, `escapement`, `gear_train`, `soul_core`）獨立比對背包中對應槽位機芯。
  - 空槽自動換上背包內最高戰力機芯；已有裝備槽位若背包中有更高戰力機芯，自動替換。
  - 卸下舊機芯安全退回背包，裝備新機芯自背包扣除，並同步寫入 `GameState.core_slots` 與 `CoreSystem.player_parts`。
- [x] **即時數值提升與介面同步刷新**：
  - 成功換裝時發出 `cores_auto_equipped` 訊號，大廳頂部 `refresh_hud()`、角色頁有效戰力膠囊（`_char_power_badge`）與五大機芯槽卡片外觀（`_refresh_char_core_slots`）同步即時更新。
  - 飄字提示戰力提升：彈出「戰力提升 +XX！已一鍵配置最高戰力機芯。」。
- [x] **最佳配置重複點擊判定**：
  - 當所有槽位已是背包內最高戰力時，點擊按鈕不重複異動資料（`changed: false`），彈出「目前已是最佳機芯配置！」飄字提示。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 即時切換，切換語系時按鈕文字即時更新（zh_TW="一鍵配置", en="Auto-Equip", ja="一括装着", ko="일괄 장착", es="Equipamiento rápido"）。
  - en、ja 下無中文殘留，零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=test_lobby_core_auto_equip ./tools/run_tests.sh`：1/1 PASS（100% 全綠，LOBBY_CORE_AUTO_EQUIP_OK，exit code 0）。
  - 覆蓋點：按鈕熱區與規格、空槽與高階機芯比對裝備、戰力大幅提升、舊件退回背包、戰力即時刷新、重複點擊最佳配置判定、六語系即時切換與零 Emoji。
- **既有回歸測試**：
  - `TEST_FILTER=test_lobby_core_replace_dialog ./tools/run_tests.sh`：1/1 PASS（前置核心比較彈窗功能完全相容）。
  - `TEST_FILTER=test_mobile_lobby ./tools/run_tests.sh`：1/1 PASS（大廳完整流程無回歸破壞）。
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_791dc011/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_char_core_slots_before_auto_equip_zh_TW.png` | 繁中角色頁五大機芯槽位（初始白板）與「一鍵配置」薄荷綠果凍按鈕（104x48px） | `0fbb92c50314307a466479627e2e7f5ec1addbf5cee7b20a3ae23984a5b08a46` |
| `proof_02_char_core_auto_equipped_toast_zh_TW.png` | 點擊一鍵配置後換上高階五槽（金/藍/紫/綠/紅），戰力從 30 飆升至 326，上方飄字「戰力提升 +296！已一鍵配置最高戰力機芯。」（觸發後 3 幀完整拍到 Toast） | `88c337143f66978876abe389749ca64cb1b7772a63f29af3174be6d2f3b7aa9a` |
| `proof_03_char_core_auto_equip_already_best_zh_TW.png` | 最佳狀態下再次點擊一鍵配置，上方飄字「目前已是最佳機芯配置！」（觸發後 3 幀完整拍到 Toast） | `f8d027d2a2cfc7552edd19b9303506bf4ed33d1e0e7b3bfc55adcff3614b58df` |
| `proof_04_char_core_auto_equip_en.png` | 英文語系角色頁 Auto-Equip 按鈕與最佳配置飄字 (Already at optimal core configuration!)，零中文殘留（觸發後 3 幀完整拍到 Toast） | `5020e7d0d464568338e843fe5f4b51ff01a9cfff03655e434df824158cd7ac87` |
| `proof_05_char_core_auto_equip_ja.png` | 日文語系角色頁 一括装着 按鈕與最佳配置飄字 (現在は最適なコア配置です！)（觸發後 3 幀完整拍到 Toast） | `44e58d80d11e9cb3e1a52f080323e8c389dea688b59598b49067681f95229e40` |
| `proof_06_btn_auto_equip_min_size_48px.png` | 一鍵配置按鈕規格特寫（尺寸 104x48px，立體厚底 5px，圓角 16px）與五槽金藍紫綠紅完成態 | `48540809b122043aaf820ab0dda7a2a70d4eb13c9ccd7ba71d0c8c489f8197fc` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含配置前白板、配置後換裝飄字、最佳配置提示、語系切換，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（20~25 幀），無時序競爭，無頭測試 `1/1 PASS`。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：按鈕位於 `c_hdr` 標題列右端，彈出之 Toast 設為 z-index=100，層次分明無穿透。
- [x] **互動元件佈局尺寸與熱區**：`BtnCoreAutoEquip` 尺寸設為 104x48px，熱區符合手遊規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 14px 加粗，深藍紫描邊，達成零 13px 以下小字。
- [x] **零系統 Emoji**：按鈕與飄字全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：五大槽位名稱與八色階名稱嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `lobby-core-auto-equip` 標記為測試中。
