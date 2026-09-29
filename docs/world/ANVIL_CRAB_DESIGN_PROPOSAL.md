# 第五十二種動物「熔砧石蟹（The Anvil Crab）」世界觀與角色設計提案

> **標題**：第五十二種動物「熔砧石蟹（The Anvil Crab）」角色與世界觀設計提案  
> **提案代號**：`ANVIL_CRAB_DESIGN_PROPOSAL`（代號：`crab` / 識別名：`race_crab`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_16f22173`（📖 世界觀｜第五十二種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零真甲殼生物組織、零生物血肉、零軟組織、零生物黏液、高耐熱粗獷鑄鐵板件、黑曜石淬火耐火磚、金色液態流光鐵水池、氣動洩壓雙聯閥門、外露螺栓鉚釘、背後必有發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調）  
> - `docs/world/regions/R06_MOLTEN_FOUNDRY.md`（第 1 行區域代號與名稱「R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano」、第 4 行「高耐熱粗獷鑄鐵板件、黑曜石淬火耐火磚、金色液態流光鐵水池、重型鍛打氣動連桿與高壓黃銅洩壓儀表套件」、第 6 行「局域走時狀態：齒輪超頻過載伴隨重錘敲擊律動（秒針每 1.5 秒急促跳動一格，伴隨重型鐵砧沉重打擊聲「鏘——噹！」；高溫熱浪引發發條金屬微幅熱脹，需精準掌握過載散熱節奏穿行）」、第 19 行「金色液態鐵水熔池（Golden Molten Iron Basins）」、第 20 行「黑曜淬火石磚步道（Obsidian Quenched Brick Walkways）」與「耐火排煙管樹（Furnace Flue Trees）」、第 21 行「重型鍛造工坊與衝壓懸橋（Heavy Forging Foundries & Stamping Bridges）」、第 22 行「黃銅洩壓儀表塔（Brass Pressure-Gauge Clocktowers）」、第 30 行「晨曦天軌 6 號熔爐重載貨運月台（Dawn Rail Heavy Freight Platform 6）」、第 32 行「高壓地熱噴射升空彈射井（Geothermal Ejection Launch Silo）」與「火山口中央鍛造神壇（Central Crucible Forge Altar）」、第 33 行「冷卻熔渣重力排料傾卸滑道（Slag Gravity Dump Chute）」、第 35 行「磁吸隔熱排渣護欄網（Magnetic Slag-Retention Grid）」、第 47 行「淬火冷卻噴淋池（Quenching Shower Station）」、第 55 行「矮人鐵匠大師·重錘布隆（Master Smith Bronn the Heavy Hammer Dwarf）」、第 65 行「陶土魔像學徒·黏土泥泥（Clay Clay the Terracotta Apprentice）」、第 73 行「熔爐溫控長老·坩堝老爹（Papa Crucible the Foundry Elder）」、第 101 行及第 238 行「黑曜石淬火神壇（Obsidian Quenched Great Anvil）」、第 101 行及第 242 行旗艦泰坦 BOSS「熔爐泰坦·重裝巨型石拳鐵豕（Titan Crucible: Iron-Tusk the Stone-Fist Boar）」、第 243 行「玄鐵石拳（Stone-Fist Hammer）」、第 244 行「背部洩壓煙囪」、第 245 行「黑曜獠牙面罩」、第 252 行特產武器「玄鐵重破大劍」、第 253 行「熔爐衝壓巨錘」、第 254 行「熱浪合金重銃」、第 255 行代表素材「玄鐵精煉鑄錠」、第 256 行「耐高溫合金彈簧」、第 257 行代表素材「熔岩黑曜石拳板（Obsidian Punch Plate）」、第 258 行「耐火石墨潤滑膏」、第 259 行「七煞星軸（銳齒之魂 / Razor Tooth Core）」、第 260 行「廉貞星軸（銳齒之魂 / Razor Tooth Core）」、第 261 行「崩山衝壓擊（Mountain-Shattering Stamping Strike）」、第 262 行「熱浪爆碎震（Thermal Shockwave Eruption）」、第 263 行「高溫過熱淬火窗口（Thermal Overheat & Quenching Window）」、第 264 行「氣動衝壓地熱氣流（Pneumatic Stamping & Thermal Updraft）」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（武術家正式名稱 `monk`，拳套標籤宣言 `\"破勢在勤\"`，武器 `fist`，數值 `atk: 1, def: 1, hp: 4, crit: 1.5, speed: 2`，玩法 `\"貼上去連打。同職也可玩爪。\"`，新手武器 `wrap_gloves`）  
> - `game/data/tables/equipment.json`（拳套正式 line: `\"fist\"`，初階武器：第 211 行 `wrap_gloves` 練拳綁帶，高階相容武器：第 224 行 `iron_knuckle` 鐵節拳套）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第九巡（第 49~54 族）第四順位核心擴充，強勢接棒「武術家 (Monk)」拳套體系重大擴充**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第五十二種動物擴充素體規格**。  
   在全專案跨越「前 48 族完全對稱平衡大圓滿」，並相繼由第 49 族熔鎧犰狳（騎士·長劍）、第 50 族風箱毛蟲（戰士·戰鎚）與第 51 族墨影烏賊（忍者·短匕）成功開啟第九巡全新篇章後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第九巡第四順位**，輪轉進入最具近身連打、破勢極致與熱血反差的核心職業——**武術家 (Monk)** 體系，原生武器掛載於**拳套（`fist` / 武術家·拳）**。  
   熔砧石蟹的加入，使全遊戲武術家拳套素體擴充至第 5 款（武術家總族群擴充至 9 款），完美對稱接棒第九巡前三順位，為第九巡注入極具工業重擊與橫行破勢的硬核動能！
