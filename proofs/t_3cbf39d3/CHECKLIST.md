# 任務 t_3cbf39d3 自檢清單（停擺巨偶勝場機芯色階權重高於普通關卡）

## 1. 規範與實作自檢
- [x] 普通關卡勝場維持現有八色階掉落權重（灰 50, 白 450, 橘 240, 藍 150, 紫 60, 金 30, 綠 15, 紅 5），完全未改動既有設定值。
- [x] 停擺巨偶勝場改走獨立權重（灰 20, 白 180, 橘 200, 藍 250, 紫 180, 金 100, 綠 50, 紅 20，合計 1000）：
  - 紫＋金＋綠＋紅合計 350 (35.0%)，明顯高於普通關卡合計 110 (11.0%)，提升逾 3 倍。
  - 白 (180)／橘 (200) 仍可掉落。
  - 灰權重 (20) 低於普通關卡 (50)，灰權重不准比普通關卡高。
- [x] 同一套 roll 函式可傳來源（`source: String = "stage"` 或 `"colossus"`），未複製第二套掉落系統。
- [x] 零新道具、未改戰鬥秒數／ATB／怒氣／命中（`BALANCE.md` §5 鎖版合規）。
- [x] 中文名與設計文件逐字對齊（黑鏽蒸氣巨象），六語系 ui.json 與 enemy.json 同名（0-QA27 通過）。
- [x] 全域零系統 Emoji。

## 2. 期望色階指數證明（固定種子 20260927，3000 次模擬）
- 普通關卡期望色階指數：1.868（以白/橘階為主，高階佔比 10.2%）
- 停擺巨偶期望色階指數：2.953（以藍/紫/金階為主，高階佔比 34.0%）
- 結論：巨偶期望色階指數 (2.953) > 普通關卡 (1.868)，巨偶出高階機率顯著提升。

## 3. 無頭測試
- `TEST_FILTER=core ./tools/run_tests.sh`: 4/4 PASS
  - `test_core_battle_drop`: CORE_BATTLE_DROP_OK
  - `test_core_color_tiers`: CORE_COLOR_TIERS_OK
  - `test_core_combat_stats`: CORE_COMBAT_STATS_OK
  - `test_core_slots_ui`: TEST_CORE_SLOTS_UI_OK
- `TEST_FILTER=colossus ./tools/run_tests.sh`: 6/6 PASS
  - `test_colossus_defeat_hint`: TEST_COLOSSUS_DEFEAT_HINT_OK
  - `test_colossus_battle`: TEST_COLOSSUS_BATTLE_OK
  - `test_colossus_daily`: TEST_COLOSSUS_DAILY_OK
  - `test_colossus_exp`: TEST_COLOSSUS_EXP_OK
  - `test_colossus_part_scrap`: TEST_COLOSSUS_PART_SCRAP_OK
  - `test_windup_to_colossus`: TEST_WINDUP_TO_COLOSSUS_OK

## 4. 實機截圖 (0-QA5 / 0-QA26 / 0-QA23)
- `proof_stage_victory.png`: 普通關卡勝場結算（色階為白階）
- `proof_colossus_victory.png`: 停擺巨偶勝場結算（色階為金階，附經驗與鐵屑）
- `proof_colossus_victory_en.png`: 英文版勝場結算查截字（無任何溢出截斷、零系統 emoji）
- `proof_colossus_victory_ja.png`: 日文版勝場結算查截字（無任何溢出截斷、零系統 emoji）
