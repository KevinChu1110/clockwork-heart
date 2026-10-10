# ForgeDialog 天宮鐵匠新增『一鍵鍛造』按鈕與連動 ForgeSystem 驗收查驗清單 (t_39e65d16)

## 任務目標
1. 在 `ForgeSystem` (`res://scripts/systems/forge_system.gd`) 實作 `auto_forge(max_tries: int = 10) -> Dictionary`，支援批次連續升階判定直至鐵屑或金幣不足、達到最大階級或達到嘗試上限。
2. 在 `ForgeDialog` (`res://scripts/ui/forge_dialog.gd`) 底部操作區新增『一鍵鍛造』按鈕 `BtnAutoForge`（熱區 >= 48px，果凍厚底 5px，薄荷綠配色），點擊後連續執行鍛造並於 `MsgLabel` 彈出成果反饋（成功次數/攻擊力成長/消耗統計）。
3. 鍛造後即時刷新三欄武器槽位數值（`WeaponSlotChipRow` 階級標籤）與頂部戰力展示（`TopPowerLabel`）。
4. 符合手遊規範：橫屏彈窗、果凍厚底、零系統 emoji、六語系支援（`ui.json` 補齊多語系文本）。
5. 新增 headless 測試 `test_forge_dialog_auto_forge.gd`，驗證 auto_forge 邏輯與 BtnAutoForge 點擊交互全數通過。

## 查驗項目與執行結果

### 1. 程式碼與功能實作
- [x] `ForgeSystem.auto_forge`：支援批次連續升階判定，完整判定 `no_scrap`（鐵屑不足）、`no_gold`（金幣不足）、`tier_max`（達到上限）以及 `max_tries`（嘗試上限）。精確回傳 `tries`、`success_count`、`fail_count`、`atk_gain`、`spent_gold`、`spent_scrap`、`tier`、`cost`。
- [x] `ForgeDialog` 底部操作區：新增 `BtnAutoForge`（熱區 52px >= 48px，果凍厚底 5px，薄荷綠 `COLOR_MINT` `#4ED86A` 配色），按鈕排版間距均勻，無圖層重疊。
- [x] 頂部戰力展示：標題列新增 `TopPowerLabel`（`get_top_power_label()`），展示最新綜合戰力（`戰力 %d`），鍛造後即時連動刷新。
- [x] 成果反饋：點擊 `BtnAutoForge` 後於 `MsgLabel` 輸出『一鍵鍛造完成！成功 %d 次（嘗試 %d 次）· 攻擊力 +%d · 消耗 %d 金幣、%d 鐵屑』，顏色為薄荷綠；失敗或無法鍛造則對應提示。
- [x] 即時連動刷新：鍛造完成後即時呼叫 `_refresh_display()`，三欄武器槽位 Chip 即時更新至最新 `(T%d)`，頂部戰力即時增長。
- [x] 六語系支援：`ui.json` 與 `<locale>.json`（zh_TW, zh_CN, en, ja, ko, es）完整補齊『一鍵鍛造』及對應反饋文字，零系統 Emoji、歐美語系零 CJK 殘留。

### 2. 實機渲染存證截圖 (1280x720)
| 截圖檔名 | 說明 | 規格與狀態 | SHA256 雜湊值 |
|---|---|---|---|
| `proof_01_forge_dialog_initial_autoforge_btn.png` | 鍛造彈窗首頁未鍛造狀態（展示 BtnAutoForge 薄荷綠按鈕、頂部戰力 91、槽位 1 T1） | 1280x720 PNG | `99528d970f91b4287d2725c3a8fd99f8d3e28fdced1cb51e018177867dba96d9` |
| `proof_02_forge_dialog_after_autoforge.png` | 一鍵鍛造完成成果反饋（成功 8 次、攻擊力 +16、消耗統計、頂部戰力 139、槽位 1 T9） | 1280x720 PNG | `3d39789699229324b58b37274277514cd0a4e5db00f9fd4aff191ec2bec48552` |
| `proof_03_forge_dialog_slot_switch.png` | 切換至槽位 2（鐵骨重鎚）數值與面板正常刷新 | 1280x720 PNG | `2ca4e0606abf8692c7818562a88bd33900d9a196db580afd246ae39be8c4db0f` |
| `proof_04_forge_dialog_max_tier_disabled.png` | 達到最大階級 T11 滿階封頂防護（BtnAutoForge 與 BtnForge 正確禁用置灰） | 1280x720 PNG | `0d4aed4dc1e08dee4a74d74ef065e6b4f2e22a437a9be2b350b3a22ba7186481` |

### 3. 無頭測試與合規斷言
- [x] `test_forge_dialog_auto_forge.gd`：單元測試覆蓋 auto_forge 邏輯判定、BtnAutoForge 點擊交互、成果反饋格式、三欄武器 Chip 數值刷新、頂部戰力展示刷新、空槽/滿階防護與六語系即時切換斷言，全數通過（`TEST_FORGE_DIALOG_AUTO_FORGE_OK`）。
- [x] `test_forge_weapon_loadout_slots.gd`：既有三欄武器槽位切換與鍛造測試全數通過（`TEST_FORGE_WEAPON_LOADOUT_SLOTS_OK`）。
- [x] `test_forge_workshop_shortcut.gd`：既有雙向直通快捷測試全數通過（`TEST_FORGE_WORKSHOP_SHORTCUT_OK`）。
- [x] `godot --path game --headless --quit-after 3`：冒煙測試 0 報錯、0 Script Error。
