# W8-B2 · 日事件×7 toast／選項字（對齊 Ken W8-K2）

> Owner：Bingo｜交 @Kevin → Frank i18n  
> 來源：`game/data/ken/w8_k2_daily_events.json`｜％不改｜漏天不補｜picksPerDay=1

## 選項 label（必須與 K2 一致）

| DayId | CharacterId | A label | B label |
|-------|-------------|---------|---------|
| D1 | xiaobai | 上滿發條 | 先休息 |
| D2 | lion | 陪練揮劍 | 擦亮黃銅甲 |
| D3 | fox | 夜探工坊 | 聽齒輪故事 |
| D4 | pig | 幫忙搬彈簧 | 分享午茶 |
| D5 | xiaobai | 拆一顆試試 | 圖鑑整理 |
| D6 | lion | 掃蕩加練 | 養精蓄銳 |
| D7 | fox | 週末抽魂加碼 | 發放零件禮 |

## Toast key（選完立刻播）

格式：`daily.{DayId}.{ChoiceId}.toast`

| key | zh-TW（數字吃表） |
|-----|-------------------|
| `daily.D1.A.toast` | 幫小白上滿！金幣＋{Gold}，發條＋{WindStamina} |
| `daily.D1.B.toast` | 先讓他休息～金幣＋{Gold}，經驗＋{exp}，發條＋{WindStamina} |
| `daily.D2.A.toast` | 陪獅揮劍！金幣＋{Gold}，經驗＋{exp} |
| `daily.D2.B.toast` | 黃銅甲擦亮了！金幣＋{Gold}，黃銅齒輪入手 |
| `daily.D3.A.toast` | 夜探工坊成功～金幣＋{Gold}，抽魂票＋{SoulTicket} |
| `daily.D3.B.toast` | 聽完齒輪故事。金幣＋{Gold}，經驗＋{exp} |
| `daily.D4.A.toast` | 彈簧搬完！金幣＋{Gold}，發條彈簧入手 |
| `daily.D4.B.toast` | 午茶真好～金幣＋{Gold}，發條＋{WindStamina} |
| `daily.D5.A.toast` | 拆一顆試試！金幣＋{Gold}（核心碎片機率中） |
| `daily.D5.B.toast` | 圖鑑整齊了。金幣＋{Gold}，經驗＋{exp} |
| `daily.D6.A.toast` | 掃蕩加練！金幣＋{Gold}，經驗＋{exp} |
| `daily.D6.B.toast` | 養精蓄銳中。金幣＋{Gold}，發條＋{WindStamina} |
| `daily.D7.A.toast` | 週末抽魂加碼！抽魂票＋{SoulTicket} |
| `daily.D7.B.toast` | 零件禮送出～金幣＋{Gold}，黃銅齒輪入手 |

## 旁白 body（貼紙感，可選）

| DayId | body key | zh-TW |
|-------|----------|-------|
| D1 | `daily.D1.body` | 小白背鑰鬆半格，走起路搖搖晃晃。 |
| D2 | `daily.D2.body` | 獅想加練，黃銅甲卻有點髒。 |
| D3 | `daily.D3.body` | 狐耳朵豎著：工坊夜裡會說話。 |
| D4 | `daily.D4.body` | 豬圍裙口袋又掉彈簧了。 |
| D5 | `daily.D5.body` | 小白盯著圖鑑缺頁：「再拆一顆？」 |
| D6 | `daily.D6.body` | 獅拍胸甲：「掃蕩，或先養精蓄銳？」 |
| D7 | `daily.D7.body` | 狐眨眼：「週末要票，還是要零件禮？」 |

## 共用

| key | zh-TW |
|-----|-------|
| `daily.title` | 今天，誰需要上發條？ |
| `daily.miss` | 昨天那格發條空轉了（不補發）。 |
| `daily.already` | 今天這格已經轉過啦。 |

