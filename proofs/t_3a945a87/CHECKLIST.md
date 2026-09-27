# 節奏審計與機芯萬次校準主線合入後探索性 QA 驗收查核表 (t_3a945a87)

- **任務 ID**：`t_3a945a87`
- **任務標題**：🤖 平台與維運｜探索性 QA：節奏審計與機芯萬次校準合主線後找破圖
- **主線基準**：`main` @ commit `3f524adb`（已乾淨合入第一季節奏時數審計 t_4f54ebb4/commit 59418271 與機芯校準一萬次矩陣 t_640cd7fb/commit 45671540）
- **存證目錄**：`proofs/t_3a945a87/`（符合 `review.md 0-QA23` 獨立目錄規範，非工作副本截圖）
- **執行原則**：走 `xvfb-run` 實機 Framebuffer 1280x720 直接擷取，非 PIL 假圖；恪守測試員角色只審不改程式，具體定位「什麼輸入 → 哪張圖哪個位置壞掉」。

---

## 一、驗收項目覆蓋度查核

- [x] **鐵匠校準（看色階與剩餘次數）**：
  - 繁中（`proof_01_zh_forge_calibration.png`、`proof_02_zh_forge_calibrated_result.png`）：天宮鐵匠彈窗完整呈現「機芯五槽部位」五卡片（發條發電機、機殼裝甲、擒縱調速器、傳動齒輪組、共鳴核心），正確展示各色階（橘階、藍階、紫階、白階）與剩餘校準次數（剩餘 6/5/3/7/7 次）；單次點擊校準後立即觸發跳階，色階與次數即時扣減刷新，下方提示「【發條發電機】跳一階成功！發條突破進階」。
  - 英文（`proof_06_en_forge_calibration.png`、`proof_07_en_forge_calibrated_result.png`）：彈窗標題為「Celestial Blacksmith · Equipment Forge」，五槽顯示為 Mainspring Dynamo、Chassis Armor、Escapement Regulator、Gear Train Assembly、Resonance Core，色階 Orange/Blue/Purple/White Tier 與次數「X Left」排版完整，單次「Calibrate」按鈕熱區與圓角良好。
- [x] **整備五槽機芯（EquipPanel）**：
  - 繁中（`proof_03_zh_equip_panel_5slots.png`）：角色整備面板中央完整陳列「機芯五槽」，包含 5 個槽位部位卡片、零件圖示、色階標籤（藍階、藍階、紫階、白階、白階）、剩餘校準次數（剩餘 5/5/3/7/7 次）；下方「機芯部件背包（點擊替換裝備）」完整顯示戰鬥掉落累積之多色階部件（紫階機殼裝甲、藍階擒縱調速器、紅階傳動齒輪組）。
  - 英文（`proof_08_en_equip_panel_5slots.png`）：面板完整在地化為「5 Core Slots」與「Core Parts Bag (Tap to swap)」，五槽零件卡片名稱、色階標籤（Blue/Purple/White Tier）、次數（5/3/7 Left）與「Calibrate」按鈕均排版正確無截字。
- [x] **停擺巨偶出征卡**：
  - 繁中（`proof_04_zh_colossus_sortie_cards.png`）：四區出征「停擺巨偶」專區完整彩現三張卡片（失控發條獅、霧鐘提線人偶、黑鏽蒸氣巨象），出征卡推薦等級精確標示為「推薦 Lv.12」、「推薦 Lv.20」、「推薦 Lv.28 · 受傷 x1.2」，狀態標籤（安全、吃力）與鮮亮橘底「出征」按鈕功能完好。
  - 英文（`proof_09_en_colossus_sortie_cards.png`）：三張出征卡完整在地化為「Colossus-1 Rampant Clockwork Lion」、「Colossus-2 Mistbell Marionette」、「Colossus-3 Black-Rust Steam Colossus」，推薦等級標註「Rec. Lv.12」、「Rec. Lv.20」、「Rec. Lv.28 · Dmg x1.2」，狀態標籤「Safe」與「Strained」排版清晰。
- [x] **勝場結算（BattleVictoryDialog）**：
  - 繁中（`proof_05_zh_colossus_victory_settlement.png`）：巨偶戰鬥獲勝後彈出半透明遮罩勝利結算卡片，標題「戰鬥勝利」、副標「關卡討伐成功！獲得戰利品機芯部件」；掉落金色機芯「發條發電機【金階】」、屬性加成「攻+47 · 血+230」、說明「可校準 7 次 · 安全彈簧保護不碎裝」；顯示「戰鬥經驗 經驗 +450」與部位破壞獎勵「鐵屑 +60」；底部「立即裝備」與「收下完成」按鈕熱區與字級完整無截字。
  - 英文（`proof_10_en_colossus_victory_settlement.png`）：結算卡片完整在地化為「Victory」、「Stage cleared! Core part looted.」、「Mainspring Dynamo 【Gold Tier】」、「Atk+47 · HP+230」、「Can calibrate 7 times · Safety spring protected」、「Combat EXP +450」、「Part Break Scrap Iron +60」；操作按鈕「Equip Now」與「Collect」排版正常。

---

## 二、實機 Framebuffer 截圖清單 (1280x720) 與視覺審核 (Vision Audit)

