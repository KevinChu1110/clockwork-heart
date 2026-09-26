# 《發條之心》角色分頁武器槽與屬性小卡六語系 查驗清單與驗收報告 (t_607b26ba)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_607b26ba`（🎮 遊戲開發｜角色分頁武器槽與屬性小卡六語系）
- **交付目錄**：`proofs/char-tab-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/char-tab-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名（如「聚魂殿」、「拳套」、「生命力」），非中文殘留。英文／西文經演算法與 Vision 雙重確認 100% 零中文字元殘留。
  - `review.md 0-QA25`：查驗大廳背景、頂欄、左側紙娃娃卡、右側武器槽與屬性卡及底部 Dock 語系連動狀態，全畫面維持同一語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_char_tab_en.png` | 角色分頁全景（en 英文全景，武器槽／提示／5張屬性小卡／頂欄／Dock） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_char_tab_ja.png` | 角色分頁全景（ja 日文全景，武器槽／提示／5張屬性小卡／頂欄／Dock） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |
| 03 | `proof_char_tab_zh_TW.png` | 角色分頁全景（zh_TW 繁中對照，武器槽／提示／5張屬性小卡／頂欄／Dock） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 繁中 | 合格 (PASS) |

---

## 二、 局部特寫 Crops 驗證清單（`proofs/char-tab-i18n/crops/`）

- `crop_char_tab_right_en.png`：右側武器輪替配置（Primary Weapon / Secondary Weapon / Special Weapon）、提示欄與 5 張屬性小卡英文特寫。
- `crop_char_tab_right_ja.png`：右側武器輪替配置（メイン武器 / サブ武器 / 絶技武器）、提示欄與 5 張屬性小卡日文特寫。
- `crop_char_tab_right_zh_TW.png`：右側武器輪替配置（首選武器 / 副手武器 / 絕技武器）、提示欄與 5 張屬性小卡繁體中文特寫。

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元與整合測試**：
   - `test_mobile_lobby.gd`：新增 `_test_character_tab_i18n()` 完整覆蓋 zh_TW、zh_CN、en、ja、ko、es 六語系下：
     - 機體外觀標題、更衣按鈕
     - 武器輪替配置標題與副標
     - 3 個武器槽位（SlotTitle、WeaponInfo）
     - 武器槽切換選中態與動態提示列（HintLabel）
     - 機體戰鬥屬性標題與戰力徽章
     - 5 張獨立屬性小卡（生命力、物理攻擊、物理防禦、暴擊率、怒氣量表之標題、副標、數值）
     - en / es 零 CJK 殘留斷言與全語系零系統 Emoji 斷言
     - 測試執行結果：`MOBILE_LOBBY_OK`。
3. **Vision 視覺審核**：
   - `proof_char_tab_en.png`：所有文字均為英文，無中文殘留，無 Emoji，排版對齊整齊，底層 Dock 與頂欄同步連動（0-QA25 通過）。
   - `proof_char_tab_ja.png`：所有文字均為日文，漢字詞彙如「聚魂殿」「拳套」皆經語系檔確認符合既定日語譯名（0-QA24 通過）。
