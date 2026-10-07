# 戰鬥部位破壞 0.4 秒慢動作頓挫與 Boss 部位將破 warn 音效整合驗收清單 (t_1a4bca3d)

- **任務 ID**：`t_1a4bca3d`
- **交付目錄**：`proofs/t_1a4bca3d/`（遵守獨立目錄規範，無跨卡覆蓋）
- **規範參照**：`docs/CLOCKWORK_ART_MUSIC_BRIEF.md` §5、`AGENTS.md` (驗證階梯)

---

## 1. 功能實作與規格對齊

依據 `docs/CLOCKWORK_ART_MUSIC_BRIEF.md` 第 5 條與任務需求：
1. **部位破壞接入 0.4 秒慢動作頓挫**：
   - `battle_sim.gd`：部位破壞（`_finish_part_break`）時將 `slowmo` 設置為 0.4 秒，並於 `part_broken` 事件中傳遞 `slowmo: 0.4`。
   - `battle_view.gd`：收到 `part_broken` 時呼叫 `trigger_part_break_slowmo(0.4)`，將 `Engine.time_scale` 縮放至 0.15 並於 0.4 秒內正弦曲線平滑恢復原速，同時保護不被常規命中定格覆蓋。
   - 特效整合：`battle_view.gd` 保留並整合金屬糖果屑碎裂特效（`_spawn_candy_chip_break` / `CandyChipVfx`）。
   - 音效整合：`audio_manager.gd` 收到 `part_broken` 事件時播放 `play_sfx("break")`。
2. **Boss 部位血量 <= 20% 自動播放 warn 音效**：
   - `battle_unit.gd`：新增 `part_warned: bool` 狀態。
   - `battle_sim.gd`：多部位與單部位傷害扣減後，若 Boss 部位血量 <= 20%（`cur_hp > 0` 且 `cur_hp / max_hp <= 0.2`），自動觸發 1 次 `part_warn` 事件並呼叫 `AudioManager.play_sfx("warn")`，且標記 `warned = true` 避免重複播放。
   - `battle_view.gd`：收到 `part_warn` 記錄戰鬥日誌「⚠ 部位瀕臨破碎！」並閃現教練提示。
3. **warn 音效徹底移出格擋窗**：
   - `audio_manager.gd`：移除 `king_slash_start` 播放 warn 音效之舊有動作，純保留作為部位將破警示。
   - 提供 `play_sfx(id, pitch_scale, volume_db)` 相容介面。

---

## 2. 測試驗證結論

1. **專屬單元測試 `test_battle_part_break_slowmo.gd`**：**PASSED (1/1)**
   - 1. 測試 Boss 部位血量 <= 20% 自動播放 1 次 warn 音效，高於 20% 不觸發，持續 <= 20% 不重複播放：**通過 (PASS)**
   - 2. 測試 warn 音效徹底移出格擋窗（king_slash_start 不再播 warn）：**通過 (PASS)**
   - 3. 測試部位破壞觸發 0.4 秒慢動作頓挫（sim.slowmo == 0.4）且 0.4s 後順暢恢復：**通過 (PASS)**
   - 4. 測試 BattleView trigger_part_break_slowmo 頓挫縮放 Engine.time_scale 介面：**通過 (PASS)**
   - 5. 測試部位破壞 break 音效與 CandyChipVfx 金屬糖果屑碎裂特效整合：**通過 (PASS)**

2. **迴歸測試 `TEST_FILTER=part_break ./tools/run_tests.sh`**：**PASSED (3/3)**
   - `test_battle_part_break_i18n` (PASS)
   - `test_battle_part_break_slowmo` (PASS)
   - `test_part_break` (PASS)

3. **無頭冒煙測試 `godot --path game --headless --quit-after 3`**：
   - 0 errors, 0 warnings，無 SCRIPT ERROR。

4. **品質自動檢查 `clock-check /opt/side/bravesoul-game`**：
   - ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞。
