# 第六種動物「烈焰虎（The Ember Tiger）」美術資產需求清單與切片規格書

> **文件狀態**：美術資產需求清單（Asset Checklist & Specification - Ready for Review）  
> **制定日期**：2026-09-16  
> **負責人**：側案·策劃總監 小凱（sideplan）  
> **審核對象**：側案製作人 老周（side）、側案美術總監 小柔（sideart）  
> **對應看板任務**：`t_828248d3`（📢 行銷｜烈焰虎（第六族）美術規格書已過審，寫紙娃娃素材需求清單）  
> **關聯前置任務**：`t_1ddf03d2`（📖 世界觀｜第六種動物「烈焰虎」紙娃娃角色設計提案，已審核通過）  
> **依據與對齊文件**：  
> - `docs/design/EMBER_TIGER_DESIGN_PROPOSAL.md`（現行已過審核心定案文件）  
> - `docs/design/paperdoll_slots.json`（7 大部件槽位機器讀取規格）  
> - `docs/design/PAPERDOLL_SLOTS_SPEC.md`（紙娃娃系統 7 大槽位與五族資產目錄規範）  
> - `game/data/tables/weapon_classes.json`（6 職業 12 大武器系統）  
> - `docs/world/CANON.md`（世界憲章：100% 零毛皮、全金屬/琺瑯玩具、背部發條鑰匙）  
> - `docs/art/art_direction.md` / `docs/ART_DIRECTION.md`（多巴胺鮮亮高飽和色盤、深藍紫厚描邊）  
> - `docs/BUSINESS.md`（F2P + 外觀無數值壓迫 Zero P2W）  

---

## 0. 執行邊界與過審規格比對總表（Specification Alignment Matrix）

本文件為純規劃與資產清單規格文件，**不產圖、不產影片、不花費任何額外生成預算**。旨在為下一棒美術總監（小柔 sideart）提供精確的切片與姿態生產需求，並為程式（阿宏 sideworker）預留標準檔案路徑。

本清單嚴格對照已過審之《烈焰虎設計提案》（`docs/design/EMBER_TIGER_DESIGN_PROPOSAL.md`），重點規格對照如下：

| 規格編號 | 提案定案規格條目 (`EMBER_TIGER_DESIGN_PROPOSAL.md`) | 本資產清單落地與收斂要求 | 合規性校核 |
|:---:|:---|:---|:---:|
| **Spec-01** | **職業收斂為「忍者（Ninja）」** | 標籤收斂至既有 6 職業之 `ninja`，嚴禁衍生刺客、狂戰等未定義職業標籤。 | ✅ 100% 對齊 |
| **Spec-02** | **武器定案「雙短刃 / 苦無（dagger）」** | 比照既有白霧（Fog）忍者定調，掛載 `dagger`（忍者·匕），不自創新武器類型。 | ✅ 100% 對齊 |
| **Spec-03** | **CANON 零毛皮世界憲章** | 嚴禁生物毛皮與肉質，虎斑以消光碳黑耐熱鋼板嵌件與百葉散熱狹縫呈現。 | ✅ 100% 對齊 |
| **Spec-04** | **標誌性機械剪影** | 額頭「工字加固鋼樑」、雙側「散熱百葉耳」、尾部「4 節分節排氣管重力虎尾」。 | ✅ 100% 對齊 |
| **Spec-05** | **多巴胺鮮亮色盤** | #E65100 餘燼橙紅、#2B2B36 碳黑耐熱鋼板、#FFA010 熔火琥珀金、#1F1A3A 深藍紫描邊。 | ✅ 100% 對齊 |
| **Spec-06** | **7 大紙娃娃部件槽位架構** | 完整對齊 `paperdoll_slots.json` 之 chassis / head_unit / winding_key 等 7 槽位。 | ✅ 100% 對齊 |
| **Spec-07** | **六大戰鬥動作姿態（128×128）** | 嚴格規範 attack / hit / idle / recover / skill / telegraph 六大動作幀意象。 | ✅ 100% 對齊 |
| **Spec-08** | **商業與數值護欄** | 純外觀資產，絕對零數值壓迫（Zero P2W），單機離線本機封裝無伺服器相依。 | ✅ 100% 對齊 |

---

## 一、 7 大模組化部件槽位需求清單（對照 paperdoll_slots.json）

