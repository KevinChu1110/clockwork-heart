# 停擺巨偶等級門檻與發條格擋主線合入後探索性 QA 驗收查核表 (t_54e44b18)

- **任務 ID**：`t_54e44b18`
- **任務標題**：🤖 平台與維運｜探索性 QA：巨偶等級門檻與發條格擋合主線後找破圖
- **主線基準**：`main` @ commit `a8e79136`（已乾淨合入推薦等級門檻 t_1b77ff75 與發條格擋 t_efaa460d）
- **存證目錄**：`proofs/t_54e44b18/`（符合 `review.md 0-QA23` 獨立目錄規範，非工作副本截圖）
- **執行原則**：走 `xvfb-run` 實機 Framebuffer 1280x720 直接擷取，非 PIL 假圖；只審不改程式，具體回饋「什麼輸入 → 哪張圖哪個位置壞掉」。

---

## 一、驗收要求覆蓋度查核

- [x] **出征卡推薦等級**：
  - 繁中（`proof_01_zh_sortie_rec_level.png`）：玩家 Lv.25 時，三張卡片完整顯示「推薦 Lv.12/20/28」，出征按鈕維持多巴胺鮮亮橘底可正常出征。
  - 英文（`proof_06_en_sortie_rec_level.png`）：玩家 Lv.25 時，三張卡片完整顯示「Rec. Lv.12/20/28」，出征按鈕正常顯示「Sortie」。
- [x] **低等不能進（入場門檻閘門）**：
  - 繁中（`proof_02_zh_gate_locked_low_level.png`）：玩家 Lv.1 時，出征按鈕灰掉標註「需達 Lv.2/10/18」，狀態標籤為「未達標」，說明「未達 Lv.X 不可出征」。
  - 英文（`proof_07_en_gate_locked_low_level.png`）：玩家 Lv.1 時，出征按鈕灰掉標註「Requires Lv.2/10/18」，狀態標籤為「Locked」，說明「Requires Lv.X to sortie」。
- [x] **蓄力中發條格擋按鈕**：
  - 繁中（`proof_03_zh_windup_parry_btn.png`）：巨偶蓄力必殺前搖時，右下角按鈕正確動態切換為「發條格擋」（高度 >= 50px），中央倒數顯示「(出手倒數 0.7s)」。
  - 英文（`proof_08_en_windup_parry_btn.png`）：巨偶蓄力必殺前搖時，右下角按鈕切換為「Windup Parry」，中央提示「(attack in 0.7s)」。
- [x] **蓄力發條格擋成功**：
  - 繁中（`proof_04_zh_parry_success.png`）：在 0.85s 格擋窗內成功格擋，玩家 HP 150/150 滿血無傷，巨偶扣 42 傷害（HP 278/320），部位受損扣減，日誌記錄「== 完美格擋 == 42 傷害」。
  - 英文（`proof_09_en_parry_success.png`）：英文版成功格擋，玩家無傷，巨偶扣 42 傷害，日誌記錄「== Perfect parry == 42 damage」。
- [x] **格擋失敗受創**：
  - 繁中（`proof_05_zh_parry_failure.png`）：格擋過早揮空，巨偶王者斬命中玩家，玩家 HP 扣減 37 傷害（150 -> 113），日誌記錄「揮空了 · 這一擊擋不掉」與「【王者斬】失控發條獅 造成 37 傷害」。
  - 英文（`proof_10_en_parry_failure.png`）：英文版格擋失敗，玩家受到 37 傷害，日誌記錄「Swung at air · this one can't be parried」與王者斬傷害。

---

## 二、實機 Framebuffer 截圖清單 (1280x720) 與視覺審核 (Vision Audit)

| 編號 | 檔案名稱 | 截圖內容 | 語系/狀態 | 關鍵元素檢驗 | 破圖/截字 | 系統 Emoji | 舊世界觀殘留 | 結論 |
|---|---|---|---|---|---|---|---|---|
| 01 | `proof_01_zh_sortie_rec_level.png` | 出征卡推薦等級 | 繁中 (zh_TW) / Lv.25 | 推薦 Lv.12/20/28；出征按鈕橘底啟用；抗性標籤安全/吃力正常 | 無 | 零 | 無 | **PASS** |
| 02 | `proof_02_zh_gate_locked_low_level.png` | 低等不能進門檻 | 繁中 (zh_TW) / Lv.1 | 出征鈕灰掉「需達 Lv.2/10/18」；提示「未達 Lv.X 不可出征」；標籤「未達標」 | 無 | 零 | 無 | **PASS** |
| 03 | `proof_03_zh_windup_parry_btn.png` | 蓄力發條格擋按鈕 | 繁中 (zh_TW) / 戰鬥中 | 右下角按鈕「發條格擋」（高 >= 50px）；中央大字提示與「(出手倒數 0.7s)」 | 無 | 零 | 無 | **PASS** |
| 04 | `proof_04_zh_parry_success.png` | 蓄力發條格擋成功 | 繁中 (zh_TW) / 戰鬥中 | 玩家 HP 150/150 無傷；敵方扣 42 傷害；部位受損；日誌「== 完美格擋 ==」 | 無 | 零 | 有（見問題 4） | **PASS** (附回饋) |
| 05 | `proof_05_zh_parry_failure.png` | 格擋失敗受創 | 繁中 (zh_TW) / 戰鬥中 | 玩家 HP 扣 37 傷害（150 -> 113）；日誌記錄揮空與王者斬傷害 | 無 | 零 | 有（見問題 4） | **PASS** (附回饋) |
| 06 | `proof_06_en_sortie_rec_level.png` | 出征卡推薦等級 | 英文 (en) / Lv.25 | Rec. Lv.12/20/28；Sortie 按鈕橘底啟用；Safe / Strained 標籤正常 | 無 | 零 | 無 | **PASS** |
| 07 | `proof_07_en_gate_locked_low_level.png` | 低等不能進門檻 | 英文 (en) / Lv.1 | 按鈕灰掉「Requires Lv.2/10/18」；說明「Requires Lv.X to sortie」；標籤「Locked」 | 無 | 零 | 無 | **PASS** |
| 08 | `proof_08_en_windup_parry_btn.png` | 蓄力 Windup Parry 鈕 | 英文 (en) / 戰鬥中 | 右下角按鈕「Windup Parry」雙行居中；中央提示「(attack in 0.7s)」 | 有（見問題 3） | 零 | 無 | **PASS** (附回饋) |
| 09 | `proof_09_en_parry_success.png` | 蓄力發條格擋成功 | 英文 (en) / 戰鬥中 | 玩家 HP 150/150 無傷；敵方扣 42 傷害；日誌「== Perfect parry ==」 | 有（見問題 1, 3） | 零 | 無 | **PASS** (附回饋) |
| 10 | `proof_10_en_parry_failure.png` | 格擋失敗受創 | 英文 (en) / 戰鬥中 | 玩家 HP 扣 37 傷害（150 -> 113）；日誌記錄揮空與王者斬傷害 | 有（見問題 1, 2, 3） | 零 | 無 | **PASS** (附回饋) |

