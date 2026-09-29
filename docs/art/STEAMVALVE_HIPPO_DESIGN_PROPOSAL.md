# 第五十六種動物「重閥河馬（The Steamvalve Hippo）」世界觀與角色設計提案

> **標題**：第五十六種動物「重閥河馬（The Steamvalve Hippo）」角色與世界觀設計提案  
> **提案代號**：`STEAMVALVE_HIPPO_DESIGN_PROPOSAL`（代號：`hippo` / 識別名：`race_hippo`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：阿宏（側案·程式 sideworker）  
> **對應看板任務**：`t_a7c53638`（📖 世界觀｜第五十六種動物紙娃娃角色設計提案（只寫文件，不產圖不產片））  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零動物肉身、零生物黏液、沖壓厚鑄耐壓黃銅板件、冷軋鎢鋼承重骨架、外露球窩減震活塞四肢、雙聯旋轉式微型氣壓安全洩壓閥門耳、雙聯同軸高壓石英壓力表目鏡、雙聯蒸氣排氣壓載水箱、外露螺栓鉚釘、背後雙聯閥門輪轂黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R04_BRASS_METROPOLIS.md`（第 1 行區域代號與名稱「R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City」、第 4 行「沖壓厚鑄黃銅板、冷軋鎢鋼外齒輪、耐熱微型蒸氣管網與高壓鎢絲指針儀表套件」、第 6 行「局域走時狀態：急促超頻伴隨高壓陣發排氣（秒針每 1.5~2 秒急促跳動一格，伴隨蒸氣閥陣發性釋放鳴笛；動能狂暴充沛，齒輪咬合緊密，需掌握蒸氣洩壓拍點穿行於重型機具之間）」、第 19 行「防滑菱形斜紋沖壓黃銅地磚」、第 20 行「摩天齒輪工坊群（Great Cog Skyspires）」、第 21 行「高壓蒸氣管道網（High-Pressure Steam Conduits）」、第 22 行「自律工廠與天街吊橋（Automated Foundry & Sky Bridges）」、第 23 行「鎢絲防爆街燈（Tungsten Filament Streetlamps）」、第 30 行「高架重軌引橋·巨輪城站（High Brass Viaduct: Metropolis Terminal）」、第 36 行「磁吸緩衝防墜鋼網」、第 44 行「鐵皮發條工程師（Tinplate Clockwork Engineers）」、第 45 行「蒸氣鍋爐巡檢犬」、第 48 行「中央蒸氣沐浴池（Central Degreasing Bath）」、第 51 行「超壓危機（Overpressure Crisis）」、第 56 行總工技師「銅齒（Cogsmith）」、第 65 行管道巡檢員「小鎢（Tungsten）」、第 73 行老鐘錶匠「星擺（Starpendulum）」、第 102 行旗艦泰坦 BOSS「城防泰坦·巨輪霸主（Titan Fortress: Greatcog the Iron Juggernaut）」、第 107-109 行「主活塞、過熱洩壓排氣閥、重裝合金裝甲板」、第 163 行與第 240 行「中央動力廣場（Central Power Plaza）」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（騎士正式名稱 `knight`，標籤宣言 `\"盾後無死角\"`，武器 `spear`，數值 `atk: 0, def: 2, hp: 4, crit: -1.0, speed: -1`，玩法 `\"中距控場、防禦迎擊、格擋反震、穿刺衝鋒。\"`，初階武器 `knight_pike`）  
> - `game/data/tables/equipment.json`（槍類正式 line: `\"spear\"`，初階相容武器：`knight_pike` 騎士長槍，高階相容武器：`ash_spear` 灰燼長槍）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡（第 55~60 族）第一順位重磅領銜擴充，開啟六大職業新十巡循環**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十六種動物擴充素體規格**。  
   在全專案於前五十五族（始祖白金兔 + 54 款擴充族）完美達成六大職業 9×6=54 族超對稱平衡收官之後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第一順位**，以領銜之姿輪轉進入最具厚重防線、迎擊控場、衝刺破陣與防禦反震的核心職業——**騎士 (Knight)** 體系，原生武器掛載於**皇家長槍 / 活塞重裝長槍（`spear` / 騎士·長槍）**。  
   重閥河馬的加入，使全遊戲騎士長槍素體擴充至第 5 款（烈鬃獅、星軌犬、破浪旗魚、旋音天鵝、重閥河馬），與騎士長劍素體（白金兔、荒原鋼狼、巡林松鼠、鐵蹄駿駒、熔鎧犰狳 5 款）達成**完全對稱的 5:5 完美平衡格局**！
