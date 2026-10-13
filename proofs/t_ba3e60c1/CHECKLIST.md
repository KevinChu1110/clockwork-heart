# 任務 t_ba3e60c1 驗收清單與存證報告

> 任務名稱：🎮 遊戲開發｜MapleInventory 探索背包支援機芯分類頁籤與機芯詳情替換彈窗直通連動
> 執行分支：`agent/20261012-maple-inventory-core-replace-t_ba3e60c1`
> 執行人員：發條之心·程式 阿宏 (`sideworker`)
> 驗收日期：2026-10-12

---

## 1. 驗收標準對齊與功能實作

| 驗收項目 | 規範標準 | 實作狀態 | 驗證證據 |
|---|---|---|---|
| **機芯分類 Chip** | 在 `CategoryChipsRow` 配置機芯分類按鈕 (id=`core`)，熱區高度 >= 40px，圓角 15px，金黃選取高亮 | ✅ 通過 | `test_maple_inventory_chips.gd` (6/6 綠)<br>`test_maple_inventory_core_replace.gd` |
| **分類篩選過濾** | 點選機芯分類即篩選背包清單，僅顯示未裝備機芯部件 (mainspring, chassis...) | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 3 通過<br>截圖 `proof_01_core_chip_filtered_zh_TW.png` |
| **專屬槽位與八色階標籤** | 選取機芯時顯示專屬槽位膠囊 (`CoreSlotCapsule` / `CoreSlotLabel`) 與八色階標籤膠囊 (`CoreTierCapsule` / `CoreTierSwatch` / `CoreTierLabel`)，字級 >= 14px，深藍紫描邊，零 Emoji | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 4 通過<br>截圖 `proof_02_core_detail_slot_and_tier_zh_TW.png` |
| **替換機芯按鈕** | 提供 `BtnReplaceCore` (高 52px，立體果凍厚底 5px，圓角 18px，熱區 >= 48px)，選取機芯時顯示並啟用，文案『替換機芯』 | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 4 通過 |
| **直通連動 CoreReplaceDialog** | 點擊替換機芯彈出 `CompareLayer` 對比彈窗，顯示新舊機芯數值、槽位、色階與色票對比 | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 5 通過<br>截圖 `proof_03_core_replace_dialog_popup_zh_TW.png` |
| **取消替換回調** | 點擊取消：關閉彈窗，裝備槽與背包保持原狀 | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 6 通過 |
| **確認替換回調** | 點擊確認：新件裝備至對應槽位、自背包移除、舊件退回背包、GameState.core_slots 更新、發射 `core_replaced` 訊號、刷新背包與戰力 (`power_score()`) | ✅ 通過 | `test_maple_inventory_core_replace.gd` Step 7 通過<br>截圖 `proof_04_core_replaced_combat_power_refreshed_zh_TW.png` |
| **六語系支援** | zh_TW, zh_CN, en, ja, ko, es 即時切換無缺詞、零 CJK 殘留 | ✅ 通過 | 截圖 `proof_05_core_inventory_en_locale.png`<br>截圖 `proof_06_core_replace_dialog_ja_locale.png` |
| **無頭冒煙與回歸** | 0 SCRIPT ERROR，相關 MapleInventory 測試 13/13 全綠 | ✅ 通過 | `godot --headless --quit-after 3` 0 error<br>13 支單元測試 100% PASS |
| **clock-check** | 自動檢查工具確認素材、import、語系與無舊詞 | ✅ 通過 | `clock-check .` 全過<br>`clock-check --live` 14 頁全過 |

---

## 2. 實機截圖存證與 SHA256 雜湊表

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_core_chip_filtered_zh_TW.png` | 點選機芯分類 Chip，過濾顯示背包機芯部件 | 1280×720 | `bc9cfd5713b592e98f0999d8d59e3947c7b3ac3a6817060d66c37beab133ed39` |
| `proof_02_core_detail_slot_and_tier_zh_TW.png` | 選取機芯部件，顯示專屬槽位標籤、八色階標籤、色票與替換機芯按鈕 | 1280×720 | `9b374984bed6333440f76fb510b5f9515a580378422af6392a9044a175db1477` |
| `proof_03_core_replace_dialog_popup_zh_TW.png` | 點擊替換機芯直通彈出 CoreReplaceDialog 對比彈窗 | 1280×720 | `3cc9b091c512c66c727f0bc89d0685cec63e791bd85bad4cef0254d582cc717d` |
| `proof_04_core_replaced_combat_power_refreshed_zh_TW.png` | 確認替換後新件入槽、舊件退回背包、戰力評分提升 (+6) 即時刷新 | 1280×720 | `f20c4f7b69abd72eb16fa8ac1d3b91cac7799edc298c2573fad4d80884c4d53c` |
| `proof_05_core_inventory_en_locale.png` | 英文語系 (Core chip, Swap Core button, Mainspring Dynamo slot) | 1280×720 | `2e9f603ec6ad7c2c0efad42a1e9a12f1b8a5c59cd1c621464c5aa47aa0e53c5c` |
| `proof_06_core_replace_dialog_ja_locale.png` | 日文語系 CoreReplaceDialog 比較確認彈窗 (コア入替) | 1280×720 | `b24ebaba57802a3cc2eccda1cc5dd28c517cb163a064e908bf928d0ec86504bb` |

*註：6 張截圖 SHA256 互不相同，零重複，各語系渲染及時序等待皆符合規範。*

---

## 3. 回歸測試清單

- `test_maple_inventory_core_replace.gd`: **PASS (100%)**
- `test_maple_inventory_chips.gd`: **PASS (100%)**
- `test_maple_inventory.gd`: **PASS (100%)**
- `test_maple_inventory_sort.gd`: **PASS (100%)**
- `test_maple_inventory_equip.gd`: **PASS (100%)**
- `test_maple_inventory_equipped.gd`: **PASS (100%)**
- `test_maple_inventory_diff.gd`: **PASS (100%)**
- `test_maple_inventory_lock.gd`: **PASS (100%)**
- `test_maple_inventory_dismantle.gd`: **PASS (100%)**
- `test_maple_inventory_shortcuts.gd`: **PASS (100%)**
- `test_maple_inventory_capacity.gd`: **PASS (100%)**
- `test_maple_inventory_batch_sell.gd`: **PASS (100%)**
- `test_maple_inventory_consumable_use.gd`: **PASS (100%)**
- `test_maple_inventory_hotbar_toggle.gd`: **PASS (100%)**
