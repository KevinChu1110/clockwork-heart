# 全面回歸驗收證明 · DummySettlementDialog 支援三欄武器輪替次數與傷害貢獻統計 (t_8f9d6203)

## 1. 任務背景與驗收目標
針對任務 `t_8f9d6203`（DummySettlementDialog 支援三欄武器輪替次數與傷害貢獻統計）：
1. **數值統計累計**：在 `game/scripts/battle/battle_sim.gd` 中記錄木人樁戰鬥期間各武器欄位 (slot 0/1/2) 的傷害累積 (`weapon_slot_damages`) 與輪替切換次數 (`weapon_swap_count`, `weapon_slot_swaps`)，並擴充 `get_dummy_combat_stats()` 回傳字典。
2. **多巴胺三欄武器貢獻卡與輪替次數展示列**：在 `game/scripts/battle/dummy_settlement_dialog.gd` 結算卡片新增展示列：
   - `WeaponContributionSection`：三欄武器傷害佔比與貢獻專屬區塊。
   - `WeaponSwapsCapsule`：輪替切換次數膠囊（柔和琥珀底 #FFEED6，圓角 12px，零 Emoji）。
   - `WeaponSlotsHBox` 與 `WeaponSlotCard_0`, `WeaponSlotCard_1`, `WeaponSlotCard_2`：
     - 清晰展示各武器名稱、品質色階標籤（凡品 #8E8A9F、良品 #2E9E4A、上品 #2575FC、極品 #9B51E0、神品 #FFA010）。
     - 傷害百分比（如 50.0%、30.0%、20.0%）與具體傷害數值（點）。
     - 多巴胺色階傷害進度彩條（天藍 #38A0FF、薄荷綠 #4ED86A、暖橘 #FFA010）。
     - 100% 零系統原生 Emoji。
3. **六語系即時切換**：補齊 zh_TW/zh_CN/en/ja/ko/es 六語系字典 key（`武器傷害貢獻`、`輪替切換`、`欄位 %d` 等），支援 `Loc.locale_changed` 動態即時刷新。
4. **單元與回歸測試**：
   - 新增專屬測試 `test_dummy_weapon_contribution.gd` 完整驗證三欄武器切換傷害累加正確性、總傷害等式驗證、UI 節點結構與六語系動態切換。
   - 更新 `test_dummy_settlement_dialog.gd`、`test_dummy_settlement_i18n.gd`、`test_dummy_combat_stats.gd` 覆蓋新增節點與詞條。
5. **手遊人因與視覺規範**：OpenGL3 實機渲染截圖存證齊全，SHA256 唯一無重複。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **三欄武器貢獻專屬測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_weapon_contribution.gd` | 1/1 通過（`TEST_DUMMY_WEAPON_CONTRIBUTION_OK`），切換次數、傷害累計、UI結構與六語系全數合格 | **PASS** |
| **數據卡結構測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_dialog.gd` | 1/1 通過（`DUMMY_SETTLEMENT_DIALOG_OK`），新增三欄武器節點與斷言全數通過 | **PASS** |
| **數據卡六語系測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_i18n.gd` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_I18N_OK`），22 條全語系即時切換全數通過 | **PASS** |
| **最高單擊與總命中測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_combat_stats.gd` | 1/1 通過（`TEST_DUMMY_COMBAT_STATS_OK`） | **PASS** |
| **歷史最佳DPS測試** | `godot --path game --headless -s res://scripts/battle/test_dummy_settlement_record.gd` | 1/1 通過（`TEST_DUMMY_SETTLEMENT_RECORD_OK`） | **PASS** |
| **木人樁基礎測試** | `godot --path game --headless -s res://scripts/battle/test_training_dummy.gd` | 1/1 通過（`TRAINING_DUMMY_OK`） | **PASS** |
| **資產匯入與語系檢查** | `/root/bin/clock-check t_8f9d6203` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結，無退休舊詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_8f9d6203/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 4 張實機全景截圖與 4 張特寫裁切圖之 SHA256 雜湊值均獨立相異，無重複或黑屏。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 輪替切換膠囊（琥珀柔和底 #FFEED6，#1F1A3A 深藍紫描邊，底厚 3px，圓角 12px）。
  - 三欄武器貢獻卡（天藍 #F4F8FD、薄荷綠 #F4FAF5、暖橘 #FFF9EE 柔和底，圓角 14px，字級 >= 11~15px）。
  - 進度彩條色彩鮮明（天藍 #38A0FF、薄荷綠 #4ED86A、暖橘 #FFA010）。
