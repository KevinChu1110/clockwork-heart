# 探索性 QA 驗收報告 · 每日發條接到停擺巨偶合主線後找破圖 (t_912c8ab4)

- **任務 ID**：`t_912c8ab4`
- **執行者**：小婷（側案·測試 sideqa）
- **關聯 PR / 主線 Commit**：`9a34a1c7 feat(daily): 每日發條做完若還有巨偶次數一鍵前往停擺巨偶`
- **規範依據**：`AGENTS.md`（驗證階梯）、`references/review.md`（0-QA5, 0-QA23, 0-QA24, 0-QA25, 0-QA26）

---

## 一、規範合規性查核

| 規範編號 | 規範項目 | 檢驗標準 | 查核結果 |
|:---|:---|:---|:---:|
| **0-QA5 / 0-QA26** | 真實 Framebuffer 擷取 | 必須使用 Godot Viewport Texture Framebuffer 原生擷取，嚴禁 PIL／手繪假圖 | **通過 (PASS)** |
| **0-QA23** | 專屬獨立輸出目錄 | OUT_DIR 嚴格限定為 `proofs/t_912c8ab4/`，絕無覆蓋或污染其他任務目錄 | **通過 (PASS)** |
| **0-QA24** | 語系翻譯正確性 | 查核 en／ja 等多語系在地化文字，排除未翻譯或 CJK 異常殘留 | **通過 (PASS)** |
| **0-QA25** | 大廳背景連動 | 彈窗開啟與語系切換時，大廳背景（頂部狀態欄、底部 Dock）同步連動切換 | **通過 (PASS)** |
| **零 Emoji 規範** | 杜絕系統 Emoji | 全介面與按鈕禁止出現原生 Emoji，採用專屬手繪／自繪風格圖示 | **通過 (PASS)** |
| **舊功能回歸** | 既有功能無損 | 大廳主介面、四區出征、發條衣櫥換裝等既有核心功能完全正常 | **通過 (PASS)** |

---

## 二、實機截圖存證清單 (1280x720 原生 Framebuffer)

輸出目錄：`proofs/t_912c8ab4/`

| 編號 | 檔案名稱 | 語言/場景 | 視覺檢查項 | MD5 雜湊值 | 判定 |
|:---:|:---|:---|:---|:---|:---:|
| 01 | `proof_01_windup_with_colossus_zh.png` | 繁中 (zh_TW) | 每日發條完成後（巨偶次數 3/3），同時顯示暖橘果凍「前往停擺巨偶」與薄荷綠「前往出征」，按鈕高度 >= 48px，零系統 Emoji | `acf00312c01af3b594106ab2d0819b8f` | **PASS** |
| 02 | `proof_02_windup_no_colossus_zh.png` | 繁中 (zh_TW) | 每日發條完成後（巨偶次數 0/3），「前往停擺巨偶」按鈕正確隱藏，原本「前往出征」按鈕維持正常顯示 | `f0b52e3b6338f4cf83a1e14ca2020551` | **PASS** |
| 03 | `proof_03_windup_with_colossus_en.png` | 英文 (en) | 查英文截字/折行：按鈕「Go to Stalled Colossus」文字單行置中完整、無溢出或截字，背景與 Dock 完整連動英文 | `d79cc247cd60f60821ce8ed4122d4419` | **PASS** |
| 04 | `proof_04_windup_with_colossus_ja.png` | 日文 (ja) | 查日文截字/折行：按鈕「停止した巨偶へ」排版完整自然無溢出，背景與 Dock 完整連動日文 | `696eeecf6b2cdba658da0dcf27c7184b` | **PASS** |
| 05 | `proof_05_old_feature_lobby.png` | 大廳主介面 (zh_TW) | 舊功能回歸：主角小白立繪與紙娃娃正常渲染、頂欄數值完整、左側四殿堂與底部 Dock 均正常無破圖 | `955f869b2db54822b39d2eb902054972` | **PASS** |
| 06 | `proof_06_old_feature_sortie_colossus.png` | 出征停擺巨偶 (zh_TW) | 舊功能回歸：點擊巨偶按鈕或切換出征，停擺巨偶模式正常切換、今日剩餘 3/3 與三隻巨偶卡片（失控發條獅等）顯示正常 | `ff86274c5ff0892f751ad5f738420f71` | **PASS** |
| 07 | `proof_07_old_feature_wardrobe.png` | 衣櫥換裝 (zh_TW) | 舊功能回歸：衣櫥彈窗正常開啟、左側紙娃娃即時預覽、右側服飾與塗裝卡片正常選取、底部確認按鈕完整 | `10f61884ae7c99a794bf27c6c733286b` | **PASS** |

---

## 三、自動化與無頭測試驗證紀錄

1. **無頭冒煙測試**：
   ```bash
   godot --path game --headless --quit-after 3
   ```
   - 結果：`0 SCRIPT ERROR`，正常退出（Exit code 0）。

2. **每日發條接到停擺巨偶專案測試**：
   ```bash
   TEST_FILTER=test_windup_to_colossus ./tools/run_tests.sh
   ```
   - 結果：`1/1 passed` (`TEST_WINDUP_TO_COLOSSUS_OK`)。

3. **發條每日系統全域回歸測試**：
   ```bash
   TEST_FILTER=windup ./tools/run_tests.sh
   ```
   - 結果：`3/3 passed` (`test_windup_daily`, `test_windup_daily_i18n`, `test_windup_to_colossus`)。

4. **停擺巨偶系統全域回歸測試**：
   ```bash
   TEST_FILTER=colossus ./tools/run_tests.sh
   ```
   - 結果：`6/6 passed` (`test_colossus_defeat_hint`, `test_colossus_battle`, `test_colossus_daily`, `test_colossus_exp`, `test_colossus_part_scrap`, `test_windup_to_colossus`)。

5. **大廳介面回歸測試**：
   ```bash
   TEST_FILTER=lobby ./tools/run_tests.sh
   ```
   - 結果：`6/6 passed` (`test_lobby_bag_i18n`, `test_lobby_equip_i18n`, `test_lobby_hall_i18n`, `test_lobby_poke_toast_i18n`, `test_lobby_sortie_i18n`, `test_mobile_lobby`)。

6. **紙娃娃與衣櫥回歸測試**：
   ```bash
   TEST_FILTER=wardrobe ./tools/run_tests.sh
   ```
   - 結果：`3/3 passed` (`test_paperdoll_wardrobe_save`, `test_wardrobe_thumbnails`, `test_wardrobe_i18n`)。

7. **彈窗對比度測試**：
   ```bash
   TEST_FILTER=dialog_contrast ./tools/run_tests.sh
   ```
   - 結果：`1/1 passed` (`test_dialog_contrast`)。

---

## 四、驗收結論

- **畫面真實性**：全部 7 張截圖均由 Godot Viewport Texture 原生 Framebuffer 擷取，零 PIL／假圖。
- **功能完整性**：
  1. 每日發條完成後，有巨偶次數時正確顯示暖橘果凍「前往停擺巨偶」按鈕；巨偶次數用罄時正確隱藏。
  2. 英文與日文環境下，按鈕文字與彈窗內容均正確在地化，無單字截字、折行或溢出按鈕邊界。
  3. 大廳主畫面、出征停擺巨偶、發條衣櫥三大核心舊功能運作完全正常，無破圖或樣式跑版。
  4. 全介面符合多巴胺鮮亮色盤與立體果凍厚底規範，無任何系統原生 Emoji。
- **結論**：**通過 (PASS)**，符合上線標準。