2. **經典玩具起源與古典機械發條橫行拳擊蟹自動機工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與鐘錶氣動鍛打自動偶史上的經典工藝原型：  
     ① **19 世紀末至 20 世紀中葉古典鐵皮發條橫行拳擊蟹玩具（Vintage Tinplate Wind-up Brawling Boxer Crab Automaton / Lehmann & Schuco Tin Crab Toy）**，通體由沖壓粗獷鑄鐵薄板、雙偏心輪橫行連桿機構與黑曜石受力面咬合而成，內部發條帶動側向小碎步快速位移與雙拳高頻交替出擊，是古典發條玩具史上最具反差萌趣與機械步進魅力的自動偶之一；  
     ② **古典鐘錶高溫氣動鐵砧機關偶（Horological Pneumatic Forge Anvil Automaton）**，腹腔內置微型氣壓連桿與齒輪活塞，在指針跳動間隙吸納熔爐熱浪、於出拳瞬間噴發高壓洩壓蒸氣，將鍛爐打鐵時「鏘——噹！」的重擊節奏轉化為連續爆破的寸勁衝壓拳；  
     ③ **古典發條鍛造工兵偶（Vintage Clockwork Foundry Sapper Automaton）**，以 2.2 頭身扁圓堅固的鑄鐵拱形甲殼、耐火石磚包角胸甲、外露黃銅散熱鉚釘與多節防滑機械足，完美詮釋武術家職業「出手快、架勢散得快、近身連打破勢、破勢在勤」之武道之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「高耐熱鑄鐵矮萌甲殼底盤、雙向潛望測距護額頭盔、四葉散熱鍛造發條鑰匙、熔爐工兵重裝石磚胸甲、雙聯壓力儀表石英凸透鏡、黑曜衝壓熔岩拳套與雙聯氣動洩壓排煙煙囪」之重工拳擊武術家素體（Cast-Iron Molten Chassis, Periscope Visor Cowl, Quad-Flue Anvil Key, Furnace Sapper Cuirass, Dual-Gauge Quartz Lens, Obsidian Magma Stamping Gauntlets & Pneumatic Exhaust Chimneys）**。
3. **生態補足：徹底終結赤焰熔爐·鍛造火山（R06）零武術家之歷史空白，打造熔爐鍛造神壇第一重裝鐵拳**：  
   在全遊戲 9 大界域中，中層高溫冶煉沙盤界域 `R06 赤焰熔爐·鍛造火山` 先前擁有熔火蜥蜴（戰士·鎚）、重角犀牛（戰士·斧）、熱流赤鳶（遊俠·弓）與熔鎧犰狳（騎士·劍）共 4 族。  
   長久以來，面對火山口翻滾的鐵水熔池與高頻落下的衝壓重錘，**該界域完全缺乏一位能夠耐受金色鐵水高溫噴濺、借助橫行步法靈巧穿梭於衝壓懸橋之間、並以黑曜石衝壓拳板砸碎卡死熔渣的「武術家 (Monk)」核心素體**。熔砧石蟹的誕生，使 R06 界域的職業生態迎來首位近身連打破勢宗師，與蜥蜴的重鎚、犀牛的開山斧、赤鳶的制空弓以及犰狳的防禦劍共同組成赤焰火山堅不可摧的五位一體陣線！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：熔砧石蟹素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十一族武器與職業光譜全盤點

盤點現有首發五族與前四十六款擴充族（總計 51 族）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **墨影烏賊（The Inksmoke Cuttlefish）**：忍者 (Ninja) —— 海淵墨影雙鋒匕（`dagger`），深海高壓氣動微泡煙幕，流體匿影死線刺殺。

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 武術家（Monk）此前在 51 族中擁有 8 款動物素體（拳套 4 款、機關爪 4 款）；
- **本提案第五十二種動物正式作為「第九巡第四順位」接棒啟動擴充，歸屬於武術家 (Monk) 體系，原生武器掛載於 `fist`（拳套 / 武術家·拳）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`武術家 (Monk)`**；
- 熔砧石蟹的加入，使全遊戲武術家拳套素體擴充至第 5 款，為第九巡打造最極致的熔爐近身連打與崩山破勢體系！

### 1.2 熔砧石蟹武器選擇：【黑曜衝壓熔岩拳套（Obsidian Stamping Magma Gauntlets）】

熔砧石蟹原生專屬武器定名為：**【黑曜衝壓熔岩拳套（Obsidian Stamping Magma Gauntlets）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 赤焰熔爐·鍛造火山之高溫黑曜石衝壓體系**！  
底層完全掛載於 `weapon_classes.json` 的 `fist`（武術家·拳）類別，享有 `fist` 既有的「破勢在勤」標籤宣言（Tagline: `\"破勢在勤\"`）、出手快、架勢散得快、對付木人樁破勢順暢、貼上去連打之特性（`atk: 1, def: 1, hp: 4, crit: 1.5, speed: 2`），完美呼應 `R06_MOLTEN_FOUNDRY.md` 第 6 行「秒針每 1.5 秒急促跳動一格，伴隨重型鐵砧沉重打擊聲鏘——噹！」之鍛造打擊節奏！

- **法源素材咬合**：  
  完全對應 `R06_MOLTEN_FOUNDRY.md` 第 257 行官方代表素材**「熔岩黑曜石拳板（Obsidian Punch Plate）」**、第 243 行拆卸部位**「玄鐵石拳（Stone-Fist Hammer）」**與第 261 行核心招式**「崩山衝壓擊（Mountain-Shattering Stamping Strike）」**，將火山口鍛造熱能轉化為高頻連打動能。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"fist\"` 的初階裝備 `wrap_gloves`（練拳綁帶，tier 1）與高階相容裝備 `iron_knuckle`（鐵節拳套，tier 3），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款拳套武術家（瓷韻熊貓、鐵拳袋鼠、鋼臂巨猩、拍浪海豹）絕不撞型之論證

