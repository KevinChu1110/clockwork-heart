# 任務存證與驗收檢查表 (t_db91143f)

- 任務 ID: t_db91143f
- 任務名稱: 🤖 平台與維運｜把已過審的停擺巨偶每日入口合進主線
- 執行角色: 阿宏（sideworker）
- 日期: 2026-09-27

## 驗收項目逐條檢核

1. **出征入口與每日次數顯示**
   - 橫屏主線出征分頁新增「停擺巨偶」模式切換按鈕，即時顯示今日剩餘次數（上限 3 次，如「停擺巨偶 · 今日剩餘: 3/3」）。
   - 按鈕熱區與高度完全滿足 >= 48px 標準。
   - 存證截圖：`proofs/t_db91143f/proof_colossus_sortie.png`（Vision 檢驗通過：無 Emoji、無破版跑版）。

2. **三張占位卡渲染**
   - 停擺巨偶出征列表呈現三張占位卡：
     1. 巨偶-1：失控發條獅 Lv.12
     2. 巨偶-2：霧鐘提線人偶 Lv.20
     3. 巨偶-3：黑鏑蒸汽巨象 Lv.28
   - 無第四隻占位怪，所有文字與數值對齊規格。

3. **同日滿 3 次限制與明天再來提示**
   - 每日免費上限 3 次，滿次後出征按鈕轉為「明天再來」。
   - 點擊觸發「今日挑戰次數已用盡，請明天再來！」提示彈窗（包含「每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。」）。
   - 存證截圖：`proofs/t_db91143f/proof_colossus_limit_dialog.png`（Vision 檢驗通過）。

4. **六語系支援與零系統 Emoji**
   - 包含 zh_TW、zh_CN、en、ja、ko、es 六語系對應詞條。
   - 全畫面零系統 Emoji，採用手繪/向量圖示與粉圓體/思源黑體。

5. **硬限制恪守**
   - 零開戰、零產新圖、零付費 API。
   - 未引入自動巡邏，分支邊界嚴謹。
   - ATB、攻速、前搖、命中常數完全鎖死未動（`verify_time_model_locked() == true`）。

6. **單元測試與回歸測試**
   - `test_colossus_daily.gd`: TEST_COLOSSUS_DAILY_OK
   - `test_save_slots.gd`: SAVE_SLOTS_OK
   - `test_mobile_lobby.gd`: MOBILE_LOBBY_OK
   - `test_lobby_sortie_i18n.gd`: LOBBY_SORTIE_I18N_OK
   - `test_core_battle_drop.gd`, `test_core_color_tiers.gd`, `test_core_combat_stats.gd`, `test_core_slots_ui.gd`: 全部 PASS