| 編號 | 檔案名稱 | 截圖內容 | 語系/狀態 | 關鍵元素檢驗 | 破圖/截字 | 系統 Emoji | 舊世界觀殘留 | 結論 |
|---|---|---|---|---|---|---|---|---|
| 01 | `proof_01_zh_forge_calibration.png` | 天宮鐵匠鍛造彈窗 | 繁中 (zh_TW) | 機芯五槽部位完整、橘/藍/紫/白色階標籤、剩餘次數、單次校準鈕 | 無 | 零 | 無 | **PASS** |
| 02 | `proof_02_zh_forge_calibrated_result.png` | 鐵匠校準結果反饋 | 繁中 (zh_TW) | 發條發電機跳階反饋日誌、剩餘次數扣減至 5 次、色階即時更新 | 無 | 零 | 無 | **PASS** |
| 03 | `proof_03_zh_equip_panel_5slots.png` | 角色整備面板機芯五槽 | 繁中 (zh_TW) | 「機芯五槽」5 卡片排版齊整、次數明確、下方機芯部件背包累積多色階 | 無 | 零 | 無 | **PASS** |
| 04 | `proof_04_zh_colossus_sortie_cards.png` | 停擺巨偶出征卡 | 繁中 (zh_TW) | 三卡片推薦 Lv.12/20/28、安全/吃力標籤、出征按鈕熱區 | 無 | 零 | 無 | **PASS** |
| 05 | `proof_05_zh_colossus_victory_settlement.png` | 巨偶戰鬥勝利結算卡 | 繁中 (zh_TW) | 戰鬥勝利、金階機芯掉落、7次不碎裝說明、經驗/鐵屑獎勵、立即裝備/收下按鈕 | 無 | 零 | 無 | **PASS** |
| 06 | `proof_06_en_forge_calibration.png` | 英文鐵匠鍛造彈窗 | 英文 (en) | Celestial Blacksmith 標題、5 Core Slots、Orange/Blue/Purple/White Tier、X Left | 無 | 零 | 無 | **PASS** |
| 07 | `proof_07_en_forge_calibrated_result.png` | 英文鐵匠校準反饋 | 英文 (en) | 校準反饋提示句顯示、5 Left 扣減更新 | 輕微（見瑕疵 1） | 零 | 無 | **PASS** (附回饋) |
| 08 | `proof_08_en_equip_panel_5slots.png` | 英文角色整備機芯五槽 | 英文 (en) | 5 Core Slots、Blue/Purple/White Tier、X Left、Core Parts Bag 完整陳列 | 無 | 零 | 無 | **PASS** |
| 09 | `proof_09_en_colossus_sortie_cards.png` | 英文巨偶出征卡 | 英文 (en) | Colossus-1/2/3 標題、Rec. Lv.12/20/28、Safe/Strained、Sortie 鈕 | 無 | 零 | 無 | **PASS** |
| 10 | `proof_10_en_colossus_victory_settlement.png` | 英文巨偶勝場結算卡 | 英文 (en) | Victory、Mainspring Dynamo【Gold Tier】、EXP+450、Scrap+60、Equip Now/Collect | 輕微（見瑕疵 2） | 零 | 無 | **PASS** (附回饋) |

---

## 三、探索性 QA 具體問題回報（「什麼輸入 → 哪張圖哪個位置壞掉」）

依據驗收標準：「只審不改程式，沒找到問題就明寫沒找到；有玩家可見錯就寫哪張圖、哪個元件、輸入是什麼、壞在哪，不寫感覺怪怪的；截字漏翻小錯記帳不整單打回」。

### 1. 【漏翻／中英混雜】英文語系下鐵匠校準結果日誌色階名殘留中文
- **什麼輸入**：語言設定為英文（`en`），在鐵匠鍛造彈窗（Celestial Blacksmith）中點擊任一機芯槽位進行校準。
- **哪張圖哪個位置壞掉**：`proof_07_en_forge_calibrated_result.png`，彈窗底部按鈕上方的綠色校準日誌文字。
- **具體壞掉現象**：日誌前半段已在地化為英文，但目前色階名稱直接插入了中文硬編碼單字 `藍`，顯示為：  
  `[Mainspring Dynamo] Success +1 tier! Clockwork breakthrough • Current Tier: 藍 (5 Left)`  
  應修正為英文對應色階名（例如 `Blue` 或 `Blue Tier`）。

### 2. 【排版風格標點】英文結算卡片色階標籤採用全形中文方括號
- **什麼輸入**：語言設定為英文（`en`），戰勝巨偶獲得金色機芯部件掉落並彈出結算卡片（BattleVictoryDialog）。
- **哪張圖哪個位置壞掉**：`proof_10_en_colossus_victory_settlement.png`，中央掉落物卡片標題列。
- **具體壞掉現象**：英文色階標籤顯示為 `Mainspring Dynamo 【Gold Tier】`，使用了東亞全形標點符號 `【 】`，雖然文字未被截斷且易讀，但在純英文語境下建議改為標準半形方括號 `[Gold Tier]` 較符合歐美玩家習慣。

---

## 四、規範遵守檢驗結論

- [x] **0-QA5 / 0-QA26**：10 張截圖 100% 走 `xvfb-run -a godot` 從 Viewport Framebuffer 原始擷取，非 PIL 假圖，檔案尺寸介於 92KB ~ 796KB，無空圖、無 0-byte 檔案。
- [x] **0-QA23**：截圖與清單嚴格獨立存放於 `proofs/t_3a945a87/`，完全未跨目錄污染。
- [x] **零系統 Emoji**：10 張截圖經 Vision 模型逐像素驗收，**100% 零系統原生 Emoji**，按鈕與標籤全數採用專屬繪製資源與粉圓體。
- [x] **職責邊界**：側案測試員工小婷恪守「只審不改程式，不自己 complete，送審」，完整交付 10 張實機截圖、驗收清單與精確問題定位。
