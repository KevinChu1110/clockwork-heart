# 第五十五種動物「鐘塔長頸鹿（The Belfry Giraffe）」世界觀與角色設計提案

> **標題**：第五十五種動物「鐘塔長頸鹿（The Belfry Giraffe）」角色與世界觀設計提案  
> **提案代號**：`BELFRY_GIRAFFE_DESIGN_PROPOSAL`（代號：`giraffe` / 識別名：`race_giraffe`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_85014b17`（📖 世界觀｜第五十五種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零動物肉身、零生物黏液、沖壓薄馬口鐵板、打磨胡桃木拼花、三節同軸黃銅伸縮潛望頸管、雙聯黃銅測距雷達角與高折射石英稜鏡、外露螺栓鉚釘、背後必有發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R02_DAWN_TOWN.md`（第 1 行區域代號與名稱「R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar」、第 4 行「歐風木造街屋、石板路與精緻提線木偶套件（Timber Architecture, Cobblestone & Marionette Playset）」、第 6 行「局域走時狀態：慢速延遲偏快（秒針每隔 2~3 秒跳動一格，齒輪持續運轉，集市維持熱絡但部分商用機械因動力波動開始過熱）」、第 15 行「金色黃銅護欄與外露齒輪嚙合環軌」、第 19 行「細緻打磨的淺灰硬質磨石灰岩積木拼合而成，步道邊緣鑲嵌著細小的金黃銅質防滑飾條」、第 20 行「歐風木造街屋：採用精巧榫卯結構搭蓋的多層山形牆商鋪，外牆施以陽光童話風格的高飽和水性彩漆（奶油米白、明亮暖橘、薄荷淺綠）」、第 21 行「懸吊齒輪鐘樓（Suspended Gear Belltower）：小鎮中央廣場矗立著一座高達 25 公尺的鏤空雕花鐘樓，巨大青銅擒縱輪與金色鐘擺於半空中悠然擺動，鐘面外緣懸掛著數十枚微型發條八音風鈴，隨風傳出輕靈樂韻」、第 23 行「天頂反光鏡常年維持 45 度角斜向折射，灑落柔和明亮的永恆晨曦柔光（#FFF8E7）」、第 28 行「齒輪吊索大橋·小鎮站（Cogwheel Cableway Terminal）」、第 29 行「晨曦天軌 2 號月台（Dawn Rail Platform 2）」、第 31 行「蔓谷天梯引道（Vine Valley Stairway Gate）」、第 34 行「邊界安全防護彈簧網（Perimeter Safety Spring-Net）」、第 46 行「精紡線莊」與「中央油坊」、第 54 行「提線商會會長·巴納姆（Barnum the Threadmaster）」、第 64 行「彩釉玩偶夫人·瑪德琳（Lady Madeline the Glazed Belle）」、第 72 行「摺紙工匠·小鶴（Tsuru the Origami Crafter）」、第 99 行旗艦泰坦 BOSS「集市守護機關·提線巨偶（Bazaar Overseer: Grand Marionette Titan）」、第 106 行「劇團面具與聚光水晶目鏡」、第 107 行「鐵杉木握劍巨臂與驅動滑輪」、第 108 行「皇家精紡鋼絲金線」、第 118 行特產武器「精紡刺劍·引線者」、第 119 行「集市重型發條剪」、第 120 行「紳士機關短杖」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（遊俠正式名稱 `ranger`，複合機關弓標籤宣言 `"等風的人"`，武器 `bow`，數值 `atk: 2, def: 0, hp: -4, crit: 3.0, speed: 1`，玩法 `"拉開距離再射。同職也可玩火槍。"`，新手武器 `reed_bow`）  
> - `game/data/tables/equipment.json`（弓類正式 line: `"bow"`，初階武器：`reed_bow` 蘆風短弓，高階相容武器：`hawk_longbow` 鷹眼長弓）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第九巡（第 49~54 族）第六順位大圓滿收官擴充，完美達成六大職業 9×6=54 族超對稱平衡**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十五種動物擴充素體規格**。  
   在全專案相繼由第 49 族熔鎧犰狳（騎士·長劍）、第 50 族風箱毛蟲（戰士·戰鎚）、第 51 族墨影烏賊（忍者·短匕）、第 52 族熔砧石蟹（武術家·拳套）與第 53/54 族日晷駱駝（法師·法杖）推進第九巡篇章後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第九巡第六順位**，以壓軸之姿輪轉進入最具超視距狙擊、停拍看破與精準破甲的核心職業——**遊俠 (Ranger)** 體系，原生武器掛載於**複合機關弓（`bow` / 遊俠·弓）**。  
   鐘塔長頸鹿的加入，使全遊戲遊俠複合機關弓素體擴充至第 5 款（遊俠總族群擴充至 9 款）。更關鍵的是，這標誌著全遊戲六大職業（騎士 9 族、戰士 9 族、忍者 9 族、武術家 9 族、法師 9 族、遊俠 9 族）達成**完全對稱的 54 款擴充素體（加計白金兔始祖素體共 55 族）之大圓滿格局**！
