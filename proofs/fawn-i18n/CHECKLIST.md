# 翠角鹿玩家可見名稱六語系落地驗收清單 (fawn-i18n)

卡號：t_b9db63af
執行人：阿翔（側案·工程師 sideworker2）
日期：2026-09-27

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「翠角鹿」、「鹿」、「遊俠」、「翡翠林緣巡守工裝」、「翡翠林緣巡守背帶工裝」、「雙色沖壓原木紋金屬板」、「沖壓雙色象牙米白與淺褐原木紋金屬板」、「翠木角尺複合機關弓」、「自翡翠深林守護巡林的發條小鹿，米白淺褐薄鐵皮板件，精密黃銅游標卡尺角尺天線與減震馬蹄墊。」、「墨綠輕布料披肩配黃銅皮扣巡守工裝」、「沖壓雙色象牙米白與淺褐原木紋金屬板，黃銅鉚釘包邊」、「卸除外裝，呈現米白淺褐原木紋金屬素體」、「無外裝 (裸機素體)」。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊（各 3142 個 key，zh_TW 1253 個 key）。
   - grep 驗證：六語系均可精確 grep 到「翠角鹿」、「鹿」、「遊俠」等核心 key。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（五語系 content/ui.json 各 3142 個 key，全部對齊，I18N_OK）。

2. **創角擴充分頁選翠角鹿連動：**
   - 擴充分頁選翠角鹿，種族名稱（`The Emerald Fawn` / `翠角鹿`）、職業標籤（`【Ranger】` / `【レンジャー】` / `【遊俠 (Ranger)】`）、外裝（`Emerald Scout Harness Tunic` / `翡翠林縁巡守サスペンダー作業着` / `翡翠林緣巡守背帶工裝`）、塗裝（`Stamped Ivory & Light Woodgrain Plate` / `スタンピング象牙ホワイト＆薄褐色木目調板` / `沖壓雙色象牙米白與淺褐原木紋金屬板`）、武器（`Verdant Caliber-Horn Composite Bow` / `翠木角尺複合からくり弓` / `翠木角尺複合機關弓`）在各語系即時正確呈現。
   - 實機截圖存證（proofs/fawn-i18n/）：
     - `proof_creation_fawn_zh_TW.png`
     - `proof_creation_fawn_en.png`
     - `proof_creation_fawn_ja.png`

3. **衣櫥外裝／塗裝標籤連動（含大廳背景/Dock 0-QA25）：**
   - 大廳打開衣櫥彈窗，切換語系後衣櫥卡片標籤即時更新；左下徽章正確顯示【The Emerald Fawn · Ranger】、【翠角鹿 · レンジャー】、【翠角鹿 · 遊俠 (Ranger)】；篩選標籤顯示【Fawn】/【鹿】/【사슴】/【Ciervo】；跨族全部列表卡片前綴顯示 [Fawn] / [鹿] / [사슴] / [Ciervo]；大廳背景與底部 Dock（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties, Adventure Bag / ぜんまい新村, 冒険バッグ）同步刷新對應語言，無局部殘留繁中。
   - 實機截圖存證（proofs/fawn-i18n/）：
     - `proof_wardrobe_fawn_zh_TW.png`
     - `proof_wardrobe_fawn_en.png`
     - `proof_wardrobe_fawn_ja.png`

4. **日／韓漢字核實（0-QA24）：**
   - 日文下角色名顯示「翠角鹿」、職業顯示「【レンジャー】」，經查核 `ja/ui.json` 種族本即設定為漢字 `"翠角鹿": "翠角鹿"`，符合 0-QA24 規範，非漏翻。

5. **無頭冒煙與回歸測試：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：37/37 PASS。
   - `TEST_FILTER=creation ./tools/run_tests.sh`：7/7 PASS。
   - `TEST_FILTER=wardrobe ./tools/run_tests.sh`：3/3 PASS。
   - `TEST_FILTER=fawn ./tools/run_tests.sh`：3/3 PASS。
