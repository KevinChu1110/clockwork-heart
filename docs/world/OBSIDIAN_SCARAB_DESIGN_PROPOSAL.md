# 第六十種動物「黑曜金龜（The Obsidian Scarab）」世界觀與角色設計提案

> **標題**：第六十種動物「黑曜金龜（The Obsidian Scarab）」角色與世界觀設計提案  
> **提案代號**：`OBSIDIAN_SCARAB_DESIGN_PROPOSAL`（代號：`scarab` / 識別名：`race_scarab`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_1e7f15ad`（📖 世界觀｜第六十種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零皮革、零動物肉身、零生物黏液、零生鏽、零機油污漬；沖壓耐熱黑曜石板件、粗砂鑄鐵底盤、象牙白溫潤白瓷腮板、熔金琥珀水晶目鏡、雙叉黃銅機械調諧觸角、可開合黑曜石亮面鞘翅、雙聯微型高壓洩壓排煙管短尾、外露精工黃銅鉚釘與球形鉸鏈、背後四葉鍛造十字火紋黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調；多巴胺高飽和鮮亮色彩）  
> - `docs/world/regions/R06_MOLTEN_FOUNDRY.md`（第 1 行區域代號與名稱「R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano」、第 4 行「高耐熱粗獷鑄鐵板件、黑曜石淬火耐火磚、金色液態流光鐵水池、重型鍛打氣動連桿與高壓黃銅洩壓儀表套件」、第 6 行「局域走時狀態：齒輪超頻過載伴隨重錘敲擊律動（秒針每 1.5 秒急促跳動一格，伴隨重型鐵砧沉重打擊聲「鏘——噹！」；高溫熱浪引發發條金屬微幅熱脹，需精準掌握過載散熱節奏穿行）」、第 19 行「金色液態鐵水熔池（Golden Molten Iron Basins）」、第 20 行「黑曜淬火石磚步道（Obsidian Quenched Brick Walkways）」與「耐火排煙管樹（Furnace Flue Trees）」、第 21 行「重型鍛造工坊與衝壓懸橋（Heavy Forging Foundries & Stamping Bridges）」、第 22 行「黃銅洩壓儀表塔（Brass Pressure-Gauge Clocktowers）」、第 29 行「深海熱液湧泉管道·加壓換乘站」、第 30 行「晨曦天軌 6 號熔爐重載貨運月台」、第 32 行「高壓地熱噴射升空彈射井」、第 33 行「冷卻熔渣重力排料傾卸滑道」、第 35 行「磁吸隔熱排渣護欄網」、第 43 行「重裝鑄鐵矮人玩偶」、第 44 行「耐火陶土魔像」、第 45 行「發條耐火工兵蜥蜴」、第 47 行「淬火冷卻噴淋池」、第 55 行矮人鐵匠大師「布隆（Bronn）」、第 64 行陶土魔像學徒「泥泥（Clay Clay）」、第 72 行熔爐溫控長老「坩堝老爹（Papa Crucible）」、第 101 行旗艦泰坦 BOSS「熔爐泰坦·重裝巨型石拳鐵豕（Titan Crucible: Iron-Tusk the Stone-Fist Boar）」、第 124 行核心掉落零件「玄鐵精煉鑄錠、耐高溫合金彈簧、熔岩黑曜石拳板、耐火石墨潤滑膏」、第 130-131 行「七煞星軸」與「廉貞星軸」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（法師正式名稱 `mage`，標籤宣言 `\"把護盾織成刃\"`，武器 `crystal`，數值 `atk: 0, def: 3, hp: 10, crit: 1.0, speed: 0`，玩法 `\"穩穩打，靠戰魂和護體撐。同職也可玩杖。\"`，初始相容武器 `shard_focus`）  
> - `game/data/tables/equipment.json`（水晶類正式 line: `\"crystal\"`，初始相容武器：`shard_focus` 碎晶聚能，tier 1）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡（第 55~60 族）第五順位核心擴充，達成法師 5:5 杖晶對稱，迎來前五大職業 10 族大滿貫**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第六十種動物擴充素體規格**。  
   在全專案相繼於第十巡首位成員第五十六種動物重閥河馬（騎士·長槍，達成 5 劍 5 槍）、第二順位第五十七種動物星岩鼴鼠（戰士·戰鎚，達成 5 斧 5 鎚）、第三順位第五十八種動物嵐翼鼯鼠（忍者·機關鏢，達成 5 匕 5 鏢）以及第四順位第五十九種動物提線猞猁（武術家·機關爪，達成 5 拳 5 爪）順利完成前四大職業雙武器對稱平衡後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第五順位**，接棒輪轉進入全遊戲最具法陣防禦、戰魂共鳴、織盾成刃與持續續航的核心職業——**法師 (Mage)** 體系，原生武器掛載於**赤焰黑曜護體靈晶（`crystal` / 法師·晶）**。  
   黑曜金龜的加入，使全遊戲法師護體靈晶素體擴充至第 5 款（玄機龜、琉璃海馬、稜鏡孔雀、澄心水豚、黑曜金龜），與法師法杖素體（靈尾狐、靈鐘鴞、星盤靈羊、星儀渡鴉、日晷駱駝 5 款）達成**完全對稱的 5:5 完美平衡格局**！  
   更重要的是，這標誌著《發條之心》在前六十族擴充里程碑中，前五大職業（騎士、戰士、忍者、武術家、法師）全部正式達成各 10 族、雙武器系統 5:5 完美對稱的歷史性大滿貫！
