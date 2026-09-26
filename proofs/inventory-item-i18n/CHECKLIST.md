# 背包道具名稱與說明六語系 驗收清單 (inventory-item-i18n)

## 1. 任務目標
背包物品欄標題／按鈕已六語系，但格子上的道具名稱與說明仍寫死繁中（`inventory_system` 資料表 name／desc），切語系詳情與快捷欄不變。本任務完成：
1. `item_name`／`item_desc`（或同等顯示路徑）改走 ContentLoc，資料表繁中當 key，並在各語系 `ui.json` 補齊對照，同時補齊 `zh_TW/item.json`。
2. 接 `Loc.locale_changed`，開著背包／快捷欄切語系，名稱、說明、tooltip、選單標籤立刻換。
3. 六語系詞條完整補齊（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）。
4. 涵蓋現在會顯示給玩家的道具（22 件），零系統 emoji，不改動道具數值、恢復量、堆疊、賣價。
5. 背包與快捷欄 chrome（大標題、使用、出售、類型說明、操作提示）保持既有手遊人體工學與多巴胺配色規範。

## 2. 交付檔案
- **系統核心**：`game/scripts/systems/inventory_system.gd`
  - `catalog(id)`：支援 ContentLoc 六語系翻譯及以繁中為 key 的 fallback 查找
  - `item_name(id)` / `item_desc(id)`：提供多語系名稱與說明獲取介面
  - `bag_list()`：回傳已在地化的 `def`，使下游所有 UI 讀取皆能自動獲得多語系資料
  - `_connect_loc_signal()`：監聽 `Loc.locale_changed`，即時發出 `inventory_changed` 與 `hotbar_changed`
- **UI 彈窗與元件**：
  - `game/scripts/ui/maple_inventory.gd`：
    - 格子 cell 支援多語系 `tooltip_text`
    - 無圖標道具支援 `glyph` 多語系在地化
    - 詳情區域 `_detail` 安全防護與 `_update_detail` 語系即時切換
  - `game/scripts/ui/maple_hotbar.gd`：
    - 接 `Loc.locale_changed`，即時更新「選單 / Menu / メニュー」按鈕文字與各 slot tooltip
- **六語系詞條檔**：
  - `game/data/i18n/content/zh_TW/item.json`（補齊繁中基準 22 件道具定義）
  - `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/item.json`（22 件道具全部具備）
  - `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/ui.json`（同步注入 22 件道具繁中為 key 之名稱與說明對照，以及「選單」與 glyph）
- **具名單元測試**：`game/scripts/systems/test_inventory_item_i18n.gd`
  - 驗證建背包後改 locale，抽驗至少 3 件（`hp_s`, `iron_scrap`, `key_rusty`）道具名稱與說明符合該語系詞條
  - 驗證 `MapleInventory` 與 `MapleHotbar` 動態切換語系即時生效
  - 驗證 0-QA24（en/es 無中文字元殘留；ja/ko 漢字完全對齊語系檔）與零系統 emoji
- **實機截圖腳本**：`tools/capture_inventory_item_i18n.gd`
- **實機截圖存證（0-QA23 獨立目錄）**：
  - `proofs/inventory-item-i18n/proof_01_inventory_item_en.png`（英文全景實機，背後大廳與快捷欄同步切換 en，0-QA25）
  - `proofs/inventory-item-i18n/crops/crop_01_inventory_item_en.png`（英文背包彈窗局部裁切）
  - `proofs/inventory-item-i18n/proof_02_inventory_item_ja.png`（日文全景實機，背後大廳與快捷欄同步切換 ja，0-QA25）
  - `proofs/inventory-item-i18n/crops/crop_02_inventory_item_ja.png`（日文背包彈窗局部裁切）
  - `proofs/inventory-item-i18n/proof_03_inventory_item_zh_TW.png`（繁中全景基準對照）
  - `proofs/inventory-item-i18n/crops/crop_03_inventory_item_zh_TW.png`（繁中背包彈窗局部裁切）

## 3. 抽樣道具多語系對照表

