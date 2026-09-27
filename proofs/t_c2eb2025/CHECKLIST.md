# t_c2eb2025 實機截圖與驗收清單

## 驗收項目檢核

- **任務標題**：🎮 遊戲開發｜整備已裝備機芯可卸回背包
- **任務卡號**：`t_c2eb2025`
- **做什麼**：
  1. 整備／鐵匠五槽已有機芯時可按「卸下」：
     - 呼叫既有 `CoreSystem.unequip_part(slot_id)`，被卸下的機芯安全回到未裝備機芯背包（`core_bag`），該槽位變空。
     - 點擊卸下後，畫面即時刷新（該槽變空、色階標籤更新為「未裝備」、該槽不再顯示卸下按鈕、背包多回該件）。
     - 空槽不顯示卸下按鈕，版面工整不破版。
     - 卸下後之部件可從未裝備背包一鍵直裝回空槽。
  2. 彈窗規格與無障礙手遊人體工學標準：
     - 彈窗卡片寬度：EquipCard 與 ForgeCard 均符合 740~760px 規範（`ResponsiveUi.apply_dialog_card`）。
     - 右上角均配備顯眼立體「✕」關閉按鈕（`ResponsiveUi.make_close_button`）。
     - 按鈕熱區與尺寸：卸下果凍厚底按鈕（`BtnUnequip`）高 50px（≥ 50px）、寬 88~118px（熱區 ≥ 48px）。
     - 100% 零系統 Emoji，多巴胺鮮亮珊瑚粉（`#FF5E8A`）立體果凍厚底（bottom border 5px），深藍紫描邊（`#1F1A3A`），圓角 14px。
  3. 六語系翻譯層（0-QA28, 0-QA29）：
     - 玩家可見字 100% 走 `_t()` / `ContentLoc.text("ui", key)` 翻譯層。
     - `zh_TW`（卸下）、`zh_CN`（卸下）、`en`（Remove）、`ja`（外す）、`ko`（해제）、`es`（Quitar）完整同步落地。
     - 切換語系時畫面即時刷新，英文與西文截圖經檢驗 100% 零中文 CJK 殘留。
  4. 硬限制遵守：
     - 零新道具、零產新圖、零花錢。
     - 未修改 ATB／攻速／前搖 1.85／格擋窗 0.85／命中公式。

## 測試結果

- `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
- `TEST_FILTER=test_equip_core_unequip ./tools/run_tests.sh`：1/1 PASS（卸下成功、空槽無卸下、卸下後可再裝備、彈窗尺寸與關閉鍵、鐵匠彈窗卸下、六語系即時切換）
- `TEST_FILTER=core ./tools/run_tests.sh`：10/10 PASS
- `TEST_FILTER=forge ./tools/run_tests.sh`：3/3 PASS
- `TEST_FILTER=equip ./tools/run_tests.sh`：6/6 PASS

## 實機截圖存證清單 (1280x720 Framebuffer 截取)

| 編號 | 檔案名稱 | 截圖內容 | 關鍵驗證項目 | 審核結果 |
|---|---|---|---|---|
| 01 | `proof_equip_core_equipped_zh_tw.png` | 繁中（zh_TW）整備面板機芯五槽有件 | 五槽看得到粉色「卸下」果凍厚底按鈕（高 50px、熱區 ≥ 48px），零系統 emoji，各色階圖示與名稱正常 | **通過 (PASS)** |
| 02 | `proof_equip_core_unequipped_zh_tw.png` | 繁中（zh_TW）點擊卸下發條發電機後 | 最左側發條發電機槽位變空，狀態為「未裝備」，「卸下」按鈕完全消失且不破版，下方背包多回金階發條發電機 | **通過 (PASS)** |
| 03 | `proof_equip_core_equipped_en.png` | 英文（en）整備面板機芯五槽有件 | 五槽按鈕為「Remove」，無任何中文 CJK 殘留（0-QA28），排版與間距工整 | **通過 (PASS)** |
| 04 | `proof_equip_core_unequipped_en.png` | 英文（en）點擊卸下發條發電機後 | 最左側槽位變空、狀態顯示「Unequipped」，「Remove」按鈕消失不破版，下方背包多回金階部件，零中文殘留 | **通過 (PASS)** |
| 05 | `proof_forge_core_equipped_zh_tw.png` | 繁中（zh_TW）鐵匠彈窗機芯五槽有件 | 彈窗寬 750px 置中，右上「✕」關閉按鈕，五槽部位皆有「卸下」立體果凍厚底按鈕，風格統一 | **通過 (PASS)** |
| 06 | `proof_forge_core_unequipped_zh_tw.png` | 繁中（zh_TW）鐵匠彈窗點擊卸下齒輪組後 | 傳動齒輪組槽位即時變更為「未裝備」，「卸下」按鈕隱藏，版面無破版 | **通過 (PASS)** |

## 規範遵從檢驗

- [x] **0-QA5 / 0-QA26**：真遊戲 Framebuffer 直接擷取（1280x720，xvfb-run，非空白圖、非假圖）。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_c2eb2025/`，不覆蓋也不污染其他任務目錄。
- [x] **0-QA28**：文字 100% 過翻譯層（`_t()` 查表，六語系同步，en 截圖零中文 CJK 殘留）。
- [x] **0-QA29**：不逾越單卡範圍，嚴格聚焦整備與鐵匠機芯卸下與未裝備背包回流。
- [x] **硬限制**：零戰鬥秒數、ATB、格擋窗等數值公式更動；零額外開銷或未授權素材；零系統 Emoji。
