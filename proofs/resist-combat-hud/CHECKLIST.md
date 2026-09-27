# 抗性吃力／過載戰鬥場上顯示受傷加深驗收報告 (resist-combat-hud)

任務卡號：`t_a9b01e4b`
負責人：阿翔（sideworker2）
日期：2026-09-27

---

## 一、需求對照與成果

| 項次 | 需求描述 | 實作方案 | 驗收證據 |
|---|---|---|---|
| 1 | 玩家 underlevel 易傷係數 ×1.2（吃力）或 ×1.5（過載）時，戰鬥場上顯示一句玩家可見提示：檔名＋倍率 | `BattleView` 左上角玩家狀態區（怒氣條下方）新增多巴胺果凍徽章 `ResistNotice`，吃力顯示「吃力 · 受傷 ×1.2」，過載顯示「過載 · 受傷 ×1.5」 | 吃力金黃底 `#FFD028`、過載珊瑚粉紅底 `#FF5E8A`，深藍紫描邊 `#1F1A3A`，粉圓體 13px；文字清晰可讀 |
| 2 | 安全檔（×1.0）不顯示這句，避免多餘字 | 當易傷係數 <= 1.0 時，`resist_notice.visible = false` 且文字為空，完全不佔空間 | 實機截圖 proof_05 (zh) 與 proof_06 (en) 達標時 100% 無提示，單元測試斷言通過 |
| 3 | 六語系、切語系即時刷新。沿用既有「安全／吃力／過載」譯名，不准另造一套 | 沿用出征卡既有譯名（zh_TW, en, zh_CN, ja, ko, es），切語系時透過 `_on_locale_changed` 觸發 `_refresh_hud` 即時切換 | 六語系單元測試全數通過，en 實機截圖「Strained · Dmg ×1.2」、「Overload · Dmg ×1.5」 |
| 4 | 提示看得到、不擋血條與攻擊鈕、無系統 emoji | 位於左上角 `SideBars/PlayerSide` 最下方，完全在血條下方（不擋血條），離右下角攻擊鈕相隔整個螢幕（不擋攻擊鈕）；純文字＋果凍底板，零系統 emoji | 1280x720 實機截圖與局部裁切驗證，無任何重疊或遮擋 |
| 5 | 只准動易傷提示顯示，不准改命中公式、不准改 ATB／攻速／前搖 1.85／格擋窗 0.85 | 戰鬥核心計時常數、公式、ATB 邏輯完全零更動 | 單元測試 `_test_timings_and_formulas_untouched` 斷言 1.85s / 0.85s 與傷害計算全綠 |

---

## 二、實機 1280x720 截圖存檔 (`proofs/resist-combat-hud/`)

- `proof_01_zh_strained_1280x720.png`：繁中 (zh_TW) 吃力檔（差 2 級，×1.2），提示「吃力 · 受傷 ×1.2」
- `proof_02_zh_overload_1280x720.png`：繁中 (zh_TW) 過載檔（差 6 級，×1.5），提示「過載 · 受傷 ×1.5」
- `proof_03_en_strained_1280x720.png`：英文 (en) 吃力檔（差 2 級，×1.2），提示「Strained · Dmg ×1.2」
- `proof_04_en_overload_1280x720.png`：英文 (en) 過載檔（差 6 級，×1.5），提示「Overload · Dmg ×1.5」
- `proof_05_zh_safe_nodisplay_1280x720.png`：繁中 (zh_TW) 達標安全檔（差 0 級，×1.0），無提示
- `proof_06_en_safe_nodisplay_1280x720.png`：英文 (en) 達標安全檔（差 0 級，×1.0），無提示
- `crops/`：左上角玩家狀態面板 1:1 局部細節裁切圖（對照字體、果凍邊框與位置）

---

## 三、驗收檢核清單

- [x] **0-QA5 / 0-QA26**：走 `xvfb-run -a godot` 從 Viewport Framebuffer 截取，非 PIL 偽造，尺寸嚴格 1280x720，每張 ~1.2MB。
- [x] **0-QA28**：六語系 `ui.json` 完整同步，文字 100% 走 ContentLoc / _t 翻譯層。
- [x] **零系統 Emoji**：全域無彩色系統 Emoji，純淨粉圓體文字。
- [x] **戰鬥秒數未動**：前搖 1.85s、格擋窗 0.85s 零更動，`test_colossus_windup_parry.gd` 8/8 全綠。
- [x] **單元測試全綠**：`test_resist_combat_hud.gd` 4 大項單元測試全數通過（達標無提示、差1-4級×1.2、差>=5級×1.5、六語系即時切換）。
- [x] **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 零 SCRIPT ERROR，exit code 0。