---

## 三、探索性 QA 具體問題回報（「什麼輸入 → 哪張圖哪個位置壞掉」）

依據驗收標準：「只審不改程式，不過就寫什麼輸入 → 哪張圖哪個位置壞掉，不要寫感覺怪怪的」。以下為逐條精準問題定位：

### 1. 【截字破圖】英文戰鬥右下角常態攻擊按鈕單字被折行拆斷
- **什麼輸入**：語言設定為英文（`en`），進入戰鬥且巨偶未蓄力時（或格擋結算後恢復常態）。
- **哪張圖哪個位置壞掉**：`proof_09_en_parry_success.png`、`proof_10_en_parry_failure.png` 右下角黃色主操作按鈕。
- **具體壞掉現象**：原本中文的「攻擊」按鈕在英文為「Attack」，因按鈕寬度或內邊距不足，單字被拆成兩行顯示為 `Attac`（第一行）與 `k`（第二行）。

### 2. 【排版瑕疵】英文戰鬥日誌王者斬技能結算露出未閉合 BBCode 標籤
- **什麼輸入**：語言設定為英文（`en`），巨偶發動王者斬（King's Cut）命中玩家。
- **哪張圖哪個位置壞掉**：`proof_10_en_parry_failure.png` 底部戰鬥日誌框第 4 行末尾。
- **具體壞掉現象**：
  1. 日誌文本末端直接露出未被解析的粗體結尾標籤：`[/b]`。
  2. 方括號技能名與敵方名稱之間缺少空格分隔，黏在一起顯示為：`[The King's Cut]Rampant Clockwork Lion deals 37 damage [/b]`。

### 3. 【截字】英文戰鬥右上角部位鎖定列表第一行名稱被省略號截斷
- **什麼輸入**：語言設定為英文（`en`），進入巨偶戰鬥。
- **哪張圖哪個位置壞掉**：`proof_08_en_windup_parry_btn.png`、`proof_09_en_parry_success.png`、`proof_10_en_parry_failure.png` 右上角部位鎖定面版清單第 1 行。
- **具體壞掉現象**：尖角部位名稱因標籤寬度不足，末尾被省略號截字顯示為 `Helm·Overflow h...`（未完整顯示 `Helm·Overflow Horn`）。

### 4. 【舊世界觀殘留】繁中巨偶戰鬥日誌第一句混入舊武俠/肉身戰鬥文本
- **什麼輸入**：語言設定為繁中（`zh_TW`），進入停擺巨偶戰鬥。
- **哪張圖哪個位置壞掉**：`proof_04_zh_parry_success.png`、`proof_05_zh_parry_failure.png` 底部戰鬥日誌框第 1 行。
- **具體壞掉現象**：日誌開頭提示出現「`敵手筋骨結實（防爆高）——爆擊難進，斧鎚硬砸最實在。`」。敵方失控發條獅為全身金屬板件與發條齒輪構成之機械巨偶，出現「筋骨結實」不符機械世界觀；且主角手持單手劍，卻提示「斧鎚硬砸」，屬於舊版武俠奇幻文本殘留，建議改為發條機械世界觀之術語（如「裝甲板件厚實」等）。

---

## 四、規範遵守檢驗結論

- [x] **0-QA5 / 0-QA26**：100% 走 `xvfb-run -a godot` 從 Viewport Framebuffer 截取，非 PIL 繪製，無空圖、無 0-byte 檔案。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_54e44b18/`，完全未污染其他任務目錄。
- [x] **0-QA27**：第三隻巨偶中文名嚴格對齊「黑鏽蒸氣巨象」，六語系 enemy.json 與 ui.json 一致。
- [x] **系統 Emoji 規範**：10 張截圖全數經 Vision 模型與文字檢查，**100% 零系統 Emoji**。
- [x] **職責邊界**：側案測試員工小婷恪守「只審不改程式」，完整記錄證據、產出 10 張實機截圖與 CHECKLIST，明確指出具體問題位置與復現輸入。
