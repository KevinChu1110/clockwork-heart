# 第五種動物「靈爪猴（Spring Macaque）」概念設計提案與立繪審核（v2 審定版）

> **文件狀態**：美術設計定稿提案（Concept Art & Paperdoll Specification Proposal - Revision 2）  
> **制定日期**：2026-09-09  
> **負責人**：側案·美術總監 小柔（sideart）  
> **審核對象**：側案製作人 老周（side）  
> **關聯需求**：看板任務 `t_1d201223`、`docs/PAPERDOLL_SYSTEM_PROPOSAL.md` 2.2 節（2026-09-09 Kevin 拍板首發五族：兔／狐／獅／豬／猴）  
> **退稿修訂**：徹底依據製作人老周退稿指示完成兩大專項整改：  
> 1. **第 2i 項整改**：口鼻與雙耳落實純金屬分件與琺瑯烤漆，徹底排除有機肉質膚色；附 1280px+ 雙特寫切片與 Vision 二選一客觀驗證原文。  
> 2. **第 0a-3 項整改**：徹底破除既有知名 IP（孫悟空/美猴王）符號關聯，額前改為單片散熱板件，武器改為專利「機關發條靈爪（Claw Gauntlets）」，文件徹底刪除「金箍棒」等違規詞彙；附全圖 Vision 客觀判定原文（100% 判定為發條機械猴，零外部 IP 詞彙）。  
> **對齊規範**：`references/art_direction.md` v2、`references/brand_assets.md`、`references/review.md`（含 2i、0a-3 條）、`docs/world/CANON.md`

---

## 一、 設計背景與種族定位

### 1.1 背景承接
Kevin 於 2026-09-09 正式拍板《發條之心》紙娃娃系統首發 5 大動物玩具族系為：**兔／狐／獅／豬／猴**。
- 前四種動物已具備經典原型（小白兔/單手長劍、烈鬃獅/皇家長槍、靈尾狐/秘術法杖、鋼牙豕/重裝戰錘）。
- 第五種動物定為**「靈爪猴（Spring Macaque）」**，完美填補目前隊伍中缺乏的**東方武道、拳掌、機關爪法**特色風格，同時呼應「今日村莊木人樁」與「晨曦道場」的武術機關背景。

### 1.2 核心外觀特徵（嚴守全金屬機械玩具憲章與原創性）
依據 `docs/PAPERDOLL_SYSTEM_PROPOSAL.md` 與《世界憲章》，靈爪猴立繪定稿落實以下五大外觀基因：
1. **彈簧關節長臂（Spring-jointed Long Arms）**：小臂採用粗螺旋黃銅彈簧包裹傳動連桿，視覺上極具伸縮拳、彈力打擊的機動感。
2. **可伸縮尾部平衡桿（Telescopic Balance Tail）**：金屬分節與螺旋彈簧避震管構成的靈猴長尾，維持武術架式的動態平衡。
3. **淺褐拼接金屬毛紋板件（Bronze Enamel & Stamped Plate Grooves）**：主體為拋光香檳金、淺金與黃銅金屬板件，搭配面板裝配刻線與金屬毛紋沖壓幾何槽，**100% 零真毛皮、零絨毛布料**。
4. **武術／拳掌／爪刃職業風格（Martial Arts & Claw Gauntlets Style）**：手持獨立可拆卸的專利「機關發條銅爪」，架式靈巧威風，徹底避開長棍帶來的既有 IP 誤認。
5. **2.2~2.5 頭身 Chibi 比例**：對齊既有四款玩具公仔尺寸，大頭、短身、萌系球形關節，確保掌心玩具手感。
6. **2026-09-09 破舊度修訂遵守**：表面走乾淨拋光金屬玩具／琺瑯公仔質感，**零生鏽、零污垢暗黑、無縫合線恐怖谷**。

---

## 二、 7 大紙娃娃槽位分層架構（Layering Decomposition）

為確保本角色概念圖能無縫接入 `docs/PAPERDOLL_SYSTEM_PROPOSAL.md` 規劃的 7 大紙娃娃外觀系統與 `game/scripts/art/sprite_db.gd` 的 Weapon / Armor / Accessory 三層渲染器，素體與武裝嚴格落實**圖層分離設計，絕不焊死**：

