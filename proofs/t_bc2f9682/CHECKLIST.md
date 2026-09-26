# 驗收證明 · 每日發條做完若還有巨偶次數就接到停擺巨偶 (t_bc2f9682)

- 任務 ID: `t_bc2f9682`
- 執行者: 阿宏 (sideworker)
- 規範參照: `AGENTS.md` (驗證階梯), `review.md` (0-QA5, 0-QA23, 0-QA25, 0-QA26)

## 驗收產出清單 (Framebuffer 擷取，零 PIL 假圖)

| 編號 | 檔案名稱 | 說明 | 視覺檢查項 | 結論 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_windup_done_with_colossus.png` | 每日發條完成畫面（有巨偶次數 3/3） | 看得見暖橘果凍厚底鈕「前往停擺巨偶」與薄荷綠「前往出征」，鈕高 >= 50px，零 Emoji | **通過 (PASS)** |
| 02 | `proof_windup_done_no_colossus.png` | 每日發條完成畫面（巨偶次數 0/3） | 「前往停擺巨偶」按鈕正確隱藏，原本「前往出征」按鈕維持正常顯示 | **通過 (PASS)** |

## 實機測試指令與結果

1. **單元測試 (入口切換、按鈕狀態、六語系即時連動)**
   ```bash
   TEST_FILTER=test_windup_to_colossus ./tools/run_tests.sh
   ```
   - 結果: `TEST_WINDUP_TO_COLOSSUS_OK` (通過)

2. **既有測試回歸**
   ```bash
   TEST_FILTER=windup ./tools/run_tests.sh
   TEST_FILTER=colossus ./tools/run_tests.sh
   TEST_FILTER=test_mobile_lobby ./tools/run_tests.sh
   TEST_FILTER=test_dialog_contrast ./tools/run_tests.sh
   ```
   - 結果: 全部通過，無 SCRIPT ERROR。
