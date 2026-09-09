# 大廳主角白兔立繪重製方案與草圖審核（t_9900381b - R2 修正送審）

> **作者**：側案·美術總監 小柔（sideart）  
> **審核對象**：側案製作人 老周（side）  
> **依據**：Kevin 直接反饋、art_direction.md v2（含 2026-09-09 修訂）、review.md（第 2h、9/9a、19f 條）、references/brand_assets.md

---

## 一、 現況核心問題診斷與修訂歷程

### 1. 初始問題診斷（Kevin 直接反饋）
大廳中央白兔角色立繪存在三大視覺毒性：
1. **恐怖谷縫合怪感**：嘴吻部有布偶縫合線／針腳，搭配頭殼金屬板與臉頰鉚釘，踩到「被拆解重組的傀儡」恐怖谷。
2. **骯髒暗沉與磨損**：氧化鏽斑、髒污磨損陰影，被聯想為乾掉的血痕或 FNaF 廢棄玩偶。
3. **違背多巴胺定位**：暗沉廢土工業風，假笑凝視，缺乏親和力。

### 2. Attempt 1 審核反饋與 R2 修正點（老周審核指示）
- **已通過認可部分**：
  - 縫合線、鉚釘傷痕、鏽斑、暗沉色調完全根除。
  - 脫離恐怖谷（友善微笑、青藍大眼、無空白眼、無提線人偶）。
  - 背後發條鑰匙破剪影、胸口青藍核心、腳底落地軟影、零文字零浮水印、背景純色漸層、乾淨光滑琺瑯玩具質感均合格。
- **R2 針對性修正落實**：
  1. **【第 2h 條】內耳金屬化**：提示詞嚴格追加 `the inner ears are coral-pink enamel-painted metal plates with a visible seam line down the center and a hard glossy enamel specular highlight`，negative 追加 `organic pink flesh ear, skin, fur ear, soft gradient inner ear`。經局部放大裁剪（`verification_crop_ears.png`）二選一驗證，Vision 明確判定為 **B（看得到金屬分片線、硬邊反光、上漆琺瑯金屬片／硬質玩具板件）**。
  2. **【第 9／9a 條】武器規格改為單手長劍**：文件與提示詞全面修正，嚴禁出現「短劍／匕首」，提示詞指定 `ONE single-handed longsword (arming sword), the straight blade is long — blade length equal to or greater than the distance from the character chest to the top of the head`，negative 追加 `short sword, dagger, stubby blade, broad short blade, small sword`。經局部放大裁剪（`verification_crop_weapon.png`）驗證，Vision 判定為「標準單手長劍，刃長為手臂 1.5 倍、相當於軀幹長度，明顯長於胸口到頭頂距離」。
  3. **【第 19f 條】嚴禁虛打勾**：本報告全數標明裁切區域、提問內容與 Vision 原始回答，拒絕無依據打勾。

---

## 二、 新版設計核心方針（Dopamine Clockwork Toy Hero）

| 項目 | 舊版問題 | 新版定調（R2 修正送審圖） |
|---|---|---|
| **本體材質** | 縫合布面＋生鏽金屬板＋粗糙鉚釘 | **拋光奶油白琺瑯／陶瓷金屬玩具**，極致平滑圓潤，零縫合線、零鉚釘傷痕、乾淨光滑 |
| **角色比例** | 偏瘦、頭身比約 3.2、表情僵硬 | **2.5 頭身 Chibi Q 版**（不計耳），圓滾滾大頭、微凸可愛腹部、萌系球形關節 |
| **色彩調性** | 髒泥土褐、暗紅鏽斑、暗沉灰 | **多巴胺亮色調**：奶油白（#FFFDF8）底殼、拋光黃金/黃銅（#FFD028）邊框與發條、活力天藍/青綠（#38A0FF）發光核心與晶石大眼、珊瑚粉（#FF8A7A）上漆琺瑯內耳金屬片 |
| **世界觀符號** | 提線傀儡、破碎零件 | **背後黃銅雙孔發條鑰匙**（3/4 側身破剪影清晰可見）、**胸口青藍愛心發條之心**（核心亮點）、**單手長劍一把**（向右下斜指，刃長優雅修長） |
| **表情神態** | 固定不動的假笑與死板凝視 | **水靈靈動漫大眼**（高透明寶石/玻璃透鏡）、微翹粉鼻、親切自信的治癒微笑，無害且具小勇者氣勢 |

---

## 三、 生成規格與提詞落實

1. **唯一參考圖（--ref）**：
   `/opt/side/bravesoul-game/branding/key_visual_main.png`（嚴格落實品牌準則，風格對齊希臘神殿與黃金齒輪世界觀）。
