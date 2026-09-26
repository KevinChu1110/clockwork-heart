# 任務存證與驗收檢查表 (t_57fe8e45)

- 任務 ID: t_57fe8e45
- 任務名稱: 🎮 遊戲開發｜停擺巨偶勝場給當前等級百分比經驗（不改秒數）
- 執行角色: 阿宏（sideworker）
- 日期: 2026-09-27

## 驗收項目逐條檢核

1. **勝場給經驗、敗場不給經驗**
   - 停擺巨偶三張卡（失控發條獅 Lv12／霧鐘提線人偶 Lv20／黑鏽蒸氣巨象 Lv28）：
     - 勝場正常發放經驗並即時加進玩家 GameState.xp。
     - 敗場不給經驗、不給五槽機芯部件，但開戰消耗 1 次當日次數。
   - 單元測試：`test_colossus_exp.gd` 實測 Lv12 勝場獲得 82 經驗；敗場經驗維持 0 增加、背包機芯數維持 0 增加、當日次數正常扣除。

2. **經驗量約為當前等級升級所需之 20%（允許正負 2% 取整）**
   - 依公式 `Formulas.colossus_xp(player_level, level_cap)` 計算：
     - Lv 1: 升級所需 65，給予 13（20.00%）
     - Lv 5: 升級所需 177，給予 35（19.77%）
     - Lv 10: 升級所需 340，給予 68（20.00%）
     - Lv 12: 升級所需 412，給予 82（19.90%）
     - Lv 18: 升級所需 652，給予 130（19.94%）
     - Lv 20: 升級所需 740，給予 148（20.00%）
     - Lv 25: 升級所需 977，給予 195（19.96%）
     - Lv 28: 升級所需 1132，給予 226（19.96%）
     - Lv 29: 升級所需 1185，給予 237（20.00%）
   - 全區間精確落在 18% ~ 22% 區間內。

3. **未滿等才加，已達第一季 Lv30 上限不加**
   - 當 `player_level >= 30`（DEFAULT_LEVEL_CAP）時，`Formulas.colossus_xp()` 回傳 0。
   - 滿等打贏巨偶時，經驗增加量為 0，`GameState.xp` 零漂移。
   - 結算卡片顯示「經驗 +0（已達上限）」。

4. **一般關卡經驗公式未被改動**
   - 一般出征 `Formulas.field_xp(max_hp, skirmish_wins)` 與獵場 `Formulas.arena_xp(max_hp, practice)` 數值維持原樣，未遭任何改動。
   - `test_colossus_exp.gd` 包含斷言鎖定。

5. **沿用既有結算卡，六語系即時切換與零系統 Emoji**
   - `BattleVictoryDialog`（結算卡片）增設 `ExpRewardPanel` 與 `ExpLabel`（字級 16px、多巴胺暖橘色、圓角 14px 內嵌面板）。
   - 支援 zh_TW、zh_CN、en、ja、ko、es 六語系：
     - zh_TW: `戰鬥經驗` · `經驗 +%d` / `經驗 +0（已達上限）`
     - zh_CN: `战斗经验` · `经验 +%d` / `经验 +0（已达上限）`
     - en: `Combat EXP` · `EXP +%d` / `EXP +0 (Max Level)`
     - ja: `戦闘経験値` · `経験値 +%d` / `経験値 +0（上限到達）`
     - ko: `전투 경험치` · `경험치 +%d` / `경험치 +0 (최대 레벨)`
     - es: `EXP de combate` · `EXP +%d` / `EXP +0 (Nivel máx.)`
   - 全介面 100% 零系統 Emoji。

6. **時間模型硬限制**
   - ATB、攻速、前搖、命中時間模型常數完全鎖死未動。

7. **實機截圖存證 (0-QA5 / 0-QA26 Framebuffer)**
   - `proofs/t_57fe8e45/proof_colossus_battle_running.png`: 橫屏巨偶戰鬥中實機截圖。
   - `proofs/t_57fe8e45/proof_colossus_battle_victory.png`: 巨偶勝場結算實機截圖（清晰可見「戰鬥經驗 經驗 +82」、【金階】發條發電機、立即裝備／收下完成按鈕，零 Emoji，零文字溢出）。
   - 經 Vision Analyze 逐項檢證通過。

8. **測試結果**
   - `TEST_FILTER=test_colossus_exp ./tools/run_tests.sh`: TEST_COLOSSUS_EXP_OK
   - `TEST_FILTER=colossus ./tools/run_tests.sh`: 全部通過 (3/3: test_colossus_battle, test_colossus_daily, test_colossus_exp)
   - `TEST_FILTER=core_battle_drop ./tools/run_tests.sh`: CORE_BATTLE_DROP_OK (1/1)
