# 驗收證明 · 停擺巨偶部位破壞掉既有鐵屑 (t_d5d54af1)

## 依據規範
- `review.md 0-QA5 / 0-QA26`：Godot framebuffer 直接擷取，嚴禁 PIL 假圖。
- `review.md 0-QA23`：OUT_DIR 獨立目錄，存證至 proofs/t_d5d54af1/，不覆蓋其他任務目錄。
- `review.md 0-QA25`：全畫面多語系動態即時連動刷新。
- 零系統 Emoji、手遊多巴胺亮色盤。

## 截圖清單
| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零 Emoji | 部位破壞鐵屑獲得 (ScrapRewardPanel) | 驗證結論 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|
| 01 | `proof_colossus_part_scrap_victory.png` | 停擺巨偶戰鬥勝場結算彈窗全景 | ✓ 無破圖 | ✓ 零 Emoji | ✓ 清晰顯示「部位破壞」「鐵屑 +2」 | **通過 (PASS)** |

## 實機規格檢核
1. 視窗解析度：1280x720 橫屏手遊標準規範。
2. 獎勵面板：CorePartDropCard（金階發條發電機）、ExpRewardPanel（經驗 +85）、ScrapRewardPanel（部位破壞：鐵屑 +2）垂直排列完好且高度適中，零截字。
3. 零系統 emoji：標題、副標、機芯卡片、經驗標籤、鐵屑標籤、按鈕 100% 無系統 emoji。
4. 巨偶破部位：戰後結算正確顯示鐵屑增額，並同步入袋至背包（既有 iron_scrap，不新道具 id）。
5. 沒破部位：ScrapRewardPanel 自動隱藏，不濫發鐵屑。
6. 一般關卡與獵場：掉落規則完全不受影響。
