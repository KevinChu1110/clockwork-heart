# 第二十六種動物「熔火蜥蜴（The Magma Salamander）」世界觀與角色設計提案

> **文件狀態**：世界觀擴充提案與角色規格書（Expansion World & Chassis Proposal - Ready for Review）  
> **制定日期**：2026-09-28  
> **負責人**：側案·策劃總監 小凱（sideplan）  
> **審核對象**：側案製作人 老周（side） / 側案美術總監 小柔（sideart） / 側案程式 阿宏（sideworker）  
> **對應看板任務**：`t_a7b236ab`（📖 世界觀｜第二十六種動物紙娃娃角色設計提案（只寫文件，不產圖不產片））  
> **關聯歸檔文件**：  
> - [`docs/design/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md`](../design/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md)  
> - [`docs/world/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md`](../world/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md)  
> - [`docs/art/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md`](../art/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md)  
> **關聯依據文件**：  
> - `docs/world/regions/R06_MOLTEN_FOUNDRY.md`（第 1 行區域代號與名稱「R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano」、第 21 行「重型鍛造工坊與衝壓懸橋」、第 32 行「高壓地熱噴射升空彈射井」、第 43 行「重裝鑄鐵矮人玩偶與大型四葉散熱鍛造發條鑰匙」、第 45 行原住種族「發條耐火工兵蜥蜴（Clockwork Magma Salamanders）：由鎢鋼耐熱鉸鏈與金屬耐火鱗片組成的四足維修爬行偶，背部馱著微型手動注油壺，在管網縫隙間穿梭巡檢」、第 47 行「淬火冷卻噴淋池」、第 102/162 行「火山口中央核心鍛造神壇」、第 206 行「氣動衝壓懸橋」、第 236 行「赤焰熔爐·鍛造火山」、第 253 行特產武器「熔爐衝壓巨錘（Foundry Stamping Sledgehammer）」、第 255 行代表素材「玄鐵精煉鑄錠」、第 256 行代表素材「耐高溫合金彈簧」、第 257 行代表素材「熔岩黑曜石拳板」、第 258 行代表素材「耐火石墨潤滑膏」）  
> - `docs/world/CANON.md`（世界憲章：100% 零毛皮零軟組織、沖壓耐火鎢鋼板件/全金屬與齒輪咬合發條玩具、背後必有發條鑰匙）  
> - `docs/design/paperdoll_slots.json` / `docs/design/PAPERDOLL_SLOTS_SPEC.md`（7 大部件槽位架構）  
> - `game/data/tables/weapon_classes.json`（6 職業 12 大武器系統，戰士·鎚 `hammer` 體系）  
> - `game/data/tables/equipment.json`（既有鎚武器 ID：第 262 行 `anvil_hammer` 砧心小鎚、第 275 行 `iron_cudgel` 鐵骨重棒、第 288 行 `bastion_blade` 壁壘厚刃）  
> - `docs/PRODUCT_LOCK_0.20.md`（§1.6 體驗支柱、§3.1 核心循環、§5.2 包體規範、§9 准入門檻）  
> - `docs/BALANCE.md`（§5 時間模型 0.15 鎖版規範）  

---

## 0. 執行摘要與邊界宣告

1. **提案定位：接棒第五巡（第 25~30 族）第二順位「戰士 (Viking)」擴充**：  
   本文件為《發條之心》既有 7 大紙娃娃部件槽位系統（`mob-paperdoll`）在第二十五種動物巡林松鼠（騎士·劍）開啟第五巡後，正式制定的**第二十六種動物擴充素體規格**。  
   依據 6 大職業標準循環（`knight` -> `viking` -> `ninja` -> `monk` -> `mage` -> `ranger`），本提案精準掛載於第二順位的 **戰士 (Viking)**，原生武器對齊 **巨鎚（`hammer` / 戰士·鎚）** 體系，象徵五巡戰士正式出陣！
2. **經典玩具起源與古典機械發條蜥蜴工藝**：  
   - 本提案選定全球古典機械玩具史與鐵皮發條動作玩具之名作——**「1950s 歐美與日本古典鐵皮發條爬行金屬蜥蜴/蠑螈機械偶（Vintage Tinplate Wind-up Crawling Salamander / Lizard Automaton）」**；  
   - 完美承接世界觀無可撼動的官方設定法源：`docs/world/regions/R06_MOLTEN_FOUNDRY.md` 第 45 行明載的原住玩具族群「**發條耐火工兵蜥蜴（Clockwork Magma Salamanders）**：由鎢鋼耐熱鉸鏈與金屬耐火鱗片組成的四足維修爬行偶，背部馱著微型手動注油壺，在管網縫隙間穿梭巡檢」；  
   - 作為全遊戲首款且唯一具備**「五節鉸鏈同軸沖壓耐熱重鋼大尾巴（內部裝配高黏度耐火石墨重力平衡阻尼器）、雙聯折疊耐熱散熱導流鰭耳、地熱鍛造鉚接防護圍裙、耐熱高溫爪靴與四葉散熱鍛造發條鑰匙」的火山工兵重裝鍛火戰士素體（Segmented Heat-Resistant Damping Tail, Folding Radiator Crests, Forging Sapper Apron, High-Temp Claws & Four-Vane Heat-Sink Key）**。
3. **生態補足：充實赤焰熔爐核心陣容**：  
   在全遊戲 9 大界域中，中層高溫浮空界域 `R06 赤焰熔爐·鍛造火山` 長期僅有第 4 族鋼牙豕（戰士·鎚）單一素體，生態極度匱乏。熔火蜥蜴的加入，使 R06 赤焰熔爐正式形成「鋼牙豕（狂暴破城鎚）× 熔火蜥蜴（地心衝壓鍛造鎚）」的雙子火山重裝鐵衛陣容！
