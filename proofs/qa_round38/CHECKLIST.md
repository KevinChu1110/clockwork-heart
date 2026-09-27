# 探索性 QA 第三十八輪：戰鬥部位已破六語系合主線後驗收清單 (qa-round38)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_e037f4a3`（🤖 平台與維運｜探索性 QA：戰鬥部位已破六語系合主線後找破圖）
- **交付目錄**：`proofs/qa_round38/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/qa_round38/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：英文與繁中語系專有名詞比對語系檔，確認詞條符合既定譯名設定（如 Xiaobai、Leo、Helm、Lion-guard heavy shield、Broken 等）。
  - `review.md 0-QA25`：全畫面連動查驗，彈窗及背景 UI（頂部狀態列、四殿堂卡、出征卡、底部 Dock、戰鬥場景 HUD 與日誌）同步連動同一語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_lobby_zh_TW.png` | 大廳繁中全景（頂欄／四殿堂卡／右側裝備與出征卡／底部5個Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 02 | `proof_02_lobby_en.png` | 大廳英文全景（頂欄／四殿堂卡／右側裝備與出征卡／底部5個Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 03 | `proof_03_creation_en.png` | 創角英文全景（分頁Launch／5張種族卡／屬性數值面板／底部確認按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 見問題清單 | 標記已知待辦 (PASS w/ Note) |
| 04 | `proof_04_wardrobe_en.png` | 衣櫥英文全景（英雄換裝彈窗／種族過濾／卡片／底部按鈕／大廳底層背景） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 見問題清單 | 標記已知待辦 (PASS w/ Note) |
| 05 | `proof_05_battle_broken_zh_TW.png` | 戰鬥部位已破繁中全景（Boss部位欄「[已破]」／玩家HUD／提示／日誌／按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 06 | `proof_06_battle_broken_en.png` | 戰鬥部位已破英文全景（Boss部位欄「[Broken]」／玩家HUD／提示／日誌／按鈕） | ⚠️ 頂部提示過長致SideBars水平溢出 | ✓ 零 | ⚠️ 左右HUD遭螢幕邊緣截斷 | ✓ 100% 英文 | 發現破版（見問題清單 3，待修） |

---

## 二、 Vision 視覺顯微審核逐張結論

1. **`proof_01_lobby_zh_TW.png`**：
   - 頂部狀態列（Lv.10 小白、戰力 64、能量 15/15、金幣 1,000、星屑 0、商城、設置）自製圖標完整，無 Emoji，排版工整無截字。
   - 左側四殿堂卡（天宮鐵匠、手藝工坊、演武競技、冒險委託）標題與副標題排版清晰，繁體中文用字規範。
   - 右側裝備欄（外裝、武器、發條、奇玩）與冒險出征卡完整容納於容器內。
   - 底部五個 Dock 按鈕（發條新村、角色裝備、四區出征、聚魂殿堂、冒險背包）居中對齊良好，全畫面無破圖、無系統 Emoji。

2. **`proof_02_lobby_en.png`**：
   - 遵守 0-QA25，大廳背景、頂欄、左右側與底部 Dock 同步切換至英文：
     - 頂部狀態列（Lv.10 Xiaobai / Power 64 / Energy 15/15 / Gold 1,000 / Stardust 0 / Shop / Settings）。
     - 左側四殿堂卡（Celestial Blacksmith / Craft Workshop / Martial Arena / Adventure Bounties）。
     - 右側出征卡（Campaign Sortie · Current Main Story / Region 2 · Lands of White Fog (2-4 BOSS) / Set Out to Battle）。
     - 底部 Dock（Cogwheel Hamlet / Hero Gear / Four Regions / Soul Hall / Adventure Bag）。
   - 英文長度適應良好，零文字截斷、零溢出、零系統 Emoji，100% 英文無中文殘留。

