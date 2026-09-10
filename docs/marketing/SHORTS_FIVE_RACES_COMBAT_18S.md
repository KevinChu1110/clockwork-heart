# 《發條之心》18 秒五族實機打擊短影音分鏡腳本與素材清單
## 主題：五大玩具族系實機戰鬥姿態全面實裝（內部企劃代號：mk-five-races）

> **文件狀態**：純分鏡腳本與實機錄影素材清單規劃（⛔ 不產片、不呼叫 Veo/fal、不發 FB、不改官網）。  
> **制定日期**：2026-09-10  
> **負責人**：側案·程式 阿宏（sideworker）  
> **對應項目**：`docs/PROJECTS.json` 中的 `mk-five-races`（五族實機打擊短影音分鏡與素材清單）  
> **核心賣點**：**「五大玩具族系實機戰鬥姿態全面上線 · 告別舊版空手與單一兔族，五族打擊手感爽快各異」** —— 戰鬥直接走 `SpriteDB.player_pose()` 切換姿態，100% 真實 Godot 實機戰鬥畫面，徹底替換舊版空手/舊兔錄影素材。  
> **交付物依據**：對齊 `references/media.md` 短影音格式、`references/brand_assets.md` 鏡頭語言準則、`references/art_direction.md` §6.5 之 9:16 規格，以及 `references/review.md` 第 10～19 條全項影片與行銷審核清單。

---

## 一、基本參數與製作規範

| 項目 | 規範標準 | 說明（依據 review.md） |
|---|---|---|
| **本片主題（內部代號）** | 五族實機戰鬥姿態實裝（`mk-five-races`） | ⚠️ 內部企劃代號，片內絕不出現此代號，亦不自立花俏片名；片尾點題卡僅由後製疊加官方字標 `branding/logo_cn.png`（第 19c 條） |
| **總長度** | **剛好 18.0 秒**（18.00s） | 精準落在 15～20 秒短影音黃金完播區間，節奏明快有力 |
| **畫幅比例** | **9:16 直式（1080×1920）** | 全片各鏡統一比例，嚴禁混用橫式 16:9 或 4:5（第 12 條） |
| **總鏡頭數** | **7 個分鏡**（Shot 1～7） | 1 個懸念開場 ＋ 5 族連續實機打擊 ＋ 1 個品牌點題收束 |
| **開場 3 秒（Hook）** | **狀態與懸念**（極近工坊微距、發條咬合急轉、青綠核心充能） | 嚴禁 Logo、嚴禁遊戲名稱、無任何自我介紹或宣傳文字（第 11 條） |
| **點題卡（CTA）** | 僅置於 Shot 7（15.5～18.0s） | 由後製無失真疊加官方字標 `branding/logo_cn.png` 於純黑底板 `branding/title_plate.png`，嚴禁 AI 生成（第 19c／15a 條）；標註「開發中畫面 · 官網搶先看」 |
| **音效原則** | **真實金屬發條實體音效優先** | 發條咬合、長劍出鞘破空、金屬交鋒、秘術爆裂、重錘砸地、彈簧連抓、齒輪喀嗒；嚴禁罐頭史詩管弦配樂（第 14 條） |
| **素材來源真實性** | **100% 基於已合併 main 之功能** | 實機鏡次（Shot 2～6）100% 來自既有 Godot 戰鬥系統與已合併入庫之五族 30 個姿態檔案，絕無概念圖冒充實機（第 16／19b／19 條） |
| **過程動詞描述** | **如實反映畫面渲染要素** | 嚴格依據實際可見的姿態切換、位移、打擊停頓與特效跳字撰寫，嚴禁腦補未畫出的動作過程（第 19i-4 條） |

---

## 二、核心賣點轉譯：五大玩具族系打擊手感特色

本支短影音專門向玩家展示《發條之心》角色視覺與手感核心升級：**五大玩具族系均已實裝專屬六大戰鬥姿態（idle、telegraph、attack、hit、recover、skill）**，戰鬥運行 `SpriteDB.player_pose()` 順暢切換，告別單一角色與舊版空手問題：

1. **兔族（小白 Whitey · 劍士）**：
   - 核心特徵：2.3 頭身米白金屬發條兔，立耳金屬板件，單手持晨光長劍。
   - 打擊特色：高速突刺前衝，觸發精確 0.15s Hitstop 打擊停頓，金色齒輪火花爆散。
2. **獅族（烈昂 Leon · 騎士）**：
   - 核心特徵：皇家守衛深藍金屬獅，金屬片沖壓鬃毛，持騎士長槍。
   - 打擊特色：長槍直線突貫，剛猛沉穩，伴隨金屬交鋒撞擊與受擊微震。