2. **經典玩具起源與古典機械發條河馬自動機工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與蒸氣工業自動機史上的經典工藝原型：  
     ① **1930s-1950s 經典古典發條鐵皮河馬自動機（Vintage Tinplate Wind-up Hippo Automaton / 德國 Schuco、Lehmann 與日本昭和金屬玩具名作）**，通體由沖壓馬口鐵板、雙偏心凸輪連動下頜大嘴開合與四足步進機構咬合而成，走動時大嘴伴隨機械咬合節奏張合釋放內部壓力，是古典玩具史上最具重量感與憨萌反差的機械自動偶之一；  
     ② **全球著名機械彈簧河馬玩具（Hungry Hippos Mechanical Spring Toys）**之高剛性槓桿回彈結構與重力低重心底盤，賦予角色沉穩防禦、反震回彈的物理手感；  
     ③ **維多利亞時代工業蒸氣管道洩壓自動檢測偶（Victorian Steam Manometer & Ballast Automaton）**，圓滾敦厚的身軀裝配防爆指針壓力表、旋轉排氣安全閥門與重載水力壓載水箱，完美詮釋騎士職業「盾後無死角、中距控場、防禦迎擊、格擋反震」之騎士之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「沖壓厚鑄耐壓黃銅矮萌底盤、安全洩壓閥門耳、雙聯同軸高壓石英壓力表目鏡、高壓抗震鉚釘胸甲、雙聯蒸氣排氣壓載箱、重閥活塞衝刺長槍與雙聯閥門輪轂發條鑰匙」之重裝防禦反震騎士素體（Steamvalve Brass Hippo Chassis, Ballast Safety-Valve Cowl, Pressure Gauge Optic Core, High-Pressure Cuirass, Dual Steam Exhaust Ballast Curio, Steamvalve Piston Heavy Lance & Valve Handwheel Brass Key）**。
3. **生態補足：終結黃銅都市·巨輪城（R04）長久無常駐專屬城防長槍騎士之生態空白**：  
   在全遊戲 9 大界域中，中高層重工業沙盤界域 `R04 黃銅都市·巨輪城` 先前擁有鋼岳象（戰士·斧）、幽影貓（忍者·匕）、鐵拳袋鼠（武術家·拳）、鋼臂巨猩（武術家·拳）、星儀渡鴉（法師·杖）、巡管守宮（忍者·鏢）與振律啄木鳥（遊俠·銃）共 7 族。  
   長久以來，面對摩天齒輪架、天街吊橋與全城管網陷入的「超壓危機（Overpressure Crisis）」，**該界域完全缺乏一位能夠在天街與重軌高架上築起防線、以超重裝低重心硬抗超壓蒸氣衝擊、手持活塞長槍迎擊暴走自律機關的「重裝城防守護騎士（Knight）」**！重閥河馬的加入，徹底填補了 R04 長期缺乏專屬長槍騎士素體的生態空白，讓 R04 的防衛體系迎來首位厚重鋼鐵壁壘，與戰士象的重劈、巨猩的重拳、啄木鳥的火銃、守宮的飛鏢共同構築巨輪城堅不可摧的安防生態！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源（僅登錄 races_specification 正表提案項目，total_races 維持現狀 54）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：重閥河馬素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十五族武器與職業光譜全盤點

盤點現有首發五族與前五十款擴充族（總計 55 族，含第 55 族鐘塔長頸鹿）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **重閥河馬（The Steamvalve Hippo）**：**騎士 (Knight) —— 重閥活塞衝刺長槍（`spear`），蒸氣超壓衝程，沉穩低重心防禦反震，雙聯排氣鳴笛迎擊。**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 戰士（Viking）9 族（鎚 5、斧 4）；
- 忍者（Ninja）9 族（匕 5、鏢 4）；
- 武術家（Monk）9 族（拳 5、爪 4）；
- 法師（Mage）9 族（杖 5、晶 4）；
- 遊俠（Ranger）9 族（弓 5、銃 4）；
- 騎士（Knight）此前在 55 族中擁有 9 款動物素體（劍 5 款、槍 4 款）；
- **本提案第五十六種動物正式作為「第十巡第一順位」領銜擴充，歸屬於騎士 (Knight) 體系，原生武器掛載於 `spear`（皇家長槍 / 騎士·長槍）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`騎士 (Knight)`**；
- 重閥河馬的加入，使全遊戲騎士長槍素體擴充至第 5 款，騎士總數達成 10 款，劍（5）與槍（5）達成完全對稱的平衡格局！

### 1.2 重閥河馬武器選擇：【重閥活塞衝刺長槍（Steamvalve Piston Heavy Lance）】

