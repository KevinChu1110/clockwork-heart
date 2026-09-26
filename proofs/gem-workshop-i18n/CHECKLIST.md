# 《發條之心》手藝工坊彈窗標題分頁按鈕六語系 查驗清單與驗收報告 (t_8226ca6c)

- **執行人**：阿翔（側案·工程師 sideworker2）
- **關聯任務**：`t_8226ca6c`（🎮 遊戲開發｜手藝工坊彈窗標題分頁按鈕六語系）
- **交付目錄**：`proofs/gem-workshop-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/gem-workshop-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名，非中文殘留。
  - `review.md 0-QA25`：查驗彈窗以外背景語系狀態，並記錄於驗收說明中。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_gem_workshop_smelt_en.png` | 熔煉分頁（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_gem_workshop_case_en.png` | 寶石櫃分頁（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 03 | `proof_gem_workshop_smelt_ja.png` | 熔煉分頁（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |
| 04 | `proof_gem_workshop_case_ja.png` | 寶石櫃分頁（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |

---

## 二、 局部特寫 Crops 驗證清單（`proofs/gem-workshop-i18n/crops/`）

- `crop_header_en.png` / `crop_header_ja.png`：彈窗主標題與兩大分頁標籤即時切換特寫。
- `crop_smelt_cards_en.png` / `crop_smelt_cards_ja.png`：三色寶石果凍卡片、碎片儲備、各階數量與熔煉／合成按鈕特寫。
- `crop_case_bonus_en.png` / `crop_case_bonus_ja.png`：全身穿戴寶石六維總加成面板特寫。
- `crop_case_actions_en.png` / `crop_case_actions_ja.png`：寶石櫃「重新盤點（Re-Inventory / 再確認）」與「一鍵鑲嵌（Quick Socket / 一括装着）」按鈕特寫。

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元測試**：
   - `test_gem_workshop.gd`：果凍化手遊規範與尺寸測試通過（TEST_GEM_WORKSHOP_OK）。
   - `test_gem_workshop_i18n.gd`：六語系字典解析、動態切換 `Loc.locale_changed` 即時刷新連動測試通過（TEST_GEM_WORKSHOP_I18N_OK）。
3. **vision_analyze 審查結論**：
   - 彈窗主體、標題、分頁、按鈕、各卡片與提示在 en 與 ja 下皆完整對應翻譯，無硬編繁中殘留。
   - 0-QA25 背景狀態備註：切換語系至 en / ja 時，大廳背景左上角世界觀引言（「世界大鐘停了。你是剛被上滿發條的兔子。」）與版本標籤（「v0.19.0 · 一周目」）仍為繁體中文，此為大廳本身未監聽 locale_changed 之固有缺陷，本單範圍限於手藝工坊彈窗，據實登載以利後續大廳修復單追蹤。