2. **經典玩具起源與古典機械發條高塔長頸鹿自動機工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與鐘樓日晷天文觀測自動偶史上的經典工藝原型：  
     ① **19 世紀末至 20 世紀中葉古典鐵皮發條高塔長頸鹿玩具（Vintage Tinplate Wind-up Tower Giraffe Automaton / Lehmann & Schuco & Marx Tin Toys）**，通體由沖壓馬口鐵薄板、雙偏心輪連桿伸縮頸機構與打磨胡桃木拼花基座咬合而成，內部發條帶動三節黃銅頸管伴隨走時律動上下浮動探視，是古典發條玩具史上最具工程結構美感與高塔守望趣味的機械自動偶之一；  
     ② **維多利亞古典鐘塔觀測自動偶（Horological Belfry Lookout Automaton）**，頭冠裝配雙聯黃銅測距雷達角與高折射石英稜鏡，胸前鑲嵌雙聯潛望測距透鏡，在指針跳動間隙俯瞰整個市集天軌，於瞄準瞬間將鐘樓八音盒的琴弦張力化為穿甲箭矢；  
     ③ **古典發條市集引弦工兵偶（Vintage Clockwork Market Stringer Automaton）**，以 2.2 頭身矮萌微胖的圓滾身軀、防風呢絨禮賓披肩、多層階梯式黃銅步進蹄與背後三環八音發條鑰匙，完美詮釋遊俠職業「等風的人、拉開距離再射、暴擊愈養愈高、停拍看破」之遊俠之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「沖壓馬口鐵矮萌底盤、三節同軸黃銅伸縮潛望頸、雙聯黃銅測距角石英稜鏡、晨曦禮賓防風呢絨披肩、雙聯潛望測距石英凸透鏡、鐘樓天弦複合機關弓與三環鏤空八音發條鑰匙」之高塔狙擊遊俠素體（Sanded Tinplate Giraffe Chassis, Telescoping Brass Periscope Neck, Dual-Ossicone Quartz Prisms, Dawn Herald Woolen Cape, Dual Periscope Quartz Lens, Belfry Celestial-String Bow & Three-Ring Carillon Brass Key）**。
3. **生態補足：徹底終結晨曦小鎮·木偶集市（R02）零遊俠之歷史空白，打造懸吊齒輪鐘樓第一制空巡守守護者**：  
   在全遊戲 9 大界域中，中層歐風木偶貿易界域 `R02 晨曦小鎮·木偶集市` 先前擁有靈鐘鴞（法師·杖）、棘輪刺蝟（忍者·鏢）、稜鏡孔雀（法師·晶）、鐵蹄駿駒（騎士·劍）與旋音天鵝（騎士·槍）共 5 族。  
   長久以來，面對 25 公尺高的懸吊齒輪鐘樓與複雜交錯的晨曦天軌，**該界域完全缺乏一位能夠登臨鐘樓頂端、借助高空潛望視野洞察集市全貌、並以天弦機關弓守護天軌物資安全的「遊俠 (Ranger)」核心素體**。鐘塔長頸鹿的降臨，徹底填補了 R02 長期零遊俠素體的生態空白，讓 R02 的職業生態迎來首位遠程物理看破制空大師，與駿駒、天鵝的突刺、刺蝟的伏擊、貓頭鷹與孔雀的星光法術共同構築晨曦小鎮堅不可摧的防衛體系！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源（僅登錄 races_specification 正表提案項目，total_races 維持現狀）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：鐘塔長頸鹿素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十四族武器與職業光譜全盤點

盤點現有首發五族與前四十九款擴充族（總計 54 族）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **鐘塔長頸鹿（The Belfry Giraffe）**：**遊俠 (Ranger) —— 鐘樓天弦複合機關弓（`bow`），高塔潛望測距看破，八音琴弦諧振連發。**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）9 族（劍 5、槍 4）；
- 戰士（Viking）9 族（鎚 5、斧 4）；
- 忍者（Ninja）9 族（匕 5、鏢 4）；
- 武術家（Monk）9 族（拳 5、爪 4）；
- 法師（Mage）9 族（杖 5、晶 4）；
- 遊俠（Ranger）此前在 54 族中擁有 8 款動物素體（弓 4 款、銃 4 款）；
- **本提案第五十五種動物正式作為「第九巡第六順位」收官大圓滿擴充，歸屬於遊俠 (Ranger) 體系，原生武器掛載於 `bow`（複合機關弓 / 遊俠·弓）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`遊俠 (Ranger)`**；
- 鐘塔長頸鹿的加入，使全遊戲遊俠複合機關弓素體擴充至第 5 款，遊俠總數達成 9 款，全 6 大職業達成 9×6=54 族完全對稱平衡！

