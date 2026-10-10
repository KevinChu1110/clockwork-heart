# 《發條之心》BattleDefeatDialog 戰敗結算『再次挑戰』按鈕連動關卡重啟驗收報告 (t_94274c40)

- **執行工程師**：阿宏（發條之心·程式 sideworker）
- **關聯任務**：`t_94274c40`（🎮 遊戲開發｜BattleDefeatDialog 戰敗結算新增『再次挑戰』按鈕連動關卡重啟）
- **交付存證目錄**：`proofs/t_94274c40/`
- **遵循規範**：
  - `review.md` 手遊人體工學與多巴胺配色規範：按鈕高度 52px、寬度 >= 170px、多巴胺薄荷綠立體厚底（bottom border 6px，圓角 20px）、零系統 Emoji、深藍紫描邊 #1F1A3A。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 彈窗與卡片正確佈局尺寸（custom_minimum_size Vector2(760, 490)），符合 740~760px 規範，避免坍塌或溢出。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_battle_defeat_retry_zh_TW.png` | `BattleDefeatDialog` 戰敗結算彈窗：展示多巴胺薄荷綠「再次挑戰」按鈕（`BtnRetryStage`，尺寸 170x52px，立體厚底 6px，圓角 20px），排版於 ReviveAdBtn 與 BtnGearUp 之間 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `2f610508e5be` | 合格 (PASS) |
| 02 | `proof_02_battle_defeat_retry_en.png` | 英文語系 (en) `BattleDefeatDialog`：彈窗內部顯示「Retry Stage」，全彈窗零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `a6d92a09d866` | 合格 (PASS) |
| 03 | `proof_03_battle_defeat_retry_restarted_combat.png` | 點擊「再次挑戰」按鈕（BtnRetryStage 觸發 pressed.emit()）後連動 BattleView 扣除能量、銷毀彈窗、玩家滿血 (HP 50/50) 重啟當前出征關卡 1-1（停擺發條鼠）之實機畫面，無任何彈窗遮擋 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `5573d96ec469` | 合格 (PASS) |

- **防作弊與真實性校驗**：3 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），對應 3 張特寫裁切圖於 `crops/` 目錄。
- **Vision 視覺複檢**：經 Vision 驗證，所有按鈕比例正確、立體厚底質感完整、無黑屏、無穿模、無截字、無任何違規 Emoji；proof_03 確認無彈窗遮擋且玩家為 50/50 滿血開戰。
- **審查意見 (Review Cycle 2) 改善對齊**：
  1. `BattleView._on_retry_stage_defeat()` 確保舊彈窗實體銷毀（`queue_free()`）置空，並在重開戰鬥前呼叫 `GameState.heal_full()` 重置玩家為滿血。
  2. `capture_regression_t_94274c40.gd` Step 4 明確透過定位 `BtnRetryStage` 並發射 `pressed.emit()` 模擬點擊，proof_03 重新渲染出無彈窗遮擋、滿血開戰畫面。
  3. `test_battle_defeat_retry.gd` 補齊重開戰鬥後玩家血量回滿斷言與彈窗銷毀斷言。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **再次挑戰** | 再次挑战 | Retry Stage | 再挑戦 | 다시 도전 | Reintentar etapa |
| **能量不足，無法再次挑戰關卡！** | 能量不足，无法再次挑战关卡！ | Not enough energy to retry stage! | エネルギー不足でステージを再挑戦できません！ | 에너지가 부족하여 스테이지를 다시 도전할 수 없습니다! | ¡Energía insuficiente para reintentar la etapa! |

---

## 三、 單元與回歸測試結果

- **無頭單元測試**：`TEST_FILTER=defeat ./tools/run_tests.sh` 5/5 全部通過 (PASS)
  - `test_battle_defeat_diagnostic`: PASS
  - `test_battle_defeat_i18n`: PASS
  - `test_battle_defeat_retry`: PASS（新增，100% 覆蓋按鈕實體、尺寸規範、信號發射、六語系動態刷新、能量充足重啟、能量不足提示）
  - `test_colossus_defeat_hint`: PASS
  - `test_energy_defeat_refund`: PASS
- **自動化檢查**：`/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`