3. **狐族（靈狐 Fox · 法師）**：
   - 核心特徵：微縮舞台藍法袍，分節金屬狐耳與機械尾，持琉璃法杖。
   - 打擊特色：法杖前引聚能光環，法球爆裂破擊，青綠核心光芒迸發。
4. **豬族（鋼牙豕 Boar · 戰士）**：
   - 核心特徵：維京沖壓玩具鎧甲，金屬豬牙與鼻板，手持鍛造巨錘。
   - 打擊特色：後仰雙手高舉蓄勢，崩山重錘砸地猛擊，地面微幅震顫與碎石飛濺。
5. **猴族（靈爪猴 Spring Macaque · 武道刺客）**：
   - 核心特徵：高光香檳金外殼，小臂粗螺旋黃銅彈簧關節，手裝機關發條銅爪。
   - 打擊特色：彈簧手臂極速伸縮連打，漫天爪痕殘影，怒氣滿額爆發「暴怒覺醒！」狀態。

---

## 三、接鏡軸線與運鏡節奏設計（連續動態流）

全片拒絕靜圖幻燈片輪播，採用「微距懸念爆發 → 五族連續打擊交接 → 品牌點題定格」的無縫銜接設計：

```
Shot 1 (0.0-3.0s)  【概念·微距】昏暗工坊微距：背後發條鑰匙急轉半圈「喀——嗒！」，青綠核心暴亮充能
        │ (核心光芒暴漲穿透，無縫切入實機戰鬥畫面)
Shot 2 (3.0-5.5s)  【實機·兔族】荒路殘兵：小白持長劍突刺，0.15s Hitstop 打擊停頓，金色齒輪火花爆散
        │ (劍刃斬擊金光橫掠，鏡頭順時針微旋推入長槍槍尖)
Shot 3 (5.5-8.0s)  【實機·獅族】巡邏守衛：烈昂騎士長槍直線突貫，金屬交鋒「鏘啷」，重擊穿透
        │ (長槍前衝氣浪激發青綠法陣光芒)
Shot 4 (8.0-10.5s) 【實機·狐族】暗影僕從：靈狐法杖前引充能，青綠法球轟擊炸裂，晶石崩解
        │ (法球爆破氣流向下衝壓，畫面上方巨錘破空呼嘯砸落)
Shot 5 (10.5-13.0s)【實機·豬族】守衛巨獸：鋼牙豕高舉巨錘蓄勢，崩山重砸震地，屏幕震顫碎石飛濺
        │ (震波掀起煙塵，彈簧小臂自煙塵中閃電般極速前伸)
Shot 6 (13.0-15.5s)【實機·猴族】守衛泰坦：靈爪猴彈簧手臂連環裂空快爪，金光四濺，跳出「暴怒覺醒！」
        │ (雙爪十字重撕震屏白閃，瞬間切純黑底板)
Shot 7 (15.5-18.0s)【合成·點題】純黑底板微推，後製疊加官方字標《發條之心》，一聲「喀嗒」收束
```

---

## 四、18 秒分鏡詳表（Shot-by-Shot）

