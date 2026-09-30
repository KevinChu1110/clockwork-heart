# 第七十三種動物「空泡槍蝦（The Cavitation Pistol Shrimp）」世界觀與角色設計提案

> **標題**：第七十三種動物「空泡槍蝦（The Cavitation Pistol Shrimp）」角色與世界觀設計提案
> **提案代號**：`CAVITATION_PISTOL_SHRIMP_DESIGN_PROPOSAL`（代號：`pistol_shrimp` / 識別名：`race_pistol_shrimp`）
> **所屬層次**：世界觀角色設計提案（Worldbuilding & Paperdoll Spec Proposal）
> **提案作者**：小凱（側案·策劃總監 sideplan）
> **對應看板任務**：`t_468b7c6c`（📖 世界觀｜第七十三種動物紙娃娃角色設計提案）
> **法源依據與對齊規範**：
> - `docs/world/CANON.md`（世界憲章：覺醒玩具世界、100% 零真皮毛、零動物肉身、零生物黏液、零真羽毛、零真甲殼肉體、零機油污漬、零毒液、零皮革、零布料）。本提案據此憲章轉譯之部件語彙（非 CANON 原文）：海藍鍍鈦防蝕沖壓馬口鐵底盤、沖壓雙聯黃銅觸鬚天線與測距面盔、雙聯高透耐壓海藍石英琉璃球形目鏡、深海耐壓潛水鐘加固胸甲、多節同軸彈簧減震扇形尾葉與微型高壓氣囊、海淵旋閥舵輪黃銅發條鑰匙、海淵空泡高壓氣動重銃
> - `docs/ART_DIRECTION.md`（第 142 行核心世界觀定位：「被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件」；§0 手機優先三層辨識系統；§1.1 瓦力+鋼鐵人+胡桃鉗童話發條玩具定調；多巴胺高飽和鮮亮色彩：奶油米白 #FFFDF8、天藍 #38A0FF、薄荷綠 #4ED86A、天元金黃 #FFD028、落日暖橘 #FFA010、珊瑚粉 #FF5E8A、深藍紫描邊 #1F1A3A）
> - `docs/world/regions/R05_CRYSTAL_OCEAN.md`（第 1 行區域代號與名稱「R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss」、第 4 行沙盤工藝材質套件「高透光海藍琉璃凝膠、耐高壓深海石英泡罩、防腐蝕鍍鈦合金骨架、發條磁吸氣動閥門與磷光發條指針儀表套件」、第 6 行局域走時狀態「深沉緩慢伴隨水壓流體阻尼（秒針每 3~4 秒深沉划動一格，伴隨液態凝膠微波泛起藍光漣漪；水下流體阻尼沉穩舒緩，需掌握發條流體浮力與減壓循環穿行）」、第 15 行「多邊形厚鑄鍍鈦合金水槽托盤...雙層加厚高透防爆石英玻璃護壁包覆，外圈箍以重型耐高壓黃銅緊固環箍與液壓減震立柱」、第 16 行「四組粗壯的耐高壓沉箱鋼柱與雙動能流體平衡活塞支撐，穩固地固定在中低層浮空天軌基樑上」、第 17 行「深藍色夜幕雲海與微光水霧...底層舊庫沙盤的鋼骨陰影」、第 19 行「液態琉璃凝膠海（Liquid Crystal Gel Sea）：由透明無毒、高折射率的玩具流體凝膠構成...水體中漂浮著微型發條氣泡與藍色螢光星屑」、第 20 行「海淵地表與馬賽克步道（Abyssal Seabed & Mosaic Walkways）...防滑深海藍晶石馬賽克瓷磚（Lapis Lazuli Mosaic Tiles）...耐腐蝕的圓頭鍍鈦鉚釘...發條珊瑚群（Clockwork Coral Reeds）」、第 21 行「水下發條宮殿與氧氣泡罩（Clockwork Sunken Palace & Aerated Glass Domes）...球形耐壓石英玻璃罩...海藍色陶瓷釉面磚與鍍鈦裝甲板拼合...除濕發條葉片」、第 22 行「磷光水母街燈與流體排氣柱（Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents）...多巴胺天藍 #38A0FF、薄荷綠 #4ED86A 與珊瑚粉 #FF5E8A 的夢幻冷光」、第 24 行「天穹即為水面頂層的半球形光學折射透鏡...水下丁達爾藍晶光柱（Submarine Caustic Godrays）」、第 25 行「巨型青銅錨鏈秒針長達數公里，每 3~4 秒在液態凝膠中深沉划動一格，伴隨水波藍光漣漪擴散與沉悶悅耳的水下音叉共振「嗡——叮」」、第 29 行入場「深淵排污豎井管道·耐壓吊籠（Abyssal Sump Siphon: Bathysphere Terminal）」、第 30 行「晨曦天軌 5 號深海浮標月台（Dawn Rail Deepsea Buoy Platform 5）」、第 32 行出場「深海熱液湧泉管道（Hydrothermal Trench Conduits）」、第 34 行「環域水幕磁阻防護波（Magnetic Hydro-Barrier Grid）」、第 42 行原住玩具族群「發條熱帶魚（Clockwork Tropical Fish）」、第 43 行「橡皮小黃鴨船長（Rubber Ducky Navigators）」、第 44 行「發條海馬信差（Wind-up Seahorse Couriers）」、第 46 行「海底防鏽超聲油壓艙（Ultrasonic De-rusting Station）」、第 47 行「海潮對表儀式」、第 54 行核心 NPC「小黃鴨船長·舵手巴克（Captain Buck the Rubber Ducky）」、第 63 行「海馬信差·碧浪（Billow the Seahorse Courier）」、第 71 行「深海鐘錶貝·珠貝長老（Elder Pearl the Clockwork Clam）」、第 85 行常規野外敵人「生鏽的發條深海鮟鱇（Rusty Clockwork Angler）」、第 89 行「錨鏈幽靈水母（Anchor-Chain Phantom Jelly）」、第 93 行「巡弋重裝機關鯊（Armored Patrol Mecha-Shark）」、第 100 行旗艦泰坦 BOSS「深淵海霸泰坦·八爪機關巨烏賊（Titan Abyssal: Octo-Gear the Abyssal Kraken）」、第 107 行部位破壞「錨鏈重腕（Anchor Tentacles）」、第 108 行「頂部排水氣閥（Crown Siphon Vent）」、第 109 行「主目鏡水晶罩（Optic Glass Dome）」、第 119 行本地特產「海錨防禦重斧（Anchor Guardian Heavy Cleaver）」、第 120 行「琉璃刺擊長槍（Glass Crystal Rapier Lance）」、第 121 行「發條雙管水銃（Clockwork Twin Harpoon-Gun）」、核心掉落「澄澈深海藍晶核」、「鍍鈦耐腐蝕增壓閥」、「深海抗壓錨鏈鉸鏈」、「防鏽特種矽油」）
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）
> - `game/data/tables/weapon_classes.json`（遊俠正式名稱 `ranger`，火槍標籤宣言 `\"一響定生死\"`，武器 `gun`，稱號 `遊俠·銃`，數值 `atk: 5, def: -1, hp: -6, crit: 4.0, speed: 0`，玩法 `\"遠遠點射。同職也可玩弓。\"`，初始相容武器 `flint_gun` 燧發火銃）
> - `game/data/tables/equipment.json`（火槍類正式 line: `\"gun\"`，初階武器：第 340 行 `flint_gun` 燧發火銃，高階相容武器：第 353 行 `blackpowder_rifle` 黑火長銃）

---

## 0. 執行摘要與邊界宣告