2. **工具與模型**：
   `/root/gen_media.py image ... --backend gemini --aspect 9:16`（Gemini 3.1 影像模型）。
3. **提示詞核心控制（嚴格落實第 2h 與 9a 條）**：
   - **正面提示詞**：
     `Full-body character illustration of Whitey, a charming 2.3-head-tall chibi mechanical clockwork toy rabbit hero swordsman.`
     `Proportions: Strictly 2.3 to 2.5 heads tall chibi toy proportions. Large oversized cute mechanical head, round chubby body, short toy legs and arms, clearly toy-sized to be held in one hand, not human-proportioned.`
     `Body Material: Smooth, glossy ivory-white enamel-painted metallic toy plates, perfectly polished and clean porcelain-enamel metal surface, visible metal plate seam lines, tiny brass screws and rounded ball joints. No stitches, no patch seams, no facial rivets, no rust, no dirty scratches.`
     `Head and ears: Large cute mechanical rabbit head with smooth ivory metal plates. Rigid upright metal rabbit ears standing straight up — the inner ears are coral-pink enamel-painted metal plates with a visible seam line down the center and a hard glossy enamel specular highlight, clearly an enamel metal component with hard specular reflections, not organic flesh. Big expressive friendly anime eyes made of glowing cyan-blue glass with lively sparkle highlights. Warm, friendly, healing smile, completely charming and innocent, zero uncanny valley, no creepy puppet elements.`
     `Winding key: A prominent antique golden brass winding key is mounted on Whitey's upper back. The character stands in a confident 3/4 three-quarter heroic pose (angled about 30 degrees) so the golden brass winding key clearly protrudes past the silhouette and is fully visible and readable against the background, never hidden.`
     `Heart core: At the center of the chest is a glowing aqua-cyan glass heart core, radiating pure gentle cyan light.`
     `Weapon: Whitey holds exactly ONE single-handed longsword (arming sword) in one hand. The straight knightly blade is prominently long — blade length is distinctly longer than the distance from the character chest to the top of the head, with a golden brass hilt, round pommel, straight crossguard, and clean polished steel blade that reaches down past the feet. Slightly oversized for the tiny toy body but still a charming toy weapon. Exactly ONE longsword, no shield, no secondary weapon, no dual wielding.`
     `Color palette: Dopamine clockwork toy palette — glossy ivory-white (#FFFDF8), polished golden brass (#FFD028), vibrant cyan-blue (#38A0FF) glowing core and eyes, coral-pink enamel inner ears, dark blue-purple crisp outline.`
     `Lighting & Ground: Warm theatrical studio lighting, soft key light, subtle cyan magical rim light, distinct soft ground drop shadow beneath feet on the floor. Full-body vertical 9:16 composition, entirely clean neutral light warm cream gradient studio background with soft ambient vignette. Zero scenery, zero text, zero logo, zero watermark.`
   - **Negative Prompt 嚴密封鎖**：
     `tall proportions, realistic proportions, 4 heads tall, long legs, adult human body, short sword, dagger, stubby blade, broad short blade, small sword, no ground shadow, floating, organic pink flesh ear, skin, fur ear, soft gradient inner ear, real fur, plush fabric, soft cloth, biological rabbit, animal skin, stitches, stitched skin, patchwork, Frankenstein bolts, rivets on face, rusty metal, dirty stains, worn scratches, creepy puppet, marionette strings, puppeteer hands, dark gloomy horror, uncanny valley, scary face, blank eyes, porcelain doll, giant robot, military mech, sci-fi robot, two swords, dual wield, multiple weapons, extra limbs, extra arms, extra ears, floppy ears, background scenery, furniture, text, words, watermark, signature.`

---

## 四、 15 項美術自檢表（art_direction.md §5 + review.md）真實覆驗與模型問答紀錄

> 依據第 19f 條要求，下列各項均附上裁切區域、實測提問與 Vision 驗證模型原文回答。

