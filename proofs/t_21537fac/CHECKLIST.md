# 全面回歸驗收證明 · 木人樁再次試招合進主線後的全站回歸驗收 (t_21537fac)

## 1. 任務背景與驗收目標
針對工程師阿翔（`sideworker2`）執行「把已過審的木人樁再次試招分支合進主線」（卡號 `t_318451d8`，commit `542dfa71`）並將 `PROJECTS.json` 更新為『已上線』（commit `debf50f2`）推上 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - `test_dummy_settlement_dialog` (1/1 PASS, `DUMMY_SETTLEMENT_DIALOG_OK`)
   - `test_dummy_settlement_i18n` (1/1 PASS, `TEST_DUMMY_SETTLEMENT_I18N_OK`)
   - `test_training_dummy` (1/1 PASS, `TRAINING_DUMMY_OK`)
   - `test_skill_dialog_dummy_practice` (1/1 PASS, `SKILL_DIALOG_DUMMY_PRACTICE_OK`)
   - `test_skill_panel_dummy_btn` (1/1 PASS, `TEST_SKILL_PANEL_DUMMY_BTN_OK`)
   - 全套 dummy 相關測試 (5/5 PASS)
   - 全套 skill 相關測試 (12/12 PASS)
   - 全套 combat 相關測試 (16/16 PASS)
   - 全套 lobby 相關測試 (11/11 PASS)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零舊詞（霧隱村/今日村莊/白霧村 零殘留）。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底雙按鈕合規、重置開打滿血連動。
