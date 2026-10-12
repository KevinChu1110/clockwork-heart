# 全面回歸驗收證明 · SkillDialog 招式升級與木人樁試招按鈕合進主線全站驗收 (t_8fe4da3b)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）實作之「SkillDialog 招式卡片支援熟練度進度條、一鍵突破升階與體悟習得」（`agent/20261008-skill-upgrade-t_98ea7703`，卡號 `t_98ea7703`）與工程師阿翔（`sideworker2`）實作之「SkillDialog 底欄新增前往木人樁試招按鈕連動大廳」（`agent/20261008-skill-dummy-practice-t_58757a2f`，卡號 `t_58757a2f`）由製作人老周乾淨合入 `main`（HEAD: `bc004106`）後，由測試員小婷（`sideqa`）執行主線全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - `test_skill_dialog_upgrade` (1/1 PASS, `SKILL_DIALOG_UPGRADE_TEST_OK`)
   - `test_skill_dialog_dummy_practice` (1/1 PASS, `SKILL_DIALOG_DUMMY_PRACTICE_OK`)
   - `test_lobby_skill_dialog_btn` (1/1 PASS, `LOBBY_SKILL_DIALOG_BTN_TEST_OK`)
   - `test_skill_priority_badge` (1/1 PASS, `SKILL_PRIORITY_BADGE_OK`)
   - 全套 skill 相關測試 (11/11 PASS)
   - 全套 lobby 相關測試 (11/11 PASS)
   - 全套 dummy 相關測試 (5/5 PASS)
   - 全套 combat 相關測試 (16/16 PASS)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零舊詞。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底合規。
5. **項目進度維護**：`PROJECTS.json` 中之 `skill-upgrade-progress` 與 `skill-dialog-dummy-btn` 均已更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **招式熟練度升級單元測試** | `TEST_FILTER=skill_dialog_upgrade ./tools/run_tests.sh` | 1/1 通過（`SKILL_DIALOG_UPGRADE_TEST_OK`） | **PASS** |
| **底欄木人樁試招按鈕單元測試** | `TEST_FILTER=skill_dialog_dummy_practice ./tools/run_tests.sh` | 1/1 通過（`SKILL_DIALOG_DUMMY_PRACTICE_OK`） | **PASS** |
| **大廳心法按鈕測試** | `TEST_FILTER=lobby_skill_dialog_btn ./tools/run_tests.sh` | 1/1 通過（`LOBBY_SKILL_DIALOG_BTN_TEST_OK`） | **PASS** |
| **出招優先膠囊標籤測試** | `TEST_FILTER=skill_priority_badge ./tools/run_tests.sh` | 1/1 通過（`SKILL_PRIORITY_BADGE_OK`） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 11/11 全部通過（五族初發招式、原創招式、招式 UI、多語系等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過（紅點、背包、裝備、大殿、出征等） | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 5/5 全部通過（木人樁戰鬥、結算彈窗、多語系等） | **PASS** |
| **全套戰鬥系統測試** | `TEST_FILTER=combat ./tools/run_tests.sh` | 16/16 全部通過（戰鬥姿態、怒氣施法、超載爆裂、傷害計算等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_8fe4da3b/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 7 張實機全景截圖與 5 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 熟練度進度條 (ProgressBar)：高度 8px、圓角 4px、薄荷綠高飽和色條，數值「熟練 15/30」排版齊整無溢出。
  - 暖橘立體果凍『突破升階』按鈕：高 48px（熱區 >= 48px）、厚底 4px、底色暖橘（`#FFA010`），滿熟練度時準確觸發。
  - 薄荷綠立體果凍『體悟習得』按鈕：高 48px（熱區 >= 48px）、厚底 4px、底色薄荷綠（`#4ED86A`），未解鎖技達標時合規呈現。
  - 金色膠囊標籤『Lv.MAX · 極階』：滿級時穩定替換按鈕，零重疊。
  - SkillDialog 底欄『前往木人樁試招』按鈕尺寸：寬 210px、高 50px（>= 50px）、熱區 >= 48px、天藍立體果凍底色（`#38A0FF`）、圓角 18px、厚底 5px。
  - 排版合規：彈窗底欄左側試招按鈕、右側暖橘關閉按鈕，中間彈性撐開，完全符合橫屏雙拇指操作人體工學。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 繁中（前往木人樁試招 / 突破升階）、簡中（前往木人桩试招）、英文（Practice at Training Dummy / Breakthrough）、日文（木人で試技する / 突破昇階）切換自如，無 CJK 殘留與重疊截字。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_skill_progress_half_zh_TW.png` | `9db50927e906c7409526759716542dbf352c82fe461a2545ad1685c2787635a9` | `80dc2323e2424e7b846a5c7cb36d05ad` | 繁中已習得招式熟練度半滿（15/30）薄荷綠進度條與未習得招式展示全景 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_skill_upgrade_orange_btn_zh_TW.png` | `44fed0b1f817e5f20ca0e834affe584bf7ee5ccf1715b239407c52edd6be554e` | `528f24d835fb096f20f6fe809e064df6` | 滿熟練度（30/30）觸發暖橘立體果凍『突破升階』按鈕實機全景 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_skill_max_tier_gold_badge_zh_TW.png` | `665fb1318a82b41bc6ffac66e26fa3bfa8392ccd26020f92d96194627222d174` | `0a7ae6c15838ffc9087cf4d5cee37e33` | 招式滿級（Lv.3）展示『Lv.MAX · 極階』金色膠囊標籤全景（無多餘按鈕） | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_skill_upgrade_dialog_en.png` | `e1f3ebbefc15a97e5eba49e55c5ac46b1de2e81ba35fba7815acf57e527dd185` | `051256f1444906e9716fa73b70c5eae3` | 英文語系（Breakthrough / Practice at Training Dummy / Lv.MAX）即時在地化全景 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_skill_dialog_bottom_dummy_btn_zh_CN.png` | `601a3d1aee96be57f449f279a6545e0cfb3ef6208866683aa79cd14961aca8ac` | `8b69993a776fa943e7771460d0c115e5` | 簡體中文全景與底欄天藍『前往木人桩试招』按鈕實機存證 | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_skill_dialog_bottom_dummy_btn_ja.png` | `df9cd632becf2b4b5790b68ca35d5f7e74468f7d79093234343567cd653e27f7` | `df1561a019bee3b1601103fe5883b99d` | 日文語系（木人で試技する / 閉じる）即時在地化全景，新字體漢字合規無截字 | ✓ 無 | ✓ 零 | **PASS** |
