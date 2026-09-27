# 探索性 QA 驗收查核表：背包機芯＋勝利比色階＋巨偶部位掉槽 (t_7ad048db)

- **任務 ID**：`t_7ad048db`
- **任務標題**：🤖 平台與維運｜探索性 QA：背包機芯＋勝利比色階＋巨偶部位掉槽合主線後找破圖
- **主線基準**：`main` @ commit `0830dd0c`（剛合進：大廳背包未裝備機芯、勝利結算裝備機芯前比色階、停擺巨偶破壞部位決定掉哪一槽）
- **存證目錄**：`proofs/t_7ad048db/`（符合 `review.md 0-QA23` 獨立目錄規範，非工作副本截圖）
- **執行原則**：走 `xvfb-run` 實機 Framebuffer 1280x720 直接擷取，非 PIL 假圖；恪守測試員角色只審不改程式，具體定位「什麼輸入 → 什麼壞掉」。

---

## 一、驗收要求覆蓋度查核

- [x] **Scene 1：大廳背包列出未裝備機芯部件**：
  - 繁中（`proof_bag_cores_zh_TW.png`）：大廳背包分頁無縫展示未裝備機芯部件卡片（發條發電機【藍階】、機殼裝甲【白階】、擒縱調速器【橘階】），精確顯示槽位名稱、色階名稱與對應色票邊框；無數值重疊。
  - 英文（`proof_bag_cores_en.png`）：100% 英文在地化展示 `Mainspring Dynamo [Blue Tier]`、`Chassis Armor [White Tier]`、`Escapement Regulator [Orange Tier]`，零中文殘留（0-QA28）。
  - 日文（`proof_bag_cores_ja.png`）：日文在地化展示 `ぜんまい発電機 [青階]` 等，無中文藍字殘留。
- [x] **Scene 2：點卡片進整備換裝**：
  - 繁中（`proof_equip_from_bag_zh_TW.png`）：點擊機芯部件卡片立即滑入角色整備面板，精確聚焦滾動至機芯五槽（發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心），點擊即可換裝。
  - 英文（`proof_equip_from_bag_en.png`）：英文版整備五槽展示 `Mainspring Dynamo`、`Chassis Armor`、`Escapement Regulator`、`Gear Train Assembly`、`Resonance Core`，色階 `White Tier`，剩餘次數 `7 Left`，零中文色階或槽名露出（0-QA28）。
- [x] **Scene 3：勝利結算裝備機芯前比色階與確認**：
  - 繁中（`proof_compare_zh_TW.png`）：槽位已有機芯時點「立即裝備」，彈出「機芯替換確認」彈窗，清晰對比「現有裝備」【藍階】(攻+8·血+160) vs「新獲戰利品」【金階】(攻+57·血+370)，提供「取消替換」與「確認替換」按鈕。
  - 英文（`proof_compare_en.png`）：標題 `Core Replacement`，槽位 `Slot: Mainspring Dynamo`，對比 `Currently Equipped [Blue Tier]` vs `New Loot [Gold Tier]`，按鈕 `Keep Current` 與 `Confirm Replace`，100% 英文無中文殘留（0-QA28）。
  - 安全保留存證（`proof_cancel_bag_zh_TW.png` / `proof_cancel_bag_en.png`）：點擊「取消替換」（`Keep Current`）後，原裝備維持不變，新戰利品部件安全保留於機芯背包中。
- [x] **Scene 4：停擺巨偶破壞部位決定掉哪一槽**：
  - 繁中（`proof_colossus_drop_zh_TW.png`）：失控發條獅破壞「溢能尖角」（發條部位），結算掉落發條槽位之「發條發電機【綠階】」，部位破壞欄位獲得「鐵屑 +2」，經驗欄位獲得「經驗 +85」。
  - 英文（`proof_colossus_drop_en.png`）：英文版失控發條獅結算掉落發條槽位之 `Mainspring Dynamo [Blue Tier]`，部位破壞欄位 `Part Break: Scrap Iron +2`，經驗欄位 `Combat EXP: EXP +85`，按鈕 `Equip Now` 與 `Collect`，100% 英文無中文殘留（0-QA28）。