4. **純規格交付**：本階段**僅交付企劃規格與設定文件**，不產出圖片圖素、不產錄製影片、不派工後續任務、不改動底層遊戲程式碼與已鎖定之戰鬥時間模型（`BALANCE.md` §5），不改動 `paperdoll_slots.json` 正式權威來源。
5. **商業與數值護欄**：  
   - **絕對零數值（Zero Pay-to-Win）**：熔火蜥蜴素體與外觀部件 100% 不額外增加任何純外觀數值壓迫，嚴守 `docs/BUSINESS.md` 規範。  
   - **武器與職業對齊**：精準收斂至既有 6 職業 12 大武器體系中之 `viking`（戰士）下轄之 **`hammer`（鎚 / 戰士·鎚）** 系統，以【熔爐衝壓巨錘（Foundry Stamping Sledgehammer）】呈現。與鋼牙豕（鍛爐巨鎚）、玄軸熊（偏心重力錘）形成 100% 徹底區隔！

---

## 一、 職業與武器定位（Class & Weapon Prototype）

### 1.1 既有二十五族武器與職業光譜全盤點

盤點現有首發五族與前二十款擴充族的原生經典武器與職業分佈如下（嚴格對齊 `review.md` 23f-1 與 0-PLAN1 之正式中文名稱）：

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

在《發條之心》現有 `game/data/tables/weapon_classes.json` 明定的 6 大職業中：
- 前 24 族達成「6 職業 × 4 族 = 24 族」之大圓滿；
- 第 25 族巡林松鼠開啟第五巡首位騎士擴充；
- 第二十六種動物按照循環第二順位精準掛載於 **`viking`（戰士）** 職業體系，原生武器對齊 **`hammer`（鎚 / 戰士·鎚）**；
- 依據 `review.md` 23f-1 規定，職業正式名稱嚴格對齊為單一正式名：**`戰士 (Viking)`**。

### 1.2 熔火蜥蜴武器選擇：【熔爐衝壓巨錘（Foundry Stamping Sledgehammer）】

熔火蜥蜴原生專屬武器定名為：**【熔爐衝壓巨錘（Foundry Stamping Sledgehammer）】**。  
該武器直接承接並完美落地於 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 第 253 行特產武器「**熔爐衝壓巨錘（Foundry Stamping Sledgehammer）**」！  
底層完全掛載於 `weapon_classes.json` 的 `hammer`（戰士·鎚）類別，享有 `hammer` 既有的「站到最後」標籤宣言（Tagline: `\"站到最後\"`）、血防最厚、鍛造成功率暗中加成、硬吃招式耐力強之特性（`atk: 1, def: 4, hp: 12, crit: 0.0, speed: 0`），完美呼應 `R06_MOLTEN_FOUNDRY.md` 第 21 行「重型鍛造工坊與衝壓懸橋」、第 255 行「玄鐵精煉鑄錠」、第 256 行「耐高溫合金彈簧」、第 257 行「熔岩黑曜石拳板」、第 258 行「耐火石墨潤滑膏」與第 140 行「崩山衝壓擊」之地底工兵重力衝壓打擊感！

- **既有武器 ID 對齊（嚴格遵守規範）**：
  - 基礎入門與進階相容武器 ID：完全對齊 `game/data/tables/equipment.json` 第 262 行既有 ID **`anvil_hammer`（砧心小鎚）**（tier 1，line: \"hammer\"，`atk: 5, def: 3, hp: 10, crit: 0, crit_dmg: 6`），進階武器對齊第 275 行既有 ID **`iron_cudgel`（鐵骨重棒）**（tier 2，line: \"iron\"，`atk: 8, def: 2, hp: 8, crit: 2, crit_dmg: 8`），專屬高階款式對齊第 288 行既有 ID **`bastion_blade`（壁壘厚刃）**（tier 3，line: \"iron\"，`atk: 12, def: 4, hp: 12, crit: 3, crit_dmg: 10`）；
  - 專屬外觀款式 ID：明確標註為待審核專屬外觀款式 `weapon_salamander_foundry_stamping_sledgehammer`（待審核，底層 100% 繼承既有 line: \"hammer\"，數值直接掛載 `anvil_hammer` / `iron_cudgel` / `bastion_blade`，絕不自行創造未定義之程式數值 id）。
- **單持規範遵守**：遵循 `review.md 0-MKT7` 單持規範，右手單持熔爐衝壓巨錘（巨錘長柄為耐熱合金，鎚頭為方形帶氣動排氣孔與鍛造鐵砧面的衝壓鎚），斜倚於肩上作重裝待發架式；左手自然下垂握拳，身後五節重鋼大尾巴貼地提供三點支撐；全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。

### 1.3 差異化定位：與鋼牙豕（鍛爐鎚）、玄軸熊（偏心重力錘）及其他 23 族絕不撞型之論證

雖然熔火蜥蜴與鋼牙豕、玄軸熊同屬 `viking`（戰士）巨鎚（`hammer`）體系，但在**鍛造工藝與打擊手感**、**力學核心與動態性格**以及**剪影輪廓與材質語言**三大維度進行 100% 徹底差異化切割，確保玩家在手機小螢幕上於 0.5 秒內清晰辨識：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   戰士職業巨鎚武器差異化對照表（鋼牙豕 vs 玄軸熊 vs 熔火蜥蜴）           │
├───────────────────┬──────────────────────┬──────────────────────┬──────────────────────┤
│ 維度              │ 鋼牙豕（Forge Boar） │ 玄軸熊（Iron Bear）  │ 熔火蜥蜴（Salamander）│
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ① 職業與武器     │ 戰士 (Viking)        │ 戰士 (Viking)        │ 戰士 (Viking)        │
│                   │ 鍛爐巨鎚 (`hammer`)  │ 玄軸偏心重力錘(`hammer`)│ 熔爐衝壓巨錘 (`hammer`)│
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ② 打擊風格與節奏 │ 野性衝撞直線爆破、   │ 陀螺偏心旋轉、       │ 氣動衝壓活塞垂直爆扣、│
│                   │ 破城開山、正面硬撼   │ 磐石護體、重力引力場 │ 洩壓熱浪排氣、工兵爆破│
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ③ 力學核心與姿態 │ 雙獠牙合金破障角、   │ 內置巨大偏心飛輪、   │ 五節重鋼同軸阻尼大尾、│
│                   │ 腹部高壓蒸氣鍋爐     │ 雙肩雙聯液壓緩衝柱   │ 雙聯散熱導流鰭耳      │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ④ 材質語彙與色彩 │ 粗砂紅棕鑄鐵板件、   │ 蒸氣巨輪深灰鎢鋼、   │ 黑曜鎢鋼冷軋薄板、    │
│                   │ 鍛爐高溫紅銅排氣管   │ 拋光黃銅壓力儀表     │ 熔岩暖金飾邊、琥珀晶鏡│
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ⑤ 發條鑰匙造型   │ 厚重十字方栓鑰匙     │ 工業重型蝶形黃銅鑰匙 │ 四葉散熱鍛造發條鑰匙  │
├───────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ⑥ 所屬界域       │ R06 赤焰熔爐·鍛造火山 │ R04 黃銅都市·巨輪城  │ R06 赤焰熔爐·鍛造火山 │
└───────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