| 07 | `proof_07_lobby_link_training_dummy_battle.png` | `6657186b27d8236f4c4a03a76eafcd532f851e009a8df14638e79fd9acba2263` | `3a042448b97b9f1bd99700ffd106c383` | 點擊試招按鈕後平滑關閉彈窗並切換至零消耗木人樁戰鬥場景實機存證 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_skill_progress_half.png` | `11308bd0f9d097932924e14cb8e925193146e5dd193b4ed0f4689ebc7ce85a6e` | `25a5de2b786856e9a74915f7c892c2bc` | 780x540 | 熟練度半滿薄荷綠進度條 (8px) 與卡片佈局特寫 | **PASS** |
| `crop_02_skill_upgrade_btn.png` | `d1b9e09b2d8a4baf123180fe2dcdfed0a59c838cb8ac91513da7b446ccee27d7` | `e6eaafb632c198fe007690b130a565b7` | 400x220 | 暖橘立體果凍『突破升階』按鈕（48px高、厚底4px）特寫 | **PASS** |
| `crop_03_skill_max_badge.png` | `110a409f72f89d16ea96af6c2f4a1db1b1d656b404d5aa5b572d835ce3dd0d5f` | `ca7b1564d04226fcb2535d9b7b1668fc` | 400x220 | 滿級『Lv.MAX · 極階』金色膠囊標籤特寫 | **PASS** |
| `crop_04_dummy_btn_zh_CN.png` | `68d26ad62f71afa423f52f85a6717ed61e6f44a15a976de6bbea6bc3191048ae` | `be8b330158e08ee42b9063aeccd0b867` | 760x100 | 底欄簡體中文『前往木人桩试招』按鈕特寫 | **PASS** |
| `crop_05_dummy_btn_ja.png` | `ff4f46707a218efb29d5e23d863c5c10bbb5064ae695b1163a91e62b6ce14c4a` | `1b44954695a379912ec8665ca013e9d4` | 760x100 | 底欄日文版『木人で試技する』按鈕特寫 | **PASS** |
