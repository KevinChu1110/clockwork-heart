# 第二十四種動物「鐵拳袋鼠（The Boxer Kangaroo）」世界觀與角色設計提案

> **文件狀態**：世界觀擴充提案與角色規格書（Expansion World & Chassis Proposal - Ready for Review）  
> **制定日期**：2026-09-28  
> **負責人**：側案·策劃總監 小凱（sideplan）  
> **審核對象**：側案製作人 老周（side） / 側案美術總監 小柔（sideart） / 側案程式 阿宏（sideworker）  
> **對應看板任務**：`t_ebe16a1f`（📖 世界觀｜第二十四種動物紙娃娃角色設計提案（只寫文件，不產圖不產片））  
> **關聯歸檔文件**：  
> - [`docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../design/BOXER_KANGAROO_DESIGN_PROPOSAL.md)  
> - [`docs/world/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../world/BOXER_KANGAROO_DESIGN_PROPOSAL.md)  
> - [`docs/art/BOXER_KANGAROO_DESIGN_PROPOSAL.md`](../art/BOXER_KANGAROO_DESIGN_PROPOSAL.md)  
> **關聯依據文件**：  
> - `docs/world/regions/R04_BRASS_METROPOLIS.md`（第 1 行區域代號與名稱「R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City」、第 4 行「沖壓厚鑄黃銅板、冷軋鎢鋼外齒輪、耐熱微型蒸氣管網與高壓鎢絲指針儀表套件」、第 16 行「外嚙合減速齒輪環軌與重型蒸氣排風槽」、第 20 行「防滑菱形斜紋沖壓黃銅地磚 Checkerplate Brass Tile」、第 21 行「摩天齒輪工坊群 Great Cog Skyspires」、第 22 行「高壓蒸氣管道網 High-Pressure Steam Conduits」、第 31 行「晨曦天軌 4 號工業月台」、第 44 行「鐵皮發條工程師 Tinplate Clockwork Engineers」、第 48 行「中央蒸氣沐浴池 Central Degreasing Bath」、第 103 行城防泰坦「巨輪霸主」、第 163 行「中央動力廣場 Central Power Plaza」、第 238 行「黃銅都市·巨輪城」、第 239 行地標「摩天齒輪工坊群」、第 240 行地標「中央動力廣場」、第 241 行「高架重軌引橋·巨輪城站」、第 242 行「深淵排污豎井管道」、第 256 行代表素材「高精鎢鋼齒輪」、第 257 行代表素材「耐熱高壓蒸氣閥」、第 258 行代表素材「合金軸承鉚釘」、第 259 行代表素材「重鍛黃銅板」、第 260 行核心星軸「武曲星軸 Wu Qu Core」、第 261 行核心星軸「破軍星軸 Po Jun Core」、第 264 行核心機制「過熱洩壓排氣窗口 Overheat Steam Vent Window」與第 265 行「蒸氣噴流浮跳」）  
> - `docs/design/paperdoll_slots.json` / `docs/design/PAPERDOLL_SLOTS_SPEC.md`（7 大部件槽位架構）  
> - `game/data/tables/weapon_classes.json`（6 職業 12 大武器系統，武術家·拳 `fist` 體系）  
> - `game/data/tables/equipment.json`（既有拳武器 ID：第 210 行 `wrap_gloves` 練拳綁帶、第 223 行 `iron_knuckle` 鐵節拳套）  
> - `docs/world/CANON.md`（世界憲章：100% 零毛皮零軟組織、沖壓耐磨黃銅合金板件/全金屬與齒輪咬合發條玩具、背後必有發條鑰匙）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `docs/BALANCE.md`（§5 時間模型 0.15 鎖版規範）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：24 族大圓滿完全閉環**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）在第二十三族琉璃海馬圓滿補足法師水晶武器後，依循標準流程制定之**第二十四種動物擴充素體規格**。  
   本提案宣告《發條之心》創角動物體系正式達成**六大職業 × 四大種族 = 二十四族完全對稱大圓滿陣容（6 職業 × 4 族 = 24 族，12 種武器每種精確對應 2 族）**！  
   本提案**精準補足全遊戲武術家職業下轄「拳（`fist`）」體系自創角以來僅有第 13 族瓷韻熊貓單一素體的最後缺口**，使武術家職業（猴·爪、穿山甲·爪、熊貓·拳、袋鼠·拳）達成「爪 2 族、拳 2 族」的完全對稱平衡，並使戰士（4）、遊俠（4）、忍者（4）、騎士（4）、法師（4）、武術家（4）六大職業全數圓滿閉環！
2. **經典玩具起源與古典機械發條拳擊袋鼠工藝**：  
   - 本提案選定全球古典機械玩具史與鐵皮發條動作玩具之世界級經典——**「19世紀末至20世紀初古典鐵皮發條拳擊袋鼠玩偶（Vintage Tinplate Wind-up Boxing Kangaroo Automaton）」**（承接 `docs/world/regions/R04_BRASS_METROPOLIS.md` 第 1 行、第 4 行「沖壓厚鑄黃銅板、冷軋鎢鋼外齒輪、耐熱微型蒸氣管網」、第 20 行「防滑菱形斜紋沖壓黃銅地磚」、第 21 行「摩天齒輪工坊群」、第 44 行「鐵皮發條工程師」、第 163 行「中央動力廣場」、第 240 行「中央動力廣場」、第 257 行「耐熱高壓蒸氣閥」與第 264 行「過熱洩壓排氣窗口」之重工沖壓、氣壓活塞衝擊與發條彈簧儲能工藝）；  
   - 作為全遊戲 24 大種族中**首款也是唯一具備「氣動活塞衝壓雙拳套、前置沖壓黃銅齒輪置物前袋、冷軋鎢鋼雙螺旋減震彈簧後腿、分節黃銅重力平衡擺動長尾與沖壓雙環冠軍黃銅發條鑰匙」的拳擊機械素體（Piston Stamping Knuckles, Front Gear Pouch, Twin Helical Tungsten Spring Legs, Segmented Counterweight Pendulum Tail & Champion Double-Ring Brass Key）**。在幾何剪影（挺拔 2.2 頭身西洋拳擊起手架式、輕盈彈跳步法、後傾重力平衡尾）、材質語彙（焦糖暖褐赤銅板件、冠軍胡桃鉗朱紅拳套、溫潤奶油米白前胸腹袋、鎢鋼深灰減震彈簧）與戰鬥手感（快節奏貼身刺拳穿透、氣壓活塞洩壓爆發、破勢寸勁連打）上，與前二十三族形成 100% 徹底差異化。
3. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
4. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：鐵拳袋鼠素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。  
   - **武器與職業對齊**：精準收斂至既有 6 職業 12 大武器體系中之 `monk`（武術家）下轄之 **`fist`（拳 / 武鬥·拳）** 系統，以【氣壓活塞雙拳套 / 衝壓黃銅拳套（Pneumatic Piston Knuckles / Brass Stamping Cestus）】呈現。補足前二十三族中拳套武器僅有第 13 族瓷韻熊貓單一素體的缺口，使全遊戲 12 大武器全面達成每種武器精確對應 2 種動物素體之終極對稱！

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有二十三族武器與職業光譜全盤點

盤點現有首發五族與前十八款擴充族的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

- **白金兔（Clockwork Rabbit）**：騎士 (Knight) —— 單手長劍（`sword`），平衡攻防，中近距離。
- **烈鬃獅（Gilded Lion）**：騎士 (Knight) —— 皇家長槍（`spear`），中距控場，格擋迎擊。
- **靈尾狐（Astral Fox）**：法師 (Mage) —— 秘術法杖（`magic`），遠程法術，技能爆發。
- **鋼牙豕（Forge Boar）**：戰士 (Viking) —— 鍛爐巨鎚（`hammer`），高防厚重，部位破壞。
- **靈爪猴（Spring Macaque）**：武術家 (Monk) —— 機關靈爪（`claw`），彈簧伸縮臂，近身連打破勢。
- **烈焰虎（Ember Tiger）**：忍者 (Ninja) —— 齒輪雙斬刃（`dagger`），伏擊撕裂，近戰極限暴擊。
- **雲嵐鶴（Cloud Crane）**：遊俠 (Ranger) —— 風弦羽翼機關弓（`bow`），超視距狙擊，遠程精準破甲。
- **玄軸熊（Iron Bear）**：戰士 (Viking) —— 玄軸偏心重力錘（`hammer` 變體），磐石壁壘，大範圍震波。
- **蒸氣企鵝（Steam Penguin）**：遊俠 (Ranger) —— 蒸氣雙管導航火槍（`gun`），直線高壓蒸氣爆發，精準點射。
- **玄機龜（Xuanji Tortoise）**：法師 (Mage) —— 玄機八卦發條星盤 / 磐甲浮空護體靈晶（`crystal`），護盾織刃，高防反震。
- **鋼岳象（Colossus Elephant）**：戰士 (Viking) —— 巨輪開山重斧（`axe`），質量重力斬劈，單發物理最高傷害。
- **碧簧蛙（Spring-Leg Frog）**：忍者 (Ninja) —— 碧葉旋刃機關鏢（`dart`），高速牽制，多段飛鏢射殺。
- **瓷韻熊貓（Porcelain Panda）**：武術家 (Monk) —— 乾坤太極機關拳套（`fist`），貼身寸勁連打破勢，動靜化勁。
- **翠角鹿（Emerald Fawn）**：遊俠 (Ranger) —— 翠木角尺複合機關弓（`bow`），停拍看破，機動連發射擊。
- **星軌犬（Orbit Hound）**：騎士 (Knight) —— 星軌雷達天線槍 / 光子信標穿刺長槍（`spear`），中距失重滑行，磁軌迎擊控場。
- **靈鐘鴞（The Chrono Owl）**：法師 (Mage) —— 渾天星儀擒縱法杖（`magic`），遠距天文彈道，延遲擒縱法陣。
- **幽影貓（The Umbral Cat）**：忍者 (Ninja) —— 暗影發條袖刃 / 匿夜弧光短匕（`dagger`），極致靜音影遁，弱點死線背刺。
- **沙鱗穿山甲（The Dune Pangolin）**：武術家 (Monk) —— 渦輪掘進破甲機關爪（`claw`），重裝下潛破勢，鋼鱗反震。
- **浪花海獺（The Tidal Otter）**：戰士 (Viking) —— 海錨防禦重斧 / 琉璃破障重斧（`axe`），洋流阻尼蓄力，浮力下墜破障。
- **星巡浣熊（The Orbit Raccoon）**：遊俠 (Ranger) —— 反重力脈衝光銃 / 軌道聚焦發條銃（`gun`），失重滑行點射，電離脈衝過載。
- **棘輪刺蝟（The Ratchet Hedgehog）**：忍者 (Ninja) —— 棘輪穿針機關鏢 / 巡影飛棘（`dart`），引線折返連刺，天機千針暴風。
- **荒原鋼狼（The Scrap Wolf）**：騎士 (Knight) —— 廢土鋸齒重鋼劍 / 破軍殘刃（`sword`），鋸齒斷刃重斬，生鏽散熱窗口暴擊。
- **琉璃海馬（The Crystal Seahorse）**：法師 (Mage) —— 深海靈晶浮空星盤 / 琉璃棱鏡核心（`crystal`），洋流阻尼懸停，藍晶透鏡聚焦射擊。

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業（`knight`、`viking`、`ninja`、`monk`、`mage`、`ranger`）中：
- 戰士（Viking）已達 4 族（鎚 2、斧 2），達成圓滿對等；
- 遊俠（Ranger）已達 4 族（弓 2、銃 2），達成圓滿對等；
- 忍者（Ninja）已達 4 族（匕 2、鏢 2），達成圓滿對等；
- 騎士（Knight）已達 4 族（劍 2、槍 2），達成圓滿對等；
- 法師（Mage）已達 4 族（杖 2、晶 2），達成圓滿對等；
- **武術家（Monk）目前為 3 族（爪 2、拳 1），其中下轄的機關拳套武器（`fist`）自第十三族瓷韻熊貓以來，是全遊戲唯一尚存「單一素體」之缺口！**

第二十四種動物鐵拳袋鼠正式選定掛載於 **`monk`（武術家）** 職業體系，原生武器對齊 **`fist`（拳 / 武鬥·拳）**。依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`武術家 (Monk)`**。  
此舉標誌著 24 族矩陣全面封頂，使武術家達成「爪 2 族、拳 2 族」之完美對稱，全遊戲 6 大職業、12 種武器體系達到終極平衡！

### 1.2 鐵拳袋鼠武器選擇：【氣壓活塞雙拳套 / 衝壓黃銅拳套（Pneumatic Piston Knuckles / Brass Stamping Cestus）】