1. **打擊手感與戰鬥風格差異（野性衝撞 vs 偏心引力 vs 氣動垂直衝壓）**：
   - **鋼牙豕（鍛爐巨鎚）**：偏向野獸衝鋒與橫掃揮擊，大角度橫向壓制。
   - **玄軸熊（玄軸偏心重力錘）**：利用偏心陀螺旋轉慣性造成大範圍離心力破防，手感注重旋轉打擊與引力牽引。
   - **熔火蜥蜴（熔爐衝壓巨錘）**：全遊戲首位**「氣動衝壓工兵鐵衛（Pneumatic Sapper Forger）」**！核心手感著重於「垂直氣動爆砸（Vertical Piston Smash）」與「高溫蒸氣排氣震波（Thermal Exhaust Quake）」。每一次揮擊命中地面，巨錘頂端的氣動氣缸瞬間釋放高壓蒸氣，爆發出沉悶如巨型鍛造砧的「鏘——轟！」聲，附帶高溫蒸氣擴散。
2. **力學核心與動態性格（衝撞短身 vs 巨熊重肩 vs 低重心五節阻尼重尾）**：
   - 鋼牙豕依靠短粗的重裝四肢與獠牙角力；玄軸熊依靠寬厚肩膀的液壓緩衝柱吸收衝擊；
   - 熔火蜥蜴則依靠**「五節鉸鏈同軸沖壓耐熱重鋼大尾巴」**。內部配備高黏度耐火石墨阻尼器。在待機時大尾巴如重錨貼地，提供穩若磐石的三點支撐；在掄起巨錘騰空下砸時，大尾巴猛烈上翹以物理力矩抵消上半身翻滾慣性，展現出無與倫比的機械穩定性與蜥蜴爬蟲工兵反差萌。
3. **幾何剪影與材質語彙（尖嘴獠牙 vs 圓滾熊體 vs 爬蟲低趴流線金屬護盾）**：
   - 熔火蜥蜴呈現 2.2 頭身低重心幾何剪影，頭頂兩道流暢的耐熱散熱鰭片，身著鉚接鍛造隔熱圍裙，身後拖著厚實堅固的金屬重鋼尾，在小螢幕上即使縮小至 32 像素，也能憑藉「低趴流線爬蟲頭部＋龐大氣動巨錘＋五節重鋼大尾」瞬間秒認。

---

## 二、 角色形象與外觀定調（Visual & Mechanism Spec）

### 2.1 角色基本檔案

- **官方正式中文名**：熔火蜥蜴
- **官方英文名稱**：The Magma Salamander
- **角色頭銜**：地心工兵·重裝鍛火者（Foundry Sapper: Heavy Forger）
- **性格原型（Archetype）**：沉穩、耐高溫、寡言而極度專注的火山地心管道維修工兵與鍛造鐵匠。對高溫熔岩與失控蒸氣視若等閒，堅信「世上沒有敲不平的壞零件，只有洩不出的過熱廢氣」。
- **核心台詞（語錄）**：「熔岩燙不壞咬緊的齒輪，只要握緊鍛錘——每一擊都能敲正世界的走時！」
- **所屬界域**：`R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano`
- **地標錨點（經 R06 嚴格查驗對齊）**：
  - 「重型鍛造工坊與衝壓懸橋」（R06 第 21 行）
  - 「氣動衝壓懸橋」（R06 第 206 行）
  - 「高壓地熱噴射升空彈射井」（R06 第 32 行）
  - 「淬火冷卻噴淋池」（R06 第 47 行）
  - 「火山口中央核心鍛造神壇」（R06 第 102 行、第 162 行）

### 2.2 幾何剪影與機械特徵（恪守 CANON.md 零毛皮鐵律）

1. **100% 零毛皮、零肉身、零軟組織轉譯**：
   - **軀體與面部**：通體嚴格禁止任何爬蟲真皮、鱗片肉質、黏液與生物軟組織。外殼全面採用「黑曜鎢鋼冷軋薄板（#2A2B32）」經高溫回火沖壓拼裝而成，邊緣鑲嵌「熔岩暖金飾邊（#D47A2A）」；面頰兩側為「溫潤奶油米白琺瑯面罩（#FFFDF8）」，以四顆沉頭螺栓穩固密封，防止高溫灰塵入侵機芯。
   - **散熱鰭角（耳部機關）**：頭頂兩側為雙聯折疊耐熱散熱導流鰭角，由薄銅散熱葉片層疊而成，在體內過熱時會如同百葉窗般展開釋放微型雪白蒸氣。
   - **耐熱重鋼大尾巴（核心辨識符號）**：五節同軸鉸鏈串接的沖壓耐熱重鋼大尾巴。每一節均為厚重黑曜鋼板，內部裝載耐火石墨潤滑阻尼器。在地面滑行時自帶清脆的鋼板摩擦聲，作為站立與揮錘時的反作用力支點。
   - **眼珠光學**：面部嵌有一對圓形「琥珀橙高溫光學水晶目鏡（#FFA010）」，鏡面內刻同心圓熔壓刻度計與溫度警戒紅線，注視目標時閃爍著堅毅深沉的光芒。
   - **四肢與爪靴**：四肢關節為粗壯耐熱球窩關節（#4A5568 冷軋鎢鋼），足部為加寬防滑耐磨合金爪靴，前端帶有三枚粗短的平底抓地齒，能在滾燙花紋鋼板與光滑岩石上穩健推進。
