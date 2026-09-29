# 第六十一種動物「彩喙巨嘴鳥（The Prism-Bill Toucan）」世界觀與角色設計提案

> **標題**：第六十一種動物「彩喙巨嘴鳥（The Prism-Bill Toucan）」角色與世界觀設計提案  
> **提案代號**：`PRISM_BILL_TOUCAN_DESIGN_PROPOSAL`（代號：`toucan` / 識別名：`race_toucan`）  
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）  
> **提案作者**：小凱（側案·策劃總監 sideplan）  
> **對應看板任務**：`t_ff23bcb9`（📖 世界觀｜第六十一種動物紙娃娃角色設計提案）  
> **法源依據與對齊規範**：  
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零皮革、零動物肉身、零生物黏液、零真羽毛、零生鏽、零機油污漬；沖壓雕花薄銅板羽紋板件、輕量化合金底盤骨架、溫潤象牙白彩釉白瓷喉胸板、雙凸透光翡翠石英瞄準目鏡、多層沖壓鏤空黃銅彩晶巨喙面罩、折扇式沖壓薄銅板導航尾羽、外露精工黃銅鉚釘與球形鉸鏈、背後三葉林冠旋翼黃銅發條鑰匙）  
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調；多巴胺高飽和鮮亮色彩：檸檬黃#FFD028、落日暖橘#FFA010、薄荷綠#4ED86A、天藍#38A0FF、珊瑚粉#FF5E8A、深藍紫描邊#1F1A3A）  
> - `docs/world/regions/R03_EMERALD_WOODS.md`（第 1 行區域代號與名稱「R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest」、第 4 行「人造短絨苔蘚、沖壓雕花薄銅板、分節金屬藤蔓與注塑樹脂發光菌菇套件」、第 6 行「局域走時狀態：慢速延遲伴隨規律停拍（秒針每隔 3~4 秒跳動一格，並伴隨約 0.9 秒短暫定格停拍；停拍間隙深林動能自鎖，唯有掌握停拍節律者方能穿行於風切之中）」、第 14-16 行「多邊形厚鑄黃銅展台底座」、「金屬樹根銅質傳動懸臂」、第 19 行「加厚短絨氈毛地毯（氈毛地毯）」與「防滑齒槽的黃銅薄板接縫」、第 20 行「機械巨木（Brass Canopy Giants）」、「手刷墨綠耐磨漆面」與「金屬防鏽齒輪樹汁（Copper Sap）」透明耐壓玻璃管道、第 21 行「發條藤蔓（Clockwork Vines）」螺旋軟鋼絲與分節小銅環、第 22 行「樹脂發光菌菇（Luminescent Resin Mushrooms）」、第 23 行「樹屋聚落（Treehouse Enclave）」發條繩索滑輪吊籃、第 25 行「丁達爾發條晨曦光斑（Tyndall Clockwork Godrays）（#D4F7D0）」、第 30 行「蔓谷天梯引道·深林站（Vine Valley Stairway Terminal）」、第 31 行「晨曦天軌 3 號月台（Dawn Rail Platform 3）」、第 33 行「高架重軌引橋·巨輪城站（High Brass Viaduct Gate）」、第 34 行「赤焰索道懸橋（Crucible Ropeway Chasm）」、第 36 行「防護金屬藤蔓彈力網（Perimeter Vine-Spring Net）」、第 44 行「守林發條小鹿（Clockwork Fawns）」、第 45 行「發條松鼠信差（Wind-up Squirrel Couriers）」、第 46 行「林木守護木偶（Arbor Sentinel Marionettes）」、第 48 行「樹汁導流泵」、第 51 行守護泰坦「疾影神隼」、第 56 行守林哨兵「風耳（Windear the Forest Watcher）」、第 65 行靈尾工藝師「小鈴（Suzu the Bell-Tailed Fox）」）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `game/data/tables/weapon_classes.json`（遊俠正式名稱 `ranger`，標籤宣言 `\"一響定生死\"`，武器 `gun`，數值 `atk: 5, def: -1, hp: -6, crit: 4.0, speed: 0`，玩法 `\"遠遠點射。同職也可玩弓。\"`，初始相容武器 `flint_gun`）  
> - `game/data/tables/equipment.json`（火槍類正式 line: `\"gun\"`，初始相容武器：`flint_gun` 燧發火銃，tier 1）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十巡第六順位核心擴充，達成遊俠 5:5 弓銃對稱，迎來全遊戲六大職業各 10 族、十二大武器系統完全對稱之終極歷史大滿貫**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第六十一種動物擴充素體規格**。  
   在全專案相繼於第十巡首位成員第五十六種動物重閥河馬（騎士·長槍，達成 5 劍 5 槍）、第二順位第五十七種動物星岩鼴鼠（戰士·戰鎚，達成 5 斧 5 鎚）、第三順位第五十八種動物嵐翼鼯鼠（忍者·機關鏢，達成 5 匕 5 鏢）、第四順位第五十九種動物提線猞猁（武術家·機關爪，達成 5 拳 5 爪）以及第五順位第六十種動物黑曜金龜（法師·護體靈晶，達成 5 杖 5 晶）順利完成前五大職業雙武器對稱平衡後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十巡第六順位（最終收官席位）**，壓軸輪轉進入全遊戲射程最遠、爆發最高、讀秒看破與遠距狙殺的核心職業——**遊俠 (Ranger)** 體系，原生武器掛載於**林冠聚能氣動銃（`gun` / 遊俠·銃）**。  
   彩喙巨嘴鳥的加入，使全遊戲遊俠火槍素體擴充至第 5 款（蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥、彩喙巨嘴鳥），與遊俠機關弓素體（雲嵐鶴、翠角鹿、幻彩變色龍、熱流赤鳶、鐘塔長頸鹿 5 款）達成**完全對稱的 5:5 完美平衡格局**！  
   更重要的是，這標誌著《發條之心》在六十一種動物擴充歷程中，**全遊戲六大核心職業（騎士、戰士、忍者、武術家、法師、遊俠）全部正式達成各 10 族、十二大武器系統 5:5 完美對稱的歷史性大滿貫**！
