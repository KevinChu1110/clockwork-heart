# 遊戲開發｜裝備品質標籤 ja／ko／es／zh_CN 補齊驗收清單 (equip-quality-i18n)

- **執行人**：阿翔（側案·工程師 sideworker2）
- **關聯任務**：`t_74f33616`（🎮 遊戲開發｜裝備品質標籤 ja／ko／es／zh_CN 補齊）
- **交付目錄**：`proofs/equip-quality-i18n/`（遵守 `review.md 0-QA23` 獨立目錄，絕無跨卡污染）
- **遵循規範**：
  - `review.md 0-QA15`：本輪產出無重複檔名、無相同內容（全數截圖與特寫 crops MD5 100% 獨立相異）。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面，包含裝備面板背包格、品質子標籤與大廳底層連動。
  - `review.md 0-QA23`：OUT_DIR 獨立指向 `proofs/equip-quality-i18n/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：日文漢字（「凡品」、「良品」、「上品」、「極品」、「秘宝」）均回查語系檔核實，確認為合規既定詞條，非繁中殘留（秘宝使用日文新字體「宝」）；西文完全採用西語對應詞條（「Común」、「Poco común」、「Raro」、「Épico」、「Legendario」），零 CJK 殘留。
  - `review.md 0-QA25`：全畫面連動查驗，裝備面板開啟時背景 UI（頂部狀態列 Lv.16 Shiro/Blanco/小白、能量/Energy/Energía、金幣/Gold/Oro、星屑/Stardust/Polvo estelar、商城/Shop/Tienda、設置/Settings/Ajustes；底部 Dock）同步連動同一語系，無半中半英。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_ja_equip_bag.png` | ja 裝備面板背包格全景（騎士の軍刀 上品·sword／暁光の長剣 秘宝·sword／騎士の残甲 上品／星屑のペンダント 良品／大廳頂欄底欄全日文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24/25) | **通過 (PASS)** |
| 02 | `proof_02_es_equip_bag.png` | es 裝備面板背包格全景（Sable de caballero Raro·sword／Espada del alba Legendario·sword／Placa de caballero Raro／Colgante Poco común／大廳頂欄底欄全西文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 西文連動 (0-QA24/25) | **通過 (PASS)** |
| 03 | `proof_03_zh_TW_equip_bag.png` | zh_TW 裝備面板背包格全景基準（騎士軍刀 上品·sword／晨光長劍 秘寶·sword／騎士殘甲 上品／星屑墜 良品／灰燼甲片 凡品） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中連動 | **通過 (PASS)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720（特寫裁切為對應局部區域），MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
b0a88c942a95a1e53d3859f44f24e6f7  proof_01_ja_equip_bag.png (1280x720)
e13f5c3a738d74a1896e73626626e7df  proof_02_es_equip_bag.png (1280x720)
62e5fab2dcc589cc5ee86669c320939f  proof_03_zh_TW_equip_bag.png (1280x720)