重閥河馬原生專屬武器定名為：**【重閥活塞衝刺長槍（Steamvalve Piston Heavy Lance）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R04_BRASS_METROPOLIS.md` 黃銅都市·巨輪城之高壓蒸氣與重工鍛造工藝體系**！  
底層完全掛載於 `weapon_classes.json` 的 `spear`（騎士·長槍）類別，享有 `spear` 既有的「盾後無死角」標籤宣言（Tagline: `\"盾後無死角\"`）、中距控場、防禦迎擊、格擋反震與穿刺衝鋒之特性（`atk: 0, def: 2, hp: 4, crit: -1.0, speed: -1`），完美呼應 `R04_BRASS_METROPOLIS.md` 第 6 行「秒針每 1.5~2 秒急促跳動一格，伴隨蒸氣閥陣發性釋放鳴笛；動能狂暴充沛，齒輪咬合緊密，需掌握蒸氣洩壓拍點穿行於重型機具之間」之戰鬥節奏！

- **法源素材咬合**：  
  完全對應 `R04_BRASS_METROPOLIS.md` 第 4 行代表材質「沖壓厚鑄黃銅板、冷軋鎢鋼外齒輪、耐熱微型蒸氣管網」、第 21 行**「高壓蒸氣管道網（High-Pressure Steam Conduits）」**與第 107-109 行泰坦核心構件**「主活塞（Main Piston）」**與**「過熱洩壓排氣閥（Overheat Relief Valve）」**，將巨輪城地下管網的高壓動能轉化為勢不可擋的二次衝刺爆發力。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"spear\"` 的初階裝備 `knight_pike`（騎士長槍，tier 1）與高階相容裝備 `ash_spear`（灰燼長槍，tier 2/3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款長槍騎士（烈鬃獅、星軌犬、破浪旗魚、旋音天鵝）絕不撞型之論證

雖然重閥河馬與烈鬃獅、星軌犬、破浪旗魚、旋音天鵝同屬 `knight`（騎士）長槍（`spear`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               騎士職業長槍系五族差異化對照表（獅 vs 犬 vs 旗魚 vs 天鵝 vs 河馬）                                   │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 烈鬃獅 (Lion)        │ 星軌犬 (Hound)       │ 破浪旗魚 (Sailfish)  │ 旋音天鵝 (Swan)      │ 重閥河馬 (Hippo)    │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 皇家殿堂正義衝鋒     │ 星軌雷達信標穿刺     │ 深海洋流流體阻尼突刺 │ 晨曦芭蕾旋律滑步控場 │ 蒸氣超壓衝程防禦反震│
│ 2. 動能來源     │ 黃金發條主游絲       │ 磁軌重力失重滑行     │ 洋流渦輪水力彈射     │ 八音盒發條擒縱諧振   │ 高壓蒸氣活塞雙腔蓄能│
│ 3. 步法特徵     │ 威嚴正步、昂首闊步   │ 輕靈滑行、磁浮掠空   │ 擺尾衝浪、流體破浪   │ 芭蕾踮步、優雅迴旋   │ 沉穩低重心、活塞踏地│
│ 4. 武器構造     │ 皇家鍍金騎士長槍     │ 星軌天線雷達信標槍   │ 螺旋破浪合金長槍     │ 八音螺旋穿刺細長槍   │ 雙腔活塞洩壓重型鋼槍│
│ 5. 主題界域     │ R01 今日村莊·四大殿堂│ R07 星穹軌道·星墜防線│ R05 琉璃汪洋·發條海淵│ R02 晨曦小鎮·木偶集市│ R04 黃銅都市·巨輪城 │
│ 6. 材質質感     │ 拋光鍍金、黃銅皇家飾 │ 航空鋁合金、耐低溫塑 │ 鍍鈦防蝕合金、琉璃晶 │ 象牙白搪瓷、八音黃銅 │ 沖壓厚鑄黃銅、冷軋鎢│
│ 7. 角色剪影     │ 威武鬃毛圓形外擴     │ 立耳修長警惕獵犬     │ 巨大背鰭劍狀銳利突刺 │ 纖長優雅長頸羽翼     │ 敦實矮萌圓滾低重裝甲│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格恪守 `docs/world/CANON.md` 憲章世界觀「**100% 零真動物生物肉身、零毛皮、零羽毛、零真甲殼有機質、零血肉黏液**」之鐵律：

