# 審查檢查表 · 章節教學對白鍵盤用語改觸控＋六語系 (chapter-tutorial-touch)

依據規範：AGENTS.md, CLAUDE.md, review.md (0-QA15, 0-QA23, 0-QA24, 0-QA25)

## 1. 工件與截圖存證 (0-QA23)
- 本輪專屬目錄：`proofs/chapter-tutorial-touch/`（未覆蓋或污染任何其他任務的 proof 目錄）。
- 實機全景截圖：
  1. `proof_tutorial_touch_en.png`：英文觸控全景，對話框顯示「Always parry the King's Cut. The fire ring flashes before it lands—tap Dodge on the flash.」，提示「▼ Tap to continue」，背景與 HUD 全英文（You, Foe, Titan Overseer Leo, Locked... Tap Lock to switch）。
  2. `proof_tutorial_touch_ja.png`：日文觸控全景，對話框顯示「王者斬は必ず受けろ。火輪は光ってから落ちる。光ったら回避をタップ。」，提示「▼ タップで進む」，背景與 HUD 全日文（味方, 敵, 守護タイタン・レオ, 捕捉... ロックタップで切替）。
  3. `proof_tutorial_touch_zh_TW.png`：繁中觸控全景對照，對話框顯示「王者斬必擋。火圈先亮再落，亮了點閃避。」，提示「▼ 點一下繼續」，背景與 HUD 全繁中。

## 2. 截圖差異性與有效性 (0-QA15)
- 各圖檔案大小與內容不同，經 Vision 逐張開圖審核通過，無假截圖。

## 3. 語系與視覺規範 (0-QA24, 0-QA25)
- 零系統 emoji：全文全介面無系統 emoji。
- 零未翻譯殘留：英文截圖零中文字殘留；日文「王者斬」「守護タイタン・レオ」經查對齊 `ja/ui.json` 既定譯名。
- 背景全域同步換語系 (0-QA25)：對話框後方戰鬥畫面之左右陣營標籤、角色名、狀態名、部位鎖定選單皆隨語系即時切換。

## 4. 測試驗證
- 單元測試：`TEST_FILTER=test_chapter_tutorial_touch_i18n ./tools/run_tests.sh` 通過 (PASS)。
- 既有回歸：`TEST_FILTER=test_battle_touch_prompt_i18n ./tools/run_tests.sh` 通過 (PASS)。
- 既有回歸：`TEST_FILTER=test_cutscene_hint_i18n ./tools/run_tests.sh` 通過 (PASS)。
- 既有回歸：`TEST_FILTER=test_enemy_name_i18n ./tools/run_tests.sh` 通過 (PASS)。
- 冒煙測試：`godot --path game --headless --quit-after 3` 0 錯誤。
