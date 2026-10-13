# 驗收清單：大廳角色頁三欄武器槽新增『一鍵卸下』按鈕與安全防護 (t_3c98e3bb)

## 1. 任務核心驗收標準對齊
- [x] **大廳角色頁『一鍵卸下』立體果凍按鈕 (BtnWeaponUnequipAll)**：
  - 在 `mobile_lobby.gd` 的角色頁（`Tab.CHARACTER`）武器輪替配置標題列（`w_hdr`）中，於現有『一鍵配置』按鈕旁新增「一鍵卸下」立體果凍按鈕（`BtnWeaponUnequipAll`）。
  - 熱區尺寸嚴格符合手機端人體工學（`custom_minimum_size = Vector2(104, 48)`，熱區 >= 48px，尺寸 >= 104x48px）。
  - 配色採《塔塔冒險隊》珊瑚粉果凍厚底風格（`COLOR_PINK` `#FF5E8A`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A` 2px、底部立體厚底 5px、圓角 16px、陰影 5px），字體使用開源粉圓體（Open Huninn 16px，深藍紫文字），零系統 Emoji。
- [x] **遍歷武器欄位卸下邏輯與安全防護**：
  - 點擊按鈕遍歷武器欄位，調用 `EquipmentSystem.unequip_loadout_slot()` 將副武器或多餘武器（slot 1, slot 2）卸下歸還背包（`GameState.equip_bag`）。
  - 安全防護：保留初始首選武器（slot 0），避免角色進入空手無武裝狀態。
  - 即時刷新三欄武器卡片（`_refresh_weapon_slot_buttons()`）、大廳頂部數值（`refresh_hud()`）、角色頁有效戰力膠囊（`_char_power_badge`）與戰鬥屬性卡片（`_refresh_char_tab_stats(true)`）。
  - 發出 `weapons_unequipped` 信號，並保存遊戲。
- [x] **全卸下切換至空手拳套防呆**：
  - 若所有武器欄位全數卸下（或主動指定卸下全部），觸發空手防呆機制（`GameState.weapon_name = "空手"`、`GameState.weapon_atk = 0`、`GameState.path_style = "fist"`、`GameState.equip_slots["weapon"] = ""`），紙娃娃與 HUD 零 SCRIPT ERROR，無崩潰現象。
- [x] **飄字反饋**：
  - 成功卸下副武器時彈出飄字：「已將副武器卸下歸還背包！」。
  - 當前已無可卸下武器時（僅存初始武器或槽位皆空），彈出防呆飄字：「當前無可卸下的武器！」。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六語系即時切換，按鈕與提示文字零 hardcode。
  - 按鈕文字對應：zh_TW="一鍵卸下", zh_CN="一键卸下", en="Quick Unsocket", ja="一括解除", ko="일괄 해제", es="Desengarzar Todo"。
  - 成功飄字與防呆飄字六語系皆已登錄於 `game/data/i18n/{code}.json` 與 `game/data/i18n/content/{code}/ui.json`，en、ja、ko、es 下無中文殘留，零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬無頭單元測試**：
  - `godot --path game --headless -s res://scripts/ui/test_lobby_weapon_unequip_all.gd`：PASS（TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK，exit code 0，0 SCRIPT ERROR）。
  - 完整覆蓋：按鈕熱區與規格（>=104x48px, >=48px touch, border_bottom 5px, radius 16px, 16px 開源粉圓體）、副武器卸下歸還背包與保留初始首選武器、無副武器防呆提示、全卸下空手拳套防呆、有效戰力即時刷新、六語系即時動態切換與零系統 Emoji。
- **武器一鍵配置單元測試**：
  - `godot --path game --headless -s res://scripts/ui/test_lobby_weapon_auto_equip.gd`：PASS（LOBBY_WEAPON_AUTO_EQUIP_OK，exit code 0）。
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_3c98e3bb/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_char_weapon_slots_with_three_weapons_zh_TW.png` | 繁中角色頁三槽武器裝備狀態與「一鍵配置」（薄荷綠）、「一鍵卸下」（珊瑚粉 #FF5E8A，104x48px）按鈕 | `4b10272eaba8209ca215464874020c6374f2a5a493c3eaadc7d704bd0ee9c5d4` |
| `proof_02_char_weapon_unequip_success_toast_zh_TW.png` | 點擊一鍵卸下後副武器歸還背包、保留初始武器，上方飄字「已將副武器卸下歸還背包！」 | `78eefc6028f1942032c02d7475a8782411cf4d9dc5ce9a943866e738ee9781e4` |
| `proof_03_char_weapon_unequip_no_secondary_toast_zh_TW.png` | 再次點擊一鍵卸下觸發無副武器防呆，上方飄字「當前無可卸下的武器！」 | `8d726568fb105fae40a6e9fa1cf71af3621e64d631970686e877da1680b86bf4` |
| `proof_04_char_weapon_unequip_bare_handed_zh_TW.png` | 全卸下狀態下切換至空手拳套防呆，三槽顯示空槽，戰力正確更新 | `1c1a4f9bc3090c1083e23819d5069e036aeabcd4b440cbea4d899504235297d0` |
| `proof_05_char_weapon_unequip_en.png` | 英文語系角色頁 Quick Unsocket 按鈕與成功飄字 (Secondary weapons unequipped and returned to bag!) | `dee46820520605fe33ebf5fdef9e7986148621b2eb9583f69386b32ad6ea0e04` |
| `proof_06_char_weapon_unequip_ja.png` | 日文語系角色頁 一括解除 按鈕與成功飄字 (副武器を外してバッグに戻しました！) | `de6c7f038ec8d62a1be65f95499d4168ec80df9bd07435ae58e90a74a6fe4b93` |
| `proof_07_btn_unequip_min_size_48px.png` | 一鍵卸下按鈕規格特寫（尺寸 104x48px，珊瑚粉 #FF5E8A，立體厚底 5px，圓角 16px，描邊 2px） | `d30a86600de6feb1645b4e1c18b13580fb7ce40b24ef88d0283f0f6079c67607` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含配置前、卸下成功飄字、防呆提示、全卸下空手防呆、按鈕規格特寫，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（20~30 幀），無時序競爭，無頭測試 `TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK` 100% 通過。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：標題與副標題採用 VBox 垂直流，三顆按鈕維持 104x48px，橫向無任何擠壓溢出或遮擋。
- [x] **互動元件佈局尺寸與熱區**：`BtnWeaponUnequipAll` 尺寸設為 104x48px，熱區符合手遊規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 16px 開源粉圓體，深藍紫描邊，零系統 Emoji。
- [x] **名稱與用詞規範**：各武器流派與品質名詞嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `lobby-weapon-unequip-all` 標記為測試中。
