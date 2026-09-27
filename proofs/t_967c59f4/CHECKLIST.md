# 驗收清單：t_967c59f4 勝利結算機芯掉落卡六語系不露中文

- **任務編號**：`t_967c59f4`
- **負責人**：阿宏（側案·程式）
- **專案進度 ID**：`victory-core-drop-i18n`
- **參照規範**：`AGENTS.md` (驗證階梯), `review.md` (0-QA5, 0-QA23, 0-QA24, 0-QA26, 0-QA27, 0-QA28)

---

## 一、實機截圖成果清單

| 編號 | 檔名 | 語系 | 驗收重點 | 瑕疵數 | 系統 Emoji | 截字溢出 | 判定 |
|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_en_victory_core_drop.png` | 英文 (en) | 結算卡標題「Victory」、副標「Stage cleared! Core part looted.」、色階「[Gold Tier]」（半形方括號無全形符號）、屬性「Atk+69 · HP+340」、說明「Can calibrate 7 times · Safety spring protected」、經驗「Combat EXP / EXP +450」、鐵屑「Part Break / Scrap Iron +60」、雙按鈕「Equip Now / Collect」（高 ≥50px、多巴胺亮色） | 零 | 零 | 無 | **通過 (PASS)** |
| 02 | `proof_02_ja_victory_core_drop.png` | 日文 (ja) | 結算卡標題「戦闘勝利」、副標「ステージ討伐成功！コアパーツを獲得しました」、部位名「ぜんまい発電機」、色階「【金階】」、屬性「攻+69 · 血+340」、說明「7回調整可能 · 安全スプリング保護」、經驗「戦闘経験値 / 経験値 +450」、鐵屑「部位破壊 / 鉄屑 +60」、雙按鈕「今すぐ装備 / 受け取る」（高 ≥50px、多巴胺亮色） | 零 | 零 | 無 | **通過 (PASS)** |

---

## 二、六語系 ui.json 對齊檢驗 (0-QA27, 0-QA28)

全 6 語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）針對結算卡相關鍵值皆已完整補齊並通過自動化檢驗：

1. **色階與標點**：
   - 英文 (en)：`"【金階】": "[Gold Tier]"`、`"【白階】": "[White Tier]"`、`"【%s】": "[%s]"`，徹底消弭全形中文括號（U+3010/U+3011）與 CJK 殘留。
   - 日文 (ja)：`"【金階】": "【金階】"`、`"【綠階】": "【緑階】"`（採用新字體「緑」U+7DD1，杜絕繁中「綠」殘留）、`"【橘階】": "【橙階】"`、`"【藍階】": "【青階】"`、`"【紅階】": "【赤階】"`。
2. **數值與狀態**：
   - `"攻+%d"`, `"防+%d"`, `"血+%d"`, `"暴擊+%.1f%%"`, `"暴傷+%.0f%%"`, `"標準數值"`。
   - 六語系 ui.json 鍵值齊備非空，切換語系即時生效。
3. **獎勵與回饋**：
   - `"戰鬥經驗"`, `"經驗 +%d"`, `"經驗 +0"`, `"經驗 +0（已達上限）"`。
   - `"部位破壞"`, `"鐵屑 +%d"`, `"鐵屑 +0"`。
   - `"已收進機芯背包"`, `"已成功替換裝備至【%s】槽位！"`。
4. **佔位文字安全**：
   - `_build_ui()` 中預設文字全數改為空字串 `""`，進入畫面第一次即由 `_refresh_display()` 走當前語系 `_t()`，玩家不會看見任何中文佔位殘影。

---

## 三、驗證指標與測試結果

- **diff 檢查**：`git diff | grep "^\+[^+].*\.text ="` 確認所有玩家可見字賦值右側皆含 `_t(`。
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 無 SCRIPT ERROR。
- **單元測試**：
  - `TEST_FILTER=core_battle_drop ./tools/run_tests.sh`: 1/1 PASS
  - `TEST_FILTER=colossus_exp ./tools/run_tests.sh`: 1/1 PASS
  - `TEST_FILTER=colossus_part_scrap ./tools/run_tests.sh`: 1/1 PASS
  - `TEST_FILTER=test_core ./tools/run_tests.sh`: 4/4 PASS
- **截圖驗收**：經 `vision_analyze` 逐像素審核，英文圖零 CJK 字元，日文圖無繁中殘留，按鈕熱區高度 ≥ 50px，符合多巴胺高飽和色盤，零系統 Emoji。
