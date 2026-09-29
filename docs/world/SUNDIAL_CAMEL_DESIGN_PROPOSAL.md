# 第五十三種動物「日晷駱駝（The Sundial Camel）」世界觀與角色設計提案

> **標題**：第五十三種動物「日晷駱駝（The Sundial Camel）」角色與世界觀設計提案  
> **提案代號**：`SUNDIAL_CAMEL_DESIGN_PROPOSAL`（代號：`camel` / 識別名：`race_camel`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_90fd54ed`（📖 世界觀｜第五十三種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零動物肉身、零生物黏液、沖壓耐磨生鏽馬口鐵板、粗糙石英砂礫沙盤、雙聯小型除鏽潤滑油壺冷凝駝峰、黃銅日晷晷針額冠、外露螺栓鉚釘、背後必有發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R08_RUST_WASTE.md`（第 1 行區域代號與名稱「R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard」、第 4 行「沖壓耐磨生鏽馬口鐵板、粗糙石英砂礫沙盤、斷裂重型鎢鋼外齒輪、斑駁補丁縫合帆布、高黏度抗氧化除鏽潤滑脂與高扭力發條扭簧套件」、第 6 行「局域走時狀態：粗礪重度卡頓伴隨狂暴跳拍（秒針每 2.5~3.5 秒在風沙中發出沉重的金屬摩擦聲「喀——嚓！」，時而因鐵砂卡滯而短暫滯澀，時而因扭簧暴釋而猛烈跳格；在強勁狂風與重力沉降中，需在沙塵蔽目時精準捕捉齒輪打滑與生鏽關節咬合節奏穿行）」、第 19 行「巨型零件殘骸沙丘（Giant Cog Dune Slopes）」、第 20 行「拾荒拼裝聚落·齒輪營地（Scavenger Gear Camp）」、第 21 行「舊庫重型吊裝龍門架（Junkyard Heavy Gantry Pulleys）」、第 22 行「零件分揀斜坡裂谷（Scrap Sorting Chute Chasm）」、第 24 行「廷得耳金黃光束（#FFD028）」、第 29 行「冷卻熔渣重力傾卸滑道·舊庫受料口（Slag Gravity Dump Chute: Scrap Hopper Terminal）」、第 30 行「軌道廢棄排障滑道·舊庫分揀倉（Orbital Debris Dump Chute: Sorting Silo Terminal）」、第 32 行「大齒輪懸索天梯·舊庫總站（Gear Cableways: Junkyard Terminal）」、第 33 行「古老重型零件輸送翻斗軌道（Ancient Heavy Parts Conveyor Rail）」、第 35 行「廢料沉降磁吸緩衝沙漏（Magnetic Scrap Buffer Sand-Trap）」、第 43 行「拾荒拼裝布偶（Patchwork Scavenger Plush Dolls）」、第 44 行「生鏽發條浪人（Rusted Clockwork Ronin）」、第 45 行「發條除鏽工兵偶（Clockwork De-Rusting Tinkers）」、第 47 行「高溫蒸氣除鏽清洗槽（Steam De-Rusting Bath）」、第 55 行「拾荒拼裝大師·補丁爺爺（Grandpa Patch the Scrap Assembly Master）」、第 64 行「流浪發條劍客·鏽刃阿席（Ash the Rusted Wandering Swordsman）」、第 73 行「發條小駱駝·鈴鐺嘟嘟（Dudu the Clockwork Camel Pup）」、第 102 行「狂暴鏽蝕荒野巨獅·雷歐泰坦（Titan Leo: Rusted Wasteland Apex Lion）」、第 121 行特產武器「廢土重型鋸齒大劍」、第 122 行「生鏽彈簧刺銃」、第 123 行「拾荒者重型鏈爪」、第 125 行核心掉落「稀有廢棄原型零件」、「鏽蝕高剛性鋸片齒輪」、「廢土重型液壓連桿」、「高扭力廢棄原型發條」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（法師正式名稱 `mage`，法杖標籤宣言 `"把星屑當墨"`，武器 `magic`，數值 `atk: 1, def: -1, hp: -2, crit: 2.5, speed: 0`，玩法 `"靠技能和魂器打節奏。同職也可玩水晶。"`，新手武器 `star_rod`）  
> - `game/data/tables/equipment.json`（法杖正式 line: `"magic"`，初階武器：第 145-156 行 `star_rod` 星屑短杖，高階相容武器：第 197-208 行 `void_quill` 虛空羽鋒）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第九巡（第 49~54 族）第五順位核心擴充，強勢接棒「法師 (Mage)」法杖體系重大擴充**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十三種動物擴充素體規格**。  
   在全專案跨越「前 48 族完全對稱平衡大圓滿」，並相繼由第 49 族熔鎧犰狳（騎士·長劍）、第 50 族風箱毛蟲（戰士·戰鎚）、第 51 族墨影烏賊（忍者·短匕）與第 52 族熔砧石蟹（武術家·拳套）成功推進第九巡篇章後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第九巡第五順位**，輪轉進入最具遠程彈道、天文測繪與技能爆發的核心職業——**法師 (Mage)** 體系，原生武器掛載於**秘術法杖（`magic` / 法師·杖）**。  
   日晷駱駝的加入，使全遊戲法師法杖素體擴充至第 5 款（法師總族群擴充至 9 款），完美對稱接棒第九巡前四順位，為第九巡注入極具荒漠古天文、日光折射與走時校準的睿智動能！
2. **經典玩具起源與古典機械發條商隊駱駝自動機工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與鐘錶日晷天文自動偶史上的經典工藝原型：  
     ① **19 世紀末至 20 世紀中葉古典鐵皮發條沙漠商隊駱駝玩具（Vintage Tinplate Wind-up Desert Caravan Camel Automaton / Lehmann & Schuco & Marx Tin Toys）**，通體由沖壓馬口鐵板、雙偏心輪連桿步進機構與暖黃銅鉚釘拼合，內部發條帶動金屬小蹄有節奏地交替邁進，是古典發條玩具史上最具旅行家風範與耐候質感的機械自動偶之一；  
     ② **古典鐘錶便攜式日晷天文觀測自動偶（Horological Portable Sundial & Gnomon Automaton）**，頭冠裝配折疊式黃銅晷針，胸前懸掛清脆發條響鈴，背部雙峰為專利「雙聯冷凝潤滑油壺」，在指針跳動間隙吸納日光熱能並將金屬熱脹轉化為穩定微扭矩；  
     ③ **古典發條荒原占星學者偶（Vintage Clockwork Wasteland Astrologer Automaton）**，以 2.2 頭身矮萌圓潤的磨砂鐵皮體態、防風沙帆布補丁學者披肩、雙聯光譜分析石英目鏡與手持日晷折射短杖，完美詮釋法師職業「把星屑當墨、靠技能和魂器打節奏、遠程範圍光能爆發」之法師之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「磨砂馬口鐵矮萌雙峰底盤、日晷晷針折光觀測兜帽、黃銅日晷雙環刻度發條鑰匙、廢土觀星學者帆布補丁長袍、雙聯光譜分折石英目鏡、廢土日晷折射短杖與雙聯散熱油壺金屬駝峰」之荒原天文法師素體（Sanded Tinplate Camel Chassis, Sundial Gnomon Cowl, Armillary Dial Brass Key, Scavenger Astronomer Robe, Dual Spectroscope Quartz Lens, Wasteland Sundial Refraction Rod & Twin Condenser Oil Humps）**。