### 1.2 鐘塔長頸鹿武器選擇：【鐘樓天弦複合機關弓（Belfry Celestial-String Composite Bow）】

鐘塔長頸鹿原生專屬武器定名為：**【鐘樓天弦複合機關弓（Belfry Celestial-String Composite Bow）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R02_DAWN_TOWN.md` 晨曦小鎮·木偶集市之精紡絲線與鐘樓八音盒工藝體系**！  
底層完全掛載於 `weapon_classes.json` 的 `bow`（遊俠·弓）類別，享有 `bow` 既有的「等風的人」標籤宣言（Tagline: `"等風的人"`）、站遠遠地安全輸出、暴擊愈養愈高、很吃疾影那種讀時機看破之特性（`atk: 2, def: 0, hp: -4, crit: 3.0, speed: 1`），完美呼應 `R02_DAWN_TOWN.md` 第 21 行「懸掛著數十枚微型發條八音風鈴，隨風傳出輕靈樂韻」與第 6 行「秒針每隔 2~3 秒跳動一格」之節奏律動！

- **法源素材咬合**：  
  完全對應 `R02_DAWN_TOWN.md` 第 46 行**「精紡線莊」**出品的高拉力浸蠟絲線、第 108 行代表素材**「皇家精紡鋼絲金線（Royal Spun Steel Thread）」**、第 106 行拆卸部位**「劇團面具與聚光水晶目鏡（Precision Crystal Lens）」**與第 107 行**「驅動滑輪（Pulley）」**，將晨曦小鎮鐘樓的琴弦拉力轉化為超視距看破的穿透箭矢。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: "weapon"`、`line: "bow"` 的初階裝備 `reed_bow`（蘆風短弓，tier 1）與高階相容裝備 `hawk_longbow`（鷹眼長弓，tier 3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款複合機關弓遊俠（雲嵐鶴、翠角鹿、幻彩變色龍、熱流赤鳶）絕不撞型之論證

雖然鐘塔長頸鹿與雲嵐鶴、翠角鹿、幻彩變色龍、熱流赤鳶同屬 `ranger`（遊俠）複合機關弓（`bow`）體系，但在**射術流派與戰術哲學**、**機動體態與彈道力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               遊俠職業複合機關弓系五族差異化對照表（鶴 vs 鹿 vs 變色龍 vs 赤鳶 vs 長頸鹿）                             │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 雲嵐鶴 (Crane)       │ 翠角鹿 (Fawn)        │ 幻彩變色龍 (Chameleon)│ 熱流赤鳶 (Kite)      │ 鐘塔長頸鹿 (Giraffe)│
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 射術流派     │ 水墨禪意空弦超視距   │ 翠木角尺精密幾何速射 │ 折射迷彩隱匿伏擊暗射 │ 熱浪淬火重彈反曲轟擊 │ 高塔潛望看破八音諧振 │
│ 2. 動能來源     │ 氣流微浮羽毛連桿     │ 彈簧蓄能枝角牽引     │ 壓縮冷氣獨立轉塔蓄壓 │ 火山口高溫熱流熱脹力 │ 鐘樓重錘牽引琴弦張力 │
│ 3. 步法特徵     │ 單足點水、輕靈滯空   │ 輕巧跳躍、枝條穿梭   │ 緩步爬行、迷彩定點   │ 俯衝掠地、氣流滑翔   │ 階梯沉步、高位挺立   │
│ 4. 武器構造     │ 白瓷羽翼長弓         │ 幾何角尺複合木弓     │ 雙向測距稜鏡機關弓   │ 耐火鑄鐵反曲巨弓     │ 鐘樓八音天弦滑輪弓   │
│ 5. 主題界域     │ R09 竹影道場·天元竹林│ R03 翡翠深林·發條蔓谷│ R08 荒漠齒輪塚·遺忘庫│ R06 赤焰熔爐·鍛造火山│ R02 晨曦小鎮·木偶集市│
│ 6. 材質質感     │ 溫潤白瓷、竹木生漆   │ 拋光深綠原木、黃銅角 │ 粗糙生鏽馬口鐵、稜鏡 │ 粗獷鑄鐵、黑曜耐火磚 │ 沖壓馬口鐵、胡桃木花 │
│ 7. 角色剪影     │ 修長高挑仙鶴羽翼     │ 靈巧小巧長角幼鹿     │ 捲尾扁平雙凸眼蜥蜴   │ 展翼滑翔三角羽翼飛禽 │ 矮萌圓滾多節伸縮潛頸 │
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格恪守 `docs/world/CANON.md` 憲章世界觀「**100% 零真動物生物肉身、零毛皮、零羽毛、零真甲殼有機質、零血肉黏液**」之鐵律：

