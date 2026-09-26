# 過場字幕繼續提示對齊對話框驗收清單 (cutscene-hint-i18n)

卡號：t_3e23733a
執行人：阿宏（側案·程式 sideworker）
審查員：小婷（側案·測試 sideqa）
日期：2026-09-26

## 一、需求與驗收盤點

1. **底欄移除 Space / E 硬編碼，對齊對話框既有規範：**
   - 原本寫死 `▼  Space / E  繼續`（鍵盤用語、無多語系、無觸控適配）。
   - 對齊 `dialogue_box.gd` 既有規則：
     - 觸控裝置判定（`DisplayServer.is_touchscreen_available()`）顯示 `▼ 點一下繼續`。
     - 桌面環境顯示 `▼ 點擊 / Space 繼續`。
     - 全專案無殘留 `Space / E` 硬編碼（`dialogue_box.tscn` 預設字串同步清理）。

2. **字串走 ContentLoc 六語系，監聽 locale_changed 即時動態刷新：**
   - 透過 `ContentLoc.text("ui", ...)` 查詢。
   - 接入 `Loc.locale_changed` 信號，在 `_enter_tree()` 註冊、`_exit_tree()` 註銷、收到信號時執行 `_update_hint_text()` 即時刷新。
   - 六語系翻譯對照：
     - `zh_TW`：觸控 `▼ 點一下繼續`｜桌面 `▼ 點擊 / Space 繼續`
     - `zh_CN`：觸控 `▼ 点一下继续`｜桌面 `▼ 点击 / Space 继续`
     - `en`：觸控 `▼ Tap to continue`｜桌面 `▼ Click / Space to continue`
     - `ja`：觸控 `▼ タップで進む`｜桌面 `▼ クリック / Space で進む`
     - `ko`：觸控 `▼ 탭하여 계속`｜桌面 `▼ 클릭 / Space 계속`
     - `es`：觸控 `▼ Toca para continuar`｜桌面 `▼ Clic / Espacio para continuar`

3. **零系統 Emoji 規範：**
   - 箭頭使用純文字 Unicode 符號 `▼`（與深藍紫字型同色渲染），絕無系統彩色 Emoji（如 🔻 等）。

4. **護欄與規範落實：**
   - **0-QA23**：截圖腳本 `game/scripts/dev/capture_cutscene_hint_i18n.gd` 之 `OUT_DIR` 嚴格設定為 `proofs/cutscene-hint-i18n/`，無覆蓋或污染任何其他卡片目錄。
   - **0-QA24**：en（`Tap to continue`）與 ja（`タップで進む`）回查 `ui.json` 詞條設定 100% 一致，非中文語系無中文殘留。
   - **0-QA25**：動態換語系連動測試驗證通過，過場全屏字幕即時隨 `locale_changed` 刷新。
   - **不可改過場劇情正文**：未修改任何 slides 文本。
   - **不准產片、不准推 main**：全數遵守。

## 二、測試驗證

1. **單元測試全綠：**
   - 指令：`TEST_FILTER=cutscene_hint ./tools/run_tests.sh`
   - 結果：`ok test_cutscene_hint_i18n TEST_CUTSCENE_HINT_I18N_OK`
   - 涵蓋範圍：
     - 六語系字典比對（觸控與桌面）
     - 非中文語系無繁中殘留檢查
     - 無 Space / E 硬編碼檢查
     - CutscenePlayer 實例初始化、觸控模式切換
     - CutscenePlayer 動態監聽 `locale_changed` 即時刷新連動（六語系完整輪測）

2. **對話框單元測試回歸全綠：**
   - 指令：`TEST_FILTER=dialogue ./tools/run_tests.sh`
   - 結果：`ok test_dialogue_dopamine DIALOGUE_DOPAMINE_TEST_OK`

## 三、實機截圖清單 (proofs/cutscene-hint-i18n/)

1. 全景實機截圖 (1280x720)：
   - `proof_cutscene_touch_zh_tw.png`：繁中觸控模式（▼ 點一下繼續）
   - `proof_cutscene_desktop_zh_tw.png`：繁中桌面模式（▼ 點擊 / Space 繼續）
   - `proof_cutscene_touch_en.png`：英文觸控實機（▼ Tap to continue）
   - `proof_cutscene_touch_ja.png`：日文觸控實機（▼ タップで進む）
   - `proof_cutscene_desktop_en.png`：英文桌面模式（▼ Click / Space to continue）
   - `proof_cutscene_desktop_ja.png`：日文桌面模式（▼ クリック / Space で進む）

2. 顯微特寫 Crops (crops/，提示區域 460x80)：
   - `crops/crop_proof_cutscene_touch_zh_tw.png`
   - `crops/crop_proof_cutscene_desktop_zh_tw.png`
   - `crops/crop_proof_cutscene_touch_en.png`
   - `crops/crop_proof_cutscene_touch_ja.png`
   - `crops/crop_proof_cutscene_desktop_en.png`
   - `crops/crop_proof_cutscene_desktop_ja.png`

經過 Vision 逐張檢查確認，文字清晰、對齊精準、零系統 emoji、無殘留 Space/E。
