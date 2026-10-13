# 《發條之心》TitleWallDialog 支援點擊佩戴稱號與大廳頭頂稱號名牌即時刷新連動 驗收檢查清單 (t_7269c551)

## 任務背景與目標
- **任務編號**：t_7269c551
- **功能描述**：
  1. TitleWallDialog 稱號牆卡片中，已解鎖稱號點擊支援「佩戴稱號」功能，並顯示「✓ 佩戴中」高亮果凍標籤與金黃光框（`COLOR_GOLD` #FFD028，果凍厚底 6px，高亮柔和金米底 #FFFBE8）。
  2. 串接 GameState 持久化保存玩家當前佩戴稱號（預設「初出茅廬」），提供 `get_equipped_title()` 與 `set_equipped_title()`，支援 `to_dict()`/`from_dict()` 存檔 round-trip。
  3. 大廳 `mobile_lobby.gd` 頭頂稱號名牌 `_hero_title_tag` 讀取 GameState 佩戴稱號即時刷新，換稱號即時更新文字。
  4. 支援六語系動態即時切換（zh_TW, zh_CN, en, ja, ko, es），稱號名牌與狀態標籤即時連動，零系統原生 Emoji。
  5. 撰寫單元與整合測試 `test_title_equip_lobby.gd`，產出實機截圖存證至 `proofs/t_7269c551/`，測試全數跑綠。

---

## 審查常見退回（~/.hermes/shared/clock-review-checklist.md）自查結果

| 項目 | 規範要求 | 自查狀態 | 實作與檢查細節 |
|---|---|---|---|
| **畫面與素材** | 熱區 >= 48px、佈局尺寸與邊距合理、避免節點坍塌 | ✅ 已檢查 | 稱號卡片尺寸 `Vector2(330, 84)`，點擊熱區充足；文字字級 16~18px，排版工整無溢出。 |
| **畫面與素材** | 實機截圖與 UI 排版在各語系下檢查邊界、圖層順序、底欄遮擋 | ✅ 已檢查 | 稱號牆彈窗 750px 居中置頂，大廳頭頂名牌懸浮於主角兔耳上方，雙行置中，無遮擋穿框。 |
| **畫面與素材** | 零系統 Emoji 規範 | ✅ 已檢查 | 標籤「✓ 佩戴中」使用標準 Unicode 向量文字符號 U+2713，全介面零系統原生 Emoji。 |
| **畫面與素材** | 多巴胺果凍樣式合規 | ✅ 已檢查 | 佩戴中卡片採用金黃光框（`#FFD028`、厚底 6px、光暈陰影），標籤金黃果凍厚底，符合手遊多巴胺視覺規範。 |
| **測試與證據** | 驗證截圖存證精準控制時序、連續截圖不可重複（SHA256 互異） | ✅ 已檢查 | 透過 `xvfb-run -a godot --rendering-driver opengl3` 產生 6 張真實 Framebuffer 截圖，6 張 SHA256 互異獨立。 |
| **測試與證據** | 單元測試穩定防 flaky、覆蓋關鍵分支與哨兵輸出 | ✅ 已檢查 | 測試覆蓋預設值、訊號發射、存檔持久化、大廳即時連動、點擊切換、未解鎖防護、六語系切換與哨兵 `TEST_TITLE_EQUIP_LOBBY_OK`。 |
| **程式與邏輯** | 跳轉與連動參數有效對齊、資料與 UI 同步即時更新 | ✅ 已檢查 | 點擊稱號卡片呼叫 `set_equipped_title()`，觸發 `equipped_title_changed` 訊號，大廳名牌與稱號牆雙向即時刷新。 |
| **資料與文案** | 嚴格對齊既有設計文件與用詞規範、零舊名詞 | ✅ 已檢查 | 六語系翻譯完全齊全（zh_TW: 初出茅廬/✓ 佩戴中, en: Fledgling Novice/✓ Equipped, ja: 駆け出し/✓ 装備中 等），無舊名詞。 |
| **流程與交付** | 執行 `clock-check` 零警告 | ✅ 已檢查 | `clock-check` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。 |

---

## 實機截圖存證清單 (proofs/t_7269c551/)

| 檔名 | 說明 | SHA256 (前 16 碼) | Vision 審查結果 |
|---|---|---|---|
| `proof_01_zh_TW_lobby_default_title.png` | 大廳初始頭頂名牌展示預設稱號【初出茅廬】小白（繁中） | `be19682ac0e360c3` | PASS，主角頭頂上方深色銘牌清晰顯示【初出茅廬】小白，無穿模、文字無溢出、零系統 Emoji |
| `proof_02_zh_TW_title_wall_equip_claw_parry.png` | 稱號牆【以劍抵爪】展示金黃光框與「✓ 佩戴中」高亮果凍標籤 | `295179ce0e5c6572` | PASS，金黃光框厚底 (6px) 鮮明，高亮果凍標籤「✓ 佩戴中」對齊工整，排版嚴謹，零系統 Emoji |
| `proof_03_zh_TW_lobby_equipped_linkage.png` | 佩戴稱號後大廳主角頭頂名牌即時同步刷新為【以劍抵爪】小白 | `db005190cb7d8ff8` | PASS，大廳頭頂名牌即時連動變更為【以劍抵爪】小白，金黃高亮字級清晰，零系統 Emoji |
| `proof_04_en_title_wall_equipped.png` | 英文語系稱號牆彈窗（Achievements · Title Wall），Sword Against Claw 顯示「✓ Equipped」 | `02e613f20a2c2b28` | PASS，標題與條件全英文連動，狀態標籤精確顯示「✓ Equipped」，底部「Back to Lobby」，零 CJK 殘留，零 Emoji |
| `proof_05_en_lobby_equipped_linkage.png` | 英文語系大廳頭頂名牌即時同步刷新為【Sword Against Claw】Xiaobai | `a5d6e0e3caf08c3a` | PASS，大廳名牌雙行英文排列【Sword Against Claw】Xiaobai，無文字溢出，零 CJK 殘留，零 Emoji |
| `proof_06_ja_title_wall_equipped.png` | 日語語系稱號牆彈窗（実績・称号の壁），剣もて爪を受く 顯示「✓ 装備中」，按鈕「ロビーへ戻る」 | `572b6878b56d615b` | PASS，日文常用漢字與新字體對齊，狀態標籤「✓ 装備中」，底部按鈕「ロビーへ戻る」，零系統 Emoji |

---

## 測試執行結果
- **無頭冒煙測試**：`godot --path game --headless --quit-after 3` -> **PASS (0 SCRIPT ERROR)**
- **自動化單元與整合測試**：`godot --path game --headless -s res://scripts/ui/test_title_equip_lobby.gd` -> **PASS (`TEST_TITLE_EQUIP_LOBBY_OK`)**
- **真實渲染與截圖驗證**：`xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_title_equip_lobby.gd` -> **PASS (6 獨立雜湊截圖)**
- **稱號牆迴歸測試**：
  - `test_title_wall_i18n.gd` -> **PASS (`TEST_TITLE_WALL_I18N_OK`)**
  - `test_title_catalog.gd` -> **PASS (`TITLE_OK`)**
  - `test_title_menu.gd` -> **PASS (`TITLE_MENU_OK`)**
- **大廳與存檔迴歸測試**：
  - `test_mobile_lobby.gd` -> **PASS (`MOBILE_LOBBY_OK`)**
  - `test_save_slots.gd` -> **PASS (`SAVE_SLOTS_OK`)**
- **自動合規檢查**：`clock-check` -> **PASS (✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞)**
