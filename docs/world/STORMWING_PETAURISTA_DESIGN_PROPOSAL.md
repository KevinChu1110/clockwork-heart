# 第五十八種動物「嵐翼鼯鼠（The Stormwing Petaurista）」世界觀與角色設計提案

> **標題**：第五十八種動物「嵐翼鼯鼠（The Stormwing Petaurista）」角色與世界觀設計提案  
> **提案代號**：`STORMWING_PETAURISTA_DESIGN_PROPOSAL`（代號：`petaurista` / 識別名：`race_petaurista`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_bfb447c8`（📖 世界觀｜第五十八種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零皮革、零動物肉身、零生物黏液、生漆打磨天然竹木拼花、高剛性椴木骨架、象牙白溫潤白瓷面甲、多節精密摺疊式漆竹翼膜連桿、多節同軸竹編平衡舵尾、外露精工黃銅鉚釘與球形鉸鏈、背後三葉禪韻風鈴黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R09_BAMBOO_GROVE.md`（第 1 行區域代號與名稱「R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo」、第 4 行「生漆陶瓷、高剛性天然竹木纖維、精密簧片木機關、溫潤青石板、精工黃銅關節與高彈性絲弦木偶套件」、第 6 行「局域走時狀態：空靈靜謐的呼吸式走時伴隨勻速破勢拍點（秒針每 3.0 秒在翠竹撞擊聲中發出清脆悠遠的木簧鐘聲「叮——咚！」，微風拂過竹梢時帶動微型簧片低吟，走時沉穩厚重而暗藏凌厲的爆發律動；需在竹浪搖曳與木人樁敲擊節奏中捕捉身法空檔）」、第 15 行「多巴胺竹翠綠（#4ED86A）、天元金黃（#FFD028）與水墨青石灰（#3A4454）飾帶」、第 19 行「發條天元竹海（Clockwork Bamboo Sea Slopes）」、第 20 行「青石武鬥古道場·演武坪（Slate Martial Dojo & Drill Ground）」、第 21 行「山門竹煙茶舍（Mountain Gate Tea Pavilion）」、第 22 行「飛瀑木簧水碓（Clockwork Waterfall Waterwheel & Pestle）」、第 29 行「古老重型零件輸送翻斗軌道·竹林終端站（Ancient Heavy Parts Conveyor Rail: Bamboo Terminal）」、第 30 行「晨曦天軌 9 號演武道場月台（Dawn Rail Platform 9: Zen Dojo Terminal）」、第 32 行「凌雲青竹懸索天梯·道場總站（Zen Bamboo Cableways: Dojo Terminal）」、第 33 行「天元雲海風帆渡口（Zen Sky-Ferry Port）」、第 35 行「翠竹彈力阻尼編織網（Elastic Bamboo Damping Web）」、第 56 行煮茶發條偶「阿茶（Acha）」、第 65 行天元道場武僧長老「圓空師傅（Master Yuan Kong）」、第 74 行機關木人樁小師弟「木木（Mu-Mu）」、第 51 行旗艦泰坦 BOSS「醉步發條武鬥熊貓·阿波泰坦（Titan Po the Drunken Clockwork Brawler Panda）」、第 87 行「狂風修羅木人傀儡」、第 92 行「嗜血機關青竹蛇」、第 96 行「醉仙滾動小熊貓機關偶」、第 125 行核心掉落零件「堅韌竹木纖維、高剛性宗師黃銅棘輪、重力調速金屬擺錘、精工黃銅高壓蓄能罐」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（忍者正式名稱 `ninja`，標籤宣言 `\"真假同色的一手\"`，武器 `dart`，數值 `atk: 2, def: 0, hp: -2, crit: 3.5, speed: 3`，玩法 `\"高速真假鏢影。同職也可玩匕首。\"`，初階武器 `mist_darts`）  
> - `game/data/tables/equipment.json`（飛鏢類正式 line: `\"dart\"`，初階武器：`mist_darts` 霧隱手鏢，中高階相容武器：`shadow_chakram` 影環飛刃）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡（第 55~60 族）第三順位核心擴充，補齊忍者 5:5 匕鏢超對稱平衡**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十八種動物擴充素體規格**。  
   在全專案相繼於第十巡首位成員第五十六種動物重閥河馬（騎士·長槍）與第二順位第五十七種動物星岩鼴鼠（戰士·戰鎚）順利補齊騎士與戰士對稱格局後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第三順位**，以靈動縹緲之姿輪轉進入全遊戲最具神速連擊、看破白霧、暴擊牽制與立體位移的核心職業——**忍者 (Ninja)** 體系，原生武器掛載於**八卦旋刃機關鏢（`dart` / 忍者·鏢）**。  
   嵐翼鼯鼠的加入，使全遊戲忍者機關鏢素體擴充至第 5 款（碧簧蛙、棘輪刺蝟、星翼蝙蝠、巡管守宮、嵐翼鼯鼠），與忍者匕首素體（烈焰虎、幽影貓、竹影青蛇、旋刃伶鼬、墨影烏賊 5 款）達成**完全對稱的 5:5 完美平衡格局**！
