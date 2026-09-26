# 裝備與武器名稱六語系 驗收清單 (equip-name-i18n)

## 1. 任務目標
角色分頁與背包裝備格切到英／日後，槽位標題已換語言，但武器與防具名稱仍是繁中。玩家看著裝備名字對不上語系。
本任務完成：
1. `equipment.json` 現有 44 件裝備名稱在六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）下完整補齊在地化字典，涵蓋武器（28件）、防具（7件）、飾品（9件）。
2. 已有譯名的「銹劍／鏽劍」「微末之刃」「空手」維持既有譯名不重做。
3. `EquipmentSystem.display_name(inst)` 與 `EquipmentSystem.label(inst)` 支援多語系即時解析與格式化，數值、品階、強化數字保持不變。
4. `EquipPanel`（武器欄、防具槽、飾品槽、背包裝備格）支援 `Loc.locale_changed` 動態連動，裝備名稱立刻切換為該語言。
5. 大廳角色分頁在切換語言時同屏即時刷新，零系統 emoji，數值維持不變。
6. 不改數值、不改掉落、不接真金流、不產新圖、不花錢。

## 2. 交付檔案
- **系統核心與邏輯**：
  - `game/scripts/systems/equipment_system.gd`：
    - `display_name(inst)`：支援依當前語系查找 `weapon.json` / `ui.json` 取得裝備名稱，並防呆支援 base_id 備援查找與銹劍別名標準化。
    - `label(inst)`：採用 `display_name(inst)` 與多語系品質標籤，維持攻、防、暴擊等數值不變。
    - 監聽 `Loc.locale_changed` 並發出 `equipment_changed` 信號。
  - `game/scripts/autoload/game_state.gd`：
    - `weapon_display()`：支援優先查 `weapon` 域並備援查 `ui` 域。
  - `game/scripts/systems/gem_system.gd`：
    - 裝備名稱獲取改用 `EquipmentSystem.display_name(inst)`。
- **UI 面板**：
  - `game/scripts/ui/panels/equip_panel.gd`：
    - `_loadout_card`、`_slot_card`、`_bag_cell` 全面改採 `EquipmentSystem.display_name(inst)`。
    - 接 `Loc.locale_changed` 訊號，開著裝備面板切換語言即時刷新。
- **六語系詞條檔**：
  - `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/weapon.json`（44 件裝備名稱完整補齊，保留既有 3 件）
  - `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/ui.json`（同步注入 44 件裝備名稱與 4 階品質標籤）
  - `game/data/i18n/{zh_TW,zh_CN,en,ja,ko,es}.json`（同步注入 44 件裝備名稱）
- **具名單元測試**：
  - `game/scripts/systems/test_equipment_name_i18n.gd`：
    - 驗證改 locale 後，抽驗 3 件缺譯裝備（`knight_saber` 騎士軍刀、`ash_mail` 灰燼甲片、`dawn_blade` 晨光長劍）顯示名等於該語系詞條。
    - 驗證「鏽劍／銹劍」、「微末之刃」、「空手」維持既有譯名。
    - 驗證 `EquipmentSystem.label` 數值未動、名稱在地化。
    - 驗證角色分頁在 en、ja 下即時刷新，攻擊／防禦數字（95/48）維持不變。
    - 驗證 0-QA24（en/es 無中文字元殘留；ja/ko 漢字完全對齊語系檔）與零系統 emoji。
- **實機截圖腳本**：
  - `game/scripts/dev/capture_equip_name_i18n.gd`
- **實機截圖存證（0-QA23 獨立目錄）**：
  - `proofs/equip-name-i18n/proof_char_tab_en.png`（英文角色分頁全景實機，背後大廳頂欄與 Dock 同步切換 en，0-QA25）
  - `proofs/equip-name-i18n/crops/crop_char_tab_right_en.png`（英文右側武器槽與屬性小卡局部裁切）
  - `proofs/equip-name-i18n/proof_char_tab_ja.png`（日文角色分頁全景實機，背後大廳頂欄與 Dock 同步切換 ja，0-QA25）
  - `proofs/equip-name-i18n/crops/crop_char_tab_right_ja.png`（日文右側武器槽與屬性小卡局部裁切）
  - `proofs/equip-name-i18n/proof_char_tab_zh_TW.png`（繁中基準對照）
  - `proofs/equip-name-i18n/crops/crop_char_tab_right_zh_TW.png`（繁中右側武器槽與屬性小卡局部裁切）

## 3. 抽樣裝備多語系對照表