鐵拳袋鼠原生專屬武器定名為：**【氣壓活塞雙拳套 / 衝壓黃銅拳套（Pneumatic Piston Knuckles / Brass Stamping Cestus）】**。  
該武器底層完全掛載於 `weapon_classes.json` 的 `fist`（武鬥·拳）類別，享有 `fist` 既有的「破勢在勤」標籤宣言（Tagline: `\"破勢在勤\"`）、出手快、架勢散得快、對付木人樁破勢順暢之特性（`atk: 1, def: 1, hp: 4, crit: 1.5, speed: 2`），完美呼應 `R04_BRASS_METROPOLIS.md` 第 4 行「沖壓厚鑄黃銅板、冷軋鎢鋼外齒輪」、第 240 行「中央動力廣場」、第 257 行「耐熱高壓蒸氣閥」、第 260 行「武曲星軸（破甲連擊）」與第 264 行「過熱洩壓排氣窗口」之工業活塞高壓衝壓世界觀！

- **既有武器 ID 對齊（嚴格遵守規範）**：
  - 基礎入門與進階相容武器 ID：完全對齊 `game/data/tables/equipment.json` 第 210 行既有 ID **`wrap_gloves`（練拳綁帶）**（tier 1，line: \"fist\"，`atk: 6, def: 1, hp: 4, crit: 3, crit_dmg: 8`），進階武器對齊第 223 行既有 ID **`iron_knuckle`（鐵節拳套）**（tier 3，line: \"fist\"，`atk: 12, def: 2, hp: 8, crit: 5, crit_dmg: 14`）；
  - 專屬外觀款式 ID：明確標註為待審核專屬外觀款式 `weapon_kangaroo_piston_brass_knuckle`（待審核，底層 100% 繼承既有 line: \"fist\"，數值直接掛載 `wrap_gloves` / `iron_knuckle`，絕不自行創造未定義之程式數值 id）。
- **單持規範遵守**：遵循 `review.md 0-MKT7` 單持規範，右手單戴重裝衝壓黃銅機關拳套（拳面配備雙聯氣動活塞衝頭與黃銅鉚接指節護板），置於胸前作攻擊準備；左手平曲護胸抱拳蓄勁，維持身法平衡；全圖精確為 1 組武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。

### 1.3 差異化定位：與瓷韻熊貓（乾坤太極機關拳套）及其他 22 族絕不撞型之論證

雖然鐵拳袋鼠與瓷韻熊貓同屬 `monk`（武術家）拳套（`fist`）體系，但在**戰鬥型態與身法節奏**、**力學核心與動態性格**以及**機械構造與材質語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機小螢幕上於 0.5 秒內清晰辨識：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   武術家職業拳套武器差異化對照表（瓷韻熊貓 vs 鐵拳袋鼠）               │
├───────────────────┬──────────────────────────┬──────────────────────────┤
│ 維度              │ 瓷韻熊貓（Porcelain Panda）│ 鐵拳袋鼠（The Boxer Kangaroo）   │
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ① 職業與武器     │ 武術家 (Monk)            │ 武術家 (Monk)            │
│                   │ 乾坤太極機關拳套(`fist`) │ 氣壓活塞衝壓拳套(`fist`) │
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ② 身法與戰鬥節奏 │ 沉穩內家拳法、太極化勁、 │ 西洋經典拳擊步法、輕快彈跳│
│                   │ 蓄勢寸勁爆發、動靜相生   │ 高頻刺拳直拳、活塞洩壓重拳│
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ③ 材質語彙與結構 │ 羊脂白瓷冰裂釉、玄墨黑生漆│ 焦糖暖褐赤銅板、胡桃鉗朱紅│
│                   │ 圓球耳罩、太極重力平衡陀 │ 沖壓前袋、雙螺旋鎢鋼彈簧腿│
│                   │ 圓形球窩尾、如意發條匙   │ 分節平衡重錘尾、雙環冠軍匙│
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ④ 所屬界域       │ R09 竹影道場·天元竹林    │ R04 黃銅都市·巨輪城      │
└───────────────────┴──────────────────────────┴──────────────────────────┘
```

1. **打擊型態差異（內家太極化勁 vs 外家高頻節奏拳擊）**：
   - **瓷韻熊貓（熊貓·拳）**：定位為「東方內家武道大師」。步法沉穩黏滯，重視以柔克剛與寸勁化勁，透過原地蓄勁引爆太極震波，核心手感在於「化勁防禦、蓄力寸勁」。
   - **鐵拳袋鼠（袋鼠·拳）**：全 24 族中唯一的**「西洋發條拳擊家（Steampunk Prize Fighter）」**。依託雙螺旋彈簧後腿進行連續「左右微幅彈跳（Bob and Weave）」；出招時以極高頻率打出節奏明快的刺拳（Jab）、擺拳（Hook）與過載升龍重拳（Piston Uppercut），伴隨活塞往復抽送與清脆排氣，給予玩家極致暢快的連擊回饋。
2. **力學核心與動態性格（太極雙魚陀螺儀 vs 雙聯氣動活塞與減震彈簧）**：
   - 瓷韻熊貓的動能源自胸膛內部的「太極雙魚重力平衡陀」，靜如處子，動如雷霆，展現東方禪意。
   - 鐵拳袋鼠的動能則源自胸腹部的「高壓蒸氣緩衝氣室」與後腿的「大直徑雙螺旋錳鋼彈簧」，待機時隨時處於躍躍欲試的微幅點地彈跳姿態，充滿 1920 年代發條鐵皮拳擊玩具的熱血、淘氣與充沛動能。
3. **幾何剪影與材質語彙（圓滾敦實半球 vs 上輕下重梨形挺拔彈跳）**：
   - 在 128×128 與 400×840 畫布上，瓷韻熊貓呈現圓滾滾的雙色拼裝球體輪廓與短小四肢；
   - 鐵拳袋鼠呈現鮮明的「挺拔梨形拳擊身軀」：頭頂雙豎立流線型長耳（內置排氣狹縫）、胸前標誌性的沖壓黃銅齒輪置物前袋（Pouch）、下肢粗壯的雙螺旋外露彈簧腿、後方延伸出具有弧形重錘配重塊的分節平衡長尾，剪影在 0.5 秒內具有 100% 絕對唯一性。

---

## 二、 外觀定調與機械美學（Aesthetic & Mechanical Canon）

### 2.1 零毛皮玩具世界憲章對齊（CANON.md Compliance）

依據《發條之心世界憲章》（`docs/world/CANON.md`）第一級根本大法，鐵拳袋鼠的造型設計**100% 徹底清除任何有機生物體特徵**：
- ⛔ **嚴禁生物皮毛、真皮肉質、生肉育兒袋、生物肌腱與肉球腳掌**；
- 100% 轉譯為：
  - **沖壓厚鑄耐磨焦糖暖褐赤銅裝甲板**（Stamped Heavy Caramel Bronze Plates）；
  - **溫潤奶油米白琺瑯烤漆腹袋外殼**（Creamy Ivory Enamel Pouch Shell）；
  - **多巴胺冠軍胡桃鉗朱紅拳套裝甲**（Prize Fighter Crimson Knuckle Armor）；
  - **冷軋鎢鋼雙螺旋減震高彈彈簧後腿**（Cold-Rolled Tungsten Helical Spring Legs）；
  - **分節式黃銅骨架配重擺動長尾**（Segmented Brass Counterweight Balance Tail）；
  - **雙聯琥珀光學儀表指針目鏡**（Twin Amber Vacuum Gauge Optical Dial Eyes）；
  - **外露耐高壓平頭黃銅螺栓與鍍鎳固定圓鉚釘**。

### 2.2 色彩配置與多巴胺色盤（Dopamine Palette & Brass Metropolis Harmony）

嚴格遵循《塔塔冒險隊》與《楓之谷》多巴胺鮮亮高飽和色盤規範，對齊巨輪城暖金工業童話氛圍，杜絕暗黑冰冷廢土或髒泥土黑灰：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        鐵拳袋鼠官方標準多巴胺配色體系                                  │
├─────────────────┬───────────┬──────────────────────────────────────────────────────────┤
│ 配色部位        │ 色碼 (HEX)│ 材質語言與視覺心理感受                                   │
├─────────────────┼───────────┼──────────────────────────────────────────────────────────┤
│ ① 主色：焦糖暖褐│ #C86D20   │ 沖壓厚鑄暖銅拋光烤漆，飽滿溫暖之古典金屬質感              │
│ ② 輔色：冠軍朱紅│ #E63946   │ 拳套衝壓裝甲與肩甲滾邊，多巴胺熱力火紅，視覺焦點極致鮮明  │
│ ③ 面甲：奶油米白│ #FFFDF8   │ 腹部置物齒輪袋與下顎面頰，溫潤奶油米白，營造親切反差萌    │
│ ④ 點綴：金黃黃銅│ #FFD028   │ 雙環冠軍發條鑰匙、前袋沖壓齒輪徽飾、拳套鉚釘，燦爛奪目    │
│ ⑤ 點綴：暖橘管線│ #FFA010   │ 蒸氣導熱導管、壓力指針刻度，展現巨輪城高壓做功能量        │
│ ⑥ 晶核：琥珀金目│ #FF9F1C   │ 雙眼儀表目鏡與胸口發條之心，溫暖澄澈之琥珀光學鏡片        │
│ ⑦ 結構：冷軋鎢鋼│ #4A5568   │ 雙腿減震螺旋彈簧、關節鉸鏈、尾部配重塊，結構紮實工業風    │
│ ⑧ 輪廓：深藍紫框│ #1F1A3A   │ 全身 2px 實體厚描邊，深藍紫取代純黑，畫面乾淨通透不髒      │
└─────────────────┴───────────┴──────────────────────────────────────────────────────────┘
```