| 鏡次 | 秒數 | 畫面內容（嚴格遵守第 19i-4 條） | 種族與姿態檔路徑（第 19e 條） | 運鏡語言 | 聲音設計（實體音優先） | 字幕與文案（第 15/15a 條） | 素材屬性與真實性標註 |
|---|---|---|---|---|---|---|---|
| **Shot 1<br>【上弦懸念】** | `0.0-3.0s`<br>(3.0s) | 昏暗工坊微距特寫。米白金屬發條兔四分之三側身剪影，背後黃銅發條鑰匙清晰外露。第 0.0s 發條鑰匙猛然急轉半圈，胸口青綠核心光芒瞬間暴亮，照亮斑駁齒輪與金屬長劍，光芒填滿畫面轉場。 | **概念模型 / 9:16 特寫素材**<br>（參照 `references/art_direction.md` §6.5 提示詞規格） | 極近微距推鏡（Dolly In 105%），景深極淺，焦點自背後鑰匙移至核心光暈。兔身不位移。 | 0.0s 一記清脆乾淨的發條齒輪咬合「喀——嗒！」（`clock.wav`），緊隨核心低頻蓄能共鳴。**零 BGM、零管弦樂。** | （開場 3 秒零文字、無 Logo、無遊戲名，依第 11 條） | **【概念素材·9:16】**<br>開場懸念氛圍引導，嚴禁 AI 圖冒充實機標籤。 |
| **Shot 2<br>【兔劍突刺】** | `3.0-5.5s`<br>(2.5s) | 光芒穿透切入荒路實機戰鬥。小白面對荒路殘兵，長劍直刺突進，命中觸發精確 0.15s 打擊停頓（Hitstop），爆散金色齒輪火花與傷害跳字，隨後順暢收招。 | **兔族（Rabbit）**<br>待機：`game/assets/sprites/player/poses/idle.png`<br>攻擊：`game/assets/sprites/player/poses/attack.png`<br>收招：`game/assets/sprites/player/poses/recover.png` | 平視直式向戰鬥中央平滑推鏡（Push In 110%），劍尖突刺衝擊感居中。 | 長劍出鞘破空「颼——」（`slash.wav`），斬擊受擊清脆金屬回響「鏘！」（`hit.wav`）。 | （遊戲畫面純淨無文字，無 Logo） | **【實機素材·REC-01】**<br>錄製自 Godot `res://scenes/battle/battle.tscn`，`setup("road_bandit")`。 |
| **Shot 3<br>【獅槍突貫】** | `5.5-8.0s`<br>(2.5s) | 劍光掠過無縫接獅衛突擊。烈昂雙手端皇家長槍向前疾刺，槍尖破風金芒直線貫穿巡邏傀儡胸甲，敵方受擊微幅震顫與金色火花飛濺。 | **獅族（Lion）**<br>待機：`game/assets/sprites/player/poses/lion/idle.png`<br>攻擊：`game/assets/sprites/player/poses/lion/attack.png`<br>技能：`game/assets/sprites/player/poses/lion/skill.png` | 沿長槍突刺衝擊軸線平滑跟進（Push In 112%），鎖定槍尖穿透點。 | 長槍前衝破空風聲，金屬撞擊交鋒「鏘啷——」（`clash.wav`）與沉重受擊音（`hit.wav`）。 | （遊戲畫面純淨無文字，無 Logo） | **【實機素材·REC-02】**<br>錄製自 Godot `res://scenes/battle/battle.tscn`，`setup("patrol_golem")`。 |
| **Shot 4<br>【狐杖爆破】** | `8.0-10.5s`<br>(2.5s) | 長槍氣浪引動青綠光陣。靈狐手持琉璃法杖前引，杖頭晶石聚能發光，瞬間爆發青綠秘術法球轟向暗影僕從，法球爆裂炸開，衝擊波擴散。 | **狐族（Fox）**<br>待機：`game/assets/sprites/player/poses/fox/idle.png`<br>預警：`game/assets/sprites/player/poses/fox/telegraph.png`<br>技能：`game/assets/sprites/player/poses/fox/skill.png`<br>攻擊：`game/assets/sprites/player/poses/fox/attack.png` | 鏡頭自法杖水晶平滑推向受擊爆裂點（Push In 115%），展現法術衝擊反饋。 | 核心能量引導呼嘯「呼——」（`fire.wav`），法球命中晶石炸裂聲「轟！」（`break.wav`）。 | （遊戲畫面純淨無文字，無 Logo） | **【實機素材·REC-03】**<br>錄製自 Godot `res://scenes/battle/battle.tscn`，`setup("shadow_servant")`。 |
| **Shot 5<br>【豬錘重砸】** | `10.5-13.0s`<br>(2.5s) | 爆風下壓，畫面頂部巨錘重重砸落！鋼牙豕雙手高舉維京巨錘後仰蓄勢，隨即全身發力猛砸地面，重錘轟擊巨獸前肢，地面微幅震顫，碎石與火星迸濺。 | **豬族（Boar）**<br>待機：`game/assets/sprites/player/poses/boar/idle.png`<br>蓄力：`game/assets/sprites/player/poses/boar/telegraph.png`<br>攻擊：`game/assets/sprites/player/poses/boar/attack.png`<br>收招：`game/assets/sprites/player/poses/boar/recover.png` | 低視角向砸地落點平滑下壓推進（Dolly Down-In 118%），著重展現重擊份量。 | 巨錘撕裂空氣破空重音（`rock.wav`），重錘砸地震裂巨響「轟——鏘！」（`break.wav`）。 | （遊戲畫面純淨無文字，無 Logo） | **【實機素材·REC-04】**<br>錄製自 Godot `res://scenes/battle/battle.tscn`，`setup("guard_beast")`。 |
| **Shot 6<br>【猴爪狂連】** | `13.0-15.5s`<br>(2.5s) | 震波煙塵散開，靈爪猴自煙塵疾衝而出！螺旋彈簧手臂高速伸展連擊，機關銅爪化作連環裂空殘影撕向守衛泰坦，火花四射，上方觸發「暴怒覺醒！」橘紅跳字！最後一爪重擊交錯白閃切純黑。 | **猴族（Macaque）**<br>待機：`game/assets/sprites/player/poses/macaque/idle.png`<br>蓄力：`game/assets/sprites/player/poses/macaque/telegraph.png`<br>技能：`game/assets/sprites/player/poses/macaque/skill.png`<br>攻擊：`game/assets/sprites/player/poses/macaque/attack.png` | 近身高動態平滑跟進特寫（Tracking In 120%），快速連擊與跳字緊湊呈現。 | 彈簧急劇伸縮呼嘯「颼——」（`wind.wav`），銅爪連續撕裂抓擊「嗤啦啦」（`slash.wav`），金屬暴擊回響（`hit.wav`）。 | 【暴怒覺醒！】<br>（遊戲原生效能跳字，無系統 emoji） | **【實機素材·REC-05】**<br>錄製自 Godot `res://scenes/battle/battle.tscn`，`setup("leo")`，預充怒氣 100%。 |
| **Shot 7<br>【點題收束】** | `15.5-18.0s`<br>(2.5s) | 白閃切入純黑底板（`branding/title_plate.png`），中央後製疊加手繪繪本風官方字標《發條之心》（`branding/logo_cn.png`）。下方標語：「給心上弦，重新出發。」底部標註：「開發中畫面 · 官網搶先看」。 | **品牌固定資產**<br>底板：`branding/title_plate.png`<br>字標：`branding/logo_cn.png` | 純黑底板微幅緩推 102%，字標邊緣一道溫暖金色高光掃過。 | 15.8s 一聲清脆悠長的單聲發條「喀嗒」（`clock.wav`），隨後安靜收尾。 | 標題卡由後製無失真疊加官方字標，不得由 AI 生成。<br>官網搶先看 | **【固定資產·合成】**<br>使用官方固定品牌資產，依第 15/16 條不放上架日、價格或下載鈕。 |

