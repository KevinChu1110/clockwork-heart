# 八族紙娃娃套件比照兔族三項瑕疵模式複檢報告（2026-09-18）

依據 Kanban 任務 `t_6735af1a` 與審查規範（`review.md` 0-ART28h、0-QA9），針對獅／狐／豬／猴／虎／鶴／熊／企鵝 8 族紙娃娃，比照 `docs/art/RABBIT_PAPERDOLL_REVIEW_2026-09-18.md` 發現之三項結構性瑕疵進行實機換裝複檢。

---

## 複檢方法與標準

1. **實機截圖存證**：
   - 透過 Godot 引擎（`xvfb-run -a godot --rendering-driver opengl3`）呼叫 `MobileLobby` 與 `WardrobeDialog`，對 8 族所有外裝（含裸機素體 none）× 所有塗裝共 69 種組合逐一實機截圖（1280×720 全景與 250×420 角色特寫裁切）。
   - 各族獨立產出一張全套件對照矩陣圖（`proof_wardrobe_matrix_<race>.png`），直觀呈現所有換裝與塗裝組合。
2. **0-QA9 數值量測**：
   - 逐層讀取 PNG 切片，使用 PIL 與 NumPy 計算最大不透明主色（忽略邊界線）、明度公式（`0.299*R + 0.587*G + 0.114*B`）與 RGB 歐氏距離。
   - 檢測領口水平切線：量測胸頸交界區域中心（X: 200~312）頂部不透明像素的 Y 座標離散度（variance、span）。
3. **Vision 多模態獨立覆核**：
   - 逐張送入視覺模型檢驗外裝厚度層次、領口曲線特徵與頭身塗裝色差。

---

## 總結盤點

| 種族 | 瑕疵 1：外裝過薄（穿了像沒穿） | 瑕疵 2：領口筆直水平切線 | 瑕疵 3：耳朵/頭部與身體塗裝色偏 | 總評 |
|---|---|---|---|---|
| **烈鬃獅 (Lion)** | ⚠️ **胡桃鉗**厚度不足（與素體高度重疊） | ⚠️ 領口與素體銜接微縫、橫切生硬 | ❌ **象牙/深藍**塗裝殘留黃金鬃毛 | 2 項瑕疵、1 項色偏 |
| **靈尾狐 (Fox)** | ✅ 通過（斗篷/儀裝輪廓明顯） | ✅ 通過（具圓弧貼合曲線） | ❌ **象牙/翡翠**塗裝殘留曜橙雷達耳 | 1 項色偏 |
| **鋼牙豕 (Boar)** | ✅ 通過（鍛鐵束帶/板甲層次足） | ⚠️ **鐵束帶**下巴領口偏平直生硬 | ❌ **赤焰**塗裝殘留生鐵灰頭罩 | 1 項微瑕、1 項色偏 |
| **靈爪猴 (Macaque)** | ✅ 通過（短褂斜襟/機關甲外擴） | ✅ 通過（斜襟交疊自然） | ❌ **青古銅**塗裝頭部未跟隨青金化 | 1 項色偏 |
| **烈焰虎 (Tiger)** | ✅ 通過（戰褂/夜行裝輪廓明顯） | ✅ 通過（微 V 領斜切自然） | ❌ **曜黑/象牙**塗裝殘留橙紅虎頭耳 | 1 項色偏 |
| **雲嵐鶴 (Crane)** | ✅ 通過（道袍飄逸/羽甲層次足） | ✅ 通過（交領與階梯倒角自然） | ⚠️ **湛藍**塗裝頭頸為純白（白鶴特徵） | 1 項色相落差 |
| **玄軸熊 (Bear)** | ✅ 通過（吊帶甲與戰鎧層次足） | ❌ **狂戰戰鎧**領口為筆直水平切線（Y=216, var=0.0） | ❌ **玄鐵灰/象牙**塗裝殘留琥珀棕耳 | 1 項嚴重瑕疵、1 項色偏 |
| **蒸氣企鵝 (Penguin)** | ⚠️ **導航員大衣**厚度偏弱（無外擴） | ❌ **深潛機關鎧**領口為筆直水平切線（Y=192, var=0.0） | ❌ **銀白/象牙**塗裝殘留深海藍頭 | 2 項瑕疵、1 項色偏 |

- **全 8 族均檢出瑕疵 3（頭部/耳朵未隨塗裝同步換色）**：切片目錄與 `paperdoll_renderer.gd` 僅兔族具備 midnight/brass 分流，其餘 8 族均只有一套 stock 預設頭部，切換塗裝時頭身色差嚴重脫節（明度差達 45~194）。
- **2 族檢出嚴重瑕疵 2（領口筆直水平切線）**：玄軸熊狂戰戰鎧、蒸氣企鵝深潛機關鎧在下巴正下方呈現完全水平直線切口（Y 座標變異度為 0.00）。
- **2 族檢出瑕疵 1（外裝層次不足穿了像沒穿）**：烈鬃獅胡桃鉗軍裝、蒸氣企鵝導航員大衣與裸機素體高度重合，剪影幾乎無外擴。