### 2.3 發條鑰匙定位與幾何結構（The Winding Key）

- **鑰匙造型**：**【沖壓黃銅雙環冠軍發條鑰匙（Championship Double-Ring Brass Key）】**。  
  主體為沖壓高亮拋光黃銅（#FFD028），外型呈現復古冠軍腰帶雙環獎章輪廓，中央雕刻有雙咬合微型齒輪浮雕，兩側手柄為圓滑加厚環形拉手。
- **插座位置**：精準位於袋鼠**背部肩胛骨中央動力齒輪箱軸心**（胸椎第 2 節動力艙後側），高於尾部根部 32px，完全避開擺動長尾與後腿跳躍軌跡。
- **力學律動與音效**：發條每順時針旋轉一圈，伴隨沉穩鏗鏘的「鏘——哧！」金屬棘輪卡榫咬合與微型排氣閥洩壓聲，象徵高壓蒸氣與發條複合動能充滿。

### 2.4 機械細節與人體工學（Chibi Ergonomics）

- **2.2 頭身 Q 版黃金比例**：頭部高 46px（含豎立長耳），軀幹長 38px，下半身彈簧腿與足部高 44px，整體站姿高度嚴格對齊既有 128×128 畫布規範。
- **耳部天線與長吻特徵**：頭頂裝配雙聯沖壓薄銅長耳，耳背設有縱向蒸氣排氣細縫，在出拳時會隨氣壓洩放微幅前後擺動；面部為流線型金屬面甲，鼻尖為一枚精緻的圓形防撞黃銅鉚釘，神態專注自信、躍躍欲試。
- **前置沖壓齒輪袋（The Clockwork Pouch）**：胸腹前側裝配由溫潤奶油米白琺瑯沖壓成型的半圓形「齒輪電容置物袋」，袋口邊緣飾有拋光黃銅卡扣，袋內整齊插放著備用發條小銷釘與微型潤滑油壺，完全符合「非生物肉體育兒袋、純機械工具包」之世界觀定義。
- **接地平衡與螺旋足底**：下肢為兩組外露的冷軋鎢鋼大直徑螺旋減震彈簧，足底為防滑菱形斜紋鎢鋼掌板，下方配置兩組高耐磨防震橡膠襯墊；後方延伸出由四節黃銅套管鉸鏈組成的長尾，尾端帶有一枚重達 1.5 公斤的圓柱形鑄鐵配重塊，確保在高速連續跳躍衝拳時重心極致穩固。

---

## 三、 7 大紙娃娃外觀槽位規劃（Paperdoll Slots Architecture）

嚴格依據 `docs/design/paperdoll_slots.json` 與 `PAPERDOLL_SLOTS_SPEC.md` 所規範之 7 大標準圖層，鐵拳袋鼠擴充資產規劃如下：

### 3.1 槽位分層與渲染管線（Z-Order Alignment）

```
[Layer Z: 05] winding_key : 沖壓黃銅雙環冠軍發條鑰匙（背部最底層插座）
[Layer Z: 10] chassis     : 鐵拳袋鼠原廠焦糖暖褐赤銅素體（含螺旋彈簧腿、平衡尾與接地軟陰影）
[Layer Z: 15] costume     : 巨輪城工匠拳王加固背帶皮甲（奶油米白腹袋與護胸皮帶）
[Layer Z: 20] head_unit   : 蒸氣拳擊長耳護額頭盔（鏤空雙眼窩）
[Layer Z: 25] optic_core  : 雙聯琥珀光學儀表目鏡＋胸口發條之心金黃晶石（accessory）
[Layer Z: 30] weapon      : 氣壓活塞衝壓黃銅拳套（右手單持重裝）
[Layer Z: 35] curio       : 雙聯微型高壓蒸氣散熱背包（back_curio 背部最外層動態飾品）
```

