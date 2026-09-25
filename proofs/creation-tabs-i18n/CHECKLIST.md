# 創角分頁與確認鈕六語系落地驗收清單 (creation-tabs-i18n)

卡號：t_9409c5c5
執行人：阿宏（側案·程式）
日期：2026-09-26

## 一、驗收要求達成盤點

1. **六語系 ui.json 齊全度與 key 對齊：**
   - 新增與補齊詞條：
     - `首發`：`首發`(zh_TW)／`首发`(zh_CN)／`Launch`(en)／`初期`(ja)／`초기`(ko)／`Lanzamiento`(es)
     - `擴充`：`擴充`(zh_TW)／`扩充`(zh_CN)／`Expansion`(en)／`拡張`(ja)／`확장`(ko)／`Expansión`(es)
     - `確認選擇 · 踏上旅途`：`確認選擇 · 踏上旅途`(zh_TW)／`确认选择 · 踏上旅途`(zh_CN)／`Confirm Selection · Begin Journey`(en)／`選択確認 · 旅立ち`(ja)／`선택 확인 · 여정 시작`(ko)／`Confirmar Selección · Emprender el Viaje`(es)
     - `返回`：`返回`(zh_TW)／`返回`(zh_CN)／`Back`(en)／`戻る`(ja)／`돌아가기`(ko)／`Volver`(es)
   - 檔案：`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 的 `ui.json` 均已寫入，以繁中原文當 key。
   - 五語系 key 數 100% 對齊（`zh_CN`、`en`、`ja`、`ko`、`es` 各 2123 個 key，`zh_TW` 165 個 key）。
   - 單元測試：`godot --path game --headless -s res://scripts/autoload/test_i18n.gd` 通過（I18N_OK）。

2. **創角介面動態即時切換：**
   - 頂部 `BtnTab_launch` 與 `BtnTab_expansion` 分頁按鈕支援 Loc，並在 `Loc.locale_changed` 信號下即時刷新。
   - 底部 `BtnConfirm`（`確認選擇 · 踏上旅途`）與 `BtnBack`（`返回`）以及 `BtnResetDefault`（`還原預設`）支援 Loc，並在 `Loc.locale_changed` 信號下即時刷新。
   - `switch_tab()` 支援繁中原文、英文標記與在地化文字呼叫。

3. **實機截圖存證（proofs/creation-tabs-i18n/，0-QA23）：**
   - 創角首發頁（Launch Tab）：
     - `proof_creation_launch_zh_TW.png`
     - `proof_creation_launch_en.png`
     - `proof_creation_launch_ja.png`
   - 創角擴充頁（Expansion Tab）：
     - `proof_creation_expansion_zh_TW.png`
     - `proof_creation_expansion_en.png`
     - `proof_creation_expansion_ja.png`
   - 大廳背景與底部 Dock 連動同步切換（0-QA25 檢查）：
     - `proof_lobby_dock_zh_TW.png`
     - `proof_lobby_dock_en.png`
     - `proof_lobby_dock_ja.png`
   - 顯微特寫 Crops（`crops/`）：
     - `crops/crop_tabs_{zh_TW,en,ja}.png`
     - `crops/crop_actions_{zh_TW,en,ja}.png`
     - `crops/crop_dock_{zh_TW,en,ja}.png`

4. **日／韓漢字翻譯核實（0-QA24 規範）：**
   - 日文下頂部顯示「初期」「拡張」，確認鈕顯示「選択確認 · 旅立ち」，返回鈕顯示「戻る」，對齊 `ja/ui.json` 詞條設定，合規非漏翻。

5. **無頭冒煙與測試全綠：**
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR。
   - `TEST_FILTER=creation ./tools/run_tests.sh`：5/5 PASSED（含 test_creation_tabs_i18n）。
   - `TEST_FILTER=i18n ./tools/run_tests.sh`：3/3 PASSED（含 test_creation_tabs_i18n）。
