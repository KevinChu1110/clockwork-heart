# 木人樁試招結算數據卡新增『再次試招』按鈕驗收證明 (t_8aaa9d27)

## 1. 任務背景與驗收目標
針對木人樁試招結算數據卡 `DummySettlementDialog` 底部新增『再次試招』按鈕：
1. **多巴胺雙按鈕並列**：底部由單一完成按鈕改為『再次試招』（暖橘立體厚底 >= 48px）與『完成試招』（金黃立體厚底 >= 48px）雙鍵並列。
2. **重置連動機制**：點擊再次試招發出 `retry_requested` 自定義信號與回調，重置木人樁狀態立即重新開打，HP 刷新為滿血 500/500，計時歸零。
3. **六語系在地化**：補齊 `ui.json` 六語系（zh_TW: 再次試招、zh_CN: 再次试招、en: Retry Trial、ja: もう一度試技、ko: 다시 연습、es: Reintentar prueba）。
4. **單元測試全綠**：
   - `test_dummy_settlement_dialog.gd`：覆蓋雙按鈕尺寸、文字、`retry_requested` 信號、回調與木人樁重置戰鬥狀態斷言。
   - `test_dummy_settlement_i18n.gd`：六語系字典與節點動態切換 14/14 全數通過，零 Emoji。
5. **無頭冒煙 0 SCRIPT ERROR**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
6. **OpenGL3 實機全景與特寫存證**：依據 review.md 規範輸出 5 張全景截圖與 4 張特寫裁切圖（雜湊皆唯一）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **數據卡單元測試** | `godot --headless -s res://scripts/battle/test_dummy_settlement_dialog.gd` | 4/4 檢驗全過（`DUMMY_SETTLEMENT_DIALOG_OK`） | **PASS** |
| **六語系單元測試** | `godot --headless -s res://scripts/battle/test_dummy_settlement_i18n.gd` | 14/14 字典解析與動態切換全數通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`） | **PASS** |
| **木人樁把關測試** | `godot --headless -s res://scripts/battle/test_training_dummy.gd` | `TRAINING_DUMMY_OK` 通過 | **PASS** |
| **導師面板試招按鈕測試** | `godot --headless -s res://scripts/ui/test_skill_panel_dummy_btn.gd` | `TEST_SKILL_PANEL_DUMMY_BTN_OK` 通過 | **PASS** |
| **招式彈窗試招按鈕測試** | `godot --headless -s res://scripts/ui/test_skill_dialog_dummy_practice.gd` | `SKILL_DIALOG_DUMMY_PRACTICE_OK` 通過 | **PASS** |
| **全站規範自動檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 截圖。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_8aaa9d27/` 與 workspace 獨立目錄。
- [x] **0-QA15（雜湊唯一性）**：所有 5 張實機全景截圖與 4 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 『再次試招』按鈕尺寸：寬 200px、高 52px（>= 48px）、暖橘立體厚底（`#FFA010`）、圓角 20px、厚底 6px。
  - 『完成試招』按鈕尺寸：寬 200px、高 52px（>= 48px）、金黃立體厚底（`#FFD028`）、圓角 20px、厚底 6px。
  - 雙鍵間距 18px，水平並列置中，符合橫屏人體工學操作體驗。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 繁中（再次試招 / 完成試招）、英文（Retry Trial / Finish Trial）、日文（もう一度試技 / 試技を終了）、韓文（다시 연습 / 연습 완료）即時連動，無截字與文字重疊。
- [x] **100% 零系統原生 Emoji**：按鈕與彈窗中完全使用自製向量與純文字，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 零破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_dummy_settlement_zh_TW.png` | `db1d8ff0c69b5f6c208cbf10bbf24f23fe498bf8a8c975b21bd2f4c9cb819c08` | `f6e1d7a865a7a5fa0fdf415e0a911d9a` | 繁中結算數據卡：底部暖橘『再次試招』與金黃『完成試招』雙按鈕並列全景 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_dummy_settlement_en.png` | `c184525425bf6e28fe6039957624740d63d7c0ee3cf31661b7434e01daef11b0` | `4df9731d0b96563ee8688af29fde9724` | 英文語系在地化：Retry Trial 與 Finish Trial 雙按鈕全景 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_dummy_settlement_ja.png` | `91f99987ebc0c902c62d7aac06bb9cdc671b9fbab3f50b71a0c68d333c8a4219` | `3517ef606419e12a92a575210a1f1c9f` | 日文語系在地化：もう一度試技 與 試技を終了 雙按鈕全景 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_dummy_settlement_ko.png` | `98eb6f94275573aa12305815df16b5566f39e01c46cd99c88eb6a53ca27434d9` | `f24ae76d34834cd216c8562ac1032141` | 韓文語系在地化：다시 연습 與 연습 완료 雙按鈕全景 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_dummy_retry_triggered_combat.png` | `ce79edb4658d069503d8de2f895d5f9b681f333bc6d10dce1a3ed74e34e7d2dd` | `b65e6e2206d0e303500d7fd085935cbc` | 點擊再次試招後重置戰鬥：木人樁刷新為 500/500 HP 滿血、重新計時開打實機畫面 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_buttons_zh_TW.png` | `f4a443aace1ee212fb8d8a838edd9f0b60b50a82e73ce16effd62ec74c97964d` | `27dc18a39fa9f0d64ab3e85832623e6f` | 440x70 | 繁中『再次試招』（暖橘立體厚底）與『完成試招』（金黃立體厚底）雙按鈕特寫 | **PASS** |
| `crop_02_buttons_en.png` | `39ebe1f7bdcee76601a1cabd722ca5964e245415728d55353d8a252c4fe83829` | `bd7458402432eaf2ff83f9c70a09ca74` | 440x70 | 英文『Retry Trial』與『Finish Trial』雙按鈕特寫 | **PASS** |
| `crop_03_buttons_ja.png` | `2ed4648f0118775774945a049e63b3e2dae8ce272c1c00d13633ba1d156c3176` | `3bf8372b39cd2597a607c396b3fb0240` | 440x70 | 日文『もう一度試技』與『試技を終了』雙按鈕特寫 | **PASS** |
| `crop_04_buttons_ko.png` | `59ce603147bd8b98d535320cb8850e3a1b9f4e9159bdb8f5d0c7da4ab55b6a94` | `f2f70b4be0a0b1b6bbfa9c34ee75e7a0` | 440x70 | 韓文『다시 연습』與『연습 완료』雙按鈕特寫 | **PASS** |