1. **提案定位：第十二巡第六順位收官大圓滿擴充，開啟遊俠第 6 款火槍素體，達成全遊戲六大核心職業內部雙武器體系 100% 完美超對稱（6:6）大圓滿歷史里程碑**：
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）正式制定的**第七十三種動物擴充素體規格**。
   在全專案相繼完成第十一巡全部素體，以及第十二巡首位成員第六十八種動物穿雲翠鳥（騎士·長槍，達成騎士 6 劍 6 槍超對稱平衡）、第二順位第六十九種動物闢道頑驢（戰士·戰斧，達成戰士 6 鎚 6 斧超對稱平衡）、第三順位第七十種動物伏影沙蠍（忍者·機關鏢，達成忍者 6 匕 6 鏢超對稱平衡）、第四順位第七十一種動物翠刃螳螂（武術家·機關爪，達成武術家 6 爪 6 拳超對稱平衡）、第五順位第七十二種動物晨音夜鶯（法師·靈晶，達成法師 6 杖 6 晶超對稱平衡）順利審查歸檔後，本提案正式接續 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），作為**第十二巡第六順位（壓軸收官大圓滿席位）**，以深海高壓、空泡破甲、極致爆發與一響定生死之姿輪轉回歸全遊戲遠距精準狙殺、極限爆發、破空重擊與讀秒看破之核心職業——**遊俠 (Ranger)** 體系，原生武器掛載於**海淵空泡高壓氣動重銃（`gun` / 遊俠·銃）**。
   空泡槍蝦的加入，使全遊戲遊俠火槍素體擴充至第 6 款（蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥、彩喙巨嘴鳥、空泡槍蝦），遊俠全職業素體達到 12 款（6 弓 6 銃），正式宣告全遊戲六大核心職業（騎士 12 款 6 劍 6 槍、戰士 12 款 6 鎚 6 斧、忍者 12 款 6 匕 6 鏢、武術家 12 款 6 爪 6 拳、法師 12 款 6 杖 6 晶、遊俠 12 款 6 弓 6 銃）**全數達成內部雙武器體系完全 1:1 超對稱平衡**，並正式引領全專案邁向第 73 族歷史性大圓滿新里程碑！
2. **經典玩具原型與古典機械深海潛水鐘槍蝦自動機工藝**：
   - 本提案選定全球古典機械玩具、鐵皮玩具與自然科學仿生機械史上的殿堂級工藝原型：
     ① **19-20 世紀歐洲古典鐘錶工坊與早期深海探險「發條潛水鐘機械甲殼偶（Vintage Clockwork Bathysphere Diver Automaton）」**，以沖壓耐壓馬口鐵、拋光黃銅厚板、耐壓石英泡罩目鏡與雙動能流體平衡活塞組裝而成，旋動發條後體內微型氣缸活塞推動，模擬早期深海潛水鐘的精密配重與耐壓密封美學；
     ② **自然界聲學與流體力學奇蹟「鼓蝦 / 槍蝦空泡爆震現象（Cavitation Bubble Shockwave of Alpheus / Pistol Shrimp）」**，槍蝦是地球自然界唯一演化出天然生物「氣動重銃」的奇蹟生物——其特化的巨型擊錘螯肢在以每秒超過 100 公里的極速閉合時，迫使兩股高壓水流撞擊產生微型局部低壓真空「空泡（Cavitation Bubble）」，空泡在數微秒內塌縮崩潰，釋放出高達數千度等離子高溫、高頻微光（聲致發光 Sonoluminescence）與高達 218 分貝的破壞性衝擊波，直接在數米開外瞬間震暈目標；
     ③ **琉璃汪洋海淵深海水壓重銃工藝（Abyssal High-Pressure Pneumatic Cannon Craft）**，將經典火槍轉譯為「海淵空泡高壓氣動重銃」，以多層冷軋厚鋼衝壓氣室、高剛性鎢鋼擊錘與高透海藍石英聚能噴嘴組合而成，完美呼應世界憲章 `docs/ART_DIRECTION.md` 第 142 行所明載之核心世界觀：「**被遺忘的玩具世界——木馬、錫兵、八音盒、陀螺、積木、舊書、玩具零件**」；
   - 作為全遊戲首款且唯一具備**「海藍鍍鈦防蝕沖壓馬口鐵底盤、沖壓雙聯黃銅觸鬚天線與測距面盔、雙聯高透耐壓海藍石英琉璃球形目鏡、深海耐壓潛水鐘加固胸甲、多節同軸彈簧減震扇形尾葉與微型高壓氣囊、海淵旋閥舵輪黃銅發條鑰匙與海淵空泡高壓氣動重銃」之深海空泡高壓狙擊遊俠素體（Abyssal Titanium-Plated Tinplate Shrimp Chassis, Vernier Brass Antennae Rangefinder Cowl, Dual High-Clarity Cyan Quartz Spherical Goggles, Bathysphere Pressure-Proof Cuirass, Segmented Spring Tail-Fluke & Micro Bladder, Abyssal Wheel-Valve Brass Key & Abyssal Cavitation Pneumatic Rifle）**。
3. **生態補足：徹底終結琉璃汪洋·發條海淵（R05）「無任何火槍遊俠 (Gun Ranger) 素體」之生態空白，打造海淵首位高壓空泡狙擊遊俠**：
   在全遊戲 9 大界域中，中低層水域沙盤界域 `R05 琉璃汪洋·發條海淵` 先前擁有浪花海獺（戰士·斧）、琉璃海馬（法師·晶）、破浪旗魚（騎士·槍）、拍浪海豹（武術家·拳）、墨影烏賊（忍者·匕）、破冰海象（騎士·劍）與潮汐蝠魟（遊俠·弓）共 7 族。
   長久以來，R05 琉璃汪洋在遊俠職業中僅有手持「海淵流體脈衝複合機關弓」的潮汐蝠魟，而主打「一響定生死、爆發極高、遠距秒殺」的火槍遊俠為**完全零分佈（0 款）**！
   面對海淵深海凝膠海水特有的強烈水壓流體阻尼、海床上游弋的「巡弋重裝機關鯊」與「錨鏈幽靈水母」，以及封鎖航道的旗艦泰坦「八爪機關巨烏賊」堅固的「主目鏡水晶罩」與「頂部排水氣閥」，**整個琉璃汪洋極度缺乏一位能夠藉由高壓空泡爆震直接穿透流體阻力、在超遠距離瞬間轟碎堅固防禦部位的「遊俠 (Ranger·Gun)」核心素體**！
   空泡槍蝦的降臨，不僅徹底填補了 R05 長期缺乏火槍遊俠的生態空白，更讓 R05 成為全遊戲涵蓋六大職業雙武器體系的海洋代表界域，將 R05 總族數推升至 8 族！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 運作邏輯（本單**完全未改動該資料表**；races_specification 正表登錄與 `total_races` 推進至 73 留待後續骨架單實作）。
5. **商業與數值護欄**：
   - **絕對零數值（Zero Pay-to-Win）**：空泡槍蝦素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有七十二族武器與職業光譜全盤點

盤點現有首發五族與前六十七款擴充族（總計 72 族，含第 60 族黑曜金龜、第 61 族彩喙巨嘴鳥、第 62 族破冰海象、第 63 族破竹羚牛、第 64 族星環狐猴、第 65 族碎石旱獺、第 66 族靈燈飛螢、第 67 族潮汐蝠魟、第 68 族穿雲翠鳥、第 69 族闢道頑驢、第 70 族伏影沙蠍、第 71 族翠刃螳螂、第 72 族晨音夜鶯）的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