依照《發條之心》既有 7 大紙娃娃槽位（`mob-paperdoll`）與分層渲染管線（Layered Sprite Multi-pass 2D Z-Ordering），烈焰虎專屬素體切片規範如下：

```
                    ┌─────────────────────────────────────────┐
                    │ Slot 3: 背部發條鑰匙 (Wind-up Key)        │ (Z: 5, 渦輪火焰蝶形鑰匙)
                    └────────────────────┬────────────────────┘
                                         ▼
┌──────────────────────────┐   ┌───────────────────┐   ┌──────────────────────────┐
│ Slot 2: 頭部機關與耳朵造型   │──▶│                   │◀──│ Slot 5: 面部光學與表情核心   │
│ (Head Unit & Ear Mech)   │   │   底層素體外殼骨架   │   │ (Optic Core & Faceplate) │
│ (Z: 20, 散熱百葉耳/工字額板)│   │   (Chassis Base)  │   │ (Z: 30, 琥珀金透鏡/機械嘴角) │
└──────────────────────────┘   │   (Z: 10)         │   └──────────────────────────┘
┌──────────────────────────┐   │                   │   ┌──────────────────────────┐
│ Slot 1: 軀體外殼與塗裝     │──▶│ 2.3頭身球關節骨架 │◀──│ Slot 4: 玩具外裝與服飾   │
│ (Chassis & Paint Shell)  │   │                   │   │ (Costume & Toy Armor)    │
│ (Z: 10, 餘燼橙紅/碳黑條紋) │   └─────────┬─────────┘   │ (Z: 25, 淬火鍛鐵戰褂)    │
└──────────────────────────┘             │             └──────────────────────────┘
┌──────────────────────────┐             │             ┌──────────────────────────┐
│ Slot 6: 手持武器外觀       │─────────────┴─────────────│ Slot 7: 隨身奇玩與尾部機關   │
│ (Handheld Weapon Skin)   │                           │ (Back Curio & Tail Unit) │
│ (Z: 40, 齒輪發條雙斬刃)    │                           │ (Z: 8, 分節排氣管重力虎尾) │
└──────────────────────────┘                           └──────────────────────────┘
```

### 1.1 各槽位詳細切片需求明細表

