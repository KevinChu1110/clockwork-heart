# 第五十九種動物「提線猞猁（The Marionette Lynx）」世界觀與角色設計提案

> **標題**：第五十九種動物「提線猞猁（The Marionette Lynx）」角色與世界觀設計提案  
> **提案代號**：`MARIONETTE_LYNX_DESIGN_PROPOSAL`（代號：`lynx` / 識別名：`race_lynx`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_7d85470c`（📖 世界觀｜第五十九種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零皮革、零動物肉身、零生物黏液；精雕拋光胡桃木底盤、打磨楓木骨架、象牙白溫潤白瓷面甲、雙聯垂直黃銅金屬絲天線天籟耳簇、雙節同軸鐘擺平衡配重短尾、外露精工黃銅鉚釘與球形鉸鏈、背後雙環八音風鈴黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調；多巴胺高飽和鮮亮色彩）  
> - `docs/world/regions/R02_DAWN_TOWN.md`（第 1 行區域代號與名稱「R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar」、第 4 行「歐風木造街屋、石板路與精緻提線木偶套件」、第 6 行「局域走時狀態：慢速延遲偏快（秒針每隔 2~3 秒跳動一格，齒輪持續運轉，集市維持熱絡但部分商用機械因動力波動開始過熱）」、第 15 行「多邊形胡桃木拼花浮空展台底座、金色黃銅護欄與外露齒輪嚙合環軌」、第 19 行「淺灰硬質磨石灰岩積木拼合街道，鑲嵌金黃銅質防滑飾條」、第 20 行「歐風木造街屋、多層山形牆商鋪、迷你黃銅發條煙囪」、第 21 行「懸吊齒輪鐘樓（Suspended Gear Belltower）」、第 28 行「齒輪吊索大橋·小鎮站（Cogwheel Cableway Terminal）」、第 29 行「晨曦天軌 2 號月台（Dawn Rail Platform 2）」、第 31 行「蔓谷天梯引道（Vine Valley Stairway Gate）」、第 32 行「巨輪城重型空軌貨運棧橋（Great Cog Rail Freight Way）」、第 34 行「邊界安全防護彈簧網（Perimeter Safety Spring-Net）」、第 46 行「精紡線莊」與「中央油坊」、第 54 行提線商會會長「巴納姆（Barnum the Threadmaster）」、第 63 行彩釉玩偶夫人「瑪德琳（Lady Madeline the Glazed Belle）」、第 71 行摺紙工匠「小鶴（Tsuru the Origami Crafter）」、第 85 行「失控自動販賣傀儡」、第 89 行「脫線提線小丑」、第 93 行「巡市木偶捕犬」、第 99 行旗艦泰坦 BOSS「集市守護機關·提線巨偶（Bazaar Overseer: Grand Marionette Titan）」、第 118 行特產掉落「精梳蜂蠟線、高剛性鐵杉木樞紐、拋光胡桃木塊、精密聚光水晶目鏡、微型精工黃銅軸承」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（武術家正式名稱 `monk`，標籤宣言 `"撕裂防線"`，武器 `claw`，數值 `atk: 2, def: 0, hp: 2, crit: 2.5, speed: 2`，玩法 `"爪痕連切。同職也可玩拳。"`，初始相容武器 `hunt_claw`）  
> - `game/data/tables/equipment.json`（爪類正式 line: `"claw"`，相容高階武器：`hunt_claw` 溢地獵爪，tier 3）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡（第 55~60 族）第四順位核心擴充，補齊武術家 5:5 拳爪超對稱平衡**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十九種動物擴充素體規格**。  
   在全專案相繼於第十巡首位成員第五十六種動物重閥河馬（騎士·長槍，達成 5 劍 5 槍）、第二順位第五十七種動物星岩鼴鼠（戰士·戰鎚，達成 5 斧 5 鎚）與第三順位第五十八種動物嵐翼鼯鼠（忍者·機關鏢，達成 5 匕 5 鏢）順利完成前三大職業對稱平衡後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第四順位**，接棒輪轉進入全遊戲最具打擊感、寸勁破勢、爪痕連切與正面攻堅的核心職業——**武術家 (Monk)** 體系，原生武器掛載於**晨曦提線裂空機關爪（`claw` / 武術家·爪）**。  
   提線猞猁的加入，使全遊戲武術家機關爪素體擴充至第 5 款（靈爪猴、沙鱗穿山甲、疾影神隼、破星蜜獾、提線猞猁），與武術家拳套素體（瓷韻熊貓、鐵拳袋鼠、鋼臂巨猩、拍浪海豹、熔砧石蟹 5 款）達成**完全對稱的 5:5 完美平衡格局**！
2. **經典玩具起源與古典歐風提線木偶猞猁雜技工藝**：  
   - 本提案選定全球古典機械玩具、提線木偶與巴洛克鐘錶工藝史上的經典工藝原型：  
     ① **1880s-1920s 歐洲古典提線木偶雜技機關偶（Vintage European Marionette Acrobatic Automaton / 捷克布拉格木偶工藝與法國 Vichy 自動機關偶名作）**，通體由細膩雕琢的拋光胡桃木、楓木榫卯關節與高張力精梳蜂蠟提線連接而成，背後配備微型平衡十字架與發條伺服盒，跳躍與撲擊時提線滑輪伴隨清脆金屬聲「喀嗒、喀嗒」自律協同收放，是古典木偶史上最具人體工學動態與機關巧思的藝術品；  
     ② **瑞士巴洛克鐘錶集市的「懸吊鐘樓巡邏機關猞猁（Clockwork Belltower Lynx Guardian）」**，小巧圓潤的 2.2 頭身身軀覆蓋象牙白溫潤瓷面甲與楓木板件，頭頂配備雙聯垂直黃銅金屬絲天線天籟耳簇，能敏銳捕捉鐘樓擒縱滴答拍點；厚實的機械爪掌內藏沖壓高硬度鎢鋼伸縮五聯爪刃，賦予角色在山形牆與石板屋簷間無聲攀躍、猛虎撲擊撕裂敵方防線的凌厲身手；  
     ③ **晨曦市集雜技演出自動偶（Dawn Bazaar Juggler Automaton）**，將經典八音風鈴音叉擒縱齒輪與氣壓提線連動鋼爪結合，完美詮釋武術家職業「撕裂防線、爪痕連切、破勢在勤」之武道之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「精雕拋光胡桃木底盤、象牙白瓷圓面甲配雙色翡翠寶石目鏡、雙聯垂直黃銅金屬絲天線天籟耳簇、雙節同軸鐘擺平衡配重短尾、晨曦小鎮提線雜技工裝背心、晨曦提線裂空機關爪與雙環八音風鈴黃銅發條鑰匙」之晨曦小鎮提線武道家素體（Polished Walnut Marionette Chassis, Ivory Porcelain Visor with Emerald Quartz Eyes, Twin Brass Wire Resonance Ear Tufts, Twin-Segment Pendulum Bobtail, Dawn Acrobat Workwear Vest, Dawn Marionette Steel Claws & Twin-Ring Chime Brass Key）**。
3. **生態補足：終結晨曦小鎮（R02）長久無武術家之歷史空白，打造高空山形牆立體巡守防線**：  
   在全遊戲 9 大界域中，中層歐風木雕市集界域 `R02 晨曦小鎮·木偶集市` 先前擁有靈鐘鴞（法師·杖）、棘輪刺蝟（忍者·鏢）、稜鏡孔雀（法師·晶）、鐵蹄駿駒（騎士·劍）、旋音天鵝（騎士·槍）與鐘塔長頸鹿（遊俠·弓）共 6 族。  
   長久以來，晨曦小鎮匯聚了優雅的法師、騎士與射手，**面對集市中央大劇院頂端失控的旗艦泰坦巨偶、在街角橫衝直撞的失控自動販賣傀儡、以及絲線死結狂暴揮擊的脫線提線小丑，整個小鎮完全缺乏一位能夠在多層山形牆商鋪屋頂與懸吊齒輪鐘樓高空懸索間無聲攀躍、以凌厲爪痕正面撕裂敵方厚重護甲、打碎失控零件架勢的「近身貼身寸勁武道家（Monk）」**！提線猞猁的降臨，徹底填補了 R02 晨曦小鎮長期以來零武術家的生態空白，為溫馨歐風集市注入了靈動剛猛的近戰破勢之魂！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 運作邏輯（僅登錄 races_specification 正表提案項目，更新 total_races 為 58）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：提線猞猁素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十八族武器與職業光譜全盤點

盤點現有首發五族與前五十三款擴充族（總計 58 族，含第 58 族嵐翼鼯鼠）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **嵐翼鼯鼠（The Stormwing Petaurista）**：忍者 (Ninja) —— 竹影八卦旋刃機關鏢（`dart`），高空滑翔翼展身法，竹梢微彈看破，破空音叉多段旋鏢牽制。
- **提線猞猁（The Marionette Lynx）**：**武術家 (Monk) —— 晨曦提線裂空機關爪（`claw`），提線滑輪連動身法，屋脊輕盈撲躍，五聯鎢鋼連切撕裂防線。**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）10 族（劍 5、槍 5，已達完全平衡）；
- 戰士（Viking）10 族（斧 5、鎚 5，已達完全平衡）；
- 忍者（Ninja）10 族（匕 5、鏢 5，由嵐翼鼯鼠補齊至完全平衡）；
- 武術家（Monk）此前在 58 族中擁有 9 款動物素體（拳套 5 款、機關爪 4 款）；
- 法師（Mage）9 族（杖 5、晶 4）；
- 遊俠（Ranger）9 族（弓 5、銃 4）；
- **本提案第五十九種動物正式作為「第十巡第四順位」核心擴充，歸屬於武術家 (Monk) 體系，原生武器掛載於 `claw`（機關爪 / 武術家·爪）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`武術家 (Monk)`**；
- 提線猞猁的加入，使全遊戲武術家機關爪素體擴充至第 5 款，武術家總數達成 10 款，拳套（5 款）與機關爪（5 款）達成完全對稱的平衡格局！

### 1.2 提線猞猁武器選擇：【晨曦提線裂空機關爪（Dawn Marionette Steel Claws）】

提線猞猁原生專屬武器定名為：**【晨曦提線裂空機關爪（Dawn Marionette Steel Claws）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R02_DAWN_TOWN.md` 晨曦小鎮·木偶集市之精緻提線木偶與胡桃木機械工藝體系**！  
底層完全掛載於 `weapon_classes.json` 的 `claw`（武術家·爪）類別，享有 `claw` 既有的「撕裂防線」標籤宣言（Tagline: `"撕裂防線"`）、破勢快、暴擊與連段兼顧、虎撲撲擊節奏兇之特性（`atk: 2, def: 0, hp: 2, crit: 2.5, speed: 2`），完美呼應 `R02_DAWN_TOWN.md` 第 6 行「局域走時狀態：慢速延遲偏快，秒針每隔 2~3 秒跳動一格，齒輪持續運轉，集市維持熱絡」之精準節奏與提線機械連動撕裂手感！

