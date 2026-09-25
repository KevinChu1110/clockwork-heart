# 碧箸蛙玩家可見名稱六語系落地驗收清單 (frog-i18n)

卡號：t_12511970
執行人：阿翔（側案·工程師）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度：**
   - 包含詞條：「碧箸蛙」、「碧簧蛙」（相容別名）、「忍者」、「碧箸巡林客工裝」、「碧簧巡林客工裝」（相容別名）、「原廠薄荷翡翠綠」、「原廠薄荷翡翠綠琺瑯烤漆」。
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入且 key 數 100% 對齊。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（各 2080 個 key，I18N_OK）。

2. **創角擴充分頁選碧箸蛙連動：**
   - 擴充分頁選碧箸蛙，種族名稱（`The Spring-Leg Frog` / `碧箸蛙`）、職業標籤（`【Ninja】` / `【忍者】`）、外裝（`Spring Forest Courier Overalls` / `碧箸巡林客作業着` / `碧箸巡林客工裝`）、塗裝（`Stock Mint Emerald Green` / `純正ミントエメラルドグリーンエナメル塗装` / `原廠薄荷翡翠綠`）在各語系即時正確呈現。
   - 實機截圖：
     - `proof_creation_frog_zh_TW.png`
     - `proof_creation_frog_en.png`
     - `proof_creation_frog_ja.png`

3. **衣櫥外裝／塗裝標籤連動（含大廳背景/Dock 0-QA25）：**
   - 大廳打開衣櫥彈窗，切換語系後衣櫥卡片標籤即時更新；大廳背景（能量、金幣、星屑、商城、設置、冒險出征）與底部 Dock（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties, Adventure Bag）同步刷新對應語言，無局部殘留繁中。
   - 實機截圖：
     - `proof_wardrobe_frog_zh_TW.png`
     - `proof_wardrobe_frog_en.png`
     - `proof_wardrobe_frog_ja.png`

4. **無頭冒煙與回歸測試：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `test_character_creation_flow.gd`：CHARACTER_CREATION_OK 全項通過。
   - `test_creation_race_tabs.gd`：CREATION_RACE_TABS_OK 全項通過。
