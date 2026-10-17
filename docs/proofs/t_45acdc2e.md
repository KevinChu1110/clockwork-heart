# 驗收證明 · SkillDialog 心法招式底欄新增『前往鍛造』快捷果凍按鈕連動 ForgeDialog (t_45acdc2e)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》招式與心法視窗（`SkillDialog`，`skill_dialog.gd`）底部操作按鈕列（`BottomBar`）新增『前往鍛造』立體果凍按鈕（`BtnGoForge`），打通心法招式直通天宮鐵匠彈窗（`ForgeDialog`）的快捷閉環：
1. **按鈕規格與樣式**：
   - 位於底部按鈕列 `BottomBar`，緊鄰『前往背包』與『前往商城』。
   - 採用多巴胺金黃色盤 `COLOR_GOLD` (`#FFD028`)，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 140x50px（符合不小於 140x48px 且高度 >= 50px 手機人體工學規範）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），100% 零系統 Emoji 與特殊符號（符合 0-UI1 規範）。
2. **點擊連動與安全關閉**：
   - 點擊後發射 `go_forge` 與 `forge_requested` 訊號。
   - 安全關閉 `SkillDialog`（發射 `closed` 訊號，無殘留遮罩）。
   - 大廳連動開啟 `ForgeDialog`（`MobileLobby.open_forge()`）。
   - 關閉鐵匠彈窗可順暢返回心法招式介面（`CONNECT_ONE_SHOT` 回跳連動）。
3. **存取器與訊號**：
   - 提供 `get_go_forge_button() -> Button` 與 `get_forge_button() -> Button` 存取器。
   - 宣告 `go_forge()` 與 `forge_requested()` 訊號。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`skill.btn_go_forge`（繁中：前往鍛造，簡中：前往锻造，en：Go to Forge，ja：鍛造へ進む，ko：단조로 이동，es：Ir a Forja）。
   - 同步更新 `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處字典。
   - 歐美語系（en, es）零 CJK 殘留與零 Emoji（符合 0-QA28 規範）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭整合測試** | `godot --path game --headless -s res://scripts/ui/test_skill_dialog_forge_shortcut.gd` | 規格、樣式、訊號、大廳連動、無遮罩殘留、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **真實 Framebuffer 截圖測試** | `xvfb-run -a godot --path game -s res://scripts/ui/test_skill_dialog_forge_shortcut.gd` | 7 張實機截圖完整產出且 SHA256 彼此相異 (exit 0) | **PASS** |
| **商城快捷回歸測試** | `godot --path game --headless -s res://scripts/ui/test_skill_dialog_shop_shortcut.gd` | 既有前往商城快捷按鈕回歸通過 | **PASS** |
| **背包快捷回歸測試** | `godot --path game --headless -s res://scripts/ui/test_skill_dialog_inventory_shortcut.gd` | 既有前往背包快捷按鈕回歸通過 | **PASS** |
| **戰力快捷回歸測試** | `godot --path game --headless -s res://scripts/ui/test_skill_power_stat_shortcut.gd` | 既有前往戰力快捷按鈕回歸通過 | **PASS** |
| **無頭冒煙測試** | `godot --path game --headless --quit-after 3` | 0 Script Error / 0 Crash | **PASS** |
| **程式與素材合規檢查** | `clock-check /opt/side/bravesoul-game` | 零警告，完全通過 (✅ 全過) | **PASS** |

---

## 3. 實機截圖存證清單 (真實 Framebuffer 渲染，符合 0-QA26)

所有實機截圖存放於 `proofs/t_45acdc2e/` 與 `docs/proofs/t_45acdc2e/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_skill_dialog_btn_go_forge.png`
   - SHA256: `43bd2181f4fbbd03f3ca9449251659def3d862c64a7b9676d6ca79a52d4a20eb`
   - 說明：繁中語系 SkillDialog 心法招式底欄展示新增的金黃立體果凍按鈕『前往鍛造』，緊鄰前往背包與前往商城，排版工整無穿框。
2. `proof_02_zh_TW_forge_dialog_opened.png`
   - SHA256: `083bdb8edb85592a214eb4e98e21ddf334e366292d8f9928030bbe8b14a5df9d`
   - 說明：點擊『前往鍛造』後安全關閉 SkillDialog 並直通連動開啟 ForgeDialog 天宮鐵匠彈窗，背景遮罩正常。
3. `proof_03_zh_CN_skill_dialog_btn_go_forge.png`
   - SHA256: `db4ab90364e66ec4f98b7b138bb3379a71fca4918c31389a7f0a046a76d2bb73`
   - 說明：簡中語系即時切換，按鈕正確顯示 `前往锻造`，無文字溢出或截斷。
4. `proof_04_en_skill_dialog_btn_go_forge.png`
   - SHA256: `3c4579e604f4418271dbcb07b646c74f24523cc3d5567b933fc5c4ea84170439`
   - 說明：英文語系即時切換，按鈕正確顯示 `Go to Forge`，排版工整。
5. `proof_05_ja_skill_dialog_btn_go_forge.png`
   - SHA256: `69b5d13fe572d927f5aafcad4a596fbe77ea05c5696dd9d24a58a3a9211d0a34`
   - 說明：日文語系即時切換，按鈕正確顯示 `鍛造へ進む`。
6. `proof_06_ko_skill_dialog_btn_go_forge.png`
   - SHA256: `c64e06d304f68b6d440e08d937d80c7a5a1b3eb3d06292c8aea2cd31c3b4cdd0`
   - 說明：韓文語系即時切換，按鈕正確顯示 `단조로 이동`。
7. `proof_07_es_skill_dialog_btn_go_forge.png`
   - SHA256: `7af529724f34220ec85b8db56d8f1b71b6fb5433cf9766974e19e815b47b1dd1`
   - 說明：西文語系即時切換，按鈕正確顯示 `Ir a Forja`。