### 3.2 七大槽位細節拆解

#### Slot 1：chassis（軀體外殼與塗裝，Layer Z=10）
- **資產 ID**：`chassis_kangaroo_caramel_bronze_default`
- **外觀特徵**：2.2 頭身袋鼠造型金屬骨架。通體噴塗高光多巴胺焦糖暖褐赤銅烤漆（#C86D20），胸腹部帶有鍍黃銅加強桁架。後腿為兩組粗壯的冷軋鎢鋼螺旋壓縮彈簧（#4A5568），尾部為四節鉸鏈連接的平衡長尾，足底包含 48×18px 橢圓形柔和投影軟陰影（接地點 x=64, y=120）。
- **規範檢查**：100% 裸機素體，武器區域（右側）0 像素殘留，眼窩完全鏤空，嚴禁畫死任何衣服或武器。

#### Slot 2：head_unit（頭部與面甲，Layer Z=20）
- **資產 ID**：`head_kangaroo_steampunk_boxer_visor`
- **外觀特徵**：沖壓耐磨黃銅拳擊護額頭盔。額頭上方配備一條加厚防撞鎢鋼護額，兩側為聳立的雙聯沖壓薄銅長耳（耳背帶有 3 條微型排氣散熱狹縫）；下顎為奶油米白烤漆面頰板，外露兩顆圓頭定位螺栓。
- **眼窩規範**：雙眼窩尺寸為精確 12×12px 鏤空透空區，透空度 100%，絕不殘留任何眼珠底色，供 `optic_core` 自由換裝。

#### Slot 3：costume（服裝與甲冑，Layer Z=15）
- **資產 ID**：`costume_kangaroo_champion_belt_harness`
- **外觀特徵**：巨輪城工匠拳王加固背帶與沖壓前袋。腹部為半圓形奶油米白琺瑯沖壓齒輪袋（#FFFDF8），袋口飾有金黃卡扣；肩部與腰間穿套加固棕褐皮帶與胡桃鉗朱紅滾邊（#E63946），胸前裝配一枚微型黃銅蒸氣壓力表。
- **晶石孔規範**：胸口正中央嚴格預留直徑 14px 的晶石展示圓孔，絕不遮擋 `optic_core` 之發條之心晶石。

#### Slot 4：optic_core（目鏡與晶核 / accessory，Layer Z=25）
- **資產 ID**：`optic_kangaroo_amber_dial_core`
- **外觀特徵**：
  - **眼部透鏡**：雙聯直徑 8px 的琥珀晶亮光學目鏡（#FF9F1C），鏡片內部刻有同心圓十字校準刻度，高光點為純白（#FFFFFF）位於左上方，散發出無所畏懼的熱血拳手神采；
  - **發條之心晶核**：位於胸口正中央，為一顆多面切割的菱形金黃晶石（#FFD028），外圍環繞微型紫銅散熱圈，隨呼吸節奏微幅發出多巴胺暖光脈動。

#### Slot 5：winding_key（發條鑰匙，Layer Z=05）
- **資產 ID**：`key_kangaroo_champion_double_ring`
- **外觀特徵**：沖壓黃銅雙環冠軍鑰匙。整體寬 38px、高 32px，由高亮拋光黃銅打造，中央雕刻雙齒輪咬合徽標，兩側為優雅對稱的加厚拉環，旋轉時具有清晰的金屬反光。
- **通用目錄同步**：產出時同步鏡像輸出至 `game/assets/sprites/player/paperdoll/key/key_kangaroo_champion_double_ring.png`。

#### Slot 6：weapon（手持武器，Layer Z=30）
- **資產 ID**：`weapon_kangaroo_piston_brass_knuckle`
- **外觀特徵**：氣壓活塞衝壓黃銅拳套。單手持握規範，右手單戴。由多巴胺胡桃鉗朱紅（#E63946）加厚沖壓鋼殼打造，拳峰嵌有兩枚高壓滑動鎢鋼衝頭，腕部帶有小型黃銅蓄氣筒與洩壓排氣管。
- **通用目錄同步**：產出時同步鏡像輸出至 `game/assets/sprites/player/paperdoll/weapon/weapon_kangaroo_piston_brass_knuckle.png`。

#### Slot 7：curio（背部飾品 / back_curio，Layer Z=35）
- **資產 ID**：`curio_kangaroo_steam_exhaust_backpack`
- **外觀特徵**：雙聯微型高壓蒸氣散熱背包。安裝於背部兩側，由一對傾斜向上的黃銅短煙囪與微型調壓閥組成。待機時每隔 2 秒噴出一縷小巧柔和的白色甜味蒸氣圈，奔跑與跳躍時帶有淡淡的金色蒸氣微粒尾跡。

---

## 四、 六大戰鬥動作姿態規格（Six Core Battle Poses）

嚴格依據既有 6 動作姿態體系（128×128 與 512×512 雙規格），拆解鐵拳袋鼠之動態表演：

### 4.1 六姿態招式意象拆解

1. **`idle`（戰鬥待機）**：
   - 2.2 頭身袋鼠身體重心微沉，雙腿螺旋彈簧以 0.8 秒為週期微幅點地彈跳（壓縮 3px 又輕快彈起）；
   - 右手重裝拳套護於頷下，左拳半握前探試探距離，長耳隨彈跳節奏靈動微顫，尾端配重塊輕觸地面保持絕佳動態平衡。
2. **`telegraph`（前搖蓄勁 / 壓縮聚能）**：
   - 身軀後挫，雙腿彈簧深壓至極限（壓縮 8px），分節長尾緊繃撐地形成三角支撐架構；
   - 右拳向後蓄力拉滿，拳套內部活塞急劇後抽吸氣，背部散熱背包噴出短促高壓蒸氣，胸口晶石亮起耀眼金色光芒。
3. **`attack`（普攻出手 / 活塞穿甲重拳）**：
   - 雙腿彈簧猛烈釋放蹬地，身軀如離弦之箭向前爆衝 10px，右拳伴隨活塞超速伸出打出一記剛猛絕倫的直拳（Straight Punch）；
   - 拳套衝頭命中目標瞬間引發氣動二次衝壓，伴隨「砰——鏘！」的金屬爆鳴與飛散的金色齒輪火花，造成致命部位削韌。
