# W6 Short 腳本 · 齒輪過載！超速暴怒連擊（小魚 · 短影音草案）

> **Persona**：小魚 · 短影音  
> **核心信念**：前三秒決定生死，畫面自己會說話。一支只講一件事。開頭直接給結果（暴擊、過載連斬、蒸氣洩壓）。  
> **對齊進度**：對齊 `docs/marketing/SHORTS_12_WEEK.md` 第 W6 週題目「齒輪過載！超速暴怒連擊」與手遊戰鬥數值炫技核心賣點。  
> **世界觀與戰鬥機制（嚴格對齊 CANON 與 review.md）**：  
> - **暴怒狀態物理本質**：`docs/world/CANON.md` 第 184–185 條 —— 戰鬥中受擊或命中累積的「怒氣值」，機械物理上為「彈力動能儲備」。怒氣滿 100% 觸發齒輪過載（Overdrive / Gear Burst）：背部備用安全閥瞬間彈開、洩壓閥噴出白熱蒸氣、眼部寶石泛起金紅光芒，體內所有齒輪進入超轉速過載！攻速大幅拉高、金色密集暴擊跳字與高頻齒輪咬合音。  
> - **角色與武器規格**：白金兔手持單手長劍（嚴格遵守 CANON 與 review.md 武器規範：兔長劍／獅長槍／狐法杖／豬巨錘）。  
> - **敵人合規鐵則（19g-10）**：本片純文件腳本，專注於**我方主角白金兔之齒輪過載機制**（怒氣條滿額、安全閥彈開蒸氣噴發、超轉速連擊斬、密集金色暴擊數字飄字與打擊停頓）。既有素材 REC-04 錄製對象因含有不可對外之雷歐畫面，本腳本在素材引導上明確標註為**內部剪輯特寫/局部裁切參考（Crop）**，對外公開發布時嚴格遵循 0-MKT2 禁令；嚴格禁止荒路匪徒（road_bandit）與非合規敵人入鏡。  
> **製作與執行邊界**：  
> - ⚠️ **純文件規格（Documentation Only）**：只寫分鏡與素材對照文件，嚴禁產圖、產片、剪片、發文；嚴禁呼叫 Veo／fal／任何付費 API；嚴禁修改遊戲程式。  
> - ⚠️ **素材真實性**：素材來源 100% 限縮在 repo 內既有戰鬥實機資產與已合併之音效／品牌資產，嚴禁發明未錄製之虛構鏡頭。

---

## ⛔ 發布前禁令附註（review.md 0-MKT2 · 側案行銷總監）

**本分鏡包含遊戲實機戰鬥錄影與 HUD 畫面，目前一律不得對外發布。**  
Kevin 現行裁示（`t_4c1dfa0b` 決策卡選項 B）：遊戲實機截圖與錄影對外暫不公開，官網與粉專只放主視覺與官方短片，畫面過關後才解禁。  
- 本文件屬**內部素材規劃與分鏡規格**，過審不等於可對外發布。  
- **既有素材排除與隔離（19g-10）**：既有實機素材 `REC-04`（`rec04_overdrive_break_9x16.mp4`）畫面中之守衛泰坦雷歐（Leo）已被列入不可對外黑名單；未來實際對外成片錄製時，必須以合規之發條玩具敵人（如竹林道場傀儡 `bamboo_spirit` 或渣滓之狼 `wolf`）或特寫裁切白兔本體／怒氣 HUD 方式替換，嚴禁露出雷歐與荒路匪徒。  
- **解禁條件**：Kevin 明示實機畫面過關並由製作人下達錄製/剪輯任務，不得擅自發布。

---

## 一、基本資料

