# t_203197f2 實機截圖與合入驗收清單

## 驗收項目檢核

- **任務標題**：🤖 平台與維運｜把已過審的巨偶推薦等級閘門與發條格擋合進主線
- **來源分支與卡片**：
  1. `t_1b77ff75`（停擺巨偶出征卡顯示推薦等級，低於王等級10級不能進）commit `f74c4b47`
  2. `t_efaa460d`（停擺巨偶蓄力必殺用既有格擋窗，按鈕寫發條格擋）commit `0c808c38` / `fc9625dc`
- **合入主線狀態**：乾淨合入，六語系 i18n 衝突已平滑合併解決，無頭冒煙 0 errors。
- **測試結果**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
  - `TEST_FILTER=colossus ./tools/run_tests.sh`：7/7 PASS
  - `TEST_FILTER=i18n ./tools/run_tests.sh`：35/35 PASS
  - `TEST_FILTER=parry ./tools/run_tests.sh`：2/2 PASS
  - `TEST_FILTER=mobile_lobby ./tools/run_tests.sh`：1/1 PASS
  - `python3 tools/verify_colossus_i18n_equality.py`：六語系 enemy.json 與 ui.json 100% 同名
  - `python3 tools/check_player_text.py`：PLAYER_TEXT_OK

## 實機截圖存證清單 (1280x720 Framebuffer 截取)

| 編號 | 檔案名稱 | 截圖內容 | 關鍵元素檢驗 | 系統 Emoji | 審核結果 |
|---|---|---|---|---|---|
| 01 | `proof_01_gate_locked_zh_tw.png` | 繁中（zh_TW）Lv1 停擺巨偶出征卡 | 顯示「推薦 Lv.12/20/28」，黑鏽蒸氣巨象出征鈕灰掉顯示「需達 Lv.18」，紅字「未達 Lv.18 不可出征」 | 零 | **通過 (PASS)** |
| 02 | `proof_02_gate_locked_en.png` | 英文（en）Lv1 停擺巨偶出征卡 | 顯示「Rec. Lv.12/20/28」，Black-Rust Steam Colossus 按鈕灰掉顯示「Requires Lv.18」，說明「Requires Lv.18 to sortie」，排版無截字 | 零 | **通過 (PASS)** |
| 03 | `proof_03_zh_colossus_windup_btn.png` | 繁中（zh_TW）巨偶蓄力必殺格擋窗 | 右下按鈕切換為「發條格擋」（高 72px >= 50px），中央倒數「格擋時機！」與「現在按 J 或點發條格擋！」 | 零 | **通過 (PASS)** |
| 04 | `proof_04_zh_parry_success.png` | 繁中（zh_TW）完美格擋成功 | 中央金色大字「完美格擋」，我方 HP 150/150 無傷，敵方扣 42 傷害，戰鬥日誌顯示完美格擋 | 零 | **通過 (PASS)** |
| 05 | `proof_05_en_colossus_windup_btn.png` | 英文（en）巨偶蓄力必殺格擋窗 | 右下按鈕切換為「Windup Parry」，中央倒數與英文提示，排版整齊無截字 | 零 | **通過 (PASS)** |
| 06 | `proof_06_en_parry_success.png` | 英文（en）完美格擋成功 | 我方 HP 150/150 無傷，敵方扣 42 傷害，英文戰鬥日誌與回饋正常 | 零 | **通過 (PASS)** |

## 規範遵從檢驗

- [x] **0-QA5 / 0-QA26**：真遊戲 Framebuffer 直接擷取，非 PIL 繪製或手繪假圖。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_203197f2/`，不污染其他任務目錄。
- [x] **0-QA27**：第三隻巨偶中文名嚴格對齊「黑鏽蒸氣巨象」，六語系 `enemy.json` 與 `ui.json` 100% 同名一致。
- [x] **0-QA28**：玩家可見字（推薦等級、不可出征、發條格擋、倒數提示等）全數納入六語系翻譯層。
- [x] **硬限制**：未修改戰鬥秒數、ATB、怒氣、前搖（1.85s / 0.85s 維持原值）；無新增道具；全介面零系統 Emoji。
