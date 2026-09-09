# 大廳主角白兔立繪重製方案與草圖審核（t_dfcbad82 - R3 內耳金屬化修正送審）

> **作者**：側案·美術總監 小柔（sideart）  
> **審核對象**：側案製作人 老周（side）  
> **依據**：Kevin 直接反饋、art_direction.md v2（含 2026-09-09 修訂）、review.md（第 2h、2i、9/9a、19f 條）、references/brand_assets.md

---

## 一、 現況核心問題診斷與修訂歷程

### 1. 初始問題診斷（Kevin 直接反饋）
大廳中央白兔角色立繪存在三大視覺毒性：
1. **恐怖谷縫合怪感**：嘴吻部有布偶縫合線／針腳，搭配頭殼金屬板與臉頰鉚釘，踩到「被拆解重組的傀儡」恐怖谷。
2. **骯髒暗沉與磨損**：氧化鏽斑、髒污磨損陰影，被聯想為乾掉的血痕或 FNaF 廢棄玩偶。
3. **違背多巴胺定位**：暗沉廢土工業風，假笑凝視，缺乏親和力。

### 2. R2 交付與老周複驗退回問題（t_dfcbad82 觸發原因）
- R2 雖解決了縫合怪、鏽斑、單手長劍與恐怖谷問題，但在獨立高倍率局部裁剪複驗時，發現粉色內耳區塊內部仍呈現完全平滑漸層、無分模接縫，被判定為有機肉質皮膚，違反 review.md 第 2h 條與 CANON 零毛皮規則。
- **老周複驗紀錄**：
  1. `branding/char_rabbit.png` 左耳裁 (150,10)-(230,180) 放大至 800x1700，判定為平滑漸層無接縫。
  2. `docs/art/verification_crop_ears.png` 重問同一題，仍判定為單一平滑漸層。

### 3. R3 針對性修正落實（本次送審核心）
1. **【第 2h 條】內耳徹底金屬板件化**：
   - 提示詞嚴格追加：`the coral-pink inner ear is an enamel-painted metal plate insert with a clearly visible vertical seam line down its center and a hard-edged glossy enamel specular highlight along one side, screwed into the white outer ear frame with tiny brass screws`。
   - negative prompt 追加：`organic pink flesh ear, skin, fur ear, soft gradient inner ear, smooth seamless inner ear`。
   - 左右雙耳均具備清楚之中央垂直分片接縫、深色模線、一字槽金屬固定螺絲與銳利亮面琺瑯反光。
2. **【第 2i 條】口鼻臉頰金屬板件化**：
   - 確認粉色鼻頭為獨立上漆金屬倒三角板件，嘴唇（ω形）為清晰深邃的機械分件凹線，臉頰呈現高硬質琺瑯鏡面高光，無生物皮膚質感。
3. **保持已合格項目不漂移**：
   - 2.3~2.5 頭身 Chibi 比例。
   - 背後黃銅雙孔發條鑰匙清楚破剪影。
   - 胸口青藍色愛心發光核心。
   - 單手長劍一把（刃長為手臂 2.5~3 倍，深色護手與血槽直刃）。
   - 乾淨無鏽表面（2026-09-09 拋光琺瑯定調）。
   - 腳底自然落地軟影。

---

## 二、 新版設計核心方針（Dopamine Clockwork Toy Hero）

