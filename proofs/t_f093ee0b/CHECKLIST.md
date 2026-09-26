# 任務存證與驗收檢查表 (t_f093ee0b)

- 任務 ID: t_f093ee0b
- 任務名稱: 🎮 遊戲開發｜停擺巨偶三張占位卡接上既有戰鬥（不產新圖）
- 執行角色: 阿翔（sideworker2）
- 日期: 2026-09-27

## 驗收項目逐條檢核

1. **三張占位卡接通既有戰鬥**
   - 出征分頁打開「停擺巨偶」，點擊三張占位卡之一（失控發條獅 Lv12／霧鐘提線人偶 Lv20／黑鏑蒸汽巨象 Lv28）進入既有橫屏戰鬥。
   - 沿用既有首領美術（leo / mirror_wraith / boar）與戰鬥畫面，未新開 Boss 場景，未產新圖。
   - 存證截圖：`proofs/t_f093ee0b/proof_colossus_battle_running.png`（Vision 檢驗通過：橫屏 1280x720，清楚呈現小白、發條獅、HUD 血條、怒氣槽與部位鎖定，零 Emoji，零破版）。

2. **每日次數與開戰扣次**
   - 點擊占位卡開戰正確消耗 1 次當日次數（初始 3 次依次減至 0 次）。
   - 每日免費上限 3 次，滿次後同日第 4 次被拒並提示「今日挑戰次數已用盡，請明天再來！」彈窗。
   - 換日（改 debug_day）後自動重置回 3 次。
   - 敗場也扣次數；戰鬥結束回到手遊大廳出征入口，剩餘次數即時可見。

3. **勝場結算與既有五槽機芯掉落**
   - 勝場彈出既有 `BattleVictoryDialog` 結算卡片，掉落五槽機芯部件之一，合法落在八色階（灰白橘藍紫金綠紅）。
   - 機芯部件正確入袋進背包與整備面板（`GameState.core_bag` 同步）。
   - 敗場扣次數但不給機芯。
   - 存證截圖：`proofs/t_f093ee0b/proof_colossus_battle_victory.png`（Vision 檢驗通過：中央浮空「戰鬥勝利」卡片、獲得【金階】發條發電機、屬性加成與果凍厚底按鈕，z-index=100 阻絕傷害跳字穿透，零 Emoji）。

4. **格擋與部位破壞**
   - 戰鬥掛載既有部位（溢能尖角、溢能核心），支援部位鎖定與部位破壞逃走。
   - 操作按鈕與熱區全數 >= 48px。

5. **硬限制恪守**
   - 零產新圖、零付費 API。
   - ATB、攻速、前搖、命中時間模型常數完全鎖死未動（`verify_time_model_locked() == true`）。
   - 未引入自動巡邏、多人、排行或課金入場券。

6. **六語系健全度與零系統 Emoji**
   - zh_TW、zh_CN、en、ja、ko、es 六語系對應敵人名稱與 UI 健全。
   - 全介面零系統 Emoji。

7. **單元與回歸測試全綠**
   - `test_colossus_battle.gd`: TEST_COLOSSUS_BATTLE_OK
   - `test_colossus_daily.gd`: TEST_COLOSSUS_DAILY_OK
   - `test_core_battle_drop.gd`: CORE_BATTLE_DROP_OK
   - `test_mobile_lobby.gd`: MOBILE_LOBBY_OK