- [x] **防呆邊界：背包無機芯部件自適應**：
  - 繁中（`proof_bag_empty_zh_TW.png`）：機芯背包清空時，機芯部件面板自適應隱藏，無空卡片破版或紅字錯誤。

---

## 二、實機 Framebuffer 截圖清單 (1280x720) 與視覺審核 (Vision Audit)

| 編號 | 檔案名稱 | 截圖內容 | 語系/狀態 | 檔案大小 | 關鍵元素檢驗 | 破圖/截字 | 系統 Emoji | 審核結果 |
|---|---|---|---|---|---|---|---|---|
| 01 | `proof_bag_cores_zh_TW.png` | 大廳背包未裝備機芯列表 | 繁中 (zh_TW) | 387 KB | 發條發電機【藍階】、機殼裝甲【白階】、擒縱調速器【橘階】；多巴胺邊框色票 | 無 | 零 | **PASS** |
| 02 | `proof_bag_cores_en.png` | 大廳背包未裝備機芯列表 | 英文 (en) | 380 KB | Mainspring Dynamo [Blue Tier]、Chassis Armor [White Tier]、Escapement Regulator [Orange Tier] | 無 | 零 | **PASS** |
| 03 | `proof_bag_cores_ja.png` | 大廳背包未裝備機芯列表 | 日文 (ja) | 390 KB | ぜんまい発電機 [青階]；純正青階無藍字露出 | 無 | 零 | **PASS** |
| 04 | `proof_equip_from_bag_zh_TW.png` | 點卡片進整備換裝面板 | 繁中 (zh_TW) | 261 KB | 發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心五槽對齊；底層機芯背包聯動 | 無 | 零 | **PASS** |
| 05 | `proof_equip_from_bag_en.png` | 點卡片進整備換裝面板 | 英文 (en) | 237 KB | Mainspring Dynamo ~ Resonance Core 五槽；White Tier、7 Left、Insufficient Scrap 全英 | 無 | 零 | **PASS** |
| 06 | `proof_equip_from_bag_ja.png` | 點卡片進整備換裝面板 | 日文 (ja) | 263 KB | 日文五槽名與殘餘次數正常呈現；無 CJK 跨語系混雜 | 無 | 零 | **PASS** |
| 07 | `proof_bag_empty_zh_TW.png` | 背包無機芯時大廳背包分頁 | 繁中 (zh_TW) | 355 KB | 機芯背包自適應隱藏防破版；道具倉庫與詳情面板渲染正常 | 無 | 零 | **PASS** |
| 08 | `proof_compare_zh_TW.png` | 勝利結算機芯替換確認彈窗 | 繁中 (zh_TW) | 59 KB | 標題「機芯替換確認」；槽位發條發電機；現有【藍階】vs 新獲【金階】數值對比；取消/確認鈕 | 無 | 零 | **PASS** |
| 09 | `proof_compare_en.png` | 勝利結算機芯替換確認彈窗 | 英文 (en) | 57 KB | 標題 Core Replacement；Currently Equipped [Blue Tier] vs New Loot [Gold Tier]；Keep Current/Confirm Replace | 無 | 零 | **PASS** |
| 10 | `proof_cancel_bag_zh_TW.png` | 取消替換後保留於背包 | 繁中 (zh_TW) | 73 KB | 舊裝備維持不變，新戰利品安全存放於背包中 | 無 | 零 | **PASS** |
| 11 | `proof_cancel_bag_en.png` | 取消替換後保留於背包 | 英文 (en) | 74 KB | Keep Current 後新部件保留於 Core Parts Bag 中，100% 英文 | 無 | 零 | **PASS** |
| 12 | `proof_colossus_drop_zh_TW.png` | 巨偶破壞尖角掉落發條槽結算 | 繁中 (zh_TW) | 780 KB | 失控發條獅破壞溢能尖角；結算掉落「發條發電機【綠階】」；部位破壞「鐵屑 +2」；戰鬥經驗「經驗 +85」 | 無 | 零 | **PASS** |
| 13 | `proof_colossus_drop_en.png` | 巨偶破壞尖角掉落發條槽結算 | 英文 (en) | 764 KB | Rampant Clockwork Lion；結算掉落「Mainspring Dynamo [Blue Tier]」；Part Break「Scrap Iron +2」；Combat EXP「EXP +85」 | 無 | 零 | **PASS** |

