# 戰鬥雜魚與關卡敵名六語系驗收報告 (enemy-name-i18n)

依據 `AGENTS.md`、`CLAUDE.md` 及 `skill_view(bravesoul, references/review.md)` 規範（0-QA15, 0-QA23, 0-QA24, 0-QA25）：

## 一、驗收要點與合規清單

1. **世界內容表 13 個雜魚／關卡敵名支援六語系 (zh_TW, zh_CN, en, ja, ko, es)**：
   - 雜魚：灰燼鼠 (`ash_rat`)、荒路匪徒 (`road_bandit`)、下水黏漿 (`sewer_slime`)、霧影 (`fog_shade`)、竹影拳靈 (`bamboo_spirit`)、林間風妖 (`forest_sprite`)、潮襲海盜 (`coast_raider`)、疤地焰靈 (`scar_wisp`)。
   - 特殊／副本：心魔 (`heart_demon`)、黑鏽浪人 (`black_ronin`)。
   - 秘境關卡小 Boss：黑鏽疤主 (`scar_lord`)、鏡廊殘影 (`mirror_wraith`)、沉船船長影 (`wreck_captain`)。
   - 全數對齊 `game/data/i18n/content/<locale>/enemy.json`，未重新造輪子或破壞既有約定譯名。

2. **戰鬥頂欄敵名與鎖定提示同步換語系**：
   - 戰鬥畫面 `BattleView` 監聽 `Loc.locale_changed` 信號。
   - 語系變更時：
     - `sim.units` 內所有敵方單位與當前敵方 `_primary_enemy()` 之 `display_name` 透過 `WorldContent.enemy_def(target_id)` 即時刷新為目標語系譯名。
     - 頂欄敵名標籤 `%EnemyName` 於 `_refresh_hud()` 即時更新顯示譯文。
     - 帶部位首領戰（如 `scar_lord`）之部位鎖定提示標籤 `_focus_hint` 及格擋提示 `parry_hint` 同步刷新為目標語系（如 `Part locked -> Overflow Core`、`Locked: Overflow Core` / `部位捕捉 → 溢れ核`、`捕捉：溢れ核`）。
     - 切回繁中 `zh_TW` 完整還原。

3. **0-QA23 目錄防覆蓋檢查**：
   - 本輪所有實機全景截圖與局部裁剪嚴格儲存於 `proofs/enemy-name-i18n/` 與 `proofs/enemy-name-i18n/crops/`。
   - 未覆蓋或更動任何本輪以外的 proof 目錄。

4. **0-QA24 既定譯名與漢字核驗**：
   - 查核日文字典：`ash_rat` ("灰燼鼠")、`fog_shade` ("霧影")、`heart_demon` ("心魔") 係沿用日文既定漢字譯名；`road_bandit` ("荒路の匪徒")、`bamboo_spirit` ("竹影の拳霊")、`scar_lord` ("黒錆の傷跡の主") 具備明確日語平假名助詞，經查字庫完全一致，非中文殘留。

5. **0-QA25 戰鬥全景同步多語系檢查**：
   - 驗證頂欄敵名、我方名稱 (Xiaobai/シロ)、我方標籤 (You/味方)、敵方標籤 (Foe/敵)、怒氣標籤 (Rage/怒気)、右下按鈕 (Pause/一時停止、Flee/逃走、Attack/攻撃)、頂部戰鬥引導說明、底部訊息框及部位面板全景元件，全數同步切換目標語言，無單一元件脫鉤殘留。

6. **零系統 emoji**：
   - 全介面與提示字串無任何系統 emoji。

## 二、實機截圖存證清單

| 檔案路徑 | 語系 | 內容摘要 | 驗證項目 |
|---|---|---|---|
| `proofs/enemy-name-i18n/proof_battle_en.png` | `en` | 雜魚戰全景 (`road_bandit`) | 頂欄敵名 `Road Bandit`、`Foe`、`You`、`Xiaobai`、`Rage`、`Pause`/`Flee`/`Attack` 全英無中文殘留 |
| `proofs/enemy-name-i18n/proof_battle_ja.png` | `ja` | 雜魚戰全景 (`road_bandit`) | 頂欄敵名 `荒路の匪徒`、`敵`、`味方`、`シロ`、`怒気`、`一時停止`/`逃走`/`攻撃` 全日文 |
| `proofs/enemy-name-i18n/proof_battle_zh_TW.png` | `zh_TW` | 雜魚戰全景 (`road_bandit`) | 頂欄敵名 `荒路匪徒`、繁體中文還原驗證 |
| `proofs/enemy-name-i18n/proof_miniboss_lock_en.png` | `en` | 關卡首領鎖定全景 (`scar_lord`) | 頂欄敵名 `Scar Lord of Blight Rust`、部位鎖定提示 `Part locked -> Overflow Core`、`Locked: Overflow Core` |
| `proofs/enemy-name-i18n/proof_miniboss_lock_ja.png` | `ja` | 關卡首領鎖定全景 (`scar_lord`) | 頂欄敵名 `黒錆の傷跡の主`、部位鎖定提示 `部位捕捉 → 溢れ核`、`捕捉：溢れ核` |

### 局部比對 (crops/)
- `crops/crop_road_bandit_en_enemy_hud.png`
- `crops/crop_road_bandit_ja_enemy_hud.png`
- `crops/crop_road_bandit_zh_TW_enemy_hud.png`
- `crops/crop_scar_lord_en_enemy_hud.png`
- `crops/crop_scar_lord_ja_enemy_hud.png`

## 三、自動化測試
- `TEST_FILTER=test_enemy_name_i18n ./tools/run_tests.sh`：PASSED (1/1)
  - 13 個敵名在 6 語系下共 78 組靜態斷言全綠。
  - `BattleSim.make_world_fight` display_name 斷言全綠。
  - `BattleView` 動態切換 en -> ja -> zh_TW 頂欄敵名與部位提示斷言全綠。
- `TEST_FILTER=test_qa_battle_name_fixes ./tools/run_tests.sh`：PASSED (1/1)
- `TEST_FILTER=test_battle_part_break_i18n ./tools/run_tests.sh`：PASSED (1/1)
- `godot --path game --headless --quit-after 3`：冒煙測試無 SCRIPT ERROR。