- **秒數累計核對**：`3.0s + 2.5s + 2.5s + 2.5s + 2.5s + 2.5s + 2.5s = 18.0 秒`（精準嚴絲合縫，共 7 鏡）。

---

## 五、Godot 實機素材錄影清單與操作序列（REC-01～REC-05）

> **審核鐵則（review.md 第 19 條、第 19b 條、第 19e 條）**：  
> 所有標示「實機」之素材，**必須能在既有 Godot 引擎中重現與錄製，且功能 100% 已合併進 main**。嚴禁以 AI 概念圖充當實機，嚴禁列出「尚未實裝」的功能。

以下為本片所需 5 支實機錄影片段規格與操作序列清單：

### 【實機素材 1：REC-01 兔族小白長劍突刺 (Whitey Sword Strike)】
- **對應分鏡**：Shot 2 (3.0s～5.5s，時長 2.50s)
- **所屬功能**：`mob-battle` 與 `race-poses`（兔族戰鬥姿態）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`（`_set_player_pose()`）、`game/scripts/art/sprite_db.gd`（`player_pose()`）
- **使用姿態檔案**：
  - `game/assets/sprites/player/poses/idle.png`
  - `game/assets/sprites/player/poses/attack.png`
  - `game/assets/sprites/player/poses/recover.png`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("road_bandit")`。
  2. 設定玩家種族：`GameState.player_race = "rabbit"`。
  3. 呼叫 `_set_player_pose("idle")`，確認待機畫面渲染穩定。
  4. 觸發單手長劍突刺攻擊：呼叫 `_set_player_pose("attack", true)`，捕捉角色縮放壓扁（`scale = Vector2(1.1, 0.94)`）與 0.15s Hitstop 停頓。
  5. 命中觸發傷害跳字與金色齒輪火花，隨後自動過渡至 `recover` 收招姿態。
- **預期畫面**：小白持長劍突刺衝擊，0.15s 命中停頓，金色火花迸散，線條清晰帶深色厚描邊。

### 【實機素材 2：REC-02 獅族烈昂長槍突貫 (Leon Lance Pierce)】
- **對應分鏡**：Shot 3 (5.5s～8.0s，時長 2.50s)
- **所屬功能**：`race-poses`（獅族六大戰鬥姿態，main 合併 commit `40ffd70`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`、`game/scripts/art/sprite_db.gd`
- **使用姿態檔案**：
  - `game/assets/sprites/player/poses/lion/idle.png`
  - `game/assets/sprites/player/poses/lion/attack.png`
  - `game/assets/sprites/player/poses/lion/skill.png`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("patrol_golem")`。
  2. 設定玩家種族：`GameState.player_race = "lion"`。
  3. 呼叫 `_apply_battle_art("patrol_golem")`，確認獅族待機姿態載入。
  4. 觸發皇家長槍突刺：呼叫 `_set_player_pose("attack", true)`，長槍向前突刺。
  5. 接續觸發技能貫日：呼叫 `_set_player_pose("skill", true)`，槍尖金光破甲穿透，敵人受擊震顫。
- **預期畫面**：金屬獅衛持皇家長槍剛猛貫穿，金色金屬格擋光芒與受擊火花，身型緊湊威武。