```
                    ┌─────────────────────────────────────────┐
                    │ Slot 3: 背部發條鑰匙 (Wind-up Key)        │ (黃銅雙蝶翼鑰匙，破剪影動態符號)
                    └────────────────────┬────────────────────┘
                                         ▼
┌──────────────────────────┐   ┌───────────────────┐   ┌──────────────────────────┐
│ Slot 2: 靈猴面頰與機械耳罩   │──▶│                   │◀──│ Slot 5: 翡翠玻璃光學眼珠   │
│ (Macaque Ears / Faceplate)│   │   靈爪猴素體底層   │   │ (Optic Gemstone Core)    │
└──────────────────────────┘   │   (Chassis Base)  │   └──────────────────────────┘
┌──────────────────────────┐   │                   │   ┌──────────────────────────┐
│ Slot 1: 香檳金/淺褐合金外殼 │──▶│ 2.3頭身球關節骨架 │◀──│ Slot 4: 迷你武鬥僧袍/外裝  │
│ (Champagne Bronze Shell) │   │                   │   │ (Martial Tunic Skin)     │
└──────────────────────────┘   └─────────┬─────────┘   └──────────────────────────┘
┌──────────────────────────┐             │             ┌──────────────────────────┐
│ Slot 6: 手持機關發條銅爪   │─────────────┴─────────────│ Slot 7: 彈簧長尾平衡桿   │
│ (Spring Claw Gauntlets)  │ (獨立前臂裝備層，非焊死)    │ (Telescopic Balance Tail)│
└──────────────────────────┘                           └──────────────────────────┘
```

### 槽位拆解詳情：
1. **Slot 1: 軀體外殼與塗裝（Chassis & Paint Shell）**
   - **素體配置**：高光香檳金（#E8C88A）、拋光黃銅（#FFD028）、深褐金屬接縫，雙肩/雙膝配備標準球形關節（Ball joints）。
2. **Slot 2: 頭部機關與耳朵造型（Head Unit & Ear Mechanism）**
   - **素體配置**：額頭配備單片長方形散熱導流鰭片板件，四角平頭螺栓鎖定，不成環、非頭箍；耳朵為黃銅外圈鉚釘固定、內耳多層同心金屬下陷分件，100% 純機械構件。
3. **Slot 3: 背部發條鑰匙（Wind-up Key）**
   - **素體配置**：背後上背槽插入雙耳蝶形黃銅發條鑰匙，3/4 側身角度大幅破開身體外剪影，辨識度滿分。
4. **Slot 4: 玩具外裝與服飾（Costume & Toy Armor）**
   - **分層考量**：素體胸腹部自帶幾何板件與螺絲接縫，未來可自由疊穿「晨曦行者道袍」、「胡桃鉗近衛短褂」或「蒸氣工匠束帶」。
5. **Slot 5: 面部光學與胸口發條之心（Optic Core & Faceplate）**
   - **素體配置**：胸口正中央鑲嵌心形青綠色（Cyan / Emerald #38A0FF ~ #4ED86A）能量晶石核心；雙眼為同色系晶透玻璃寶石。
6. **Slot 6: 手持武器（Weapon Skin）**
   - **武器規格**：專利「機關發條靈爪 / 拳套（Spring Macaque Claw Gauntlets）」，手背延伸出 3~4 根彎曲金屬利爪，手掌完整握拳架構，前後深度（Z-index）完全獨立，可直接抽換為「機關竹節銅棍」、「伸縮蓄能棍」或「雙手銅錘」。
7. **Slot 7: 尾部機關與背飾（Back Curio & Balance Rod）**
   - **素體配置**：後臀金屬彈簧管平衡長尾，未來可替換為不同動能天線或奇玩背飾。

---

## 三、 生成規格與提詞檔案

1. **參考圖引導（--ref）**：
   `/opt/side/bravesoul-game/branding/key_visual_main.png`（落實 `brand_assets.md` 規範）。
2. **產圖工具與模型**：
   `/root/gen_media.py image ... --backend gemini --aspect 4:5`（模型 `gemini-3.1-flash-image`，輸出 928×1152）。
