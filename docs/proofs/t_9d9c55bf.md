# 全面回歸驗收證明 · 手藝工坊一鍵卸下、勝利整頓、武器與機芯卸下等前四分支合進主線 (t_9d9c55bf)

## 1. 任務背景與驗收目標
針對已通過測試審查（測試小婷 `sideqa` 完成審查驗收並簽核通過）之四項重要養成與操作閉環功能分支：
1. **`gem-workshop-auto-unsocket`（t_87339dc9）**：分支 `origin/agent/20261013-gem-workshop-auto-unsocket-t_87339dc9`（commit `b35eb603f`）
   - 手藝工坊 `GemWorkshopDialog` 寶石櫃支援『一鍵卸下』已鑲嵌寶石（`BtnAutoUnsocket` 珊瑚粉立體果凍按鈕，130x48px，熱區 >= 48px，厚底 5px，深藍紫描邊 2px，零 Emoji）。
   - 連動 `GemSystem` 安全卸下並全數歸還背包，屬性即時歸零刷新，防呆提示與六語系（zh_TW, zh_CN, en, ja, ko, es）支援。
2. **`victory-gear-up-shortcut`（t_0b3a919b）**：分支 `origin/agent/20261013-victory-gear-up-btn-t_0b3a919b`（commit `defa4a474`）
   - 戰鬥勝利結算彈窗 `BattleVictoryDialog` 新增『前往整頓』快捷按鈕（`BtnGearUp`，140x50px，熱區 >= 48px，天藍果凍厚底 5px，零 Emoji）。
   - 點擊後安全關閉結算彈窗，直通大廳並精準跳轉至角色裝備 Tab（`TAB_CHARACTER`），支援掉落機芯紅點導航與六語系支援。
3. **`lobby-weapon-unequip-all`（t_3c98e3bb）**：分支 `origin/agent/20261013-lobby-weapon-unequip-all-t_3c98e3bb`（commit `51f6b28b7`）
   - 大廳角色頁三欄武器槽新增『一鍵卸下』按鈕（`BtnWeaponUnequipAll`，104x48px，熱區 >= 48px，珊瑚粉果凍厚底 5px，深藍紫描邊 2px，零 Emoji）。
   - 安全防護：副武器卸下保留主武器切換為空手木刀、戰力即時刷新、六語系支援。
4. **`lobby-core-unequip-all`（t_0ea90d60）**：分支 `origin/agent/20261013-lobby-core-unequip-all-t_0ea90d60`（commit `799ef5ba5`）
   - 大廳角色頁五大機芯槽新增『一鍵卸下』按鈕（`BtnCoreUnequipAll`，104x48px，熱區 >= 48px，珊瑚粉果凍厚底 5px，深藍紫描邊 2px，零 Emoji）。
   - 安全防護：五槽全部安全卸下並歸還背包、空槽點擊防呆阻擋飄字、戰力即時刷新、六語系支援。

由工程師阿翔（`sideworker2`）在 `main` 主線執行四分支無衝突乾淨整併（Merge commits: `d78cf51ef`, `f57da8eb0`, `30361e102`, `fc42e8035`），執行全套無頭冒煙測試、四項專屬單元測試與關聯回歸測試、`clock-check` 檢查，並透過 `/root/project_status.py` 同步將對應項目更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **寶石櫃一鍵卸下單元測試** | `TEST_FILTER=test_gem_auto_unsocket ./tools/run_tests.sh` | 1/1 PASS，`TEST_GEM_AUTO_UNSOCKET_OK`，按鈕規格、卸下歸還背包、屬性清空、防呆與六語系全綠 | **PASS** |
| **勝利結算前往整頓單元測試** | `TEST_FILTER=test_battle_victory_gear_up ./tools/run_tests.sh` | 1/1 PASS，`TEST_BATTLE_VICTORY_GEAR_UP_OK`，快捷按鈕、信號連動跳轉裝備 Tab、六語系全綠 | **PASS** |
| **武器槽一鍵卸下單元測試** | `TEST_FILTER=test_lobby_weapon_unequip_all ./tools/run_tests.sh` | 1/1 PASS，`TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK`，按鈕規格、副武卸下、防呆與六語系全綠 | **PASS** |
| **武器槽一鍵配置回歸測試** | `TEST_FILTER=test_lobby_weapon_auto_equip ./tools/run_tests.sh` | 1/1 PASS，`LOBBY_WEAPON_AUTO_EQUIP_OK`，回歸無破壞 | **PASS** |
| **機芯槽一鍵卸下單元測試** | `TEST_FILTER=test_lobby_core_unequip_all ./tools/run_tests.sh` | 1/1 PASS，`TEST_LOBBY_CORE_UNEQUIP_ALL_OK`，按鈕規格、五槽卸下歸還、空槽防呆、六語系全綠 | **PASS** |
| **代碼與素材關聯檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個；⚠️ 直接在 main 上改（本卡為維運整併卡，預期操作） | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表 (proofs/t_9d9c55bf/)
所有截圖皆以真實 OpenGL3 渲染驅動於 1280×720 解析度下透過真實 Viewport Framebuffer 產生，零假圖，17 張 SHA256 各自獨立：

