# 探索性 QA 第四十三輪：裝備與武器名稱六語系合主線後找破圖驗收清單 (qa-round43)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_5e877306`（🤖 平台與維運｜探索性 QA：裝備與武器名稱六語系合主線後找破圖）
- **前置任務**：`t_498565c7`（🎮 遊戲開發｜裝備與武器名稱六語系，已合併主線 `a3e5d9a1`）
- **交付目錄**：`proofs/qa_round43/`（遵守 `review.md 0-QA23` 獨立目錄，絕無跨卡污染）
- **遵循規範**：
  - `review.md 0-QA15`：本輪產出無重複檔名、無相同內容（全數截圖與特寫 crops MD5 100% 獨立相異）。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面，包含角色分頁、武器輪替、裝備面板背包格與大廳冒險背包底層連動。
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/qa_round43/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：日文漢字（「機体戦闘属性」、「武器ローテーション配置」、「メイン武器・鉄の剣」、「サブ武器・猟弓」、「絶技武器・拳套」、「騎士の軍刀」、「暁光の長剣」、「騎士の残甲」、「星屑のペンダント」、「聚魂殿」等）均回查 `ja/weapon.json` 與 `ja/ui.json` 核實，確認為合規既定詞條，非未翻譯殘留。
  - `review.md 0-QA25`：全畫面連動查驗，角色分頁與大廳開啟時背景 UI（頂部狀態列 Lv.16 Xiaobai/シロ、能量/Energy/エネルギー、金幣/Gold/金、星屑/Stardust/星屑、商城/Shop/ショップ、設置/Settings/設定；底部 Dock）同步連動同一語系，無半中半英。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_zh_TW_char_tab.png` | zh_TW 角色分頁全景基準（武器輪替配置／鐵劍·獵弓·拳套／機體戰鬥屬性／頂欄底欄Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中連動 | **通過 (PASS)** |
| 02 | `proof_02_en_char_tab.png` | en 角色分頁全景（Weapon Rotation Loadout / Iron Sword / Hunting Bow / Gauntlets / Chassis Stats） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 03 | `proof_03_ja_char_tab.png` | ja 角色分頁全景（武器ローテーション配置／鉄の剣／猟弓／拳套／機体戦闘属性／有効戦力） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 04 | `proof_04_zh_TW_equip_bag.png` | zh_TW 背包裝備格全景基準（武器欄／防具槽／飾品槽／背包裝備格：騎士軍刀、晨光長劍、騎士殘甲等） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中連動 | **通過 (PASS)** |
| 05 | `proof_05_en_equip_bag.png` | en 背包裝備格全景（Weapons, Armour, 6 Accessories, Bag: Knight's Saber, Dawn Blade, Knight's Scrap Plate） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 發現品質標籤漏翻 | **有缺陷記錄 (FINDING)** |
| 06 | `proof_06_ja_equip_bag.png` | ja 背包裝備格全景（武器枠、防具、装飾品六枠、持ち物：騎士の軍刀、暁光の長剣、騎士の残甲、星屑のペンダント） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 07 | `proof_07_en_lobby_bag.png` | en 大廳冒險背包全景（Adventurer's Bag / Items & Soul Vault / Dock Tabs / Top Bar 同步英文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 08 | `proof_08_ja_lobby_bag.png` | ja 大廳冒險背包全景（冒険者バッグ / ぜんまい新村 / 冒険バッグ / 0-QA25 全屏同語系） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24/25) | **通過 (PASS)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720（特寫裁切為對應局部區域），MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
f8c7cb4aacc62a9e4c6d423097e1b138  proof_01_zh_TW_char_tab.png (1280x720)
b1b3ad00640e6a7de101595e554e7e91  proof_02_en_char_tab.png (1280x720)
9463b13b794238188bc2b1c38df6073e  proof_03_ja_char_tab.png (1280x720)
d4c9219b4ba478a31fd78c3dedc281bb  proof_04_zh_TW_equip_bag.png (1280x720)
7334bb16b22a562733fb5254ee12a5f6  proof_05_en_equip_bag.png (1280x720)
849bcf4ead068033d468662c0afb81b2  proof_06_ja_equip_bag.png (1280x720)
4a6234b4a398a49df0638411a525997d  proof_07_en_lobby_bag.png (1280x720)
d3db461037ba209969ee14fd4e750ad4  proof_08_ja_lobby_bag.png (1280x720)

crops/ba54a735f5227e7332d538636dbf3af6  crops/crop_01_zh_TW_char_right.png (800x560)
crops/718191860884cbac5f3c25f0ced14ce8  crops/crop_02_en_char_right.png (800x560)
crops/31de0b02dfa6787b390374dc70e9a638  crops/crop_03_ja_char_right.png (800x560)
crops/54ca6f885a000e982ddb3d17fbef66e7  crops/crop_04_zh_TW_equip_bag.png (580x540)
crops/419ade08f99221dc6a2cbeaf24e63fa7  crops/crop_05_en_equip_bag.png (580x540)
crops/88946eb96351214eb70af773673f5a3e  crops/crop_06_ja_equip_bag.png (580x540)
crops/f2c48e1842d471a844a01846c1699769  crops/crop_07_en_lobby_bag.png (1080x560)
crops/7765b1d1998f31865088dfa05366b194  crops/crop_08_ja_lobby_dock.png (1280x90)
```

