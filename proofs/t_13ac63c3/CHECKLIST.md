# 全面回歸驗收證明 · DummySettlementDialog 支援歷史最佳 DPS 紀錄與新紀錄徽章 (t_13ac63c3)

## 1. 任務背景與驗收目標
針對任務 `t_13ac63c3`（DummySettlementDialog 支援歷史最佳 DPS 紀錄與新紀錄徽章）：
1. **存檔持久化**：在 `game/scripts/autoload/game_state.gd` 新增 `best_dummy_dps: float = 0.0` 屬性，並對齊 `to_dict()`、`from_dict()`、`reset_new_game()` 存檔持久化。
2. **最佳紀錄比對與徽章**：在 `game/scripts/battle/dummy_settlement_dialog.gd` 新增最佳紀錄比對：
   - 若當前 DPS > best_dummy_dps，更新 best_dummy_dps，並在 DPS 數據卡右上角展示金黃果凍「新紀錄」膠囊標籤（#FFD028 帶深藍紫描邊，零 Emoji）。
   - 若未超越則顯示「歷史最佳：XXX DPS」輔助說明（深藍紫/灰紫文字清晰標示）。
3. **六語系支援**：補齊 zh_TW/zh_CN/en/ja/ko/es 六語系字典 key，並支援 `Loc.locale_changed` 即時切換刷新。
4. **單元與回歸測試**：撰寫 `test_dummy_settlement_record.gd` 覆蓋新紀錄與未破紀錄兩種邏輯分支，確保 0 SCRIPT ERROR，全套 dummy 測試全綠。
5. **手遊人因與視覺規範**：無系統 Emoji，多巴胺配色，OpenGL3 實機截圖存證齊全。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **歷史最佳DPS單元測試** | `TEST_FILTER=test_dummy_settlement_record ./tools/run_tests.sh` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_RECORD_OK`），覆蓋新紀錄/未破紀錄/存檔/六語系 | **PASS** |
| **數據卡結構測試** | `TEST_FILTER=test_dummy_settlement_dialog ./tools/run_tests.sh` | 1/1 通過（`DUMMY_SETTLEMENT_DIALOG_OK`） | **PASS** |
| **數據卡六語系切換測試** | `TEST_FILTER=test_dummy_settlement_i18n ./tools/run_tests.sh` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`） | **PASS** |
| **全套木人樁測試** | `TEST_FILTER=test_dummy ./tools/run_tests.sh` | 3/3 全部通過 | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結，無退休舊詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_13ac63c3/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 9 張實機全景截圖與 9 張特寫裁切圖之 SHA256 雜湊值均獨立相異，無重複或黑屏。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 新紀錄膠囊標籤（#FFD028 金黃底，#1F1A3A 深藍紫描邊，果凍厚底 4px，圓角 10px）。
  - 未超越紀錄時底部清晰顯示「歷史最佳：XXX DPS」（#7A6E8A 灰紫深藍文字）。
  - 數據卡對稱整潔，無文字溢出或穿透。
- [x] **六語系即時切換**：
  - 繁中（新紀錄 / 歷史最佳：XXX DPS）
  - 簡中（新纪录 / 历史最佳：XXX DPS）
  - 英文（New Record / Best: XXX DPS）
  - 日文（新記録 / 歴代最高：XXX DPS）
  - 韓文（신기록 / 최고 기록: XXX DPS）
  - 西文（Nuevo récord / Mejor récord: XXX DPS）
  - 即時切換無需重啟，無缺漏與截字。
