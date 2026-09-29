# 第五十七種動物「星岩鼴鼠（The Asteroid Mole）」世界觀與角色設計提案

> **標題**：第五十七種動物「星岩鼴鼠（The Asteroid Mole）」角色與世界觀設計提案  
> **提案代號**：`ASTEROID_MOLE_DESIGN_PROPOSAL`（代號：`mole` / 識別名：`race_mole`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_e0951e61`（📖 世界觀｜第五十七種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零動物肉身、零生物黏液、高密度工程聚合物塑料板件 ABS/POM、冷軋鎢鋼承重骨架、防爆聚碳酸酯採礦護目罩、微型冷氣反推噴嘴、足底磁吸防滑矽膠滾足、外露精密螺栓與防震鉚釘、背後四葉微型發條天線鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R07_STARFALL_ORBIT.md`（第 1 行區域代號與名稱「R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station」、第 4 行「高密度工程聚合物塑料板件、透明聚碳酸酯太空艙罩、高光幻彩螢光軌道連桿、微型冷氣反推噴嘴與失重磁浮導軌套件」、第 6 行「局域走時狀態：星穹失重懸停與脈衝量子跳拍（秒針每 3.0 秒在無重力真空中劃過一圈優雅弧線，伴隨電子發條合成音「嗶——嗡！」；失重微浮力引發發條齒輪低阻力空轉，需精準掌握反衝制動節奏穿行）」、第 15 行「乳白色高強度工程聚合物塑料模組（ABS/POM 玩具塑料板件）」、第 19 行「聚合物太空艙模組（Polymer Astro-Dome Complex）」、第 20 行「高光懸空螢光軌道（Luminescent Neon Mag-Tracks）」、第 21 行「太陽能帆板與微型排氣天線（Solar Polymer Sails & Micro-Pneumatic Masts）」、第 22 行「太空拼裝維修船塢（Space Assembly Drydocks）」、第 29 行「高壓地熱升空彈射井·軌道受壓對接艙（Geothermal Ejection Launch Silo: Orbital Docking Port）」、第 31 行「垂直磁浮天軌·星穹軌道月台（Vertical Mag-Rail: Orbital Terminal）」、第 32 行「軌道廢棄排障滑道（Orbital Debris Dump Chute）」、第 34 行「失重慣性磁力捕捉網（Zero-G Inertia Magnetic Capture Grid）」、第 46 行「高真空抗靜電除塵室（Electrostatic De-Dusting Airlock）」、第 54 行宇航機器人隊長「螺栓隊長（Captain Bolt）」、第 63 行太空發條小狗「萊卡波波（Popo）」、第 71 行軌道站資深工程師「光纖婆婆（Granny Fiber）」、第 100 行旗艦泰坦 BOSS「星穹泰坦·多臂組裝軌道採礦機（Titan Starfall: Multi-Arm Orbital Mining Rig）」、第 107-109 行「軌道採礦多聯機械臂、背部冷氣反推推進器、聚碳酸酯座艙罩」、第 120 行特產武器「高頻等離子重錘（High-Frequency Plasma Sledgehammer）」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（戰士正式名稱 `viking`，標籤宣言 `\"站到最後\"`，武器 `hammer`，數值 `atk: 1, def: 4, hp: 12, crit: 0.0, speed: 0`，玩法 `\"站著硬扛，耗到對手先倒。同職也可玩斧。\"`，初階武器 `anvil_hammer`）  
> - `game/data/tables/equipment.json`（鎚類正式 line: `\"hammer\"`，初階武器：`anvil_hammer` 鐵砧重鎚，中高階相容武器：`iron_cudgel` 生鐵短棍、`bastion_blade` 堡壘巨砧）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡（第 55~60 族）第二順位重磅擴充，開啟戰士 5:5 超對稱平衡**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十七種動物擴充素體規格**。  
   在全專案於第十巡首位成員第五十六種動物重閥河馬（騎士·長槍）順利補齊騎士長槍達到 5:5 劍槍對稱後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第二順位**，以磐石之姿輪轉進入全遊戲最具極限血防、鍛造霸體、部位破壞與硬扛反震的核心職業——**戰士 (Viking)** 體系，原生武器掛載於**高頻等離子衝壓重鎚（`hammer` / 戰士·鎚）**。  
   星岩鼴鼠的加入，使全遊戲戰士戰鎚素體擴充至第 5 款（玄軸熊、熔火蜥蜴、撼地野牛、風箱毛蟲、星岩鼴鼠），與戰士戰斧素體（鋼牙豕、鋼岳象、浪花海獺、重角犀牛、劈木河狸 5 款）達成**完全對稱的 5:5 完美平衡格局**！
