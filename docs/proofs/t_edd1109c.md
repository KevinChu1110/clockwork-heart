# 驗收證明 · MapleInventory 探索背包底欄新增『前往衣櫥』快捷果凍按鈕連動 WardrobeDialog (t_edd1109c)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》探索背包視窗（`MapleInventory`，`maple_inventory.gd`）底欄快捷按鈕列（`GridBottomBar`）新增『前往衣櫥』立體果凍按鈕（`BtnGoWardrobe`），打通探索背包直通衣櫥換裝彈窗（`WardrobeDialog`）的快捷閉環：
1. **按鈕規格與樣式**：
   - 位於底欄快捷按鈕列 `GridBottomBar`，與容量進度膠囊、一鍵整理及前往戰力按鈕並列。
   - 採用多巴胺暖橘色盤 `#FFA010`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 120x48px（符合手機端熱區 >= 48px 規範）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），100% 零系統 Emoji 與特殊符號（符合 0-UI1 規範）。
2. **點擊連動與安全關閉**：
   - 點擊後發射 `go_wardrobe` 與 `wardrobe_requested` 訊號，同時發射 `closed` 訊號。
   - 安全關閉 `MapleInventory`（無殘留遮罩）。
   - 大廳連動開啟 `WardrobeDialog`（`MobileLobby.open_wardrobe()` / `MobileLobby.open_wardrobe_dialog()`）。
   - 流暢切換至衣櫥換裝彈窗介面。
3. **存取器與訊號**：
   - 提供 `get_go_wardrobe_button() -> Button`、`get_bag_go_wardrobe_button() -> Button` 與 `get_wardrobe_button() -> Button` 存取器。
   - 宣告 `go_wardrobe()` 與 `wardrobe_requested()` 訊號。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`inventory.btn_go_wardrobe`（繁中：前往衣櫥，簡中：前往衣橱，en：To Wardrobe，ja：衣装部屋へ，ko：옷장으로，es：A Guardarropa）。
   - 同步更新 `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處字典。
   - 歐美語系（en, es）零 CJK 殘留（符合 0-QA28 規範）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|\n| **快捷按鈕整合測試** | `xvfb-run -a godot --path game -s res://scripts/ui/test_maple_inventory_wardrobe_shortcut.gd` | 規格、樣式、訊號、大廳連動、無遮罩殘留、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **無頭整合測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_wardrobe_shortcut.gd` | 無頭環境穩定 PASS (exit 0) | **PASS** |
| **戰力前往背包測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_power_stat_shortcut.gd` | 回歸測試通過 (exit 0) | **PASS** |
| **稱號前往背包測試** | `godot --path game --headless -s res://scripts/ui/test_title_wall_inventory_shortcut.gd` | 回歸測試通過 (exit 0) | **PASS** |
| **程式與素材合規檢查** | `clock-check .` | 零警告，完全通過 (✅ 全過) | **PASS** |

---

## 3. 實機截圖存證清單 (真實 Framebuffer 渲染，符合 0-QA26)

所有實機截圖存放於 `proofs/t_edd1109c/` 與 `docs/proofs/t_edd1109c/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `38e0d8c8d9b9ed2bc3d3f458b8d2f1f3d97752bc653668f3a67fb21e98b88dbb`
   - 說明：繁中語系 MapleInventory 探索背包底欄展示新增的暖橘立體果凍按鈕『前往衣櫥』。
2. `proof_02_zh_TW_click_go_wardrobe_opens_wardrobe_dialog.png`
   - SHA256: `f704906e565fab7d99d271a80c5319f13b7dfc0928e815b208cafbdeddcf674f`
   - 說明：點擊『前往衣櫥』後安全關閉 MapleInventory 並直通連動開啟 WardrobeDialog 換裝衣櫥彈窗。
3. `proof_03_zh_CN_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `63e390310efa254b784efcc81c6f2b5b90780ebcfa41bb8630953496b5d4843f`
   - 說明：簡中語系即時切換，按鈕正確顯示 `前往衣橱`，無文字溢出或截斷。
4. `proof_04_en_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `5f2a248c3a4920bfdfd92655e48adfa9941ff1cc58e84884c200e179148903ef`
   - 說明：英文語系即時切換，按鈕正確顯示 `To Wardrobe`，零 CJK 殘留。
5. `proof_05_ja_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `5d39db634c4ee96d1d10fdfb650dda5b50b8fba9b7c8f4f51ee2526eb44a3b21`
   - 說明：日文語系即時切換，按鈕正確顯示 `衣装部屋へ`。
6. `proof_06_ko_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `a1ff228053db1b91ca54ce8eda03bf71c3c34b9dc5979eacce1d6c59214198b2`
   - 說明：韓文語系即時切換，按鈕正確顯示 `옷장으로`。
7. `proof_07_es_maple_inventory_btn_go_wardrobe.png`
   - SHA256: `8d822ba87fdc476d0aa5ded9c2756ddd9f961a2b9d9b9e426cb1444e02199220`
   - 說明：西文語系即時切換，按鈕正確顯示 `A Guardarropa`，零 CJK 殘留。
8. `proof_08_loop_back_to_maple_inventory.png`
   - SHA256: `a3b82a157afd6073c8165651ca069407710a0c4ea4a76ffde94a5b67d32c2d54`
   - 說明：關閉換裝衣櫥回到探索背包，繁中語系恢復，完成閉環驗證。