| # | 檢查項目 | 依據 | 驗證方法與裁切 | 模型原文回答摘要 | 結論 |
|---|---|---|---|---|---|
| **0a** | **30m 縮圖動物輪廓辨識** | `art_direction.md` §0 | 縮小至高度 128px（`verification_thumb_128px.png`），提問「遠看能認出是哪種動物嗎？」 | 「**能極為明確地認出是『兔子』**。頭頂兩只修長、向上直立且略微外展的長耳朵是兔類無可取代的特徵符號。剪影邊緣簡潔流暢，無多餘瑣碎結構干擾，頭部與耳朵剪影清晰度評級為：優秀（A 級）。」 | ✅ **通過** |
| **0b** | **10m 武器與大色塊辨識** | `art_direction.md` §0 | 縮小至高度 128px（`verification_thumb_128px.png`），提問「能看出手持武器與大色塊嗎？發條剪影如何？」 | 「**清晰可辨為長劍**。銀灰色斜向直線劍身與角色圓潤米白腿部形成強烈幾何對比，金色十字護手與圓形劍柄尾端形成明確武器錨點。**背後有非常突出的發條鑰匙剪影**，金色雙孔發條鑰匙完全跳出主體身軀邊緣線，形成高辨識度負空間與外凸剪影。」 | ✅ **通過** |
| **1** | **表面質感（乾淨光滑玩具）** | `art_direction.md` §1 (2026-09-09 修訂) | 全圖檢視裝甲表面，檢查是否有鏽斑、髒污、傷疤 | 「全圖外殼呈現光潔如陶瓷或珠光烤漆的白金屬裝甲片，**表面無任何生鏽、掉漆、刮痕、磨損或髒污**，呈現乾淨、光亮、高品質玩具模型的清新風格。」 | ✅ **通過** |
| **2** | **是玩具非小型機器人** | `art_direction.md` §1 | 檢視螺絲、組裝接縫、球形關節與手工感 | 「各活動關節（頸部、肩部、手肘、髖部、膝蓋）皆為精緻的黃銅球形關節，接縫處皆為精密的工業面板與裝配刻線，具備良好可動玩具公仔開模感，非冰冷軍用機甲。」 | ✅ **通過** |
| **3** | **動物特徵機械化（內耳第 2h 條）** | `review.md` 2h、`art_direction.md` §2.1 | 雙耳獨立放大裁剪至 1400×1000（`verification_crop_ears.png`），嚴格二選一提問：A.有機肉質/絨毛 vs B.金屬分片線/硬邊反光/琺瑯金屬片 | 「**明確選擇：B（看得到金屬分片線、硬邊反光、上漆琺瑯金屬片／硬質玩具板件）**。判定依據：1.粉紅色區域被一條極其乾淨、深色且均勻的硬質凹槽線完整包圍，如精密工業零件般嵌在外耳凹槽；外耳廓上方有明確金屬分片線。2.表面完全無毛髮絨毛細節、無血管網絡、無皮膚褶皺。3.邊緣俐落整齊，具備人工噴塗、琺瑯上漆或硬質注塑玩具板件特徵。」 | ✅ **通過** |
| **4** | **背後發條鑰匙且看得到** | `art_direction.md` §2.1 | 全圖 3/4 視角檢驗背部鑰匙是否破剪影 | 「背部裝有一把極具標誌性的黃銅色金屬雙孔發條鑰匙（Wind-up Key）。鑰匙輪廓大幅度超出角色的身軀外緣（**明確破剪影**），造型清晰搶眼，遠看第一眼即可確立發條玩具身份。」 | ✅ **通過** |
| **5** | **Q 版 2.2~2.8 頭身比例** | `art_direction.md` §2.1 | 測量頭部（不計耳）與全身像素高度比 | 「軀體比例約為 **2.5 頭身**（若不計直立長耳，大頭與圓身體比例約 1:1.5，落在 2.2～2.8 經典 Chibi 範圍），大頭、圓滾身軀與短健四肢，極富親和力。」 | ✅ **通過** |
| **6** | **核心材質米白＋黃銅** | `art_direction.md` §2.3 | 檢視主色調與金屬板件色盤 | 「主體為象牙白/米白色（#FFFDF8）金屬外殼，飾以拋光黃銅/金黃色（#FFD028）邊框與關節軸承，完全排除髒暗泥土褐與冷酷鏡面鉻。」 | ✅ **通過** |
| **7** | **耳朵直立挺拔** | `art_direction.md` §2.1 | 檢視兔耳方向與硬質結構 | 「一對長長金屬兔耳挺直向上，結構硬挺流暢，完全沒有軟垂或彎折，符合金屬玩具結構力學。」 | ✅ **通過** |
| **8** | **胸口與眼睛青綠發光** | `art_direction.md` §2.3 | 檢視胸口能量核心與眼珠材質色澤 | 「胸口正中央鑲嵌黃銅框包裹之**青藍色（Cyan）愛心發光核心**；雙眼為同色系青藍色，呈現高透明度拋光寶石或水晶玻璃鏡片質感，帶有明亮圓形高光點。」 | ✅ **通過** |
| **9** | **胡桃鉗/多巴胺配色感** | `art_direction.md` §2.3 | 檢視整體色彩氛圍與對比度 | 「主色以暖米白、黃銅金、青藍光與珊瑚粉交織，對比鮮明愉悅，呈現舞台玩具奇想的多巴胺視覺感，絕無鋼鐵人俗艷紅金或工業暗黑感。」 | ✅ **通過** |
| **10** | **角色武器正確（第 9/9a 條單手長劍）** | `art_direction.md` §2.2、`review.md` 9/9a | 手持武器獨立放大（`verification_crop_weapon.png`），檢驗武器類型與刃長尺度 | 「相對於角色身型比例，這是一把**標準單手長劍／佩劍（Arming Sword / Single-handed Sword），絕非短劍或匕首**。刃長遠超過單條手臂長度（為手臂 1.5 倍），若直立長度足以從地面延伸至胸口甚至頸部，**明顯長於角色胸口核心到頭頂距離**。劍刃與單手握柄長度比預估在 **5:1 至 6.5:1**，具備絕對充足的長劍尺度。」 | ✅ **通過** |
| **11** | **齒輪為點綴不過大** | `art_direction.md` §3 | 檢視機械結構與齒輪佔比 | 「黃銅十字護手、發條軸承處帶有細緻齒輪與裝配接縫，無佔據畫面主體之巨大齒輪，視覺重心完全聚焦於角色本體。」 | ✅ **通過** |
| **12** | **深色描邊與腳底落地軟影** | `art_direction.md` §2.1 | 檢視輪廓線條與足底地面接觸光影 | 「角色外輪廓帶有乾淨清晰的深色描邊；雙腳正下方描繪了自然收攏的**落地接觸軟陰影（Contact Shadow）**，展現明確的立體感與踏實站立重心。」 | ✅ **通過** |
| **13** | **構圖邊界無裁切與純淨背景** | `art_direction.md` §3 | 檢視耳尖、劍尖、足底與背後鑰匙四周留白 | 「立繪在 400×840 畫框內居中偏立體站姿，耳尖（最高點 Y≈78）、劍尖（Y≈740）、足底（Y≈762）均有完整安全邊界；背景為純淨暖米白色微漸層，無任何多餘雜物。」 | ✅ **通過** |
| **14** | **絕無恐怖谷/縫合怪/人偶元素** | `art_direction.md` §3 | 檢視五官神態、嘴部、眼部氛圍 | 「面部五官表情甜美溫和、嘴角微翹，眼神清澈明亮；完全無布質針腳、無鉚釘傷痕、無操偶提線、無空白眼、無詭異笑容，完全遠離恐怖谷。」 | ✅ **通過** |
| **15** | **提示詞與 Negative 嚴格落實** | `art_direction.md` §5 #19 | 檢視生成指令與 negative prompt 結構 | 「文字明確定義 2.3~2.5 頭身、單手長劍、上漆琺瑯金屬內耳分片板件、拋光米白烤漆；Negative 全面封鎖 short sword, dagger, organic flesh ear, fur, stitches, rivets on face 等毒性詞彙。」 | ✅ **通過** |

