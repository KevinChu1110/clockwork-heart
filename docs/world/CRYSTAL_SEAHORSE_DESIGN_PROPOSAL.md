# 第二十三種動物「琉璃海馬（The Crystal Seahorse）」世界觀與角色設計提案

> **文件狀態**：世界觀擴充提案與角色規格書（Expansion World & Chassis Proposal - Ready for Review）  
> **制定日期**：2026-09-28  
> **負責人**：側案·策劃總監 小凱（sideplan）  
> **審核對象**：側案製作人 老周（side） / 側案美術總監 小柔（sideart） / 側案程式 阿宏（sideworker）  
> **對應看板任務**：`t_f5db0642`（📖 世界觀｜第二十三種動物紙娃娃角色設計提案（只寫文件，不產圖不產片））  
> **關聯歸檔文件**：  
> - [`docs/design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md)  
> - [`docs/world/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../world/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md)  
> - [`docs/art/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md`](../art/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md)  
> **關聯依據文件**：  
> - `docs/world/regions/R05_CRYSTAL_OCEAN.md`（第 1 行區域代號與名稱「R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss」、第 4 行「高透光海藍琉璃凝膠、耐高壓深海石英泡罩、防腐蝕鍍鈦合金骨架、發條磁吸氣動閥門與磷光發條指針儀表套件」、第 19 行「液態琉璃凝膠海 Liquid Crystal Gel Sea」、第 20 行「海淵地表與馬賽克步道 Abyssal Seabed & Mosaic Walkways」、「發條珊瑚群 Clockwork Coral Reeds」、第 21 行「水下發條宮殿與氧氣泡罩 Clockwork Sunken Palace & Aerated Glass Domes」、第 22 行「磷光水母街燈與流體排氣柱 Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents」、第 24-25 行「水下丁達爾藍晶光柱」、「青銅錨鏈秒針」、第 29 行「深淵排污豎井管道·耐壓吊籠 Abyssal Sump Siphon: Bathysphere Terminal」、第 30 行「晨曦天軌 5 號深海浮標月台 Dawn Rail Deepsea Buoy Platform 5」、第 44 行「發條海馬信差 Wind-up Seahorse Couriers」、第 64 行核心 NPC「海馬信差·碧浪 Billow the Seahorse Courier」、第 72 行核心 NPC「深海鐘錶貝·珠貝長老 Elder Pearl the Clockwork Clam」、第 194 行核心機制「洋流阻尼與浮力散熱窗口 Hydro-Damping & Buoyancy Window」、第 202 行核心機制「上升氣泡井與耐壓石英泡罩 Buoyancy Bubble Lifts & Air Domes」、第 236 行地標「水下發條宮殿」、第 237 行地標「藍晶石海淵平原」、第 253 行代表素材「澄澈深海藍晶核」、第 254 行代表素材「鍍鈦耐腐蝕增壓閥」、第 257 行核心星軸「天府星軸 Tian Fu Core」、第 258 行核心星軸「太陰星軸 Tai Yin Core」）  
> - `docs/design/paperdoll_slots.json` / `docs/design/PAPERDOLL_SLOTS_SPEC.md`（7 大部件槽位架構）  
> - `game/data/tables/weapon_classes.json`（6 職業 12 大武器系統，法師·晶 `crystal` 體系）  
> - `game/data/tables/equipment.json`（既有水晶武器 ID：第 392 行 `shard_focus` 碎晶聚能、第 405 行 `prism_scepter` 棱鏡權杖）  
> - `docs/world/CANON.md`（世界憲章：100% 零毛皮零軟組織、沖壓成型耐壓鍍鈦金屬板件/全金屬與齒輪咬合發條玩具、三叉戟珊瑚晶簇黃銅發條鑰匙）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `docs/BALANCE.md`（§5 時間模型 0.15 鎖版規範）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位**：本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）在第二十二族荒原鋼狼圓滿完成騎士長劍對稱後，比照前二十二族標準流程制定之**第二十三種動物擴充素體規格**。本提案標誌著六大職業朝向 24 族完全對稱陣容（6 職業 × 4 族 = 24 族，每種武器精確對應 2 族）邁出最關鍵的倒數第二步——**補足全遊戲自創角上線以來唯一長期單一匱乏的「法師·晶（Mage Crystal）」素體缺口**，使法師職業（狐·杖、鴞·杖、龜·晶、海馬·晶）達成「杖 2 族、晶 2 族」完全對稱平衡，並使戰士、遊俠、忍者、騎士、法師五大職業全數達成 4 族圓滿對稱！
2. **經典玩具起源與古典機械發條深海海馬工藝**：
   - 本提案選定全球古典機械玩具史與水族微縮自動人偶經典名作——**「19世紀末歐洲古典鐘錶發條咬合潛水海馬自動人偶（Victorian Clockwork Swimming Seahorse Automata）」**（直接承接 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 第 1 行、第 4 行「高透光海藍琉璃凝膠、耐高壓深海石英泡罩、防腐蝕鍍鈦合金骨架」、第 20 行「海淵地表與馬賽克步道」、「發條珊瑚群」、第 21 行「水下發條宮殿與氧氣泡罩」、第 44 行「發條海馬信差」、第 64 行核心 NPC「海馬信差·碧浪」、第 72 行「深海鐘錶貝·珠貝長老」、第 194 行「洋流阻尼與浮力散熱窗口」、第 253 行「澄澈深海藍晶核」與第 257-258 行「天府星軸」、「太陰星軸」之耐壓深潛、高折射琉璃稜鏡與發條浮力阻尼工藝）；
   - 作為全遊戲 23 大種族中**首款也是唯一的三叉齒輪晶冠頂盔、節狀鍍鈦球窩脊椎、捲曲預應力螺旋板簧尾、雙聯微型螺旋推進晶鰭、三叉戟珊瑚晶簇黃銅發條鑰匙與深海靈晶浮空星盤素體（Trident Crown Head Unit, Segmented Titanium Spine, Pre-stressed Torsion Spring Tail, Twin Dorsal Fin Propellers, Trident Coral Key & Abyssal Prism Astrolabe）**。在材質工藝（高透光海藍琺瑯烤漆裝甲、象牙米白陶瓷面頰與胸板、消光鍍鈦耐壓骨架、雙聯深海藍寶石透鏡目鏡、珊瑚晶金三叉戟發條鑰匙與防滑減震三柱液壓接地鰭足）、幾何辨識（優雅挺拔 2.2 頭身水生法師姿態、右手懸引浮空多面深海靈晶星盤、左手微曲作引導水流阻尼與晶盾編織之法術起手架式、身後高頻振顫微型晶鰭與捲曲彈簧尾）與戰鬥身法（洋流阻尼懸停、浮力頂點下墜重擊、藍晶護盾織刃反震、潮汐星陣暴發）上，與前二十二族形成 100% 徹底差異化之視覺辨識度與打擊回饋。
3. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
4. **商業與數值護欄**：
   - **絕對零數值（Zero Pay-to-Win）**：琉璃海馬素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。
   - **武器與職業對齊**：精準收斂至既有 6 職業 12 大武器體系中之 `mage`（法師）下轄之 **`crystal`（水晶 / 法師·晶）** 系統，以【深海靈晶浮空星盤 / 琉璃棱鏡核心（Abyssal Prism Astrolabe / Crystal Focus）】呈現。補足前二十二族中水晶武器僅有第 10 族玄機龜單一素體的長期缺口，使法師職業（狐·杖、鴞·杖、龜·晶、海馬·晶）達成「杖 2 族、晶 2 族」的完全對稱平衡，並使全遊戲唯一長期僅有單一素體（浪花海獺）的深水界域 R05 琉璃汪洋迎來第二位守護者！

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有二十二族武器與職業光譜全盤點

盤點現有首發五族與前十七款擴充族的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 之正式中文名稱）：

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

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業（`knight`、`viking`、`ninja`、`monk`、`mage`、`ranger`）中：
- 戰士（Viking）已達 4 族（鎚 2、斧 2），達成圓滿對等；
- 遊俠（Ranger）已達 4 族（弓 2、銃 2），達成圓滿對等；
- 忍者（Ninja）已達 4 族（匕 2、鏢 2），達成圓滿對等；
- 騎士（Knight）已達 4 族（劍 2、槍 2），達成圓滿對等；
- 武術家（Monk）已有 3 族（拳 1、爪 2）；
- **法師（Mage）目前為 3 族（杖 2、晶 1），其中下轄的護體靈晶武器（`crystal`）自第十族玄機龜以來，歷經 12 族未曾獲得任何擴充！**
- 與此同時，在全遊戲 9 大界域中，中低層水域沙盤界域 `R05 琉璃汪洋·發條海淵` 長期僅有第 19 族浪花海獺（戰士·斧）孤身鎮守，是全地圖 9 大界域中唯一僅有單一素體的生態最薄弱界域！

第二十三種動物琉璃海馬正式選定掛載於 **`mage`（法師）** 職業體系，原生武器對齊 **`crystal`（水晶 / 法師·晶）**。依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`法師 (Mage)`**。  
此舉完美填補水晶武器長久以來的單一匱乏，使法師職業達成「杖 2 族、晶 2 族」的完全對稱平衡，並使 R05 琉璃汪洋形成「浪花海獺戰士 × 琉璃海馬法師」的經典深海水域雙搭檔！

### 1.2 琉璃海馬武器選擇：【深海靈晶浮空星盤 / 琉璃棱鏡核心（Abyssal Prism Astrolabe / Crystal Focus）】

琉璃海馬原生專屬武器定名為：**【深海靈晶浮空星盤 / 琉璃棱鏡核心（Abyssal Prism Astrolabe / Crystal Focus）】**。  
該武器底層完全掛載於 `weapon_classes.json` 的 `crystal`（法師·晶）類別，享有 `crystal` 既有的「把護盾織成刃」標籤宣言（Tagline: `"把護盾織成刃"`）、卓越的防禦、充沛的生命與魂槽輔助特性（`atk: 0, def: 3, hp: 10, crit: 1.0, speed: 0`），完美呼應 `R05_CRYSTAL_OCEAN.md` 第 4 行「高透光海藍琉璃凝膠、耐高壓深海石英泡罩」、第 20 行「深海藍晶石馬賽克瓷磚」、第 76 行珠貝長老傳授「深海藍晶石防禦與反傷星軸」、第 194 行「洋流阻尼與浮力散熱窗口」與第 253 行代表素材「澄澈深海藍晶核」之深海光學棱鏡與液態阻尼防禦世界觀！

- **既有武器 ID 對齊（嚴格遵守規範）**：
  - 基礎入門與進階相容武器 ID：完全對齊 `game/data/tables/equipment.json` 第 392 行既有 ID **`shard_focus`（碎晶聚能）**（tier 1，line: "crystal"，`atk: 4, def: 2, hp: 10, crit: 2, crit_dmg: 8`），進階武器對齊第 405 行既有 ID **`prism_scepter`（棱鏡權杖）**（tier 3，line: "crystal"，`atk: 10, def: 4, hp: 16, crit: 4, crit_dmg: 12`）；
  - 專屬外觀款式 ID：明確標註為待審核專屬外觀款式 `weapon_seahorse_abyssal_prism_astrolabe`（待審核，底層 100% 繼承既有 line: "crystal"，數值直接掛載 `shard_focus` / `prism_scepter`，絕不自行創造未定義之程式數值 id）。
- **單持規範遵守**：遵循 `review.md 0-MKT7` 單持規範，右手微曲優雅懸引浮空旋轉之「深海靈晶浮空星盤」（高折射率深海藍晶石多面稜鏡，內嵌微型發條磁懸浮陀飛輪與黃銅同心環）；左手空手自然微曲作引導水流阻尼與晶盾編織之法術起手架式，維持身法重心，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。

### 1.3 差異化定位：與玄機龜（玄機八卦發條星盤）及其他 21 族絕不撞型之論證

