# 大廳 UI 視覺重製設計方案（希臘神殿石柱 × 黑曜石底色 × 黃金齒輪）

> **文件狀態**：設計提案（只產設計方案與示意圖，不改動 `mobile_lobby.gd` 程式碼）  
> **對齊標準**：`docs/ART_DIRECTION.md`（v2 手機優先、破舊機械玩具、神殿構圖）、`web/css/temple.css`（官網定調色碼）  
> **驗證示意圖**：`docs/lobby_ui_redesign_concept.png`（附 Vision 分析報告與 15 項自檢表）  
> **提案負責**：側案·美術總監 小柔  

---

## 1. 背景與核心問題剖析

在 `t_482c7b06` 驗收與官網視覺審查過程中發現：遊戲內現行大廳 UI（`game/scripts/ui/mobile_lobby.gd`）仍停留在舊版**「多巴胺彩虹吊旗＋Tata Adventure 糖果色」**風格（包括檔案開頭 class 註解、`_build_carnival_buntings` 六色彩旗、`TATA_CARD_BG` 奶油白底卡片與 24px 大果凍圓角）。

這套視覺存在三大致命問題：
1. **世界觀嚴重割裂**：現行官網與核心主視覺已定調為**「希臘神殿石柱、深邃黑曜石底色、古典黃金齒輪、青綠發條之心」**，而大廳卻呈現幼兒向遊樂園糖果風，導致官方網站無法採用實機截圖（先前只能以占位卡替代）。
2. **違背手機優先高對比辨識**：高飽和的草莓粉、活力橘、蜜糖黃與亮白卡片混雜，在小尺寸手機螢幕上邊緣辨識度渙散，缺乏層次感與金屬重量感。
3. **氛圍與角色設定脫節**：主角群是「從廢墟中甦醒、帶有磨損鏽斑的機械發條玩具」，置身於亮麗多巴胺遊樂園彩旗下顯得極其違和，完全抹煞了「被遺忘的古典玩具劇場」之敘事厚度。

本方案旨在**不破壞現行程式邏輯、資料綁定與按鈕熱區（≥48px）**的前提下，提供一套完整的視覺轉換規格與資源重製藍圖。

---

## 2. 美學轉換對照（Before vs After）

| 設計維度 | 現行舊版（Tata 多巴胺糖果風 ⛔） | 重構新版（希臘神殿 × 黑曜石 × 黃金齒輪 ✅） |
|---|---|---|
| **整體氛圍** | 幼兒向慶典、遊樂園、多巴胺糖果色 | 古典玩具劇場、希臘神殿遺跡、神秘機械莊嚴感 |
| **主場景底圖** | 浮空城堡、藍天白雲綠草地（`SkyKingdomBg`） | 希臘神殿凹槽石柱長廊、黑曜石高光地磚、邊緣精密黃金齒輪咬合軸 |
| **裝飾元素** | 頂部六色三角吊旗（`_bunting_flags`）、彩色星芒粒子 | 移除彩旗；引入極微量飄浮的「黃金以太塵埃（Golden Ether Motes）」與青綠齒輪齒隙光暈 |
| **卡片與面板底色** | 溫潤奶油米白（`#FFFDF8`）、溫暖巧克力棕描邊 | 深邃黑曜石（`#0B0A0E` / `#141218`）、古典金細線微光鑲邊（`#D4AF37`） |
| **邊框與圓角規格** | 18~24px 膨脹果凍大圓角、5~6px 果凍厚底邊 | 6~10px 古典神殿倒角／微圓角、1px 金線內嵌、角落帶幾何希臘回紋（Meander）裝飾 |
| **英雄展台底座** | 彩虹漸層光環（草莓粉＋蜜糖黃＋薄荷綠） | 古典黃銅星盤日晷基座（Astrolabe Dial Plinth），黑曜石石板嵌同心刻度環與青綠以太符文 |
| **角色對話氣泡** | 橘邊白底圓角卡通氣泡（「今天也要元氣滿滿出發！」） | 黑曜石底象牙金邊氣泡，文字為象牙白，口吻回歸覺醒玩具冒險者語氣 |
| **文字層次** | 咖啡色字（`TATA_BROWN`）配彩色描邊 | 象牙白主文字（`#F4EBD4`）、柔和象牙次標（`#C9BFA8`）、高對比高抗光性 |

---

## 3. 官方標準色板定義（嚴格沿用現行官網與定調色碼）

