# 《發條之心》再次挑戰雙按鈕與鐵匠三槽鍛造全面回歸驗收報告 (t_2554e391)

- **驗收審查員**：小婷（發條之心·測試 sideqa）
- **關聯任務**：`t_2554e391`（🤖 平台與維運｜再次挑戰雙按鈕與鐵匠三槽鍛造合併後的全面回歸驗收）
- **前置任務**：`t_1ab442e6`（三分支乾淨合併至 main：`agent/20261009-defeat-retry-t_94274c40`、`agent/20261010-victory-replay-t_e5eff657`、`agent/20261009-forge-loadout-t_5fbd8e22`，最新 commit `feaead9f`）
- **交付存證目錄**：`proofs/t_2554e391/`
- **遵循規範**：
  - `review.md` 人因人機工程與多巴胺視覺規範：按鈕熱區 >= 48px（實際 >= 52px）、立體果凍厚底 5~6px、圓角 16~24px、零 Emoji、多巴胺色盤（金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A、深藍紫描邊 #1F1A3A）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 彈窗與晶片元件正確佈局尺寸（min_size >= 44px），零折行、零溢出、零重疊。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留（依 review.md 0-QA28 驗證）。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_battle_defeat_retry_zh_TW.png` | `BattleDefeatDialog` 戰敗結算彈窗：展示「再次挑戰」按鈕（`BtnRetryStage`，尺寸 170x52px，6px 薄荷綠立體厚底，圓角 20px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `1492cdd26262` | 合格 (PASS) |
| 02 | `proof_02_battle_defeat_retry_en.png` | 英文語系 (en) `BattleDefeatDialog`：顯示 "Retry Stage"，零 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `03cb4ad13e40` | 合格 (PASS) |
| 03 | `proof_03_battle_defeat_restarted_combat.png` | 點擊戰敗「再次挑戰」後連動 `BattleView`：扣除 1 點能量、重開 ash_rat 戰鬥、玩家滿血滿狀態、原戰敗彈窗銷毀、全景實機戰鬥中 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `ad0c26835fce` | 合格 (PASS) |
| 04 | `proof_04_battle_victory_replay_zh_TW.png` | `BattleVictoryDialog` 1-1 出征勝利結算彈窗：展示暖橘立體厚底「再次挑戰」按鈕（`BtnReplayStage`，尺寸 170x52px，與「收下完成」「挑戰下一關」整齊並列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `efb7f4f1cac2` | 合格 (PASS) |
| 05 | `proof_05_battle_victory_final_stage_replay.png` | `BattleVictoryDialog` 4-4 末關勝利結算：自動隱藏「挑戰下一關」，但「再次挑戰」保持顯示，支援重複刷關 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `58764a009146` | 合格 (PASS) |
| 06 | `proof_06_battle_victory_replay_en.png` | 英文語系 (en) `BattleVictoryDialog`：顯示 "Retry Stage"，零 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `1a7f9d5f34e4` | 合格 (PASS) |
| 07 | `proof_07_battle_victory_replayed_combat.png` | 點擊勝利「再次挑戰」後連動 `BattleView`：扣除 1 點能量、重複挑戰 1-1 關卡、玩家滿血滿狀態、原勝利彈窗銷毀、全景實機戰鬥中 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `7e9588e3bab5` | 合格 (PASS) |
| 08 | `proof_08_forge_slot1_main_weapon.png` | `ForgeDialog` 天宮鐵匠三欄武器槽位（`WeaponSlotChipRow`，晶片高度 46px >= 44px）：展示槽位 1 微末之刃（T1 凡品，副詞條：暫無） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `12ee6aa382a7` | 合格 (PASS) |
| 09 | `proof_09_forge_slot2_sub_weapon.png` | 點擊槽位 2 切換至副手武器（鐵骨重鎚 T2）：品質色階即時切換為【上品】、副詞條即時切換為【暴擊 +5.0% · 防禦 +8】、攻擊力 +24、升階花費 80 金幣 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `e6b6ee8ec1ee` | 合格 (PASS) |
| 10 | `proof_10_forge_slot3_special_weapon.png` | 點擊槽位 3 切換至絕技武器（赤炎神弓 T3）：品質色階即時切換為【秘寶】、副詞條即時切換為【暴擊 +12.5% · 生命 +50】、攻擊力 +36 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `d53253dc30d7` | 合格 (PASS) |
| 11 | `proof_11_forge_slot2_upgraded.png` | 切回槽位 2 點擊「升階鍛造」：鐵骨重鎚從 T2 升至 T3、攻擊力提升至 +26、金幣正確扣除、面板數值與 Chip 1 即時連動刷新 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `f37444b8719c` | 合格 (PASS) |
| 12 | `proof_12_forge_dialog_en_no_cjk.png` | 英文語系 (en) 下 `ForgeDialog` 介面：顯示 "Slot 1", "Slot 2", "Slot 3", "Quality Tier: Common", "Sub-stats: None"，零 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `053a15c822cc` | 合格 (PASS) |

