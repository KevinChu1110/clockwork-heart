# 第六十三種動物「破竹羚牛（The Bamboo-Cleaving Takin）」世界觀與角色設計提案

> **標題**：第六十三種動物「破竹羚牛（The Bamboo-Cleaving Takin）」角色與世界觀設計提案  
> **提案代號**：`BAMBOO_CLEAVING_TAKIN_DESIGN_PROPOSAL`（代號：`takin` / 識別名：`race_takin`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_1371827c`（📖 世界觀｜第六十三種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零皮革、零動物肉身、零生物黏液、零真羽毛、零生鏽、零機油污漬；沖壓耐磨青古銅鑄鐵合金底盤、象牙白溫潤彩釉白瓷護腹腹板、雙聯鍛造黃銅反曲扭角、精工冷軋鎢鋼防塵面甲、半球形高透耐震翡翠石英目鏡、天元拓荒開山粗麻道袍與沖壓黃銅護肩甲、雙聯高壓竹露潤滑油壺與背部排氣減震水碓閥門、三葉天元雕花黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調；多巴胺高飽和鮮亮色彩：檸檬黃#FFD028、落日暖橘#FFA010、薄荷綠#4ED86A、天藍#38A0FF、珊瑚粉#FF5E8A、深藍紫描邊#1F1A3A）  
> - `docs/world/regions/R09_BAMBOO_GROVE.md`（第 1 行區域代號與名稱「R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo」、第 4 行「沙盤工藝材質套件：生漆陶瓷、高剛性天然竹木纖維、精密簧片木機關、溫潤青石板、精工黃銅關節與高彈性絲弦木偶套件」、第 6 行「局域走時狀態：空靈靜謐的呼吸式走時伴隨勻速破勢拍點（秒針每 3.0 秒在翠竹撞擊聲中發出清脆悠遠的木簧鐘聲「叮——咚！」，微風拂過竹梢時帶動微型簧片低吟，走時沉穩厚重而暗藏凌厲的爆發律動；需在竹浪搖曳與木人樁敲擊節奏中捕捉身法空檔）」、第 15 行「青古銅榫卯壁板與雕琢著祥雲波紋的深色鑄鐵角件」、第 19 行「發條天元竹海（Clockwork Bamboo Sea Slopes）」、第 20 行「青石武鬥古道場·演武坪（Slate Martial Dojo & Drill Ground）」、第 21 行「山門竹煙茶舍（Mountain Gate Tea Pavilion）」、第 22 行「飛瀑木簧水碓（Clockwork Waterfall Waterwheel & Pestle）」、第 25 行「天元秒針由青銅合竹雕琢而成，針身長達五公里，每 3.0 秒在翠竹撞擊聲中平穩向前跳動一格，伴隨著悠遠宏亮的『叮——咚！』晨鐘之音」、第 29 行「古老重型零件輸送翻斗軌道·竹林終端站（Ancient Heavy Parts Conveyor Rail: Bamboo Terminal）」、第 30 行「晨曦天軌 9 號演武道場月台（Dawn Rail Platform 9: Zen Dojo Terminal）」、第 32 行「凌雲青竹懸索天梯·道場總站（Zen Bamboo Cableways: Dojo Terminal）」、第 33 行「天元雲海風帆渡口（Zen Sky-Ferry Port）」、第 35 行「翠竹彈力阻尼編織網（Elastic Bamboo Damping Web）」、第 43 行「陶瓷熊貓武僧（Porcelain Panda Monks）」、第 44 行「木雕竹葉青蛇（Carved Bamboo Green Vipers）」、第 45 行「演武木人童子（Clockwork Dummy Apprentices）」、第 47 行「高純度清香竹露潤滑油」、第 51 行守護泰坦「醉步發條武鬥熊貓·阿波泰坦」、第 56 行煮茶發條偶「阿茶（Acha）」、第 65 行天元道場武僧長老「圓空師傅（Master Yuan Kong）」、第 74 行機關木人樁小師弟「木木（Mu-Mu）」、第 87 行「狂風修羅木人傀儡（Gale Asura Wooden Dummy）」、第 91 行「巡林木雕竹葉青蛇（Forest-Patrolling Carved Bamboo Viper）」、第 95 行「醉步陶瓷武僧傀儡（Drunken-Stance Porcelain Monk Puppet）」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（戰士正式名稱 `viking`，標籤宣言 `"站到最後才是贏家"`，武器 `axe`，數值 `atk: 3, def: 2, hp: 12, crit: -2.0, speed: -1`，玩法 `"防禦高血厚，拿重斧敲擊部位。同職也可拿鎚。"`，初始相容武器 `battle_axe`）  
> - `game/data/tables/equipment.json`（戰斧類正式 line: `"axe"`，初始相容武器：`battle_axe` 戰斧，tier 1）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十一巡第二順位核心擴充，開啟戰士 6:5 戰斧對稱擴張，迎來第 63 族大陣容**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第六十三種動物擴充素體規格**。  
   在全專案相繼於第十巡收官（第 60 族黑曜金龜法師·晶、第 61 族彩喙巨嘴鳥遊俠·銃達成前 60 族與 12 武器 5:5 完美平衡）以及第十一巡首位成員第六十二種動物破冰海象（騎士·長劍，開啟騎士 6 劍 5 槍體系）順利完成審查與歸檔後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十一巡第二順位**，以磐石之勢輪轉進入全遊戲血防最厚重、霸體蓄力、部位破壞與穩重反制的核心職業——**戰士 (Viking)** 體系，原生武器掛載於**天元破竹開山巨斧（`axe` / 戰士·斧）**。  
   破竹羚牛的加入，使全遊戲戰士戰斧素體擴充至第 6 款（鋼岳象、浪花海獺、重角犀牛、劈木河狸、鋼牙豕/星岩鼴鼠、破竹羚牛），呼應騎士長劍擴充，開啟第十一巡全新對稱篇章！  
2. **經典玩具起源與東方機巧發條羚牛自動偶工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與東方機巧自動偶史上的經典工藝原型：  
     ① **1920s-1950s 經典古典發條鐵皮重獸自動機（Vintage Tinplate Wind-up Heavy Beast Automaton / 德國 Schuco、Lehmann 與日本昭和時代重裝發條獸名作）**，通體由沖壓青古銅馬口鐵、偏心重力凸輪與防滑重型齒輪足底咬合而成，走動時粗壯四肢伴隨發條節奏「鏗、鏘、咚」沉穩踏地，是古典機械玩具史上最具沉浸打擊感與厚重手感的重裝自動偶代表；  
     ② **東方機巧木石榫卯與生漆陶瓷工藝偶（Oriental Karakuri Craft & Zen Puppet Automaton）**，將羚牛（金毛扭角羚）生活於高山高海拔密竹險峰、以強悍身軀破開千年老竹的雄渾生態，轉譯為青古銅鑄鐵外殼、象牙白生漆陶瓷胸腹護板與雙聯鍛造黃銅反曲扭角，兼具東方禪意道場的古雅與重裝機械的厚重霸氣；  
     ③ **道場劈竹開山拓荒工藝（Zen Dojo Bamboo-Cleaving Pioneer Craftsman）**，將經典開山大斧轉譯為「天元破竹開山巨斧」，斧身以青鋼榫卯加固，配以天然竹木纖維編織防滑握把與排氣減震水碓閥門，完美詮釋戰士職業「站到最後才是贏家、防禦高血厚、拿重斧敲擊部位」之戰士之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「青古銅鑄鐵重裝底盤、黃銅反曲扭角重盔、翡翠石英耐震雙目鏡、天元拓荒道袍重肩甲、雙聯竹露油壺減震閥、三葉天元雕花黃銅發條鑰匙與天元破竹開山巨斧」之竹影道場拓荒戰士素體（Bronze Cast Chassis, Brass Twisted Horn Cowl, Emerald Quartz Visors, Zen Pioneer Robe, Dual Bamboo Oil Flasks, Tri-Leaf Zen Brass Key & Zen Bamboo-Cleaving Battle Axe）**。  
3. **生態補足：徹底終結天元竹林（R09）長久以來「零戰士」之歷史空白，打造道場破障霸體防線**：  
   在全遊戲 9 大界域中，中下層東方武道沙盤界域 `R09 竹影道場·天元竹林` 先前僅擁有瓷韻熊貓（武術家·拳）、竹影青蛇（忍者·匕）、澄心水豚（法師·晶）與嵐翼鼯鼠（忍者·鏢）共 4 族，是全遊戲 9 大界域中族群數量最少、生態最為單薄的界域。  
   更重要的是，天元竹林長久以來在武術家寸勁、青蛇遁影與水豚靜思之外，**面對狂暴木人樁、失控狂風修羅木人傀儡、以及守護泰坦阿波泰坦醉拳過載卡住的青銅榫頭危機，整個竹影道場完全缺乏一位能夠立足演武坪、以超重青古銅底盤穩抗衝擊、以雙刃拓荒開山巨斧劈開雜亂鋼竹與破開重型障礙的「戰士 (Viking·Axe)」核心素體**！破竹羚牛的降臨，徹底終結了 R09 天元竹林長期以來零戰士的生態歷史空白，為道場補齊最後一塊關鍵的防禦與拓荒基石！  
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 運作邏輯（僅登錄 races_specification 正表提案項目，更新 total_races 為 62）。  
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：破竹羚牛素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。  

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有六十二族武器與職業光譜全盤點

盤點現有首發五族與前五十七款擴充族（總計 62 族，含第 60 族黑曜金龜、第 61 族彩喙巨嘴鳥、第 62 族破冰海象）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **提線猞猁（The Marionette Lynx）**：武術家 (Monk) —— 晨曦提線裂空機關爪（`claw`），提線滑輪連動身法，屋脊輕盈撲躍，五聯鎢鋼連切撕裂防線。
- **黑曜金龜（The Obsidian Scarab）**：法師 (Mage) —— 赤焰黑曜護體靈晶（`crystal`），多面黑曜石晶核懸浮調諧，耐熱六足滑步，織盾成刃引爆地熱晶芒！
- **彩喙巨嘴鳥（The Prism-Bill Toucan）**：遊俠 (Ranger) —— 林冠聚能氣動銃（`gun`），高空林冠光學測距，多室減速氣動高壓發射，雙爪扣枝抗震，一響定生死！
- **破冰海象（The Icebreaker Walrus）**：騎士 (Knight) —— 深淵破冰海軍短闊劍（`sword`），深海超耐壓鐘底盤，雙聯鎢鋼破冰鑿破障，低重心水壓阻尼格擋，重刃下劈破陣迎擊！
- **破竹羚牛（The Bamboo-Cleaving Takin）**：**戰士 (Viking) —— 天元破竹開山巨斧（`axe`），青古銅鑄鐵重裝底盤，黃銅反曲扭角破障，站到最後霸體蓄力，開山重劈裂地破勢！**

在《發條之心》全專案進入第十一巡擴充體系後：
- 騎士（Knight）達到 11 族（劍 6、槍 5）；
- 戰士（Viking）此前擁有 10 族（斧 5、鎚 5）；
- **本提案第六十三種動物正式作為「第十一巡第二順位」核心擴充，歸屬於戰士 (Viking) 體系，原生武器掛載於 `axe`（戰斧 / 戰士·斧）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`戰士 (Viking)`**；
- 破竹羚牛的加入，使全遊戲戰士戰斧素體擴充至第 6 款，戰士總數達成 11 款，使戰士（6 斧 5 鎚）與騎士（6 劍 5 槍）在第十一巡形成嚴謹對稱的先鋒陣容！

### 1.2 破竹羚牛武器選擇：【天元破竹開山巨斧（Zen Bamboo-Cleaving Battle Axe）】

- **底層武器掛載**：掛載於 `game/data/tables/weapon_classes.json` 之 `axe`（戰斧）體系，繼承戰士「站到最後才是贏家、防禦高血厚、拿重斧敲擊部位」的核心戰術宣言。相容既有初始裝備 `battle_axe`（戰斧，tier 1）；
- **專屬武器外觀與機巧設計**：
  - 武器外觀命名：`weapon_takin_zen_bamboo_cleaving_axe`（天元破竹開山巨斧 / Zen Bamboo-Cleaving Battle Axe）；
  - 斧面構造：由高強度打磨生漆黑鐵與青古銅冷軋板精密鉚接而成的雙刃大斧，斧刃經過天元竹海微風高頻淬火，散發薄荷綠（#4ED86A）與天元金黃（#FFD028）相間的金屬反光；
  - 減重與力學結構：斧身兩側開有八卦減重透氣孔與齒輪配重槽，斧柄以多層天然老竹纖維加壓複合而成，外層纏繞粗麻防滑吸震帶；
  - 單持規範（0-MKT7 嚴格遵守）：右手單手穩握戰斧長柄中下段，斧刃斜指地面蓄勢待發；左臂自然屈曲於胸前，厚實的青古銅護腕與黃銅鉚釘護肩面向前方，形成嚴密防禦格擋姿態，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。

### 1.3 戰鬥風格與數值無關手感

- **重步穩踏與減震拍點**：配合 R09 天元竹林每 3.0 秒「叮——咚！」的勻速秒針鐘鳴，破竹羚牛在待機與移動時每一步踏在青石板上都帶有沉重的金屬摩擦音與「咚」的青石沉降感；
- **霸體蓄力與部位破壞反饋**：在發動攻擊與重劈時，背部排氣減震水碓閥門微噴出白熱竹露蒸氣（「哧——！」），利用重力慣性自上而下劃出扇形破竹光弧，對怪物部位進行精確打擊；
- **與既有 5 款戰斧戰士之差異化切分矩陣**：

| 戰士族群 | 原生武器名稱 | 戰鬥流派 | 核心動能 | 步法特徵 | 剪影與視覺辨識 |
|---|---|---|---|---|---|
| **鋼岳象** | 巨輪開山重斧 | 開山質量重劈 | 巨型重力衝壓 | 直線沉重重步 | 巨輪長鼻與長牙重裝長斧 |
| **浪花海獺** | 琉璃破障重斧 | 洋流阻尼下墜 | 水壓浮力反推 | 搖擺滑步踏浪 | 扁平尾與琉璃海錨闊斧 |
| **重角犀牛** | 熔爐破陣重鋼戰斧 | 淬火直線衝陣 | 地熱超壓衝程 | 狂暴直線衝鋒 | 巨大淬火單鼻角與雙手長柄單持斧 |
| **劈木河狸** | 深林拓荒劈木巨斧 | 工程三點定位劈斫 | 齒輪滑輪咬合 | 扁尾貼地扎根 | 穿孔黃銅扁尾與拓荒伐木重斧 |
| **破竹羚牛** | **天元破竹開山巨斧** | **道場破障霸體重劈** | **竹海共振排氣減震** | **八角青石沉穩扎馬** | **黃銅反曲雙扭角、粗麻道袍肩甲與雙刃開山斧** |

---

## 二、 外觀視覺與機械構造（Visual & Mechanical Anatomy）

### 2.1 2.0~2.2 頭身 Chibi 玩具比例與輪廓

- **經典 Q 版人體工學**：整體嚴格遵循 2.0 ~ 2.2 頭身比。頭部包含沉穩防塵面甲與碩大黃銅扭角約佔身高 45%，圓滾敦厚的青古銅合金軀幹佔 35%，短粗扎實的青石防滑雙足佔 20%，完美杜絕傳統嚴肅機甲或粗方塊感；
- **剪影辨識（Silhouette Distinction）**：
  - 頭頂高聳向外側反曲的「雙聯鍛造黃銅扭角」（#FFD028），呈現經典金毛扭角羚的辨識特徵；
  - 敦厚微弓的戰鬥站姿，背部微微隆起，露出雙聯竹露油壺與排氣水碓閥門；
  - 單持重斧斜立身側，左肩高聳的黃銅護肩甲與道袍下擺構成沉穩如山的三角形幾何剪影。

### 2.2 CANON 零毛皮世界憲章材質轉譯

嚴格遵守 `docs/world/CANON.md` 世界憲章鐵律，**100% 零真動物生物肉身、零毛皮、零真皮、零皮革、零黏液、零真羽毛、零生鏽、零機油污漬**：

- **軀幹與底盤（Chassis）**：
  - 沖壓高強度青古銅鑄鐵合金板件（#3A4454），邊角以多巴胺薄荷綠（#4ED86A）耐磨烤漆包邊；
  - 胸腹部覆蓋溫潤如玉的象牙白彩釉白瓷護腹板（#FFFDF8），瓷面上帶有細微冰裂紋，並繪有淺金色太極齒輪暗紋；
- **頭部與面罩（Head Unit）**：
  - 沖壓打磨青鋼面甲，雙頰鑲嵌光滑黃銅咬合齒輪；
  - 頭頂立體反曲的「雙聯鍛造黃銅扭角」，角尖拋光發亮，角身刻有同心圓加強肋線；
- **目鏡系統（Optic Core）**：
  - 半球形高透耐震翡翠石英目鏡（#4ED86A），內置同心圓十字校準刻度，目鏡周圍嵌有深藍紫（#1F1A3A）金屬防眩眼眶；
- **服飾外裝（Costume）**：
  - 天元道場拓荒粗麻織物道袍（#FFFDF8），邊緣飾以落日暖橘（#FFA010）高飽和滾邊；
  - 左肩裝配單側沖壓黃銅護肩甲（#FFD028），中心飾有一枚天元祥雲浮雕黃銅鉚扣；
- **背飾與機能構件（Back Curio）**：
  - 背部左右兩側各掛載一只高壓竹露潤滑油壺（透明耐壓玻璃外包黃銅護網），中央連通微型排氣減震水碓閥門；
- **發條鑰匙（Winding Key）**：
  - 背部正中央垂直插入一柄「三葉天元雕花黃銅發條鑰匙（#FFD028）」，鑰匙三葉柄部各鏤空有一枚祥雲孔洞，中心鉚釘點綴鮮亮珊瑚粉（#FF5E8A）。

### 2.3 多巴胺童話配色盤（Dopamine Color Palette）

嚴格杜絕任何髒黑、泥土暗沉與傳統辦公室灰冷感，全面比照《塔塔冒險隊》與《發條之心》多巴胺鮮亮高飽和色彩體系：

- **基底色（Base）**：`#FFFDF8`（奶油米白 / 溫潤彩釉白瓷胸腹板與素雅道袍）；
- **主色（Primary）**：`#4ED86A`（薄荷竹翠綠 / 青古銅板件烤漆飾邊與翡翠石英目鏡）；
- **金色（Accent Gold）**：`#FFD028`（天元金黃 / 雙聯鍛造黃銅扭角、三葉發條鑰匙與戰斧雕花）；
- **暖橘色（Accent Orange）**：`#FFA010`（落日暖橘 / 道袍防磨滾邊與肩甲飾帶）；
- **青石暗色（Secondary）**：`#3A4454`（青石古銅灰 / 鑄鐵底盤基底，沉穩高質感）；
- **珊瑚粉（Detail Pink）**：`#FF5E8A`（多巴胺珊瑚粉 / 發條鑰匙中心鉚釘與油壺指示浮標）；
- **外輪廓線（Outline）**：`#1F1A3A`（深藍紫立體手繪描邊，全圖採用 1.5~2.0px 加粗描邊，徹底消弭毛刺與髒黑感）。

