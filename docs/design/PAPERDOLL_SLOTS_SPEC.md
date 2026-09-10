# 《發條之心》紙娃娃系統：7 大部件槽位與 5 大動物素體規格書

> **文件狀態**：核心系統規格定稿（System & Asset Specification - Ready for Review）  
> **制定日期**：2026-09-09  
> **負責人**：策劃總監 小凱（sideplan）  
> **對應看板任務**：`t_2f3d31f3`（🎮 遊戲開發｜紙娃娃系統：設計 paperdoll_slots.json 部位槽規格）  
> **對應機器讀取設定檔**：`docs/design/paperdoll_slots.json`  
> **依據與對齊文件**：`docs/PAPERDOLL_SYSTEM_PROPOSAL.md`（第 3 節）、`docs/art/SPRING_MACAQUE_DESIGN_PROPOSAL.md`（commit ecfd4aa / t_1d201223）、`docs/art/WHITEY_REDESIGN_PROPOSAL.md`、`docs/world/CANON.md`、`docs/ART_DIRECTION.md` v2、`docs/BUSINESS.md`  

---

## 0. 邊界與護欄宣告（Scope & Guardrails）

1. **⛔ 明確排除、不越權決定（Stuck at t_f0737f11）**：
   - **四英雄是否升格為可自訂素體**：本單不拍板、不替換現有四英雄固定角色邏輯，這項決策仍卡在 `t_f0737f11` 等候 Kevin 最終裁示。
   - **社交系統做到哪一層（P0/P1/P2）**：非即時同屏遊客、互讚、公會等功能範圍與時程同樣待 `t_f0737f11` 裁示。
   - **本單職責**：專注產出**技術與美術可獨立推進的槽位規格、素體尺寸、貼圖命名規範與資產分層架構**。
2. **世界憲章鐵則**：
   - 100% 零毛皮、全金屬/琺瑯組裝玩具。嚴禁任何生物肉質膚色、毛皮紋理、恐怖谷縫合線與暗黑廢土鏽蝕。
3. **商業變現鐵則**：
   - 絕對零數值壓迫（Zero Pay-to-Win）。所有紙娃娃槽位 100% 不增加任何攻擊、生命、防禦等數值。

---

## 1. 7 大模組化機械部件槽位定義（Slot Architecture）

依據 `docs/PAPERDOLL_SYSTEM_PROPOSAL.md` 第 3.1 節，規劃 7 大外觀槽位。在 Godot 2D 渲染管線中採用 Multi-pass 分層貼圖合成（Layered Sprite），各槽位定義與渲染順序（Z-Index）如下：

```
                    ┌─────────────────────────────────────────┐
                    │ Slot 3: 背部發條鑰匙 (Wind-up Key)        │ (Z: 5, 破剪影動態符號)
                    └────────────────────┬────────────────────┘
                                         ▼
┌──────────────────────────┐   ┌───────────────────┐   ┌──────────────────────────┐
│ Slot 2: 頭部機關與耳朵造型   │──▶│                   │◀──│ Slot 5: 面部光學與表情核心   │
│ (Head Unit & Ear Mech)   │   │   底層素體外殼骨架   │   │ (Optic Core & Faceplate) │
│ (Z: 20)                  │   │   (Chassis Base)  │   │ (Z: 30)                  │
└──────────────────────────┘   │   (Z: 10)         │   └──────────────────────────┘
┌──────────────────────────┐   │                   │   ┌──────────────────────────┐
│ Slot 1: 軀體外殼與塗裝     │──▶│ 2.3頭身球關節骨架 │◀──│ Slot 4: 玩具外裝與服飾   │
│ (Chassis & Paint Shell)  │   │                   │   │ (Costume & Toy Armor)    │
│ (Z: 10)                  │   └─────────┬─────────┘   │ (Z: 25)                  │
└──────────────────────────┘             │             └──────────────────────────┘
┌──────────────────────────┐             │             ┌──────────────────────────┐
│ Slot 6: 手持武器外觀       │─────────────┴─────────────│ Slot 7: 隨身奇玩與尾部機關   │
│ (Handheld Weapon Skin)   │                           │ (Back Curio & Tail Unit) │
│ (Z: 40)                  │                           │ (Z: 8)                   │
└──────────────────────────┘                           └──────────────────────────┘
```

### 槽位詳細規格表