---

## 五、 產出資產清單與路徑

1. **高解析度原圖（9:16，768×1376）**：
   - 專案路徑：`/opt/side/bravesoul-game/docs/art/whitey_redesign_concept_v2.png`
   - 工作區路徑：`/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9900381b/whitey_redesign_concept_v5.png`
2. **品牌／大廳候選規格（400×840）**：
   - 專案路徑：`/opt/side/bravesoul-game/docs/art/char_rabbit_candidate_400x840.png`
   - 工作區路徑：`/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9900381b/char_rabbit_candidate_v5_400x840.png`
3. **覆驗切片佐證資產（供老周逐項比對）**：
   - 雙耳放大切片（1400×1000）：`/opt/side/bravesoul-game/docs/art/verification_crop_ears.png`
   - 武器放大切片（1000×1400）：`/opt/side/bravesoul-game/docs/art/verification_crop_weapon.png`
   - 128px 縮圖切片（61×128）：`/opt/side/bravesoul-game/docs/art/verification_thumb_128px.png`

---

## 六、 後續工序（待老周確認核准後執行）

1. **老周 Review 核准**：確認草圖構圖、色彩、內耳金屬分片（第 2h 條）與單手長劍規格（第 9/9a 條）符合品牌定調。
2. **正式入庫與同步（核准後第二階段）**：
   - 覆蓋 `branding/char_rabbit.png`（400×840）
   - 覆蓋 `web/media/hero/char_rabbit.png`（400×840）
   - 產出遊戲內所需之透明底 Sprite 姿態（`game/assets/sprites/player/poses/idle.png` 等，尺寸 128×128 RGBA）
3. **交由阿宏（sideworker）接上 UI 替換，小婷（sideqa）驗證實機大廳截圖**。