| 項目 | 規格標準 | 說明 |
|---|---|---|
| **週次** | W6（12 週題庫系統炫技專題） | 對齊 `docs/marketing/SHORTS_12_WEEK.md` W6 列 |
| **片名** | 《齒輪過載！超速暴怒連擊》 | 內部企劃命名，短影音成片中不放花俏宣傳片名 |
| **規格時長** | **精準 30.0 秒**（30.00s，900 幀） | 平台黃金完播區間（28–32s），直式 9:16（1080×1920，30fps） |
| **0–3s 鉤子** | **【齒輪過載，轉速拉滿！】** | 第 0 秒無片頭、無 Logo、無自我介紹，直接給怒氣安全閥彈開與金色暴擊炸裂 |
| **核心賣點** | 怒氣滿 100% 齒輪過載、攻速拉高 +25%、連續突刺揮斬、密集金色暴擊數字飄字、蒸氣洩壓 | 展現極致金屬打擊反饋與數值爽感 |
| **預期指標** | 完播率、重播率、吸引留言「這攻速太爽了吧」「齒輪音效好帶感」「這是什麼遊戲」 | 小魚 Persona 成果檢驗 |
| **建議成片路徑** | `web/media/shorts/w06_overdrive_30s.mp4` | 依循 shorts 命名規範 |

---

## 二、30 秒鏡頭分鏡與逐秒時間軸（Shot-by-Shot）

全片 6 鏡接龍（Shot 1~6），無縫銜接，嚴格對齊 30 秒通用模板與人體工學安全區（上下各留 15%，打擊焦點與字幕落於中下 1/3）。

