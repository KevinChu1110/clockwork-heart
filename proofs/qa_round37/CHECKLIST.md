# 探索性 QA 第三十七輪：角色分頁／稱號牆／木人樁結算六語系合主線後驗收清單 (qa-round37)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_a9546caa`（🤖 平台與維運｜探索性 QA：角色分頁／稱號牆／木人樁結算六語系合主線後找破圖）
- **交付目錄**：`proofs/qa_round37/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/qa_round37/`，無覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：英文與繁中語系專有名詞比對語系檔，確認詞條符合設定（如 Xiaobai、Leo、Abo、Veilfog 等）。
  - `review.md 0-QA25`：全畫面連動查驗，彈窗及背景 UI（頂部狀態列、紙娃娃卡、底部 Dock、戰鬥場景日誌）同步連動同一語系，無未翻譯中文殘留。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_char_tab_zh_TW.png` | 大廳角色分頁（繁中全景：武器槽位／說明列／5張屬性小卡／頂欄／Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 02 | `proof_02_char_tab_en.png` | 大廳角色分頁（英文全景：武器槽位／說明列／5張屬性小卡／頂欄／Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 03 | `proof_03_title_wall_zh_TW.png` | 稱號牆（繁中全景：成就·稱號牆標題／計數／成就卡片／未解鎖標籤／返回標題按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 04 | `proof_04_title_wall_en.png` | 稱號牆（英文全景：Achievements·Title Wall／Unlocked 計數／成就卡片／Locked 標籤／Back to the title 按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |
| 05 | `proof_05_dummy_settlement_zh_TW.png` | 木人樁結算卡（繁中全景：木人試招數據卡／三項數值卡／完成試招／背景木人樁戰鬥UI與日誌） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中 | 通過 (PASS) |
| 06 | `proof_06_dummy_settlement_en.png` | 木人樁結算卡（英文全景：Dummy Trial Report／三項數值卡／Finish Trial／背景 Training Dummy 戰鬥UI與日誌） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文 | 通過 (PASS) |

---

## 二、 Vision 視覺顯微審核逐張結論

1. **`proof_01_char_tab_zh_TW.png`**：
   - 角色分頁武器槽（首選武器·鐵劍、副手武器·獵弓、絕技武器·拳套）與三段作戰序列提示列排版工整。
   - 5 張機體戰鬥屬性卡（生命力、物理攻擊、物理防禦、暴擊率、怒氣量表）文字與數值對齊完整，無文字截斷。
   - 頂部狀態列與底部五個 Dock 按鈕（發條新村、角色裝備、四區出征、聚魂殿堂、冒險背包）全數為標準繁體字。
   - 全畫面零系統 Emoji，無破圖。

2. **`proof_02_char_tab_en.png`**：
   - 遵守 0-QA25，彈窗與底層 UI 同步切換至英文：頂部狀態列（Lv.10 Xiaobai / Power / Energy / Gold / Stardust / Shop / Settings）、左側紙娃娃區（Chassis Appearance / Wardrobe）、右側武器輪替區（Weapon Rotation Loadout / Primary / Secondary / Special Weapon）、5 張屬性小卡（Health / Physical ATK / Physical DEF / CRIT Rate / Rage Gauge）、底部 Dock（Cogwheel Hamlet / Hero Gear / Four Regions / Soul Hall / Adventure Bag）。
   - 英文文字排版無溢出截字，零系統 Emoji，全畫面無未翻譯中文殘留。

3. **`proof_03_title_wall_zh_TW.png`**：
   - 標題「成就·稱號牆」、進度「（已解鎖 0/24）」、關閉「✕」按鈕正常。
   - 稱號卡片文字（以劍抵爪、看破者、破架之人、追風的、岸上最後、我不慕強權、晨光中的兔子、裂縫行者）與達成條件、狀態標籤「未解鎖」皆為標準繁體中文。
   - 底部橙黃立體厚底按鈕「返回標題」無截字無溢出，零系統 Emoji，無破圖。

4. **`proof_04_title_wall_en.png`**：
   - 遵守 0-QA24、0-QA25，標題（Achievements · Title Wall）、計數進度（Unlocked 0/24）、卡片稱號與條件說明、狀態標籤（Locked）、底部操作按鈕（Back to the title）全數英文化。
   - 專有名詞（Leo、White Fog、Veilfog、Abo、Shadowwind、Stonefist）皆符合成就既定英文設定，彈窗內 100% 零中文殘留，零系統 Emoji，無破圖。

5. **`proof_05_dummy_settlement_zh_TW.png`**：
   - 中央白底浮空結算卡標題「木人試招數據卡」、三卡「本次總傷害 500」、「試招耗時 12.8 秒」、「秒傷 (DPS) 39.1 點／秒」、按鈕「完成試招」繁中顯示完整。
   - 遵守 0-QA25，背景戰鬥畫面 UI（玩家名稱「小白」、敵手「木人樁」、上方提示列「木人樁不反擊·自由試刀·右上可結束」、下方日誌、右下「結束試招」）同步呈現標準繁體中文，無混雜語系。
   - 數值精確度經計算無誤，零系統 Emoji，無破圖。

6. **`proof_06_dummy_settlement_en.png`**：
   - 中央結算卡標題（Dummy Trial Report）、三卡標籤與單位（Total Damage 500 pts / Trial Duration 12.8s / DPS 39.1 pts/s）、按鈕（Finish Trial）全數英文化。
   - 遵守 0-QA24、0-QA25，背景戰鬥畫面（頂部玩家名稱 Xiaobai、敵手 Training Dummy、提示列、戰鬥日誌、控制按鈕 End Trial / Attack 等）全數切換為英文，無中文殘留。
   - 數值計算精確無誤，零系統 Emoji，無破圖。

---

## 三、 總體結論

**這三塊沒有玩家可見破圖**。合進主線之大廳角色分頁（武器槽與屬性小卡）、稱號牆標題按鈕、木人樁結算卡在繁中與英文實機全景下均版面完整、字級適應良好、零系統 Emoji，背景與彈窗均嚴格遵守 0-QA25 同步連動同一語系，100% 合格。