4. **`skill`（怒氣大招·旋衝過載暴風連擊 / 破勢在勤）**：
   - 背部發條鑰匙超頻疾轉，雙腿彈簧連續踏地騰空跳躍，雙拳展開如暴風驟雨般的六連環活塞刺拳；
   - 終結一記由下而上的全功率過載升龍拳（Steam Overdrive Uppercut），巨大氣浪伴隨金色齒輪光陣將目標擊飛浮空，完美詮釋「破勢在勤」之拳道真諦！
5. **`hit`（受擊震顫）**：
   - 身軀受衝擊向後仰角 18 度，長耳後擺，胸前齒輪袋震出數顆微型金色螺栓光影；
   - 粗壯彈簧腿向後迅速拖行滑步 6px，長尾重重砸地止住後退勢頭，雙拳迅速架起格擋姿態。
6. **`recover`（倒地虛弱 / 洩壓冷卻）**：
   - 蒸氣系統短暫過載，身軀單膝跪地，雙腿彈簧放鬆舒展，頭頂長耳低垂；
   - 散熱背包釋放長長一聲白霧洩壓「嘶——」，經過 0.7 秒冷卻後，發條主齒輪「喀嗒」自鎖，袋鼠輕捷躍起重回拳擊架式。

### 4.2 戰鬥打擊回饋與相機震動（Juice & Game Feel）

- **音效設計（SFX）**：普攻採用清脆厚重的「蒸氣活塞衝擊（Steam Piston Slam）」與重型黃銅撞擊聲；怒氣大招觸發時加入澎湃的「工業氣動過載重低音」與鐘錶發條急轉蜂鳴。
- **相機反饋**：普攻命中觸發 2.0px 高頻水平微震（50ms）；怒氣終結升龍重拳觸發 4.5px 縱向強烈衝擊震動（120ms）並伴隨 0.06 秒硬直幀凍結（Hitstop），打擊手感剛猛紮實。

---

## 五、 產品層准入（PRODUCT_LOCK_0.20.md §9 門檻自答）

依據《0.20 Product Lock》第 9 節規定，任何新增內容必須完整自答准入門檻六題，逐題檢驗合格方准備案：

### Q1：它掛在 §3.1 核心循環的哪一環？
> **合格回答**：**精準掛在「養成」與「解鎖玩具／發條」這一環。**  
> **詳細論證**：  
> 鐵拳袋鼠並非孤立的新玩法，而是現有 7 大紙娃娃換裝體系（`mob-paperdoll`）在前二十三族基礎上的「第 24 款可解鎖動物素體外殼（Chassis）」。玩家透過通關 R04 黃銅都市·巨輪城章節探索獎勵、擊破旗艦 BOSS·城防泰坦·巨輪霸主掉落稀有零件「高精鎢鋼齒輪」與「耐熱高壓蒸氣閥」在中央動力廣場工坊組裝解鎖、或外觀盲盒抽取獲得；解鎖後完全複用客戶端既有的武器鍛造、十四星軸入魂、怒氣技能樹三層養成鏈，百分之百依循 `探索 → 戰鬥 → 掉落 → 養成 → 解鎖玩具／發條 → 新區域 → 劇情` 的唯一直線主循環。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
> **合格回答**：**同時服務第 1 支柱（第一優先）與第 2 支柱（第二優先）。**  
> **詳細論證**：  
> 1. **服務第 1 支柱（第一優先：世界與角色）**：補強 R04 黃銅都市·巨輪城缺少武術家常駐素體的生態短板！以多巴胺焦糖暖褐赤銅板件、冠軍朱紅拳套、溫潤米白前袋與雙環冠軍發條鑰匙，塑造出自信頑強、熱血樂觀的蒸氣拳擊工匠形象，深化「在鋼鐵齒輪轟鳴的工業都市中，依然有躍動不息的發條拳擊玩具在追尋夢想」的童話基調。  
> 2. **服務第 2 支柱（第二優先：即時戰鬥演出）**：2.2 頭身梨形挺拔剪影、雙螺旋彈簧跳躍身法、長尾動態平衡與高速活塞重拳極其吸睛，配合快節奏刺拳連擊與過載升龍大招，確保「在手機小螢幕上即使 10 秒無 UI 也能一眼看出是鐵拳袋鼠在熱血搏擊」，徹底解決武術家拳套體系長期缺乏第二素體的遺憾。

### Q3：玩家在手機上用單手拇指能不能操作它？
> **合格回答**：**100% 能。**  
> **詳細論證**：  
> 鐵拳袋鼠完全沿用現有的橫屏雙拇指手遊人體工學架構：創角與衣櫥換裝卡片熱區均 ≥ 48px，杜絕誤觸；戰鬥中點擊單鍵即可順暢完成連續刺拳、蓄力衝壓與全螢幕怒氣大招釋放，絕無複雜多指搓招或虛擬搖桿拖曳負擔，完全保留單手大拇指暢玩之流暢體驗。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
> **合格回答**：**完全不需要。**  
> **詳細論證**：  
> 鐵拳袋鼠的素體結構、貼圖切片與動畫參數全部離線封裝於客戶端本機資料庫。在離線無網路狀態下，玩家可順暢創建角色、換裝與通關全主線副本，嚴格恪守 §6「保留零連線可通關」原則。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
> **合格回答**：**絕對不會。**  
> **詳細論證**：  
> 單一套動物素體的完整 2D 資產清冊包括：400×840 官方立牌（約 220 KB）、128×128 戰鬥 6 姿態圖（約 120 KB）、7 槽位局部切片圖層（約 170 KB），經 TinyPNG / WebP 壓縮後，總資產增量嚴格控制在 **0.8 MB 以內**。⚠️ 需特別注意 `PRODUCT_LOCK_0.20.md` §5.2 記載之現況為「Web 目錄 135 MB」、首包目標 50～80 MB，**目前尚未達標**；本族的 0.8 MB 增量相對於該既有缺口極小，但首包瘦身是專案既有欠帳，不因本提案而消解。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
> **合格回答**：  
> 1. **放棄為袋鼠繪製生物皮毛、真皮肉質與生物育兒袋的奢想**：放棄一切生物毛皮紋理與肉體物理模擬，嚴格將材質收斂為「沖壓厚鑄赤銅板、溫潤奶油琺瑯腹袋、鎢鋼螺旋彈簧與分節黃銅尾」，並嚴格遵循 `weapon_classes.json` 的 `fist` 數值與已鎖定之 `BALANCE.md` §5 時間模型（0.15），捍衛低階手機流暢度與戰鬥平衡。  
> 2. **放棄暗黑暴力地下黑拳或血腥格鬥風格**：嚴禁使用暴力血腥、生鏽廢土或恐怖殘暴意象，嚴格將拳擊美學轉譯為「多巴胺焦糖暖褐（#C86D20）、冠軍朱紅（#E63946）、奶油米白（#FFFDF8）與金黃黃銅（#FFD028）」，展現發條玩具在巨輪城陽光蒸氣中堂堂正正切磋競技的熱血童話核心。

