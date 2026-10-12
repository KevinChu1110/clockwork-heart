# 全面回歸驗收證明 · 木人樁歷史最佳 DPS 紀錄合進主線後的全站回歸驗收 (t_c1e38003)

## 1. 任務背景與驗收目標
針對工程師阿翔（`sideworker2`）執行「把已過審的木人樁最佳 DPS 紀錄分支合進主線」（卡號 `t_90b5b929`，merge commit `32933f66`）並將 `PROJECTS.json` 更新為『已上線』（commit `0a61226d`）推上 `origin/main` 後，由測試員小婷（`sideqa`）在 `main` 主線執行全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - `test_dummy_settlement_record` (1/1 PASS, `TEST_DUMMY_SETTLEMENT_RECORD_OK`)
   - `test_dummy_settlement_dialog` (1/1 PASS, `DUMMY_SETTLEMENT_DIALOG_OK`)
   - `test_dummy_settlement_i18n` (1/1 PASS, `TEST_DUMMY_SETTLEMENT_I18N_OK`)
   - `test_training_dummy` (1/1 PASS, `TRAINING_DUMMY_OK`)
   - `test_skill_dialog_dummy_practice` (1/1 PASS, `SKILL_DIALOG_DUMMY_PRACTICE_OK`)
   - `test_skill_panel_dummy_btn` (1/1 PASS, `TEST_SKILL_PANEL_DUMMY_BTN_OK`)
   - 全套 dummy 相關測試 (6/6 PASS)
   - 全套 skill 相關測試 (12/12 PASS)
   - 全套 lobby 相關測試 (11/11 PASS)
   - 全套 combat 相關測試 (16/16 PASS)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零舊詞（霧隱村/今日村莊/白霧村 零殘留）。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖與特寫裁切圖，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底雙按鈕合規、新紀錄果凍標籤與歷史最佳 DPS 數值清晰對齊。
5. **項目進度維護**：`PROJECTS.json` 中之 `dummy-dps-record` 項目已確認維持為『已上線』。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **歷史最佳DPS單元測試** | `TEST_FILTER=test_dummy_settlement_record ./tools/run_tests.sh` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_RECORD_OK`） | **PASS** |
| **數據卡結構測試** | `TEST_FILTER=test_dummy_settlement_dialog ./tools/run_tests.sh` | 1/1 通過（`DUMMY_SETTLEMENT_DIALOG_OK`） | **PASS** |
| **數據卡六語系切換測試** | `TEST_FILTER=test_dummy_settlement_i18n ./tools/run_tests.sh` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`） | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 6/6 全部通過（最佳紀錄、再次試招、重置信號、多語系等） | **PASS** |
| **全套招式系統測試** | `TEST_FILTER=skill ./tools/run_tests.sh` | 12/12 全部通過（五族招式、自選首選、招式升階、木人樁試招按鈕等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 11/11 全部通過（紅點、背包、裝備、大殿、心法彈窗按鈕等） | **PASS** |
| **全套戰鬥系統測試** | `TEST_FILTER=combat ./tools/run_tests.sh` | 16/16 全部通過（1v1/1v3、超載爆裂、怒氣出招、命中計算等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_c1e38003/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 9 張實機全景截圖與 9 張特寫裁切圖之 MD5 / SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 新紀錄膠囊標籤（#FFD028 金黃底，#1F1A3A 深藍紫描邊，果凍厚底 4px，圓角 10px）。
  - 未超越紀錄時底部清晰顯示「歷史最佳：XXX DPS」（#7A6E8A 灰紫深藍文字）。
  - 底部左側暖橘色『再次試招』按鈕（#FFA010 厚底）寬 140px、高 48px（>= 48px），立體黑色描邊厚底。
  - 底部右側金黃色『完成試招』按鈕（#FFD028 厚底）寬 140px、高 48px（>= 48px），立體黑色描邊厚底。
  - 數據卡對稱整潔，無文字溢出或穿透。
- [x] **0-QA24 / 0-QA25（六語系即時切換）**：
  - 繁中（新紀錄 / 歷史最佳：XXX DPS / 再次試招 / 完成試招）
  - 簡中（新纪录 / 历史最佳：XXX DPS / 再次试招 / 完成试招）
  - 英文（New Record / Best: XXX DPS / Retry Trial / Finish Trial）
  - 日文（新記録 / 歴代最高：XXX DPS / もう一度試技 / 試技を終了）
  - 韓文（신기록 / 최고 기록: XXX DPS / 다시 연습 / 연습 완료）
  - 西文（Nuevo récord / Mejor récord: XXX DPS / Reintentar prueba / Finalizar prueba）
  - 即時切換無需重啟，無缺漏與截字。