嚴格沿用 `web/css/temple.css` 與 `docs/ART_DIRECTION.md` 既定色碼，**不新發明任何顏色**：

```gdscript
## ── 希臘神殿 · 黑曜石 × 古典金標準色盤 (對齊 temple.css) ──
const OBSIDIAN_BASE      := Color(0.043, 0.039, 0.055, 1.0)  ## #0B0A0E：黑曜石最深底色（大廳基底、極致沉浸）
const OBSIDIAN_CARD      := Color(0.078, 0.071, 0.094, 1.0)  ## #141218：黑曜石卡片面色（各 Tab 內容容器底）
const OBSIDIAN_WARM      := Color(0.102, 0.090, 0.122, 1.0)  ## #1A171F：微溫黑曜石（按鈕常態、次級浮層）
const OBSIDIAN_DEEP      := Color(0.027, 0.024, 0.039, 1.0)  ## #07060A：黑曜石凹槽（背包空格、輸入槽陰影）

const GOLD_CLASSICAL     := Color(0.831, 0.686, 0.216, 1.0)  ## #D4AF37：古典金（主邊框、按鈕強調、黃金齒輪高光）
const GOLD_HOVER         := Color(0.941, 0.843, 0.549, 1.0)  ## #F0D78C：黃金亮色（選中激活、按鈕懸停亮邊）
const BRONZE_ANTIQUE     := Color(0.549, 0.416, 0.102, 1.0)  ## #8C6A1A：仿古黃銅（邊框底厚度、陰影咬合、暗金槽）
const BRONZE_WARM        := Color(0.769, 0.573, 0.165, 1.0)  ## #C4922A：暖古銅（次級數值金、勳章飾邊）

const TEAL_CORE          := Color(0.243, 0.812, 0.749, 1.0)  ## #3ECFBF：以太青綠核心（生命/戰力強調、發條能量、眼睛發光）
const TEAL_CORE_DARK     := Color(0.122, 0.541, 0.502, 1.0)  ## #1F8A80：以太青綠暗底（能量槽背景、發條蓄力條暗部）

const INK_IVORY          := Color(0.957, 0.922, 0.831, 1.0)  ## #F4EBD4：象牙白文字（一級主標、關鍵數值、極高對比度）
const INK_IVORY_SOFT     := Color(0.788, 0.749, 0.659, 1.0)  ## #C9BFA8：柔和象牙白（次級說明文字、次標籤）
const INK_IVORY_MUTED    := Color(0.541, 0.502, 0.439, 1.0)  ## #8A8070：弱化象牙白（禁用狀態、冷卻時間、副單位）

const CORAL_RUST         := Color(0.769, 0.361, 0.290, 1.0)  ## #C45C4A：鐵鏽珊瑚紅（危險警告、BOSS 標籤、殘血警示）
const STEEL_BLUE         := Color(0.420, 0.549, 0.682, 1.0)  ## #6B8CAE：淬火精鋼藍（防禦屬性、冷卻中裝備）

const LINE_GOLD          := Color(0.831, 0.686, 0.216, 0.38) ## 金線微光邊框（1px 卡片外框、神殿勾勒）
const LINE_GOLD_SOFT     := Color(0.831, 0.686, 0.216, 0.18) ## 輔助分界金線（列表格線、卡片內部分割）
```

> **⛔ 排他紅線**：  
> 嚴禁出現 `#FF6699`（草莓粉）、`#4ED86A`（糖果綠）、`#38A0FF`（晴空藍）、`#FFA010`（多巴胺橘）、`#FFFDF8`（奶油白卡片）。所有面板一律回歸黑曜石＋古典金。

---

## 4. 全域 HUD 與框架重構設計

### 4.1 背景場景（Background Layer）
* **現狀**：載入 `sky_kingdom_bg.png`，畫面為開闊藍天、白雲與綠色草地。
* **重製改法**：
  * 背景更換為**「神殿石柱黑曜石大廳」**手繪底圖（`res://assets/sprites/maps/temple_lobby_bg.png`），採 16:9 LINEAR 平滑採樣。
  * **構圖遵循 `art_direction.md` 第 3 節**：
    * 兩側對稱矗立希臘式凹槽大理石巨柱，黃金齒輪與傳動軸精巧咬合於石柱外側，作為畫面邊界框架；
    * 遠景中央高挑採光天井處懸浮著適中尺寸的「齒輪之心（Gear Heart）」，散發溫暖青綠（`#3ECFBF`）以太微光；
    * 前景與中景為乾淨、水平延伸的黑曜石石板地面，具備柔和的高光倒影，中央完整保留乾淨角色站位與互動空間；
    * 彻底**移除** `_build_carnival_buntings()`（彩虹吊旗）與飄浮的草莓粉/蜜糖黃星星。