2. **服飾與外裝（Slot 4: Costume）**：
   - 身穿「地熱工兵耐火鉚接圍裙與吊帶（#FF5E8A 珊瑚粉金屬扣帶搭配耐火暗棕皮面）」，斜跨一條多巴胺金黃齒輪工具帶（#FFD028），掛載小型手動注油注脂槍與精密螺絲扳手；胸前護甲嵌有一面微縮蒸氣壓力錶。

### 2.3 發條鑰匙規格：【四葉散熱鍛造發條鑰匙（Four-Vane Heat-Sink Forging Key）】

- **鑰匙 ID**：`key_salamander_four_vane_heatsink`
- **中文名稱**：四葉散熱鍛造發條鑰匙
- **英文名稱**：Four-Vane Heat-Sink Forging Key
- **造型特徵**：由耐高溫鍛造合金與黃銅一體鑄造，頂部為古典四葉閥輪排氣孔造型，每片葉片外緣帶有微縮散熱格柵，中心鑲嵌一枚小巧的金屬鉚釘；
- **安裝位置**：背部中央偏高位（`back_center_high`），穿過耐火工兵背帶直插體內主發條盒；
- **動態與聲效**：自帶穩健慢速旋轉（每 5 秒旋轉一圈），伴隨沉穩厚重的「嗒——咯、咯」金屬制動聲，在揮動巨錘蓄力時，四葉排氣孔噴吐微型金色火星氣流。

### 2.4 塗裝與色票規劃（8 組多巴胺鮮亮高飽和色盤）

全角色色彩嚴格對標《塔塔冒險隊》與《新楓之谷》之陽光童話多巴胺色調，徹底杜絕髒黑、泥土暗沉與恐怖廢土感：

```
┌──────────────────┬─────────────┬────────────────────────────────────────────────────────┐
│ 色彩名稱         │ 色票 Hex    │ 應用部位與材質質感                                     │
├──────────────────┼─────────────┼────────────────────────────────────────────────────────┤
│ 1. 黑曜鎢鋼 (主) │ #2A2B32     │ 主軀幹外殼、手臂重鋼外板、大尾巴基底板件（回火冷光）   │
│ 2. 熔岩暖金 (次) │ #D47A2A     │ 板件邊緣飾緣、大尾巴分節鉸鏈環片、散熱角外導流面       │
│ 3. 奶油米白 (琺瑯│ #FFFDF8     │ 面部琺瑯面罩、下顎板件、胸甲中心溫潤護心盤             │
│ 4. 金黃齒輪 (散熱│ #FFD028     │ 腹部散熱百葉窗、四葉發條鑰匙、巨錘氣動洩壓閥、工具腰帶 │
│ 5. 琥珀澄光 (目鏡│ #FFA010     │ 雙眼高溫光學水晶鏡片、巨錘地熱能量核心（高透光亮色）   │
│ 6. 冷軋鎢鋼 (骨架│ #4A5568     │ 四肢耐熱球窩關節、足底防滑抓地齒、巨錘合金長柄         │
│ 7. 珊瑚粉紅 (服飾│ #FF5E8A     │ 地熱工兵吊帶飾扣、巨錘氣管隔熱護圈（多巴胺活潑點綴）   │
│ 8. 深藍紫   (描邊│ #1F1A3A     │ 全角色外輪廓深色厚描邊（2~3px 經典賽璐璐手繪線條）     │
└──────────────────┴─────────────┴────────────────────────────────────────────────────────┘
```

---

## 三、 紙娃娃 7 大部件槽位設計（7-Slot Paperdoll Architecture）

依據 `docs/design/PAPERDOLL_SLOTS_SPEC.md` 與 `mob-paperdoll` 模組化規範，規劃 7 大獨立槽位，全面支援衣櫥自由混搭：

```
                    ┌──────────────────────────────────────────────┐
                    │ Slot 3: 發條鑰匙 (Winding Key)               │
                    │ key_salamander_four_vane_heatsink            │
                    │ (四葉散熱鍛造發條鑰匙)                       │
                    └──────────────────────┬───────────────────────┘
                                           ▼
┌───────────────────────────────┐        ┌───┐        ┌───────────────────────────────┐
│ Slot 2: 頭部/鰭角 (Head Unit) │        │角 │        │ Slot 5: 面部光學 (Optic Core) │
│ head_salamander_radiator_     │───────▶│色 │◀───────│ face_salamander_amber_dial_   │
│ crest_horns                   │        │   │        │ lens                          │
│ (折疊耐熱散熱鰭角)            │        │紙 │        │ (琥珀澄光熔壓目鏡)            │
└───────────────────────────────┘        │   │        └───────────────────────────────┘
┌───────────────────────────────┐        │娃 │        ┌───────────────────────────────┐
│ Slot 1: 外殼材質 (Chassis)    │        │   │        │ Slot 4: 玩具服飾 (Costume)    │
│ chassis_salamander_magma_     │───────▶│娃 │◀───────│ costume_salamander_foundry_   │
│ tungsten_default              │        │   │        │ sapper_apron                  │
│ (黑曜鎢鋼耐熱金屬素體)        │        │素 │        │ (地熱工兵耐火鉚接圍裙)        │
└───────────────────────────────┘        │   │        └───────────────────────────────┘
┌───────────────────────────────┐        │體 │        ┌───────────────────────────────┐
│ Slot 6: 手持武器 (Weapon)     │        │   │        │ Slot 7: 隨身背飾 (Back Curio) │
│ weapon_salamander_foundry_    │───────▶│   │◀───────│ curio_salamander_segmented_   │
│ stamping_sledgehammer         │        └───┘        │ damping_tail                  │
│ (熔爐衝壓巨錘)                │                     │ (五節重鋼同軸阻尼大尾巴)      │
└───────────────────────────────┘                     └───────────────────────────────┘
```

### 3.1 各槽位規格明細

