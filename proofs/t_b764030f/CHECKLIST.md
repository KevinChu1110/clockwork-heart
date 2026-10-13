# 《發條之心》ClockworkVaultDialog 發條儲能庫新增『前往背包』快捷果凍按鈕連動探索背包 驗收檢查清單 (t_b764030f)

## 任務背景與目標
- **任務編號**：t_b764030f
- **功能描述**：
  1. 在 `ClockworkVaultDialog`（`clockwork_vault_dialog.gd`）的底部操作區（`foot_box`）新增『前往背包』快捷果凍按鈕（`BtnGoInventory`）。
  2. 按鈕規格：熱區高度 52px（>= 50px, >= 48px），多巴胺高飽和色盤（薄荷綠 `#4ED86A`、深藍紫描邊 `#1F1A3A`、果凍厚底 5px、圓角 18px、字級 17px 開源粉圓體），零系統 Emoji。
  3. 底部按鈕區並列四顆果凍按鈕：普通領取 (`ClaimButton`)、雙倍領取 (`DoubleClaimButton`)、前往鍛造 (`BtnGoForge`)、前往背包 (`BtnGoInventory`)。
  4. 點擊後安全關閉儲能庫彈窗並發射 `go_inventory` 與 `inventory_requested` 訊號，大廳接收後即時開啟探索背包 (`MapleInventory`)，讓玩家領取放置收益後一鍵無縫直通背包檢視物資，操作路徑順暢閉環。
  5. 支援六語系動態即時切換（zh_TW, zh_CN, en, ja, ko, es），更新各語系 `ui.json` 與主語言檔，零 13px 以下小字。
  6. 撰寫自動化單元與整合測試 `test_clockwork_vault_inventory_shortcut.gd` 與真實 OpenGL3 實機截圖存證至 `proofs/t_b764030f/`，驗證 7 張截圖 SHA256 互異。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | `BtnGoInventory` 尺寸為 `Vector2(150, 52)`，高度 52px >= 50px，熱區充足；字級 17px，無截斷無溢出。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 彈窗底部四按鈕（普通領取、雙倍領取、前往鍛造、前往背包）水平等高並列，間距均勻（12px），無遮擋穿框；禁用狀態按鈕保持立體圓角暗色槽與對比邊框。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 全語系下按鈕純淨文字渲染，零 Unicode 系統 Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 薄荷綠 `#4ED86A` 底色、深藍紫描邊 `#1F1A3A`、底邊厚底 5px、圓角 18px，符合人體工學與視覺標準。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run godot` 產生 7 張真實 Framebuffer 截圖，7 張 SHA256 互異獨立。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試包含按鈕規格、六語系即時切換、跳轉連動、彈窗銷毀、大廳開啟探索背包與哨兵 `TEST_CLOCKWORK_VAULT_INVENTORY_SHORTCUT_OK`。 |
| **程式與邏輯** | 跳轉與子模式參數有效對齊、無縫連動探索背包 | ✅ 已檢查 | 點擊 `BtnGoInventory` 發射 `go_inventory` 與 `inventory_requested`，安全關閉 `ClockworkVaultDialog`，大廳開啟 `MapleInventory`。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全齊全（zh_TW: 前往背包, zh_CN: 前往背包, en: Go to Inventory, ja: インベントリへ進む, ko: 인벤토리로 이동, es: Ir al Inventario），無舊名詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check /root/.../bravesoul-game` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_b764030f/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_vault_four_buttons_zh_TW.png` | 發條儲能庫彈窗底部並列普通領取、雙倍領取、前往鍛造、前往背包四顆多巴胺果凍按鈕（繁體中文） | `bf047cee97f126c6` | PASS，四按鈕基線整齊對稱，薄荷綠與金黃果凍厚底鮮明，禁用態帶有立體暗色底槽與邊框，文字無穿模截斷，零 Emoji |
| `proof_02_vault_go_inventory_en.png` | 前往背包按鈕即時切換為英文 `Go to Inventory` | `884988b7ed27717d` | PASS，純英文字體排版完整，零 CJK 殘留，零 Emoji |
| `proof_03_vault_go_inventory_ja.png` | 前往背包按鈕即時切換為日文 `インベントリへ進む` | `fd6599b51a914f20` | PASS，日文顯示完整無缺字，零 Emoji |
| `proof_04_vault_go_inventory_ko.png` | 前往背包按鈕即時切換為韓文 `인벤토리로 이동` | `6e9d8783da94eb93` | PASS，韓文顯示完整無缺字，零 Emoji |
| `proof_05_vault_go_inventory_es.png` | 前往背包按鈕即時切換為西文 `Ir al Inventario` | `3a41bc1f36206c66` | PASS，西文顯示完整無缺字，零 CJK 殘留，零 Emoji |
| `proof_06_vault_go_inventory_zh_CN.png` | 前往背包按鈕即時切換為簡中 `前往背包` | `564aa6ab128fe3a3` | PASS，簡體中文顯示正確，零 Emoji |
| `proof_07_click_go_inventory_opens_maple_inventory.png` | 點擊前往背包即時關閉儲能庫彈窗並開啟探索背包 MapleInventory 進行物資檢視 | `2647a4498192e6dc` | PASS，儲能庫彈窗已安全關閉，探索背包彈窗正常開啟，分類頁籤齊全，物品格與詳情卡清晰，無疊窗無穿模 |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元測試**：`godot --path game --headless -s res://scripts/ui/test_clockwork_vault_inventory_shortcut.gd` -> **PASS (`TEST_CLOCKWORK_VAULT_INVENTORY_SHORTCUT_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game -s res://scripts/ui/test_clockwork_vault_inventory_shortcut.gd` -> **PASS (7 獨立雜湊截圖)**
- **迴歸測試**：
  - `test_vault_double_claim.gd` -> **PASS (`VAULT_DOUBLE_CLAIM_TEST_OK`)**
  - `test_lobby_vault_bubble.gd` -> **PASS (`LOBBY_VAULT_BUBBLE_TEST_OK`)**
  - `test_vault_forge_shortcut.gd` -> **PASS (`TEST_VAULT_FORGE_SHORTCUT_OK`)**
- **自動合規檢查**：`clock-check /root/.../bravesoul-game` -> **PASS (✅ 全過)**
