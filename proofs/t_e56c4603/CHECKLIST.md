# TitleWallDialog 稱號牆新增『前往背包』快捷果凍按鈕連動 MapleInventory 驗收存證 (t_e56c4603)

## 任務目標
1. 在 `TitleWallDialog` (`game/scripts/ui/title_wall_dialog.gd`) 稱號牆視窗底欄操作按鈕列 (`ButtonRow`)，新增『前往背包』(`BtnGoInventory`) 快捷果凍按鈕。
2. 點擊後發射 `inventory_requested` 與 `closed` 訊號並安全關閉彈窗 (`_on_close()`)，大廳 `MobileLobby` (`game/scripts/ui/mobile_lobby.gd`) 監聽訊號後平滑連動開啟 `MapleInventory` 探索背包。
3. 按鈕尺寸與視覺規範：
   - 位於 `ButtonRow` 底部按鈕列中，與『前往戰力』、『前往衣櫥』、『前往商城』、『卸下稱號』並列。
   - 熱區尺寸 150x52px（符合手機端熱區 >= 48px 與高度 >= 50px 規範）。
   - 多巴胺薄荷綠色盤 (`COLOR_MINT` `#4ED86A`)，深藍紫描邊 (`COLOR_BORDER` `#1F1A3A`)，文字深藍紫 `#1F1A3A` 帶白描邊 (outline 2px)，立體果凍厚底 5px，圓角 18px，字級 18px 開源粉圓體 (Open Huninn)，100% 零系統 Emoji。
4. 提供存取器 `get_go_inventory_button()` 與 `get_inventory_button()`。
5. 支援六語系 i18n 即時刷新（`zh_TW`: 「前往背包」, `zh_CN`: 「前往背包」, `en`: 「To Inventory」, `ja`: 「バッグへ」, `ko`: 「가방으로 이동」, `es`: 「Ir a Mochila」），英西語系零 CJK 殘留。
6. 撰寫單元與整合測試 `test_title_wall_inventory_shortcut.gd`，在非 headless (xvfb) 下產出 8 張六語系實機截圖存證，執行 `clock-check` 確認無警告。
7. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態為「測試中」。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，稱號牆底欄六按鈕並列排版整齊，文字無穿框，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoInventory` 尺寸 150x52px（熱區 >= 48px，高 >= 50px），深藍紫文字 #1F1A3A 帶白描邊搭配薄荷綠底 #4ED86A，立體厚底 5px，圓角 18px，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e56c4603` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏、無遮罩殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 6~10 幀，無頭與實機測試穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_title_wall_inventory_shortcut`、`test_title_wall_dialog_shop_shortcut`、`test_title_wall_wardrobe_shortcut`、`test_title_wall_power_stat_shortcut` 等測試全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoInventory` 發射 `closed` 與 `inventory_requested` 訊號並關閉稱號牆彈窗，大廳連動開啟 `MapleInventory`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 稱號牆點擊『前往背包』直達探索背包，分類頁籤齊全，無卡死、無破圖。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全（zh_TW: 前往背包, zh_CN: 前往背包, en: To Inventory, ja: バッグへ, ko: 가방으로 이동, es: Ir a Mochila），英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `title-wall-inventory-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與產證檔案已 commit 至工作分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_title_wall_with_btn_go_inventory.png` | 繁中稱號牆彈窗：底欄六按鈕並列，薄荷綠果凍按鈕『前往背包』(150x52px) 正常顯示 | 1280x720 | `caabdc9e70788b2a2af4a1a2d5250bab337830150ad5bc822cb51afeb5bb2c95` |
| 02 | `proof_02_zh_TW_inventory_opened_from_title_wall.png` | 點擊前往背包：直通開啟 MapleInventory 探索背包，底層無遮罩殘留 | 1280x720 | `f855fe65cafa2cc18d331e5f8616504ae91c790664e4698e1db6cbdc84bdf89c` |
| 03 | `proof_03_zh_CN_title_wall_btn_go_inventory.png` | 簡中語系即時切換：『前往背包』 | 1280x720 | `19470ff2a2a7555c2c266f1c40bd575c369018257fbc1cd359f44ff90a051bd0` |
| 04 | `proof_04_en_title_wall_btn_go_inventory.png` | 英文語系即時切換："To Inventory"，零 CJK 殘留 | 1280x720 | `ff3100b8cdb5404a98a3f33ff241d5e77fb446cfbf0c5091e6ec44da82423bc5` |
| 05 | `proof_05_ja_title_wall_btn_go_inventory.png` | 日文語系即時切換：『バッグへ』 | 1280x720 | `0c9459834be1e64c47bcb48466a27e04e281788d40707037f72e3ad4710f8115` |
| 06 | `proof_06_ko_title_wall_btn_go_inventory.png` | 韓文語系即時切換：『가방으로 이동』 | 1280x720 | `6c9223325b7d7a5b5065c673148ac28b44bdfe003b4fac46e1c9269b744d1507` |
| 07 | `proof_07_es_title_wall_btn_go_inventory.png` | 西文語系即時切換："Ir a Mochila"，零 CJK 殘留 | 1280x720 | `c04efa1ebd5e37f03fe8fa9d865a83b36f04608d4a9acdc88f792c2cf953e7b7` |
| 08 | `proof_08_loop_back_to_title_wall.png` | 關閉探索背包回到稱號牆：繁中文案無縫恢復，完整閉環驗證 | 1280x720 | `ff73802179be687e3c1fe5653adbfc4bdd3a63bf973a5a6e7c7cbf5e516be599` |