### 【實機素材 3：REC-03 狐族靈狐法杖爆破 (Fox Staff Blast)】
- **對應分鏡**：Shot 4 (8.0s～10.5s，時長 2.50s)
- **所屬功能**：`race-poses`（狐族六大戰鬥姿態，main 合併 commit `40ffd70`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`、`game/scripts/art/sprite_db.gd`
- **使用姿態檔案**：
  - `game/assets/sprites/player/poses/fox/idle.png`
  - `game/assets/sprites/player/poses/fox/telegraph.png`
  - `game/assets/sprites/player/poses/fox/skill.png`
  - `game/assets/sprites/player/poses/fox/attack.png`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("shadow_servant")`。
  2. 設定玩家種族：`GameState.player_race = "fox"`。
  3. 呼叫 `_set_player_pose("telegraph")`，法杖前引聚能前搖，角色拉長蓄力（`scale = Vector2(0.97, 1.05)`）。
  4. 呼叫 `_set_player_pose("skill", true)`，法杖高舉迸裂青綠秘法光環。
  5. 呼叫 `_set_player_pose("attack", true)`，法球釋放命中僕從，產生青綠爆裂衝擊波。
- **預期畫面**：靈狐揮杖前引釋放秘法，青綠光環與法球爆散，藍色法袍與金屬機械尾分件清晰。

### 【實機素材 4：REC-04 豬族鋼牙豕重錘砸地 (Boar Hammer Smash)】
- **對應分鏡**：Shot 5 (10.5s～13.0s，時長 2.50s)
- **所屬功能**：`race-poses`（野豬六大戰鬥姿態，main 合併 commit `40ffd70`）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`、`game/scripts/art/sprite_db.gd`
- **使用姿態檔案**：
  - `game/assets/sprites/player/poses/boar/idle.png`
  - `game/assets/sprites/player/poses/boar/telegraph.png`
  - `game/assets/sprites/player/poses/boar/attack.png`
  - `game/assets/sprites/player/poses/boar/recover.png`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("guard_beast")`。
  2. 設定玩家種族：`GameState.player_race = "boar"`。
  3. 呼叫 `_set_player_pose("telegraph")`，巨錘雙手高舉後仰蓄勢。
  4. 呼叫 `_set_player_pose("attack", true)`，巨錘重重力劈砸地，產生地面震波與碎石特效。
  5. 自動過渡至 `_set_player_pose("recover")`，錘頭接地緩衝收招。
- **預期畫面**：鋼牙豕巨錘力劈華山，金屬碰撞震顫感強烈，維京沖壓鎧甲與金屬獠牙極具辨識度。

### 【實機素材 5：REC-05 猴族靈爪猴彈簧狂連 (Macaque Spring Claw)】
- **對應分鏡**：Shot 6 (13.0s～15.5s，時長 2.50s)
- **所屬功能**：`race-poses` 與 `mob-battle`（靈爪猴戰鬥姿態與暴怒覺醒）
- **Godot 場景路徑**：`res://scenes/battle/battle.tscn`
- **對應腳本**：`game/scripts/battle/battle_view.gd`（`trigger_fury_awakening()`）、`game/scripts/art/sprite_db.gd`
- **使用姿態檔案**：
  - `game/assets/sprites/player/poses/macaque/idle.png`
  - `game/assets/sprites/player/poses/macaque/telegraph.png`
  - `game/assets/sprites/player/poses/macaque/skill.png`
  - `game/assets/sprites/player/poses/macaque/attack.png`
- **錄製操作序列**：
  1. 啟動 `res://scenes/battle/battle.tscn`，傳入參數 `setup("leo")`。
  2. 設定玩家種族：`GameState.player_race = "macaque"`，預充怒氣至 100%（`player.rage = 100.0`）。
  3. 呼叫 `trigger_fury_awakening()`，畫面中央上方跳出「暴怒覺醒！」橘紅跳字。
  4. 呼叫 `_set_player_pose("skill", true)`，靈猴彈簧手臂極速前衝連環抓撓，爆出漫天金色爪痕。
  5. 呼叫 `_set_player_pose("attack", true)`，雙爪交錯重劈完成終結收招，隨後畫面白閃切黑。
- **預期畫面**：靈爪猴彈簧雙臂極速抓打、金光璀璨，暴怒覺醒跳字亮眼，多巴胺打擊反饋拉滿。

---

## 六、review.md 第 19e 條逐項查證清單（檔案存在性與大小驗證）

依據 `references/review.md` 第 19e 條與第 19e-1 條要求，對分鏡表（第四節、第五節）提及之所有姿態檔案、場景、Shader、腳本、音效與品牌資產進行實體 `ls` / `stat` 逐條查驗，**證明所有檔案 100% 存在於倉庫中**：

### 1. 五族六大戰鬥姿態檔案清單（30/30 實體存在）