3. **`proof_03_creation_en.png`**：
   - 頂部分頁標籤（Launch / Expansion）、5張首發種族卡（Clockwork Rabbit, Astral Fox, Gilded Lion, Forge Boar, Spring Macaque）與底部按鈕（Reset Defaults, Confirm Selection · Begin Journey, Back）皆完整英文化且排版正常。
   - 全畫面零破圖、零系統 Emoji、無文字裁切。
   - 語系混雜部分：外裝與塗裝卡片名稱（原廠象牙白等）及左側職業後綴（【劍士】）仍為中文，對應現有待辦卡 `creation-variant-i18n`（創角外裝與塗裝名稱六語系），本單不修並詳列於第三節。

4. **`proof_04_wardrobe_en.png`**：
   - 遵守 0-QA25，背後大廳底層（頂欄、左側功能、底部 Dock）同步切換為英文（Lv.10 Xiaobai / Cogwheel Hamlet / Adventure Bag 等）。
   - 衣櫥彈窗大標題（Clockwork Wardrobe · Hero Outfits）、副標題、種族標籤列（Rabbit, Fox, Lion...）、底部按鈕（Reset, Random, Confirm Outfit · Apply New Look）皆完整英文化，排版無破圖、零系統 Emoji。
   - 語系混雜部分：外裝卡片第2、3張（蒸氣工匠吊帶工作裝、皇家巡遊金屬禮服）與底漆卡片（原廠象牙白、黃銅原金拋光、午夜深藍烤漆）仍為中文，同屬待辦卡 `creation-variant-i18n`，本單不修。

5. **`proof_05_battle_broken_zh_TW.png`**（特寫：`crops/crop_part_hud_zh_TW.png`）：
   - 右上角 Boss 部位血條欄中，破損盾牌部位清晰顯示為 `甲·獅衛重盾 [已破]`，血條呈灰色破壞狀態，文字與右側血條保持安全間隔，無重疊或截字。
   - 頂部鎖定提示（`部位鎖定 → 獅衛重盔`）、左側玩家 HUD（`小白`、`HP 50/50 · 武 16/16`、粉紅血條、怒氣條）與右側/左側邊界保持標準 28px 安全邊距，無貼邊裁切。
   - 下方戰鬥日誌與右下技能按鈕（暫停、逃離、攻擊）繁中顯示工整，全畫面零系統 Emoji、無破圖。

6. **`proof_06_battle_broken_en.png`**（特寫：`crops/crop_part_hud_en.png`）：
   - 右上角 Boss 部位血條欄中，破損盾牌部位清晰顯示為 `l·Lion-guard heavy shield [Broken]`，標籤尾端 `[Broken]` 完整無缺，血條呈灰色破壞狀態，部位破壞在地化本身顯示正常。
   - 下方戰鬥日誌（操作提示、技能說明、對白）與右下按鈕（Pause, Flee, Attack）全數英文化，全畫面零系統 Emoji。
   - **發現嚴重水平溢出與截字破版**：
     - 頂部 `PartFocusHint` / `ParryHint` 英文提示字串長達 87 字元（`Locked: Knight's heavy helm · Tab to switch · Armor break lowers defense / Crown break enrages`），導致頂部 `SideBars`（HBoxContainer）最小寬度超出螢幕 1280px。
     - 因 `SideBars` 設定 `grow_horizontal = 2`（Both），超寬後向左右兩側同時外擴溢出：
       - 左側玩家 HUD 貼齊 $x=0$：角色名 `Xiaobai` 完全被推擠至螢幕左外裁切，血量文字開頭遭截斷為 `0/50 · Wpn 16/16`，粉紅血條無留白邊距。
       - 右側 Boss HUD 貼齊 $x=1279$：Boss 名稱右端與血條右端超出右螢幕邊界截斷。
     - 詳見第三節問題清單第 3 項，依任務規範記錄「什麼輸入 → 什麼壞掉」，本單不修。

---

## 三、 玩家可見問題清單（依規範「什麼輸入 → 什麼壞掉」，本單不修）

本輪探索性 QA 依規範逐張檢視，發現以下現存語系未覆蓋與介面破版項目：

