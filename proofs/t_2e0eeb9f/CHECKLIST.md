# 驗收清單：ForgeDialog 天宮鐵匠新增持有鐵屑進度膠囊與鐵屑不足前往拆解快捷按鈕 (t_2e0eeb9f)

## 1. 任務核心驗收標準對齊
- [x] **ForgeDialog 機芯五槽部位面板頂部新增『鐵屑持有膠囊』（IronScrapCapsule 與 _scrap_label / IronScrapLabel）**：
  - 在 `game/scripts/ui/forge_dialog.gd` 機芯五槽面板頂部（`core_head`）新增 `IronScrapCapsule` 進度膠囊與 `IronScrapLabel` 標籤。
  - 即時讀取 `GameState.iron_scrap` / `CoreSystem.get_player_scrap()` 與單次校準消耗（`CoreSystem.get_calibration_scrap_cost()`，預設 5）。
  - 鐵屑充足時（>= 5），顯示例如「鐵屑：24（每次消耗 5）」，膠囊為暖黃/米白底色，文字為深藍紫高對比色階。
- [x] **鐵屑不足警告色階與『前往拆解』立體果凍按鈕（BtnGoDismantle）**：
  - 當鐵屑不足時（< 5），膠囊呈現珊瑚粉警告色階（`COLOR_CARD_PINK` 與 `COLOR_TEXT_PINK`）。
  - 在膠囊旁即時顯現『前往拆解』立體果凍按鈕（`BtnGoDismantle`）。
  - 熱區與尺寸規格：高度 >= 48px（`custom_minimum_size = Vector2(110, 48)`），圓角 18px，薄荷綠果凍厚底 5px（`COLOR_MINT` `#4ED86A`），零系統 Emoji。
  - 鐵屑充足時，按鈕安全隱藏（`visible = false`）。
- [x] **信號連動與大廳直通 MapleInventory 探索背包機芯分類 Chip**：
  - 點擊『前往拆解』時，發出 `dismantle_requested` 信號並播放 UI 音效。
  - 大廳（`MobileLobby`）連動監聽 `dismantle_requested`，關閉天宮鐵匠彈窗，直通開啟 `MapleInventory` 探索背包並自動切換至機芯分類 Chip（`set_category("core")`）。
  - 玩家可立即選取多餘未裝備機芯執行拆解換取鐵屑，形成「校準 -> 鐵屑不足 -> 一鍵前往背包拆解 -> 獲取鐵屑回流校準」之完整養成閉環。
- [x] **六語系在地化切換與字級規範**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六大語系即時切換。
  - 膠囊與按鈕文字皆使用開源粉圓體（Open Huninn），字級嚴格 >= 16px，無 13px 以下小字。
  - 歐美語系 (en, es) 零 CJK 漢字殘留，全語系 0 系統 Emoji。
- [x] **單元測試與實機 Framebuffer 截圖存證**：
  - 新增單元測試 `game/scripts/ui/test_forge_dialog_scrap_shortcut.gd`，完整驗證 UI 結構、數值更新、狀態切換、信號連動與六語系。
  - 產出真實 OpenGL3 實機 Framebuffer 截圖存證至 `proofs/t_2e0eeb9f/`。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=test_forge_dialog_scrap_shortcut ./tools/run_tests.sh`：1/1 PASS（100% 全綠，`TEST_FORGE_DIALOG_SCRAP_SHORTCUT_OK`，exit code 0）。
- **既有回歸測試**：
  - `TEST_FILTER=forge ./tools/run_tests.sh`：10/10 PASS（100% 全綠，無任何回歸破壞）。
  - `TEST_FILTER=maple_inventory ./tools/run_tests.sh`：15/15 PASS（100% 全綠）。
- **無頭冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2e0eeb9f/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_2e0eeb9f/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_scrap_sufficient_capsule_zh_TW.png` | 鐵屑充足 (scrap=24) 膠囊米黃底色「鐵屑：24（每次消耗 5）」，前往拆解按鈕隱藏 | `8073918d492032403ae5f12e46c0a3ed3479932daed37faf74949a70a1ee05f5` |
| `proof_02_scrap_insufficient_warning_dismantle_btn_zh_TW.png` | 鐵屑不足 (scrap=2) 珊瑚粉警告色階「鐵屑：2（每次消耗 5）」，顯現『前往拆解』薄荷綠果凍按鈕 | `11f679d98b4577877147e06901e69f8b628c0b25baaf30b3de1f3341ef24e3e1` |
| `proof_03_click_dismantle_opens_maple_inventory_chip_zh_TW.png` | 點擊『前往拆解』連動開啟 MapleInventory 背包並切換至機芯分類 Chip ('core') | `89e2a45bc17da698a891d9174f10442e0a06bbba929a7a5490d171c110bd5e38` |
| `proof_04_scrap_capsule_dismantle_btn_en.png` | 英文語系 (en) Iron Scrap: 2 (Cost 5) 與 Dismantle 按鈕，零 CJK 殘留 | `b0f26b91aa2bb269f5a473bc3ff54d6b1e7290b67903055bbf635bd1bffd2d25` |
| `proof_05_scrap_capsule_dismantle_btn_ja.png` | 日文語系 (ja) 鉄くず：2（消費 5）與 分解へ 按鈕 | `f04f64d9951b731832ef6dd4cb43b341617fa7f9860ac6fd2844fcd028d9eb46` |
| `proof_06_scrap_capsule_dismantle_btn_ko.png` | 韓文語系 (ko) 고철: 2 (소모 5) 與 분해하러 가기 按鈕 | `cd4524025026e2a09b54598a897615719783fd14da04ae87f86308cab483faff` |
