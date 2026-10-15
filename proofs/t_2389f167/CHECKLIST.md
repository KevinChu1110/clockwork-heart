# PowerStatDialog 戰力屬性總覽新增每日上發條委託進度卡片與前往委託快捷按鈕驗收存證 (t_2389f167)

## 驗收重點
- [x] PowerStatDialog 捲軸中成功構建 WindupDailyCard 冒險委託上發條卡片（溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px）。
- [x] 委託狀態標籤膠囊 WindupStatusCapsule 與 WindupStatusLabel 支援待完成與今日已完成狀態切換。
- [x] 今日領取膠囊 WindupClaimCapsule 與 WindupClaimLabel 支援今日未領取、可領取獎勵與今日已領取狀態。
- [x] 委託進度標籤 WindupProgressLabel 動態顯示今日委託完成進度（如 0/3 -> 3/3）。
- [x] 前往委託立體果凍按鈕 BtnGoWindupDaily 規格合規（寬 120px、高 48px 符合熱區 >= 48px、底邊 5px、圓角 18px、零系統 Emoji）。
- [x] 點擊 BtnGoWindupDaily 正確發射 windup_daily_requested 訊號並關閉 PowerStatDialog，連動大廳直通開啟 WindupDailyDialog。
- [x] 完整支援六語系 i18n 即時切換無缺失（zh_TW, zh_CN, en, ja, ko, es），零系統 Emoji。

## 實機截圖清單
| 截圖檔案 | SHA256 (前 16 碼) | 說明 |
|---|---|---|
| `proof_01_windup_card_zh_TW_initial.png` | `a8a70a736fea8080` | 繁體中文初始狀態（未完成、待完成委託/今日未領取膠囊與前往委託按鈕） |
| `proof_02_windup_card_completed_3_of_3.png` | `040bf0edc27d7987` | 每日委託全完成狀態（今日已完成綠膠囊、今日已領取藍膠囊、3/3進度） |
| `proof_03_windup_card_en.png` | `160042caa1c0cd98` | 英文語言 (en) 實機渲染存證 |
| `proof_04_windup_card_ja.png` | `0baeb4dbc75d4d09` | 日文語言 (ja) 實機渲染存證 |
| `proof_05_windup_card_ko.png` | `dee71320e26d2d64` | 韓文語言 (ko) 實機渲染存證 |
| `proof_06_windup_card_es.png` | `f6d490b2c6e34697` | 西班牙文語言 (es) 實機渲染存證 |
| `proof_07_windup_card_zh_CN.png` | `b3ec2d93ac9646df` | 簡體中文語言 (zh_CN) 實機渲染存證 |
| `proof_08_click_go_windup_opens_windup_daily_dialog.png` | `aa53bff07a143f3e` | 點擊前往委託後安全關閉戰力彈窗並開啟 WindupDailyDialog 真畫面 |