5. **項目進度維護**：`PROJECTS.json` 中之 `dummy-retry-btn` 項目已成功對齊為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **再次試招結算數據卡單元測試** | `TEST_FILTER=test_dummy_settlement_dialog ./tools/run_tests.sh` | 1/1 通過（`DUMMY_SETTLEMENT_DIALOG_OK`） | **PASS** |
| **再次試招六語系即時切換測試** | `TEST_FILTER=test_dummy_settlement_i18n ./tools/run_tests.sh` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`） | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 5/5 全部通過（再次試招按鈕、重置信號、多語系、木人樁戰鬥等） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 12/12 全部通過（五族招式、自選首選、招式升階、木人樁試招按鈕等） | **PASS** |
| **全套戰鬥系統測試** | `TEST_FILTER=combat ./tools/run_tests.sh` | 16/16 全部通過（1v1/1v3、超載爆裂、怒氣出招、命中計算等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過（紅點、背包、裝備、大殿、心法彈窗按鈕等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_21537fac/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 7 張實機全景截圖與 7 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 底部左側暖橘色『再次試招』按鈕（#FFA010 厚底）寬 140px、高 48px（>= 48px），立體黑色描邊厚底。
  - 底部右側金黃色『完成試招』按鈕（#FFD028 厚底）寬 140px、高 48px（>= 48px），立體黑色描邊厚底。
  - 彈窗寬度適中，三欄數據卡清晰對稱，完全符合橫屏雙拇指操作防誤觸標準。
- [x] **重置開打流程連動**：
  - 點擊『再次試招』正確發射 `retry_requested` 信號，彈窗正常關閉，木人樁 HP 刷新為滿血 500/500、重新計時開打。
- [x] **0-QA24 / 0-QA25（六語系即時切換）**：
  - 繁中（再次試招 / 完成試招）
  - 簡中（再次试招 / 完成试招）
  - 英文（Retry Trial / Finish Trial）
  - 日文（もう一度試技 / 試技を終了）
  - 韓文（다시 연습 / 연습 완료）
  - 西文（Reintentar prueba / Finalizar prueba）
  - 切換即時刷新，無 CJK 殘留與重疊截字。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_dummy_settlement_zh_TW.png` | `9345eae5a20f78bce8bc35942b1e9ea61e6ad7ac9d68a2dab47aedcdb29bf988` | `31c69d2bd567497e61b0dc104a5ad25a` | 繁中木人試招數據卡全景：再次試招（暖橘厚底）與完成試招（金黃厚底）雙按鈕並列 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_dummy_settlement_en.png` | `7ac6454e4e699b6372626e6b9235a8816127aa8570659993edc9207e3fa98c44` | `a95a35f877e16f39004685d73be891da` | 英文版全景：Retry Trial 與 Finish Trial，Title Case 標準在地化 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_dummy_settlement_ja.png` | `4bc22b0a60b7124e757cac3ded331db2f56bde2b1da0479a98a2ecbcb24da8e9` | `20e9d271a52f4e7b25b839fd2064e6ac` | 日文版全景：もう一度試技 與 試技を終了，日文字型工整無截字 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_dummy_settlement_ko.png` | `2e109f5ca7954fca0c78772faed13cda4022d5735a4992184221cb05ed589564` | `a17cc2f502bedaffc7da11a77fb6e9b6` | 韓文版全景：다시 연습 與 연습 완료，韓文在地化流暢 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_dummy_settlement_es.png` | `fb3516f9f10e26364836d22a41477ae5443dc39f4c64d1dd7d2e2ead629a792f` | `314934775f00fc6528217fbf21364b06` | 西文版全景：Reintentar prueba 與 Finalizar prueba，無溢出重疊 | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_dummy_settlement_zh_CN.png` | `008c2aac03b19b1fad1a3da5ddc46171875633853fb53a87b3b47d18dfa84282` | `bb1c448fbdfa11b23d92193320ba33ff` | 簡中版全景：再次试招 与 完成试招，簡體字形完整無缺漏 | ✓ 無 | ✓ 零 | **PASS** |
| 07 | `proof_07_dummy_retry_triggered_combat.png` | `72524e49d225be362509b0b5b89aa04217d1ee9b201a3edfc8b2fe92b3021c80` | `faaec655ead8ab49343fcc0c1221c3af` | 點擊再次試招後戰鬥實機全景：木人樁 HP 滿血 500/500，彈窗關閉重新開打 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_buttons_zh_TW.png` | `f4a443aace1ee212fb8d8a838edd9f0b60b50a82e73ce16effd62ec74c97964d` | `27dc18a39fa9f0d64ab3e85832623e6f` | 440x70 | 繁中雙按鈕特寫（再次試招暖橘厚底 + 完成試招金黃厚底） | **PASS** |
| `crop_02_buttons_en.png` | `39ebe1f7bdcee76601a1cabd722ca5964e245415728d55353d8a252c4fe83829` | `bd7458402432eaf2ff83f9c70a09ca74` | 440x70 | 英文雙按鈕特寫（Retry Trial + Finish Trial） | **PASS** |
| `crop_03_buttons_ja.png` | `2ed4648f0118775774945a049e63b3e2dae8ce272c1c00d13633ba1d156c3176` | `3bf8372b39cd2597a607c396b3fb0240` | 440x70 | 日文雙按鈕特寫（もう一度試技 + 試技を終了） | **PASS** |
| `crop_04_buttons_ko.png` | `59ce603147bd8b98d535320cb8850e3a1b9f4e9159bdb8f5d0c7da4ab55b6a94` | `f2f70b4be0a0b1b6bbfa9c34ee75e7a0` | 440x70 | 韓文雙按鈕特寫（다시 연습 + 연습 완료） | **PASS** |
| `crop_05_buttons_es.png` | `c23986d6fd16b1028bb76ea179010afd2b941d012fb297d51fd5c91707334455` | `174777b154a2d55f8040201f102e76a5` | 440x70 | 西文雙按鈕特寫（Reintentar prueba + Finalizar prueba） | **PASS** |
| `crop_06_buttons_zh_CN.png` | `6fafa45667690e25bf37dce7f6d01518012c6c6145c495840d5ddc50d5857e1f` | `66ec6cf0343df0201e52f54e85b68be2` | 440x70 | 簡中雙按鈕特寫（再次试招 + 完成试招） | **PASS** |
| `crop_07_dummy_hp_reset.png` | `089bb189903cf27387653a0e1cc46637a45ac2ff9fb8120d34ed4fa8b23b071f` | `986a8650a7640f3e7ee70458f6e19938` | 400x150 | 右上角木人樁 HP 重置為 500/500 滿血特寫 | **PASS** |