| 槽位編號 | 槽位識別碼 (`slot_id`) | 中文名稱 | 英文名稱 | 渲染層級 (`z_index`) | 必備子組件清單 | 機械結構細節與 CANON 美學規範 | 建議初始款式與變體規劃 |
|:---:|:---|:---|:---|:---:|:---|:---|:---|
| **Slot 1** | `chassis` | **軀體外殼與塗裝** | Chassis & Paint Shell | `10` | • `torso_shell`（胸腹主底殼）<br>• `limb_ball_joints`（四肢黃銅球窩關節）<br>• `forearm_plates`（前臂散熱槽板件）<br>• `lower_leg_springs`（小腿重載阻尼）<br>• `footplates`（抓地防滑金屬足盤） | • **材質工藝**：餘燼橙紅拋光琺瑯（`#E65100`），外覆消光碳黑耐熱鋼板幾何嵌片。<br>• **關節規範**：外露式黃銅球窩旋轉關節（Ball-and-socket），帶平頭組裝螺栓刻線。<br>• **足部特徵**：底盤壓鑄耐磨防滑黑色合成橡膠墊，嚴禁生物肉墊。<br>• **禁令**：嚴禁任何生物肌理、有機皮膚、真毛皮或縫合怪縫線。 | • `paint_ember_orange`（原廠餘燼橙紅，Common）<br>• `paint_volcano_black`（鍛爐淬火曜黑，Rare）<br>• `paint_molten_gold`（熔金過載琉璃，Legendary） |
| **Slot 2** | `head_unit` | **頭部機關與耳朵造型** | Head Unit & Ear Mechanism | `20` | • `cranium_shell`（厚鋼頭殼）<br>• `louvered_ears`（雙側散熱百葉短耳）<br>• `forehead_reinforcement`（工字加固鋼板）<br>• `cheek_exhaust_flaps`（雙階排氣導風板） | • **額頭「王」字**：以縱橫交錯的高溫鍛鐵工字型加固壓條呈現，四角以 M2 平頭鉚釘牢固鉚接於頭骨，近看是純機械加固樑，遠看具備霸氣剪影。<br>• **雙耳造型**：外耳為弧形碳鋼沖壓厚板；內耳由 3~4 片傾斜金屬散熱百葉鰭片（Louvers）組成，外緣帶微型鉚釘。<br>• **雙頰輪廓**：左右兩側外展微型雙階排氣導風片，打破頭部純圓剪影，強化 30m 剪影辨識。 | • `head_ember_tiger_stock`（標準百葉耳與工字鋼樑額板，Common）<br>• `head_ember_mask_stealth`（暗夜行者排氣面罩，Rare） |
| **Slot 3** | `winding_key` | **背部發條鑰匙** | Wind-up Key | `5` | • `back_gear_socket`（背脊黃銅齒輪插座）<br>• `turbine_flame_key`（渦輪火焰齒輪雙翼鑰匙） | • **跨族相容**：上背正中插座孔徑 100% 符合全種族公規，向身後 3/4 側方伸出，主動破開外輪廓剪影。<br>• **造型細節**：旋鈕蝶翼外緣雕琢為渦輪鋸齒火焰弧線，呈現微型增壓閥質感。<br>• **動態演出**：待機時每 4.0 秒順時針平穩旋轉 1 圈；技能過載釋放時疾轉（0.5 秒/圈）並帶有些微金黃火花。 | • `key_turbine_flame`（渦輪火焰發條鑰匙，Common）<br>• 支援跨種族混搭：可無縫裝配白金兔古銅鑰匙或靈尾狐星芒鑰匙。 |
| **Slot 4** | `costume` | **玩具外裝與服飾** | Costume & Toy Armor | `25` | • `chest_armor`（淬火護胸鋼板）<br>• `artisan_tunic`（耐火工匠短褂）<br>• `brass_buckles`（雙聯大尺寸黃銅暗扣）<br>• `split_skirt`（短款開衩下擺） | • **初始款式**：**「餘燼工匠淬火戰褂（Ember Artisan Quenched Tunic）」**。<br>• **版型細節**：深褐耐火琺瑯薄鋼片層疊，邊緣帶暗金屬包邊；胸前配備兩枚大尺寸黃銅暗扣；短款開衩剪裁，完全不遮擋腿部球關節與尾部擺動。<br>• **背部開孔**：背脊預留標準發條鑰匙插座孔，100% 相容全種族外裝版型。 | • `costume_ember_tunic`（餘燼工匠淬火戰褂，Common）<br>• `costume_ash_ninja_garb`（灰燼夜行機關裝，Rare） |
| **Slot 5** | `optic_core` | **面部光學與表情核心** | Optic Core & Faceplate | `30` | • `gemstone_eyes`（琥珀金多面透鏡眼珠）<br>• `metal_nose`（拋光鍛黑三角合金小鼻）<br>• `mouth_groove`（ω 型自信微張機械嘴角槽）<br>• `chest_heart_gem`（胸口菱形發條之心晶石） | • **眼部光學**：晶瑩剔透的多面切割高光玻璃透鏡，帶有熔火琥珀金反光（#FFA010）。<br>• **口鼻分模**：鍛黑三角金屬小鼻；ω 形深邃機械分件嘴角刻線，散發敏捷自信微笑。<br>• **心臟共鳴**：胸口正中央嵌有菱形發條之心晶石，待機時呈現正弦波呼吸微光（週期 2.5 秒），受擊時轉暗紅頻閃。 | • `core_molten_amber`（原廠熔火琥珀核心，Common）<br>• `core_crimson_overdrive`（過載熾紅核心，Rare） |
| **Slot 6** | `weapon` | **手持武器外觀** | Handheld Weapon Skin | `40` | • `twin_sabers_main`（主手齒輪發條短刃）<br>• `twin_sabers_off`（副手反曲反手短刃）<br>• `gear_core_guard`（外露齒輪護手盤） | • **武器本體**：專利**「齒輪發條雙斬刃（Twin Ember Sabers）」**，完全收斂至 `weapon_classes.json` 之 `dagger`（忍者·匕）體系。<br>• **手持架勢**：主手刃長 68px 前傾微弧，副手刃長 68px 反手持握；刀背嵌外露微型黃銅齒輪與三道導熱槽。<br>• **可抽換性**：獨立武器道具層，絕不與手臂焊死；握持點統一對齊 (88, 76)。 | • `wpn_twin_ember_sabers`（齒輪發條雙斬刃，Common）<br>• `wpn_ash_kunai_pair`（灰燼機關苦無雙刃，Rare） |
| **Slot 7** | `back_curio` | **隨身奇玩與尾部機關** | Back Curio & Tail Unit | `8` | • `exhaust_tail_links`（4節漸縮金屬耐熱套管）<br>• `tail_ball_bearings`（節間球形軸承）<br>• `twin_tail_pipes`（尾梢雙孔微型排氣管嘴） | • **原生尾部**：**「分節排氣管重力虎尾（Articulated Exhaust Pipe Tail）」**。<br>• **結構尺度**：長度約為素體高度 65%，由 4 節漸縮形金屬套管與球形軸承相互咬合串接而成。<br>• **動態與特效**：尾梢為雙聯微縮排氣管嘴，待機自然 S 型延遲擺動，戰鬥蓄勁向上高揚，噴出極少量冷凝白氣與金黃微粒。 | • `curio_exhaust_tiger_tail`（分節排氣管重力虎尾，Common）<br>• 支援懸浮奇玩：身側左上方 (28, 40) 安全空間懸浮物相容。 |

