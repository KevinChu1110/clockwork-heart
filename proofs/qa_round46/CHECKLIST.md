# 探索性 QA 第四十六輪：六語系與裝備面板合主線後實機巡檢存證報告

- **任務編號**：`t_b14c60c0`
- **專案代號**：`qa-round46`（探索性 QA：六語系與裝備面板合主線後找破圖）
- **受檢主線版本**：commit `829c3922`（已包含六語系、裝備面板折行修復、W8 Hub 殼、過場字幕提示、大廳戳碰氣泡與聚魂完畢提示）
- **交付目錄**：`proofs/qa_round46/`（遵守 `review.md 0-QA23` 獨立專屬目錄，絕無跨卡覆蓋）
- **測試環境**：Godot 4.7.1.stable.official.a13da4feb, OpenGL3 Compatibility Renderer, Xvfb 1280x720x24

---

## 一、驗收規範審核結果 (review.md)

1. **`review.md 0-QA15`（查重與 MD5 唯一性）**：
   - 本輪產出 15 張全景實機截圖與 15 張局部 Crops，全數經 MD5 查核，100% 獨立相異，無重複命名、無重複內容。
2. **`review.md 0-QA17`（實機規格 1280x720）**：
   - 全景截圖全數為 1280x720 實機渲染幀緩衝（Framebuffer），非概念圖或設計稿。
3. **`review.md 0-QA23`（OUT_DIR 獨立目錄防護）**：
   - OUT_DIR 嚴格限定為 `proofs/qa_round46/`，未修改、覆蓋或干擾任何其他任務之 proof 目錄。
4. **`review.md 0-QA24`（多語系既定譯名與漢字回查）**：
   - 日文漢字（「凡品」「良品」「上品」「極品」「秘宝」「玩具の山の縁」「初回クリアと掃討」「聚魂完了」等）已回查 `ja.json` 與 `content/ja/ui.json` 核實，確認採用日本當用漢字與新字體規範（如「宝」非繁中「寶」），非繁中殘留。
   - 韓文、西文、簡體中文詞條亦經回查語系檔，確認符合既定譯名。
5. **`review.md 0-QA25`（全畫面多語系同步連動）**：
   - 查驗全景截圖中，同屏之大廳背景、頂部狀態列（Lv.16 / 角色名 / 能量 / 金幣 / 星屑 / 商城 / 設置）及底部導航 Dock（五大頁籤）同步連動目標語系，無局部殘留繁中之情形。

---

## 二、實機全景截圖清單（15 張 1280x720，MD5 100% 獨立）