| 種族 | 姿態 | 倉庫實體路徑 | 檔案大小 | 查驗結果 |
|---|---|---|---|---|
| **兔族 (Rabbit)** | idle | `game/assets/sprites/player/poses/idle.png` | 14,028 Bytes | ✅ 通過 |
| **兔族 (Rabbit)** | telegraph | `game/assets/sprites/player/poses/telegraph.png` | 12,802 Bytes | ✅ 通過 |
| **兔族 (Rabbit)** | attack | `game/assets/sprites/player/poses/attack.png` | 12,808 Bytes | ✅ 通過 |
| **兔族 (Rabbit)** | hit | `game/assets/sprites/player/poses/hit.png` | 12,240 Bytes | ✅ 通過 |
| **兔族 (Rabbit)** | recover | `game/assets/sprites/player/poses/recover.png` | 14,028 Bytes | ✅ 通過 |
| **兔族 (Rabbit)** | skill | `game/assets/sprites/player/poses/skill.png` | 12,808 Bytes | ✅ 通過 |
| **獅族 (Lion)** | idle | `game/assets/sprites/player/poses/lion/idle.png` | 23,065 Bytes | ✅ 通過 |
| **獅族 (Lion)** | telegraph | `game/assets/sprites/player/poses/lion/telegraph.png` | 24,832 Bytes | ✅ 通過 |
| **獅族 (Lion)** | attack | `game/assets/sprites/player/poses/lion/attack.png` | 21,930 Bytes | ✅ 通過 |
| **獅族 (Lion)** | hit | `game/assets/sprites/player/poses/lion/hit.png` | 23,758 Bytes | ✅ 通過 |
| **獅族 (Lion)** | recover | `game/assets/sprites/player/poses/lion/recover.png` | 22,726 Bytes | ✅ 通過 |
| **獅族 (Lion)** | skill | `game/assets/sprites/player/poses/lion/skill.png` | 24,458 Bytes | ✅ 通過 |
| **狐族 (Fox)** | idle | `game/assets/sprites/player/poses/fox/idle.png` | 19,549 Bytes | ✅ 通過 |
| **狐族 (Fox)** | telegraph | `game/assets/sprites/player/poses/fox/telegraph.png` | 19,178 Bytes | ✅ 通過 |
| **狐族 (Fox)** | attack | `game/assets/sprites/player/poses/fox/attack.png` | 22,205 Bytes | ✅ 通過 |
| **狐族 (Fox)** | hit | `game/assets/sprites/player/poses/fox/hit.png` | 20,740 Bytes | ✅ 通過 |
| **狐族 (Fox)** | recover | `game/assets/sprites/player/poses/fox/recover.png` | 18,382 Bytes | ✅ 通過 |
| **狐族 (Fox)** | skill | `game/assets/sprites/player/poses/fox/skill.png` | 21,983 Bytes | ✅ 通過 |
| **豬族 (Boar)** | idle | `game/assets/sprites/player/poses/boar/idle.png` | 22,631 Bytes | ✅ 通過 |
| **豬族 (Boar)** | telegraph | `game/assets/sprites/player/poses/boar/telegraph.png` | 24,691 Bytes | ✅ 通過 |
| **豬族 (Boar)** | attack | `game/assets/sprites/player/poses/boar/attack.png` | 28,444 Bytes | ✅ 通過 |
| **豬族 (Boar)** | hit | `game/assets/sprites/player/poses/boar/hit.png` | 21,466 Bytes | ✅ 通過 |
| **豬族 (Boar)** | recover | `game/assets/sprites/player/poses/boar/recover.png` | 23,512 Bytes | ✅ 通過 |
| **豬族 (Boar)** | skill | `game/assets/sprites/player/poses/boar/skill.png` | 21,362 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | idle | `game/assets/sprites/player/poses/macaque/idle.png` | 20,123 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | telegraph | `game/assets/sprites/player/poses/macaque/telegraph.png` | 19,652 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | attack | `game/assets/sprites/player/poses/macaque/attack.png` | 17,052 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | hit | `game/assets/sprites/player/poses/macaque/hit.png` | 18,873 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | recover | `game/assets/sprites/player/poses/macaque/recover.png` | 9,247 Bytes | ✅ 通過 |
| **猴族 (Macaque)** | skill | `game/assets/sprites/player/poses/macaque/skill.png` | 18,789 Bytes | ✅ 通過 |

### 2. 場景、著色器與邏輯腳本清單（實體存在）

