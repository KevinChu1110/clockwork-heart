# 實機驗收證明 · SkillDialog 招式卡片自選首發出招與戰鬥連動驗收 (t_c007db84)

## 1. 任務背景與驗收目標
針對任務 `t_c007db84`「🎮 遊戲開發｜SkillDialog 招式卡片支援點擊設為首選並連動戰鬥首發出招」，工程師阿宏（`sideworker`）完成以下實作：
1. **SkillDialog 招式卡片操作按鈕**：已習得攻擊招式卡片右側提供『設為首發』/『已設首發』操作按鈕（高 48px，熱區 >= 48px，立體果凍圓角厚底樣式）。
2. **SkillSystem 與跨存檔持久化**：
   - 提供 `get_preferred_skill`、`set_preferred_skill`、`clear_preferred_skill`、`has_preferred_skill` API。
   - `GameState` 支援 `preferred_skills: Dictionary` 跨存檔保存（`to_dict` / `from_dict`）。
   - `pick_battle_skill(hp_ratio, weapon_line)` 優先回傳玩家偏好首發招式（即使其 CATALOG priority 小於其他已習得技能）。
3. **戰鬥與木人樁連動**：木人樁與實戰開戰時（HP ratio 1.0）確實優先施放該招式。
4. **多語系支援**：六語系（zh_TW, zh_CN, en, ja, ko, es）翻譯齊全，支援即時切換刷新。
5. **單元與回歸測試全綠**：
   - `test_skill_custom_priority.gd` (1/1 PASS, `SKILL_CUSTOM_PRIORITY_OK`, 0 SCRIPT ERROR)。
   - 全套 skill 測試 12/12 通過。
   - 全套 lobby 測試 11/11 通過。
   - 全套 dummy 測試 5/5 通過。
   - 全套 combat 測試 16/16 通過。
6. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底合規。

---

## 2. 自動化測試執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR | **PASS** |
| **自選首發出招單元測試** | `TEST_FILTER=test_skill_custom_priority ./tools/run_tests.sh` | 1/1 通過（`SKILL_CUSTOM_PRIORITY_OK`） | **PASS** |
| **出招優先膠囊標籤測試** | `TEST_FILTER=skill_priority_badge ./tools/run_tests.sh` | 1/1 通過（`SKILL_PRIORITY_BADGE_OK`） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 12/12 全部通過 | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過 | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 5/5 全部通過 | **PASS** |
| **全套戰鬥系統測試** | `TEST_FILTER=combat ./tools/run_tests.sh` | 16/16 全部通過 | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_c007db84/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 5 張實機全景截圖與 4 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 『設為首發』/『已設首發』按鈕高度 48px（>= 48px），寬度 104px，底邊厚底 4px，圓角 16px。
  - 當前選中首發招式時，按鈕底色為金黃柔和底 `#FFF4D0`、字色 `#9A6B00`；未選中時為白底 `#FFFFFF`、字色 `#1F1A3A`。
  - 頂部摘要連動顯示當前平常首發技能名稱，排版規律整齊。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 繁中（設為首發 / 已設首發 / 平常首發）、簡中（设为首发 / 已设首发 / 平时首发）、英文（Set as Opener / Opener Set / Normal Opener）、日文（初手に設定 / 初手設定済 / 通常初手）切換自如，無 CJK 殘留與重疊截字。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_skill_custom_priority_slash_zh_TW.png` | `29ea195bd514c691bef65258fc6d920352738af14a168a57847b9d4545e7cb6c` | `255d459766667e8e9e5d5d5abb4b5629` | 繁中自選橫斬為首發：橫斬帶【平常首發】金黃膠囊標籤與【已設首發】按鈕，反戈一擊帶【設為首發】按鈕，頂部摘要連動「平常出招：橫斬」 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_skill_custom_priority_counter_strike_zh_TW.png` | `37b8434d3a4e436c8f099e88f9cf423fecee6f14d08387e29add65ecb13f6990` | `c69e1580d7e099ce0b8d7c94f7b7bef1` | 繁中切換反戈一擊為首發：反戈一擊帶【平常首發】膠囊標籤與【已設首發】按鈕，橫斬轉為【設為首發】，頂部摘要連動「平常出招：反戈一擊」 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_skill_custom_priority_en.png` | `394c637b17390fb41dc792886367cd9a3f350dc67b81463ff754b4c43b4f1ca1` | `2c7cd130eaef8a84d88a5e4aefcf17b5` | 英文語系即時在地化：Normal Opener 膠囊標籤、Opener Set / Set as Opener 操作按鈕 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_skill_custom_priority_ja.png` | `a2bd4377c2fbc9f6901bdcfafb2dcae71feb7517a2b148011fcd9708c70b83d3` | `3b8c637a6975a685d6b90f009bc62699` | 日文語系即時在地化：通常初手 膠囊標籤、初手設定済 / 初手に設定 操作按鈕 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_training_dummy_opener_slash.png` | `ba9f351dde9ce87d35d8b9d21c17f8b9d24776f51eb6964ee52441d88c2db43d` | `ff2070508c32399db5d919bdf8700731` | 點擊試招按鈕進入木人樁實戰場景，實戰首發出招確實連動自選招式（橫斬） | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切圖清單 (crops/)

| 裁切檔名 | SHA256 | MD5 | 尺寸 | 涵蓋區域與驗證重點 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_skill_custom_slash.png` | `e923437158504b1b0f70dee2e4c22b15d798b25f7c5d380741dbe164c27d99f6` | `bee75ed4c7cf8f64dd0d2cab8ff993c6` | 780x540 | 繁中自選橫斬為首發特寫（【平常首發】膠囊標籤 + 【已設首發】立體厚底按鈕） | **PASS** |
| `crop_02_skill_custom_counter_strike.png` | `3e7ef0b5fd5bf91d26e795af7e31b1560bb6c68027a072adf11a01f2a672b7e7` | `4171d6ba239ae55974d0c4a4595ec1ed` | 470x220 | 切換反戈一擊為首發動作區特寫（【平常首發】轉移至反戈一擊） | **PASS** |
| `crop_03_skill_custom_en.png` | `e684d492d7bd05b6eb5173281c05effcd8dbb21da4ef0735b70a79c051601d8f` | `36319642d4eb9bbe8e49c826e33cf27b` | 780x540 | 英文語系特寫（Normal Opener, Opener Set, Set as Opener 無穿框截字） | **PASS** |
| `crop_04_skill_custom_ja.png` | `0e4a30038fcb25b543ec9df788f8d9437c9329d6bee8a89749271c7f2ae9f99f` | `3c8f217df6a5b3c79fd3b2c69d4b1410` | 780x540 | 日文語系特寫（通常初手, 初手設定済, 初手に設定 漢字合規無截字） | **PASS** |