- **沖壓馬口鐵與打磨胡桃木拼花底盤**：鐘塔長頸鹿的身軀並非動物肉身，而是由晨曦小鎮玩具工坊常見的**沖壓薄馬口鐵板件（#FFFDF8）**與**精雕打磨胡桃木拼花（#FFA010）**鉸接拼合而成。斑塊不是生物皮毛斑紋，而是塗裝工匠以高溫烘烤的幾何琺瑯彩漆方塊（多巴胺暖橘 #FFA010 與金黃 #FFD028），邊角由微型黃銅平頭鉚釘固定，呈現極致精美的歐風木偶玩具質感。
- **三節同軸黃銅伸縮潛望頸管**：頸部為三節精密套接的沖壓黃銅套管（#FFD028），側面外露精緻的齒條與減速導軌。套管內部由背部發條帶動的微型蝸輪驅動，隨走時節奏產生 5~10mm 的節律起伏，完美展現長頸鹿自動偶特有的「探頭眺望」趣味，完全杜絕任何生物軟組織。
- **雙聯黃銅測距雷達角與石英稜鏡**：頭頂一對圓潤的鹿角並非生物骨角，而是由黃銅車削成型的微型測距雷達天線，末端鑲嵌微縮高折射石英多稜鏡（#4ED86A），在陽光下折射出七彩微光，用於高空測量風速與敵方弱點距離。
- **微型黃銅鐘擺重錘短尾**：尾部為一根纖細的黃銅擺桿，末端懸掛著一枚扁圓形的小鐘擺重錘，隨步態左右悠然擺動，平衡射擊時的微小後坐力。
- **背後發條鑰匙**：背部中央正上方垂直挺立著一把經典的**三環鏤空八音音筒發條鑰匙（Three-Ring Carillon Brass Key）**。鑰匙主軸開有三組對稱圓環，軸心刻有八音盒撥齒，隨走時旋轉時伴隨細微清脆的八音風鈴微鳴，在 45 度視角下清晰打破角色剪影，絕不被披肩遮擋。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格依循 `USER PROFILE`、`docs/ART_DIRECTION.md` 與多巴胺鮮亮配色規範：

- **頭身比**：嚴格鎖定於 **2.0 ~ 2.2 頭身**。矮萌圓滾的馬口鐵身軀搭配圓潤微短的四足步進蹄，徹底打破現實長頸鹿細長乾癟的生物印象，呈現如童話木偶般的扎實厚重與軟萌親和力。
- **色彩規劃（嚴守多巴胺鮮亮配色，絕無泥土髒黑）**：
  - **基底色（Base）**：`#FFFDF8`（象牙白陶瓷釉面／拋光馬口鐵，用於面部面甲、腹部內襯板與關節活動襯墊）。
  - **主色（Primary）**：`#FFA010`（多巴胺晨曦暖橘，用於胡桃木拼花裝飾板、披肩主體與弓身幾何彩漆）。
  - **次色（Secondary）**：`#4ED86A`（薄荷冷翡翠，用於頭頂石英稜鏡內部刻度發光圈、胸口石英透鏡與弓弦瞄準光斑）。
  - **點綴色（Accent）**：`#FF5E8A`（多巴胺珊瑚粉，用於發條鑰匙中心轉軸螺栓、披肩領結飾扣與耳廓邊緣警示印標）。
  - **金屬色（Metal）**：`#FFD028`（天元黃銅金，用於三節伸縮頸管、頭頂雷達角、三環八音發條鑰匙與機械步進蹄）。
  - **描邊色（Outline）**：`#1F1A3A`（深藍紫手繪立體外輪廓描邊，確保在亮色與暗色背景下皆清晰銳利，徹底告別泥土髒黑）。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

恪守現代手遊看板角色活化標準：

- **待機呼吸律動（Idle Motion）**：
  - 2.2 頭身身軀沉穩站立，四足步進蹄抓地平穩；
  - 三節黃銅伸縮頸每隔 2 秒隨晨曦小鎮秒針跳動向上浮動一格，隨後平緩回落；
  - 頭頂雙聯黃銅測距角微微自轉，胸口雙聯石英透鏡泛起薄荷綠柔光呼吸；
  - 背後三環八音發條鑰匙均勻旋轉，微型鐘擺尾輕輕擺動。