2. **經典玩具起源與古典機械發條滑翔鼯鼠機關工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與東方機關木偶史上的經典工藝原型：  
     ① **1930s-1950s 經典發條鐵皮空中特技滑翔機關偶（Vintage Tinplate Wind-up Acrobatic Glider Automaton / 德國 Schuco、Lehmann 與日本昭和野村 Nomura 名作）**，通體由沖壓薄馬口鐵骨架、彈簧摺疊翼板與同軸離心調速擒縱齒輪咬合而成，起跳釋放時雙側翼板伴隨清脆金屬聲「喀嗒——！」彈開展開滑翔，是古典玩具史上最具空氣動力學美感與機關巧思的自動偶之一；  
     ② **江戶時代東方機巧木偶·翻空飛鳶機關鼯鼠（Edo Karakuri Aerial Glider Automaton）**，圓滾敦厚的身軀採用高溫生漆陶瓷面甲與打磨竹木薄片榫卯嵌合，腹側配備多節同軸摺疊竹篾翼膜與扁平竹編舵尾，賦予角色在林梢氣流間輕盈懸浮、借風借力旋身穿透的優雅動態；  
     ③ **天元竹海風動擒縱鐘錶機關自動偶（Zen Bamboo Horological Glider）**，將經典風鈴音叉擒縱齒輪與氣動多角旋刃機關鏢結合，完美詮釋忍者職業「真假同色的一手、連擊速度快、看破身法」之忍者之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「生漆竹木拼花矮萌底盤、白瓷面甲硃砂忍者目鏡、雙聯薄竹葉聲納收音耳、多節同軸精密摺疊式漆竹翼膜連桿、多節竹編平衡舵短尾、竹影八卦旋刃機關鏢與三葉禪韻風鈴黃銅發條鑰匙」之天元竹林空嵐暗忍素體（Lacquered Bamboo Inlay Chassis, White Porcelain Cinnabar Visor Cowl, Bamboo-Leaf Sonar Ears, Folding Glider Wing-Harness, Segmented Bamboo-Weave Rudder Tail, Zen Octagonal Bamboo Shuriken & Three-Leaf Wind-Chime Brass Key）**。
3. **生態補足：終結天元竹林（R09）高空林冠空域無機關鏢忍者之歷史空白，打造林海制空巡檢哨**：  
   在全遊戲 9 大界域中，中下層東方武道沙盤界域 `R09 竹影道場·天元竹林` 先前擁有靈爪猴（武術家·爪）、瓷韻熊貓（武術家·拳）、玄機龜（法師·晶）、澄心水豚（法師·晶）、竹影青蛇（忍者·匕）與雲嵐鶴（遊俠·弓）共 6 族。  
   長久以來，竹影青蛇專注於低矮竹根石隙伏擊，雲嵐鶴專注於超遠距離定點狙擊，**面對天元竹海高空萬頃竹浪中搖擺的竹梢梢頭、深谷懸崖上方繚繞的雲霧氣流、以及暴走泰坦阿波揮舞竹棍掀起的狂暴氣浪，該界域完全缺乏一位能夠在林冠間張開摺疊翼膜乘風滑翔、凌空看破狂風死角、手持多角旋刃飛鏢高速牽制並打散敵人架勢的「高空滑翔機動忍者（Ninja）」**！嵐翼鼯鼠的降臨，徹底填補了 R09 高空林冠機動飛鏢素體的生態空白，為東方武術聖地注入了輕靈飄逸的空中武道魂！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源（僅登錄 races_specification 正表提案項目，total_races 維持現狀 56）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：嵐翼鼯鼠素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十七族武器與職業光譜全盤點

盤點現有首發五族與前五十二款擴充族（總計 57 族，含第 57 族星岩鼴鼠）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **星岩鼴鼠（The Asteroid Mole）**：戰士 (Viking) —— 星穹高頻等離子重鎚（`hammer`），失重磁吸定點霸體，高頻電漿震盪碎岩，引力波衝壓粉碎。
- **嵐翼鼯鼠（The Stormwing Petaurista）**：**忍者 (Ninja) —— 竹影八卦旋刃機關鏢（`dart`），高空滑翔翼展身法，竹梢微彈看破，破空音叉多段旋鏢牽制。**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）10 族（劍 5、槍 5，已達完全平衡）；
- 戰士（Viking）10 族（斧 5、鎚 5，已達完全平衡）；
- 武術家（Monk）9 族（拳 5、爪 4）；
- 法師（Mage）9 族（杖 5、晶 4）；
- 遊俠（Ranger）9 族（弓 5、銃 4）；
- 忍者（Ninja）此前在 57 族中擁有 9 款動物素體（匕首 5 款、機關鏢 4 款）；
- **本提案第五十八種動物正式作為「第十巡第三順位」核心擴充，歸屬於忍者 (Ninja) 體系，原生武器掛載於 `dart`（機關鏢 / 忍者·鏢）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`忍者 (Ninja)`**；
- 嵐翼鼯鼠的加入，使全遊戲忍者機關鏢素體擴充至第 5 款，忍者總數達成 10 款，匕首（5 款）與機關鏢（5 款）達成完全對稱的平衡格局！

### 1.2 嵐翼鼯鼠武器選擇：【竹影八卦旋刃機關鏢（Zen Octagonal Bamboo Shuriken）】