2. **經典玩具起源與古典機械發條巨嘴鳥工藝**：  
   - 本提案選定全球古典機械玩具、鐵皮玩具與光學測候工藝史上的經典工藝原型：  
     ① **1910s-1930s 歐洲古典發條鐵皮鳥類自動機關玩具（Vintage European Tinplate Wind-up Toucan / Pecking Bird Automaton / 德國 Ernst Paul Lehmann、Schuco 與 Marx 鐵皮彩繪鳥偶名作）**，通體由沖壓薄馬口鐵、高光多巴胺琺瑯彩釉與齒輪連桿咬合而成，標誌性的巨大鳥喙在發條釋放時伴隨清脆金屬節奏「咔、噠、嗒」靈動開合，雙足在金屬橫桿上穩定側跳，是古典機械玩具史上最具幾何誇張剪影與色彩視覺張力的自動偶名品；  
     ② **維多利亞時代林冠測候與光學測距發條巨嘴鳥（Victorian Horological Canopy Rangefinder Toucan Automaton）**，將巨嘴鳥標誌性的龐大鳥喙轉譯為多層沖壓鏤空黃銅面罩，內置雙凸石英測距透鏡、微型氣動閥門與同心圓十字瞄準光圈，能穿透茂密林冠霧氣精準鎖定目標距離；  
     ③ **古典發條玩具射擊手偶（Vintage Clockwork Marksman Automaton）**，將經典發條玩具的單發發射機構轉譯為「林冠聚能氣動銃」，側置轉輪發條供彈盤在扳機扣動時旋轉上膛，配合花瓣形洩壓制退器噴出清脆的高壓氣動果實彈，完美詮釋遊俠職業「一響定生死、遠遠點射」之射手之魂；  
   - 完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；  
   - 作為全遊戲首款且唯一具備**「林冠輕量化合金素體底盤、彩晶折光巨嘴面罩、翡翠石英瞄準目鏡、蔓谷探險巡林獵裝、多節沖壓銅片導航尾翼、三葉林冠旋翼黃銅發條鑰匙與林冠聚能氣動銃」之翡翠深林巨嘴遊俠素體（Canopy Alloy Chassis, Prism-Bill Brass Visor Cowl, Emerald Quartz Monocle, Vine Valley Scout Harness, Segmented Copper Rudder Tail, Tri-Vane Canopy Rotor Brass Key & Canopy Prism Pneumatic Arquebus）**。
3. **生態補足：徹底終結翡翠深林（R03）長久零火槍手之歷史空白，打造林冠高空光學狙擊防線**：  
   在全遊戲 9 大界域中，中層浮空林地界域 `R03 翡翠深林·發條蔓谷` 先前擁有靈尾狐（法師·杖）、碧簧蛙（忍者·鏢）、翠角鹿（遊俠·弓）、巡林松鼠（騎士·劍）、疾影神隼（武術家·爪）、劈木河狸（戰士·斧）與風箱毛蟲（戰士·鎚）共 7 族。  
   長久以來，翡翠深林在地表與低空擁有敏捷的鹿弓、松鼠劍客、劈木河狸與風箱毛蟲，**但面對林冠高層機械巨木（Brass Canopy Giants）頂部交錯纏繞的發條藤蔓（Clockwork Vines）、樹屋聚落（Treehouse Enclave）周圍濃密的林間丁達爾霧氣、以及守護泰坦疾影神隼狂暴掀起的高空風切危機，整個深林完全缺乏一位能夠站在高聳樹冠平台、以彩晶巨喙內部雙凸透鏡進行超視距光學測距、以高壓氣動重銃自上而下定點破除障礙與風切核心的「火槍遊俠 (Ranger·Gun)」核心素體**！彩喙巨嘴鳥的降臨，徹底填補了 R03 翡翠深林長期以來零火槍手的生態空白，讓 R03 達成機關弓與氣動銃雙遠程體系並存的完備陣容！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 運作邏輯（僅登錄 races_specification 正表提案項目，更新 total_races 為 60）。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：彩喙巨嘴鳥素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有六十族武器與職業光譜全盤點

盤點現有首發五族與前五十五款擴充族（總計 60 族，含第 60 族黑曜金龜）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

- **白金兔（Clockwork Rabbit）**：劍士 (Knight) —— 單手長劍（`sword`），平衡攻防，中近距離。
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
- **彩喙巨嘴鳥（The Prism-Bill Toucan）**：**遊俠 (Ranger) —— 林冠聚能氣動銃（`gun`），高空林冠光學測距，多室減速氣動高壓發射，雙爪扣枝抗震，一響定生死！**

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 騎士（Knight）10 族（劍 5、槍 5，已達完全平衡）；
- 戰士（Viking）10 族（斧 5、鎚 5，已達完全平衡）；
- 忍者（Ninja）10 族（匕 5、鏢 5，已達完全平衡）；
- 武術家（Monk）10 族（拳 5、爪 5，已達完全平衡）；
- 法師（Mage）10 族（杖 5、晶 5，由黑曜金龜補齊至完全平衡）；
- 遊俠（Ranger）此前在 60 族中擁有 9 款動物素體（機關弓 5 款、火槍 4 款）；
- **本提案第六十一種動物正式作為「第十巡第六順位」收官擴充，歸屬於遊俠 (Ranger) 體系，原生武器掛載於 `gun`（火槍 / 遊俠·銃）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`遊俠 (Ranger)`**；
- 彩喙巨嘴鳥的加入，使全遊戲遊俠火槍素體擴充至第 5 款，遊俠總數達成 10 款，機關弓（5 款）與火槍（5 款）達成完全對稱的平衡格局！**全遊戲六大職業正式達成各 10 族、十二大武器系統 5:5 完美對稱的大滿貫**！

### 1.2 彩喙巨嘴鳥武器選擇：【林冠聚能氣動銃（Canopy Prism Pneumatic Arquebus）】

彩喙巨嘴鳥原生專屬武器定名為：**【林冠聚能氣動銃（Canopy Prism Pneumatic Arquebus）】**。  
該武器**完全精準對齊並落地於 `docs/world/regions/R03_EMERALD_WOODS.md` 翡翠深林·發條蔓谷之機械巨木與樹汁導流氣動體系**！  
底層完全掛載於 `weapon_classes.json` 的 `gun`（遊俠·銃）類別，享有 `gun` 既有的「一響定生死」標籤宣言（Tagline: `\"一響定生死\"`）、爆發極高、遠距離秒殺機會、打中極爽之特性（`atk: 5, def: -1, hp: -6, crit: 4.0, speed: 0`），完美呼應 `R03_EMERALD_WOODS.md` 第 6 行「局域走時狀態：慢速延遲伴隨規律停拍，秒針每隔 3~4 秒跳動一格，並伴隨約 0.9 秒短暫定格停拍；停拍間隙深林動能自鎖，唯有掌握停拍節律者方能穿行於風切之中」之深林呼吸節奏與超視距狙擊點射手感！

