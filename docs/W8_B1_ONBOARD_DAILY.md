# W8-B1 · 新手 3 分鐘＋每日「誰要上發條」×7

> Owner：Bingo｜交 @Kevin → Frank／Mark／Alice  
> 對齊：§8 煙測、抽魂唯一池、Art Pivot v2 貼紙語氣｜⛔ 不寫轉蛋／翠嶺／藍條  
> CharacterId：`xiaobai`／`lion`／`fox`／`pig`（`rabbit` 僅 alias）

---

## A. 新手 3 分鐘（對白＋cue）

目標：0–180s 內完成「知道發條→打到拆→看圖鑑→抽一魂（可跳過消費）」

| t(s) | 節點 | 畫面／操作 | 對白 key | 文案 | Cue |
|------|------|------------|----------|------|-----|
| 0–10 | `N01` | 小白睜眼、背鑰轉 | `onb.n01` | 呀——背上一緊，發條轉起來了！ | `sfx.ui.wind_tick` |
| 10–25 | `N02` | 胸口光 HUD 首次 | `onb.n02` | （系統）看胸口那圈～那是發條，不是藍條。 | `sfx.ui.wind_tick` |
| 25–50 | `N03` | 短走／點調查 | `onb.n03` | 齒輪還在嘀嗒。去摸摸看！ | `sfx.explore.interact` |
| 50–70 | `N04` | 遇敵進戰 | `onb.n04` | 擋路的，請開～ | `sfx.battle.start` |
| 70–110 | `N05` | 接縫亮→拆 | `onb.n05` | 接縫開開！鎖那一塊——拆！ | `sfx.battle.part_break` |
| 110–130 | `N06` | 糖果屑＋入袋 | `onb.n06` | 黃銅齒輪，圖鑑＋1！ | `sfx.dismantle.core_glint`（或 pop） |
| 130–160 | `N07` | 抽魂 UI（1 張教學票） | `onb.n07` | 上緊——抽一格！看看會跳出什麼貼紙。 | `soul.pull_start` |
| 160–180 | `N08` | 結果卡／可換裝 | `onb.n08` | 新東西進口袋了。今天，還想幫誰上發條？ | `soul.pull_outfit` 或 `pull_part` |

**教學票**：`SoulTicket`×1（僅新手，不進付費池文案）  
**可跳過**：N07 可「稍後再說」，但 N05 拆零件不可跳（對齊 60s 首拆精神，整段壓在 3 分鐘內）。

### 新手字串表

| key | zh-TW |
|-----|-------|
| `onb.n01` | 呀——背上一緊，發條轉起來了！ |
| `onb.n02` | 看胸口那圈～那是發條，不是藍條。 |
| `onb.n03` | 齒輪還在嘀嗒。去摸摸看！ |
| `onb.n04` | 擋路的，請開～ |
| `onb.n05` | 接縫開開！鎖那一塊——拆！ |
| `onb.n06` | 黃銅齒輪，圖鑑＋1！ |
| `onb.n07` | 上緊——抽一格！看看會跳出什麼貼紙。 |
| `onb.n08` | 新東西進口袋了。今天，還想幫誰上發條？ |

---

## B. 每日事件 ×7（「今天，誰需要上發條？」）

結構：事件 id｜對象｜30 字內劇情｜玩家二選一｜獎勵暗示（Ken 填％）｜粉專鉤

| Day | EventId | 對象 | 劇情 | A | B | 獎勵暗示 | 粉專鉤 |
|-----|---------|------|------|---|---|----------|--------|
| 1 | `daily.wind_xiaobai` | xiaobai | 小白背鑰鬆半格，走起路搖搖晃晃。 | 幫他上滿 | 先讓他休息 | 發條＋／親密＋ | 你會幫小白上滿嗎？ |
| 2 | `daily.wind_lion` | lion | 獅的護心背心扣子卡死，心光一閃一閃。 | 幫獅扣上 | 笑他笨手笨腳 | 金幣／親密 | 獅該不該自己扣？ |
| 3 | `daily.wind_fox` | fox | 狐的圍巾被風吹成螺旋，堅持說是造型。 | 幫她整理 | 再繞兩圈更可愛 | SoulTicket 碎片 | 圍巾要整齊還是亂？ |
| 4 | `daily.wind_pig` | pig | 豬圍裙口袋掉出黃銅屑，像一路種星星。 | 幫他撿齊 | 留著當路標 | 零件機率↑ | 屑屑撿起來嗎？ |
| 5 | `daily.wind_clock` | 大鐘（場景） | 停擺大鐘咳了一聲，要請誰去聽診。 | 派今日編隊 | 自己去聽 | 掃蕩券／經驗 | 你派誰去聽大鐘？ |
| 6 | `daily.wind_codex` | 圖鑑 | 圖鑑缺一頁陰影，寫著「還差一顆心」。 | 去拆一次 | 去抽一魂 | 指向 §8／抽魂 | 拆還是抽？ |
| 7 | `daily.wind_share` | 玩家 | 發條之心問：今天這格，送給誰？ | 選四角色之一 | 留給自己 | 日獎勵＋展示 | 今天上給誰？留言角色 |

### 日事件共用 cue

| Cue | 時機 |
|-----|------|
| `sfx.ui.wind_tick` | 事件開場 |
| `sfx.ui.confirm` | 選 A／B |
| `soul.pull_start` | Day6 若選抽魂 |
| `sfx.battle.part_break` | Day6 若選拆 |

### 日事件字串 key 例（Day1）

| key | zh-TW |
|-----|-------|
| `daily.wind_xiaobai.title` | 今天，誰需要上發條？ |
| `daily.wind_xiaobai.body` | 小白背鑰鬆半格，走起路搖搖晃晃。 |
| `daily.wind_xiaobai.a` | 幫他上滿 |
| `daily.wind_xiaobai.b` | 先讓他休息 |

（Day2–7 同結構，`EventId` 代換。）

---

## C. Cue 總表（本檔新增／沿用）

| Cue ID | 用途 |
|--------|------|
| `sfx.ui.wind_tick` | 發條／日事件開場 |
| `sfx.ui.confirm` | UI 確認 |
| `sfx.explore.interact` | 新手調查 |
| `sfx.battle.start`／`part_break` | 新手戰鬥／拆 |
| `sfx.dismantle.core_glint` | 稀有閃 |
| `soul.pull_start`／`pull_part`／`pull_outfit` | 抽魂（已有文案於 W7-B1） |

---

## D. 驗收

- [ ] 新手 ≤180s 可走到第一次拆＋看過圖鑑  
- [ ] 日事件 7 則皆無轉蛋用語  
- [ ] key 與 CharacterId 正式欄為 `xiaobai`  
- [ ] Mark 可直接抽 Day 列當粉專每日鉤  

