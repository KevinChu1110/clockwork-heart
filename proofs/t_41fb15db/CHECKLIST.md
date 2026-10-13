# 全面回歸驗收證明 · BattleSim 與 DummySettlementDialog 新增木人樁最高單擊與總命中統計 (t_41fb15db)

## 1. 任務背景與驗收目標
針對任務 `t_41fb15db`（BattleSim 與 DummySettlementDialog 新增木人樁最高單擊與總命中統計）：
1. **數值統計累計**：在 `game/scripts/battle/battle_sim.gd` 中記錄木人樁戰鬥期間玩家造成的單擊最高傷害 (`max_hit_damage`) 與總命中次數 (`total_hit_count`)，並擴充 `get_dummy_combat_stats()` 回傳字典。
2. **多巴胺雙膠囊數據列**：在 `game/scripts/battle/dummy_settlement_dialog.gd` 結算卡片新增雙膠囊數據列：
   - `MaxHitCapsule`：最高單擊膠囊（天藍柔和卡片底，字級 >= 14px，加粗深藍紫文字）。
   - `TotalHitsCapsule`：總命中次數膠囊（薄荷綠柔和卡片底，字級 >= 14px，加粗深藍紫文字）。
   - 包含 `CapsulesHBox`、`MaxHitValueLabel`、`TotalHitsValueLabel` 等節點與對應 getters。
   - 100% 零系統原生 Emoji。
3. **六語系即時切換**：補齊 zh_TW/zh_CN/en/ja/ko/es 六語系字典 key（`最高單擊`、`總命中次數`、`次`），支援 `Loc.locale_changed` 動態刷新。
4. **單元與回歸測試**：
   - 更新 `test_dummy_settlement_dialog.gd` 覆蓋雙膠囊節點結構、數值對齊與 getters。
   - 更新 `test_dummy_settlement_i18n.gd` 覆蓋 19 條全語系即時刷新與零 Emoji。
   - 新增 `test_dummy_combat_stats.gd` 專門驗證 BattleSim 數值累計精準度與 DummySettlementDialog 雙膠囊規範。
5. **手遊人因與視覺規範**：OpenGL3 實機渲染截圖存證齊全，SHA256 唯一無重複。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **數據卡結構測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_dialog.gd` | 1/1 通過（`DUMMY_SETTLEMENT_DIALOG_OK`），雙膠囊結構與數值斷言全數合格 | **PASS** |
| **數據卡六語系測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_i18n.gd` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`），19 條六語系即時切換全數通過 | **PASS** |
| **歷史最佳DPS測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_record.gd` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_RECORD_OK`） | **PASS** |
| **最高單擊與總命中專屬測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_combat_stats.gd` | 1/1 通過（`TEST_DUMMY_COMBAT_STATS_OK`），BattleSim 數值累計與雙膠囊規範全數合格 | **PASS** |
| **木人樁基礎測試** | `godot --path game --headless -s res://scripts/battle/test_training_dummy.gd` | 1/1 通過（`TRAINING_DUMMY_OK`） | **PASS** |
| **資產匯入與語系檢查** | `/root/bin/clock-check t_41fb15db` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結，無退休舊詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_41fb15db/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 4 張實機全景截圖與 4 張特寫裁切圖之 SHA256 雜湊值均獨立相異，無重複或黑屏。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 最高單擊膠囊（天藍柔和卡片底 #F0F7FF，#1F1A3A 深藍紫描邊，底部厚底 3px，圓角 16px）。
  - 總命中次數膠囊（薄荷綠柔和卡片底 #F0FAF2，#1F1A3A 深藍紫描邊，底部厚底 3px，圓角 16px）。
  - 標籤字級 14px，數值字級 20px（加粗深藍紫文字），字級 >= 14px 全數合規。
- [x] **六語系即時切換**：
  - 繁中（最高單擊 XX 點 / 總命中次數 XX 次）
  - 簡中（最高单击 XX 点 / 总命中次数 XX 次）
  - 英文（Max Hit XX pts / Total Hits XX hits）
  - 日文（最大単撃 XX pt / 総命中回数 XX 回）
  - 韓文（최고 단타 XX 점 / 총 적중 횟수 XX 회）
  - 西文（Golpe máx. XX pts / Total de impactos XX veces）
- [x] **100% 零系統原生 Emoji**：所有介面完全使用純文字與向量元件，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | 涵蓋內容與驗收重點 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_01_dummy_settlement_zh_TW.png` | `1495954a1314ec0aff053e59baa6b803d26a8fd3c63c6ed7a94b7793e2d32d94` | 繁中雙膠囊全景：最高單擊 96 點（天藍膠囊）與總命中次數 16 次（薄荷綠膠囊） | **PASS** |
| 02 | `proof_02_dummy_settlement_en.png` | `d94389d05ba802335bd54e5ffa8f88b99f6f4b8bc92b05e4e37a5f74480fcb75` | 英文雙膠囊全景：Max Hit 96 pts 與 Total Hits 16 hits | **PASS** |
| 03 | `proof_03_dummy_settlement_ja.png` | `bc17a7463434530aee26977b37b11ccad15fcbc31a66077cc8e70fc9e54c0d07` | 日文雙膠囊全景：最大単撃 96 pt 與 総命中回数 16 回 | **PASS** |
| 04 | `proof_04_dummy_settlement_live_combat.png` | `d4277c285e79737d1502f45a7a4791713f32e1b12c2b0f53edcd657ebd9735f2` | 真實木人樁戰鬥步進後彈出之結算數據卡（真實累計最高單擊與命中次數） | **PASS** |

---

## 5. 特寫裁切圖清單 (Crops, 740x80)

| 編號 | 特寫圖檔名 | SHA256 | 特寫區域 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `crops/crop_01_capsules_zh_TW.png` | `71b9b36a6a5cc0f11f15d02e2a4703ba336a748768df86bb94d93f28fcb45360` | 繁中雙膠囊列特寫（最高單擊 96 點 / 總命中次數 16 次） | **PASS** |
| 02 | `crops/crop_02_capsules_en.png` | `33e88da07f2b84b9ffc983f4657f1d430cc86e85c077978d59d1fbbefc5b7eac` | 英文雙膠囊列特寫（Max Hit 96 pts / Total Hits 16 hits） | **PASS** |
| 03 | `crops/crop_03_capsules_ja.png` | `6b4c75809e1413c18a8c6966f66e0bd9a0dae90aaaa0db0dfa4f3f6e7b8fa978` | 日文雙膠囊列特寫（最大単撃 96 pt / 総命中回数 16 回） | **PASS** |
| 04 | `crops/crop_04_capsules_live.png` | `d3fe40e744ef7a090d94146f36c0cdadcc9dc583d1e1ca107f1872075a368180` | 真實戰鬥數據雙膠囊列特寫 | **PASS** |