2. **經典玩具起源與古典機械發條掘地鼴鼠太空工程偶工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與太空時代自動偶史上的經典工藝原型：  
     ① **1950s-1970s 經典古典發條鐵皮掘地鼴鼠自動機（Vintage Tinplate Wind-up Digging Mole Automaton / 德國 Schuco、Lehmann 與日本昭和 TPS、Nomura 金屬玩具名作）**，通體由沖壓馬口鐵板、雙偏心齒輪連動前爪刨挖機構與底部步進滾輪咬合而成，走動時雙爪伴隨發條節奏高速向內撥動，是古典玩具史上最具工程機械美感與踏實手感的機械自動偶之一；  
     ② **1960 年代太空競賽熱潮下的登月採礦探索發條偶（Retro Space-Age Lunar Prospector & Asteroid Drilling Automaton）**，圓滾敦厚的身軀裝配防爆聚碳酸酯採礦護目罩、微型冷氣姿態反推氣嘴與磁吸防滑工程滾足，賦予角色在失重軌道上沉穩吸附、抗震破岩的扎實物理反饋；  
     ③ **維多利亞天文台小行星採礦與地質檢測自動偶（Victorian Horological Asteroid Mineral Prospector）**，將經典鐘錶擒縱齒輪與高頻等離子重鎚結合，完美詮釋戰士職業「站到最後、血和防禦最厚、站著硬扛、耗到對手先倒」之戰士之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「乳白工程塑料耐磨矮萌底盤、聚碳酸酯防爆採礦面罩、雙聯超導微型雷達葉片耳、軌道高壓防塵防靜電工裝、短粗圓筒形冷氣反推短尾、星穹高頻等離子重鎚與四葉天線金黃發條鑰匙」之星穹重裝破岩戰士素體（Polymer Astro-Mole Chassis, Polycarbonate Mining Visor Cowl, Superconducting Radar-Vane Ears, Orbital Anti-Static Heavy Dungarees, Cold-Gas Counter-Thrust Cylinder Tail, Orbital Plasma Sledgehammer & Four-Vane Antenna Brass Key）**。
3. **生態補足：徹底終結高軌星穹界域（R07）零戰士之歷史空白，湊齊空間站六大職業大滿貫陣容**：  
   在全遊戲 9 大界域中，頂層高軌星穹沙盤界域 `R07 星穹軌道·外星基地` 先前擁有星軌犬（騎士·槍）、星巡浣熊（遊俠·銃）、星盤靈羊（法師·杖）、暗翼蝙蝠（忍者·鏢）與破星蜜獾（武術家·爪）共 5 族。  
   長久以來，面對外軌道星環船塢中暴走的超級巨偶「星穹泰坦·多臂組裝軌道採礦機」，以及失控四處拋灑的帶電塑料隕石與堅硬的小行星浮石，**該界域完全缺乏一位能夠在無重力真空軌道上以磁吸滾足定點站樁、正面硬抗高速漂移星岩衝擊、手持等離子重鎚粉碎障礙並拆解泰坦堅固關節的「重裝防禦工程戰士（Viking）」**！星岩鼴鼠的降臨，徹底填補了 R07 長期零戰士素體的生態空白，讓 R07 成為繼中層各大界域後，首個集齊「騎士、戰士、忍者、武術家、法師、遊俠」全 6 職完全生態的終極高軌沙盤！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源（僅登錄 races_specification 正表提案項目，total_races 維持現狀 54）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：星岩鼴鼠素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十六族武器與職業光譜全盤點

盤點現有首發五族與前五十一款擴充族（總計 56 族，含第 56 族重閥河馬）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

- **白金兔（Clockwork Rabbit）**：騎士 (Knight) —— 單手長劍（`sword`），平衡攻防，中近距離。
- **烈鬃獅（Gilded Lion）**：騎士 (Knight) —— 皇家長槍（`spear`），中距控場，格擋迎擊。
- **靈尾狐（Astral Fox）**：法師 (Mage) —— 秘術法杖（`magic`），遠程法術，技能爆發。
- **鋼牙豕（Forge Boar）**：戰士 (Viking) —— 鍛爐巨鎚（`hammer`），高防厚重，部位破壞。
- **靈爪猴（Spring Macaque）**：武術家 (Monk) —— 機關靈爪（`claw`），彈簧伸縮臂，近身連打破勢。
- **烈焰虎（The Ember Tiger）**：忍者 (Ninja) —— 齒輪雙斬刃（`dagger`），伏擊撕裂，近戰極限暴擊。
- **雲嵐鶴（The Cloud Crane）**：遊俠 (Ranger) —— 風弦羽翼機關弓（`bow`），超視距狙擊，遠程精準破甲。
- **玄軸熊（The Iron Bear）**：戰士 (Viking) —— 玄軸偏心重力錘（`hammer`），磐石壁壘，大範圍震波。
- **蒸氣企鵝（The Steam Penguin）**：遊俠 (Ranger) —— 蒸氣雙管導航火槍（`gun`），直線高壓蒸氣爆發，精準點射。
- **玄機龜（The Xuanji Tortoise）**：法師 (Mage) —— 玄機八卦發條星盤 / 磐甲浮空護體靈晶（`crystal`），護盾織刃，高防反震。
- **鋼岳象（The Colossus Elephant）**：戰士 (Viking) —— 巨輪開山重斧（`axe`），質量重力斬劈，單發物理最高傷害。
- **碧簧蛙（The Spring-Leg Frog）**：忍者 (Ninja) —— 碧葉旋刃機關鏢（`dart`），高速牽制，多段飛鏢射殺。
- **瓷韻熊貓（The Porcelain Panda）**：武術家 (Monk) —— 乾坤太極機關拳套（`fist`），貼身寸勁連打破勢，動靜化勁。
- **翠角鹿（The Emerald Fawn）**：遊俠 (Ranger) —— 翠木角尺複合機關弓（`bow`），停拍看破，機動連發射擊。
- **星軌犬（The Orbit Hound）**：騎士 (Knight) —— 星軌雷達天線槍 / 光子信標穿刺長槍（`spear`），中距失重滑行，磁軌迎擊控場。
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
- **墨影烏賊（The Inksmoke Cuttlefish）**：忍者 (Ninja) —— 海淵墨影雙鋒匕（`dagger`），深海高壓氣動微泡煙幕，流體匿影死線刺殺。
- **熔砧石蟹（The Anvil Crab）**：武術家 (Monk) —— 黑曜衝壓熔岩拳套（`fist`），熔爐鐵砧高頻衝壓，橫行碎步閃避破勢。
- **日晷駱駝（The Sundial Camel）**：法師 (Mage) —— 廢土日晷折射短杖（`magic`），雙峰冷凝油壺調諧，日光陰影折光轟擊。
- **鐘塔長頸鹿（The Belfry Giraffe）**：遊俠 (Ranger) —— 鐘樓天弦複合機關弓（`bow`），高塔潛望測距看破，八音琴弦諧振連發。
- **重閥河馬（The Steamvalve Hippo）**：騎士 (Knight) —— 重閥活塞衝刺長槍（`spear`），蒸氣超壓衝程，沉穩低重心防禦反震，雙聯排氣鳴笛迎擊。
- **星岩鼴鼠（The Asteroid Mole）**：**戰士 (Viking) —— 星穹高頻等離子重鎚（`hammer`），失重磁吸定點霸體，高頻電漿震盪碎岩，引力波衝壓粉碎。**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）10 族（劍 5、槍 5，已達完全平衡）；
- 忍者（Ninja）9 族（匕 5、鏢 4）；
- 武術家（Monk）9 族（拳 5、爪 4）；
- 法師（Mage）9 族（杖 5、晶 4）；
- 遊俠（Ranger）9 族（弓 5、銃 4）；
- 戰士（Viking）此前在 56 族中擁有 9 款動物素體（斧 5 款、鎚 4 款）；
- **本提案第五十七種動物正式作為「第十巡第二順位」核心擴充，歸屬於戰士 (Viking) 體系，原生武器掛載於 `hammer`（戰鎚 / 戰士·鎚）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`戰士 (Viking)`**；
- 星岩鼴鼠的加入，使全遊戲戰士戰鎚素體擴充至第 5 款，戰士總數達成 10 款，戰斧（5 款）與戰鎚（5 款）達成完全對稱的平衡格局！