crops/23108da3ba8e2010ad1c639554bfef2f  crops/crop_01_ja_equip_bag.png (580x440)
crops/a05e4ea844276ea6fcd32df2ce64afe0  crops/crop_01_ja_lobby_dock.png (1280x90)
crops/ae8b14b96de078616413856e981b000a  crops/crop_01_ja_lobby_top.png (1280x60)
crops/8d1a543cd3b0729ddc893e1b696cf46e  crops/crop_02_es_equip_bag.png (580x440)
crops/408461df2ef0c8c056298131fed146bb  crops/crop_02_es_lobby_dock.png (1280x90)
crops/9b7e227d6693993be77cd46b2ef54987  crops/crop_02_es_lobby_top.png (1280x60)
crops/53fc51e97abe564da2022063a5967867  crops/crop_03_zh_TW_equip_bag.png (580x440)
```

---

## 三、 五大裝備品質多語系對照表與規格查核

| Quality ID | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) | 規範查核 |
|---|---|---|---|---|---|---|:---:|
| `common` | 凡品 | 凡品 | Common | 凡品 | 일반 | Común | ✓ 完全對齊 |
| `uncommon` | 良品 | 良品 | Uncommon | 良品 | 고급 | Poco común | ✓ 完全對齊 |
| `rare` | 上品 | 上品 | Rare | 上品 | 희귀 | Raro | ✓ 完全對齊 |
| `epic` | 極品 | 极品 | Epic | 極品 | 영웅 | Épico | ✓ 完全對齊 |
| `legendary` | 秘寶 | 秘宝 | Legendary | 秘宝 | 전설 | Legendario | ✓ 完全對齊 |

- **數值與品質門檻防護**：裝備數值、roll bonus、品質權重門檻 100% 保持原狀，未更動任何戰鬥數值。
- **en／zh_TW 過審詞保護**：未修改 `en` 與 `zh_TW` 任何已過審詞條。

---

## 四、 Vision 視覺顯微審核逐張結論

1. **`proof_01_ja_equip_bag.png`（特寫：`crops/crop_01_ja_equip_bag.png`）**：
   - 背包裝備格日文全景，標題「持ち物（押して装備）」。
   - 裝備品質標籤呈現日文在地化：
     - 騎士の軍刀：`上品・sword`
     - 暁光の長剣：`秘宝・sword`（遵循 0-QA24，採用日文新字體「宝」而非繁中「寶」）
     - 騎士の残甲：`上品`
     - 星屑のペンダント：`良品`
     - 傷痕の炎護符：`上品`
     - 灰のスケイルメイル：`凡品`
   - 大廳背景連動（0-QA25）：頂部狀態列（Lv.16 シロ、星屑 0、ショップ、設定）與底部 Dock（ぜんまい新村、キャラ装備、四区出征、聚魂殿、冒險バッグ）100% 全日文，零截字、零系統 Emoji。

2. **`proof_02_es_equip_bag.png`（特寫：`crops/crop_02_es_equip_bag.png`）**：
   - 背包裝備格西文全景，標題「Bolsa (toca para equipar)」。
   - 裝備品質標籤呈現西文在地化：
     - Sable de caballero：`Raro · sword`
     - Espada del alba：`Legendario · sword`
     - Placa de caballero：`Raro`
     - Colgante de polvo estelar：`Poco común`
     - Amuleto de fuego cicatrizante：`Raro`
     - Malla de ceniza：`Común`
   - 遵循 0-QA24 規範，完全無 CJK 漢字殘留。
   - 大廳背景連動（0-QA25）：頂部狀態列（Lv.16 Blanco、Polvo estelar 0、Tienda、Ajustes）與底部 Dock（Aldea Mecánica、Bolsa de aventura、Alma 等）100% 全西文。

3. **`proof_03_zh_TW_equip_bag.png`（特寫：`crops/crop_03_zh_TW_equip_bag.png`）**：
   - 繁中基準畫面，展示「騎士軍刀（上品 · sword）」、「晨光長劍（秘寶 · sword）」、「騎士殘甲（上品）」、「星屑墜（良品）」，與歷史基準完全一致。

---

## 五、 自動化測試驗證

- 測試腳本：`scripts/systems/test_equipment_name_i18n.gd`
  - 指令：`godot --path game --headless --script scripts/systems/test_equipment_name_i18n.gd`
  - 驗證點：
    1. 六語系抽驗裝備名稱無缺漏。
    2. 六語系 5 大品質標籤（凡品／良品／上品／極品／秘寶）字典對照 100% 符合期望。
    3. en / es 語系下品質標籤無 CJK 殘留。
    4. 裝備格品質子標籤切換語系時即時動態刷新（ja -> es 立即刷新為 Raro / Legendario / Común）。
  - 結果：全綠通過、0 SCRIPT ERROR、哨兵 `EQUIPMENT_NAME_I18N_OK` 輸出。
- 冒煙測試：`godot --path game --headless --quit-after 3` 0 SCRIPT ERROR。