| Base ID | 槽位 | 品階 | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|---|---|
| `rusty_blade` | weapon | T1 | 鏽劍 | 锈剑 | Rusty Sword | 錆びた剣 | 녹슨 검 | Espada oxidada |
| `meager_edge` | weapon | T2 | 微末之刃 | 微末之刃 | Meager Edge | 微末の刃 | 미말의 칼날 | Filo Ínfimo |
| `knight_saber` | weapon | T3 | 騎士軍刀 | 骑士军刀 | Knight's Saber | 騎士の軍刀 | 기사의 군도 | Sable de caballero |
| `gale_edge` | weapon | T4 | 疾風刃 | 疾风刃 | Gale Edge | 疾風の刃 | 질풍의 칼날 | Filo del vendaval |
| `dawn_blade` | weapon | T5 | 晨光長劍 | 晨光长剑 | Dawn Blade | 暁光の長剣 | 여명의 장검 | Espada del alba |
| `ash_mail` | armor | T1 | 灰燼甲片 | 灰烬甲片 | Ash Scale Mail | 灰のスケイルメイル | 잿빛 비늘갑옷 | Malla de ceniza |
| `knight_plate` | armor | T3 | 騎士殘甲 | 骑士残甲 | Knight's Scrap Plate | 騎士の残甲 | 기사의 잔갑옷 | Placa de caballero |
| `star_pendant` | necklace | T1 | 星屑墜 | 星屑坠 | Stardust Pendant | 星屑のペンダント | 별빛가루 펜던트 | Colgante de polvo estelar |
| `blade_ring` | ring | T2 | 鋒勢指環 | 锋势指环 | Bladestance Ring | 鋭刃の指輪 | 검세의 반지 | Anillo de filo |
| `scar_amulet` | amulet | T3 | 疤焰護符 | 疤焰护符 | Scarfire Amulet | 傷痕の炎護符 | 흉터불꽃 호신부 | Amuleto de fuego cicatrizante |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/equip-name-i18n/`，絕無修改或覆蓋其他任務之 proof 目錄。
- [x] **0-QA24（日／韓漢字核實、英文無 CJK 殘留）**：
  - 日文實機截圖中的漢字（「機体」「戦闘」「属性」「武器」「有効戦力」「鉄の剣」「猟弓」「拳套」等）經回查 `ja/weapon.json` 與 `ja/ui.json`，均為合法之日本常用漢字與新字體規範。
  - 英文全景實機截圖經 Vision 審查確認 100% 純英文，完全無中文字元殘留。
- [x] **0-QA25（同屏即時換語系）**：
  - 在角色分頁開啟狀態下動態切換語系，角色分頁（標題、副標題、武器槽、屬性小卡）與背景大廳（頂部狀態列 Lv.10 Xiaobai/シロ、Energy/エネルギー、Gold/金、Shop/ショップ、Settings/設定；底部導航頁籤）全數 100% 同屏即時連動刷新。
- [x] **零系統 Emoji**：介面圖標皆為遊戲自定義資產與字體，無任何原生系統 Emoji。
- [x] **數值不變**：物理攻擊（95）、物理防禦（48）、生命力（520）、暴擊率（22%）、怒氣量表（20 點）數值完全維持不變。

## 5. 實機截圖清單與 MD5

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 01 | `proof_char_tab_en.png` | 角色分頁英文全景（角色卡＋武器槽＋屬性小卡＋大廳背景頂欄/Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 02 | `proof_char_tab_ja.png` | 角色分頁日文全景（角色卡＋武器槽＋屬性小卡＋大廳背景頂欄/Dock） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 03 | `proof_char_tab_zh_TW.png` | 角色分頁繁中全景基準對照 | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 繁中基準 | **通過 (PASS)** |

**MD5 雜湊唯一性查核（0-QA15 內部無重複）：**
- `proof_char_tab_en.png`: `db73e7fb32c7d7ec35d0fb6641187879`
- `proof_char_tab_ja.png`: `dbf11afd5ab6710f6eb6524d12d1ad02`
- `proof_char_tab_zh_TW.png`: `c3476aceeb7e0fb8f19aff1b670eaea0`
- `crops/crop_char_tab_right_en.png`: `e32e0abbdf9aef3285b8c43f013dea04`
- `crops/crop_char_tab_right_ja.png`: `8da744e50305c7e098bac90f1868ffb4`
- `crops/crop_char_tab_right_zh_TW.png`: `44d26d2efa5d017eecbc5ee37d6aa66a`