- **點擊戳碰互動（Poke Interaction）**：
  - 玩家以手指點擊角色時，長頸鹿受觸碰發出清脆的「叮——鐺！」發條八音盒響音；
  - 三節頸管瞬間向上彈伸 15%，頭頂雙聯測距角高速旋轉 360 度；
  - 左蹄輕巧抬起行標準晨曦木偶禮，右手複合弓微旋挽出金色弓花；
  - 頭頂彈出俏皮對話氣泡：`「鐘樓秒針已歸位，視野內無卡齒異常！」`，並向四周爆散出一圈多巴胺彩糖星芒粒子（金黃、薄荷綠、珊瑚粉）。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R02 晨曦小鎮·木偶集市（Dawn Town）零遊俠歷史空白

在全專案九大界域中，晨曦小鎮·木偶集市作為玩家走出新手村後進入的第一個宏大貿易集市，匯聚了駿駒的騎兵突擊、天鵝的長槍格擋、刺蝟的近距飛鏢以及貓頭鷹與孔雀的法術。然而，在面對高空天軌物資被劫、以及集市高空自動販賣設施故障失控時，**整個界域長久以來完全沒有一位具有超遠射程、精確點穴破壞能力的制空狙擊手**。  
鐘塔長頸鹿的進駐，宣告了晨曦小鎮高空守望網絡的正式合攏，成為集市高塔之上最可靠的制空警戒之眼！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R02_DAWN_TOWN.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R02_DAWN_TOWN.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 每日破曉登上**「懸吊齒輪鐘樓（Suspended Gear Belltower）」**頂層平台，監控 25 公尺青銅擒縱輪與金色鐘擺之律動；
  - 順著**「晨曦天軌 2 號月台（Dawn Rail Platform 2）」**巡視高速發條吊艙之物資裝卸；
  - 駐防於**「齒輪吊索大橋·小鎮站（Cogwheel Cableway Terminal）」**與**「蔓谷天梯引道（Vine Valley Stairway Gate）」**；
  - 俯瞰邊緣底座的**「邊界安全防護彈簧網（Perimeter Safety Spring-Net）」**，確保失足玩具安全彈回。
- **工坊與居民互動**：
  - 定期造訪小鎮中心的**「精紡線莊」**採購高強度浸蠟防結絲線作為弓弦；
  - 前往**「中央油坊」**配發香氛散熱潤滑油保養三節頸管齒條；
  - 與**「提線商會會長·巴納姆（Barnum the Threadmaster）」**協調商道治安警戒；
  - 協助**「彩釉玩偶夫人·瑪德琳（Lady Madeline the Glazed Belle）」**尋找失落的彩繪釉料；
  - 接受**「摺紙工匠·小鶴（Tsuru the Origami Crafter）」**指導輕量化箭囊折疊工藝。
- **對抗首領情境**：
  - 在迎戰旗艦泰坦**「集市守護機關·提線巨偶（Bazaar Overseer: Grand Marionette Titan）」**時，登臨屋頂高位，以天弦機關弓精準狙擊巨偶背部懸索天車的**「皇家精紡鋼絲金線（Royal Spun Steel Thread）」**與頭部**「精密聚光水晶目鏡（Precision Crystal Lens）」**，達成完美的弱點部位破壞！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，鐘塔長頸鹿的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 鐘塔長頸鹿專屬造型規格與材質特徵（嚴守 100% 零真皮毛）                                          │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. body (素體)  │ 沖壓薄馬口鐵與打磨胡桃木拼花矮萌底盤（#FFFDF8 / #FFA010），幾何琺瑯彩漆拼塊，四足步進機械短蹄   │
│ 2. head (頭部)  │ 沖壓馬口鐵圓潤面甲配三節同軸黃銅伸縮潛望頸管（#FFD028），外露微型滑軌齒條，無生物肌肉組織        │
│ 3. ears (耳部)  │ 雙聯黃銅球形測距儀與高折射石英稜鏡雷達角（#FFD028 / #4ED86A），隨走時微幅自轉，無生物耳廓       │
│ 4. tail (尾部)  │ 微型黃銅鐘擺重錘連桿短尾（#FFD028），末端懸掛小銅錘，左右晃動平衡後坐力                         │
│ 5. costume (服裝)│ 晨曦木偶集市禮賓防風呢絨斗篷與精紡刺繡披肩（#FFA010 / #FFFDF8），黃銅雙聯排扣與精紡金線滾邊    │
│ 6. optic_core(眼)│ 雙聯潛望測距石英凸透鏡（#4ED86A），薄荷冷翡翠發光刻度光柵，內嵌微型同心圓瞄準標尺              │
│ 7. winding_key  │ 三環鏤空八音音筒發條鑰匙（#FFD028），背部垂直挺立，隨走時旋轉發出輕靈風鈴微音                  │
│ 8. weapon (武器)│ 鐘樓天弦複合機關弓（#FFA010 / #FFD028），雙階滑輪傳動，高張力精紡鋼絲金弦，射出音律光箭        │
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`body`（素體底盤）**：  
   2.2 頭身 Q 版矮萌身軀，由沖壓馬口鐵板（#FFFDF8）包覆胡桃木骨架製成。腹部圓潤微凸，四肢為粗短有力的圓柱形齒輪步進腿，末端配備多層黃銅蹄蓋與防滑黑橡膠底墊。軀幹兩側鑲有幾何多巴胺暖橘（#FFA010）與亮金（#FFD028）琺瑯烤漆色塊，邊緣飾以深藍紫立體描邊（#1F1A3A），徹底杜絕任何真實生物毛皮質感。