- **防作弊與真實性校驗**：12 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），對應 12 張特寫裁切圖於 `crops/` 目錄。
- **視覺複檢**：所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **再次挑戰** | 再次挑战 | Retry Stage | 再挑戦 | 다시 도전 | Reintentar etapa |
| **槽位 1** | 槽位 1 | Slot 1 | スロット 1 | 슬롯 1 | Ranura 1 |
| **槽位 2** | 槽位 2 | Slot 2 | スロット 2 | 슬롯 2 | Ranura 2 |
| **槽位 3** | 槽位 3 | Slot 3 | スロット 3 | 슬롯 3 | Ranura 3 |
| **品質色階：凡品** | 品质色阶：凡品 | Quality Tier: Common | 品質等級：凡品 | 품질 등급: 일반 | Nivel de calidad: Común |
| **品質色階：上品** | 品质色阶：上品 | Quality Tier: Rare | 品質等級：上品 | 품질 등급: 고급 | Nivel de calidad: Raro |
| **品質色階：秘寶** | 品质色阶：秘宝 | Quality Tier: Epic | 品質等級：秘宝 | 품질 등급: 희귀 | Nivel de calidad: Épico |
| **副詞條：暫無** | 副词条：暂无 | Sub-stats: None | 追加効果：なし | 보조 옵션: 없음 | Sub-atributos: Ninguno |
| **微末之刃** | 微末之刃 | Humble Blade | 微末の刃 | 미천한 검 | Hoja Humilde |
| **鐵骨重鎚** | 铁骨重锤 | Iron Bone Hammer | 鉄骨の重槌 | 철골 중망치 | Martillo Óseo |
| **赤炎神弓** | 赤炎神弓 | Blazing Bow | 赤炎の神弓 | 적염의 신궁 | Arco Llameante |

---

## 三、 測試套件與審查指令驗證結果

1. **無頭冒煙測試**：
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR，編譯與加載完全正常。
2. **單元與驗收測試套件**：
   - `test_battle_defeat_retry.gd`：`TEST_BATTLE_DEFEAT_RETRY_OK`（通過）
   - `test_battle_victory_replay.gd`：`TEST_BATTLE_VICTORY_REPLAY_OK`（通過）
   - `test_forge_weapon_loadout_slots.gd`：`TEST_FORGE_WEAPON_LOADOUT_SLOTS_OK`（通過）
   - `test_i18n.gd`：`I18N_OK`（全部語系鍵值對齊通過）
3. **全站回歸驗證腳本**：
   - `res://../tools/capture_regression_t_2554e391.gd`：`TEST_REGRESSION_T_2554E391_OK`（12 張實機截圖存證與 SHA256 檢核全數通過）。
   - `python3 tools/verify_proofs_t_2554e391.py`：`[OK] 全部 12 張實機全景截圖與 12 張特寫裁切圖校驗完全合格！`
4. **自動化審查檢查器**：
   - `/root/bin/clock-check /opt/side/bravesoul-game`：缺 .import 0 個，素材完整。