### 4.2 頂部資源列（Top HUD Bar）
* **現狀**：奶油白底大圓角面板（高 64px，`UiStyle.TATA_CARD_BG`），包含等級、名稱、戰力、體力、金幣、齒輪。
* **重製改法**：
  * **容器外觀**：改為黑曜石半透明面板（`OBSIDIAN_BASE` @ 88% alpha），上下帶 1px 古典金線（`LINE_GOLD`），圓角收為 8px（符合神殿俐落刻線，告別 22px 膨脹圓角）。
  * **玩家個人資訊**：
    * 玩家頭像框：由圓形白框改為「黃銅齒輪雕花外框」，內襯象牙黑曜漸層底。
    * 等級徽章：深古銅底＋象牙白加粗字 `Lv.1`。
    * 角色名稱：`INK_IVORY` 象牙白字，取消白色粗描邊，改用 1px 深黑曜石陰影。
    * 戰力膠囊：黑曜石凹槽底＋古典金邊框，顯示 `✦ 482`（數字以 `#D4AF37` 呈現）。
  * **資源計數膠囊（體力、金幣、鑽石）**：
    * 膠囊底色改為 `OBSIDIAN_DEEP`（深黑凹槽），邊框為 `LINE_GOLD_SOFT`。
    * 數值文字使用 `INK_IVORY`，體力數值使用 `TEAL_CORE`（`15/15`）。
    * 購買按鈕「+」改為古典黃銅浮雕方鈕（28×28px，帶 1px 金邊，觸控熱區維持 48×48px）。

### 4.3 底部導航欄（Bottom Navigation Dock）
* **現狀**：奶油白底大圓角 Dock（高 72px，`UiStyle.TATA_CARD_BG`），5 個 Tab 按鈕均勻分佈。
* **重製改法**：
  * **容器外觀**：採用黑曜石神殿飾底板（`OBSIDIAN_BASE` @ 95% alpha），頂部拉出一條 2px 古典金鑲邊，兩側角隅點綴幾何希臘回紋（Meander）微刻。圓角由 24px 修正為 8px。
  * **5 個 Tab 按鈕狀態機**：
    * **未選中狀態（Inactive）**：
      * 底色為透明或 `OBSIDIAN_WARM`，文字為柔和象牙白 `INK_IVORY_SOFT`（#C9BFA8）。
      * 按鈕無邊框或僅帶極弱金線，低調不搶視覺。
    * **選中狀態（Active）**：
      * 底色變換為「古典黃金金屬漸層」（`#D4AF37` 至 `#C4922A`），文字轉為高對比的深黑曜石字（`#0B0A0E`）或反白立體字。
      * 按鈕正下方亮起一條 3px 高的青綠色能量呼吸指示光條（`TEAL_CORE` #3ECFBF），帶微微外發光。
    * **尺寸與熱區**：維持按鈕高 56px，寬度自適應填滿（橫屏單鍵寬度 > 220px），遠高於 ≥48px 人體工學標準。

---

## 5. 五大 Tab 逐一重構規格詳解

### 5.1 Tab 1：今日村莊（Village - 主城大廳）
* **中央英雄展台**：
  * **底盤重塑**：移除 `_rainbow_ring`（多巴胺彩虹光環），替換為「黃銅星盤日晷基座（Astrolabe Plinth）」——拋光黑曜石八角石台，鑲嵌同心黃金齒輪刻度環，間隙微透青綠以太流光。
  * **主角白兔互動**：
    * 保留 2.5 頭身發條金屬兔立繪、呼吸縮放動畫與點擊 Poke 姿態切換（揮劍、伸展）。
    * 移除點擊時爆發的「彩色糖果星芒粒子」，替換為「黃金火花與微型齒輪彈跳效果」。
  * **對話氣泡**：
    * 外框改為 `OBSIDIAN_CARD`（深黑曜石底）＋1px 古典金線（`GOLD_CLASSICAL`），圓角 8px。
    * 文字改為 `INK_IVORY`，台詞由過度幼態賣萌轉為覺醒機械玩具的堅毅好奇口吻（例如：「背後的發條上得剛剛好，出發吧！」、「聽見神殿齒輪的轉動聲了嗎？」）。