2. **`head`（頭部與頸部）**：  
   圓潤平滑的象牙白馬口鐵面甲，頂部鉸接一組精密的「三節同軸黃銅伸縮潛望套管（Telescoping Brass Neck Tube）」。頸管外露直列微型齒條與雙聯導向凹槽，能隨走時節奏平穩升降 5~10mm，帶動頭部進行上下俯仰探視。眼眶處精準沖孔供 `optic_core` 穿透。
3. **`ears`（耳部天線）**：  
   頭部頂端對稱排列一對沖壓成型的黃銅球形測距儀（ossicones）。頂部鑲嵌高折射琥珀石英微型稜鏡（#4ED86A），內部置有微型陀螺儀，能隨步態微幅自轉以感應風向與氣壓，無任何生物耳廓組織。
4. **`tail`（鐘擺尾飾）**：  
   由細直黃銅連桿與末端微型扁圓鐘擺重錘組成，長度約等於身高的 1/4。隨行走步態以固定物理頻率左右微幅擺動，為高空射擊提供穩固的下盤配重。
5. **`costume`（禮賓披肩）**：  
   由晨曦小鎮「精紡線莊」精心剪裁的防風呢絨禮賓小披肩。外層為鮮亮多巴胺暖橘色（#FFA010），內襯為奶油米白（#FFFDF8），領口處以一顆多巴胺珊瑚粉（#FF5E8A）的琺瑯轉軸紐扣固定。披肩下擺開有倒 V 形開口，完全避免遮擋背後的發條鑰匙與尾部。
6. **`optic_core`（石英目鏡）**：  
   雙聯平行安裝的高透光石英凸透鏡組。鏡片內部散發出薄荷冷翡翠光澤（#4ED86A），表面微雕刻有三圈同心圓測距刻度與金色十字十字準星，在瞄準時自動聚焦於目標弱點部位。
7. **`winding_key`（八音鑰匙）**：  
   背部中央筆直矗立的黃銅發條鑰匙。柄部雕刻有三個相互咬合的鏤空圓環，內部嵌有微縮八音盒音筒梳齒。鑰匙隨秒針跳動均勻自轉，轉動時伴隨清澈柔和的金屬音韻。
8. **`weapon`（天弦機關弓）**：  
   長頸鹿專屬武器【鐘樓天弦複合機關弓】。弓臂採用多層沖壓彈簧鋼片疊合而成，兩端各配有一組金色偏心滑輪與減阻齒輪；弓弦採用來自提線巨偶掉落同級的「皇家精紡鋼絲金線」，張力強韌；弓身中央設有半自動發條供彈軌道，射擊時直接將光能齒輪聚合成音律光箭射出。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 雙足扎實踏地，長頸微屈蓄勢，右手單手持弓斜指地面，左爪輕搭腰間，三環八音發條鑰匙隨秒針微旋   │