雖然琉璃海馬與玄機龜同屬 `mage`（法師）水晶（`crystal`）體系，但在**戰鬥型態與身法節奏**、**力學核心與動態性格**以及**機械構造與材質語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機小螢幕上於 0.5 秒內清晰辨識：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   法師職業水晶武器差異化對照表（玄機龜 vs 琉璃海馬）                   │
├───────────────────┬──────────────────────────┬──────────────────────────┤
│ 維度              │ 玄機龜（Xuanji Tortoise）│ 琉璃海馬（The Crystal Seahorse） │
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ① 職業與武器     │ 法師 (Mage)              │ 法師 (Mage)              │
│                   │ 玄機八卦發條星盤(`crystal`)│ 深海靈晶浮空星盤(`crystal`)│
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ② 身法與戰鬥節奏 │ 沉重磐石穩步推進、        │ 垂直優雅浮力懸停、        │
│                   │ 縮頸重甲高防原地反震、    │ 洋流阻尼蓄力、浮力頂點下墜│
│                   │ 東方八卦陣地防禦織網      │ 藍晶透鏡聚焦光束切割      │
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ③ 材質語彙與結構 │ 青銅古翠綠烤漆、太極雙魚  │ 高透海藍琺瑯烤漆、鍍鈦骨架│
│                   │ 陶瓷雲石白胸甲、青銅套筒  │ 象牙白陶瓷面頰、雙聯晶鰭  │
│                   │ 縮頸四柱重足、太極發條匙  │ 捲曲螺旋彈簧尾、三叉晶冠匙│
├───────────────────┼──────────────────────────┼──────────────────────────┤
│ ④ 所屬界域       │ R09 竹影道場·天元竹林    │ R05 琉璃汪洋·發條海淵    │
└───────────────────┴──────────────────────────┴──────────────────────────┘
```

1. **打擊型態差異（重裝陣地反震 vs 立體浮力阻尼聚焦射擊）**：
   - **玄機龜（龜·晶）**：定位為「磐石壁壘陣地法師」。四足著地穩固如山，戰鬥時依託龜甲縮頸與青銅厚甲原地展開八卦護盾，硬接敵方重擊後將動能轉化為反震衝擊波，核心手感在於「站定防禦、反震破勢」。
   - **琉璃海馬（海馬·晶）**：全 23 族中唯一的**「立體浮力洋流阻尼法師（Buoyancy Flow & Prism Weaver）」**。海馬身形纖細挺拔，借助預應力螺旋板簧尾在海床上點地起伏懸停；出招時利用洋流阻尼蓄力，在浮力懸停頂點（0.8 秒）引導星盤晶石多面稜鏡聚焦射出高能藍晶射線，命中敵方破綻引發晶爆穿甲，兼備水下立體機動性與精準穿刺。
2. **力學核心與動態性格（沉穩太極玄學 vs 古典深海耐壓光學工藝）**：
   - 玄機龜的發條動能源自「太極雙魚齒輪咬合與玄機經緯環」，行進沉重，強調動靜相生與以柔克剛。
   - 琉璃海馬的發條動能則源自「深海高壓抗逆流螺旋扭簧與微型齒輪箱」，背部高頻微幅扇動的雙聯晶鰭散發出童話水生玩具特有的輕盈與靈動，待機時伴隨水泡微波起伏，展現優雅冷靜的深海學者氣質。
3. **幾何剪影與材質語彙（低矮半球重甲 vs 垂直挺拔王冠長吻）**：
   - 在 128×128 與 400×840 畫布上，玄機龜呈現寬扁低矮的橢圓半球體重甲輪廓與伸展四足；
   - 琉璃海馬則呈現鮮明對比的「垂直修長 S 型優雅曲線」：頭頂帶有標誌性的沖壓三叉王冠晶冠、面部為纖細套筒式金屬吸水長吻、頸胸呈現多層鍍鈦環甲弧線、下半身則是向上內卷的螺旋金屬板簧尾，剪影在 0.5 秒內具有 100% 絕對唯一性。

---

## 二、 外觀定調與機械美學（Aesthetic & Mechanical Canon）

### 2.1 零毛皮玩具世界憲章對齊（CANON.md Compliance）

依據《發條之心世界憲章》（`docs/world/CANON.md`）第一級根本大法，琉璃海馬的造型設計**100% 徹底清除任何有機生物體特徵**：
- ⛔ **嚴禁生物魚皮、濕滑黏液、生肉魚鰓與真魚鱗**；
- 100% 轉譯為：
  - **耐壓鍍鈦合金沖壓裝甲板**（Titanium Pressure-Proof Hull Plates）；
  - **拋光高透光海藍色琺瑯烤漆外殼**（Polished Cyan Enamel Coating）；
  - **象牙米白陶瓷面頰與胸板**（Ivory Porcelain Faceplates & Breastplate）；
  - **雙聯深海藍寶石光學透鏡目鏡**（Twin Ocean Sapphire Optical Core Lenses）；
  - **雙層高韌性半透明薄荷螢綠矽膠背鰭**（Dual Fluor-Mint Silicone Propeller Fins）；
  - **捲曲預應力螺旋板簧尾部足底**（Coiled Pre-stressed Spring Tail Baseplate）；
  - **外露耐腐蝕平頭黃銅螺栓與鍍鈦密封圓頭鉚釘**。

### 2.2 色彩配置與多巴胺色盤（Dopamine Palette & Dawson Day 258）

嚴格遵循《塔塔冒險隊》與《楓之谷》多巴胺鮮亮高飽和色盤規範，杜絕暗黑冰冷深海或髒泥土黑灰：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        琉璃海馬官方標準多巴胺配色體系                                  │
├─────────────────┬───────────┬──────────────────────────────────────────────────────────┤
│ 配色部位        │ 色碼 (HEX)│ 材質語言與視覺心理感受                                   │
├─────────────────┼───────────┼──────────────────────────────────────────────────────────┤
│ ① 主色：海藍琺瑯│ #38A0FF   │ 琉璃汪洋多巴胺天藍拋光琺瑯烤漆，高亮通透，深海童話色彩    │
│ ② 輔色：薄荷海藍│ #2EC4B6   │ 雙聯背鰭與水下耐壓密封圈，薄荷青綠琉璃螢光，清新靈動      │
│ ③ 面甲：象牙陶瓷│ #FFFDF8   │ 面頰板與胸前護板，溫潤陽光奶油米白，營造親切反差萌        │
│ ④ 點綴：珊瑚晶金│ #FFD028   │ 三叉戟發條鑰匙、頭頂王冠齒輪齒尖與同心刻度環，金黃璀璨    │
│ ⑤ 點綴：珊瑚晶粉│ #FF5E8A   │ 微型氣壓平衡閥、引力導線端子，增添甜美多巴胺玩具細節      │
│ ⑥ 晶核：深海藍晶│ #1C54B2   │ 雙眼光學透鏡與星盤核心晶石，沉穩深邃之光學石英藍          │
│ ⑦ 結構：消光鍍鈦│ #7A8B99   │ 球窩脊椎關節、吸水長吻套筒與螺栓，工藝結構紮實可靠        │
│ ⑧ 輪廓：深藍紫框│ #1F1A3A   │ 全身 2px 實體厚描邊，深藍紫取代純黑，畫面乾淨通透不髒      │
└─────────────────┴───────────┴──────────────────────────────────────────────────────────┘
```

