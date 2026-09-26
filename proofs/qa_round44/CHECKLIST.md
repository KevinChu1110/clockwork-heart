# 探索性 QA 第四十四輪：武術館十二流派六語系合主線後找破圖驗收清單 (qa-round44)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_ddabe756`（🤖 平台與維運｜探索性 QA：武術館十二流派六語系合主線後找破圖）
- **前置任務**：`t_9d4df0da`（🎮 遊戲開發｜武術館兵器架十二流派名稱與說明六語系，已合併主線 `ec3322d5`）
- **交付目錄**：`proofs/qa_round44/`（遵守 `review.md 0-QA23` 獨立目錄，絕無跨卡污染）
- **遵循規範**：
  - `review.md 0-QA15`：本輪產出無重複檔名、無相同內容（全數截圖與特寫 crops MD5 100% 獨立相異）。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面，包含兵器架十二顆按鈕「短名·稱號」、選定後玩法句與第一條優點對話框、目前流派狀態連動。
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/qa_round44/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄（如 `proofs/weapon-classes-i18n/` 等舊檔案均完整保留未更動）。
  - `review.md 0-QA24`：日文漢字（「武器系統（6職×2）」、「現在：弓・レンジャー・弓・Lv1」、「剣・騎士・剣」、「長槍・騎士・槍」、「遊び方」、「戦魂は聚魂殿で」等）均回查 `ja.json`、`craft.json` 與 `content/ja/weapon_class.json` 核實，確認為合規既定詞條，非未翻譯殘留。
  - `review.md 0-QA25`：全畫面連動查驗，兵器架彈窗標題、引言說明、目前流派狀態、流派按鈕、底層對話框及大廳 chrome 均同步連動同一語系，無半中半英。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_en_sword_rack.png` | en 兵器架全景（Weapon system (6 classes × 2) / Currently: Sword · Knight · Sword · Lv1 / 12 流派按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 02 | `proof_02_en_sword_chosen_dialog.png` | en 選定劍對話框全景（System / Playstyle: Close to mid range... / Balanced offense and defense...） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 發現雙句號標點 | **有缺陷記錄 (FINDING)** |
| 03 | `proof_03_ja_bow_rack.png` | ja 兵器架全景（武器系統（6職×2） / 現在：弓・レンジャー・弓・Lv1 / 12 流派按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 04 | `proof_04_ja_bow_chosen_dialog.png` | ja 選定弓對話框全景（システム / 遊び方：間合いを取って安全圏から射貫く... / 安全な長距離から安定して攻撃） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 發現雙句號標點 | **有缺陷記錄 (FINDING)** |
| 05 | `proof_05_zh_TW_sword_rack.png` | zh_TW 兵器架基準全景（武器系統（6職×2） / 目前：劍·騎士·劍 · Lv1 / 12 流派按鈕） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中連動 | **通過 (PASS)** |
| 06 | `proof_06_zh_TW_sword_chosen_dialog.png` | zh_TW 選定劍對話框基準全景（系統 / 玩法：近身中距離... / 攻防平均，最好上手） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 發現雙句號標點 | **有缺陷記錄 (FINDING)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720（特寫裁切為對應局部區域），MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
be33f555ea266df8d2ad13de857e123d  proof_01_en_sword_rack.png (1280x720)
b08ed85a3b828a5010cd11112afd9dd0  proof_02_en_sword_chosen_dialog.png (1280x720)
3c76daaa0d7a0e36a4ca11bf84f4fd1b  proof_03_ja_bow_rack.png (1280x720)
b5fdb973a7c6327d2807b6fc12d588ec  proof_04_ja_bow_chosen_dialog.png (1280x720)
eede64795c84f7deace6d6243d0300ae  proof_05_zh_TW_sword_rack.png (1280x720)
df8eda325fdc6254d89b005fda32e274  proof_06_zh_TW_sword_chosen_dialog.png (1280x720)

crops/5e28df52a87565316c1e73ee6766043a  crops/crop_01_en_sword_buttons.png (920x560)
crops/2f5955cf3efeba3316e117921d520f23  crops/crop_02_en_sword_dialog.png (1220x270)
crops/3747c3c6b19473b0d74650021cf24d5b  crops/crop_03_ja_bow_buttons.png (920x560)
crops/cde6582dbf4ebbaab3e34eab6fad1844  crops/crop_04_ja_bow_dialog.png (1220x270)
crops/44a4397988099f555e2e1b3a61172c8d  crops/crop_05_en_header_status.png (1280x90)
crops/7ac4ec588f2fbce91a3391d24907436e  crops/crop_06_ja_header_status.png (1280x90)
crops/218f9cfb46e2a3d58a4854bc5fd21801  crops/crop_07_zh_TW_buttons.png (920x560)
crops/b636d7a621a3c7be888dbe32ddaaed7d  crops/crop_08_zh_TW_dialog.png (1220x270)
```