| 鏡次與秒數 | 鏡頭與畫面要點 | 鏡頭語言與運鏡 | 聲音與音效設計（實體金屬發條音優先） | 畫面字幕（中下 1/3，粉圓體帶厚描邊） | 規定對應 repo 既有真實素材路徑 |
|---|---|---|---|---|---|
| **Shot 1<br>0.0s – 3.0s**<br>（爆發鉤子<br>Hook 3s） | **【開局過載·安全閥彈開】**<br>第 0 秒絕不黑屏、無 Logo、無自我介紹。畫面直接特寫白金兔戰鬥待機突入暴怒瞬態：下方怒氣槽瞬間衝上 100% 金紅頂峰，白兔背部黃銅發條鑰匙急轉！備用安全閥瞬間彈開，噴出濃烈白熱蒸氣，橘紅跳字「暴怒覺醒！」伴隨高光破空炸開！ | **微距特寫緩推**<br>以 115% Push In 平滑微推聚焦主角背部發條鑰匙急轉與安全閥蒸氣噴發，消除靜止幀。 | 齒輪由慢轉急狂轉蜂鳴「滋滋滋——」→ 安全閥彈脫高壓洩氣「嘶——砰！」→ 暴怒覺醒清脆音效。<br>⚠️ 前 3 秒嚴禁背景音樂，純以高反差金屬物理音直擊耳膜。 | **齒輪過載，轉速拉滿！**<br>（亮金粗字帶深藍紫厚描邊） | - `docs/marketing/shots/rec04_overdrive_break_9x16_crop.mp4`（0.0s~3.0s 過載覺醒段）<br>- `docs/marketing/shots/rec04_overdrive_break.png`<br>- `proofs/battle_hud_contrast/proof_battle_crop_rage.png` |
| **Shot 2<br>3.0s – 10.0s**<br>（機制展示<br>Setup 7s） | **【普攻蓄能·彈力動能儲備】**<br>切入手機橫屏 9:16 直式戰鬥全景視角，展示戰鬥人體工學。右手拇指熱區 `ThumbPad` 清晰可見。白金兔單手持長劍（dawn_blade）踏步揮斬，刀刀命中敵方機巧玩具，怒氣槽由 70% 伴隨每次命中節奏「鏘、鏘、鏘」迅速充能至 100%，展示「受擊與命中皆為發條上弦」的物理本質。 | **中景推進**<br>直式畫面平滑推鏡（Push In 110%），由全景逐漸聚焦至右下操作熱區與角色揮劍動態。 | 節奏明快、點踏清晰的輕快機械戰鬥打擊音，長劍出鞘破空「颼——」與清脆彈刀「鏘！」。BGM 輕微淡入（低飽和 16-bit 輕快鼓點，-18dB）。 | **受擊命中皆上弦<br>怒氣一滿，極限爆發** | - `docs/marketing/shots/rec01_thumb_pad_9x16.mp4`（普攻節奏與 ThumbPad 操作熱區）<br>- `docs/marketing/shots/rec01_thumb_pad.png`<br>- `proofs/hud_dopamine/proof_battle_hud_hotbar.png`<br>- `proofs/combat_feel/combat_10s_verified.mp4` |
| **Shot 3<br>10.0s – 18.0s**<br>（超速連擊<br>Core I 8s） | **【轉速狂飆·攻速+25%超速連斬】**<br>怒氣 100% 齒輪超轉速運轉！白兔攻速拉高 25%，展開暴風驟雨般的「連續突刺揮斬」！長劍化作殘影，精確觸發 3 次連續命中（0.08s Hitstop 打擊停頓 ＋ 受擊閃白 `_flash` ＋ 震屏 `_shake = 0.35`），刀刀卡點，節奏令人血脈賁張！ | **動感追焦運鏡**<br>隨斬擊節奏每擊施加微幅衝擊推進（Push In 120%），打擊卡點白閃轉場，展現刀刀入肉的紮實金屬打擊感。 | 密集超高轉速齒輪咬合聲「咔噠咔噠咔噠！」伴隨連續 3 聲沉重金屬斬擊破空「哈！鏘！鏘！鏘！」，打擊停頓點重音明確。 | **攻速狂飆 25%！<br>暴怒連斬，齒輪狂暴咬合** | - `docs/marketing/shots/rec04_overdrive_break_9x16.mp4`（1.5s~5.5s 連續三次斬擊高光）<br>- `game/scripts/battle/battle_view.gd`（暴擊震屏與 0.08s 停頓邏輯）<br>- `proofs/battle_breathe/proof_battle_attack_strike.png` |
| **Shot 4<br>18.0s – 25.0s**<br>（數值炫技<br>Core II 7s） | **【金色暴擊·滿屏跳字回饋】**<br>連擊命中高潮！畫面特寫暴擊數值與戰鬥日誌：滿屏金色立體大字「17 CRIT!」「17 CRIT!」「17 CRIT!」爆散飄升，戰鬥日誌多巴胺高對比即時跳行結算。敵方發條受擊震顫後仰，火花與糖果屑粒子漫天噴散，打擊反饋感拉滿！ | **數值特寫微推**<br>鏡頭聚焦於數字飄散與敵方受擊區域，緩慢推鏡 112%，展現高飽和多巴胺黃金暴擊跳字。 | 密集暴擊跳字叮噹作響「叮！叮！叮！」（金幣共鳴音）＋ 糖果屑晶瑩散落音，爽快感登頂。 | **金色暴擊連發！<br>滿屏跳字，數值拉滿** | - `docs/marketing/shots/rec04_overdrive_break_9x16.mp4`（3 次連續暴擊跳字片段）<br>- `proofs/battlelog/proof_battle_log_dopamine.png`<br>- `proofs/combat_feel/frame_c_damage_float.png` |
| **Shot 5<br>25.0s – 27.5s**<br>（收束治癒<br>Payoff 2.5s） | **【洩壓歸位·收劍待機】**<br>過載爆發結束，怒氣歸零。白金兔側身瀟灑收劍入鞘，背後安全閥閉合「喀嗒」，浮空島大廳彩色糖果星芒與金色齒輪微粒環繞綻放，切換為治癒自信的 Q 版待機呼吸姿態。 | **平滑拉回**<br>自戰鬥緊湊張力平滑淡出，銜接至大廳明亮多巴胺糖果色氛圍，展現熱血與治癒的反差萌。 | 蒸汽洩壓尾音「嘶——」→ 清脆收劍入鞘「叮！」→ 溫暖柔和的 16-bit 木管吉他尾韻。 | **給心上弦，讓世界轉動！<br>這打擊感你給幾分？** | - `web/media/hero/fb_lobby_9x16.mp4`（大廳呼吸與待機）<br>- `proofs/battle_breathe/proof_battle_idle_breathe_t0.png`<br>- `screenshots/proof_bravesoul_hero_interact.png` |
| **Shot 6<br>27.5s – 30.0s**<br>（品牌收束<br>CTA 2.5s） | **【官方字標與簡介引流】**<br>柔和白閃切入官方純黑底板（`title_plate.png`），中央後製疊加官方字標《發條之心》（`logo_cn.png`）。下方標語：「給心上弦，重新出發。」右下小白黃銅發條鑰匙剪影。底部標註：「開發中畫面 · 官網搶先看」。 | **純黑底板微推**<br>純黑底板微幅緩推 102%，官方手繪中文字標金屬邊緣一道柔和暖金反光掠過。 | 一聲清脆悠長、餘音裊裊的單聲發條齒輪咬合「喀嗒」（`clock.wav`），全片乾淨俐落收尾。 | **官網連結在簡介 · 發條之心**<br>（留言區告訴我們） | - `branding/title_plate.png`<br>- `branding/logo_cn.png`<br>- `branding/key_visual_main.png` |