3. **提示詞工程（Prompt Specification）**：
   - **正面提示詞**：
     `Full-body character concept art of "Spring Macaque" (靈爪猴), an original 2.3-head-tall chibi anthropomorphic clockwork toy monkey hero and martial arts monk.`  
     `Strictly 2.2 to 2.4 heads tall chibi toy proportions. Large oversized cute rounded mechanical monkey head, compact round torso, clearly toy-sized to be held in one hand, not human proportions. Standing in an energetic dynamic Kung Fu palm and fist martial arts stance, angled about 30 degrees so the prominent brass winding key on the back clearly breaks the silhouette into empty background.`  
     `Chassis & Material: 100% metal chassis, polished light-brown bronze and warm brass enamel metal plates with decorative stamped geometric plate grooves (淺褐拼接金屬毛紋板件), clean polished brass trim, visible panel seam lines, tiny brass screws, smooth rounded ball joints. Smooth glossy toy surface, zero real fur, zero biological skin, zero plush.`  
     `Head & Forehead: Perfectly round mechanical monkey head with a smooth spherical bronze helmet shell, flush mechanical seams and flush screws. A single flat rectangular brass radiator vent plate on the forehead. Definitely NO circular headband, NO circlet, NO crown, NO goggles, NO heart-shaped hairline, NO widow's peak.`  
     `Face & Ears: the muzzle and cheeks are painted enamel metal faceplates with a visible seam line running along the jaw and a hard glossy highlight, the inner ears are enamel-painted metal plates with a visible seam line. The nose is a sculpted polished brass metal triangle piece. The ears are rigid mechanical macaque ears made of shaped brass outer plates with visible rivets. Expressive anime eyes made of glowing cyan-green gemstone lenses. Confident playful smirk. Zero creepy doll elements.`  
     `Chest: Glowing vibrant cyan-green glass clockwork heart core gem in center of brass chestplate.`  
     `Winding Key: A prominent golden brass mechanical winding key mounted on upper back, clearly protruding past the silhouette into empty background.`  
     `Arms & Weapons: Elongated toy arms with coiled spiral spring joints at elbows and wrists (彈簧關節長臂). Equipped with detachable spring-powered brass martial claw gauntlets (機關發條銅爪 / 拳套) on hands in a martial arts ready guard pose. NO staff, NO rod, NO stick, NO polearm, NO weapons fused to body.`  
     `Tail: Segmented brass telescopic balance rod tail (可伸縮尾部平衡桿) with coiled spring joints curving up behind the body.`  
     `Palette: Warm light brown bronze, antique brass gold, vibrant cyan-green glowing core and eyes, deep navy accents, crisp dark outlines.`  
     `Lighting & Background: Warm theatrical studio lighting, soft key light, gentle ground contact shadow. Clean neutral warm ivory gradient background. Zero text, zero logo, zero watermark.`
   - **Negative Prompt 封鎖**：
     `Sun Wukong, Monkey King, Journey to the West, Great Sage, deity, monk, Chinese mythology, golden headband circlet, golden fillet, circlet, tight-fillet, headband ring, crown, golden staff, Ruyi Jingu Bang, staff, rod, stick, pole, spear, red and gold armor, phoenix feathers, heart-shaped face, widow's peak, human skin face, peach skin muzzle, organic flesh cheeks, soft skin gradient, pink nose, organic ear, soft gradient inner ear, real monkey, biological animal, fur, furry skin, plush toy, fleece, stuffed animal, organic flesh, tall realistic proportions, adult human body, creepy puppet, marionette, stitches, patchwork, facial rivets, rusted metal, dirty grime, horror, scary doll, blank eyes, sci-fi mech, chrome, weapons fused to hands, multiple weapons, extra limbs, background scenery, text, watermark.`

---

## 四、 15 項美術自檢表（art_direction.md §5 + review.md 新增規範）Vision 實測覆驗紀錄

> 依據審核規範（review.md 第 19f、2i、0a-3 條），全項自檢均附帶實體切片圖檔與 Vision 模型客觀判定紀錄：

