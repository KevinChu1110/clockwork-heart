# 全面回歸驗收證明 · 大廳招式心法按鈕與優先標籤合進主線全站驗收 (t_5fc8b2fb)

## 1. 任務背景與驗收目標
針對工程師阿宏（`sideworker`）實作之「大廳角色頁新增『招式心法』入口按鈕連動 SkillDialog」（`agent/20261008-lobby-skill-btn`，卡號 `t_c914852d`）與工程師阿翔（`sideworker2`）實作之「SkillDialog 招式卡片顯示當前出招優先膠囊標籤」（`agent/20261008-skill-priority-badge-t_cbafae97`，卡號 `t_cbafae97`）由製作人老周乾淨合入 `main`（HEAD: `da1f711d`）後，由測試員小婷（`sideqa`）執行主線全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - `test_lobby_skill_dialog_btn` (1/1 PASS, `LOBBY_SKILL_DIALOG_BTN_TEST_OK`)
   - `test_skill_priority_badge` (1/1 PASS, `SKILL_PRIORITY_BADGE_OK`)
   - 全套 skill 相關測試 (9/9 PASS)
   - 全套 lobby 相關測試 (11/11 PASS)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零舊詞。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底合規。
5. **項目進度維護**：`PROJECTS.json` 中之 `lobby-skill-dialog-btn` 與 `skill-priority-badge` 均已更新為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **大廳按鈕交互與樣式測試** | `TEST_FILTER=lobby_skill_dialog_btn ./tools/run_tests.sh` | 1/1 通過（`LOBBY_SKILL_DIALOG_BTN_TEST_OK`） | **PASS** |
| **招式出招優先膠囊標籤測試** | `TEST_FILTER=skill_priority_badge ./tools/run_tests.sh` | 1/1 通過（`SKILL_PRIORITY_BADGE_OK`） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 9/9 全部通過（五族初發招式、原創招式、招式 UI、多語系等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過（紅點、背包、裝備、大殿、出征等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_5fc8b2fb/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 6 張實機全景截圖與 6 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 大廳角色頁『招式 · 核心心法』按鈕高度 50px（>= 50px）、熱區 >= 48px、立體厚底 5px、圓角 18px、底色 COLOR_SKY（天藍色），立體陰影層次分明。
  - SkillDialog 寬度 760px，頂部關閉「✕」按鈕 50x50px，底部亦具備 140x50px 圓角關閉按鈕。
  - PriorityBadge 膠囊標籤：平常首發金黃底（#FFF4D0）搭配深棕金字（#9A6B00）；危急應急天藍底（#F0F7FF）搭配天藍字（#38A0FF）；圓角 12px、上下內距 4px、字級 13px 加粗，零 13px 以下難辨小字。
- [x] **0-QA24 / 0-QA25（多語系即時切換）**：
  - 角色頁按鈕在繁中下為「招式 · 核心心法」，英文下即時切換為「Skills & Passives」，零文字溢出穿框。
  - SkillDialog 內戰鬥出招優先摘要與 PriorityBadge 膠囊標籤在繁中（平常首發 / 危急應急）、英文（Normal Opener / Crisis Emergency）、日文（通常発動 / 緊急時発動）切換自如，無 CJK 殘留與重疊。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_lobby_character_tab_skill_btn_zh_TW.png` | `0038a0cce3eff62d56d4f7001f7ddad629b38eb5cdc260f50b45e50a250fc18b` | `67f05ebc6931e3b3a655bd865b5dd5b9` | 大廳角色頁（Tab.CHARACTER）左側『招式 · 核心心法』天藍果凍立體厚底按鈕實機全景 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_lobby_character_tab_skill_btn_en.png` | `7a50a2d1c70216ef50837d8329121bb3170dbbfb97db115905f78202817a83ff` | `b5291e0a8f2c896c28548052ed38f094` | 大廳角色頁英文語系（Skills & Passives）即時切換實機全景，零文字穿框 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_skill_dialog_popup_normal_badge_zh_TW.png` | `75bbbb72107d66211020e984bebd765dd3c6783f71dcb8dfb446b4ac823a8354` | `84e083c17af0b0d9c2ba45d5cbefb6aa` | 點擊按鈕彈出 SkillDialog，頂部戰鬥優先出招摘要與斬擊卡片「平常首發」金黃膠囊標籤 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_skill_dialog_popup_panic_badge_zh_TW.png` | `3fd531a1901081ae02aea78e43abee8da69b30f01aeda7c5d6ad5b7fec914a4d` | `a213f967846e5512bde33d7b14c71605` | 習得應急技能後，SkillDialog 同時呈現「平常首發」與「危急應急」雙膠囊標籤與連動摘要 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_skill_dialog_popup_en.png` | `89dcc5d577b7dd6a3e7002a88c7fdb89f15a3525bcfe420e3db819efb25de944` | `423e65b7250b6062c30da58c36cc2eab` | SkillDialog 英文語系（Normal Opener / Crisis Emergency）即時在地化全景，零 CJK 殘留 | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_skill_dialog_popup_ja.png` | `f4ce86d37eca4c5d613d956e69ff93987dde0d1fe9763818d00aae50a4453ed5` | `301cb9319b03e16c684ed838c4e79d8b` | SkillDialog 日文語系（通常発動 / 緊急時発動）即時在地化全景，新字體漢字合規 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_lobby_skill_btn_zh_TW.png` | `0a6d75211c51ed3187e33291a7571ad8db45b6070f68d1776f8ae8021d807f91` | `62ca076dfd5ab965b600922324ea9f55` | 328x70 | 大廳角色頁左側『招式 · 核心心法』多巴胺天藍立體厚底按鈕特寫 | **PASS** |
| `crop_02_lobby_skill_btn_en.png` | `b1e5446330e32a1edcc825336e34157e6c21a6ff933bf6cd2fa6770cede330ac` | `628dcb9453f1b38fb12b62d21a8b0917` | 328x70 | 角色頁英文版『Skills & Passives』按鈕特寫，排版均勻防誤觸 | **PASS** |
| `crop_03_skill_dialog_normal_zh_TW.png` | `6887b8b6c78a54033cd976d784a44318e97822863f9555948949aefef16e1665` | `5f1b905b1cd1a75a0d24bdb28a679ed1` | 760x560 | SkillDialog 初始態：頂部優先摘要與「平常首發」金黃膠囊標籤特寫 | **PASS** |
| `crop_04_skill_dialog_panic_zh_TW.png` | `84a93a46400cb98afe27fc5e4d4643279c34a533e3d1c817d094daf1376481ab` | `75e764f710cff02a71c62fa8aced51be` | 760x560 | SkillDialog 雙標籤態：「平常首發」金黃與「危急應急」天藍膠囊標籤特寫 | **PASS** |
| `crop_05_skill_dialog_en.png` | `23f3c1407ecc9e38c5b02aa987c077096e09d658b0713f05d661d1f42197bcae` | `13e21b1188ffc125b4cce09253b241e3` | 760x560 | SkillDialog 英文版：Normal Opener 與 Crisis Emergency 雙標籤特寫 | **PASS** |
| `crop_06_skill_dialog_ja.png` | `8afda4e7913d74748224cf4aca1d7b6aabed70ad8e6ca935cd0d89c059e0557e` | `918d2a0a345435cfc74ebe74b3b33742` | 760x560 | SkillDialog 日文版：通常発動 與 緊急時発動 雙標籤特寫 | **PASS** |