1. **Slot 1: 素體外殼（Chassis）**
   - **預設 ID**：`chassis_salamander_magma_tungsten_default`
   - **外觀描述**：2.2 頭身低重心 Q 版發條蜥蜴金屬素體。主軀幹由黑曜鎢鋼冷軋薄板（#2A2B32）沖壓而成，邊緣鑲嵌熔岩暖金飾邊（#D47A2A），面部覆蓋溫潤奶油米白琺瑯面罩（#FFFDF8），胸前具備散熱排氣小格柵。
2. **Slot 2: 頭部與鰭角機關（Head Unit）**
   - **預設 ID**：`head_salamander_radiator_crest_horns`
   - **外觀描述**：雙聯折疊式耐熱薄銅散熱導流鰭角，表面具有細密散熱片刻線，過熱時微幅向外展開洩壓。
3. **Slot 3: 背部發條鑰匙（Winding Key）**
   - **預設 ID**：`key_salamander_four_vane_heatsink`
   - **外觀描述**：四葉散熱鍛造發條鑰匙，黃銅閥輪排氣孔造型，自帶微型金色火星旋轉特效。
4. **Slot 4: 服飾外裝（Costume）**
   - **預設 ID**：`costume_salamander_foundry_sapper_apron`
   - **外觀描述**：地熱工兵耐火鉚接圍裙。包含耐磨皮質圍裙、珊瑚粉金屬扣帶、工具懸掛金黃腰帶及胸口指針式微型蒸氣壓力錶。
5. **Slot 5: 面部光學與表情（Optic Core / Accessory）**
   - **預設 ID**：`face_salamander_amber_dial_lens`
   - **外觀描述**：直徑 12px 圓形琥珀澄光高溫光學水晶鏡片（#FFA010），鏡面雷射微雕同心圓熔壓刻度計與溫度警戒指針。
6. **Slot 6: 手持武器（Weapon）**
   - **預設 ID**：`weapon_salamander_foundry_stamping_sledgehammer`
   - **外觀描述**：右手單持熔爐衝壓巨錘。長柄約 52px，錘頭為四方帶洩壓孔的氣動鋼砧錘（寬 28px × 高 24px），揮動時尾端散逸淡金色熱浪。
7. **Slot 7: 隨身背飾與尾部奇玩（Curio / Back Curio）**
   - **預設 ID**：`curio_salamander_segmented_damping_tail`
   - **外觀描述**：五節同軸鉸鏈沖壓耐熱重鋼大尾巴。長約 48px，末端厚重平整，貼地滑行提供穩固三點支撐。

---

## 四、 六大戰鬥動作姿態意象拆解（Six Combat Poses Breakdown）

嚴格對齊 `docs/design/PAPERDOLL_SLOTS_SPEC.md` 與 128×128 像素戰鬥精靈幀標準：

1. **`idle`（待機 / 重裝穩健站姿）**：
   - 2.2 頭身蜥蜴雙足寬距踏地，身軀低重心微幅呼吸起伏（週期約 1.1 秒，垂直浮動 2px）；
   - 右手單持熔爐衝壓巨錘斜架於肩頭，左手握拳置於腰側，身後五節重鋼尾巴穩貼地面作為三腳架支撐，散熱鰭角緩緩微張微合。
2. **`telegraph`（前搖蓄勁 / 氣缸增壓上揚）**：
   - 雙膝深蹲蓄力，右手將巨錘高高向後上方舉起，錘頭氣動氣缸「吱——嗤！」拉伸蓄壓；
   - 尾巴猛然向後水平懸空鎖死作為平衡配重，雙目琥珀橙鏡片指針飆升至警戒紅線，地面震落微型金黃火星。
3. **`attack`（普攻出手 / 氣動鍛砧下砸）**：
   - 藉由下蹲彈簧瞬間爆發躍起半步，巨錘伴隨萬鈞之勢雷霆下砸（Vertical Sledge Slam）；
   - 錘頭接觸地面的剎那，氣缸噴出環形高壓白霧與金色火花「鏘——轟！」，引發地面輕微微震，重創敵人護甲。
4. **`skill`（怒氣大招·赤焰八荒天爐破 / 崩山衝壓擊）**：
   - 背部四葉鑰匙超頻疾轉，尾巴瘋狂甩動噴射熱浪，蜥蜴高高躍起 4 米空中；
   - 雙手合抱巨錘藉助重力與下墜動能轟然向下暴扣，直接於地面引發直徑 6 米的環形熔岩地裂衝擊波，伴隨「崩山衝壓擊」強烈破壞 BOSS 外裝零件！
5. **`hit`（受擊震顫）**：
   - 身軀後仰 15 度，圍裙金屬扣微響，胸口蒸出數團白色冷卻水霧；
   - 重鋼大尾巴猛然拍打地面自鎖剎車，巨錘及時杵地穩住重心，迅速回正身位。
6. **`recover`（倒地虛弱 / 散熱冷卻休眠）**：
   - 體內發條暫時洩壓停機，單膝跪地，巨錘斜支於旁支撐上身，頭部鰭角完全展開散熱；
   - 冷卻 0.7 秒後，背部主發條盒「咔噠」一聲咬合復位，眼部琥珀光再次點亮，生龍活虎地揮錘躍起。

---

## 五、 產品層准入（PRODUCT_LOCK_0.20.md §9 門檻自答）

依據《0.20 Product Lock》第 9 節規定，任何新增內容必須完整自答准入門檻六題，逐題檢驗合格方准備案：

### Q1：它掛在 §3.1 核心循環的哪一環？
> **合格回答**：**精準掛在「養成」與「解鎖玩具／發條」這一環。**  
> **詳細論證**：  
> 熔火蜥蜴並非孤立的新玩法，而是現有 7 大紙娃娃換裝體系（`mob-paperdoll`）在二十五族基礎上的「第 26 款可解鎖動物素體外殼（Chassis）」。玩家透過通關 R06 赤焰熔爐·鍛造火山章節探索獎勵、擊破旗艦 BOSS·工坊守衛泰坦·重裝石拳鐵豕掉落稀有素材「玄鐵精煉鑄錠」與「耐高溫合金彈簧」在火山口中央鍛造神壇組裝解鎖、或外觀盲盒抽取獲得；解鎖後完全複用客戶端既有的武器鍛造、十四星軸入魂、怒氣技能樹三層養成鏈，百分之百依循 `探索 → 戰鬥 → 掉落 → 養成 → 解鎖玩具／發條 → 新區域 → 劇情` 的唯一直線主循環。

