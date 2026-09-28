# 第五十一種動物「墨影烏賊（The Inksmoke Cuttlefish）」世界觀與角色設計提案

> **標題**：第五十一種動物「墨影烏賊（The Inksmoke Cuttlefish）」角色與世界觀設計提案  
> **提案代號**：`INKSMOKE_CUTTLEFISH_DESIGN_PROPOSAL`（代號：`cuttlefish` / 識別名：`race_cuttlefish`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_89ff2601`（📖 世界觀｜第五十一種動物紙娃娃角色設計提案（只寫文件，不產圖不產片））  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零真鱗片、零生物血肉、零軟組織、零生物黏液、高耐壓防腐鍍鈦合金板件、深海石英琉璃泡罩、氣動洩壓雙聯氣閥、外露螺栓鉚釘、背後必有發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R05_CRYSTAL_OCEAN.md`（第 1 行區域代號與名稱「R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss」、第 4 行「高透光海藍琉璃凝膠、耐高壓深海石英泡罩、防腐蝕鍍鈦合金骨架、發條磁吸氣動閥門與磷光發條指針儀表套件」、第 6 行「局域走時狀態：深沉緩慢伴隨水壓流體阻尼（秒針每 3~4 秒深沉划動一格，伴隨液態凝膠微波泛起藍光漣漪；水下流體阻尼沉穩舒緩，需掌握發條流體浮力與減壓循環穿行）」、第 19 行「液態琉璃凝膠海（Liquid Crystal Gel Sea）」、第 20 行「海淵地表與馬賽克步道（Abyssal Seabed & Mosaic Walkways）」與「深海藍晶石馬賽克瓷磚（Lapis Lazuli Mosaic Tiles）」、第 20 行「發條珊瑚群（Clockwork Coral Reeds）」、第 21 行「水下發條宮殿與氧氣泡罩（Clockwork Sunken Palace & Aerated Glass Domes）」、第 22 行「磷光水母街燈與流體排氣柱（Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents）」、第 24 行「水下丁達爾藍晶光柱（Submarine Caustic Godrays）」、第 25 行「天頂巨型青銅錨鏈秒針」、第 29 行「深淵排污豎井管道·耐壓吊籠（Abyssal Sump Siphon: Bathysphere Terminal）」、第 30 行「晨曦天軌 5 號深海浮標月台（Dawn Rail Deepsea Buoy Platform 5）」、第 32 行「深海熱液湧泉管道（Hydrothermal Trench Conduits）」、第 34 行「環域水幕磁阻防護波（Magnetic Hydro-Barrier Grid）」、第 42 行「發條熱帶魚（Clockwork Tropical Fish）」、第 43 行及第 54 行「小黃鴨船長·舵手巴克（Captain Buck）」、第 44 行及第 63 行「海馬信差·碧浪（Billow）」、第 71 行「深海鐘錶貝·珠貝長老（Elder Pearl）」、第 85 行「生鏽的發條深海鮟鱇（Rusty Clockwork Angler）」、第 89 行「錨鏈幽靈水母（Anchor-Chain Phantom Jelly）」、第 93 行「巡弋重裝機關鯊（Armored Patrol Mecha-Shark）」、第 100 行旗艦泰坦 BOSS「深淵海霸泰坦·八爪機關巨烏賊（Titan Abyssal: Octo-Gear the Abyssal Kraken）」、第 107 行「錨鏈重腕（Anchor Tentacles）」、第 108 行「頂部排水氣閥（Crown Siphon Vent）」、第 109 行「主目鏡水晶罩（Optic Glass Dome）」、第 111 行「海潮發條主擺輪」、第 119 行特產武器「海錨防禦重斧」、第 120 行「琉璃刺擊長槍」、第 121 行「發條雙管水銃」、第 123 行核心掉落「澄澈深海藍晶核（Pure Abyssal Blue Quartz Core）」、「鍍鈦耐腐蝕增壓閥」、「深海抗壓錨鏈鉸鏈」、「防鏽特種矽油」、第 129 行「天府星軸（固甲之魂 / Plated Iron Core）」、第 130 行「太陰星軸（旋簧之魂 / Coiled Spring Core）」、第 139 行「潮汐迴旋斬」、第 140 行「氣泡踏浪衝」、第 151 行第五章「琉璃之海與沉睡巨錨」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（忍者正式名稱 `ninja`，匕首標籤宣言 `\"藏在袖裡的殺意\"`，武器 `dagger`，數值 `atk: 3, def: 0, hp: -4, crit: 4.0, speed: 2`，新手武器 `star_fang`）  
> - `game/data/tables/equipment.json`（短匕正式 line: `\"dagger\"`，初階武器：第 158 行 `star_fang` 星牙短匕，高階相容武器：第 171 行 `nebula_needle` 星雲細針）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第九巡（第 49~54 族）第三順位接棒，強勢開啟「忍者 (Ninja)」短匕體系重大擴充**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十一種動物擴充素體規格**。  
   在全專案跨越「前 48 族完全對稱平衡大圓滿」，並相繼由第 49 族熔鎧犰狳（騎士·長劍）與第 50 族風箱毛蟲（戰士·戰鎚）成功開啟第九巡篇章後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第九巡第三順位**，輪轉進入最具匿影爆發與致命連擊的核心職業——**忍者 (Ninja)** 體系，原生武器掛載於**短匕（`dagger` / 忍者·匕）**。  
   墨影烏賊的加入，使全遊戲忍者短匕素體擴充至第 5 款（忍者總族群擴充至 9 款），為第九巡注入極致的深海匿影與高速刺殺動能！
2. **經典玩具起源與古典水下發條烏賊自動機工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與鐘錶氣動煙幕自動偶史上的經典工藝原型：  
     ① **19 世紀末至 20 世紀中葉古典鐵皮發條潛水烏賊玩具（Vintage Tinplate Wind-up Diving Squid/Cuttlefish Automaton）**，通體由沖壓防腐鍍鈦薄板、微型水下螺旋推進軸與深海藍搪瓷拼合，內部發條帶動側鰭柔性波浪擺動，是古典發條玩具史上最具流體動態與深海浪漫魅力的自動偶之一；  
     ② **古典鐘錶水下氣動發煙機關偶（Horological Submarine Pneumatic Aerosol Automaton）**，背載微型發條驅動之雙聯高壓氣動墨囊氣罐，在指針跳動間隙吸納流體並瞬間噴發高壓微氣泡與無毒深藍色流體煙霧，製造視覺盲區盲刺對手；  
     ③ **古典發條深海刺客偶（Vintage Clockwork Abyssal Shinobi Automaton）**，以 2.2 頭身矮萌圓頂深潛頭盔、流線型抗壓胸甲與分節合金觸腕，完美詮釋忍者職業「貼身爆發高、森羅連刺節奏兇、藏在袖裡的殺意」之忍者之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「沖壓鍍鈦與琉璃海藍搪瓷素體底盤、深潛圓頂頭盔與氣動平衡側鰭、三葉深海渦輪水流發條鑰匙、海淵夜行輕量耐壓背心、雙聯水下耐壓石英探照目鏡、海淵墨影雙鋒匕與氣動高壓發煙雙聯墨囊氣罐」之深海刺客短匕素體（Titanium Cyan-Enamel Chassis, Diving Cowl with Balance Fins, Tri-Vane Turbine Key, Abyssal Shinobi Cuirass, Dual Quartz Optic Lens, Abyssal Inksmoke Twin Daggers & Pneumatic Ink-Siphon Pack）**。
