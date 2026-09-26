# 戰鬥操作提示改觸控用語＋六語系 驗收證明 (battle-touch-prompt-i18n)

## 驗收規範對照 (review.md)
- **0-QA23 (目錄隔離)**：輸出檔案嚴格限定於 `proofs/battle-touch-prompt-i18n/`，無覆蓋或污染任何其他卡片的目錄。
- **0-QA24 (漢字與外語判定)**：日文「回避をタップ」「ロックをタップ」、韓文「회피 탭」「락온 탭」均對齊六語系 `ui.json`，非中文殘留。
- **0-QA25 (全景同步換語系)**：戰鬥全景包含頂欄敵我標籤、部位血條、底部日誌與右下操作按鈕，全部在切換語系時同步即時更新。

## 截圖清單
1. `proof_battle_touch_en.png`：英文觸控全景，日誌包含「The King's Cut... tap Dodge」，部位教學包含「Tap Lock」，零鍵盤鍵名，全英文 UI。
2. `proof_battle_touch_ja.png`：日文觸控全景，日誌包含「王者斬は受ければ反撃できる・火輪が光ったら回避をタップして跳べ」「ロックをタップ」，零鍵盤鍵名，全日文 UI。
3. `proof_battle_touch_zh_TW.png`：繁中觸控全景，日誌包含「王者斬要擋，擋住就能反擊 · 火圈亮起後點閃避跳開」「點鎖定」，零鍵盤鍵名。

## 測試結果
- `test_battle_touch_prompt_i18n.gd` 通過 (TEST_BATTLE_TOUCH_PROMPT_I18N_OK)
- `test_enemy_name_i18n.gd` 通過 (TEST_ENEMY_NAME_I18N_OK)
- `test_battle_part_break_i18n.gd` 通過 (TEST_BATTLE_PART_BREAK_I18N_OK)
- `test_qa_battle_name_fixes.gd` 通過 (TEST_QA_BATTLE_NAME_FIXES_OK)
- 全部 34 支 i18n 測試 100% 通過 (34/34 TESTS PASSED)