雖然熔砧石蟹與瓷韻熊貓、鐵拳袋鼠、鋼臂巨猩、拍浪海豹同屬 `monk`（武術家）拳套（`fist`）體系，但在**拳法流派與破勢哲學**、**機動體態與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               武術家職業拳套系五族差異化對照表（熊貓 vs 袋鼠 vs 巨猩 vs 海豹 vs 石蟹）                                │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 瓷韻熊貓 (Panda)     │ 鐵拳袋鼠 (Kangaroo)  │ 鋼臂巨猩 (Gorilla)   │ 拍浪海豹 (Seal)      │ 熔砧石蟹 (Crab)     │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 拳理與流派   │ 乾坤太極動靜化勁     │ 西洋擂台彈簧活塞刺拳 │ 高壓蒸氣重鍛鐵壁重拳 │ 深海流體對拍推手     │ 熔爐鐵砧高頻衝壓崩山 │
│ 2. 動能來源     │ 陶瓷發條游絲化勁     │ 雙足螺旋彈簧回彈勢能 │ 鍋爐蒸氣陣發超壓衝擊 │ 洋流浮力磁阻阻尼     │ 地熱氣動衝壓與黑曜熱 │
│ 3. 步法特徵     │ 圓弧沉步、以柔克剛   │ 單向直線彈跳、進退快 │ 沉重前壓、正面推進   │ 水流滑行、拍浪旋轉   │ 橫行碎步、側向低姿閃 │
│ 4. 武器構造     │ 陶瓷外殼太極拳套     │ 黃銅衝壓活塞拳套     │ 重型鎢鋼蒸氣鍛打拳套 │ 琉璃耐壓深海雙鰭拳套 │ 黑曜石淬火衝壓熔岩拳 │
│ 5. 主題界域     │ R09 竹影林·天元道場  │ R04 黃銅都市·巨輪城  │ R04 黃銅都市·巨輪城  │ R05 琉璃汪洋·發條海淵 │ R06 赤焰熔爐·鍛造火山 │
│ 6. 材質質感     │ 溫潤白瓷、竹木生漆   │ 暖金黃銅、浸油皮革   │ 灰黑生鐵、蒸氣管網   │ 海藍琉璃、鍍鈦合金   │ 粗獷鑄鐵、黑曜淬火石 │
│ 7. 角色剪影     │ 圓滾黑白國寶熊貓     │ 長耳高挑跳躍拳擊手   │ 寬肩巨臂重型泰山體態 │ 圓錐流線深海鰭狀體態 │ 扁圓拱頂橫行多足矮萌 │
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格恪守 `docs/world/CANON.md` 憲章世界觀「**100% 零真動物生物肉身、零毛皮、零羽毛、零真甲殼有機質、零血肉黏液**」之鐵律：

- **粗獷鑄鐵與黑曜淬火石磚甲殼**：熔砧石蟹的甲殼並非生物幾何甲殼，而是由重工業鍛造火山中常見的**沖壓高耐熱粗獷鑄鐵板件（#2A272A）**與**黑曜石淬火耐火磚（#1F1A3A）**鉸接而成。板件邊緣帶有高溫淬火留下的金紅漸變灼痕，四角固定有外露的黃銅平頭固定螺栓（#FFD028），呈現沉穩堅固的玩具質感。
- **雙向潛望測距護額頭盔**：頭部為沖壓成型的半圓形鑄鐵護額，頂部探出兩根微型黃銅潛望式石英測距目鏡管。目鏡可獨立旋轉 360 度，內部鑲嵌高折射琥珀金黃透鏡，活潑靈動，展現蟹類玩具特有的探頭張望趣味。
- **雙聯氣動排煙煙囪**：背部兩側裝配一對小型直立鑄鐵洩壓煙囪，頂部帶有微型黃銅配重防雨閥蓋，隨呼吸節奏規律開合，排出微量淡白蒸氣煙圈（無任何有害廢氣，純童話發條蒸氣）。
- **側向多節機械步進足**：兩側各有三對微型多節同軸合金步進滾足，末端包覆高摩擦防滑耐磨黑色橡膠底墊，使石蟹在滾燙石磚與鐵軌上橫行時穩定抓地，踩出清脆明快的「踏、踏、踏」金屬節奏。
- **背後發條鑰匙**：背部中央正上方垂直挺立著一把經典的**四葉散熱鍛造發條鑰匙（Quad-Flue Anvil Key）**。主軸由耐高溫淬火鎢鋼精鍛而成，四片旋葉開有對稱圓孔，旋轉時流暢均勻，在 45 度視角下清晰打破角色剪影，絕不被甲殼或背部奇物遮擋。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

對齊 Kevin 規範之「**2.2 頭身矮萌比例、楓之谷 × 塔塔冒險多巴胺鮮亮高飽和色盤**」，拒絕泥土髒灰與辦公室 PPT 暗沉感：

- **頭身比例**：整體高寬比接近 1:1.15，矮萌微胖，橫向擴展的圓弧甲殼賦予其極強的重心穩定感與玩具鈍感萌態。
- **多巴胺多色協調**：
  - **基底底盤（Baseplate）**：奶油米白（#FFFDF8）襯墊與精磨耐熱耐火石磚；
  - **核心主色（Primary）**：赤焰暖橘（#FFA010）與熔岩金黃（#FFD028）高溫警示漆面，明亮活潑；
  - **輔助色（Secondary）**：薄荷淺綠（#4ED86A）石英儀表刻度與高光洩壓指示；
  - **點綴提亮（Accent）**：珊瑚粉（#FF5E8A）高溫預警鉚釘與關節轉軸密封圈；
  - **金屬質感（Metal）**：高光金黃（#FFD028）鍛造黃銅發條鑰匙與齒輪連桿；
  - **外框描邊（Outline）**：深藍紫（#1F1A3A）深邃粗描邊（2~3px），勾勒出極度清晰的手遊邊緣。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