3. **生態補足：徹底終結琉璃汪洋·發條海淵（R05）零忍者之歷史空白，打造深海發條宮殿第一影行者**：  
   在全遊戲 9 大界域中，中低層水域沙盤界域 `R05 琉璃汪洋·發條海淵` 先前僅有浪花海獺（戰士·斧）、琉璃海馬（法師·晶）、破浪旗魚（騎士·槍）與拍浪海豹（武術家·拳）共 4 族，不僅是全遊戲種族數量最稀少之界域，更長期以來**完全缺乏一位能借助液態凝膠水壓阻尼掩護、以高壓氣動墨囊釋放瞬態煙幕、手持雙鋒短匕在丁達爾光柱暗角執行弱點刺殺的「忍者 (Ninja)」核心素體**。墨影烏賊的降臨，徹底填補了 R05 長期零忍者素體的生態空白，讓深海琉璃宮殿擁有了最神祕凌厲的暗影守護者！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：墨影烏賊素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十族武器與職業光譜全盤點

盤點現有首發五族與前四十五款擴充族（總計 50 族）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

- **白金兔（Clockwork Rabbit）**：騎士 (Knight) —— 單手長劍（`sword`），平衡攻防，中近距離。
- **烈鬃獅（Gilded Lion）**：騎士 (Knight) —— 皇家長槍（`spear`），中距控場，格擋迎擊。
- **靈尾狐（Astral Fox）**：法師 (Mage) —— 秘術法杖（`magic`），遠程法術，技能爆發。
- **鋼牙豕（Forge Boar）**：戰士 (Viking) —— 鍛爐巨鎚（`hammer`），高防厚重，部位破壞。
- **靈爪猴（Spring Macaque）**：武術家 (Monk) —— 機關靈爪（`claw`），彈簧伸縮臂，近身連打破勢。
- **烈焰虎（Ember Tiger）**：忍者 (Ninja) —— 齒輪雙斬刃（`dagger`），伏擊撕裂，近戰極限暴擊。
- **雲嵐鶴（Cloud Crane）**：遊俠 (Ranger) —— 風弦羽翼機關弓（`bow`），超視距狙擊，遠程精準破甲。
- **玄軸熊（Iron Bear）**：戰士 (Viking) —— 玄軸偏心重力錘（`hammer`），磐石壁壘，大範圍震波。
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
- **鐵拳袋鼠（The Boxer Kangaroo）**：武術家 (Monk) —— 氣壓活塞雙拳套 / 衝壓黃銅拳套（`fist`），西洋拳擊步法，活塞洩壓重拳。
- **巡林松鼠（The Timber Squirrel）**：騎士 (Knight) —— 翡翠發條細劍 / 穿林機關花劍（`sword`），西洋花劍高速穿刺，停拍看破突進。
- **熔火蜥蜴（The Magma Salamander）**：戰士 (Viking) —— 熔爐衝壓巨錘（`hammer`），氣動垂直衝壓，洩壓熱浪排氣。
- **竹影青蛇（The Bamboo Viper）**：忍者 (Ninja) —— 疾風竹影短匕（`dagger`），柔韌波浪遊動身法，竹梢彈跳疾刺。
- **疾影神隼（The Swift Falcon）**：武術家 (Monk) —— 疾影穿雲機關爪（`claw`），高空俯衝撕裂，風影殘影連續爪痕。
- **星盤靈羊（The Astral Ram）**：法師 (Mage) —— 星軌游絲共鳴杖（`magic`），失重星軌引力轟擊，游絲共振廣域天體脈衝。
- **幻彩變色龍（The Mirage Chameleon）**：遊俠 (Ranger) —— 幻彩棱鏡複合機關弓（`bow`），光學干涉迷彩伏擊，雙向砲塔獨立測距貫穿。
- **破浪旗魚（The Hydrofoil Sailfish）**：騎士 (Knight) —— 破浪螺旋合金衝刺長槍（`spear`），深海流體破浪突刺，洋流阻尼彈射貫穿。
- **重角犀牛（The Heavyhorn Rhino）**：戰士 (Viking) —— 熔爐破陣重鋼戰斧（`axe`），直線衝壓重劈，黑曜淬火碎甲。
- **星翼蝙蝠（The Starwing Bat）**：忍者 (Ninja) —— 超導脈衝星紋鏢（`dart`），失重立體懸停，高頻聲納弱點鎖定。
- **鋼臂巨猩（The Steelarm Gorilla）**：武術家 (Monk) —— 高壓蒸氣鍛打拳套（`fist`），重裝前臂鐵壁封架，活塞衝壓直拳破勢。
- **稜鏡孔雀（The Prism Peacock）**：法師 (Mage) —— 萬花筒聚能稜鏡（`crystal`），萬花折光幾何光刃，織盾成刃光學護體。
- **沙哨狐獴（The Sentry Meerkat）**：遊俠 (Ranger) —— 生鏽彈簧刺銃（`gun`），直立潛望測距狙擊，三腳金屬尾接地抗後座。
- **鐵蹄駿駒（The Ironhoof Courser）**：騎士 (Knight) —— 晨曦齒輪騎兵劍（`sword`），古典旋轉木馬戰馬衝鋒，奔馳半月破陣橫斬。
- **劈木河狸（The Woodchopper Beaver）**：戰士 (Viking) —— 深林拓荒劈木巨斧（`axe`），工程伐木工兵，穿孔重尾三點定位破障重劈。
- **旋刃伶鼬（The Whirling Stoat）**：忍者 (Ninja) —— 廢土旋刃弧光短匕（`dagger`），狹管穿梭幽影，多節同軸平衡尾迴旋斬。
- **拍浪海豹（The Clapping Seal）**：武術家 (Monk) —— 琉璃氣動拍浪拳套（`fist`），深海流體推手，雙鰭齒輪對拍氣動破勢。
- **星儀渡鴉（The Armillary Raven）**：法師 (Mage) —— 渾天星儀發條短杖（`magic`），天文星圖測繪，同軸渾天聚焦天頂光柱。
- **熱流赤鳶（The Thermal Kite）**：遊俠 (Ranger) —— 熱流淬火複合機關弓（`bow`），升空熱流滑翔俯衝速射，淬火重彈反曲破甲爆轟。
- **旋音天鵝（The Melodic Swan）**：騎士 (Knight) —— 八音螺旋穿刺長槍（`spear`），晨曦芭蕾滑步迎擊，八音音筒多節長頸優雅控場。
- **撼地野牛（The Groundshaker Bison）**：戰士 (Viking) —— 廢土重砧碎鐵巨鎚（`hammer`），荒漠舊庫拆解工程，工字鋼角與重砧粉碎破障。
- **巡管守宮（The Conduit Gecko）**：忍者 (Ninja) —— 黃銅棘輪多角機關鏢（`dart`），高空管網附著倒掛，微型間歇吸盤突襲，多角折射伏擊。
- **破星蜜獾（The Starbreaker Honey Badger）**：武術家 (Monk) —— 逐星裂空機關爪（`claw`），失重冷氣反推向量衝鋒，合金爪正面撕裂防線。
- **澄心水豚（The Serene Capybara）**：法師 (Mage) —— 澄心太極護體靈晶（`crystal`），太極流體阻尼與心境定力，安詳圓融織盾成刃。
- **振律啄木鳥（The Resonance Woodpecker）**：遊俠 (Ranger) —— 振律重型氣動火銃（`gun`），高空垂直管道測振錨定，長筒高壓氣動重銃狙擊，三點抗震尾板支撐點射。
- **熔鎧犰狳（The Crucible Armadillo）**：騎士 (Knight) —— 玄鐵重破大劍（`sword`），黑曜高溫淬火重斬，重裝板甲反震攻堅。
- **風箱毛蟲（The Bellows Caterpillar）**：戰士 (Viking) —— 蔓谷風箱重壓鎚（`hammer`），手風琴式蓄壓定點夯擊，節律減震站到最後。

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 忍者（Ninja）此前在 50 族中擁有 8 款動物素體（短匕 4 款、機關鏢 4 款）；
- **本提案第五十一種動物正式作為「第九巡第三順位」接棒啟動擴充，歸屬於忍者 (Ninja) 體系，原生武器掛載於 `dagger`（短匕 / 忍者·匕）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`忍者 (Ninja)`**；
- 墨影烏賊的加入，使全遊戲忍者短匕素體擴充至第 5 款，為即將展開的第九巡打造最極致的深海暗影匿蹤與弱點背刺體系！