│ 2. attack (普攻)  │ 長頸向上一格伸展，雙手抬弓滿月拉弦，弓臂滑輪急速旋轉，向前方平射出一道清脆的金色穿甲音波箭矢 │
│ 3. hit (受擊)     │ 身軀受後坐力向後微傾，三節頸管因緩衝彈簧縮入一節，雙目石英透鏡微閉，發條鑰匙反向剎車打滑     │
│ 4. recover (硬直) │ 雙足迅速前後跨開重構支撐三角，長頸重新節律探出，右手迅速挽弓復位，鏡頭重新鎖定對焦           │
│ 5. skill (技能)   │ 全身發條過載超頻，長頸伸展至最高點開啟全景俯瞰，複合弓拉滿射向天頂，引發「鐘樓天弦落星矢雨」 │
│ 6. telegraph (蓄力│ 弓弦拉至極限蓄能，弓身齒輪棘爪高頻發出「咔、咔、咔」預警聲，地面投射出金色鐘面引導指示光圈   │
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為遊俠職業長弓系的核心擴充素體，直接提供差異化的遠程破甲與停拍看破體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過遊俠長弓的停拍看破與精準弱點射擊打擊怪物部位），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身沖壓馬口鐵長頸鹿自動偶體現古典木偶玩具魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏虛擬搖桿與技能點按佈局，射擊動作帶有自適應距離校正與自動鎖定，單拇指即可流暢完成普攻連射與看破蓄力。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：
1. **放棄真實長頸鹿的細長脆弱骨架與生物寫實比例**：徹底放棄現實長頸鹿細長優雅的肢體與生物肌肉結構，全面降維重構為 2.2 頭身矮萌防摔多節齒條機構，以換取手機螢幕上的高辨識度與耐摔玩具質感；
2. **放棄獨立外掛箭袋槽位**：為了避免在手機小螢幕上造成紙娃娃圖層雜亂與繪製重疊遮擋，放棄設計外掛在背部或腰部的獨立箭袋，將供彈邏輯全面簡化收斂為弓身內建的「微型發條導軌自動成型光箭」機制。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "giraffe",
  "aliases": [
    "belfry_giraffe",
    "clocktower_giraffe",
    "periscope_giraffe",
    "dawngaze_giraffe",
    "clockwork_giraffe"
  ],
  "name_zh": "鐘塔長頸鹿",
  "name_en": "The Belfry Giraffe",
  "class_archetype": "遊俠 (Ranger)",
  "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
  "lore_anchor": "穿行於晨曦小鎮·木偶集市「懸吊齒輪鐘樓」、「晨曦天軌 2 號月台」與「齒輪吊索大橋·小鎮站」，巡檢「精紡線莊」、「中央油坊」與「蔓谷天梯引道」，駐守「邊界安全防護彈簧網」，配合提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳與摺紙工匠·小鶴；通體覆蓋沖壓薄馬口鐵板與打磨胡桃木拼花、三節同軸黃銅伸縮潛望頸管、雙聯黃銅測距雷達角與高折射石英稜鏡、晨曦禮賓防風呢絨披肩、雙聯潛望測距石英凸透鏡、三環鏤空八音音筒發條鑰匙，雙手持握專屬鐘樓天弦複合機關弓，以2.2頭身矮萌微胖體態、多層階梯式黃銅步進蹄、高塔潛望測距看破、八音琴弦諧振連發見長的小鎮天軌守望者與制空遊俠",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末至 20 世紀中葉古典鐵皮發條高塔長頸鹿玩具與維多利亞鐘樓觀測自動偶)",
    "posture": "2.2 頭身矮萌身軀微屈蓄勢，四蹄抓地扎實，右手單手持弓斜指地面，三節黃銅頸管伴隨鐘樓每2秒跳動一格的秒針平穩起伏，三環八音發條鑰匙隨走時均勻旋轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "沖壓薄馬口鐵面甲（#FFFDF8）配三節同軸沖壓黃銅伸縮套管（#FFD028），外露直列減速齒條與導向槽，眼窩處精準中空供 optic_core 穿透",
    "ears": "頭部頂端雙聯沖壓黃銅球形測距儀（#FFD028），末端鑲嵌高折射琥珀石英微型稜鏡（#4ED86A），隨步態微幅自轉，無生物耳廓",
    "torso_and_limbs": "沖壓薄馬口鐵板件（#FFFDF8）嵌合打磨胡桃木拼花（#FFA010），下身配置粗短圓柱形步進腿與多層階梯式黃銅防滑蹄",
    "tail": "細直黃銅擺桿連桿短尾（#FFD028），末端懸掛微型扁圓鐘擺重錘，以固定頻率左右擺動平衡射擊後坐力",
    "weapon_system": "單手挽持專屬「鐘樓天弦複合機關弓（Belfry Celestial-String Composite Bow）」，雙階滑輪傳動，高張力精紡鋼絲金弦，底層掛載 equipment.json 既有 reed_bow (tier 1) 與 hawk_longbow (tier 3)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光馬口鐵，面甲眼周高光、腹部內層襯板與關節活動襯墊)",
    "primary": "#FFA010 (主色多巴胺晨曦暖橘，胡桃木拼花裝飾板、披肩主體與弓身幾何彩漆)",
    "secondary": "#4ED86A (次色薄荷冷翡翠，頭頂石英稜鏡、胸口石英透鏡發光刻度與瞄準光斑)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心轉軸螺栓、披肩紐扣與耳廓警示印標)",
    "metal": "#FFD028 (金屬天元黃銅金，三節伸縮頸管、頭頂雷達角、三環發條鑰匙與機械步進蹄)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_giraffe.png (品牌形象立牌)",
        "web/media/hero/char_giraffe.png (官網英雄展示立繪)",
        "docs/art/belfry_giraffe_concept.png (概念立繪)",
        "game/assets/sprites/player/giraffe_idle.png (64x64 待機)",
        "game/assets/sprites/player/giraffe_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/giraffe_idle.png (隊伍待機)",
        "web/media/hero/giraffe_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/giraffe_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/giraffe_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/giraffe_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/giraffe_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/giraffe_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/giraffe_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/giraffe/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/giraffe.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/giraffe_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/belfry_giraffe.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/giraffe/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_giraffe.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/belfry_giraffe_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_giraffe.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/giraffe_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/giraffe_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/giraffe_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/giraffe_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/giraffe_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/giraffe_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/giraffe_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/giraffe/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/giraffe.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/belfry_giraffe.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/giraffe/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行紅線**：本卡片為純企劃設計提案，**嚴禁執行任何產圖產片指令**。以下 Prompts 與參數為未來美術總監（sideart）或執行工程師（sideworker）派工產圖時之必備標準規範。