| Item ID | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|
| `hp_s` | 小紅水 | 小红水 | Small Red Draught | 小さな赤い水 | 작은 붉은 물 | Poción roja pequeña |
| `hp_s` (desc) | 恢復 25 生命。 | 恢复 25 生命。 | Restores 25 health. | 生命を 25 回復。 | 생명을 25 회복. | Restaura 25 de vida. |
| `bread` | 乾糧 | 干粮 | Dry Rations | 干し飯 | 마른 양식 | Ración seca |
| `bread` (desc) | 恢復 15 生命。路上充飢。 | 恢复 15 生命。路上充饥。 | Restores 15 health. Something for the road. | 生命を 15 回復。道中の腹の足し。 | 생명을 15 회복. 길에서 요기용. | Restaura 15 de vida. Algo para el camino. |
| `iron_scrap` | 鐵屑 | 铁屑 | Scrap Iron | 鉄屑 | 철 부스러기 | Chatarra de hierro |
| `iron_scrap` (desc) | 鍛造基礎材。鐵匠與商店都收。 | 锻造基础材。铁匠与商店都收。 | Basic forging material. Both the smith and the shop buy it. | 鍛造の基礎素材。鍛冶屋も店も買い取る。 | 제작 기초재. 대장장이도 상점도 사들인다. | Material básico de forja. Lo compran el herrero y la tienda. |
| `key_rusty` | 鏽劍（紀念） | 锈剑（纪念） | Rusty Sword (keepsake) | 錆びた剣（記念） | 녹슨 검（기념） | Espada oxidada (recuerdo) |
| `key_rusty` (desc) | 霧廊入口撿起的那把。已鍛成正器後仍留念。 | 雾廊入口捡起的那把。已锻成正器后仍留念。 | The one you picked up at the mist-gallery mouth. Kept even after it was forged proper. | 霧廊の入口で拾ったあの一振り。正式に鍛え直したあとも手元に。 | 안개회랑 어귀에서 주운 그 한 자루. 제대로 벼린 뒤에도 간직. | La que recogiste a la entrada de la galería de niebla. La guardas aun tras forjarla en condiciones. |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/inventory-item-i18n/`，絕無修改或覆蓋其他任務之 proof（如 `proofs/inventory/`、`proofs/inventory-i18n/` 等舊檔案均完整保留未更動）。
- [x] **0-QA24（日／韓漢字核實、英文無 CJK 殘留）**：
  - 日文實機截圖中的漢字（「干し飯」、「回復」、「道中の腹の足し」、「使う / 売却」、「登録」、「ぜんまい」等）經回查 `ja/item.json` 與 `ja/ui.json`，確認均為合法之日本常用漢字與新字體規範，用語自然道地。
  - 英文全景實機截圖經 Vision 審查確認 100% 純英文，完全無中文字元殘留（glyph 亦在地化為字母 "S"）。
- [x] **0-QA25（彈窗以外同屏同步換語系）**：
  - 在背包開啟狀態下動態切換語系，背包彈窗內部（標題、副標題、道具名、道具說明、按鈕、操作提示）與背景 UI（頂部狀態列 Gold/Stardust/Shop/Settings、右側裝備與出征、底部導航頁籤、底部快捷欄選單 Menu/メニュー）全數 100% 同屏即時連動刷新。
- [x] **零系統 Emoji**：介面圖標皆為遊戲自定義資產與字體，無任何原生系統 Emoji。

## 5. 實機截圖清單與 MD5

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 01 | `proof_01_inventory_item_en.png` | 背包道具英文全景（彈窗＋大廳背景頂欄/出征/Dock/快捷欄Menu） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 02 | `proof_02_inventory_item_ja.png` | 背包道具日文全景（彈窗＋大廳背景頂欄/出征/Dock/快捷欄メニュー） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 03 | `proof_03_inventory_item_zh_TW.png` | 背包道具繁中全景基準對照 | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 繁中基準 | **通過 (PASS)** |

**MD5 雜湊唯一性查核（0-QA15 內部無重複）：**
- `proof_01_inventory_item_en.png`: `04abd95656fb5af05205e0ead4d83d6a`
- `proof_02_inventory_item_ja.png`: `bffcc440615a8421e7a651575b3db545`
- `proof_03_inventory_item_zh_TW.png`: `7514a92afa678a2e8136722c213ff6ca`
- `crops/crop_01_inventory_item_en.png`: `a42610a6af173ef7e256f4d0aa911c93`
- `crops/crop_02_inventory_item_ja.png`: `9f804e7ad7c3ef871eeb10ffb6656ebf`
- `crops/crop_03_inventory_item_zh_TW.png`: `b45703f9e48ad04b348a601cd6ac9f5d`