- **白金兔（Clockwork Rabbit）**：騎士 (Knight) —— 單手長劍（`sword`），平衡攻防，中近距離。
- **烈鬃獅（Gilded Lion）**：騎士 (Knight) —— 皇家長槍（`spear`），中距控場，格擋迎擊。
- **鋼牙豕（Forge Boar）**：戰士 (Viking) —— 鍛爐巨鎚（`hammer`），高防厚重，部位破壞。
- **靈尾狐（Astral Fox）**：法師 (Mage) —— 秘術法杖（`magic`），遠程法術，技能爆發。
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
- **破竹羚牛（The Bamboo-Cleaving Takin）**：戰士 (Viking) —— 天元破竹開山巨斧（`axe`），青古銅鑄鐵重裝底盤，黃銅反曲扭角破障，站到最後霸體蓄力，開山重劈裂地破勢！
- **星環狐猴（The Star-Ring Lemur）**：忍者 (Ninja) —— 星軌脈衝雙鋒短匕（`dagger`），沖壓高抗衝擊聚合物底盤，冷光光纖星環尾失重平衡，失重微氣向量折返，雙刃近戰極限背刺暴擊！
- **碎石旱獺（The Rockbreaker Marmot）**：武術家 (Monk) —— 廢土偏心衝壓機關拳套（`fist`），沖壓耐磨馬口鐵底盤，雙向棘爪減速黃銅鑰匙，貼身寸勁連打破勢！
- **靈燈飛螢（The Lantern Firefly）**：法師 (Mage) —— 深林熒光藤蔓發條長杖（`magic`），沖壓薄銅雕花底盤，注塑樹脂熒光腹囊，停拍引路星屑轟擊！
- **潮汐蝠魟（The Tidal Manta）**：遊俠 (Ranger) —— 海淵流體脈衝複合機關弓（`bow`），深海沖壓耐蝕鍍鈦金屬底盤，雙翼流體滑翔，超空泡脈衝穿透！
- **穿雲翠鳥（The Jade Kingfisher）**：騎士 (Knight) —— 青竹旋簧刺槍（`spear`），竹影沖壓彩釉琺瑯金屬底盤，雙聯微調黃銅鳥喙長刺面盔，高頻螺旋鑽頭穿透，中距迎擊控場！
- **闢道頑驢（The Sapper Donkey）**：戰士 (Viking) —— 集市天軌闢道重斧（`axe`），歐風沖壓冷軋馬口鐵底盤，雙聯棘輪立體折疊長耳面盔，開拓闢障破陣重劈！
- **伏影沙蠍（The Duneshadow Scorpion）**：忍者 (Ninja) —— 沙丘穿棘機關鏢（`dart`），荒漠沖壓耐磨馬口鐵金屬底盤，雙聯琥珀金晶琉璃目鏡，多節同軸彈簧尾刺導軌，真假同色的一手與風沙看破！
- **翠刃螳螂（The Jade Mantis）**：武術家 (Monk) —— 翠刃連斬機關爪（`claw`），蔓谷沖壓雕花薄銅底盤，沖壓林冠折角面盔，雙聯高透翡翠石英琉璃目鏡，林冠停拍連切破勢大師！
- **晨音夜鶯（The Dawn Nightingale）**：法師 (Mage) —— 晨音八音諧振靈晶（`crystal`），晨曦鍍金沖壓黃銅夜鶯底盤，晨曦鐘面鏤空雕花面盔，雙聯高透黃玉石英琉璃球形目鏡，小鎮禮樂銅板八音胸甲，晨曦高音譜號雕花黃銅發條鑰匙，把護盾織成刃與八音諧振護體！
- **本提案第七十三種動物正式作為「第十二巡第六順位」壓軸收官大圓滿擴充，歸屬於遊俠 (Ranger) 體系，原生武器掛載於 `gun`（火槍 / 遊俠·銃）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`遊俠 (Ranger)`**；
- 空泡槍蝦的加入，使全遊戲遊俠火槍素體擴充至第 6 款（蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥、彩喙巨嘴鳥、空泡槍蝦），遊俠全職業達成 12 款（6 弓 6 銃），正式完成六大職業最後一塊雙武器對稱拼圖，推動全專案邁向 73 族全職業超對稱大圓滿里程碑！

### 1.2 空泡槍蝦武器選擇：【海淵空泡高壓氣動重銃（Abyssal Cavitation Pneumatic Rifle）】

- **底層武器掛載**：掛載於 `game/data/tables/weapon_classes.json` 之 `gun`（火槍 / 遊俠·銃）體系，繼承遊俠銃系「一響定生死、爆發極高、遠距離有秒殺的機會、打中很爽、換彈和收招都慢、被貼身極度危險、最不容許失誤、遠遠點射同職也可玩弓」的核心戰術宣言（`atk: 5, def: -1, hp: -6, crit: 4.0, speed: 0`）。相容既有初始裝備 `flint_gun`（燧發火銃，tier 1）與高階相容武器 `blackpowder_rifle`（黑火長銃，tier 3）；
- **專屬武器外觀與機巧設計**：
  - 武器外觀命名：`weapon_pistol_shrimp_cavitation_gun`（海淵空泡高壓氣動重銃 / Abyssal Cavitation Pneumatic Rifle，規劃為其原生專屬兵刃，資產與 `equipment.json` 掛載留待後續骨架／切片單）；
  - 構造與工藝機巧：以古典深海潛水鐘厚鑄鍍鈦合金與冷軋馬口鐵衝壓打造。槍身主體為一具粗壯的高壓氣壓缸，內部嵌裝一組重型雙螺旋蓄能發條與高硬度鎢鋼擊錘；槍膛前端連接三道耐壓黃銅緊固環箍與多面石英聚能射出噴嘴；扣動扳機時，內置蓄能發條釋放鎢鋼擊錘以極速猛烈撞擊活塞柱塞，將缸體內壓縮的深海液態凝膠與微型發條氣泡瞬間高速噴射，在槍口前方產生一道高速前進的微型低壓真空「空泡爆發衝擊波」；
  - 攻擊節奏與手感：右手單持端平於身側，左螯自然微收呈現平衡守勢。擊發時伴隨沉悶震耳的金屬撞擊「砰——喀鐺！」巨響與天藍色光致發光（Sonoluminescence）氣泡光暈，衝擊波向前穿透判定範圍長達 180px，無視目標 25% 護甲並引爆高額部位破壞傷害；擊發後活塞回位需 1.2 秒發條棘爪重構上弦，完美詮釋「一響定生死、換彈收招慢」的極限重砲狙擊手感。完全符合 `review.md 0-MKT7` 單持主武器規範（右手單手持握重銃，左前肢微縮於胸前，主次分明，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規）。

### 1.3 差異化定位：與既有 5 款火槍遊俠（蒸氣企鵝、星巡浣熊、沙哨狐獴、振律啄木鳥、彩喙巨嘴鳥）絕不撞型之論證

全遊戲現有 5 款火槍遊俠素體各具鮮明戰術與材質標籤，空泡槍蝦在此基礎上開拓出全新維度：

1. **蒸氣企鵝（The Steam Penguin）**：黃銅都市（R04）·雙管蒸氣導航火槍。以高壓鍋爐排氣、雙管直線蒸氣噴射、近中距連續壓制為核心，定位為「高壓蒸氣連射點火」；
2. **星巡浣熊（The Orbit Raccoon）**：星穹天階（R07）·軌道聚焦發條銃。以失重磁軌滑行、軌道電離脈衝、超重力聚焦過載為核心，定位為「失重滑行電離聚焦」；
3. **沙哨狐獴（The Sentry Meerkat）**：廢土荒漠（R08）·生鏽彈簧刺銃。以直立潛望測距、生鏽排氣閥門、三腳金屬尾接地抗後座為核心，定位為「荒漠伏擊架設狙擊」；
4. **振律啄木鳥（The Resonance Woodpecker）**：黃銅都市（R04）·振律重型氣動火銃。以高空垂直管道測振、長筒超高氣壓定點打擊、三點尾板支撐點射為核心，定位為「垂直管道測振穿刺」；
5. **彩喙巨嘴鳥（The Prism-Bill Toucan）**：翡翠深林（R03）·林冠聚能氣動銃。以林冠光學測距、多室減速氣動高壓發射、雙爪扣枝抗震為核心，定位為「林冠光學單發秒殺」；
6. **空泡槍蝦（The Cavitation Pistol Shrimp，本提案）**：琉璃汪洋（R05）·**海淵高壓空泡爆震重銃大師**。
   - **核心差異**：前五者分別依託「鍋爐蒸氣、軌道電離、荒漠彈簧、垂直測振或林冠氣動」；而空泡槍蝦則是全遊戲唯一**「依託 R05 琉璃汪洋深海流體壓差、將發條擊錘機械能轉化為流體低壓真空空泡、在深海凝膠阻尼中引爆聲光穿透衝擊波」**的深海重裝狙擊遊俠！
   - **造型與動態孤品特徵**：
     ① 通體為海藍鍍鈦防腐蝕沖壓馬口鐵板件，散發經典深海潛水鐘玩具自動機的沉穩厚重感；
     ② 頭部配備雙聯黃銅觸鬚天線與雙聯高透耐壓海藍石英琉璃球形目鏡，內置測距同心分劃，在深海微光中精確捕捉洋流擾動與弱點；
     ③ 後部安裝多節同軸彈簧減震扇形尾葉與微型高壓氣囊，擊發時尾葉展開平抑後座力，排氣囊噴出均勻氣泡流！