| 槽位編號 | 識別碼 (`slot_id`) | 中文名稱 | 英文名稱 | 渲染層級 (`z_index`) | 涵蓋部位與子組件 | 機械細節與美學憲章 | 經典範例款式 |
|:---:|:---|:---|:---|:---:|:---|:---|:---|
| **Slot 1** | `chassis` | **軀體外殼與塗裝** | Chassis & Paint Shell | `10` | 軀幹底殼、四肢球形關節、小臂骨架、後腿彈簧、腳掌底盤 | 拋光金屬板件、高光琺瑯陶瓷烤漆、平頭螺栓與裝配刻線；零毛皮、無縫合線。 | 原廠象牙白、胡桃鉗皇家朱紅、午夜深藍、黃銅原金、赤焰熔爐烤漆、翡翠螢光釉面、天元青古銅烤漆 |
| **Slot 2** | `head_unit` | **頭部機關與耳朵造型** | Head Unit & Ear Mechanism | `20` | 頭蓋骨金屬殼、左右機械雙耳、額頭散熱導流板件 | 內耳必須有垂直分模刻線與琺瑯鏡面反射；額板單片平頭螺栓固定（不成環、非金箍）；30m 剪影極度分明。 | 雙聯長立金屬耳（兔）、雷達天線耳（狐）、外擴金屬鬃毛冠（獅）、鋼板罩耳（豬）、同心圓耳罩（猴） |
| **Slot 3** | `winding_key` | **背部發條鑰匙** | Wind-up Key | `5` | 背脊正中齒輪插座、蝶翼旋鈕 / 齒輪鑰匙主體 | 【全遊戲靈魂焦點】上背插座固定，向側後方伸出並破外剪影；待機自轉（4秒/圈），技能過載疾轉伴隨微量蒸氣火花。 | 雙孔古銅鑰匙、八音盒T型蝶翼發條、星芒齒輪旋鈕、皇家十字冠冕發條、展翼天使雙發條 |
| **Slot 4** | `costume` | **玩具外裝與服飾** | Costume & Toy Armor | `25` | 胸腹短褂/胸甲、肩甲/領巾、腰帶、裙甲/短褲 | 微縮玩偶舞台服裝質感，顯眼粗縫線、黃銅暗扣；嚴禁現代寫實長袍；統一 Chibi 軀幹胸腰版型。 | 胡桃鉗近衛軍裝、蒸氣工匠吊帶工作裝、晨曦行者武道短褂、星紋占星斗篷、星象觀測者金屬儀裝、粗獷鍛爐護胸鐵束帶、維京重裝鍛鐵板甲、皇家巡遊金屬禮服、天元演武者機關甲 |
| **Slot 5** | `optic_core` | **面部光學與表情核心** | Optic Core & Faceplate | `30` | 雙眼寶石透鏡、上漆金屬倒三角小鼻、深邃機械嘴角槽、胸口發條心晶石 | 晶瑩發光玻璃透鏡（天藍/翡翠綠/琥珀金）；倒三角純金屬鼻；ω形深邃機械分件凹線；胸口正中心臟晶石同步呼吸閃爍。 | 天青翡翠核心、琥珀烈陽核心、星海紫晶核心、飛行員護目鏡光學面板 |
| **Slot 6** | `weapon` | **手持武器外觀** | Handheld Weapon Skin | `40` | 主手武器持握部、刃/槍頭/杖端、副手爪套/盾牌 | 獨立道具層，絕不與手臂焊死；玩具比例偏大，具厚實玩具質感與發條齒輪機關；支援 12 大武器體系。 | 晨曦發條單手長劍、機關發條靈爪護手、皇家黃銅突刺長槍、星盤晶核法杖、鍛爐鐵砧重型戰鎚 |
| **Slot 7** | `back_curio` | **隨身奇玩與尾部機關** | Back Curio & Tail Balance Unit | `8` | 金屬連桿長尾、螺旋彈簧避震尾、身側懸浮微縮奇玩 | 多節金屬避震機械長尾；或懸浮於身側左上方 (28, 40) 的發條寵物奇玩，自帶微幅呼吸浮動動態。 | 伸縮彈簧機關平衡長尾（猴）、多節星軸導能尾（狐）、黃銅多節連桿扇尾（獅）、自走發條小信鴿、迷你雙聯排氣管、懸浮八音盒 |

---

## 2. 初始 5 大動物族系素體規格與命名規範

