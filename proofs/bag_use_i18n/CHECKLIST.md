# 背包使用／出售／重要物品提示六語系 驗收清單 (bag_use_i18n)

## 1. 任務目標
在背包或快捷欄使用道具、賣掉素材、點到重要物品時，畫面上那句提示要跟語系走。切到英／日／韓／西／簡中時不要還跳出繁中「使用失敗」「賣出某某」「重要物品不能消耗」。

## 2. 交付檔案
- 系統核心：`game/scripts/systems/inventory_system.gd`
  - 增加 `static func _t(s: String) -> String`
  - `use_item()`、`use_hotbar_slot()`、`sell_all_materials()` 回傳字串全面改走 `ContentLoc.text("ui", ...)`
- 大廳背包 UI：`game/scripts/ui/mobile_lobby.gd`
  - `_on_bag_use_pressed`、右鍵與雙擊透過 `_show_bag_msg(res)` 彈出動態 toast 提示
  - 重要物品時 `_bag_use_btn` 保持可點擊（文字為「無法使用」），點擊時即時彈出「重要物品不能消耗」多語系警示
  - `_show_toast` 加入單例管理與動態寬度計算，避免多次點擊重疊疊字或長文字溢出
- 六語系字典擴充（各補增 16 組鍵，無系統 emoji、無 AI 腔）：
  - `game/data/i18n/content/zh_TW/ui.json`
  - `game/data/i18n/content/zh_CN/ui.json`
  - `game/data/i18n/content/en/ui.json`
  - `game/data/i18n/content/ja/ui.json`
  - `game/data/i18n/content/ko/ui.json`
  - `game/data/i18n/content/es/ui.json`
- 具名單元測試：`game/scripts/systems/test_bag_use_i18n.gd`
- 實機截圖腳本：`game/scripts/dev/capture_bag_use_i18n.gd`

## 3. 六語系字典映射對照表

| Key | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|
| `使用【%s】· %s` | `使用【%s】· %s` | `使用【%s】· %s` | `Used [%s] · %s` | `【%s】を使用 · %s` | `【%s】 사용 · %s` | `Usaste [%s] · %s` |
| `使用【%s】` | `使用【%s】` | `使用【%s】` | `Used [%s]` | `【%s】を使用` | `【%s】 사용` | `Usaste [%s]` |
| `賣出【%s】· 金 +%d` | `賣出【%s】· 金 +%d` | `出售【%s】· 金 +%d` | `Sold [%s] · gold +%d` | `【%s】を売却 · 金 +%d` | `【%s】 판매 · 골드 +%d` | `Vendiste [%s] · oro +%d` |
| `【%s】是重要物品，不能消耗。` | `【%s】是重要物品，不能消耗。` | `【%s】是重要物品，不能消耗。` | `[%s] is a key item and cannot be consumed.` | `【%s】は重要アイテムのため消費できません。` | `【%s】(은)는 중요 아이템이므로 소모할 수 없습니다.` | `[%s] es un objeto clave y no se puede consumir.` |
| `使用失敗。` | `使用失敗。` | `使用失败。` | `Failed to use.` | `使用に失敗しました。` | `사용에 실패했습니다.` | `Error al usar.` |
| `賣出失敗。` | `賣出失敗。` | `出售失败。` | `Failed to sell.` | `売却に失敗しました。` | `판매에 실패했습니다.` | `Error al vender.` |
| `沒有這個道具。` | `沒有這個道具。` | `没有这个道具。` | `Item not found.` | `該当のアイテムがありません。` | `해당 아이템이 없습니다.` | `El objeto no existe.` |
| `無法使用。` | `無法使用。` | `无法使用。` | `Cannot be used.` | `使用できません。` | `사용할 수 없습니다.` | `No se puede usar.` |
| `第 %d 格是空的。開 I 背包指派道具。` | `第 %d 格是空的。開 I 背包指派道具。` | `第 %d 格是空的。按 I 打开背包指定道具。` | `Slot %d is empty. Open bag (I) to assign items.` | `スロット %d は空です。I キーでバッグを開いて道具を登録してください。` | `슬롯 %d이(가) 비어 있습니다. I 키로 배낭을 열어 아이템을 등록하세요.` | `La casilla %d está vacía. Abre la bolsa (I) para asignar un objeto.` |
| `沒有可賣的材料。` | `沒有可賣的材料。` | `没有可出售的材料。` | `No sellable materials.` | `売却できる素材がありません。` | `판매할 수 있는 재료가 없습니다.` | `No hay materiales para vender.` |
| `賣出材料 %d 件 · 金 +%d` | `賣出材料 %d 件 · 金 +%d` | `出售材料 %d 件 · 金 +%d` | `Sold %d materials · gold +%d` | `素材を %d 個売却 · 金 +%d` | `재료 %d개 판매 · 골드 +%d` | `Vendiste %d materiales · oro +%d` |
| `星屑 +%d` | `星屑 +%d` | `星屑 +%d` | `Stardust +%d` | `星屑 +%d` | `별가루 +%d` | `Polvo estelar +%d` |
| `HP +%d` | `HP +%d` | `HP +%d` | `HP +%d` | `HP +%d` | `HP +%d` | `HP +%d` |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/bag_use_i18n/`，無修改或覆蓋其他卡片之 proof。
- [x] **0-QA24（非中文無中文殘留）**：
  - 英文截圖中，Toast 提示為 `[Friendship Key] is a key item and cannot be consumed.` 及 `Sold [Scrap Iron] · gold +6`，零 CJK 漢字殘留。
  - 使用具備向量 PNG 圖標的 `friendship_key`，避免純文字佔位符漢字。
- [x] **0-QA25（彈窗以外同屏同步換語系）**：
  - 實機截圖中，頂部 Header、大廳背景、底部 Dock（Cogwheel Hamlet, Hero Gear, Four Regions, Soul Hall, Adventure Bag）均同步切換為英文與日文，無繁中殘留。
- [x] **零系統 Emoji**：所有介面與 toast 均無系統 emoji。

## 5. 實機截圖存證清單
- `proof_01_key_item_en.png`：英文版重要物品提示全景截圖
- `crops/crop_01_key_item_en.png`：英文版重要物品提示與道具詳情裁切圖
- `proof_02_sell_item_en.png`：英文版售出材料提示全景截圖
- `crops/crop_02_sell_item_en.png`：英文版售出材料提示與道具詳情裁切圖
- `proof_03_key_item_ja.png`：日文版重要物品提示全景截圖
- `crops/crop_03_key_item_ja.png`：日文版重要物品提示與道具詳情裁切圖
- `proof_04_sell_item_ja.png`：日文版售出材料提示全景截圖
- `crops/crop_04_sell_item_ja.png`：日文版售出材料提示與道具詳情裁切圖
- `proof_05_key_item_zh_TW.png`：繁體中文基準對照全景截圖
- `crops/crop_05_key_item_zh_TW.png`：繁體中文基準對照裁切圖

## 6. 測試執行命令
```bash
# 冒煙與無 SCRIPT ERROR 驗證
godot --path game --headless --quit-after 3

# 具名六語系單元測試
godot --path game --headless -s res://scripts/systems/test_bag_use_i18n.gd

# 既有回歸測試
godot --path game --headless -s res://scripts/ui/test_lobby_bag_i18n.gd
godot --path game --headless -s res://scripts/battle/test_battle_items.gd
godot --path game --headless -s res://scripts/systems/test_daily_tracks.gd
```
