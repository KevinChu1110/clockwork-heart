# 全面回歸驗收證明 · SkillDialog 招式首選與戰鬥首發連動合進主線全站驗收 (t_b4716ab5)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）實作之「SkillDialog 招式卡片支援點擊設為首選並連動戰鬥首發出招」（`agent/20261008-skill-custom-priority-t_c007db84`，卡號 `t_c007db84`）由製作人老周乾淨合入 `main`（HEAD: `4401d05d`）後，由測試員小婷（`sideqa`）執行主線全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - `test_skill_custom_priority` (1/1 PASS, `SKILL_CUSTOM_PRIORITY_OK`)
   - `test_skill_dialog_upgrade` (1/1 PASS, `SKILL_DIALOG_UPGRADE_TEST_OK`)
   - `test_skill_dialog_dummy_practice` (1/1 PASS, `SKILL_DIALOG_DUMMY_PRACTICE_OK`)
   - `test_lobby_skill_dialog_btn` (1/1 PASS, `LOBBY_SKILL_DIALOG_BTN_TEST_OK`)
   - `test_skill_priority_badge` (1/1 PASS, `SKILL_PRIORITY_BADGE_OK`)
   - 全套 skill 相關測試 (12/12 PASS)
   - 全套 lobby 相關測試 (11/11 PASS)
   - 全套 dummy 相關測試 (5/5 PASS)
   - 全套 combat 相關測試 (16/16 PASS)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零舊詞。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底合規。
