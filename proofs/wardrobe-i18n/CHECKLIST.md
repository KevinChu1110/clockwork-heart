# 衣櫥星紋斗篷／裸機素體／彈窗標題按鈕六語系落地驗收清單 (wardrobe-i18n)

卡號：t_2d2c11cb
執行人：阿翔（側案·工程師 sideworker2）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「星紋斗篷」、「無外裝 (裸機素體)」、彈窗標題「發條衣櫥 · 英雄換裝」、副標「個人化外觀部件即時切換 · 零數值純視覺展示」、提示「外裝庫」、「點「全部」可跨族穿：騎士／法師／遊俠／格鬥／維京」、按鈕「還原預設」、「隨機」、「確認換裝 · 套用新外觀」、「✓ 已選用」等。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊（各 2120 個 key，zh_TW 161 個 key）。
   - grep 驗證：六語系均可精確 grep 到「星紋斗篷」與「無外裝 (裸機素體)」key。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（五語系 content/ui.json 各 2120 個 key，全部對齊，I18N_OK）。

2. **衣櫥彈窗外框與標題按鈕接入 i18n（缺陷 2 修復）：**
   - 大標題「發條衣櫥 · 英雄換裝」改走 `_t()`，切 en 為 `Clockwork Wardrobe · Hero Outfits`，切 ja 為 `ゼンマイ衣装棚 · 英雄の着替え`。
   - 副標題「個人化外觀部件即時切換 · 零數值純視覺展示」改走 `_t()`，切外語即時連動。
   - 種族列提示「外裝庫」與「點「全部」可跨族穿...」改走 `_t()`，切外語即時連動。
   - 底部操作按鈕「還原預設」、「隨機」、「確認換裝 · 套用新外觀」改走 `_t()`，切 en 為 `Reset`、`Random`、`Confirm Outfit · Apply New Look`；切 ja 為 `デフォルトに戻す`、`ランダム`、`着替え確認 · 新しい外見を適用`。
   - 綁定 `Loc.locale_changed` 信號，切換語言時彈窗即時刷新所有文字。

3. **蛙族第二套「星紋斗篷」與第三張「無外裝 (裸機素體)」六語系連動（缺陷 1 修復）：**
   - 進入蛙族衣櫥，第二套外裝卡片正確顯示 `Astral Cape`（en）／`星紋のマント`（ja）／`星紋斗篷`（zh_TW）。
   - 第三張素體卡片正確顯示 `No Costume (Bare Frame)`（en）／`外装なし (素体)`（ja）／`無外裝 (裸機素體)`（zh_TW）。
   - 選中狀態標籤正確顯示 `✓ Selected`（en）／`✓ 選択中`（ja）／`✓ 已選用`（zh_TW）。
   - 左側 512 預覽即時切換為對應外裝或裸機素體。

4. **大廳背景與底部 Dock 連動同步切換（0-QA25 檢查）：**
   - 在 en 語系下：頂部 Shop/Settings、玩家資訊、底部 Dock（Cogwheel Hamlet, Adventure Bag）均同步顯示英文。
   - 在 ja 語系下：頂部ショップ/設定、底部ぜんまい新村/冒險バッグ均同步顯示日文。

5. **日／韓漢字翻譯核實（0-QA24 規範）：**
   - 日文下「星紋のマント」、「外装なし (素体)」、「ゼンマイ衣装棚 · 英雄の着替え」對齊 `ja/ui.json` 詞條設定，合規無漏翻。

6. **實機截圖與局部 Crops 存證（proofs/wardrobe-i18n/，0-QA23）：**
   - 蛙選星紋斗篷：
     - `proof_wardrobe_frog_astral_zh_TW.png`
     - `proof_wardrobe_frog_astral_en.png`
     - `proof_wardrobe_frog_astral_ja.png`
   - 蛙選裸機素體：
     - `proof_wardrobe_frog_bare_zh_TW.png`
     - `proof_wardrobe_frog_bare_en.png`
     - `proof_wardrobe_frog_bare_ja.png`
   - 顯微比對特寫：
     - `crops/crop_wardrobe_title_{zh_TW,en,ja}.png`
     - `crops/crop_wardrobe_cards_{zh_TW,en,ja}.png`
     - `crops/crop_wardrobe_actions_{zh_TW,en,ja}.png`
     - `crops/crop_dock_{zh_TW,en,ja}.png`

7. **無頭冒煙與測試全綠：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=wardrobe ./tools/run_tests.sh`：3/3 PASSED（含新增 test_wardrobe_i18n）。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：2/2 PASSED（含新增 test_wardrobe_i18n）。