### Q2：它服務 §1.6 哪一根體驗支柱？第幾優先？
> **合格回答**：**同時服務第 1 支柱（第一優先）與第 2 支柱（第二優先）。**  
> **詳細論證**：  
> 1. **服務第 1 支柱（第一優先：世界與角色）**：補強 R06 赤焰熔爐·鍛造火山僅有鋼牙豕一族的生態短板！以古典經典發條金屬爬蟲玩具為底蘊，搭配黑曜鎢鋼冷軋薄板、熔岩暖金飾邊與四葉散熱鍛造鑰匙，完美體現「地心管網工兵與重裝鍛火者」的童話機械工匠氛圍。  
> 2. **服務第 2 支柱（第二優先：即時戰鬥演出）**：2.2 頭身低重心剪影、五節同軸重鋼尾、氣動巨錘爆砸下落震撼力極強，在手機小螢幕上即使無 UI 也能一眼辨識出是耐熱蜥蜴在剛猛鍛砸，為戰士職業巨鎚體系增添前所未有的氣動衝壓打擊手感。

### Q3：玩家在手機上用單手拇指能不能操作它？
> **合格回答**：**100% 能。**  
> **詳細論證**：  
> 熔火蜥蜴完全沿用現有的橫屏雙拇指手遊人體工學架構：創角與衣櫥換裝卡片熱區均 ≥ 48px，杜絕誤觸；戰鬥中點擊單鍵即可順暢完成連續重砸、氣缸增壓與全螢幕怒氣大招釋放，絕無複雜多指搓招或虛擬搖桿拖曳負擔，完全保留單手大拇指暢玩之流暢體驗。

### Q4：它需不需要伺服器才能運作？（需要就違反 §6）
> **合格回答**：**完全不需要。**  
> **詳細論證**：  
> 熔火蜥蜴的素體結構、貼圖切片與動畫參數全部離線封裝於客戶端本機資料庫。在離線無網路狀態下，玩家可順暢創建角色、換裝與通關全主線副本，嚴格恪守 §6「保留零連線可通關」原則。

### Q5：它會不會讓首包超過 §5.2 的 50～80 MB？
> **合格回答**：**絕對不會。**  
> **詳細論證**：  
> 單一套動物素體的完整 2D 資產清冊包括：400×840 官方立牌（約 210 KB）、128×128 戰鬥 6 姿態圖（約 110 KB）、7 槽位局部切片圖層（約 150 KB），經 TinyPNG / WebP 壓縮後，總資產增量嚴格控制在 **0.8 MB 以內**。⚠️ 需特別注意 `PRODUCT_LOCK_0.20.md` §5.2 記載之現況為「Web 目錄 135 MB」、首包目標 50～80 MB，**目前尚未達標**；本族的 0.8 MB 增量相對於該既有缺口極小，但首包瘦身是專案既有欠帳，不因本提案而消解。

### Q6：為了做它，要放棄什麼？（「不用放棄什麼」一律退件）
> **合格回答**：  
> 1. **放棄為蜥蜴爬蟲繪製生物濕滑真皮、黏液與肉質軟組織的奢想**：放棄一切生物生物組織與黏液流體模擬，嚴格將材質收斂為「冷軋黑曜鎢鋼板、熔岩暖金飾邊、奶油琺瑯面罩與五節重鋼同軸尾」，並嚴格遵循 `weapon_classes.json` 的 `hammer` 數值與已鎖定之 `BALANCE.md` §5 時間模型（0.15），捍衛低階手機流暢度與戰鬥平衡。  
> 2. **放棄寫實笨重無法自拔的繁瑣硬直機制**：放棄寫實鍛錘過度冗長的拖沓前後搖，將其提煉為符合手遊明快節奏的「氣動增壓後起手＋沉穩垂直下砸」，色彩採用「多巴胺黑曜鎢鋼（#2A2B32）、熔岩暖金（#D47A2A）、琥珀澄光（#FFA010）與金黃（#FFD028）」，展現發條玩具在地心陽光與熱浪中熱血鍛打的童話核心。

---

## 六、 機器讀取規格配置章節（paperdoll_slots.json 擴充對照段落）

後續待審核通過後，可直接映射併入 `docs/design/paperdoll_slots.json` 之結構化配置段落如下（僅供資料規格備案，本任務不直接竄改主檔）：