- **沖壓厚鑄耐壓黃銅底盤與冷軋鎢鋼骨架**：重閥河馬的身軀並非動物肉身，而是由巨輪城重型機械廠鍛造的**沖壓厚鑄耐壓黃銅板件（#FFA010 / #FFFDF8）**與內部冷軋鎢鋼承重框架鉚接而成。圓滾飽滿的腹部由厚達 5mm 的弧形鋼印馬口鐵護甲包覆，表面分佈著加固鉚釘與外露螺栓（#1F1A3A），絕無任何生物皮膚或軟組織。
- **可活動式沖壓雙層金屬大頜與排氣隔柵**：河馬標誌性的大嘴為上下雙層沖壓弧面金屬頜骨，由左右兩組重型齒輪鉸鏈（#FFD028）連動。張開嘴時，內部露出的是多層黃銅冷卻進氣散熱隔柵與微型防卡彈簧舌板，隨走時節律張合以排出內部聚積的微量冷凝水氣，完全杜絕任何牙齒、牙齦或唾液等生物器官。
- **雙聯旋轉式微型氣壓安全洩壓閥門耳**：頭頂兩側看似河馬小圓耳的結構，實質上為一對精密的「雙聯微型黃銅旋轉洩壓風門（Rotating Relief Valves）」。閥門外圈帶有刻度溝槽，伴隨體內蒸氣壓力的升降，風門會以微小頻率輕快自轉，並發出極細微的「嘶——」排氣聲，兼具散熱指示與超壓報警功能。
- **雙聯同軸高壓石英壓力表目鏡**：眼眶處安裝有一對圓形金屬外殼防爆壓力表（Manometer Optic Core）。表盤內部為薄荷冷翡翠發光刻度光柵（#4ED86A），黑色微型指針隨戰鬥怒氣與能量波動擺動，在鎖定敵方弱點時指針直指紅色超壓警戒線。
- **雙聯金屬蒸氣排氣壓載水箱短尾**：尾部並非肉尾，而是一組外掛於後臀部的微型高壓壓載平衡水箱（Ballast Tank），末端連接著一個短錐形的手動冷凝水排水閥栓，在衝鋒時提供穩固的下盤配重反扭矩。
- **背後發條鑰匙**：背部中央正上方垂直挺立著一把極具工業蒸汽美感的**雙聯閥門輪轂黃銅發條鑰匙（Valve Handwheel Brass Key）**。造型借鑒古典工廠管道閥門手輪，外緣為雙層防滑滾花黃銅圓輪，中心為粗壯的十字加固鋼軸，隨走時旋轉時沉穩剛勁，在 45 度視角下清晰打破角色剪影，極具工程視覺張力。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格依循 `USER PROFILE`、`docs/ART_DIRECTION.md` 與多巴胺鮮亮配色規範：

- **頭身比**：嚴格鎖定於 **2.0 ~ 2.2 頭身**。矮萌圓滾的敦厚身軀搭配粗短有力的四足活塞減震金屬短腿，徹底打破現實河馬粗笨兇殘的印象，呈現出宛如古典發條胡桃鉗重裝衛兵般的扎實安全感與極致反差萌。
- **色彩規劃（嚴守多巴胺鮮亮配色，絕無泥土髒黑）**：
  - **基底色（Base）**：`#FFFDF8`（象牙白陶瓷釉面／拋光馬口鐵，用於面部前頜高光板、腹部抗震襯板與關節活動墊圈）。
  - **主色（Primary）**：`#FFA010`（多巴胺巨輪暖橘，用於軀幹厚鑄金屬板、胸甲外緣塗裝與長槍配重段）。
  - **次色（Secondary）**：`#4ED86A`（薄荷冷翡翠，用於眼部壓力表盤背光、長槍活塞管導壓液發光線與瞄準刻度環）。
  - **點綴色（Accent）**：`#FF5E8A`（多巴胺珊瑚粉，用於耳部洩壓閥安全指示環、胸甲應急手動拉閥與散熱風門邊緣標籤）。
  - **金屬色（Metal）**：`#FFD028`（天元黃銅金，用於長槍主槍管、發條閥門手輪鑰匙、四足步進活塞管與面頰傳動齒輪）。
  - **描邊色（Outline）**：`#1F1A3A`（深藍紫手繪立體外輪廓描邊，確保在亮色與暗色背景下皆清晰銳利，徹底告別泥土髒黑）。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

恪守現代手遊看板角色活化標準：

- **待機呼吸律動（Idle Motion）**：
  - 2.2 頭身圓滾身軀沉穩屹立，四足活塞減震金屬蹄深紮地面；
  - 伴隨秒針每 1.5~2 秒急促跳動一格，胸部與腹部微幅膨脹起伏，背部雙聯排氣水箱輕微噴出一縷細小的白色微光蒸氣泡；
  - 頭頂雙聯洩壓閥門耳隨呼吸規律旋轉半圈，眼部壓力表指針在薄荷綠光柵間輕快微顫；
  - 背後雙聯閥門輪轂發條鑰匙以沉穩低速勻速自轉，手持長槍槍尖穩如磐石斜指前方。
- **點擊戳碰互動（Poke Interaction）**：
  - 玩家以手指點擊角色時，河馬受觸碰發出清脆有力的活塞洩壓鳴笛聲「噗哧——咻！」；
  - 金屬大頜瞬間張開 30 度露出黃銅冷卻進氣格柵，頭頂雙聯洩壓耳高速空轉 360 度；
  - 右手長槍向前有力突刺半步隨後收回胸前，左臂金屬護甲在胸前發出清脆的「鏘！」撞擊聲；
  - 頭頂彈出元氣滿滿的對話氣泡：`「管網壓力平穩，任何超壓震波都過不了這道閥門！」`，並向四周爆散出一圈多巴胺彩糖星芒粒子（金黃、薄荷綠、珊瑚粉）。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R04 黃銅都市·巨輪城（Brass Metropolis）零常駐專屬城防騎士歷史空白

