# 《發條之心》ShopDialog 商城彈窗底部新增『前往背包』快捷果凍按鈕連動探索背包 驗收檢查清單 (t_6821e62c)

## 任務背景與目標
- **任務編號**：t_6821e62c
- **功能描述**：
  1. 在 `ShopDialog`（`shop_dialog.gd`）商城彈窗底部新增『前往背包』快捷立體果凍按鈕（`BtnGoInventory`）。
  2. 按鈕規格：熱區高度 52px（>= 50px，符合手機觸控熱區 >= 48px），寬度 160px，薄荷綠色盤 `#4ED86A`、深藍紫描邊 `#1F1A3A`、果凍厚底 5px、圓角 18px、字級 17px 開源粉圓體（OpenHuninn），零系統 Emoji。
  3. 點擊後安全關閉 ShopDialog 彈窗並發射 `go_inventory` 與 `inventory_requested` 訊號，大廳接收後即時開啟探索背包（`MapleInventory`），提供玩家在商城購買或檢視後快速前往背包檢視資產的捷徑，無疊窗或殘留遮罩。
  4. 支援六語系動態即時切換（zh_TW, zh_CN, en, ja, ko, es），更新各語系 `ui.json` 與主語言檔，字級 >= 16px，無零碎小字。
  5. 撰寫自動化單元與整合測試 `test_shop_inventory_shortcut.gd` 並產出真實 OpenGL3 實機截圖存證至 `proofs/t_6821e62c/`，驗證 7 張截圖 SHA256 互異獨立。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | `BtnGoInventory` 尺寸為 `Vector2(160, 52)`，高度 52px >= 50px，熱區充足；字級 17px，彈窗主卡片高度 580px 居中於 720px 畫面，無截斷無溢出。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 彈窗底部 FooterBar 居中安置前往背包按鈕，上下留白合理，無遮擋穿框，各語系文字完整無溢出。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 全語系下按鈕純淨文字渲染，零 Unicode 系統 Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 薄荷綠 `#4ED86A` 底色、深藍紫描邊 `#1F1A3A`、底邊厚底 5px、圓角 18px，符合人體工學與視覺標準。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run godot` 產生 7 張真實 Framebuffer 截圖，7 張 SHA256 互異獨立（0 重複）。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試包含按鈕規格、六語系即時切換、跳轉連動、彈窗銷毀、大廳開啟探索背包與哨兵 `TEST_SHOP_INVENTORY_SHORTCUT_OK`。 |
| **程式與邏輯** | 跳轉與子模式參數有效對齊、無縫連動探索背包 | ✅ 已檢查 | 點擊 `BtnGoInventory` 發射 `go_inventory` 與 `inventory_requested`，安全關閉 `ShopDialog`，大廳開啟 `MapleInventory`。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全齊全（zh_TW: 前往背包, zh_CN: 前往背包, en: Go to Inventory, ja: インベントリへ進む, ko: 인벤토리로 이동, es: Ir al Inventario），無舊名詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check .` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_6821e62c/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_shop_go_inventory_zh_TW.png` | 商城彈窗底部展示薄荷綠立體果凍按鈕『前往背包』（繁體中文） | `012d6b83395ae05f` | PASS，居中於底部操作欄，薄荷綠與深藍紫描邊對比鮮明，字體清晰，無殘留遮罩，零 Emoji |
| `proof_02_shop_go_inventory_en.png` | 前往背包按鈕即時切換為英文 `Go to Inventory` | `e4ae6208b7d403dd` | PASS，純英文字體排版完整，零 CJK 殘留，零 Emoji |
| `proof_03_shop_go_inventory_ja.png` | 前往背包按鈕即時切換為日文 `インベントリへ進む` | `46979e6faf643a65` | PASS，日文顯示完整無缺字，零 Emoji |
| `proof_04_shop_go_inventory_ko.png` | 前往背包按鈕即時切換為韓文 `인벤토리로 이동` | `4f23ae7107583666` | PASS，韓文顯示完整無缺字，零 Emoji |
| `proof_05_shop_go_inventory_es.png` | 前往背包按鈕即時切換為西文 `Ir al Inventario` | `65c5960214330853` | PASS，西文顯示完整無缺字，零 CJK 殘留，零 Emoji |
| `proof_06_shop_go_inventory_zh_CN.png` | 前往背包按鈕即時切換為簡中 `前往背包` | `a694553189dd656e` | PASS，簡體中文顯示正確，零 Emoji |
| `proof_07_click_go_inventory_opens_maple_inventory.png` | 點擊前往背包即時關閉商城彈窗並開啟探索背包 MapleInventory | `0f60cdd721cf644d` | PASS，商城彈窗已安全關閉，探索背包彈窗正常開啟，無疊窗無穿模，物資檢視路徑完美閉環 |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元測試**：`godot --path game --headless -s res://scripts/ui/test_shop_inventory_shortcut.gd` -> **PASS (`TEST_SHOP_INVENTORY_SHORTCUT_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game -s res://scripts/ui/test_shop_inventory_shortcut.gd` -> **PASS (7 獨立雜湊截圖)**
- **既有測試回歸**：
  - `test_shop_dialog.gd` -> **PASS (`SHOP_DIALOG_OK`)**
  - `test_clockwork_vault_inventory_shortcut.gd` -> **PASS (`TEST_CLOCKWORK_VAULT_INVENTORY_SHORTCUT_OK`)**
  - `test_soul_hall_inventory_shortcut.gd` -> **PASS (`SOUL_HALL_INVENTORY_SHORTCUT_TEST_OK`)**
- **自動合規檢查**：`clock-check .` -> **PASS (✅ 全過)**