- **法源素材咬合**：  
  完全對應 `R03_EMERALD_WOODS.md` 第 4 行代表材質「人造短絨苔蘚、沖壓雕花薄銅板、分節金屬藤蔓與注塑樹脂發光菌菇套件」、第 20 行「機械巨木（Brass Canopy Giants）」、「手刷墨綠耐磨漆面」與「金屬防鏽齒輪樹汁（Copper Sap）」透明耐壓玻璃管道、第 21 行「發條藤蔓（Clockwork Vines）」、第 22 行「樹脂發光菌菇（Luminescent Resin Mushrooms）」以及第 25 行「丁達爾發條晨曦光斑（Tyndall Clockwork Godrays）（#D4F7D0）」，將林冠古樹的黃銅氣動導管與光學折射原理轉譯為高空狙擊銃。
- **單持規範遵守（0-MKT7）**：  
  遵循 `review.md 0-MKT7` 單持規範，右手單持長管沖壓黃銅氣動火銃，左手穩穩托握槍身下方帶有軟木防滑握把的護木，槍托精密抵住右肩金屬關節，全圖精確為 1 把單持火銃，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- **既有武器 ID 對齊（嚴格遵守規範）**：  
  在資料表關聯層，原生武器可完全向下相容掛載既有 `equipment.json` 中 `slot: \"weapon\"`、`line: \"gun\"` 的相容裝備 `flint_gun`（燧發火銃，tier 1，`atk: 10, def: 0, hp: 0, crit: 8, crit_dmg: 20`），完全不自創新武器體系，不破壞既有數值平衡。

### 1.3 差異化定位：與既有 4 款火槍遊俠（蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥）絕不撞型之論證