在全專案九大界域中，黃銅都市·巨輪城作為全發條世界最高科技的重工業都城，雖然聚集了象、袋鼠、猩猩、渡鴉、守宮與啄木鳥等優秀工匠與遠近戰士，但在整座城市陷入「超壓危機（Overpressure Crisis）」、城防泰坦暴走封鎖全域的關鍵時刻，**整個界域長久以來完全缺乏一位具有超重裝低重心、能在過熱氣浪與重型自律裝甲前築起絕對防線、以長槍精準卡位迎擊的「重裝城防守護騎士」**。  
重閥河馬的進駐，填補了巨輪城最關鍵的一道安全閥門，成為整座工業浮空都市穿梭於天街與地下管網之間的最強城防鐵壁！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R04_BRASS_METROPOLIS.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R04_BRASS_METROPOLIS.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 日夜穿梭於縱橫交錯的**「高壓蒸氣管道網（High-Pressure Steam Conduits）」**（`R04_BRASS_METROPOLIS.md` 第 21 行），手動調節卡死的主管道洩壓手輪；
  - 巡邏於懸空數百米的**「摩天齒輪工坊群（Great Cog Skyspires）」**與**「自律工廠與天街吊橋（Automated Foundry & Sky Bridges）」**（第 20、22 行），護送受驚的鐵皮工匠；
  - 駐守於**「高架重軌引橋·巨輪城站（High Brass Viaduct: Metropolis Terminal）」**（第 30 行），引導自翡翠深林駛來的發條軌道列車安全減速進站；
  - 仰賴周邊設置的**「磁吸緩衝防墜鋼網（Magnetic Buffer Arresting Nets）」**（第 36 行），確保高空突進時無墜落深淵風險；
  - 定期前往城中央的**「中央蒸氣沐浴池（Central Degreasing Bath）」**（第 48 行），以高純度白礦物油蒸氣洗淨活塞縫隙中的碳化油泥與金屬碎屑。
- **工坊與居民互動**：
  - 接受**總工技師·銅齒（Chief Engineer Cogsmith）**（第 56 行）的委託，擔任應急搶險先鋒，以長槍頂住瀕臨破裂的高壓閥門；
  - 協助**管道巡檢員·小鎢（Tungsten the Valve Inspector）**（第 65 行）排查地下管網的水錘異音；
  - 配合**老鐘錶匠·星擺（Starpendulum the Ancient Horologist）**（第 73 行）調校背部發條手輪的走時擒縱機構，確保全城「鳴笛對時」毫秒不差；
  - 與同伴**鐵皮發條工程師（Tinplate Clockwork Engineers）**與**蒸氣鍋爐巡檢犬**（第 44、45 行）組成全天候管網巡防班組。
- **對抗首領情境**：
  - 在挑戰旗艦泰坦**「城防泰坦·巨輪霸主（Titan Fortress: Greatcog the Iron Juggernaut）」**（第 102 行）時，挺身迎向巨輪霸主的鋼鐵碾壓，以活塞長槍精準卡入泰坦過熱卡死的**「主活塞（Main Piston）」**與**「過熱洩壓排氣閥（Overheat Relief Valve）」**（第 107-109 行），阻斷過載動能回灌，為隊友小白創造拆卸部位破壞的黃金作戰窗口！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，重閥河馬的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 重閥河馬專屬造型規格與材質特徵（嚴守 100% 零真皮毛）                                            │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. body (素體)  │ 沖壓厚鑄黃銅與冷軋鎢鋼矮萌底盤（#FFA010 / #FFFDF8），多層加固鉚釘外板，四足活塞減震金屬蹄         │
