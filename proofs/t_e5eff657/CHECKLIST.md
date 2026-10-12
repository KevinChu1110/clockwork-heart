# 《發條之心》BattleVictoryDialog 勝利結算『再次挑戰』按鈕支援重複刷關驗收報告 (t_e5eff657)

- **執行工程師**：阿翔（發條之心·工程師 sideworker2）
- **關聯任務**：`t_e5eff657`（🎮 遊戲開發｜BattleVictoryDialog 勝利結算新增『再次挑戰』按鈕支援重複刷關）
- **交付存證目錄**：`proofs/t_e5eff657/`
- **遵循規範**：
  - `review.md` 第 28 條與手遊人體工學規範：橫屏彈窗寬度 756px（符合 740~760px 規範）、按鈕高度 52px、多巴胺亮色果凍按鈕（bottom border 6px，圓角 20px，配色暖橘 #FFA010）、熱區 >= 48px、零系統 Emoji、深藍紫描邊 #1F1A3A。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --resolution 1280x720` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 彈窗與卡片正確佈局尺寸（`_dialog_card.custom_minimum_size = Vector2(756, 420)`），按鈕列整齊排列零折行穿模。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留，頂層與 content 表同步齊全。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_battle_victory_replay_zh_TW.png` | `BattleVictoryDialog` 1-1 出征勝利結算彈窗：展示多巴胺暖橘「再次挑戰」按鈕（`BtnReplayStage`，尺寸 170x52px，立體厚底 6px，圓角 20px），與立即裝備、收下完成、挑戰下一關排列整齊無折行穿模 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `ab55676b626c` | 合格 (PASS) |
| 02 | `proof_02_battle_victory_replay_en.png` | 英文語系 (en) `BattleVictoryDialog`：彈窗內部顯示「Retry Stage」，全彈窗按鈕文字零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `a98f31f9d47e` | 合格 (PASS) |
| 03 | `proof_03_battle_victory_restarted_combat.png` | 點擊「再次挑戰」按鈕（`BtnReplayStage` 觸發 `replay_stage_requested`）後連動 BattleView 扣除 1 點能量、銷毀結算彈窗、玩家滿血 (HP 50/50) 重啟當前出征關卡 1-1 之實機畫面，無任何彈窗遮擋 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `aa54fe1eb944` | 合格 (PASS) |
| 04 | `proof_04_battle_victory_final_stage_replay.png` | 4-4 出征末關結算彈窗：展示「再次挑戰」按鈕正常顯示支援重複刷關，而「挑戰下一關」按鈕自動隱藏（無後續關卡避免越界） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `16c24733b583` | 合格 (PASS) |

- **防作弊與真實性校驗**：4 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），對應 4 張特寫裁切圖於 `crops/` 目錄。
- **Vision 視覺複檢**：經 Vision 驗證，所有按鈕比例正確、立體厚底質感完整、無黑屏、無穿模、無截字、無任何違規 Emoji；proof_03 確認無彈窗遮擋且玩家為 50/50 滿血開戰。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/*.json` 及 `game/data/i18n/content/<locale>/ui.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **再次挑戰** | 再次挑战 | Retry Stage | 再挑戦 | 다시 도전 | Reintentar etapa |
| **能量不足，無法再次挑戰關卡！** | 能量不足，无法再次挑战关卡！ | Not enough energy to retry stage! | エネルギー不足でステージを再挑戦できません！ | 에너지가 부족하여 스테이지를 다시 도전할 수 없습니다! | ¡Energía insuficiente para reintentar la etapa! |

---

## 三、 單元與回歸測試結果

- **無頭單元測試**：
  - `test_battle_victory_replay.gd`: PASS（新增，100% 覆蓋按鈕節點、尺寸人因、信號發射、六語系動態刷新、末關顯示/隱藏、能量充足扣除重啟、能量不足防護）
  - `test_battle_victory_next_stage.gd`: PASS (無任何回歸)
  - `test_battle_defeat_retry.gd`: PASS (無任何回歸)
  - `test_victory_part_break_badges.gd`: PASS (無任何回歸)
  - `test_core_battle_drop.gd`: PASS (無任何回歸)
- **回歸 Runner 執行**：
  - `TEST_FILTER=victory ./tools/run_tests.sh`: 4/4 PASS
  - `TEST_FILTER=defeat ./tools/run_tests.sh`: 5/5 PASS
- **自動化檢查**：`/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`