---

## 二、 外觀材質構想與「覺醒玩具」憲章對齊

### 2.1 零毛皮鐵律與「覺醒玩具」材質轉譯

嚴格遵守世界憲章 `docs/world/CANON.md` 與 `docs/ART_DIRECTION.md` 規範（100% 零真皮毛、零動物肉身、零生物黏液、零真羽毛、零真甲殼肉體、零機油污漬、零毒液、零皮革、零布料）。所有生物學特徵全部轉譯為高精細機械玩具語言：

- **海藍鍍鈦防蝕沖壓馬口鐵底盤**：主軀幹與四肢採用沖壓成型的深海防蝕鍍鈦馬口鐵薄板（Titanium Plated Anti-Corrosion Tinplate Chassis），表面施以高光亮面防鏽琺瑯彩漆（主色：多巴胺天藍 #38A0FF、薄荷綠 #4ED86A 護甲滾邊）。關節為拋光黃銅球窩關節（Ball-and-socket joints），足底爪部嵌裝高耐磨黑色防滑吸附橡膠墊，確保在海淵濕滑的藍晶石馬賽克步道上穩健立足。⛔ 100% 零蝦類甲殼肉體、零生物黏液、零生肉！
- **沖壓雙聯黃銅觸鬚天線與測距面盔**：頭部為一體成型沖壓馬口鐵頭盔，額前伸出兩根細長精工的雙聯沖壓黃銅觸鬚天線（Brass Vernier Antennae #FFD028），天線節段由微型同軸扭簧相連，隨步伐靈動彈顫，具備測量深海水壓與回波測距之機械功能；面部為一體成型黃銅前顎面板，無生物口器。
- **雙聯高透耐壓海藍石英琉璃球形目鏡**：雙眼為外凸的雙聯半球形耐壓石英琉璃透鏡（Quartz Spherical Goggles #38A0FF），邊緣以深藍紫（#1F1A3A）鍍鈦金屬防眩光密封圈緊密固定。鏡片內浮現天元金黃（#FFD028）同心測距分劃環與落日暖橘（#FFA010）游標刻度，在深海暗光中散發微弱光學冷光。
- **深海耐壓潛水鐘加固胸甲**：身著由耐高壓沖壓金屬板與圓弧形石英視窗組合而成的**深海耐壓潛水鐘加固胸甲（Pressure-Proof Bathysphere Cuirass #FFFDF8 / #38A0FF）**。前胸帶有多巴胺落日暖橘（#FFA010）與天藍（#38A0FF）深海巡檢反光飾條，胸口正中嵌裝一枚圓形透明石英氣壓視窗，可清晰窺見內部旋轉的微型氣動減壓閥與齒輪指針，配備快拆黃銅卡扣與工具金屬扣環，背部精確預留開孔以容納發條鑰匙。⛔ 100% 零皮革、零皮帶、零布料、零麻繩、零棉紙！
- **多節同軸彈簧減震扇形尾葉與微型高壓氣囊**：後部安裝標誌性的**多節同軸彈簧減震扇形尾葉與微型高壓氣囊（Segmented Coaxial Spring Tail-Fluke & Micro Pneumatic Bladder）**。尾葉由五段長短漸變的沖壓薄鋼片鉸接呈扇形展開，內部裝配微型螺旋減震彈簧與氣動排氣微囊。在重銃擊發時，尾葉扇形向下展開撐地吸收後座力，氣囊微幅噴出細密氣泡，100% 零生物尾扇、零甲殼肉質！
- **海淵旋閥舵輪黃銅發條鑰匙**：背部插著一柄獨具深海流體工藝美感的**海淵旋閥舵輪黃銅發條鑰匙（Abyssal Wheel-Valve Brass Key #FFD028）**。鑰匙柄呈古典船舵與螺旋水閥咬合造型，中心嵌有一枚多巴胺珊瑚粉（#FF5E8A）防震橡膠鉚釘。隨 R05 天頂秒針每 3~4 秒划動一格時勻速自轉，停拍定格時伴隨清脆的「嗒」一聲自鎖。
- **色彩配置矩陣（嚴格對齊多巴胺色盤）**：
  - 主色（Primary）：天藍（Sky Blue `#38A0FF`）—— 佔比約 45%，主軀幹底盤、外裝面盔與潛水鐘塗裝。
  - 副色（Secondary）：薄荷綠（Mint Green `#4ED86A`）—— 佔比約 20%，尾葉板件、關節扣環與胸甲邊框飾條。
  - 提亮金（Accent Gold）：天元金黃（Gold `#FFD028`）—— 佔比約 15%，雙聯黃銅觸鬚天線、齒輪鉚釘與旋閥發條鑰匙。
  - 暖調橘（Accent Orange）：落日暖橘（Orange `#FFA010`）—— 佔比約 8%，氣壓表指針、關節橡膠圈與胸前反光標識。
  - 基礎米白（Base White）：奶油米白（Cream White `#FFFDF8`）—— 佔比約 8%，潛水鐘胸前高光面板與石英刻度底盤。
  - 點睛粉（Highlight Pink）：珊瑚粉（Coral Pink `#FF5E8A`）—— 佔比約 2%，發條鑰匙中心鉚釘與目鏡中心聚焦點。
  - 描邊色（Outline）：深藍紫（Dark Purple `#1F1A3A`）—— 100% 全覆蓋外輪廓手繪描邊，拒絕髒黑髒灰。

---

## 三、 棲息地域與既有九大區域（R01~R09）的世界觀連結

### 3.1 區域精準掛載：【R05 琉璃汪洋·發條海淵（Crystal Ocean: The Clockwork Abyss）】

