# 玄機龜玩家可見名稱六語系落地驗收清單 (tortoise-i18n)

卡號：t_15816ac0
執行人：阿翔（側案·工程師）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「玄機龜」、「法師」、「天元道場玄機護甲」、「原廠青銅古翠綠」。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊（各 2091 個 key）。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（各 2091 個 key，I18N_OK）。

2. **創角擴充分頁選玄機龜連動：**
   - 擴充分頁選玄機龜，種族名稱（`The Xuanji Tortoise` / `玄機龜`）、職業標籤（`【Mage】` / `【法師】` / `【法師 (mage)】`）、外裝（`Zen Dojo Xuanji Harness` / `天元道場玄機護甲`）、塗裝（`Stock Antique Bronze Emerald Green` / `純正青銅古翠緑` / `原廠青銅古翠綠`）在各語系即時正確呈現。
   - 實機截圖存證（proofs/tortoise-i18n/）：
     - `proof_creation_tortoise_zh_TW.png`
     - `proof_creation_tortoise_en.png`
     - `proof_creation_tortoise_ja.png`

3. **衣櫥外裝／塗裝標籤連動（含大廳背景/Dock 0-QA25）：**
   - 大廳打開衣櫥彈窗，切換語系後衣櫥卡片標籤即時更新；大廳背景（能量、金幣、星屑、商城、設置、冒險出征）與底部 Dock（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties, Adventure Bag / ぜんまい新村, 冒険バッグ）同步刷新對應語言，無局部殘留繁中。
   - 實機截圖存證（proofs/tortoise-i18n/）：
     - `proof_wardrobe_tortoise_zh_TW.png`
     - `proof_wardrobe_tortoise_en.png`
     - `proof_wardrobe_tortoise_ja.png`

4. **無頭冒煙與回歸測試：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：1/1 PASS。
   - `TEST_FILTER=creation ./tools/run_tests.sh`：4/4 PASS。
   - `TEST_FILTER=wardrobe ./tools/run_tests.sh`：2/2 PASS。
   - `TEST_FILTER=tortoise ./tools/run_tests.sh`：2/2 PASS。