---

## 八族複檢逐項對照表（依 review.md 0-ART28h 規範）

| 種族 | 套別 | 檢查項 | 證據截圖路徑 | 通過或現象描述 |
|---|---|---|---|---|
| **烈鬃獅** | 胡桃鉗近衛軍裝 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/lion/crop_lion_nutcracker_guard_brass_gold.png` | ⚠️ **不合格（偏薄）**：金屬胸甲與素體重疊過高，缺乏外擴布料/肩章輪廓，與裸機對比差異極小。 |
| **烈鬃獅** | 蒸氣工匠吊帶裝 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/lion/crop_lion_steam_artisan_brass_gold.png` | ✅ **通過**：深色吊帶裙與口袋結構明確，外輪廓與素體有清晰區隔。 |
| **烈鬃獅** | 兩款外裝 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/lion/wardrobe_lion_nutcracker_guard_brass_gold.png` | ⚠️ **局部瑕疵**：領口與素體頸部接合處呈現水平橫切，局部有微小白線斷層縫隙。 |
| **烈鬃獅** | 原廠象牙白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_lion_mane_colors.png` | ❌ **不合格**：鬃毛與耳朵依然為黃銅色 (77, 30, 15)，與象牙白身體 (229, 223, 212) 明度差 181.2，嚴重脫節。 |
| **烈鬃獅** | 午夜深藍塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_lion_mane_colors.png` | ❌ **不合格**：黃金鬃毛配深藍身 (35, 45, 70)，色距 70.8，頭部未跟隨換色。 |
| **靈尾狐** | 星紋見習斗篷 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/fox/crop_fox_astral_cape_fox_orange.png` | ✅ **通過**：深藍披肩與肩甲剪影外擴顯著，層次分明。 |
| **靈尾狐** | 星象觀測者儀裝 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/fox/crop_fox_astral_observer_fox_orange.png` | ✅ **通過**：金色胸前觀測儀器體積明顯，非光潔素體。 |
| **靈尾狐** | 兩款外裝 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/fox/crop_fox_astral_cape_fox_orange.png` | ✅ **通過**：斗篷呈圓弧貼合曲線，儀裝具備金屬立體護頸邊框，無筆直切線。 |
| **靈尾狐** | 原廠象牙白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_fox_ear_colors.png` | ❌ **不合格**：雷達耳仍為曜橙色 (255, 168, 89)，與象牙白身體 (254, 244, 220) 色距 151.5、明度差 59.2。 |
| **靈尾狐** | 翡翠螢光釉面 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_fox_ear_colors.png` | ❌ **不合格**：曜橙耳配翠綠身體 (183, 255, 225)，色距 176.8，完全未跟隨綠化。 |
| **鋼牙豕** | 粗獷鍛爐鐵束帶 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/boar/crop_boar_viking_harness_brass_gold.png` | ✅ **通過**：十字型皮件、中央圓盤扣件與鉚釘層次立體。 |
| **鋼牙豕** | 維京重裝鍛鐵板甲 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/boar/crop_boar_viking_ironclad_brass_gold.png` | ✅ **通過**：大面積鍛鐵胸甲與雙列鉚釘肩甲，輪廓厚實。 |
| **鋼牙豕** | 粗獷鍛爐鐵束帶 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/boar/crop_boar_viking_harness_brass_gold.png` | ⚠️ **局部瑕疵**：下巴正下方領口金屬橫切線略生硬，但兩側有皮帶斜度延伸。 |
| **鋼牙豕** | 赤焰熔爐塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_boar_cowl_colors.png` | ❌ **不合格**：頭罩仍為生鐵灰 (45, 57, 80)，與赤紅身體 (246, 160, 82) 色距 225.9、明度差 120.8。 |
| **靈爪猴** | 晨曦行者武道短褂 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/macaque/crop_macaque_dawn_monk_tunic_ivory_stock.png` | ✅ **通過**：紅色布料厚度、斜襟滾邊與腰帶束繩立體分明。 |
| **靈爪猴** | 天元演武者機關甲 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/macaque/crop_macaque_zen_striker_ivory_stock.png` | ✅ **通過**：外擴榫卯板件與鎖甲結構，剪影差異顯著。 |
| **靈爪猴** | 兩款外裝 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/macaque/crop_macaque_dawn_monk_tunic_ivory_stock.png` | ✅ **通過**：短褂為斜襟交疊，機關甲為微傾倒梯形，無筆直水平橫切。 |
| **靈爪猴** | 天元青古銅塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/macaque/crop_macaque_none_bamboo_bronze.png` | ❌ **不合格**：身體轉為金黃青銅 (219, 171, 67)，同軸金屬耳仍為暗褐 (119, 74, 41)，明度差 89.8。 |
| **烈焰虎** | 餘燼工匠淬火戰褂 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/tiger/crop_tiger_ember_tunic_ember_orange.png` | ✅ **通過**：下擺皮帶扣環與多層布料剪影明顯。 |
| **烈焰虎** | 灰燼夜行機關裝 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/tiger/crop_tiger_ash_ninja_garb_ember_orange.png` | ✅ **通過**：金邊鑲飾與擴展肩腰輪廓，覆蓋感充實。 |
| **烈焰虎** | 兩款外裝 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/tiger/crop_tiger_ember_tunic_ember_orange.png` | ✅ **通過**：微 V 領與菱形飾物收口，無筆直水平切線。 |
| **烈焰虎** | 鍛爐淬火曜黑 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_tiger_ear_colors.png` | ❌ **不合格**：頭部與虎耳仍為橙紅 (120, 28, 8)，與曜黑軀幹 (44, 39, 60) 色距 92.7，形成紅頭黑身。 |
| **烈焰虎** | 原廠象牙白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_tiger_ear_colors.png` | ❌ **不合格**：頭部與虎耳仍為橙紅，與象牙白軀幹 (160, 152, 142) 色距 186.9、明度差 100.0。 |
| **雲嵐鶴** | 凌雲羽衣輕鋼道袍 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/crane/crop_crane_zephyr_robe_crane_porcelain.png` | ✅ **通過**：下擺與腰封束帶立體飄逸，非單薄素體。 |
| **雲嵐鶴** | 晴空巡獵機關羽甲 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/crane/crop_crane_sky_hunter_mail_crane_porcelain.png` | ✅ **通過**：階梯狀羽甲與肩部導風板件，輪廓外擴顯著。 |
| **雲嵐鶴** | 兩款外裝 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/crane/crop_crane_zephyr_robe_crane_porcelain.png` | ✅ **通過**：道袍採交領設計，羽甲具倒角過渡，無筆直水平切線。 |
| **雲嵐鶴** | 晴空凌雲湛藍 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/crane/crop_crane_none_zephyr_azure.png` | ⚠️ **局部色偏**：頭部維持白瓷白 (237, 242, 248)，軀幹為深湛藍，雖具白鶴生物特徵但機甲配色斷層。 |
| **玄軸熊** | 玄軸工坊吊帶甲 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/bear/crop_bear_ironclad_overalls_bear_amber.png` | ✅ **通過**：皮革繫帶、金屬搭扣與腰側掛包層次分明。 |
| **玄軸熊** | 狂戰破陣機關戰鎧 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/bear/crop_bear_berserker_cuirass_bear_amber.png` | ✅ **通過**：酒紅胸甲、厚重護肩與裙甲體積感充實。 |
| **玄軸熊** | 狂戰破陣機關戰鎧 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/details/detail_bear_neckline_comparison.png` | ❌ **嚴重不合格**：下巴正下方領口（Y=216, span=0, var=0.00）呈現完全筆直水平橫切線，缺乏弧度。 |
| **玄軸熊** | 重裝礦山玄鐵灰 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/bear/crop_bear_none_iron_quarry.png` | ❌ **不合格**：頭耳維持琥珀黃銅，與玄鐵灰軀幹 (48, 62, 86) 色距 329.6、明度差 194.4。 |
| **玄軸熊** | 原廠象牙白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/bear/crop_bear_none_ivory_stock.png` | ❌ **不合格**：頭耳維持琥珀黃銅，與象牙白軀幹 (185, 170, 148) 色距 153.5、明度差 83.0。 |
| **蒸氣企鵝** | 深海導航員大衣 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/penguin/crop_penguin_navigator_harness_penguin_navy.png` | ⚠️ **不合格（偏薄）**：剪影與素體高度一致，僅腹部增添暗紋與金色線條，缺乏大衣立體外擴厚度。 |
| **蒸氣企鵝** | 淵海深潛耐壓機關鎧 | 瑕疵 1（外裝厚度） | `proofs/eight_races_paperdoll_review/penguin/crop_penguin_abyssal_diver_cuirass_penguin_navy.png` | ✅ **通過**：厚重深藍胸甲、肩甲鉸鏈閥與核心反應爐輪廓分明。 |
| **蒸氣企鵝** | 淵海深潛耐壓機關鎧 | 瑕疵 2（領口弧度） | `proofs/eight_races_paperdoll_review/details/detail_penguin_neckline_comparison.png` | ❌ **嚴重不合格**：鳥喙下巴正下方（Y=192, span=0, var=0.00）為一條完全筆直的金色水平金屬橫切線。 |
| **蒸氣企鵝** | 極光冰川銀白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_penguin_head_colors.png` | ❌ **不合格**：頭部仍為深海藍 (49, 70, 115)，與銀白軀幹 (255, 255, 255) 色距 310.3、明度差 186.1。 |
| **蒸氣企鵝** | 原廠象牙白塗裝 | 瑕疵 3（耳身配色） | `proofs/eight_races_paperdoll_review/details/detail_penguin_head_colors.png` | ❌ **不合格**：頭部仍為深海藍，與象牙白軀幹 (235, 226, 210) 色距 260.7、明度差 158.0。 |