### 2.3 發條鑰匙定位與幾何結構（The Winding Key）

- **鑰匙造型**：**【三叉戟珊瑚晶簇黃銅發條鑰匙（Trident Coral-Crystal Winding Key）】**。  
  主體為巴洛克工藝沖壓成型的拋光金黃黃銅（#FFD028），鑰匙手柄呈現優雅的三叉戟輪廓，三叉戟中央環形凹槽內鑲嵌一顆高透光深海藍晶石（#38A0FF），兩側外沿雕刻有發條珊瑚細緻的齒輪枝椏紋理。
- **插座位置**：精準位於海馬**背部中上部動力艙脊椎軸心**（胸椎第 3 節齒輪箱後側），高於雙聯背鰭上方 8px，完全避開背鰭扇動軌跡。
- **力學律動與音效**：發條每順時針旋轉一圈，伴隨沉穩悅耳的「叮——哧！」聲響（金屬齒輪自鎖與水壓平衡微氣閥排氣聲），象徵深海深潛氣動發條能量注入。

### 2.4 機械細節與人體工學（Chibi Ergonomics）

- **2.2 頭身 Q 版黃金比例**：頭部高 48px（含王冠），軀幹長 36px，下半身螺旋彈簧尾長 44px，整體站姿高度嚴格對齊既有 128×128 畫布規範。
- **頭部王冠與長吻特徵**：頭頂裝配由三枚黃銅齒輪片拼合而成的三叉王冠頂盔，面部為可前後微幅伸縮 4px 的金屬套筒吸水長吻，長吻前端帶有金黃銅箍，表情呆萌可愛且兼具精密儀器感。
- **接地平衡與螺旋足底**：下半身為一體成型的五節鍍鈦螺旋板簧尾，尾端向內捲曲形成穩固的環形底座，底座下方配置三組微型矽膠吸盤腳墊，確保在海床瓷磚與陸地木質地板上均能穩固站立，並在受擊時提供極佳的垂直減震彈性。

---

## 三、 7 大紙娃娃外觀槽位規劃（Paperdoll Slots Architecture）

嚴格依據 `docs/design/paperdoll_slots.json` 與 `PAPERDOLL_SLOTS_SPEC.md` 所規範之 7 大標準圖層，琉璃海馬擴充資產規劃如下：

### 3.1 槽位分層與渲染管線（Z-Order Alignment）

```
[Layer Z: 05] winding_key : 三叉戟珊瑚晶簇黃銅發條鑰匙（背部最底層插座）
[Layer Z: 10] chassis     : 琉璃海馬原廠海藍琺瑯烤漆素體（含螺旋彈簧尾與接地軟陰影）
[Layer Z: 15] costume     : 海淵天宮星象輕甲工裝（象牙白胸甲與護肩）
[Layer Z: 20] head_unit   : 沖壓高透石英水晶冠冕頂盔（鏤空雙眼窩）
[Layer Z: 25] optic_core  : 雙聯深海藍寶石透鏡目鏡＋胸口發條之心天藍晶石（accessory）
[Layer Z: 30] weapon      : 深海靈晶浮空星盤（右手單持懸引）
[Layer Z: 35] curio       : 雙聯微型發條螺旋推進晶鰭（back_curio 背部最外層動態飾品）
```

### 3.2 七大槽位細節拆解

#### Slot 1：chassis（軀體外殼與塗裝，Layer Z=10）
- **資產 ID**：`chassis_seahorse_abyssal_cyan_default`
- **外觀特徵**：2.2 頭身海馬造型金屬骨架。通體噴塗高光多巴胺海藍琺瑯烤漆（#38A0FF），胸腹部帶有鍍鈦水平條紋防壓加強筋。頸部與尾部為外露的球窩機械關節，下半身為五節高彈錳鋼螺旋板簧尾，尾部末端配備三柱微型液壓減震平衡鰭足，足底包含 48×16px 橢圓形柔和投影軟陰影（接地點 x=64, y=120）。
- **規範檢查**：100% 裸機素體，武器區域（右側）0 像素殘留，眼窩完全鏤空，嚴禁畫死任何衣服或武器。

#### Slot 2：head_unit（頭部與面甲，Layer Z=20）
- **資產 ID**：`head_seahorse_crown_visor`
- **外觀特徵**：沖壓耐壓鍍鈦深海頂盔，額頭上方延伸出一具精緻的三叉王冠狀齒輪晶冠，齒尖為多巴胺金黃（#FFD028）；面部為套筒式吸水長吻，吻端飾有黃銅微調刻度圈；面頰兩側為象牙米白陶瓷面頰板（#FFFDF8），外露兩顆 2px 圓頭固定螺栓。
- **眼窩規範**：雙眼窩尺寸為精確 12×12px 鏤空透空區，透空度 100%，絕不殘留任何眼珠底色，供 `optic_core` 自由換裝。

