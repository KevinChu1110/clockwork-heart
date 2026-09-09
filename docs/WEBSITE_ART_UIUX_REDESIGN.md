# 《發條之心》官網整體視覺與 UI/UX 系統性重製指南
> **文件性質**：美術總監（小柔）審查報告與實作規格書  
> **對齊標準**：`references/art_direction.md`（v2 手機優先、希臘神殿黑曜石×黃金齒輪）、`docs/LOBBY_UI_REDESIGN.md`、Kevin UI 規範（拒絕 PPT 感、3D 果凍厚底按鈕、粉圓體）  
> **實作對象**：側案程式 阿宏（sideworker）  
> **關聯看板任務**：`t_0aee77cb`  

---

## 1. 審查背景與根本病灶剖析

針對 Kevin 提出的核心反饋：**『根本美術效果 UIUX 要改，不是小修』**，美術部對現行線上官網（https://kevinchu1110.github.io/clockwork-heart/）進行了逐頁、逐層級的深度審查。

目前的根本問題**絕非單純「刪除重複區塊」**，而是存在三大結構性美術崩壞：

### 根本病灶 1：CSS 多層覆蓋造成的「死黑沉悶與僵硬感」
* 早期 `site.css` 與 `sections.css` 殘留了 Tata 糖果風與白色卡片樣式。
* 後期為了對齊神殿風格，以 `temple.css` 強制將全站背景暴力替換為 `#0B0A0E`（黑曜石純黑），並將圓角全域硬切為 `6px~10px`、按鈕切為 `4px` 倒角方塊。
* **後果**：整頁從頭滑到尾是一整片漆黑死寂，完全抹殺了世界觀的空間縱深與探索呼吸感。神殿的「黑曜石」本應是帶有鏡面反光的奢華琉璃質地，卻被做成了「未完工的暗黑施工現場」。

### 根本病灶 2：嚴重的「傳統辦公室 PPT 簡報感」
* 核心特色大量使用純文字條列（`ul.feature__list`）、小字體標籤（`0.78rem~0.82rem`）、灰色弱化說明文字。
* 按鈕皆為扁平純文字超連結，缺少手遊該有的「立體觸控感」與「點擊誘惑力」。
* 首頁充斥多達 4 處「占位卡（Placeholder Cards）」，印著 SVG 齒輪並寫著「調校中」、「即將登場」，嚴重給人「遊戲尚未成熟、內容空洞」的半成品廉價印象。

### 根本病灶 3：品牌資產與遊戲大廳風格脫節
* 官方已經定案並由 Kevin 選定的中文手繪字標（`branding/logo_cn_black.png`），官網居然完全沒用！GNB 與 Hero 僅使用普通純文字 `發條之心` 搭配簡陋的 SVG 小圈。
* 實機大廳展示截圖（`proof_mobile_lobby_home.png`）仍是舊版的「藍天綠草地浮空城堡」，與神殿黑曜石世界觀徹底衝突。
* 全站 10 個子頁面（`pages/*.html`）竟然全部私自引用 Google Fonts 的「思源黑體（`Noto Sans TC`）」，直接破壞了 Kevin 嚴格要求的「開源粉圓體（Open Huninn）」規範！

---

## 2. 四大視覺維度系統性重整方案

### 2.1 視覺層級與資訊架構（Visual Hierarchy）
現行首頁高達 13 個區塊，實機截圖重複出現 3 次，特色說明反覆換皮換卡片堆疊。應精簡收斂為 **7 大高張力黃金模組**：