---

## 三、 十二流派六語系名稱、說明與數值完整核驗表

全數 12 流派均已抽檢比對 `zh_TW`、`en`、`ja`（及 `zh_CN`、`ko`、`es`），按鈕字樣符合「短名 · 稱號」，數值未被竄改：

| 流派 ID | 職業 | zh_TW 按鈕（短名·稱號） | en 按鈕（短名·稱號） | ja 按鈕（短名·稱號） | 玩法句 (Play) 與 第一優點 (Pro0) 多語系狀態 | 基礎數值 (atk/def/hp/crit/spd) | 數值是否被改 |
|:---:|:---:|---|---|---|---|:---:|:---:|
| `sword` | 騎士 | 劍·騎士·劍 | Sword · Knight · Sword | 剣・騎士・剣 | zh_TW/en/ja 完整對齊，en 絕非單字母 S | 2 / 1 / 0 / 1.0 / 0 | ✓ 完全未改 |
| `spear` | 騎士 | 長槍·騎士·槍 | Spear · Knight · Spear | 長槍・騎士・槍 | zh_TW/en/ja 完整對齊，中距離控制說明齊備 | 3 / 2 / 2 / 0.5 / 0 | ✓ 完全未改 |
| `axe` | 維京 | 斧·維京·斧 | Axe · Viking · Axe | 斧・ヴァイキング・斧 | zh_TW/en/ja 完整對齊，單下高傷特點明確 | 4 / 1 / 2 / 0.5 / -1 | ✓ 完全未改 |
| `hammer` | 維京 | 鎚·維京·鎚 | Hammer · Viking · Hammer | 槌・ヴァイキング・槌 | zh_TW/en/ja 完整對齊，高防高血說明齊備 | 1 / 4 / 12 / 0.0 / 0 | ✓ 完全未改 |
| `dagger` | 忍者 | 匕首·忍者·匕 | Dagger · Ninja · Dagger | 短剣・忍者・短剣 | zh_TW/en/ja 完整對齊，近身急刺特點明確 | 3 / 0 / -4 / 4.0 / 2 | ✓ 完全未改 |
| `dart` | 忍者 | 鏢·忍者·鏢 | Dart · Ninja · Dart | 鏢・忍者・鏢 | zh_TW/en/ja 完整對齊，連擊殘像說明齊備 | 2 / 0 / -2 / 3.5 / 3 | ✓ 完全未改 |
| `fist` | 武鬥 | 拳·武鬥·拳 | Fist · Monk · Fist | 拳・武闘・拳 | zh_TW/en/ja 完整對齊，貼身連打破勢說明齊備 | 1 / 1 / 4 / 1.5 / 2 | ✓ 完全未改 |
| `claw` | 武鬥 | 爪·武鬥·爪 | Claw · Monk · Claw | 爪・武闘・爪 | zh_TW/en/ja 完整對齊，爪痕連切特點明確 | 2 / 0 / 2 / 2.5 / 2 | ✓ 完全未改 |
| `magic` | 法師 | 杖·法師·杖 | Staff · Mage · Staff | 杖・法師・杖 | zh_TW/en/ja 完整對齊，技能高倍率特點明確 | 1 / -1 / -2 / 2.5 / 0 | ✓ 完全未改 |
| `crystal` | 法師 | 水晶·法師·晶 | Crystal · Mage · Crystal | 水晶・法師・晶 | zh_TW/en/ja 完整對齊，護盾陣地特點明確 | 0 / 3 / 10 / 1.0 / 0 | ✓ 完全未改 |
| `bow` | 遊俠 | 弓·遊俠·弓 | Bow · Ranger · Bow | 弓・レンジャー・弓 | zh_TW/en/ja 完整對齊，遠距安全射擊特點明確 | 2 / 0 / -4 / 3.0 / 1 | ✓ 完全未改 |
| `gun` | 遊俠 | 火槍·遊俠·銃 | Gun · Ranger · Gun | 銃・レンジャー・銃 | zh_TW/en/ja 完整對齊，極限爆發特點明確 | 5 / -1 / -6 / 4.0 / 0 | ✓ 完全未改 |

### 官網與外部資料守護
- `web/data/weapon_classes.json`：未被修改（Git log 最近修改為 2026-09-15 鎚系出手調整），完全無變動。

---

## 四、 Vision 視覺顯微審核逐張結論

