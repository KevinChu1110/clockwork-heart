# 停擺巨偶蓄力必殺與發條格擋驗收清單 (t_efaa460d)

- **任務 ID**：`t_efaa460d`
- **交付目錄**：`proofs/t_efaa460d/`（遵守 `review.md 0-QA23` 獨立目錄規範，絕無跨卡覆蓋）
- **規範參照**：`AGENTS.md` (驗證階梯), `review.md` (0-QA5, 0-QA23, 0-QA26, 0-QA27)

---

## 1. 0-QA26 / 0-QA5 真實機 Framebuffer 存證

所有截圖均為 1280x720 實機 Godot Viewport Texture Framebuffer 渲染截取，絕無 PIL 假圖。

| 編號 | 檔名 | 涵蓋場景與語系 | 按鈕文案 | 部位與格擋回饋 | 零 Emoji | 驗證結論 |
|---|---|---|---|---|---|---|
| 01 | `proof_01_zh_colossus_windup_parry_btn.png` | 繁中（zh_TW）失控發條獅蓄力必殺 | 右下角按鈕文案「發條格擋」（高度 72px >= 50px） | 中央綠色大字「發條格擋」倒數、出手倒數 0.7s | ✓ 零 | **通過 (PASS)** |
| 02 | `proof_02_zh_colossus_parry_success.png` | 繁中（zh_TW）完美格擋成功 | 右下角按鈕恢復「攻擊」 | 中央「完美格擋」特效、鎖定部位「甲·溢能核心」耐久條受損扣減、日誌「== 完美格擋 == 42 傷害」 | ✓ 零 | **通過 (PASS)** |
| 03 | `proof_03_en_colossus_windup_parry_btn.png` | 英文（en）失控發條獅蓄力必殺 | 右下角按鈕文案「Windup Parry」雙行整齊無截字 | 中央「Windup Parry」大字倒數、「Charged Strike」蓄力提示 | ✓ 零 | **通過 (PASS)** |
| 04 | `proof_04_ja_colossus_windup_parry_btn.png` | 日文（ja）黑鏽蒸氣巨象蓄力必殺 | 右下角按鈕文案「ぜんまいパリィ」雙行整齊無截字 | 中央「ぜんまいパリィ」大字倒數、「黒錆の蒸気巨象」0-QA27 同名 | ✓ 零 | **通過 (PASS)** |

---

## 2. 0-QA27 六語系譯名與設計文件對齊檢驗

- 設計文件：`docs/design/CORE_LOOP_REVAMP_PROPOSAL.md:84` 定案第三隻巨偶中文名為「**黑鏽蒸氣巨象**」（非釩、非汽）。
- 檢驗結果：`enemy.json` 與 `ui.json` 六語系完全一致，100% 逐語同名：
  - `zh_TW`: 黑鏽蒸氣巨象 == 黑鏽蒸氣巨象
  - `zh_CN`: 黑锈蒸气巨象 == 黑锈蒸气巨象
  - `en`: Black-Rust Steam Colossus == Black-Rust Steam Colossus
  - `ja`: 黒錆の蒸気巨象 == 黒錆の蒸気巨象
  - `ko`: 검은녹 증기 거상 == 검은녹 증기 거상
  - `es`: Coloso de Vapor de Óxido Negro == Coloso de Vapor de Óxido Negro

---

## 3. 單元測試檢驗結論

- `test_colossus_windup_parry.gd` 通過（1/1）：
  - 三隻巨偶（colossus_lion / colossus_puppet / colossus_elephant）蓄力必殺時格擋窗正確在 0.85s 開啟。
  - 時間模型鎖定：前搖 1.85s，格擋窗 0.85s（BALANCE.md §5）。
  - 成功格擋後走既有完美格擋，鎖定部位 hp 下降或已破壞，材料為既有 iron_scrap。
  - 普通關卡雜魚戰（black_ronin）按鈕文案保持「攻擊」，零「發條格擋」。
  - 六語系 ui.json 發條格擋詞條全數到位且零系統 emoji。
- `TEST_FILTER=colossus ./tools/run_tests.sh` 通過（7/7）。
- 核心戰鬥測試通過：
  - `test_battle_thumb` (PASS)
  - `test_battle_part_break_i18n` (PASS)
  - `test_battle_touch_prompt_i18n` (PASS)
  - `test_battle_events` (PASS)
  - `test_formulas` (PASS)
  - `test_parry_discipline` (PASS)