```json
{
  "race_id": "salamander",
  "race_name_zh": "熔火蜥蜴",
  "race_name_en": "The Magma Salamander",
  "class_archetype": "戰士 (Viking)",
  "weapon_line": "hammer",
  "native_realm_id": "R06",
  "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
  "lore_anchor": [
    "重型鍛造工坊與衝壓懸橋",
    "氣動衝壓懸橋",
    "高壓地熱噴射升空彈射井",
    "淬火冷卻噴淋池",
    "火山口中央核心鍛造神壇"
  ],
  "palette": {
    "primary_hull": "#2A2B32",
    "secondary_hull": "#D47A2A",
    "faceplate_enamel": "#FFFDF8",
    "gold_accent": "#FFD028",
    "amber_optic": "#FFA010",
    "tungsten_frame": "#4A5568",
    "apron_coral": "#FF5E8A",
    "outline": "#1F1A3A"
  },
  "winding_key_spec": {
    "key_id": "key_salamander_four_vane_heatsink",
    "name_zh": "四葉散熱鍛造發條鑰匙",
    "name_en": "Four-Vane Heat-Sink Forging Key",
    "position": "back_center_high",
    "rotation_sound": "sfx_foundry_valve_ratchet"
  },
  "slots_manifest": {
    "chassis": "chassis_salamander_magma_tungsten_default",
    "head_unit": "head_salamander_radiator_crest_horns",
    "costume": "costume_salamander_foundry_sapper_apron",
    "optic_core": "face_salamander_amber_dial_lens",
    "winding_key": "key_salamander_four_vane_heatsink",
    "weapon": "weapon_salamander_foundry_stamping_sledgehammer",
    "curio": "curio_salamander_segmented_damping_tail"
  },
  "pending_assets": [
    "game/assets/sprites/player/paperdoll/salamander/chassis/chassis_salamander_magma_tungsten_default.png",
    "game/assets/sprites/player/paperdoll/salamander/head_unit/head_salamander_radiator_crest_horns.png",
    "game/assets/sprites/player/paperdoll/salamander/costume/costume_salamander_foundry_sapper_apron.png",
    "game/assets/sprites/player/paperdoll/salamander/optic_core/face_salamander_amber_dial_lens.png",
    "game/assets/sprites/player/paperdoll/salamander/winding_key/key_salamander_four_vane_heatsink.png",
    "game/assets/sprites/player/paperdoll/salamander/weapon/weapon_salamander_foundry_stamping_sledgehammer.png",
    "game/assets/sprites/player/paperdoll/salamander/back_curio/curio_salamander_segmented_damping_tail.png",
    "game/assets/sprites/player/paperdoll/key/key_salamander_four_vane_heatsink.png",
    "game/assets/sprites/player/paperdoll/weapon/weapon_salamander_foundry_stamping_sledgehammer.png",
    "game/assets/sprites/player/paperdoll/salamander/proof_paperdoll_salamander_composite.png",
    "game/assets/sprites/player/paperdoll/salamander/proof_paperdoll_salamander_magenta.png",
    "game/assets/sprites/player/paperdoll/salamander/proof_salamander_all_7_slices.png",
    "game/assets/sprites/player/battle/salamander/salamander_battle_poses_128.png",
    "game/assets/sprites/player/showcase/salamander_idle_hd.png"
  ]
}
```

---

## 七、 效能與包體預算評估（Performance & Package Budget）

### 7.1 資產增量預算（Asset Budget Breakdown）

嚴格執行手機輕量化標準，全資產經過 TinyPNG / WebP 無損/高保真壓縮：

```
┌──────────────────────────────────────────────────────────────┬───────────────┬──────────────┐
│ 資產類別與檔案路徑                                           │ 原始預估容量  │ 壓縮後目標   │
├──────────────────────────────────────────────────────────────┼───────────────┼──────────────┤
│ 1. 400×840 官方立牌展台圖 (salamander_idle_hd.png)           │ ~450 KB       │ ≤ 210 KB     │
│ 2. 128×128 戰鬥六姿態精靈圖 (6 幀 768×128 條狀圖)           │ ~240 KB       │ ≤ 110 KB     │
│ 3. 7 大紙娃娃獨立槽位切片圖層 (128×128 RGBA8888 × 7)         │ ~300 KB       │ ≤ 150 KB     │
│ 4. 通用目錄鏡像檔 (key/ 與 weapon/ 兩枚圖示)                 │ ~60 KB        │ ≤ 30 KB      │
│ 5. 驗收合成圖與洋紅邊界校驗圖 (僅存證，不打包進 Release)     │ [Dev Only]    │ [0 KB 首包]  │
├──────────────────────────────────────────────────────────────┼───────────────┼──────────────┤
│ 總計（加入首包之正式 Release 資產增量）                      │ ~1.05 MB      │ ≤ 0.50 MB    │
└──────────────────────────────────────────────────────────────┴───────────────┴──────────────┘
```

- **包體欠帳與門檻說明**：
  - 據實核對現狀：`PRODUCT_LOCK_0.20.md` §5.2 明載當前專案 Web 目錄為 135 MB，距離目標 50~80 MB 尚在收斂推進中，本提案嚴格保證單族增量 < 0.8 MB，不增加額外首包負擔。

### 7.2 執行期記憶體與 Token 成本評估（Runtime & Token Cost）

1. **客戶端記憶體與 DrawCall 負載**：
   - 熔火蜥蜴 7 大槽位切片完全複用既有的 2D 紙娃娃 CanvasItem 著色器（`sprite_db.gd`），不新增額外材質 Pass；
   - 單一角色待機狀態佔用 VRAM 約 1.0 MB，符合行動裝置低階 2GB RAM 設備同屏 10 人流暢 60 FPS 規範。
2. **LLM 描述與資料結構 Token 預算**：
   - 機器讀取規格配置段落（JSON）嚴格控制在 300 ~ 330 tokens 之間；
   - 欄位命名嚴格遵循既有 `paperdoll_slots.json` 規範，避免冗餘深層巢狀結構，大幅降低後續 Agent 在解析、檢索與代碼生成時的 Prompt 上下文開銷。

---

## 八、 驗收 Checklist（對齊 review.md、0-PLAN1、23f-1、0-MKT7 與 CANON 規範）

