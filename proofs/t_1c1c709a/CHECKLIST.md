# 驗收清單：大廳聚魂殿堂新增『一鍵卸下』全部戰魂果凍按鈕與連動安全防護 (t_1c1c709a)

## 1. 任務核心驗收標準對齊
- [x] **大廳聚魂殿堂『一鍵卸下』立體果凍按鈕 (BtnUnequipAllSouls)**：
  - 在 `mobile_lobby.gd` 的聚魂殿堂（`Tab.SOUL_HALL`）底部操作欄中新增立體果凍按鈕（`BtnUnequipAllSouls`）。
  - 熱區尺寸嚴格符合手機端人體工學（`custom_minimum_size = Vector2(160, 52)`，高度 52px >= 50px，熱區 >= 48px）。
  - 配色採《塔塔冒險隊》多巴胺亮色盤珊瑚粉厚底果凍風格（`COLOR_PINK` `#FF5E8A`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A` 2px、底部立體厚底 5px、圓角 18px、陰影 6px），字體使用開源粉圓體（Open Huninn 16px，深藍紫加粗文字），零系統 Emoji。
  - 同步增設『一鍵配置』按鈕（`BtnAutoEquipSouls`，天藍 `#38A0FF`，160x52px），達成完整一鍵配置與一鍵卸下雙向操作體驗。
- [x] **串接 SoulSystem.unequip_all_souls() 安全卸回背包**：
  - 點擊按鈕安全卸下所有魂槽戰魂並返還背包，同步更新 `GameState.soul_slots` 與 `GameState.souls`（`equipped = false`）。
  - 即時發出 `souls_unequipped` 信號，並保存遊戲狀態。
- [x] **空槽防呆安全防護與 Toast 提示**：
  - 若所有魂槽本來就為空，安全攔截並彈出防呆飄字：「未裝備任何戰魂」，不執行無效寫入，回傳 `changed = false`。
  - 成功卸下戰魂時彈出飄字：「已卸下所有戰魂」。
- [x] **即時刷新聚魂殿堂 BBCode 狀態與戰力屬性**：
  - 聚魂殿堂內新增 `SoulStatusBBCode` 富文字狀態面板（`RichTextLabel`，支援 BBCode），卸下後即時同步 `SoulSystem.panel_status_bbcode()`。
  - 槽位即時顯示為「空」，入魂戰力加成正確歸零，同步調用 `refresh_hud()` 與 `_refresh_char_tab_stats()`。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六語系即時切換，按鈕與提示文字零 hardcode。
  - 按鈕文字對應：zh_TW="一鍵卸下", zh_CN="一键卸下", en="Quick Unsocket", ja="一括解除", ko="일괄 해제", es="Desengarzar Todo"。
  - 成功飄字與防呆飄字六語系皆已登錄於 `game/data/i18n/{code}.json` 與 `game/data/i18n/content/{code}/ui.json`，en、ja、ko、es 下無中文殘留，零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬單元與整合測試**：
  - `godot --path game --headless -s res://scripts/ui/test_soul_hall_unequip_all.gd`：PASS（`TEST_SOUL_HALL_UNEQUIP_ALL_OK`，exit code 0，0 SCRIPT ERROR）。
- **聚魂系統相關回歸測試**：
  - `TEST_FILTER=soul ./tools/run_tests.sh`：9/9 PASS（`test_soul_draw_v2`, `test_soul_system`, `test_maple_inventory_soul_shortcut`, `test_power_stat_soul_shortcut`, `test_soul_draw_clean_compliance`, `test_soul_draw_i18n`, `test_soul_hall_inventory_shortcut`, `test_soul_hall_unequip_all`, `test_town_soul_auto_equip`）。
- **無頭冒煙測試**：
  - `godot --path game --headless --quit-after 5`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_1c1c709a/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_empty_safeguard_zh_TW.png` | 空槽狀態點擊一鍵卸下，觸發安全防呆判定 | `a9eb2c8d14da8b252cd9a5958b19f766dcefc5020330d8de0b58de8369558da0` |
| `proof_02_slots_equipped_zh_TW.png` | 滿槽戰魂裝備狀態，BBCode 面板顯示三槽滿載與戰力屬性加成 | `d992e01a203d385854a4239eb9e7e2160b411fa1170fe5f058f93670a3c1a58f` |
| `proof_03_unequip_success_toast_zh_TW.png` | 點擊一鍵卸下後戰魂全數歸還背包，BBCode 面板顯示槽位全空 | `fdf6030dd38452f6f18218a3a85ce45ab78e3db82c251a25092e2c33190505ed` |
| `proof_04_auto_equip_best_zh_TW.png` | 點擊一鍵配置，自動挑選最佳戰魂入槽填滿 | `4401193265e7e4d0fe27866053b0dab9aac971b84c0f1ccd21a2b6ee87f77ffa` |
| `proof_05_locale_en.png` | 英文語系 Quick Unsocket 按鈕與聚魂殿堂介面展示 | `ab3ebb3290ac8b137ebaca80f30aaf05a9be90bd3f55530f5d8d97b25c9a92eb` |
| `proof_06_locale_ja.png` | 日文語系 一括解除 按鈕與聚魂殿堂介面展示 | `0e72d54a1f37160bf39ba4f87d09fbb792a5c0aa17e19ae39f8b5c35197bcb27` |
| `proof_07_locale_ko.png` | 韓文語系 일괄 해제 按鈕與聚魂殿堂介面展示 | `87ef4b3b94ee6b12805dc58f2ce9c7937c757559025f9c8c7a510de8bea891bb` |
| `proof_08_locale_es.png` | 西班牙文語系 Desengarzar Todo 按鈕與聚魂殿堂介面展示 | `21bc93969c44cad0b5c8762303f80ef464ff2f3acd44532c1851a10d4e0baedd` |
| `proof_09_locale_zh_CN.png` | 簡體中文語系 一键卸下 按鈕與聚魂殿堂介面展示 | `fcfe2e4918b26e3e87f2ba278244dea3cca4ae23689c27648139369083f2ac79` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文、韓文、西文、簡中各情境截圖齊全，包含空槽防呆、滿槽配置、卸下歸還背包、雙向一鍵配置，9 張 SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（5~6 幀），無時序競爭，無頭測試 `TEST_SOUL_HALL_UNEQUIP_ALL_OK` 100% 通過。
- [x] **UI 排版邊界與圖層順序**：按鈕置於底欄 HBox，高度 52px，橫向間隔 14px，無重疊或超出框線。
- [x] **互動元件佈局尺寸與熱區**：`BtnUnequipAllSouls` 尺寸設為 160x52px，高度 >= 50px，熱區符合手遊規範（>= 48px）。
- [x] **字級規範**：字體大小 16px 開源粉圓體，深藍紫描邊，零系統 Emoji。
- [x] **名稱與用詞規範**：戰魂槽位名稱與四大共鳴核心詞彙嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `soul-hall-unequip-all` 標記為測試中。
