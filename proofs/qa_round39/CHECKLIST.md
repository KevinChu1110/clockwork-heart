# 探索性 QA 第三十九輪：英文戰鬥頂欄修復合主線後驗收清單 (qa-round39)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_eabd9508`（🤖 平台與維運｜探索性 QA：英文戰鬥頂欄修復合主線後找破圖）
- **交付目錄**：`proofs/qa_round39/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/qa_round39/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：英文與多語系專有名詞比對語系檔，確認詞條符合既定譯名設定（如 Xiaobai、Titan Overseer Leo、Knight's heavy helm 等）。
  - `review.md 0-QA25`：全畫面連動查驗，彈窗及背景 UI（頂部狀態列、四殿堂卡、出征卡、底部 Dock、戰鬥場景 HUD 與日誌）同步連動同一語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_lobby_zh_TW.png` | 大廳繁中全景（頂欄／四殿堂卡／右側裝備與出征卡／底部5個Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 02 | `proof_02_lobby_en.png` | 大廳英文全景（頂欄／四殿堂卡／右側裝備與出征卡／底部5個Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 03 | `proof_03_creation_en.png` | 創角英文全景（分頁Launch／5張種族卡／職業後綴／外裝與塗裝選項／底部確認按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 04 | `proof_04_wardrobe_en.png` | 衣櫥英文全景（英雄換裝彈窗／種族過濾／外裝卡／底漆卡／底部按鈕／大廳底層背景） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 05 | `proof_05_battle_broken_zh_TW.png` | 戰鬥部位已破繁中全景（Boss部位欄「[已破]」／玩家HUD／提示／日誌／按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 06 | `proof_06_battle_broken_en.png` | 戰鬥部位已破英文全景（英文打雷歐：左右血條與角色名完整可見、頂欄鎖定提示自動換行無溢出） | ✓ 無 | ✓ 零 | ✓ 無裁切 | ✓ 100% 英文 (除玩家存檔名) | 通過 (PASS) |
| 07 | `proof_07_battle_broken_es.png` | 戰鬥部位已破西語全景（西語長譯代表：頂欄左右安全邊距 >= 24px，無超出截斷） | ✓ 無 | ✓ 零 | ✓ 無裁切 | ✓ 100% 西語 (除玩家存檔名) | 通過 (PASS) |

---

## 二、 Vision 視覺顯微審核逐張結論

1. **`proof_01_lobby_zh_TW.png`**：
   - 頂部狀態列（Lv.10 小白、戰力 63、能量 15/15、金幣 1,000、星屑 0、商城、設置）自製圖標完整，無 Emoji，排版工整無截字。
   - 左側四殿堂卡（天宮鐵匠、手藝工坊、演武競技、冒險委託）標題與副標題排版清晰，繁體中文用字規範。
   - 右側裝備欄（外裝、武器、發條、奇玩）與冒險出征卡完整容納於容器內。
   - 底部五個 Dock 按鈕（發條新村、角色裝備、四區出征、聚魂殿堂、冒險背包）居中對齊良好，全畫面無破圖、無系統 Emoji。

2. **`proof_02_lobby_en.png`**：
   - 遵守 0-QA25，大廳背景、頂欄、左右側與底部 Dock 同步切換至英文：
     - 頂部狀態列（Lv.10 Xiaobai / Power 63 / Energy 15/15 / Gold 1,000 / Stardust 0 / Shop / Settings）。
     - 左側四殿堂卡（Celestial Blacksmith / Craft Workshop / Martial Arena / Adventure Bounties）。
     - 右側出征卡（Campaign Sortie · Current Main Story / Region 2 · Lands of White Fog (2-4 BOSS) / Set Out to Battle）。
     - 底部 Dock（Cogwheel Hamlet / Hero Gear / Four Regions / Soul Hall / Adventure Bag）。
   - 英文長度適應良好，零文字截斷、零溢出、零系統 Emoji，100% 英文無中文殘留。

