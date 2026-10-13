# 《發條之心》ClockworkVaultDialog 發條儲能庫新增『前往鍛造』快捷果凍按鈕連動天宮鐵匠 驗收檢查清單 (t_842a278f)

## 任務背景與目標
- **任務編號**：t_842a278f
- **功能描述**：
  1. 在 `ClockworkVaultDialog`（`clockwork_vault_dialog.gd`）的底部操作區（`foot_box`）新增『前往鍛造』快捷果凍按鈕（`BtnGoForge`）。
  2. 按鈕規格：熱區高度 52px（>= 50px, >= 48px），多巴胺高飽和色盤（金黃 `#FFD028`、深藍紫描邊 `#1F1A3A`、果凍厚底 5px、圓角 18px、字級 18px 開源粉圓體），零系統 Emoji。
  3. 底部按鈕區並列三顆果凍按鈕：普通領取 (`ClaimButton`)、雙倍領取 (`DoubleClaimButton`)、前往鍛造 (`BtnGoForge`)。
  4. 點擊後發射 `forge_requested` 訊號並關閉儲能庫彈窗，大廳接收後即時開啟天宮鐵匠 (`ForgeDialog`)，將領取的鐵屑直接導流至裝備鍛造與機芯校準。
  5. 支援六語系動態即時切換（zh_TW, zh_CN, en, ja, ko, es），更新各語系 `ui.json` 與主語言檔。
  6. 撰寫自動化測試與真實 OpenGL3 實機截圖存證至 `proofs/t_842a278f/`，驗證 6 張截圖 SHA256 互異。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | `BtnGoForge` 尺寸為 `Vector2(200, 52)`，高度 52px >= 50px，熱區充足；字級 18px，無截斷無溢出。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 彈窗底部三按鈕（普通領取、雙倍領取、前往鍛造）水平等高並列，間距均勻，無遮擋穿框。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 全語系下按鈕純淨文字渲染，零 Unicode 系統 Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 金黃 `#FFD028` 底色、深藍紫描邊 `#1F1A3A`、底邊厚底 5px、圓角 18px，符合人體工學與視覺標準。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run -a godot --rendering-driver opengl3` 產生 6 張真實 Framebuffer 截圖，6 張 SHA256 互異。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試包含按鈕規格、六語系即時切換、跳轉連動、彈窗銷毀、大廳開啟天宮鐵匠與哨兵 `TEST_VAULT_FORGE_SHORTCUT_OK`。 |
| **程式與邏輯** | 跳轉與子模式參數有效對齊、無縫連動天宮鐵匠 | ✅ 已檢查 | 點擊 `BtnGoForge` 發射 `forge_requested`，關閉 `ClockworkVaultDialog`，大廳開啟 `ForgeDialog`。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全齊全（zh_TW: 前往鍛造, zh_CN: 前往锻造, en: Go to Forge, ja: 鍛造へ進む, ko: 단조로 이동, es: Ir a Forja），無舊名詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check /opt/side/bravesoul-game` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_842a278f/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_vault_three_buttons_zh_TW.png` | 發條儲能庫彈窗底部並列普通領取、雙倍領取、前往鍛造三顆多巴胺果凍按鈕（繁體中文） | `3da05fb57945e9c2` | PASS，三按鈕基線整齊對稱，金黃果凍厚底鮮明，文字無穿模截斷，零 Emoji |
| `proof_02_vault_go_forge_en.png` | 前往鍛造按鈕即時切換為英文 `Go to Forge` | `60c785408e3c63d8` | PASS，純英文字體排版完整，零 CJK 殘留，零 Emoji |
| `proof_03_vault_go_forge_ja.png` | 前往鍛造按鈕即時切換為日文 `鍛造へ進む` | `bc985344e597263e` | PASS，日文顯示完整無缺字，零 Emoji |
| `proof_04_vault_go_forge_ko.png` | 前往鍛造按鈕即時切換為韓文 `단조로 이동` | `e2f57d47232ba99c` | PASS，韓文顯示完整無缺字，零 Emoji |
| `proof_05_vault_go_forge_es.png` | 前往鍛造按鈕即時切換為西文 `Ir a Forja` | `b61ac790024dfd90` | PASS，西文顯示完整無缺字，零 CJK 殘留，零 Emoji |
| `proof_06_click_go_forge_opens_forge_dialog.png` | 點擊前往鍛造即時關閉儲能庫彈窗並開啟天宮鐵匠 ForgeDialog 進行裝備鍛造與機芯校準 | `eba841cb81ab0438` | PASS，儲能庫彈窗已關閉，天宮鐵匠彈窗正常開啟，槽位與機芯部位齊全，版面整潔，零 Emoji |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元測試**：`godot --path game --headless -s res://scripts/ui/test_vault_forge_shortcut.gd` -> **PASS (`TEST_VAULT_FORGE_SHORTCUT_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_vault_forge_shortcut.gd` -> **PASS (6 獨立雜湊截圖)**
- **迴歸測試**：
  - `test_vault_double_claim.gd` -> **PASS (`VAULT_DOUBLE_CLAIM_TEST_OK`)**
  - `test_lobby_vault_bubble.gd` -> **PASS (`LOBBY_VAULT_BUBBLE_TEST_OK`)**
- **自動合規檢查**：`clock-check /opt/side/bravesoul-game` -> **PASS (✅ 全過)**
