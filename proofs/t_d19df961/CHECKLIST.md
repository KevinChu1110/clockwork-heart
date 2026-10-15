# 《發條之心》WeaponSwapDialog 武器更換彈窗支援直通 PowerStatDialog 快捷按鈕 查驗清單與驗收報告 (t_d19df961)

- **任務代號**：`t_d19df961`
- **任務名稱**：🎮 遊戲開發｜WeaponSwapDialog 武器更換彈窗底欄新增『前往戰力』快捷果凍按鈕連動 PowerStatDialog
- **執行人員**：阿宏（sideworker）
- **審核人員**：小婷（sideqa）
- **工作分支**：`agent/20261015-weapon-swap-power-stat-shortcut-t_d19df961`
- **日期**：2026-10-15

---

## 驗收規範對照與查驗結果

| 驗收項目 | 規格要求 | 實作與查驗結果 | 審查判定 |
|---|---|---|---|
| **按鈕存在與佈局** | WeaponSwapDialog 底部操作按鈕列新增 `BtnGoPowerStat`「前往戰力」按鈕 | `BtnGoPowerStat` 位於底部操作列（與 `BtnGoForge`、`BtnBottomClose` 並列），佈局結構清晰 | **合格 (PASS)** |
| **手遊人體工學與多巴胺視覺** | 熱區尺寸 >= 100x48px，立體果凍厚底 5px，圓角 16px，多巴胺高飽和金黃色盤（#FFD028），深藍紫文字與描邊，零系統 Emoji | 按鈕尺寸 130x48px，StyleBoxFlat `border_width_bottom=5`，`corner_radius=16`，背景金黃 `COLOR_GOLD`，文字深藍紫 `COLOR_TEXT_DARK`，100% 零 Emoji | **合格 (PASS)** |
| **點擊連動開啟 PowerStatDialog** | 點擊 `BtnGoPowerStat` 發射 `power_stat_requested` 訊號並關閉 WeaponSwapDialog，連動開啟 PowerStatDialog | 點擊時依序發射 `power_stat_requested` 與 `closed`，呼叫 `queue_free()` 安全關閉彈窗；`MobileLobby` 監聽並呼叫 `open_power_stat_dialog()` 平滑開啟戰力屬性總覽 | **合格 (PASS)** |
| **按鈕存取器** | 提供 `get_go_power_stat_button() -> Button` | `weapon_swap_dialog.gd` 提供 `get_go_power_stat_button()` 存取器 | **合格 (PASS)** |
| **六語系 i18n 支援** | 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時切換，對齊 `ui.json` 鍵值 `weapon_swap.go_power_stat`，歐美非中文語系無中文殘留 | 六語系 `content/{loc}/ui.json` 與 `{loc}.json` 全數補齊，動態切換即時生效，en / ko / es 零 CJK 殘留 | **合格 (PASS)** |
| **單元與整合測試覆蓋** | 新增 `test_weapon_swap_power_stat_shortcut.gd` 覆蓋樣式規格、信號關閉、大廳連動與六語系 | 測試於 headless 模式 100% 跑綠，退出碼 0，無任何 SCRIPT ERROR | **合格 (PASS)** |
| **實機截圖存證** | 真實 OpenGL3 (xvfb) 渲染，存證截圖至 `proofs/t_d19df961/`，SHA256 互不相同，零破圖零截字 | 產出 3 張實機截圖，經 Vision 逐幀驗收無破圖、無截字、排版完美 | **合格 (PASS)** |

---

## 實機截圖存證清單 (OpenGL3 1280x720)

| 編號 | 檔名 | 說明 | 狀態/視覺檢驗 | SHA256 |
|---|---|---|---|---|
| 01 | `proof_01_weapon_swap_dialog_btn_go_power_stat.png` | WeaponSwapDialog 底部操作列新增金黃色「前往戰力」立體果凍按鈕（`BtnGoPowerStat`，130x48px，厚底 5px，圓角 16px） | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `096f444bd838` |
| 02 | `proof_02_power_stat_dialog_opened.png` | 點擊「前往戰力」後成功發射 `power_stat_requested` 信號，平滑關閉更換彈窗並連動大廳 `MobileLobby` 開啟戰力屬性總覽彈窗（`PowerStatDialog`） | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `0459f0e582b6` |
| 03 | `proof_03_weapon_swap_power_stat_en.png` | 英文語系 (`en`) 下 `WeaponSwapDialog`：快捷按鈕顯示「Go to Stats」，排版自然無截字無溢出 | ✓ 無破圖 / ✓ 零Emoji / ✓ 零截字 | `ccc2f1089bb7` |

---

## 常見退回自查清單對照 (Clock Review Checklist)

1. **測試與證據**：
   - [x] 驗證截圖存證確實對齊驗收項目，連續截圖 SHA256 獨立不重複（096f444bd838 / 0459f0e582b6 / ccc2f1089bb7）。
   - [x] 單元與整合測試穩定跑綠，無時序競爭，在無頭模式與有頭模式皆穩定通過。
   - [x] CHECKLIST.md 誠實記錄實機截圖現況，經 Vision 驗證無溢出破版。
2. **畫面與素材**：
   - [x] 實機截圖在窄螢幕與彈窗邊界下排版合理，按鈕尺寸 130x48px 符合人體工學（>= 48px），立體厚底 5px。
   - [x] 多巴胺鮮亮高飽和金黃色盤（#FFD028），文字深藍紫加粗（#1F1A3A），零系統 Emoji。
3. **程式與邏輯**：
   - [x] `WeaponSwapDialog` 發射 `power_stat_requested` 並安全關閉（`queue_free`），`MobileLobby` 接收並連動 `open_power_stat_dialog()`，無殘留彈窗。
4. **資料與文案**：
   - [x] 六語系在地化翻譯對齊既有字典規範，歐美語系無中文殘留。
5. **流程與交付**：
   - [x] 使用 `project_status.py` 同步專案狀態至「測試中」。
   - [x] 所有修改完整 commit 至分支 `agent/20261015-weapon-swap-power-stat-shortcut-t_d19df961`，工作區乾淨。