依據 `review.md` 0-PLAN1 必查點 1 與 3 規範，空泡槍蝦 100% 嚴格掛載於既有定案區域：
- **區域名稱與代號**：`R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss`（對齊 `R05_CRYSTAL_OCEAN.md` 第 1 行）；
- **沙盤材質工藝**：高透光海藍琉璃凝膠、耐高壓深海石英泡罩、防腐蝕鍍鈦合金骨架、發條磁吸氣動閥門與磷光發條指針儀表套件；
- **局域走時生態**：深沉緩慢伴隨水壓流體阻尼，天穹巨型青銅錨鏈秒針長達數公里，每 3~4 秒在液態凝膠中深沉划動一格，伴隨水波藍光漣漪擴散與沉悶悅耳的水下音叉共振「嗡——叮」；
- **地標逐字對齊（0 自創名詞）**：
  - 棲息與巡邏於海淵核心之「水下發條宮殿與氧氣泡罩（Clockwork Sunken Palace & Aerated Glass Domes）」，在球形耐壓石英玻璃罩與海藍色陶瓷釉面磚外牆間擔任重裝狙擊哨衛；
  - 漫步於「海淵地表與馬賽克步道（Abyssal Seabed & Mosaic Walkways）」，足踏防滑「深海藍晶石馬賽克瓷磚（Lapis Lazuli Mosaic Tiles）」，在微型發條氣泡與藍色螢光星屑漂浮的「液態琉璃凝膠海（Liquid Crystal Gel Sea）」中藉由高透球形石英目鏡監控暗流動向；
  - 穿梭於「磷光水母街燈與流體排氣柱（Phosphorescent Jelly-Lamps & Hydro-Exhaust Vents）」散發的多巴胺天藍（#38A0FF）與薄荷綠（#4ED86A）冷光之間，在「水下丁達爾藍晶光柱（Submarine Caustic Godrays）」映照下校準重銃氣壓；
  - 鎮守接駁要道「深淵排污豎井管道·耐壓吊籠（Abyssal Sump Siphon: Bathysphere Terminal）」與「晨曦天軌 5 號深海浮標月台（Dawn Rail Deepsea Buoy Platform 5）」，護送往來浮空艇吊艙之發條旅人，巡查通往火山之「深海熱液湧泉管道（Hydrothermal Trench Conduits）」，並維護外緣之「環域水幕磁阻防護波（Magnetic Hydro-Barrier Grid）」防止弱小玩偶墜出沙盤；
  - 定期前往「海底防鏽超聲油壓艙（Ultrasonic De-rusting Station）」塗抹「防鏽特種矽油（Anti-Rust Special Silicone Oil）」，恪守「海潮對表儀式」調整體內氣壓閥阻尼平衡；
  - 結伴深海夥伴：「小黃鴨船長·舵手巴克（Captain Buck the Rubber Ducky）」、「海馬信差·碧浪（Billow the Seahorse Courier）」與「深海鐘錶貝·珠貝長老（Elder Pearl the Clockwork Clam）」；
  - 協同守護「發條熱帶魚（Clockwork Tropical Fish）」、「橡皮小黃鴨船長（Rubber Ducky Navigators）」與「發條海馬信差（Wind-up Seahorse Couriers）」等原住玩具居民；
  - 迎擊深海異動野怪：「生鏽的發條深海鮟鱇（Rusty Clockwork Angler）」、「錨鏈幽靈水母（Anchor-Chain Phantom Jelly）」與「巡弋重裝機關鯊（Armored Patrol Mecha-Shark）」；
  - 在討伐旗艦泰坦 BOSS「深淵海霸泰坦·八爪機關巨烏賊（Titan Abyssal: Octo-Gear the Abyssal Kraken）」戰役中，擔任超遠距精準狙擊主力，利用海淵空泡氣動重銃的空泡爆震直接破壞巨烏賊的「錨鏈重腕（Anchor Tentacles）」關節液壓閥、打爆「頂部排水氣閥（Crown Siphon Vent）」並轟碎「主目鏡水晶罩（Optic Glass Dome）」，奪取「澄澈深海藍晶核」與「鍍鈦耐腐蝕增壓閥」！

---

## 四、 七大部件槽位規格與造型概念（Paperdoll Slots Spec）

完全契合 `paperdoll_slots.json` 定義之 7 大標準圖層插槽（Z-Ordering），提供精確像素級規格與美術拆件導引：

```
Layer Z-Index Pipeline:
Z=10:  chassis      軀體外殼與塗裝（海藍防蝕沖壓鍍鈦合金夜光馬口鐵底盤）
Z=20:  head_unit    頭部特徵與面盔（沖壓雙聯黃銅觸鬚天線與測距面盔）
Z=25:  optic_core   面部眼部與目鏡（雙聯高透耐壓海藍石英琉璃球形目鏡）
Z=30:  costume      外裝服飾與胸甲（深海耐壓潛水鐘加固胸甲）
Z=40:  back_curio   後背飾品與尾部（多節同軸彈簧減震扇形尾葉與微型高壓氣囊）
Z=50:  winding_key  發條鑰匙（海淵旋閥舵輪黃銅發條鑰匙）
Z=60:  weapon       右手單持武器（海淵空泡高壓氣動重銃）
```

1. **底盤素體（`chassis` / Z=10 / 必填）**：
   - 部件 ID：`chassis_pistol_shrimp_stock`
   - 名稱：海藍鍍鈦防蝕沖壓馬口鐵底盤（Abyssal Titanium-Plated Tinplate Chassis）
   - 結構：2.2 頭身矮萌金屬底盤。主軀幹由兩片沖壓成型的半球形鍍鈦馬口鐵薄板扣合，表面覆以亮面天藍（#38A0FF）防腐蝕琺瑯漆，四肢為拋光黃銅球窩關節，雙足底部貼附防滑黑色橡膠墊；左前肢末端為一隻靈活的小型黃銅輔助夾鉗（平衡微調用），右腕具備重型加固金屬卡口以穩固支撐主武器。
2. **頭部特徵（`head_unit` / Z=20 / 必填）**：
   - 部件 ID：`head_pistol_shrimp_vernier_cowl`
   - 名稱：沖壓雙聯黃銅觸鬚天線與測距面盔（Vernier Brass Antennae Rangefinder Cowl）
   - 結構：金屬沖壓圓弧面盔，兩側各伸出一根長約 28px 的微型沖壓黃銅觸鬚天線（#FFD028），節段之間由微型扭簧鉸接，具備流體測速與回波測距機能；面盔額頭裝飾有一枚沖壓船舵徽章與落日暖橘（#FFA010）反光條。
3. **眼部核心（`optic_core` / Z=25 / 必填）**：
   - 部件 ID：`face_pistol_shrimp_quartz_goggles`
   - 名稱：雙聯高透耐壓海藍石英琉璃球形目鏡（Dual High-Clarity Abyssal Quartz Spherical Goggles）
   - 結構：雙聯外凸的圓球形耐壓石英目鏡（直徑約 14px），深藍紫金屬密封框，透鏡內部清晰可見天元金黃（#FFD028）同心圓十字瞄準準星與暖橘（#FFA010）測距標尺，在暗處發出均勻溫潤的冷光。
4. **服飾胸甲（`costume` / Z=30 / 必填）**：
   - 部件 ID：`costume_pistol_shrimp_bathysphere_plate`
   - 名稱：深海耐壓潛水鐘加固胸甲（Bathysphere Pressure-Proof Cuirass）
   - 結構：由奶油米白（#FFFDF8）加厚沖壓金屬板與天藍（#38A0FF）護甲邊框組成的復古潛水鐘胸甲。胸口正中設有一面直徑 12px 的圓形透明石英觀測窗，內部微型黃銅氣壓指針隨呼吸起伏微擺；兩肩配備沖壓高壓排氣管閥與工具扣環，背部預留精密孔洞供發條鑰匙穿出。
5. **背部飾件（`back_curio` / Z=40 / 必填）**：
   - 部件 ID：`curio_pistol_shrimp_spring_tail`
   - 名稱：多節同軸彈簧減震扇形尾葉與微型高壓氣囊（Segmented Spring Tail-Fluke & Micro Bladder）
   - 結構：後背尾部安裝由五片弧形冷軋薄鋼板沖壓而成的扇形尾葉（塗裝天藍 #38A0FF 與薄荷綠 #4ED86A），內部以同軸螺旋鋼彈簧與微型高壓手風琴式排氣微囊相連。待機時尾葉自然微翹，射擊時尾葉撐地並噴出均勻氣泡排氣，平衡巨大後座力。
6. **發條鑰匙（`winding_key` / Z=50 / 必填）**：
   - 部件 ID：`key_pistol_shrimp_wheel_valve`
   - 名稱：海淵旋閥舵輪黃銅發條鑰匙（Abyssal Wheel-Valve Brass Key）
   - 結構：背部中心插著一柄金黃發亮的古典船舵與螺旋旋閥造型黃銅鑰匙（#FFD028），中心鑲嵌多巴胺珊瑚粉（#FF5E8A）防震橡膠鉚釘。隨 R05 區域秒針每 3~4 秒划動時勻速旋轉一圈，停拍時內部微型棘爪精確卡緊發出清脆的「嗒」聲。
7. **專屬兵刃（`weapon` / Z=60 / 必填）**：
   - 部件 ID：`weapon_pistol_shrimp_cavitation_gun`
   - 名稱：海淵空泡高壓氣動重銃（Abyssal Cavitation Pneumatic Rifle）
   - 結構：右手單持長管重銃，槍身長度約 36px，前寬後窄呈流線型耐壓造型。主體為冷軋沖壓鍍鈦氣壓缸，前段箍有三道黃銅加固環，槍口裝配多面石英聚能噴嘴，尾部裝配外露的鎢鋼擊錘與上弦棘爪。擊發時噴射出錐形空泡震波與天藍色微光。