- **待機小動作（Idle Micro-Action）**：  
  每隔 3 秒，石蟹身軀會伴隨發條走時律動進行微幅左右重心交替（蟹行踏步）；頂部的兩根黃銅潛望目鏡隨機朝不同方向輕輕轉動並一伸一縮；雙拳在胸前微幅碰擊，發出輕微而悅耳的「叮——」打鐵金屬音，背部煙囪隨之噗出一朵微型蒸氣小花。
- **點擊戳碰互動（Poke Interaction）**：  
  當玩家在手機大廳或衣櫥界面點擊石蟹時，石蟹會立刻向側向疾步滑行半步，擺出經典的「橫行防禦拳架」！雙手黑曜石拳套在身前重重對撞，迸發出一圈彩糖般的金色星芒粒子（#FFD028, #FFA010）；頭頂跳出俏皮對話氣泡：**「鍛鐵趁熱，出拳要勤！看我的崩山衝壓！」**

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R06 赤焰熔爐·鍛造火山（Molten Foundry）零武術家歷史空白

在全遊戲 9 大界域中，中層高溫冶煉沙盤界域 `R06 赤焰熔爐·鍛造火山` 先前已有熔火蜥蜴（戰士·鎚）、重角犀牛（戰士·斧）、熱流赤鳶（遊俠·弓）與熔鎧犰狳（騎士·劍）共 4 族。  
長久以來，面對火山口翻滾的鐵水熔池與高頻落下的衝壓重錘，**該界域完全缺乏一位能夠耐受金色鐵水高溫噴濺、借助橫行步法靈巧穿梭於衝壓懸橋之間、並以黑曜石衝壓拳板砸碎卡死熔渣的「武術家 (Monk)」素體**。熔砧石蟹的誕生，使 R06 界域的職業生態迎來首位近身連打破勢宗師，與蜥蜴的重鎚、犀牛的開山斧、赤鳶的制空弓以及犰狳的防禦劍共同組成赤焰火山堅不可摧的五位一體陣線！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 既有地標與設定

熔砧石蟹在赤焰熔爐的世界觀錨點，緊密穿插於以下既有官方地標、設施與 NPC 之中（逐字精確對齊 `R06_MOLTEN_FOUNDRY.md`，100% 存在，無任何捏造詞彙）：

1. **核心地標與工藝巡邏線**：  
   - 熔砧石蟹一族常年活躍於**「重型鍛造工坊與衝壓懸橋（Heavy Forging Foundries & Stamping Bridges）」**（第 21 行）周邊，利用低重心橫行步態在震顫劇烈的懸橋鋼樑上健步如飛；  
   - 牠們駐足於高溫灼熱的**「黑曜淬火石磚步道（Obsidian Quenched Brick Walkways）」**（第 20 行），雙拳沾取熔渣修補磚面接縫；  
   - 牠們嬉戲於閃爍金光的**「金色液態鐵水熔池（Golden Molten Iron Basins）」**（第 19 行）池畔，以高耐熱鑄鐵甲殼汲取鐵水熱能為腹腔發條蓄能；  
   - 牠們棲息於高聳林立的**「耐火排煙管樹（Furnace Flue Trees）」**（第 20 行）樹根齒輪座下方，清理堆積的碳化金屬碎屑；  
   - 在高聳入雲的**「黃銅洩壓儀表塔（Brass Pressure-Gauge Clocktowers）」**（第 22 行）指針跳動間隙，石蟹武者們聆聽每 1.5 秒急促跳動一格的齒輪律動，將拳法節奏精準校準至毫秒級；  
   - 牠們也是火山口核心**「黑曜石淬火神壇（Obsidian Quenched Great Anvil）」**（第 101/238 行）與**「火山口中央鍛造神壇（Central Crucible Forge Altar）」**（第 32 行）的常駐演武者，以拳套直接承受神壇落下的衝壓考驗。
2. **交通設施與物料排卸協防**：  
   - 石蟹一族負責引導通往火山頂層的**「高壓地熱噴射升空彈射井（Geothermal Ejection Launch Silo）」**（第 32 行）物料運輸，以強硬甲殼抵擋升空時的碎石衝擊；  
   - 定期巡查由火山斜坡直通底層廢土的**「冷卻熔渣重力排料傾卸滑道（Slag Gravity Dump Chute）」**（第 33 行），用黑曜拳套砸碎卡塞在滑道喉口的凝固鋼渣塊；  
   - 守護外圍安全邊界**「磁吸隔熱排渣護欄網（Magnetic Slag-Retention Grid）」**（第 35 行），防止暴走金屬殘渣翻出沙盤；  
   - 引導自 R02 駛抵**「晨曦天軌 6 號熔爐重載貨運月台（Dawn Rail Heavy Freight Platform 6）」**（第 30 行）的重型貨運列車，協助搬卸沉重的金屬原礦。