### 2.4 發條鑰匙規格（Key Specification）

- **鑰匙名稱**：`key_takin_tri_leaf_zen_brass`（三葉天元雕花黃銅發條鑰匙）；
- **自轉節律**：每隔 3.0 秒伴隨天元竹海鐘鳴平穩勻速順時針旋轉一格（約 30 度），同時帶動體內微型擒縱棘輪發出清脆的「嗒、鈴——」共鳴；
- **插座公規化**：遵循標準背部發條插座接口規範，與既有全 62 族發條鑰匙 100% 互換無阻。

---

## 三、 地標關聯與世界觀生態融入（Landmark & Narrative Integration）

### 3.1 官方界域對齊：R09 竹影道場·天元竹林

本提案中所有世界觀敘事、巡查動線與任務背景，**100% 逐字引用自官方區域檔案 `docs/world/regions/R09_BAMBOO_GROVE.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **主要巡查據點**：
  - 「青石武鬥古道場·演武坪（Slate Martial Dojo & Drill Ground）」：破竹羚牛每日清晨在此進行千次破竹巨斧下劈修煉，以沉重蹄足踏平震動青石板；
  - 「發條天元竹海（Clockwork Bamboo Sea Slopes）」：穿行於發條竹林坡道之間，揮動巨斧為穿梭的竹雕青蛇與熊貓武僧開闢巡林石徑，斬除過載糾結的金屬竹蔓；
  - 「山門竹煙茶舍（Mountain Gate Tea Pavilion）」：在茶舍門前痛飲阿茶師傅煮沸的「高純度清香竹露潤滑油」，浸潤重型球形關節與減震齒輪；
  - 「飛瀑木簧水碓（Clockwork Waterfall Waterwheel & Pestle）」：負責維護水車木碓的傳動軸，以巨斧砍伐合規硬木修復老舊木人樁；
- **邊界與交通接駁點**：
  - 「古老重型零件輸送翻斗軌道·竹林終端站（Ancient Heavy Parts Conveyor Rail: Bamboo Terminal）」：定點檢修自 R08 荒漠齒輪塚抵達的重型翻斗礦車，確保減震枕木無變形；
  - 「晨曦天軌 9 號演武道場月台（Dawn Rail Platform 9: Zen Dojo Terminal）」：迎接自中央浮空島天宮大廳抵達的求道旅客；
  - 「凌雲青竹懸索天梯·道場總站（Zen Bamboo Cableways: Dojo Terminal）」：護送修煉有成的武僧搭乘竹藤吊籠前往天宮大廳；
  - 「天元雲海風帆渡口（Zen Sky-Ferry Port）」：檢查風帆滑翔飛舟的青古銅扣具；
  - 「翠竹彈力阻尼編織網（Elastic Bamboo Damping Web）」：巡邏邊界防墜網，確保彈力青竹無開裂老化。

### 3.2 角色背景故事與 NPC 關係網絡

- **身世起源**：破竹羚牛是由道場初代機關大師以高山重型拓荒機偶為原型所雕鑿的發條自動偶。長久以來，它默默承擔著天元竹林最繁重艱鉅的開山拓石與道場修繕重任；
- **與圓空師傅的默契**：長老圓空師傅曾指點破竹羚牛：「力大若無章法，巨斧亦會崩口；唯有順應竹節之紋理，方能一斧破開萬丈竹浪。」破竹羚牛將此銘記於芯，將剛猛巨斧與道場呼吸走時融為一體；
- **與煮茶偶阿茶的茶友誼**：阿茶總會在水碓旁為羚牛備好一整桶溫熱的清香竹露，笑稱「羚牛師兄喝油像喝山泉一樣痛快」；
- **與木人小師弟木木的互動**：木木最喜歡爬在羚牛寬闊平穩的雙扭角上打瞌睡，羚牛揮斧開山時，木木便在旁邊手忙腳亂地幫忙搬運竹料；
- **直面阿波泰坦的破局重任**：守護泰坦「醉步發條武鬥熊貓·阿波泰坦」因背脊主軸被青銅榫頭卡死而陷入狂暴。全道場弟子皆因阿波的霸道醉拳而無法近身，唯有擁有極限霸體與防禦厚度的破竹羚牛，能夠頂住狂暴醉拳的連續轟擊，以精準的巨斧下劈精確斬擊卡住的榫頭，助泰坦恢復清明！

---

## 四、 紙娃娃七大部件槽位規格（Paperdoll 7-Slot Specifications）

嚴格比照 `docs/design/paperdoll_slots.json` 七大標準部件規範，為破竹羚牛規劃專屬部件條目：

```json
{
  "race_id": "takin",
  "name_zh": "破竹羚牛",
  "name_en": "The Bamboo-Cleaving Takin",
  "default_items": {
    "chassis": "chassis_takin_bronze_cast_default",
    "head_unit": "head_takin_brass_twisted_horn_cowl",
    "optic_core": "face_takin_emerald_quartz_visors",
    "costume": "costume_takin_zen_pioneer_heavy_robe",
    "back_curio": "curio_takin_dual_bamboo_oil_flasks",
    "winding_key": "key_takin_tri_leaf_zen_brass",
    "weapon": "weapon_takin_zen_bamboo_cleaving_axe"
  }
}
```

### 4.1 各槽位詳細規格描述

1. **底盤素體（`chassis`）**：
   - ID：`chassis_takin_bronze_cast_default`
   - 名稱：青古銅鑄鐵重裝底盤
   - 規格：2.2 頭身矮萌重裝獸人素體，四肢為高硬度青古銅球形關節，足部為防滑青石蹄，腹部嵌象牙白彩釉白瓷板，100% 零毛皮零肌肉。
2. **頭部護具（`head_unit`）**：
   - ID：`head_takin_brass_twisted_horn_cowl`
   - 名稱：黃銅反曲扭角重盔
   - 規格：沖壓防塵青鋼面甲，兩側延伸出標誌性的高光黃銅反曲扭角（#FFD028），抗震耐撞。
3. **眼部目鏡（`optic_core`）**：
   - ID：`face_takin_emerald_quartz_visors`
   - 名稱：翡翠石英耐震雙目鏡
   - 規格：半球形凸透石英目鏡，散發微亮多巴胺薄荷綠光輝（#4ED86A），內置同心圓受力分析網格。
4. **服飾服裝（`costume`）**：
   - ID：`costume_takin_zen_pioneer_heavy_robe`
   - 名稱：天元拓荒道袍重肩甲
   - 規格：米白天然粗麻短袍配落日暖橘飾邊，左肩單側沖壓黃銅重型護肩甲，腰繫深藍紫編織腰帶。
5. **背飾組件（`back_curio`）**：
   - ID：`curio_takin_dual_bamboo_oil_flasks`
   - 名稱：雙聯竹露油壺減震閥
   - 規格：雙聯微型金屬護網油壺與氣動洩壓排氣閥，移動時隨秒針節律噴吐微型白熱蒸氣環。
6. **發條鑰匙（`winding_key`）**：
   - ID：`key_takin_tri_leaf_zen_brass`
   - 名稱：三葉天元雕花黃銅發條鑰匙
   - 規格：三葉鏤空古典黃銅鑰匙，中心飾有珊瑚粉耐震鉚釘（#FF5E8A），每 3.0 秒自轉一格。
7. **專屬武器（`weapon`）**：
   - ID：`weapon_takin_zen_bamboo_cleaving_axe`
   - 名稱：天元破竹開山巨斧
   - 規格：單手持握雙刃大斧，斧面鏤空太極透氣槽，柄身以高剛性複合竹木編織，符合 0-MKT7 單持規範。

---

## 五、 六大標準戰鬥姿態規劃（Six Combat Poses Specifications）

嚴格對齊 `review.md` 姿態標準與 LANCZOS 雙規格（128x128 / 512x512）要求：

1. **待機姿態（`idle`）**：
   - 動作特徵：身體微側 30 度穩固扎馬站姿，雙蹄踏定青石板；右手單手將巨斧斜立於右側，左臂曲於胸前呈現沉穩守勢；背後發條鑰匙每 3.0 秒平穩自轉，油壺閥門規律吐出微型蒸氣；
2. **預警姿態（`telegraph`）**：
   - 動作特徵：雙膝微下沉，重心後移蓄力，雙扭角微微前傾對準目標；右臂單手將巨斧高舉過頭頂，斧刃泛起高亮多巴胺金黃（#FFD028）破勢預警光暈；
3. **攻擊姿態（`attack`）**：
   - 動作特徵：猛然前踏半步，右臂引導巨斧帶動沉重重力動能自上而下劃出 180 度開山重劈，斧刃觸地瞬間激盪出弧形薄荷綠碎石衝擊波；
4. **受擊姿態（`hit`）**：
   - 動作特徵：上身後仰約 15 度，雙蹄死死抓地滑退半步；左肩黃銅重肩甲向前頂起格擋，體內傳動齒輪發出清脆的「鏗鏘」抗震反彈火花，霸體不倒；
5. **收招姿態（`recover`）**：
   - 動作特徵：重劈過後雙足重新站穩，雙手自然接過斧柄由下往上回旋收招，背部水碓排氣閥「哧——！」長鳴排出一團減震蒸氣，回歸待機防禦架勢；
6. **技能姿態（`skill`）**：
   - 動作特徵：【破竹旋風斬】破竹羚牛原地單手橫掄戰斧旋轉一整圈，斧身八卦鏤空孔激起銳利竹浪呼嘯，隨後接一記勢大力沉的跳躍重劈，周身爆發出落日暖橘與薄荷綠交織的璀璨齒輪星芒粒子！

---

## 六、 PRODUCT_LOCK §9 准入門檻六問六答（Gatekeeper Six Questions & Six Answers）

1. **問題一：這個設計服務哪一根核心體驗支柱？**
   - **回答**：服務第一支柱「**世界與角色情感共鳴（Awakening Toy World & Tactile Companionship）**」與第二支柱「**打擊感與手感回饋（Weighty Combat & Tactile Crunch）**」。破竹羚牛以古典發條重裝玩具與東方道場工藝為底蘊，以其踏實厚重的步伐、霸體下劈與反差萌態，徹底終結 R09 天元竹林「零戰士」的生態空白，給予玩家無與倫比的安全感與破障打擊樂趣。
2. **問題二：核心循環中掛在哪一個節點？**
   - **回答**：掛載於核心戰鬥循環之「**戰鬥出征（破壞霸體/敲擊部位）-> 掉落零件/解鎖圖鑑 -> 衣櫥紙娃娃外觀收集與客製化（Paperdoll Customization）**」。為喜愛高血防重裝、霸體換血、沉穩攻堅與道場國風美學的玩家提供無可替代的戰士外觀素體選擇。
3. **問題三：是否增加首包體積（Bundle Size Impact）？**
   - **回答**：本提案為純文字 Markdown 規格文件，增量為 0。未來紙娃娃切片與資產嚴格遵循首包預算規範，預估總素材量 < 0.8 MB，完全在預算控制之內。
4. **問題四：有沒有增加額外的維護成本或代碼複雜度？**
   - **回答**：完全零代碼改動。底層武器完全相容既有 `axe`（戰斧）與 `battle_axe`，七大槽位完全繼承既有 `paperdoll_renderer.gd` 渲染管線，無需新增任何新系統邏輯。
5. **問題五：商業化模型是什麼？**
   - **回答**：嚴格落實 `docs/BUSINESS.md` 規範，素體與外觀部件為純外觀收集品，**絕對零付費數值壓迫（Zero Pay-to-Win）**，可透過主線進度解鎖、圖鑑成就兌換或常規外觀補給獲得。
6. **問題六：這個功能放棄了什麼？**
   - **回答**：放棄了敏捷高頻連段、浮空位移與遠程投射能力；專注於極致的近身血防肉搏、部位破壞蓄力重劈與不動如山的道場霸體守護者體驗。

---

## 七、 資料表註冊配置（JSON Payload for `paperdoll_slots.json`）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "takin",
  "aliases": [
    "bamboo_cleaving_takin",
    "zen_takin",
    "clockwork_takin",
    "golden_takin",
    "mountain_takin"
  ],
  "name_zh": "破竹羚牛",
  "name_en": "The Bamboo-Cleaving Takin",
  "class_archetype": "戰士 (Viking)",
  "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
  "lore_anchor": "駐守於竹影道場·天元竹林「青石武鬥古道場·演武坪」，穿行於「發條天元竹海」與「飛瀑木簧水碓」之間，仰望「凌雲青竹懸索天梯·道場總站」與「晨曦天軌 9 號演武道場月台」，巡檢「古老重型零件輸送翻斗軌道·竹林終端站」與「翠竹彈力阻尼編織網」，在「山門竹煙茶舍」飲用清香竹露潤滑油保養軸承，結伴圓空師傅、煮茶偶阿茶與木人小師弟木木，庇護陶瓷熊貓武僧、木雕竹葉青蛇與演武木人童子；通體覆蓋沖壓青古銅鑄鐵合金底盤與象牙白瓷護腹板、雙聯鍛造黃銅反曲扭角重盔、翡翠石英耐震雙目鏡、天元拓荒道袍重肩甲、雙聯竹露油壺減震閥、三葉天元雕花黃銅發條鑰匙，右手單持專屬天元破竹開山巨斧，以2.2頭身矮萌厚重體態、扎實青石蹄踏步、霸體蓄力開山重劈見長的天元竹林守護戰士",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1920s-1950s 經典古典發條鐵皮重獸偶與東方機巧榫卯自動偶)",
    "posture": "2.2 頭身矮萌重裝身軀微側30度穩重扎馬站姿，雙蹄穩踏地面，右手單持雙刃戰斧斜立於身側，左臂曲於胸前呈厚重防禦架勢，背後三葉發條鑰匙隨竹林秒針每3.0秒鐘鳴一格勻速自轉",
    "standee_height_px": 800,
    "standee_width_px": 560
  },
  "mechanical_features": {
    "horns": "雙聯鍛造高光黃銅反曲扭角，角尖微向上翹，刻有同心圓加強肋線，隨步伐微幅震動",
    "face": "沖壓青鋼防塵面甲，雙頰鑲嵌光滑黃銅咬合齒輪，半球形高透耐震翡翠石英雙目鏡",
    "torso_and_limbs": "青古銅鑄鐵合金厚重底盤，胸腹鑲嵌溫潤象牙白生漆陶瓷板，四肢為球形轉向鉸鏈配防滑青石蹄",
    "venting": "背部左右雙聯耐壓玻璃竹露油壺，中央連通微型水碓氣動排氣減震閥門",
    "key": "三葉天元祥雲雕花黃銅發條鑰匙，中心飾有珊瑚粉防震鉚釘"
  },
  "color_palette": {
    "primary": "#FFFDF8 (奶油白陶瓷生漆胸腹板與道袍)",
    "secondary": "#4ED86A (多巴胺薄荷綠板件烤漆邊與翡翠石英目鏡)",
    "accent_gold": "#FFD028 (天元金黃雙扭角、發條鑰匙與戰斧雕花)",
    "accent_orange": "#FFA010 (落日暖橘道袍防磨滾邊)",
    "dark_bronze": "#3A4454 (青古銅鑄鐵厚重板件底盤)",
    "accent_pink": "#FF5E8A (珊瑚粉防震鉚釘與油壺浮標)",
    "outline": "#1F1A3A (深藍紫立體手繪描邊)"
  },
  "default_items": {
    "chassis": "chassis_takin_bronze_cast_default",
    "head_unit": "head_takin_brass_twisted_horn_cowl",
    "optic_core": "face_takin_emerald_quartz_visors",
    "costume": "costume_takin_zen_pioneer_heavy_robe",
    "back_curio": "curio_takin_dual_bamboo_oil_flasks",
    "winding_key": "key_takin_tri_leaf_zen_brass",
    "weapon": "weapon_takin_zen_bamboo_cleaving_axe"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

依據專案美術總監規範與品牌資產手冊（`brand_assets.md`、`art_direction.md`），為未來概念產圖提供標準化雙規格提示詞（嚴守 `--ref branding/key_visual_main.png`）：

### 8.1 官方立繪概念提示詞（Hero Standee Prompt）

```text
Chibi 2.2 head-to-body ratio clockwork takin warrior toy automaton, standing firmly on aged slate pavement of a zen bamboo grove dojo. Pure awakening toy, 100% NO animal fur, NO leather, NO organic meat, NO biological tissue, NO rust, NO oil stains. Crafted from stamped heavy bronze cast plates (#3A4454 and #4ED86A mint green trims) and polished ivory white porcelain belly plate (#FFFDF8). Head featuring prominent forged twisted brass horns curved outwards (#FFD028 gold) and glowing dual emerald quartz visor eyes (#4ED86A mint green) set in deep indigo violet metal frames (#1F1A3A). Wearing a zen pioneer heavy linen training robe (#FFFDF8) with sunset warm orange trim (#FFA010) and a single stamped brass pauldrons on the left shoulder. On the back, dual glass flasks of bamboo lubricating oil with brass protective mesh and a rotating tri-leaf zen cloud-carved brass wind-up key with a coral pink central rivet (#FF5E8A). Right hand single-wields a heavy double-bladed bamboo-cleaving battle axe with woven bamboo fiber handle grip. Solid wide stance, thick bottom jelly buttons feel, crisp hand-drawn cell-shading with deep indigo violet outlines (#1F1A3A), bright warm morning sun tyndall rays filtering through bamboo, clean cream white background --ar 1:1 --stylize 250
```

### 8.2 負面提示詞（Negative Prompt）

```text
flesh, realistic animal fur, skin texture, biological horns, teeth, real takin, beast face, dark fantasy, dirty rust, grunge, oil leaks, steampunk goggles, photorealistic, human face, 3D blender render, ugly, deformed, blurry, extra limbs, dual wielding, floating weapons, messy background, low quality
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **23f-1 職業正式名稱檢驗**：全文 100% 統一使用 `戰士 (Viking)` 單一正式名，無狂戰士、角鬥士、開山狂徒等混淆自創詞彙。
- [x] **0-MKT7 單持武器檢驗**：破竹羚牛右手單持 `天元破竹開山巨斧`，左手為胸前護身防禦架勢，全圖精準 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模。
- [x] **CANON 世界憲章檢驗**：100% 零真皮毛、零皮革、零肉身、零生物黏液、零真羽毛、零生鏽；身軀為沖壓青古銅鑄鐵合金底盤、生漆陶瓷胸腹板、黃銅扭角、石英目鏡、三葉發條鑰匙。
- [x] **ART_DIRECTION 多巴胺色彩檢驗**：高飽和鮮亮色彩（奶油米白 #FFFDF8、薄荷綠 #4ED86A、天元金黃 #FFD028、落日暖橘 #FFA010、青古銅灰 #3A4454、珊瑚粉 #FF5E8A），深藍紫立體手繪描邊（#1F1A3A），絕無暗黑泥土廢土色。
- [x] **區域生態錨定檢驗（0-PLAN1 必查點 1 & 3）**：精準咬合 `R09_BAMBOO_GROVE.md`，深度融入天元竹林之道場演武坪、木簧水碓、山門茶舍、圓空師傅、阿茶、木木與守護泰坦阿波泰坦醉拳危機，地標 100% 逐字對齊既有檔案，零自創地標。
- [x] **盤點表全盤點檢驗（0-PLAN1 必查點 4）**：第 1.1 節精準盤點既有首發五族與前 57 款擴充族（總計 62 族，含第 60 族黑曜金龜、第 61 族彩喙巨嘴鳥、第 62 族破冰海象），職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠）。
- [x] **包體與准入門檻檢驗（0-PLAN1 必查點 2 & PRODUCT_LOCK §9）**：純文字 Markdown 規格文件，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況，明確放棄事項，符合零數值壓迫（Zero Pay-to-Win）原則。
- [x] **7 大槽位與 6 大姿態完備**：chassis、head_unit、optic_core、costume、back_curio、winding_key、weapon 七大槽位 ID 規範齊全；idle、telegraph、attack、hit、recover、skill 六大戰鬥姿態節律完備。