2. **經典玩具起源與古典機械發條聖甲蟲／金龜子工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與微型鐘錶工藝史上的經典工藝原型：  
     ① **1900s-1930s 歐洲古典發條鐵皮金龜子／聖甲蟲自動機關玩具（Vintage European Tinplate Wind-up Scarab / Beetle Automaton / 德國 Ernst Paul Lehmann No. 499 "Scarabäus" 1903 年經典名作、Schuco 與 Marx 鐵皮甲蟲）**，通體由沖壓馬口鐵、高光多巴胺彩釉與齒輪傳動連桿咬合而成，背部外殼以雙扇精工黃銅鉸鏈固定，發條釋放時雙翅鞘甲微揚，六足在金屬板件上伴隨清脆節律「嗒、嗒、嗒」穩定爬行，是古典機械玩具史上最具機構工藝美感與幾何對稱魅力的自動偶；  
     ② **維多利亞時代微型鐘錶工藝——「火山口地熱測溫發條金龜（Victorian Horological Geothermal Scarab Automaton）」**，圓滾敦厚的身軀覆蓋著高溫淬火黑曜石陶瓷與防鏽鑄鐵板件，頭部裝配有一對分叉的黃銅機械調諧觸角，背部鞘翅下隱藏著微型耐高溫發條擒縱盒與散熱百葉窗，能敏銳感應火山鍛造的熱能脈衝；  
     ③ **古典神話太陽神車發條機關偶（Mythological Clockwork Solar Scarab Automaton）**，將經典聖甲蟲推動光芒晶球的傳奇意象，轉譯為懸浮自轉的「赤焰黑曜護體靈晶」，多面黑曜石晶體在胸前緩慢旋轉折射灼熱霞光，完美詮釋法師職業「把護盾織成刃、穩穩打、靠戰魂和護體撐」之法道之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「黑曜耐火鑄鐵矮萌底盤、黑曜淬火雙叉金角面罩、熔金琥珀水晶目鏡、赤焰熔爐隔熱工匠護裙、可開合雙扇黑曜亮面鞘翅、雙聯微型高壓洩壓排煙管短尾、赤焰黑曜護體靈晶與四葉鍛造十字火紋黃銅發條鑰匙」之赤焰熔爐黑曜法師素體（Quenched Obsidian Chassis, Twin-Horn Brass Visor Cowl, Molten Amber Crystal Eyes, Crucible Artisan Apron, Deployable Obsidian Elytra, Twin Micro-Vent Exhaust Tail, Crucible Obsidian Shield-Focus & Four-Leaf Forge Cross-Fire Brass Key）**。
3. **生態補足：徹底終結赤焰熔爐（R06）長久零法師之歷史空白，打造火山口晶核熱能防護線**：  
   在全遊戲 9 大界域中，中層高溫冶煉沙盤界域 `R06 赤焰熔爐·鍛造火山` 先前擁有熔火蜥蜴（戰士·鎚）、重角犀牛（戰士·斧）、熱流赤鳶（遊俠·弓）、熔鎧犰狳（騎士·劍）與熔砧石蟹（武術家·拳）共 5 族。  
   長久以來，赤焰熔爐匯聚了剛猛的重裝戰士、破陣劍客與硬漢拳師，**面對火山口金色流光鐵水池翻滾的過載熱浪、失控泰坦石拳鐵豕狂暴噴湧的高溫熔渣、以及遍佈全域的超溫熔毀危機，整個熔爐火山完全缺乏一位能夠在滾燙熔池與衝壓懸橋間穩定懸浮、以耐高溫黑曜石多面結晶匯聚地熱能量、為周圍工匠編織高溫耐熱屏障並將過載衝擊轉化為環形破甲光刃的「法師 (Mage)」核心素體**！黑曜金龜的降臨，徹底填補了 R06 赤焰熔爐長期以來零法師的生態空白，讓 R06 達成騎士、戰士、武術家、遊俠、法師五大光譜完備的重工火山陣容！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 運作邏輯（僅登錄 races_specification 正表提案項目，更新 total_races 為 59）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：黑曜金龜素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有五十九族武器與職業光譜全盤點

盤點現有首發五族與前五十四款擴充族（總計 59 族，含第 59 族提線猞猁）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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
- **黑曜金龜（The Obsidian Scarab）**：**法師 (Mage) —— 赤焰黑曜護體靈晶（`crystal`），多面黑曜石晶核懸浮調諧，耐熱六足滑步，織盾成刃引爆地熱晶芒！**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）10 族（劍 5、槍 5，已達完全平衡）；
- 戰士（Viking）10 族（斧 5、鎚 5，已達完全平衡）；
- 忍者（Ninja）10 族（匕 5、鏢 5，已達完全平衡）；
- 武術家（Monk）10 族（拳 5、爪 5，由提線猞猁補齊至完全平衡）；
- 法師（Mage）此前在 59 族中擁有 9 款動物素體（法杖 5 款、護體靈晶 4 款）；
- 遊俠（Ranger）9 族（弓 5、銃 4）；
- **本提案第六十種動物正式作為「第十巡第五順位」核心擴充，歸屬於法師 (Mage) 體系，原生武器掛載於 `crystal`（護體靈晶 / 法師·晶）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`法師 (Mage)`**；
- 黑曜金龜的加入，使全遊戲法師護體靈晶素體擴充至第 5 款，法師總數達成 10 款，法杖（5 款）與護體靈晶（5 款）達成完全對稱的平衡格局！全遊戲前五大職業達成各 10 族的對稱大滿貫！

### 1.2 黑曜金龜武器選擇：【赤焰黑曜護體靈晶（Crucible Obsidian Shield-Focus）】