3. **友好 NPC 互動羈絆**：  
   - 與首席鐵匠**「矮人鐵匠大師·重錘布隆（Master Smith Bronn the Heavy Hammer Dwarf）」**（第 55/249 行）是最佳打鐵搭檔。布隆手持巨鎚鍛造大件，石蟹則以雙拳快攻為工件進行「千層高頻密實打褶」，被布隆親切稱為「火山最可靠的四爪副鍛手」；  
   - 與**「陶土魔像學徒·黏土泥泥（Clay Clay the Terracotta Apprentice）」**（第 65/250 行）是打鬧玩伴，常在**「淬火冷卻噴淋池（Quenching Shower Station）」**（第 47 行）旁比試耐熱拔河，石蟹指導泥泥如何利用低重心抗衡衝擊力；  
   - 經常向**「熔爐溫控長老·坩堝老爹（Papa Crucible the Foundry Elder）」**（第 73/251 行）請教熱力平衡心法，藉長老調配的耐火石墨潤滑膏保養全身球窩關節。
4. **與旗艦泰坦 BOSS「石拳鐵豕」的武道對峙**：  
   - 面對火山口狂暴失控的超巨型守衛泰坦**「熔爐泰坦·重裝巨型石拳鐵豕（Titan Crucible: Iron-Tusk the Stone-Fist Boar）」**（第 101/242 行），熔砧石蟹因同具重拳武道底蘊，完全洞悉其揮拳慣性；  
   - 當主角小白挑戰泰坦時，石蟹作為破勢戰術總教頭，指點小白如何把握**「高溫過熱淬火窗口（Thermal Overheat & Quenching Window）」**（第 263 行）的 1.2 秒過熱定格機會，利用**「氣動衝壓地熱氣流（Pneumatic Stamping & Thermal Updraft）」**（第 264 行）躍上泰坦肩膀，精準拆卸三大要害：**「玄鐵石拳（Stone-Fist Hammer）」**（第 243 行）、**「背部洩壓煙囪（Back Crucible Vents）」**（第 244 行）與**「黑曜獠牙面罩（Obsidian Tusks & Visor）」**（第 245 行），粉碎泰坦的狂暴核心！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據《發條之心》官方 7 大部件槽位規範（`paperdoll_slots.json`），熔砧石蟹之 7 大槽位完整規劃如下：

```json
{
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_crab_molten_iron_default",
    "display_name": "鑄鐵鍛爐矮萌甲殼素體底盤",
    "material": "沖壓粗獷鑄鐵板件（#2A272A），邊緣帶有高溫淬火金黃灼痕（#FFD028），腹底襯以象牙白耐火陶瓷釉板（#FFFDF8），下身配置三對同軸黃銅步進滾足與耐磨橡膠防滑爪",
    "visual_features": "2.2 頭身矮萌微胖體態，重心極低，接縫外露粗大黃銅半圓鉚釘，側向六足整齊排列帶有彈性連桿，步態輕快可愛，無任何生物黏液或有機甲殼"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_crab_periscope_visor_cowl",
    "display_name": "雙向潛望測距護額頭盔",
    "material": "沖壓厚鑄生鐵護額拱蓋（#2A272A），外漆赤焰暖橘高溫防銹漆（#FFA010），頂部伸出一對雙向旋轉黃銅潛望式石英測距筒（#FFD028）",
    "visual_features": "扁圓弧形盔頂剪影，中央眼窩區域精準鏤空（max alpha=0）供 optic_core 探出，兩側各有一枚小型洩壓散熱孔，微縮探頭靈活俏皮"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_crab_quad_flue_crucible_t_bar",
    "display_name": "四葉散熱鍛造發條鑰匙",
    "material": "高剛性鍛造淬火鎢鋼主軸，搭配帶有對稱減重孔的四葉扁平十字黃銅旋葉（#FFD028），中心鑲嵌珊瑚粉耐磨軸承鉚釘（#FF5E8A）",
    "visual_features": "背部中央偏上方垂直插入，四葉幾何輪廓鮮明突破角色外廓，旋轉時勻速流暢，去背邊緣銳利乾淨，4 角完全透明無底板"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_crab_furnace_sapper_cuirass",
    "display_name": "熔爐工兵重裝石磚胸甲",
    "material": "深黑曜石淬火磚紋胸甲（#1F1A3A），邊緣鑲以高飽和赤焰暖橘防撞條（#FFA010），胸前以黃銅鍛造鉚釘鎖固，肩部配有厚實石棉耐火肩墊",
    "visual_features": "嚴格遵循 0-ART26b 上裝與下身解耦規範（y>=96 嚴格 0 像素無畫死下身），胸口中央嵌有重型金屬鐵砧浮雕徽記，厚重扎實兼具童話工兵萌態"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_crab_dual_gauge_convex_lens",
    "display_name": "雙聯壓力儀表石英凸透鏡",
    "material": "高透耐高溫石英雙凸透鏡，表面鍍有黃金防眩反光干涉膜（#FFD028），內部刻有薄荷綠壓力刻度光柵與微型指針（#4ED86A）",
    "visual_features": "鏡片中心精準對齊 head_unit 潛望鏡筒鏤空處（min alpha=255），散發出溫暖明亮的金黃光芒，隨情緒微調光芒明暗度"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_crab_obsidian_stamping_fist",
    "display_name": "黑曜衝壓熔岩拳套",
    "material": "雙手重裝黑曜石鍛造拳套（#1F1A3A），拳面嵌裝耐熱黑曜石厚受力板（#FFA010 熔岩流光凹槽），背部配有微型黃銅氣動洩壓衝壓閥（#FFD028）",
    "visual_features": "右手單手持握主拳套向前高舉護面、左手副拳套微屈收於腰側蓄勢，符合 review.md 0-MKT7 單持/成對主次分明無穿模規範，拳面不擋臉"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_crab_pneumatic_exhaust_chimney",
    "display_name": "雙聯氣動洩壓排煙煙囪",
    "material": "一對對稱直立的沖壓生鐵小型排煙管（#2A272A），管口配備活動式薄銅洩壓蓋板（#FFD028），底部連接細密散熱格柵",
    "visual_features": "牢固架設於甲殼背側左右兩端，中央預留充足空間避開發條鑰匙旋轉軌跡，戰鬥出拳時有節律地噴出微型白色蒸氣環"
  }
}
```

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