雖然彩喙巨嘴鳥與蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥同屬 `ranger`（遊俠）火槍（`gun`）體系，但在**戰術流派與戰鬥風格**、**動能來源與步法力學**以及**材質剪影與視覺語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機螢幕上於 0.5 秒內清晰辨識：

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               遊俠職業火槍系五族差異化對照表（企鵝 vs 浣熊 vs 狐獴 vs 啄木鳥 vs 巨嘴鳥）                            │
├─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┤
│ 維度            │ 蒸氣企鵝 (Penguin)   │ 星巡浣熊 (Raccoon)   │ 沙哨狐獴 (Meerkat)   │ 振律啄木鳥(Woodpecker│ 彩喙巨嘴鳥 (Toucan) │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────┤
│ 1. 戰鬥流派     │ 近距雙管蒸氣爆射     │ 失重滑行、脈衝過載   │ 三腳架潛望超遠狙擊   │ 垂直管道錨定高頻點射 │ 林冠高枝折光看破狙擊│
│ 2. 動能來源     │ 雙聯高壓冷凝蒸氣缸   │ 微型引力反推伺服盒   │ 重型螺旋避震彈簧     │ 活塞高頻往復振律泵   │ 三葉旋翼分段氣動氣缸│
│ 3. 步法特徵     │ 搖擺滑步、肚皮制動   │ 零重力懸浮滑行       │ 三點直立測距立樁     │ 垂直爪鉤樹幹固定貼附 │ 雙爪扣枝側躍、尾翼展│
│ 4. 武器構造     │ 雙管並聯短銃配壓力表 │ 流線型聚合物脈衝導軌 │ 加長螺栓鐵皮銃配地刺 │ 八角形氣動重銃配音叉 │ 雕花沖壓長銃配轉輪盤│
│ 5. 主題界域     │ R05 琉璃汪洋·發條海淵│ R07 星穹軌道·外星基地│ R08 荒漠齒輪塚·遺忘庫│ R04 黃銅都市·巨輪城  │ R03 翡翠深林·發條蔓谷│
│ 6. 材質質感     │ 鍍鈦合金、防水防凍釉 │ 輕量聚合物、電鍍鋁   │ 磨損馬口鐵、防鏽清漆 │ 耐磨深灰鑄鐵、黃銅音叉│ 沖壓薄銅板、彩釉瓷板│
│ 7. 角色剪影     │ 圓滾矮胖直立企鵝偶   │ 環紋粗尾、失重護目鏡 │ 瘦長筆挺、三腳支撐尾 │ 堅硬長喙、三點抗震尾 │ 2.2頭身矮萌多巴胺彩喙│
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴守 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md`，100% 徹底清除所有真皮毛、皮革、生物真羽毛、動物肉身與泥土髒污，全面轉譯為精緻古典林冠發條自動鳥偶機械質感：

- **沖壓雕花薄銅板羽紋板件與輕量化合金底盤**：彩喙巨嘴鳥的身軀絕非生物鳥類羽毛或血肉，而是由沖壓雕花薄銅板（Stamped Brass Plates #FFD028 / #4ED86A）與輕量化鋁合金骨架鉚接而成，體態呈現 2.0 ~ 2.2 頭身矮萌微胖 Q 版造型。胸部鑲嵌溫潤細緻的**象牙白彩釉白瓷喉胸板（#FFFDF8）**，表面飾以多巴胺落日暖橘（#FFA010）琺瑯漸層線條。雙足為粗壯圓潤的精工黃銅三叉球窩鳥爪（#FFD028），爪底配備耐磨橡膠防滑抓握墊，能在機械樹枝與管線上穩固抓握，絕無任何生物組織。
- **多層沖壓鏤空黃銅彩晶巨嘴面罩**：巨嘴鳥最具標誌性的巨大鳥喙，被轉譯為**多層沖壓鏤空黃銅彩晶巨嘴面罩（Prism-Bill Brass Visor Cowl）**。喙部本體由輕質黃銅薄板沖壓成型，表面施以明亮鮮豔的多巴胺四色彩釉漸層（檸檬黃 #FFD028 -> 落日橙 #FFA010 -> 薄荷綠 #4ED86A -> 海藍 #38A0FF）。巨喙內部鏤空中空，巧妙容納光學測距稜鏡與氣動微型減速閥門，上喙前端設有微型氣動排氣孔，射擊時排出細密蒸氣；頭頂延伸出一簇小巧俏皮的沖壓薄銅板羽冠（#4ED86A），完全杜絕任何有機生物組織。
- **翡翠石英雙凸瞄準目鏡**：面罩兩側眼眶處精準鏤空，鑲嵌一對清澈透明的雙凸翡翠石英透鏡（Emerald Quartz Monocle #4ED86A / #38A0FF）。眼周手工繪製深藍紫立體防眩光描邊（#1F1A3A），蓄力狙擊時，鏡片內部顯現金色同心圓十字瞄準標線光紋，溫暖純淨，充滿古典光學測距儀器的精緻感。
- **蔓谷探險巡林獵裝**：身著由耐磨帆布與薄銅片包邊裁切的**蔓谷探險巡林獵裝（Vine Valley Scout Harness）**。主體為多巴胺薄荷淺綠（#4ED86A），領口與下擺飾有落日暖橘（#FFA010）防風滾邊與微型黃銅小排扣，背後預留發條插孔，腰間掛載微型黃銅發條齒輪彈匣包，散發出陽光探險家的活潑朝氣。
- **折扇式沖壓薄銅板導航尾羽**：後腰部位裝配一具**折扇式沖壓薄銅板導航尾羽（Segmented Copper Rudder Tail #FFD028 / #38A0FF）**。由三片疊合的沖壓羽紋銅板以微型發條鉸鏈相連，跳躍與射擊時如折扇般靈巧展開，提供氣動制動與跳躍平衡，下端飾有海藍色琺瑯彩繪。
- **三葉林冠旋翼黃銅發條鑰匙**：背部中央挺立一枚**「三葉林冠旋翼黃銅發條鑰匙（Tri-Vane Canopy Rotor Brass Key #FFD028 / #4ED86A）」**，造型宛如微型三葉螺旋槳，邊緣圓潤無銳角，中心固定一枚珊瑚粉防塵鉚釘（#FF5E8A），隨深林秒針每 3~4 秒跳動一格勻速自轉。

### 2.2 2.2 頭身 Q 版矮萌人體工學與多巴胺鮮亮色彩規範

嚴格遵循 Kevin 與使用者畫像核心審美原則：
- **比例**：矮萌可愛的 2.0 ~ 2.2 頭身比，頭部帶有標誌性的大號彩晶巨喙，身體圓潤矮胖，雙爪穩健抓握，側身微偏持槍瞄準，姿態靈動活潑。
- **多巴胺鮮亮高飽和色盤（拒絕暗黑泥土灰黑）**：
  - **奶油米白底色（#FFFDF8）**：象牙白彩釉白瓷喉胸板、腹部高光，溫潤明亮，清爽無污漬。
  - **多巴胺金黃（#FFD028）**：彩晶巨喙基底、三葉發條鑰匙、黃銅三叉爪、槍管雕花與齒輪彈匣。
  - **多巴胺落日暖橘（#FFA010）**：巨喙漸層中段、工裝防風滾邊、瞄準鏡十字光紋。
  - **多巴胺薄荷淺綠（#4ED86A）**：巡林工裝獵裝主色、頭頂羽冠、翡翠石英目鏡、巨喙漸層下緣。
  - **多巴胺天藍（#38A0FF）**：巨喙尖端彩釉、導航尾羽裝飾條、洩壓蒸氣微光。
  - **多巴胺珊瑚粉（#FF5E8A）**：發條鑰匙中心鉚釘、腰間彈匣包縫線標記。
  - **深藍紫立體手繪描邊（#1F1A3A）**：取代傳統髒黑泥土色，勾勒金屬板件邊緣，賦予強烈的手繪通透感。

### 2.3 待機小動作、呼吸感與 Poke 點擊互動

拒絕靜止死板木樁，為彩喙巨嘴鳥設計活靈活現的 Q 版發條動態：
- **待機呼吸感（Idle Breathing）**：
  - 2.2 頭身身軀每隔 3~4 秒配合深林走時律動進行一次微幅上下起伏，胸前白瓷板件與羽紋銅片輕微收放；
  - 右手托持的林冠氣動銃槍口微幅上下點動，左手輕扶護木，巨喙前端每隔數秒吐出微縮白色水霧蒸氣；
  - 背部三葉螺旋發條鑰匙隨秒針跳拍勻速旋轉，導航尾羽如折扇般輕巧微晃。
- **待機專屬小動作（Special Idle Animations）**：
  - **「巨喙調焦與排氣」**：每隔 8 秒，巨嘴鳥將巨大鳥喙向下微壓，眼部翡翠石英透鏡閃爍出同心圓十字光標，隨後上喙輕微張開「哧——」地噴出一圈薄荷綠色氣壓煙圈，頭頂羽冠俏皮地彈動兩下；
  - **「轉輪上膛」**：左手拇指撥動氣動銃側面的發條供彈轉輪，發出連續三聲清脆的「咔、嗒、叮！」機械齒輪咬合聲，隨後自信地將槍口斜上一揚。
- **Poke 點擊互動（點擊反應反饋）**：
  - 玩家以手指點擊角色時，彩喙巨嘴鳥如受驚的小機關鳥般雙爪原地高高跳起半公尺，導航尾羽在空中完全展開成扇面，在半空中輕巧翻轉半圈後穩穩落地；
  - 頭頂彈出俏皮對話氣泡：「**這片林冠的每一根發條藤蔓，都在我的彩晶十字線裡！**」或「**別看我嘴大，一響定生死從不失手！**」，周身爆散出 4~6 枚檸檬黃微型齒輪與薄荷綠晶芒火花粒子。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 終結 R03 翡翠深林·發條蔓谷無火槍手之歷史空白

在全專案九大界域中，中層浮空林地界域 `R03 翡翠深林·發條蔓谷` 先前擁有 7 族，涵蓋輕靈法杖（靈尾狐）、高速機關鏢（碧簧蛙）、敏捷短弓（翠角鹿）、西洋花劍（巡林松鼠）、突進機關爪（疾影神隼）、工程巨斧（劈木河狸）與定點重鎚（風箱毛蟲）。  
然而，面對深林高層機械巨木（Brass Canopy Giants）頂部縱橫交錯的發條藤蔓、遠距樹屋聚落間的警戒盲區、以及深林停拍節奏下的突發危機，**長久以來完全缺乏一位能夠站在制高點樹冠平台、以精密光學鏡片測距、無視藤蔓阻隔以高壓氣動重銃定點貫穿的「火槍遊俠 (Ranger·Gun)」核心素體**。彩喙巨嘴鳥的入駐，徹底補齊了 R03 最具戰術威懾的高空光學狙擊防線！

### 3.2 100% 逐字對齊引用 `docs/world/regions/R03_EMERALD_WOODS.md` 既有地標與設定

本提案中所有世界觀敘事、任務情境與巡邏路線，**100% 逐字引用自官方區域檔案 `docs/world/regions/R03_EMERALD_WOODS.md`，絕對零自創地標**（嚴格遵守 `review.md` 0-PLAN1 規範）：

- **穿行巡檢地標**：
  - 終年棲息駐守於高聳入雲的**「機械巨木（Brass Canopy Giants）」**（`R03_EMERALD_WOODS.md` 第 20 行）樹冠最高處觀測平台，以彩晶巨喙內置透鏡穿透**「手刷墨綠耐磨漆面」**枝幹間流動的**「金屬防鏽齒輪樹汁（Copper Sap）」**透明玻璃管道，監測全林區動能；
  - 穿梭於盤根錯節的**「發條藤蔓（Clockwork Vines）」**（`R03_EMERALD_WOODS.md` 第 21 行）之間，利用螺旋軟鋼絲與小銅環構成的滑索高空巡邏；
  - 巡防以輕量化松木拼板搭蓋的**「樹屋聚落（Treehouse Enclave）」**（`R03_EMERALD_WOODS.md` 第 23 行），乘搭**「發條繩索滑輪吊籃」**在各樹冠平台間提供高空火力庇護；
  - 俯瞰下方林地步道上盛開的**「樹脂發光菌菇（Luminescent Resin Mushrooms）」**（`R03_EMERALD_WOODS.md` 第 22 行），為在半透明翠綠與檸檬黃柔光中夜行的發條居民提供防衛警戒；
  - 借力林冠灑落的**「丁達爾發條晨曦光斑（Tyndall Clockwork Godrays）（#D4F7D0）」**（`R03_EMERALD_WOODS.md` 第 25 行），校準翡翠石英目鏡的折射角與射擊彈道；
  - 駐防深林西南林緣懸崖的**「蔓谷天梯引道·深林站（Vine Valley Stairway Terminal）」**（`R03_EMERALD_WOODS.md` 第 30 行），監控自區域 2 晨曦小鎮（R02）升降而來的齒輪天梯；
  - 巡守深林西側林緣巨木觀測台下方的**「晨曦天軌 3 號月台（Dawn Rail Platform 3）」**（`R03_EMERALD_WOODS.md` 第 31 行），護送來自中央浮空島天宮大廳的發條懸浮吊艙；
  - 遠眺北側邊境通往區域 4 黃銅都市的**「高架重軌引橋·巨輪城站（High Brass Viaduct Gate）」**（`R03_EMERALD_WOODS.md` 第 33 行）與東南深谷通往區域 6 赤焰熔爐的**「赤焰索道懸橋（Crucible Ropeway Chasm）」**（第 34 行）；
  - 依託展台外緣由高彈鋼絲與綠色矽膠套編織的**「防護金屬藤蔓彈力網（Perimeter Vine-Spring Net）」**（`R03_EMERALD_WOODS.md` 第 36 行），演練高空跳躍滑翔與失足反彈緩衝戰術；
  - 每日降落至巨木根部的**「樹汁導流泵」**（`R03_EMERALD_WOODS.md` 第 48 行）取用純淨天然潤滑樹脂保養氣動銃氣缸。
- **核心 NPC 互動情境**：
  - 與林地外緣的**守林哨兵·風耳（Windear the Forest Watcher）**（`R03_EMERALD_WOODS.md` 第 56 行）組成地面長耳測候與高空巨嘴狙擊的經典射手搭檔，在深林秒針「停拍定格」瞬間，風耳指引風切方向，彩喙巨嘴鳥以氣動銃瞬發破障；
  - 拜訪聚落中的**靈尾工藝師·小鈴（Suzu the Bell-Tailed Fox）**（`R03_EMERALD_WOODS.md` 第 65 行），請小鈴以尾尖發條共鳴鈴鐺校準銃管發條彈匣的諧振頻率，並調校翡翠瞄準鏡片；
  - 守護地面結隊巡邏的**「守林發條小鹿（Clockwork Fawns）」**（第 44 行）、傳遞零件的**「發條松鼠信差（Wind-up Squirrel Couriers）」**（第 45 行）以及維修金屬藤蔓的**「林木守護木偶（Arbor Sentinel Marionettes）」**（第 46 行）。
- **守護泰坦作戰支援**：
  - 面對深林中央失控狂暴的守護泰坦**「疾影神隼」**（`R03_EMERALD_WOODS.md` 第 51 行）掀起的毀滅性金屬風切，彩喙巨嘴鳥憑藉巨喙測距鏡精準捕捉神隼俯衝時的停拍間隙，以高壓氣動光彈點射破壞神隼的翼尖動能棘輪，支援小白成功平息風切危機！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

依據專案核心紙娃娃規格書 `docs/design/paperdoll_slots.json`，彩喙巨嘴鳥的 7 大獨立部件槽位與專屬武器拆解如下：

### 4.1 核心槽位拆解矩陣

```
┌─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 部件槽位 (Slot) │ 彩喙巨嘴鳥專屬造型規格與材質特徵（嚴守 100% 零真皮毛、零皮革、零生鏽、零污漬）                  │
├─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. chassis (素體)│ 林冠輕量化合金素體底盤（#FFFDF8 / #FFD028），沖壓薄銅板骨架配象牙白瓷喉胸板，黃銅球窩三叉鳥爪   │
│ 2. head_unit(頭)│ 彩晶折光巨嘴面罩（#FFD028 / #FFA010 / #4ED86A），沖壓多層鏤空黃銅彩晶巨喙，前額飾翠綠琺瑯羽冠  │
│ 3. optic_core(眼)│ 翡翠石英瞄準目鏡（#4ED86A / #38A0FF），高透光雙凸翡翠石英鏡片嵌深藍紫眼眶，內刻十字瞄準標線   │
│ 4. costume (服裝)│ 蔓谷探險巡林獵裝（#4ED86A / #FFA010），薄荷綠耐磨工裝短馬甲，飾落日暖橘防風滾邊與微型黃銅排扣   │
│ 5. back_curio   │ 多節沖壓銅片導航尾翼（#FFD028 / #38A0FF），三聯折扇式沖壓薄銅板舵羽，隨跳躍展開維持空力平衡   │
│ 6. winding_key  │ 三葉林冠旋翼黃銅發條鑰匙（#FFD028 / #4ED86A），三葉微型螺旋槳造型，中心嵌珊瑚粉防塵鉚釘         │
│ 7. weapon (武器)│ 林冠聚能氣動銃（#FFD028 / #2B2630 / #4ED86A），右手單持長管黃銅氣動銃，側置轉輪發條供彈盤     │
└─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 部件細節深入描述

1. **`chassis`（素體底盤）**：  
   2.0 ~ 2.2 頭身 Q 版矮萌微胖金屬鳥偶身軀，由沖壓雕花薄銅板（#FFD028）與輕量化耐蝕合金骨架鉚接而成。喉胸部位鑲嵌光潔溫潤的象牙白彩釉白瓷襯板（#FFFDF8），胸前帶有精緻的微型排氣散熱閥門刻線。雙足為粗壯圓潤的精工黃銅三叉球窩鳥爪，爪底配有耐磨黑色橡膠抓握墊，抓握在機械巨木枝幹上平穩紮實，發出清脆有力的金屬踏音，徹底杜絕任何真實生物外殼或肉身質感。
2. **`head_unit`（頭部面罩）**：  
   標誌性的多層沖壓鏤空黃銅彩晶巨喙面罩。面罩本體呈現經典巨嘴鳥誇張的弧形幾何輪廓，表面塗刷高光多巴胺四色彩釉漸層（檸檬黃 #FFD028 -> 落日暖橘 #FFA010 -> 薄荷綠 #4ED86A -> 海藍 #38A0FF），巨喙內部鏤空可見微型氣動閥門與石英稜鏡導軌，前額挺立著一簇沖壓薄銅板翠綠羽冠（#4ED86A），兼具發條玩具的童趣與精密儀器的工藝感。
3. **`optic_core`（瞄準目鏡）**：  
   一對圓潤清澈的雙凸翡翠石英瞄準透鏡（#4ED86A / #38A0FF）。眼周施以深藍紫（#1F1A3A）立體防眩光手繪外框，目光敏銳專注。蓄力瞄準時，鏡片中心泛起微縮金色同心圓十字狙擊標線，透光溫暖清澈，絕無恐怖複眼或鏡片裂紋。
4. **`costume`（巡林獵裝）**：  
   由高飽和薄荷淺綠（#4ED86A）耐磨帆布與薄銅片包邊裁切的探險巡林短馬甲。前襟配備四枚精巧的黃銅圓排扣，領口與下擺飾有落日暖橘（#FFA010）防風滾邊，背部精確預留發條插孔，腰帶兩側懸掛微型黃銅發條齒輪彈匣盒，充分展現林冠遊俠的冒險家風采。
5. **`back_curio`（導航尾翼）**：  
   安裝於後腰微型球形鉸鏈上的折扇式沖壓薄銅板導航尾翼（#FFD028 / #38A0FF）。由三片沖壓羽紋薄銅板疊合而成，尾片端部飾以多巴胺天藍色彩繪。平時自然下垂微晃，跳躍與射擊時如折扇般展開成扇形，提供空氣阻尼與平衡配重。
6. **`winding_key`（三葉旋翼發條鑰匙）**：  
   背部中央挺立的三葉林冠旋翼黃銅發條鑰匙。採用深林耐磨黃銅（#FFD028）精密鑄造，造型宛如一具微型三葉螺旋槳，扇葉邊緣施以薄荷綠（#4ED86A）烤漆包邊，中心固定一枚珊瑚粉防塵鉚釘（#FF5E8A）。隨深林秒針每 3~4 秒跳動一格勻速自轉，發出微弱清脆的齒輪咬合聲。
7. **`weapon`（林冠聚能氣動銃）**：  
   彩喙巨嘴鳥專屬武器【林冠聚能氣動銃】。右手單持長管雕花黃銅氣動銃（#FFD028 / #2B2630），槍身前段裝配花瓣形洩壓制退器，中段配備軟木握把與發條增壓氣缸，側置圓盤形轉輪發條供彈盒，左手穩穩托握護木。擊發時，槍口噴出一團高壓白色蒸氣與翠綠色聚能光彈，音效響亮乾脆。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格依循專案六大標準戰鬥姿態（`poses/` 規範，128x128 像素基準與 512x512 LANCZOS 高清雙規格）：

```
┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────┐
│ 姿態標籤 (Pose)   │ 姿態動作描述與機械運動節奏（完全符合 2.2 頭身 Q 版人體工學）                                  │
├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. idle (待機)    │ 側面微側30度穩健高枝站姿，雙爪緊扣踏板，雙手托持氣動銃斜向上45度，巨嘴面罩前傾，目鏡微光流轉  │
│ 2. attack (普攻)  │ 踏步半蹲，氣動銃前平舉穩固擊發，槍口爆出一團薄荷綠與金黃色高壓蒸氣彈芒，巨喙微張排氣洩壓       │
│ 3. hit (受擊)     │ 身軀受震向後微仰，雙爪滑步抓地卸力，導航尾羽向下展開充當煞車阻尼，面罩排氣孔噴出急促白色蒸氣 │
│ 4. recover (硬直) │ 雙足蹬地彈起復位，左手拇指撥動供彈轉輪發出「咔嗒」上膛聲，頭頂羽冠抖動校準，迅速重組狙擊站姿 │
│ 5. skill (技能)   │ 雙足發力躍起半空，背部發條旋翼超頻急轉，雙手握銃向下三段連射高壓光彈，在地面炸裂出環形翠綠波 │
│ 6. telegraph (蓄力│ 深度下沉重心，三叉鳥爪鎖定地面，銃管與巨喙同軸對準目標，目鏡十字光紋劇烈閃爍，周身匯聚金綠光 │
└───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

依據 `docs/PRODUCT_LOCK_0.20.md` 第 9 章准入門檻硬規則逐條答辯：

### Q1：它掛在哪個核心循環的哪一環？
**答**：掛載於 §3.1 核心循環的**第二環「出征戰鬥與關卡推進（Combat & Exploration）」**與**第四環「外觀展示與角色收集（Collection & Customization）」**。作為遊俠職業火槍系的核心擴充素體，直接提供超視距爆發狙殺、讀秒看破停拍、部位精確貫穿與高爽快打擊感的射擊體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
**答**：服務第一優先支柱**「爽快打擊與看破手感（Timing & Precision Break）」**（透過火槍職業「一響定生死」機制，在敵人招式停拍定格瞬間抓準時機擊發高爆光彈觸發暴擊秒殺），以及第二優先支柱**「被遺忘的發條童話世界觀（Forgotten Clockwork Fairy Tale）」**（以 2.2 頭身沖壓薄銅板、彩晶多巴胺巨喙與發條鳥偶體現翡翠深林的冒險童話魅力）。

### Q3：玩家在手機上用單手拇指能不能操作它？
**答**：**能**。完全相容於既有橫屏雙拇指操作配置，火槍點射自帶智能遠程鎖定與弱點吸附判定，單拇指即可輕鬆完成點擊點射、長按精準狙擊與滑動釋放高空散射絕招。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
**答**：**不需要**。100% 本機離線運算，紙娃娃切片與動作姿態完全儲存於客戶端本機資料夾，嚴守「零連線可通關」鐵律。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
**答**：**不會**。  
據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況：「Web 目錄 135 MB 且尚未達標，首包瘦身是既有欠帳、不因本提案消解」。  
本提案為**純規格與世界觀文本檔案（約 50 KB）**，不產出任何圖素與二進位資產，不增加首包負擔；後續若實作圖素資產，將嚴格依循 128x128 索引色切片與紋理壓縮規範，增量小於 150 KB。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
**答**：  
1. **放棄真實鳥類生物羽毛、肉質鳥喙與飛行滯空能力**：徹底放棄自然界鳥類的生物羽毛組織與令人生畏的尖銳角質，全面轉譯為 2.2 頭身矮萌沖壓薄銅板羽紋、圓潤白瓷胸板與多巴胺彩晶黃銅巨喙，放棄無限制長時間空中飛行，限制為雙足扣枝短暫跳躍滑翔，以換取手機螢幕上的高親和力、高辨識度與發條玩具童趣質感；  
2. **放棄雙持雙槍或重型加特林機槍的繁雜視覺方案**：為了避免在手機小螢幕上複雜槍械結構造成嚴重視覺遮擋與掉幀，放棄設計雙持或多管旋轉機槍，嚴格遵守 `0-MKT7` 單持規範，改為右手單持一把結構清晰、帶側置轉輪彈匣的「林冠聚能氣動銃」，左手維持托握護木的沉穩射手姿態。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置：

```json
{
  "race_id": "toucan",
  "aliases": [
    "prism_bill_toucan",
    "canopy_toucan",
    "clockwork_toucan",
    "emerald_toucan",
    "prism_toucan"
  ],
  "name_zh": "彩喙巨嘴鳥",
  "name_en": "The Prism-Bill Toucan",
  "class_archetype": "遊俠 (Ranger)",
  "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
  "lore_anchor": "駐守於翡翠深林·發條蔓谷「機械巨木」樹冠頂部觀測平台，穿行於「發條藤蔓」與「樹屋聚落」各樹冠平台，沐浴「丁達爾發條晨曦光斑」，仰望「高架重軌引橋·巨輪城站」與「赤焰索道懸橋」，巡檢「蔓谷天梯引道·深林站」與「晨曦天軌 3 號月台」，依託「防護金屬藤蔓彈力網」與「樹脂發光菌菇」，在「樹汁導流泵」前保養氣缸，結伴守林哨兵·風耳、靈尾工藝師·小鈴，庇護守林發條小鹿、發條松鼠信差與林木守護木偶；通體覆蓋沖壓雕花薄銅板合金底盤與象牙白瓷喉胸板、多層沖壓鏤空黃銅彩晶巨嘴面罩、翡翠石英瞄準目鏡、蔓谷探險巡林獵裝、折扇式沖壓薄銅板導航尾羽、三葉林冠旋翼黃銅發條鑰匙，右手單持專屬林冠聚能氣動銃，以2.2頭身矮萌微胖體態、粗壯黃銅三叉爪扣枝、林冠光學測距與遠距定點一響定生死見長的深林高空遊俠",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1910s-1930s 歐洲古典發條鐵皮鳥偶與維多利亞光學測候偶)",
    "posture": "2.2 頭身矮萌身軀微側30度高枝站姿，雙爪穩固扣握踏板，右手單持氣動火銃斜指前上方，左手托握護木，彩晶巨嘴前傾測距，背後三葉發條鑰匙隨深林秒針每3~4秒跳拍一格勻速自轉",
    "standee_height_px": 840,
    "standee_width_px": 420
  },
  "mechanical_features": {
    "head_and_neck": "沖壓薄銅板圓形頭盔配彩晶巨喙面罩（#FFD028 / #FFA010 / #4ED86A / #38A0FF），前額挺立沖壓薄銅板羽冠，兩腮鑲嵌溫潤象牙白瓷板（#FFFDF8），眼眶處鏤空透光",
    "ears": "無外耳，以頭頂三片分層沖壓薄銅板羽冠替代，隨林間微風與氣壓波動微幅彈動",
    "torso_and_limbs": "沖壓雕花薄銅板與輕量化合金骨架外殼，胸腹鑲嵌象牙白瓷喉胸襯板，雙足為粗壯精工黃銅三叉球窩鳥爪配耐磨橡膠防滑抓握墊",
    "tail": "折扇式沖壓薄銅板導航尾羽（#FFD028 / #38A0FF），三聯折扇式沖壓薄銅片以微型發條鉸鏈相連，提供跳躍氣動制動",
    "weapon_system": "右手單持專屬「林冠聚能氣動銃（Canopy Prism Pneumatic Arquebus）」，雕花長管配花瓣形洩壓制退器與側置轉輪發條供彈盤，底層掛載 equipment.json 既有 flint_gun (tier 1)"
  },
  "color_palette": {
    "base": "#FFFDF8 (基底象牙白彩釉白瓷高光，喉胸襯板與腹部高光)",
    "primary": "#FFD028 (主色多巴胺金黃，彩晶巨喙基底、三葉旋翼鑰匙、黃銅三叉鳥爪與銃身雕花)",
    "secondary": "#4ED86A (次色多巴胺薄荷淺綠，巡林工裝獵裝主色、頭頂羽冠、翡翠石英目鏡)",
    "accent": "#FFA010 (點綴色多巴胺落日暖橘，巨喙漸層中段、工裝防風滾邊、瞄準鏡十字光紋)",
    "detail": "#38A0FF (細節色多巴胺天藍，巨喙尖端彩釉、導航尾羽裝飾飾條、洩壓蒸氣微光)",
    "metal": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心鉚釘與彈匣包縫線標記)",
    "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
  },
  "asset_naming_conventions": {
    "status": {
      "existing": [],
      "pending": [
        "branding/char_toucan.png (品牌形象立牌)",
        "web/media/hero/char_toucan.png (官網英雄展示立繪)",
        "docs/art/prism_bill_toucan_concept.png (概念立繪)",
        "game/assets/sprites/player/toucan_idle.png (64x64 待機)",
        "game/assets/sprites/player/toucan_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/toucan_idle.png (隊伍待機)",
        "web/media/hero/toucan_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/toucan_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/toucan_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/toucan_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/toucan_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/toucan_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/toucan_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/toucan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/toucan.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/toucan_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/prism_bill_toucan.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/toucan/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
      ]
    },
    "branding_standee": "branding/char_toucan.png (420x840 -> 1344x1680) [待產出]",
    "branding_concept_art": "docs/art/prism_bill_toucan_concept.png (928x1152) [待產出]",
    "web_hero": "web/media/hero/char_toucan.png (420x840 -> 1344x1680) [待產出]",
    "web_preview": "web/media/hero/toucan_idle.png (128x128) [待產出]",
    "game_sprite_idle_base": "game/assets/sprites/player/toucan_idle.png (64x64) [待產出]",
    "game_sprite_idle_hi": "game/assets/sprites/player/toucan_idle_x3.png (128x128) [待產出]",
    "game_sprite_party_idle": "game/assets/sprites/player/party/toucan_idle.png (128x128) [待產出]",
    "game_sprite_battle": "game/assets/sprites/player/toucan_battle.png (128x128) [待產出]",
    "game_sprite_walk": "game/assets/sprites/player/toucan_walk_{0..3}.png (64x64) [待產出]",
    "game_sprite_walk_hi": "game/assets/sprites/player/toucan_walk_{0..3}_x3.png (128x128) [待產出]",
    "game_action_poses": "game/assets/sprites/player/poses/toucan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
    "portrait_hud": "game/assets/sprites/portraits/toucan.png (128x128) [待產出]",
    "portrait_dialogue": "game/assets/sprites/portraits/prism_bill_toucan.png (384x480) [待產出]",
    "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/toucan/{slot_id}/{item_id}.png [待產出]"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⚠️ **執行提醒（嚴守任務邊界）**：本任務為「只寫文件，不產圖不產片」。以下提示詞僅作企劃歸檔與規格預置，等待後續美術產圖任務由 sideart 領取執行。

### 8.1 彩喙巨嘴鳥角色單體立繪 Prompt（4:5 垂直角色畫）

```text
masterpiece, best quality, 2.2 head-to-body ratio chibi cute clockwork mechanical toy toucan ranger hero, named The Prism-Bill Toucan, standing firmly on a mossy brass tree branch pedestal in Emerald Woods. Made of stamped copper plumage plates, lightweight aluminum frame, glazed ivory-white porcelain throat plate, and gleaming brass joint spheres. Distinctive oversized cute toy prism toucan bill made of hollow stamped brass with vibrant gradient enamel colors (lemon yellow #FFD028, sunset orange #FFA010, mint green #4ED86A, and sky blue #38A0FF), and a tiny crest of mint green copper feather plates on forehead. Wearing a charming mint green scout vest with warm orange trim and tiny brass buttons, glowing dual emerald quartz monocle eyes with golden crosshair reticle tick marks, and a three-piece segmented copper rudder tail feather at the back. Right hand holding a long ornate stamped brass pneumatic arquebus rifle with a floral muzzle brake and side-mounted clockwork wheel magazine, left hand steadily supporting the foregrip. A prominent tri-vane canopy rotor brass wind-up key mounted on the center back with a coral pink rivet. Clean, dopamine vibrant candy-like colors, lemon yellow #FFD028, sunset orange #FFA010, mint green #4ED86A, sky blue #38A0FF, ivory white #FFFDF8, dark purple-blue outlines #1F1A3A, soft Tyndall forest morning godrays illumination, zero real feathers, zero real fur, zero flesh, zero organic parts, pure mechanical toy bird automaton, 4:5 aspect ratio.
```

### 8.2 彩喙巨嘴鳥翡翠深林場景同框 Prompt（16:9 橫屏戰鬥/宣傳插畫）

```text
panoramic vibrant fairy tale scene in R03 Emerald Woods Vine and Gear Forest. In the center foreground, a 2.2 head-body ratio cute mechanical toy toucan ranger perches bravely on a giant brass tree branch high in the canopy, aiming a long stamped brass pneumatic rifle downwards through winding clockwork vines and glowing resin mushrooms. In the background, majestic stamped brass giant canopy trees, suspended treehouse enclaves with rope-pulley baskets, distant brass viaduct bridges, and soft Tyndall clockwork morning godrays filtering through the green forest dome. Dopamine bright cheerful palette, mint green, lemon yellow, warm orange, ivory white, crisp clockwork toy aesthetic, bold stylized outlines, zero real fur, zero real feathers, cinematic wide-angle 16:9 aspect ratio.
```

### 8.3 產圖執行指令參照（CLI Reference）

```bash
# 產出單體立繪（4:5 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.1 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 4:5 \
  --out docs/art/prism_bill_toucan_concept.png

# 產出宣傳場景橫圖（16:9 比例，強制帶 --ref）
python3 /root/gen_media.py image \
  --prompt "<8.2 Prompt>" \
  --ref branding/key_visual_main.png \
  --aspect 16:9 \
  --out docs/art/prism_bill_toucan_scene.png
```

---

## 九、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **0-PLAN1 第一條：地名／建築名 100% 來自既有區域文件**：  
  全篇嚴格引用 `docs/world/regions/R03_EMERALD_WOODS.md` 既有地標（機械巨木、發條藤蔓、樹脂發光菌菇、樹屋聚落、蔓谷天梯引道·深林站、晨曦天軌 3 號月台、高架重軌引橋·巨輪城站、赤焰索道懸橋、防護金屬藤蔓彈力網、樹汁導流泵）與居民 NPC（守林哨兵·風耳、靈尾工藝師·小鈴、守護泰坦「疾影神隼」），**完全零自創地標**。
- [x] **0-PLAN1 第二條：PRODUCT_LOCK §9 Q5 包體問答據實引用**：  
  完全符合規範，實問實答引用 §5.2「現況 Web 目錄 135 MB 尚未達標，首包瘦身是既有欠帳、不因本提案消解」，不偽稱已達標。
- [x] **0-PLAN1 第三條：origin_realm 編號與名稱完全吻合**：  
  嚴格對齊為 `R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest`，完全吻合。
- [x] **0-PLAN1 第四條：盤點表職業中文名嚴格使用正式名**：  
  全面對齊 `weapon_classes.json` 與 `paperdoll_slots.json`：劍士(Knight)／騎士(Knight)／法師(Mage)／戰士(Viking)／武術家(Monk)／忍者(Ninja)／遊俠(Ranger)，無任何自創花名。
- [x] **23f-1 條款：class_archetype 嚴格對齊六大職業**：  
  正表欄位與全文嚴格標註為單一正式名：`遊俠 (Ranger)`。
- [x] **0-MKT7 條款：單持武器與雙手姿勢規範**：  
  右手單持林冠聚能氣動銃，左手穩穩托握護木，左右肢體姿態描述清晰，0 雙持穿模。
- [x] **CANON 世界憲章零毛皮零皮革鐵律**：  
  100% 零真動物肉身、零生物毛皮、零皮革、零真羽毛、零黏液、零生鏽、零機油污漬；通體轉譯為沖壓雕花薄銅板、輕量化合金底盤、象牙白彩釉白瓷喉胸板、翡翠石英瞄準目鏡、多層沖壓鏤空黃銅彩晶巨喙、折扇式沖壓薄銅板導航尾羽與三葉林冠旋翼黃銅發條鑰匙。
- [x] **遊俠火槍與機關弓對稱平衡**：  
  作為第十巡第六順位收官擴充，補齊遊俠火槍第 5 款，與遊俠機關弓（5 款）達成完全 5:5 對稱平衡！全遊戲六大職業正式達成各 10 族、十二大武器 5:5 完美對稱大滿貫！
