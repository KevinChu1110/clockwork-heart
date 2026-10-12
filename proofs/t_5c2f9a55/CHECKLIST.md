# 驗收清單：大廳角色頁武器輪替配置新增『一鍵配置』最高戰力武器 (t_5c2f9a55)

## 1. 任務核心驗收標準對齊
- [x] **EquipmentSystem 自動挑選最佳武器邏輯 (auto_equip_best_weapons)**：
  - 在 `equipment_system.gd` 實作 `auto_equip_best_weapons()` 與輔助評分排序比對函式 `_sort_weapons_comparator`、`get_weapon_attack`、`get_weapon_quality_rank`、`calculate_weapon_power`。
  - 依「攻擊力」（主要）與「品質」（次要）嚴格排序背包武器，自動挑選最佳武器填入已解鎖的三個武器槽位（0, 1, 2）。
  - 若等級僅解鎖部分欄位（Lv1: 1 槽、Lv10: 2 槽、Lv16: 3 槽），僅配置已解鎖槽位，不影響鎖定槽位。
  - 換裝時將卸下之舊武器安全退回背包，裝備之新武器自背包扣除並存入 `GameState.equip_worn`，同步調用 `_sync_active_weapon_mirror()` 鏡像作用中武器與流派。
  - 發出 `weapons_auto_equipped` 信號與 `equipment_changed` 信號，並保存遊戲。
- [x] **大廳角色頁一鍵配置立體果凍按鈕 (BtnWeaponAutoEquip)**：
  - 在 `mobile_lobby.gd` 的角色頁（`Tab.CHARACTER`）武器輪替配置標題列（`w_hdr`）新增「一鍵配置」果凍按鈕（`BtnWeaponAutoEquip`）。
  - 熱區尺寸嚴格符合手機端人體工學（`custom_minimum_size = Vector2(104, 48)`，熱區 >= 48px，尺寸 >= 104x48px）。
  - 配色採《塔塔冒險隊》薄荷綠果凍厚底風格（`COLOR_MINT` `#4ED86A`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A`、底部立體厚底 5px、圓角 16px、陰影 5px），字體使用開源粉圓體（Open Huninn 14px，加粗，深藍紫加深描邊），零系統 Emoji。
- [x] **信號發出與即時介面刷新**：
  - 點擊按鈕調用 `auto_equip_weapons()`，成功換裝時發出 `weapons_auto_equipped` 訊號。
  - 即時刷新三欄武器卡（`_refresh_weapon_slot_buttons()`）、大廳頂部數值（`refresh_hud()`）、角色頁有效戰力膠囊（`_char_power_badge`）與戰鬥屬性卡片（`_refresh_char_tab_stats(true)`）。
  - 飄字提示戰力提升：彈出「戰力提升 +XX！已一鍵配置最高戰力武器。」（若戰力持平則提示「已一鍵配置最高戰力武器。」）。
- [x] **最佳配置重複點擊判定**：
  - 當所有已解鎖武器槽位已是背包中最強武器時，點擊按鈕不重複異動資料（`changed: false`），彈出「目前已是最佳武器配置！」飄字提示。
- [x] **六語系即時切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 即時切換，切換語系時按鈕文字即時更新（zh_TW="一鍵配置", zh_CN="一键配置", en="Auto-Equip", ja="一括装着", ko="일괄 장착", es="Equipamiento rápido"）。
  - en、ja、ko、es 下無中文殘留，零系統 Emoji。
  - 標題與說明採垂直 VBox 佈局，防止英／西等長語系在窄螢幕或 1280 橫屏下產生任何橫向邊界溢出或裁切。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=lobby_weapon_auto_equip ./tools/run_tests.sh`：1/1 PASS（100% 全綠，LOBBY_WEAPON_AUTO_EQUIP_OK，exit code 0）。
  - 覆蓋點：按鈕熱區與規格（>=104x48px, >=48px touch, border_bottom 5px, radius 16px）、依攻擊力與品質比對裝備最強三把武器（星紋龍牙 atk 90 epic、燼木銳矛 atk 70 rare、風葦輕弓 atk 50 uncommon）、弱武器退回背包、有效戰力大幅提升、三槽卡片即時刷新、重複點擊最佳配置判定、六語系即時切換與零系統 Emoji。
- **大廳迴歸測試**：
  - `TEST_FILTER=lobby ./tools/run_tests.sh`：15/15 PASS（全部大廳相關測試全綠）。
- **裝備系統迴歸測試**：
  - `TEST_FILTER=equipment ./tools/run_tests.sh`：2/2 PASS。
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_5c2f9a55/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下直接自 Viewport Texture Image 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_char_weapon_slots_before_auto_equip_zh_TW.png` | 繁中角色頁三槽武器輪替配置（初始低階）與「一鍵配置」薄荷綠果凍按鈕（104x48px），右側屬性卡（暴擊率、怒氣量表）完全收納於白色面板內，圓角、邊框、陰影完整，與底欄保持乾淨安全間距 | `292eedcc654f0c71fbc09567cf8ca7c73414a446df04473c7551d4b15cb88c84` |
| `proof_02_char_weapon_auto_equipped_toast_zh_TW.png` | 點擊一鍵配置後換上最強三槽武器（星紋龍牙/燼木銳矛/風葦輕弓），戰力從 89 飆升至 196，上方飄字「戰力提升 +107！已一鍵配置最高戰力武器。」 | `5df24f910bf4cabe94735aa4841dca84d6d18ba907ba88ec2f7d124c64bda15a` |
| `proof_03_char_weapon_auto_equip_already_best_zh_TW.png` | 最佳狀態下再次點擊一鍵配置，上方飄字「目前已是最佳武器配置！」 | `774f706355ed891338e7cba4d743088556d663082c24af031ef9736b31a4b15f` |
| `proof_04_char_weapon_auto_equip_en.png` | 英文語系角色頁 Auto-Equip 按鈕與最佳配置飄字 (Already at optimal weapon configuration!)，零中文殘留，屬性卡完整保留邊框圓角與安全留白 | `3e65a47a9c5021d12afbafff7640f2ef99c31d1f034a9d7109725874007fb3e0` |
| `proof_05_char_weapon_auto_equip_ja.png` | 日文語系角色頁 一括装着 按鈕與最佳配置飄字 (現在は最適な武器配置です！)，屬性卡完整無遮擋裁切 | `f73de257fcdc6a8d49c8380a6102ba44b28da928b55cb60d94f53bb847628181` |
| `proof_06_btn_auto_equip_min_size_48px.png` | 一鍵配置按鈕規格特寫（尺寸 104x48px，立體厚底 5px，圓角 16px）與三槽武器完成態 | `ce84fb2a33aeb678a446f7fa9844e0c4091b4f44d1f069b43078461979074006` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含配置前初始態、配置後換裝飄字、最佳配置提示、語系切換，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（20~25 幀），無時序競爭，無頭測試 `1/1 PASS`。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：標題與副標題採用 VBox 垂直流，按鈕維持 104x48px，橫向無任何擠壓溢出。
- [x] **互動元件佈局尺寸與熱區**：`BtnWeaponAutoEquip` 尺寸設為 104x48px，熱區符合手遊規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 14px，深藍紫描邊，達成零 13px 以下小字。
- [x] **零系統 Emoji**：按鈕與飄字全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：各武器流派與品質名詞嚴格對齊既有定義。
- [x] **專案狀態更新**：已透過 `project_status.py` 將 `lobby-weapon-auto-equip` 標記為測試中。
