# 《發條之心》PowerStatDialog 戰力屬性總覽三槽武器卡片支援點擊更換聯動 WeaponSwapDialog 查驗清單與驗收報告 (t_4fbba577)

- **任務代號**：`t_4fbba577`
- **任務名稱**：🎮 遊戲開發｜PowerStatDialog 戰力屬性總覽三槽武器卡片支援點擊更換聯動 WeaponSwapDialog
- **執行人員**：阿翔（sideworker2）
- **審核人員**：小婷（sideqa）
- **工作分支**：`agent/20261015-power-stat-weapon-swap-shortcut-t_4fbba577`
- **日期**：2026-10-15

---

## 驗收規範對照與查驗結果

| 驗收項目 | 規格要求 | 實作與查驗結果 | 審查判定 |
|---|---|---|---|
| **三槽卡片更換按鈕** | PowerStatDialog 的 WeaponLoadoutCard 三槽武器卡片（SlotCard_0/1/2）新增點擊交互與『更換』果凍按鈕 | 每個槽位卡片內建 `BtnSwapWeapon`「更換」果凍按鈕，卡片本身 `gui_input` 亦支援點擊交互 | **合格 (PASS)** |
| **手遊人體工學與多巴胺視覺** | 熱區尺寸 >= 48px（80x48px），多巴胺高飽和天藍色盤（#38A0FF），立體果凍厚底 4px，圓角 12px，零系統 Emoji | 按鈕尺寸 80x48px，StyleBoxFlat `border_width_bottom=4`，`corner_radius=12`，背景天藍 `COLOR_SKY`，文字奶油白加粗，100% 零 Emoji | **合格 (PASS)** |
| **點擊連動開啟 WeaponSwapDialog** | 點擊槽位卡片或按鈕發射 `weapon_swap_requested(slot_idx)` 訊號並關閉 PowerStatDialog，連動 MobileLobby 開啟 WeaponSwapDialog(slot_idx) | 點擊時發射 `weapon_swap_requested(slot_idx)` 與 `closed`，呼叫 `queue_free()` 安全關閉彈窗；`MobileLobby` 監聽並呼叫 `open_weapon_swap_dialog(slot_idx)` 開啟並鎖定對應槽位 | **合格 (PASS)** |
| **按鈕存取器** | 提供 `get_slot_card_button(slot_idx: int) -> Button` 存取器 | `power_stat_dialog.gd` 提供 `get_slot_card_button(slot_idx)` 存取器，精確取得 0/1/2 各槽位按鈕 | **合格 (PASS)** |
| **六語系 i18n 支援** | 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時切換，對齊 `ui.json` 鍵值 `power_stat.swap_weapon`，歐美非中文語系無中文殘留 | 六語系 `content/{loc}/ui.json` 與 `{loc}.json` 全數補齊，動態切換即時生效，en / es 零 CJK 殘留（英文顯示「Swap」） | **合格 (PASS)** |
| **單元與整合測試覆蓋** | 新增 `test_power_stat_weapon_swap_shortcut.gd` 覆蓋樣式規格、信號傳遞、大廳連動與六語系 | 測試於 `./tools/run_tests.sh` 100% 跑綠，退出碼 0，無任何 SCRIPT ERROR | **合格 (PASS)** |
| **實機截圖存證** | 真實 OpenGL3 (xvfb) 渲染，存證截圖至 `proofs/t_4fbba577/`，SHA256 互不相同，零破圖零截字 | 產出 3 張實機截圖，經 Vision 逐幀驗收無破圖、無截字、排版完美 | **合格 (PASS)** |

---

## 實機截圖存證清單 (OpenGL3 1280x720)

| 編號 | 檔名 | 說明 | 狀態/視覺檢驗 | SHA256 |
|---|---|---|---|---|
| 01 | `proof_01_power_stat_weapon_swap_shortcut_zh_tw.png` | 繁中語系下 PowerStatDialog 戰力屬性總覽：三槽武器卡片（首選武器、副手武器、絕技武器）各自具備藍色立體果凍「更換」按鈕（80x48px，厚底 4px，圓角 12px），排版工整有足夠安全邊距 | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `d29c33d7846e` |
| 02 | `proof_02_weapon_swap_dialog_opened.png` | 點擊槽位「更換」按鈕後成功發射 `weapon_swap_requested(0)` 信號，平滑關閉戰力總覽並連動大廳 `MobileLobby` 開啟武器更換彈窗（`WeaponSwapDialog`），選中首選武器槽位 | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `d538ef844e0f` |
| 03 | `proof_03_power_stat_weapon_swap_en.png` | 英文語系 (`en`) 下 PowerStatDialog：三槽武器卡片更換按鈕顯示「Swap」，副標題角色名顯示英文「Xiaobai」，卡片邊距舒適無截字 | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `f0d28841051e` |

---

## 常見退回自查清單對照 (Clock Review Checklist)

1. **測試與證據**：
   - [x] 驗證截圖存證確實對齊驗收項目，連續截圖 SHA256 獨立不重複（d29c33d7846e / d538ef844e0f / f0d28841051e）。
   - [x] 單元與整合測試穩定跑綠（`TEST_FILTER=test_power_stat_weapon_swap_shortcut ./tools/run_tests.sh` 通過）。
   - [x] CHECKLIST.md 誠實記錄實機截圖現況，經 Vision 驗證無溢出破版。
2. **畫面與素材**：
   - [x] 實機截圖在滾動與彈窗邊界下排版合理，按鈕尺寸 80x48px 符合人體工學（>= 48px），立體厚底 4px。
   - [x] 多巴胺鮮亮高飽和天藍色盤（#38A0FF），文字奶油白加粗，零系統 Emoji。
3. **程式與邏輯**：
   - [x] `PowerStatDialog` 發射 `weapon_swap_requested(slot_idx)` 並安全關閉（`queue_free`），`MobileLobby` 接收並連動 `open_weapon_swap_dialog(slot_idx)`，無殘留彈窗。
4. **資料與文案**：
   - [x] 六語系在地化翻譯對齊既有字典規範，歐美語系無中文殘留。
5. **流程與交付**：
   - [x] 使用 `project_status.py` 同步專案狀態至「測試中」。
   - [x] 所有修改完整 commit 至分支 `agent/20261015-power-stat-weapon-swap-shortcut-t_4fbba577`，工作區乾淨。