---

## 二、 武器定案與體系收斂（Ninja Archetype & Weapon Canon）

### 2.1 嚴格對齊既有武器系統（禁止自創新武器類型）
在 `game/data/tables/weapon_classes.json` 中，遊戲嚴格鎖定 6 大職業、12 大武器系統：
```json
"professions": {
  "knight": ["sword", "spear"],
  "viking": ["axe", "hammer"],
  "ninja":  ["dagger", "dart"],
  "monk":   ["fist", "claw"],
  "mage":   ["magic", "crystal"],
  "ranger": ["bow", "gun"]
}
```

現有五族原生武器分佈：
- 白金兔：`knight`（`sword`，晨曦單手劍）
- 烈鬃獅：`knight`（`spear`，皇家長槍）
- 靈尾狐：`mage`（`magic`，星盤晶核法杖）
- 鋼牙豕：`viking`（`hammer`，鍛爐鐵砧戰鎚）
- 靈爪猴：`monk`（`claw`，機關彈簧靈爪）

**烈焰虎武器定案**：
- **正式職業定位**：**`ninja`（忍者）**。現有五族完全缺乏忍者職業之代表動物素體，烈焰虎補齊該光譜空缺。
- **武器唯一對齊**：完全對齊 `weapon_classes.json` 中 `ninja` 的核心主武器 **`dagger`（匕首 / 雙短刃）**，初始預設對應 `star_fang` 規格。
- **副武器/衍生配件**：若推出投擲暗器或奇玩變體，嚴格對齊 `ninja` 的次要武器 **`dart`（鏢 / 苦無）**，對應 `mist_darts` 規格。
- **比照白霧（Fog）忍者定調**：
  遊戲內既有 BOSS 白霧（`boss_fox.png` / `battle_ninja_village_1.png` / `fog_hide`）代表了正統機關忍者風格——身法靈動、煙幕冷卻、雙短刃急刺、投擲機關暗器。烈焰虎作為玩家端可操作的第六族素體，**完全承襲白霧忍者的戰鬥語彙，堅決不自創新武器類型（如：巨型手裏劍、鐮鎖、火砲、刺刀等均屬違規自創）**。

### 2.2 武器手感與戰鬥數值機制映射表

| 戰鬥機制關鍵項 | 烈焰虎雙短刃（Twin Ember Sabers）之具體反饋 | 數值體系與系統依據 (`weapon_classes.json`) |
|:---|:---|:---|
| **極限暴擊 (Critical Burst)** | 雙刃採用雙手弧形反曲短刃，刀脊內建微型發條齒輪與排氣閥，擊中瞬間發條瞬間釋能，打擊反饋清脆爆發。 | 完全對齊 `dagger` 之 `crit: 4.0`（全近戰武器最高基礎暴擊率），契合忍者（Ninja）伏擊撕裂定位。 |
| **高頻連段 (Multi-Hit)** | 左右雙刃交替突刺切割，揮舞間隔極短，迅速疊加打擊數（Combo）。 | 對齊 `dagger` 之 `speed: 2` 與怒氣（Rage）高頻累積速率。 |
| **部位破壞 (Part Break)** | 對應 `CANON.md` 第 219 行泰坦 BOSS 零件拆卸機制。高密度切割弱點散熱管線與鉚釘，快速觸發裝甲崩落。 | 契合弱點打擊（Weak Point Strike）邏輯，對輕裝甲與關節部位具備破勢加成。 |
| **防禦劣勢 (Glass Cannon)** | 身板較薄，強調以高速閃避與招架化解傷害。 | 對齊 `dagger` 之 `def: 0, hp: -4`，維持標準時間模型與風險收益平衡。 |

