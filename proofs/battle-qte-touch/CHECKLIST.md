# 戰鬥時機窗與互動窗鍵盤用語改觸控＋六語系驗收報告 (t_0b3c225c)

## 任務摘要
- 任務：`t_0b3c225c` 🎮 遊戲開發｜戰鬥時機窗與互動窗鍵盤用語改觸控＋六語系
- 目標：
  1. 戰鬥進行中的時機窗／互動窗／閃避提示完全消除鍵盤鍵名（「按 J」「滑鼠左鍵」），改為觸控用語（「點畫面」「點閃避」）。
  2. 桌面模式保留鍵盤鍵名（按 J / 滑鼠）。
  3. 相關句支援 ContentLoc／_t 六語系（zh_TW, zh_CN, en, ja, ko, es），開著戰鬥切語系 (locale_changed) 即時更換，切回繁中還原。
  4. 全文零系統 emoji。

## 修改檔案
1. `game/scripts/battle/battle_view.gd`：
   - 修正格擋時機窗提示 `parry_hint.text` 在觸控下顯示「準備：倒數到「格擋」再點閃避」（桌面保留「準備：倒數到「格擋」再按」）。
   - 修正石像落石提示 `parry_hint.text` 在觸控下顯示「輸出本體 · 落岩仍要點閃避」（桌面保留「輸出本體 · 落岩仍要 J」）。
   - 優化 `_on_locale_changed`：重設 `_parry_note_left = 0`，若教練提示 `_coach` 正在顯示則立即更新翻譯，若危害或敵方前搖進行中則立即刷新對應 HUD。
   - 優化 `_refresh_hud`：修復危害進行中（如落石/火圈）被一般待機 HUD 覆蓋的邏輯缺陷；在敵方前搖中即便暫停亦刷新多語系文字。
   - 擴充 `_kh()` 容錯過濾：針對長片語（「按 J 或滑鼠左鍵」「按 J 或點畫面」「滑鼠左鍵」「再按」「仍要 J」）與英文日文鍵鼠片語進行純淨觸控用語替換。
2. `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/ui.json`：
   - 補齊時機窗、互動窗、閃避、落石、王者斬相關觸控與桌面詞條，確保六語系 100% 完整無漏翻。
3. `game/scripts/battle/test_battle_qte_touch_i18n.gd`：
   - 新增專屬單元測試，涵蓋六語系字典、觸控王者斬與落石時機窗、戰鬥中動態切換 en/ja/zh_TW、桌面鍵盤模式驗證。
4. `game/scripts/dev/capture_battle_qte_touch_i18n.gd`：
   - 本輪專屬實機截圖腳本，輸出至 `proofs/battle-qte-touch/`。

## 審查核驗對照（review.md）
- **0-QA23**：OUT_DIR 指向本輪獨立專屬目錄 `proofs/battle-qte-touch/`，未改動或覆蓋任何舊輪次截圖。
- **0-QA24**：日文漢字與專有名詞（如「パリィ」「回避をタップ」「連携窓」）均對齊既有語系檔，無漏翻或誤判。
- **0-QA25**：實機截圖核驗全景，確認時機窗/互動窗切換語系時，背景 UI（Ally/Foe、Player/Enemy Name、HP/Rage、Pause/Flee/Attack、部位鎖定）同步變更為對應語系。
- **0-QA15**：截圖實機渲染各不相同，無重複圖檔。
- **零數值更動**：未修改任何戰鬥數值或關卡平衡參數。
- **零系統 emoji**：所有文案皆無 Unicode 系統 emoji。

## 實機截圖清單
- `proofs/battle-qte-touch/proof_battle_qte_en.png`：觸控王者斬時機窗（英文全景，Parry / Tap Dodge now! / Parry window!）
- `proofs/battle-qte-touch/proof_battle_qte_ja.png`：觸控王者斬時機窗（日文全景，パリィ / 今すぐ回避をタップ！ / パリィのタイミング！）
- `proofs/battle-qte-touch/proof_battle_qte_zh_TW.png`：觸控王者斬時機窗（繁中全景，格擋 / 現在點閃避！ / 格擋時機！）
- `proofs/battle-qte-touch/proof_battle_hazard_rockfall_en.png`：觸控落石互動窗（英文全景，Interaction: tap Dodge / Dodge / Falling rock! Tap Dodge now）
- `proofs/battle-qte-touch/proof_battle_hazard_rockfall_ja.png`：觸控落石互動窗（日文全景，連携窓：回避をタップ / 避け / 落岩！今すぐ回避をタップ）

## 測試結果
- `TEST_FILTER=test_battle_qte_touch_i18n ./tools/run_tests.sh`：PASSED (1/1)
- `TEST_FILTER=touch ./tools/run_tests.sh`：PASSED (4/4)
- `TEST_FILTER=i18n ./tools/run_tests.sh`：PASSED (36/36)
- `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