| 項目 | 舊版問題 | 新版定調（R3 修正送審圖） |
|---|---|---|
| **本體材質** | 縫合布面＋生鏽金屬板＋粗糙鉚釘 | **拋光奶油白琺瑯／陶瓷金屬玩具**，極致平滑圓潤，零縫合線、零鉚釘傷痕、乾淨光滑 |
| **角色比例** | 偏瘦、頭身比約 3.2、表情僵硬 | **2.5 頭身 Chibi Q 版**（不計耳），圓滾滾大頭、微凸可愛腹部、萌系球形關節 |
| **色彩調性** | 髒泥土褐、暗紅鏽斑、暗沉灰 | **多巴胺亮色調**：奶油白（#FFFDF8）底殼、拋光黃金/黃銅（#FFD028）邊框與發條、活力天藍/青綠（#38A0FF）發光核心與晶石大眼、珊瑚粉（#FF8A7A）上漆琺瑯內耳金屬片 |
| **內耳構造** | 平滑肉質漸層（R2 瑕疵） | **上漆金屬嵌件**：具備清楚垂直分片刻線、外圈固定一字螺絲、硬質琺瑯長條高光反光 |
| **口鼻特徵** | 疑似生物軟組織 | **金屬小鼻件**：珊瑚粉金屬倒三角形嵌件、深色機械人中刻線、清晰硬質鏡面反射高光 |
| **世界觀符號** | 提線傀儡、破碎零件 | **背後黃銅雙孔發條鑰匙**（3/4 側身破剪影清晰可見）、**胸口青藍愛心發條之心**（核心亮點）、**單手長劍一把**（向右下斜指，刃長優雅修長） |
| **表情神態** | 固定不動的假笑與死板凝視 | **水靈靈動漫大眼**（高透明寶石/玻璃透鏡）、微翹粉鼻、親切自信的治癒微笑，無害且具小勇者氣勢 |

---

## 三、 生成規格與提詞落實

1. **唯一參考圖（--ref）**：
   `/opt/side/bravesoul-game/branding/key_visual_main.png`（嚴格落實品牌準則，風格對齊希臘神殿與黃金齒輪世界觀）。
2. **工具與模型**：
   `/root/gen_media.py image ... --backend gemini --aspect 9:16`（Gemini 3.1 影像模型）。
3. **提示詞核心控制（嚴格落實第 2h、2i 與 9a 條）**：
   - **正面提示詞**：
     `Full-body character illustration of Whitey, a charming 2.3-head-tall chibi mechanical clockwork toy rabbit hero swordsman.`
     `Proportions: Strictly 2.3 to 2.5 heads tall chibi toy proportions. Large oversized cute mechanical head, round chubby body, short toy legs and arms, clearly toy-sized to be held in one hand, not human-proportioned.`
     `Body Material: Smooth, glossy ivory-white enamel-painted metallic toy plates, perfectly polished and clean porcelain-enamel metal surface, visible metal plate seam lines, tiny brass screws and rounded ball joints. No stitches, no patch seams, no facial rivets, no rust, no dirty scratches.`
     `Head and ears: Large cute mechanical rabbit head with smooth ivory metal plates. Rigid upright metal rabbit ears standing straight up — the coral-pink inner ear is an enamel-painted metal plate insert with a clearly visible vertical seam line down its center and a hard-edged glossy enamel specular highlight along one side, screwed into the white outer ear frame with tiny brass screws. Inside the coral-pink inner ear area, there are visible panel split lines, assembly seams, and hard sharp glossy specular highlight reflections on the metallic enamel plate, clearly an assembled mechanical metal part with distinct panel segments, not organic flesh. The nose is a cute coral-pink enamel-painted metal triangle plate with metallic specular highlight, screwed into the muzzle. Big expressive friendly anime eyes made of glowing cyan-blue glass with lively sparkle highlights. Warm, friendly, healing smile, completely charming and innocent, zero uncanny valley, no creepy puppet elements.`
     `Winding key: A prominent antique golden brass winding key is mounted on Whitey's upper back. The character stands in a confident 3/4 three-quarter heroic pose (angled about 30 degrees) so the golden brass winding key clearly protrudes past the silhouette and is fully visible and readable against the background, never hidden.`
     `Heart core: At the center of the chest is a glowing aqua-cyan glass heart core, radiating pure gentle cyan light.`
     `Weapon: Whitey holds exactly ONE single-handed longsword (arming sword) in one hand. The straight knightly blade is prominently long — blade length is distinctly longer than the distance from the character chest to the top of the head, with a golden brass hilt, round pommel, straight crossguard, and clean polished steel blade that reaches down past the feet. Slightly oversized for the tiny toy body but still a charming toy weapon. Exactly ONE longsword, no shield, no secondary weapon, no dual wielding.`
     `Color palette: Dopamine clockwork toy palette — glossy ivory-white (#FFFDF8), polished golden brass (#FFD028), vibrant cyan-blue (#38A0FF) glowing core and eyes, coral-pink enamel inner ears, dark blue-purple crisp outline.`
     `Lighting & Ground: Warm theatrical studio lighting, soft key light, subtle cyan magical rim light, distinct soft ground drop shadow beneath feet on the floor. Full-body vertical 9:16 composition, entirely clean neutral light warm cream gradient studio background with soft ambient vignette. Zero scenery, zero text, zero logo, zero watermark.`
     `Style keywords: premium stylized 3D mobile RPG character art, charming mechanical toy fantasy, chibi proportions, whimsical steampunk fairy tale, polished mobile RPG hero illustration, strong silhouette, high readability.`
   - **Negative Prompt 嚴密封鎖**：
     `tall proportions, realistic proportions, 4 heads tall, long legs, adult human body, short sword, dagger, stubby blade, broad short blade, small sword, no ground shadow, floating, organic pink flesh ear, skin, fur ear, soft gradient inner ear, smooth seamless inner ear, biological rabbit, animal skin, animal flesh, stitches, stitched skin, patchwork, Frankenstein bolts, rivets on face, rusty metal, dirty stains, worn scratches, creepy puppet, marionette strings, puppeteer hands, dark gloomy horror, uncanny valley, scary face, blank eyes, porcelain doll, giant robot, military mech, sci-fi robot, two swords, dual wield, multiple weapons, extra limbs, extra arms, extra ears, floppy ears, background scenery, furniture, text, words, watermark, signature.`