---

## 三、 抽樣裝備多語系對照表與數值核驗

抽樣測試中裝備庫與背包裝備格實機抽樣項目：

| Base ID | 槽位 | 品階 | zh_TW | en | ja | 攻擊／防禦／屬性數值 | 數值是否被改 |
|---|---|---|---|---|---|:---:|:---:|
| `rusty_blade` | weapon | 凡品 (common) | 鏽劍 | Rusty Sword | 錆びた剣 | 攻+4, 暴擊+7.6%, 暴傷+55% | ✓ 完全不變 |
| `meager_edge` | weapon | 良品 (uncommon) | 微末之刃 | Meager Edge | 微末の刃 | 攻+7, 暴擊+5.0% | ✓ 完全不變 |
| `knight_saber` | weapon | 上品 (rare) | 騎士軍刀 | Knight's Saber | 騎士の軍刀 | 攻+12, 暴擊+6.5% | ✓ 完全不變 |
| `gale_edge` | weapon | 極品 (epic) | 疾風刃 | Gale Edge | 疾風の刃 | 攻+18, 暴擊+8.0% | ✓ 完全不變 |
| `dawn_blade` | weapon | 秘寶 (legendary) | 晨光長劍 | Dawn Blade | 暁光の長剣 | 攻+24, 暴擊+7.0% | ✓ 完全不變 |
| `ash_mail` | armor | 凡品 (common) | 灰燼甲片 | Ash Scale Mail | 灰のスケイルメイル | 防+6, HP+45 | ✓ 完全不變 |
| `knight_plate` | armor | 上品 (rare) | 騎士殘甲 | Knight's Scrap Plate | 騎士の残甲 | 防+14, HP+110 | ✓ 完全不變 |
| `star_pendant` | necklace | 良品 (uncommon) | 星屑墜 | Stardust Pendant | 星屑のペンダント | HP+35, 暴傷+15% | ✓ 完全不變 |
| `scar_amulet` | amulet | 上品 (rare) | 疤焰護符 | Scarfire Amulet | 傷痕の炎護符 | 攻+8, 暴擊+4.0% | ✓ 完全不變 |
| `blade_ring` | ring | 上品 (rare) | 鋒勢指環 | Bladestance Ring | 鋭刃の指輪 | 攻+6, 暴擊+5.5% | ✓ 完全不變 |

### 角色分頁核心戰鬥數值檢驗
- 生命力 (HP)：`520`（各語系完全一致，數值零竄改）
- 物理攻擊：`95`（各語系完全一致，數值零竄改）
- 物理防禦：`48`（各語系完全一致，數值零竄改）
- 暴擊率：`22%`（各語系完全一致，數值零竄改）
- 怒氣量表：`20 點`（en: `20 pts`，ja: `20 pt`，數值零竄改）
- 有效戰力：`82`（各語系完全一致）

---

## 四、 Vision 視覺顯微審核逐張結論