- [x] **100% 零系統原生 Emoji**：按鈕、HUD、卡片標籤與彈窗中完全使用自製向量/藝術字與純文字，無系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | MD5 | 涵蓋內容與驗收重點 | 破圖 | 零 Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_new_record_zh_TW.png` | `0432daa211dff4741a352a3bd420567f88049de029048639aa2479bd65034450` | `75abb9ca240eb9d2a0cddcc9a11143e7` | 繁中新紀錄全景：DpsCard 右上角金黃果凍「新紀錄」標籤（#FFD028 帶深藍紫描邊） | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_new_record_en.png` | `bf88a4a7befd3349bd32c929796ee2f9eaa6bdac2fbbd96250c64e702980e25a` | `e24fe1a173eecf62eb491f69e19a3973` | 英文新紀錄全景：DpsCard 右上角 \"New Record\" 標籤 | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_new_record_ja.png` | `4efe447ab1f676b8d6b4180a516120db5d07a82277265872fc6c74e1b2fdc469` | `59aeb6cd546b124d48f1dcbc35ea612b` | 日文新紀錄全景：DpsCard 右上角 \"新記録\" 標籤 | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_no_record_zh_TW.png` | `9473100d6f477b9f687695e1d09d07abc8419176295d4887b9f57e3458af5548` | `8ba15d29b953f8fe73305ce2f5b2e814` | 繁中未破紀錄全景：DpsCard 底部標示「歷史最佳：250.0 DPS」 | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_no_record_en.png` | `37119f8d980df78fc0f71805e23a04e9cef01a8f15855db4ca6304a2574a211d` | `7c92e23e9f0996bcbd5649ea0576968d` | 英文未破紀錄全景：DpsCard 底部標示 \"Best: 250.0 DPS\" | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_no_record_ja.png` | `fc5127f13559e8b45c01e4fc80628fb3d2d63508924b047fe123816586df625a` | `936a2df3e5d299c793bf8256448b999c` | 日文未破紀錄全景：DpsCard 底部標示 \"歴代最高：250.0 DPS\" | ✓ 無 | ✓ 零 | **PASS** |
| 07 | `proof_07_no_record_ko.png` | `0ca9072659e7ccde0cdad70a880f413e1b513ba5528b0498964bda7c638d522f` | `01a090bf9ef3cfe9996bd27184cd1e0e` | 韓文未破紀錄全景：DpsCard 底部標示 \"최고 기록: 250.0 DPS\" | ✓ 無 | ✓ 零 | **PASS** |
| 08 | `proof_08_no_record_es.png` | `5105998850169aef604e5400945d1ead9be7599d11834d6cade5509078ffcc59` | `de49615bc7f2cef3a96fe8b89b710a05` | 西文未破紀錄全景：DpsCard 底部標示 \"Mejor récord: 250.0 DPS\" | ✓ 無 | ✓ 零 | **PASS** |
| 09 | `proof_09_no_record_zh_CN.png` | `17ad44c4963474bad1a456d0c54b95a8f99da3fe0596361682388b3677aee9c7` | `0bb0c1ebd622cf155b575bf39781e95b` | 簡中未破紀錄全景：DpsCard 底部標示 \"历史最佳：250.0 DPS\" | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/, 260x160)

| 特寫檔名 | SHA256 | MD5 | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---|:---:|:---|:---:|
| `crop_01_new_record_dps_zh_TW.png` | `631fa2cc9e44c2b395203b677e590d44c46d738ac5068582af8eeb086448fab2` | `97f1e106e7c669f97e35d47384af14bb` | 260x160 | 繁中 DpsCard 新紀錄金黃果凍膠囊標籤特寫 | **PASS** |
| `crop_02_new_record_dps_en.png` | `33b8f1d89c7fa15353f5e6c9154b93e9fc8109f668ff136e8bbbf53bfac8cf69` | `09925cc6c2e9a26712ae4c3130abb267` | 260x160 | 英文 DpsCard \"New Record\" 標籤特寫 | **PASS** |
| `crop_03_new_record_dps_ja.png` | `a7541a60fcb66275764faad3fe6f04a31645675f5e9122e9496ff4ca0db94d64` | `c0d5a7e0b3303b88a87720e1953a6260` | 260x160 | 日文 DpsCard \"新記録\" 標籤特寫 | **PASS** |
| `crop_04_no_record_dps_zh_TW.png` | `11ef12cf816b87f744db57a8ed035f995327688606949843a88d0949914ec2bb` | `586280bddd8761af18ea3ea13bec92f5` | 260x160 | 繁中 DpsCard 歷史最佳 DPS 標籤特寫 | **PASS** |
| `crop_05_no_record_dps_en.png` | `88047cf1dff63c3c9d1d35e66b68135c70786701e21f39aa264bd65ce9c2213f` | `b12c604d344121bfb88e5e48ca29d057` | 260x160 | 英文 DpsCard \"Best: 250.0 DPS\" 標籤特寫 | **PASS** |
| `crop_06_no_record_dps_ja.png` | `320dbf582e118a440b5537fc44904e49f2e670eaf6e6fdab9c5b79039c2be9b8` | `d556ecfe264fcfa06489d3fdbde547ae` | 260x160 | 日文 DpsCard \"歴代最高：250.0 DPS\" 標籤特寫 | **PASS** |
| `crop_07_no_record_dps_ko.png` | `62745702ea147cac698d2d9efa4aa31cf423fde0a92a6d979897efdff41b4377` | `98c9be1f194b977fccb455e8f5eb74b0` | 260x160 | 韓文 DpsCard \"최고 기록: 250.0 DPS\" 標籤特寫 | **PASS** |
| `crop_08_no_record_dps_es.png` | `1309057b4bb73d4e466cd574f54f704c80330dade4542140c39a77a869626e4d` | `b1d26c144db79022e43e957351c7aee3` | 260x160 | 西文 DpsCard \"Mejor récord: 250.0 DPS\" 標籤特寫 | **PASS** |
| `crop_09_no_record_dps_zh_CN.png` | `d1585f2ed29cdb19c6ba07b0abb4aa7024fd59346519fa2fe8309fc0d87f84c9` | `bc2f8858244609cf294e5d53e243938b` | 260x160 | 簡中 DpsCard \"历史最佳：250.0 DPS\" 標籤特寫 | **PASS** |