---

## 三、實機素材檔案真實性清單（全部通過實體存在驗證）

本分鏡腳本所引導之所有資產，100% 存在於倉庫中，絕不使用任何未錄製或虛構檔案：

### 1. 核心實機短影音片段（9:16 直式 H.264）
- `docs/marketing/shots/rec04_overdrive_break_9x16.mp4`（402 KB，REC-04 怒氣滿額暴怒連斬實機錄影）
- `docs/marketing/shots/rec04_overdrive_break_9x16_crop.mp4`（315 KB，REC-04 特寫裁切版，聚焦怒氣與連斬）
- `docs/marketing/shots/rec04_overdrive_break.png`（1,495 KB，REC-04 實機原生截圖）
- `docs/marketing/shots/rec04_overdrive_break_9x16_thumb.png`（1,212 KB，REC-04 9:16 關鍵幀縮圖）
- `docs/marketing/shots/rec01_thumb_pad_9x16.mp4`（295 KB，REC-01 右手拇指熱區與普攻節奏實機錄影）
- `docs/marketing/shots/rec01_thumb_pad.png`（1,631 KB，REC-01 實機截圖）
- `proofs/combat_feel/combat_10s_verified.mp4`（218 KB，實機戰鬥 10 秒驗證影片）
- `web/media/hero/fb_lobby_9x16.mp4`（大廳待機與多巴胺氛圍直式片段）

### 2. 戰鬥數值、暴擊飄字與 HUD 截圖證明
- `proofs/battle_hud_contrast/proof_battle_crop_rage.png`（20 KB，怒氣槽高對比度實機裁切圖）
- `proofs/hud_dopamine/proof_battle_hud_hotbar.png`（1.4 MB，多巴胺操作熱區實機截圖）
- `proofs/battle_breathe/proof_battle_attack_strike.png`（1.2 MB，斬擊命中高光瞬間）
- `proofs/battlelog/proof_battle_log_dopamine.png`（1.4 MB，戰鬥日誌多巴胺高對比跳字截圖）
- `proofs/combat_feel/frame_c_damage_float.png`（傷害浮動與暴擊飄字原生幀）
- `proofs/battle_breathe/proof_battle_idle_breathe_t0.png`（白金兔戰鬥待機呼吸姿態）
- `screenshots/proof_bravesoul_hero_interact.png`（414 KB，大廳主角戳碰星芒與揮劍姿態）

### 3. 官方品牌與片尾點題資產
- `branding/title_plate.png`（373 KB，官方純黑底板）
- `branding/logo_cn.png`（866 KB，官方手繪中文字標）
- `branding/key_visual_main.png`（1.8 MB，官方主視覺標準圖）

### 4. 戰鬥系統底層實作依據（GDScript）
- `game/scenes/battle/battle.tscn`（實機戰鬥主場景）
- `game/scripts/battle/battle_view.gd`（第 2571–2574 行：`is_crit` 觸發 `_shake = 0.35` 震屏與 `trigger_hit_stop(0.08)` 打擊停頓）
- `game/scripts/battle/battle_sim.gd`（第 12 行：`RAGE_MAX := 100.0`；第 534/593 行：普攻與連擊累積怒氣邏輯）
- `game/scripts/dev/capture_rec04_break.gd`（REC-04 錄製驅動腳本：怒氣 100%、`trigger_fury_awakening` 與三次連斬）

---

## 四、合規紅線與禁入畫面清單（review.md 嚴格查驗）

剪輯與素材選用時，嚴格遵守以下禁令，違者一律退單：

