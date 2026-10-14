# PowerStatDialog 停擺巨偶挑戰進度卡片與前往挑戰快捷按鈕驗收存證 (t_72c395b0)

## 驗收重點
- [x] PowerStatDialog 捲軸中具備 ColossusCard 停擺巨偶卡片（奶油白底、深藍紫描邊、橙色標題、次數膠囊）。
- [x] 今日挑戰次數膠囊讀取正確，支援動態刷新顯示（x/3）。
- [x] 推薦目標依玩家等級動態適配（Lv.1~9 推薦發條獅，Lv.10~17 推薦提線人偶，Lv.18+ 推薦蒸氣巨象）。
- [x] 前往挑戰果凍按鈕 BtnGoColossus 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。
- [x] 點擊 BtnGoColossus 正確發射 colossus_requested 訊號並關閉彈窗，連動大廳直通出征/停擺巨偶介面。
- [x] 完整支援六語系即時切換（zh_TW, zh_CN, en, ja, ko, es），無缺漏字或 Emoji。

## 存證截圖列表
| 檔案名稱 | SHA256 (前 16 碼) | 說明 |
|---|---|---|
| `proof_01_colossus_card_zh_TW.png` | `1bfd20dd5b350bed` | 繁體中文預設展示：停擺巨偶卡片、今日挑戰: 3/3 與前往挑戰按鈕 |
| `proof_02_colossus_entries_1_of_3.png` | `ee0c324248e5270a` | 次數動態刷新展示：今日挑戰: 1/3 |
| `proof_03_colossus_target_elephant_lv25.png` | `ab4485fd0d85f2f0` | 推薦目標動態刷新展示：Lv.25 推薦黑鏽蒸氣巨象 (Lv.28) |
| `proof_04_colossus_card_en.png` | `14af4cae1b667c40` | 六語系展示：英文 (en) Dormant Colossus / Challenge |
| `proof_05_colossus_card_ja.png` | `6f9fe04cbf0621fa` | 六語系展示：日文 (ja) 停止した巨像 / 挑戦へ |
| `proof_06_colossus_card_ko.png` | `f56c736c17dafcaf` | 六語系展示：韓文 (ko) 멈춘 거상 / 도전하기 |
| `proof_07_colossus_card_es.png` | `b2426a4b0f1ca9eb` | 六語系展示：西文 (es) Coloso Inerte / Desafiar |
| `proof_08_colossus_card_zh_CN.png` | `bbe4bb489472bb22` | 六語系展示：簡體中文 (zh_CN) 停摆巨偶 / 前往挑战 |
| `proof_09_click_go_colossus_switches_lobby_to_colossus.png` | `1ee55cdcd237972c` | 點擊前往挑戰後連動大廳直通出征停擺巨偶介面 |

