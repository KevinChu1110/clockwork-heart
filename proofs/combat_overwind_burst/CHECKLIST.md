# 戰鬥發條超載爆裂（Overwind Burst）驗收報告

任務卡號：`t_3767de1f`
負責人：阿宏（sideworker）
日期：2026-10-07

---

## 一、需求對照與成果

| 項次 | 需求描述 | 實作方案 | 驗收證據 |
|---|---|---|---|
| 1 | 戰鬥滿怒（rage >= 100）或觸發狂暴/技能時，觸發「發條超載爆裂（Overwind Burst）」視覺回饋 | 在 `BattleSim` 累怒滿額（`_gain_rage`）、手動暴怒（`trigger_fury_awakening`）與滿怒技能釋放（`skill_cast`）時發送 `overwind_burst` 事件；`BattleView` 接收並執行 `trigger_overwind_burst()` | 單元測試 `test_combat_overwind_burst.gd` 3 大情境全部通過，事件源標記正確 |
| 2 | 0.3 秒全螢幕暗角震動（vignette / screen shake） | `BattleView` 動態建立全螢幕 320x180 漸層暗角圖層（`OverwindVignette`，中心通透無遮擋，四角深黑曜石棕漸變＋金色火環過渡），Tween 控制 0.04s 漸入、0.16s 保持、0.10s 淡出；螢幕震動 `_shake = 0.35` 配合 `hit_stop(0.08)` | 實機截圖 `proof_02_overwind_burst_peak.png` 四角明顯暗角，Vision 驗證確認清晰聚焦，`_shake >= 0.3` 斷言通過 |
| 3 | 金色齒輪火花噴射粒子動效（CPU/GPU particles） | 採用 `CPUParticles2D`（保證跨平台、Web、行動端與 headless 一致穩定）：金色星芒火花粒子（`BurstSparks` 40 顆）與程式化繪製之 8 齒金屬發條齒輪粒子（`BurstGears` 16 顆，高速旋轉向外弧線噴射） | 實機截圖 `proof_02_overwind_burst_peak.png` 主角身側大量旋轉齒輪與金黃火花四散，Vision 驗證確認鮮明飽和 |
| 4 | 播放 overwind 金屬爆裂音效 | `AudioManager` 實作 `play_overwind_burst()`，支援 `overwind.wav` 專檔，缺檔時走重金屬撞擊 `clash` (1.15) ＋ 金屬崩裂 `break` (1.05) ＋ 發條咬合 `clock` (1.25) 多層次複合音效 | `AudioManager.play_overwind_burst()` 與 `on_battle_event` 測試全數通過 |
| 5 | 六語系提示同步 | 橫幅、飄字與日誌同步支援六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），中英文橫幅置中清晰，100% 零系統 emoji | 六語系字典斷言通過，`proof_03_overwind_burst_en.png` 實機英文橫幅 "Overwind Burst!" 驗證通過 |

---

## 二、實機 1280x720 截圖存檔 (`proofs/combat_overwind_burst/`)

- `proof_01_battle_idle.png`：常態戰鬥截圖（未爆裂基準對照，無暗角）
- `proof_02_overwind_burst_peak.png`：繁中版滿怒超載爆裂峰值（全螢幕暗角＋金色齒輪噴濺＋金色星芒火花＋「發條超載爆裂！」橫幅＋主角高光）
- `proof_03_overwind_burst_en.png`：英文版滿怒超載爆裂峰值（英文 "Overwind Burst!" 橫幅＋全螢幕暗角＋齒輪噴濺）

---

## 三、驗收檢核清單

- [x] **0-QA5 / 0-QA26**：100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 擷取，1280x720 原始截圖，非假圖。
- [x] **0-QA28**：六語系 `ui.json` 與根目錄 `<loc>.json` 完整補齊，ContentLoc 翻譯層無缺漏。
- [x] **零系統 Emoji**：全域無彩色系統 Emoji，純淨粉圓體與遊戲美術樣式。
- [x] **單元測試全綠**：`test_combat_overwind_burst.gd` 4 大項單元測試全數通過（事件發送、音效播放、六語系、BattleView 節點與視覺觸發）。
- [x] **迴歸測試無壞死**：`test_fury_awakening.gd`、`test_combat_full_rage_cast.gd` 全綠。
- [x] **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 零 SCRIPT ERROR，exit code 0。
- [x] **自動檢查 clock-check**：`clock-check /opt/side/bravesoul-game` 顯示「✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞」。
- [x] **專案狀態同步**：`python3 /root/project_status.py combat-overwind-burst 測試中` 已同步更新。