1. **創角外觀細項與職業後綴未英文化**：
   - **輸入**：語言設定切換至英文（en）→ 進入創角介面（Creation）。
   - **現象**：
     - 左側角色職業標籤顯示為 `【Clockwork Rabbit • 劍士】`，後綴「劍士」未翻譯。
     - 左側背景介紹文字仍為繁中。
     - 右側 Costume 欄位中文副標（`經典紅藍胡桃鉗...`）與 Chassis 欄位名稱（`原廠象牙白`）仍為繁中。
   - **歸屬**：此為既有待辦 `docs/PROJECTS.json` 中的 `creation-variant-i18n`（創角外裝與塗裝名稱六語系，草稿狀態），本單不修。

2. **衣櫥部分外裝與底漆卡片名稱未英文化**：
   - **輸入**：語言設定切換至英文（en）→ 大廳點擊英雄外觀進入衣櫥（Wardrobe）。
   - **現象**：
     - Outfits 卡片第 2、3 套顯示為繁中「`蒸氣工匠吊帶工作裝`」、「`皇家巡遊金屬禮服`」。
     - Paint Finish 卡片全數顯示為繁中「`原廠象牙白`」、「`黃銅原金拋光`」、「`午夜深藍烤漆`」。
   - **歸屬**：同屬待辦項目 `creation-variant-i18n`，本單不修。

3. **英文戰鬥頂部 HUD 水平溢出破版（導致左右兩側玩家與 Boss HUD 遭螢幕邊緣截斷）**：
   - **輸入**：語言設定切換至英文（en）→ 進入戰鬥（Boss Leo）。
   - **現象**：
     - 頂部提示（`PartFocusHint` / `ParryHint`）英文提示字串長達 87 字元（`Locked: Knight's heavy helm · Tab to switch · Armor break lowers defense / Crown break enrages`），導致 `SideBars`（HBoxContainer）容器之最小寬度超出 1280px。
     - 在 `grow_horizontal = 2` 作用下向左右兩側溢出，導致：
       - 左側玩家 HUD 被推擠貼齊 $x=0$，玩家名稱 `Xiaobai` 完全被推出螢幕左側不可見，血量文字遭截斷（僅剩 `0/50 · Wpn 16/16`，原 `HP 50/50` 消失），左邊界無標準 28px 留白。
       - 右側 Boss HUD 被推擠貼齊 $x=1279$，Boss 名稱與血條右端超出螢幕右邊界截斷。
   - **歸屬**：戰鬥介面頂部 HUD / `SideBars` 之最小寬度約束與換行排版缺失。依任務要求「本單不修，寫明輸入與壞掉現象」，留待後續戰鬥 UI 排版任務開卡修復。

---

## 四、 總體結論

**戰鬥部位「已破」六語系標籤在地化驗證完成，但發現英文戰鬥頂部 HUD 存在水平溢出破版**。

1. **部位已破在地化**：剛合進主線之戰鬥部位「已破」六語系標籤（繁中 `[已破]`、英文 `[Broken]`）在實機全景與特寫下，標籤字樣完整、血條呈灰色破壞狀態、無 Emoji，在地化本體無破圖。
2. **大廳與彈窗連動**：大廳底層背景、頂欄與底部 Dock 均嚴格遵守 0-QA25 同步連動同一語系；創角與衣櫥之既有未英文化項目已確認對齊待辦卡 `creation-variant-i18n`。
3. **發現玩家可見破版（本單不修，如實記錄）**：在英文戰鬥介面下，因頂部提示字串長達 87 字元，造成 `SideBars` 水平溢出破版，左右兩側玩家 HUD 與 Boss HUD 均遭到螢幕邊界嚴重截斷（Xiaobai 角色名被推到螢幕外、血量文字截斷、Boss HUD 溢出）。已依任務第 3 條與審查意見如實記錄「什麼輸入 → 什麼壞掉」，本單不修，交由主管與工程師安排排版修復卡。