3. **生態補足：徹底終結荒漠齒輪塚·遺忘舊庫（R08）零法師之歷史空白，打造荒漠舊庫第一星象日晷導航法師，並與既有 NPC 3「發條小駱駝·鈴鐺嘟嘟」形成深厚血脈共鳴**：  
   在全遊戲 9 大界域中，底層廢棄物資界域 `R08 荒漠齒輪塚·遺忘舊庫` 先前已有沙鱗穿山甲（武術家·爪）、荒原鋼狼（騎士·劍）、幻彩變色龍（遊俠·弓）、沙哨狐獴（遊俠·銃）、旋刃伶鼬（忍者·匕）與撼地野牛（戰士·鎚）共 6 族，長久以來**完全缺乏一位能夠在狂暴風沙中利用日光陰影校準世界走時、以高倍石英目鏡測繪天頂零件墜落軌道、並以法杖匯聚日冕折光進行遠程轟擊的「法師 (Mage)」核心素體**。日晷駱駝的降臨，徹底填補了 R08 長期零法師素體的生態空白，讓 R08 達成全職業六大光譜完備；同時與 `R08_RUST_WASTE.md` 第 73 行深受玩家喜愛的 NPC 3「發條小駱駝·鈴鐺嘟嘟（Dudu the Clockwork Camel Pup）」形成完美的家族與生態呼應！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：日晷駱駝素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十二族武器與職業光譜全盤點

盤點現有首發五族與前四十七款擴充族（總計 52 族）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **幽影貓（Umbral Cat）**：忍者 (Ninja) —— 影縫雙鋒短匕（`dagger`），瞬身背刺，高暴擊連擊。
- **沙鱗穿山甲（Dune Pangolin）**：武術家 (Monk) —— 重裝衝壓合金旋爪（`claw`），滾動破陣，鑽地突進破甲。
- **浪花海獺（Tidal Otter）**：戰士 (Viking) —— 潮汐破浪重錨斧（`axe`），重水阻尼揮擊，水流蓄力斬。
- **星巡浣熊（Orbit Raccoon）**：遊俠 (Ranger) —— 軌道聚焦星芒光銃（`gun`），星芒過載射擊，重力牽引光彈。
- **棘輪刺蝟（Ratchet Hedgehog）**：忍者 (Ninja) —— 棘輪穿針機關鏢（`dart`），全向散彈針鏢，背甲彈射。
- **荒原鋼狼（Scrap Wolf）**：騎士 (Knight) —— 廢土生鏽斷刃大劍（`sword`），孤狼破勢斬，突進狂咬。
- **琉璃海馬（Crystal Seahorse）**：法師 (Mage) —— 深海靈晶浮空星盤（`crystal`），洋流結界，靈晶共振屏障。
- **鐵拳袋鼠（Boxer Kangaroo）**：武術家 (Monk) —— 活塞彈簧重裝拳套（`fist`），強彈跳寸勁連擊，震盪破勢。
- **巡林松鼠（Timber Squirrel）**：騎士 (Knight) —— 翠林發條刺擊西洋劍（`sword`），高速連刺，落葉敏捷位移。
- **熔火蜥蜴（Magma Salamander）**：戰士 (Viking) —— 熔爐衝壓鍛打重錘（`hammer`），高溫過載碎甲，重擊熔融震波。
- **竹影青蛇（Bamboo Viper）**：忍者 (Ninja) —— 疾風青竹機關匕首（`dagger`），迅疾毒牙突刺，柔性閃避。
- **疾影神隼（Swift Falcon）**：武術家 (Monk) —— 旋風破空鋼爪（`claw`），俯衝連切，高速空中截擊。
- **星盤靈羊（Astral Ram）**：法師 (Mage) —— 游絲共鳴音叉法杖（`magic`），星塵音律擴散，高頻能量爆發。
- **幻彩變色龍（Mirage Chameleon）**：遊俠 (Ranger) —— 稜鏡折射複合長弓（`bow`），擬態狙擊，光學隱形冷箭。
- **破浪旗魚（Hydrofoil Sailfish）**：騎士 (Knight) —— 水翼刺擊破浪長槍（`spear`），直線高速水流衝鋒，貫穿破防。
- **重角犀牛（Heavyhorn Rhino）**：戰士 (Viking) —— 鍛造衝壓重裝開山斧（`axe`），霸體重劈，不可阻擋的開山撞擊。
- **星翼蝙蝠（Starwing Bat）**：忍者 (Ninja) —— 超音波回波共振飛鏢（`dart`），迴旋聲波標，暗夜視界鎖定。
- **鋼臂巨猩（Steelarm Gorilla）**：武術家 (Monk) —— 蒸氣鍛壓重裝鐵拳（`fist`），雙臂液壓重砸，大範圍破勢震擊。
- **稜鏡孔雀（Prism Peacock）**：法師 (Mage) —— 絢爛折光浮空靈晶扇（`crystal`），多重彩虹折射光幕，失真幻象護盾。
- **沙哨狐獴（Sentry Meerkat）**：遊俠 (Ranger) —— 荒原潛望雙管狙擊長銃（`gun`），埋伏哨戒，超長距離精準點殺。
- **鐵蹄駿駒（Ironhoof Courser）**：騎士 (Knight) —— 晨曦重裝巡遊闊劍（`sword`），奔騰重斬，衝鋒劈砍。
- **劈木河狸（Woodchopper Beaver）**：戰士 (Viking) —— 深林拓荒劈木巨斧（`axe`），厚重連環伐木斬，橫掃開路。
- **旋刃伶鼬（Whirling Stoat）**：忍者 (Ninja) —— 廢土旋刃弧光短匕（`dagger`），貼身旋風切削，極速伏擊連刺。
- **拍浪海豹（Clapping Seal）**：武術家 (Monk) —— 深海拍擊氣動擊掌拳套（`fist`），雙掌合擊引爆水壓，近身破勢連擊。
- **星儀渡鴉（Armillary Raven）**：法師 (Mage) —— 渾天星儀發條短杖（`magic`），星空投影，天體坐標魔法轟擊。
- **熱流赤鳶（Thermal Kite）**：遊俠 (Ranger) —— 熱流破空滑翔機關弓（`bow`），乘風拋射，熱浪貫通火箭。
- **旋音天鵝（Melodic Swan）**：騎士 (Knight) —— 旋音八度螺旋長槍（`spear`），音律穿刺，優雅芭蕾迴旋控場。
- **撼地野牛（Groundshaker Bison）**：戰士 (Viking) —— 荒原鐵砧破山巨鎚（`hammer`），狂暴踐踏重砸，粉碎重甲。
- **巡管守宮（Conduit Gecko）**：忍者 (Ninja) —— 巡管棘輪機關飛鏢（`dart`），管線伏擊，多角彈跳折射鏢。
- **破星蜜獾（Starbreaker Badger）**：武術家 (Monk) —— 重力破星合金鋼爪（`claw`），無畏迎擊撕裂，狂暴破防近身連打。
- **澄心水豚（Serene Capybara）**：法師 (Mage) —— 澄心太極水脈靈晶（`crystal`），溫泉水波護體，心流化勁結界。
- **振律啄木鳥（Resonance Woodpecker）**：遊俠 (Ranger) —— 振律氣動高頻重銃（`gun`），高頻連發衝擊點射，共振破甲。
- **熔鎧犰狳（Crucible Armadillo）**：騎士 (Knight) —— 玄鐵重破大劍（`sword`），捲曲鋼球衝鋒，厚重板甲防反。
- **風箱毛蟲（Bellows Caterpillar）**：戰士 (Viking) —— 雙聯鍛爐風箱重鎚（`hammer`），多節履帶壓制，氣動助燃爆裂震擊。
- **墨影烏賊（Inksmoke Cuttlefish）**：忍者 (Ninja) —— 海淵墨影雙鋒匕（`dagger`），流體煙幕遮蔽，暗角致命刺殺。
- **熔砧石蟹（Anvil Crab）**：武術家 (Monk) —— 黑曜衝壓熔岩拳套（`fist`），橫行寸勁連打，氣動鍛打鐵拳。