│ 2. head (頭部)  │ 沖壓弧面金屬面甲配可活動式金屬大頜（#FFFDF8 / #FFD028），內置黃銅冷卻進氣格柵，無生物口腔組織    │
│ 3. ears (耳部)  │ 雙聯旋轉式微型氣壓安全洩壓閥門耳（#FFD028 / #FF5E8A），外圈帶刻度溝槽，隨走時排氣旋轉，無肉耳     │
│ 4. tail (尾部)  │ 雙聯蒸氣排氣壓載水箱與錐形排水閥短尾（#FFA010 / #FFD028），微型金屬水箱提供低重心配重平衡         │
│ 5. costume (服裝)│ 巨輪城重裝抗震高壓鉚釘胸甲（#FFA010 / #FFFDF8），多層重疊黃銅護甲，珊瑚粉色應急拉閥與管線滾邊   │
│ 6. optic_core(眼)│ 雙聯同軸高壓石英壓力表目鏡（#4ED86A），薄荷冷翡翠發光刻度光柵，內嵌微型同心圓刻度與黑色金屬指針 │
│ 7. winding_key  │ 雙聯閥門輪轂黃銅發條鑰匙（#FFD028），背部垂直挺立，工業蒸汽管道閥門手輪造型，自轉剛勁穩重      │
│ 8. weapon (武器)│ 重閥活塞衝刺長槍（#FFD028 / #4ED86A），槍身內置雙腔往復活塞，突刺時釋放高壓蒸氣二次爆發加速      │
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`body`（素體底盤）**：  
   2.2 頭身 Q 版矮萌身軀，由沖壓厚鑄耐壓黃銅板（#FFA010 / #FFFDF8）包覆冷軋鎢鋼框架製成。腹部圓滾飽滿，四肢為粗壯堅固的圓柱形液壓活塞避震腿，末端配備多層加厚黃銅蹄蓋與黑色防滑耐油橡膠墊。軀幹兩側鑲有多巴胺暖橘色塊與深藍紫立體鉚釘（#1F1A3A），徹底杜絕任何真實生物毛皮質感。
2. **`head`（頭部與頜骨）**：  
   圓潤厚實的象牙白金屬面甲，下方鉸接一組可張合 45 度的沖壓黃銅大頜。頜骨兩側外露精密傳動齒輪軸承，張合時露出內部的多層金屬進氣散熱片與發條防卡舌簧。眼眶處精準沖孔供 `optic_core` 壓力表透鏡穿透。
3. **`ears`（洩壓閥耳）**：  
   頭部頂端兩側對稱安裝的一對微型黃銅旋轉洩壓安全閥。頂端帶有多巴胺珊瑚粉（#FF5E8A）的超壓警示色環，內部裝配微型離心調速器，隨體內蒸氣壓陣發性高速自轉，無任何生物耳廓組織。
4. **`tail`（壓載水箱尾）**：  
   由圓柱形微型黃銅壓載水箱與末端小錐形排氣閥組成，長度約為身高的 1/5。緊湊外掛於臀部中軸線，在衝鋒時平衡上半身活塞長槍的重力矩。
5. **`costume`（高壓胸甲）**：  
   由巨輪城總工坊打造的耐高壓鉚釘重裝胸甲。主體施以明亮多巴胺暖橘彩漆（#FFA010），胸前以粗大的冷軋鎢鋼排扣固定，兩肩配備圓弧形高壓防浪護肩，胸口斜跨一組耐壓紫銅管線與珊瑚粉應急手動洩壓拉環。
6. **`optic_core`（壓力表目鏡）**：  
   雙聯平行安裝的高精度工業防爆石英壓力表。表盤散發薄荷冷翡翠螢光（#4ED86A），表面微雕三圈同心圓壓力標尺，內部黑色金屬指針隨戰鬥情緒動態擺動。
7. **`winding_key`（手輪發條鑰匙）**：  
   背部中央挺立的黃銅手輪發條鑰匙。造型採用古典重工業蒸氣閥門輪轂，雙圓環外緣帶有精密防滑滾花，中軸刻有調速棘齒。鑰匙隨秒針跳動勻速自轉，轉動時伴隨厚重金屬齒輪嚙合聲。
8. **`weapon`（重閥活塞長槍）**：  
   河馬專屬武器【重閥活塞衝刺長槍】。長達身高的 1.8 倍，槍身前半段為粗獷的錐形螺紋穿刺鋼錐，中段設有透明耐壓石英管包覆的高壓蒸氣活塞缸，後半段為黃銅配重握柄與防護護手盤。突刺瞬間活塞點火釋放超壓蒸氣，為穿甲突刺提供二次爆發推力。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 四足抓地沉穩屹立，長槍斜立於右側，背部排氣孔微幅噴出蒸氣微光，閥門手輪發條鑰匙勻速自轉         │
