# 戰鬥部位「已破」標籤六語系驗收清單 (battle-broken-i18n)

依據 `references/review.md` 規範（0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25）：

## 一、0-QA23 查 OUT_DIR 獨立性
- 截圖腳本與輸出目錄嚴格限定為 `proofs/battle-broken-i18n/`，絕不寫入或覆蓋其它卡片之 proof 目錄。
- 產出檔案清單與 MD5：
  - `proof_battle_broken_en.png` (e1ce5a5a8873a3594ee38bc7274756fa, 1280x720)
  - `proof_battle_broken_ja.png` (78e5c26c9feff2e1c12fea8f09340689, 1280x720)
  - `proof_battle_broken_zh_TW.png` (f377b7b7a1386e54a035f192ab330ee4, 1280x720)
  - `crops/crop_part_hud_en.png` (fef70126acc0bab719bf58ae0042720e)
  - `crops/crop_part_hud_ja.png` (ef1131469412b88025f3df99b6914541)
  - `crops/crop_part_hud_zh_TW.png` (556035f647e9950b34af9ca303e448ae)
  - MD5 100% 互異獨立。

## 二、0-QA24 日文／韓文漢字與在地化對齊
- 詞條依 `game/data/i18n/content/<locale>/ui.json` 既定遊戲術語對齊：
  - 日文：「甲·騎士の大盾 [破壊済]」、「兜·騎士の重兜」、「部位捕捉 → 騎士の重兜」等，符合日版遊戲既定漢字與怪物部位破壞用語，無中文殘留。
  - 英文：「I·Lion-guard heavy shield [Broken]」、「Helm·Knight's heavy helm」、「Part locked → Knight's heavy helm」等。
  - 韓文：「갑·사자 수호 대방패 [파괴됨]」、「투구·사자 수호 중갑 투구」、「부위 고정 → 사자 수호 중갑 투구」等。
  - 西班牙文：「I·Gran escudo del león guardia [Roto]」、「Yelmo·Yelmo pesado del león guardia」等。
  - 簡體中文：「甲·骑士重盾 [已破]」、「盔·骑士重盔」等。
  - 繁體中文：「甲·獅衛重盾 [已破]」、「盔·獅衛重盔」等。

## 三、0-QA25 畫面整體語系一致性
- 驗證畫面部位資訊欄（PartPanel）、上方提示列（Parry/Focus Hint）、玩家狀態列、敵方狀態列、下方戰鬥提示與對話框、右下動作按鈕（Pause/Flee/Attack）同步為同一語系，零硬編殘留。
- BattleView 節點監聽 `Loc.locale_changed` 信號，支援切換語系即時刷新部位標籤與提示。

## 四、功能與數值檢驗
- 數值正確性：Leo Boss 420 血量、部位血量、未破部位標籤維持正確。
- 零系統 Emoji：全畫面與所有按鈕無系統 emoji。
- 單元測試：
  - `test_battle_part_break_i18n.gd`: 通過（`TEST_BATTLE_PART_BREAK_I18N_OK`）
  - 無頭冒煙測試 `godot --path game --headless --quit-after 3`: 無 SCRIPT ERROR