#### Slot 3：costume（服裝與甲冑，Layer Z=15）
- **資產 ID**：`costume_seahorse_abyssal_scholar_harness`
- **外觀特徵**：海淵天宮星象學者輕甲工裝。前胸為象牙白陶瓷釉面胸甲，兩側帶有海藍色鍍鈦弧形護肩，腰間配有防腐蝕編織背帶與一只小巧的黃銅指針氣壓計。
- **晶石孔規範**：胸口正中央嚴格預留直徑 14px 的晶石展示圓孔，絕不遮擋 `optic_core` 之發條之心晶石。

#### Slot 4：optic_core（目鏡與晶核 / accessory，Layer Z=25）
- **資產 ID**：`optic_seahorse_ocean_sapphire`
- **外觀特徵**：
  - **眼部透鏡**：雙聯直徑 8px 的深海藍寶石透鏡（#1C54B2），內置同心圓刻度發光光圈，高光點為純白（#FFFFFF）位於左上方，散發出專注而純真的學者神采；
  - **發條之心晶核**：位於胸口正中央，為一顆多面切割的菱形天藍晶石（#38A0FF），周圍環繞極細的黃銅防護卡爪，隨呼吸節奏微幅發出多巴胺柔光脈動。

#### Slot 5：winding_key（發條鑰匙，Layer Z=05）
- **資產 ID**：`key_seahorse_trident_coral_spire`
- **外觀特徵**：三叉戟珊瑚晶簇黃銅鑰匙。整體寬 36px、高 32px，巴洛克拋光金黃黃銅打造，中央三叉戟鏤空處鑲嵌天藍色晶石，插座高出背鰭上方，旋轉時具有清晰的金屬光澤反射。
- **通用目錄同步**：產出時同步鏡像輸出至 `game/assets/sprites/player/paperdoll/key/key_seahorse_trident_coral_spire.png`。

#### Slot 6：weapon（手持武器，Layer Z=30）
- **資產 ID**：`weapon_seahorse_abyssal_prism_astrolabe`
- **外觀特徵**：深海靈晶浮空星盤。單手持握規範，右手懸引。由三層大小不一、逆向緩慢旋轉的鍍鈦經緯金屬刻度環組成，核心懸浮著一顆八面體高折射率深海藍晶石（#38A0FF），晶石向外散發出微弱的淡天藍色流光星屑。
- **通用目錄同步**：產出時同步鏡像輸出至 `game/assets/sprites/player/paperdoll/weapon/weapon_seahorse_abyssal_prism_astrolabe.png`。

#### Slot 7：curio（背部飾品 / back_curio，Layer Z=35）
- **資產 ID**：`curio_seahorse_twin_propeller_fins`
- **外觀特徵**：雙聯微型發條螺旋推進晶鰭。安裝於海馬背部兩側，由雙層多巴胺薄荷綠半透明高韌性矽膠（#2EC4B6）與黃銅鉸鏈製成。待機時以 12 Hz 頻率微幅高頻顫動，向後排出細小的發條氣泡微粒，極具玩具靈動感。

---

## 四、 六大戰鬥動作姿態規格（Six Core Battle Poses）

嚴格依據既有 6 動作姿態體系（128×128 與 512×512 雙規格），拆解琉璃海馬之動態表演：

### 4.1 六姿態招式意象拆解

1. **`idle`（戰鬥待機）**：
   - 2.2 頭身海馬挺拔優雅立於海床，尾端螺旋板簧以 1.2 秒為週期微微壓縮 2px 又舒展，身體如同在水中自然呼吸浮沉；
   - 右手微曲，深海靈晶星盤在手心上方 6px 處平穩懸浮緩速自轉；背部雙聯薄荷晶鰭輕快振顫，雙眼透鏡晶光微動。
2. **`telegraph`（前搖蓄勁 / 攻擊準備）**：
   - 海馬身軀後傾 12 度，尾部螺旋彈簧深度下壓蓄力，胸口晶石爆發出多巴胺天藍色光芒；
   - 浮空星盤三層經緯環逆向超速旋轉，周圍水流凝膠向星盤中心急劇收縮，形成肉眼可見的「洋流阻尼旋渦」，蓄勢待發。
3. **`attack`（普攻出手 / 晶芒穿刺）**：
   - 尾部彈簧猛然彈射釋放，身軀向前優雅滑行衝刺 8px，右手向前優雅一指；
   - 星盤核心晶石射出一道極細的多稜鏡光束，瞬間洞穿目標弱點，伴隨清脆的「叮——嗡！」水晶共鳴音效，造成精準部位破壞累積。
4. **`skill`（怒氣大招·潮汐星陣暴發 / 護盾織刃）**：
   - 背部發條鑰匙全速飛旋，海馬騰空懸停至半空中，星盤升至頭頂化作直徑 96px 的巨大發條天球儀光陣；
   - 光陣中央凝聚出數十枚菱形藍晶光錐，如暴雨般朝前方扇形區域傾瀉轟擊，隨後光陣化為一層包裹自身的藍晶護盾，完美演繹「把護盾織成刃」之標籤奧義！
5. **`hit`（受擊震顫）**：
   - 身軀向後仰角 15 度，頭頂三叉晶冠劇烈震顫，金屬吸水長吻噴出一縷細密氣泡；
   - 尾部彈簧迅速向後伸展抵住地面化解衝擊力，左手抬起護住胸口發條之心，雙眼透鏡短暫閃爍微弱黃光。
6. **`recover`（倒地虛弱 / 散熱修復）**：
   - 發條動力短暫卸載，身軀向前微微俯傾，螺旋尾放鬆盤曲，背鰭停止振顫；
   - 星盤核心光芒暗淡回落至手邊，經過 0.8 秒減壓排氣「哧——」的一聲，背部發條自鎖齒輪重新「喀噠」咬合，海馬重新優雅挺起身軀。

### 4.2 戰鬥打擊回饋與相機震動（Juice & Game Feel）

