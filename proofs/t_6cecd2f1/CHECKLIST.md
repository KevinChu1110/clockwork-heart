# 停擺巨偶出征卡世界觀副標 驗收查核表 (t_6cecd2f1)

## 一、任務要求與改動項目
- [x] **世界觀副標**：失控發條獅、霧鐘提線人偶、黑鏽蒸氣巨象三張出征卡各加入 20–40 字世界觀副標。
  - 巨偶-1（失控發條獅）：`胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。`（37字）
  - 巨偶-2（霧鐘提線人偶）：`白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。`（38字）
  - 巨偶-3（黑鏽蒸氣巨象）：`冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。`（37字）
- [x] **CANON 對齊**：零毛皮、金屬板件、上鍊發條、零系統 Emoji、不准舊 IP（無葫蘆／翠嶺／餘燼／魔王）。
- [x] **名稱逐字對齊**：第三隻準確逐字對齊命名為「黑鏽蒸氣巨象」（非「鐧」、非「汽」），對齊 `docs/design/CORE_LOOP_REVAMP_PROPOSAL.md`（第 84、233 行）。
- [x] **六語系對齊（review.md 0-QA27）**：
  - 同一隻在 `enemy.json` 與 `ui.json` 譯名完全相等，經 `verify_colossus_i18n_equality.py` 全 6 語系驗證通過：
    - zh_TW: `黑鏽蒸氣巨象`
    - zh_CN: `黑锈蒸气巨象`
    - en: `Black-Rust Steam Colossus`
    - ja: `黒錆の蒸気巨象`
    - ko: `검은녹 증기 거상`
    - es: `Coloso de Vapor de Óxido Negro`
- [x] **排版無溢出**：
  - 橫屏出征卡完整看見副標，自動折行，不截字、不換行壓住出征鈕。
  - 繁中、英文、日文實機截圖完整無溢出，邊距舒適，右側出征鈕清晰居中。

## 二、實機 Framebuffer 截圖清單（0-QA23 / 0-QA26）
| 序號 | 檔案路徑 | 語系 | 驗收重點 | Vision 查驗結果 |
|---|---|---|---|---|
| 01 | `proofs/t_6cecd2f1/proof_colossus_blurb_zh_tw.png` | 繁中 (zh_TW) | 三張出征卡副標完整顯示、不截字、不壓鈕、零 Emoji、黑鏽蒸氣巨象逐字對齊 | **通過 (PASS)** |
| 02 | `proofs/t_6cecd2f1/proof_colossus_blurb_en.png` | 英文 (en) | 三張卡英文副標無溢出、不壓鈕、零 Emoji、名稱為 Black-Rust Steam Colossus | **通過 (PASS)** |
| 03 | `proofs/t_6cecd2f1/proof_colossus_blurb_ja.png` | 日文 (ja) | 三張卡日文副標無溢出、不壓鈕、零 Emoji、名稱為 黒錆の蒸気巨象 | **通過 (PASS)** |

## 三、自動化測試通過清單
1. `TEST_FILTER=colossus ./tools/run_tests.sh`：6/6 全部通過（test_colossus_defeat_hint, test_colossus_battle, test_colossus_daily, test_colossus_exp, test_colossus_part_scrap, test_windup_to_colossus）
2. `TEST_FILTER=i18n ./tools/run_tests.sh`：35/35 全部通過（含 test_i18n, test_enemy_name_i18n, test_lobby_sortie_i18n 等）
3. `python3 tools/verify_colossus_i18n_equality.py`：6 語系對齊驗證通過 (ALL 6 LOCALES COLOSSUS NAMES EQUAL VERIFIED)
