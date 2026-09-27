# t_eb5f970f 實機截圖與驗收清單

## 驗收項目檢核

- **任務標題**：🎮 遊戲開發｜機芯八色階名稱六語系（鐵匠／整備／結算不准露中文色階字）
- **任務卡號**：`t_eb5f970f`
- **做什麼**：
  1. 六語系 `ui.json` 補齊機芯八色階（灰／白／橘／藍／紫／金／綠／紅）譯名：
     - 英文用 Gray / White / Orange / Blue / Purple / Gold / Green / Red
     - 日文用對應漢字或片語（灰 / 白 / 橙 / 青 / 紫 / 金 / 緑 / 赤），不中式直譯亂造
     - 補齊繁中、簡中、韓文、西文對應單字與括號模版（`【%s】`、`【%s · %s階】%s（%s · 剩餘校準：%d 次）`、`[color=#fc8]掉落機芯部件：【%s階】%s[/color]` 等）
  2. 鐵匠校準 (`forge_dialog.gd`)、整備面板機芯槽 (`equip_panel.gd`)、勝利結算機芯掉落卡 (`battle_victory_dialog.gd`) 及戰鬥日誌 (`battle_view.gd`) 玩家可見色階名稱 100% 走 `_t()` 翻譯層。
  3. 切換至英文與日文時，鐵匠校準、整備與結算畫面上看不到任何中文色階字（如「藍」、「紫」、「階」等）。
  4. 繁中仍正常顯示灰、白、橘、藍、紫、金、綠、紅與「藍階」等字面。
  5. 語系切換即時生效。
  6. 嚴格遵守硬限制：零戰鬥秒數、ATB、格擋窗、命中公式修改；零花錢；零新圖；全介面零系統 Emoji。

## 測試結果

- `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR
- `TEST_FILTER=core_tier_i18n ./tools/run_tests.sh`：1/1 PASS（八色階六語系字典映射、鐵匠校準、整備面板、結算卡全通過）
- `TEST_FILTER=i18n ./tools/run_tests.sh`：36/36 PASS
- `TEST_FILTER=forge ./tools/run_tests.sh`：3/3 PASS
- `TEST_FILTER=core ./tools/run_tests.sh`：4/4 PASS

## 實機截圖存證清單 (1280x720 Framebuffer 截取)

| 編號 | 檔案名稱 | 截圖內容 | 關鍵色階驗證 | 審核結果 |
|---|---|---|---|---|
| 01 | `proof_forge_calibrate_zh_TW.png` | 繁中（zh_TW）天宮鐵匠機芯校準 | 校準訊息顯示「目前色階：藍階」，卡片標籤顯示「白階」 | **通過 (PASS)** |
| 02 | `proof_equip_panel_zh_TW.png` | 繁中（zh_TW）角色整備面板五槽 | 發條發電機槽位顯示「白階 · 剩餘 7 次」，繁中字型完整 | **通過 (PASS)** |
| 03 | `proof_forge_calibrate_en.png` | 英文（en）天宮鐵匠機芯校準 | 訊息顯示 `Current Tier: Blue`，五槽顯示 `White Tier`，無中文色階字 | **通過 (PASS)** |
| 04 | `proof_equip_panel_en.png` | 英文（en）角色整備面板五槽 | 五槽顯示 `White Tier · 7 Left`，按鈕顯示 `Calibrate`，無中文 | **通過 (PASS)** |
| 05 | `proof_forge_calibrate_ja.png` | 日文（ja）天宮鐵匠機芯校準 | 訊息顯示 `現在の階級：青階`，五槽顯示 `白階`，按鈕顯示 `校正`，無中文「藍」 | **通過 (PASS)** |
| 06 | `proof_equip_panel_ja.png` | 日文（ja）角色整備面板五槽 | 五槽顯示 `白階 · 残り 7 回`，按鈕顯示 `校正`，日文詞彙純正 | **通過 (PASS)** |
| 07 | `proof_victory_drop_en.png` | 英文（en）戰鬥勝利機芯部件卡 | 掉落卡色階標籤顯示 `[Blue Tier]`，無中文色階字 | **通過 (PASS)** |
| 08 | `proof_victory_drop_ja.png` | 日文（ja）戰鬥勝利機芯部件卡 | 掉落卡色階標籤顯示 `【青階】`，符合日文字典 | **通過 (PASS)** |

## 規範遵從檢驗

- [x] **0-QA5 / 0-QA26**：真遊戲 Framebuffer 直接擷取，非 PIL 繪製或手繪假圖。
- [x] **0-QA23**：截圖獨立輸出至 `proofs/t_eb5f970f/`，不污染其他任務目錄。
- [x] **0-QA28**：譯名進檔且畫面 100% 過翻譯層（八色階名稱在六語系 `ui.json` 完整補齊，且所有 UI 標籤與提示文字均經由 `_t()` 翻譯）。
- [x] **0-QA29**：不逾越單卡範圍，嚴格鎖定機芯色階名稱六語系多語化。
- [x] **硬限制**：未修改戰鬥時間模型、數值公式；零花錢；零新圖；零系統 Emoji。