### A. 手藝工坊寶石櫃一鍵卸下（4 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_gem_workshop_unsocket_socketed_zh_TW.png` | 寶石櫃有已鑲嵌寶石，『一鍵卸下』珊瑚粉果凍按鈕高亮可用 (130x48px) | 1280×720 | `16dc69a623708ce3459925c7a464fba755e50d3fded3a5625f85b2ca9f90bf43` |
| `proof_02_gem_workshop_unsocket_success_toast_zh_TW.png` | 點擊一鍵卸下後孔位清空、屬性歸零、成功提示飄字顯示並歸還背包 | 1280×720 | `06156855eb17722091a00f0a5af6046856d0fcee7d263c317a61a4b718d5ea97` |
| `proof_03_gem_workshop_unsocket_no_gem_guard_zh_TW.png` | 無寶石狀態防呆點擊飄字提示「當前無已鑲嵌寶石！」 | 1280×720 | `89319554e0304081e0aabaf6cdc208f6493c4b828da1e277d3ba0d8770e5b0ce` |
| `proof_04_gem_workshop_unsocket_en.png` | 英文語系 (en) 下『Quick Unsocket』按鈕與介面展示，零 CJK 殘留 | 1280×720 | `62c72c92a3aef4243b7a037d6260eec4df9c219d61bcc209ac8e5a151782d53e` |

### B. 戰鬥勝利結算前往整頓（3 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_05_battle_victory_dialog_zh_TW.png` | 繁中 BattleVictoryDialog 勝利結算展示『前往整頓』天藍果凍按鈕 (140x50px) | 1280×720 | `1d1a896d4d4c4c01072ab377b2d3a17d8eefbd9a34637509cdd3fc52e42552f5` |
| `proof_06_battle_victory_dialog_en.png` | 英文語系 (en) 下勝利結算展示『Gear Up』按鈕，零 CJK 殘留 | 1280×720 | `733923e46fd921ee864891c2f2b385bedefd26696e94c16e83d4bc133c56fee1` |
| `proof_07_gear_up_transition_lobby_character.png` | 點擊前往整頓後安全關閉結算彈窗並精準跳轉大廳角色裝備 Tab 實景 | 1280×720 | `df6d95bd9ee42af697a82a6acb49a2a6d70b87e214830480b8aede304adca44f` |

### C. 大廳角色頁三欄武器槽一鍵卸下（5 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_08_char_weapon_slots_three_weapons_zh_TW.png` | 裝備三把武器狀態展示『一鍵卸下』珊瑚粉果凍按鈕 (104x48px) | 1280×720 | `4b10272eaba8209ca215464874020c6374f2a5a493c3eaadc7d704bd0ee9c5d4` |
| `proof_09_char_weapon_unequip_success_toast_zh_TW.png` | 點擊一鍵卸下後副武器卸下並彈出提示飄字「已卸下副武器」 | 1280×720 | `78eefc6028f1942032c02d7475a8782411cf4d9dc5ce9a943866e738ee9781e4` |
| `proof_10_char_weapon_unequip_no_secondary_toast_zh_TW.png` | 無副武器時點擊卸下防呆提示「無副武器可卸下」 | 1280×720 | `8d726568fb105fae40a6e9fa1cf71af3621e64d631970686e877da1680b86bf4` |
| `proof_11_char_weapon_unequip_bare_handed_zh_TW.png` | 卸下後主角切換至空手木刀、戰力即時刷新 | 1280×720 | `1c1a4f9bc3090c1083e23819d5069e036aeabcd4b440cbea4d899504235297d0` |
| `proof_12_char_weapon_unequip_en.png` | 英文語系 (en) 下『Unequip All』按鈕與介面展示，零 CJK 殘留 | 1280×720 | `dee46820520605fe33ebf5fdef9e7986148621b2eb9583f69386b32ad6ea0e04` |