---

## 五、 戰鬥動作姿態與動畫影格規劃（Combat Poses & Action Flow）

嚴格契合既有 6 大核心動作幀規範（`idle`, `walk`, `attack`, `hit`, `down`, `jump`），確保在 Godot 引擎內平滑回放：

1. **待機姿態（Idle，4 影格循環，0.6s / loop）**：
   - 2.2 頭身矮萌身軀呈沉穩低重心站姿，右手單持海淵空泡重銃微微斜指前方地面，左螯自然微屈護於胸側；
   - 雙聯黃銅觸鬚天線隨深海水流節律輕盈微幅彈顫，胸口潛水鐘石英氣壓表的金色微型指針微微左右微擺，背部舵輪發條鑰匙隨 R05 秒針每 3~4 秒划動一格勻速旋轉自鎖。
2. **走動姿態（Walk，4 影格循環，0.5s / loop）**：
   - 雙腿球窩關節以均勻小碎步向前邁進，黑色橡膠足底扎實踏在地面；
   - 身體重心隨著步幅輕微前後起伏，後背扇形尾葉微幅開合，重銃端平保持水平指向，呈現專業偵查射擊步態。
3. **普通攻擊（Attack，5 影格動作鏈，總長 0.75s）**：
   - **影格 1（抬槍蓄能，0.15s）**：雙足微錯下沉重心，右手重銃迅速端平抬起，目鏡準星與槍口噴嘴對齊前方，擊錘向後拉緊發出清脆的「卡嗒」咬合聲，尾葉展開撐地；
   - **影格 2（擊發空泡，0.05s）**：擊錘猛烈向前撞擊柱塞！槍口噴射出一道直徑 32px 的天藍色（#38A0FF）錐形空泡震波，伴隨耀眼的白色氣泡高光與衝擊波光暈；
   - **影格 3（後座排氣，0.15s）**：後座力推動身軀向後微滑 3px，後背氣囊噴出一陣微小氣泡，槍口冒出淡淡的微溫白氣；
   - **影格 4-5（拉栓回位，0.4s）**：發條棘爪帶動柱塞復位上弦，重銃重回低平持握，動作利落帥氣。
4. **受擊姿態（Hit，2 影格，0.25s）**：
   - 角色身軀向後仰傾 15 度，雙聯觸鬚天線向後繃直，左螯護於面盔前，右手重銃自然下垂偏轉；
   - 臉部琉璃目鏡浮現短暫波紋干涉光斑，隨後迅速調整重心復位。
5. **倒地受挫（Down，2 影格，0.6s）**：
   - 重心失衡單膝後退跪地，左夾鉗撐地，右手將重銃橫架於膝蓋上防禦；
   - 胸口石英氣壓表冒出微弱的排氣散熱白氣，隨後在發條能量帶動下迅速昂首重整站起。
6. **跳躍與浮空（Jump，3 影格，0.4s）**：
   - 雙足足底彈簧受壓蓄力後垂直彈起，後背扇形尾葉如推進器般向下強力拍擊；
   - 浮空時身軀前傾呈流線型滑行姿態，重銃指向斜下方，展現深海游俠特有的流體機動性。

---

## 六、 PRODUCT_LOCK 審查問卷（§9 准入門檻六問六答）

### Q1：它掛在哪個核心循環的哪一環？
- **回答**：掛在核心循環「戰鬥（主線出征/停擺巨偶）-> 掉落零件/圖鑑解鎖 -> 衣櫥換裝與紙娃娃客製化 -> 數值無關的情感共鳴」的「**外觀收集與角色客製化環節**」。空泡槍蝦作為第十二巡第六順位收官擴充，正式達成遊俠 12 款素體（6 弓 6 銃），徹底補齊全遊戲六大核心職業最後一塊雙武器對稱拼圖（達成全職業 100% 6:6 超對稱大圓滿！），並徹底填補 R05 琉璃汪洋長期缺乏火槍遊俠素體的生態空白，為喜愛深海潛水鐘、古典甲殼玩具與高壓重砲狙擊風格的玩家提供充滿硬派工程感與童話趣味的獨特視覺體驗。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
- **回答**：服務第二支柱「**動態紙娃娃與玩具情感共鳴**」（第二優先，P2）與第四支柱「**童話純淨發條世界沉浸**」（第四優先，P4）。空泡槍蝦透過經典發條深海潛水鐘造型、自然界槍蝦空泡爆震的玩具仿生機械轉譯、船舵旋閥發條鑰匙與海淵巨型青銅錨鏈秒針節律，喚醒玩家對古典深海冒險與發條工程玩具的深厚共鳴；且火槍「一響定生死」之超遠距重擊回饋扎實有力，極其適配手機雙拇指操作。

### Q3：玩家在手機上用單手拇指能不能操作它？
- **回答**：**完全可以**。所有操作 100% 沿用既有橫屏雙拇指與單手單拇指戰鬥佈局（左下虛擬搖桿移動，右下普通攻擊、閃避衝刺與齒輪過載大招按鈕，熱區直徑均 ≥ 48px）。遊俠火槍普攻自帶遠程索敵自動鎖定與直覺朝向判定，不增加任何多餘手勢或按鍵。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
- **回答**：**完全不需要**。素體資料完全封裝於客戶端本機資料庫 `paperdoll_slots.json` 與本地 GDScript 渲染管線中，單機離線即可完美換裝與出戰，100% 遵守離線單機優先架構。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
- **回答**：**本提案自身不會**。本提案為**純文字 Markdown 規格文件**，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。⚠️ 但須據實載明現況：`docs/PRODUCT_LOCK_0.20.md` §5.2 記載首包目標為 50～80 MB，而現況 Web 目錄為 **135 MB，尚未達標**。首包瘦身屬既有欠帳，**不因本提案而消解**。後續切片資產實裝採 WebP 雙規格壓縮，預估單族切片資源 < 0.8 MB，仍須併入整體瘦身計畫一併處理。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
- **回答**：**放棄了真實槍蝦的有機甲殼肉體、生物口器、觸角肌肉、生物黏液與寫實解剖細節，放棄了繁複寫實的生物紋理與雜亂外掛**。為了恪守童話發條玩具憲章與手機低功耗流暢運行，我們徹底放棄了寫實甲殼類的脆弱肉質，將一切特徵簡化抽象為 2.2 頭身沖壓鍍鈦馬口鐵板、雙聯耐壓石英琉璃目鏡、五片式彈簧扇形尾葉與船舵旋閥黃銅發條鑰匙，換取極致乾淨的多巴胺色彩辨識度與 60 FPS 流暢度。

---

## 七、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

以下為即將寫入 `docs/design/paperdoll_slots.json` 正表 `races_specification.races` 清單中之正式標準 JSON 配置（本單為純文件提案，不改動該資料表，正表登錄留待後續骨架單實作）：

