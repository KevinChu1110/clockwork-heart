# 戰鬥頂欄鎖定提示水平排版與多語系適配驗收報告 (battle-en-hud-overflow)

- **執行人**：阿翔（側案·工程師 sideworker2）
- **關聯卡號**：`t_07c57dfd`（🎮 遊戲開發｜英文戰鬥頂欄鎖定提示把左右血條擠出畫面）
- **交付目錄**：`proofs/battle_en_hud_overflow/`
- **遵循規範**：
  - `review.md 0-QA23`：獨立交付目錄，絕不覆蓋、干擾或覆寫其他任務之 proof。
  - `review.md 0-QA24`：英文與多語系名詞對齊既定詞條（Xiaobai、Titan Overseer Leo、Helm、Armor 等）。
  - `review.md 0-QA25`：全畫面多語系連動查驗。
  - 無系統 Emoji、不改動 `.github/workflows`、不動 `release/`、不產付費資產。

---

## 一、 根本原因排查與修復措施

### 1. 根本原因
- 頂部提示標籤 `%ParryHint` 原設為 `autowrap_mode = TextServer.AUTOWRAP_OFF`，且容器 `SideBars` 設為 `grow_horizontal = 2`（雙向外擴）。
- 英文及西班牙文等長譯鎖定提示字串長達 80~90 字元，單行最小寬度達 778px~826px，導致 `SideBars` 最小寬度擴增至 1360px~1468px（超過 1280 橫屏）。
- 雙向溢出後，左端 `position.x` 變為負值（-40px ~ -94px），使左側玩家角色名與 HP 被推出螢幕左邊緣截斷；右側 Boss HUD 亦被推擠超出螢幕右邊緣（1320px ~ 1374px）。
- 敵方部位面板 `PartPanel` 之子標籤未設長度截斷限制，長譯時將右側 HUD 撐大至 298px~358px，加劇擠壓。

### 2. 修復措施
- **排版防禦約束**：
  1. `%ParryHint` 開啟 `autowrap_mode = TextServer.AUTOWRAP_WORD_SMART` 與居中對齊，消除單行強制最小寬度，自適應兩側 HUD 間的 720px 安全中軸寬度。
  2. `battle.tscn` 場景預設同步補上 `autowrap_mode = 3`，防止節點初創尚未套用 Chrome 樣式時排版跳動。
  3. `PartPanel` 設定 `custom_minimum_size.x = 220`，部位名稱標籤 `lab` 與焦點提示 `_focus_hint` 套用 `TextServer.OVERRUN_TRIM_ELLIPSIS` 及 `clip_text = true`，鎖死右側寬度於標準 220px。
- **多語系文案精煉**：
  - 英文：`Locked: %s · Tab: Switch · Break armor: -DEF / Crown: Enrage`
  - 西文：`Fijado: %s · Tab: Cambiar · Romper armadura: -DEF / Corona: Enfurece`
  - 日文：`捕捉：%s · Tab で切替 · 甲破壊: 防御低下 / 冠破壊: 激怒`
  - 韓文：`고정: %s · Tab 전환 · 갑옷 파괴: 방어 하락 / 관 파괴: 격노`
  - 簡中：`锁定：%s · Tab 切换 · 破甲降防／破冠激怒`
  - 繁中：保持原案行為不變，功能完整無虞。

---

## 二、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 左右 HUD 邊距 | 頂欄排版 | 零 Emoji | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_battle_broken_zh_TW.png` | 戰鬥繁中全景（Boss 部位破損、頂欄鎖定提示、玩家 HUD、日誌） | 左 x=28, 右 edge=1252 | 單行居中無溢出 | ✓ 零 | 通過 (PASS) |
| 02 | `proof_02_battle_broken_en.png` | 戰鬥英文全景（Boss 部位破損、頂欄鎖定提示、玩家 HUD、日誌） | 左 x=28, 右 edge=1252 | 單行居中無溢出 | ✓ 零 | 通過 (PASS) |
| 03 | `proof_03_battle_broken_es.png` | 戰鬥西語全景（西語長譯鎖定提示、部位欄、日誌） | 左 x=28, 右 edge=1252 | 雙行工整居中不撐破 | ✓ 零 | 通過 (PASS) |

特寫圖存放於 `crops/`：
- `crop_top_hud_en.png`：英文頂欄全域特寫（左玩家名、HP條、中鎖定提示、右Boss血條部位欄無縫留白）。
- `crop_top_hud_zh_TW.png`：繁中頂欄全域特寫。
- `crop_top_hud_es.png`：西語長譯頂欄全域特寫。

---

## 三、 具名測試驗證 (test_battle_hud_overflow_i18n.gd)

- 指令：`TEST_FILTER=battle_hud_overflow ./tools/run_tests.sh`
- 涵蓋語系：`en`、`es`、`ja`、`ko`、`zh_TW`
- 結果：`TEST_BATTLE_HUD_OVERFLOW_I18N_OK`（1/1 PASS，無 SCRIPT ERROR）。
- 相關回歸測試：
  - `TEST_FILTER=part_break ./tools/run_tests.sh`（2/2 PASS）
  - `TEST_FILTER=hud_contrast ./tools/run_tests.sh`（1/1 PASS）
  - `TEST_FILTER=acc_leo ./tools/run_tests.sh`（1/1 PASS）