| 截圖檔名 | 語系代碼 | 巡檢功能畫面 | 驗收核心重點 | MD5 |
|---|---|---|---|---|
| `proof_01_ja_equip_quality.png` | `ja` | 裝備品質標籤 | 凡品/良品/上品/極品/秘宝（新字體宝），大廳頂底欄同步 ja (0-QA25) | `37ff44dd3b8a6a6a57e3f8a032d201c1` |
| `proof_02_ko_equip_quality.png` | `ko` | 裝備品質標籤 | 일반/고급/희귀/영웅/전설，零 CJK 殘留，大廳頂底欄同步 ko (0-QA25) | `8d38e7720dd3ba67e9f3b584d436a546` |
| `proof_03_es_equip_quality.png` | `es` | 裝備品質標籤 | Común/Poco común/Raro/Épico/Legendario，零 CJK，大廳頂底欄同步 es (0-QA25) | `72242617f300c3b52d3a246944e5ce67` |
| `proof_04_zh_CN_equip_quality.png` | `zh_CN` | 裝備品質標籤 | 凡品/良品/上品/极品/秘宝，簡中字形無繁中殘留，大廳同步 zh_CN (0-QA25) | `e62fe9a2fb6bc6594dcf4d8eb3487c6f` |
| `proof_05_en_equip_wrap.png` | `en` | 裝備面板折行保護 | Bladestance Ring 單字中不折行，Rare 標籤在框內無溢出，大廳同步 en (0-QA25) | `c26c43f2bbccca05fc1a8684bbd4177e` |
| `proof_06_zh_TW_equip_weapon.png` | `zh_TW` | 裝備面板武器類型 | 上品 · 劍、秘寶 · 劍，無未翻譯英文 sword 殘留，大廳繁中基準 | `8762ea882672bfbb30f81a700da617d5` |
| `proof_07_en_w8_hub.png` | `en` | W8 Hub 殼章節介面 | 橫幅 Toy-pile Edge、章節資訊、4 操作按鈕、日常事件全英文化，零 emoji | `1d3b163e198b598d9ba8feaa14828135` |
| `proof_08_ja_w8_hub.png` | `ja` | W8 Hub 殼即時刷新 | 開著畫面動態切換語系即時刷新 (0-QA25)，日文漢字合規 (0-QA24) | `071f6733827ec31a6136d8f8045cf188` |
| `proof_09_desktop_zh_TW_cutscene.png` | `zh_TW` | 過場字幕繼續提示 | 桌面模式呈現「▼ 點擊 / Space 繼續」，右下角對齊對話框，零 emoji | `a2b6e7f26629ae9e075fc98d1a10408d` |
| `proof_10_touch_en_cutscene.png` | `en` | 過場字幕繼續提示 | 觸控模式呈現「▼ Tap to continue」，對齊對話框，零 emoji | `93f8704d0b115456f91d5fc67d4f901a` |
| `proof_11_touch_ja_cutscene.png` | `ja` | 過場字幕繼續提示 | 觸控模式呈現「▼ タップで進む」，對齊對話框，零 emoji | `96d79bc5b244799017ae7a44f568e64c` |
| `proof_12_en_lobby_poke.png` | `en` | 大廳主角戳碰氣泡 | 氣泡文字 The wind-up key on my back...，大廳底層同步 en (0-QA25) | `2a2be92017c6a6f1ea4b016f407b8a73` |
| `proof_13_ja_lobby_poke.png` | `ja` | 大廳主角戳碰氣泡 | 氣泡文字 背中のゼンマイが回る限り...，大廳底層同步 ja (0-QA25) | `c08fbdcedcb8ee590130cc2f02ea26ff` |
| `proof_14_ja_lobby_toast.png` | `ja` | 聚魂完畢浮動提示 | 提示文字 聚魂完了！戦魂の欠片と戦魂経験を獲得！，大廳同步 ja (0-QA25) | `cf5a5ee2811a76c67bf338bf3e7b1659` |
| `proof_15_zh_TW_lobby_toast.png` | `zh_TW` | 聚魂完畢浮動提示 | 提示文字 聚魂完畢！已獲得戰魂碎片與戰魂經驗！，繁中基準 | `fa1858de19b52479e0ba395f1fa69e06` |

---

## 三、特寫 Crops 清單（15 張局部細節對照）

