# 大廳背包未選格六語系驗收清單 (t_e9dd14a7)

## 驗收規範依據
- 依據 `AGENTS.md` / `CLAUDE.md` 及 `review.md`：
  - 0-QA23：具備實機截圖與具名測試
  - 0-QA24：切換至 en、ja 等外語時，介面無繁體中文殘留
  - 0-QA25：同屏所有文字即時切換同一語系
  - 0-QA08：零系統 emoji，改用純淨文字或自繪圖示

## 驗證項目

### 1. 未選格說明六語系映射
| 語系 | 標題 | 請點選格子提示 | 消耗品說明 | 素材說明 | 重要物說明 |
|---|---|---|---|---|---|
| zh_TW | 冒險者背包 | 請點選左側格子查看道具詳情。 | 消耗品：使用回復狀態 | 素材：點擊使用可賣出金幣 | 重要物：劇情關鍵道具 |
| zh_CN | 冒险者背包 | 请点击左侧格子查看道具详情。 | 消耗品：使用恢复状态 | 素材：点击使用可出售金币 | 重要物：剧情关键道具 |
| en | Adventurer's Bag | Please select a slot on the left to view item details. | Consumable: Use to restore stats | Material: Click use to sell for gold | Key Item: Story-critical item |
| ja | 冒険者のバッグ | 左側のマスを選択して道具の詳細を確認してください。 | 消耗品：使用して状態を回復 | 素材：使うをクリックしてゴールドで売却 | 重要品：ストーリー重要アイテム |
| ko | 모험가의 배낭 | 왼쪽 슬롯을 선택하여 아이템 상세를 확인하세요. | 소모품: 사용하여 상태 회복 | 재료: 사용을 눌러 골드로 판매 | 중요 아이템: 스토리 핵심 아이템 |
| es | Bolsa de aventurero | Selecciona una casilla de la izquierda para ver los detalles del objeto. | Consumible: Usar para recuperar estado | Material: Pulsa usar para vender por oro | Objeto clave: Objeto crucial para la historia |

### 2. 同屏相關元件即時刷新
| 元件 | zh_TW | en | ja |
|---|---|---|---|
| 背包標題 | 冒險者背包 | Adventurer's Bag | 冒険者のバッグ |
| 背包副標 | 道具與戰魂倉庫 · 點選格子查看詳情 | Item & Soul Storage · Tap slot to view details | 道具と戦魂の倉庫 · マスをタップして詳細確認 |
| 使用/賣出按鈕 | 使用 / 賣出 | Use / Sell | 使う / 売却 |
| 快捷欄按鈕 | 放到快捷欄 | Assign to Hotbar | ショートカットに登録 |
| 底部提示 | 點選格子查看詳情 · 雙擊或點擊按鈕使用 | Tap slot to view details · Double-tap or press button to use | マスをタップして詳細確認 · ダブルタップまたはボタンで使用 |

### 3. 單元測試與無頭冒煙
- 具名單元測試：`game/scripts/ui/test_lobby_bag_i18n.gd`（`LOBBY_BAG_I18N_OK` 通過）
- 大廳回歸測試：`TEST_FILTER=lobby ./tools/run_tests.sh` 5/5 全數 PASS
- 無頭冒煙測試：`godot --path game --headless --quit-after 3` 0 腳本錯誤（0 SCRIPT ERROR）

### 4. 實機截圖存檔
- `proofs/lobby-bag-i18n/proof_bag_unselected_en.png`（英文背包未選格全景）
- `proofs/lobby-bag-i18n/proof_bag_unselected_ja.png`（日文背包未選格全景）
- `proofs/lobby-bag-i18n/proof_bag_unselected_zh_TW.png`（繁中背包未選格全景）
- `proofs/lobby-bag-i18n/crops/crop_bag_detail_en.png`（英文右側說明細節）
- `proofs/lobby-bag-i18n/crops/crop_bag_detail_ja.png`（日文右側說明細節）
- `proofs/lobby-bag-i18n/crops/crop_bag_detail_zh_TW.png`（繁中右側說明細節）