* **左側四大殿堂入口卡片（王都鐵匠、手藝工坊、演武競技、冒險委託）**：
  * **現狀**：4 張縱向卡片，尺寸 240×72px。
  * **重製樣式**：
    * 卡片本體採用黑曜石浮雕金屬牌（`OBSIDIAN_CARD` 底色，四角鉚接小螺絲）。
    * 左側圖示：預渲染的古典黃銅浮雕徽章（鍛造重錘、寶石熔爐、雙刃長槍、發條捲軸），帶金屬光澤。
    * 右側文字：標題為 `GOLD_CLASSICAL`，副標為 `INK_IVORY_SOFT`。
    * 點擊熱區維持 240×72px（完全符合手遊單手操作）。
* **右側當前主線卡片（出征戰情板）**：
  * 移除奶油白底，改為「黑曜石戰情報告板」（`OBSIDIAN_CARD` 底色＋2px `GOLD_CLASSICAL` 邊框）。
  * 標題「當前主線」使用 `BRONZE_WARM`，關卡名「第二地區 · 聖獅王城 (2-4 BOSS)」使用 `INK_IVORY` 加粗。
  * 「前往出征」按鈕（`btn_go_adventure`）：重製為預渲染黃金厚底壓鑄按鈕（尺寸 280×68px），主色為金色金屬質感，居中為「前往出征」立體字與推進箭頭。

### 5.2 Tab 2：角色裝備與紙娃娃（Character）
* **左側：角色全貌展示卡**：
  * 容器背景採用古典神殿壁龕（Niche）手繪底圖，頂部聚光燈柔和照射，腳底帶有深色軟影，完美融入黑曜石地坪。
* **右側：三欄武器輪替系統與屬性**：
  * **三欄武器卡槽（首選鐵劍、副手獵弓、絕技拳套）**：
    * 現狀：白底圓角小格（130×68px）。
    * 重製：改為「重型黃銅武器陳列匣」——深黑凹槽底色（`OBSIDIAN_DEEP`），外圍 2px 黃銅壓條與四角鉚釘，武器圖標以手繪金屬質感呈現，選中時亮起青綠以太高光框。
  * **屬性面板（RichTextLabel）**：
    * 底色使用 `OBSIDIAN_CARD`，去除刺眼霓虹色，改用典雅高對比世界觀配色：
      * 標題：`[color=#D4AF37][b]機體戰鬥屬性 (有效戰力 482)[/b][/color]`
      * 生命力 (HP)：`[color=#3ECFBF]520[/color]`（以太青綠）
      * 物理攻擊：`[color=#D4AF37]95[/color]`（古典金）
      * 物理防禦：`[color=#6B8CAE]48[/color]`（淬火精鋼）
      * 暴擊率：`[color=#F0D78C]22%[/color]`（金琥珀）
      * 怒氣量表：`[color=#C45C4A]20 點 (滿怒超頻運轉 +25% 性能)[/color]`（鐵鏽珊瑚紅）

### 5.3 Tab 3：四區出征（Adventure）
* **頂部地區切換導航（第一地區～第四地區）**：
  * 按鈕樣式改為「神殿黃銅刻籤」：4 顆水平按鈕（175×46px，垂直熱區擴大至 48px）。
  * 未選中：`OBSIDIAN_WARM` 底＋`INK_IVORY_MUTED` 字。
  * 選中：`GOLD_CLASSICAL` 漸層底＋`OBSIDIAN_BASE` 凹刻字＋底部青綠能量點。
* **關卡卡片網格（2×2 佈局，尺寸 430×105px）**：
  * **普通關卡**：
    * 底色為 `OBSIDIAN_CARD`，邊框為 1px `LINE_GOLD`。
    * 左側關卡編號「2-1」以金色印章牌呈現，關卡名稱為 `INK_IVORY`，戰力推薦使用 `INK_IVORY_SOFT`。
    * 「出征」按鈕為黃銅厚底按鈕（110×48px）。
  * **BOSS 關卡（首領部位破壞）**：
    * 卡片邊框加粗為 2px `BRONZE_ANTIQUE` 帶微弱紅珊瑚警示呼吸光（`CORAL_RUST`）。
    * 右上角標註「部位破壞可」金屬銘牌。
    * 「挑戰首領」按鈕採用高對比度古典金拉絲厚底按鈕。