- **法源素材咬合**：  
  完全對應 `R02_DAWN_TOWN.md` 第 4 行代表材質「歐風木造街屋、石板路與精緻提線木偶套件」、第 15 行「多邊形胡桃木拼花浮空展台底座、金色黃銅護欄與外露齒輪嚙合環軌」、第 46 行「精紡線莊」與第 118 行特產掉落「精梳蜂蠟線、高剛性鐵杉木樞紐、微型精工黃銅軸承」，將晨曦集市的提線滑輪與鎢鋼爪刃結合為破開機關防線的近戰利刃。
- **單持規範遵守（0-MKT7）**：  
  遵循 `review.md 0-MKT7` 單持規範，右手單持主機關爪套（手掌與腕部覆蓋精雕拋光胡桃木護腕與黃銅鉸鏈，前伸五聯沖壓冷軋鎢鋼弧刃，長度約 24px，內置微型發條回縮棘爪與提線滑輪）；左手五指自然微曲收攏於胸前，掌心朝內作靈貓防守架勢與提線平衡引手，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: "weapon"`、`line: "claw"` 的相容裝備 `hunt_claw`（溢地獵爪，tier 3，`atk: 13, def: 0, hp: 0, crit: 12, crit_dmg: 24`），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款機關爪武術家（靈爪猴、沙鱗穿山甲、疾影神隼、破星蜜獾）絕不撞型之論證

雖然提線猞猁與靈爪猴、沙鱗穿山甲、疾影神隼、破星蜜獾同屬 `monk`（武術家）機關爪（`claw`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               武術家職業爪系武器五族差異化對照表（猴 vs 穿山甲 vs 神隼 vs 蜜獾 vs 猞猁）                          │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 靈爪猴 (Macaque)     │ 沙鱗穿山甲(Pangolin) │ 疾影神隼 (Falcon)    │ 破星蜜獾 (Badger)    │ 提線猞猁 (Lynx)     │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 彈簧伸縮臂遠距撕裂   │ 重裝下潛破勢鑽地突擊 │ 高空俯衝撕裂風影殘痕 │ 冷氣反推衝鋒正面硬撼 │ 提線滑輪連動屋脊撲擊│
│ 2. 動能來源     │ 雙向高壓螺旋彈簧拉伸 │ 渦輪掘進發條重力離心 │ 氣動羽翼高空氣壓俯衝 │ 微型冷氣高壓反推噴嘴 │ 提線張力滑輪與鐘擺簧│
│ 3. 步法特徵     │ 靈活後空翻、騰空抓握 │ 蜷曲滾動、重甲鑽地遁地│ 盤旋折返、高空俯衝掠地│ 向量噴射直線霸體衝刺 │ 輕盈跳躍、屋頂無聲肉墊│
│ 4. 武器構造     │ 剪式伸縮黃銅三聯爪   │ 弧面螺旋鑽孔重鋼開山爪│ 流線型猛禽雙聯破空鋼爪│ 寬幅加厚四聯合金撕裂爪│ 五聯氣動回縮精工鎢鋼爪│
│ 5. 主題界域     │ R09 竹影道場·天元竹林│ R08 荒原齒輪塚·廢土堆 │ R03 翡翠深林·發條蔓谷│ R07 星穹軌道·外星基地│ R02 晨曦小鎮·木偶集市│
│ 6. 材質質感     │ 生漆木雕、黃銅彈簧   │ 沖壓厚重生鏽合金鋼鱗 │ 輕量化拋光鋁合金骨架 │ 高密度抗衝擊工程塑料 │ 拋光胡桃木、象牙白瓷│
│ 7. 角色剪影     │ 修長雙臂靈動身段長尾 │ 圓盤球狀低矮重裝甲身 │ 雙翼後掠高挑流線鳥偶 │ 平頂平頭厚裝短肢方鈍 │ 2.2頭身雙金天線耳短尾│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴守 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md`，100% 徹底清除所有真皮毛、皮革、羽毛、生物肉身與泥土髒污，全面轉譯為精緻古典歐風木雕與提線木偶自動偶質感：