---

## 具體待修現象描述（供後續開卡直接對著改）

依據任務指示第 3 點：**「若某族真的有問題，只記錄現象，⛔ 不要自己動手改素材——這單是複檢盤點，不是修復單，修復另開卡分派給對應總監。」**

### 1. 領口筆直水平切線修復（優先級：高）
- **玄軸熊·狂戰破陣機關戰鎧 (`costume_berserker_cuirass_512.png`)**：
  - 現象：Y=216 的頂部金色/深灰金屬護頸邊緣為絕對筆直水平直線，橫跨胸頸寬度 25px 以上。
  - 修復要求：將中心領口改為順應頸部與圓拱核心下沉的 U 型微弧度（V 型或倒圓角均可），不可為水平直角切片。
- **蒸氣企鵝·淵海深潛耐壓機關鎧 (`costume_abyssal_diver_cuirass_512.png`)**：
  - 現象：Y=192 的頂部金色金屬邊緣為絕對筆直水平直線，直接頂在企鵝鳥喙下巴底端。
  - 修復要求：將領口金屬封邊改為向下略微弧形收邊，配合圓形胸頸生理過渡。

### 2. 外裝過薄穿了像沒穿修復（優先級：中）
- **烈鬃獅·胡桃鉗近衛軍裝 (`costume_nutcracker_guard_512.png`)**：
  - 現象：金屬胸甲與素體緊密貼合，無布料外擴剪影，視覺上難以一眼辨認是否著裝。
  - 修復要求：增加肩章、雙排扣紅藍禮服的布料厚度與外擴輪廓，確保與無外裝並排時一眼可辨。