為配合既有六大戰鬥姿態體系（`idle`, `telegraph`, `attack`, `recover`, `skill`, `hit`），熔砧石蟹各姿態規劃如下（嚴格對齊 `review.md` Rule 4b-4、Rule 4b-5、Rule 4b-6 與 0-QA16）：

1. **待機姿態（`idle`）**：  
   2.2 頭身矮萌身軀微蹲扎穩低馬步，六足抓地平穩；右手主拳套橫抬於胸前護住面頰，左手副拳套斜指前下方蓄勢待發；頭頂雙向潛望石英目鏡朝前方好奇探視，背後四葉發條鑰匙隨每 1.5 秒急促跳動一格的熔爐律動輕快轉動，排氣煙囪規律噗出微型白蒸氣，神情專注沉著。
2. **前搖預警姿態（`telegraph`）**：  
   石蟹重心極限下沉！六足向外展開抓緊地面，身軀高度向下壓縮 25%；雙手拳套在胸前重重對撞發出「鏘！」的打鐵清脆巨響，背後排氣煙囪洩壓蓋猛然跳開，噴出濃烈白霧；拳套黑曜石受力面劇烈泛起金紅高溫流光，氣動衝壓活塞拉至最大行程，蓄滿崩山重擊之勢。
3. **出招攻擊姿態（`attack`）**：  
   側向滑步如電瞬衝半步！右手黑曜拳套借氣動連桿彈射爆發，自側向猛力揮出一記勢大力沉的衝壓重擺拳！拳面直擊目標核心，空中劃出一道燃燒著多巴胺金黃（#FFD028）與暖橘（#FFA010）的巨大弧光光刃；命中瞬間引發「轟——鏘！」的沉重鐵砧重擊震盪，爆散出滿屏多巴胺金星與機械火花。
4. **收招硬直姿態（`recover`）**：  
   重拳落地定格，身形借橫向慣性滑步半周卸去後座力；背部排煙管悠長呼出一口白蒸氣「嘶——」，右手拳套利落收回胸前，左手拳套向前微架，六足微彈重回穩固架勢。
5. **奧義技能姿態（`skill`）——【熔砧黑曜·千度衝壓崩山破（Anvil Obsidian Mountain-Shatter Combo）】**：  
   熔砧石蟹身形借地熱上升氣流凌空躍起！背後四葉發條鑰匙超頻疾轉化作金色光環；石蟹雙拳在空中完全閉合為一具巨型鐵砧狀合體重錘，自空中向地面轟然垂直衝壓砸落！正中目標時引發天崩地裂般的震波，大地迸射出四道金色鐵水般的童話熔岩地泉，漫天飄落晶瑩的金黃齒輪雨與多巴胺星芒，瞬間瓦解全場敵人防禦架勢！
6. **受擊反饋姿態（`hit`）**：  
   受到衝擊時，石蟹身軀向後滑移 12px，六足在石磚地面劃出火星；甲殼微縮，雙拳死死交叉封架於身前護住眼眶目鏡，背部煙囪噴出一股雜亂蒸氣，頑強抗住衝擊，絕不倒下。

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

### Q1：它掛在哪個核心循環的哪一環？
- **回答**：掛在核心循環「戰鬥（主線出征/停擺巨偶）-> 掉落零件/圖鑑解鎖 -> 衣櫥換裝與紙娃娃客製化 -> 數值無關的情感共鳴」的「**外觀收集與角色客製化環節**」。熔砧石蟹作為第九巡第四順位擴充，正式將全遊戲總族群擴充至五十二族，填補了 R06 赤焰熔爐長期缺乏武術家拳套素體的重大空白，為喜愛重工業鍛造題材與熱血近身格鬥的玩家提供極致硬派又反差可愛的發條石蟹玩具視覺體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
- **回答**：服務第一根體驗支柱「**極致反差萌（2.2 頭身 Q 版矮萌發條石蟹揮舞巨大黑曜石拳套，以橫行滑步展現熱血拳法）**」與第三根體驗支柱「**深厚世界觀與玩具敘事（古典鐵皮發條橫行蟹玩具、熔爐神壇鐵砧守護者傳承）**」。第一優先！

### Q3：玩家在手機上用單手拇指能不能操作它？
- **回答**：**完全可以**。所有戰鬥、移動與換裝交互完全複用既有武術家職業雙拇指操作介面，按鈕熱區嚴格 >= 48px，拳套近身連打與破勢節奏判定清晰，單手拇指在手機大廳與紙娃娃衣櫥中點擊互動流暢無阻。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
- **回答**：**絕對不需要**。純客戶端本機單機離線架構，素體資料、部件配置與動畫切片 100% 內嵌於本機 Godot 客戶端中，斷網狀態下所有紙娃娃部件與戰鬥姿態運轉如常，嚴守 §6 單機無伺服器紅線。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
- **回答**：**絕對不會**。依據 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況，目前 Web 目錄約 135 MB，首包瘦身（50~80 MB）屬於整體專案既有歷史欠帳；本提案為**純文字 Markdown 規格文件**，0 圖片、0 影片、0 聲音素材，直接新增包體為 0 KB！未來由美術與程式建置資產時，嚴格遵循雙規格（128x128 像素圖、512x512 高清圖）及 WebP/PNG 壓縮管線，預估單族全部資產增量 < 0.8 MB，不造成包體非理性膨脹。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
- **回答**：**放棄了「真實甲殼動物生物肉身、尖銳濕黏足爪與有機內臟軟組織」**，嚴格以「沖壓高耐熱鑄鐵板件、黑曜石石磚、氣動洩壓連桿、四葉發條鑰匙與橡膠防滑滾足」進行古典童話的發條玩具轉譯；**放棄了「自創新武器類別（如巨型剪鉗或噴火管）以追求噱頭的數值膨脹誘惑」**，完全收斂並服膺於既有武術家·拳套（`monk/fist`）體系；**放棄了「搶快直接產圖產片」**，嚴格遵守審查規範先立規格審定定稿後，再交棒下游依序建置骨架與資產。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