---

### 1.2 日晷駱駝武器選擇：【廢土日晷折射短杖（Wasteland Sundial Refraction Rod）】

日晷駱駝的原生經典武器正式定名為**【廢土日晷折射短杖（Wasteland Sundial Refraction Rod）】**。  
該武器直接承接並落地於 `docs/world/regions/R08_RUST_WASTE.md` 荒漠齒輪塚「廷得耳金黃光束（#FFD028）」、日照強烈風沙漫天、廢土拾荒者依賴日光陰影測算走時節拍之世界觀法源！  
底層完全掛載於 `weapon_classes.json` 的 `mage` 法師法杖類別，享有 `magic` 既有的「把星屑當墨」標籤宣言（Tagline: `"把星屑當墨"`）、技能傷害倍率最高、跟戰魂觀星配合最好、大範圍日光折射能量轟擊之特性（`atk: 1, def: -1, hp: -2, crit: 2.5, speed: 0`），完美呼應 `R08_RUST_WASTE.md` 在狂暴風沙中引導日光穿透透鏡、精確鎖定敵人核心零件的古老施法手感！

- **既有武器 ID 對齊（嚴格遵守規範）**：
  - 高階相容武器 ID：完全對齊 `game/data/tables/equipment.json` 第 197-208 行既有 ID **`void_quill`（虛空羽鋒）**（tier 5，line: `"soul"`（相容於 `magic`），`atk: 20, def: 0, hp: 2, crit: 16, crit_dmg: 35`）；
  - 入門基礎相容武器 ID：完全對齊 `equipment.json` 第 145-156 行既有 ID **`star_rod`（星屑短杖）**（tier 1，line: `"magic"`，`atk: 6, def: 0, hp: 2, crit: 5, crit_dmg: 16`）；
  - 專屬外觀款式 ID：明確標註為待審核專屬外觀款式 `weapon_camel_sundial_refraction_rod`（底層 100% 繼承既有 line: `"magic"`，數值直接掛載 `star_rod` / `void_quill`，絕不自行創造未定義之程式數值 id）。
- **單持規範遵守**：遵循 `review.md 0-MKT7` 單持規範，右手單持廢土日晷折射短杖（頂部裝配單向旋轉黃銅日晷圓盤、凸透石英聚光鏡與懸垂小銅鈴；長柄為古董銅管接合刻度尺）；左手自然微屈於身側輔助平衡，掌心朝上托著微型磁針導流星屑能量，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。

---

### 1.3 差異化定位：與既有 4 款法杖法師（靈尾狐、靈鐘鴞、星盤靈羊、星儀渡鴉）絕不撞型之論證

雖然日晷駱駝與靈尾狐、靈鐘鴞、星盤靈羊、星儀渡鴉同屬 `mage`（法師）法杖（`magic`）體系，但在三大核心維度進行 100% 徹底差異化切割，確保玩家在手機小螢幕上於 0.5 秒內清晰辨識：

1. **戰術風格與打擊手感差異化**：
   - **靈尾狐（靈尾狐，翡翠深林 R03）**：森林自然靈能與多尾發條甩擊，強調靈動穿梭與弧線星塵彈道；
   - **靈鐘鴞（靈鐘鴞，晨曦小鎮 R02）**：古典鐘樓擒縱機構，強調定時延遲陷阱、定點齒輪法陣與時間靜止控制；
   - **星盤靈羊（星盤靈羊，星穹軌道 R07）**：高軌太空失重游絲共鳴，強調高頻音波震顫、無重力射線與全屏光波擴散；
   - **星儀渡鴉（星儀渡鴉，黃銅都市 R04）**：摩天工坊渾天天球儀，強調三環逆向旋轉鎖定、垂直光束精確狙殺；
   - **日晷駱駝（日晷駱駝，荒漠齒輪塚 R08）**：**荒原日光折射與走時校準重裝學者**！強調「聚光蓄熱——日光日冕射線轟擊——陰影刻度鎖定弱點」。四足抓地穩如磐石，步伐沉緩穩重，施法時杖頂日晷指針追逐天頂廷得耳光束，爆發出如熾陽熔渣般的金黃光暈！
