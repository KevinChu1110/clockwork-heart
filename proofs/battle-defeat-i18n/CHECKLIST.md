# 戰鬥失敗復活彈窗六語系即時刷新 驗收清單 (battle-defeat-i18n)

## 1. 任務目標
玩家戰敗彈窗（看廣告復活／結束戰鬥）切語系時，標題、說明、復活鈕、放棄鈕仍停在開啟當下的語言。本任務完成：
1. 戰鬥失敗、發條動能耗盡說明、二次機會說明、觀看廣告立即復活、結束戰鬥、今日復活次數已達上限、已移除廣告直接領取，全部走 ContentLoc。
2. 接 `Loc.locale_changed`，開著彈窗切語系整窗即時刷新。
3. 六語系詞條補齊（`zh_TW` 補齊 10 組核心鍵及戰鬥 HUD 相關鍵）。
4. 復活仍是 50% 生命、廣告次數規則不變。
5. 橫屏 750px（740～760px）、按鈕高 ≥50px（復活鈕 52px、結束鈕 52px、右上關閉鈕 50x50px）、全程零系統 emoji。

## 2. 交付檔案
- **彈窗核心**：`game/scripts/battle/battle_defeat_dialog.gd`
  - 增加 `_enter_tree()` / `_exit_tree()` / `_connect_loc_signal()` / `_disconnect_loc_signal()` / `_on_locale_changed()`
  - 增加 `_update_ui_texts()`，更新 `_title_lbl`、`_sub_lbl`、`_give_up_btn` 並呼叫 `_refresh_display()`
  - 命名節點 `TitleLbl`, `SubLbl`, `HintLbl`, `TipLbl`, `ReviveAdBtn`, `GiveUpBtn`, `CloseBtn`, `DefeatCard`
  - 提供輔助存取函式 `get_title_text()`, `get_subtitle_text()`, `get_hint_text()`, `get_tip_text()`, `get_revive_button_text()`, `get_give_up_button_text()`
- **戰鬥背景視圖連動 (0-QA25)**：`game/scripts/battle/battle_view.gd`
  - 在 `_on_locale_changed()` 補齊戰鬥 HUD 同屏切換：怒氣標籤（`battle.rage`）、陣營標籤（`battle.ally`/`battle.enemy`）、玩家名稱、木人樁名稱、頂部提示列、拇指操控區各按鈕（鎖定、換武、技能、暫停、攻擊、結束試招）
- **六語系詞條補齊**：
  - `game/data/i18n/content/zh_TW/ui.json`（補齊 19 組鍵）
- **具名單元測試**：`game/scripts/battle/test_battle_defeat_i18n.gd`
- **實機截圖腳本**：`tools/capture_battle_defeat_i18n.gd`
- **實機截圖存證（0-QA23 獨立目錄）**：
  - `proofs/battle-defeat-i18n/proof_01_battle_defeat_en.png`（英文全景實機，背後戰鬥場景同步切換 en，0-QA25）
  - `proofs/battle-defeat-i18n/crops/crop_01_battle_defeat_en.png`（英文彈窗局部裁切）
  - `proofs/battle-defeat-i18n/proof_02_battle_defeat_ja.png`（日文全景實機，背後戰鬥場景同步切換 ja，0-QA25）
  - `proofs/battle-defeat-i18n/crops/crop_02_battle_defeat_ja.png`（日文彈窗局部裁切）
  - `proofs/battle-defeat-i18n/proof_03_battle_defeat_zh_TW.png`（繁中全景基準對照）
  - `proofs/battle-defeat-i18n/crops/crop_03_battle_defeat_zh_TW.png`（繁中彈窗局部裁切）

## 3. 六語系詞條映射對照表