1. ⛔ **不可對外敵人絕對禁令（19g-10 條）**：
   - **雷歐（Leo）**：已被列入不可對外黑名單（穿重甲之毛皮獅獸人，違反 CANON 零毛皮鐵則）。`REC-04` 錄影中雷歐若入鏡，**剪輯時必須嚴格裁切（Crop）僅保留我方白金兔攻擊動作、發條鑰匙、安全閥蒸氣與怒氣/暴擊 HUD**，嚴禁露出雷歐面部、鬃毛或身軀！
   - **荒路匪徒（road_bandit）**：舊版實機錄影多為人類盜匪，未重錄前**嚴禁任何含荒路匪徒之實機片段入鏡**。
2. ⛔ **零毛皮鐵則（CANON）**：
   - 畫面中所有角色必須為金屬板件、琺瑯烤漆公仔，關節帶有球形軸承與沉頭螺栓，背部外露黃銅發條鑰匙。嚴禁任何毛髮、生物皮膚或血肉。
3. ⛔ **0-MKT2 實機截圖/錄影對外禁令**：
   - 本腳本為內部剪輯與錄製規劃規格。成片未經 Kevin 裁示畫面解禁前，**嚴禁發布至 Facebook、YouTube 或任何公開頻道**。
4. ⛔ **杜絕 AI 生成假實機**：
   - 嚴禁使用 Veo、fal.ai 或任何文字生成影片工具冒充實機。所有戰鬥畫面必須 100% 來自 Godot 引擎錄製產出。
5. ⛔ **誠實文案與零承諾（第 15/16 條）**：
   - 文案內絕不提及上架日期、價格、營收或未開放之合作；不放未上架之 App Store / Google Play 下載按鈕；片尾僅標註「開發中畫面 · 官網搶先看」。

---

## 五、剪輯與音訊組裝指引（剪映／Premiere 執行貼上）

1. **畫幅與幀率**：統一 9:16（1080×1920），30fps，主要打擊點、數值跳字與字幕置於中央 70% 舒適安全區內。
2. **前 3 秒節奏卡點**：第 0.0 秒蒸氣噴發，第 1.0 秒卡點「暴怒覺醒！」橘紅跳字，第 2.0 秒展開連斬，節奏緊湊不拖沓。
3. **打擊反饋加強**：每次斬擊命中（10.0s~18.0s）配合遊戲原生 Hitstop 停頓，畫面切換 2~4 幀白閃（Flash White），強調金屬撞擊感。
4. **音訊分軌建議**：
   - **語音/口播**：無口播（純字幕視覺流），讓觀眾專注享受金屬打擊音。
   - **音效軌（SFX，-6dB）**：高壓蒸氣噴發、發條高速急轉蜂鳴、金屬斬擊碰撞、暴擊金幣跳字清脆音、片尾發條喀嗒單音。
   - **背景音樂軌（BGM，-18dB）**：輕快低飽和 16-bit 童話戰鬥旋律，第 0–3 秒淡出靜音，第 3 秒中景普攻起微弱淡入，不搶金屬實體音。

---

## 六、社群貼文文案備份（解禁後 YouTube Shorts / FB Reels 用）

> ⚠️ 依 0-MKT2 禁令，本則貼文需待實機畫面解禁後方可排程發布。

```
齒輪過載，轉速拉滿！這才是玩具世界的狂暴連擊 🔥

誰說發條玩具只能慢吞吞？
怒氣滿 100%，背部安全閥瞬間彈開！
高壓蒸氣洩壓、攻速狂飆 25%，
白金兔超轉速暴怒連斬，金色暴擊滿屏狂跳！

⚡ 戰鬥核心亮點：
・受擊命中皆上弦，彈力動能極限儲備
・安全閥高壓洩氣，體內齒輪超轉速運轉
・純手勢直覺開打，刀刀有停頓、刀刀有回饋！

這暴怒連斬打擊感，你給幾分？留言區告訴我們👇

🐇 發條之心 Clockwork Heart
發條玩具冒險手遊 · 四大職業 · 器／魂／招

▶️ 官網：https://KevinChu1110.github.io/clockwork-heart/
⬇️ 下載：https://KevinChu1110.github.io/clockwork-heart/pages/download.html

#發條之心 #ClockworkHeart #手遊推薦 #發條玩具 #動作手遊 #打擊感 #Shorts #YouTubeShorts #Reels
```