- **音效設計（SFX）**：普攻採用清脆高頻的「玻璃水琴音階（Glass Chime）」與金屬音叉共鳴；怒氣大招觸發時加入深沉激昂的「深海錨鏈齒輪震顫重低音」，層次分明。
- **相機反饋**：普攻命中觸發 1.5px 輕微水平微震（60ms）；怒氣大招終結一擊觸發 4.0px 全向徑向衝擊波震動（120ms）並伴隨 0.05 秒幀凍結（Hitstop），賦予法師武器極致爽快的打擊反饋。

---

## 五、 產品層准入（PRODUCT_LOCK_0.20.md §9 門檻自答）

依據《0.20 Product Lock》第 9 節規定，任何新增內容必須完整自答准入門檻六題，逐題檢驗合格方准備案：

### Q1：它掛在 §3.1 核心循環的哪一環？
> **合格回答**：**精準掛在「養成」與「解鎖玩具／發條」這一環。**  
> **詳細論證**：  
> 琉璃海馬並非孤立的新玩法，而是現有 7 大紙娃娃換裝體系（`mob-paperdoll`）在前二十二族基礎上的「第 23 款可解鎖動物素體外殼（Chassis）」。玩家透過通關 R05 琉璃汪洋·發條海淵章節探索獎勵、擊破旗艦 BOSS·深淵海霸泰坦·八爪機關巨烏賊掉落稀有素材「澄澈深海藍晶核」與「鍍鈦耐腐蝕增壓閥」在水下發條宮殿工坊組裝解鎖、或外觀盲盒抽取獲得；解鎖後完全複用客戶端既有的武器鍛造、十四星軸入魂、怒氣技能樹三層養成鏈，百分之百依循 `探索 → 戰鬥 → 掉落 → 養成 → 解鎖玩具／發條 → 新區域 → 劇情` 的唯一直線主循環。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
> **合格回答**：**同時服務第 1 支柱（第一優先）與第 2 支柱（第二優先）。**  
> **詳細論證**：  
> 1. **服務第 1 支柱（第一優先：世界與角色）**：補強 R05 琉璃汪洋·發條海淵長久以來僅有一種原生動物（浪花海獺）的嚴重失衡生態！以多巴胺天藍琺瑯烤漆、象牙米白陶瓷面龐、三叉齒輪晶冠與珊瑚晶金三叉戟發條鑰匙，塑造出高雅、智慧、沉靜守護的深海學者形象，深化「在萬米凝膠海淵深處依然有晶瑩剔透的童話發條在跳動」的宏大奇想世界底色。  
> 2. **服務第 2 支柱（第二優先：即時戰鬥演出）**：2.2 頭身垂直 S 型挺拔剪影、螺旋板簧尾部接地姿態、右手懸引浮空多面藍晶星盤極其獨特，配合洋流阻尼蓄力射擊與怒氣大招潮汐星陣暴發，確保「在手機小螢幕上即使 10 秒無 UI 也能一眼看出是琉璃海馬在優雅施法」，補全法師水晶武器長久以來僅有玄機龜單一素體的缺口。

### Q3：玩家在手機上用單手拇指能不能操作它？
> **合格回答**：**100% 能。**  
> **詳細論證**：  
> 琉璃海馬完全沿用現有的橫屏雙拇指手遊人體工學架構：創角與衣櫥換裝卡片熱區均 ≥ 48px，杜絕誤觸；戰鬥中點擊單鍵即可順暢完成普攻聚焦射擊、蓄力浮力懸停引導與全螢幕怒氣大招釋放，絕無複雜多指搓招或虛擬搖桿拖曳負擔，完全保留單手大拇指暢玩之流暢體驗。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
> **合格回答**：**完全不需要。**  
> **詳細論證**：  
> 琉璃海馬的素體結構、貼圖切片與動畫參數全部離線封裝於客戶端本機資料庫。在離線無網路狀態下，玩家可順暢創建角色、換裝與通關全主線副本，嚴格恪守 §6「保留零連線可通關」原則。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
> **合格回答**：**絕對不會。**  
> **詳細論證**：  
> 單一套動物素體的完整 2D 資產清冊包括：400×840 官方立牌（約 220 KB）、128×128 戰鬥 6 姿態圖（約 120 KB）、7 槽位局部切片圖層（約 170 KB），經 TinyPNG / WebP 壓縮後，總資產增量嚴格控制在 **0.8 MB 以內**。⚠️ 需特別注意 `PRODUCT_LOCK_0.20.md` §5.2 記載之現況為「Web 目錄 135 MB」、首包目標 50～80 MB，**目前尚未達標**；本族的 0.8 MB 增量相對於該既有缺口極小，但首包瘦身是專案既有欠帳，不因本提案而消解。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
> **合格回答**：  
> 1. **放棄為海馬繪製生物魚鱗、濕滑黏液、生肉鰓裂與軟體魚鰭的奢想**：放棄一切高功耗的液體流體即時運算與魚皮物理模擬，嚴格將材質收斂為「耐壓鍍鈦沖壓板件、象牙米白陶瓷面頰、雙層高韌性薄荷矽膠背鰭與螺旋錳鋼板簧尾」，並嚴格遵循 `weapon_classes.json` 的 `crystal` 數值與已鎖定之 `BALANCE.md` §5 時間模型（0.15），捍衛低階手機流暢度與戰鬥平衡。  
> 2. **放棄冰冷陰森的深海克蘇魯或恐怖怪物設定**：嚴禁使用幽閉陰暗、腐朽生鏽或恐怖深淵怪物設定，嚴格將深海美學轉譯為「多巴胺天藍（#38A0FF）、薄荷海藍（#2EC4B6）、象牙米白（#FFFDF8）與珊瑚晶金（#FFD028）」，展現發條玩具在琉璃海淵中宛如水晶宮殿學者般純真好奇的浪漫奇想，捍衛全年齡熱血童話核心。

---

## 六、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

後續待審核通過後，可直接映射併入 `docs/design/paperdoll_slots.json` 之結構化配置段落如下（僅供資料規格備案，本任務不直接竄改主檔）：