Kevin 於 2026-09-09 正式拍板首發 5 大動物族系為：**兔、狐、獅、豬、猴**。其中第 5 種「靈爪猴（Spring Macaque）」補位東方武道機關特色。

### 2.1 五大族系基礎規格對照表

| 種族識別碼 (`race_id`) | 種族中文 | 種族英文 | 職業風格標籤 | 靈源界域 | 頭身比 (Chibi) | 核心外觀特徵 | 主色調與材質 |
|:---|:---|:---|:---|:---|:---:|:---|:---|
| `rabbit` | **白金兔** | Clockwork Rabbit | 劍士 (Knight) | R01 今日村莊·發條新村 / Today Village: Cogwheel Hamlet | 2.3 ~ 2.5 | 雙聯長立金屬耳、珊瑚粉金屬內耳、倒三角小金屬鼻、胸口青藍心形核心、單手長劍 | 象牙白 (#FFFDF8) 琺瑯、黃銅金 (#FFD028)、天藍光 (#38A0FF) |
| `lion` | **烈鬃獅** | Gilded Lion | 騎士 (Knight) | R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City | 2.2 ~ 2.4 | 外擴金屬疊片鬃毛冠、剛毅厚重黃銅胸甲、鉸鏈粗壯四肢、長多節黃銅連桿尾（尾端為可展開扇形金屬扇片）、皇家長槍 | 拋光黃銅 (#E5A93C)、近衛朱紅 (#B84A39)、琥珀金 (#FFA010) |
| `fox` | **靈尾狐** | Astral Fox | 法師 (Mage) | R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest | 2.3 ~ 2.5 | 尖聳雷達天線耳、三至五節懸浮連桿星軸長尾、流線型輕金屬殼、星盤晶核秘術法杖 | 暖橘烤漆 (#E87A38)、深紫藍 (#4A3B7A)、紫晶光 (#A855F7) |
| `boar` | **鋼牙豕** | Forge Boar | 戰士 (Viking) | R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano | 2.1 ~ 2.3 | 衝壓鋼板野豬鼻、雙根外露鎢鋼長獠牙、鉚接加厚肩甲、粗螺旋金屬彈簧短尾、鍛爐鐵砧重型戰鎚 | 黑鐵合金 (#474D58)、鍛爐烈火 (#D9532F)、鎢鋼銀 (#C0C5CE) |
| `macaque` *(alias: `monkey`)* | **靈爪猴** | Spring Macaque | 武術家 (Monk) | R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo | 2.2 ~ 2.4 | 雙小臂螺旋黃銅彈簧避震套管、單片長方形額前導流板、伸縮平衡長尾、機關靈爪護手 | 香檳金/淺褐 (#E8C88A)、黃銅金 (#FFD028)、翡翠綠 (#4ED86A) |

---

### 2.2 靈爪猴（Spring Macaque）對齊規範

依據交辦需求，第 5 種動物靈爪猴之命名與檔案結構**徹底對齊 `docs/art/char_` 慣例與 `char_rabbit` 現有結構**：

#### (1) 品牌與立繪標準命名
- **高解析概念原畫**：`docs/art/spring_macaque_concept.png`（928×1152，4:5 縱向）
- **立繪展台標準候選圖**：`docs/art/char_macaque_candidate_400x840.png`（400×840）
- **正式品牌全尺寸立牌**：`branding/char_macaque.png`（400×840，對齊 `branding/char_rabbit.png`）
- **官網英雄展示圖**：`web/media/hero/char_macaque.png`（400×840）
- **官網動態預覽圖**：`web/media/hero/macaque_idle.png`（128×128）

#### (2) 遊戲內 `game/assets/sprites/player/` 完整檔案鏡像對齊表

| 用途 / 類別 | 白金兔既有檔案結構 (`char_rabbit`) | 靈爪猴對齊檔案結構 (`char_macaque`) | 尺寸與格式 | 資源狀態 (Status) |
|:---|:---|:---|:---:|:---|
| **基礎待機幀 (1x)** | `game/assets/sprites/player/rabbit_idle.png` | `game/assets/sprites/player/macaque_idle.png` | 64×64 RGBA | 兔既有 / 猴既有 |
| **高畫質待機幀 (3x)** | `game/assets/sprites/player/rabbit_idle_x3.png` | `game/assets/sprites/player/macaque_idle_x3.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **大廳/隊伍展示幀** | `game/assets/sprites/player/rabbit_idle_x3.png` | `game/assets/sprites/player/party/macaque_idle.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **戰鬥特寫姿態** | `game/assets/sprites/player/rabbit_battle.png` | `game/assets/sprites/player/macaque_battle.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **行走動畫 (0~3 幀, 1x)** | `game/assets/sprites/player/rabbit_walk_{0..3}.png` | `game/assets/sprites/player/macaque_walk_{0..3}.png` | 64×64 RGBA | 兔既有 / 猴既有 |
| **行走動畫 (0~3 幀, 3x)** | `game/assets/sprites/player/rabbit_walk_{0..3}_x3.png` | `game/assets/sprites/player/macaque_walk_{0..3}_x3.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **戰鬥 6 大動作姿態** | `game/assets/sprites/player/poses/{attack,hit,idle,recover,skill,telegraph}.png` | `game/assets/sprites/player/poses/macaque/{attack,hit,idle,recover,skill,telegraph}.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **HUD 戰鬥頭像** | `game/assets/sprites/portraits/rabbit.png` | `game/assets/sprites/portraits/macaque.png` | 128×128 RGBA | 兔既有 / 猴既有 |
| **對話框半身像** | `game/assets/sprites/portraits/rabbit.png` | `game/assets/sprites/portraits/spring_macaque.png` | 384×480 RGBA | 兔既有 / 猴既有 |
| **紙娃娃切片目錄** | `game/assets/sprites/player/paperdoll/rabbit/{slot}/{id}.png` | `game/assets/sprites/player/paperdoll/macaque/{slot}/{id}.png` | 128×128 RGBA | 兔既有 / 猴既有 |

---

### 2.3 五大族系資產清冊與實體產出狀態表 (Asset Status & Inventory)

為防止下一棒工程師或美術執行時 `ls` 檔案撲空，特別註明各族系目前實際硬碟實體路徑與產出狀態：

| 種族代號 (`race_id`) | 既有現存實體檔案 (Existing Assets) | 前瞻待產出檔案 (Pending Assets) | 實體檔案目錄說明與備註 |
|:---|:---|:---|:---|
| `rabbit` (白金兔) | • `branding/char_rabbit.png` (400×840 立牌)<br>• `docs/art/char_rabbit_candidate_400x840.png`<br>• `web/media/hero/char_rabbit.png` (400×840 官網英雄圖)<br>• `web/media/hero/rabbit_idle.png` (128×128 官網預覽圖)<br>• `game/assets/sprites/player/rabbit_idle.png` (64×64)<br>• `game/assets/sprites/player/rabbit_idle_x3.png` (128×128)<br>• `game/assets/sprites/player/rabbit_battle.png` (128×128)<br>• `game/assets/sprites/player/rabbit_walk_{0..3}.png` (64×64)<br>• `game/assets/sprites/player/rabbit_walk_{0..3}_x3.png` (128×128)<br>• `game/assets/sprites/player/poses/` (6大戰鬥動作幀)<br>• `game/assets/sprites/portraits/rabbit.png` (128×128)<br>• `game/assets/sprites/player/paperdoll/rabbit/` (7大部件切片) | | 基準核心素體，遊戲內基礎與戰鬥資產齊全；紙娃娃系統切片為本期設計規格。 |
| `lion` (烈鬃獅) | • `branding/char_lion.png` (400×840 立牌)<br>• `web/media/hero/char_lion.png` (400×840 官網英雄圖)<br>• `web/media/hero/lion_idle.png` (128×128 官網預覽圖)<br>• `game/assets/sprites/player/party/lion_idle.png` (128×128)<br>• `game/assets/sprites/player/lion_battle.png` (128×128)<br>• `game/assets/sprites/player/lion_walk_{0..3}.png` (64×64)<br>• `game/assets/sprites/player/lion_walk_{0..3}_x3.png` (128×128)<br>• `game/assets/sprites/portraits/lion.png` (128×128 HUD)<br>• `game/assets/sprites/portraits/lion_knight.png` (對話框頭像)<br>• `game/assets/sprites/player/paperdoll/lion/` (7大部件切片) | • `game/assets/sprites/player/lion_idle.png` (64×64)<br>• `game/assets/sprites/player/poses/lion/` | 官網英雄預覽、隊伍展示幀、戰鬥特寫姿態、行走動畫與 HUD 戰鬥頭像已全數產出齊全。 |
| `fox` (靈尾狐) | • `branding/char_fox.png` (400×840 立牌)<br>• `web/media/hero/char_fox.png` (400×840 官網英雄圖)<br>• `web/media/hero/fox_idle.png` (128×128 官網預覽圖)<br>• `game/assets/sprites/player/party/fox_idle.png` (128×128)<br>• `game/assets/sprites/player/fox_battle.png` (128×128 戰鬥特寫姿態)<br>• `game/assets/sprites/player/fox_walk_{0..3}.png` (64×64)<br>• `game/assets/sprites/player/fox_walk_{0..3}_x3.png` (128×128)<br>• `game/assets/sprites/player/poses/fox/` (6大戰鬥動作姿態目錄)<br>• `game/assets/sprites/portraits/fox.png` (128×128 HUD)<br>• `game/assets/sprites/portraits/fox_mage.png` (對話框頭像)<br>• `game/assets/sprites/player/paperdoll/fox/` (7大部件切片) | • `game/assets/sprites/player/fox_idle.png` (64×64) | 隊伍展示待機幀、戰鬥特寫、6大動作姿態目錄與紙娃娃切片已全數產出齊全。 |
| `boar` (鋼牙豕) | • `branding/char_boar.png` (400×840 立牌)<br>• `web/media/hero/char_boar.png` (400×840 官網英雄圖)<br>• `web/media/hero/boar_idle.png` (128×128 官網預覽圖)<br>• `game/assets/sprites/player/party/boar_idle.png` (128×128)<br>• `game/assets/sprites/player/boar_battle.png` (128×128)<br>• `game/assets/sprites/player/boar_walk_{0..3}.png` (64×64)<br>• `game/assets/sprites/player/boar_walk_{0..3}_x3.png` (128×128)<br>• `game/assets/sprites/portraits/boar.png` (128×128 HUD)<br>• `game/assets/sprites/portraits/boar_warrior.png` (對話框頭像)<br>• `game/assets/sprites/player/paperdoll/boar/` (7大部件切片) | • `game/assets/sprites/player/boar_idle.png` (64×64)<br>• `game/assets/sprites/player/poses/boar/` | 官網英雄預覽、隊伍展示幀、戰鬥特寫姿態、行走動畫與 HUD 戰鬥頭像已全數產出齊全。 |
| `macaque` (靈爪猴) | • `docs/art/spring_macaque_concept.png` (928×1152 原畫)<br>• `docs/art/spring_macaque_thumb_128px.png` (驗證縮圖)<br>• `docs/art/spring_macaque_crop_*.png` (部位驗證切片)<br>• `branding/char_macaque.png` (400×840 立牌)<br>• `docs/art/char_macaque_candidate_400x840.png`<br>• `web/media/hero/char_macaque.png` (400×840 官網英雄圖)<br>• `web/media/hero/macaque_idle.png` (128×128 官網預覽圖)<br>• `game/assets/sprites/player/macaque_idle.png` (64×64)<br>• `game/assets/sprites/player/macaque_idle_x3.png` (128×128)<br>• `game/assets/sprites/player/party/macaque_idle.png` (128×128)<br>• `game/assets/sprites/player/macaque_battle.png` (128×128)<br>• `game/assets/sprites/player/macaque_walk_{0..3}.png` (64×64)<br>• `game/assets/sprites/player/macaque_walk_{0..3}_x3.png` (128×128)<br>• `game/assets/sprites/player/poses/macaque/` (6大戰鬥動作姿態目錄)<br>• `game/assets/sprites/portraits/macaque.png` (128×128 HUD)<br>• `game/assets/sprites/portraits/spring_macaque.png` (384×480 對話框半身像)<br>• `game/assets/sprites/player/paperdoll/macaque/` (7大部件切片＋第二套外裝天元演武者機關甲與第二套塗裝天元青古銅) | | 概念定稿（t_1d201223）已通過；全套立繪、官網與遊戲內 2D 資產（t_6e267e1b）已依 paperdoll_slots 規格產出齊全；第二套外裝與塗裝變體（t_0fca8056）已補齊。 |

---

## 3. 部件替換美術輸出尺寸標準（Art Output Standards）

### 3.1 三級尺寸階梯規範

```
【第一級：展示立牌與大廳立繪 (Standee)】
  └─ 尺寸：400 × 840 px (RGBA 透明 PNG)
  └─ 用途：創角選人介面、角色詳情面板、大廳特寫、官網展示
  └─ 錨點：(200, 800) px（雙足接地接觸點）
  └─ 頭頂位置：約 y = 200 px；頭部直徑約 260 px；維持 2.3~2.5 頭身

【第二級：遊戲內 2D 紙娃娃貼圖層 (In-Game Modular Layers)】
  └─ 尺寸：128 × 128 px (RGBA 透明 PNG)（相容 1x 降採樣 64 × 64 px）
  └─ 用途：大廳走動、大地圖探索、戰鬥姿態渲染
  └─ 錨點：(64, 120) px（雙足接觸中心點）
  └─ 合成方式：全槽位貼圖共用 (0, 0) 畫布原點直接疊合，零即時座標計算開銷

【第三級：頭像與隊列圖示 (Portraits & Icons)】
  └─ 對話框立繪：384 × 480 px
  └─ 好友名片 / 戳碰特寫：256 × 256 px
  └─ HUD / 戰鬥行動順序頭像：128 × 128 px
```

### 3.2 跨種族互換相容性（Interchangeability Rules）

1. **100% 跨種族通用槽位**：
   - **`winding_key`（發條鑰匙）**：上背齒輪插座位置與孔徑在五大素體上高度公規化，任意抽取的發條鑰匙均可無縫裝配於兔/狐/獅/豬/猴。
   - **`weapon`（手持武器）**：右手握持點統一對齊 (88, 76)，雙手爪套自適應對稱。
   - **`back_curio`（懸浮奇玩）**：浮空微縮玩具共用身側左上方 (28, 40) 安全空間，絕不遮擋頭部耳朵或手持武器。
2. **種族專屬適配槽位**：
   - **`head_unit`（頭部機關）**：各族原生耳部剪影極度強烈（兔長耳、狐尖耳、獅鬃毛、猴圓耳罩）。未來若推出通用頭飾（如飛行員護目鏡、近衛軍大蓋帽），美術需依據五族耳部開孔預留對應透明通道。
   - **`costume`（服飾外裝）**：五大種族軀幹均維持 2.2~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬) 由渲染器微調縮放 1.05x。

---

## 4. 目錄結構與落實清單（Asset Blueprint）

```
bravesoul-game/
├── docs/
│   └── design/
│       ├── paperdoll_slots.json          # 機器讀取核心設定規格檔 (本單核心交付)
│       └── PAPERDOLL_SLOTS_SPEC.md       # 本規格說明文件
├── branding/
│   ├── char_rabbit.png                   # 400x840 基準白兔立牌
│   ├── char_lion.png                     # 400x840 (由928x1152標準化)
│   ├── char_fox.png                      # 400x840 (由928x1152標準化)
│   ├── char_boar.png                     # 400x840 (由928x1152標準化)
│   └── char_macaque.png                  # 400x840 靈爪猴立牌 (對齊char_rabbit規格)
└── game/assets/sprites/player/
    ├── rabbit_idle.png / rabbit_idle_x3.png
    ├── lion_idle.png / party/lion_idle.png
    ├── fox_idle.png / party/fox_idle.png
    ├── boar_idle.png / party/boar_idle.png
    ├── macaque_idle.png / macaque_idle_x3.png / party/macaque_idle.png
    └── paperdoll/                        # 紙娃娃模組化切片庫
        ├── weapon/                       # 通用武器層
        ├── armor/                        # 通用服裝外裝層
        ├── accessory/                    # 通用飾品層
        ├── key/                          # 通用發條鑰匙層
        ├── curio/                        # 通用奇玩層
        ├── rabbit/                       # 兔族專屬素體與耳朵
        ├── lion/                         # 獅族專屬素體與鬃毛
        ├── fox/                          # 狐族專屬素體與尾部
        ├── boar/                         # 豬族專屬素體與獠牙
        └── macaque/                      # 猴族專屬素體與彈簧尾
```

---

## 5. 結語與提報審查

本規格書與 `docs/design/paperdoll_slots.json` 嚴格貫徹了 Kevin 關於「首發 5 種動物（兔/狐/獅/豬/猴）」、「7 大機械化部件槽位」與「400×840 素體標準」之指示，同時嚴守護欄不涉及未拍板之四英雄地位與社交架構。

規格已就緒，建請側案製作人老周（side）進行 Review！
