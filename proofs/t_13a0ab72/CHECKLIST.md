# 《發條之心》大廳聚魂殿堂新增『前往背包』快捷果凍按鈕連動探索背包素材頁籤 驗收檢查清單 (t_13a0ab72)

## 任務背景與目標
- **任務編號**：t_13a0ab72
- **功能描述**：
  1. 在 `mobile_lobby.gd` 的 `_build_soul_hall_tab()` 底欄操作區（`bot_h`）新增『前往背包』立體果凍按鈕（`BtnGoInventory`）。
  2. 按鈕規格：熱區高度 52px（>= 48px），多巴胺高飽和色盤（珊瑚粉 `#FF5E8A`、深藍紫描邊 `#1F1A3A`、果凍厚底 5px、圓角 18px、字級 16px 開源粉圓體），零系統 Emoji。
  3. 點擊後呼叫 `open_maple_inventory("material")`，無縫開啟探索背包並自動定位至素材分類頁籤。
  4. 支援六語系動態即時切換（zh_TW, zh_CN, en, ja, ko, es），更新並驗證各語系在地化。
  5. 撰寫自動化測試與真實 OpenGL3 實機截圖存證至 `proofs/t_13a0ab72/`。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | `BtnGoInventory` 尺寸為 `Vector2(200, 52)`，高度 52px >= 48px，熱區充足；字級 16px，無截斷無溢出。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 六語系下底欄三按鈕（一鍵吸收、前往背包、聚魂十連）水平基線對齊，間距均勻，無遮擋穿框。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 全語系下按鈕純淨文字渲染，零 Unicode Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 珊瑚粉 `#FF5E8A` 底色、深藍紫描邊 `#1F1A3A`、底邊厚底 5px、圓角 18px，符合人體工學與視覺標準。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run -a godot --rendering-driver opengl3` 產生 6 張真實 Framebuffer 截圖，6 張 SHA256 互異。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試包含按鈕規格、六語系即時切換、跳轉連動、雙向閉環與哨兵 `TEST_SOUL_HALL_INVENTORY_SHORTCUT_OK`。 |
| **程式與邏輯** | 跳轉與子模式參數有效對齊、無縫連動探索背包 | ✅ 已檢查 | 點擊 `BtnGoInventory` 呼叫 `open_maple_inventory("material")`，成功開啟背包並切換至素材分類。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全一致（zh_TW/zh_CN: 前往背包, en: Go to Inventory, ja: インベントリへ進む, ko: 인벤토리로 이동, es: Ir al Inventario），無舊名詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check /opt/side/bravesoul-game` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_13a0ab72/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_soul_hall_bottom_bar_three_buttons_zh_TW.png` | 聚魂殿堂底欄並列一鍵吸收、前往背包、聚魂十連三顆多巴胺果凍按鈕（繁體中文） | `cc56eaea21e882a2` | PASS，三按鈕基線整齊對稱，珊瑚粉果凍厚底鮮明，文字無穿模截斷，零 Emoji |
| `proof_02_soul_hall_go_inventory_btn_en.png` | 聚魂殿堂前往背包按鈕即時切換為英文 `Go to Inventory` | `82d8bc7e862962b2` | PASS，純英文字體排版完整，零 CJK 殘留，零 Emoji |
| `proof_03_soul_hall_go_inventory_btn_ja.png` | 聚魂殿堂前往背包按鈕即時切換為日文 `インベントリへ進む` | `5dcda0d84698bc14` | PASS，日文顯示完整無缺字，零 Emoji |
| `proof_04_soul_hall_go_inventory_btn_ko.png` | 聚魂殿堂前往背包按鈕即時切換為韓文 `인벤토리로 이동` | `5e1a8b1d8cda8539` | PASS，韓文顯示完整無缺字，零 Emoji |
| `proof_05_soul_hall_go_inventory_btn_es.png` | 聚魂殿堂前往背包按鈕即時切換為西文 `Ir al Inventario` | `ee2971adc964973c` | PASS，西文顯示完整無缺字，零 CJK 殘留，零 Emoji |
| `proof_06_click_go_inventory_opens_maple_inventory_material.png` | 點擊前往背包即時開啟探索背包 MapleInventory 並自動切換至素材分類頁籤 | `b7f6cab9f24904cf` | PASS，探索背包彈窗正常開啟，頂部素材 Chip 高亮選中，版面整潔，零 Emoji |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元測試**：`godot --path game --headless -s res://scripts/ui/test_soul_hall_inventory_shortcut.gd` -> **PASS (`TEST_SOUL_HALL_INVENTORY_SHORTCUT_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_soul_hall_inventory_shortcut.gd` -> **PASS (6 獨立雜湊截圖)**
- **迴歸測試**：
  - `test_maple_inventory_soul_shortcut.gd` -> **PASS (`MAPLE_INVENTORY_SOUL_SHORTCUT_OK`)**
  - `test_maple_inventory_shortcuts.gd` -> **PASS (`MAPLE_INVENTORY_SHORTCUTS_OK`)**
- **自動合規檢查**：`clock-check /opt/side/bravesoul-game` -> **PASS (✅ 全過)**