嵐翼鼯鼠原生專屬武器定名為：**【竹影八卦旋刃機關鏢（Zen Octagonal Bamboo Shuriken）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R09_BAMBOO_GROVE.md` 竹影道場·天元竹林之東方武道機關與高剛性竹木纖維工藝體系**！  
底層完全掛載於 `weapon_classes.json` 的 `dart`（忍者·鏢）類別，享有 `dart` 既有的「真假同色的一手」標籤宣言（Tagline: `\"真假同色的一手\"`）、連擊速度快、很吃白霧那種看破的打法、暴擊和命中都好之特性（`atk: 2, def: 0, hp: -2, crit: 3.5, speed: 3`），完美呼應 `R09_BAMBOO_GROVE.md` 第 6 行「秒針每 3.0 秒在翠竹撞擊聲中發出清脆悠遠的木簧鐘聲『叮——咚！』，微風拂過竹梢時帶動微型簧片低吟」之東方禪意空靈飛鏢手感！

- **法源素材咬合**：  
  完全對應 `R09_BAMBOO_GROVE.md` 第 4 行代表材質「高剛性天然竹木纖維、生漆陶瓷、精密簧片木機關」、第 19 行**「發條天元竹海（Clockwork Bamboo Sea Slopes）」**與第 125 行核心掉落零件**「堅韌竹木纖維（Tough Bamboo Fiber）」**與**「高剛性宗師黃銅棘輪（Master Brass Ratchet Cog）」**，將天元竹海的高彈性竹木與黃銅軸承轉化為撕裂氣流的多角旋刃飛鏢。
- **單持規範遵守（0-MKT7）**：  
  遵循 `review.md 0-MKT7` 單持規範，右手單持竹影八卦旋刃機關鏢（直徑約 28px，鏢身為八角弧刃沖壓薄鋼與高剛性壓縮竹片，中心嵌有一枚微型黃銅滾珠軸承，旋轉時自帶音叉共鳴孔）；左手五指自然舒展微曲，隨身側摺疊翼膜自然展開作滑翔氣流平衡姿態，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"dart\"` 的初階裝備 `mist_darts`（霧隱手鏢，tier 1）與中高階相容裝備 `shadow_chakram`（影環飛刃，tier 3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款機關鏢忍者（碧簧蛙、棘輪刺蝟、星翼蝙蝠、巡管守宮）絕不撞型之論證