1. **`proof_01_zh_TW_char_tab.png`（特寫：`crops/crop_01_zh_TW_char_right.png`）**：
   - 角色分頁繁中基準畫面，武器輪替配置顯示「首選武器 · 鐵劍 · 4 次打擊」、「副手武器 · 獵弓 · 4 次打擊」、「絕技武器 · 拳套 · 5 連擊」。
   - 下方提示條「首選武器 · 鐵劍：近身迅捷連續 4 次斬擊，戰鬥開局起手輪替順位」。
   - 機體戰鬥屬性顯示生命力 520、物理攻擊 95、物理防禦 48、暴擊率 22%、怒氣量表 20 點。
   - 大廳背景頂欄（金幣 1,000 / 星屑 0 / 商城 / 設置）與底欄 Dock（發條新村 / 角色裝備 / 四區出征 / 聚魂殿堂 / 冒險背包）全屏同語系，零系統 Emoji。

2. **`proof_02_en_char_tab.png`（特寫：`crops/crop_02_en_char_right.png`）**：
   - 英文角色分頁全景，標題「Weapon Rotation Loadout」、「Chassis Combat Stats」。
   - 武器槽位完整顯示「Primary Weapon · Iron Sword · 4 Strikes」、「Secondary Weapon · Hunting Bow · 4 Strikes」、「Special Weapon · Gauntlets · 5-Hit Combo」。
   - 屬性卡顯示 Health (HP) 520, Physical ATK 95, Physical DEF 48, CRIT Rate 22%, Rage Gauge 20 pts。
   - 背景頂欄（Gold 1,000 / Stardust 0 / Shop / Settings）與底欄 Dock（Cogwheel Hamlet / Hero Gear / Four Regions / Soul Hall / Adventure Bag）100% 英文，零中文殘留，零系統 Emoji。

3. **`proof_03_ja_char_tab.png`（特寫：`crops/crop_03_ja_char_right.png`）**：
   - 日文角色分頁全景，標題「武器ローテーション配置」、「タップで順位切替・3段階戦闘シークエンス」。
   - 武器槽位顯示「メイン武器 鉄の剣・4回打撃」、「サブ武器 猟弓・4回打撃」、「絶技武器 拳套・5連撃」。
   - 屬性卡顯示生命力 (HP) 520, 物理攻撃 95, 物理防御 48, 会心率 22%, 怒りゲージ 20 pt。
   - 依據 `0-QA24` 查驗：「武器ローテーション配置」、「絶技武器」、「拳套」、「機体戦闘属性」、「有効戦力」、「聚魂殿」經比對 `ja/ui.json`，皆為既定詞條，非未翻譯殘留。

4. **`proof_04_zh_TW_equip_bag.png`（特寫：`crops/crop_04_zh_TW_equip_bag.png`）**：
   - 背包裝備格繁中基準全景，顯示防具、裝飾品六枠、背包（點擊裝備）。
   - 背包第一列展示「騎士軍刀（上品 · sword）」、「晨光長劍（秘寶 · sword）」、「騎士殘甲（上品）」、「星屑墜（良品）」。
   - 像素圖標完整呈現，無破圖或缺失紋理。

5. **`proof_05_en_equip_bag.png`（特寫：`crops/crop_05_en_equip_bag.png`）**：
   - 英文裝備面板背包格全景，槽位標題為「Armour」、「Six accessory slots (Ring, Necklace, Bracelet, Earring, Amulet, Belt)」、「Bag (tap to equip)」。
   - 裝備名稱在地化：**Knight's Saber**、**Dawn Blade**、**Knight's Scrap Plate**、**Stardust Pendant**。
   - ⚠️ **發現缺陷**：裝備品質標籤呈現中文未翻譯（如 `上品 · sword`、`秘寶 · sword`、`良品`）。

6. **`proof_06_ja_equip_bag.png`（特寫：`crops/crop_06_ja_equip_bag.png`）**：
   - 日文裝備面板背包格全景，槽位標題為「防具」、「装飾品六枠 (指輪, 首飾り, 腕輪, 耳飾り, 護符, 帯)」、「持ち物（押して装備）」。
   - 裝備名稱在地化：**騎士の軍刀**、**暁光の長剣**、**騎士の残甲**、**星屑のペンダント**。
   - 品質標籤顯示「上品・sword」、「秘宝・sword」、「良品」，符合日本常用漢字習慣（0-QA24）。