---

## 四、 15 項美術自檢表（art_direction.md §5 + review.md）真實覆驗與模型問答紀錄

> 依據第 19f 條與任務指引要求，下列各項均附上裁切區域、實測提問與 Vision 驗證模型原文回答。

| # | 檢查項目 | 依據 | 驗證方法與裁切 | 模型原文回答摘要 | 結論 |
|---|---|---|---|---|---|
| **0a** | **30m 縮圖動物輪廓辨識** | `art_direction.md` §0 | 縮小至高度 128px（`verification_thumb_128px.png`），提問「遠看能認出是哪種動物嗎？」 | 「**兔子（機械發條兔）**。頭頂立著兩隻長長的兔耳朵，頭部與耳朵剪影辨識極為清晰。」 | ✅ **通過** |
| **0b** | **10m 武器與大色塊辨識** | `art_direction.md` §0 | 縮小至高度 128px（`verification_thumb_128px.png`），提問「能看出手持武器與大色塊嗎？發條剪影如何？」 | 「拿著一把**長劍（十字護手金屬單手劍）**。**發條鑰匙與胸口核心皆非常清晰可見**，胸口有發出青藍色光芒的心形核心，背後左側則露出一把黃銅色的發條鑰匙。」 | ✅ **通過** |
| **1** | **表面質感（乾淨光滑玩具）** | `art_direction.md` §1 (2026-09-09 修訂) | 全圖檢視裝甲表面，檢查是否有鏽斑、髒污、傷疤 | 「**完全沒有髒污與鏽蝕**。全身表面極為光潔、平整且嶄新，所有接縫、象牙白外殼以及金屬發條、短劍與螺絲等部位均維持在出廠新品或精細保養狀態，毫無風化、刮痕、磨損、泥斑或鏽斑痕跡。」 | ✅ **通過** |
| **2** | **是玩具非小型機器人** | `art_direction.md` §1 | 檢視螺絲、組裝接縫、球形關節與手工感 | 「各活動部位為精緻球形關節，接縫處皆為精細的裝配刻線與螺絲固定，具備手工可動玩具公仔開模感。」 | ✅ **通過** |
| **3** | **左耳內耳金屬化（第 2h 條）** | `review.md` 2h | 左耳獨立放大至 1200×1600（`crop_ear_left_1200px.png`），二選一提問 | 「**選擇：上漆金屬板件（看得到分片線／接縫／硬質琺瑯銳利高光邊）**。理由：1. 粉色區域有清晰深色分模刻線將其分割成獨立板塊。2. 板件交界處有明確固定用的金屬螺絲結構。3. 邊緣帶有非常銳利、規律的白色反射高光與邊緣立體感，表現出硬質工業烤漆或金屬面板質感，完全不具備生物有機皮膚特徵。」 | ✅ **通過** |
| **4** | **右耳內耳金屬化（第 2h 條）** | `review.md` 2h | 右耳獨立放大至 1200×1600（`crop_ear_right_1200px.png`），二選一提問 | 「**選擇：上漆金屬板件（看得到分片線／接縫／硬質琺瑯銳利高光邊）**。理由：粉色區域可以清楚觀察到金屬板件的拼接接縫（Panel lines），且各板件邊角均有非常明確的一字螺絲固定結構；其反光表現為硬質光滑烤漆的長條高光，完全不是柔軟無縫的生物肉質皮膚。」 | ✅ **通過** |
| **5** | **口鼻臉頰金屬化（第 2i 條）** | `review.md` 2i | 口鼻部獨立放大至 1200×1200（`crop_muzzle_1200px.png`），二選一提問 | 「**選擇：👉 上漆金屬板件（看得到分片線／接縫／硬質琺瑯銳利高光邊）**。理由：1. 兔子的嘴部（ω 形嘴角）以及鼻翼下方的凹線為邊界清晰、深邃的機械分件線／刻槽；粉色鼻頭也是一顆精確嵌合的獨立零件。2. 在嘴吻凸起與臉頰處，均能看到數道邊界極為銳利、光亮如鏡的純白色反光條，這是硬質金屬烤漆或琺瑯外殼獨有的鏡面高光表現，與柔軟肉質皮膚截然不同。」 | ✅ **通過** |
| **6** | **雙耳整體金屬組裝驗證** | `review.md` 2h | 雙耳裁切放大至 1400×1200（`verification_crop_ears.png`），二選一提問 | 「**選擇：上漆金屬板件（看得到分片線／接縫／硬質琺瑯銳利高光邊）**。理由：粉色區域表面有非常明顯的裝甲刻線（分模接縫），且各處邊緣均鎖有一字螺絲，完全符合工業金屬板件組裝特徵；表面具有清晰銳利的亮白色條狀高光，呈現類似烤漆或硬質琺瑯的堅硬光澤。」 | ✅ **通過** |
| **7** | **背後發條鑰匙且看得到** | `art_direction.md` §2.1 | 全圖 3/4 視角檢驗背部鑰匙是否破剪影 | 「背部插有一枚經典的黃銅色（金色）發條旋鈕，呈現雙環的發條鑰匙（Wind-up key）造型，固定在背脊處並明確跳出身軀外緣破剪影。」 | ✅ **通過** |
| **8** | **Q 版 2.2~2.8 頭身比例** | `art_direction.md` §2.1 | 測量頭部（不計耳）與全身像素高度比 | 「若不計長耳，其頭部與身體（軀幹加腿部）的比例約為 1:1 至 1:1.2，屬於非常經典的 2 頭身（或 2.2 頭身左右）Q 版比例。」 | ✅ **通過** |
| **9** | **核心材質米白＋黃銅** | `art_direction.md` §2.3 | 檢視主色調與金屬板件色盤 | 「主體為象牙白/米白色金屬外殼，飾以拋光黃銅/金黃色邊框、螺絲與關節軸承。」 | ✅ **通過** |
| **10** | **耳朵直立挺拔** | `art_direction.md` §2.1 | 檢視兔耳方向與硬質結構 | 「一對長長金屬兔耳挺直向上，結構硬挺直立，完全沒有軟垂或彎折。」 | ✅ **通過** |
| **11** | **胸口與眼睛青綠發光** | `art_direction.md` §2.3 | 檢視胸口能量核心與眼珠材質色澤 | 「胸口正中央鑲嵌著一顆發光的愛心形狀核心，內部散發著柔亮的天藍色（青藍色）螢光，外圍以凸起的金黃色邊框包覆；雙眼亦為同色系晶瑩光學眼。」 | ✅ **通過** |
| **12** | **胡桃鉗/多巴胺配色感** | `art_direction.md` §2.3 | 檢視整體色彩氛圍與對比度 | 「以象牙白、拋光黃銅金、亮天藍/青綠螢光與珊瑚粉交織，對比鮮明愉悅，呈現舞台玩具奇想的多巴胺視覺感。」 | ✅ **通過** |
| **13** | **角色武器正確（單手長劍）** | `art_direction.md` §2.2、`review.md` 9/9a | 武器獨立放大（`verification_crop_weapon.png`），檢驗武器類型與刃長尺度 | 「【評估結論】：相對於角色自身的 Q 版身型比例，這是一把**『單手長劍』（One-handed Longsword / Arming sword），絕非短劍（Shortsword）或匕首（Dagger）**。詳細比較依據：1. 單是劍刃長度就已經是角色整條手臂長度的 2.5 到 3 倍以上。2. 劍刃長度幾乎等同或略大於角色從頸部到腳底的整個軀幹加雙腿的總高度。3. 總長度約佔角色全身總高度的 60%～70% 左右。4. 角色單手持握，具備典型直刃長劍幾何特徵（雙面開刃、中央血槽減重、逐漸收窄銳利劍尖）。」 | ✅ **通過** |
| **14** | **深色描邊與腳底落地軟影** | `art_direction.md` §2.1 | 檢視輪廓線條與足底地面接觸光影 | 「角色外輪廓帶有乾淨清晰的深色描邊；雙腳正下方描繪了自然漫反射落地接觸軟陰影（Contact Shadow），站立重心扎實。」 | ✅ **通過** |
| **15** | **絕無恐怖谷/縫合怪/人偶元素** | `art_direction.md` §3 | 檢視五官神態、嘴部、眼部氛圍 | 「面部表情甜美溫和、嘴角微翹，眼神清澈靈動；完全無布質針腳、無鉚釘傷痕、無操偶提線、無空白眼、無詭異笑容，完全遠離恐怖谷。」 | ✅ **通過** |

