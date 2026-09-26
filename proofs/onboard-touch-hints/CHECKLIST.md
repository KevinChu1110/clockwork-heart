# 新手引導底列提示改觸控用語＋六語系 驗收核對清單 (onboard-touch-hints)

依據 `AGENTS.md`、`CLAUDE.md` 及 `skill_view(bravesoul, references/review.md)` 規範（0-QA15, 0-QA23, 0-QA24, 0-QA25）：

## 一、驗收總覽
- **任務名稱**：🎮 遊戲開發｜新手引導底列提示改觸控用語＋六語系 (`t_33e9446c`)
- **專案項目**：`onboard-touch-hints`
- **交付目錄**：`proofs/onboard-touch-hints/`（0-QA23 獨立專屬目錄，絕無跨卡覆蓋）

## 二、需求驗收查核表
- [x] **觸控／手機模式**：提示文字改為「點一下繼續 · 部分步驟可「稍後再說」」，完全移除「空白鍵／Space／スペース／스페이스／Espacio／空格键」。
- [x] **桌面模式**：保留原「空白鍵／下一步 · 部分步驟可「稍後再說」」，兩套依實際輸入裝置（`DisplayServer.is_touchscreen_available()` 或 `force_touch_mode`）自動判斷。
- [x] **六語系完整對齊與即時動態刷新**：
  - `zh_TW`: `點一下繼續 · 部分步驟可「稍後再說」`
  - `zh_CN`: `点一下继续 · 部分步骤可「稍后再说」`
  - `en`: `Tap to continue · Some steps can be skipped with "Later"`
  - `ja`: `タップで進む · 一部の手順は「あとで」でスキップ可能`
  - `ko`: `탭하여 계속 · 일부 단계는 「나중에」로 건너뛰기 가능`
  - `es`: `Toca para continuar · Algunos pasos se pueden omitir con «Más tarde»`
  - 監聽 `Loc.locale_changed`，開著引導動態切換語系時底列提示同步更新，切回繁中還原。
- [x] **零系統 emoji**：純文字呈現，無任何系統原生 emoji。
- [x] **零數值修改、零推 main**：僅修改 UI 表現層、i18n 字典與單元測試。

## 三、實機截圖存證（0-QA23 / 0-QA24 / 0-QA25）
截圖解析度皆為 1280x720，MD5 經查核 100% 獨立無覆蓋：

| 檔案名稱 | 模式 / 語言 | 規格 | MD5 |
|---|---|---|---|
| `proof_onboard_touch_en.png` | 觸控模式 · 英文 (en) | 1280x720 | `2d69b32b05d87a88e2113f43bbe617bf` |
| `proof_onboard_touch_ja.png` | 觸控模式 · 日文 (ja) | 1280x720 | `0551da34f7382f1cf45b804d3b29ce07` |
| `proof_onboard_touch_zh_TW.png` | 觸控模式 · 繁體中文 (zh_TW) | 1280x720 | `5de7247523f125a3837b6e1da7691324` |

## 四、測試執行結果
- **無頭冒煙測試**：
  `godot --path game --headless --quit-after 3` -> 0 errors passed
- **新手引導測試全綠**：
  `TEST_FILTER=onboard ./tools/run_tests.sh` -> 3/3 passed
  - `test_onboard_flow`: passed
  - `test_onboard_i18n`: passed（驗證桌面與觸控兩種模式六語系詞條解析、動態切換、違禁鍵名排除）
  - `test_onboard_view_dopamine`: passed
- **觸控與回歸測試全綠**：
  - `TEST_FILTER=touch ./tools/run_tests.sh` -> 2/2 passed
  - `TEST_FILTER=i18n ./tools/run_tests.sh` -> 34/34 passed