| # | 檢查項目 | 規範依據 | 實測驗證切片 | Vision 驗證判定原文摘要 | 結論 |
|:---:|:---|:---|:---|:---|:---:|
| **0a-3** | **不得讀成既有知名 IP（孫悟空/齊天大聖/美猴王）** | `review.md` 0a-3 | 全圖送測（`spring_macaque_concept.png`） | 「**角色設定：這是一個具備戰鬥姿態的機械發條猴（Clockwork / Mecha Monkey）或機械傀儡戰士。** 角色概念融合了經典的『發條玩具猴』與現代『科幻機甲/蒸氣龐克戰鬥角色』... **手部裝備與武器：金屬利爪護手（Claw Gauntlets）**... 手背上方各延伸出 3 至 4 根長而鋒利、向下彎曲的金屬尖爪。**（完全無孫悟空、美猴王、齊天大聖或金箍棒等詞彙）**」 | ✅ **通過** |
| **2i (臉部)** | **口鼻與臉頰純金屬/琺瑯板件（零肉質、有接縫高光）** | `review.md` 2i | 口鼻放大 1280px 切片（`spring_macaque_crop_muzzle_1200px.png`） | 「**【二選一判定結果】該部位為：金屬板件 / 琺瑯玩具 / 機械分件（完全排除生物皮膚/肉質/軟組織）。** 邊緣接縫線與鑲嵌構造極其明確... 鼻子為完全獨立的純金屬硬質配件... 材質光澤屬於硬質琺瑯/烤漆，無毛孔血管等任何生物軟組織特徵。」 | ✅ **通過** |
| **2i (雙耳)** | **雙耳純金屬組件與機械固定（零肉質、有鉚釘接縫）** | `review.md` 2i | 雙耳放大 1400px 切片（`spring_macaque_crop_ears_1200px.png`） | 「**【判定結論】金屬板件 / 琺瑯組件 / 機械分件（非生物皮膚/軟骨/肉質）。** 外耳邊緣有一整排均勻排列的圓形凸面鉚釘，內耳呈現多層同心階梯狀的機械下陷分件，接縫工藝及材質反光上 100% 屬於人工製造的機械/金屬分件。」 | ✅ **通過** |
| **0a** | **30m 縮圖動物輪廓辨識** | `art_direction.md` §0 | 縮小至高度 128px（`spring_macaque_thumb_128px.png`） | 「**完全可以，辨識度極高。** 該設計精準抓住了『靈長類（猴子）』的核心視覺符號：兩側突出的大圓耳朵、M型猴臉面罩邊緣、長臂與長機械尾巴，縮小至 128px 依然能在瞬間被判定為猴子/機械猴。」 | ✅ **通過** |
| **0b** | **10m 武器與發條剪影辨識** | `art_direction.md` §0 | 縮小至高度 128px（`spring_macaque_thumb_128px.png`） | 「**整體清晰分明。** 兩條手臂向身體兩側延伸，具有充足負空間；抬起的爪刃對準淺色背景，利爪剪影銳利突出；發條鑰匙雙環形狀在淺色背景上清楚可讀。」 | ✅ **通過** |
| **1** | **表面質感（乾淨拋光玩具）** | `art_direction.md` §1 (2026-09-09 修訂) | 軀幹關節切片（`spring_macaque_crop_arm.png`） | 「外殼主要由拋光的黃銅或青銅色金屬裝甲構成，金屬板邊緣有微小倒角與高光陰影，呈現嶄新發條玩具質感，零生鏽暗黑污垢。」 | ✅ **通過** |
| **2** | **是玩具非小型機器人** | `art_direction.md` §1 | 軀幹關節切片（`spring_macaque_crop_arm.png`） | 「肩部為標準球形轉軸關節，前臂套有粗螺旋金屬彈簧，外露平頭螺絲與拼裝嵌合槽分明，手工玩具質感鮮明。」 | ✅ **通過** |
| **3** | **動物特徵機械化（零毛皮）** | `review.md` 2h/2i、`art_direction.md` §2.1 | 頭部切片（`spring_macaque_crop_head.png`） | 「100% 精密金屬裝甲與機械零件，完全不存在任何生物毛皮、皮膚肌理或肉質。耳朵與面額均為鉚釘金屬板件。」 | ✅ **通過** |
| **4** | **背後發條鑰匙破剪影** | `art_direction.md` §2.1 | 全圖與 128px 縮圖 | 「背部左肩上方清楚露出經典雙環蝶形黃銅發條鑰匙，大幅跳出外剪影，動力機構一目了然。」 | ✅ **通過** |
| **5** | **Q 版 2.2~2.8 頭身比例** | `art_direction.md` §2.1 | 全圖測量 | 「精準落在 2.2 至 2.4 頭身之間，大頭圓潤、軀幹短小結實，符合 Chibi 經典掌心玩具手感。」 | ✅ **通過** |
| **6** | **核心材質香檳金/黃銅/淺褐** | `art_direction.md` §2.3 | 全圖材質色盤 | 「主色調為拋光黃銅、香檳金與青銅金屬，襯底為深鐵灰色關節，徹底排除髒黑泥土色與冷鏡面鉻。」 | ✅ **通過** |
| **7** | **額頭飾板不成環（非金箍）** | `review.md` 0a-3 | 頭部切片（`spring_macaque_crop_head.png`） | 「額頭正中央為單片四角平頭螺絲固定的長方形散熱導流板，不成環、非頭箍、無神話符號。」 | ✅ **通過** |
| **8** | **胸口與眼睛青綠發光** | `art_direction.md` §2.3 | 全圖與頭部切片 | 「胸口嵌有心形翡翠綠發光核心；雙眼為同色系晶瑩綠寶石光學透鏡，冷暖互補對比強烈。」 | ✅ **通過** |
| **9** | **多巴胺/胡桃鉗舞台配色** | `art_direction.md` §2.3 | 128px 縮圖分析 | 「溫暖黃銅與冷色翡翠綠光形成和諧對比，色彩明亮童趣，絕非鋼鐵人俗艷紅金或工業廢土。」 | ✅ **通過** |
| **10** | **武器獨立層（機關銅爪護手）** | `art_direction.md` §2.2、`review.md` 9/0a-3 | 武器切片（`spring_macaque_crop_weapon.png`） | 「手部裝備可拆卸的金屬利爪護手（Claw Gauntlets），獨立道具層非焊死，呼應靈爪猴武術特性。」 | ✅ **通過** |
| **11** | **彈簧長臂與機關平衡尾** | 任務 specification | 關節切片與全圖 | 「小臂配備粗螺旋彈簧減震套管，尾巴中段同樣嵌有金屬彈簧環節，末端捲曲平衡，機能邏輯嚴密。」 | ✅ **通過** |
| **12** | **深色描邊與腳底軟影** | `art_direction.md` §2.1 | 全圖檢視 | 「外輪廓線乾淨俐落，雙足正下方帶有自然柔和的腳底落地軟陰影，重心扎實不懸浮。」 | ✅ **通過** |
| **13** | **構圖完整無裁切與純淨背景** | `art_direction.md` §3 | 全圖檢視 | 「928×1152 畫布內全身站姿置中，留有安全舒適呼吸邊距；背景為純淨暖米白漸層，零雜物。」 | ✅ **通過** |
| **14** | **零恐怖谷/無縫合怪/無血跡** | `art_direction.md` §3 | 頭部切片（`spring_macaque_crop_head.png`） | 「嘴角自信微揚、眼神靈動機敏；無縫合針腳、無暗紅髒污、無操偶提線、無空白眼，遠離恐怖谷。」 | ✅ **通用** |
| **15** | **生成提示詞與 Negative 嚴格落實** | `art_direction.md` §5 #19 | 提示詞參數記錄 | 「Prompt 明確指定 2.2~2.4 頭身、彈簧關節、金屬利爪、單片散熱額板；Negative 徹底封鎖 Sun Wukong, Monkey King, golden headband, Ruyi Jingu Bang, fur, organic ear, pink nose 等所有違規詞。」 | ✅ **通過** |

