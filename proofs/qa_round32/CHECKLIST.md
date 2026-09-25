# 《發條之心》探索性 QA 第三十二輪 查驗清單與缺陷報告 (Round 32 Checklist)

- **測試日期**：2026-09-26
- **測試員**：小婷（側案·測試 sideqa）
- **關聯卡號**：`t_2657d397`
- **關聯前置任務**：`t_0cd6ba66`（創角雙分頁）、`t_2b2a49b4`（翠角鹿骨架）、`t_f43c1625`（熊貓戰鬥六姿態）
- **存檔目錄**：`/opt/side/bravesoul-game/proofs/qa_round32/`

---

## 一、 實機截圖四項核驗清單（每張圖：破圖／emoji／截字／糊圖）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零系統Emoji | 零截字 | 零128糊圖 | 審核結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | `proof_01_creation_launch.png` | 創角首發頁（五卡一屏） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 2 | `proof_02_creation_expansion.png` | 創角擴充頁（含瓷韻熊貓） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 3 | `proof_03_creation_panda_selected.png` | 點熊貓後中央 512 舞台預覽 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 4 | `proof_04_creation_fawn_check.png` | 創角擴充頁向右滾動翠角鹿卡片 | ✗ **空卡** | ✓ 零Emoji | ✓ 零截字 | ✓ 無糊圖 | **發現缺陷 (FAIL)** |
| 5 | `proof_05_creation_fawn_selected.png` | 創角選取翠角鹿中央預覽檢查 | ✗ **舞台空白** | ✓ 零Emoji | ✓ 零截字 | ✓ 無糊圖 | **發現缺陷 (FAIL)** |
| 6 | `proof_06_battle_panda_idle.png` | 熊貓戰鬥待機 (idle 512) | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 7 | `proof_07_battle_panda_attack.png` | 熊貓戰鬥攻擊 (attack 512) | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 8 | `proof_08_battle_panda_hit.png` | 熊貓戰鬥受擊 (hit 512) | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 9 | `proof_09_wardrobe_panda.png` | 衣櫥抽查熊貓（長袍＋白瓷塗裝） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 10 | `proof_10_wardrobe_fawn_filter.png` | 衣櫥抽查翠角鹿（篩選「鹿」） | ✗ **空卡/空白** | ✓ 零Emoji | ✓ 零截字 | ✓ 無糊圖 | **發現缺陷 (FAIL)** |
| 11 | `proof_11_wardrobe_all_fawn.png` | 衣櫥篩選「全部」滾動至翠角鹿卡 | ✗ **空卡露出** | ✓ 零Emoji | ✓ 零截字 | ✓ 無糊圖 | **發現缺陷 (FAIL)** |

---

## 二、 瓷韻熊貓（第十三族）專項查核

1. **六大戰鬥姿態檔案與品質查驗**：
   - `poses/panda/idle_512.png`：512x512 PNG，存在且無 128 退路。
   - `poses/panda/telegraph_512.png`：512x512 PNG，存在且無 128 退路。
   - `poses/panda/attack_512.png`：512x512 PNG，存在且無 128 退路。
   - `poses/panda/recover_512.png`：512x512 PNG，存在且無 128 退路。
   - `poses/panda/skill_512.png`：512x512 PNG，存在且無 128 退路。
   - `poses/panda/hit_512.png`：512x512 PNG，存在且無 128 退路。
   - 無效姿態安全回傳 `null`，嚴格恪守 0-QA22 防護。
2. **實機戰鬥運行驗證**：
   - 待機、攻擊（太極衝拳）、受擊（機關護甲防禦態）三大姿態實機渲染正常，無任何破圖、零系統 Emoji、戰鬥日誌與數值無截字。
3. **創角與衣櫥整合**：
   - 創角擴充頁正常顯示瓷韻熊貓卡片與縮圖，點擊即時套用 512 舞台與預設長袍＋白瓷塗裝。
   - 衣櫥篩選晶片列包含「貓」，選用【禪道學徒生漆長袍】與【羊脂白瓷生漆塗裝】即時套用無誤。

---