│ 2. attack (普攻)  │ 四足踏步發力向前突進，大嘴微微張開排氣，長槍平端直線突刺，活塞管噴出一道剛勁的白色錐形氣柱   │
│ 3. hit (受擊)     │ 身軀受衝擊向後頓挫半步，四足活塞減震腿劇烈下壓吸震，眼部壓力表指針劇烈抖動，耳部洩壓閥排氣   │
│ 4. recover (硬直) │ 雙足重重跺地穩住身形，大嘴猛然合攏發出清脆金屬閉合聲，長槍回防胸前架起鋼鐵壁壘，重新鎖定目標 │
│ 5. skill (技能)   │ 全身高壓管網超頻過載，大嘴仰天怒張發出長鳴汽笛，持長槍發起「超壓破陣全速衝鋒」，地面留下排氣焦痕│
│ 6. telegraph (蓄力│ 身軀下沉進入超低重心防禦姿態，長槍槍身活塞缸光芒高亮蓄能，地面投射出扇形重壓防禦指示光圈     │
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為騎士職業長槍系的核心擴充素體，直接提供差異化的中距迎擊、格擋反震與低重心衝刺體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過騎士長槍的防禦迎擊、格擋反震與部位破壞弱點突刺），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身沖壓厚鑄耐壓黃銅河馬自動機體現古典機械玩具的沉穩厚重魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏虛擬搖桿與技能點按佈局，長槍突刺動作帶有自適應吸附與防禦格擋判定，單拇指即可流暢完成普攻連突刺與看破迎擊。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實河馬龐大笨拙的寫實生物比例與泥濘水棲習性**：徹底放棄現實河馬粗大身軀與生物特徵，全面轉譯為 2.2 頭身矮萌防摔多層沖壓厚黃銅板件與高壓活塞機械結構，以換取手機螢幕上的高辨識度與耐摔玩具質感；  
2. **放棄獨立外掛重型防禦大盾牌**：為了避免在手機螢幕上長槍與大盾同時存在造成嚴重的紙娃娃圖層雜亂與穿模遮擋，放棄設計外掛在左手的實體重盾，將防禦格擋判定完全融入長槍槍身的「寬幅鎢鋼護手盤」與身軀內建的「重裝厚鑄胸甲」反震機制之中。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "hippo",
  "aliases": [
    "steamvalve_hippo",
    "ballast_hippo",
    "pressure_hippo",
    "greatcog_hippo",
    "clockwork_hippo"
  ],
  "name_zh": "重閥河馬",
  "name_en": "The Steamvalve Hippo",
  "class_archetype": "騎士 (Knight)",
  "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
  "lore_anchor": "穿行於黃銅都市·巨輪城「摩天齒輪工坊群」、「高壓蒸氣管道網」與「高架重軌引橋·巨輪城站」，巡檢「自律工廠與天街吊橋」與「中央蒸氣沐浴池」，駐守防護「磁吸緩衝防墜鋼網」，配合總工技師·銅齒、管道巡檢員·小鎢與老鐘錶匠·星擺；通體覆蓋沖壓厚鑄黃銅板件與冷軋鎢鋼骨架、雙聯旋轉式微型氣壓安全洩壓閥門耳、雙聯同軸高壓石英壓力表目鏡、巨輪城重裝抗震高壓鉚釘胸甲、雙聯蒸氣排氣壓載水箱、雙聯閥門輪轂黃銅發條鑰匙，雙手持握專屬重閥活塞衝刺長槍，以2.2頭身矮萌微胖體態、四足活塞減震金屬蹄、蒸氣超壓衝程、沉穩低重心防禦反震見長的巨輪城防衛者與鋼鐵壁壘騎士",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1930s-1950s 古典鐵皮發條河馬自動機與維多利亞蒸氣管道洩壓自動檢測偶)",
    "posture": "2.2 頭身矮萌身軀沉穩屹立，四足活塞蹄扎實抓地，右手單手持長槍斜指前方，雙耳微型洩壓閥門伴隨秒針每1.5秒跳動一格規律旋轉排氣，雙聯閥門手輪發條鑰匙隨走時均勻自轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "沖壓厚鑄黃銅面甲（#FFFDF8 / #FFA010）配可活動式金屬大頜，內置黃銅冷卻進氣散熱隔柵，眼窩處精準沖孔供 optic_core 穿透",
    "ears": "頭部頂端雙聯旋轉式微型黃銅安全洩壓閥（#FFD028），外圈帶有珊瑚粉超壓警示環，隨走時排氣自轉，無生物耳廓",
    "torso_and_limbs": "沖壓厚鑄耐壓黃銅板件（#FFA010）包覆冷軋鎢鋼框架，下身配置四足圓柱形活塞避震腿與加厚黃銅防滑蹄蓋",
    "tail": "圓柱形微型黃銅壓載水箱與錐形排水閥短尾（#FFA010 / #FFD028），以固定重量提供低重心衝鋒配重平衡",
    "weapon_system": "單手挽持專屬「重閥活塞衝刺長槍（Steamvalve Piston Heavy Lance）」，槍身內置雙腔往復活塞，突刺時釋放高壓蒸氣二次加速，底層掛載 equipment.json 既有 knight_pike (tier 1) 與 ash_spear (tier 2/3)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光馬口鐵，面部前頜高光、腹部抗震襯板與活動襯墊)",
    "primary": "#FFA010 (主色多巴胺巨輪暖橘，厚鑄黃銅外殼、胸甲塗裝與長槍配重段)",
    "secondary": "#4ED86A (次色薄荷冷翡翠，眼部壓力表盤背光、長槍導壓液發光線與瞄準刻度)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，洩壓閥安全指示環、胸甲應急拉閥與排風標籤)",
    "metal": "#FFD028 (金屬天元黃銅金，長槍主槍管、發條閥門手輪鑰匙、四足活塞管與面頰齒輪)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_hippo.png (品牌形象立牌)",
        "web/media/hero/char_hippo.png (官網英雄展示立繪)",
        "docs/art/steamvalve_hippo_concept.png (概念立繪)",
        "game/assets/sprites/player/hippo_idle.png (64x64 待機)",
        "game/assets/sprites/player/hippo_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/hippo_idle.png (隊伍待機)",
        "web/media/hero/hippo_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/hippo_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/hippo_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/hippo_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/hippo_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/hippo_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/hippo_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/hippo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/hippo.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/hippo_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/steamvalve_hippo.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/hippo/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_hippo.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/steamvalve_hippo_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_hippo.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/hippo_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/hippo_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/hippo_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/hippo_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/hippo_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/hippo_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/hippo_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/hippo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/hippo.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/steamvalve_hippo.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/hippo/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行紅線**：本卡片為純企劃設計提案，**嚴禁執行任何產圖產片指令**。以下 Prompts 與參數為未來美術總監（sideart）或執行工程師（sideworker）派工產圖時之必備標準規範。

