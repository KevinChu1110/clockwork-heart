# 探索背包底欄新增『前往戰力』快捷果凍按鈕連動PowerStatDialog 驗收文件 (t_2d1c7fbd)

- **任務 ID**：`t_2d1c7fbd`
- **卡片標題**：探索背包底欄新增前往戰力快捷按鈕連動PowerStatDialog
- **執行人員**：阿翔（sideworker2，發條之心·工程師）
- **審查人員**：小婷（sideqa，發條之心·測試）
- **所屬專案**：發條之心 / Clockwork Heart (`/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2d1c7fbd/bravesoul-game`)
- **工作分支**：`agent/20261014-maple-inventory-power-stat-shortcut-t_2d1c7fbd`

---

## 1. 變更概述

1. **MapleInventory (`game/scripts/ui/maple_inventory.gd`)**：
   - 宣告 `signal power_stat_requested()`。
   - 探索背包底欄 `GridBottomBar` 新增『前往戰力』快捷按鈕 `BtnGoPowerStat`。
   - 尺寸與熱區：`custom_minimum_size = Vector2(120, 48)`（寬度 >= 120px，高度 >= 48px）。
   - 樣式：果凍底厚度 5px，圓角 18px，配色多巴胺金黃（`COLOR_GOLD #FFD028`），文字深藍紫（`COLOR_TEXT_DARK #1F1A3A`），字級 16px，粉圓體字型，100% 零系統 Emoji。
   - 點擊連動：點擊觸發 `_on_go_power_stat_pressed()`，發射 `power_stat_requested` 與 `closed` 訊號，自動關閉背包並通知大廳直通開啟 `PowerStatDialog`。
   - 提供存取器：`get_go_power_stat_button() -> Button` 與 `get_bag_go_power_stat_button() -> Button`。

2. **MobileLobby (`game/scripts/ui/mobile_lobby.gd`)**：
   - 在 `open_maple_inventory()` 連接 `power_stat_requested` 訊號，收到時調用 `open_power_stat_dialog()`。
   - 在 `open_power_stat_dialog()` 連接 `inventory_requested` 訊號，收到時調用 `open_maple_inventory()`。

3. **PowerStatDialog (`game/scripts/ui/power_stat_dialog.gd`)**：
   - 宣告 `signal inventory_requested()`。
   - 底部按鈕列 `BottomBar` 新增『前往背包』快捷果凍按鈕 `BtnGoInventory`（尺寸 140x48px，熱區 >= 48px，薄荷綠果凍底 5px）。
   - 點擊觸發 `_on_go_inventory_pressed()`，發射 `inventory_requested` 與 `closed` 訊號，關閉總覽並返回探索背包，形成完整的雙向快捷閉環。
   - 提供存取器：`get_go_inventory_button() -> Button`。

4. **六語系在地化 (i18n)**：
   - 新增 `inventory.btn_go_power_stat` 與 `power_stat.btn_go_inventory` 鍵值至六語系字典：
     - `zh_TW`: 前往戰力 / 前往背包
     - `zh_CN`: 前往战力 / 前往背包
     - `en`: Go to Stats / Go to Inventory
     - `ja`: 戦力詳細へ / インベントリへ進む
     - `ko`: 전투력으로 이동 / 인벤토리로 이동
     - `es`: Ir a Estadísticas / Ir al Inventario

5. **測試與存證**：
   - 撰寫單元與整合驗收測試 `game/scripts/ui/test_maple_inventory_power_stat_shortcut.gd`。
   - 在 `xvfb-run opengl3` 實機環境下截取 9 張存證截圖至 `proofs/t_2d1c7fbd/`，SHA256 全部獨立不重複，經 Vision 驗證無破圖遮擋。

---

## 2. 驗證結果

```text
=======================================================
🎉 全部 MapleInventory 前往戰力快捷按鈕單元與閉環測試通過！
TEST_MAPLE_INVENTORY_POWER_STAT_SHORTCUT_OK
=======================================================
```

- `clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2d1c7fbd/bravesoul-game`：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞。
- 迴歸測試：`test_maple_inventory.gd`、`test_maple_inventory_sort.gd`、`test_maple_inventory_capacity.gd`、`test_power_stat_dialog_equip_shortcut.gd` 全綠。