---

## 三、 六大戰鬥動作姿態需求清單（Combat Action Poses）

對照 `game/assets/sprites/player/poses/` 目錄規範，烈焰虎的六大戰鬥動作姿態（128×128 px RGBA）詳細美術需求如下：

| 動作代號 | 動作名稱 | 尺寸與畫布規範 | 幀數與架式意象 | 關鍵視覺焦點與機械回饋 |
|:---:|:---|:---:|:---|:---|
| **`idle`** | **戰鬥待機** | 128×128 px<br>雙足接地中心點 (64, 120) | **低伏備戰架式（Prowling Stance）**：<br>重心前傾微沉，雙膝彈簧微壓；右手刃平舉身前防禦，左手刃反握護於身側；尾部在身後呈 S 型自然波浪擺動；背部發條鑰匙勻速自轉。 | 身體帶有上下 2px 的正弦波呼吸起伏（Sine-wave Bounce），散發蓄勢待發的掠食者張力。 |
| **`telegraph`** | **出招蓄勁** | 128×128 px<br>雙足接地中心點 (64, 120) | **壓縮彈簧蓄能（Coil Compression）**：<br>雙腿關節劇烈向後壓縮蓄力，單爪抓地，身形幾乎貼地；雙刃向後收攏蓄勢；額頭散熱百葉亮起高溫金光；背部發條鑰匙超頻疾速飛轉。 | 極其明顯的前搖提示（Telegraph），讓玩家直觀預判即將發動極速猛撲。 |
| **`attack`** | **普攻出手** | 128×128 px<br>雙足接地中心點 (64, 120) | **交錯撕裂雙斬（Cross Ember Slash）**：<br>彈簧瞬間釋能前衝半步，右手刃由右上向左下斜劈，左手刃緊隨其後水平抹斬，在身前空氣中割出 **X 字型橙紅金屬刀痕**與金黃火花。 | 動作極度乾脆俐落（Snappy），收刀乾淨，展現高攻速高暴擊的忍者特質。 |
| **`skill`** | **怒氣大招** | 128×128 px<br>雙足接地中心點 (64, 120) | **猛虎裂空炎渦（Ember Cyclone Pounce）**：<br>雙腿彈簧過載彈射騰空，身軀在空中高速迴旋半圈，雙刃帶動齒輪噴出熾熱氣流，化作旋轉金屬利刃風暴向下怒砸斬擊；尾部排氣孔噴出濃烈白霧。 | 誇張的空中滯空感與地面震盪衝擊波，造成巨額暴擊傷害與裝甲削韌。 |
| **`hit`** | **受擊硬直** | 128×128 px<br>雙足接地中心點 (64, 120) | **雙刃交叉格擋後滑（Defensive Recoil）**：<br>身軀向後仰退，雙刃在胸前交叉抵擋衝擊；頭部微偏，雙耳百葉散熱片劇烈震顫；關節處冒出一縷白色洩壓蒸氣，足底擦出火花。 | 雖受擊但保持猛獸韌性，不顯脆弱崩壞感，符合頑強發條玩具設定。 |
| **`recover`** | **受擊復位** | 128×128 px<br>雙足接地中心點 (64, 120) | **翻滾緩衝單膝架刃（Spring Re-anchor）**：<br>單手與單刃撐地滑行止退，隨即翻轉雙刃，後腿阻尼彈簧復位彈起，重新切回 `idle` 低伏備戰姿態；發條齒輪發出清脆重啟聲。 | 展現無比靈活的機械身法，迅速重返戰鬥節奏。 |

---

## 四、 零毛皮材質與世界憲章（CANON.md）合規對照表

所有烈焰虎美術資產的提詞、生成與修整，必須 100% 恪守《世界憲章》（`docs/world/CANON.md`）第十章鐵律，禁止任何生物肉質與真毛皮：

