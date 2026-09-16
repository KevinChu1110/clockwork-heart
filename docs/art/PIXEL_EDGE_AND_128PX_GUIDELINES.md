# 128px 紙娃娃像素邊緣清理與產圖防呆規範 (Pixel Edge & 128px Clarity Guidelines)

> 本規範由側案·美術總監 小柔 針對 Kevin 對首發兔族小白（Whitey）「邊緣模糊、手部糊成色塊」之反饋建立。供所有 128x128 像素級紙娃娃切片與後續族系（狐/獅/豬/猴/熊/鶴/企鵝等）產圖與後製時嚴格遵循。

---

## 一、 問題根因分析 (Root Cause Analysis)

經過像素級數據盤點與視覺拆解，造成「邊緣模糊、手部成色塊、胸前細節渙散」的核心根因有四：

1. **128px 畫布塞入過多高解析度細節 (Over-detailing)**：
   - 原版在 AI 產圖或繪製時，提示詞偏向高精度立體質感（漸層反光、金屬絲光、微米級陰影），縮小到 128x128 畫布時，有限像素無法承載細碎漸層，各像素在採樣時被「平均混色」，導致對比度劇降、細節發散。
2. **下採樣抗鋸齒羽化 (Anti-Aliasing Semi-Alpha Blur)**：
   - 在進行縮放或羽化去背時，邊緣產生了 1~3 像素寬的半透明漸層（Alpha 介於 20~220）。在單層看可能不明顯，但紙娃娃系統由 7 大圖層（Z: 5..40）層層疊加時，各層邊緣半透明像素相互加成混色，使整體角色輪廓呈現發灰、起霧的「毛邊光暈」。
3. **服裝圖層主體透明度不足 (Translucent Tunic Defect)**：
   - 原始 `costume_nutcracker_guard.png` 的胸前布料 Alpha 值僅約 35~50（70% 透明），底層素體外殼穿透上浮，使鮮紅軍服退色成粉灰，雙排金扣與飾繩也失去底色依託。
4. **極小手部結構缺乏像素級幾何分件 (Chunky Hand Structure Missing)**：
   - 角色手部在 128px 畫布上僅約 4~6 像素寬。在沒有明確指節刻線（Crease）與深色邊界的情況下，膚色像素直接黏成一團，無法傳達「握拳」或「握持」動態。

---

## 二、 產圖提示詞 (Prompt) 規範

今後產出紙娃娃切片或角色原畫時，**嚴禁**使用引導細密雜訊的關鍵詞，必須強制注入像素清晰度約束：

### 1. 正向提示詞必帶 (Mandatory Positive Keywords)
- `crisp hard-edge pixel clarity, bold clean outlines, deep warm brown outlines (#2C1C16)`
- `simplified macro details designed for 128x128 canvas, strong silhouette readability`
- `distinct toy mechanical joints, clear knuckle creases, chunky toy hands`
- `flat cel-shaded blocks with high contrast highlights and shadows, saturated stage toy palette`
- `zero semi-transparent gradient blur, 100% opaque solid fills`

### 2. 反向提示詞必帶 (Mandatory Negative Keywords)
- `micro details, noisy textures, photorealistic gradients, soft airbrush, gaussian blur`
- `semi-transparent edge feathering, anti-aliased edge haze, foggy halo, blurry silhouette`
- `muddy unreadable fingers, blob hands, washed out colors, low contrast pastel wash`

---

## 三、 後製管線與像素級驗收標準 (Post-processing Pipeline & QA)

所有入庫的 128x128 切片素材，必須經過自動化/腳本驗證：

| 檢驗項目 | 規範標準 | 失敗表現（退件） |
|---|---|---|
| **邊緣半透明率 (Semi-Alpha Ratio)** | 外輪廓半透明像素（`0 < alpha < 255`）比例必須為 **0.0%**（純硬邊） | 邊界帶有 1~2px 的羽化半透明漸層 |
| **外輪廓線 (Silhouette Outline)** | 最外圈非透明像素必須統一為深暖褐 `#2C1C16`（`C_OUTLINE`） | 浮空未勾邊、或輪廓為雜色邊緣 |
| **服裝主體 (Costume Body)** | 服裝布料與底層板件 Alpha 必須為 **255** 實心填滿 | 半透明透底、看到底層機械接縫穿幫 |
| **手部指節 (Knuckles & Clasp)** | 右手與左手握持處必須有至少 2~3 根清晰玩具指節，帶 1px 深色分界刻線與亮面高光 | 像素糊成肉團、指頭無分段、無握持結構 |
| **胸前細節 (Cords & Buttons)** | 飾繩以 1px 俐落水平/微弧金色飾線呈現，雙排扣以 2x2 立體金方/圓釘排列，對比度明確 | 細密花紋糊成髒點、扣子大小位置不一 |

---

## 四、 首發五族抽查範圍回報

本次盤點確認：**邊緣羽化半透明問題普遍存在於首發五族與後續族系**：
- **兔（Rabbit）**：修復前 composite 半透明率 22.0%（已由本任務完成像素級重構，達到 0.0% 純硬邊）；
- **狐（Fox）**：composite 半透明率 15.7%，尾巴達 46.3%；
- **獅（Lion）**：composite 半透明率 21.6%，尾巴達 74.6%；
- **豬（Boar）**：composite 半透明率 12.6%，chassis 達 15.7%；
- **猴（Macaque）**：composite 半透明率 29.1%，chassis 達 50.2%。

依側案美術規範，後續族系將依看板任務排程，比照本手冊之管線逐族推進清理，避免一次性盲目重產引發回歸風險。