### 5.4 Tab 4：聚魂殿堂（Soul Hall - 封靈罐四階）
* **設計意象**：由幼兒糖果罐徹底轉型為**「希臘神殿以太祭壇（Aether Altar）」**。
* **四階封靈罐重塑**：
  * 維持綠、藍、紫、橙四階級，但色盤與材質徹底金屬古董化：
    1. **綠階封靈罐**：青銅綠鏽古罐（Verdigris Bronze Vessel）——斑駁銅綠與微弱青綠光（`#3ECFBF`）。
    2. **藍階封靈罐**：淬火精鋼青金罐（Tempered Steel Vessel）——深邃精鋼與幽藍光（`#6B8CAE`）。
    3. **紫階封靈罐**：黑曜紫晶秘法罐（Obsidian Amethyst Vessel）——黑曜石外殼嵌紫晶發條。
    4. **橙階封靈罐**：日輪黃金聖器罐（Golden Solar Vessel）——奢華黃金浮雕與熾金以太齒輪。
  * **點亮狀態反饋**：未點亮時為黯淡灰銅金屬；點亮時頂部發條鑰匙旋轉，罐身縫隙散發強烈以太光芒。
* **底部操作列**：
  * 「一鍵吸收灰魂」：磨砂黑曜石長方按鈕（210×52px，符合 ≥48px）。
  * 「聚魂十連」：預渲染黃金壓鑄雕花按鈕（220×56px，`btn_draw_10.png` 重製為黃金發條主題）。

### 5.5 Tab 5：冒險背包（Bag）
* **倉庫網格佈局**：
  * 8 欄 × 3 列共 24 格，單格尺寸維持 72×72px（遠大於 48px 熱區要求）。
  * **空格底槽**：改為 `OBSIDIAN_DEEP`（#07060A）金屬凹槽，帶 1px 內凹暗影與 `LINE_GOLD_SOFT` 邊界刻線。
  * **道具品階邊框**：
    * 粗糙（白）：生鐵暗灰框
    * 普通（綠）：青銅綠鏽框
    * 精良（藍）：精鋼青藍框
    * 史詩（紫）：黑曜秘銀框
    * 傳奇（橙）：黃金齒輪浮雕框

---

## 6. 資料綁定與人體工學相容性驗證

本重構方案在視覺層面進行 100% 翻新，但對程式碼結構實施**零破壞性解耦**：

1. **節點樹與標籤綁定 100% 兼容**：
   - 頂部數值節點：`_lv_label`, `_name_label`, `_power_label`, `_energy_label`, `_gold_label`, `_gem_label` 結構完全一致，僅樣式面板（StyleBoxFlat）與字體色彩常量指向新的黑曜石色碼。
   - 內部方法 `refresh_hud()`, `_switch_tab()`, `_select_region()`, `_do_gourd_draw()` 無需修改一行邏輯。
2. **手遊橫屏雙拇指熱區規格（全部 ≥ 48px）**：
   | 互動元件 | 寬度 × 高度 (px) | 規範標準 | 判定 |
   |---|---|---|---|
   | 頂部資源加號鈕 | 48 × 48 | ≥ 48px | ✅ 通過 |
   | 底部 Dock Tab 鈕 | > 200 × 56 | ≥ 48px | ✅ 通過 |
   | 主城四大殿堂卡 | 240 × 72 | ≥ 48px | ✅ 通過 |
   | 前往出征大按鈕 | 280 × 68 | ≥ 48px | ✅ 通過 |
   | 出征關卡卡片 | 430 × 105 | ≥ 48px | ✅ 通過 |
   | 四地區切換標籤 | 175 × 48 | ≥ 48px | ✅ 通過 |
   | 封靈罐點擊按鈕 | 145 × 170 | ≥ 48px | ✅ 通過 |
   | 背包道具槽位 | 72 × 72 | ≥ 48px | ✅ 通過 |
3. **無系統 Emoji 與純 Label PPT 感**：
   - 徹底摒棄任何系統內建 Emoji，所有標籤圖標均由自研手繪金屬部件與幾何符號（`✦`、`⚔`、`⚙`）組成。
   - 核心按鈕全面使用預渲染金屬質感壓鑄板件，徹底消除傳統辦公室 PPT 平淡感。