供下游骨架建置任務與資料表同步腳本參考之標準 JSON 區塊片段（嚴格遵守 `review.md` 0-QA30 前置防護規範，預先給足唯一 aliases）：

```json
{
  "crab": {
    "race_id": "crab",
    "name": "熔砧石蟹",
    "name_en": "The Anvil Crab",
    "aliases": ["anvil_crab", "crucible_crab", "molten_crab", "boxer_crab", "clockwork_crab"],
    "class_archetype": "monk",
    "weapon_class": "fist",
    "default_weapon_id": "wrap_gloves",
    "native_realm_id": "R06",
    "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
    "toy_lineage": "19 世紀末至 20 世紀中葉古典鐵皮發條橫行拳擊蟹玩具與鐘錶氣動鍛打機關偶",
    "color_palette": {
      "base": "#FFFDF8",
      "primary": "#FFA010",
      "secondary": "#4ED86A",
      "accent": "#FF5E8A",
      "metal": "#FFD028",
      "outline": "#1F1A3A"
    },
    "slots": {
      "chassis": "chassis_crab_molten_iron_default",
      "head_unit": "head_crab_periscope_visor_cowl",
      "winding_key": "key_crab_quad_flue_crucible_t_bar",
      "costume": "costume_crab_furnace_sapper_cuirass",
      "optic_core": "face_crab_dual_gauge_convex_lens",
      "weapon": "weapon_crab_obsidian_stamping_fist",
      "back_curio": "curio_crab_pneumatic_exhaust_chimney"
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

### 8.1 熔砧石蟹角色單體立繪 Prompt（4:5 垂直角色畫）

```
Full-body character illustration of a charming 2.2-head-tall anthropomorphic mechanical toy crab martial artist boxer, known as The Anvil Crab.

