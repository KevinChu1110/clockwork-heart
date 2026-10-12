# 《發條之心》背包Tab武器裝備詳情新增『拆解回收』按鈕驗收報告 (t_68937335)

- **執行工程師**：阿宏（發條之心·程式 sideworker）
- **關聯任務**：`t_68937335`（🎮 遊戲開發｜背包Tab武器裝備詳情新增『拆解回收』按鈕連動 EquipmentSystem）
- **交付存證目錄**：`proofs/t_68937335/`
- **遵循規範**：
  - `review.md` 人因人機工程與多巴胺視覺規範：按鈕高度 >= 52px（水平彈性擴充）、立體果凍厚底 5px、圓角 18px、零 Emoji、多巴胺鮮亮珊瑚粉底色（#FF5E8A 底色、#FF7B9E hover、#1F1A3A 深藍紫描邊、白色加描邊文字）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 元件佈局高度 52px，非裝備類消耗品/材料嚴格隱藏按鈕防誤觸，零折行、零溢出、零重疊。
    - 裝備鎖定（EquipmentSystem.is_locked）與穿戴中（worn/loadout）嚴格阻擋拆解並提示鎖定/穿戴狀態。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_bag_weapon_selected_zh_TW.png` | `MobileLobby` 背包Tab：選中武器【鏽劍】時，右側面板顯示珊瑚粉果凍厚底「拆解回收」按鈕（`BtnBagDismantle`，高度 52px，底邊 5px 立體厚底） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `0fe475f51380` | 合格 (PASS) |
| 02 | `proof_02_bag_consumable_selected_hidden.png` | `MobileLobby` 背包Tab：選中消耗品【微型備用齒輪】時，「拆解回收」按鈕嚴格隱藏，原按鈕列排版正常 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `bb5eeaa5e312` | 合格 (PASS) |
| 03 | `proof_03_bag_weapon_locked_disabled.png` | `MobileLobby` 背包Tab：選中已鎖定武器時，「拆解回收」按鈕切換為「已鎖定」且處於禁用狀態，下方提示「裝備已鎖定，無法拆解。」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `1ce8c6001431` | 合格 (PASS) |
| 04 | `proof_04_bag_weapon_equipped_disabled.png` | `MobileLobby` 背包Tab：選中穿戴中武器時，「拆解回收」按鈕切換為「裝備中」且處於禁用狀態，下方提示「裝備中無法拆解，請先卸下。」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `3176d19f3d04` | 合格 (PASS) |
| 05 | `proof_05_bag_weapon_selected_en.png` | 英文語系 (en) 背包Tab：選中武器時按鈕顯示 "Dismantle"，屬性顯示 "Tier: 1 Quality: Rare"，全英文無 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `d644c18916ae` | 合格 (PASS) |
| 06 | `proof_06_dismantled_toast_and_refreshed.png` | 點擊「拆解回收」後成功呼叫 `EquipmentSystem.dismantle(uid)`，獲得鐵屑與金幣，彈出獲得提示 Toast，背包與資源即時刷新 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `9093f52bdbec` | 合格 (PASS) |

- **防作弊與真實性校驗**：6 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），並經 Vision 複檢通過。
- **視覺複檢**：所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **拆解回收** | 拆解回收 | Dismantle | 分解回収 | 분해 회수 | Desmantelar |
| **已鎖定** | 已锁定 | Locked | ロック中 | 잠금됨 | Bloqueado |
| **裝備中** | 装备中 | Equipped | 装備中 | 장착 중 | Equipado |
| **裝備已鎖定，無法拆解。** | 装备已锁定，无法拆解。 | Equipment is locked and cannot be dismantled. | 装備がロックされているため分解できません。 | 장비가 잠겨 있어 분해할 수 없습니다. | El equipo está bloqueado y no se puede desmantelar. |
| **裝備中無法拆解，請先卸下。** | 装备中无法拆解，请先卸下。 | Equipped items cannot be dismantled. Please unequip first. | 装備中のため解体できません。先に外してください。 | 장착 중에는 분해할 수 없습니다. 먼저 해제해 주세요. | No se puede desmantelar mientras esté equipado. Desequípalo primero. |
| **拆解裝備回收鐵屑與金幣** | 拆解装备回收铁屑与金币 | Dismantle equipment for scrap iron and gold | 装備を分解して鉄屑とゴールドを回収 | 장비를 분해하여 철 부스러기와 골드 회수 | Desmantela equipo para obtener chatarra y oro |

---

## 三、 單元與無頭測試驗證結論

- 測試腳本：`res://scripts/ui/test_bag_dismantle_btn.gd`
- 驗證項：
  1. 按鈕存在性、高度 >= 52px、圓角 18px、5px 果凍厚底、多巴胺鮮亮珊瑚粉色盤 (#FF5E8A)、白字深藍紫描邊 (#1F1A3A)、零系統 Emoji。
  2. 未選取、消耗品 (hp_s)、材料 (iron_scrap)、重要物 (key_rusty) 嚴格隱藏按鈕。
  3. 武器 (rusty_blade)、自訂裝備 (custom_shield_test) 精確顯示按鈕。
  4. 裝備鎖定防拆：鎖定狀態按鈕禁用且顯示「已鎖定」，dismantle 呼叫被安全阻擋；解鎖後按鈕恢復啟用。
  5. 穿戴中防拆：穿戴狀態按鈕禁用且顯示「裝備中」，dismantle 呼叫被安全阻擋；卸下後按鈕恢復啟用。
  6. 成功拆解回收：鐵屑與金幣收益正確入帳，Toast 彈出，背包清單與選取狀態即時刷新。
  7. 六語系字典映射與動態切換，非繁中無 CJK 中文殘留。
- 測試結果：`TEST_BAG_DISMANTLE_BTN_OK` (100% 綠燈通過，0 SCRIPT ERROR)。
