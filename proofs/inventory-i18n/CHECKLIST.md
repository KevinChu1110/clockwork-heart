# 《發條之心》背包物品欄標題按鈕與類型說明六語系 查驗清單與驗收報告 (t_d92206e6)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_d92206e6`（🎮 遊戲開發｜背包物品欄標題按鈕與類型說明六語系）
- **交付目錄**：`proofs/inventory-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/inventory-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名，非中文殘留。
  - `review.md 0-QA25`：查驗彈窗以外背景語系狀態，大廳頂部狀態列、右側裝備出征卡片與底部 Dock 全數呈現同語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_inventory_en.png` | 背包物品欄（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_inventory_ja.png` | 背包物品欄（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |

---

## 二、 語系對照與詞條清單

所有玩家可見文字均透過 `Loc.t()` / `_t()` 對接 `game/data/i18n/content/<locale>/ui.json`：

| 來源原文 (zh_TW) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) | 簡體中文 (zh_CN) |
|---|---|---|---|---|---|
| 物品欄 | Inventory | インベントリ | 소지품 | Inventario | 物品栏 |
| 冒險者背包 · 點選格子查看詳情 | Adventurer's Bag · Tap slot to view details | 冒険者のバッグ · マスをタップして詳細確認 | 모험가의 배낭 · 슬롯을 눌러 상세 확인 | Bolsa de aventurero · Toca una casilla para ver detalles | 冒险者背包 · 点击格子查看详情 |
| 冒險者背包 | Adventurer's Bag | 冒険者のバッグ | 모험가의 배낭 | Bolsa de aventurero | 冒险者背包 |
| 使用 / 賣出 | Use / Sell | 使う / 売却 | 사용 / 판매 | Usar / Vender | 使用 / 出售 |
| 放到快捷欄 | Assign to Hotbar | ショートカットに登録 | 단축칸에 등록 | Asignar a acceso rápido | 放入快捷栏 |
| 左鍵點選查看 · 雙擊或右鍵快速使用 | Click to view · Double-click or right-click to quick use | クリックで確認 · ダブルクリックか右クリックで即時使用 | 클릭하여 확인 · 더블 클릭 또는 우클릭으로 빠른 사용 | Clic para ver · Doble clic o clic derecho para uso rápido | 左键点击查看 · 双击或右键快速使用 |
| 請點選左側格子查看道具詳情。 | Please select a slot on the left to view item details. | 左側のマスを選択して道具の詳細を確認してください。 | 왼쪽 슬롯을 선택하여 아이템 상세를 확인하세요. | Selecciona una casilla de la izquierda para ver los detalles del objeto. | 请点击左侧格子查看道具详情。 |
| 消耗品：使用回復狀態 | Consumable: Use to restore stats | 消耗品：使用して状態を回復 | 소모품: 사용하여 상태 회복 | Consumible: Usar para recuperar estado | 消耗品：使用恢复状态 |
| 素材：點擊使用可賣出金幣 | Material: Click use to sell for gold | 素材：使うをクリックしてゴールドで売却 | 재료: 사용을 눌러 골드로 판매 | Material: Pulsa usar para vender por oro | 素材：点击使用可出售金币 |
| 重要物：劇情關鍵道具 | Key Item: Story-critical item | 重要品：ストーリー重要アイテム | 중요 아이템: 스토리 핵심 아이템 | Objeto clave: Objeto crucial para la historia | 重要物：剧情关键道具 |
| 消耗品 | Consumable | 消耗品 | 소모품 | Consumible | 消耗品 |
| 素材（點擊使用可賣出） | Material (Click Use to Sell) | 素材（使うをクリックで売却） | 재료 (사용 클릭 시 판매) | Material (Pulsa usar para vender) | 素材（点击使用可出售） |
| 重要道具 | Key Item | 重要アイテム | 중요 아이템 | Objeto clave | 重要道具 |
| 類型：%s | Type: %s | タイプ：%s | 유형: %s | Tipo: %s | 类型：%s |

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元測試**：
   - `test_maple_inventory.gd`：包含彈窗尺寸（740~760px）、按鈕尺寸（>=50px）、24 格物品欄、零系統 emoji、格子選取明細連動、以及**六語系 (en, ja, ko, es, zh_CN, zh_TW) 即時動態切換 `Loc.locale_changed` 完整驗證通過**（`MAPLE_INVENTORY_OK`）。
   - `test_dialog_contrast.gd`：對比度與壓明度規範檢查通過（`DIALOG_CONTRAST_OK`）。
3. **Vision 模型審查**：
   - `proof_inventory_en.png` 與 `proof_inventory_ja.png` 親自開圖審查。
   - 標題、副標、按鈕、提示與道具類型標籤均已完整對應翻譯，無硬編繁中殘留。
   - 背後大廳背景、頂部資源列（Gold/Shop/Settings 或 金/ショップ/設定）、右側裝備出征面板與底部 Dock 皆同步為同一語系，嚴格落實 0-QA25 規範。
   - 日文漢字完全依據語系檔，採當用漢字/新字體（如：鉄屑、売却、登録、冒険、タイプ），符合 0-QA24 規範。