- [x] **六語系即時切換**：
  - 繁中（武器傷害貢獻 / 輪替切換 3 次 / 欄位 1 / 欄位 2 / 欄位 3）
  - 簡中（武器伤害贡献 / 轮替切换 3 次 / 栏位 1 / 栏位 2 / 栏位 3）
  - 英文（Weapon Damage / Weapon Swaps 3 hits / Slot 1 / Slot 2 / Slot 3）
  - 日文（武器ダメージ貢献 / 武器切り替え 3 回 / スロット 1 / スロット 2 / スロット 3）
  - 韓文（무기 피해 기여 / 무기 교체 3 회 / 슬롯 1 / 슬롯 2 / 슬롯 3）
  - 西文（Daño por arma / Cambios de arma 3 veces / Ranura 1 / Ranura 2 / Ranura 3）
- [x] **100% 零系統原生 Emoji**：所有介面完全使用純文字、向量色塊與彩條，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | 涵蓋內容與驗收重點 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_01_dummy_weapon_contrib_zh_TW.png` | `cf36c92025217ab5c39a434e26952da82786398fd84204a4e976b24aa14a5f3d` | 繁中三欄武器貢獻全景：白鐵長劍(50.0%)、淬毒短刃(30.0%)、破軍巨錘(20.0%)與輪替切換 3 次 | **PASS** |
| 02 | `proof_02_dummy_weapon_contrib_en.png` | `baed126ff106648c148ffc6c75d4fa9389bcf433246766af2af9fa6599ad80a3` | 英文全景：Weapon Damage、Weapon Swaps、Slot 1/2/3 即時切換 | **PASS** |
| 03 | `proof_03_dummy_weapon_contrib_ja.png` | `0b7f6fa9792b0f90bdc0352333986d35c8bac4a0273b63e0270fc0f71191620e` | 日文全景：武器ダメージ貢献、武器切り替え、スロット 1/2/3 即時切換 | **PASS** |
| 04 | `proof_04_dummy_weapon_contrib_live.png` | `7506786c67f717f1819fa43e5b273a9a60992f63110087dc0839593e177ab716` | 真實木人樁戰鬥輪替步進後結算全景（真實累計三欄武器傷害與 2 次輪替） | **PASS** |

---

## 5. 特寫裁切圖清單 (Crops, 740x135)

| 編號 | 特寫圖檔名 | SHA256 | 特寫區域 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `crops/crop_01_weapon_contrib_zh_TW.png` | `5b20bbe127fb5c619ba81a54dd28255e88cf71b6c30a491e91397bf9d772f213` | 繁中三欄武器貢獻卡與輪替切換膠囊特寫 | **PASS** |
| 02 | `crops/crop_02_weapon_contrib_en.png` | `e4a313518f9c539ddf1e98a955447bba0a690429f4f4007dfe45f1d68cfc40fd` | 英文三欄武器貢獻卡與輪替切換膠囊特寫 | **PASS** |
| 03 | `crops/crop_03_weapon_contrib_ja.png` | `ab64789f68aa06c4b6f98d0f99fcfb81ea4fffd86a872a0338052e976a268142` | 日文三欄武器貢獻卡與輪替切換膠囊特寫 | **PASS** |
| 04 | `crops/crop_04_weapon_contrib_live.png` | `66cd1cc2b11e290c6b01f743a9e9bfc2fdaf932af2b6666f17b3386e8a1c6463` | 真實戰鬥數據三欄武器貢獻卡特寫 | **PASS** |
