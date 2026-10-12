# 戰力總覽快捷與背包一鍵整理合進主線後的全站回歸驗收清單 (t_262e5894)

## 任務目標
1. 驗證 t_a9a4b310（戰力屬性總覽快捷與背包一鍵整理）合入 main 分支後的全站穩定性與功能運作。
2. 執行迴歸測試確認 123+ 支測試全綠，0 失敗，0 SCRIPT ERROR。
3. 執行自動化截圖腳本產生實機驗證截圖存證至 proofs/t_262e5894/。
4. 執行 clock-check 與 clock-check --live 確認官網與遊戲無破圖、無死連結、無舊 IP/名詞殘留。

## 查驗項目與執行結果

### 1. 功能與規格回歸驗證
- [x] **PowerStatDialog 雙快捷跳轉按鈕**：
  - 寶石卡片內包含『前往工坊』(`BtnGoWorkshop`)，招式卡片內包含『前往心法』(`BtnGoSkill`)。
  - 尺寸 84x36px，熱區 >= 48px，果凍厚底 4px。
  - 多巴胺色盤：前往工坊暖橘 (`#FFA010`)，前往心法天藍 (`#38A0FF`)，零系統 Emoji。
  - 點擊後正確發射 `workshop_requested` 與 `skill_requested` 信號並關閉彈窗，大廳成功連動打開 `GemWorkshopDialog` 與 `SkillDialog`。
  - 繁中 (zh_TW)、英文 (en)、簡中 (zh_CN)、日文 (ja)、韓文 (ko)、西文 (es) 六語系無缺失、無未翻譯 key。
- [x] **MapleInventory 探索背包一鍵整理**：
  - 背包網格底部中央金黃果凍厚底按鈕『一鍵整理』(`BtnSortItems`)，尺寸 120x48px，熱區 >= 48px，果凍底厚度 5px，底色金黃 (`#FFD028`)。
  - 點擊後調用 `sort_items()`，依裝備/寶石/消耗品/材料分類優先序及品質降序排列，即時刷新格子顯示並保留選取與連動詳情卡。
  - 六語系支援：zh_TW (一鍵整理)、en (Auto-Sort)、zh_CN (一键整理)、ja (一括整理)、ko (자동 정리)、es (Organizar)。

### 2. 實機渲染存證截圖 (1280x720, OpenGL3)
| 截圖檔名 | 說明 | 規格與狀態 | SHA256 雜湊值 (前 12 碼) |
|---|---|---|---|
| `proof_01_power_stat_shortcuts_zh_tw.png` | PowerStatDialog 繁中渲染（滾動展示前往工坊/前往心法雙果凍按鈕） | 1280x720 PNG | `21ae68b6b9da` |
| `proof_02_power_stat_shortcuts_en.png` | PowerStatDialog 英文切換（Go to Workshop / Go to Skills 無截字溢出） | 1280x720 PNG | `6d59736dd2a2` |
| `proof_03_lobby_gem_workshop.png` | 大廳點擊前往工坊連動開啟 GemWorkshopDialog（手藝工坊·寶石熔煉） | 1280x720 PNG | `79d33e21ebaf` |
| `proof_04_lobby_skill_dialog.png` | 大廳點擊前往心法連動開啟 SkillDialog（旅途·招式心法） | 1280x720 PNG | `66c10fbdbca7` |
| `proof_05_inventory_before_sort.png` | 探索背包一鍵整理前未排序狀態（展示打亂道具與金黃厚底 BtnSortItems） | 1280x720 PNG | `db6ded42afc2` |
| `proof_06_inventory_after_sort.png` | 探索背包點擊一鍵整理後排序狀態（裝備/寶石/消耗品/材料分類與品質降序排列） | 1280x720 PNG | `c809da697f70` |
| `proof_07_inventory_sort_en.png` | 探索背包英文語系切換（Auto-Sort 按鈕與全英文介面清晰無截斷） | 1280x720 PNG | `0ef2482b1b3a` |

* 7 張存證截圖經 SHA256 雜湊互異性檢驗，全數互不相同，無黑屏、無重複存證，經 Vision 逐張審查無任何穿模破圖。

### 3. 無頭測試與合規斷言
- [x] `test_power_stat_shortcuts.gd`：PASS (`TEST_POWER_STAT_SHORTCUTS_OK`)。
- [x] `test_power_stat_dialog_equip_shortcut.gd`：PASS (`TEST_POWER_STAT_EQUIP_SHORTCUT_OK`)。
- [x] `test_power_stat_dialog.gd`：PASS (`TEST_POWER_STAT_DIALOG_OK`)。
- [x] `test_maple_inventory.gd`：PASS (`MAPLE_INVENTORY_OK`)。
- [x] `test_maple_inventory_sort.gd`：PASS (`MAPLE_INVENTORY_SORT_OK`)。
- [x] `test_vault_double_claim.gd` / `test_lobby_vault_bubble.gd` / `test_idle_clockwork_vault.gd`：PASS。
- [x] `test_bag_workshop_shortcut.gd` / `test_bag_weapon_forge_shortcut.gd`：PASS。
- [x] `action_poses` 測試套件 (52/52 支) 全部通過。
- [x] `skeleton` 骨架測試套件 (54/54 支) 全部通過。
- [x] 全站迴歸測試累積通過 123+ 支測試（100% 全綠，0 失敗，0 SCRIPT ERROR）。
- [x] 無頭冒煙測試 `godot --path game --headless --quit-after 3`：0 報錯、0 SCRIPT ERROR。
- [x] `clock-check .` 檢查：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。
- [x] `clock-check --live` 檢查：`✅ 官網 14 頁都打得開，沒有舊名詞`。