1. **`proof_01_en_sword_rack.png`（特寫：`crops/crop_01_en_sword_buttons.png`、`crops/crop_05_en_header_status.png`）**：
   - 英文版兵器架全景，頂欄標題「Weapon system (6 classes × 2)」。
   - 引言說明三行：「Two weapon sets per class, neither primary. Techniques follow the weapon in hand.」、「Gear from Ding, souls from Starreader, skills from Greybeard.」、「Now: Sword · Knight · Sword · Lv1」，完整正確。
   - 選定按鈕顯示高亮亮黃色「Sword · Knight · Sword」，其餘依序顯示「Spear · Knight · Spear」、「Axe · Viking · Axe」、「Hammer · Viking · Hammer」、「Dagger · Ninja · Dagger」、「Dart · Ninja · Dart」、「Fist · Monk · Fist」等。
   - 徹底清除單字母「S」，無任何系統 Emoji，無破圖，無文字重疊。

2. **`proof_02_en_sword_chosen_dialog.png`（特寫：`crops/crop_02_en_sword_dialog.png`）**：
   - 英文版選定劍流派時的彈出對話框，發話人「System」，提示「▼ Click / Space to continue」。
   - 對話文本：「Playstyle: Close to mid range, alternating normal strikes and rage skills. The spear is also playable in this class.. Balanced offense and defense, easiest to master」。
   - 玩法句與第一條優點完整載入，無字型破損、無跑版；但發現句中出現贅餘標點 `.. `（見下節缺陷紀錄）。

3. **`proof_03_ja_bow_rack.png`（特寫：`crops/crop_03_ja_bow_buttons.png`、`crops/crop_06_ja_header_status.png`）**：
   - 日文版兵器架全景，標題「武器系統（6職×2）」。
   - 引言說明三行：「各職に武器二系統、主副の別なし。技は手にした武器に従う。」、「器は釘釘、魂は星読、技は灰鬚。」、「現在：弓・レンジャー・弓・Lv1」。
   - 流派按鈕依序顯示「剣・騎士・剣」、「長槍・騎士・槍」、「斧・ヴァイキング・斧」、「槌・ヴァイキング・槌」、「短剣・忍者・短剣」、「鏢・忍者・鏢」、「拳・武闘・拳」、「爪・武闘・爪」。
   - 依 `0-QA24` 回查語系檔，日文漢字完全符合 `ja.json` 定義，無繁中殘留，零系統 Emoji。

4. **`proof_04_ja_bow_chosen_dialog.png`（特寫：`crops/crop_04_ja_bow_dialog.png`）**：
   - 日文版選定弓流派時的彈出對話框，發話人「システム」，提示「▼ クリック / Space で進む」。
   - 對話文本：「遊び方：間合いを取って安全圏から射貫く。同職で銃も扱える。。安全な長距離から安定して攻撃」。
   - 玩法句與第一條優點完整載入；發現句中出現贅餘雙句號 `。。`，且末尾缺少句點（見下節缺陷紀錄）。

5. **`proof_05_zh_TW_sword_rack.png` 與 `proof_06_zh_TW_sword_chosen_dialog.png`**：
   - 繁中版作為基準驗收，兵器架顯示「目前：劍·騎士·劍 · Lv1」，對話框顯示「選定武器流派【劍·騎士·劍】」，按鈕與引言排版標準無異常。

---

## 五、 探索性 QA 缺陷發現記錄（Player-Visible Findings）

依據任務指示：「找到玩家可見缺陷就在 comment 寫『什麼輸入 → 什麼壞掉』，不要自己改程式；小錯（漏翻一詞、舊截圖）留給製作人收尾。」

### 缺陷 1：選定流派確認對話框出現贅餘雙標點符號（雙句號）
- **輸入 (Input)**：在武術館兵器架點擊任意流派按鈕（例如點擊劍或弓），觸發 `_set_path_and_back` 並播放 `forge.path_chosen` 對話。
- **壞掉現象 (Defect)**：
  - **en 語系**：對話框顯示 `Playstyle: Close to mid range, alternating normal strikes and rage skills. The spear is also playable in this class.. Balanced offense and defense, easiest to master`，句中出現兩個點 `.. `。
  - **ja 語系**：對話框顯示 `遊び方：間合いを取って安全圏から射貫く。同職で銃も扱える。。安全な長距離から安定して攻撃`，句中出現兩個句號 `。。`，且後方優點句末未加句號。
  - **zh_TW 語系**：對話框顯示 `玩法：近身中距離，普攻和怒氣技輪著來。同職也可玩槍。。攻防平均，最好上手`，同樣出現雙句號 `。。`。
- **根本原因 (Root Cause)**：
  `game/data/dialogues/*/craft.json` 中的模板定義為：
  - en: `"Playstyle: {play}. {pro}"`
  - ja: `"遊び方：{play}。{pro}"`
  - zh_TW: `"玩法：{play}。{pro}"`
  而 `weapon_class.json` 中各流派之 `play` 詞條結尾已包含原生標點符號（如 `。` 或 `.`），字串替換後導致標點重複疊加。
- **建議收尾 (Recommendation)**：由製作人在 `craft.json` 中將模板調整為 `{play} {pro}` 或在 `main.gd` 傳入前將 `play` 尾部句點修剪（strip）。