黑曜金龜原生專屬武器定名為：**【赤焰黑曜護體靈晶（Crucible Obsidian Shield-Focus）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 赤焰熔爐·鍛造火山之高溫黑曜石淬火與耐火陶瓷工藝體系**！  
底層完全掛載於 `weapon_classes.json` 的 `crystal`（法師·晶）類別，享有 `crystal` 既有的「把護盾織成刃」標籤宣言（Tagline: `\"把護盾織成刃\"`）、防禦血量與輔助出色、魂槽特別好用、活得久耗得起之特性（`atk: 0, def: 3, hp: 10, crit: 1.0, speed: 0`），完美呼應 `R06_MOLTEN_FOUNDRY.md` 第 6 行「局域走時狀態：齒輪超頻過載伴隨重錘敲擊律動，秒針每 1.5 秒急促跳動一格，伴隨重型鐵砧沉重打擊聲鏘——噹！」之高溫熱諧振節奏與黑曜石結晶屏障保護反震手感！

- **法源素材咬合**：  
  完全對應 `R06_MOLTEN_FOUNDRY.md` 第 4 行代表材質「高耐熱粗獷鑄鐵板件、黑曜石淬火耐火磚、金色液態流光鐵水池」、第 20 行「黑曜淬火石磚步道」、第 101 行「黑曜石淬火神壇」、第 124 行核心掉落「玄鐵精煉鑄錠、耐高溫合金彈簧、熔岩黑曜石拳板」以及第 131 行「廉貞星軸（烈火淬金：受擊反震與霸體反擊）」，將火山口高溫黑曜岩的晶體結構轉化為護衛周身並反震敵人的靈晶法器。
- **單持規範遵守（0-MKT7）**：  
  遵循 `review.md 0-MKT7` 單持規範，右手向前平伸虛托，掌心上方浮空懸浮直徑約 20px 的多面稜鏡黑曜石晶核，晶核外圍環繞兩道逆向自轉的細緻黃銅刻度調諧環（#FFD028 / #FFA010）；左手微屈立於胸前結出專注調溫法印，全圖精確為 1 組浮空法器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"crystal\"` 的相容裝備 `shard_focus`（碎晶聚能，tier 1，`atk: 0, def: 2, hp: 8, crit: 0.5, speed: 0`），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款護體靈晶法師（玄機龜、琉璃海馬、稜鏡孔雀、澄心水豚）絕不撞型之論證

