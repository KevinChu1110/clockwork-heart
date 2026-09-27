# t_642cd663 實機截圖與驗收清單

## 驗收項目檢核

- **任務標題**：🎮 遊戲開發｜勝利結算裝備機芯前，跟現有槽比色階再確認
- **任務卡號**：`t_642cd663`
- **做什麼**：
  1. 玩家打完關卡按「立即裝備」時：
     - 若該槽已有機芯部件 → 彈出機芯替換比較彈窗（`CompareLayer` / `CompareCard`），展示槽位名、色階名、攻/防/血數值比較（現有裝備 vs 新獲戰利品）。
     - 點擊「確認替換」（`BtnConfirmReplace`）才覆蓋該槽位（`cs.equip_part`），立即裝備按鈕切換為「已裝備」並禁用。
     - 點擊「取消替換」（`BtnCancelReplace`）或右上關閉按鈕，舊件不被覆蓋，新件安全保留在背包（`core_bag`），彈窗關閉。
     - 若該槽是空槽 → 維持現況直接一鍵裝上，不多一道確認。
  2. 六語系 `ui.json` 完整補齊替換彈窗鍵值（`機芯替換確認`、`該槽位已有裝備機芯，是否確認替換？`、`現有裝備`、`新獲戰利品`、`確認替換`、`取消替換`、`新部件已保留在機芯背包中`、`槽位：%s` 等），100% 經由 `_t()` 翻譯層。
  3. 切換至英文（en）與日文（ja）時，比較彈窗內之標題、副標、槽位名、八色階（`[Blue Tier]`、`[Gold Tier]`、`青階` 等）與數值標籤全部走在地化翻譯，零中文色階字或中文殘留。
  4. 語系切換即時生效（`_on_locale_changed` 同步更新比較彈窗）。
  5. 遵守硬限制：未修改戰鬥秒數、ATB、命中、格擋窗；零新道具、零花錢、零產新圖；全介面零系統 Emoji；沿用既有果凍彈窗與多巴胺色票。

## 測試結果

- `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
- `TEST_FILTER=test_core_replace_compare ./tools/run_tests.sh`：1/1 PASS（空槽直裝、已有槽比對取消留背包、已有槽確認覆蓋、六語系即時切換與外語無中文殘留）
- `TEST_FILTER=core ./tools/run_tests.sh`：6/6 PASS
- `TEST_FILTER=forge ./tools/run_tests.sh`：3/3 PASS

## 實機截圖存證清單 (1280x720 Framebuffer 截取)

| 編號 | 檔案名稱 | 截圖內容 | 關鍵驗證項目 | 審核結果 |
|---|---|---|---|---|
| 01 | `proof_compare_zh_TW.png` | 繁中（zh_TW）勝利結算機芯替換比較彈窗 | 標題「機芯替換確認」，展示槽位發條發電機、現有【藍階】(攻+8·血+160) 與新獲【金階】(攻+57·血+370)，按鈕「取消替換」與「確認替換」 | **通過 (PASS)** |
| 02 | `proof_cancel_bag_zh_TW.png` | 繁中（zh_TW）點擊取消後角色整備面板背包 | 現有槽位維持【藍階】，新獲部件【金階】安好保留於機芯部件背包中 | **通過 (PASS)** |
| 03 | `proof_compare_en.png` | 英文（en）勝利結算機芯替換比較彈窗 | 標題 `Core Replacement`，Slot: Mainspring Dynamo，`Currently Equipped [Blue Tier]` vs `New Loot [Gold Tier]`，按鈕 `Keep Current` 與 `Confirm Replace`，100% 英文零中文殘留 | **通過 (PASS)** |
| 04 | `proof_cancel_bag_en.png` | 英文（en）點擊取消後角色整備面板背包 | 現有槽位維持 `Blue Tier`，新件 `Mainspring Dynamo [Gold Tier]` 保留在 Core Parts Bag 中，100% 英文 | **通過 (PASS)** |

## 規範遵從檢驗

- [x] **0-QA5 / 0-QA26**：真遊戲 Framebuffer 直接擷取（1280x720，非空白圖、非 PIL 假圖）。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_642cd663/`，不污染其他任務目錄。
- [x] **0-QA28**：譯名進檔且畫面 100% 過翻譯層（`_t()` 查表，en/ja 截圖無中文 CJK 殘留）。
- [x] **0-QA29**：不逾越單卡範圍，嚴格聚焦結算機芯替換比較與確認覆蓋/取消進背包流程。
- [x] **硬限制**：零戰鬥秒數、ATB、格擋窗等數值公式更動；零額外開銷或未授權素材；零系統 Emoji。