3. **`proof_03_creation_en.png`**：
   - 追蹤確認：`creation-variant-i18n`（commit `1394c049`）合進主線後，上一輪標記之問題已全數修復。
   - 頂部分頁標籤（Launch / Expansion）、5張首發種族卡（Clockwork Rabbit, Astral Fox, Gilded Lion, Forge Boar, Spring Macaque）。
   - 左側角色職業標籤已英文化為 `【Swordsman】`，左側背景介紹文字全數英文化。
   - 右側 Costume 欄位（Nutcracker Guard Uniform 等）與 Chassis Shell 欄位名稱（Factory Ivory White 等）全數英文化。
   - 底部按鈕（Reset Defaults, Confirm Selection · Begin Journey, Back）皆完整英文化且排版正常。全畫面零破圖、零系統 Emoji、無文字裁切、無中文殘留。

4. **`proof_04_wardrobe_en.png`**：
   - 遵守 0-QA25，背後大廳底層（頂欄、左側功能、底部 Dock）同步切換為英文（Lv.10 Xiaobai / Cogwheel Hamlet / Adventure Bag 等）。
   - 衣櫥彈窗大標題（Clockwork Wardrobe · Hero Outfits）、副標題、種族標籤列（Rabbit, Fox, Lion...）、底部按鈕（Reset, Random, Confirm Outfit · Apply New Look）皆完整英文化。
   - 追蹤確認：Outfits 卡片（Nutcracker Guard Uniform, Steam Artisan Overalls 等）與 Paint Finish 卡片（Factory Ivory White, Polished Raw Brass 等）全數英文化，無中文殘留，零系統 Emoji、無破圖。

5. **`proof_05_battle_broken_zh_TW.png`**（特寫：`crops/crop_battle_hud_zh_TW.png`、`crops/crop_part_hud_zh_TW.png`）：
   - 右上角 Boss 部位血條欄中，破損盾牌部位清晰顯示為 `甲·獅衛重盾 [已破]`，血條呈灰色破壞狀態，文字與右側血條保持安全間隔，無重疊或截字。
   - 頂部鎖定提示（`鎖定：獅衛重盔 · Tab 切換 · 破甲降防 / 破冠激怒`）、左側玩家 HUD（`小白`、`HP 50 / 50 · 武 16/16`、粉紅血條、怒氣條）與右側/左側邊界保持標準安全邊距，無貼邊裁切。
   - 下方戰鬥日誌與右下技能按鈕（暫停、逃離、攻擊）繁中顯示工整，全畫面零系統 Emoji、無破圖。

6. **`proof_06_battle_broken_en.png`**（特寫：`crops/crop_battle_hud_en.png`、`crops/crop_part_hud_en.png`）：
   - **驗收核心項目**：英文戰鬥頂欄修復（commit `2d1c4b88`）合進主線後效果確認：
     - **左側玩家 HUD 完整可見**：玩家角色名稱（`小白`）、生命數值標籤（`HP 50 / 50 · Wpn 16/16`）、粉色血條與下方白色 Rage 條完整保留在畫面內，距左側邊界留有充足安全邊距（>= 16px），徹底解決了上一輪被推出螢幕左側不可見與血量遭截斷之破版問題！
     - **中軸提示自適應排版**：`Locked: Knight's heavy helm · Tab: Switch · Break armor: -DEF / Crown: Enrage` 經文案精煉與排版防禦，在中軸區域居中呈現，未向兩側擠壓 `SideBars`。
     - **右側 Boss HUD 與部位欄完整可見**：Boss 名稱（`Titan Overseer Leo`）、血條（`HP 420 / 420`）與部位欄面板本體完整可見，距右側邊界留有充足安全邊距（>= 16px），未被推出螢幕右側！
     - **PartPanel 限寬與省略號保護**：部位欄維持 220px 限寬，子標籤套用 `OVERRUN_TRIM_ELLIPSIS` 截斷保護，確保極限長譯名不會將 HUD 撐破畫面寬度。
     - 下方戰鬥日誌（操作提示、技能說明、對白）與右下按鈕（Pause, Flee, Attack）全數英文化，全畫面零系統 Emoji。