| 檢查項目 | 傳統生物特徵（⛔ 100% 嚴禁） | 發條玩具機械化轉譯（✅ CANON 合規標準） | 材質與視覺呈現工藝 |
|:---|:---|:---|:---|
| **虎身表皮** | 任何動物毛皮、絨毛布料、柔軟肉質皮膚、肉粉色皮層。 | **高溫陽極氧化金屬板件（Anodized Metal Shell）**。 | 拋光亮面餘燼橙紅琺瑯（`#E65100`），表面具備微光烤漆質感，接縫處可見平頭金屬裝配螺栓。 |
| **虎紋斑紋** | 手繪生物黑色毛紋、雜亂斑點、寫實虎皮紋路。 | **消光碳黑耐熱鋼板嵌件（Matte Black Plate Inlays）** 與 **百葉散熱排氣狹縫（Thermal Vent Slits）**。 | 幾何沖壓凹槽高低差，背脊與肩部規則排列金屬板件接縫與陰影凹槽，自然形成剛硬機械虎斑。 |
| **額頭特徵** | 玄幻發光符咒、毛皮印記、寫實動物毛流「王」字。 | **工字型加固鋼樑結構（I-Beam Reinforcement Plate）**。 | 縱向鍛鐵加固壓條與三道橫向耐熱鋼樑交錯咬合，四角以微型平頭鉚釘牢牢鎖定於頭蓋骨上。 |
| **耳朵構造** | 柔軟肉質毛耳、內部粉嫩耳肉、絨毛邊緣。 | **散熱百葉金屬弧耳（Louvered Heat-Sink Ears）**。 | 外耳為厚鍛黑鋼板沖壓成型，弧度俐落；內耳為 3~4 層向下傾斜的金屬散熱百葉鰭片，邊緣帶鉚釘。 |
| **足爪掌底** | 貓科動物粉紅肉墊、生物指甲、尖銳骨爪。 | **壓鑄耐磨防滑橡膠底盤（Die-cast Rubber Grip Plates）**。 | 深黑合成橡膠耐磨防滑襯塊，抓地力強；金屬嵌合腳趾無任何生物肉感。 |
| **尾部機關** | 柔軟毛茸茸肉尾、生物骨骼關節。 | **分節排氣管重力虎尾（Articulated Exhaust Pipe Tail）**。 | 4 節漸縮形金屬耐熱套管與球形接頭串接，尾梢為雙聯微縮排氣管嘴，散發微量白色冷凝蒸氣。 |
| **面部表情** | 嗜血獠牙、血盆大口、粉嫩舌頭、兇殘魔物表情。 | **ω 型機械嘴角槽線與多面透鏡眼珠**。 | 晶瑩發光琥珀金玻璃透鏡（`#FFA010`）；自信微笑的微張機械凹槽分模線；純金屬三角小鼻。 |
| **動力象徵** | 生物心臟、魔法光環、無源超自然浮游物。 | **背部黃銅發條插座與渦輪火焰鑰匙（Wind-up Key）**。 | 上背部正中標準黃銅插座，插入帶有火焰鋸齒輪廓的旋鈕鑰匙，持續提供走時機械動能。 |
| **受擊表現** | 流血、骨折、肉質飛濺、斷肢殘破感。 | **高壓蒸氣洩壓、火花四濺、螺栓零件震顫鬆脫**。 | 受擊時噴出白色洩壓蒸氣，符合全年齡溫暖玩具世界觀（Kinetic Disassembly）。 |

---

## 五、 完整資產命名規範與目錄清冊（比照五族目錄格式）

比照 `docs/design/PAPERDOLL_SLOTS_SPEC.md` 第 2.2 與 2.3 節五族既有結構，烈焰虎（`tiger`）待產出之完整資產清冊與路徑鏡像對齊表如下：

### 5.1 品牌、展示與立繪標準命名表