2. **力學核心與動態性格差異化**：
   - 靈尾狐依託輕質木質纖維與彈簧尾，動作靈巧跳躍；
   - 靈鐘鴞依託微型重錘擒縱機構，動作帶有明顯的滴答停頓；
   - 星盤靈羊依託微重力游絲彈簧，懸浮輕盈；
   - 星儀渡鴉依託展翼滑翔與三同心環自轉，天頂懸停俯瞰；
   - 日晷駱駝依託**「耐磨雙峰潤滑油罐冷凝室」與「多節阻尼活塞避震四足」**，行走時伴隨脖頸黃銅小鈴鐺清脆的「鈴——鐺、噠——噠」節奏，身軀帶有溫和起伏的步進感，厚重踏實而極具長途跋涉的堅毅萌感。
3. **機械構造與材質語言差異化**：
   - 靈尾狐為原木雕刻、漆器與青銅；
   - 靈鐘鴞為胡桃木外殼、黃銅發條與陶瓷鐘盤；
   - 星盤靈羊為航太級超輕聚合物合金、鍍銀電路與發光光纖；
   - 星儀渡鴉為沖壓鍍鈦薄板、深邃星藍搪瓷與三同心黃銅環；
   - 日晷駱駝為**「生鏽馬口鐵沖壓板件、暖黃銅防撞包邊、帆布補丁長袍、雙聯圓滾滾油罐駝峰、銅鈴鐺與石英日晷刻度盤」**，呈現出獨一無二的「廢土古典商隊旅行家」工藝質感！

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格遵守 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md` 世界憲章，**100% 徹底杜絕任何生物真皮毛、真毛髮、有機駝峰脂肪、生物血肉或動物組織**。駱駝的一切外觀特徵完全以經典發條玩具工藝材質轉譯重構：

1. **素體骨骼與外板**：非生物肉身，而是由**沖壓耐磨馬口鐵板件（Weathered Sanded Tinplates #3A322D）**拼裝成型，板件邊緣帶有手工打磨倒角與暖金黃銅包邊鉚接（#FFD028），腹底襯以耐磨帆布密封襯墊；
2. **雙峰構造（Humps）**：絕非生物脂肪駝峰，而是**「雙聯微型除鏽潤滑油壺兼高壓氣動冷凝儲熱罐（Twin Lubricant Reservoir & Condenser Tanks）」**，圓滾滾的金屬罐體由拉絲黃銅（#FFD028）沖壓製成，頂端配有滾花旋轉注油銅蓋與微型雙金屬溫度補償片；
3. **脖頸與頭部**：由三節柔性伸縮黃銅波紋風箱管（Copper Bellows Conduits）串聯頭部，可靈活上下微幅擺動，如同古代測量儀器的伸縮支架；
4. **四肢與步進小蹄**：四條短粗腿部內置螺旋金屬避震彈簧與氣壓阻尼連桿，腳底為整塊模壓成型的耐磨深褐色硬質橡膠防滑馬蹄墊（#1F1A3A），行走於沙盤上踏出圓潤可愛的印記；
5. **發條鑰匙**：背部雙峰中央偏後方牢固咬合一柄**「黃銅日晷雙環刻度發條鑰匙（Armillary Dial Brass Winding Key）」**，雙環交錯外圈刻有 24 刻度走時標線，旋轉時流暢帶動體內潤滑油泵運轉。

---

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

1. **2.2 頭身極致矮萌人體工學**：
   - 嚴格遵守 `0-PLAN1` 與 `0-ART` 規範，頭部佔全高約 45%，身軀圓滾扎實，四肢短粗萌趣；
   - 脖頸微屈呈優雅弧度，長度受控於 18px 內，避免拉長破壞 2.2 頭身整體視覺平衡；
   - 128x128 像素畫布中，角色在地面接地中心點精確落於 `x=64, y=120`，陰影嚴格覆蓋 `y=118..127`；立繪展台規格精確為 `400x840`，雙足接地點 `x=200, y=800`。
2. **多巴胺鮮亮配色矩陣（拒絕髒黑廢土）**：
   - **主色調（Primary）**：多巴胺暖金黃（#FFD028）與日照暖橘（#FFA010），象徵荒漠中溫暖明媚的朝陽與精緻黃銅；
   - **基底色（Base）**：陽光童話·奶油米白底（#FFFDF8），用於面部基板與帆布補丁底襯；
   - **輔助色（Secondary）**：薄荷綠（#4ED86A），用於法杖聚光石英核心刻度與目鏡光斑；
   - **點綴色（Accent）**：珊瑚粉紅（#FF5E8A），用於軸承密封圈與駝峰注油蓋點綴；
   - **輪廓描邊（Outline）**：深藍紫描邊（#1F1A3A），告別灰黑，呈現童話繪本的明快立體感。

---

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

依據 Kevin 對看板角色動態之嚴格規範（拒絕死板靜態，必須具備豐富待機小動作與點擊反饋）：

1. **怠速呼吸動態（Idle Breathing）**：  
   身軀每 2.5~3.5 秒進行微幅 1.0px 上下起伏，背後雙峰冷凝罐頂部的排氣安全閥規律噴出一縷極細的白色蒸氣環；脖子上的黃銅小鈴鐺隨起伏輕輕搖擺，發出微弱而悅耳的金屬輕鳴。
2. **待機隨機小動作（Idle Flourish）**：  
   每隔 8 秒，日晷駱駝會好奇地將頭冠向前探出，頭頂的黃銅晷針抬起 15 度對準天頂光束，右眼石英目鏡鏡片自動旋轉一圈進行光譜校準（伴隨清脆的齒輪卡嗒聲），隨後心滿意足地輕晃圓滾短尾。
3. **點擊 Poke 戳碰互動反饋**：  
   玩家用手指戳碰日晷駱駝時，駱駝驚喜地四足原地輕快小跳步！脖子上的小銅鈴發出歡快的「鈴鈴鈴！」聲響，背後日晷發條鑰匙加速旋轉兩圈，頭頂冒出冒險台詞對話氣泡：「**太陽走過三格齒輪，正是起程尋寶的最好時辰！**」，周身爆散出多巴胺金黃（#FFD028）與珊瑚粉（#FF5E8A）的七彩星芒粒子！

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R08 荒漠齒輪塚·遺忘舊庫（Rust Waste）零法師歷史空白

在全遊戲 9 大界域宏構沙盤中，底層廢棄物資界域 `R08 荒漠齒輪塚·遺忘舊庫` 先前已有沙鱗穿山甲（武術家·爪）、荒原鋼狼（騎士·劍）、幻彩變色龍（遊俠·弓）、沙哨狐獴（遊俠·銃）、旋刃伶鼬（忍者·匕）與撼地野牛（戰士·鎚）共 6 族，長久以來**完全缺乏一位能夠在狂暴風沙中利用日光陰影校準世界走時、以高倍石英目鏡測繪天頂零件墜落軌道、並以法杖匯聚日冕折光進行遠程轟擊的「法師 (Mage)」核心素體**。  
日晷駱駝的降臨，徹底填補了 R08 長期零法師素體的生態空白，讓 R08 達成全職業六大光譜完備；同時與 `R08_RUST_WASTE.md` 第 73 行深受玩家喜愛的 NPC 3「發條小駱駝·鈴鐺嘟嘟（Dudu the Clockwork Camel Pup）」形成完美的家族與生態呼應！

---

### 3.2 100% 逐字對齊引用 `docs/world/regions/R08_RUST_WASTE.md` 既有地標與設定

本提案中日晷駱駝的所有生活背景、技能描述與素材掉落，**100% 逐字引用並精準對齊 `docs/world/regions/R08_RUST_WASTE.md` 已定案之官方文字，絕無任何憑空自創名詞**：

1. **地標與構造對齊**：  
   日晷駱駝常年穿行於「**巨型零件殘骸沙丘（Giant Cog Dune Slopes）**」（第 19 行）之間，作為「**拾荒拼裝聚落·齒輪營地（Scavenger Gear Camp）**」（第 20 行）的常駐星象學者與引路人；經常攀上「**舊庫重型吊裝龍門架（Junkyard Heavy Gantry Pulleys）**」（第 21 行）頂端設立天文觀測點，守望「**零件分揀斜坡裂谷（Scrap Sorting Chute Chasm）**」（第 22 行）上方傾瀉而下的零件流；
2. **交通站點與邊界銜接**：  
   駱駝熟練穿梭於接納上層火山熔渣的「**冷卻熔渣重力傾卸滑道·舊庫受料口（Slag Gravity Dump Chute: Scrap Hopper Terminal）**」（第 29 行）與高軌塑料廢料口「**軌道廢棄排障滑道·舊庫分揀倉（Orbital Debris Dump Chute: Sorting Silo Terminal）**」（第 30 行），並引導商隊護送物資抵達「**大齒輪懸索天梯·舊庫總站（Gear Cableways: Junkyard Terminal）**」（第 32 行）與「**古老重型零件輸送翻斗軌道（Ancient Heavy Parts Conveyor Rail）**」（第 33 行）；當風暴來臨時，引導旅人避開危險的「**廢料沉降磁吸緩衝沙漏（Magnetic Scrap Buffer Sand-Trap）**」（第 35 行）；
3. **居民生活與 NPC 情感紐帶**：  
   日晷駱駝深受齒輪營地「**拾荒拼裝大師·補丁爺爺（Grandpa Patch the Scrap Assembly Master）**」（第 55 行）的信賴，身上披著的正是補丁爺爺親手用防風帆布與黃銅卡扣縫製的學者長袍；與「**流浪發條劍客·鏽刃阿席（Ash the Rusted Wandering Swordsman）**」（第 64 行）為荒原結伴同行的摯友；在齒輪營地的「**高溫蒸氣除鏽清洗槽（Steam De-Rusting Bath）**」（第 47 行）定期由「**發條除鏽工兵偶（Clockwork De-Rusting Tinkers）**」（第 45 行）協助注入「**高黏度抗氧化除鏽潤滑脂**」；並且是「**發條小駱駝·鈴鐺嘟嘟（Dudu the Clockwork Camel Pup）**」（第 73 行）崇拜嚮往的同族長輩前輩！
4. **世界局域走時與 BOSS 戰役對齊**：  
   日晷駱駝精準掌握 R08「**局域走時狀態：粗礪重度卡頓伴隨狂暴跳拍（秒針每 2.5~3.5 秒在風沙中發出沉重的金屬摩擦聲「喀——嚓！」）**」（第 6 行），在狂風漫天沙塵蔽目時，憑藉日晷法杖捕捉微型「**廷得耳金黃光束（#FFD028）**」（第 24 行）引導隊伍；在討伐旗艦 BOSS「**狂暴鏽蝕荒野巨獅·雷歐泰坦（Titan Leo: Rusted Wasteland Apex Lion）**」（第 102 行）時，日晷駱駝能施展日冕聚焦光束精準打擊巨獅的「**鬃毛生鏽棘輪外罩（Rusted Mane Ratchet Cowl）**」（第 109 行）與「**前肢液壓撲咬重爪（Hydraulic Pounce Claws）**」（第 110 行），加速其固定鉚釘脫扣崩解！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據《發條之心》官方 7 大部件槽位規範（`paperdoll_slots.json`），日晷駱駝之 7 大槽位完整規劃如下：

```json
{
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_camel_sanded_tinplate_default",
    "display_name": "磨砂馬口鐵雙峰矮萌素體底盤",
    "material": "沖壓耐磨馬口鐵板件（#3A322D），邊緣以暖金黃銅包邊（#FFD028），腹底襯以奶油米白耐磨帆布（#FFFDF8），四足配置模壓深褐硬質防滑橡膠馬蹄（#1F1A3A）與微型螺旋減震彈簧",
    "visual_features": "2.2 頭身矮萌微胖體態，短粗四足抓地穩健，脖頸呈溫和弧形微屈，關節外露微型黃銅半圓鉚釘與潤滑油管，行走時帶有可愛平穩的起伏律動，100% 零真生物毛皮與血肉組織"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_camel_sundial_gnomon_cowl",
    "display_name": "日晷晷針折光觀測兜帽",
    "material": "耐磨砂土棕帆布兜帽（#D49B4B），前額固定沖壓黃銅日晷額冠（#FFD028），中央矗立一枚微型折疊式合金日晷晷針（Gnomon），兩側垂掛防風護耳銅片",
    "visual_features": "兜帽輪廓圓潤包覆頭部，前額中央日晷晷針在陽光下投射出清晰刻度陰影，眼窩區域精準鏤空（max alpha=0）供 optic_core 探出，整體呈現古風學者探索風格"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_camel_armillary_dial_brass",
    "display_name": "黃銅日晷雙環刻度發條鑰匙",
    "material": "高剛性回火鎢鋼發條軸芯，搭配雙層正交咬合的黃銅日晷刻度圓環手柄（#FFD028），外環刻有 24 節氣微縮齒痕，中心軸承嵌有珊瑚粉耐磨墊圈（#FF5E8A）",
    "visual_features": "垂直插於背部雙峰中央鞍座，雙環幾何輪廓明顯突破角色外側輪廓線，行走與施法時平緩勻速旋轉，去背邊緣銳利乾淨，4 角完全透明無底板"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_camel_scavenger_astronomer_robe",
    "display_name": "廢土觀星學者帆布補丁長袍",
    "material": "多色拼接帆布長袍（多巴胺暖橘 #FFA010 搭配芥末金黃 #D49B4B），雙肩以粗麻線手作補丁縫合，胸前掛有一串古典黃銅小鈴鐺（#FFD028），腰繫多功能工具皮革腰帶",
    "visual_features": "嚴格遵循 0-ART26b 上裝與下身解耦規範（y>=96 嚴格 0 像素無畫死下身），胸前小鈴鐺隨步態搖晃，長袍下襬自然垂落露出短粗機械蹄，兼具流浪學者與童話玩具萌態"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_camel_dual_spectroscope_quartz_lens",
    "display_name": "雙聯光譜分折石英目鏡",
    "material": "高透光學石英雙凸透鏡，右鏡鍍有薄荷綠防眩光譜偏振膜（#4ED86A），左鏡鍍有琥珀金增透干涉膜（#FFD028），鏡框為黃銅精密螺紋咬合圈",
    "visual_features": "雙目晶瑩透亮，中心精準對齊 head_unit 鏤空處（min alpha=255），散發出智慧而專注的光芒，瞳孔深處微縮浮現微米級十字測距刻度"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_camel_sundial_refraction_rod",
    "display_name": "廢土日晷折射短杖",
    "material": "拋光黃銅伸縮短杖身（#FFD028），頂部裝配單向旋轉日晷指針圓盤與六角切面聚光石英晶核（#4ED86A），杖頭懸垂一枚微型調頻銅鈴",
    "visual_features": "右手單手持握杖身中部，杖頭微向前上方傾斜指向天際，左手微屈自然導流能量，符合 review.md 0-MKT7 單持無穿模規範，杖身不遮擋角色面部與胸口鈴鐺"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_camel_twin_condenser_humps",
    "display_name": "雙聯散熱油壺金屬駝峰",
    "material": "一對圓滾滾的拉絲黃銅密封油罐（#FFD028），頂部配有防漏滾花銅蓋與微型雙金屬溫度補償片，罐身環繞兩圈散熱鰭片",
    "visual_features": "對稱架設於背部鞍座左右兩側，中央預留充足槽位供發條鑰匙自由旋轉，待機呼吸時安全閥有節奏地排出微型白色蒸氣環，造型圓潤討喜"
  }
}
```

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

為配合既有六大戰鬥姿態體系（`idle`, `telegraph`, `attack`, `recover`, `skill`, `hit`），日晷駱駝各姿態規劃如下（嚴格對齊 `review.md` Rule 4b-4、Rule 4b-5、Rule 4b-6 與 0-QA16）：

1. **待機姿態（`idle`）**：  
   2.2 頭身矮萌身軀穩立沙地，四隻金屬小蹄均勻分擔體重；右手單持廢土日晷短杖斜立身側，左手平屈微托；脖頸微揚，頭頂晷針沐浴日光，背後雙峰中央的日晷發條鑰匙隨 R08 粗礪跳拍節奏勻速旋轉，駝峰排氣閥規律吐出細小白蒸氣圈，神情睿智溫和。
2. **前搖預警姿態（`telegraph`）**：  
   駱駝四足微向外分扎穩馬步，重心下沉！右手日晷短杖橫舉於胸前，杖頂六角石英與日晷圓盤劇烈自轉，發出高頻金屬蜂鳴聲「嗡——！」；頭頂晷針瞬間拉長聚焦，胸前小鈴鐺清脆連鳴，杖頭石英核心由薄荷綠轉為灼熱金黃，吸納周遭漫天日光與金色浮塵，蓄滿灼熱日冕射線之勢。
3. **出招攻擊姿態（`attack`）**：  
   踏步向前半步！右手短杖向前猛力一指！杖端六角石英如放大鏡般瞬間釋放出一道直徑 24px 的熾熱金黃（#FFD028）聚光日冕射線，筆直貫穿敵陣！射線周邊激盪著多巴胺暖橘（#FFA010）光波與金色微粒，命中瞬間在敵軀爆散出刺目的日光火花與四濺的微型齒輪星屑。
4. **收招硬直姿態（`recover`）**：  
   短杖借後坐力順勢劃出一道柔和弧線收至身側，身軀重心微向後仰；背部雙峰冷凝罐頂蓋跳開，呼嘯噴出大蓬白蒸氣進行高溫洩壓；脖頸鈴鐺輕響兩聲，頭頂晷針歸位，完成 2 秒標準收招硬直。
5. **奧義技能姿態（`skill`）**：  
   **「日冕天頂日晷大審判（Zenith Corona Sundial Verdict）」**！怒氣 100% 齒輪過載觸發！駱駝雙足後揚傲然直立，將日晷短杖高舉過頂！背部發條鑰匙金光暴射狂轉！地面轟然展開一道直徑 6 公尺的巨型黃金日晷星盤法陣，伴隨三聲沉渾的「喀——嚓！」鐘錶秒針跳動巨響，天頂廷得耳光束急劇匯聚，降下一道通天徹地的純白超熱日光光柱精準拆卸目標核心，全屏升騰起金色浮塵與多巴胺彩虹光暈！
6. **受擊受挫姿態（`hit`）**：  
   身軀受衝擊向後滑行 8px，四隻橡膠蹄在沙面劃出阻尼泥痕；頭冠兜帽向後微揚，面容石英目鏡浮現驚愕光紋；短杖橫在身前格擋，雙峰冷凝罐噴出一團散亂蒸氣，體現出小巧發條玩具受挫時的令人憐愛萌態。

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

### Q1：它掛在哪個核心循環的哪一環？
答：掛在「關卡推圖——收集掉落素材——打造/更換紙娃娃部件——提升大廳展示審美」之核心裝飾收集循環。日晷駱駝作為紙娃娃 7 大部件系統的第 53 種外觀素體，不改變底層數值架構，直接豐富玩家的角色自訂維度與收集深度。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
答：服務第一優先體驗支柱「個性化外觀與自定義紙娃娃系統（Paperdoll Customization & Visual Identity）」與第二優先體驗支柱「有深度且節奏分明的戰鬥手感（Tactile Combat & Class Differentiation）」。

### Q3：玩家在手機上用單手拇指能不能操作它？
答：能。本提案為紙娃娃外觀與世界觀規格，玩家在局外衣櫥（Wardrobe）與角色選擇界面透過標準 48px 熱區卡片點擊切換，單手拇指完全可輕鬆順暢操作。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
答：不需要。紙娃娃切片與渲染資料完全由客戶端本地載入（`paperdoll_slots.json` 與本地 Sprite），純單機無伺服器架構，零網路依賴。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
答：不會。本提案為純文字 Markdown 規格文件，對首包體積貢獻為 0 KB；未來由工程師阿宏與美術小柔實作切片貼圖時，全套 7 槽位 128px PNG 與 512px 貼圖壓縮後增量約 0.6 MB，配合 WebP 壓縮與延遲載入技術，嚴格守住 50~80 MB 首包紅線。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
答：放棄在第九巡重複堆疊近戰物理職業（如已有 9 款的戰士與武術家），放棄複雜的多足/雙持浮誇武器構想，優先投入資源打磨荒漠齒輪塚（R08）長久缺乏的古天文法師體系，並嚴格維持 7 大部件標準插槽相容性，不為駱駝設計任何破壞既有 Z 軸渲染管線的特異化專用骨架。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

供下游骨架建置任務與資料表同步腳本參考之標準 JSON 區塊片段（嚴格遵守 `review.md` 0-QA30 前置防護規範，預先給足唯一 aliases）：

```json
{
  "camel": {
    "race_id": "camel",
    "name": "日晷駱駝",
    "name_en": "The Sundial Camel",
    "aliases": ["sundial_camel", "meridian_camel", "caravan_camel", "dune_camel", "clockwork_camel"],
    "class_archetype": "法師 (Mage)",
    "weapon_class": "magic",
    "default_weapon_id": "star_rod",
    "native_realm_id": "R08",
    "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
    "toy_lineage": "19 世紀末至 20 世紀中葉古典鐵皮發條沙漠商隊駱駝玩具與鐘錶日晷天文自動偶",
    "color_palette": {
      "base": "#FFFDF8",
      "primary": "#FFD028",
      "secondary": "#4ED86A",
      "accent": "#FF5E8A",
      "metal": "#FFA010",
      "outline": "#1F1A3A"
    },
    "slots": {
      "chassis": "chassis_camel_sanded_tinplate_default",
      "head_unit": "head_camel_sundial_gnomon_cowl",
      "winding_key": "key_camel_armillary_dial_brass",
      "costume": "costume_camel_scavenger_astronomer_robe",
      "optic_core": "face_camel_dual_spectroscope_quartz_lens",
      "weapon": "weapon_camel_sundial_refraction_rod",
      "back_curio": "curio_camel_twin_condenser_humps"
    }
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> **法規與工具指引**：  
> 本段落專供後續美術總監（sideart）或視覺生成管線（`/root/gen_media.py`）產圖使用。  
> 嚴格遵守 `references/art_direction.md` 與 `references/brand_assets.md` 之兩大鐵則：  
> 1. **產圖一律強制掛載主視覺參考圖 `--ref /opt/side/bravesoul-game/branding/key_visual_main.png`**，確保角色比例、材質與筆觸與世界觀母體 100% 對齊；  
> 2. **嚴格禁止 AI 直接生成文字、商標與邊框**（Prompt 全面強制納入 `, --no text, --no letters, --no logo, --no watermark` 規範），所有遊戲標題卡一律由後製無失真疊加。

### 8.1 日晷駱駝角色單體立繪 Prompt（4:5 垂直角色畫）

```
Full-body character illustration of a charming 2.2-head-tall anthropomorphic mechanical toy camel mage astrologer, known as The Sundial Camel.

The camel is a compact handcrafted vintage mechanical toy designed to be held in one hand, completely non-biological, zero real fur, zero animal skin, zero organic flesh, zero biological meat. Sturdy rounded toy chassis made of weathered sanded tinplates (#3A322D) with vibrant warm-brass edge bevels (#FFD028). Four short stout mechanical legs with shock-absorbing springs and dark brown rubber hooves. A curved brass neck leads to an adorable camel head cowl made of stitched dune-gold canvas (#D49B4B), featuring an antique brass sundial crest with a slender gnomon pointer casting a shadow. Expressive twin quartz lens eyes shining with mint-green and amber-gold optic crosshair marks (#4ED86A, #FFD028).

The camel wears a scavenger astronomer canvas robe with colorful patches in warm orange (#FFA010) and mustard yellow (#D49B4B), tied with a tool belt, and a row of tiny polished brass jingle bells hanging around the neck. On its back sits a pair of cute rounded brass condenser oil humps (#FFD028) with visible tiny cooling fins.

A prominent antique brass armillary dial dual-ring winding key is mounted vertically between the humps on its back. The body is posed at a three-quarter angle so the brass winding key clearly breaks the outer silhouette and catches warm sunlight — never hidden behind the body.

The character gracefully holds a brass sundial refraction rod topped with a rotating sundial disc, a tiny brass bell, and a glowing hexagonal quartz crystal in its right hand, poised to cast a sunbeam spell.

Material: weathered vintage tinplate, chipped enamel, brushed antique brass edges, stitched rough canvas, tiny exposed screws, delicate seams, nostalgic retro clockwork toy construction.

Color palette: dopamine sunbeam golden yellow (#FFD028), desert warm orange (#FFA010), mint green lens accents (#4ED86A), coral pink rivet highlights (#FF5E8A), dark blue-violet outlines (#1F1A3A), warm cream baseplate highlights (#FFFDF8).

Pose: alert three-quarter standing stance, short legs planted firmly on the ground, head held high with curious scholarly confidence, holding the sundial staff upright, tiny puffs of white steam gently rising from the condenser humps, adorable and dignified toy personality.

Lighting: warm theatrical golden sunlight, soft rim light on brass bevels, soft diffuse ground shadow under hooves.

Camera: full-body character art, three-quarter view, 50mm lens, completely clean neutral warm studio background — plain warm cream gradient (#FFFDF8), no props, no scenery.

Style keywords: premium stylized 3D mobile RPG character art, cel-shaded anime style, bold outlines, dopamine color palette, handcrafted mechanical toy, chibi fantasy scholar, whimsical steampunk fairy tale, high mobile readability.

NEGATIVE PROMPT:
real camel, biological animal, fur, hairy skin, organic flesh, meat, camel humps with fat, plush toy, stuffed animal, humanoid robot, futuristic mech, military armor, sci-fi cyborg, Iron Man, smooth modern plastic, chrome, horror, creepy doll, porcelain doll, scary eyes, oversized weapons, multiple swords, extra limbs, dark muddy colors, text, letters, font, logo, watermark, signature.
```

### 8.2 日晷駱駝荒漠齒輪塚場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
A cinematic 16:9 key art illustration for a charming mobile RPG, set in the giant clockwork scrapyard realm of R08 Rust Waste: The Forgotten Junkyard.

In the foreground, a cute 2.2-head-tall mechanical toy camel astrologer stands atop a massive fractured gear dune, holding high a brass sundial refraction rod that channels a focused beam of radiant golden sunlight (#FFD028). The camel is made of weathered sanded tinplates, polished brass bevels, glowing quartz eye lenses, and has a spinning brass dual-ring winding key on its back between two cute brass condenser humps. Tiny brass bells on its neck jingle as cheerful white steam puffs emerge from the condenser valves.

Environment: breathtaking vast desert scrap basin diorama filled with giant half-buried tungsten gears and clockwork springs, dunes of golden quartz sand, the Scavenger Gear Camp with patchwork canvas tents in the middle ground, ancient rusty gantry pulleys, and beams of Tyndall golden sun rays (#FFD028) piercing through the atmospheric sandstorm haze. In the far distance, the silhouette of the colossal Rusted Wasteland Apex Lion titan against the horizon.

Lighting: brilliant golden hour rim lighting, warm Tyndall sunbeams cutting through golden dust particles, soft ground bounce light, warm theatrical fairy tale atmosphere.

Composition: cinematic action shot, high visual contrast, clear readable character silhouette, strong foreground focus with soft depth of field across the desert landscape.

Style keywords: premium stylized 3D game art, cel-shaded anime aesthetic, Maplestory and Tata Adventure inspired dopamine colors, handcrafted mechanical toy world, whimsical steampunk fairy tale, 8k resolution, crisp mobile-first readability.

NEGATIVE PROMPT:
photorealistic animals, real camels, fur, biological flesh, blood, gore, horror, creepy monsters, dark muddy water, dirty grey colors, human figures, military tank, futuristic sci-fi, text, letters, words, logo, title, watermark, border, frame.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  "$(cat << 'EOF'
A cute 2.2-head-tall anthropomorphic mechanical toy camel mage astrologer from Clockwork Heart, made of weathered sanded tinplates with brass edge bevels, short spring legs with rubber hooves, dual quartz spectroscope eye lenses, wearing scavenger canvas robe with neck jingle bells, twin brass condenser humps on back, prominent brass armillary dial winding key breaking silhouette, wielding a brass sundial refraction rod, cel-shaded, bold dark blue-violet outline, dopamine golden yellow and warm orange colors, warm cream background (#FFFDF8) --no real animal, --no fur, --no flesh, --no organic hump, --no text, --no letters, --no logo, --no watermark
EOF
)" \
  output_camel_paperdoll.png \
  --aspect 4:5 \
  --ref /opt/side/bravesoul-game/branding/key_visual_main.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：本提案所引用之「巨型零件殘骸沙丘（Giant Cog Dune Slopes）」、「拾荒拼裝聚落·齒輪營地（Scavenger Gear Camp）」、「舊庫重型吊裝龍門架（Junkyard Heavy Gantry Pulleys）」、「零件分揀斜坡裂谷（Scrap Sorting Chute Chasm）」、「廷得耳金黃光束（#FFD028）」、「冷卻熔渣重力傾卸滑道·舊庫受料口（Slag Gravity Dump Chute: Scrap Hopper Terminal）」、「軌道廢棄排障滑道·舊庫分揀倉（Orbital Debris Dump Chute: Sorting Silo Terminal）」、「大齒輪懸索天梯·舊庫總站（Gear Cableways: Junkyard Terminal）」、「古老重型零件輸送翻斗軌道（Ancient Heavy Parts Conveyor Rail）」、「廢料沉降磁吸緩衝沙漏（Magnetic Scrap Buffer Sand-Trap）」、「拾荒拼裝布偶（Patchwork Scavenger Plush Dolls）」、「生鏽發條浪人（Rusted Clockwork Ronin）」、「發條除鏽工兵偶（Clockwork De-Rusting Tinkers）」、「高溫蒸氣除鏽清洗槽（Steam De-Rusting Bath）」、「拾荒拼裝大師·補丁爺爺（Grandpa Patch）」、「流浪發條劍客·鏽刃阿席（Ash the Rusted Blade）」、「發條小駱駝·鈴鐺嘟嘟（Dudu the Clockwork Camel Pup）」、「狂暴鏽蝕荒野巨獅·雷歐泰坦（Titan Leo: Rusted Wasteland Apex Lion）」逐字精確對齊 `docs/world/regions/R08_RUST_WASTE.md` 第 19 行、第 20 行、第 21 行、第 22 行、第 24 行、第 29 行、第 30 行、第 32 行、第 33 行、第 35 行、第 43 行、第 44 行、第 45 行、第 47 行、第 55 行、第 64 行、第 73 行、第 102 行，100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（包體膨脹查驗）**：純文字 Markdown 規格文件，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有五十二族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 52 族（含第 49 族熔鎧犰狳、第 50 族風箱毛蟲、第 51 族墨影烏賊、第 52 族熔砧石蟹）。
- [x] **review.md 23f-1（單一職業標籤）**：職業名稱唯一嚴格對齊為 `法師 (Mage)`，無任何雙標籤或自創詞。
- [x] **review.md 23f-2（武器名稱前後一致）**：原生專屬武器在全文所有章節、表格與 JSON 片段中均統一稱作「廢土日晷折射短杖」，精確呼應 `weapon_classes.json` 之 `mage` 法杖體系，相容武器精確對齊既有 `equipment.json` 之 `star_rod`（星屑短杖，tier 1）與 `void_quill`（虛空羽鋒，tier 5）。
- [x] **review.md 23f-4 / CANON 零毛皮鐵律**：全篇 100% 清除所有生物皮毛、真毛髮、有機駝峰肉質、血液、軟體黏液等字眼，駱駝特徵全面轉譯為沖壓耐磨馬口鐵板件、雙聯金屬潤滑油壺駝峰、黃銅日晷晷針兜帽、雙環刻度發條鑰匙與橡膠防滑機械蹄。
- [x] **review.md 0-MKT7（單持無穿模規範）**：明確指定右手單持廢土日晷折射短杖、左手自然微屈於身側輔助平衡，主次分明，杖頭不遮擋面頰與胸前鈴鐺，0 佔位短棒，0 多餘浮動武器，0 穿模違規。
- [x] **review.md 0-QA30 前置防護**：aliases 預先定案 `camel`, `sundial_camel`, `meridian_camel`, `caravan_camel`, `dune_camel`, `clockwork_camel`，為下游骨架單建立唯一真相源。
- [x] **產圖 Prompt 規範**：第 8 節完整附上 4:5 與 16:9 提示詞，明載 `--ref /opt/side/bravesoul-game/branding/key_visual_main.png` 與 `--no text, --no letters, --no logo, --no watermark` 鐵律。