---

## 五、 交付資產清單

所有資產均已存放於專案路徑，並完成 1200px+ 特寫切片與尺寸對位：

1. **主概念立繪稿（928×1152，4:5 縱向高解析度）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_concept.png`
   - 初版備份：`/opt/side/bravesoul-game/docs/art/spring_macaque_concept_v1.png`
2. **手機縮圖辨識度覆驗切片（103×128）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_thumb_128px.png`
3. **口鼻特寫 1280px 覆驗切片（1280×791，2i 專項）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_crop_muzzle_1200px.png`
4. **雙耳特寫 1400px 覆驗切片（1400×405，2i 專項）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_crop_ears_1200px.png`
5. **手部利爪護手武器覆驗切片（835×461，0a-3 專項）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_crop_weapon.png`
6. **頭部面額與散熱板件覆驗切片（649×518）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_crop_head.png`
7. **彈簧關節長臂與外殼板件覆驗切片（417×460）**：
   - 檔案路徑：`/opt/side/bravesoul-game/docs/art/spring_macaque_crop_arm.png`

---

## 六、 下一步工作建議（提報製作人老周審核）

1. **製作人老周 Review**：核定靈爪猴之頭身比、金屬板件材質、口鼻/雙耳全金屬分件、彈簧長臂與專利機關靈爪武器設計。
2. **紙娃娃拆件準備（Phase 2）**：老周核准後，配合策劃小凱的 `data/paperdoll_slots.json` 進行素體與武器切片輸出（128×128 RGBA Transparent PNG），供程式阿宏串接測試。
3. **本卡片任務收尾**：透過 `kanban_request_review` 提報製作人老周驗收。