### 1.2 星岩鼴鼠武器選擇：【星穹高頻等離子重鎚（Orbital Plasma Sledgehammer）】

星岩鼴鼠原生專屬武器定名為：**【星穹高頻等離子重鎚（Orbital Plasma Sledgehammer）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R07_STARFALL_ORBIT.md` 星穹軌道·外星基地之高頻等離子與小行星採礦工程體系**！  
底層完全掛載於 `weapon_classes.json` 的 `hammer`（戰士·鎚）類別，享有 `hammer` 既有的「站到最後」標籤宣言（Tagline: `\"站到最後\"`）、血和防禦最厚、鍛造成功率暗中高一點、硬吃招式也不太會死、站著硬扛耗到對手先倒之特性（`atk: 1, def: 4, hp: 12, crit: 0.0, speed: 0`），完美呼應 `R07_STARFALL_ORBIT.md` 第 120 行官方特產武器「高頻等離子重錘（High-Frequency Plasma Sledgehammer）：巨錘類，具備 6 次揮動耐久。錘頭內置微型反重力線圈，自帶被動『引力震盪』（重砸命中敵人時引發小型失重引力場，使周圍敵人浮空 2 秒並削弱護甲 35%）」之戰鬥機制！

- **法源素材咬合**：  
  完全對應 `R07_STARFALL_ORBIT.md` 第 4 行代表材質「高密度工程聚合物塑料板件、透明聚碳酸酯太空艙罩、高光幻彩螢光軌道連桿」、第 22 行**「太空拼裝維修船塢（Space Assembly Drydocks）」**與第 107-109 行泰坦核心構件**「軌道採礦多聯機械臂（Orbital Mining Claws）」**與**「聚合物輕量裝甲板（Lightweight Polymer Armor Plate）」**，將太空站的工程拆解工具轉化為粉碎星岩的重型兵裝。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"hammer\"` 的初階裝備 `anvil_hammer`（鐵砧重鎚，tier 1）與中高階相容裝備 `iron_cudgel`（生鐵短棍，tier 2）、`bastion_blade`（堡壘巨砧，tier 3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款戰鎚戰士（玄軸熊、熔火蜥蜴、撼地野牛、風箱毛蟲）絕不撞型之論證