雖然嵐翼鼯鼠與碧簧蛙、棘輪刺蝟、星翼蝙蝠、巡管守宮同屬 `ninja`（忍者）機關鏢（`dart`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               忍者職業鏢系武器五族差異化對照表（蛙 vs 刺蝟 vs 蝙蝠 vs 守宮 vs 鼯鼠）                               │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 碧簧蛙 (Frog)        │ 棘輪刺蝟 (Hedgehog)  │ 星翼蝙蝠 (Bat)       │ 巡管守宮 (Gecko)     │ 嵐翼鼯鼠 (Petaurista│
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 高彈跳牽制多段速射   │ 鋼刺自體收發展開飛刺 │ 失重立體懸停聲納鎖定 │ 管壁磁吸倒掛折射伏擊 │ 氣動翼膜滑翔旋身甩鏢│
│ 2. 動能來源     │ 腿部雙重螺旋彈簧蓄能 │ 單向棘爪棘輪發條釋放 │ 超導星紋微型引力陀螺 │ 巨輪城負壓氣動吸盤   │ 天元竹海山嵐氣動浮力│
│ 3. 步法特徵     │ 垂直高跳、落地微蹲   │ 圓球滾動、碎步小衝刺 │ 倒吊懸停、失重漂移滑行│ 扁平爬壁、四足吸盤伏地│ 竹梢彈躍、空中滑空懸浮│
│ 4. 武器構造     │ 三葉弧形旋刃翠綠木鏢 │ 淬火穿針鋼棘引線飛鏢 │ 五角超導螢光星紋鏢   │ 四角弧刃冷軋黃銅多角鏢│ 八角竹鋼嵌合音叉旋刃│
│ 5. 主題界域     │ R03 翡翠深林·發條蔓谷│ R02 晨曦小鎮·木偶集市│ R07 星穹軌道·外星基地│ R04 黃銅都市·巨輪城  │ R09 竹影道場·天元竹林│
│ 6. 材質質感     │ 沖壓薄銅板件、彈簧鋼 │ 拋光黃銅殼、淬火鋼棘 │ 聚碳酸酯翼、螢光光纖 │ 冷軋黃銅、深黑耐熱合金│ 溫潤白瓷、生漆竹木拼花│
│ 7. 角色剪影     │ 大腿曲折蓄力高蹲姿態 │ 圓滾弧形棘甲短促四肢 │ 寬幅機械摺疊翼倒錐形 │ 扁平爬行低重心多節齒尾│ 圓滾矮萌雙側張開滑翔翼│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴守 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md`，100% 徹底清除所有真皮毛、皮革、羽毛、生物肉身與泥土髒污，全面轉譯為精緻古典東方木機關與陶瓷自動偶質感：

- **溫潤白瓷面甲與打磨竹木拼花底盤**：嵐翼鼯鼠的身軀並非生物皮毛肉身，而是由天元道場工坊以**高溫燒製的溫潤象牙白瓷板件（Lacquered White Porcelain #FFFDF8）**與內部高剛性打磨竹木拼花骨架榫卯卡扣咬合而成。圓滾矮萌的 2.2 頭身軀幹由淡雅生漆竹木板件包覆，表面分佈著微型黃銅銷釘與防震接縫，絕無任何生物毛皮或動物皮屑。
- **多節精密摺疊式漆竹翼膜連桿**：鼯鼠標誌性的滑翔飛膜被徹底轉譯為一對**多節同軸精密摺疊式漆竹翼膜連桿（Lacquered Bamboo-Lath Folding Glider Wings）**。骨架由薄型高韌性實心竹篾與黃銅活動鉸鏈（#FFD028）鉚接，翼面覆蓋著高抗撕裂的薄層防水塗層和紙薄板（#4ED86A 薄荷竹翠綠），邊緣以極細黃銅壓條固定。平時自然摺疊收攏於身側兩脅，起跳滑翔時隨發條機構清脆「喀嗒——！」彈開展開，完全杜絕任何動物翼膜或肉質軟組織。
- **多節同軸竹編平衡舵短尾**：尾部並非毛茸茸的尾巴，而是一條**多節同軸竹編扁平平衡舵短尾（Segmented Bamboo-Weave Rudder Tail）**。尾芯為微型同軸發條鋼絲連桿，外包多層打磨平滑的薄竹編片，末端呈扁平橢圓形舵板，滑翔時隨氣流微幅擺動調整姿態，完全杜絕生物長毛。
- **雙聯薄竹葉聲納收音耳**：頭部兩側看似小巧圓耳的部位，實質上為一對微型「雙聯薄竹葉聲納收音耳（Bamboo-Leaf Sonar Acoustic Ears）」。耳廓由薄型生漆竹木薄片（#4ED86A）與微型黃銅轉軸（#FFD028）鉸接，隨走時脈衝與風向微幅顫動調焦，無任何生物耳廓肉質。
- **黑曜石英目鏡與硃砂暗忍面紋**：面部中央嵌有一對深邃通透的黑曜石英透鏡（Obsidian Quartz Goggles #1F1A3A），眼眶邊緣手工手繪著傳統東方戲劇硃砂紅印記（#FF5E8A），待機時散發平靜清明的微光，鎖定破勢時瞳孔中浮現出微型金色八卦游標刻度。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格遵循 Kevin 與使用者畫像核心審美原則：
- **比例**：矮萌可愛的 2.0 ~ 2.2 頭身比，頭大身小，四肢圓短精巧，站立時微屈雙膝，雙爪捧鏢於身前，側身滑翔姿態極具動感。
- **多巴胺鮮亮高飽和色盤（拒絕暗黑泥土灰黑）**：
  - **奶油白瓷底色（#FFFDF8）**：白瓷面頰、腹部襯板高光，溫潤乾淨，杜絕髒濁。
  - **多巴胺薄荷竹翠綠（#4ED86A）**：竹木外殼、摺疊滑翔翼膜主色、八角旋刃飛鏢鏢刃塗裝。
  - **多巴胺天藍（#38A0FF）**：暗忍胸甲飾邊、石英目鏡反光、水墨漸層流蘇。
  - **多巴胺金黃（#FFD028）**：三葉發條鑰匙、黃銅鉸鏈、飛鏢中心滾珠軸承與關節鉚釘。
  - **多巴胺珊瑚粉 / 硃砂紅（#FF5E8A）**：眼角忍者面紋、發條鑰匙中心按鈕、飛鏢中心標記。
  - **深藍紫立體手繪描邊（#1F1A3A）**：高反差立體外輪廓線，取代傳統髒黑泥土色。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

拒絕靜止死板木樁，為嵐翼鼯鼠設計活靈活現的 Q 版發條動態：
- **待機呼吸感（Idle Breathing）**：
  - 2.2 頭身身軀每 2.2 秒進行一次微幅上下起伏，兩側摺疊竹翼隨呼吸微幅開合 3~5 度，展現如輕巧呼吸般的氣動浮力；
  - 扁平竹編舵尾以 0.4 秒微延遲自然呈波浪形輕輕上下拍動；
  - 背後三葉禪韻風鈴黃銅發條鑰匙隨秒針每 3.0 秒跳動一格勻速自轉，發出微弱空靈的風鈴木簧鐘聲。
- **待機專屬小動作（Special Idle Animations）**：
  - **「試翼彈風」**：每隔 9 秒，鼯鼠雙爪向兩側微張，身側摺疊竹翼驟然彈開至半展狀態「喀嗒！」，身軀微懸浮離地 4px，隨後輕盈收回，神態靈巧機警；
  - **「指尖轉鏢」**：右手單手將竹影八卦旋刃鏢在食指尖如微型竹蜻蜓般高速自轉一圈，發出清脆的「咻——！」破空聲，隨後穩穩抓回胸前。
- **Poke 點擊互動（點擊反應反饋）**：
  - 玩家以手指點擊角色時，嵐翼鼯鼠被戳得向後輕盈空翻半圈，兩側摺疊翼膜完全展開如微型滑翔傘，懸停空中 0.5 秒後輕巧落回原位，發出「咻——嗒！」的木簧回彈音；
  - 頭頂彈出俏皮對話氣泡：「**天元之風，吹得動整片竹海呢！**」或「**看破身法，這一下可刺不中我喔！**」，周身爆散出 4~6 枚半透明薄荷綠竹葉光芒粒子與天元金黃星芒。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R09 竹影道場·天元竹林高空林冠空域無機關鏢忍者之歷史空白

在全專案九大界域中，中下層東方武道沙盤界域 `R09 竹影道場·天元竹林` 雖然擁有強大的地面武僧、伏地刺客與遠程神射手，但在面對懸崖深谷上方掠過的強勁山嵐、以及暴走巨偶「醉步發條武鬥熊貓·阿波泰坦」揮舞重柱掀起的竹浪風暴時，**長久以來完全缺乏一位能夠在林梢借風滑翔、在高空視野中洞悉敵方重心轉移破綻、並以超高頻多角旋刃進行空中壓制牽制的「高空滑翔機動忍者」**。嵐翼鼯鼠的入駐，補齊了 R09 最靈動的空中防衛線。

### 3.2 100% 逐字對齊引用 `docs/world/regions/R09_BAMBOO_GROVE.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R09_BAMBOO_GROVE.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 於萬頃青竹隨風搖曳的**「發條天元竹海（Clockwork Bamboo Sea Slopes）」**（`R09_BAMBOO_GROVE.md` 第 19 行）竹梢間借風滑翔，巡查竹節內部微型扭簧的共振狀態；
  - 降落於孤峰之巔的**「青石武鬥古道場·演武坪（Slate Martial Dojo & Drill Ground）」**（`R09_BAMBOO_GROVE.md` 第 20 行），在黃銅太極齒輪陣列上方演練空中旋身甩鏢身法；
  - 掠過常年蒸騰白熱茶煙的**「山門竹煙茶舍（Mountain Gate Tea Pavilion）」**（`R09_BAMBOO_GROVE.md` 第 21 行），取用高純度清香竹露潤滑油保養雙翼黃銅鉸鏈；
  - 穿梭於飛瀉而下的流泉之畔**「飛瀑木簧水碓（Clockwork Waterfall Waterwheel & Pestle）」**（`R09_BAMBOO_GROVE.md` 第 22 行），監測水車帶動的石臼研磨節奏；
  - 沿西南山谷巡查**「古老重型零件輸送翻斗軌道·竹林終端站（Ancient Heavy Parts Conveyor Rail: Bamboo Terminal）」**（`R09_BAMBOO_GROVE.md` 第 29 行），為來自荒漠舊庫的礦車護航；
  - 駐守山門外緣懸空挑台**「晨曦天軌 9 號演武道場月台（Dawn Rail Platform 9: Zen Dojo Terminal）」**（`R09_BAMBOO_GROVE.md` 第 30 行），迎接自中央天宮大廳抵達的發條吊艙；
  - 借後山試煉絕頂的**「凌雲青竹懸索天梯·道場總站（Zen Bamboo Cableways: Dojo Terminal）」**（`R09_BAMBOO_GROVE.md` 第 32 行）上升氣流盤旋巡視；
  - 展翼俯瞰沙盤東側飛瀑邊緣的**「天元雲海風帆渡口（Zen Sky-Ferry Port）」**（`R09_BAMBOO_GROVE.md` 第 33 行），為出航的發條滑翔飛舟引導航向；
  - 依託沙盤邊界的**「翠竹彈力阻尼編織網（Elastic Bamboo Damping Web）」**（`R09_BAMBOO_GROVE.md` 第 35 行），作為高空特技翻滾的彈跳緩衝跳板。
- **核心 NPC 互動情境**：
  - 與**煮茶發條偶·阿茶（Acha the Tea-Brewing Puppet）**（`R09_BAMBOO_GROVE.md` 第 56 行）品茗對坐，以竹露茶洗滌機芯塵埃，靜心調校旋刃飛鏢的平衡重心；
  - 接受**天元道場武僧長老·圓空師傅（Master Yuan Kong）**（`R09_BAMBOO_GROVE.md` 第 65 行）的空中身法點撥，領悟「乘風借力·破勢在動」的無上飛鏢奧義；
  - 指導**機關木人樁小師弟·木木（Little Dummy Mu-Mu）**（`R09_BAMBOO_GROVE.md` 第 74 行）修復脫落的木銷手臂，並示範如何在狂風中保持步伐平穩。
- **守護泰坦作戰支援**：
  - 面對失控的古代頂級機關獸**「醉步發條武鬥熊貓·阿波泰坦（Titan Po）」**（`R09_BAMBOO_GROVE.md` 第 51 行），嵐翼鼯鼠利用空中滑翔避開阿波泰坦狂暴揮擊的重型竹棍，自空中俯衝投擲八卦旋刃機關鏢，精準擊中卡死阿波背脊主軸的青銅指針榫頭，為地面進攻隊友創造關鍵破勢時機！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，嵐翼鼯鼠的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 嵐翼鼯鼠專屬造型規格與材質特徵（嚴守 100% 零真皮毛、零皮革）                                    │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. body (素體)  │ 生漆竹木拼花矮萌底盤（#FFFDF8 / #4ED86A），打磨椴木骨架與白瓷胸腹板，四肢精工黃銅球形鉸鏈       │
│ 2. head (頭部)  │ 白瓷竹葉耳暗忍面甲兜帽（#FFFDF8 / #4ED86A），象牙白瓷面頰配生漆竹片兜帽，無生物毛髮口鼻組織     │
│ 3. ears (耳部)  │ 雙聯薄竹葉聲納收音耳（#4ED86A / #FFD028），天然竹篾複合壓製，黃銅微型轉軸鉸接，隨風微動，無肉耳 │
│ 4. tail (尾部)  │ 多節同軸竹編平衡舵短尾（#4ED86A / #FFD028），多層薄竹編片內嵌鋼絲連桿，末端扁平橢圓舵板       │
│ 5. costume (服裝)│ 天元竹林摺疊翼膜暗忍胸甲（#4ED86A / #1F1A3A），雙脅配備多節同軸摺疊竹篾翼膜與黃銅快拆胸扣帶   │
│ 6. optic_core(眼)│ 黑曜石英目鏡硃砂忍者面甲（#1F1A3A / #FF5E8A），黑曜石英透鏡嵌白瓷面甲，眼眶繪硃砂紅忍者飾紋     │
│ 7. winding_key  │ 三葉禪韻風鈴黃銅發條鑰匙（#FFD028 / #FF5E8A），背部挺立三葉風鈴音叉造型，中心嵌珊瑚粉防塵鉚釘 │
│ 8. weapon (武器)│ 竹影八卦旋刃機關鏢（#4ED86A / #FFD028 / #1F1A3A），八角沖壓鋼刃嵌竹纖維核心，帶黃銅軸承與音叉孔│
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`body`（素體底盤）**：  
   2.2 頭身 Q 版矮萌身軀，由高密度生漆打磨天然竹木拼花（#4ED86A / #FFFDF8）包覆打磨椴木骨架製成。胸腹部嵌有平滑溫潤的象牙白瓷襯板，四肢關節為光滑的精工黃銅球形鉸鏈（#FFD028）。下身配置短促靈活的雙足，足底裝配防滑耐磨橡膠減震軟墊，踏步時在青石板上留下清脆踏音，徹底杜絕任何真實生物毛皮質感。
2. **`head`（頭部與兜帽）**：  
   圓滾光潔的白瓷半球形頭部面甲，兩側配有生漆竹片編織的暗忍護額與護腮。面部正前方眼眶處精準沖孔供 `optic_core` 透光，鼻樑轉譯為細緻的竹節通風濾口，整體呈現出東方傳統木偶與現代發條玩具交融的雅緻美感。
3. **`ears`（竹葉聲納耳）**：  
   頭部兩側對稱安裝的一對微型竹葉聲納收音耳。耳片由天然竹纖維與薄黃銅箔（#FFD028）複合壓製，外形宛如兩片修長挺拔的翠綠嫩竹葉，隨走時律動與高空風向微幅自轉顫動，無任何肉質耳廓組織。
4. **`tail`（竹編平衡舵短尾）**：  
   長度約為身高的 1/4，由多節同軸打磨薄竹編片以發條鋼絲串聯而成。末端呈扁平橢圓形的空氣動力學平衡舵，在空中滑翔時微幅擺動以調整偏航與仰角，落地時自然收攏微翹。
5. **`costume`（摺疊翼膜胸甲）**：  
   由深藍紫（#1F1A3A）防塵高韌生漆竹片與耐磨帆布組合製成的暗忍練功胸甲。最大特色為雙脅兩側配置的**多節同軸精密摺疊式漆竹翼膜連桿**，平時緊密摺疊收攏，跳躍時受胸甲彈簧聯動瞬間彈開成扇形滑翔翼膜，邊緣帶有天元金黃銅加固邊條。
6. **`optic_core`（黑曜目鏡面紋）**：  
   一對深邃明亮的黑曜石英透鏡（#1F1A3A）。平時透出寧靜深沉的微光，眼角周圍繪有亮麗的硃砂紅忍者面紋（#FF5E8A），進入看破蓄力狀態時，鏡片中心泛起一圈翠綠色與金黃色交織的八卦方位羅盤刻度。
7. **`winding_key`（風鈴發條鑰匙）**：  
   背部中央挺立的三葉禪韻風鈴黃銅發條鑰匙。採用天元黃銅金（#FFD028）精鑄，造型宛如三片典雅的風鈴葉片圍繞中心樞軸排列，樞軸內嵌一枚珊瑚粉防塵鉚釘。隨秒針每 3.0 秒跳動一格勻速旋轉，發出微弱清脆的風鈴金鳴。
8. **`weapon`（八卦旋刃機關鏢）**：  
   嵐翼鼯鼠專屬武器【竹影八卦旋刃機關鏢】。直徑約身高的 1/3，外圈為八角弧形鋒利沖壓冷軋薄鋼刃，內芯為高剛性高密度壓縮竹木纖維，中心嵌入一枚微型黃銅滾珠軸承與音叉破空孔。擲出時在空中高速自轉，發出如山泉琴鳴般的「咻——！」破空嘯音。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 側身45度輕靈站姿，雙爪捧鏢於胸前，雙側竹篾翼膜收攏，背後三葉風鈴鑰匙勻速自轉，竹編舵尾微翹微擺│
│ 2. attack (普攻)  │ 踏空滑步半步，右手腕部微型棘輪驟響，將八角機關鏢高速甩手平射擲出，雙側翼膜微張維持平衡，破空流光│
│ 3. hit (受擊)     │ 身軀受震向後微仰浮空，雙側翼膜如降落傘般瞬間彈開吃風減速，落地滑退半步，面甲硃砂紋光圈閃爍   │
│ 4. recover (硬直) │ 雙足抓穩青石地面，迅速收攏翼膜，右手橫握機關鏢護於胸前，黑曜石英目鏡準星收縮重置，氣息調勻   │
│ 5. skill (技能)   │ 借竹梢動能騰空躍起，摺疊翼膜完全展開乘風滑翔，半空中幻化為殘影甩出4枚八角機關鏢化作漫天竹暴風│
│ 6. telegraph (蓄力│ 身軀壓低伏於地面，雙爪按地蓄力，背後雙翼微開呈蓄勢彈射狀，右手機關鏢在指尖高速空轉發出音叉嗡鳴│
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為忍者職業機關鏢系的核心擴充素體，直接提供空中滑翔機動、超高頻多角旋刃牽制與破空看破白霧的高操作上限戰鬥體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過忍者機關鏢的高速真假鏢影、多段連擊破勢與看破白霧打法），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身高溫白瓷面甲與摺疊竹篾翼膜鼯鼠自動偶體現東方古典玩具的機巧靈動魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏雙拇指操作配置，機關鏢投擲動作帶有自適應扇形鎖定判定，單拇指即可輕鬆完成空中滑步點射、走位牽制與技能釋放。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實鼯鼠濃密毛皮、長毛大尾與夜行性畏光習性**：徹底放棄現實鼯鼠的皮毛肉身與夜行特徵，全面轉譯為 2.2 頭身矮萌溫潤白瓷面甲、打磨竹木拼花骨架與摺疊竹篾滑翔翼，以換取手機螢幕上的高辨識度與耐摔玩具質感；  
2. **放棄雙持雙手各擲一枚機關鏢的複雜動作方案**：為了避免在手機螢幕上雙手持鏢造成嚴重的紙娃娃圖層雜亂與穿模遮擋，放棄設計雙持雙飛鏢，嚴格遵守 `0-MKT7` 單持規範，改為右手單手持握一枚輪廓清晰、高速自轉的「竹影八卦旋刃機關鏢」，左爪維持自然舒展的滑翔氣流平衡姿態。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "petaurista",
  "aliases": [
    "stormwing_petaurista",
    "flying_squirrel",
    "glider",
    "zen_petaurista",
    "clockwork_petaurista"
  ],
  "name_zh": "嵐翼鼯鼠",
  "name_en": "The Stormwing Petaurista",
  "class_archetype": "忍者 (Ninja)",
  "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
  "lore_anchor": "滑翔於竹影道場·天元竹林「發條天元竹海」與「青石武鬥古道場·演武坪」，穿梭於「山門竹煙茶舍」與「飛瀑木簧水碓」，巡檢「古老重型零件輸送翻斗軌道·竹林終端站」與「晨曦天軌 9 號演武道場月台」，守望「凌雲青竹懸索天梯·道場總站」與「天元雲海風帆渡口」，依託防護「翠竹彈力阻尼編織網」，配合煮茶發條偶·阿茶、天元道場武僧長老·圓空師傅與機關木人樁小師弟·木木；通體覆蓋高溫象牙白瓷面甲與生漆竹木拼花底盤、白瓷竹葉耳暗忍面甲兜帽、雙聯薄竹葉聲納收音耳、多節同軸精密摺疊式漆竹翼膜連桿、多節同軸竹編平衡舵短尾、三葉禪韻風鈴黃銅發條鑰匙，右手單持專屬竹影八卦旋刃機關鏢，以2.2頭身矮萌微胖體態、四肢精工黃銅球形鉸鏈、竹梢微彈看破、高空滑翔翼展身法與破空音叉多段旋鏢牽制見長的東方武道機巧暗忍",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1930s-1950s 古典鐵皮空中特技滑翔機關偶與東方機巧木偶)",
    "posture": "2.2 頭身矮萌身軀側身45度輕靈站立，雙足微屈抓地，雙爪捧八卦機關鏢立於胸前，身側摺疊竹翼收攏，舵尾微翹，三葉風鈴發條鑰匙隨秒針每3.0秒跳拍一格勻速自轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "溫潤象牙白瓷圓形面甲（#FFFDF8 / #4ED86A），頭頂配備生漆打磨竹片暗忍兜帽與竹節濾氣孔，眼眶處精準中空供黑曜石英目鏡穿透",
    "ears": "頭部兩側對稱安裝雙聯薄竹葉聲納收音耳（#4ED86A / #FFD028），天然竹篾壓製薄片配微型黃銅轉軸，隨風顫動調焦，無肉耳",
    "torso_and_limbs": "打磨椴木骨架外包生漆竹木板件（#4ED86A）與白瓷胸板，雙脅配備多節同軸摺疊竹篾滑翔翼膜連桿，四肢為精工黃銅球形鉸鏈",
    "tail": "多節同軸打磨薄竹編片平衡舵短尾（#4ED86A / #FFD028），內嵌微型發條鋼絲連桿，末端為扁平橢圓舵板",
    "weapon_system": "右手單持專屬「竹影八卦旋刃機關鏢（Zen Octagonal Bamboo Shuriken）」，八角沖壓鋼刃嵌竹纖維核心，自帶滾珠軸承與破空音叉孔，底層掛載 equipment.json 既有 mist_darts (tier 1) 與 shadow_chakram (tier 3)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白瓷/打磨椴木高光，面甲基座、胸腹白瓷襯板與手爪關節)",
    "primary": "#4ED86A (主色多巴胺薄荷竹翠綠，竹木外殼、摺疊滑翔翼膜與機關鏢鏢刃塗裝)",
    "secondary": "#38A0FF (次色多巴胺天藍，暗忍胸甲飾邊、石英目鏡反光與水墨漸層流蘇)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉/硃砂紅，眼眶忍者面紋、發條鑰匙中心按鈕與飛鏢中心標記)",
    "metal": "#FFD028 (金屬天元黃銅金，三葉風鈴發條鑰匙、黃銅活動鉸鏈與飛鏢中心軸承)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_petaurista.png (品牌形象立牌)",
        "web/media/hero/char_petaurista.png (官網英雄展示立繪)",
        "docs/art/stormwing_petaurista_concept.png (概念立繪)",
        "game/assets/sprites/player/petaurista_idle.png (64x64 待機)",
        "game/assets/sprites/player/petaurista_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/petaurista_idle.png (隊伍待機)",
        "web/media/hero/petaurista_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/petaurista_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/petaurista_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/petaurista_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/petaurista_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/petaurista_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/petaurista_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/petaurista/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/petaurista.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/petaurista_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/stormwing_petaurista.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/petaurista/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_petaurista.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/stormwing_petaurista_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_petaurista.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/petaurista_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/petaurista_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/petaurista_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/petaurista_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/petaurista_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/petaurista_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/petaurista_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/petaurista/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/petaurista.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/stormwing_petaurista.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/petaurista/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行提醒（嚴守任務邊界）**：本任務為「只寫文件，不產圖不產片」。以下提示詞僅作企劃歸檔與規格預置，等待後續美術產圖任務由 sideart 領取執行。

### 8.1 嵐翼鼯鼠角色單體立繪 Prompt（4:5 垂直角色畫）

```text
masterpiece, best quality, 2.2 head-to-body ratio chibi cute clockwork mechanical toy flying squirrel ninja hero, named The Stormwing Petaurista, standing dynamically on a weathered slate stone pedestal in a misty bamboo forest. Made of glazed ivory-white porcelain faceplate, polished green lacquered bamboo wood shell, and warm brass joints. Distinctive folding bamboo-lath glider wing flaps attached between arms and flanks with tiny brass hinges, half-spread in aerodynamic posture. Wearing a miniature dark navy ninja vest, obsidian quartz goggle lenses with red cinnabar ninja eye-markings, dual upright bamboo-leaf acoustic ears, and a segmented bamboo-weave flat rudder tail. Holding a spinning octagonal bamboo-and-steel shuriken dart in right hand, left hand slightly curved for gliding balance. A prominent three-leaf wind-chime brass winding key prominently mounted on the center back. Clean, dopamine vibrant candy-like colors, mint emerald green #4ED86A, ivory white #FFFDF8, gold brass #FFD028, sky blue #38A0FF, coral pink #FF5E8A, bold dark blue-purple outline #1F1A3A, soft Tyndall morning sunlight, zero fur, zero skin, zero feathers, pure mechanical wooden and porcelain toy automaton, 4:5 aspect ratio.
```

### 8.2 嵐翼鼯鼠天元竹林道場場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```text
panoramic vibrant fairy tale scene in R09 Bamboo Grove Zen Puppet Dojo. In the center foreground, a 2.2 head-body ratio cute mechanical toy flying squirrel ninja with spread folding bamboo glider wings leaps gracefully between high swaying bamboo stalks, right hand throwing a glowing octagonal bamboo shuriken dart leaving emerald-and-gold light trails in the air. In the background, sprawling misty bamboo sea slopes with floating morning mists, ancient slate martial dojo training grounds with gear-shaped zen patterns, mountain tea pavilion with gentle steam, waterfall waterwheel, and distant floating island horizons under soft golden morning sky. Dopamine bright cheerful palette, mint green, gold, ivory white, coral pink, crisp clockwork toy aesthetic, bold stylized outlines, zero real fur, zero feathers, wide-angle cinematic 16:9 aspect ratio.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 4:5 \
  --out docs/art/stormwing_petaurista_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 16:9 \
  --out docs/art/stormwing_petaurista_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R09_BAMBOO_GROVE.md` 既有地標（發條天元竹海、青石武鬥古道場·演武坪、山門竹煙茶舍、飛瀑木簧水碓、古老重型零件輸送翻斗軌道·竹林終端站、晨曦天軌 9 號演武道場月台、凌雲青竹懸索天梯·道場總站、天元雲海風帆渡口、翠竹彈力阻尼編織網）與居民 NPC（煮茶發條偶·阿茶、天元道場武僧長老·圓空師傅、機關木人樁小師弟·木木、旗艦泰坦 BOSS「醉步發條武鬥熊貓·阿波泰坦」），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`忍者 (Ninja)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  右手單持竹影八卦旋刃機關鏢，左手自然舒展作滑翔氣流平衡姿態，左右肢體姿態描述清晰，0 雙持穿模。
- [x] **CANON 世界憲章零毛皮零皮革鐵律**：  
  100% 零真動物肉身、零生物毛皮、零皮革、零羽毛、零黏液；通體轉譯為象牙白溫潤白瓷面甲、生漆打磨天然竹木拼花、打磨椴木骨架、多節同軸精密摺疊式漆竹翼膜連桿、多節同軸竹編平衡舵短尾、黑曜石英目鏡、硃砂紅印記與三葉禪韻風鈴黃銅發條鑰匙。
- [x] **忍者機關鏢與匕首對稱平衡**：  
  作為第十巡第三順位擴充，補齊忍者機關鏢第 5 款，與忍者匕首（5 款）達成完全 5:5 對稱平衡！
