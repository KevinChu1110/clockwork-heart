# 探索背包底欄新增『前往戰力』快捷果凍按鈕連動PowerStatDialog 驗收存證 (t_2d1c7fbd)

## 任務目標
1. 在 MapleInventory (`game/scripts/ui/maple_inventory.gd`) 探索背包底欄（`GridBottomBar`）新增『前往戰力』（`BtnGoPowerStat`）快捷果凍按鈕。
2. 點擊後發射 `power_stat_requested` 與 `closed` 訊號並關閉背包，通知 MobileLobby (`game/scripts/ui/mobile_lobby.gd`) 開啟 PowerStatDialog 戰力屬性總覽。
3. 在 PowerStatDialog 底欄新增『前往背包』（`BtnGoInventory`），點擊後發射 `inventory_requested` 訊號並返回探索背包，確保雙向快捷閉環。
4. 按鈕尺寸與視覺規範：
   - 按鈕尺寸寬度 >= 120px、高度 48px（符合熱區 >= 48px），底部果凍厚度 5px，圓角 18px。
   - 多巴胺金黃鮮亮高飽和色盤（#FFD028），文字深藍紫（#1F1A3A），字級 16px 開源粉圓體，100% 零系統 Emoji。
5. 提供存取器 `get_go_power_stat_button()` 與 `get_bag_go_power_stat_button()`。
6. 支援六語系 i18n 即時刷新（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），歐美語系零 CJK 殘留。
7. 撰寫單元與整合測試 `test_maple_inventory_power_stat_shortcut.gd`，在非 headless (xvfb) 下產出實機截圖存證，執行 `clock-check` 確認無警告。
8. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，背包底欄與 PowerStatDialog 底欄三按鈕間距合理無擁擠穿模，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 120x48px（熱區 >= 48px），文字採深藍紫 #1F1A3A 搭配金黃底 #FFD028，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2d1c7fbd/bravesoul-game` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 9 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game("rabbit")`，時序等待幀數控制在 3~5 幀，穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_maple_inventory_power_stat_shortcut`、`test_maple_inventory`、`test_maple_inventory_sort`、`test_maple_inventory_capacity`、`test_power_stat_dialog_equip_shortcut` 等測試全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 發射 `closed` 訊號並關閉背包，大廳連動開啟 `PowerStatDialog`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與雙向閉環 | ✅ 已檢查 | 背包底欄點擊『前往戰力』開啟戰力總覽；戰力總覽點擊『前往背包』返回探索背包，閉環流暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已新增 `inventory-power-stat-shortcut` 並更新狀態為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261014-maple-inventory-power-stat-shortcut-t_2d1c7fbd` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_maple_inv_btn_go_power_stat.png` | 繁中探索背包底欄：容量膠囊、一鍵整理旁展示金黃果凍按鈕『前往戰力』(120x48px) | 1280x720 | `d795b293e92c46e286ece404987d0f36789d83e920f5f15ea0292a3242ba8f09` |
| 02 | `proof_02_zh_TW_power_stat_dialog_opened.png` | 點擊前往戰力：直通開啟 PowerStatDialog 戰力屬性總覽，底欄展示前往整頓、前往背包與確定 | 1280x720 | `78ecaf58282fb19e1ebaf8601e0d1a6893a39803dcbe69a0f7c89b89e97b9b4b` |
| 03 | `proof_03_zh_TW_loop_back_to_maple_inventory.png` | 雙向閉環：從戰力總覽點擊『前往背包』安全關閉總覽返回探索背包 | 1280x720 | `e6307ff5c7fa6e8e7c4b3a7db8bc76cf7168f92865fb5be260fee8674bc20679` |
| 04 | `proof_locale_zh_TW_maple_inv_power_stat_btn.png` | 繁中語系切換刷新：『前往戰力』 | 1280x720 | `6787ac4e8d73d94c573ad53630551127855cf362be5d8e57a57c0d01622b5780` |
| 05 | `proof_locale_zh_CN_maple_inv_power_stat_btn.png` | 簡中語系切換刷新：『前往战力』 | 1280x720 | `bae4435d67e180ad32f8c30428e1d7303df67f5dc13b53436ce185183b9879ca` |
| 06 | `proof_locale_en_maple_inv_power_stat_btn.png` | 英文語系切換刷新：\"Go to Stats\"，零 CJK 殘留 | 1280x720 | `ac94f8e3388f2083b3e0b6c5de70741e27a61906d90272bb73680a526d8a40f0` |
| 07 | `proof_locale_ja_maple_inv_power_stat_btn.png` | 日文語系切換刷新：『戦力詳細へ』 | 1280x720 | `19f59f03cc76e0f9c1e33f54bfd34072f03598f4be6ddcb6bd2eef6766375a4e` |
| 08 | `proof_locale_ko_maple_inv_power_stat_btn.png` | 韓文語系切換刷新：『전투력으로 이동』 | 1280x720 | `2602a6ea13630f2325ac5b5bafb510a57c4964c842a78c1a4a37204684dcaef7` |
| 09 | `proof_locale_es_maple_inv_power_stat_btn.png` | 西文語系切換刷新：\"Ir a Estadísticas\"，零 CJK 殘留 | 1280x720 | `b4ac46dce89f480995c5172a95ebbe01668ec7d13eb04e8f170ce08cfce7d265` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_2d1c7fbd/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：Exit 0

# 3. 功能單元與整合測試
godot --path game --headless -s res://scripts/ui/test_maple_inventory_power_stat_shortcut.gd
# 輸出：TEST_MAPLE_INVENTORY_POWER_STAT_SHORTCUT_OK (Exit 0)

# 4. 關聯單元與雙向迴歸測試
godot --path game --headless -s res://scripts/ui/test_maple_inventory.gd
# 輸出：MAPLE_INVENTORY_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_maple_inventory_sort.gd
# 輸出：MAPLE_INVENTORY_SORT_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_maple_inventory_capacity.gd
# 輸出：MAPLE_INVENTORY_CAPACITY_OK (Exit 0)
godot --path game --headless -s res://scripts/ui/test_power_stat_dialog_equip_shortcut.gd
# 輸出：TEST_POWER_STAT_EQUIP_SHORTCUT_OK (Exit 0)

# 5. 實機渲染截圖存證
xvfb-run -a -s "-screen 0 1280x720x24" godot --path game -s res://scripts/ui/test_maple_inventory_power_stat_shortcut.gd
# 輸出：9 張獨立唯一截圖成功產出，雜湊無碰撞
```