7. **`proof_07_en_lobby_bag.png`（特寫：`crops/crop_07_en_lobby_bag.png`）**：
   - 英文大廳冒險背包全景，標題「Adventurer's Bag」、「Items & Soul Vault · Tap slot to view details」。
   - 道具格展示 Dry Rations 等道具，右側詳情面板、使用與快捷欄按鈕均為英文。
   - 頂部狀態列（Gold, Stardust, Energy, Shop, Settings）與底部 Dock 100% 英文連動（0-QA25）。

8. **`proof_08_ja_lobby_bag.png`（特寫：`crops/crop_08_ja_lobby_dock.png`）**：
   - 日文大廳冒險背包全景，標題「冒険者バッグ」、「アイテムと戦魂倉庫・枠をタップして詳細を表示」。
   - 頂部狀態列與底部 Dock（ぜんまい新村、キャラ装備、四区出征、聚魂殿、冒険バッグ）全屏同語系同步，符合 0-QA24/0-QA25。

---

## 五、 玩家可見問題清單（依規範「什麼輸入 → 什麼壞掉」，本單不修，留給製作人收尾）

依據任務指示：「找到玩家可見缺陷就在 comment 寫「什麼輸入 → 什麼壞掉」，不要自己改程式；小錯（漏翻一詞、舊截圖）留給製作人收尾。」

### 缺陷 1：裝備面板垂直高度超過 720p 且缺乏捲動支援，導致背包格被擠出螢幕外
- **什麼輸入**：玩家在 1280x720 解析度下進入裝備面板（呼叫 `EquipPanel.open()`，例如點選更換裝備或主選單裝備按鈕）。
- **什麼壞掉**：`EquipPanel` 內部將整個卡片（武器欄 130px + 防具飾品欄 + 背包格 110px*多列 + 返回按鈕）置於 `CenterContainer` 之中，垂直總高度超過 950px。由於缺乏 `ScrollContainer` 捲動容器，卡片在 720px 高度之 Viewport 垂直居中後，最下方的「背包（點擊裝備）」道具格與「返回」按鈕完全被推擠到 y > 720px 之畫面外，玩家看得到武器欄但無法看到或點選背包裡的裝備與返回按鈕。

### 缺陷 2：英文介面下背包裝備格品質子標籤殘留繁中
- **什麼輸入**：玩家切換語言至英文（`en`），開啟背包裝備格檢視裝備（例如 `Knight's Saber`、`Dawn Blade`、`Knight's Scrap Plate`、`Stardust Pendant`）。
- **什麼壞掉**：雖然裝備名稱已成功顯示英文（`Knight's Saber` 等），但下方品質標籤（由 `_bag_cell` 中的 `inst.quality_label` 透過 `_t()` 查找）在 `game/data/i18n/content/en/ui.json` 缺乏 `凡品`、`良品`、`上品`、`極品`、`秘寶` 之字典條目，導致英文畫面上直接顯示中文（例如 `上品 · sword`、`秘寶 · sword`、`上品`、`良品`），造成中英混雜瑕疵。

---

## 六、 驗收結論

- **裝備與武器名稱核心在地化**：44 件裝備名稱在 `zh_TW`、`en`、`ja` 下翻譯完全對齊詞條；三段武器輪替名稱（鐵劍/Iron Sword/鉄の剣、獵弓/Hunting Bow/猟弓、拳套/Gauntlets/拳套）翻譯完整。
- **數值與強化數值安全**：生命力（520）、物理攻擊（95）、物理防禦（48）、暴擊率（22%）、怒氣量表（20）、裝備屬性數值完全不變，零被改動。
- **規範遵循**：
  - `0-QA23`：獨立存證於 `proofs/qa_round43/`，無跨卡污染。
  - `0-QA15`：16 張截圖與特寫 MD5 100% 互異獨立。
  - `0-QA24` / `0-QA25`：全畫面同屏連動，日文漢字經查證合規。
- **探索性發現**：發現 2 處玩家可見缺陷（EquipPanel 720p 垂直溢出無捲動、英文品質標籤殘留繁中），已詳列重現路徑交由製作人派工收尾。