### 8.1 重閥河馬角色單體立繪 Prompt（4:5 垂直角色畫）

```
chibi mechanical toy hippo knight, The Steamvalve Hippo, 2.2 head-body ratio, adorable chunky wind-up tinplate automaton. Stamped heavy-gauge brass body plates #FFA010 with ivory white enamel highlights #FFFDF8 and golden rivets #FFD028, visible mechanical seams, absolutely zero animal fur, zero organic flesh, zero biological texture. Sturdy rounded tinplate head with articulated metal jaw revealing brass radiator intake grilles inside. Crowned with dual rotating miniature brass pressure safety relief valves as ears tipped with coral-pink warning bands #FF5E8A. Glowing mint-green dial manometer pressure gauge optical lenses as eyes #4ED86A with delicate black indicator needle. Wearing a heavy-duty industrial brass cuirass with riveted overlapping plates and coral-pink emergency pull valve. On its back stands an imposing dual-ring industrial pipe handwheel brass wind-up key #FFD028. Four chunky steam-piston suspension legs with heavy brass hooves. Cylindrical brass ballast tank tail with miniature drain petcock. Holding a massive steampunk piston-driven heavy thrusting lance with glowing mint conduits. Pure clean ivory white studio background, vibrant dopamine color palette, bold dark blue-purple clean outline #1F1A3A, cel shaded, MapleStory and Tata Adventure toy aesthetic, cheerful fairy tale lighting, masterpiece, 8k resolution.
```

### 8.2 重閥河馬巨輪城高空管道場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
panoramic vibrant fairy tale scene in R04 Brass Metropolis The Great Cog City. In the center foreground, a 2.2 head-body ratio cute mechanical toy hippo knight with glowing mint pressure gauge eyes and dual rotating safety valve ears, leveling a massive brass steam-piston lance in a solid defensive stance. Standing heroically on a suspension bridge catwalk overlooking towering skyscraper gear workshops, intricate elevated high-pressure steam conduits, and high brass viaduct train rails bathed in golden morning light. Giant spinning cogs, rising steam plumes, distant sky train cars in the clear vibrant blue sky. Clean dark blue-purple outlines, vibrant dopamine colors (golden yellow #FFD028, warm orange #FFA010, mint green #4ED86A, celestial blue #38A0FF), zero dirt or muddy filters, warm whimsical toy world, official splash art style.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt 內容>" \
  --aspect 4:5 \
  --ref branding/key_visual_main.png \
  --out docs/art/steamvalve_hippo_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt 內容>" \
  --aspect 16:9 \
  --ref branding/key_visual_main.png \
  --out docs/art/steamvalve_hippo_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R04_BRASS_METROPOLIS.md` 既有地標（摩天齒輪工坊群、高壓蒸氣管道網、自律工廠與天街吊橋、鎢絲防爆街燈、高架重軌引橋·巨輪城站、磁吸緩衝防墜鋼網、中央蒸氣沐浴池、中央動力廣場）與居民 NPC（總工技師·銅齒、管道巡檢員·小鎢、老鐘錶匠·星擺），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`騎士 (Knight)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  騎士長槍遵循單手持槍迎擊衝刺規格，左右肢體姿態描述清晰。
- [x] **CANON 世界憲章零毛皮鐵律**：  
  100% 零真動物肉身、零生物毛皮、零羽毛、零黏液；通體轉譯為沖壓厚鑄黃銅、冷軋鎢鋼骨架、外露球窩活塞腿、雙聯洩壓閥門耳、石英壓力表目鏡與閥門手輪發條鑰匙。
- [x] **騎士長槍與長劍對稱平衡**：  
  作為第十巡首位擴充，補齊騎士長槍第 5 款，與騎士長劍（5 款）達成完全 5:5 對稱平衡！