| 順序 | 模組名稱 | 視覺形式 | 核心目標 |
|---|---|---|---|
| **01** | **Hero 磅礡首屏** | 官方字標 Logo + 15s 預告片背景 + 雙黃金立體按鈕 | 奠定奇想發條玩具手遊品牌高度 |
| **02** | **神殿石柱與四英雄** | 主視覺 Showcase + 四族公仔立繪 Tab 切換 | 展現「全金屬、背負發條鑰匙」世界觀 |
| **03** | **核心玩法三軸** | 三大視覺化圖卡（15 圈能量律動 / 聽音部位拆卸 / 器魂招三軸） | 告別純文字列表，以圖解展示獨特玩法 |
| **04** | **實機大廳與日常** | 神殿黑曜石大廳實機圖 + 點擊戳碰互動說明 | 呈現 2.2 頭身白兔活化生態與橫屏雙拇指手感 |
| **05** | **戰鬥與系統實機瞬間** | 3 欄式真實截圖（強敵部位破壞 / 聚魂殿抽魂 / 釘釘鍛造） | 用真畫面說話，絕不放占位卡 |
| **06** | **六大界域沙盤探索** | Bento 網格（騎士堡壘、霧隱村、道場、森林、深港、法師之塔） | 呈現非線性地圖與古典玩具劇場風貌 |
| **07** | **Final CTA 號召啟程** | 官方發條之心光暈底台 + 雙主按鈕（實機影音 / 立即下載） | 轉化預約與社群追蹤 |

### 2.2 間距與版面節奏（Spacing Rhythm）
* **清除內聯寫死的碎裂間距**：禁止 `style="padding:2.2rem 0"`、`style="padding:1.6rem 0"`。
* **建立 8pt 系統化階梯**：
  - 區塊垂直 Padding：桌面端一律 `96px`（`6rem`），手機端 `56px`（`3.5rem`）。
  - 模組標題（`sec-head`）與內容間距：固定 `40px`（`2.5rem`）。
  - 內容卡片內部 Padding：一律 `24px~32px`。
* **移除硬性金色分割劃線**：拿掉 `border-top: 1px solid rgba(212,175,55,0.2)`，改用「黑曜石鏡面深淺微漸層（`#0B0A0E` ↔ `#141218`）」自然過渡。

### 2.3 色彩對比與材質升級（Color & Materials）
嚴格落實「神殿黑曜石 × 古典黃金齒輪 × 青綠發條之心」的三角平衡：
* **底色層次（Obsidian Layers）**：
  - 全域基底：`#0B0A0E`（深黑曜石）。
  - 卡片浮層：`#141218` 至 `#1A171F`（微溫黑曜石漸層，帶 1px `rgba(212, 175, 55, 0.35)` 鑲金細線）。
  - 凹槽與背景：`#07060A`（深邃黑曜石凹槽）。
* **提亮焦點（Golden Highlights）**：
  - 關鍵數值、徽章、強調邊框使用 `#F0D78C`（高光金）與 `#D4AF37`（古典金）。
  - 徹底杜絕灰暗濁黃（`#8A8070` 用於說明文字導致閱讀困難，次級文字全面提升至 `#C9BFA8` 象牙柔白）。
* **能量點睛（Teal Core Emissive）**：
  - 發條能量、核心指示、選中態微光一律使用 `#3ECFBF`（以太青綠），並在深色背景加上 `0 0 16px rgba(62, 207, 191, 0.4)` 柔和光暈。

### 2.4 卡片統一規範（Universal Card System）
廢除全站各行其是的 6px、8px、18px、22px 混亂設定，統一卡片標準：
```css
.card, .sys-card, .bento-card, .hero-panel {
  background: linear-gradient(165deg, rgba(26, 23, 31, 0.95) 0%, rgba(18, 16, 24, 0.98) 100%);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 18px; /* 回歸手遊大圓角舒適感 */
  box-shadow: 
    inset 0 1px 0 rgba(240, 215, 140, 0.25), /* 頂部內嵌金屬高光 */
    0 12px 32px rgba(0, 0, 0, 0.55);          /* 沉浸感深黑投影 */
  backdrop-filter: blur(12px);
  transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease;
}
.card:hover {
  transform: translateY(-4px);
  border-color: rgba(240, 215, 140, 0.7);
  box-shadow: 
    inset 0 1px 0 rgba(240, 215, 140, 0.4),
    0 0 24px rgba(212, 175, 55, 0.25),
    0 16px 40px rgba(0, 0, 0, 0.65);
}
```

---

## 3. 對齊 Kevin UI 規範之落差修正

