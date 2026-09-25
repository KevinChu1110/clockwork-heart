# 瓷韻熊貓玩家可見名稱六語系落地驗收清單 (panda-i18n)

卡號：t_384547a6
執行人：阿宏（側案·程式 sideworker）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「瓷韻熊貓」、「武術家」、「禪道學徒生漆長袍」、「羊脂白瓷生漆塗裝」。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊（各 2092 個 key，zh_TW 134 個 key）。
   - grep 驗證：六語系均可精確 grep 到「瓷韻熊貓」與「武術家」key。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（五語系 content/ui.json 各 2092 個 key，全部對齊，I18N_OK）。

2. **創角擴充分頁選瓷韻熊貓連動：**
   - 擴充分頁選瓷韻熊貓，種族名稱（`The Porcelain Panda` / `磁韻パンダ` / `瓷韻熊貓`）、職業標籤（`【Monk】` / `【武術家】` / `【武術家 (Monk)】`）、外裝（`Zen Apprentice Lacquer Robe` / `禅道見習い生漆長袍` / `禪道學徒生漆長袍`）、塗裝（`Mutton-Fat White Porcelain Lacquer` / `羊脂白磁生漆塗装` / `羊脂白瓷生漆塗裝`）在各語系即時正確呈現。
   - 實機截圖存證（proofs/panda-i18n/）：
     - `proof_creation_panda_zh_TW.png`
     - `proof_creation_panda_en.png`
     - `proof_creation_panda_ja.png`

3. **衣櫥外裝／塗裝標籤連動（含大廳背景/Dock 0-QA25）：**
   - 大廳打開衣櫥彈窗，切換語系後衣櫥卡片標籤即時更新；左下徽章正確顯示【The Porcelain Panda · Monk】、【磁韻パンダ · 武術家】、【瓷韻熊貓 · 武術家 (Monk)】；大廳背景（Shop/ショップ、Settings/設定、出征按鈕）與底部 Dock（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties, Adventure Bag / ぜんまい新村, 冒険バッグ）同步刷新對應語言，無局部殘留繁中。
   - 實機截圖存證（proofs/panda-i18n/）：
     - `proof_wardrobe_panda_zh_TW.png`
     - `proof_wardrobe_panda_en.png`
     - `proof_wardrobe_panda_ja.png`

4. **日／韓漢字核實（0-QA24）：**
   - 日文下角色名顯示「磁韻パンダ」、職業顯示「【武術家】」，經查核 `ja/ui.json` 詞條本即設定為漢字 `"武術家": "武術家"`，符合 0-QA24 規範，非漏翻。

5. **無頭冒煙與回歸測試：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：1/1 PASS。
   - `TEST_FILTER=creation ./tools/run_tests.sh`：4/4 PASS。
   - `TEST_FILTER=wardrobe ./tools/run_tests.sh`：2/2 PASS。
   - `TEST_FILTER=panda ./tools/run_tests.sh`：1/1 PASS。
