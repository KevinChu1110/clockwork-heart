# 全面回歸驗收證明 · BattleVictoryDialog 支援三欄武器戰鬥數據統計膠囊 (t_6586cf54)

## 1. 任務背景與驗收目標
針對任務 `t_6586cf54`（BattleVictoryDialog 支援三欄武器戰鬥數據統計膠囊（輪替次數與傷害貢獻））：
1. **數值統計累計**：在主線/BOSS戰鬥勝利時，將戰鬥中三欄武器總切換輪替次數 (`weapon_swap_count`, `weapon_slot_swaps`) 與各欄位傷害 (`weapon_slot_damages`) 透過 `get_combat_stats()` / `BattleSim.last_victory_combat_stats` 傳入 `BattleVictoryDialog`。
2. **多巴胺三欄武器戰鬥數據統計膠囊列**：在 `BattleVictoryDialog` 資訊區新增 `WeaponLoadoutStatsCapsules`：
   - `WeaponStatsHeaderHBox`：頂部標題與輪替次數膠囊。
   - `WeaponStatsTitleLabel`：「傷害貢獻」標題（字級 14px，深藍紫字體加粗，零 Emoji）。
   - `WeaponSwapsCapsule`：輪替切換次數膠囊（柔和琥珀底 #FFF3E0，#1F1A3A 深藍紫描邊，底厚 3px，圓角 12px，零 Emoji）。
   - `WeaponSlotsHBox` 與 `WeaponSlotCard_0`, `WeaponSlotCard_1`, `WeaponSlotCard_2`：
     - 清晰展示各欄位標題（首選武器、副手武器、絕技武器）、武器名稱（鐵劍、獵弓、拳套）。
     - 傷害百分比（如 50.0%、30.0%、20.0%）與具體傷害數值（點）。
     - 多巴胺色階傷害進度彩條（天藍 #38A0FF、薄荷綠 #4ED86A、暖橘 #FFA010）。
     - 100% 零系統原生 Emoji。
     - 字級規範：全彈窗所有 Label 與 Button 字級均 >= 14px，100% 零 13px 以下小字。
3. **六語系即時切換**：補齊 zh_TW/zh_CN/en/ja/ko/es 六語系字典 key（`傷害貢獻`、`輪替切換`、`首選武器`、`副手武器`、`絕技武器` 等），支援 `Loc.locale_changed` 動態即時刷新。
4. **單元與回歸測試**：
   - 新增專屬測試 `test_victory_weapon_loadout_stats.gd` 完整驗證三欄武器統計節點存在性、傷害佔比與輪替次數計算正確性、全彈窗字級 >= 14px 規範、100% 零 Emoji、以及六語系動態即時切換。
   - 回歸測試 `test_victory_part_break_badges.gd` 驗證既有功能零回歸破壞。
5. **手遊人因與視覺規範**：OpenGL3 實機渲染截圖存證齊全，SHA256 唯一無重複。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **三欄武器統計專屬測試** | `godot --path game --headless -s res://scripts/battle/test_victory_weapon_loadout_stats.gd` | 1/1 通過（`TEST_VICTORY_WEAPON_LOADOUT_STATS_OK`），節點結構、數值佔比、字級>=14px、零Emoji與六語系即時切換全數綠燈 | **PASS** |
| **部位破壞徽章回歸測試** | `godot --path game --headless -s res://scripts/battle/test_victory_part_break_badges.gd` | 1/1 通過（`TEST_VICTORY_PART_BREAK_BADGES_OK`），既有部位破壞徽章與多巴胺獎勵入袋演出完全正常 | **PASS** |
| **資產匯入與語系檢查** | `/root/bin/clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6586cf54` | 素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_6586cf54/` 獨立目錄。
- [x] **0-QA15（雜湊唯一性）**：所有 3 張實機全景截圖與 3 張特寫裁切圖之 SHA256 雜湊值均獨立相異，無重複或黑屏。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 輪替切換膠囊（琥珀柔和底 #FFF3E0，#1F1A3A 深藍紫描邊，底厚 3px，圓角 12px）。
  - 三欄武器貢獻卡（天藍 #F4F8FD、薄荷綠 #F4FAF5、暖橘 #FFF9EE 柔和底，圓角 14px，字級 >= 14px）。
  - 進度彩條色彩鮮明（天藍 #38A0FF、薄荷綠 #4ED86A、暖橘 #FFA010）。
  - 字級規範：所有 Label 與 Button 字級均 >= 14px，零 13px 以下小字。
- [x] **六語系即時切換**：
  - 繁中（傷害貢獻 / 輪替切換 8 次 / 首選武器 / 副手武器 / 絕技武器）
  - 簡中（伤害贡献 / 轮替切换 8 次 / 首选武器 / 副手武器 / 绝技武器）
  - 英文（Damage Contribution / Weapon Swaps 8 hits / Primary Weapon / Secondary Weapon / Special Weapon）
  - 日文（ダメージ貢献 / 武器切り替え 8 回 / メイン武器 / サブ武器 / 絶技武器）
  - 韓文（피해 기여 / 무기 교체 8 회 / 주 무기 / 보조 무기 / 필살 무기）
  - 西文（Contribución de daño / Cambios de arma 8 veces / Arma Principal / Arma Secundaria / Arma Especial）
- [x] **100% 零系統原生 Emoji**：所有介面完全使用純文字、向量色塊與彩條，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 | 涵蓋內容與驗收重點 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `proof_01_victory_weapon_stats_zh_TW.png` | `7d8ad73a5b03d995d70e36e380bea4fc968c340eb2cc9931f81dea194881a624` | 繁中勝利結算全景：傷害貢獻、輪替切換 9 次、首選武器鐵劍(53.6%)、副手武器獵弓(28.4%)、絕技武器拳套(18.0%) | **PASS** |
| 02 | `proof_02_victory_weapon_stats_en.png` | `3a6d69e0e0be94a841a03f469e9d4565fd5f0258f474daebdd799e875a2e8d17` | 英文全景：Damage Contribution, Weapon Swaps 9 hits, Primary/Secondary/Special Weapon 即時切換 | **PASS** |
| 03 | `proof_03_victory_weapon_stats_ja.png` | `189e0f2ea1ed389e38a729cf792221720efcb22488abed1d0a3a286b5fc8b714` | 日文全景：ダメージ貢献、武器切り替え 9 回、メイン/サブ/絶技武器 即時切換 | **PASS** |

---

## 5. 特寫裁切圖清單 (Crops, 730x170)

| 編號 | 特寫圖檔名 | SHA256 | 特寫區域 | 判定 |
|:---:|:---|:---|:---|:---:|
| 01 | `crop_01_stats_zh_TW.png` | `3373ca2bd1bfb4ba861599bd12021d1657694fda7b6671561131a689e2918dc4` | 繁中三欄武器統計膠囊與彩條特寫 | **PASS** |
| 02 | `crop_02_stats_en.png` | `3909300bb286bcc5b234b4f632dcfa1951843d3f96403e96d0fec3448fbb7e73` | 英文三欄武器統計膠囊與彩條特寫 | **PASS** |
| 03 | `crop_03_stats_ja.png` | `c093260cd6125941d6d896800a69f6d470bebb2564b46483b4da290488e3481c` | 日文三欄武器統計膠囊與彩條特寫 | **PASS** |
