# 驗收證明 · BattleDefeatDialog 戰敗結算新增『前往背包』快捷果凍按鈕連動 MapleInventory (t_0bfa03fb)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》戰鬥失敗結算彈窗（`BattleDefeatDialog`，`battle_defeat_dialog.gd`）底欄新增天藍色立體果凍按鈕『前往背包』（`BtnGoInventory`），點擊後發出 `inventory_requested` 訊號並連動喚起探索背包 `MapleInventory`，與已完成的 `BattleVictoryDialog` 對稱形成完整閉環：
1. **按鈕規格與樣式**：
   - 位於底部操作按鈕列（`BottomActions`），緊鄰『前往戰力』（`BtnGoPowerStat`）按鈕。
   - 多巴胺天藍色盤 `#38A0FF`（`COLOR_SKY`），深藍紫描邊 `#1F1A3A`，文字白色 `#FFFDF8` 帶深色描邊。
   - 熱區尺寸 130x52px（高度 52px，寬度 130px，滿足 130~150px 範圍且熱區 >= 48px，符合手機端防誤觸人因規範）。
   - 立體果凍厚底 6px（`border_width_bottom = 6`），圓角 20px（在 18~20px 規範內），字級 17px 開源粉圓體（Open Huninn），零系統 Emoji、零禁止符號。
2. **點擊連動與彈窗銷毀**：
   - 點擊後發射 `inventory_requested` 與 `go_inventory` 訊號並執行 `setup` 傳入之 `on_inventory` 回調。
   - 安全銷毀結算彈窗（`queue_free`），無殘留遮罩、無介面卡死。
   - 連動調起 `MapleInventory` 探索背包，大廳與戰鬥皆能無縫接軌。
3. **存取器**：
   - 提供 `get_go_inventory_button() -> Button`。
   - 提供 `get_inventory_button() -> Button`（相容別名）。
   - 提供 `get_go_inventory_button_text() -> String`。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 繁中：前往背包
   - 簡中：前往背包
   - 英文：Go to Inventory（零 CJK 殘留）
   - 日文：インベントリへ進む
   - 韓文：인벤토리로 이동
   - 西文：Ir al Inventario（零 CJK 殘留）
   - 全語系零系統 Emoji。
5. **合規與自動化測試**：
   - 遵守 review.md 與 AGENTS.md 規範，撰寫單元與整合測試 `test_battle_defeat_inventory_shortcut.gd`。
   - 執行 `clock-check` 確保零警告，OpenGL3 真實渲染截圖存證完備。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |\
| **前往背包快捷測試** | `godot --path game --headless -s scripts/battle/test_battle_defeat_inventory_shortcut.gd` | 按鈕實例、樣式尺寸、點擊訊號、回調連動、MapleInventory連動、六語系即時切換全部 PASS (exit 0) | **PASS** |\
| **相關測試回歸驗證** | 跑過既有 5 個戰敗相關測試 (`test_battle_defeat_power_stat_shortcut`, `test_battle_defeat_retry`, `test_battle_defeat_diagnostic`, `test_battle_defeat_i18n`, `test_colossus_defeat_hint`) | 全數通過 (exit 0) | **PASS** |\
| **程式與素材合規檢查** | `clock-check t_0bfa03fb` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |\

---

## 3. 實機截圖存證清單 (OpenGL3 真實 Framebuffer 渲染)

所有實機截圖存放於 `proofs/t_0bfa03fb/` 與 `docs/proofs/t_0bfa03fb/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_battle_defeat_dialog_btn_go_inventory_zh_TW.png`
   - SHA256: `0e48934dd2f33596e447ed7bcde8bd3b52c21c265ba69d76ec19f9fb29d2c3a6`
   - 說明：繁中語系下戰敗結算底欄顯示『前往背包』果凍按鈕（天藍色立體果凍厚底 6px、圓角 20px、高 52px、熱區 130x52px >= 48px、零 Emoji）。
2. `proof_02_battle_defeat_dialog_en.png`
   - SHA256: `2431c935c9435d1782854586087ff650268d6f16c3ecd7c4cfa059a086b14bda`
   - 說明：英文語系 (en) 即時動態切換，按鈕正確顯示 "Go to Inventory"，零 CJK 殘留、零 Emoji、無文字折行溢出。
3. `proof_03_battle_defeat_dialog_ja.png`
   - SHA256: `cad5ab6ec5bef557a61b59b295e4109544f0d07bf1f64e352cc224f732a59556`
   - 說明：日文語系 (ja) 即時動態切換，按鈕正確顯示「インベントリへ進む」，零 Emoji。
4. `proof_04_battle_defeat_dialog_ko.png`
   - SHA256: `ac9a1f1b3b8202456157d23e8622d556489efcb9006fd5608a639ea6ec55be01`
   - 說明：韓文語系 (ko) 即時動態切換，按鈕正確顯示「인벤토리로 이동」，零 Emoji。
5. `proof_05_battle_defeat_dialog_es.png`
   - SHA256: `2e88227b72e57a9a19e488c301955d2c93c05a08e73db61a006fcd2279f766ee`
   - 說明：西文語系 (es) 即時動態切換，按鈕正確顯示 "Ir al Inventario"，零 CJK 殘留、零 Emoji。
6. `proof_06_click_btn_go_inventory_opens_maple_inventory.png`
   - SHA256: `6e2053d02411084cd0ed8434790605a0b169cfa6a484f7beda55ba718e47ea9f`
   - 說明：點擊『前往背包』關閉戰敗彈窗並連動調起 MapleInventory 探索背包，無殘留遮罩無卡死。

---

## 4. 專案狀態更新
- `defeat-inventory-shortcut`：`開發中` → `測試中`（完成開發、自測與截圖存證，送審 sideqa）