| 檔案路徑 | 類型 | 檔案大小 | 查驗結果 |
|---|---|---|---|
| `game/scenes/battle/battle.tscn` | 核心戰鬥場景 | 8,614 Bytes | ✅ 通過 |
| `game/scenes/main.tscn` | 遊戲主場景 | 1,123 Bytes | ✅ 通過 |
| `game/shaders/outline.gdshader` | 角色深色厚描邊著色器 | 1,053 Bytes | ✅ 通過 |
| `game/shaders/foot_shadow.gdshader` | 獨立層落地柔化橢圓軟影著色器 | 517 Bytes | ✅ 通過 |
| `game/scripts/battle/battle_view.gd` | 戰鬥核心表現視圖邏輯 | 118,829 Bytes | ✅ 通過 |
| `game/scripts/art/sprite_db.gd` | 動態姿態與紙娃娃資產索引庫 | 34,423 Bytes | ✅ 通過 |

### 3. 實體音效清單（Procedural SFX / One-shots，實體存在）

| 檔案路徑 | 用途與聽感 | 檔案大小 | 查驗結果 |
|---|---|---|---|
| `game/assets/audio/sfx/clock.wav` | 發條齒輪咬合「喀——嗒！」（Shot 1 開場與 Shot 7 收束） | 2,690 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/slash.wav` | 長劍揮斬破空聲與爪擊撕裂聲（Shot 2、Shot 6） | 7,100 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/hit.wav` | 金屬受擊打擊與暴擊反饋聲（Shot 2、Shot 3、Shot 6） | 5,336 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/clash.wav` | 長槍兵器重擊交鋒聲「鏘啷」（Shot 3） | 6,658 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/fire.wav` | 核心爆能與法杖法術釋放聲「呼——」（Shot 4） | 15,478 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/break.wav` | 秘法爆裂與重錘砸地震裂聲（Shot 4、Shot 5） | 8,864 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/rock.wav` | 巨錘破空鈍擊重音（Shot 5） | 8,864 Bytes | ✅ 通過 |
| `game/assets/audio/sfx/wind.wav` | 靈猴彈簧手臂極速伸縮破風聲（Shot 6） | 11,068 Bytes | ✅ 通過 |

### 4. 品牌固定資產（官方字標與底板，實體存在）

| 檔案路徑 | 類型與用途 | 檔案大小 | 查驗結果 |
|---|---|---|---|
| `branding/logo_cn.png` | 官方手繪繪本風中文字標（Shot 7 點題卡後製無失真疊加） | 866,886 Bytes | ✅ 通過 |
| `branding/title_plate.png` | 官方純黑底板（Shot 7 點題卡底板） | 373,881 Bytes | ✅ 通過 |
| `branding/key_visual_main.png` | 官方主視覺基準資產（Shot 1 參考基準） | 1,735,537 Bytes | ✅ 通過 |

---

## 七、總監審核清單逐項對照（對齊 review.md）

本份腳本已完成自我審查，逐條符合 `references/review.md` 之所有紅線與標準，每項皆附客觀查證依據：

