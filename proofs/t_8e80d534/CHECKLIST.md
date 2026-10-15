# PowerStatDialog 玩具家族與外裝卡片連動前往衣櫥快捷按鈕驗收存證 (t_8e80d534)

## 驗收重點
- [x] PowerStatDialog 捲動區具備 WardrobeCard 玩具家族與外裝展示卡片（米黃底、深藍紫描邊、橙色標題）。
- [x] 玩具家族膠囊正確讀取並顯示當前玩家家族（預設胡桃鉗兔）。
- [x] 當前外裝膠囊正確讀取並顯示當前外裝名稱（預設胡桃鉗近衛軍裝）。
- [x] 前往衣櫥果凍按鈕 BtnGoWardrobe 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。
- [x] 實作 scroll_to_wardrobe_card() 方法可將可視區域平滑捲動至 WardrobeCard。
- [x] 點擊 BtnGoWardrobe 正確發射 wardrobe_requested 訊號並關閉彈窗，連動大廳開啟 WardrobeDialog。
- [x] 完整支援六語系即時切換（zh_TW, zh_CN, en, ja, ko, es），無缺漏字或 Emoji。

## 存證截圖列表
| 檔案名稱 | SHA256 (前 16 碼) | 說明 |
|---|---|---|
| `proof_01_zh_TW_power_stat_initial_overview.png` | `f2ce20b756aed79b` | 繁體中文 PowerStatDialog 戰力總覽初始頂部視圖 |
| `proof_03_zh_TW_scroll_to_wardrobe_card.png` | `56d3b85291f58aee` | 透過 scroll_to_wardrobe_card() 聚焦捲動至 WardrobeCard 玩具外裝卡片 |
| `proof_02_zh_TW_click_go_wardrobe_opens_wardrobe_dialog.png` | `ad25487f6a4c94b6` | 點擊 BtnGoWardrobe 前往衣櫥後連動開啟 WardrobeDialog 換裝衣櫥彈窗 |
| `proof_04_en_power_stat_wardrobe_card.png` | `0db25b616ccad9f4` | English: WardrobeCard with Toy Family & Outfit and Wardrobe button |
| `proof_05_ja_power_stat_wardrobe_card.png` | `b9cee92b5a637da8` | Japanese: WardrobeCard with Toy Family & Outfit and Wardrobe button |
| `proof_06_ko_power_stat_wardrobe_card.png` | `bd20bc5b0237624e` | Korean: WardrobeCard with Toy Family & Outfit and Wardrobe button |
| `proof_07_es_power_stat_wardrobe_card.png` | `68c30b2f5ff895e2` | Spanish: WardrobeCard with Toy Family & Outfit and Wardrobe button |