- [x] **CANON.md 零毛皮鐵律**：100% 零真爬蟲皮、零肉質、零黏液、零肉身、零生物軟組織；全數轉譯為沖壓黑曜鎢鋼冷軋薄板件、溫潤奶油米白琺瑯面頰與面罩、五節同軸鉸鏈重鋼阻尼大尾巴、雙聯折疊耐熱散熱鰭角、琥珀橙光學水晶目鏡、四葉散熱鍛造發條鑰匙與鎢鋼防滑抓地爪靴。
- [x] **CANON.md 背部發條鑰匙**：背部高位動力插座配備「四葉散熱鍛造發條鑰匙」，黃銅閥輪散熱排氣造型，旋轉伴隨沉穩金屬制動鳴響「嗒——咯、咯」。
- [x] **review.md 23f-1 職業正式名稱**：正式名稱精準採用單一規範名：**`戰士 (Viking)`**，完全依據 `weapon_classes.json` 規範名，無任何自創新名。
- [x] **review.md 0-MKT7 單持武器規範**：右手單持熔爐衝壓巨錘架於肩頭，左手自然下垂握拳，身後五節大尾巴貼地支撐，全圖精確為 1 把武器，0 佔位短棒，0 多餘浮動武器，0 雙持穿模違規。
- [x] **既有武器 ID 嚴格對齊**：精準對應 `equipment.json` 第 262 行既有 `anvil_hammer`（砧心小鎚）、第 275 行 `iron_cudgel`（鐵骨重棒）與第 288 行 `bastion_blade`（壁壘厚刃）；專屬款式 `weapon_salamander_foundry_stamping_sledgehammer` 明確標註待審，底層掛載 `hammer` line，不准自行創造未審 id。
- [x] **review.md 0-PLAN1 必查點 1（地標查驗）**：`lore_anchor` 所載「重型鍛造工坊與衝壓懸橋」、「氣動衝壓懸橋」、「高壓地熱噴射升空彈射井」、「淬火冷卻噴淋池」與「火山口中央核心鍛造神壇」逐字比對 `docs/world/regions/R06_MOLTEN_FOUNDRY.md` 第 21 行、第 206 行、第 32 行、第 47 行與第 102/162 行 100% 存在，無任何自創詞彙。
- [x] **review.md 0-PLAN1 必查點 2（首包數字查驗）**：據實引用 `PRODUCT_LOCK_0.20.md` §5.2 現況「Web 目錄 135 MB、首包目標 50~80 MB、尚未達標」，預估單族資產增量 < 0.8 MB，未捏造已達標假前提。
- [x] **review.md 0-PLAN1 必查點 3（區域編號查驗）**：精準掛載 `R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano`，編號與區域名稱與既有檔案第 1 行 100% 一致。
- [x] **review.md 0-PLAN1 必查點 4（盤點表職業中文名）**：第 1.1 節既有二十五族盤點表職業中文名稱全數採用正式標準名稱（騎士/法師/戰士/武術家/忍者/遊俠），精確盤點既有 25 族（含第 21 族棘輪刺蝟、第 22 族荒原鋼狼、第 23 族琉璃海馬、第 24 族鐵拳袋鼠與第 25 族巡林松鼠）。
- [x] **世界觀素材與法源對齊**：完美銜接 R06 第 45 行「發條耐火工兵蜥蜴」法源，特產武器掛載第 253 行「熔爐衝壓巨錘」，材料對齊第 255 行「玄鐵精煉鑄錠」、第 256 行「耐高溫合金彈簧」與第 258 行「耐火石墨潤滑膏」。
- [x] **差異化論證**：深入論證與鋼牙豕（鍛爐巨鎚）、玄軸熊（偏心重力錘）在戰鬥打擊（氣動垂直衝壓 vs 野性衝撞 vs 偏心引力）、動態平衡（重鋼同軸阻尼尾 vs 液壓緩衝柱 vs 粗壯短腿）與材質色盤上的 100% 徹底區隔。
- [x] **7 大紙娃娃槽位完整度**：Slot 1~7 涵蓋 chassis / head_unit / winding_key / costume / optic_core (accessory) / weapon / curio (back_curio)，命名規則與擴充款式定義完備，可供美術直接產切片。
- [x] **純文件交付邊界**：嚴守任務要求，未產圖、未產片、零花費、未改動底層程式碼與正式 `paperdoll_slots.json` 權威檔。

---

## 九、 六語系在地化對照表（Localization Lexicon）

| 專有名詞分類 | 繁體中文 | 簡體中文 | 英文（EN） | 西班牙文（ES） | 日文（JA） | 韓文（KO） |
|:---|:---|:---|:---|:---|:---|:---|
| **角色全名** | 熔火蜥蜴 | 熔火蜥蜴 | The Magma Salamander | La Salamandra Magmática | マグマ・サラマンダー | 마그마 살라맨더 |
| **角色頭銜** | 地心工兵·重裝鍛火者 | 地心工兵·重装锻火者 | Foundry Sapper: Heavy Forger | Zapador de Fundición: Forjador Pesado | 炉心工兵・重装鍛冶師 | 지심 공병·중장 단조자 |
| **原生武器** | 熔爐衝壓巨錘 | 熔炉冲压巨锤 | Foundry Stamping Sledgehammer | Maza Estampadora de Fundición | 熔炉プレス巨槌 | 용광로 프레스 거대망치 |
| **專屬發條鑰匙**| 四葉散熱鍛造發條鑰匙 | 四叶散热锻造发条钥匙 | Four-Vane Heat-Sink Forging Key | Llave Forjada de Cuatro Aspas Disipadoras | 四葉放熱鍛造ぜんまい鍵 | 4엽 방열 단조 태엽 키 |
| **頭部鰭角** | 折疊耐熱散熱鰭角 | 折叠耐热散热鳍角 | Folding Radiator Crest Horns | Crestas Plegables de Disipación Térmica | 折畳耐熱放熱フィン角 | 접이식 내열 방열 핀 뿔 |
| **面部光學** | 琥珀澄光熔壓目鏡 | 琥珀澄光熔压目镜 | Amber Dial Pressure Lens | Lente Óptica de Presión Ámbar | 琥珀ダイヤル熔圧レンズ | 호박 다이얼 용압 렌즈 |
| **核心背飾** | 五節重鋼同軸阻尼大尾 | 五节重钢同轴阻尼大尾 | Segmented Heavy Steel Damping Tail | Cola Amortiguadora de Acero Pesado | 五節重鋼同軸ダンパー大尾 | 5마디 중강 동축 댐핑 꼬리 |
| **核心招式 1** | 氣動衝壓垂直爆砸 | 气动冲压垂直爆砸 | Pneumatic Piston Slam | Golpe de Pistón Neumático | 気動プレス垂直スマッシュ | 기동 프레스 수직 강타 |
| **核心招式 2** | 赤焰八荒天爐破 | 赤焰八荒天炉破 | Eight-Realms Crucible Cataclysm | Cataclismo del Crisol de Ocho Reinos | 赤焔八荒天炉破 | 붉은 불꽃 팔황 천로파 |
| **核心機制** | 氣動洩壓熱浪震波 | 气动泄压热浪震波 | Pneumatic Thermal Shockwave | Onda de Choque Térmica Neumática | 気動減圧熱波衝撃波 | 기동 감압 열파 충격파 |