## 三、 翠角鹿（第十四族）缺陷報告（什麼輸入 → 什麼壞掉）

依任務要求：「翠角鹿還沒圖：創角／衣櫥若露出空卡、占位色塊或 128 糊圖，記成缺陷並開修，不要當合格。沒露出也要寫清楚『玩家看不到』。」

### 【缺陷 1】創角擴充頁露出翠角鹿空卡與空白人偶
- **觸發輸入**：
  1. 進入創角介面（`paperdoll_select_demo.tscn`）。
  2. 點擊「擴充」分頁（`switch_tab("expansion")`）。
  3. 將上方種族滾動列向右滑動至最末端。
  4. 點選「翠角鹿」按鈕。
- **壞掉現象**：
  1. 上方種族列最右側露出「翠角鹿」按鈕，但卡片縮圖完全留白缺失（空卡，Missing Asset），見 `proof_04_creation_fawn_check.png`。
  2. 點選「翠角鹿」後，左側中央 512 舞台僅繪製腳底灰色陰影，角色立繪與 7 大槽位完全空白隱形（狀態欄顯示 `載入: 0/7`），見 `proof_05_creation_fawn_selected.png`。
- **根本原因**：
  `paperdoll_select_demo.gd` 之 `EXPANSION_RACES` 陣列過早納入 `"fawn"`，且 `RACES_DATA["fawn"]["thumb"]` 指向不存在的圖檔 `fawn_idle_hd.png`。

### 【缺陷 2】衣櫥介面露出「鹿」篩選晶片與空卡
- **觸發輸入**：
  1. 開啟衣櫥介面（`wardrobe_dialog.gd`）。
  2. 點擊上方種族篩選列最右側的「鹿」晶片。
- **壞掉現象**：
  1. 右側外裝服飾與機體塗裝卡片區露出「翡翠林緣巡守工裝」、「無外裝 (裸機素體)」、「雙色沖壓原木紋金屬板」，上方圖標縮圖全為空白占位色塊（空卡），見 `proof_10_wardrobe_fawn_filter.png`。
  2. 左側角色預覽區完全空白無角色立繪，且下方標籤出現文字不一致（第一行殘留存檔名稱「瓷韻熊貓」，第二行顯示「【翠角鹿・遊俠 (Ranger)】」）。
  3. 若篩選「全部」並滾動至最底部，外裝與塗裝卡片最末尾亦直接露出無圖標的翠角鹿空卡，見 `proof_11_wardrobe_all_fawn.png`。
- **根本原因**：
  `wardrobe_dialog.gd` 之 `RACE_FILTER_OPTIONS` 過早加入 `{"id": "fawn", "name_zh": "鹿"}`，且 `_rebuild_cards()` 的 `target_races` 納入了尚無美術資源的 `"fawn"`。

### 【修復建議】
在翠角鹿 7 槽切片與 512 立繪資產產出並驗收前，創角 `EXPANSION_RACES` 與衣櫥 `RACE_FILTER_OPTIONS` 不應將 `"fawn"` 曝露給玩家，應暫時從玩家前端顯示名單移除或加上 `has_race_assets` 守衛，直到美術資源齊全再正式接上。

---

## 四、 驗收指令執行紀錄

- `godot --path game --headless --quit-after 3`：**0 SCRIPT ERROR**（通過）。
- `TEST_FILTER=paperdoll ./tools/run_tests.sh`：**20/20 PASSED**（通過）。
- `TEST_FILTER=creation ./tools/run_tests.sh`：**4/4 PASSED**（通過）。
- `godot --path game --headless -s res://scripts/battle/test_battle_events.gd`：**TEST_BATTLE_EVENTS_OK**（通過）。
- `godot --path game --headless -s res://scripts/art/test_panda_action_poses.gd`：**PANDA_ACTION_POSES_TEST_OK**（通過）。
- `godot --path game --headless -s res://scripts/art/test_paperdoll_fawn_skeleton.gd`：**PAPERDOLL_FAWN_SKELETON_OK**（通過）。
- **Vision 檢驗**：全部 11 張實機截圖均已由 Vision 模型完成逐張驗證與異常標定。