```json
{
  "race_id": "seahorse",
  "race_name_zh": "琉璃海馬",
  "race_name_en": "The Crystal Seahorse",
  "native_profession": "mage",
  "native_weapon_class": "crystal",
  "starter_weapon_id": "shard_focus",
  "native_realm_id": "R05",
  "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
  "lore_anchor": [
    "水下發條宮殿",
    "藍晶石海淵平原",
    "海淵地表與馬賽克步道",
    "發條珊瑚群",
    "深淵排污豎井管道·耐壓吊籠"
  ],
  "palette": {
    "primary_hull": "#38A0FF",
    "secondary_hull": "#2EC4B6",
    "faceplate_enamel": "#FFFDF8",
    "gold_accent": "#FFD028",
    "coral_pink": "#FF5E8A",
    "crystal_core": "#1C54B2",
    "titanium_frame": "#7A8B99",
    "outline": "#1F1A3A"
  },
  "winding_key_spec": {
    "key_id": "key_seahorse_trident_coral_spire",
    "name_zh": "三叉戟珊瑚晶簇黃銅發條鑰匙",
    "name_en": "Trident Coral-Crystal Winding Key",
    "position": "back_center_high",
    "rotation_sound": "sfx_steam_windup_chime"
  },
  "slots_manifest": {
    "chassis": "chassis_seahorse_abyssal_cyan_default",
    "head_unit": "head_seahorse_crown_visor",
    "costume": "costume_seahorse_abyssal_scholar_harness",
    "optic_core": "optic_seahorse_ocean_sapphire",
    "winding_key": "key_seahorse_trident_coral_spire",
    "weapon": "weapon_seahorse_abyssal_prism_astrolabe",
    "curio": "curio_seahorse_twin_propeller_fins"
  },
  "pending_assets": [
    "game/assets/sprites/player/paperdoll/seahorse/chassis/chassis_seahorse_abyssal_cyan_default.png",
    "game/assets/sprites/player/paperdoll/seahorse/head_unit/head_seahorse_crown_visor.png",
    "game/assets/sprites/player/paperdoll/seahorse/costume/costume_seahorse_abyssal_scholar_harness.png",
    "game/assets/sprites/player/paperdoll/seahorse/optic_core/optic_seahorse_ocean_sapphire.png",
    "game/assets/sprites/player/paperdoll/seahorse/winding_key/key_seahorse_trident_coral_spire.png",
    "game/assets/sprites/player/paperdoll/seahorse/weapon/weapon_seahorse_abyssal_prism_astrolabe.png",
    "game/assets/sprites/player/paperdoll/seahorse/back_curio/curio_seahorse_twin_propeller_fins.png",
    "game/assets/sprites/player/paperdoll/key/key_seahorse_trident_coral_spire.png",
    "game/assets/sprites/player/paperdoll/weapon/weapon_seahorse_abyssal_prism_astrolabe.png",
    "game/assets/sprites/player/paperdoll/seahorse/proof_paperdoll_seahorse_composite.png",
    "game/assets/sprites/player/paperdoll/seahorse/proof_paperdoll_seahorse_magenta.png",
    "game/assets/sprites/player/paperdoll/seahorse/proof_seahorse_all_7_slices.png",
    "game/assets/sprites/player/battle/seahorse/seahorse_battle_poses_128.png",
    "game/assets/sprites/player/showcase/seahorse_idle_hd.png"
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
│ 1. 400×840 官方立牌展台圖 (seahorse_idle_hd.png)             │ ~480 KB       │ ≤ 220 KB     │
│ 2. 128×128 戰鬥六姿態精靈圖 (6 幀 768×128 條狀圖)           │ ~240 KB       │ ≤ 110 KB     │
│ 3. 7 大紙娃娃獨立槽位切片圖層 (128×128 RGBA8888 × 7)         │ ~320 KB       │ ≤ 160 KB     │
│ 4. 通用目錄鏡像檔 (key/ 與 weapon/ 兩枚圖示)                 │ ~60 KB        │ ≤ 30 KB      │
│ 5. 驗收合成圖與洋紅邊界校驗圖 (僅存證，不打包進 Release)     │ [Dev Only]    │ [0 KB 首包]  │
├──────────────────────────────────────────────────────────────┼───────────────┼──────────────┤
│ 總計（加入首包之正式 Release 資產增量）                      │ ~1.10 MB      │ ≤ 0.52 MB    │
└──────────────────────────────────────────────────────────────┴───────────────┴──────────────┘
```

- **包體欠帳與門檻說明**：
  - 據實核對現狀：`PRODUCT_LOCK_0.20.md` §5.2 明載當前專案 Web 目錄為 135 MB，距離目標 50~80 MB 尚在收斂推進中，本提案嚴格保證單族增量 < 0.8 MB，不增加額外首包負擔。

### 7.2 執行期記憶體與 Token 成本評估（Runtime & Token Cost）

1. **客戶端記憶體與 DrawCall 負載**：
   - 琉璃海馬 7 大槽位切片完全複用既有的 2D 紙娃娃 CanvasItem 著色器（`sprite_db.gd`），不新增額外材質 Pass；
   - 單一角色待機狀態佔用 VRAM 約 1.0 MB，符合行動裝置低階 2GB RAM 設備同屏 10 人流暢 60 FPS 規範。
2. **LLM 描述與資料結構 Token 預算**：
   - 機器讀取規格配置段落（JSON）嚴格控制在 310 ~ 340 tokens 之間；
   - 欄位命名嚴格遵循既有 `paperdoll_slots.json` 規範，避免冗餘深層巢狀結構，大幅降低後續 Agent 在解析、檢索與代碼生成時的 Prompt 上下文開銷。

---

