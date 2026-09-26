# 視覺/文案微調批次（本週）驗收清單 (t_141471d6)

依據 `references/review.md` 規範（0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25）與任務驗收條件：

## 一、驗收總覽
- [x] **0-QA23 獨立目錄**：所有交付截圖與裁切圖嚴格限定於 `proofs/copy-polish-week/`，絕無修改或覆蓋其他任務之 proof 目錄。
- [x] **0-QA24 日韓漢字對齊語系檔**：日文版「武闘」「剣・騎士・剣」「拳・武闘・拳」「遊び方」等漢字完全對齊 `content/ja/ui.json` 與 `ja/weapon_class.json`，使用日本新字體「闘」（門內豆寸），無繁中殘留。
- [x] **0-QA25 全景與即時連動**：全景實機截圖中彈窗、對話框、背景皆與當前語系完全一致。
- [x] **問題 1 修復（雙句號清除）**：
  - 調整 `game/data/dialogues/*/craft.json` 六語系模板中的 `forge.path_chosen`：
    - `zh_TW` / `zh_CN`: `玩法：{play}{pro}`（移除多餘句號）
    - `ja`: `遊び方：{play}{pro}`（移除多餘句號）
    - `en`: `Playstyle: {play} {pro}`（移除多餘句號，保留單空格）
    - `ko`: `플레이: {play} {pro}`（移除多餘句號，保留單空格）
    - `es`: `Estilo de juego: {play} {pro}`（移除多餘句號，保留單空格）
  - 同步更新 `test_main_dialog_golden.json`。
  - 對話中「玩法句」與「優點句」之間僅保留 1 個句號，優點句完整顯示，流派數值完全未變。
- [x] **問題 2 修復（職業名「武鬥」補齊譯名）**：
  - 於六語系 `game/data/i18n/content/*/ui.json` 補齊 `武鬥` 詞條：
    - `zh_TW`: `武鬥`
    - `zh_CN`: `武斗`
    - `en`: `Monk`
    - `ja`: `武闘`
    - `ko`: `무투`
    - `es`: `Monje`
  - 兵器架與介面上拳/爪職稱不再單露繁中「武鬥」。
- [x] **零系統 Emoji**：介面、按鈕與文本全數無系統 emoji。

## 二、測試與驗證

1. **無頭冒煙測試**：
   - 指令：`godot --path game --headless --quit-after 3`
   - 結果：0 錯誤，無 SCRIPT ERROR，退出碼 0。

2. **單元測試 (test_weapon_classes_i18n.gd)**：
   - 指令：`TEST_FILTER=test_weapon_classes_i18n ./tools/run_tests.sh`
   - 結果：通過（`WEAPON_CLASSES_I18N_OK`，Exit code 0）。
   - 包含新增斷言：
     - 六語系 `ContentLoc.text("ui", "武鬥")` 精準匹配對應譯名。
     - 六語系 12 流派選定對話 `forge.path_chosen` 逐一檢查絕無 `..` 或 `。。`。

## 三、實機截圖與特寫存證 (proofs/copy-polish-week/)

1. `proof_01_en_rack.png` (1280x720 全景實機，en)
   - 特寫：`crops/crop_01_en_rack.png`
   - 說明：英文兵器架清單中，拳流派正確顯示為 `Fist · Monk · Fist`，無未翻譯中文「武鬥」。
2. `proof_02_ja_rack.png` (1280x720 全景實機，ja)
   - 特寫：`crops/crop_02_ja_rack.png`
   - 說明：日文兵器架清單中，拳流派顯示為 `拳・武闘・拳`、爪流派顯示為 `爪・武闘・爪`，符合 0-QA24 日本字體標準。
3. `proof_03_en_sword_dialog.png` (1280x720 全景實機，en)
   - 特寫：`crops/crop_03_en_sword_dialog.png`
   - 說明：英文版選定劍流派確認對話，內容為 `Playstyle: Close to mid range, alternating normal strikes and rage skills. The spear is also playable in this class. Balanced offense and defense, easiest to master`，句中僅有單個句點 `.`，無贅餘 `..`。
4. `proof_04_ja_bow_dialog.png` (1280x720 全景實機，ja)
   - 特寫：`crops/crop_04_ja_bow_dialog.png`
   - 說明：日文版選定弓流派確認對話，內容為 `遊び方：間合いを取って安全圏から射貫く。同職で銃も扱える。安全な長距離から安定して攻撃`，句中僅有單個句號 `。`，無贅餘雙句號 `。。`。
5. `proof_05_zh_TW_sword_dialog.png` (1280x720 全景實機，zh_TW)
   - 特寫：`crops/crop_05_zh_TW_sword_dialog.png`
   - 說明：繁中版選定劍流派確認對話，內容為 `玩法：近身中距離，普攻和怒氣技輪著來。同職也可玩槍。攻防平均，最好上手`，句中僅有單個句號 `。`，無贅餘雙句號 `。。`。

## 四、MD5 唯一性驗證 (0-QA15)
- `proof_01_en_rack.png`: `eddddc307d2a47e557aa116094368441`
- `proof_02_ja_rack.png`: `24e6fc21712744695f55c4cd1abbc1b7`
- `proof_03_en_sword_dialog.png`: `e024c9c62f50bb4d7974eff7361ec381`
- `proof_04_ja_bow_dialog.png`: `6391560391e7217421ccae58ee6a4154`
- `proof_05_zh_TW_sword_dialog.png`: `5c19819991eb9a33cebcc9c179e10ff6`
- `crops/crop_01_en_rack.png`: `84281da0661cf648b57fc7720fd81bf0`
- `crops/crop_02_ja_rack.png`: `58895339abf49eecd7dcefee951c9402`
- `crops/crop_03_en_sword_dialog.png`: `a641ea84b78135b5369d8c382bbdeb51`
- `crops/crop_04_ja_bow_dialog.png`: `168799021c6072378d653d187c1f9682`
- `crops/crop_05_zh_TW_sword_dialog.png`: `d87d8b21208f4596549c800212273b88`
10 張圖檔 MD5 100% 獨立唯一，未覆蓋任何既有任務之截圖。
