# 鋼岳象玩家可見名稱六語系落地驗收清單 (elephant-i18n)

卡號：t_ba84bd40
執行人：阿宏（側案·程式）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「鋼岳象」、「戰士」、「巨輪工坊厚鋼工裝」、「原廠巨輪工坊黃銅原金」，以及相容別名「巨輪工坊先鋒吊帶甲」、「原廠黃銅原金」。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（各 2087 個 key，I18N_OK）。

2. **創角擴充分頁選鋼岳象連動：**
   - 擴充分頁選鋼岳象，種族名稱（`The Colossus Elephant` / `鋼岳象`）、職業標籤（`【Warrior】` / `【戰士】`）、外裝（`Great Cog Foundry Heavy Steel Overalls` / `巨輪工房厚鋼作業着` / `巨輪工坊厚鋼工裝`）、塗裝（`Stock Great Cog Foundry Brass Gold` / `純正巨輪工房黄銅原金` / `原廠巨輪工坊黃銅原金`）在各語系即時正確呈現。
   - 實機截圖存證（proofs/elephant-i18n/）：
     - `proof_creation_elephant_zh_TW.png`
     - `proof_creation_elephant_en.png`
     - `proof_creation_elephant_ja.png`

3. **衣櫥外裝／塗裝標籤連動（含大廳背景/Dock 0-QA25）：**
   - 大廳打開衣櫥彈窗，切換語系後衣櫥卡片標籤即時更新；大廳背景（能量、金幣、星屑、商城、設置、冒險出征）與底部 Dock（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties, Adventure Bag）同步刷新對應語言，無局部殘留繁中。
   - 實機截圖存證（proofs/elephant-i18n/）：
     - `proof_wardrobe_elephant_zh_TW.png`
     - `proof_wardrobe_elephant_en.png`
     - `proof_wardrobe_elephant_ja.png`

4. **無頭冒煙與回歸測試：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：1/1 PASS。
   - `test_character_creation_flow.gd`：CHARACTER_CREATION_OK 全項通過。
   - `test_creation_race_tabs.gd`：CREATION_RACE_TABS_OK 全項通過。