### D. 大廳角色頁五大機芯槽一鍵卸下（5 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_13_core_slots_equipped_five_cores_zh_TW.png` | 裝備五大機芯狀態展示『一鍵卸下』珊瑚粉果凍按鈕 (104x48px) | 1280×720 | `1988d0ffe2c0ddd403738dba8decd3e1e2d7188a999f53f4b3052aed7145336f` |
| `proof_14_core_unequip_success_toast_zh_TW.png` | 點擊一鍵卸下後五槽全數清空、歸還背包，飄字提示「已卸下所有機芯」 | 1280×720 | `7eeed0b0960fea83c38c515e119edfbb5d0f1cbfd99cbba9da638553ccea3a31` |
| `proof_15_core_unequip_empty_guard_toast_zh_TW.png` | 空槽狀態點擊防呆提示「未裝備任何機芯」 | 1280×720 | `f76a0e008a33e6969c800940b7002066b3520b7fc180c26b1a5cdcb393b4bac2` |
| `proof_16_core_unequip_en.png` | 英文語系 (en) 下『Quick Unsocket』按鈕與介面展示，零 CJK 殘留 | 1280×720 | `df5f07152a6a67a29feeb0234c74f797f23ff2e8db2888c336e125aa068f23c1` |
| `proof_17_btn_core_unequip_min_size_48px.png` | 機芯一鍵卸下按鈕熱區與尺寸 (104x48px) 符合 >=48px 規範驗證 | 1280×720 | `3cdb97b8cf74374ab6ddc70112dcb18a3b476b4d7049acd9142d2ec2b65ae482` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **畫面與素材**：
  - 各按鈕熱區皆符合手機端規範（>= 48px，按鈕高 48~50px）。
  - 按鈕樣式均為立體果凍厚底按鈕（珊瑚粉 #FF5E8A、天藍 #38A0FF，厚底 5px，深藍紫描邊 2px，圓角 16~18px）。
  - 全域零系統 Emoji，全面使用開源粉圓體與質感多巴胺配色。
  - 17 張截圖 SHA256 各自獨立無重複，ViewPort 與語系渲染完整無黑屏。
- [x] **測試與證據**：
  - 無頭引擎冒煙測試 0 SCRIPT ERROR 通過。
  - 單元測試（寶石一鍵卸下、勝利結算整頓、武器一鍵卸下、機芯一鍵卸下）全部 1/1 PASS 通過。
  - 測試輸出無 flaky 時序競爭。
- [x] **程式與邏輯**：
  - 合併無衝突，所有 autoload、信號連動、語系字串完全對齊。
  - 機芯與寶石卸下後安全返還背包，戰力與屬性數值即時刷新。
  - 空槽與無副武器時具備完善防呆保護。
- [x] **資料與文案**：
  - 六語系（zh_TW, zh_CN, en, ja, ko, es）鍵值齊全，歐美語系零 CJK 殘留。
  - 無已退役舊名詞（霧隱村／今日村莊／白霧村 零殘留）。
- [x] **流程與交付**：
  - `docs/PROJECTS.json` 透過 `python3 /root/project_status.py` 將 `gem-workshop-auto-unsocket`、`victory-gear-up-shortcut`、`lobby-weapon-unequip-all`、`lobby-core-unequip-all` 四項全數更新為『已上線』。
  - 工作目錄乾淨，無未追蹤或未提交之暫存檔案。