### 1.2 墨影烏賊武器選擇：【海淵墨影雙鋒匕（Abyssal Inksmoke Twin Daggers）】

墨影烏賊原生專屬武器定名為：**【海淵墨影雙鋒匕（Abyssal Inksmoke Twin Daggers）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 琉璃汪洋·發條海淵之深海暗影匿行體系**！  
底層完全掛載於 `weapon_classes.json` 的 `dagger`（忍者·匕）類別，享有 `dagger` 既有的「藏在袖裡的殺意」標籤宣言（Tagline: `\"藏在袖裡的殺意\"`）、貼身爆發高、森羅連刺節奏兇、暴擊好之特性（`atk: 3, def: 0, hp: -4, crit: 4.0, speed: 2`），完美呼應 `R05_CRYSTAL_OCEAN.md` 第 6 行「秒針每 3~4 秒深沉划動一格，伴隨液態凝膠微波泛起藍光漣漪；水下流體阻尼沉穩舒緩」之深海暗影律動！

- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"dagger\"` 的初階裝備 `star_fang`（星牙短匕，tier 2）與高階相容裝備 `nebula_needle`（星雲細針，tier 3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款短匕忍者（烈焰虎、幽影貓、竹影青蛇、旋刃伶鼬）絕不撞型之論證

雖然墨影烏賊與烈焰虎、幽影貓、竹影青蛇、旋刃伶鼬同屬 `ninja`（忍者）短匕（`dagger`）體系，但在**匕法流派與刺殺哲學**、**機動體態與流體力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               忍者職業短匕系五族差異化對照表（虎 vs 貓 vs 青蛇 vs 伶鼬 vs 烏賊）                                    │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 烈焰虎 (Tiger)       │ 幽影貓 (Cat)         │ 竹影青蛇 (Viper)     │ 旋刃伶鼬 (Stoat)     │ 墨影烏賊 (Cuttlefish)│
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ ① 匕法與哲學   │ 齒輪雙斬暴烈伏擊     │ 匿夜暗影弧光背刺     │ 竹梢彈跳柔韌疾刺     │ 廢土狹管迴旋連割     │ 凝膠墨煙盲區弱點死刺 │
│                 │ (高溫撕裂極限暴擊)   │ (死線暗殺無聲影遁)   │ (波浪遊動多段滲透)   │ (多節平衡尾高速急旋) │ (氣動噴煙製造背刺盲區)│
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ ② 所屬界域     │ R06 赤焰熔爐·火山    │ R02 晨曦小鎮·鐘樓    │ R09 雲海竹林·道場    │ R08 荒漠齒輪塚·廢土  │ R05 琉璃汪洋·海淵   │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ ③ 核心力學動態 │ 猛獸撲躍、雙爪下壓   │ 輕盈腳步、躡足躍起   │ 彈性蛇行、波浪遊動   │ 低矮細長、竄動平衡   │ 氣動虹吸、流體滑行  │
│                 │ (剛猛衝擊暴烈重斬)   │ (無聲肉球踏步背刺)   │ (關節S型折疊疾刺)    │ (離心擺動狹縫穿梭)   │ (微型反推破水滑翔)  │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ ④ 剪影輪廓特徵 │ 鋼鐵虎耳、鋸齒雙刃   │ 貓耳立挺、短小雙匕   │ 扁平蛇頭、竹節細刃   │ 細長立耳、多節長尾   │ 圓頂頭盔、兩側游動鰭│
│                 │ (黑鐵赤金、熱浪排氣) │ (午夜墨藍、暗銀發條) │ (竹青烤漆、纖巧翠綠) │ (象牙白鐵皮、黑尖尾) │ (海藍搪瓷、鍍鈦雙匕)│
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ ⑤ 戰鬥角色定位 │ 熔岩高熱過載突進     │ 陰影死角潛行獵手     │ 高速彈跳破綻打擊     │ 廢土狹道多段收割     │ 流體阻尼「煙幕遁術」 │
│                 │ (狂暴伏擊撕裂重創)   │ (高命中死線瞬殺)     │ (柔性機動連環點殺)   │ (高敏捷暴風撕扯)     │ (破水匿蹤、爆發連刺) │
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

