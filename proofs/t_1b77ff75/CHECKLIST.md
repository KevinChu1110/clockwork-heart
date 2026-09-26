# 停擺巨偶出征卡推薦等級與入場門檻限制 驗收查核表 (t_1b77ff75)

## 一、任務要求與改動項目
- [x] **推薦等級顯示**：三張停擺巨偶出征卡完整顯示推薦等級：
  - 失控發條獅：`推薦 Lv.12`
  - 霧鐘提線人偶：`推薦 Lv.20`
  - 黑鏽蒸氣巨象：`推薦 Lv.28`（對齊 CORE_LOOP_REVAMP 支柱三）
- [x] **等級門檻限制（低於王等級 10 級不能進）**：
  - 門檻計算：`req_level = boss_level - 10`
    - 失控發條獅：門檻 Lv.2（Lv.1 不能進、Lv.2 能進）
    - 霧鐘提線人偶：門檻 Lv.10（Lv.9 不能進、Lv.10 能進）
    - 黑鏽蒸氣巨象：門檻 Lv.18（Lv.1 不能進、Lv.18 能進）
- [x] **未達門檻視覺表現與阻擋**：
  - 玩家等級 < 該王等級 - 10 時：
    - 出征按鈕灰掉（灰色立體厚底按鈕，高度 52px >= 50px），按鈕文字標註 `需達 Lv.X`（英文 `Requires Lv.X`、日文 `Lv.Xで解放`）
    - 用一句話說明為何不能進：`推薦 Lv.X · 未達 Lv.X 不可出征`（英文 `Rec. Lv.X · Requires Lv.X to sortie`、日文 `推奨 Lv.X・Lv.X未満出撃不可`）
    - 點擊按鈕跳出 Toast 提示，不進入戰鬥
- [x] **達到門檻維持可出征**：
  - 達到門檻後，出征按鈕維持多巴胺鮮亮橘色高亮（高度 52px >= 50px），按鈕文字為 `出征`，可正常點擊出征進戰鬥
- [x] **逐字對齊設計文件與六語系同名**：
  - 第三隻巨偶逐字對齊「黑鏽蒸氣巨象」（非「鐧」、非「汽」）
  - 六語系 `enemy.json` 與 `ui.json` 嚴格相等（通過 `verify_colossus_i18n_equality.py` 驗證）
- [x] **硬限制遵守**：
  - 沿用既有出征卡與每日 3 次次數，不准新道具、不准產圖、不准花錢、不准改戰鬥秒數／ATB／怒氣／命中（通過 `test_colossus_daily.gd` 時間模型常數鎖定檢驗）
  - 零系統原生 Emoji

## 二、實機 Framebuffer 截圖清單（0-QA23 / 0-QA26）
| 序號 | 檔案路徑 | 語系/等級 | 驗收重點 | Vision 查驗結果 |
|---|---|---|---|---|
| 01 | `proofs/t_1b77ff75/proof_colossus_gate_locked_zh_tw.png` | 繁中 (zh_TW) / Lv.1 | 門檻未達：出征鈕灰掉（需達 Lv.2/10/18，高 52px >= 50px）、顯示推薦等級與「未達 Lv.X 不可出征」、零 Emoji | **通過 (PASS)** |
| 02 | `proofs/t_1b77ff75/proof_colossus_gate_unlocked_zh_tw.png` | 繁中 (zh_TW) / Lv.20 | 等級達標：出征鈕維持橘色高亮「出征」、顯示推薦等級與抗性狀態、零 Emoji | **通過 (PASS)** |
| 03 | `proofs/t_1b77ff75/proof_colossus_gate_en.png` | 英文 (en) / Lv.1 | 英文排版整齊無溢出無截字、按鈕顯示 Requires Lv.X、零 Emoji | **通過 (PASS)** |
| 04 | `proofs/t_1b77ff75/proof_colossus_gate_ja.png` | 日文 (ja) / Lv.1 | 日文排版整齊無溢出無截字、按鈕顯示 Lv.Xで解放、零 Emoji | **通過 (PASS)** |

## 三、自動化測試通過清單
1. `TEST_FILTER=colossus ./tools/run_tests.sh`：6/6 全部通過
   - `test_colossus_defeat_hint`：PASS
   - `test_colossus_battle`：PASS
   - `test_colossus_daily`：PASS（包含 Lv1 不能進巨象、Lv18 能進；獅門檻 2、提線門檻 10；換日與次數消耗邏輯不變）
   - `test_colossus_exp`：PASS
   - `test_colossus_part_scrap`：PASS
   - `test_windup_to_colossus`：PASS
2. `python3 tools/verify_colossus_i18n_equality.py`：六語系全數一致 PASS
3. `godot --path game --headless --quit-after 3`：冒煙測試 0 script error PASS