- **蒸氣企鵝·深海導航員大衣 (`costume_navigator_harness_512.png`)**：
  - 現象：大衣僅以金色羅盤線條貼於腹部，兩側無大衣翻領或厚質風衣下擺。
  - 修復要求：增添立體大衣翻領、肩章或向外延伸的深色風衣下擺剪影。

### 3. 頭部/耳朵塗裝同步缺失（系統性切片架構修復，優先級：高）
- 現象：所有 8 族在 `assets/sprites/player/paperdoll/<race>/head_unit/` 目錄下均僅有單一 `_stock_512.png`，缺乏塗裝變體切片；`paperdoll_renderer.gd` 亦僅有兔族 `midnight` / `brass` 的耳部分流邏輯。
- 修復要求：
  - 為獅、狐、豬、猴、虎、鶴、熊、企鵝補齊對應塗裝之 `head_unit` 切片（如狐補 ivory/emerald 耳、虎補 black/ivory 頭耳、企鵝補 polar/ivory 頭部等）。
  - 在 `paperdoll_renderer.gd` 的 `resolve_slot_texture_path_512` 擴展八族頭耳塗裝解析邏輯。

---

## 存證檔案清單

- **八族對照矩陣圖**：
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_lion.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_fox.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_boar.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_macaque.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_tiger.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_crane.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_bear.png`
  - `proofs/eight_races_paperdoll_review/proof_wardrobe_matrix_penguin.png`
- **特寫對照條**：
  - `proofs/eight_races_paperdoll_review/details/detail_bear_neckline_comparison.png`
  - `proofs/eight_races_paperdoll_review/details/detail_penguin_neckline_comparison.png`
  - `proofs/eight_races_paperdoll_review/details/detail_fox_ear_colors.png`
  - `proofs/eight_races_paperdoll_review/details/detail_lion_mane_colors.png`
  - `proofs/eight_races_paperdoll_review/details/detail_boar_cowl_colors.png`
  - `proofs/eight_races_paperdoll_review/details/detail_tiger_ear_colors.png`
  - `proofs/eight_races_paperdoll_review/details/detail_penguin_head_colors.png`
- **全套 69 組實機換裝截圖與特寫**：存放於 `proofs/eight_races_paperdoll_review/<race>/` 目錄下。