- [x] **100% 零系統原生 Emoji**：所有介面完全使用純文字與向量元件，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | 涵蓋內容與驗收重點 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_01_new_record_zh_TW.png` | `901be67e8fe6db61bc781b997cc932caf6e2fc5ab897ee129cd32633394ebeec` | 繁中新紀錄全景：DpsCard 右上角金黃果凍「新紀錄」標籤（#FFD028 帶深藍紫描邊） | **PASS** |
| 02 | `proof_02_new_record_en.png` | `8ff404e8a1cf687a806926988ed7d6591aed1a573a60b14bf0429607bf4f3c68` | 英文新紀錄全景：DpsCard 右上角 "New Record" 標籤 | **PASS** |
| 03 | `proof_03_new_record_ja.png` | `92fcd33bc3aa3bfda5ba943f1c9e4a07ecef35b6a05116721626b7b30c6d73b2` | 日文新紀錄全景：DpsCard 右上角 "新記録" 標籤 | **PASS** |
| 04 | `proof_04_no_record_zh_TW.png` | `221a312c90c4fa4a76b3ace3d2f97878a7157136f79968dd3e6ca239ef025140` | 繁中未破紀錄全景：DpsCard 底部標示「歷史最佳：250.0 DPS」 | **PASS** |
| 05 | `proof_05_no_record_en.png` | `58408c02dafb36cd06b862c204aee705bd9a0ee3b7c46d09a23d78d432893cb7` | 英文未破紀錄全景：DpsCard 底部標示 "Best: 250.0 DPS" | **PASS** |
| 06 | `proof_06_no_record_ja.png` | `719a00eb943044de90305e28bb8da279cadd655c85dba19f1611d2835aabb17c` | 日文未破紀錄全景：DpsCard 底部標示 "歴代最高：250.0 DPS" | **PASS** |
| 07 | `proof_07_no_record_ko.png` | `9b8929f899c2327e54b114f3072a76edcf058b58b44fb9be7edd57392943a526` | 韓文未破紀錄全景：DpsCard 底部標示 "최고 기록: 250.0 DPS" | **PASS** |
| 08 | `proof_08_no_record_es.png` | `a8f506c3266f1243de132d07aa004befbebd1f6240d17606478d43d744672688` | 西文未破紀錄全景：DpsCard 底部標示 "Mejor récord: 250.0 DPS" | **PASS** |
| 09 | `proof_09_no_record_zh_CN.png` | `3104d654660b5b8b1c661b3a8d6a4dcd4355a858eb5c5c908b60867b772b07c1` | 簡中未破紀錄全景：DpsCard 底部標示 "历史最佳：250.0 DPS" | **PASS** |

---

## 5. 特寫裁切圖清單 (Crops, 260x160)

| 編號 | 特寫圖檔名 | SHA256 | 特寫區域 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `crops/crop_01_new_record_dps_zh_TW.png` | `631fa2cc9e44c2b395203b677e590d44c46d738ac5068582af8eeb086448fab2` | 繁中 DpsCard 新紀錄膠囊標籤特寫 | **PASS** |
| 02 | `crops/crop_02_new_record_dps_en.png` | `33b8f1d89c7fa15353f5e6c9154b93e9fc8109f668ff136e8bbbf53bfac8cf69` | 英文 DpsCard "New Record" 標籤特寫 | **PASS** |
| 03 | `crops/crop_03_new_record_dps_ja.png` | `a7541a60fcb66275764faad3fe6f04a31645675f5e9122e9496ff4ca0db94d64` | 日文 DpsCard "新記録" 標籤特寫 | **PASS** |
| 04 | `crops/crop_04_no_record_dps_zh_TW.png` | `11ef12cf816b87f744db57a8ed035f995327688606949843a88d0949914ec2bb` | 繁中 DpsCard 歷史最佳 DPS 標籤特寫 | **PASS** |
| 05 | `crops/crop_05_no_record_dps_en.png` | `88047cf1dff63c3c9d1d35e66b68135c70786701e21f39aa264bd65ce9c2213f` | 英文 DpsCard "Best: 250.0 DPS" 標籤特寫 | **PASS** |
| 06 | `crops/crop_06_no_record_dps_ja.png` | `320dbf582e118a440b5537fc44904e49f2e670eaf6e6fdab9c5b79039c2be9b8` | 日文 DpsCard "歴代最高：250.0 DPS" 標籤特寫 | **PASS** |
| 07 | `crops/crop_07_no_record_dps_ko.png` | `62745702ea147cac698d2d9efa4aa31cf423fde0a92a6d979897efdff41b4377` | 韓文 DpsCard "최고 기록: 250.0 DPS" 標籤特寫 | **PASS** |
| 08 | `crops/crop_08_no_record_dps_es.png` | `1309057b4bb73d4e466cd574f54f704c80330dade4542140c39a77a869626e4d` | 西文 DpsCard "Mejor récord: 250.0 DPS" 標籤特寫 | **PASS** |
| 09 | `crops/crop_09_no_record_dps_zh_CN.png` | `d1585f2ed29cdb19c6ba07b0abb4aa7024fd59346519fa2fe8309fc0d87f84c9` | 簡中 DpsCard "历史最佳：250.0 DPS" 標籤特寫 | **PASS** |