| 用途 / 類別 | 白金兔既有資產結構 (`char_rabbit`) | 烈焰虎鏡像資產結構 (`char_tiger`) | 尺寸與格式 | 資源狀態 (Status) |
|:---|:---|:---|:---:|:---:|
| **高解析概念原畫** | `docs/art/whitey_r3_concept.png` | `docs/art/ember_tiger_concept.png` | 928×1152 RGBA | ⏳ 待產出 (Pending) |
| **立繪展台標準候選圖** | `docs/art/char_rabbit_candidate_400x840.png` | `docs/art/char_tiger_candidate_400x840.png` | 400×840 RGBA | ⏳ 待產出 (Pending) |
| **正式品牌全尺寸立牌** | `branding/char_rabbit.png` | `branding/char_tiger.png` | 400×840 RGBA | ⏳ 待產出 (Pending) |
| **官網英雄展示圖** | `web/media/hero/char_rabbit.png` | `web/media/hero/char_tiger.png` | 400×840 RGBA | ⏳ 待產出 (Pending) |
| **官網動態預覽圖** | `web/media/hero/rabbit_idle.png` | `web/media/hero/tiger_idle.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |

### 5.2 遊戲內 2D Sprite 與戰鬥姿態鏡像表

| 用途 / 類別 | 白金兔既有資產結構 (`rabbit`) | 烈焰虎鏡像資產結構 (`tiger`) | 尺寸與格式 | 資源狀態 (Status) |
|:---|:---|:---|:---:|:---:|
| **基礎待機幀 (1x)** | `game/assets/sprites/player/rabbit_idle.png` | `game/assets/sprites/player/tiger_idle.png` | 64×64 RGBA | ⏳ 待產出 (Pending) |
| **高畫質待機幀 (3x)** | `game/assets/sprites/player/rabbit_idle_x3.png` | `game/assets/sprites/player/tiger_idle_x3.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |
| **大廳/隊伍展示幀** | `game/assets/sprites/player/party/rabbit_idle.png` | `game/assets/sprites/player/party/tiger_idle.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |
| **戰鬥特寫姿態** | `game/assets/sprites/player/rabbit_battle.png` | `game/assets/sprites/player/tiger_battle.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |
| **行走動畫 (0~3 幀, 1x)** | `game/assets/sprites/player/rabbit_walk_{0..3}.png` | `game/assets/sprites/player/tiger_walk_{0..3}.png` | 64×64 RGBA | ⏳ 待產出 (Pending) |
| **行走動畫 (0~3 幀, 3x)** | `game/assets/sprites/player/rabbit_walk_{0..3}_x3.png` | `game/assets/sprites/player/tiger_walk_{0..3}_x3.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |
| **戰鬥姿態：待機** | `game/assets/sprites/player/poses/rabbit/idle.png` | `game/assets/sprites/player/poses/tiger/idle.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **戰鬥姿態：前搖** | `game/assets/sprites/player/poses/rabbit/telegraph.png` | `game/assets/sprites/player/poses/tiger/telegraph.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **戰鬥姿態：普攻** | `game/assets/sprites/player/poses/rabbit/attack.png` | `game/assets/sprites/player/poses/tiger/attack.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **戰鬥姿態：大招** | `game/assets/sprites/player/poses/rabbit/skill.png` | `game/assets/sprites/player/poses/tiger/skill.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **戰鬥姿態：受擊** | `game/assets/sprites/player/poses/rabbit/hit.png` | `game/assets/sprites/player/poses/tiger/hit.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **戰鬥姿態：復位** | `game/assets/sprites/player/poses/rabbit/recover.png` | `game/assets/sprites/player/poses/tiger/recover.png` | 128×128 RGBA | ✅ 已產出 (Ready) |
| **HUD 戰鬥頭像** | `game/assets/sprites/portraits/rabbit.png` | `game/assets/sprites/portraits/tiger.png` | 128×128 RGBA | ⏳ 待產出 (Pending) |
| **對話框半身像** | `game/assets/sprites/portraits/rabbit.png` | `game/assets/sprites/portraits/ember_tiger.png` | 384×480 RGBA | ⏳ 待產出 (Pending) |

### 5.3 紙娃娃模組化切片圖層清冊（Layered Paperdoll Slices）

所有切片畫布尺寸統一為 **128×128 px 透明 RGBA**，原點 (0, 0) 對齊雙足落地點 (64, 120)：

