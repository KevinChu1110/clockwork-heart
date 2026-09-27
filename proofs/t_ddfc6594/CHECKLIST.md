# t_ddfc6594 實機截圖與驗收清單

## 驗收項目檢核

- **任務標題**：🎮 遊戲開發｜整備裝備機芯前跟現有槽比色階再確認
- **任務卡號**：`t_ddfc6594`
- **做什麼**：
  1. 整備／鐵匠面板按「裝備」時：
     - 若該槽已有機芯部件 → 彈出機芯替換比較彈窗（`CompareLayer` / `CompareCard`），展示槽位名、兩邊色階名與色票（`OldColorSwatch`, `NewColorSwatch`）、攻/防/血數值比較（現有裝備 vs 新獲戰利品）。
     - 點擊「確認替換」（`BtnConfirmReplace`）才覆蓋該槽位（`cs.equip_part`），舊件回到機芯背包（`core_bag`），新件上槽。
     - 點擊「取消替換」（`BtnCancelReplace`）或右上關閉按鈕（`CompareCloseButton`），舊件不被覆蓋，新件安全保留在背包，彈窗關閉，槽與背包不變。
     - 若該槽是空槽 → 維持一鍵直裝，不彈窗，新件從背包移至該槽。
  2. 沿用既有比較彈窗與文案 key，零另外自造一套：
     - `機芯替換確認`、`該槽位已有裝備機芯，是否確認替換？`、`現有裝備`、`新獲戰利品`、`確認替換`、`取消替換`、`新部件已保留在機芯背包中`、`槽位：%s` 等。
     - 玩家可見字六語系走 `ContentLoc.text("ui", key)` / `_t()` 翻譯層，切語系即時刷新。
  3. 彈窗規格與無障礙手遊標準：
     - 彈窗卡片寬度 740px（介於 740~760px 規範）。
     - 按鈕熱區均 ≥ 48px：`BtnCancelReplace` (210x52)、`BtnConfirmReplace` (210x52)、`CompareCloseButton` (52x52)。
     - 零系統 Emoji，使用粉圓體（Open Huninn）字型與多巴胺鮮亮高飽和色票。
  4. 硬限制遵守：
     - 零新道具、零產新圖、零花錢。
     - 未修改 ATB／攻速／前搖 1.85／格擋窗 0.85／命中公式。

## 測試結果

- `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
- `TEST_FILTER=test_equip_core_replace ./tools/run_tests.sh`：1/1 PASS（空槽一鍵直裝、已有槽比對取消留背包、已有槽確認覆蓋舊件回背包、六語系即時切換與外語無中文殘留）
- `TEST_FILTER=test_core ./tools/run_tests.sh`：6/6 PASS
- `TEST_FILTER=test_lobby_bag_core_list ./tools/run_tests.sh`：1/1 PASS

## 實機截圖存證清單 (1280x720 Framebuffer 截取)

| 編號 | 檔案名稱 | 截圖內容 | 關鍵驗證項目 | 審核結果 |
|---|---|---|---|---|
| 01 | `proof_equip_core_compare_zh_tw.png` | 繁中（zh_TW）整備面板機芯替換比較彈窗 | 標題「機芯替換確認」，槽位「發條發電機」，現有【白階】(攻+2·血+60·白色票) vs 新獲【金階】(攻+57·血+270·金色票)，按鈕「取消替換」與「確認替換」，熱區 >= 48px，右上關閉按鈕 | **通過 (PASS)** |
| 02 | `proof_equip_core_compare_en.png` | 英文（en）整備面板機芯替換比較彈窗 | 標題 `Core Replacement`，Slot: Mainspring Dynamo，`Currently Equipped [White Tier]` vs `New Loot [Gold Tier]`，兩側方形色票，按鈕 `Keep Current` 與 `Confirm Replace`，100% 英文零中文殘留 | **通過 (PASS)** |
| 03 | `proof_equip_core_compare_ja.png` | 日文（ja）整備面板機芯替換比較彈窗 | 標題 `コア交換確認`，道地色階名與按鈕文案 `現在のままにする` 與 `交換する`，兩側色票正確對齊 | **通過 (PASS)** |
| 04 | `proof_equip_core_confirmed_zh_tw.png` | 繁中（zh_TW）點擊確認替換後整備面板 | 發條發電機槽位成功換上金階（高亮金框、金階文字、剩餘 7 次），換下的原白階部件出現在下方機芯背包中 | **通過 (PASS)** |

## 規範遵從檢驗

- [x] **0-QA5 / 0-QA26**：真遊戲 Framebuffer 直接擷取（1280x720，xvfb-run，非空白圖、非假圖）。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_ddfc6594/`，不污染其他任務目錄。
- [x] **0-QA25**：語系切換時背景與彈窗一併即時切換。
- [x] **0-QA28**：文字 100% 過翻譯層（`_t()` 查表，en 截圖零中文 CJK 殘留）。
- [x] **0-QA29**：不逾越單卡範圍，嚴格聚焦整備機芯裝備前色階比較與確認覆蓋/取消進背包流程。
- [x] **硬限制**：零戰鬥秒數、ATB、格擋窗等數值公式更動；零額外開銷或未授權素材；零系統 Emoji。