- **精雕拋光胡桃木底盤與象牙白瓷面甲**：提線猞猁的身軀絕非生物皮毛肉身，而是由晨曦小鎮巴納姆商會工坊以**百年陳化拋光胡桃木（Polished Walnut #8B5A2B）**精心車削榫接而成，胸腹部覆蓋溫潤細緻的**象牙白打磨楓木與白瓷板件（#FFFDF8）**。體態呈現 2.2 頭身矮萌微胖 Q 版造型，四肢關節為光滑靈巧的精工黃銅球窩鉸鏈（#FFD028），表面分佈著微型鉚釘與防震縫線，絕無任何生物毛皮、皮屑或血肉。
- **雙聯垂直黃銅金屬絲天線天籟耳簇**：猞猁標誌性的耳尖簇毛被徹底轉譯為一對**雙聯垂直黃銅金屬絲天線天籟耳簇（Twin Brass Wire Resonance Ear Tufts）**。耳廓為精雕胡桃木立耳（外塗薄荷淺綠 #4ED86A 彩釉飾邊），耳尖各矗立著三根微型精工黃銅金屬絲天線（#FFD028），內部纏繞著細微的共鳴音叉線圈，能精準接收鐘樓大鐘每 2 秒一次的走時震顫與提線絲線的微振諧波，完全杜絕任何動物毛簇。
- **雙色翡翠寶石玻璃目鏡**：面部中央嵌有一對清澈透亮的雙色翡翠寶石玻璃目鏡（Emerald Quartz Goggles #4ED86A / #38A0FF）。眼眶周圍施以陽光童話風格的暖橘水性彩漆飾邊（#FFA010），鏡片內部雕刻有細微的同軸刻度圈，鎖定破勢時瞳孔中心泛起金色十字準星，透光溫暖柔和，絕無恐怖陶瓷裂紋。
- **五聯氣動回縮精工鎢鋼機關爪**：前臂護腕以胡桃木外包黃銅護圈固定，爪掌內建精密微型提線滑輪組。五根爪刃為沖壓冷軋高硬度鎢鋼弧刃（#FFD028 / #1F1A3A），待機時順滑回縮於木質指節內，撲擊破勢時伴隨清脆金屬聲「喀——嚓！」順暢彈射伸出，安全、乾淨且充滿機械咬合的美感。
- **雙節同軸鐘擺平衡配重短尾**：尾部並非毛茸茸的小短尾，而是一枚精緻小巧的**雙節同軸鐘擺平衡配重短尾（Twin-Segment Pendulum Bobtail）**。由兩節車削胡桃木圓柱與黃銅萬向擺動鉸鏈連接，末端嵌有一枚圓球形黃銅配重鉛錘（#FFD028），在跳躍與撲擊時如節拍器般擺動提供重心回饋，完全杜絕生物短尾毛皮。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格遵循 Kevin 與使用者畫像核心審美原則：
- **比例**：矮萌可愛的 2.0 ~ 2.2 頭身比，頭大身小，四肢圓潤厚實，站立時微屈膝下沉重心，右手前探亮爪，左手收胸護架，神態自信專注。
- **多巴胺鮮亮高飽和色盤（拒絕暗黑泥土灰黑）**：
  - **奶油米白底色（#FFFDF8）**：白瓷面頰、胸腹襯板高光，溫潤乾淨，杜絕髒濁。
  - **多巴胺暖橘主色（#FFA010）**：胡桃木外裝彩漆、耳廓正面塗裝、背心領口飾邊。
  - **多巴胺薄荷淺綠（#4ED86A）**：翡翠寶石目鏡、背心扣帶、手腕提線滑輪護套飾條。
  - **多巴胺天藍（#38A0FF）**：目鏡外圈透鏡光暈、提線導引絲線流蘇。
  - **多巴胺金黃（#FFD028）**：雙環發條鑰匙、黃銅鉸鏈、爪刃基座、鐘擺配重球與天線耳簇。
  - **多巴胺珊瑚粉（#FF5E8A）**：發條鑰匙中心按鈕、鼻頭防塵護墊印記。
  - **深藍紫立體手繪描邊（#1F1A3A）**：高反差立體外輪廓線，取代傳統髒黑泥土色。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

