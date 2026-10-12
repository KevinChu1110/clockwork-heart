# 《發條之心》背包Tab前往鍛造快捷按鈕主線合併後回歸驗收報告 (t_58e87148 / t_d9a6aa7e)

- **執行測試**：小婷（發條之心·測試 sideqa）
- **關聯任務**：`t_58e87148`（🤖 平台與維運｜合併 PR 與主線發布）、`t_d9a6aa7e`（🤖 平台與維運｜背包Tab前往鍛造快捷按鈕合進主線後的全面回歸驗收）
- **前置合併**：`agent/20261010-bag-tab-forge-shortcut`（commit 583486ce）已合入 `main`（merge commit 111dd2ed, HEAD 494fabf6）
- **交付存證目錄**：`proofs/t_58e87148/` 與 `proofs/t_d9a6aa7e/`
- **遵循規範**：
  - `review.md` 人體工學與多巴胺視覺規範：按鈕高度 >= 44px（實作 52px）、立體果凍厚底 5px、圓角 18px、零系統 Emoji、多巴胺暖橘色盤（#FFA010 暖橘、#FFD028 金黃、#1F1A3A 深藍紫描邊）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 4 張連續截圖 SHA256 完全獨立互異（無重複冒充），無黑屏/破圖。
    - 元件佈局高度 >= 44px，非裝備類消耗品/材料嚴格隱藏按鈕防誤觸，零折行、零溢出、零重疊。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留（依 review.md 0-QA28 驗證）。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_bag_weapon_selected_zh_TW.png` | `MobileLobby` 背包Tab：選中武器【鏽劍】時，右側面板顯示暖橘果凍厚底「前往鍛造」按鈕（`BtnBagGoForge`，高度 52px >= 44px，底邊 5px 立體厚底） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `6c5cd06ed68b` | 合格 (PASS) |
| 02 | `proof_02_bag_consumable_selected_hidden.png` | `MobileLobby` 背包Tab：選中消耗品【微光潤滑油】時，「前往鍛造」按鈕嚴格隱藏，原按鈕列自然等分排版 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `70a8ecefb31b` | 合格 (PASS) |
| 03 | `proof_03_bag_weapon_selected_en.png` | 英文語系 (en) 背包Tab：選中武器時按鈕顯示 "Go to Forge"，右側詳情面板全英文無 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `03b7e5fa70b4` | 合格 (PASS) |
| 04 | `proof_04_forge_dialog_transitioned.png` | 點擊「前往鍛造」後自動關閉/隱藏背包，無縫彈出天宮鐵匠 `ForgeDialog`，並精確將【鏽劍】帶入為鍛造目標 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `ea594c9f7eda` | 合格 (PASS) |

- **防作弊與真實性校驗**：4 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），通道均方差與像素極值校驗均正常（非黑屏、非純色）。
- **視覺複檢**：所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json`、`item.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **前往鍛造** | 前往锻造 | Go to Forge | 鍛造へ進む | 단조로 이동 | Ir a Forja |
| **鏽劍** | 锈剑 | Rusty Sword | 錆びた剣 | 녹슨 검 | Espada oxidada |
| **器階：第 %d 階  品質：%s** | 器阶：第 %d 阶  品质：%s | Tier: %d  Quality: %s | 器階：第 %d 階  品質：%s | 기계: 제 %d 단계  품질: %s | Nivel: %d  Calidad: %s |
| **基礎武器 · 點擊前往鍛造可進行強化** | 基础武器 · 点击前往锻造可进行强化 | Basic weapon · Tap Go to Forge to enhance | 基礎武器 · 鍛造へ進むをタップして強化 | 기본 무기 · 단조로 이동을 탭하여 강화 | Arma básica · Toca Ir a Forja para mejorar |

---

## 三、 單元與無頭測試驗證結論

- 測試腳本：
  1. `res://scripts/ui/test_bag_weapon_forge_shortcut.gd`：`TEST_BAG_WEAPON_FORGE_SHORTCUT_OK` (100% 綠燈，0 SCRIPT ERROR)。
  2. `res://scripts/ui/test_mobile_lobby.gd`：`MOBILE_LOBBY_OK` (100% 綠燈，0 SCRIPT ERROR)。
  3. `res://scripts/ui/test_weapon_swap_forge_shortcut.gd`：`TEST_WEAPON_SWAP_FORGE_SHORTCUT_OK` (100% 綠燈，0 SCRIPT ERROR)。
- 驗證項：
  1. 按鈕存在性、高度 >= 44px、圓角 18px、5px 立體厚底、多巴胺暖橘色盤、零系統 Emoji。
  2. 未選取、消耗品 (hp_s)、材料 (iron_scrap)、重要物 (key_rusty) 嚴格隱藏按鈕。
  3. 武器 (rusty_blade)、自訂裝備 (custom_shield) 精確顯示按鈕。
  4. 點擊按鈕自動關閉/隱藏背包分頁，彈出天宮鐵匠彈窗 `ForgeDialog` 並帶入裝備。
  5. 目標裝備位於三欄槽位之一時，`ForgeDialog` 自動切換對應槽位（副手武器/特殊武器）。
  6. 六語系字典映射與動態切換，非繁中無 CJK 中文殘留。
- 回歸驗證結論：主線合併後所有背包與鐵匠連動功能回歸運作完美，無衝突或破壞既有大廳架構。