| 檢查項目 | 審查標準 | 本腳本具體落實措施與查證依據（第 19f 條） | 判定 |
|---|---|---|---|
| **第 10 條 / 第 10c 條** | **畫面真的在動** | 拒絕靜圖幻燈片。全片 7 鏡皆具備實體運鏡（Dolly In 105%～120%、Push In 110%～125%），且實機鏡次包含角色姿態切換（idle→telegraph→attack→recover/skill）與 Hitstop 縮放（`scale` 1.1 緩動回彈），動態連續，無靜止幀。 | ✅ 合格 |
| **第 11 條** | **開場三秒給懸念，不給 Logo 與遊戲名** | Shot 1（0.0～3.0s）為發條兔背後鑰匙旋轉與核心充能微距特寫，純實體咬合音效，畫面零文字、無 Logo、無遊戲名。 | ✅ 合格 |
| **第 12 條** | **鏡次接得上** | 嚴格維持接鏡動態軸線：微距光芒穿透 → 兔劍突刺金光掠過 → 獅槍突貫破風 → 狐杖法球爆裂下壓 → 豬錘破空重砸震地 → 猴爪極速連環撕裂 → 白閃切入純黑底板。 | ✅ 合格 |
| **第 13 條** | **標「不移動」的鏡次真的不走** | Shot 1 標明小白原位靜止（僅鑰匙旋轉與核心充能），Shot 7 標明純黑底板微幅緩推，無角色任意位移漂移。 | ✅ 合格 |
| **第 14 條 / 第 14a 條** | **實體音優先，嚴禁罐頭史詩管弦樂** | 全片音效 100% 由倉庫既有 Procedural SFX 實體音（`clock.wav`, `slash.wav`, `hit.wav`, `clash.wav`, `fire.wav`, `break.wav`, `rock.wav`, `wind.wav`）依時間軸對點觸發，無任何罐頭史詩 BGM。 | ✅ 合格 |
| **第 15 條** | **嚴禁承諾上架日、價格、合作** | 片尾僅呈現「開發中畫面 · 官網搶先看」，無任何「即將上市」、「免費下載」、「限定禮包」等字樣。 | ✅ 合格 |
| **第 15a 條** | **畫面無外加宣傳文字與浮水印** | Shot 2～6 遊戲實機畫面保持 100% 原始乾淨 HUD，無後加宣傳粗體字；僅 Shot 7 點題卡由後製無失真疊加官方固定字標 `branding/logo_cn.png`。 | ✅ 合格 |
| **第 16 條 / 第 19b 條** | **不暗示已完成，不拿 AI 圖冒充實機** | 概念素材（Shot 1）與品牌固定資產（Shot 7）明確標示；實機打擊（Shot 2～6）100% 錄自 Godot 戰鬥場景，真實呈現。 | ✅ 合格 |
| **第 17 條** | **切入點獨立，風格不撞車** | 本片切入點為純粹的「五大玩具族系實機戰鬥打擊手感全亮相」，與 `SHORTS_SOUL_BATTLE_POLISH_30S.md`（聚焦聚魂保底與單手操控）及 `STORYBOARD_AWAKENING.md`（品牌概念覺醒）之主題與畫面完全不同。 | ✅ 合格 |
| **第 19 條 / 第 19e 條** | **素材列出必須是已存在之合併功能** | 所列 30 個姿態檔案、場景 `battle.tscn`、`main.tscn`、著色器與音效檔案共 47 項實體資產，全數經 `ls -l` 逐條查驗存在且位在 main 分支，無任何虛構路徑。 | ✅ 合格 |
| **第 19c 條** | **不得自立片名與分歧點題** | 移除花俏宣傳片名，統一為內部企劃代號 `mk-five-races`（片內不呈現）；點題卡標明後製無失真疊加官方字標 `branding/logo_cn.png`，嚴禁 AI 生成。 | ✅ 合格 |
| **第 19f 條** | **自我檢查表每一項要有查證方式** | 每一項審核條款均附有明確查驗方式（實體檔案大小、路徑查核、邏輯腳本對齊），絕無虛假打勾。 | ✅ 合格 |
| **第 19i-4 條** | **不准描述未畫出的過程動詞** | 嚴格依據遊戲內實際可見之姿態（attack, telegraph, recover, skill）、縮放反彈（Squash & Stretch）與打擊停頓進行客觀描述，無腦補動作。 | ✅ 合格 |
| **第 22 條** | **不違背 CANON 世界憲章** | 嚴格遵守「覺醒的金屬發條玩具」世界觀：五族均為金屬/琺瑯板件玩具公仔，零毛皮、背後外露發條鑰匙、胡桃鉗色盤、齒輪部位破壞無血肉。 | ✅ 合格 |
| **第 23 條** | **名詞六語系皆可翻譯** | 涉及之種族（Rabbit, Lion, Fox, Boar, Macaque）與武器/技能名詞皆在多語系字典支援範圍內，無僅中文成立之雙關語。 | ✅ 合格 |

---

## 八、下一棒實作指引（錄影與合成人員，按部就班即可出片）

下一棒執行人員無需猜測，照以下步驟即可完成 9:16 實機短影音出片：

1. **實機素材錄製（sideworker）**：
   - 啟動既有 Godot 引擎（搭配 Xvfb 虛擬顯示器），依據第五節之 REC-01 至 REC-05 操作序列，分別錄製 5 段 1080×1920 (9:16) 實機無損影片（每段 2.50 秒）。
   - 錄製時確認 `GameState.player_race` 對應各族（`"rabbit"`, `"lion"`, `"fox"`, `"boar"`, `"macaque"`），並確保 `outline.gdshader` 與 `foot_shadow.gdshader` 正常生效。
2. **開場懸念素材準備**：
   - 依據 Shot 1 規劃，使用既有工坊微距高解析素材或使用 `gen_media.py` 生成 9:16 微距圖（需帶 `--ref branding/key_visual_main.png` 並符合 §6.5 規範），裁切為 1080×1920 配合 105% Dolly In。
3. **剪接與音效合成**：
   - 使用 ffmpeg 依據第四節時間軸（精準 18.0 秒，7 個分鏡）進行接龍拼接。
   - 匯入第六節列出之 8 支 Procedural SFX 實體音效（44100Hz AAC 立體聲），嚴格對點對齊各族揮斬、長槍破空、法術轟擊、巨錘砸地與靈猴連抓打擊點。
   - 片尾 15.5s～18.0s 疊加純黑底板 `branding/title_plate.png` 與官方字標 `branding/logo_cn.png`。
4. **輸出成品驗收**：
   - 輸出路徑建議：`web/media/shorts/mk_shorts_five_races_combat_18s.mp4`（1080×1920，30fps，精準 540 幀 / 18.00s）。
   - 依據 review.md 第 10c 條抽格比對 PSNR (<50dB)，音軌確認無罐頭管弦樂後送審。
