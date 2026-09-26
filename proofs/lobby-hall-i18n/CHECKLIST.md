# 《發條之心》大廳左側四殿堂卡標題副標六語系 查驗清單與驗收報告 (t_48d09604)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_48d09604`（🎮 遊戲開發｜大廳左側四殿堂卡標題副標六語系）
- **交付目錄**：`proofs/lobby-hall-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/lobby-hall-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名（如「演武競技」、「冒険依頼」），非中文殘留。
  - `review.md 0-QA25`：查驗大廳背景、頂欄、右側出征卡與底部 Dock 語系連動狀態，全畫面維持同一語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_lobby_hall_village_en.png` | 大廳村莊全景（en 英文全景，四殿堂卡標題與副標） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_lobby_hall_village_ja.png` | 大廳村莊全景（ja 日文全景，四殿堂卡標題與副標） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |
| 03 | `proof_lobby_hall_village_zh_TW.png` | 大廳村莊全景（zh_TW 繁中對照，四殿堂卡標題與副標） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 繁中 | 合格 (PASS) |

---

## 二、 局部特寫 Crops 驗證清單（`proofs/lobby-hall-i18n/crops/`）

- `crop_hall_cards_en.png`：左側四殿堂卡（Celestial Blacksmith / Craft Workshop / Martial Arena / Adventure Bounties）英文標題與副標題特寫。
- `crop_hall_cards_ja.png`：左側四殿堂卡（天宮の鍛冶屋 / 工芸工房 / 演武競技 / 冒険依頼）日文標題與副標題特寫。
- `crop_hall_cards_zh_TW.png`：左側四殿堂卡（天宮鐵匠 / 手藝工坊 / 演武競技 / 冒險委託）繁體中文標題與副標題特寫。

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元測試**：
   - `test_lobby_hall_i18n.gd`：六語系字典解析、動態切換 `Loc.locale_changed` 即時刷新連動測試通過（LOBBY_HALL_I18N_OK）。
   - `test_mobile_lobby.gd`：大廳四大殿堂卡片熱區、自繪圖示、果凍厚底、彈窗連動測試通過（MOBILE_LOBBY_OK）。
   - `test_lobby_equip_i18n.gd`：裝備綱要六語系切換通過（LOBBY_EQUIP_I18N_OK）。
   - `test_i18n.gd`：全語系字詞完整度測試通過（I18N_OK）。
3. **像素顯微驗證**：
   - `tools/verify_hall_cards_pixels.py`：觸控高度 >= 48px、果凍厚底 thickness（未選取 4px、選取 5px）、自繪圖示像素數 > 80px 全數通過（ALL_HALL_CARDS_PIXEL_VERIFICATIONS_PASSED）。
4. **vision_analyze 審查結論**：
   - 四張殿堂卡在 en 與 ja 下皆清楚呈現標題與副標題，字級適中無截字。
   - 0-QA25 檢查：頂欄（Shop/Settings 或 ショップ/設定）、右側出征卡（Set Out to Battle 或 出征する）、底部 Dock（五頁籤）全數同步切換為同一語系。
   - 0-QA24 檢查：日文下「演武競技」、「冒険依頼」符合日文漢字規範。