---

## 7. 概念示意圖生成與 Vision 15 項自檢報告

為驗證本方案構圖與美學可行性，使用 `gen_media.py image` 搭配 `--ref branding/key_visual_main.png` 產出了大廳視覺概念示意圖：  
**圖檔路徑**：`/opt/side/bravesoul-game/docs/lobby_ui_redesign_concept.png`

### 7.1 產圖提示詞（Prompt）存檔
```text
A 16:9 mobile RPG lobby screen concept and environment for a charming mechanical toy fantasy game.
A grand forgotten classical toy theater temple hall with massive fluted Greek temple stone columns and weathered obsidian stone platform flooring.
Antique brass and golden mechanical clockwork gears, drive shafts, and cogs are elegantly integrated into the temple stone pillars as decorative architectural accents, never cluttering the central space.
In the center foreground stands a charming 2.5-head-tall chibi ivory-white mechanical toy rabbit hero holding ONE single-handed longsword, with an antique brass winding key visible on its back, rigid metal upright ears, expressive cyan-green glass eyes, and a glowing cyan-green chest core.
In the upper midground floating gently behind the central stage is the intricate antique brass Gear Heart mechanism radiating a soft mystical cyan-green glow.
Materials: polished dark obsidian stone, fluted classical marble pillars, aged brass, ivory painted metal with chipped enamel, subtle rust, rivets, screws, warm patina.
Color palette: obsidian deep black (#0B0A0E), classical antique gold (#D4AF37), warm brass, ivory metal, with radiant cyan-green (#3ECFBF) magical highlights.
Lighting: dramatic warm theatrical golden sunlight beaming through high neoclassical temple colonnades, volumetric rays illuminating floating dust motes, cyan rim light from the mechanical core, soft grounding floor shadows.
Composition: clear mobile game lobby layout, expansive clean central stage for hero display and gameplay interaction, edges framed by stately columns and brass gears, uncluttered top and bottom zones reserved for mobile HUD and navigation dock.
Camera: eye-level medium-wide shot, 35mm lens, high readability at mobile phone screen resolution.
Style keywords: premium stylized 3D game art, handcrafted mechanical toy fantasy, whimsical steampunk neoclassical fairy tale, Greek temple colonnade, high contrast, strong silhouettes, clean mobile UI friendly composition.
NEGATIVE PROMPT:
colorful carnival bunting flags, rainbow flags, candy colors, bright party confetti, flat modern corporate illustration, plush toy, real animal fur, biological rabbit, humanoid robot, military mech, Iron Man shiny armor, giant overpowering gears covering the entire screen, industrial factory, horror, creepy porcelain doll, blank eyes, messy cluttered floor, photorealistic human, text, logo, watermark, UI buttons, multiple swords, extra limbs.
```

### 7.2 Vision 自檢詳細過程與檢驗表（依據 `art_direction.md` 第 5 節 15 項 + 第 0 節兩項）