拒絕靜止死板木樁，為提線猞猁設計活靈活現的 Q 版發條動態：
- **待機呼吸感（Idle Breathing）**：
  - 2.2 頭身身軀每 2.0 秒進行一次微幅上下起伏，胸前胡桃木關節伴隨呼吸發出極細微的發條游絲律動；
  - 背部雙環八音風鈴黃銅發條鑰匙隨秒針每 2.5 秒跳動一格勻速自轉，發出微弱清脆的八音盒齒音；
  - 雙聯黃銅金屬絲天線耳簇每隔 4 秒隨環境微風輕微顫動調焦，雙節鐘擺短尾左右擺動兩下。
- **待機專屬小動作（Special Idle Animations）**：
  - **「彈爪校準」**：每隔 8 秒，猞猁右手輕輕向前虛抓，五聯鎢鋼爪刃瞬間齊刷刷彈出「喀嗒！」，爪尖在空中劃出三道微小金色光弧，隨後流暢收回掌中，神情機警帥氣；
  - **「提線理耳」**：左爪輕輕抬起拂過頭頂的黃銅天線耳簇，牽動背後微型提線發出一聲空靈風鈴鳴響「叮——！」。
- **Poke 點擊互動（點擊反應反饋）**：
  - 玩家以手指點擊角色時，提線猞猁如受驚小貓般原地彈起懸空半公尺，四肢張開露出金屬肉墊，背後提線十字架光影一閃，隨後輕盈如落葉般四足落地，尾巴鐘擺急促擺動平衡；
  - 頭頂彈出俏皮對話氣泡：「**鐘樓的發條可沒停，別小看提線的力量！**」或「**我的爪刃比鐘錶秒針還要精準喔！**」，周身爆散出 4~6 枚半透明暖橘齒輪與薄荷綠星芒粒子。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R02 晨曦小鎮·木偶集市無武術家之歷史空白