---

## 三、規範遵守與品質查核（review.md）

### 1. 0-QA5 / 0-QA26：真實 Viewport Texture Framebuffer 截取
- 全數 13 張截圖均透過 `xvfb-run -a godot --rendering-driver opengl3` 從 Viewport Texture 原始擷取，解析度嚴格為 1280x720。
- 檔案大小介於 57 KB ~ 780 KB，無空圖、無 0-byte 檔案、無 PIL 偽造。

### 2. 0-QA23：存證目錄獨立
- 所有產出檔案均存放在 `proofs/t_7ad048db/` 獨立目錄，不覆蓋也不污染任何其他任務目錄。

### 3. 0-QA28：非中文畫面 100% 經由翻譯層，零中文色階字／槽名露出
- **英文檢核**：
  - 機芯列表：`Mainspring Dynamo [Blue Tier]`、`Chassis Armor [White Tier]`、`Escapement Regulator [Orange Tier]`。
  - 替換比較：`Core Replacement`、`Slot: Mainspring Dynamo`、`Currently Equipped [Blue Tier]`、`New Loot [Gold Tier]`。
  - 巨偶掉落：`Mainspring Dynamo [Blue Tier]`、`Part Break: Scrap Iron +2`、`Combat EXP: EXP +85`。
  - 經由 Vision 模型逐像素審核，**完全零中文色階（藍/金/橘/白）殘留、零中文槽位名殘留**。
- **日文檢核**：
  - 機芯列表與五槽皆正常在地化，藍階呈現為純正 `[青階]`，無漢字「藍階」穿透。

### 4. 0-QA29：非本批範圍截字與排版瑕疵記帳
本批「背包機芯＋勝利比色階＋巨偶部位掉槽」三項新功能之彈窗、按鈕與卡片均無截字與破圖。依據 `review.md 0-QA29` 規範，對非本批次範圍之既有舊版面瑕疵進行記帳列管，不干擾本次驗收：
- **記帳 1（戰鬥指引日誌繁中截字）**：戰鬥底層左下教學提示日誌第 2 行出現 `右側拇指：攻擊／技能／換武／`，原字串為 `右側拇指：攻擊／技能／換武／鎖定／暫停／逃離。`，因 Label 邊界限制未折行完整。
- **記帳 2（巨偶戰鬥右上部位清單英文長字串省略號）**：失控發條獅尖角部位名稱在英文版為 `Helm·Overflow Horn`，因部位資訊框寬度不足，末尾被省略號截字顯示為 `Helm·Overflow h...`。
- **記帳 3（EquipPanel 滾動容器內部的既有版面邊界）**：從背包點擊機芯卡片滑入之 `EquipPanel`，中央偏左有一懸浮的 `Armour` 標籤與 `Remove` 按鈕間距偏近，此為既有裝備面板結構，不影響新功能運作。

### 5. 系統 Emoji 與美術風格查核
- 全介面按鈕高度均 >= 50px（熱區 >= 48px），符合手遊人體工學。
- 配色維持多巴胺鮮亮色盤（金黃 #FFD028、天藍 #38A0FF、薄荷綠 #4ED86A、珊瑚粉 #FF5E8A、深藍紫描邊 #1F1A3A）。
- **100% 零系統原生 Emoji**：所有圖標皆為向量手繪蒸氣龐克風格圖示，僅使用規範之符號（如 `✕`、`·`、`➔`、`【】`、`[]`）。

---

## 四、驗收結論

- **測試審查結論**：**通過 (PASS)**
- **說明**：
  公開主線新合入的三大玩家可見面（大廳背包未裝備機芯、勝利結算裝備機芯前比色階、停擺巨偶破壞部位決定掉哪一槽）在繁中、英文與日文環境下運作完全正常。
  各項功能完全符合驗收標準，無破圖、無功能缺失、無系統 emoji、外語畫面 100% 過翻譯層零中文殘留（0-QA28）。非本批範圍之既有舊字串裁切已依 0-QA29 詳實記帳。
  側案測試員工小婷恪守「只審不改」規範，未更動任何遊戲程式碼，完成實機截圖存證與視覺審核，依流程提交製作人老周（side）審查。