| Key | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|
| `戰鬥失敗` | `戰鬥失敗` | `战斗失败` | `Defeat` | `敗北` | `전투 패배` | `Derrota` |
| `發條動能耗盡，齒輪暫時停擺！` | `發條動能耗盡，齒輪暫時停擺！` | `发条动能耗尽，齿轮暂时停摆！` | `Clockwork kinetic energy depleted, gears brought to a halt!` | `ぜんまい動力が尽き、歯車が一時停止した！` | `태엽 동력이 다하여, 톱니가 잠시 멈췄습니다!` | `¡La energía de la cuerda se ha agotado y los engranajes se han detenido!` |
| `二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！` | `二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！` | `二次机会：观看赞助广告即可重新上链，立即以 50% 生命值重返战场！` | `Second Chance: Watch a sponsor ad to rewind, returning to battle with 50% HP!` | `セカンドチャンス：広告を視聴してぜんまいを巻き直し、HP 50% で即座に戦場へ復帰！` | `두 번째 기회: 스폰서 광고를 시청하여 태엽을 다시 감고, 즉시 HP 50%로 전장에 복귀합니다!` | `Segunda oportunidad: ¡mira un anuncio para recargar la cuerda y vuelve al combate con 50% de PS!` |
| `二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！` | `二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！` | `二次机会：已移除广告，可直接重新上链，立即以 50% 生命值重返战场！` | `Second Chance: Ads removed, rewind directly and return to battle with 50% HP immediately!` | `セカンドチャンス：広告削除済み、直接ぜんまいを巻き直して HP 50% で即座に戦場へ復帰！` | `두 번째 기회: 광고가 제거되어 바로 태엽을 다시 감고, 즉시 HP 50%로 전장에 복귀합니다!` | `Segunda oportunidad: ¡anuncios eliminados, puedes recargar la cuerda directamente y volver al combate con 50% de PS!` |
| `若是選擇承認敗北，將返回城鎮整頓裝備與招式。` | `若是選擇承認敗北，將返回城鎮整頓裝備與招式。` | `若是选择承认败北，将返回城镇整顿装备与招式。` | `Accepting defeat will return you to town to reorganize equipment and skills.` | `敗北を認める場合、町に戻って装備と技を整えます。` | `패배를 인정하면 마을로 돌아가 장비와 기술을 정비합니다.` | `Si aceptas la derrota, volverás a la aldea a organizar tu equipo y técnicas.` |
| `若是選擇承認敗北，將返還 2 點能量並返回整頓。` | `若是選擇承認敗北，將返還 2 點能量並返回整頓。` | `若是选择承认败北，将返还 2 点能量并返回整顿。` | `Admitting defeat will refund 2 energy and return to regroup.` | `敗北を認める場合、エネルギーが2点返還され、体勢を立て直します。` | `패배를 인정하면 에너지 2점을 반환받고 재정비하러 돌아갑니다.` | `Si aceptas la derrota, recuperarás 2 de energía y volverás a reagruparte.` |
| `觀看廣告立即復活  (%d/%d)` | `觀看廣告立即復活  (%d/%d)` | `观看广告立即复活  (%d/%d)` | `Watch Ad to Revive Instantly  (%d/%d)` | `広告を見て即座に復活  (%d/%d)` | `광고 보고 즉시 부활  (%d/%d)` | `Ver anuncio y revivir al instante  (%d/%d)` |
| `已移除廣告，直接領取  (%d/%d)` | `已移除廣告，直接領取  (%d/%d)` | `已移除广告，直接领取  (%d/%d)` | `Ads Removed, Claim Directly  (%d/%d)` | `広告削除済み、直接受取  (%d/%d)` | `광고 제거됨, 즉시 수령  (%d/%d)` | `Anuncios eliminados, reclamar directamente  (%d/%d)` |
| `今日復活次數已達上限 (0/%d)` | `今日復活次數已達上限 (0/%d)` | `今日复活次数已达上限 (0/%d)` | `Daily revives limit reached (0/%d)` | `本日の復活上限に達しました (0/%d)` | `오늘 부활 횟수 상한 도달 (0/%d)` | `Límite de resurrecciones diario alcanzado (0/%d)` |
| `結束戰鬥` | `結束戰鬥` | `结束战斗` | `End Battle` | `戦闘終了` | `전투 종료` | `Terminar combate` |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/battle-defeat-i18n/`，無修改或覆蓋其他任務之 proof 目錄。
- [x] **0-QA24（日／韓漢字核實、英文與西文無 CJK 殘留）**：
  - 英文全景中，彈窗標題為 `Defeat`、說明為 `Clockwork kinetic energy depleted, gears brought to a halt!`、按鈕為 `Watch Ad to Revive Instantly (3/3)`、`End Battle`，背景戰鬥 HUD 為 `Xiaobai`、`Rage`、`Training Dummy`、`Pause`、`End Trial`、`Attack`，零 CJK 漢字殘留。
  - 日文全景中，漢字（敗北、ぜんまい動力、歯車、一時停止、広告、復活、町、装備、技、戦闘終了、木人、味方、敵、怒気、試技終了、攻撃）均核實符合日本語當用漢字標準。
- [x] **0-QA25（彈窗以外同屏同步換語系）**：
  - 實機截圖中，背景戰鬥場景之玩家姓名（Xiaobai / シロ）、怒氣標籤（Rage / 怒気）、陣營標籤（Ally / 味方, Enemy / 敵）、木人樁名稱（Training Dummy / 木人）、頂部提示說明、底部操作按鈕（Pause, End Trial, Attack / 一時停止, 試技終了, 攻撃）均同步切換為該語系。
- [x] **零系統 Emoji**：所有介面與按鈕均無系統 emoji。
- [x] **尺寸規範**：橫屏寬度 750px（介於 740～760px），按鈕高 ≥50px（復活鈕 52px、結束鈕 52px、右上關閉按鈕 50x50px）。

## 5. 測試執行命令與驗證記錄

```bash
# 1. 無頭冒煙測試（0 SCRIPT ERROR）
godot --path game --headless --quit-after 3

# 2. 具名六語系即時切換單元測試
godot --path game --headless -s res://scripts/battle/test_battle_defeat_i18n.gd

# 3. 去廣告既有測試回歸
godot --path game --headless -s res://scripts/systems/test_remove_ads_mock.gd

# 4. 廣告獎勵機制既有測試回歸
godot --path game --headless -s res://scripts/systems/test_ad_reward_mock.gd
```