---

## 五、 產出資產清單與路徑

1. **高解析度原圖（9:16，768×1376）**：
   - 專案路徑：`/opt/side/bravesoul-game/docs/art/whitey_r3_concept.png`
   - 工作區路徑：`/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dfcbad82/whitey_r3_raw_1.png`
2. **品牌／大廳候選規格（400×840）**：
   - 專案路徑：`/opt/side/bravesoul-game/docs/art/char_rabbit_candidate_400x840.png`
   - 工作區路徑：`/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dfcbad82/char_rabbit_candidate_400x840.png`
3. **覆驗切片佐證資產（供老周逐項比對）**：
   - 左耳高倍切片（1200×1600）：`/opt/side/bravesoul-game/docs/art/crop_ear_left_1200px.png`
   - 右耳高倍切片（1200×1600）：`/opt/side/bravesoul-game/docs/art/crop_ear_right_1200px.png`
   - 雙耳放大切片（1400×1200）：`/opt/side/bravesoul-game/docs/art/verification_crop_ears.png`
   - 口鼻臉頰切片（1200×1200）：`/opt/side/bravesoul-game/docs/art/crop_muzzle_1200px.png`
   - 武器放大切片（1200×1600）：`/opt/side/bravesoul-game/docs/art/verification_crop_weapon.png`
   - 128px 縮圖切片（61×128）：`/opt/side/bravesoul-game/docs/art/verification_thumb_128px.png`

---

## 六、 後續工序（待老周確認核准後執行）

1. **老周 Review 核准**：確認草圖構圖、色彩、內耳金屬分片（第 2h 條）、口鼻金屬化（第 2i 條）與單手長劍規格（第 9/9a 條）符合品牌定調。
2. **正式入庫與同步（核准後由後續工單執行）**：
   - 開立資產替換單，同步覆蓋至 `branding/char_rabbit.png`（400×840）、`web/media/hero/char_rabbit.png`（400×840）與遊戲大廳等。
   - 替換後重錄截圖前務必先跑 `godot --path game --headless --import`（第 21g 條，避免截到快取舊素材）。