### 3.1 3D 鑄金琺瑯果凍厚底按鈕（徹底取代 4px 扁平方塊）
按鈕是手遊官網最核心的互動觸點。現行 4px 倒角的純文字連結必須全面升級為「**古典黃金鑄造 × 琺瑯琉璃 3D 厚底按鈕**」：
```css
/* ── 主行動按鈕：黃金鑄造果凍厚底 ── */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0 1.8rem;
  font-family: "Open Huninn", sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: #1A1204 !important;
  background: linear-gradient(180deg, #FFF0B8 0%, #F0D78C 28%, #D4AF37 70%, #AA821C 100%);
  border: 1px solid #FFE699;
  border-radius: 16px; /* 舒適大圓角，告別 4px */
  position: relative;
  box-shadow: 
    0 5px 0 #5C440E,                          /* 5px 實體立體厚槽 */
    0 10px 24px rgba(212, 175, 55, 0.35);     /* 暖金環境輝光 */
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.btn-primary:hover {
  background: linear-gradient(180deg, #FFFFFF 0%, #FCE29E 25%, #E5BF45 70%, #B88E22 100%);
  transform: translateY(-2px);
  box-shadow: 
    0 7px 0 #5C440E,
    0 14px 28px rgba(212, 175, 55, 0.45);
}

.btn-primary:active {
  transform: translateY(3px);                  /* 扎實的機械下沉按壓反饋 */
  box-shadow: 
    0 2px 0 #5C440E,
    0 4px 12px rgba(212, 175, 55, 0.3);
}

/* ── 次要按鈕：黑曜石琉璃金線厚底 ── */
.btn-ghost {
  min-height: 52px;
  padding: 0 1.6rem;
  font-family: "Open Huninn", sans-serif;
  font-size: 1.02rem;
  font-weight: 700;
  color: #F4EBD4 !important;
  background: linear-gradient(180deg, #24202C 0%, #15131A 100%);
  border: 1.5px solid rgba(212, 175, 55, 0.6);
  border-radius: 16px;
  box-shadow: 0 4px 0 #0E0C12, 0 8px 20px rgba(0, 0, 0, 0.4);
  transition: all 0.15s ease;
}
.btn-ghost:hover {
  background: linear-gradient(180deg, #2D2838 0%, #1A1722 100%);
  border-color: #F0D78C;
  color: #FFFFFF !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 0 #0E0C12, 0 12px 24px rgba(212, 175, 55, 0.2);
}
.btn-ghost:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #0E0C12;
}
```

### 3.2 字體 100% 統一為粉圓體（清除思源黑體）
* **問題**：`gallery.html`、`trailers.html`、`systems.html`、`weapons.html`、`equipment.html`、`walkthrough.html`、`guide.html`、`maps.html`、`download.html`、`account.html` 10 個檔案中均有：
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap" rel="stylesheet" />
  ```
* **整改要求**：
  1. 全數刪除上述 10 個 HTML 內的 Google Fonts `Noto Sans TC` 外部載入標籤。
  2. 確保所有頁面皆統一載入 `css/site.css` 中的 local `@font-face`（`jf-openhuninn-2.1.ttf`）。
  3. `body` 與所有標題、按鈕一律繼承 `"Open Huninn", "jf-openhuninn", sans-serif`。

### 3.3 品牌官方字標（Logo）正式置入
* 官方美術資源庫中已具備 Kevin 選定的手繪書冊風字標（`branding/logo_cn_black.png`），現已同步拷貝至 `web/media/branding/logo_cn_black.png`。
* **導覽列（GNB）修改**：
  將純文字 `.logo` 改為帶有官方高解析透明黑底字標圖示：
  ```html
  <a class="logo" href="index.html">
    <img src="media/branding/logo_cn_black.png" alt="發條之心 Clockwork Heart" class="logo-img" style="height:38px;width:auto;display:block;" />
  </a>
  ```
* **Hero 區塊修改**：
  在主標題上方加入品牌 Logo 徽章或直接以官方字標作為 Visual Crest，取代單純的純文字 `h1`。

### 3.4 導覽列（GNB）資訊瘦身
* **現狀痛點**：GNB 塞滿了 10 個文字連結（首頁、流派、圖鑑、地圖、養成、攻略、指南、畫面、下載、帳號），在任何螢幕上都像行政後台導航。
* **重構整合方案**（精簡為 5 大入口 + 1 個 CTA 實體金鈕）：
  1. **首頁** (`index.html`)
  2. **世界觀與角色** (`#temple-showcase`)
  3. **系統與圖鑑** (`pages/systems.html`，內含裝備/武器/殿堂)
  4. **影音與畫面** (`pages/gallery.html`，內含預告片/實機截圖)
  5. **冒險指南** (`pages/guide.html`，內含攻略/地圖)
  6. 右側按鈕：**【立即下載】**（`.btn-primary` 立體金鈕，直通 `pages/download.html`）