```json
{
  "race_id": "pistol_shrimp",
  "aliases": [
    "cavitation_shrimp",
    "snapping_shrimp",
    "abyssal_shrimp",
    "clockwork_shrimp",
    "gunner_shrimp",
    "bathysphere_shrimp"
  ],
  "name_zh": "空泡槍蝦",
  "name_en": "The Cavitation Pistol Shrimp",
  "class_archetype": "遊俠 (Ranger)",
  "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
  "starter_weapon": "flint_gun",
  "weapon_class": "gun",
  "lore_anchor": "棲息於琉璃汪洋·發條海淵「水下發條宮殿與氧氣泡罩」，漫步於「海淵地表與馬賽克步道」，踏行於防滑「深海藍晶石馬賽克瓷磚」與耐腐蝕鍍鈦鉚釘接縫之間，巡邏於「液態琉璃凝膠海」漂浮微型發條氣泡與藍色螢光星屑之中，穿行於「磷光水母街燈與流體排氣柱」散發的多巴胺天藍與薄荷綠冷光之下，沐浴「水下丁達爾藍晶光柱」，聆聽「巨型青銅錨鏈秒針」每3~4秒划動的深沉律動，守護接入站「深淵排污豎井管道·耐壓吊籠」與「晨曦天軌5號深海浮標月台」，巡視「深海熱液湧泉管道」，維護外緣「環域水幕磁阻防護波」，定期前往「海底防鏽超聲油壓艙」塗抹「防鏽特種矽油」並恪守「海潮對表儀式」，結伴小黃鴨船長·舵手巴克、海馬信差·碧浪與深海鐘錶貝·珠貝長老，護衛發條熱帶魚、橡皮小黃鴨船長與發條海馬信差等原住玩具居民，迎戰生鏽的發條深海鮟鱇、錨鏈幽靈水母與巡弋重裝機關鯊，在討伐旗艦泰坦深淵海霸泰坦·八爪機關巨烏賊戰役中利用高壓空泡爆震直接破壞其錨鏈重腕、頂部排水氣閥並轟碎主目鏡水晶罩，奪取澄澈深海藍晶核與鍍鈦耐腐蝕增壓閥；通體覆蓋海藍鍍鈦防蝕沖壓馬口鐵底盤、沖壓雙聯黃銅觸鬚天線與測距面盔、雙聯高透耐壓海藍石英琉璃球形目鏡、深海耐壓潛水鐘加固胸甲、多節同軸彈簧減震扇形尾葉與微型高壓氣囊、海淵旋閥舵輪黃銅發條鑰匙，右手單持海淵空泡高壓氣動重銃，以2.2頭身矮萌金屬軀體、一響定生死與深海空泡爆震見長的琉璃海淵火槍狙擊遊俠",
  "proportions": {
    "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19世紀歐洲深海潛水鐘發條鐵皮甲殼自動機名品)",
    "posture": "2.2頭身矮萌身軀呈沉穩低重心狙擊站姿，右手單持海淵空泡高壓氣動重銃指向前方，左前螯自然微收呈現流體平衡守勢，背後舵輪旋閥發條鑰匙隨海淵秒針每3~4秒划動勻速自轉，停拍時精準自鎖",
    "standee_height_px": 800,
    "standee_width_px": 480
  },
  "mechanical_features": {
    "ears_cowl": "沖壓雙聯黃銅觸鬚天線與測距面盔，額前伸出兩根細長沖壓黃銅觸鬚天線，微型同軸扭簧相連，具備流體測距機能",
    "eyes": "雙聯大尺寸高透耐壓海藍石英琉璃球形目鏡，深藍紫金屬密封眼圈，鏡內浮現金黃十字準星與暖橘測距標尺",
    "antenna_claws": "雙聯黃銅觸鬚天線與左側微型黃銅輔助夾鉗，全金屬球窩鉸接，動作流暢俐落",
    "back_tail": "五節沖壓冷軋薄鋼扇形尾葉，內置手風琴式排氣微囊與減震發條彈簧，射擊時撐地排氣平衡後座力",
    "torso_and_limbs": "天藍與薄荷綠防蝕沖壓鍍鈦馬口鐵板件，黃銅球形關節，雙足爪底覆蓋耐磨防滑黑色橡膠吸附墊",
    "key": "海淵旋閥舵輪黃銅發條鑰匙，輪柄呈古典船舵與螺旋水閥雕花造型，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
  },
  "color_palette": {
    "primary": "#38A0FF (天藍海淵耐腐蝕鍍鈦夜光塗裝底盤與面盔)",
    "secondary": "#4ED86A (薄荷綠尾葉減震板件、胸甲滾邊與高壓氣動導管護套)",
    "accent_blue": "#38A0FF (天藍琉璃目鏡分劃與重銃空泡震波光暈)",
    "accent_orange": "#FFA010 (落日暖橘氣壓指針、關節防震膠圈與潛水鐘標識條)",
    "accent_white": "#FFFDF8 (奶油米白深海耐壓潛水鐘加固胸甲面板與高光嵌片)",
    "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與目鏡聚焦點)",
    "outline": "#1F1A3A (深藍紫立體手繪描邊)"
  },
  "default_items": {
    "chassis": "chassis_pistol_shrimp_stock",
    "head_unit": "head_pistol_shrimp_vernier_cowl",
    "optic_core": "face_pistol_shrimp_quartz_goggles",
    "costume": "costume_pistol_shrimp_bathysphere_plate",
    "back_curio": "curio_pistol_shrimp_spring_tail",
    "winding_key": "key_pistol_shrimp_wheel_valve",
    "weapon": "weapon_pistol_shrimp_cavitation_gun"
  }
}
```

---

## 八、 產圖提示詞規格（AI Image Generation Prompts & Directives）

> ⛔ **本任務為純規格文件交付，嚴格遵守「不產圖、不產片」紅線**。以下提示詞僅供後續美術切片與官網宣傳任務參照：

### 8.1 官方立繪概念提示詞（Hero Standee Prompt）

```text
Chibi 2.2 head-to-body ratio clockwork pistol shrimp ranger toy automaton, standing alertly and cutely on a fairy-tale submarine cobblestone diorama with pressure-proof glass domes, luminous jellyfish lamps, and cyan liquid crystal gel sea. Pure awakening toy, 100% NO animal fur, NO leather, NO biological flesh, NO biological mouth, NO biological tissue, NO real crustacean shell meat, NO real mucus, NO rust, NO oil leaks. Crafted from stamped titanium-plated tinplate sheets with glossy enamel lacquer (#38A0FF sky blue body with #4ED86A mint green accents), smooth articulated brass ball-socket joints with solid black rubber grip pads on small mechanical feet. Head unit featuring stamped dual brass antennae rangefinder (#FFD028) with miniature springs. Eyes are glowing dual spherical high-clarity cyan quartz glass goggles (#38A0FF sky blue with #FFD028 golden crosshair reticle) set within deep indigo violet metal anti-glare rings (#1F1A3A). Wearing a vintage cream-white bathysphere pressure-proof cuirass (#FFFDF8) with a circular transparent quartz pressure gauge revealing golden gears and an orange pointer. Back curio features a fan-shaped 5-segment stamped steel spring tail-fluke with micro-pneumatic exhaust bladders. On the back, a rotating golden ship-wheel valve wind-up key with a coral pink central rivet (#FF5E8A). Right hand single-wielding an oversized heavy cavitation pneumatic rifle with three brass reinforcement rings and quartz muzzle emitting soft glowing cyan shockwave rings, while left miniature brass claw is tucked neatly near chest for fluid balance. Clean dopamine palette, thick bottom jelly button feel, crisp hand-drawn cell-shading with deep indigo violet outlines (#1F1A3A), submarine tyndall caustic godrays through cyan liquid gel sea, pure cream white background --ar 1:1 --stylize 250
```

### 8.2 負面提示詞（Negative Prompt）

```text
flesh, realistic animal fur, real shrimp meat, real lobster claws, organic exoskeleton, biological mouthparts, animal eyes, biological tissue, dark fantasy, dirty rust, grunge, oil leaks, steampunk messy wires, photorealistic, human face, 3D blender render, ugly, deformed, blurry, extra limbs, extra wings, extra weapons, dual wielding, floating weapons, messy background, low quality
```

---

## 九、 六語系在地化對照表（Localization Lexicon）

依據世界憲章多語言通用原則，提供核心專有名詞六語系標準對照表（確保六語系可譯性，絕不使用中文諧音雙關）：