在全專案九大界域中，中層歐風市集界域 `R02 晨曦小鎮·木偶集市` 先前擁有 6 族，涵蓋遠程法師、狙擊遊俠與陣列騎士，但面對集市中央大劇院失控巨像揮舞巨劍、脫線小丑在街角狂舞、以及狂暴捕犬低伏撲咬時，**長久以來完全缺乏一位能夠在山形牆與懸吊鐘樓高空懸索間無聲攀躍、以凌厲爪痕正面撕裂敵方厚重護甲、打碎失控零件架勢的「近身貼身寸勁武道家（Monk）」**。提線猞猁的入駐，補齊了 R02 最具威懾力的立體防衛線。

### 3.2 100% 逐字對齊引用 `docs/world/regions/R02_DAWN_TOWN.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R02_DAWN_TOWN.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 於小鎮中央廣場矗立的**「懸吊齒輪鐘樓（Suspended Gear Belltower）」**（`R02_DAWN_TOWN.md` 第 21 行）高空懸索間無聲跳躍，傾聽巨大青銅擒縱輪與金色鐘擺的擺動韻律；
  - 駐守沙盤西南端的發條纜車裝卸站**「齒輪吊索大橋·小鎮站（Cogwheel Cableway Terminal）」**（`R02_DAWN_TOWN.md` 第 28 行），守護來自今日村莊（R01）的懸空纜車安全靠泊；
  - 巡防北側高台**「晨曦天軌 2 號月台（Dawn Rail Platform 2）」**（`R02_DAWN_TOWN.md` 第 29 行），接駁來自中央浮空島天宮大廳的高速發條吊艙；
  - 穿梭於東北角懸崖邊由大型齒輪鏈條牽引的**「蔓谷天梯引道（Vine Valley Stairway Gate）」**（`R02_DAWN_TOWN.md` 第 31 行），清除卡在引道齒輪中的廢舊線繩；
  - 巡視通往黃銅都市（R04）高架重軌的**「巨輪城重型空軌貨運棧橋（Great Cog Rail Freight Way）」**（`R02_DAWN_TOWN.md` 第 32 行），檢視軌道支撐懸臂的水平咬合；
  - 依託展台底座外緣延伸佈設的**「邊界安全防護彈簧網（Perimeter Safety Spring-Net）」**（`R02_DAWN_TOWN.md` 第 34 行），演練失足彈回的極限受身步法；
  - 巡守於小鎮中心的**「精紡線莊」**與**「中央油坊」**（`R02_DAWN_TOWN.md` 第 46 行），引導居民安全領取香氛散熱發條潤滑油；
  - 縱躍於歐風木造街屋的**「多層山形牆商鋪」**（`R02_DAWN_TOWN.md` 第 20 行）屋頂，在迷你黃銅發條煙囪噴出的微溫蒸氣中穿梭巡哨；
  - 踏行於細緻打磨的淺灰硬質磨石灰岩街道，踏足於**「多邊形胡桃木拼花浮空展台底座」**（`R02_DAWN_TOWN.md` 第 15 行）與金黃銅質防滑飾條之上。
- **核心 NPC 互動情境**：
  - 與拋光胡桃木紳士**提線商會會長·巴納姆（Barnum the Threadmaster）**（`R02_DAWN_TOWN.md` 第 54 行）緊密合作，擔任商會首席巡市警衛，以提線機關爪保護商會稀有物資；
  - 探望露天茶座邊慈愛的彩釉小熊淑女**彩釉玩偶夫人·瑪德琳（Lady Madeline the Glazed Belle）**（`R02_DAWN_TOWN.md` 第 63 行），代為巡回散落在街角商鋪的精梳棉線與彩繪釉料；
  - 與七彩靈巧的**摺紙工匠·小鶴（Tsuru the Origami Crafter）**（`R02_DAWN_TOWN.md` 第 71 行）研討輕量化爪套卡扣結構，借摺紙抗拉韌性強化提線滑輪的耐久度。
- **守護泰坦作戰支援**：
  - 面對中央大劇院失控的古代傳奇守衛**「集市守護機關·提線巨偶（Bazaar Overseer: Grand Marionette Titan）」**（`R02_DAWN_TOWN.md` 第 99 行），提線猞猁利用靈巧的屋頂跳躍身法避開舞台巨劍的大範圍橫掃，躍上巨偶天車懸索，以五聯鎢鋼機關爪精準切斷卡死天車傳動齒箱的亂線，合力解除防衛協議溢出危機！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，提線猞猁的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 提線猞猁專屬造型規格與材質特徵（嚴守 100% 零真皮毛、零皮革）                                    │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. body (素體)  │ 提線木偶精雕胡桃木矮萌底盤（#8B5A2B / #FFFDF8），打磨楓木骨架與白瓷胸腹襯板，黃銅球窩關節       │