| # | 檢查項目 | 依據標準 | 示意圖實測觀察與判定 | 結果 |
|---|---|---|---|:---:|
| **0a** | **30m 縮圖動物輪廓辨識** | `art_direction.md` 0 節 | 縮小至 128px 時，直立長耳、緊湊頭身與持劍剪影極其清晰，兔子角色輪廓瞬間可讀。 | ✅ **通過** |
| **0b** | **10m 武器與大色塊辨識** | `art_direction.md` 0 節 | 右手持單手長劍向外伸展，劍身與身體負空間明確，黃金握柄與銀刃色塊鮮明，絕無黏連。 | ✅ **通過** |
| **1** | **破舊感與歷史痕跡** | `art_direction.md` 1 節 | 象牙白裝甲邊緣帶有自然漆面剝落、微鏽斑與細微刮痕，呈現在閣樓歷經歲月的骨董玩具質感。 | ✅ **通過** |
| **2** | **是玩具非小型機器人** | `art_direction.md` 1 節 | 身體為手工旋鉚與螺絲拼接結構，關節圓潤微拙，保留非工業對稱的手工感，絕非冷酷高科技機甲。 | ✅ **通過** |
| **3** | **動物特徵機械化** | `art_direction.md` 2.1 節 | 兔耳為金屬板件包邊加固、臉頰無生物毛皮、鼻翼與關節皆為機械件，零生物軟肉感。 | ✅ **通過** |
| **4** | **背後發條鑰匙看得到** | `art_direction.md` 2.1 節 | 主角背後左上方清晰外露古典黃銅蝴蝶發條鑰匙，破壞死板對稱並強化發條玩具符號。 | ✅ **通過** |
| **5** | **Q 版 2.2~2.8 頭身比** | `art_direction.md` 2.1 節 | 不計耳朵，頭部高度與全身比例約 1:2.45，軀幹四肢短小討喜，完美落在 2.2~2.8 範圍。 | ✅ **通過** |
| **6** | **核心材質斑駁黃銅/米白** | `art_direction.md` 2.3 節 | 主體為象牙米白金屬漆面配斑駁古黃銅飾邊，完全排除絨毛、鏡面鉻或現代塑膠感。 | ✅ **通過** |
| **7** | **耳朵直立不垂** | `art_direction.md` 2.1 節 | 雙耳硬質挺立向上，金屬結構絕無軟垂，符合玩具結構力學。 | ✅ **通過** |
| **8** | **胸口與眼睛青綠發光** | `art_direction.md` 2.3 節 | 胸前圓形以太核心散發純淨青綠（`#3ECFBF`）光暈，眼珠為青綠晶石玻璃，焦點匯聚。 | ✅ **通過** |
| **9** | **胡桃鉗典雅舞台配色** | `art_direction.md` 2.3 節 | 畫面以象牙白、古典金、黑曜石與青綠微光交織，兼具胡桃鉗劇場的莊重與典雅，無鋼鐵人俗艷紅金。 | ✅ **通過** |
| **10** | **角色武器正確（單手劍）** | `art_direction.md` 2.2 節 | 主角手持單把單手長劍，絕無雙持或違背職業設定之武器。 | ✅ **通過** |
| **11** | **齒輪為邊緣點綴不過大** | `art_direction.md` 3 節 | 黃金齒輪精巧纏繞在兩側神殿石柱外緣，中央視野開闊，齒輪未搶佔視覺重心。 | ✅ **通過** |
| **12** | **深色描邊與腳底軟影** | `art_direction.md` 2.1 節 | 角色輪廓具備清晰高對比邊界，腳底在地表投射出自然的接觸陰影與金屬反光，站立穩固。 | ✅ **通過** |
| **13** | **場景保留乾淨可玩空間** | `art_direction.md` 3 節 | 中央黑曜石石板開闊平整，無巨大突起障礙物，為 HUD、展台與未來 UI 留下充裕的安全負空間。 | ✅ **通過** |
| **14** | **16:9 手機橫屏規格** | `brand_assets.md` | 產圖比例精確為 16:9 橫屏，視野開闊，完美適配手機與平板橫向視野。 | ✅ **通過** |
| **15** | **零恐怖/瓷娃娃元素** | 2026-09-05 退稿準則 | 角色面容親切溫暖、眼神靈動好奇，毫無空洞黑眼眶、裂紋或恐怖片人偶感。 | ✅ **通過** |

**自檢總結**：17 項檢驗標準全數打勾合格，充分驗證「希臘神殿石柱 × 黑曜石底色 × 古典黃金齒輪」視覺定調在大廳構圖與手遊 UI 承載上的完美可行性。

---

## 8. 結論與執行建議

1. **視覺資產升級清單**：
   - 繪製/匯入 `res://assets/sprites/maps/temple_lobby_bg.png`（神殿黑曜石底圖）。
   - 產出 4 張神殿黃銅殿堂卡牌圖（鐵匠、工坊、競技、委託）。
   - 重製 `btn_go_adventure.png` 與 `btn_draw_10.png` 為黃金厚底壓鑄按鈕。
2. **代碼重構路徑（後續由 sideworker 阿宏執行，本次不動 code）**：
   - 在 `ui_style.gd` 中新增神殿黑曜石色碼常數（替換或新增覆蓋舊的 `TATA_*` 糖果色）。
   - 在 `mobile_lobby.gd` 中拔除 `_build_carnival_buntings()`。
   - 將各 Tab 的 `StyleBoxFlat` 由 `TATA_CARD_BG` 調整為 `OBSIDIAN_CARD` 與 8px 圓角。
3. **官網聯動效益**：
   - 本設計落實後，實機大廳截圖將可無縫替換 `web/pages/gallery.html` 與 `web/index.html` 中的「大廳全面重構中占位卡」，徹底解決官網宣傳圖脫節之痛點。