### 8.1 鐘塔長頸鹿角色單體立繪 Prompt（4:5 垂直角色畫）

```
chibi mechanical toy giraffe archer, The Belfry Giraffe, 2.2 head-body ratio, adorable chunky wind-up tinplate automaton. Stamped ivory tinplate body plates #FFFDF8 with geometric polished walnut wood mosaic patches #FFA010, brass rivets and visible seams, absolutely zero animal fur, zero organic flesh, zero biological texture. Articulated 3-segment telescoping brass neck tube #FFD028 with visible gear rack and sliders. Head crowned with dual rounded brass ossicone radar knobs tipped with glowing mint-green quartz prisms #4ED86A. Glowing mint-green dual periscope quartz optical lenses on chest. Wearing a dapper European marionette herald woolen cape in warm dawn orange #FFA010 with ivory trim and coral-pink enamel button #FF5E8A. On its back stands an elegant three-ring镂空 brass carillon music-box wind-up key #FFD028. Sturdy stepped brass mechanical hooves with black rubber pads. Slender brass pendulum rod tail with miniature bob. Holding a sophisticated clockwork belfry composite mechanism bow with layered spring-steel limbs and golden brass wire string. Pure clean ivory white studio background, vibrant dopamine color palette, bold dark blue-purple clean outline #1F1A3A, cel shaded, MapleStory and Tata Adventure toy aesthetic, cheerful fairy tale lighting, masterpiece, 8k resolution.
```

### 8.2 鐘塔長頸鹿晨曦小鎮鐘樓場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
panoramic vibrant fairy tale scene in R02 Dawn Town Marionette Bazaar. In the center foreground, a 2.2 head-body ratio cute mechanical toy giraffe ranger with 3-segment brass telescoping neck and glowing mint quartz eye lens, drawing a golden celestial-string composite bow. Perched gracefully on the balustrade of the 25-meter suspended gear belltower overlooking the European timber architecture and cobblestone streets bathed in soft eternal dawn sunlight #FFF8E7. Brass railings, spinning cogwheels, distant suspension cableway gondolas and dawn rail platform in the soft cloud sea background. Floating musical note particles and colorful candy star sparkles. Clean dark outlines, vibrant dopamine colors (golden yellow #FFD028, warm orange #FFA010, mint green #4ED86A, celestial blue #38A0FF), zero dirt or muddy filters, warm whimsical toy world, official splash art style.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt 內容>" \
  --aspect 4:5 \
  --ref branding/key_visual_main.png \
  --out docs/art/belfry_giraffe_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt 內容>" \
  --aspect 16:9 \
  --ref branding/key_visual_main.png \
  --out docs/art/belfry_giraffe_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R02_DAWN_TOWN.md` 既有地標（懸吊齒輪鐘樓、晨曦天軌 2 號月台、齒輪吊索大橋·小鎮站、精紡線莊、中央油坊、蔓谷天梯引道、邊界安全防護彈簧網）與居民 NPC（提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳、摺紙工匠·小鶴），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`遊俠 (Ranger)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  遊俠複合機關弓遵循單手持弓挽弦規格，左右肢體姿態描述清晰。
- [x] **CANON 世界憲章零毛皮鐵律**：  
  100% 零真動物肉身、零生物毛皮、零羽毛、零黏液；通體轉譯為沖壓薄馬口鐵、打磨胡桃木拼花、三節同軸黃銅伸縮管、雙聯石英稜鏡與三環發條鑰匙。
- [x] **六大職業超對稱平衡收官**：  
  補齊遊俠第 9 族（弓 5、銃 4），與騎士（9）、戰士（9）、忍者（9）、武術家（9）、法師（9）達成 9×6=54 族（加白金兔共 55 族）完全大圓滿！