The crab is a compact handcrafted vintage mechanical toy designed to be held in one hand, completely non-biological, zero real shell, zero animal meat, zero organic slime. Wide rounded stylized carapace made of stamped cast-iron alloy plates painted in rustic charcoal black (#2A272A) with vibrant warm-orange heat accents (#FFA010) and golden-yellow bevels (#FFD028). Symmetrical articulated brass walking legs on the sides with black anti-slip rubber footpads. A head cowl features two playful brass periscope tubes holding expressive twin convex quartz eye lenses shining in warm golden-amber light (#FFD028) with mint-green gauge markings (#4ED86A).

The crab wears a furnace sapper cuirass made of quilted dark obsidian firebricks (#1F1A3A) bound with dopamine warm-orange borders and brass rivets. Twin miniature cast-iron exhaust chimneys are mounted on the upper back, puffing tiny white steam rings.

A prominent antique brass four-vane anvil cross winding key is mounted vertically on the upper back. The body is positioned at a three-quarter angle so the brass winding key clearly breaks the outer silhouette and catches warm specular light — never hidden behind the body.

The character wields heavy mechanical boxing gauntlets made of quenched dark obsidian with glowing orange heat-channels in an alert boxing high-guard pose.

Material: chipped cast-iron enamel, aged brushed brass edges, polished obsidian plates, tiny exposed silver screws, delicate seams, subtle scratches and toy imperfections, nostalgic antique toy construction.

Color palette: dopamine warm orange (#FFA010), sunbeam golden yellow (#FFD028), mint green gauge accents (#4ED86A), coral pink rivet highlights (#FF5E8A), dark obsidian violet-black outlines (#1F1A3A), warm cream baseplate highlights (#FFFDF8).

Pose: dynamic low-center boxer crouch pose, side-stepping stance, right fist held high guarding cheek, left fist held ready, tiny steam puffs escaping from chimneys, adorable yet tough toy personality.

Lighting: warm theatrical stage lighting, golden molten rim light, soft volumetric embers, soft ground foot shadow.

Camera: full-body character art, three-quarter view, 50mm lens, completely clean neutral warm studio background — plain warm cream gradient (#FFFDF8), no props, no scenery.

Style keywords: premium stylized 3D mobile RPG character art, cel-shaded anime style, bold outlines, dopamine color palette, handcrafted mechanical toy, chibi fantasy brawler, whimsical steampunk fairy tale, high readability.

NEGATIVE PROMPT:
real crab, real crustacean, biological animal, organic flesh, slimy shell, crab meat, seafood, plush toy, stuffed animal, humanoid robot, futuristic mech, military armor, sci-fi cyborg, Iron Man, smooth modern plastic, chrome, horror, creepy doll, porcelain doll, scary eyes, oversized weapons, multiple swords, extra limbs, dark muddy colors, text, letters, font, logo, watermark, signature.
```

### 8.2 熔砧石蟹熔爐鍛造場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```
A cinematic 16:9 key art illustration for a charming mobile RPG, set in the volcanic clockwork forge realm of R06 Molten Foundry.

In the foreground, a cute 2.2-head-tall mechanical toy crab boxer leaps across an iron suspension bridge over golden molten iron basins. The crab is made of stamped cast-iron plates, brass walking legs, dual glowing quartz eye lenses, and has a spinning brass cross winding key on its back. It delivers a punch with a heavy obsidian stamping gauntlet, creating a burst of bright dopamine golden sparks and soft steam clouds. Twin back chimneys emit cheerful white steam puffs.

Environment: breathtaking clockwork volcano forge diorama inside a caldera, golden molten iron pools glowing with warm light, dark obsidian quenched brick walkways, massive pneumatic stamping bridges, brass pressure-gauge clocktowers in the background, furnace flue trees with gentle heat distortion. In the far background, the silhouette of a giant clockwork stone-fist boar titan atop the Great Anvil.

Lighting: brilliant golden molten underlighting, dramatic rim lighting on cast-iron plates, sparkling fairy-tale toy embers (#FFD028, #FFA010), warm theatrical atmosphere.

Composition: cinematic action shot, high visual contrast, clear readable character silhouette, strong foreground focus with soft depth of field in the background.

Style keywords: premium stylized 3D game art, cel-shaded anime aesthetic, Maplestory and Tata Adventure inspired dopamine colors, handcrafted mechanical toy world, whimsical steampunk fairy tale, 8k resolution, crisp mobile-first readability.

NEGATIVE PROMPT:
photorealistic animals, real crabs, seafood, slimy flesh, blood, gore, horror, creepy monsters, dark muddy water, dirty grey colors, human figures, military tank, futuristic sci-fi, text, letters, words, logo, title, watermark, border, frame.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  "$(cat << 'EOF'
A cute 2.2-head-tall anthropomorphic mechanical toy crab boxer from Clockwork Heart, made of stamped cast-iron plates, articulated brass walking legs, dual quartz periscope optic lenses, wearing obsidian sapper cuirass, wielding heavy obsidian stamping gauntlets in boxing guard, prominent brass four-vane cross winding key on upper back breaking silhouette, twin back chimneys puffing tiny steam, cel-shaded, bold dark blue-violet outline, dopamine colors, warm cream background (#FFFDF8) --no real animal, --no flesh, --no organic shell, --no text, --no letters, --no logo, --no watermark
EOF
)" \
  output_crab_paperdoll.png \
  --aspect 4:5 \
  --ref /opt/side/bravesoul-game/branding/key_visual_main.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：本提案所引用之「金色液態鐵水熔池（Golden Molten Iron Basins）」、「黑曜淬火石磚步道（Obsidian Quenched Brick Walkways）」、「耐火排煙管樹（Furnace Flue Trees）」、「重型鍛造工坊與衝壓懸橋（Heavy Forging Foundries & Stamping Bridges）」、「黃銅洩壓儀表塔（Brass Pressure-Gauge Clocktowers）」、「晨曦天軌 6 號熔爐重載貨運月台（Dawn Rail Heavy Freight Platform 6）」、「高壓地熱噴射升空彈射井（Geothermal Ejection Launch Silo）」、「火山口中央鍛造神壇（Central Crucible Forge Altar）」、「黑曜石淬火神壇（Obsidian Quenched Great Anvil）」、「冷卻熔渣重力排料傾卸滑道（Slag Gravity Dump Chute）」、「磁吸隔熱排渣護欄網（Magnetic Slag-Retention Grid）」、「淬火冷卻噴淋池（Quenching Shower Station）」、「矮人鐵匠大師·重錘布隆（Master Smith Bronn）」、「陶土魔像學徒·黏土泥泥（Clay Clay）」、「熔爐溫控長老·坩堝老爹（Papa Crucible）」、「熔爐泰坦·重裝巨型石拳鐵豕（Titan Crucible: Iron-Tusk the Stone-Fist Boar）」逐字精確對齊 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 第 19 行、第 20 行、第 21 行、第 22 行、第 30 行、第 32 行、第 33 行、第 35 行、第 47 行、第 55 行、第 65 行、第 73 行、第 101/238 行、第 242 行，100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（包體膨脹查驗）**：純文字 Markdown 規格文件，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有五十一族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 51 族（含第 49 族熔鎧犰狳、第 50 族風箱毛蟲、第 51 族墨影烏賊）。
- [x] **review.md 23f-1（單一職業標籤）**：職業名稱唯一嚴格對齊為 `武術家 (Monk)`，無任何雙標籤或自創詞。
- [x] **review.md 23f-2（武器名稱前後一致）**：原生專屬武器在全文所有章節、表格與 JSON 片段中均統一稱作「黑曜衝壓熔岩拳套」，精確呼應 `R06_MOLTEN_FOUNDRY.md` 第 257 行「熔岩黑曜石拳板」與第 261 行「崩山衝壓擊」鍛造重拳工藝，相容武器精確對齊既有 `equipment.json` 之 `wrap_gloves`（練拳綁帶，tier 1）與 `iron_knuckle`（鐵節拳套，tier 3）。
- [x] **review.md 23f-4 / CANON 零毛皮鐵律**：全篇 100% 清除所有生物皮毛、真角質甲殼、肉質、血液、軟體黏液等字眼，石蟹特徵全面轉譯為沖壓高耐熱鑄鐵板件、黑曜石石磚、氣動洩壓雙聯煙囪、四葉十字發條鑰匙與橡膠防滑機械滾足。
- [x] **review.md 0-MKT7（單持無穿模規範）**：明確指定右手持主拳套向前高舉護面、左手副拳套微屈收於腰側蓄勢，主次分明，拳面不擋臉，0 佔位短棒，0 多餘浮動武器，0 穿模違規。
- [x] **review.md 0-QA30 前置防護**：aliases 預先定案 `crab`, `anvil_crab`, `crucible_crab`, `molten_crab`, `boxer_crab`, `clockwork_crab`，為下游骨架單建立唯一真相源。
- [x] **產圖 Prompt 規範**：第 8 節完整附上 4:5 與 16:9 提示詞，明載 `--ref /opt/side/bravesoul-game/branding/key_visual_main.png` 與 `--no text, --no letters, --no logo, --no watermark` 鐵律。
