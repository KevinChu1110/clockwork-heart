# 發條之心工作室 驗收證明 · MapleInventory 探索背包支援選取機芯拆解回收與安全防護 (t_00903732)

## 1. 任務目標與實作摘要
依據看板任務 `t_00903732` 之規格要求，於 `game/scripts/ui/maple_inventory.gd` 探索背包中實作機芯物品選取拆解回收與安全防護：
1. **未裝備機芯拆解回收**：
   - 當玩家在機芯頁籤選取未裝備機芯時，顯示珊瑚粉果凍厚底按鈕『拆解回收』（高度 52px >= 48px，立體厚底 5px，圓角 18px，字級 18px，零 Emoji）。
   - 點擊後依 `CoreSystem` 八色階標準產出鐵屑：灰1／白2／橘3／藍4／紫5／金6／綠8／紅10，發放至 `GameState.iron_scrap`（與 `inventory["iron_scrap"]` 雙向同步連動）並自背包扣除該機芯。
   - 播放 UI 音效與飄字提示（例如『拆解【傳動齒輪組·藍階】：獲得鐵屑 ×4』），發送 `core_dismantled` 與 `equipment_dismantled` 訊號，即時刷新背包格子與容量進度（`Capacity 4/24` -> `3/24`）。
2. **安全防護機制**：
   - 若該機芯已裝備於五大槽位（`is_selected_item_equipped()` 檢查 `EquipmentSystem`、`GameState.core_slots`、`CoreSystem.ALL_SLOT_IDS` 與 `player_parts`）：按鈕切換為禁用置灰（`disabled=true`），文案顯示『已裝備無法拆解』，程式呼叫 `dismantle_selected()` 亦嚴格阻擋並彈出提示，嚴防誤拆上身機芯。
   - 若機芯已鎖定：按鈕切換為禁用置灰，顯示『已鎖定無法拆解』，嚴防誤拆珍貴機芯。
3. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`，包含『拆解回收』、『已裝備無法拆解』、『拆解機芯回收鐵屑』、『機芯部件 · 強化發條動力核心』等鍵值，經 Vision 分析確認零中文殘留。
4. **單元測試與驗證**：
   - 撰寫 `game/scripts/ui/test_maple_inventory_core_dismantle.gd` 覆蓋 13 項單元斷言（八色階鐵屑計算、色階對齊、安全阻擋、飄字、即時容量刷新、語系切換、零 Emoji、實機截圖 SHA256 互異），全數通過。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **機芯拆解專屬單元測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_core_dismantle.gd` | 13/13 步驟全數通過，八色階鐵屑計算與防護 100% 驗證 (exit 0) | **PASS** |
| **背包裝備拆解回歸測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_dismantle.gd` | 13/13 步驟全數通過 (exit 0) | **PASS** |
| **背包機芯頁籤替換測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_core_replace.gd` | 12/12 步驟全數通過 (exit 0) | **PASS** |
| **大廳機芯一鍵配置測試** | `godot --path game --headless -s res://scripts/ui/test_lobby_core_auto_equip.gd` | 4/4 步驟全數通過 (exit 0) | **PASS** |
| **大廳機芯替換彈窗測試** | `godot --path game --headless -s res://scripts/ui/test_lobby_core_replace_dialog.gd` | 6/6 步驟全數通過 (exit 0) | **PASS** |
| **自動檢查 clock-check** | `/root/bin/clock-check /opt/side/bravesoul-game` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_core_equipped_protected_zh_tw.png` | 選取已裝備發條發電機機芯：右側顯示屬性，按鈕置灰禁用顯示『已裝備無法拆解』 | 1280×720 | `74c6f3a5a4899d10d92089b616a6b1e52e255bd9a7f09cac69ad5ea3b1d95b1f` |
| `proof_02_core_unequipped_ready_dismantle_zh_tw.png` | 選取未裝備傳動齒輪組（藍階）：右側顯示攻擊+15，下方顯示珊瑚粉果凍按鈕『拆解回收』 | 1280×720 | `a985083403d0743ac4c388ebca236e841ebdf36327ccc17fabd2ca09e6f65ba3` |
| `proof_03_core_dismantled_scrap_gained_zh_tw.png` | 拆解後獲得鐵屑×4入袋：容量即時更新為 3/24，背包藍階機芯已扣除，底部飄字提示 | 1280×720 | `57ad96579f45bc7b9acd061ec23d0df341c68ea7144cb233dd45b8e76250d941` |
| `proof_04_core_dismantle_en.png` | 英文語系驗證：Resonance Core · Gold Tier，按鈕顯示『Dismantle』，零中文殘留 | 1280×720 | `821070e13e02b1843c253de511c9767db5e5f54dde36c35e3da55a2f4ade9101` |
| `proof_05_core_dismantle_ja.png` | 日文語系驗證：共鳴コア・金階，按鈕顯示『分解回収』，完全日文化無破圖 | 1280×720 | `be923065f1e488ee3522809ed4807f53f6ad16a79a2d38f4dcc9413823f8df3a` |

*註：全部 5 張實機截圖 SHA256 互異，經 Vision AI 驗證無破圖、無豆腐塊、無系統 Emoji、多語系無殘留中文。*

---

## 4. 審查常見退回自查表（對照 clock-review-checklist.md）

- [x] **測試與證據**：測試腳本截圖精準控制等待時序（4~6 幀），確保 Viewport 與語系渲染完成；連續截圖 SHA256 互異，各語系切換正確，有 Toast 提示與容量即時刷新證據。
- [x] **單元與功能測試**：覆蓋八色階鐵屑計算（灰1/白2/橘3/藍4/紫5/金6/綠8/紅10）、已裝備五大槽位安全阻擋、已鎖定安全阻擋、訊號發射與數值即時斷言。
- [x] **畫面與素材**：按鈕熱區高度 52px >= 48px，底邊 5px，圓角 18px，無 13px 以下小字，100% 零系統 Emoji。
- [x] **程式與邏輯**：`GameState.iron_scrap` 雙向連動、`is_selected_item_equipped()` 涵蓋五大槽位辨識、`CoreSystem.dismantle_part()` 嚴格校準。
- [x] **資料與文案**：六語系（zh_TW, zh_CN, en, ja, ko, es）完整對齊，無殘留中文或缺詞。
- [x] **流程與交付**：`docs/PROJECTS.json` 透過 `python3 /root/project_status.py inventory-core-dismantle-recycle 測試中` 更新完成。