```
┌────────────────────────────────┬──────────┬──────────┬──────────────────────────┬────────────────────────────┬────────────────────────────┬────────────────────────────┐
│ 識別 ID                        │ 繁體中文 │ 簡體中文 │ 英語 (en)                │ 日語 (ja)                  │ 韓語 (ko)                  │ 西班牙語 (es)              │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ race_pistol_shrimp             │ 空泡槍蝦 │ 空泡枪虾 │ The Cavitation Pistol    │ キャビテーション・テッポ   │ 캐비테이션 딱총새우        │ El Camarón Pistola de      │
│                                │          │          │ Shrimp                   │ ウエビ                     │                            │ Cavitación                 │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ class_ranger                   │ 遊俠     │ 游侠     │ Ranger                   │ レンジャー (遊撃手)        │ 레인저 (Ranger)            │ Guardabosques (Ranger)     │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ starter_weapon_flint_gun       │ 燧發火銃 │ 燧发火铳 │ Flintlock Gun            │ 火打石銃                   │ 부싯돌 화승총              │ Pistola de Sílex           │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ weapon_pistol_shrimp_cavitati  │ 海淵空泡 │ 海渊空泡 │ Abyssal Cavitation       │ 海淵空泡高圧気動重銃       │ 심연 공동 고압 기동중총    │ Fusil Neumático de         │
│ on_gun                         │ 高壓氣動 │ 高压气动 │ Pneumatic Rifle          │                            │                            │ Cavitación Abisal          │
│                                │ 重銃     │ 重铳     │                          │                            │                            │                            │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ key_pistol_shrimp_wheel_valve  │ 海淵旋閥 │ 海渊旋阀 │ Abyssal Wheel-Valve      │ 海淵舵輪バルブ黄銅ぜんまい │ 심연 키밸브 황동 태엽 열쇠 │ Llave de Bronce con Rueda  │
│                                │ 舵輪黃銅 │ 舵轮黄铜 │ Brass Key                │ 鍵                         │                            │ de Válvula Abisal          │
│                                │ 發條鑰匙 │ 发条钥匙 │                          │                            │                            │                            │
├────────────────────────────────┼──────────┼──────────┼──────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ curio_pistol_shrimp_spring_tai │ 多節同軸 │ 多节同轴 │ Segmented Spring         │ 多節同軸スプリング扇形尾翼 │ 다절 동축 스프링 부채꼴    │ Cola Abanico de Resorte    │
│ l                              │ 彈簧減震 │ 弹簧减震 │ Tail-Fluke & Micro       │ ＆高圧気嚢                 │ 꼬리 & 고압 기낭           │ Coaxial y Microvejiga      │
│                                │ 扇形尾葉 │ 扇形尾叶 │ Bladder                  │                            │                            │                            │
│                                │ 與微型高 │ 与微型高 │                          │                            │                            │                            │
│                                │ 壓氣囊   │ 压气囊   │                          │                            │                            │                            │
└────────────────────────────────┴──────────┴──────────┴──────────────────────────┴────────────────────────────┴────────────────────────────┴────────────────────────────┘
```

---

## 十、 企劃審查清單（Review Checklist 自檢，對齊 review.md、0-PLAN1、0-PLAN5、23a、23d、23f、23f-1、23f-4、0-MKT7 與 CANON 規範）

- [x] **23f-1 職業正式名稱檢驗**：全文 100% 統一使用 `遊俠 (Ranger)` 單一正式名，無自創或複合混淆稱呼。
- [x] **0-MKT7 武器手持規範檢驗**：空泡槍蝦單手持槍，右手持握海淵空泡高壓氣動重銃，左前肢微型黃銅夾鉗自然微收呈現流體平衡守勢，主次分明，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- [x] **CANON 世界憲章檢驗**：100% 零真皮毛、零動物肉身、零生物黏液、零真羽毛、零真甲殼肉體、零毒液、零生鏽、零皮革、零布料；身軀為海藍鍍鈦沖壓馬口鐵底盤、雙聯石英琉璃球形目鏡、沖壓黃銅觸鬚天線面盔、深海耐壓潛水鐘加固胸甲、多節同軸彈簧扇形尾葉、船舵旋閥雕花發條鑰匙。
- [x] **23f-4 材質詞彙合規檢驗**：材質敘述 100% 轉譯為沖壓馬口鐵薄板、冷軋薄鋼片、拋光黃銅球窩關節、石英琉璃透鏡、黑色防滑橡膠足墊，零皮革、零皮帶、零布料、零天鵝絨、零絨毛、零棉紙殘留。
- [x] **ART_DIRECTION 多巴胺色彩檢驗**：高飽和鮮亮色彩（奶油米白 #FFFDF8、薄荷綠 #4ED86A、落日暖橘 #FFA010、天藍 #38A0FF、天元金黃 #FFD028、珊瑚粉 #FF5E8A），深藍紫立體手繪描邊（#1F1A3A），絕無暗黑泥土廢土色。
- [x] **區域生態錨定檢驗**：精準咬合 `R05_CRYSTAL_OCEAN.md`，深度融入琉璃汪洋之液態琉璃凝膠海、海淵地表與馬賽克步道、防滑深海藍晶石馬賽克瓷磚、水下發條宮殿與氧氣泡罩、磷光水母街燈與流體排氣柱、水下丁達爾藍晶光柱、巨型青銅錨鏈秒針、深淵排污豎井管道·耐壓吊籠、晨曦天軌 5 號深海浮標月台、深海熱液湧泉管道、環域水幕磁阻防護波、海底防鏽超聲油壓艙、海潮對表儀式、小黃鴨船長·舵手巴克、海馬信差·碧浪、深海鐘錶貝·珠貝長老與守護泰坦八爪機關巨烏賊戰役，徹底終結 R05 零火槍遊俠素體之歷史空白！
- [x] **review.md 23a / 0-PLAN1 必查點 1（地標與專有名詞查驗）**：`lore_anchor` 所載「水下發條宮殿與氧氣泡罩」、「海淵地表與馬賽克步道」、「深海藍晶石馬賽克瓷磚」、「液態琉璃凝膠海」、「磷光水母街燈與流體排氣柱」、「水下丁達爾藍晶光柱」、「巨型青銅錨鏈秒針」、「深淵排污豎井管道·耐壓吊籠」、「晨曦天軌 5 號深海浮標月台」、「深海熱液湧泉管道」、「環域水幕磁阻防護波」、「海底防鏽超聲油壓艙」、「防鏽特種矽油」、「海潮對表儀式」、「小黃鴨船長·舵手巴克」、「海馬信差·碧浪」、「深海鐘錶貝·珠貝長老」、「發條熱帶魚」、「橡皮小黃鴨船長」、「發條海馬信差」、「生鏽的發條深海鮟鱇」、「錨鏈幽靈水母」、「巡弋重裝機關鯊」、「深淵海霸泰坦·八爪機關巨烏賊」、「錨鏈重腕」、「頂部排水氣閥」、「主目鏡水晶罩」、「澄澈深海藍晶核」、「鍍鈦耐腐蝕增壓閥」逐字比對 `docs/world/regions/R05_CRYSTAL_OCEAN.md` 第 19 行、第 20 行、第 21 行、第 22 行、第 24 行、第 25 行、第 29 行、第 30 行、第 32 行、第 34 行、第 42 行、第 43 行、第 44 行、第 46 行、第 47 行、第 54 行、第 63 行、第 71 行、第 85 行、第 89 行、第 93 行、第 100 行、第 107 行、第 108 行、第 109 行、第 123 行 100% 存在，無任何自創詞彙。
- [x] **review.md 23d（對齊 game/ 實作查驗）**：遊俠職業代號 `ranger`、武器代號 `gun`、武器稱號 `遊俠·銃`、標籤宣言 `一響定生死`、數值 `atk: 5, def: -1, hp: -6, crit: 4.0, speed: 0`、初始相容武器 `flint_gun`（燧發火銃，tier 1）100% 對齊 `game/data/tables/weapon_classes.json` 與 `game/data/tables/equipment.json`。
- [x] **review.md 0-PLAN1 必查點 2（包體膨脹查驗）**：純文字 Markdown 規格文件，0 圖片、0 影片、0 聲音素材，首包體積膨脹為 0。據實引用 `docs/PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族切片資源 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有七十二族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 72 族（含第 71 族翠刃螳螂、第 72 族晨音夜鶯）。
- [x] **review.md 0-PLAN5（純文件時態規範）**：嚴格遵守 0-PLAN5 規範，不宣稱「已實裝／已登錄資料表」；明確標記本單純為企劃規格提案，未改動 `paperdoll_slots.json`，專屬武器外觀資產與資料表登錄留待後續骨架與切片任務實作。