雖然星岩鼴鼠與玄軸熊、熔火蜥蜴、撼地野牛、風箱毛蟲同屬 `viking`（戰士）戰鎚（`hammer`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               戰士職業戰鎚系五族差異化對照表（熊 vs 蜥蜴 vs 野牛 vs 毛蟲 vs 鼴鼠）                                 │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 玄軸熊 (Bear)        │ 熔火蜥蜴 (Salamander)│ 撼地野牛 (Bison)     │ 風箱毛蟲 (Caterpillar│ 星岩鼴鼠 (Mole)     │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 偏心飛輪離心重砸     │ 垂直氣動衝壓洩壓鍛砸 │ 廢土重砧粉碎破障     │ 手風琴式風箱蓄壓夯地 │ 失重磁吸定點電漿碎岩│
│ 2. 動能來源     │ 玄軸偏心配重陀       │ 高壓地熱蒸氣衝壓氣缸 │ 工字鋼梁與生鐵重力矩 │ 多節同軸皮革風箱蓄能 │ 超導微型反重力電漿環│
│ 3. 步法特徵     │ 沉穩正步、厚重大踏步 │ 伏地爬行、尾部平衡微跳│ 踏地震地、重蹄前壓   │ 多節蠕行、滾足自鎖   │ 磁吸吸盤滾足、爪刨滑│
│ 4. 武器構造     │ 雙向偏心配重黃銅圓錘 │ 帶散熱孔方型鍛造鋼錘 │ 工字鋼柄生鐵四方重砧 │ 手風琴壓縮風箱重壓鎚 │ 透明聚合物電漿衝壓鎚│
│ 5. 主題界域     │ R06 赤焰熔爐·鍛造火山│ R06 赤焰熔爐·鍛造火山│ R08 荒漠齒輪塚·遺忘庫│ R03 翡翠深林·發條蔓谷│ R07 星穹軌道·外星基地│
│ 6. 材質質感     │ 焦糖琥珀漆、鑄鋼板件 │ 黑曜鎢鋼、耐熱琺瑯面 │ 生鏽深褐馬口鐵、防鏽 │ 沖壓薄銅環、墨綠皮革 │ 乳白高密度塑料、螢光│
│ 7. 角色剪影     │ 寬厚圓肩雄壯巨靈     │ 低趴修長帶同軸大尾   │ 高聳駝峰寬肩角盔重甲 │ 多節扁圓手風琴蠕動   │ 圓滾敦厚大爪護目太空│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格恪守 `docs/world/CANON.md` 憲章世界觀「**100% 零真動物生物肉身、零毛皮、零羽毛、零真甲殼有機質、零血肉黏液**」之鐵律：

- **乳白高密度工程塑料底盤與冷軋鎢鋼骨架**：星岩鼴鼠的身軀並非動物肉身，而是由太空站模組工坊拼裝的**高密度工程聚合物塑料板件（ABS/POM #FFFDF8 / #38A0FF）**與內部冷軋鎢鋼承重框架卡扣鉚接而成。圓滾敦厚的身軀由高抗衝擊工程塑料外殼包裹，表面分佈著精密微型螺栓與防震接縫，絕無任何生物皮毛、軟組織或地下泥土髒污。
- **多層沖壓掘地機械合金爪**：鼴鼠標誌性的刨土大爪被徹底轉譯為一對**重型沖壓合金多齒工程採礦爪（Alloy Mining Shovel Paws）**。爪尖採用經過硬化處理的鎢鋼多刃鎬齒，爪背嵌入微型冷氣排氣孔，雙腕處裝配外露同軸傳動齒輪（#FFD028），揮爪與握持重鎚時隨走時節律輕快咬合，完全杜絕任何角質真爪或生物肉墊。
- **雙聯超導微型雷達葉片耳**：頭部兩側看似鼴鼠隱蔽小耳的部位，實質上為一對微型「雙聯超導聲納雷達葉片（Superconducting Sonar-Vane Ears）」。葉片由薄型天元金黃銅片（#FFD028）與薄荷冷翡翠發光微型光纖（#4ED86A）編織而成，在真空失重環境中以微小頻率輕快旋轉，負責探測前方小行星碎石的引力波頻率，無任何生物耳廓。
- **防爆聚碳酸酯採礦護目罩與琥珀點陣目鏡**：眼眶處安裝有一具半球形高透防爆聚碳酸酯宇航採礦面罩。面罩內部由多巴胺暖橘（#FFA010）點陣 LED 晶片投射出呆萌專注的大圓眼睛，在鎖定星岩弱點時目鏡轉為薄荷綠十字光標，既具備防強光護目功能，又展現童話玩具的情感溫度。
- **短粗圓筒形冷氣反推平衡短尾**：尾部並非肉尾，而是一具短粗的圓筒形微型冷氣反推排氣噴管（Cold-Gas Thruster Cylinder Tail）。尾端帶有珊瑚粉色（#FF5E8A）的橡膠防撞環與四孔定向微型噴嘴，在重鎚下砸時噴射微量白色低溫氣霧，提供失重環境下不可或缺的下盤反衝配重。
- **背後發條鑰匙**：背部中央正上方垂直挺立著一把充滿科幻發條美感的**四葉微型發條天線鑰匙（Four-Vane Antenna Brass Key）**。鑰匙柄部呈四葉十字對稱雷達天線造型（#FFD028），中心軸承鑲嵌多巴胺珊瑚粉防塵鉚釘，隨秒針每 3.0 秒在失重太空中劃過弧線時勻速旋轉，伴隨清脆的「嗶——嗡！」電子鐘琴調諧音。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格依循 `USER PROFILE`、`docs/ART_DIRECTION.md` 與多巴胺鮮亮配色規範：

- **頭身比**：嚴格鎖定於 **2.0 ~ 2.2 頭身**。矮萌圓滾的微胖體態搭配短粗有力的磁吸工程四肢與寬幅採礦鏟爪，呈現出宛如古典發條太空玩具矮人礦工般的踏實憨厚感與極致反差萌。
- **色彩規劃（嚴守多巴胺鮮亮配色，絕無泥土髒黑）**：
  - **基底色（Base）**：`#FFFDF8`（象牙白工程塑料 / 拋光鋁鎳金屬，用於面罩基座高光、腹部抗靜電襯板與關節活動墊圈）。
  - **主色（Primary）**：`#38A0FF`（多巴胺天藍，用於太空採礦防護外殼、胸甲塗裝與重鎚鎚頭外罩）。
  - **次色（Secondary）**：`#4ED86A`（薄荷冷翡翠，用於雷達天線導光纖維、等離子重鎚聚能環與面罩刻度光圈）。
  - **點綴色（Accent）**：`#FF5E8A`（多巴胺珊瑚粉，用於冷氣反推噴嘴防撞環、重鎚過載指示燈與發條軸心按鈕）。
  - **金屬色（Metal）**：`#FFD028`（天元黃銅金，用於四葉天線發條鑰匙、採礦爪同軸齒輪與重鎚金屬握柄）。
  - **描邊色（Outline）**：`#1F1A3A`（深藍紫手繪立體外輪廓描邊，確保在亮色與暗色背景下皆清晰銳利，徹底告別泥土髒黑）。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

恪守現代手遊看板角色活化標準：

- **待機呼吸律動（Idle Motion）**：
  - 2.2 頭身圓滾身軀穩穩踩定地面，四足磁吸矽膠吸盤緊扣軌道，右手單持等離子重鎚斜置身前；
  - 伴隨星穹每 3.0 秒跳拍一格的走時節奏，胸腹輕微起伏，背部冷氣短尾微幅噴出一圈晶瑩的小冰晶氣霧；
  - 頭部兩側雷達葉片耳有節奏地轉動半圈，護目面罩內部的點陣 LED 眼睛好奇地眨動兩下；
  - 背後四葉天線金黃發條鑰匙勻速自轉，等離子重鎚的薄荷綠電漿能量環泛起柔和的呼吸微光。
- **點擊戳碰互動（Poke Interaction）**：
  - 玩家以手指點擊角色時，星岩鼴鼠被戳得向後彈跳半步，磁吸滾足發出清脆的「啾——啪！」吸附音；
  - 護目面罩內部的點陣 LED 眼睛瞬間化為興奮的波浪形眨眼（^o^），雙爪開心揮舞；
  - 右手將等離子重鎚在身前重重頓地，地面盪開一圈薄荷綠色失重引力波紋，頭頂彈出元氣對話氣泡：`「小行星碎石準備就緒！這一鎚下去，連星雲都能震開！」`；
  - 同時向四周爆散出一圈多巴胺彩糖星芒粒子（天藍、薄荷綠、金黃）。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R07 星穹軌道·外星基地（Starfall Orbit）零戰士歷史空白

在全專案九大界域中，頂層高軌星穹沙盤界域 `R07 星穹軌道·外星基地` 雖然擁有強大的遠程射手、法師、刺客與敏捷近戰，但在面對巨大的外軌道失控工程設備時，**長久以來完全缺乏一位能夠在失重真空環境下以強大磁吸抓地、正面硬扛碎石洪流、以超重鈍擊破壞堅固卡扣的「重裝防禦工程戰士」**。  
星岩鼴鼠的加入，讓星穹軌道迎來了最堅實的防護後盾，補齊了全域首位戰鎚戰士，構築起完整的空間站防衛隊伍！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R07_STARFALL_ORBIT.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R07_STARFALL_ORBIT.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 穿行於由半球形高透聚碳酸酯艙罩覆蓋的**「聚合物太空艙模組（Polymer Astro-Dome Complex）」**（`R07_STARFALL_ORBIT.md` 第 19 行），修補艙體抗衝擊外殼；
  - 巡防於各大艙體之間橫跨的交通動脈**「高光懸空螢光軌道（Luminescent Neon Mag-Tracks）」**（第 20 行），藉助磁吸阻尼在霓虹光軌上平穩前行；
  - 檢修外壁矗立的成排超薄光子帆板**「太陽能帆板與微型排氣天線（Solar Polymer Sails & Micro-Pneumatic Masts）」**（第 21 行），清除帆板表面的碎星微粒；
  - 駐守於外圍延伸的巨型模組化拼裝支架**「太空拼裝維修船塢（Space Assembly Drydocks）」**（第 22 行），為停泊的蛋形單人宇航膠囊進行外殼加固；
  - 定期巡查空間站下層中央對接港的**「高壓地熱升空彈射井·軌道受壓對接艙（Geothermal Ejection Launch Silo: Orbital Docking Port）」**（第 29 行），引導自赤焰熔爐升空的耐壓吊艙安全靠泊；
  - 巡守核心生活區西側月台**「垂直磁浮天軌·星穹軌道月台（Vertical Mag-Rail: Orbital Terminal）」**（第 31 行），護送往返中層天宮大廳的玩具旅客；
  - 監控空間站外壁下層長達數公里的低摩擦塑料管道**「軌道廢棄排障滑道（Orbital Debris Dump Chute）」**（第 32 行），粉碎堵塞管道的超大塊廢料；
  - 依託空間站外緣 360 度環繞的雙層高彈力透明網**「失重慣性磁力捕捉網（Zero-G Inertia Magnetic Capture Grid）」**（第 34 行），在無重力下砸時獲得全方位防墜保障；
  - 每日輪值進入**「高真空抗靜電除塵室（Electrostatic De-Dusting Airlock）」**（第 46 行），進行靜電中和與全氟聚醚合成潤滑油滴注維護。
- **工坊與居民互動**：
  - 與**宇航機器人隊長·螺栓隊長（Captain Bolt the Space Explorer Robot）**（第 54 行）並肩巡防，交流真空冷氣向量噴嘴的使用心得；
  - 與**太空發條小狗·萊卡波波（Popo the Clockwork Space Pup）**（第 63 行）結伴探險，由萊卡波波在前方標記失重迷宮，星岩鼴鼠則在後方以重鎚掃除塌方阻礙；
  - 接受**軌道站資深工程師·光纖婆婆（Granny Fiber the Orbital Chief Engineer）**（第 71 行）的調校指點，學習在失重環境下以等離子重鎚精準拆卸卡扣的順序。
- **對抗首領情境**：
  - 在挑戰旗艦泰坦**「星穹泰坦·多臂組裝軌道採礦機（Titan Starfall: Multi-Arm Orbital Mining Rig）」**（第 100 行）時，挺身屹立於星環船塢前沿，以磁吸滾足死死吸附軌道，正面硬抗巨偶採礦臂的砸擊；
  - 抓住巨偶雙臂重砸平台產生失重浮空震盪後的 3 秒收臂硬直窗口，以等離子重鎚對準**「軌道採礦多聯機械臂（Orbital Mining Claws）」**的前肢鉸鏈卡扣（第 107 行）施加高頻破甲重砸，擊碎卡扣封印其抓投技能，為隊友創造破壞**「背部冷氣反推推進器」**與**「聚碳酸酯座艙罩」**（第 108、109 行）的決定性戰機！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，星岩鼴鼠的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 星岩鼴鼠專屬造型規格與材質特徵（嚴守 100% 零真皮毛）                                            │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. body (素體)  │ 乳白高密度工程塑料（ABS/POM #FFFDF8 / #38A0FF）與合金採礦爪底盤，四足磁吸防滑工程矽膠吸盤滾足   │
│ 2. head (頭部)  │ 防爆聚碳酸酯太空採礦護目頭盔（#FFFDF8 / #38A0FF），前端配備沖壓合金掘進面罩，無生物口鼻組織       │
│ 3. ears (耳部)  │ 雙聯超導微型雷達葉片耳（#FFD028 / #4ED86A），超薄黃銅片與薄荷光纖編織，隨走時旋轉，無肉耳       │
│ 4. tail (尾部)  │ 圓筒形微型冷氣反推短尾（#38A0FF / #FF5E8A），末端帶珊瑚粉防撞橡膠環與四孔定向反推微型噴嘴       │
│ 5. costume (服裝)│ 軌道高抗衝擊防護工裝背帶褲（#38A0FF / #4ED86A），高強度尼龍編織帶，胸前嵌防爆工具插槽與氣閥標籤│
│ 6. optic_core(眼)│ 琥珀點陣 LED 採礦護目目鏡（#FFA010 / #4ED86A），聚碳酸酯罩內投射呆萌圓眼，鎖定時切換薄荷綠十字光標│
│ 7. winding_key  │ 四葉微型發條天線鑰匙（#FFD028 / #FF5E8A），背部垂直挺立，十字雷達天線造型，中心軸承嵌珊瑚粉防塵鉚釘│
│ 8. weapon (武器)│ 星穹高頻等離子重鎚（#38A0FF / #4ED86A / #FFD028），透明聚合物鎚身內嵌高頻電漿環，下砸釋放引力震盪│
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`body`（素體底盤）**：  
   2.2 頭身 Q 版矮萌敦實身軀，由高密度乳白工程塑料板件（ABS/POM #FFFDF8）包覆冷軋鎢鋼骨架製成。雙臂前端為重型沖壓合金多齒工程採礦爪，腕部帶有外露傳動齒輪（#FFD028）。下身配置短粗穩重的圓柱形腿部，足底裝配四枚防滑耐磨磁吸矽膠吸盤，行走時緊扣高光螢光軌道，徹底杜絕任何真實生物毛皮質感。
2. **`head`（頭部與面罩）**：  
   圓滾平滑的半球形乳白工程塑料頭盔，兩頰帶有多巴胺天藍色（#38A0FF）抗衝擊護腮。面部正前方嵌入一塊高強度透明聚碳酸酯採礦護目罩，鼻樑部位轉譯為沖壓黃銅微型通風過濾閥，眼眶處精準沖孔供 `optic_core` 點陣 LED 光芒透出。
3. **`ears`（雷達葉片耳）**：  
   頭部兩側對稱安裝的一對微型超導雷達天線葉片。葉片由超薄天元金黃銅（#FFD028）與薄荷冷翡翠發光微型光纖（#4ED86A）複合沖壓而成，隨走時脈衝微幅自轉，負責接收空間站小行星探測信標，無任何肉質耳廓組織。
4. **`tail`（冷氣反推短尾）**：  
   由短粗圓筒形高密度塑料外殼製成的微型冷氣反推噴嘴，長度約為身高的 1/6。末端套有一枚多巴胺珊瑚粉（#FF5E8A）矽膠防撞環，周圍均勻分佈四個微型反推排氣孔，在揮鎚時噴出低溫氣霧以平衡失重反衝力。
5. **`costume`（軌道採礦工裝）**：  
   由高抗衝擊聚合物帆布與塑料板件壓合製成的太空工程背帶工裝褲。主色為多巴胺天藍（#38A0FF），兩側點綴薄荷綠（#4ED86A）螢光安全指示帶，胸前配有高強度黃銅快拆卡扣與多功能零件插槽，肩部配備加厚耐磨防撞墊。
6. **`optic_core`（點陣護目目鏡）**：  
   雙聯高亮度多巴胺暖橘（#FFA010）點陣 LED 顯示目鏡。平時在面罩內投射出溫暖明亮的大圓眼睛，待機眨眼時呈現活潑波浪紋；進入戰鬥蓄力時光芒增強，中心浮現出薄荷冷翡翠色的精密十字瞄準準星。
7. **`winding_key`（天線發條鑰匙）**：  
   背部中央挺立的四葉十字發條天線鑰匙。採用天元黃銅金（#FFD028）鑄造，四片天線翼板外緣呈流線型圓角，中心樞軸鑲嵌一枚珊瑚粉防塵鉚釘。隨秒針每 3.0 秒跳拍一次勻速旋轉，伴隨清脆柔和的電子音律。
8. **`weapon`（等離子重鎚）**：  
   星岩鼴鼠專屬武器【星穹高頻等離子重鎚】。全長約身高的 1.3 倍，長柄由高剛性輕量化冷軋鎢鋼管製成，鎚頭為透明聚碳酸酯封裝的四方厚重衝壓箱體，內部清晰可見高速運轉的微型反重力電漿能量環（#4ED86A）。揮砸時電漿環高亮閃爍，砸中目標時釋放出小型失重引力場與電弧震盪。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 雙足磁吸抓地穩如泰山，雙爪平穩握持等離子重鎚立於身側，背部冷氣尾微幅噴氣，天線發條鑰匙勻速自轉 │
│ 2. attack (普攻)  │ 踏步向前發動沉穩重擊，雙爪合握鎚柄自右上方斜向砸落，鎚頭電漿環爆閃，在地面砸出引力裂痕       │
│ 3. hit (受擊)     │ 身軀受震向後微仰，四足矽膠吸盤在軌道上滑出半步，面罩點陣 LED 眼睛泛起雪花波紋，尾部噴氣自平衡 │
│ 4. recover (硬直) │ 雙足重重吸扣地面穩住身形，雙爪將重鎚護於身前架起防護壁壘，面罩重置為冷靜綠色光標，重新鎖定目標│
│ 5. skill (技能)   │ 全身推進器超頻噴射，雙爪高舉重鎚躍起至失重半空蓄力，以「引力崩星重砸」向下夯落，引發全屏電漿震波│
│ 6. telegraph (蓄力│ 身軀下蹲扎緊馬步，雙爪將鎚頭平貼地面開始高頻引力充能，鎚身電漿環光芒轉為耀眼綠光，地面投射蓄力環│
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為戰士職業戰鎚系的核心擴充素體，直接提供高防硬扛、失重磁吸站樁與引力部位破壞的高容錯戰鬥體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過戰士戰鎚的霸體硬扛、部位破壞與重砸硬直破勢），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身高密度乳白工程塑料鼴鼠太空工程偶體現復古太空玩具的扎實純真魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏雙拇指操作配置，戰鎚蓄力下砸動作帶有大範圍吸附與自適應地面鎖定判定，單拇指即可流暢完成站樁普攻連砸與破勢重擊。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實鼴鼠細密毛皮、地下泥濘習性與微小視力弱點**：徹底放棄現實鼴鼠的皮毛肉身與懼光特徵，全面轉譯為 2.2 頭身矮萌高密度工程塑料太空採礦裝甲與防爆護目鏡，以換取手機螢幕上的高辨識度與耐摔玩具質感；  
2. **放棄雙持雙手各拿一把採礦十字鎬的繁複動作方案**：為了避免在手機螢幕上雙手持械造成嚴重的紙娃娃圖層雜亂與穿模遮擋，放棄設計雙持採礦雙鎬，改為右手單手持握一把輪廓清晰、質量厚重的「星穹高頻等離子重鎚」，左爪維持自然抓握引力導向姿態。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "mole",
  "aliases": [
    "asteroid_mole",
    "prospector_mole",
    "orbital_mole",
    "space_mole",
    "clockwork_mole"
  ],
  "name_zh": "星岩鼴鼠",
  "name_en": "The Asteroid Mole",
  "class_archetype": "戰士 (Viking)",
  "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
  "lore_anchor": "巡弋於星穹軌道·外星基地「聚合物太空艙模組」與「高光懸空螢光軌道」，巡檢「太陽能帆板與微型排氣天線」與「太空拼裝維修船塢」，守望「高壓地熱升空彈射井·軌道受壓對接艙」與「垂直磁浮天軌·星穹軌道月台」，維護清理「軌道廢棄排障滑道」，依託防護「失重慣性磁力捕捉網」，並在「高真空抗靜電除塵室」保養除塵，配合宇航機器人隊長·螺栓隊長、太空發條小狗·萊卡波波與軌道站資深工程師·光纖婆婆；通體覆蓋高密度乳白工程塑料板件（ABS/POM）與冷軋鎢鋼骨架、防爆聚碳酸酯採礦護目頭盔、雙聯超導微型雷達葉片耳、軌道高抗衝擊防護工裝背帶褲、琥珀點陣LED採礦護目目鏡、圓筒形微型冷氣反推短尾、四葉微型發條天線鑰匙，雙手持握專屬星穹高頻等離子重鎚，以2.2頭身矮萌微胖體態、四足磁吸防滑工程矽膠吸盤滾足、失重磁吸定點霸體、高頻電漿震盪碎岩見長的高軌空間站採礦工程師與鋼鐵重裝戰士",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 古典鐵皮發條掘地鼴鼠與太空探索工程自動偶)",
    "posture": "2.2 頭身矮萌身軀沉穩屹立，四足磁吸吸盤牢牢吸附地面，雙爪平穩握持等離子重鎚立於身前偏右，背部冷氣噴管微幅排氣，天線發條鑰匙隨秒針每3.0秒跳拍一格勻速旋轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "乳白高密度工程塑料圓形面甲（#FFFDF8 / #38A0FF），前端配備防爆聚碳酸酯採礦護目罩與黃銅微型過濾閥，眼窩處精準中空供 optic_core 穿透",
    "ears": "頭部兩側對稱安裝雙聯超導微型雷達葉片耳（#FFD028 / #4ED86A），超薄黃銅片與薄荷光纖編織，隨走時脈衝微幅自轉，無生物耳廓",
    "torso_and_limbs": "高密度工程塑料板件（#FFFDF8）包覆冷軋鎢鋼框架，雙臂為重型沖壓合金多齒採礦爪，下身配置四足圓柱形腿部與防滑耐磨磁吸矽膠吸盤滾足",
    "tail": "短粗圓筒形高密度塑料冷氣反推排氣噴嘴（#38A0FF / #FF5E8A），末端帶珊瑚粉防撞橡膠環與四孔定向反推微型噴孔",
    "weapon_system": "單手挽持專屬「星穹高頻等離子重鎚（Orbital Plasma Sledgehammer）」，透明聚碳酸酯鎚身內嵌高頻電漿環，下砸釋放引力震盪，底層掛載 equipment.json 既有 anvil_hammer (tier 1)、iron_cudgel (tier 2) 與 bastion_blade (tier 3)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白工程塑料/拋光鋁鎳金屬，面罩基座高光、腹部抗靜電襯板與活動襯墊)",
    "primary": "#38A0FF (主色多巴胺天藍，太空採礦防護外殼、胸甲塗裝與重鎚鎚頭外罩)",
    "secondary": "#4ED86A (次色薄荷冷翡翠，雷達天線導光纖維、等離子重鎚聚能環與面罩刻度光圈)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，冷氣反推噴嘴防撞環、重鎚過載指示燈與發條軸心按鈕)",
    "metal": "#FFD028 (金屬天元黃銅金，四葉發條天線鑰匙、採礦爪同軸齒輪與重鎚金屬握柄)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_mole.png (品牌形象立牌)",
        "web/media/hero/char_mole.png (官網英雄展示立繪)",
        "docs/art/asteroid_mole_concept.png (概念立繪)",
        "game/assets/sprites/player/mole_idle.png (64x64 待機)",
        "game/assets/sprites/player/mole_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/mole_idle.png (隊伍待機)",
        "web/media/hero/mole_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/mole_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/mole_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/mole_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/mole_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/mole_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/mole_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/mole/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/mole.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/mole_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/asteroid_mole.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/mole/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_mole.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/asteroid_mole_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_mole.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/mole_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/mole_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/mole_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/mole_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/mole_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/mole_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/mole_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/mole/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/mole.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/asteroid_mole.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/mole/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行紅線**：本卡片為純企劃設計提案，**嚴禁執行任何產圖產片指令**。以下 Prompts 與參數為未來美術總監（sideart）或執行工程師（sideworker）派工產圖時之必備標準規範。

### 8.1 星岩鼴鼠角色單體立繪 Prompt（4:5 垂直角色畫）

```
chibi mechanical toy mole warrior, The Asteroid Mole, 2.2 head-body ratio, adorable chunky wind-up tinplate and engineering polymer automaton. Stamped milky-white ABS plastic body #FFFDF8 with celestial blue armor plating #38A0FF and mint-green trim #4ED86A, visible mechanical seams and titanium rivets #FFD028, absolutely zero animal fur, zero organic flesh, zero biological texture. Sturdy rounded polymer helmet with transparent polycarbonate mining visor revealing cheerful glowing amber LED dot-matrix eyes #FFA010. Equipped with heavy alloy digging shovel paws with brass gears. Crowned with dual miniature brass radar-vane antenna ears #FFD028 tipped with glowing mint fiber optics. Wearing a celestial-blue heavy-duty orbital astronaut sapper dungaree suit with tool latches and coral-pink emergency valve buttons #FF5E8A. On its back stands an imposing four-vane antenna brass wind-up key #FFD028 with a coral-pink center cap. Cylindrical cold-gas thruster tail with coral-pink bumper. Holding a massive high-tech transparent polymer plasma sledgehammer with glowing mint-green fusion core. Pure clean ivory white studio background, vibrant dopamine color palette, bold dark blue-purple clean outline #1F1A3A, cel shaded, MapleStory and Tata Adventure toy aesthetic, cheerful fairy tale lighting, masterpiece, 8k resolution.
```

### 8.2 星岩鼴鼠高軌星穹太空站場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
panoramic vibrant fairy tale scene in R07 Starfall Orbit Polymer Space Station. In the center foreground, a 2.2 head-body ratio cute mechanical toy mole warrior with glowing amber visor eyes and dual radar-vane ears, planting magnetic suction boots firmly on a glowing neon track, resting a massive glowing plasma sledgehammer on the platform in a heroic defensive stance. In the background, sprawling milky-white polymer astro-domes, luminescent neon mag-tracks, solar polymer sails with golden brass radar masts, and space assembly drydocks hovering in the zero-gravity void against a deep velvet cosmic sky with cheerful colorful star nebula lights. Distant egg-shaped space capsules floating by. Clean dark blue-purple outlines, vibrant dopamine colors (celestial blue #38A0FF, mint green #4ED86A, golden yellow #FFD028, warm orange #FFA010, coral pink #FF5E8A), zero dirt or dark grim filters, warm whimsical toy world, official splash art style.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt 內容>" \
  --aspect 4:5 \
  --ref branding/key_visual_main.png \
  --out docs/art/asteroid_mole_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt 內容>" \
  --aspect 16:9 \
  --ref branding/key_visual_main.png \
  --out docs/art/asteroid_mole_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R07_STARFALL_ORBIT.md` 既有地標（聚合物太空艙模組、高光懸空螢光軌道、太陽能帆板與微型排氣天線、太空拼裝維修船塢、高壓地熱升空彈射井·軌道受壓對接艙、垂直磁浮天軌·星穹軌道月台、軌道廢棄排障滑道、失重慣性磁力捕捉網、高真空抗靜電除塵室）與居民 NPC（宇航機器人隊長·螺栓隊長、太空發條小狗·萊卡波波、軌道站資深工程師·光纖婆婆），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`戰士 (Viking)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  戰士戰鎚遵循單手持握重鎚下砸與站樁姿態，左右肢體姿態描述清晰。
- [x] **CANON 世界憲章零毛皮鐵律**：  
  100% 零真動物肉身、零生物毛皮、零羽毛、零黏液；通體轉譯為乳白高密度工程塑料（ABS/POM）、冷軋鎢鋼骨架、沖壓合金採礦爪、防爆聚碳酸酯護目罩、雙聯超導雷達耳、點陣 LED 目鏡與四葉天線發條鑰匙。
- [x] **戰士戰鎚與戰斧對稱平衡**：  
  作為第十巡第二順位擴充，補齊戰士戰鎚第 5 款，與戰士戰斧（5 款）達成完全 5:5 對稱平衡！
