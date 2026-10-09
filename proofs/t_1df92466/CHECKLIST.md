# 《發條之心》WeaponSwapDialog 武器更換彈窗支援直通天宮鐵匠鍛造按鈕 查驗清單與驗收報告 (t_1df92466)

- **執行人**：阿翔（發條之心·工程師 sideworker2）
- **關聯任務**：`t_1df92466`（🎮 遊戲開發｜WeaponSwapDialog 武器更換彈窗支援直通天宮鐵匠鍛造按鈕）
- **交付目錄**：`proofs/t_1df92466/`
- **遵循規範**：
  - `review.md` 人因規範：彈窗按鈕熱區 >= 48px、立體果凍厚底 5px、零 Emoji、多巴胺鮮亮高飽和色盤。
  - `clock-review-checklist.md`：
    - 連續截圖不可重複（SHA256 不得相同），存證對齊驗收項目與完整互動過程。
    - 彈窗與卡片正確佈局尺寸（custom_minimum_size / min_size），避免坍塌或溢出。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_weapon_swap_dialog_btn_go_forge.png` | WeaponSwapDialog 底部操作列新增天藍色「前往鍛造」立體果凍按鈕（熱區 >= 48px，厚底 5px，與「關閉」並列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `3689a2af9a80` | 合格 (PASS) |
| 02 | `proof_02_forge_dialog_opened.png` | 點擊「前往鍛造」後，發送 `forge_requested` 信號，平滑關閉更換彈窗並連動大廳 `MobileLobby.open_forge()` 開啟天宮鐵匠鍛造彈窗 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `800fc886bbfc` | 合格 (PASS) |
| 03 | `proof_03_weapon_swap_dialog_i18n.png` | 英文語系 (en) 下即時在地化顯示「Go to Forge」，摘要與說明文字無中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `505203131cc2` | 合格 (PASS) |

- **防作弊校驗**：三張實機截圖 SHA256 完全獨立互異（無重複上傳冒充）。
- **Vision 視覺審核**：經 Vision 驗證，按鈕熱區與立體果凍厚底完整呈現，色盤對比度良好，關閉彈窗並開啟鐵匠彈窗連動流暢，英文語系無中文殘留。

---

## 二、 語系對照與詞條清單

所有玩家可見文字均透過 `ContentLoc.text("ui", ...)` / `_t()` 對接 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| 前往鍛造 | 前往锻造 | Go to Forge | 鍛造へ進む | 단조로 이동 | Ir a Forja |

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR，編譯與加載完全正常。
2. **單元與驗收測試**：
   - `res://scripts/ui/test_weapon_swap_forge_shortcut.gd`：
     - ✓ WeaponSwapDialog 底部操作列存在 `BtnGoForge` 按鈕。
     - ✓ 按鈕尺寸 `custom_minimum_size = Vector2(130, 48)`（高度 >= 48px，寬度 >= 48px），符合人體工學。
     - ✓ StyleBoxFlat 具備 `border_width_bottom = 5`（立體果凍厚底 5px），圓角 16px，天藍多巴胺色盤 `#38A0FF`。
     - ✓ 點擊 `BtnGoForge` 成功發射 `forge_requested` 信號與 `closed` 信號，彈窗進入 `queue_free`。
     - ✓ 大廳 `MobileLobby` 正確監聽 `forge_requested` 並呼叫 `open_forge()` 成功開啟 `ForgeDialog`。
     - ✓ 六語系（zh_TW / zh_CN / en / ja / ko / es）即時在地化完全正確，且歐美韓等非中文語系無中文殘留、零 Emoji。
     - ✓ 產出 3 張實機截圖存證且 SHA256 獨立互異。
     - 測試結論：`TEST_WEAPON_SWAP_FORGE_SHORTCUT_OK` 通過。
3. **既有迴歸測試**：
   - `res://scripts/ui/test_lobby_weapon_swap_dialog.gd`：`TEST_LOBBY_WEAPON_SWAP_DIALOG_OK` 通過。
4. **自動化審查檢查器**：
   - `/root/bin/clock-check /opt/side/bravesoul-game`：
     - `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。