- `crop_01_ja_equip_quality.png` (580x440): ja 裝備網格品質標籤（上品・剣 / 秘宝・剣 / 上品 / 良品 / 凡品）
- `crop_02_ko_equip_quality.png` (580x440): ko 裝備網格品質標籤（희귀 · 검 / 전설 · 검 / 희귀 / 고급 / 일반）
- `crop_03_es_equip_quality.png` (580x440): es 裝備網格品質標籤（Raro · Espada / Legendario · Espada / Raro / Poco común / Común）
- `crop_04_zh_CN_equip_quality.png` (580x440): zh_CN 裝備網格品質標籤（上品·剑 / 秘宝·剑 / 上品 / 良品 / 凡品）
- `crop_05_en_equip_wrap.png` (170x160): en 裝備網格第 6 格 Bladestance Ring 單字不折行與 Rare 標籤邊界安全
- `crop_06_zh_TW_equip_weapon.png` (250x150): zh_TW 裝備網格武器欄位（上品 · 劍 / 秘寶 · 劍，無 sword 殘留）
- `crop_07_en_w8_hub.png` (1240x680): en W8 Hub 殼全域資訊卡片與操作按鈕群
- `crop_08_ja_w8_hub.png` (1240x680): ja W8 Hub 殼動態切換後即時刷新資訊卡片與操作按鈕群
- `crop_09_desktop_zh_TW_cutscene.png` (460x80): zh_TW 桌面模式過場提示「▼ 點擊 / Space 繼續」
- `crop_10_touch_en_cutscene.png` (460x80): en 觸控模式過場提示「▼ Tap to continue」
- `crop_11_touch_ja_cutscene.png` (460x80): ja 觸控模式過場提示「▼ タップで進む」
- `crop_12_en_lobby_poke.png` (460x150): en 大廳主角戳碰氣泡與稱號標籤
- `crop_13_ja_lobby_poke.png` (460x150): ja 大廳主角戳碰氣泡與稱號標籤
- `crop_14_ja_lobby_toast.png` (720x110): ja 頂部聚魂完畢提示橫幅「聚魂完了！戦魂の欠片と戦魂経験を獲得！」
- `crop_15_zh_TW_lobby_toast.png` (720x110): zh_TW 頂部聚魂完畢提示橫幅「聚魂完畢！已獲得戰魂碎片與戰魂經驗！」

---

## 四、探索性 QA 缺陷與優化建議（遵循「只寫什麼輸入 → 什麼壞掉，不准改程式」）

### 【缺陷 1】大廳主角戳碰長英文台詞右側緊貼邊界邊緣
- **什麼輸入**：語系設為 `en`，在大廳點擊主角觸發戳碰台詞 1（`_current_speech_index = 1`，台詞內容："The wind-up key on my back is wound just right, let's go!"）。
- **什麼壞掉**：該英文字串共 58 字元，在動態字級 13px 下單行寬度接近 260px 氣泡框之有效內寬。字串末端字母「o」及驚嘆號「!」緊貼氣泡框最右側圓角邊線，右側安全邊距不足 2px。若字串稍長或遇到更長名稱，文字將溢出或折損。
- **建議改進方向（交由工程師處理）**：`mobile_lobby.gd` 的 `_speech_label` 建議增加 `autowrap_mode = TextServer.AUTOWRAP_WORD_SMART`，或氣泡外框寬度依字長動態計算/提供合適 padding。

### 【缺陷 2】裝備卡片白色名稱文字在淺底色卡片上對比度偏低（無障礙體驗建議）
- **什麼輸入**：開啟裝備面板（所有語系，如 ja、ko、zh_CN、zh_TW），檢視背包物品欄卡片。
- **什麼壞掉**：卡片底色為米白／極淺粉白色（`#FFFDF8`），其上之道具名稱（如「騎士の軍刀」「기사의 군도」「骑士军刀」）採用白色字體，文字與背景色差（Contrast Ratio）極低，在強光或手機螢幕上辨讀較吃力。
- **建議改進方向（交由工程師處理）**：道具名稱文字建議改為深深藍紫（如主題描邊色 `#1F1A3A`）或深棕色，或加入深色文字陰影/描邊。

---

## 五、結論與驗收判定

本輪實機巡檢涵蓋 6 大合併項目、15 張全景實機截圖與 15 張 Crops，經 `verify_qa_round46.py` 自動化工具量測與 Vision 逐圖審查：
1. 裝備品質標籤六語系完整合規，日韓西簡無繁中殘留。
2. 裝備面板英文單字無折行截斷、繁中無殘留 sword。
3. W8 Hub 殼全域玩家可見字六語系在地化且支援即時動態刷新。
4. 過場字幕繼續提示依輸入設備與語系切換正常，精準對齊對話框。
5. 全場景 100% 零系統 Emoji、無致命破圖。
6. 巡檢發現之 2 項視覺/排版微調點已明確記錄為缺陷清單。
