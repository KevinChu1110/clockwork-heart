# 驗收清單：大廳角色頁五大機芯槽新增『一鍵卸下』按鈕與安全防護 (t_0ea90d60)

## 1. 任務核心驗收標準對齊
- [x] **大廳角色頁『一鍵卸下』立體果凍按鈕 (BtnCoreUnequipAll)**：
  - 在 `mobile_lobby.gd` 的角色頁（`Tab.CHARACTER`）機芯五槽配置標題列（`c_hdr`）中，於現有『一鍵配置』按鈕旁新增「一鍵卸下」立體果凍按鈕（`BtnCoreUnequipAll`）。
  - 熱區尺寸嚴格符合手機端人體工學（`custom_minimum_size = Vector2(104, 48)`，熱區 >= 48px，尺寸 >= 104x48px）。
  - 配色採《塔塔冒險隊》珊瑚粉果凍厚底風格（`COLOR_PINK` `#FF5E8A`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A` 2px、底部立體厚底 5px、圓角 16px、陰影 5px），字體使用開源粉圓體（Open Huninn 16px，深藍紫文字），零系統 Emoji。
- [x] **安全卸下五槽機芯邏輯與背包歸還**：
  - 點擊按鈕檢查已裝備機芯，調用 `CoreSystem.unequip_all_cores()` 將五槽機芯安全卸下歸還背包（`CoreSystem.core_inventory`）。
  - 同步清空 `GameState.core_slots` 與 `CoreSystem.player_parts`，五槽卡片即時刷新為「未裝備」狀態。
  - 即時刷新大廳頂部數值（`refresh_hud()`）、角色頁有效戰力膠囊（`_char_power_badge`）與機體戰鬥屬性卡片（`_refresh_char_tab_stats(false)`），總戰力由 147 即時回落至 20。
  - 發出 `cores_unequipped` 信號，並安全保存。
- [x] **空槽防呆安全防護**：
  - 若五槽本來就未裝備機芯，或二次點擊一鍵卸下，安全攔截並彈出防呆飄字：「未裝備任何機芯」，不執行無效寫入。
- [x] **飄字反饋**：
  - 成功卸下機芯時彈出飄字：「已卸下所有機芯」。
  - 當前未裝備任何機芯時，彈出防呆飄字：「未裝備任何機芯」。
  - Toast 浮層優化於頂部安全留白區（offset_top=66, offset_bottom=104），絕不遮擋「武器輪替配置」標題或機芯槽位。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六語系即時切換，按鈕與提示文字零 hardcode。
  - 按鈕文字對應：zh_TW="一鍵卸下", zh_CN="一键卸下", en="Quick Unsocket", ja="一括解除", ko="일괄 해제", es="Desengarzar Todo"。
  - 成功飄字與防呆飄字六語系皆已登錄於 `game/data/i18n/{code}.json` 與 `game/data/i18n/content/{code}/ui.json`，en、ja、ko、es 下無中文殘留，零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬無頭單元測試**：
  - `godot --path game --headless -s res://scripts/ui/test_lobby_core_unequip_all.gd`：PASS（TEST_LOBBY_CORE_UNEQUIP_ALL_OK，exit code 0，0 SCRIPT ERROR）。
  - 完整覆蓋：按鈕熱區與規格（>=104x48px, >=48px touch, border_bottom 5px, radius 16px, 16px 開源粉圓體）、空槽狀態防呆、裝備五槽後一鍵卸下歸還背包、UI 卡片狀態即時刷新、有效戰力即時回落、cores_unequipped 信號發射、二次卸下防呆、六語系即時動態切換與零系統 Emoji。
- **機芯一鍵配置回歸測試**：
  - `godot --path game --headless -s res://scripts/ui/test_lobby_core_auto_equip.gd`：PASS（LOBBY_CORE_AUTO_EQUIP_OK，exit code 0）。
- **武器一鍵卸下回歸測試**：
  - `godot --path game --headless -s res://scripts/ui/test_lobby_weapon_unequip_all.gd`：PASS（TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK，exit code 0）。
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_0ea90d60`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_0ea90d60/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_core_slots_equipped_five_cores_zh_TW.png` | 繁中角色頁五槽機芯裝備狀態與「一鍵配置」（薄荷綠）、「一鍵卸下」（珊瑚粉 #FF5E8A，104x48px）成對按鈕 | `1988d0ffe2c0ddd403738dba8decd3e1e2d7188a999f53f4b3052aed7145336f` |
| `proof_02_core_unequip_success_toast_zh_TW.png` | 點擊一鍵卸下後五槽機芯歸還背包、卡片顯示未裝備、戰力回落，上方飄字「已卸下所有機芯」 | `7eeed0b0960fea83c38c515e119edfbb5d0f1cbfd99cbba9da638553ccea3a31` |
| `proof_03_core_unequip_empty_guard_toast_zh_TW.png` | 再次點擊一鍵卸下觸發空槽防呆，上方飄字「未裝備任何機芯」 | `f76a0e008a33e6969c800940b7002066b3520b7fc180c26b1a5cdcb393b4bac2` |
| `proof_04_core_unequip_en.png` | 英文語系角色頁 Quick Unsocket 按鈕與成功飄字 (All cores unequipped) | `df5f07152a6a67a29feeb0234c74f797f23ff2e8db2888c336e125aa068f23c1` |
| `proof_05_core_unequip_ja.png` | 日文語系角色頁 一括解除 按鈕與成功飄字 (すべてのコアを解除しました) | `a61c03d877c4d507f01158f48e8cf58350c0756b34d101eb94837d2b2180152d` |
| `proof_06_btn_core_unequip_min_size_48px.png` | 一鍵卸下按鈕規格特寫（尺寸 104x48px，珊瑚粉 #FF5E8A，立體厚底 5px，圓角 16px，描邊 2px） | `3cdb97b8cf74374ab6ddc70112dcb18a3b476b4d7049acd9142d2ec2b65ae482` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含配置前、卸下成功飄字、空槽防呆提示、按鈕規格特寫，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（20~30 幀），無時序競爭，無頭測試 `TEST_LOBBY_CORE_UNEQUIP_ALL_OK` 100% 通過。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：Toast 浮層位置垂直調校至安全留白區（offset_top=66..104），絕不遮擋任何標題或槽位；兩顆按鈕維持 104x48px，橫向無任何擠壓溢出或遮擋。
- [x] **互動元件佈局尺寸與熱區**：`BtnCoreUnequipAll` 尺寸設為 104x48px，熱區符合手遊規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 16px 開源粉圓體，深藍紫描邊，零系統 Emoji。
- [x] **名稱與用詞規範**：五大機芯槽位名稱與八色階名詞嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `lobby-core-unequip-all` 標記為測試中。