5. **項目進度維護**：`PROJECTS.json` 中之 `skill-custom-priority` 項目已透過 `project_status.py` 成功更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **自選首發出招單元測試** | `TEST_FILTER=test_skill_custom_priority ./tools/run_tests.sh` | 1/1 通過（`SKILL_CUSTOM_PRIORITY_OK`） | **PASS** |
| **招式熟練度升級單元測試** | `TEST_FILTER=skill_dialog_upgrade ./tools/run_tests.sh` | 1/1 通過（`SKILL_DIALOG_UPGRADE_TEST_OK`） | **PASS** |
| **底欄木人樁試招按鈕單元測試** | `TEST_FILTER=skill_dialog_dummy_practice ./tools/run_tests.sh` | 1/1 通過（`SKILL_DIALOG_DUMMY_PRACTICE_OK`） | **PASS** |
| **大廳心法按鈕測試** | `TEST_FILTER=lobby_skill_dialog_btn ./tools/run_tests.sh` | 1/1 通過（`LOBBY_SKILL_DIALOG_BTN_TEST_OK`） | **PASS** |
| **出招優先膠囊標籤測試** | `TEST_FILTER=skill_priority_badge ./tools/run_tests.sh` | 1/1 通過（`SKILL_PRIORITY_BADGE_OK`） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 12/12 全部通過（五族初發招式、原創招式、招式 UI、自選首選出招、多語系等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過（紅點、背包、裝備、大殿、出征等） | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 5/5 全部通過（木人樁戰鬥、結算彈窗、多語系等） | **PASS** |
| **全套戰鬥系統測試** | `TEST_FILTER=combat ./tools/run_tests.sh` | 16/16 全部通過（戰鬥姿態、怒氣施法、超載爆裂、傷害計算等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_b4716ab5/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 6 張實機全景截圖與 5 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 『設為首發』/『已設首發』按鈕高度 48px（>= 48px），寬度 104px，底邊厚底 4px，圓角 16px。
  - 當前選中首發招式時，按鈕底色為金黃柔和底 `#FFF4D0`、字色 `#9A6B00`；未選中時為白底 `#FFFFFF`、字色 `#1F1A3A`。
  - 頂部摘要連動顯示當前平常首發技能名稱，排版規律整齊。
  - SkillDialog 底欄『前往木人樁試招』按鈕尺寸：寬 210px、高 50px（>= 50px）、熱區 >= 48px、天藍立體果凍底色（`#38A0FF`）、圓角 18px、厚底 5px。
  - 排版合規：彈窗底欄左側試招按鈕、右側暖橘關閉按鈕，中間彈性撐開，完全符合橫屏雙拇指操作人體工學。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 繁中（平常首發 / 設為首發 / 已設首發）、簡中（平时首发 / 设为首发 / 已设首发）、英文（Normal Opener / Set as Opener / Opener Set）、日文（通常初手 / 初手に設定 / 初手設定済）切換自如，無 CJK 殘留與重疊截字。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_skill_custom_priority_slash_zh_TW.png` | `f218ff6cb17df9bdcc64408ece056f9530e3d863d1313e237dfe653901bb8a52` | `71952e76c208a20e128caac94cc1db64` | 繁中自選橫斬為首發：橫斬帶【平常首發】金黃膠囊標籤與【已設首發】按鈕，反戈一擊帶【設為首發】按鈕，頂部連動「平常出招：橫斬」 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_skill_custom_priority_counter_strike_zh_TW.png` | `024dc16a9e4eb328e8d98ca5e9d60c3a011e851c6401401895504c3f8d983a32` | `27167955d43d39043a6a9e461a881573` | 繁中切換反戈一擊為首發：反戈一擊帶【平常首發】膠囊標籤與【已設首發】按鈕，橫斬轉為【設為首發】，頂部連動「平常出招：反戈一擊」 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_skill_custom_priority_en.png` | `526820ab911be4506fa840cdef3ccaea8ae76bb4359c6a9b9eeed3731491122b` | `c0c843f63e7c81239650412c1571c380` | 英文語系即時在地化：Normal Opener 膠囊標籤、Opener Set / Set as Opener 操作按鈕 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_skill_custom_priority_ja.png` | `f0bb1e6ce93d0297fec5c5c0080161549f68e1e5e94d92ddfb79a936a34e22b8` | `58581c7c0ed32626fc14d0d78b693631` | 日文語系即時在地化：通常初手 膠囊標籤、初手設定済 / 初手に設定 操作按鈕 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_skill_upgrade_and_dummy_btn_zh_TW.png` | `ef21400f3c7cd7a677e28805bd3c1f36f29dcedc8747e0df13abb6bdce695c9b` | `df2bf08ae0ba1efdf62741611b055639` | 突破升階暖橘按鈕、熟練度滿、首發按鈕與底欄前往木人樁試招按鈕共存全景 | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_training_dummy_opener_slash.png` | `bf399487f9ca29c2f989fff71660077af7db7ea2b082a32d321383119155a687` | `1feaa781f894be66b75cd0875607aa27` | 點擊底欄試招按鈕進入木人樁實戰場景，實戰首發出招連動自選首發橫斬 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_skill_custom_slash.png` | `dc24eac1ba59eb8a6311b90c9697aed1cbe15f1f597042ec5f071764c819b3f8` | `5c4ac9b4005df112f907b3e02310b918` | 780x540 | 繁中自選橫斬為首發特寫（【平常首發】膠囊標籤 + 【已設首發】立體厚底按鈕） | **PASS** |
| `crop_02_skill_custom_counter_strike.png` | `de65c7b74fab889e6bd984f202a6c0f7ff9cabfdf062a9b6634a5d5764ddfd61` | `004aa4319dfe4f18d834e96fb01b0993` | 470x220 | 切換反戈一擊為首發動作區特寫（【平常首發】轉移至反戈一擊） | **PASS** |
| `crop_03_skill_custom_en.png` | `f0c3c13c2dda119ec8db9fc16a570e5b0414a83f6f452bbc9ad9792936dc7130` | `62e64a57cd3f54f2e933925cb76c7997` | 780x540 | 英文語系特寫（Normal Opener, Opener Set, Set as Opener 無穿框截字） | **PASS** |
| `crop_04_skill_custom_ja.png` | `4eaf232bb85084dd85761c7a7289e030258b269bfe3607064d8e567dcb8e5d39` | `aee54d1cabff0f8e0a38c9186e73978e` | 780x540 | 日文語系特寫（通常初手, 初手設定済, 初手に設定 漢字合規無截字） | **PASS** |
| `crop_05_skill_bottom_bar.png` | `f993ed1b3a6c57b3be3955fc9906328a9f0402df3e2beff5334b7552948b293f` | `b98bf1add2568147fc9e33e9adf157ba` | 760x100 | 底欄天藍色『前往木人樁試招』按鈕與暖橘關閉按鈕特寫 | **PASS** |