---

## 六、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

後續待審核通過後，可直接映射併入 `docs/design/paperdoll_slots.json` 之結構化配置段落如下（僅供資料規格備案，本任務不直接竄改主檔）：

```json
{
  "race_id": "kangaroo",
  "race_name_zh": "鐵拳袋鼠",
  "race_name_en": "The Boxer Kangaroo",
  "native_profession": "monk",
  "native_weapon_class": "fist",
  "starter_weapon_id": "wrap_gloves",
  "native_realm_id": "R04",
  "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
  "lore_anchor": [
    "中央動力廣場",
    "摩天齒輪工坊群",
    "高架重軌引橋·巨輪城站",
    "深淵排污豎井管道",
    "中央蒸氣沐浴池"
  ],
  "palette": {
    "primary_hull": "#C86D20",
    "secondary_hull": "#FFA010",
    "faceplate_enamel": "#FFFDF8",
    "boxing_crimson": "#E63946",
    "gold_accent": "#FFD028",
    "amber_core": "#FF9F1C",
    "tungsten_frame": "#4A5568",
    "outline": "#1F1A3A"
  },
  "winding_key_spec": {
    "key_id": "key_kangaroo_champion_double_ring",
    "name_zh": "沖壓黃銅雙環冠軍發條鑰匙",
    "name_en": "Championship Double-Ring Brass Key",
    "position": "back_center_high",
    "rotation_sound": "sfx_steam_piston_ratchet"
  },
  "slots_manifest": {
    "chassis": "chassis_kangaroo_caramel_bronze_default",
    "head_unit": "head_kangaroo_steampunk_boxer_visor",
    "costume": "costume_kangaroo_champion_belt_harness",
    "optic_core": "optic_kangaroo_amber_dial_core",
    "winding_key": "key_kangaroo_champion_double_ring",
    "weapon": "weapon_kangaroo_piston_brass_knuckle",
    "curio": "curio_kangaroo_steam_exhaust_backpack"
  },
  "pending_assets": [
    "game/assets/sprites/player/paperdoll/kangaroo/chassis/chassis_kangaroo_caramel_bronze_default.png",
    "game/assets/sprites/player/paperdoll/kangaroo/head_unit/head_kangaroo_steampunk_boxer_visor.png",
    "game/assets/sprites/player/paperdoll/kangaroo/costume/costume_kangaroo_champion_belt_harness.png",
    "game/assets/sprites/player/paperdoll/kangaroo/optic_core/optic_kangaroo_amber_dial_core.png",
    "game/assets/sprites/player/paperdoll/kangaroo/winding_key/key_kangaroo_champion_double_ring.png",
    "game/assets/sprites/player/paperdoll/kangaroo/weapon/weapon_kangaroo_piston_brass_knuckle.png",
    "game/assets/sprites/player/paperdoll/kangaroo/back_curio/curio_kangaroo_steam_exhaust_backpack.png",
    "game/assets/sprites/player/paperdoll/key/key_kangaroo_champion_double_ring.png",
    "game/assets/sprites/player/paperdoll/weapon/weapon_kangaroo_piston_brass_knuckle.png",
    "game/assets/sprites/player/paperdoll/kangaroo/proof_paperdoll_kangaroo_composite.png",
    "game/assets/sprites/player/paperdoll/kangaroo/proof_paperdoll_kangaroo_magenta.png",
    "game/assets/sprites/player/paperdoll/kangaroo/proof_kangaroo_all_7_slices.png",
    "game/assets/sprites/player/battle/kangaroo/kangaroo_battle_poses_128.png",
    "game/assets/sprites/player/showcase/kangaroo_idle_hd.png"
  ]
}
```

---

## 七、 效能與包體預算評估（Performance & Package Budget）

### 7.1 資產增量預算（Asset Budget Breakdown）

嚴格執行手機輕量化標準，全資產經過 TinyPNG / WebP 無損/高保真壓縮：

```
┌──────────────────────────────────────────────────────────────┬───────────────┬──────────────┐
│ 資產類別與檔案路徑                                           │ 原始預估容量  │ 壓縮後目標   │
├──────────────────────────────────────────────────────────────┼───────────────┼──────────────┤
│ 1. 400×840 官方立牌展台圖 (kangaroo_idle_hd.png)             │ ~460 KB       │ ≤ 210 KB     │
│ 2. 128×128 戰鬥六姿態精靈圖 (6 幀 768×128 條狀圖)           │ ~240 KB       │ ≤ 110 KB     │
│ 3. 7 大紙娃娃獨立槽位切片圖層 (128×128 RGBA8888 × 7)         │ ~310 KB       │ ≤ 150 KB     │
│ 4. 通用目錄鏡像檔 (key/ 與 weapon/ 兩枚圖示)                 │ ~60 KB        │ ≤ 30 KB      │
│ 5. 驗收合成圖與洋紅邊界校驗圖 (僅存證，不打包進 Release)     │ [Dev Only]    │ [0 KB 首包]  │
├──────────────────────────────────────────────────────────────┼───────────────┼──────────────┤
│ 總計（加入首包之正式 Release 資產增量）                      │ ~1.07 MB      │ ≤ 0.50 MB    │
└──────────────────────────────────────────────────────────────┴───────────────┴──────────────┘
```

- **包體欠帳與門檻說明**：
  - 據實核對現狀：`PRODUCT_LOCK_0.20.md` §5.2 明載當前專案 Web 目錄為 135 MB，距離目標 50~80 MB 尚在收斂推進中，本提案嚴格保證單族增量 < 0.8 MB，不增加額外首包負擔。

### 7.2 執行期記憶體與 Token 成本評估（Runtime & Token Cost）

1. **客戶端記憶體與 DrawCall 負載**：
   - 鐵拳袋鼠 7 大槽位切片完全複用既有的 2D 紙娃娃 CanvasItem 著色器（`sprite_db.gd`），不新增額外材質 Pass；
   - 單一角色待機狀態佔用 VRAM 約 1.0 MB，符合行動裝置低階 2GB RAM 設備同屏 10 人流暢 60 FPS 規範。
2. **LLM 描述與資料結構 Token 預算**：
   - 機器讀取規格配置段落（JSON）嚴格控制在 310 ~ 340 tokens 之間；
   - 欄位命名嚴格遵循既有 `paperdoll_slots.json` 規範，避免冗餘深層巢狀結構，大幅降低後續 Agent 在解析、檢索與代碼生成時的 Prompt 上下文開銷。