---

## 4. 具體素材替換與下架清單

| 現行素材路徑 / 元素 | 現存問題 | 替換對策與路徑 | 狀態 |
|---|---|---|---|
| `web/media/shots/proof_mobile_lobby_home.png` | 舊版浮空城堡藍天草地，與神殿風格割裂 | 替換為 `web/media/shots/proof_mobile_lobby_temple.png`（神殿黑曜石石柱大廳已過審概念圖） | ✅ 檔案已就緒 |
| `index.html` 晨光工坊占位卡 (`placeholder-card`) | 醜陋 SVG 齒輪 +「調校中」半成品標籤 | 替換為真實探索場景圖卡 + 特色文字說明（可採用 `web/media/shots/proof_20_mist_shrine.png` 或 `proof_18_forest_lake.png`） | ✅ 現成截圖在庫 |
| `index.html` 養成系統占位卡 (`placeholder-card`) | 醜陋 SVG 多邊形 +「即將揭曉」標籤 | 替換為 `web/media/shots/proof_soul_pity.png`（聚魂殿抽魂實機介面） | ✅ 現成截圖在庫 |
| `index.html` 流派切換占位卡 (`placeholder-card`) | 醜陋 SVG 占位卡 | 替換為 `web/media/shots/proof_forge_panel.png`（鍛造介面實機截圖） | ✅ 現成截圖在庫 |
| 導覽列與 Hero 純文字標題 | 缺乏官方手繪字標，像內部文件 | 引入 `web/media/branding/logo_cn_black.png` | ✅ 檔案已同步 |

---

## 5. 給阿宏（sideworker）的實作工單檢核表

- [ ] **Task 1: 清理全站字型違規**
  - 檢視並移除 `web/pages/*.html`（共 10 檔）中所有 `fonts.googleapis.com/.../Noto+Sans+TC` 標籤。
  - 確認全站所有頁面均透過 `css/site.css` 正確載入並優先套用 `Open Huninn`。

- [ ] **Task 2: 重構按鈕與全域圓角 CSS**
  - 在 `web/css/temple.css` 中，將 `.btn`、`.btn-primary`、`.btn-ghost` 重構為第 3.1 節規範的「3D 鑄金琺瑯果凍厚底規格」（5px 實體厚槽、14~16px 圓角、`:active` 3px 下沉）。
  - 將 `.card`、`.sys-card`、`.bento-card` 全面統一為 18px 圓角與雙層微光陰影（第 2.4 節規格）。

- [ ] **Task 3: GNB 與頁面導覽重整**
  - 修改 `web/js/site.js` 中的導覽列生成邏輯，將 10 個連結收斂為 5 大入口，右側為立體金色「下載」按鈕。
  - 將 Logo 文字換為 `media/branding/logo_cn_black.png`。

- [ ] **Task 4: 首頁區塊去重與占位卡拔除**
  - 依照第 2.1 節之 7 大模組規劃，刪除重複出現的實機截圖滾動軌道。
  - 拔除首頁所有 `.placeholder-card`，替換為真實截圖與視覺圖卡（見第 4 節對照表）。
  - 將實機大廳截圖路徑更新為 `media/shots/proof_mobile_lobby_temple.png`。

- [ ] **Task 5: 驗證與回報**
  - 跑完所有改動後，在本機開啟瀏覽器確認無破圖、無字型漂移、手機 RWD 雙拇指握持無按鈕遮擋（熱區 ≥48px）。
  - 由阿宏於完成後提交 PR，交由美術總監（小柔）以 15 項自檢表進行視覺驗收。
