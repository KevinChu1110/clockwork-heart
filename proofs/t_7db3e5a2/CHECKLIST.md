# 《發條之心》天宮鐵匠武器槽新增『更換裝備』按鈕連動 WeaponSwapDialog 查驗清單與驗收報告 (t_7db3e5a2)

- **審查卡號**：`t_7db3e5a2`
- **對應模組**：`ForgeDialog` (`game/scripts/ui/forge_dialog.gd`)、`WeaponSwapDialog` (`game/scripts/ui/weapon_swap_dialog.gd`)、`MobileLobby` (`game/scripts/ui/mobile_lobby.gd`)
- **審查標準**：完全遵循多巴胺鮮亮高飽和色盤、手遊人體工學規範、0-QA5 / 0-QA26 / 0-QA28（六語系無缺詞、零Emoji、真實 OpenGL3 Framebuffer 截圖存證）

---

## 1. 核心驗收標準對齊

| 項目 | 規範標準 | 實作情況 | 驗收結果 |
|---|---|---|---|
| **更換裝備立體果凍按鈕** | 位於武器鍛造區當前槽位標題列（`WeaponStatusHead`），尺寸高度 >= 48px，熱區 >= 48px，圓角 18px，天藍果凍厚底 5px，深藍紫描邊 2px，零系統 Emoji | `BtnSwapWeapon`：`custom_minimum_size = Vector2(110, 48)`，天藍色立體果凍厚底 5px、圓角 18px、深藍紫描邊 2px、字級 16px 粉圓體，零 Emoji | **合格 (PASS)** |
| **點擊連動開啟 WeaponSwapDialog** | 點擊後發出 `swap_weapon_requested` 信號，並連動開啟武器庫更換裝備彈窗 `WeaponSwapDialog` | 點擊 `BtnSwapWeapon` 觸發 `_on_swap_weapon_pressed`，發射 `swap_weapon_requested(slot_idx)`，並順暢實例化載入 `WeaponSwapDialog` 置於前層展示 | **合格 (PASS)** |
| **換裝閉環原地刷新** | 選取新武器換裝發出 `weapon_swapped` 後，`ForgeDialog` 原地接收事件並更新當前槽位裝備、攻擊力數值、三欄槽位標籤與鍛造狀態 | `_on_weapon_swapped_from_dialog` 原地更新槽位裝備並同步呼叫 `_sync_state_from_weapon()`、`_refresh_display()` 與 `_refresh_all_forge_core_slots()`，轉發 `weapon_swapped` 信號 | **合格 (PASS)** |
| **六語系即時在地化切換** | 支援 zh_TW, zh_CN, en, ja, ko, es 六語系即時切換，字級 >= 16px，無缺詞，歐美語系零 CJK 殘留 | 六語系精確對齊：繁中「更換裝備」、簡中「更换装备」、英文「Change Equipment」、日文「装備変更」、韓文「장비 교체」、西文「Cambiar equipo」，即時切換零刷新破版 | **合格 (PASS)** |
| **無頭單元測試與回歸測試** | 附專屬無頭單元測試腳本，既有測試無回歸破壞 | `test_forge_swap_weapon_dialog.gd`：`TEST_FORGE_SWAP_WEAPON_DIALOG_OK` (PASS)；forge 相關 12/12 TESTS PASSED | **合格 (PASS)** |

---

## 2. 實機 Framebuffer 截圖存證清單 (OpenGL3, 1280x720)

所有截圖皆為 OpenGL3 渲染驅動於 1280x720 下真實 Framebuffer 輸出，經 SHA256 驗證彼此獨立無重複：

| 編號 | 檔案名稱 | 截圖內容說明 | 破圖檢核 | Emoji檢核 | 截字檢核 | SHA256 前綴 | 狀態 |
|---|---|---|---|---|---|---|---|
| 01 | `proof_01_forge_dialog_btn_swap_weapon_zh_TW.png` | 繁中天宮鐵匠武器鍛造區當前槽位標題列：天藍色『更換裝備』立體果凍按鈕（`BtnSwapWeapon`，110x48px，厚底 5px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `d705f752b687` | 合格 (PASS) |
| 02 | `proof_02_weapon_swap_dialog_opened.png` | 點擊『更換裝備』後順暢連動開啟 `WeaponSwapDialog`（750px 橫屏、全螢幕半透明遮罩、三欄槽位與庫存武器清單） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `205a6d0a81b9` | 合格 (PASS) |
| 03 | `proof_03_weapon_swapped_forge_refreshed.png` | 於 `WeaponSwapDialog` 更換武器（天工神刃 T5 攻擊+999）後，彈窗關閉且 `ForgeDialog` 原地即時刷新武器名稱、攻擊力與槽位標籤 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `9b4192592eb8` | 合格 (PASS) |
| 04 | `proof_04_forge_btn_swap_weapon_zh_CN.png` | 簡體中文語系 (zh_CN) 下 `BtnSwapWeapon` 顯示「更换装备」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `08dce2efa03c` | 合格 (PASS) |
| 05 | `proof_05_forge_btn_swap_weapon_en.png` | 英文語系 (en) 下 `BtnSwapWeapon` 顯示「Change Equipment」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `6b32d287e396` | 合格 (PASS) |
| 06 | `proof_06_forge_btn_swap_weapon_ja.png` | 日文語系 (ja) 下 `BtnSwapWeapon` 顯示「装備変更」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `a39e6c7e717e` | 合格 (PASS) |
| 07 | `proof_07_forge_btn_swap_weapon_ko.png` | 韓文語系 (ko) 下 `BtnSwapWeapon` 顯示「장비 교체」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `7d36117925a8` | 合格 (PASS) |
| 08 | `proof_08_forge_btn_swap_weapon_es.png` | 西班牙文語系 (es) 下 `BtnSwapWeapon` 顯示「Cambiar equipo」，零 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `cb1ee40beae9` | 合格 (PASS) |
| 09 | `proof_09_forge_empty_slot_swap_weapon.png` | 切換至空武器槽位時，依然具備『更換裝備』按鈕，玩家可直接換裝，體驗無斷點 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `03e61309901e` | 合格 (PASS) |

---

## 3. 常見退回自查核對 (clock-review-checklist.md)

- [x] **截圖存證對齊驗收項目與完整互動過程**：截圖完整呈現按鈕位置、點擊開啟更換彈窗、換裝後原地刷新、六語系即時切換、空槽位操作，所有截圖 SHA256 獨立唯一。
- [x] **單元測試防 flaky**：測試腳本等待幀數充分（15~20 幀），信號接收採用 Dictionary 追蹤，無時序競爭，`TEST_FORGE_SWAP_WEAPON_DIALOG_OK` (PASS)。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：`BtnSwapWeapon` 整合於 `WeaponStatusHead` 標題列，彈出之 `WeaponSwapDialog` z-index=85，層次分明且全螢幕 Scrim 正常發揮。
- [x] **互動元件佈局尺寸與熱區**：`BtnSwapWeapon` custom_minimum_size = (110, 48)，高度與點擊熱區符合手遊規範 (>= 48px)。
- [x] **字級規範**：字體大小 16px 粉圓體，深藍紫描邊 2px，達成零小字。
- [x] **零系統 Emoji**：按鈕、提示全域無 Unicode 系統 Emoji。
- [x] **全站零退化與回歸測試**：既有 forge 相關單元測試 12/12 全數跑綠。