---

## 八、 驗收 Checklist（對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **CANON.md 零毛皮鐵律**：100% 零生物毛皮、零肉身、零肉墊、零生物育兒袋、零軟組織；全數轉譯為沖壓厚鑄焦糖暖褐赤銅板件、溫潤奶油米白琺瑯面頰與腹袋、冷軋鎢鋼雙螺旋減震彈簧、分節黃銅重力平衡長尾、雙聯琥珀光學儀表目鏡、沖壓黃銅雙環冠軍發條鑰匙與鎢鋼防滑接地掌板。
- [x] **CANON.md 背部發條鑰匙**：背部高位動力插座配備「沖壓黃銅雙環冠軍發條鑰匙」，拋光黃銅雙環獎章造型，中央浮雕咬合齒輪，旋轉伴隨清脆金屬卡榫與微型洩壓聲「鏘——哧！」。
- [x] **review.md 23f-1 職業正式名稱**：正式名稱精準採用單一規範名：**`武術家 (Monk)`**，完全依據 `weapon_classes.json` 規範名，無任何自創新名。
- [x] **review.md 0-MKT7 單持武器規範**：右手單戴重裝氣壓活塞衝壓黃銅拳套置於胸前，左手平曲護胸抱拳蓄勁，全圖精確為 1 組武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- [x] **既有武器 ID 嚴格對齊**：精準對應 `equipment.json` 第 210 行既有 `wrap_gloves`（練拳綁帶）與第 223 行 `iron_knuckle`（鐵節拳套）；專屬款式 `weapon_kangaroo_piston_brass_knuckle` 明確標註待審，底層掛載 `fist` line，不准自行創造未審 id。
- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：`lore_anchor` 所載「中央動力廣場」、「摩天齒輪工坊群」、「高架重軌引橋·巨輪城站」、「深淵排污豎井管道」與「中央蒸氣沐浴池」逐字比對 `docs/world/regions/R04_BRASS_METROPOLIS.md` 第 48 行、第 239 行、第 240 行、第 241 行與第 242 行 100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（首包數字查驗）**：據實引用 `PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有二十三族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 23 族（含第 21 族棘輪刺蝟、第 22 族荒原鋼狼與第 23 族琉璃海馬）。
- [x] **世界觀十四主星對齊**：掛載 R04 特產之「武曲星軸（破甲連擊 / Wu Qu Core）」與「破軍星軸（銳齒之魂 / Po Jun Core）」，象徵高頻連擊削韌、衝壓破甲與重工機械動能。
- [x] **職業與武器平衡**：補足武術家職業下轄 `fist`（拳 / 武鬥·拳）僅有第 13 族瓷韻熊貓單一素體之缺口，達成武術家職業（爪 2、拳 2）對等平衡，正式達成全遊戲六大職業（戰士 4、遊俠 4、忍者 4、騎士 4、法師 4、武術家 4）共 24 族大圓滿完全閉環！
- [x] **7 大紙娃娃槽位完整度**：Slot 1~7 涵蓋 chassis / head_unit / winding_key / costume / optic_core (accessory) / weapon / curio (back_curio)，命名規則與擴充款式定義完備，可供美術直接產切片。
- [x] **純文件交付邊界**：嚴守任務要求，未產圖、未產片、零花費、未改動底層程式碼與正式 `paperdoll_slots.json` 權威檔。

---

## 九、 六語系在地化對照表（Localization Lexicon）

| 專有名詞分類 | 繁體中文 | 簡體中文 | 英文（EN） | 西班牙文（ES） | 日文（JA） | 韓文（KO） |
|:---|:---|:---|:---|:---|:---|:---|
| **角色全名** | 鐵拳袋鼠 | 铁拳袋鼠 | The Boxer Kangaroo | El Canguro Boxeador | アイアン・カンガルー | 아이언 캥거루 |
| **角色頭銜** | 蒸氣拳擊家·巨輪冠軍 | 蒸气拳击家·巨轮冠军 | Steam Pugilist: Cog Champion | Pugilista de Vapor: Campeón de Gran Engranaje | 蒸気拳闘士・巨輪の王者 | 증기 권투가·거륜의 챔피언 |
| **原生武器** | 氣壓活塞衝壓黃銅拳套 | 气压活塞冲压黄铜拳套 | Pneumatic Brass Stamping Knuckle | Puño Estampado Neumático de Latón | 気圧ピストン真鍮ナックル | 기압 피스톤 황동 너클 |
| **專屬發條鑰匙**| 沖壓黃銅雙環冠軍鑰匙 | 冲压黄铜双环冠军钥匙 | Championship Double-Ring Brass Key | Llave de Latón de Doble Anillo de Campeón | プレス真鍮二連チャンピオン鍵 | 프레스 황동 더블 링 챔피언 키 |
| **頭部頂盔** | 蒸氣拳擊長耳護額頭盔 | 蒸气拳击长耳护额头盔 | Steampunk Long-Ear Boxer Visor | Visera de Boxeador de Orejas Largas de Vapor | 蒸気ボクサー長耳バイザー兜 | 증기 복서 장이 바이저 투구 |
| **面部光學** | 雙聯琥珀光學儀表目鏡 | 双联琥珀光学仪表目镜 | Twin Amber Vacuum Gauge Eyes | Ojos de Manómetro Óptico de Ámbar Dobles | 複眼琥珀メーター光学レンズ | 복안 호박 게이지 광학 렌즈 |
| **核心背飾** | 雙聯微型高壓蒸氣散熱背包 | 双联微型高压蒸气散热背包 | Twin Steam Exhaust Backpack | Mochila de Escape de Vapor Doble | ぜんまい式二連蒸気排気バックパック | 태엽식 2연장 증기 배기 백팩 |
| **核心招式 1** | 活塞穿甲重拳 | 活塞穿甲重拳 | Piston Armor-Piercing Straight | Puñetazo Perforante de Pistón | ピストン徹甲ストレート | 피스톤 철갑 스트레이트 |
| **核心招式 2** | 旋衝過載暴風連擊 | 旋冲过载暴风连击 | Steam Overdrive Flurry | Ráfaga de Sobrecarga de Vapor | 蒸気過負荷ラッシュ | 증기 과부하 난타 |
| **核心機制** | 蒸氣噴流浮跳破勢 | 蒸气喷流浮跳破势 | Steam Vent Leap & Stance Break | Salto de Vapor y Ruptura de Postura | 蒸気噴流跳躍・崩し | 증기 분출 도약 파세 |