│ 2. head (頭部)  │ 歐風提線雙天線金耳兜帽（#8B5A2B / #FFA010），胡桃木雕刻立耳配黃銅天線耳簇，無生物肉質口鼻     │
│ 3. ears (耳部)  │ 雙聯垂直黃銅金屬絲天線天籟耳簇（#FFD028 / #4ED86A），三聯黃銅天線絲內嵌音叉共鳴線圈，隨秒針顫動│
│ 4. tail (尾部)  │ 雙節同軸鐘擺平衡配重短尾（#8B5A2B / #FFD028），兩節車削胡桃木圓柱外接黃銅萬向鉸鏈與配重鉛錘    │
│ 5. costume (服裝)│ 晨曦小鎮提線雜技工裝背心（#FFA010 / #4ED86A），暖橘色彩釉帆布配薄荷綠提線滑輪扣帶與黃銅排扣   │
│ 6. optic_core(眼)│ 雙色翡翠寶石目鏡彩釉面甲（#4ED86A / #FFA010），雙色翡翠石英透鏡嵌象牙白瓷，手繪多巴胺暖橘眼紋 │
│ 7. winding_key  │ 雙環八音風鈴黃銅發條鑰匙（#FFD028 / #FF5E8A），背部雙環對稱音叉風鈴造型，中心嵌珊瑚粉防塵鉚釘 │
│ 8. weapon (武器)│ 晨曦提線裂空機關爪（#FFD028 / #8B5A2B / #1F1A3A），沖壓鎢鋼五聯弧刃嵌胡桃木腕套，內建提線滑輪 │
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`body`（素體底盤）**：  
   2.2 頭身 Q 版矮萌身軀，由高密度拋光胡桃木（#8B5A2B）精雕榫接而成。胸前與小腹鑲嵌光潔溫潤的象牙白瓷襯板（#FFFDF8），四肢為圓潤小巧的精工黃銅球窩鉸鏈（#FFD028）。足底裝配防滑橡膠軟墊，行走時在集市磨石板路上發出輕快踏音，徹底杜絕任何真實生物毛皮質感。
2. **`head`（頭部與兜帽）**：  
   圓滾光潤的白瓷半球形頭部面甲，頭頂覆蓋胡桃木雕刻的雜技小圓帽與護額飾邊。面部中央眼眶處精準沖孔供 `optic_core` 透光，鼻部轉譯為一枚珊瑚粉銅質防塵圓鈕，整體呈現古典木偶與發條玩具融合的俏皮萌感。
3. **`ears`（黃銅天線耳）**：  
   頭部兩側對稱安裝的一對微型提線猞猁立耳。耳殼為雕花胡桃木（外緣塗薄荷淺綠彩漆），耳尖各延伸出三根細密挺拔的黃銅金屬絲天線（#FFD028），能隨鐘樓大鐘每 2 秒一次的走時脈衝微幅顫動調焦，無任何生物耳廓肉質。
4. **`tail`（鐘擺平衡短尾）**：  
   長度約為身高的 1/5，由兩節車削胡桃木圓柱以黃銅萬向鉸鏈相連。末端鑲有一枚沉甸甸的拋光黃銅圓球配重鉛錘（#FFD028），奔跑與跳躍時左右勻速擺動提供物理平衡，落地時自然下垂。
5. **`costume`（雜技工裝背心）**：  
   由高飽和暖橘色（#FFA010）耐磨彩釉帆布製成的古典集市雜技背心。前襟配備四枚精緻的黃銅小圓扣，雙肩附帶薄荷綠（#4ED86A）皮革質感金屬提線滑輪扣帶，背後預留發條插孔，兼具童話慶典氛圍與武道活動人體工學。
6. **`optic_core`（翡翠寶石目鏡）**：  
   一對深邃晶瑩的雙色翡翠寶石玻璃透鏡（#4ED86A / #38A0FF）。眼周手工繪製暖橘色彩釉猞猁眼紋（#FFA010），目光專注清澈，在進入連擊破勢蓄力狀態時，鏡片中心浮現出微縮金色齒輪刻度標尺。
7. **`winding_key`（八音風鈴發條鑰匙）**：  
   背部中央挺立的雙環八音風鈴黃銅發條鑰匙。採用晨曦黃銅金（#FFD028）精密鑄造，造型宛如一對相互交疊的八音盒風鈴金環，中心固定一枚珊瑚粉防塵鉚釘（#FF5E8A）。隨秒針每 2.5 秒跳動一格自轉，發出微弱空靈的鐘鳴鈴響。
8. **`weapon`（提線裂空機關爪）**：  
   提線猞猁專屬武器【晨曦提線裂空機關爪】。手腕由胡桃木護腕與微型棘輪滑輪緊密包覆，前伸五聯沖壓冷軋鎢鋼爪刃（#FFD028 / #1F1A3A）。出爪揮擊時，提線牽引內部簧片發出清脆的「喀嚓！」破風聲，爪痕在空氣中留下優雅的暖橘與金色多巴胺流光。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 側身45度矮萌站姿，右手前屈亮爪，左手收胸護架，天線耳簇微顫，背後雙環發條鑰匙勻速自轉，短尾微擺│
