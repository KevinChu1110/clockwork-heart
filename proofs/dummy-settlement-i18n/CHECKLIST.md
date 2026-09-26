# 木人樁結算卡標題按鈕六語系驗收清單 (dummy-settlement-i18n)

依據 `references/review.md` 規範（0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25）：

## 一、0-QA23 查 OUT_DIR 獨立性
- 截圖腳本與輸出目錄嚴格限定為 `proofs/dummy-settlement-i18n/`，絕不寫入或覆蓋其它卡片之 proof 目錄。
- 產出檔案清單與 MD5：
  - `proof_dummy_settlement_en.png` (807a66c95e02ee752a1f950f70e083fb, 1280x720)
  - `proof_dummy_settlement_ja.png` (b4a5f3d4b33a620733aeb9a454fa78b4, 1280x720)
  - `proof_dummy_settlement_zh_TW.png` (261f29ef47a000d2bdad8ddb79c095a7, 1280x720)
  - `crops/crop_dummy_settlement_en.png` (32c9deac49b90abbdd2a4bb3e0f7919f, 780x460)
  - `crops/crop_dummy_settlement_ja.png` (d24775d9e10bc748d77f30ccb59b806a, 780x460)
  - `crops/crop_dummy_settlement_zh_TW.png` (350b03cd7c8d5c622c1d432bd90d2abd, 780x460)
  - MD5 100% 互異獨立。

## 二、0-QA24 日文／韓文漢字與在地化對齊
- 詞條依 `game/data/i18n/content/<locale>/ui.json` 既定遊戲術語對齊：
  - 日文：「木人試技データカード」、「武術館「技」訓練フィードバック · エネルギー消費 0」、「総ダメージ」、「試技時間」、「秒間ダメージ (DPS)」、「試技を終了」等，皆符合日版《勇者之魂》既定漢字與平假名習慣，非中文殘留。
  - 韓文：「목인 연습 데이터 카드」、「총 피해량」、「연습 시간」、「초당 피해량 (DPS)」、「연습 완료」等。
  - 英文：「Dummy Trial Report」、「Total Damage」、「Trial Duration」、「DPS」、「Finish Trial」等。

## 三、0-QA25 畫面整體語系一致性（彈窗＋背景 UI）
- 驗證畫面不僅中央浮空結算卡完成切換，背景戰鬥畫面上之玩家名稱（Xiaobai / シロ / 小白）、敵手名稱（Training Dummy / 木人 / 木人樁）、上方提示列、下方戰鬥日誌與右下控制按鈕（End Trial / 試技終了 / 結束試招）同步為同一語系，零混合或硬編殘留。
- 彈窗節點監聽 `Loc.locale_changed` 信號，支援即時動態熱切換刷新。

## 四、功能與數值檢驗
- 數值精確度：總傷害 500、耗時 12.8s、DPS 39.1 於各語系切換下數值與小數點保持一致，零被篡改。
- 零系統 Emoji：全畫面與所有按鈕無系統 emoji。
- 單元測試：
  - `test_dummy_settlement_dialog.gd`: 通過（`DUMMY_SETTLEMENT_DIALOG_OK`）
  - `test_dummy_settlement_i18n.gd`: 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`）