| 槽位 ID (`slot_id`) | 渲染層級 (`z_index`) | 目標檔案路徑 (`game/assets/sprites/player/paperdoll/...`) | 說明與圖層內容 | 資源狀態 (Status) |
|:---|:---:|:---|:---|:---:|
| `chassis` | `10` | `tiger/chassis/paint_ember_orange.png` | 餘燼橙紅拋光琺瑯底殼素體、黃銅球關節、橡膠足盤 | ⏳ 待產出 (Pending) |
| `head_unit` | `20` | `tiger/head_unit/head_ember_tiger_stock.png` | 鍛黑厚鋼頭殼、散熱百葉短耳、額頭工字加固樑 | ⏳ 待產出 (Pending) |
| `winding_key` | `5` | `key/key_turbine_flame.png` | 跨種族通用渦輪火焰齒輪雙翼發條鑰匙 | ⏳ 待產出 (Pending) |
| `costume` | `25` | `tiger/costume/costume_ember_tunic.png` | 餘燼工匠淬火戰褂，開衩短版耐火鋼片甲 | ⏳ 待產出 (Pending) |
| `optic_core` | `30` | `tiger/optic_core/core_molten_amber.png` | 琥珀金多面晶石眼珠、鍛黑三角鼻、發條之心晶石 | ⏳ 待產出 (Pending) |
| `weapon` | `40` | `weapon/wpn_twin_ember_sabers.png` | 獨立武器層：齒輪發條雙斬刃（左右雙持短刃） | ⏳ 待產出 (Pending) |
| `back_curio` | `8` | `tiger/back_curio/curio_exhaust_tiger_tail.png` | 4 節漸縮形金屬分節套管排氣管重力虎尾 | ⏳ 待產出 (Pending) |

---

## 六、 下游流水線交接與產圖自檢指引（Pipeline Handoff & Quality Gates）

### 6.1 美術總監（小柔 sideart）執行自檢清單（產圖驗收標準）
在實際使用生圖工具產圖或進行分層切片時，小柔需對照以下項目逐一打勾驗收：
- [ ] **比例檢驗**：標準 2.2~2.4 頭身 Chibi，大頭圓潤、四肢粗短有力，嚴禁寫實人體比例。
- [ ] **CANON 零毛皮檢驗**：100% 無真毛皮、無羽毛、無有機肌膚。虎斑全為幾何鋼板沖壓嵌件與百葉散熱狹縫。
- [ ] **額頭鋼樑檢驗**：額頭「王」字是由縱橫交錯的加固工字型鍛鐵壓條與螺栓固定，嚴禁畫成毛紋或玄幻符咒。
- [ ] **雙耳結構檢驗**：內耳具備傾斜金屬散熱百葉鰭片，外緣有組裝平頭鉚釘。
- [ ] **尾部機械檢驗**：尾巴由 4 節漸縮金屬耐熱套管與球形接頭串接，尾尖為雙聯排氣孔。
- [ ] **發條鑰匙檢驗**：背後正中插有渦輪火焰發條鑰匙，破開側身外剪影。
- [ ] **武器規範檢驗**：手持雙短刃（反曲弧刀、刀脊微齒輪），嚴禁自創非規長柄武器或長槍法杖。
- [ ] **色盤檢驗**：主色餘燼橙紅（#E65100）、碳黑鋼板（#2B2B36）、金光核心（#FFA010）、深藍紫描邊（#1F1A3A），無髒泥土灰黑。

### 6.2 側案程式（阿宏 sideworker）資料庫注入與目錄準備
- [ ] 將 `docs/design/EMBER_TIGER_DESIGN_PROPOSAL.md` 第六節之 JSON 規格，更新合併至 `game/data/tables/paperdoll_slots.json` 與 `docs/design/paperdoll_slots.json`。
- [ ] 建立遊戲內紙娃娃空目錄結構：`game/assets/sprites/player/paperdoll/tiger/{chassis,head_unit,costume,optic_core,back_curio}` 以及 `poses/tiger/`。

### 6.3 側案測試（小婷 sideqa）冒煙檢驗重點
- [ ] 當紙娃娃系統載入 `tiger` 種族設定時，驗證槽位合成管線無缺失 Key、無空指針崩潰。
- [ ] 驗證武器槽位載入 `wpn_twin_ember_sabers` 時，底層 weapon class 正確識別為 `dagger`，暴擊與攻速加成計算正確。

---

## 七、 結語

本需求清單全面落實 `t_828248d3` 之任務目標：
1. 完整盤點並定義 7 大部件槽位之機械化組件需求；
2. 武器定案嚴格收斂至忍者（雙短刃 / 苦無），比照白霧定調，零自創新武器；
3. 規範六大戰鬥姿態意象與 128×128 畫布標準；
4. 條目式落實 CANON 零毛皮鐵律；
5. 全文嚴格遵循五族既有目錄格式與鏡像檔案命名。

文件已就緒，提請側案製作人老周（side）與美術總監小柔（sideart）審閱！