│ 2. attack (普攻)  │ 踏步前衝半步，右手腕部提線滑輪驟響，五聯鎢鋼爪刃呼嘯彈出向前斜劈，空氣中撕裂出兩道金黃弧光   │
│ 3. hit (受擊)     │ 身軀受震向後微仰，雙爪交叉護胸抵消衝擊，雙足在石板地面滑退兩步，面甲翡翠目鏡光芒急促閃爍     │
│ 4. recover (硬直) │ 四足輕巧觸地卸力，迅速後躍半步穩住重心，右手橫爪護於身前，天線耳微擺重置鐘擺頻率，調勻機芯律動│
│ 5. skill (技能)   │ 借提線拉力騰空躍起，半空中翻滾一週施展「提線旋身連切」，連續抓出4道交錯爪痕，引爆大範圍破勢光芒│
│ 6. telegraph (蓄力│ 身軀完全伏低呈貓科捕食蓄勢姿態，雙爪按地抓緊石板，背後發條鑰匙超頻急轉，五聯鋼爪發出金屬嗡鳴│
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為武術家職業機關爪系的核心擴充素體，直接提供貼身寸勁連打破勢、爪痕連切撕裂防線與高速立體突進的高手感戰鬥體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過武術家機關爪的快節奏爪痕連擊、破勢削韌與近身防守反擊打法），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身拋光胡桃木雕刻與提線木偶猞猁自動偶體現歐風古典集市的機關童話魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏雙拇指操作配置，機關爪近戰撲擊動作自帶前方扇形自動吸附判定，單拇指即可輕鬆完成連續點擊普攻連段、閃避位移與絕招爆發。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實猞猁濃密雪地毛皮、肉球腳掌與長毛頰鬚**：徹底放棄現實貓科動物的生物毛皮與肉質特徵，全面轉譯為 2.2 頭身矮萌拋光胡桃木外殼、象牙白瓷面甲與雙聯黃銅金屬絲天線耳簇，以換取手機螢幕上的高辨識度與耐摔木偶玩具質感；  
2. **放棄雙持雙爪同步揮擊的繁複動作方案**：為了避免在手機小螢幕上雙手持爪造成紙娃娃圖層嚴重重疊遮擋與雜亂穿模，放棄設計雙手雙爪，嚴格遵守 `0-MKT7` 單持規範，改為右手單手持握機械結構分明的「晨曦提線裂空機關爪」，左手維持自然微曲收胸的古典武道防禦架勢。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "lynx",
  "aliases": [
    "marionette_lynx",
    "clockwork_lynx",
    "bobcat",
    "bazaar_lynx",
    "dawn_lynx"
  ],
  "name_zh": "提線猞猁",
  "name_en": "The Marionette Lynx",
  "class_archetype": "武術家 (Monk)",
  "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
  "lore_anchor": "縱躍於晨曦小鎮·木偶集市「懸吊齒輪鐘樓」與「多層山形牆商鋪」屋頂，穿梭於「齒輪吊索大橋·小鎮站」與「晨曦天軌 2 號月台」，巡檢「蔓谷天梯引道」與「巨輪城重型空軌貨運棧橋」，守望小鎮外緣「邊界安全防護彈簧網」，穿梭於「精紡線莊」與「中央油坊」，配合提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳與摺紙工匠·小鶴；通體覆蓋拋光胡桃木雕刻底盤與象牙白瓷面甲、歐風提線雙天線金耳兜帽、雙聯垂直黃銅金屬絲天線天籟耳簇、雙節同軸鐘擺平衡配重短尾、雙環八音風鈴黃銅發條鑰匙，右手單持專屬晨曦提線裂空機關爪，以2.2頭身矮萌微胖體態、四肢精工黃銅球窩鉸鏈、提線滑輪連動身法、屋頂無聲肉墊撲躍與五聯鎢鋼連切撕裂防線見長的歐風市集機關武道家",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1880s-1920s 歐洲古典提線木偶雜技機關偶與巴洛克鐘錶自動偶)",
    "posture": "2.2 頭身矮萌身軀側身45度沉穩站姿，雙足微屈下沉抓地，右手前探亮爪，左手收胸護架，背後雙環發條鑰匙隨秒針每2.5秒跳拍一格勻速自轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "溫潤象牙白瓷圓形面甲（#FFFDF8 / #FFA010），頭頂配備精雕胡桃木雜技小圓帽與護額，眼眶處精準沖孔供雙色翡翠寶石目鏡透光",
    "ears": "頭部兩側對稱安裝雙聯垂直黃銅金屬絲天線天籟耳簇（#FFD028 / #4ED86A），三聯黃銅金屬絲內嵌共鳴音叉線圈，隨秒針微動調焦，無肉耳",
    "torso_and_limbs": "百年陳化拋光胡桃木骨架外包楓木板件（#8B5A2B）與白瓷胸腹襯板，四肢為精工黃銅球窩關節與防滑橡膠軟墊",
    "tail": "雙節同軸車削胡桃木圓柱短尾（#8B5A2B / #FFD028），外接黃銅萬向擺動鉸鏈與圓球形黃銅配重鉛錘",
    "weapon_system": "右手單持專屬「晨曦提線裂空機關爪（Dawn Marionette Steel Claws）」，沖壓高硬度鎢鋼五聯弧刃嵌胡桃木護腕，內置提線滑輪與棘輪機構，底層掛載 equipment.json 既有 hunt_claw (tier 3)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白瓷/打磨楓木高光，面甲基座、胸腹白瓷襯板與手爪襯墊)",
    "primary": "#FFA010 (主色多巴胺暖橘，胡桃木外裝彩漆、耳廓正面塗裝與背心領口飾邊)",
    "secondary": "#4ED86A (次色多巴胺薄荷淺綠，雙色翡翠寶石目鏡、背心扣帶與滑輪飾條)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，鼻頭防塵印記與發條鑰匙中心鉚釘)",
    "metal": "#FFD028 (金屬晨曦黃銅金，雙環發條鑰匙、天線耳簇、黃銅鉸鏈與爪刃基座)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_lynx.png (品牌形象立牌)",
        "web/media/hero/char_lynx.png (官網英雄展示立繪)",
        "docs/art/marionette_lynx_concept.png (概念立繪)",
        "game/assets/sprites/player/lynx_idle.png (64x64 待機)",
        "game/assets/sprites/player/lynx_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/lynx_idle.png (隊伍待機)",
        "web/media/hero/lynx_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/lynx_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/lynx_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/lynx_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/lynx_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/lynx_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/lynx_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/lynx/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/lynx.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/lynx_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/marionette_lynx.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/lynx/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_lynx.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/marionette_lynx_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_lynx.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/lynx_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/lynx_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/lynx_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/lynx_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/lynx_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/lynx_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/lynx_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/lynx/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/lynx.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/marionette_lynx.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/lynx/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行提醒（嚴守任務邊界）**：本任務為「只寫文件，不產圖不產片」。以下提示詞僅作企劃歸檔與規格預置，等待後續美術產圖任務由 sideart 領取執行。

