# 每日發條彈窗標題按鈕六語系 (windup-daily-i18n) 交付審核清單

依據 `references/review.md` 規範（0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25）：

## 一、0-QA23 查 OUT_DIR
- 截圖腳本 `game/scripts/dev/capture_windup_daily_i18n_proof.gd` 之 `OUT_DIR` 嚴格設定為 `proofs/windup-daily-i18n/`。
- 本輪截圖檔案均存於 `proofs/windup-daily-i18n/` 與 `proofs/windup-daily-i18n/crops/`，完全未動到任何其他卡的 proof 目錄。

## 二、0-QA24 日/韓沿用漢字與既定譯名以語系檔為準
- 韓語/日語詞彙如「聚魂殿」、「冒險委託」、「灰イタチ」、「釘釘」等對齊既有語系檔，未有漏翻或未定義 key。

## 三、0-QA25 彈窗以外大廳與底部 Dock 一起換語系
- `proof_windup_dialog_zh_TW.png` / `proof_windup_done_zh_TW.png`: 繁中彈窗與繁中大廳背景、繁中底部五頁籤 Dock。
- `proof_windup_dialog_en.png` / `proof_windup_done_en.png`: 英文彈窗（Adventure Commission · Who Needs Winding Today?、Leave Commission、Set Out to Battle、Today's Commission Completed）與英文大廳背景、英文底部五頁籤 Dock（Cogwheel Hamlet / Hero Gear / Four Regions / Soul Hall / Adventure Bag）。
- `proof_windup_dialog_ja.png` / `proof_windup_done_ja.png`: 日文彈窗（冒険依頼 · 今日ゼンマイを巻くのは誰？、依頼を離れる、出征する、本日の依頼達成済）與日文大廳背景、日文底部五頁籤 Dock（ぜんまい新村 / キャラ装備 / 四区出征 / 聚魂殿 / 冒険バッグ）。

## 四、驗收標準查驗
1. 六語系 ui.json 都能 grep 到「今天誰需要上發條」：
   `grep -n "今天誰需要上發條" game/data/i18n/content/*/ui.json` 全數命中（六語系齊全）。
2. 實機截圖存 proofs/windup-daily-i18n/：zh_TW / en / ja 各兩張（未完成 + 已完成），局部 crops 齊全。
3. `godot --path game --headless --quit-after 3` 0 SCRIPT ERROR。
4. `TEST_FILTER=windup ./tools/run_tests.sh`（2/2 PASS，含 test_windup_daily_i18n）。
5. `TEST_FILTER=i18n ./tools/run_tests.sh`（4/4 PASS，含 test_windup_daily_i18n）。