7. **`proof_07_battle_broken_es.png`**（特寫：`crops/crop_battle_hud_es.png`）：
   - 西班牙語長譯代表驗收：
     - 頂部鎖定提示（`Fijado: Yelmo pesado del león guardia · Tab: Cambiar · Romper armadura: -DEF / Corona: Enfurece`）長字串自適應折行居中，未撐破 1280 橫屏。
     - 左側玩家 HUD（`HP 50 / 50 · Arma 16/16`、`Furia`）與右側 Boss HUD（`Titán Guardián Leo`、`HP 420 / 420`）兩端均維持 24~32px 安全留白，無超出截斷。
     - 下方戰鬥日誌與按鈕（Pausa, Huir, Ataque）完整在地化，零系統 Emoji。

---

## 三、 前輪探索性 QA（Round 38）已知問題修復追蹤

| 前輪問題 | 前輪現象 | 本輪追蹤驗證結果 | 狀態 |
|---|---|---|:---:|
| 1. 創角外裝與塗裝未英文化 | 創角右側 Costume / Chassis 仍為中文，職業後綴顯示【劍士】 | `creation-variant-i18n` 合入後，【Swordsman】及各卡片全數英文化 | **已修復 (RESOLVED)** |
| 2. 衣櫥卡片未英文化 | 衣櫥第2/3套外裝與底漆卡片名稱仍為繁中 | `creation-variant-i18n` 合入後，衣櫥卡片全數英文化 | **已修復 (RESOLVED)** |
| 3. 英文戰鬥頂部 HUD 水平溢出破版 | 英文鎖定提示撐破 1280 橫屏，導致玩家名/血條與 Boss 名/血條被擠出螢幕邊緣 | `t_07c57dfd`（commit `2d1c4b88`）合入後，頂部 HUD 兩側安全邊距 >= 16px，左右血條與角色名完整可見無裁切 | **已修復 (RESOLVED)** |

---

## 四、 玩家可見問題清單（依規範「什麼輸入 → 什麼壞掉」，本單不修）

本輪探索性 QA 全量核驗大廳（繁／英）、創角（英）、衣櫥（英）、戰鬥（繁／英／西），**未發現任何影響玩家體驗的畫面破版、文字溢出破圖或系統 Emoji 殘留問題**。

細節優化建議（低優先級，不影響功能）：
1. **玩家名稱多語系預設值**：若全新開局未自訂名稱，英文環境下可考慮讓預設名稱連動翻譯為 `Xiaobai`（目前存檔預設名為字串 `小白`，戰鬥中直接讀取存檔自訂名顯示）。
2. **西語/英文部位面板省略號**：右側部位面板因啟用 220px 限寬保護，極長部位名稱尾端會以省略號 `...` 截斷，此為防止撐破橫屏的刻意設計（Design Trade-off），後續若需展示完整名稱可考慮以點擊浮動提示（Tooltip）補充。

---

## 五、 總體結論

**驗收結論：通過 (PASS)**

1. **英文戰鬥頂欄修復驗收合格**：在 1280x720 標準橫屏下，英文與西語戰鬥之玩家 HUD、Boss HUD、血條與角色名稱完全在螢幕之內且清晰可見，安全邊距達標，中軸提示居中自適應，不再產生水平溢出破版。
2. **大廳、創角、衣櫥連動穩定**：前輪修復之 `creation-variant-i18n` 成果完好保留，各模組在多語系切換下無回歸缺陷、無系統 Emoji、無破圖。
3. **交付符合各項規範**：獨立交付於 `proofs/qa_round39/`（遵守 0-QA23），無 cross-card 污染，未改動 workflows 與 release 發佈檔。
