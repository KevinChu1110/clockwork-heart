# 驗收證明 · 探索性 QA：巨偶部位鐵屑與校準跳階合主線 (t_ec3692e3)

## 依據規範
- `review.md 0-QA5 / 0-QA26`：Godot ViewportTexture framebuffer 直接擷取，嚴禁 PIL／手繪假圖。
- `review.md 0-QA23`：OUT_DIR 獨立目錄，存證至 `proofs/t_ec3692e3/`，不覆蓋其他任務目錄。
- `review.md 0-QA25`：全畫面多語系動態即時連動刷新，背景與彈窗語系一致。
- `review.md 0-QA27`：巨偶中文名對齊世界觀設計文件「黑鏽蒸氣巨象」，六語系 `enemy.json` 與 `ui.json` 同 id 譯名 100% 逐一相等。
- 零系統 Emoji、多巴胺鮮亮高飽和色盤。
- 舊功能未損壞（大廳主城、四區出征、角色衣櫥、冒險背包）。

## 實機截圖清單
| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 截字溢出 | 驗證結論 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_forge_calibrate_result.png` | 鐵匠校準結果：發條發電機跳階成功、突破進階結果句、金屬色階橘階、剩餘次數正確遞減、失敗不碎裝 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 02 | `proof_02_colossus_victory_scrap.png` | 停擺巨偶勝場結算：ScrapRewardPanel 清楚展示「部位破壞」「鐵屑 +2」、勝場掉落機芯與經驗值 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 03 | `proof_03_lobby_zh_tw.png` | 大廳主畫面繁中：浮空島天空王國、主角小白、頂部 HUD 能量與貨幣、底部 Dock 一級入口 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 04 | `proof_04_colossus_sortie_zh_tw.png` | 出征分頁停擺巨偶模式繁中：入口按鈕、剩餘 3/3 次數、三張巨偶卡（失控發條獅 Lv12、霧鐘提線人偶 Lv20、黑鏽蒸氣巨象 Lv28） | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 05 | `proof_05_lobby_en.png` | 英文語系大廳全景：檢查英文排版、HUD 數值、Dock 按鈕英文化與版面邊距 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 06 | `proof_06_colossus_sortie_ja.png` | 日文語系出征巨偶模式：停止した巨偶、暴走のぜんまい獅子、霧鐘の操り人形、黒錆の蒸気巨象、日文版面無溢出 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 07 | `proof_07_wardrobe_zh_tw.png` | 衣櫥換裝舊功能：發條衣櫥彈窗、紙娃娃預覽、套裝卡片清單、保存與關閉按鈕 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |
| 08 | `proof_08_bag_iron_scrap_zh_tw.png` | 冒險背包舊功能：背包格子道具清單、既有道具 iron_scrap (鐵屑) 數量與說明完好展示 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 無截字 | **通過 (PASS)** |

## 關鍵檢核點落實說明

### 1. 0-QA5 / 0-QA26（真遊戲畫面截圖）
全數截圖均由 Godot 引擎無頭執行時直接抓取 root ViewportTexture Framebuffer，無使用 PIL、無手繪假圖，保證 100% 呈現手遊真機運行畫面。

### 2. 0-QA23（獨立存證目錄）
截圖與清單全部輸出至 `proofs/t_ec3692e3/`，無污染、無覆蓋其他卡片之存證目錄。

### 3. 0-QA27（巨偶中文名對齊與六語系一致性）
- 依據專案核心黑鏽世界觀與 Commit `631515b9`，第三隻巨偶中文名為「黑鏽蒸氣巨象」（`colossus_elephant`）。
- 執行 `tools/verify_colossus_i18n_equality.py` 嚴格驗證六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）：
  - `zh_TW`: enemy='黑鏽蒸氣巨象' == ui['黑鏽蒸氣巨象']='黑鏽蒸氣巨象'
  - `zh_CN`: enemy='黑锈蒸气巨象' == ui['黑鏽蒸氣巨象']='黑锈蒸气巨象'
  - `en`: enemy='Black-Rust Steam Colossus' == ui['黑鏽蒸氣巨象']='Black-Rust Steam Colossus'
  - `ja`: enemy='黒錆の蒸気巨象' == ui['黑鏽蒸氣巨象']='黒錆の蒸気巨象'
  - `ko`: enemy='검은녹 증기 거상' == ui['黑鏽蒸氣巨象']='검은녹 증기 거상'
  - `es`: enemy='Coloso de Vapor de Óxido Negro' == ui['黑鏽蒸氣巨象']='Coloso de Vapor de Óxido Negro'
- 六語系 `enemy.json` 與 `ui.json` 同 id 譯名 100% 逐一相等，零分歧。

### 4. 零系統 Emoji 檢核
全畫面（鐵匠按鈕、巨偶卡片、結算 ScrapRewardPanel、大廳 HUD、Dock 導航、衣櫥、背包）100% 清除 Emoji，採用向量幾何圖標、手繪圖資與圓潤粉圓字體。

### 5. 舊功能回歸檢核
- 大廳主城：浮空島天空王國正常顯示、看板角色待機正常、頂部數值正常。
- 四區出征：四區主線按鈕與停擺巨偶子模式切換流暢、無衝突。
- 換裝衣櫥：角色紙娃娃換裝、套裝讀取正常。
- 冒險背包：既有道具顯示與鐵屑（iron_scrap）數量展示正常。