## 八、 驗收 Checklist（對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **CANON.md 零毛皮鐵律**：100% 零真魚鱗、零黏液、零魚鰓、零毛皮、零肉身、零肉墊、零軟組織；全數轉譯為沖壓耐腐蝕鍍鈦合金板件、象牙米白陶瓷面頰與胸甲、三叉齒輪晶冠頂盔、高韌性矽膠雙聯背鰭、雙聯深海藍寶石透鏡目鏡、三叉戟珊瑚晶簇黃銅發條鑰匙與三柱微型液壓接地足。
- [x] **CANON.md 背部發條鑰匙**：背部高位動力插座配備「三叉戟珊瑚晶簇黃銅發條鑰匙」，拋光黃銅三叉戟造型，中央鑲嵌深海藍晶石，旋轉伴隨清脆齒輪自鎖與水壓微氣閥排氣聲「叮——哧！」。
- [x] **review.md 23f-1 職業正式名稱**：正式名稱精準採用單一規範名：**`法師 (Mage)`**，完全依據 `weapon_classes.json` 規範名，無任何自創新名。
- [x] **review.md 0-MKT7 單持武器規範**：右手單持懸引專利深海靈晶浮空星盤，左手空手自然微曲作引導水流阻尼與晶盾編織之法術起手架式，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- [x] **既有武器 ID 嚴格對齊**：精準對應 `equipment.json` 第 392 行既有 `shard_focus`（碎晶聚能）與第 405 行 `prism_scepter`（棱鏡權杖）；專屬款式 `weapon_seahorse_abyssal_prism_astrolabe` 明確標註待審，底層掛載 `crystal` line，不准自行創造未審 id。
- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：`lore_anchor` 所載「水下發條宮殿」、「藍晶石海淵平原」、「海淵地表與馬賽克步道」、「發條珊瑚群」與「深淵排污豎井管道·耐壓吊籠」逐字比對 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 第 20 行、第 21 行、第 29 行、第 236 行、第 237 行與第 238 行 100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（首包數字查驗）**：據實引用 `PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有二十二族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 22 族（含第 21 族棘輪刺蝟與第 22 族荒原鋼狼）。
- [x] **世界觀十四主星對齊**：掛載 R05 特產之「天府星軸（固甲之魂 / Tian Fu Core）」與「太陰星軸（旋簧之魂 / Tai Yin Core）」，象徵鍍鈦抗壓固甲、深海螺旋板簧與澄澈靈動的法術防禦。
- [x] **職業與武器平衡**：補足法師職業下轄 `crystal`（水晶 / 法師·晶）僅有第 10 族玄機龜單一素體之缺口，達成法師職業（杖 2、晶 2）對等平衡，使戰士、遊俠、忍者、騎士、法師五大核心職業全數達成完全對稱平衡，並使 R05 琉璃汪洋從單一素體拓展為雙素體守護陣容。
- [x] **7 大紙娃娃槽位完整度**：Slot 1~7 涵蓋 chassis / head_unit / winding_key / costume / optic_core (accessory) / weapon / curio (back_curio)，命名規則與擴充款式定義完備，可供美術直接產切片。
- [x] **純文件交付邊界**：嚴守任務要求，未產圖、未產片、零花費、未改動底層程式碼與正式 `paperdoll_slots.json` 權威檔。

---

## 九、 六語系在地化對照表（Localization Lexicon）

| 專有名詞分類 | 繁體中文 | 簡體中文 | 英文（EN） | 西班牙文（ES） | 日文（JA） | 韓文（KO） |
|:---|:---|:---|:---|:---|:---|:---|
| **角色全名** | 琉璃海馬 | 琉璃海马 | The Crystal Seahorse | El Caballito de Cristal | 琉璃のタツノオトシゴ | 유리 해마 |
| **角色頭銜** | 海淵星象學者·宮殿守護者 | 海渊星象学者·宫殿守护者 | Abyssal Astronomer: Palace Sentinel | Astrónomo Abisal: Centinela del Palacio | 海淵の星象学者・宮殿の守護者 | 심연의 점성학자·궁전의 수호자 |
| **原生武器** | 深海靈晶浮空星盤 | 深海灵晶浮空星盘 | Abyssal Prism Astrolabe | Astrolabio de Prisma Abisal | 深海霊晶浮遊アストロラーベ | 심해 영정 부유 아스트롤라베 |
| **專屬發條鑰匙**| 三叉戟珊瑚晶簇黃銅鑰匙 | 三叉戟珊瑚晶簇黄铜钥匙 | Trident Coral-Crystal Brass Key | Llave de Latón Coralino Tridente | 三叉戟珊瑚晶クラスタ真鍮ぜんまい鍵 | 삼지창 산호 결정 황동 태엽 열쇠 |
| **頭部頂盔** | 沖壓高透石英水晶冠冕頂盔 | 冲压高透石英水晶冠冕顶盔 | Stamped Quartz Crown Visor | Corona Estampada de Cuarzo Marino | プレス高透明石英水晶クラウン兜 | 프레스 고투명 석영 크리스털 크라운 투구 |
| **面部光學** | 雙聯深海藍寶石透鏡目鏡 | 双联深海蓝宝石透镜目镜 | Twin Ocean Sapphire Optical Core | Lentes Ópticas Dobles de Zafiro Oceánico | 複眼深海サファイア光学レンズ | 복안 심해 사파이어 광학 렌즈 |
| **核心背飾** | 雙聯微型發條螺旋推進晶鰭 | 双联微型发条螺旋推进晶鳍 | Twin Clockwork Propeller Fins | Aletas Propulsoras Mecánicas Dobles | ぜんまい式二連スクリュー推進ヒレ | 태엽식 2연장 스크루 추진 지느러미 |
| **核心招式 1** | 藍晶聚光穿刺 | 蓝晶聚光穿刺 | Prism Light Ray Thrust | Estocada de Rayo Prismático | 藍晶集光ピアッシング | 남정 집광 관통 |
| **核心招式 2** | 潮汐星陣暴發 | 潮汐星阵暴发 | Tidal Constellation Burst | Explosión de la Constelación de Marea | 潮汐星陣バースト | 조석 성진 폭발 |
| **核心機制** | 洋流阻尼浮力下墜重擊 | 洋流阻尼浮力下坠重击 | Hydro-Damping Buoyancy Plunge | Golpe Descendente con Amortiguación | 水流減衰浮力急降下撃 | 수류 감쇠 부력 급강하 타격 |
