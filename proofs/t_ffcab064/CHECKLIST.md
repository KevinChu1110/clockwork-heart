# 停擺巨偶：每日3次次數與出征入口骨架 驗收報告 (t_ffcab064)

## 任務資訊
- **卡號**：`t_ffcab064`
- **標題**：🎮 遊戲開發｜停擺巨偶：每日3次次數與出征入口骨架（不開戰、不產圖）
- **執行人**：側案處工程師 阿翔 (`sideworker2`)
- **審查人**：測試 小婷 (`sideqa`)

---

## 驗收項目清單

| 編號 | 檢驗項目 | 規範標準 | 實測結果 | 判定 |
|:---:|:---|:---|:---|:---:|
| 1 | **大廳出征入口** | 出征分頁可見「停擺巨偶」入口與今日剩餘次數 (上限 3) | 頂部模式切換列顯示 `停擺巨偶 · 今日剩餘: 3/3`，選中時呈高亮橘色果凍底 | **PASS** |
| 2 | **三張占位卡片** | 僅失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏑蒸汽巨象 Lv28，零自創第四隻 | 依序渲染三張既有出征卡 chrome，等級分別為 12、20、28 | **PASS** |
| 3 | **每日次數模擬** | 同日呼叫 3 次後第 4 次被拒，換日（隔日 00:00）自動重置為 3 次 | 單元測試 `test_colossus_daily.gd` 驗證同日第 4 次拒絕碼 `daily_limit_reached`，隔日重置為 3 | **PASS** |
| 4 | **按鈕與彈窗規範** | 滿 3 次後按鈕顯示「明天再來」，點擊跳出提示彈窗，沿用既有體力不足彈窗樣式與果凍鈕，不准新畫面 | 按鈕動態切換為「明天再來」，點擊彈出遮罩、奶油米白底、果凍確定鈕彈窗 | **PASS** |
| 5 | **手遊操作熱區** | 橫屏單手點得到，熱區 $\ge$ 48px | 入口按鈕 380×50px、卡片按鈕 145×52px，熱區均 $\ge$ 48px | **PASS** |
| 6 | **硬限制守護** | 嚴禁改動 ATB、攻速、前搖、命中等時間模型常數 | `verify_time_model_locked()` 驗證 atb_max=100.0, strike_duration=0.08, telegraph=1.85 零漂移 | **PASS** |
| 7 | **存檔版號升級** | GameState.VERSION 升級至 10，SaveMigration CURRENT 10，支援舊存檔自動補齊欄位 | `test_save_slots.gd` 56 個欄位 round-trip 與 1→10 升級步驟全數 PASS | **PASS** |
| 8 | **六語系即時刷新** | 支援 zh_TW, zh_CN, en, ja, ko, es，切換語系即時刷新，零系統原生 Emoji | 六語系字典鍵值齊全，`0-QA25` 即時連動刷新，零系統 Emoji | **PASS** |
| 9 | **實機截圖證明** | 採用 Godot 原生 Viewport Framebuffer 截圖 (0-QA5 / 0-QA26)，存放於本輪目錄 (0-QA23) | 產出 `proof_colossus_sortie.png` 與 `proof_colossus_limit_dialog.png` | **PASS** |

---

## 實機截圖證明檔案

1. `proofs/t_ffcab064/proof_colossus_sortie.png`
   - 出征分頁停擺巨偶入口按鈕、今日剩餘 3/3 次數、三張占位卡片全景。
2. `proofs/t_ffcab064/proof_colossus_limit_dialog.png`
   - 耗盡 3 次後按鈕切換「明天再來」，點擊觸發提示彈窗全景。

---

## 測試指令與輸出紀錄

```bash
# 1. 單元測試
TEST_FILTER=colossus ./tools/run_tests.sh
# 輸出: ok test_colossus_daily TESTS PASSED (1/1)

# 2. 存檔遷移測試
TEST_FILTER=save_slots ./tools/run_tests.sh
# 輸出: ok test_save_slots SAVE_SLOTS_OK TESTS PASSED (1/1)

# 3. 出征卡六語系連動測試
TEST_FILTER=lobby_sortie ./tools/run_tests.sh
# 輸出: ok test_lobby_sortie_i18n LOBBY_SORTIE_I18N_OK TESTS PASSED (1/1)
```