1. **匕法流派與刺殺哲學差異**：  
   - **烈焰虎**主打「**高溫撕裂猛撲**」，依託 R06 赤焰熔爐，以齒輪高速旋轉的雙斬刃強行撕裂重甲；  
   - **幽影貓**主打「**暗夜死線背刺**」，依託 R02 晨曦小鎮鐘樓陰影，以消音發條踏步實現絕對無聲的單點死線狙殺；  
   - **竹影青蛇**主打「**竹梢柔韌滲透**」，依託 R09 雲海竹林，藉助多節竹骨的柔韌彈跳在枝梢間遊動穿刺；  
   - **旋刃伶鼬**主打「**狹管高速迴旋**」，依託 R08 荒漠廢土，以多節配重尾維持離心平衡，在管道狹縫中疾旋雙刃；  
   - **墨影烏賊**則主打「**水下煙幕盲區死刺（Inksmoke Ambush）**」，依託 R05 琉璃汪洋的液態凝膠與丁達爾光柱，利用背部高壓氣動墨囊瞬間噴發深藍色發條微粒煙幕，在水波阻尼中製造對手 1.5 秒視覺盲區，雙足微型反推推進滑翔至敵後死角，施展精準致命的雙刃十字死線貫穿！

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格恪守世界觀根本大法 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md` 第 142 行之鐵律：**全域 100% 零真動物皮毛、零真鱗片角質、零生物血肉、零軟組織、零生物黏液**。墨影烏賊的一切自然生物特徵，全部純淨轉譯為童話古典發條機械、沖壓金屬、高透石英琉璃、防腐鍍鈦薄板與深海潛水玩具結構：

1. **烏賊軀幹轉譯 -> 沖壓鍍鈦與琉璃海藍搪瓷素體底盤（Titanium-Plated Chassis with Abyssal Cyan Enamel）**：  
   徹底杜絕生物軟體黏液與肉質觸感，身軀採用古典鐵皮發條潛水艇與深海探險偶工藝，由高強度防腐沖壓鍍鈦薄板（#38A0FF）與象牙白防滑瓷釉（#FFFDF8）拼合而成，表面經過雙層耐磨防鏽清漆烘烤，接縫處外露整齊的鍍銀圓頭鉚釘與細密發條密封圈。  
2. **烏賊頭部轉譯 -> 深潛圓頂頭盔與氣動平衡側鰭（Diving Cowl with Articulated Hydro-Fins）**：  
   自然界軟體頭部轉譯為一體沖壓成型的鐘形深潛圓頂頭盔，頂部配有微型黃銅洩壓閥門；頭部兩側對稱伸出一對由薄沖壓黃銅片鉸接而成的靈巧「波浪平衡側鰭（Articulated Brass Balance Fins）」，隨水流與走時律動輕微扇動，發出清脆的齒輪咬合聲。  
3. **烏賊雙眼轉譯 -> 雙聯水下耐壓石英探照目鏡（Dual Pressure-Proof Quartz Optic Lenses）**：  
   自然生物大眼轉譯為深嵌於頭盔眼眶內的圓形雙凸耐壓石英晶體透鏡，鏡面呈高透天藍（#38A0FF）與微光薄荷綠（#4ED86A）多巴胺冷色調，內置水平橫縫測距光柵與指針刻度圈，眼神專注凌厲而充滿玩具童趣。  
4. **烏賊觸腕轉譯 -> 四分節合金軟鋼觸肢滾輪短足（Segmented Alloy Tendon Skirt & Rolling Claws）**：  
   自然界十條柔軟觸手轉譯為下半身整齊排列的四對（共 8 條）短小精悍的分節金屬機械觸肢，由精密軟鋼絞線與微型黃銅套管穿套而成，末端配備微型防滑橡膠吸盤與小型鍍鈦滑輪，在海床馬賽克瓷磚上滑行無聲迅捷，矮萌可愛。  
5. **烏賊墨囊轉譯 -> 氣動高壓發煙雙聯墨囊氣罐（Pneumatic High-Pressure Ink-Siphon Pack）**：  
   自然生物墨囊轉譯為背部後側裝載的雙聯鍍鈦微型氣動氣罐，內部灌裝高密度無毒海藍色玩具發條微粒乾粉與流體凝膠，頂部裝設兩枚微型氣壓指針表與定向虹吸噴嘴，在施展煙幕遁術時噴射出絢麗的藍光微氣泡煙霧。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

為恪守 Kevin 指示之「**2.2 頭身 Q 版、深暖褐/藍紫描邊、亮色賽璐璐上色、嚴禁泥土暗黑髒灰**」之黃金規範，墨影烏賊之視覺色彩完全收斂於高工藝多巴胺色盤：

- **底色（Base）**：象牙白陶瓷釉 / 拋光鋁鎳金屬（#FFFDF8），用於面甲眼周高光、腹部內層襯板與關節活動襯墊，乾淨通透；
- **主色（Primary）**：多巴胺海天藍（#38A0FF），用於沖壓鍍鈦圓頂頭盔外殼、側鰭主體、雙鋒短匕護手與背部氣罐塗裝；
- **次色（Secondary）**：薄荷冷翡翠（#4ED86A），用於石英目鏡內部刻度發光圈、側鰭邊緣防撞膠條與短匕刃面高光；
- **點綴色（Accent）**：多巴胺珊瑚粉（#FF5E8A），用於發條鑰匙中心轉軸鉚釘、氣罐壓力警戒指針與頭頂洩壓氣閥按鈕；
- **金屬板件（Metal）**：拋光黃銅（#FFD028）與海軍深藍防鏽漆板（#1A3558），呈現深海發條鐘錶玩具的華麗與精緻感，絕非髒污泥土色；
- **描邊色（Outline）**：深藍紫/深暖褐（#1F1A3A），全域禁止髒黑與死黑，邊緣線條圓潤飽滿。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

為了徹底破除靜態立繪廉價感，賦予角色鮮活的玩具生命力，墨影烏賊規劃專屬動態表現：

- **待機呼吸律動（Idle Breathing & Hydrodynamic Rhythm）**：  
  2.2 頭身敦實渾圓的身軀保持每 3~4 秒一次的有節奏輕微起伏（完美契合 R05 琉璃汪洋秒針水壓流體律動），頭部兩側的黃銅波浪側鰭隨呼吸微微扇動；背部三葉渦輪發條鑰匙以沉穩均勻的速度旋轉；每隔 6 秒觸發專屬特寫小動作：烏賊警惕地向左右轉動石英目鏡，雙手反握的海淵雙鋒短匕在身前俐落地打了一個刀花「唰——鏘！」，隨後背後氣罐虹吸嘴俏皮地吐出兩串晶瑩剔透的小氣泡，伴隨一聲微弱的「咕嚕——啵」，可愛度破表。
- **選角與紙娃娃 Poke 點擊互動（Poke Interaction）**：  
  當玩家在選角大廳、紙娃娃衣櫥或冒險背包中點擊墨影烏賊時：  
  1. **動作切換**：烏賊如受驚般瞬間向後凌空翻滾半圈！背部雙聯墨囊「噗嗤！」一聲噴出一小團夢幻的淡藍色螢光煙霧；隨後它從煙霧中以極其帥氣的忍者蹲伏姿態破水滑出，雙手短匕交錯護胸，頭部石英目鏡驟然閃亮起耀眼的薄荷綠光芒；  
  2. **對話氣泡**：頭頂彈出圓滾粉圓體對話氣泡，顯示專屬台詞：「**水下的影子比光更致命！只要氣泡還沒散，我的匕首就已經到了！**」；  
  3. **粒子特效**：腳底滑行處爆散出數枚透明琉璃水珠、微型薄荷綠星芒與多巴胺珊瑚粉小氣泡粒子，展現深海忍者帥氣與童話矮萌的極致交融。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R05 琉璃汪洋·發條海淵（Crystal Ocean）零忍者歷史空白

在《發條之心》的 9 大宏偉沙盤界域中，中低層水域沙盤界域 `R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss` 擁有獨特的液態流體阻尼物理規則。然而在此之前，該界域僅有戰士（海獺）、法師（海馬）、騎士（旗魚）與武術家（海豹）四族駐留，全域**長期缺乏一位精通流體阻尼潛行、善用深海水壓盲區、執行弱點突襲的刺客職業**。  
墨影烏賊作為第九巡第三順位領銜者，其棲息地 100% 精確錨定於 R05 琉璃汪洋，終結了全遊戲唯一「無忍者沙盤大區」的歷史空缺！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 既有地標與設定

墨影烏賊的世界觀設定與背景故事，全面且嚴格地逐字對齊並深度嵌入 `docs/world/regions/R05_CRYSTAL_OCEAN.md`：

1. **棲息地標與生活場景**：  
   - 墨影烏賊一族世代棲息並巡邏於海淵核心的**「海淵地表與馬賽克步道（Abyssal Seabed & Mosaic Walkways）」**周邊；  
   - 牠們隱匿於由軟質矽膠與金屬彈簧組成的**「發條珊瑚群（Clockwork Coral Reeds）」**暗隙中，藉助珊瑚叢隨流體擺動發出的清脆輕響掩蓋自身的發條走時聲；  
   - 牠們是**「水下發條宮殿與氧氣泡罩（Clockwork Sunken Palace & Aerated Glass Domes）」**外圍防線最機敏的守衛者，負責守護高透石英玻璃外壁不受暴走機械水族的破壞；  
   - 在**「磷光水母街燈與流體排氣柱（Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents）」**的光影死角處，烏賊忍者們以冷色調搪瓷外殼融於多巴胺天藍（#38A0FF）與薄荷綠（#4ED86A）的光暈中，無影無形；  
   - 牠們穿梭於**「水下丁達爾藍晶光柱（Submarine Caustic Godrays）」**的光暗交界線，掌握光學折射角度實施絕對死角伏擊；  
   - 隨時仰望橫跨水下天際的**「天頂巨型青銅錨鏈秒針」**，在秒針每 3~4 秒划動一格、水波泛起藍光漣漪的瞬間發動高速突刺！
2. **交通接駁與哨卡職責**：  
   - 烏賊一族駐守於西北頂層水下接駁閘口**「深淵排污豎井管道·耐壓吊籠（Abyssal Sump Siphon: Bathysphere Terminal）」**，引導從 R04 巨輪城降入深海的冒險者；  
   - 定期巡視海面上層**「晨曦天軌 5 號深海浮標月台（Dawn Rail Deepsea Buoy Platform 5）」**下方錨鏈，清理攀附其上的海生發條水垢；  
   - 嚴密監控東南斷裂帶深處直通 R06 鍛造火山的**「深海熱液湧泉管道（Hydrothermal Trench Conduits）」**，防範熔岩熱流過載逆灌；  
   - 引導偏離航道的幼年玩具遠離沙盤邊緣危險區**「環域水幕磁阻防護波（Magnetic Hydro-Barrier Grid）」**。
3. **友好 NPC 互動羈絆**：  
   - 與**「小黃鴨船長·舵手巴克（Captain Buck the Rubber Ducky）」**是多年老友，巴克常載運烏賊一族特製的防鏽潤滑油，而烏賊則在水下為巴克的探險船護航，掃除暗礁機關；  
   - 與**「海馬信差·碧浪（Billow the Seahorse Courier）」**組合成深海默契雙人組，在水流湍急的珊瑚迷宮中互為前後哨，交換洋流情報；  
   - 定期前往**「深海鐘錶貝·珠貝長老（Elder Pearl the Clockwork Clam）」**座前，聆聽古老游絲調校心法，用長老傳授的消泡水壓諧振秘法打磨雙鋒短匕。
4. **與旗艦泰坦 BOSS「八爪機關巨烏賊」的宿命對照**：  
   - 面對暴走的超巨型守衛泰坦**「深淵海霸泰坦·八爪機關巨烏賊（Titan Abyssal: Octo-Gear the Abyssal Kraken）」**，墨影烏賊因同屬頭足類玩具工藝體系，對其精密機械弱點瞭若指掌；  
   - 在主角小白挑戰 BOSS 時，墨影烏賊作為關鍵戰術嚮導，指引小白精準定位三大拆卸部位：如何繞開**「錨鏈重腕（Anchor Tentacles）」**的橫掃死角、如何在釋放高壓水流時攀上**「頂部排水氣閥（Crown Siphon Vent）」**、以及如何借氣泡反衝打擊**「主目鏡水晶罩（Optic Glass Dome）」**，最終助小白贏得象徵海洋權限的**「海潮發條主擺輪」**！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據《發條之心》官方 7 大部件槽位規範（`paperdoll_slots.json`），墨影烏賊之 7 大槽位完整規劃如下：

```json
{
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_cuttlefish_abyssal_cyan_default",
    "display_name": "鍍鈦合金與琉璃海藍搪瓷素體底盤",
    "material": "高抗壓防腐鍍鈦薄板外殼（#38A0FF），嵌合象牙白防滑陶瓷釉襯板（#FFFDF8），下身配置四對分節軟鋼機械觸肢滾足與耐磨橡膠吸盤",
    "visual_features": "2.2 頭身矮萌流線型體態，圓潤緊湊，接縫處外露微型鍍銀防水螺栓，四對金屬小觸肢排列整齊，滑行步態輕快可愛，無任何生物黏液"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_cuttlefish_diving_cowl_fins",
    "display_name": "深潛圓頂頭盔與氣動平衡側鰭",
    "material": "沖壓成型鐘形鍍鈦深潛頭盔（#38A0FF），頂部裝配黃銅洩壓閥門（#FFD028），兩側對稱鉸接一對薄沖壓黃銅波浪平衡側鰭",
    "visual_features": "圓弧水滴型頭盔剪影，眼眶部位精準中空（max alpha=0）供 optic_core 透出，兩側側鰭微翹帶有細小齒輪鉸鏈，隨水流微動"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_cuttlefish_tri_vane_turbine_brass",
    "display_name": "三葉深海渦輪水流發條鑰匙",
    "material": "高剛性鍛造黃銅主軸搭配三葉螺旋渦輪扁平開孔旋葉（#FFD028），中央轉軸嵌裝多巴胺珊瑚粉鉚釘（#FF5E8A），配置微型水流阻尼軸承",
    "visual_features": "背部第三節正中垂直插入，三葉對稱螺旋槳幾何輪廓，旋轉時流暢均勻，剪影鮮明突破角色輪廓，去背邊緣銳利乾淨無雜質"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_cuttlefish_abyssal_shinobi_cuirass",
    "display_name": "海淵夜行輕量耐壓背心",
    "material": "深海耐磨防水海軍藍浸膠帆布（#1A3558），胸前加裝弧面天藍色沖壓胸甲（#38A0FF）與薄荷綠防撞包角（#4ED86A），肩部附帶金屬導流扣帶",
    "visual_features": "嚴格遵循 0-ART26b 上裝與下身解耦規範（y>=96 嚴格 0 像素無畫死下身），胸甲正中嵌裝深海浪花齒輪暗記，輕量貼身，兼具夜行刺客與童話水手質感"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_cuttlefish_dual_quartz_optic_lens",
    "display_name": "雙聯水下耐壓石英探照目鏡",
    "material": "澄澈高透耐壓石英晶體雙凸透鏡，表面鍍有高折射防反光藍綠干涉膜（#38A0FF），內置薄荷綠水平測距光柵與刻度指針（#4ED86A）",
    "visual_features": "鏡片中心精準對齊 head_unit 眼窩鏤空區域（min alpha=255），散發出幽微凌厲的藍綠冷光，透鏡外圈咬合微型黃銅調節齒圈"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_cuttlefish_abyssal_inksmoke_dagger",
    "display_name": "海淵墨影雙鋒匕",
    "material": "雙持鍍鈦弧刃短匕（#38A0FF），刀脊帶有深藍流體導槽與微型放血氣孔，黃銅護手刻有浪花浮雕（#FFD028），柄首配有配重平衡螺母",
    "visual_features": "右手單手反握主短匕於身前、左爪持副匕微屈護胸，雙刀刃口泛著薄荷綠淬火鋒芒，符合 review.md 0-MKT7 單持/成對主次分明無穿模規範"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_cuttlefish_pneumatic_ink_siphon",
    "display_name": "氣動高壓發煙雙聯墨囊氣罐",
    "material": "雙聯垂直排列沖壓鍍鈦氣筒（#38A0FF），頂部配備微型氣壓表與虹吸發煙噴嘴，底部連接柔性黃銅編織輸氣軟管",
    "visual_features": "牢固安裝於背部上側，兩側氣筒對稱排布，中央留有標準發條開孔，與發條鑰匙錯位排布無任何重疊穿模，戰鬥時偶爾噴出微泡"
  }
}
```

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

為配合既有六大戰鬥姿態體系（`idle`, `telegraph`, `attack`, `recover`, `skill`, `hit`），墨影烏賊各姿態規劃如下（嚴格對齊 `review.md` Rule 4b-4、Rule 4b-5、Rule 4b-6 與 0-QA16）：

1. **待機姿態（`idle`）**：  
   2.2 頭身矮萌身軀微伏，四對短小金屬觸肢抓地平穩；右手反握主鋒匕橫於胸前，左手短匕斜指向下；頭頂兩側波浪側鰭隨每 3~4 秒的海淵秒針律動緩慢扇動，石英目鏡藍綠冷光均勻流轉，神態沉著警惕，身周隱現微弱水流波動。
2. **前搖預警姿態（`telegraph`）**：  
   身軀極限後伏下沉！四對觸肢緊抓地面蓄能，身軀高度壓縮 30%；雙匕在胸前呈「X」型交叉咬合，背後雙聯氣罐氣壓表指針驟跳至紅色超壓區，虹吸噴嘴噴射出一股短促的深藍色微氣泡煙霧；石英目鏡轉為警示亮綠光芒，蓄滿破水刺殺之勢。
3. **出招攻擊姿態（`attack`）**：  
   身形如離弦之箭般破水貼地瞬衝！背部氣罐瞬間釋放高壓氣流，借流體反推極速滑行半步，雙手短匕由胸前十字瞬間向兩側暴力抹出，在空中劃出兩道交錯的薄荷綠弧光死線；命中目標時引發清脆銳利的「唰——錚！」金屬切割脆響，激起大片螢光水花與機械齒輪碎屑。
4. **收招硬直姿態（`recover`）**：  
   短匕斬落定格，身形順勢半旋卸力；背部氣罐噴嘴悠長地排出一縷白霧氣泡「嘶——」，烏賊單膝點地，左手短匕利落收回腰間，右手短匕刀花旋轉後反握定格，重心平穩回歸。
5. **奧義技能姿態（`skill`）——【海淵墨影·千刃虹吸暗影殺（Abyssal Inksmoke Phantom Guillotine）】**：  
   墨影烏賊身形凌空躍起，背部三葉發條鑰匙急促超頻旋轉！雙聯氣罐在身周全面引爆，全場瞬間被濃烈的深藍色發條微粒煙幕籠罩；煙幕中烏賊化為四道幽藍殘影，以流體極速對敵人弱點連續發動六次極速死角穿刺（「森羅連刺」）；最後一擊破煙而出，雙匕凌空垂直貫刺而下，引發巨大的深海渦流水爆，炸裂全場敵人防線，漫天飄落晶瑩水泡與多巴胺星芒！
6. **受擊反饋姿態（`hit`）**：  
   受到衝擊時，身軀向後滑退 10px，四對金屬觸肢緊緊抓地卸力，兩側黃銅側鰭如防護盾般向前收攏合抱；頭部微縮入深潛頭盔，雙匕交叉死死封架於面前，金屬碰撞火星四濺，咬牙抗衡衝擊。

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

### Q1：它掛在哪個核心循環的哪一環？
- **回答**：掛在核心循環「戰鬥（主線出征/停擺巨偶）-> 掉落零件/圖鑑解鎖 -> 衣櫥換裝與紙娃娃客製化 -> 數值無關的情感共鳴」的「**外觀收集與角色客製化環節**」。墨影烏賊作為第九巡第三順位擴充，正式將全遊戲總族群擴充至五十一族，填補了 R05 琉璃汪洋長期缺乏忍者短匕素體的重大空白，為喜愛深海題材與高速匿蹤刺客的玩家提供極致精巧的發條烏賊玩具視覺體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
- **回答**：服務第一根體驗支柱「**極致反差萌（2.2 頭身 Q 版矮萌發條烏賊手持雙鋒短匕，噴吐夢幻氣泡煙霧展現凌厲刺殺反差）**」與第三根體驗支柱「**深厚世界觀與玩具敘事（古典鐵皮潛水烏賊玩具、深海琉璃發條宮殿守護者傳承）**」。第一優先！

### Q3：玩家在手機上用單手拇指能不能操作它？
- **回答**：**完全可以**。所有戰鬥、移動與換裝交互完全複用既有忍者職業雙拇指操作介面，按鈕熱區嚴格 >= 48px，高速突進與弱點連刺判定清晰，單手拇指在手機大廳與紙娃娃衣櫥中點擊互動流暢無阻。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
- **回答**：**絕對不需要**。純客戶端本機單機離線架構，素體資料、部件配置與動畫切片 100% 內嵌於本機 Godot 客戶端中，斷網狀態下所有紙娃娃部件與戰鬥姿態運轉如常，嚴守 §6 單機無伺服器紅線。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
- **回答**：**絕對不會**。依據 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況，目前 Web 目錄約 135 MB，首包瘦身（50~80 MB）屬於整體專案既有歷史欠帳；本提案為**純文字 Markdown 規格文件**，0 圖片、0 影片、0 聲音素材，直接新增包體為 0 KB！未來由美術與程式建置資產時，嚴格遵循雙規格（128x128 像素圖、512x512 高清圖）及 WebP/PNG 壓縮管線，預估單族全部資產增量 < 0.8 MB，不造成包體非理性膨脹。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
- **回答**：**放棄了「真實烏賊生物軟組織、柔軟黏液與有機吸盤觸角」**，嚴格以「沖壓防腐鍍鈦薄板、深潛石英頭盔、氣動發煙雙聯氣罐、三葉渦輪發條鑰匙與分節軟鋼機械滾足」進行古典童話的發條玩具轉譯；**放棄了「自創新武器類別（如投擲苦無或雙節棍）以追求噱頭的數值膨脹誘惑」**，完全收斂並服膺於既有忍者·短匕（`ninja/dagger`）體系；**放棄了「搶快直接產圖產片」**，嚴格遵守審查規範先立規格審定定稿後，再交棒下游依序建置骨架與資產。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

供下游骨架建置任務與資料表同步腳本參考之標準 JSON 區塊片段：

```json
{
  "cuttlefish": {
    "race_id": "cuttlefish",
    "name": "墨影烏賊",
    "name_en": "The Inksmoke Cuttlefish",
    "aliases": ["inksmoke_cuttlefish", "abyssal_cuttlefish", "mimic_cuttlefish", "clockwork_cuttlefish"],
    "class_archetype": "ninja",
    "weapon_class": "dagger",
    "default_weapon_id": "star_fang",
    "native_realm_id": "R05",
    "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
    "toy_lineage": "19 世紀末古典鐵皮發條潛水烏賊玩具與鐘錶水下氣動發煙機關偶",
    "color_palette": {
      "base": "#FFFDF8",
      "primary": "#38A0FF",
      "secondary": "#4ED86A",
      "accent": "#FF5E8A",
      "metal": "#FFD028",
      "outline": "#1F1A3A"
    },
    "slots": {
      "chassis": "chassis_cuttlefish_abyssal_cyan_default",
      "head_unit": "head_cuttlefish_diving_cowl_fins",
      "winding_key": "key_cuttlefish_tri_vane_turbine_brass",
      "costume": "costume_cuttlefish_abyssal_shinobi_cuirass",
      "optic_core": "face_cuttlefish_dual_quartz_optic_lens",
      "weapon": "weapon_cuttlefish_abyssal_inksmoke_dagger",
      "back_curio": "curio_cuttlefish_pneumatic_ink_siphon"
    }
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> **法規與工具指引**：  
> 本段落專供後續美術總監（sideart）或視覺生成管線（`/root/gen_media.py`）產圖使用。  
> 嚴格遵守 `references/art_direction.md` 與 `references/brand_assets.md` 之兩大鐵則：  
> 1. **產圖一律強制掛載主視覺參考圖 `--ref branding/key_visual_main.png`**，確保角色比例、材質與筆觸與世界觀母體 100% 對齊；  
> 2. **嚴格禁止 AI 直接生成文字、商標與邊框**（Prompt 全面強制納入 `--no text, --no letters, --no logo, --no watermark` 規範），所有遊戲標題卡一律由後製無失真疊加。

### 8.1 墨影烏賊角色單體立繪 Prompt（4:5 垂直角色畫）

```
Full-body character illustration of a charming 2.2-head-tall anthropomorphic mechanical toy cuttlefish shinobi assassin, known as The Inksmoke Cuttlefish.

The cuttlefish is a compact handcrafted vintage mechanical toy designed to be held in one hand, completely non-biological, zero real skin, zero tentacles flesh, zero organic slime. Large rounded stylized diving cowl helmet made of stamped titanium alloy painted in vibrant cyan enamel (#38A0FF) with ivory-white ceramic baseplate highlights (#FFFDF8). Symmetrical articulated thin brass swimming balance fins (#FFD028) on the sides of the head. Expressive glowing twin convex quartz eye lenses shining in mint-cyan light (#4ED86A, #38A0FF). Lower body features four pairs of tiny segmented spring-steel mechanical tentacles ending in brass roller claws.

The cuttlefish wears a lightweight deep-sea navy shinobi cuirass with dopamine cyan trim and mint-green shockproof corners. A dual-cylinder brass pneumatic ink-siphon backpack is mounted on the upper back with tiny pressure gauges.

A prominent antique brass three-vane marine turbine winding key is mounted on the upper back. The body is positioned at a three-quarter angle so the brass winding key clearly breaks the outer silhouette and catches warm specular light — never hidden behind the body.

The character wields exactly ONE pair of twin titanium curved daggers with hydrodynamic grooved blades in a classic ninja reverse grip.

Material: chipped cyan and ivory enamel, aged brushed brass edges, polished titanium plates, tiny exposed silver screws, delicate seams, subtle scratches and toy imperfections, nostalgic antique toy construction.

Color palette: dopamine sky blue (#38A0FF), mint green highlights (#4ED86A), coral pink accent rivets (#FF5E8A), warm brass (#FFD028), deep navy trim (#1A3558), dark blue-violet outlines (#1F1A3A).

Pose: dynamic alert ninja standing crouch pose, twin daggers held ready, tiny bubble puffs escaping from the ink siphon, adorable yet sharp toy personality.

Lighting: warm theatrical stage lighting, soft volumetric caustics, cyan magical rim light, soft ground foot shadow.

Camera: full-body character art, three-quarter view, 50mm lens, completely clean neutral warm studio background — plain warm cream gradient (#FFFDF8), no props, no scenery.

Style keywords: premium stylized 3D mobile RPG character art, cel-shaded anime style, bold outlines, dopamine color palette, handcrafted mechanical toy, chibi fantasy ninja, whimsical steampunk fairy tale, high readability.

NEGATIVE PROMPT:
real cuttlefish, real squid, real octopus, biological animal, organic flesh, slimy skin, tentacles with wet flesh, plush toy, stuffed animal, humanoid robot, futuristic mech, military armor, sci-fi cyborg, Iron Man, smooth modern plastic, chrome, horror, creepy doll, porcelain doll, scary eyes, oversized weapons, multiple swords, extra limbs, dark muddy colors, text, letters, font, logo, watermark, signature.
```

### 8.2 墨影烏賊水下海淵主視覺與場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
A cinematic 16:9 key art illustration for a charming mobile RPG, set in the underwater clockwork diorama realm of R05 Crystal Ocean.

In the foreground, a cute 2.2-head-tall mechanical toy cuttlefish ninja leaps through transparent cyan liquid gel seawater, twin curved daggers flashing with bright mint-green edge glow. The cuttlefish is made of stamped cyan-enameled titanium plates, articulated brass side-fins, dual glowing quartz eye lenses, and has a spinning brass turbine winding key on its back. The backpack ink-siphon emits a harmless, whimsical plume of sparkling deep-blue toy mist and luminous bubbles.

Environment: breathtaking underwater clockwork ocean diorama inside a giant glass dome, transparent cyan liquid gel sea, glowing crystal palace towers with quartz air domes, colorful silicone clockwork coral reefs, lapis lazuli mosaic tiled seabed, glowing phosphorescent jellyfish streetlamps (#38A0FF, #4ED86A). In the far background, a giant copper anchor chain ticking underwater and the silhouette of a giant clockwork kraken titan.

Lighting: luminous Tyndall underwater caustic godrays piercing through the crystal sea, sparkling bioluminescent bubbles, warm golden highlights on brass gears, vibrant dopamine color atmosphere.

Composition: cinematic action shot, high visual contrast, clear readable character silhouette, strong foreground focus with soft depth of field in the background.

Style keywords: premium stylized 3D game art, cel-shaded anime aesthetic, Maplestory and Tata Adventure inspired dopamine colors, handcrafted mechanical toy world, whimsical steampunk fairy tale, 8k resolution, crisp mobile-first readability.

NEGATIVE PROMPT:
photorealistic animals, real marine life, slimy tentacles, blood, gore, horror, creepy monsters, dark muddy water, dirty grey colors, human figures, military submarine, futuristic sci-fi, text, letters, words, logo, title, watermark, border, frame.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  "$(cat << 'EOF'
A cute 2.2-head-tall anthropomorphic mechanical toy cuttlefish ninja from Clockwork Heart, made of stamped cyan enamel titanium plates, rigid brass balance fins, dual quartz optic lenses, wearing abyssal shinobi cuirass, holding twin curved daggers, prominent brass turbine winding key on upper back breaking silhouette, cel-shaded, bold dark blue-violet outline, dopamine colors, warm cream background (#FFFDF8) --no real animal, --no flesh, --no slimy tentacles, --no text, --no letters, --no logo, --no watermark
EOF
)" \
  output_cuttlefish_paperdoll.png \
  --aspect 4:5 \
  --ref /opt/side/bravesoul-game/branding/key_visual_main.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：本提案所引用之「液態琉璃凝膠海（Liquid Crystal Gel Sea）」、「海淵地表與馬賽克步道（Abyssal Seabed & Mosaic Walkways）」、「深海藍晶石馬賽克瓷磚（Lapis Lazuli Mosaic Tiles）」、「發條珊瑚群（Clockwork Coral Reeds）」、「水下發條宮殿與氧氣泡罩（Clockwork Sunken Palace & Aerated Glass Domes）」、「磷光水母街燈與流體排氣柱（Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents）」、「水下丁達爾藍晶光柱（Submarine Caustic Godrays）」、「天頂青銅錨鏈秒針」、「深淵排污豎井管道·耐壓吊籠（Abyssal Sump Siphon: Bathysphere Terminal）」、「晨曦天軌 5 號深海浮標月台（Dawn Rail Deepsea Buoy Platform 5）」、「深海熱液湧泉管道（Hydrothermal Trench Conduits）」、「環域水幕磁阻防護波（Magnetic Hydro-Barrier Grid）」、「小黃鴨船長·舵手巴克（Captain Buck）」、「海馬信差·碧浪（Billow）」、「深海鐘錶貝·珠貝長老（Elder Pearl）」、「深淵海霸泰坦·八爪機關巨烏賊（Titan Abyssal: Octo-Gear the Abyssal Kraken）」逐字精確對齊 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 第 19 行、第 20 行、第 21 行、第 22 行、第 24 行、第 25 行、第 29 行、第 30 行、第 32 行、第 34 行、第 54 行、第 63 行、第 71 行、第 100 行，100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（包體膨脹查驗）**：純文字 Markdown 規格文件，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有五十族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 50 族（含第 49 族熔鎧犰狳、第 50 族風箱毛蟲）。
- [x] **review.md 23f-1（單一職業標籤）**：職業名稱唯一嚴格對齊為 `忍者 (Ninja)`，無任何雙標籤或自創詞。
- [x] **review.md 23f-2（武器名稱前後一致）**：原生專屬武器在全文所有章節、表格與 JSON 片段中均統一稱作「海淵墨影雙鋒匕」，精確呼應 `R05_CRYSTAL_OCEAN.md` 海淵暗影刺客工藝，相容武器精確對齊既有 `equipment.json` 之 `star_fang`（星牙短匕，tier 2）與 `nebula_needle`（星雲細針，tier 3）。
- [x] **review.md 23f-4 / CANON 零毛皮鐵律**：全篇 100% 清除所有生物皮毛、真角質鱗片、肉質、血液、軟體黏液等字眼，烏賊特徵全面轉譯為沖壓防腐鍍鈦薄板、深潛石英頭盔、雙聯氣動墨囊氣罐、三葉渦輪發條鑰匙與分節軟鋼機械觸肢滾足。
- [x] **review.md 0-MKT7（單持無穿模規範）**：明確指定右手反握主鋒匕、左手副匕微屈護胸，雙刀主次分明，0 佔位短棒，0 多餘浮動武器，0 穿模違規。
- [x] **review.md 0-QA30 前置防護**：aliases 預先定案 `cuttlefish`, `inksmoke_cuttlefish`, `abyssal_cuttlefish`, `mimic_cuttlefish`, `clockwork_cuttlefish`，為下游骨架單建立唯一真相源。
- [x] **產圖 Prompt 規範**：第 8 節完整附上 4:5 與 16:9 提示詞，明載 `--ref branding/key_visual_main.png` 與 `--no text, --no letters, --no logo, --no watermark` 鐵律。