### 8.1 提線猞猁角色單體立繪 Prompt（4:5 垂直角色畫）

```text
masterpiece, best quality, 2.2 head-to-body ratio chibi cute clockwork mechanical toy lynx monk hero, named The Marionette Lynx, standing dynamically on a cobblestone pedestal in a European clockwork bazaar. Made of polished rich walnut wood, glazed ivory-white porcelain faceplate, and gleaming brass joint spheres. Distinctive upright wooden ears topped with twin vertical brass wire acoustic antenna tufts with tiny resonance coils. Wearing a vibrant warm orange acrobat workwear vest with mint green straps and brass buttons, glowing dual-tone emerald quartz gemstone eyes, and a twin-segment walnut pendulum bobtail with brass counterweight sphere. Right hand wearing a mechanical steel claw gauntlet with five retractable curved spring-steel blades and tiny marionette pull-cords, left hand held in a defensive martial posture. A prominent twin-ring chime brass wind-up key mounted on the center back. Clean, dopamine vibrant candy-like colors, warm orange #FFA010, mint green #4ED86A, ivory white #FFFDF8, gold brass #FFD028, sky blue #38A0FF, bold dark blue-purple outline #1F1A3A, soft Tyndall morning sunlight, zero fur, zero skin, zero organic parts, pure mechanical wooden and porcelain toy automaton, 4:5 aspect ratio.
```

### 8.2 提線猞猁晨曦小鎮集市場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```text
panoramic vibrant fairy tale scene in R02 Dawn Town Marionette Bazaar. In the center foreground, a 2.2 head-body ratio cute mechanical toy lynx monk leaps gracefully between European timbered gabled rooftops, right hand slashing forward with glowing five-bladed steel claws leaving golden and warm orange light trails. In the background, bustling cobblestone marketplace with suspended gear belltower swinging its bronze pendulum, marionette shops with pastel painted facades, cableway platforms, steam vents puffing lavender-tinted puffs under warm golden morning sky. Dopamine bright cheerful palette, warm orange, mint green, gold, ivory white, crisp clockwork toy aesthetic, bold stylized outlines, zero real fur, zero feathers, wide-angle cinematic 16:9 aspect ratio.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 4:5 \
  --out docs/art/marionette_lynx_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 16:9 \
  --out docs/art/marionette_lynx_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R02_DAWN_TOWN.md` 既有地標（懸吊齒輪鐘樓、齒輪吊索大橋·小鎮站、晨曦天軌 2 號月台、蔓谷天梯引道、巨輪城重型空軌貨運棧橋、邊界安全防護彈簧網、精紡線莊、中央油坊、多層山形牆商鋪、胡桃木拼花浮空展台底座）與居民 NPC（提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳、摺紙工匠·小鶴、守衛泰坦「集市守護機關·提線巨偶」），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`武術家 (Monk)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  右手單持晨曦提線裂空機關爪，左手收胸護架作防守平衡姿態，左右肢體姿態描述清晰，0 雙持穿模。
- [x] **CANON 世界憲章零毛皮零皮革鐵律**：  
  100% 零真動物肉身、零生物毛皮、零皮革、零羽毛、零黏液；通體轉譯為精雕拋光胡桃木底盤、打磨楓木骨架、象牙白溫潤白瓷面甲、雙聯垂直黃銅金屬絲天線天籟耳簇、雙色翡翠寶石目鏡、雙節同軸鐘擺平衡配重短尾、五聯鎢鋼伸縮爪刃與雙環八音風鈴黃銅發條鑰匙。
- [x] **武術家機關爪與拳套對稱平衡**：  
  作為第十巡第四順位擴充，補齊武術家機關爪第 5 款，與武術家拳套（5 款）達成完全 5:5 對稱平衡！