雖然黑曜金龜與玄機龜、琉璃海馬、稜鏡孔雀、澄心水豚同屬 `mage`（法師）護體靈晶（`crystal`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               法師職業靈晶系五族差異化對照表（玄機龜 vs 琉璃海馬 vs 稜鏡孔雀 vs 澄心水豚 vs 黑曜金龜）             │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 玄機龜 (Tortoise)    │ 琉璃海馬 (Seahorse)  │ 稜鏡孔雀 (Peacock)   │ 澄心水豚 (Capybara)  │ 黑曜金龜 (Scarab)   │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 八卦陣列護體、反震結界│ 洋流阻尼懸停、透鏡聚焦│ 萬花折光光刃、幾何織盾│ 太極流體阻尼、安詳化勁│ 熔爐熱能吸納、淬火晶刃│
│ 2. 動能來源     │ 八卦發條星盤偏心重擺 │ 浮力微氣囊與水流游絲 │ 扇形開合棘輪八音發音筒│ 溫泉浮力游絲慢速調速擺│ 耐高溫雙發條熱膨脹連桿│
│ 3. 步法特徵     │ 沉穩四足定點結印站樁 │ 垂直波浪浮動、洋流懸浮│ 芭蕾優雅滑步、扇面自轉│ 敦實慢步、頂水沉穩站樁│ 六足精工滑步、鞘翅微揚│
│ 4. 武器構造     │ 浮空八卦銅盤護體靈晶 │ 琉璃水母透鏡懸浮靈晶 │ 萬花筒聚能稜鏡靈晶   │ 澄心太極浮空靈晶(頂橘)│ 赤焰黑曜雙環懸浮晶核│
│ 5. 主題界域     │ R09 竹影道場·天元竹林│ R05 晶透海淵·發條洋流│ R02 晨曦小鎮·木偶集市│ R09 竹影道場·天元竹林│ R06 赤焰熔爐·鍛造火山│
│ 6. 材質質感     │ 青銅雕花、八卦生漆玉石│ 吹製透光藍玻璃、黃銅鰭│ 彩色鑲嵌玻璃、黃銅翎羽│ 溫潤青石板、防塵練功布│ 高溫淬火黑曜石、鑄鐵板│
│ 7. 角色剪影     │ 厚重金屬龜甲與觀星儀 │ S形流線海馬軀幹與背鰭│ 典雅高挑鳥偶、開合尾羽│ 方鈍圓滾微胖體態瞇眼 │ 2.2頭身雙叉金角雙扇鞘翅│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴守 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md`，100% 徹底清除所有真皮毛、皮革、羽毛、生物肉身與泥土髒污，全面轉譯為精緻古典高溫鍛造甲蟲機械自動偶質感：

- **沖壓耐熱黑曜石板件與粗砂鑄鐵底盤**：黑曜金龜的身軀絕非生物甲蟲甲殼或血肉，而是由赤焰熔爐矮人鐵匠大師布隆以**耐高溫粗砂鑄鐵模組（Cast Iron #2B2630 / #1F1A3A）**精密壓鑄成型，體態呈現 2.2 頭身矮萌微胖 Q 版造型。胸前鑲嵌溫潤細緻的**象牙白耐火白瓷腮板（#FFFDF8）**，表面施以多巴胺暖橘（#FFA010）幾何彩釉防燙線條。六足為圓潤小巧的精工黃銅球窩轉動鉸鏈（#FFD028），足底裝有耐熱矽膠微型吸震軟墊，絕無任何生物組織或黏液。
- **黑曜淬火雙叉金角面罩**：金龜標誌性的額角被轉譯為一對**黑曜淬火雙叉金角面罩（Twin-Horn Brass Visor Cowl）**。頭盔本體為圓滑打磨的黑曜岩面罩，前額挺立著一對分叉的黃銅機械調諧觸角（#FFD028），內置微型測溫熱電偶合金絲，能隨熔爐秒針每 1.5 秒一次的走時震顫靈敏微顫，完全杜絕昆蟲肉質觸鬚。
- **熔金琥珀水晶石英目鏡**：面甲中央眼眶處精準鏤空，鑲嵌一對清澈通透的熔金琥珀水晶石英透鏡（Molten Amber Crystal Visor #FFA010 / #FFD028）。眼眶周圍施以深藍紫立體手繪描邊（#1F1A3A），蓄力施法時，琥珀晶體深處亮起六角形結晶法陣光紋，溫暖純淨，絕無猙獰複眼或裂紋。
- **可開合雙扇黑曜石亮面鞘翅**：背部裝配有一對精研拋光的黑曜石亮面鞘翅（Deployable Obsidian Elytra #2B2630）。鞘翅表面飾有金色黃銅幾何包邊與多巴胺珊瑚橙彩繪條紋，施展技能與散熱時，雙翅如跑車剪刀門般向上彈開 30 度，露出內部金色齒輪組與蜂窩狀黃銅散熱孔，噴出細密的微溫水霧。
- **雙聯微型高壓洩壓排煙管短尾**：後腰部位並非昆蟲腹部尾節，而是一對精緻小巧的**雙聯微型高壓洩壓排煙管短尾（Twin Micro-Vent Exhaust Tail #FFD028 / #2B2630）**。以黑曜石萬向球形鉸鏈相連，定時噴出兩朵小巧可愛的半透明白色蒸氣圈，提供氣壓平衡與俏皮動態。
- **四葉鍛造十字火紋黃銅發條鑰匙**：背部中央挺立一枚**「四葉鍛造十字火紋黃銅發條鑰匙（Four-Leaf Forge Crucible Brass Key #FFD028 / #FFA010）」**，採用火山耐熱黃銅精密鍛造，中心鑲有一枚珊瑚粉耐高溫圓形鉚釘（#FF5E8A），隨火山秒針每 1.5 秒急促跳動一格勻速自轉。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格遵循 Kevin 與使用者畫像核心審美原則：
- **比例**：矮萌可愛的 2.0 ~ 2.2 頭身比，頭大身小，六足短圓粗壯，站立時微屈足下沉重心，右手向前虛托浮空靈晶，左手收胸結印，神態沉穩自信而富有童趣。
- **多巴胺鮮亮高飽和色盤（拒絕暗黑泥土灰黑）**：
  - **奶油米白底色（#FFFDF8）**：象牙白耐火白瓷腮板、胸腹襯板高光，溫潤明亮，杜絕髒濁。
  - **多巴胺暖橘主色（#FFA010）**：隔熱工匠圍裙、琥珀水晶目鏡、鞘翅彩繪飾條、靈晶核心能量流光。
  - **多巴胺薄荷淺綠（#4ED86A）**：圍裙耐熱密封飾條、靈晶能量外圈光暈、肩部鉸鏈裝飾。
  - **多巴胺天藍（#38A0FF）**：洩壓蒸氣微光、靈晶調諧刻度環投影光芒。
  - **多巴胺金黃（#FFD028）**：四葉發條鑰匙、雙叉機械觸角、黃銅球窩鉸鏈、鞘翅包邊與靈晶調諧環。
  - **多巴胺珊瑚粉（#FF5E8A）**：發條鑰匙中心鉚釘、護裙口袋刺繡標記。
  - **深藍紫立體手繪描邊（#1F1A3A）**：取代傳統髒黑泥土色，賦予黑曜石裝甲強烈的手繪通透感。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

拒絕靜止死板木樁，為黑曜金龜設計活靈活現的 Q 版發條動態：
- **待機呼吸感（Idle Breathing）**：
  - 2.2 頭身身軀每 1.5 秒配合火山秒針進行一次微幅上下起伏，胸前鑄鐵板件與散熱孔伴隨呼吸發出極細微的發條律動；
  - 掌心上方的赤焰黑曜靈晶以每秒半圈的平穩速度自轉，外圍兩枚黃銅刻度環逆向迴旋，折射出柔和的橙金多巴胺光斑；
  - 背部四葉十字發條鑰匙隨秒針每 1.5 秒急促跳動一格勻速旋轉，排煙短尾定時吐出微縮白煙圈。
- **待機專屬小動作（Special Idle Animations）**：
  - **「靈晶調溫」**：每隔 7 秒，金龜右手食指輕輕向上彈撥，浮空靈晶瞬間向上躍起半個頭高並加速自轉，隨後精準落回掌心上方，周圍爆出一圈細小的金色火花星芒；
  - **「鞘翅揚散」**：背後雙扇黑曜鞘翅伴隨「喀嗒」一聲向兩側彈開，蜂窩散熱孔噴出兩股細密白霧，雙叉金角愉悅地上下擺動兩下，隨後鞘翅輕巧合攏。
- **Poke 點擊互動（點擊反應反饋）**：
  - 玩家以手指點擊角色時，黑曜金龜如同被敲打的發條小鐵盒般原地彈起半公尺，六足微張，背後鞘翅猛烈展開，浮空靈晶在身前迅速擴散成一道半球形六角黑曜晶體防護罩；
  - 頭頂彈出俏皮對話氣泡：「**熔爐的高溫我最懂，我的晶盾連鐵豕都撞不碎！**」或「**看我把防禦護盾織成切甲光刃！**」，周身爆散出 4~6 枚暖橘色微型齒輪與薄荷綠水晶碎芒粒子。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R06 赤焰熔爐·鍛造火山無法師之歷史空白

在全專案九大界域中，中層高溫冶煉沙盤界域 `R06 赤焰熔爐·鍛造火山` 先前擁有 5 族，涵蓋重裝戰士（鎚、斧）、破障劍客（劍）、破勢拳師（拳）與遠距神射（弓），但面對火山口熔岩過熱沸騰、石拳鐵豕狂暴甩出的碎石熔渣、以及全域齒輪超頻危機，**長久以來完全缺乏一位能夠在滾燙熔池與衝壓懸橋間穩定懸浮、以耐高溫黑曜石多面結晶匯聚地熱能量、為周圍工匠編織高溫耐熱屏障並將過載衝擊轉化為環形破甲光刃的「法師 (Mage)」核心素體**。黑曜金龜的入駐，徹底補齊了 R06 最具戰略價值的高溫能量防線。

### 3.2 100% 逐字對齊引用 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R06_MOLTEN_FOUNDRY.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 常年駐守於火山口中央最高處的核心**「黑曜石淬火神壇（Obsidian Quenched Great Anvil）」**（`R06_MOLTEN_FOUNDRY.md` 第 101 行、第 238 行）與**「火山口中央鍛造神壇（Central Crucible Forge Altar）」**（第 102 行、第 162 行），引導地熱結晶能量為勇者進行護體靈晶的高溫熱諧振淬火調校；
  - 穿梭於火山口翻滾奔騰的**「金色液態鐵水熔池（Golden Molten Iron Basins）」**（`R06_MOLTEN_FOUNDRY.md` 第 19 行）兩岸，踏足於鑲嵌金黃耐熱黃銅墊片的**「黑曜淬火石磚步道（Obsidian Quenched Brick Walkways）」**（第 20 行），巡檢排列兩側的**「耐火排煙管樹（Furnace Flue Trees）」**；
  - 橫跨懸吊於沸騰熔池之上的**「重型鍛造工坊與衝壓懸橋（Heavy Forging Foundries & Stamping Bridges）」**（`R06_MOLTEN_FOUNDRY.md` 第 21 行），在不停往復運動的鍛鎚連桿下方以黑曜晶盾庇護運送原胚的工匠偶；
  - 依託遍佈工坊的高聳**「黃銅洩壓儀表塔（Brass Pressure-Gauge Clocktowers）」**（`R06_MOLTEN_FOUNDRY.md` 第 22 行），觀測雙針指針與圓形排氣閥門的熱壓數值，以靈晶吸收異常的熱壓波動；
  - 巡防外圍環形高架鐵軌端點的**「晨曦天軌 6 號熔爐重載貨運月台（Dawn Rail Heavy Freight Platform 6）」**（`R06_MOLTEN_FOUNDRY.md` 第 30 行），協助重型金屬原礦列車安全入軌；
  - 巡守於火山口鍛造神壇後方的**「高壓地熱噴射升空彈射井（Geothermal Ejection Launch Silo）」**（`R06_MOLTEN_FOUNDRY.md` 第 32 行），檢測直通頂層星穹軌道（R07）的高壓氣缸密封狀態；
  - 巡視火山下層外壁排渣口的**「冷卻熔渣重力排料傾卸滑道（Slag Gravity Dump Chute）」**（`R06_MOLTEN_FOUNDRY.md` 第 33 行），以晶刃擊碎卡阻滑道的凝固巨型熔渣球；
  - 依託外壁懸崖的**「磁吸隔熱排渣護欄網（Magnetic Slag-Retention Grid）」**（`R06_MOLTEN_FOUNDRY.md` 第 35 行），演練失足彈回與磁吸緩衝救護防線；
  - 定期引導工匠前往**「淬火冷卻噴淋池（Quenching Shower Station）」**（`R06_MOLTEN_FOUNDRY.md` 第 47 行）進行恆溫退火，使用耐高溫石墨潤滑粉末噴塗齒輪縫隙。
- **核心 NPC 互動情境**：
  - 與粗獷鑄鐵工匠**矮人鐵匠大師·重錘布隆（Master Smith Bronn the Heavy Hammer Dwarf）**（`R06_MOLTEN_FOUNDRY.md` 第 55 行）結為鍛造默契搭檔，布隆揮動發條鍛錘時，黑曜金龜在鐵砧周圍展開靈晶隔熱屏障，防止熾熱火星灼傷學徒；
  - 照護圓滾滾的紅陶小泥偶**陶土魔像學徒·黏土泥泥（Clay Clay the Terracotta Apprentice）**（`R06_MOLTEN_FOUNDRY.md` 第 64 行），以微溫的黑曜晶光幫助泥泥均勻烘烤定型剛捏製好的小陶磚；
  - 拜會古老重裝鑄鐵玩偶**熔爐溫控長老·坩堝老爹（Papa Crucible the Foundry Elder）**（`R06_MOLTEN_FOUNDRY.md` 第 72 行），向老爹請教「七煞破壞」與「廉貞淬火」的星軸調諧秘法，藉老爹吐出的白煙圈校準發條鑰匙。
- **守護泰坦作戰支援**：
  - 面對火山口中央核心鍛造神壇失控狂暴的**「熔爐泰坦·重裝巨型石拳鐵豕（Titan Crucible: Iron-Tusk the Stone-Fist Boar）」**（`R06_MOLTEN_FOUNDRY.md` 第 101 行），黑曜金龜在鐵豕釋放毀滅性「震地八荒裂」與高溫熔渣拋擲時，升起堅不可摧的赤焰黑曜護體法陣，吸收狂暴衝擊轉化為環形破甲刃芒，支援小白精確破壞鐵豕的「玄鐵石拳」、「背部洩壓煙囪」與「黑曜獠牙面罩」，成功修復冷卻循環系統！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，黑曜金龜的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 黑曜金龜專屬造型規格與材質特徵（嚴守 100% 零真皮毛、零皮革、零生鏽、零污漬）                    │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. chassis (素體)│ 黑曜耐火鑄鐵矮萌底盤（#2B2630 / #FFFDF8），沖壓粗砂鑄鐵外殼配象牙白瓷腮板，黃銅球窩轉動關節     │
│ 2. head_unit(頭)│ 黑曜淬火雙叉金角面罩（#2B2630 / #FFD028），打磨黑曜岩圓盔配額前雙叉黃銅機械調諧觸角，無生物肉質│
│ 3. optic_core(眼)│ 熔金琥珀透鏡耐火面甲（#FFA010 / #FFD028），高透光熔金琥珀石英晶片嵌黑曜面罩，深藍紫防燙眼眶   │
│ 4. costume (服裝)│ 赤焰熔爐隔熱工匠護裙（#FFA010 / #4ED86A），暖橘色耐高溫彩釉帆布小圍裙，飾薄荷綠封條與黃銅排扣 │
│ 5. back_curio   │ 雙聯微型高壓洩壓排煙管短尾（#FFD028 / #2B2630），兩根仰角黃銅排氣短管，定時噴出微縮白色蒸氣圈│
│ 6. winding_key  │ 四葉鍛造十字火紋黃銅發條鑰匙（#FFD028 / #FFA010），耐熱黃銅四葉十字造型，中心嵌珊瑚粉防塵鉚釘   │
│ 7. weapon (武器)│ 赤焰黑曜護體靈晶（#2B2630 / #FFD028 / #FFA010），右手懸浮多面黑曜晶核，環繞雙道黃銅調諧齒環  │
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`chassis`（素體底盤）**：  
   2.2 頭身 Q 版矮萌微胖金屬身軀，由高耐熱粗砂鑄鐵模組（#2B2630）沖壓鑄造而成。胸前與兩腮鑲嵌溫潤光潔的象牙白耐火白瓷襯板（#FFFDF8），表面分佈著細微的防震鉚釘與多巴胺金黃（#FFD028）彩釉飾條。六足為圓潤小巧的精工黃銅球窩鉸鏈，足底配備耐熱矽膠微型吸震軟墊，行走時在熔爐石磚步道上發出踏實厚重的金屬踏音，徹底杜絕任何真實生物外殼或黏液質感。
2. **`head_unit`（頭部面罩）**：  
   圓潤光滑的打磨黑曜岩半球形頭盔面甲。前額挺立著一對長約 18px 的雙叉黃銅機械調諧觸角（#FFD028），內部纏繞著微型熱電偶合金絲，能敏銳感應環境溫度與走時震顫。面部中央眼眶處精準鏤空供 `optic_core` 透光，鼻部轉譯為一枚精工金屬排氣微孔，整體散發出古典機械金龜與發條玩具融合的俏皮威嚴感。
3. **`optic_core`（琥珀水晶目鏡）**：  
   一對晶瑩剔透的熔金琥珀水晶石英透鏡（#FFA010 / #FFD028）。眼周手工繪製深藍紫（#1F1A3A）立體手繪防燙外框，目光專注沉著。在引導靈晶編織護體法陣與蓄力時，鏡片中心泛起微縮六角形黑曜石結晶符印光芒，透光溫暖柔和，絕無恐怖裂紋。
4. **`costume`（隔熱工匠護裙）**：  
   由高飽和暖橘色（#FFA010）耐高溫彩釉厚帆布裁切的古典工匠小圍裙。前襟配備四枚精緻的黃銅小圓排扣，領口與口袋邊緣飾以薄荷綠（#4ED86A）耐熱密封飾條，背後預留發條插孔，下擺微揚露出靈巧的黃銅六足，兼具重工業防護功能與童話慶典氛圍。
5. **`back_curio`（洩壓排煙短尾）**：  
   安裝於後腰黑曜石球形鉸鏈上的雙聯微型高壓洩壓排煙管短尾（#FFD028 / #2B2630）。由兩根向上傾斜 30 度的精工拋光黃銅排氣短管組成，隨角色呼吸與發條自轉，每隔數秒規律地噴出一對直徑約 8px 的半透明白色蒸氣圈，提供氣壓緩衝與趣味動態。
6. **`winding_key`（十字火紋發條鑰匙）**：  
   背部中央挺立的四葉鍛造十字火紋黃銅發條鑰匙。採用赤焰黃銅金（#FFD028）精密鑄造，造形如同一對交叉疊合的鍛造火焰十字徽記，四葉邊緣帶有優雅的倒角打磨，中心固定一枚珊瑚粉防塵鉚釘（#FF5E8A）。隨熔爐秒針每 1.5 秒急促跳動一格自轉，發出微弱清脆的齒輪咬合聲。
7. **`weapon`（赤焰黑曜護體靈晶）**：  
   黑曜金龜專屬武器【赤焰黑曜護體靈晶】。右手向前平伸虛托，掌心上方約 12px 處懸浮一顆直徑約 20px 的多面稜鏡黑曜石晶核（#2B2630 / #FFA010），晶體表面折射出鏡面高光與赤金霞光；外圍環繞兩道細緻的黃銅刻度調諧齒環（#FFD028），逆向自轉發出嗡鳴。施法時，晶體向外投射出半透明六角晶格護盾，將所受傷害轉化為破甲晶芒反震敵人。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 正面微側30度穩健站姿，六足微屈抓地，右手虛托浮空旋轉之黑曜靈晶，左手結印護胸，雙叉金角微顫    │
│ 2. attack (普攻)  │ 踏步前推，右手掌心微震，浮空靈晶向正前方疾射三道旋轉黑曜結晶飛刃，伴隨清脆破空玻璃爆裂音     │
│ 3. hit (受擊)     │ 身軀受震向後微仰，靈晶瞬間張開小型六角晶格護盾抵擋衝擊，背部鞘翅微揚洩壓，排煙尾吐出急促蒸氣 │
│ 4. recover (硬直) │ 六足穩健踩踏地面卸力，靈晶回旋至掌心重新調諧，雙叉金角左右搖擺校準頻率，迅速重組防衛架勢     │
│ 5. skill (技能)   │ 雙手高舉合十，背後黑曜鞘翅完全張開，靈晶高懸頭頂暴射璀璨赤金光芒，在周身織成巨大晶體屏障破敵 │
│ 6. telegraph (蓄力│ 身軀下沉進入深度蓄力，靈晶內部熾熱金光劇烈充能，雙道黃銅調諧環超頻急轉，腳下浮現地熱晶格法陣 │
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為法師職業護體靈晶系的核心擴充素體，直接提供穩健防護、織盾成刃、戰魂反震與陣容續航的高手感戰鬥體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過法師護體靈晶的「穩穩打，靠戰魂和護體撐」機制，在敵人攻擊瞬間以晶盾吸收並觸發受擊反震破甲），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身沖壓黑曜耐火鑄鐵與發條金龜自動偶體現熔爐火山的工匠童話魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏雙拇指操作配置，靈晶護盾施放與結晶射擊自帶智能索敵與護盾自動展開判定，單拇指即可輕鬆完成連續點擊普攻連段、長按蓄力開盾與絕招爆發。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 55 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實昆蟲生物甲殼、細密腿刺與多對複眼**：徹底放棄自然界甲蟲的生物組織與令人生畏的昆蟲特徵，全面轉譯為 2.2 頭身矮萌沖壓鑄鐵外殼、圓潤象牙白瓷腮板與雙叉黃銅機械觸角，以換取手機螢幕上的高親和力、高辨識度與發條玩具童趣質感；  
2. **放棄雙持雙晶核或全方位浮游砲的繁雜視覺方案**：為了避免在手機小螢幕上多顆浮動水晶與複雜光束造成嚴重視覺遮擋與掉幀，放棄設計多顆浮游光球，嚴格遵守 `0-MKT7` 單持規範，改為右手單手引導懸浮一顆結構分明、帶雙黃銅刻度環的「赤焰黑曜護體靈晶」，左手維持專注立胸結印的法師古典姿態。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "scarab",
  "aliases": [
    "obsidian_scarab",
    "crucible_scarab",
    "forge_beetle",
    "clockwork_scarab",
    "volcano_scarab"
  ],
  "name_zh": "黑曜金龜",
  "name_en": "The Obsidian Scarab",
  "class_archetype": "法師 (Mage)",
  "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
  "lore_anchor": "駐守於赤焰熔爐·鍛造火山「火山口中央鍛造神壇」與「黑曜石淬火神壇」，穿行於「金色液態鐵水熔池」兩岸的「黑曜淬火石磚步道」與「耐火排煙管樹」，跨越「重型鍛造工坊與衝壓懸橋」，仰望「黃銅洩壓儀表塔」，巡邏「晨曦天軌 6 號熔爐重載貨運月台」、「高壓地熱噴射升空彈射井」與「冷卻熔渣重力排料傾卸滑道」，依託「磁吸隔熱排渣護欄網」與「淬火冷卻噴淋池」，結伴矮人鐵匠大師·布隆、陶土魔像學徒·泥泥與熔爐溫控長老·坩堝老爹；通體覆蓋高溫淬火黑曜岩底盤與象牙白瓷腮板、黑曜淬火雙叉金角面罩、熔金琥珀水晶目鏡、赤焰熔爐隔熱工匠護裙、可開合雙扇黑曜亮面鞘翅、雙聯微型高壓洩壓排煙管短尾、四葉鍛造十字火紋黃銅發條鑰匙，右手單持專屬赤焰黑曜護體靈晶，以2.2頭身矮萌微胖體態、六足精工黃銅球窩鉸鏈、熔爐地熱晶核吸納、多面晶刃反震破勢與織盾成刃見長的高溫火山機關造物法師",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1900s-1930s 歐洲古典發條鐵皮聖甲蟲與維多利亞鐘錶地熱自動偶)",
    "posture": "2.2 頭身矮萌身軀微側30度穩健站姿，六足微屈下沉抓地，右手向前虛托浮空旋轉靈晶，左手收胸結印，背後四葉發條鑰匙隨秒針每1.5秒跳拍一格勻速自轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "打磨黑曜岩半球形頭罩（#2B2630），前額挺立雙叉黃銅機械調諧觸角（#FFD028），兩腮鑲嵌溫潤象牙白瓷耐火腮板（#FFFDF8），眼眶處鏤空透光",
    "ears": "無外耳，以額前雙叉黃銅機械調諧觸角（#FFD028）替代，內置微型熱電偶合金絲隨秒針微顫測溫",
    "torso_and_limbs": "高耐熱粗砂鑄鐵模組（#2B2630）沖壓外殼，胸腹鑲嵌白瓷耐火襯板，四肢為精工黃銅球窩轉動鉸鏈與矽膠吸震軟墊",
    "tail": "雙聯微型高壓洩壓排煙管短尾（#FFD028 / #2B2630），兩根仰角黃銅排氣短管，每隔數秒噴出微型白色蒸氣圈",
    "weapon_system": "右手單持專屬「赤焰黑曜護體靈晶（Crucible Obsidian Shield-Focus）」，浮空旋轉多面黑曜晶核配雙黃銅刻度調諧環，底層掛載 equipment.json 既有 shard_focus (tier 1)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白瓷耐火高光，兩腮腮板、胸腹襯板高光)",
    "primary": "#FFA010 (主色多巴胺暖橘，隔熱工匠圍裙、琥珀透鏡、鞘翅彩繪飾條)",
    "secondary": "#4ED86A (次色多巴胺薄荷淺綠，圍裙密封飾條、靈晶能量外圈光暈)",
    "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心鉚釘與口袋刺繡印記)",
    "metal": "#FFD028 (金屬赤焰黃銅金，四葉發條鑰匙、雙叉觸角、鉸鏈與靈晶調諧環)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_scarab.png (品牌形象立牌)",
        "web/media/hero/char_scarab.png (官網英雄展示立繪)",
        "docs/art/obsidian_scarab_concept.png (概念立繪)",
        "game/assets/sprites/player/scarab_idle.png (64x64 待機)",
        "game/assets/sprites/player/scarab_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/scarab_idle.png (隊伍待機)",
        "web/media/hero/scarab_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/scarab_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/scarab_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/scarab_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/scarab_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/scarab_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/scarab_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/scarab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/scarab.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/scarab_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/obsidian_scarab.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/scarab/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_scarab.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/obsidian_scarab_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_scarab.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/scarab_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/scarab_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/scarab_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/scarab_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/scarab_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/scarab_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/scarab_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/scarab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/scarab.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/obsidian_scarab.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/scarab/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行提醒（嚴守任務邊界）**：本任務為「只寫文件，不產圖不產片」。以下提示詞僅作企劃歸檔與規格預置，等待後續美術產圖任務由 sideart 領取執行。

### 8.1 黑曜金龜角色單體立繪 Prompt（4:5 垂直角色畫）

```text
masterpiece, best quality, 2.2 head-to-body ratio chibi cute clockwork mechanical toy scarab beetle mage hero, named The Obsidian Scarab, standing firmly on an obsidian quenched brick pedestal in a volcano forge. Made of glossy polished obsidian plates, dark cast-iron frame, glazed ivory-white porcelain cheeks, and gleaming brass joint spheres. Distinctive rounded obsidian helmet with a pair of cute twin-forked brass mechanical tuning horn antennae. Wearing a vibrant warm orange heat-resistant artisan apron with mint green trim and tiny brass buttons, glowing dual-tone molten amber crystal eyes, and twin deployable polished obsidian elytra wing-covers slightly parted revealing glowing internal brass clockwork gears. At the back, a pair of tiny upward-angled brass micro-vent exhaust pipes puffing delicate transparent white steam rings. Right hand holding forward levitating a glowing faceted dark obsidian crystal orb encircled by two counter-rotating thin brass gauge rings with golden runic tick marks, left hand held in a focused spellcasting gesture. A prominent four-leaf forge cross-fire brass wind-up key mounted on the center back. Clean, dopamine vibrant candy-like colors, warm orange #FFA010, mint green #4ED86A, ivory white #FFFDF8, gold brass #FFD028, deep obsidian black-purple #1F1A3A, soft Tyndall volcanic forge illumination, zero fur, zero skin, zero organic parts, zero ugly bugs, pure mechanical and obsidian toy automaton, 4:5 aspect ratio.
```

### 8.2 黑曜金龜赤焰熔爐場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```text
panoramic vibrant fairy tale scene in R06 Molten Foundry Crucible Volcano. In the center foreground, a 2.2 head-body ratio cute mechanical toy obsidian scarab beetle mage stands confidently on a heavy stamping suspension bridge above golden glowing liquid metal pools, right hand forward projecting a massive shimmering hexagonal obsidian crystal barrier that reflects heat waves into sharp radiant blades. In the background, majestic cast-iron forges, brass pressure-gauge clocktowers releasing puffs of steam, towering flue trees, and distant colossal gear structures under a warm fiery sunset-colored smoked-glass dome. Dopamine bright cheerful palette, warm orange, mint green, gold, ivory white, crisp clockwork toy aesthetic, bold stylized outlines, zero real fur, zero feathers, wide-angle cinematic 16:9 aspect ratio.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 4:5 \
  --out docs/art/obsidian_scarab_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 16:9 \
  --out docs/art/obsidian_scarab_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 既有地標（黑曜石淬火神壇、火山口中央鍛造神壇、金色液態鐵水熔池、黑曜淬火石磚步道、耐火排煙管樹、重型鍛造工坊與衝壓懸橋、黃銅洩壓儀表塔、晨曦天軌 6 號熔爐重載貨運月台、高壓地熱噴射升空彈射井、冷卻熔渣重力排料傾卸滑道、磁吸隔熱排渣護欄網、淬火冷卻噴淋池）與居民 NPC（矮人鐵匠大師·布隆、陶土魔像學徒·泥泥、熔爐溫控長老·坩堝老爹、守護泰坦「熔爐泰坦·重裝巨型石拳鐵豕」），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`法師 (Mage)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  右手單持赤焰黑曜護體靈晶（浮空單晶核配雙調諧環），左手收胸結守護法印，左右肢體姿態描述清晰，0 雙持穿模。
- [x] **CANON 世界憲章零毛皮零皮革鐵律**：  
  100% 零真動物肉身、零生物毛皮、零皮革、零羽毛、零黏液、零生鏽、零機油污漬；通體轉譯為沖壓耐熱黑曜石板件、粗砂鑄鐵底盤、象牙白溫潤白瓷腮板、熔金琥珀水晶目鏡、雙叉黃銅機械調諧觸角、可開合雙扇黑曜亮面鞘翅、雙聯微型高壓洩壓排煙管短尾與四葉鍛造十字火紋黃銅發條鑰匙。
- [x] **法師護體靈晶與法杖對稱平衡**：  
  作為第十巡第五順位擴充，補齊法師護體靈晶第 5 款，與法師法杖（5 款）達成完全 5:5 對稱平衡！全遊戲前五大職業達成各 10 族、雙武器 5:5 完美對稱大滿貫！
