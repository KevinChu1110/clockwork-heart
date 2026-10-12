# 全面回歸驗收證明 · 木人樁傷害統計與大廳武器更換彈窗合進主線後的全站回歸驗收 (t_97f7f067)

## 1. 任務背景與驗收目標
針對前置任務 `t_003bad6a` 成功將木人樁三欄武器貢獻與傷害統計（`t_8f9d6203`，merge commit `59270115`）和大廳角色頁更換武器裝備彈窗連動武器庫（`t_a53d6368`，merge commit `4a37393d`）乾淨合併至 `main` 分支並推上 `origin/main`（最新 commit `a5a58cd7`），且 `PROJECTS.json` 中之 `dummy-combat-stats`、`dummy-weapon-contribution` 與 `lobby-weapon-swap-dialog` 均已標記為『已上線』後，由測試員小婷（`sideqa`）在 `main` 主線執行全站回歸驗收與實機存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元與回歸測試全綠**：
   - 全套 dummy 測試集 (8/8 PASS，含三欄貢獻、最高單擊/總命中、歷史最佳紀錄、UI結構、六語系等)
   - 全套 lobby 測試集 (12/12 PASS，含武器更換彈窗、武器庫連動、大廳紅點、心法按鈕等)
   - 全套 equipment 測試集 (2/2 PASS，含裝備拆解、裝備名稱六語系等)
   - 全套 combat 測試集 (13/13 PASS，含 1v1/1v3、超載爆裂、怒氣出招、命中計算等)
   - 全套 battle 測試集 (16/16 PASS，含戰鬥日誌、打擊反饋、事件系統、在地化等)
   - 核心在地化測試 `test_i18n.gd` (PASS，六語系 1024 鍵對齊、ui.json 3670 鍵全部對齊)
3. **自動化檢查與規範**：
   - `/root/bin/clock-check --live`：公開官網 14 頁全開、零退休舊詞（霧隱村/今日村莊/白霧村 零殘留）。
   - `/root/bin/clock-check /opt/side/bravesoul-game`：0 缺 .import、0 斷鏈、0 軟連結。在 main 執行回歸驗收係屬刻意為之。
4. **實機截圖存證**：依據 `review.md`（0-QA5, 0-QA15, 0-QA23, 0-QA24, 0-QA25, 0-QA26）規範，透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720 實機全景圖 12 張與特寫裁切圖 7 張，經 Vision 審查確認零穿模、零黑屏、零系統 Emoji、多巴胺立體厚底按鈕合規、三欄貢獻卡比例清晰、大廳更換武器彈窗 750px 置中且屬性即時更新。
5. **項目進度維護**：`PROJECTS.json` 中相關項目維持『已上線』無回退。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 | **PASS** |
| **全套木人樁系統測試** | `TEST_FILTER=dummy ./tools/run_tests.sh` | 8/8 全部通過（武器貢獻、最高單擊、總命中、最佳紀錄、多語系等） | **PASS** |
| **全套大廳系統測試** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 12/12 全部通過（武器更換彈窗、裝備同步、背包、紅點等） | **PASS** |
| **全套裝備系統測試** | `TEST_FILTER=equipment ./tools/run_tests.sh` | 2/2 全部通過（裝備拆解、裝備名稱六語系） | **PASS** |
| **全套核心戰鬥測試** | `TEST_FILTER=test_combat ./tools/run_tests.sh` | 13/13 全部通過（1v1/1v3、超載爆裂、怒氣出招、五族招式等） | **PASS** |
| **全套戰鬥介面測試** | `TEST_FILTER=test_battle_ ./tools/run_tests.sh` | 16/16 全部通過（戰鬥事件、多巴胺日誌、觸控防誤觸等） | **PASS** |
| **語系完整性測試** | `godot --path game --headless -s res://scripts/autoload/test_i18n.gd` | 6 語系各 1024 key、ui.json 各 3670 key 全部對齊 | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA5 / 0-QA26（真實 OpenGL3 渲染存證）**：100% 透過 `xvfb-run -a godot --rendering-driver opengl3` 擷取真實 Framebuffer 1280x720，拒絕虛假圖片。
- [x] **0-QA23（獨立 Proof 目錄）**：所有實機全景圖與特寫圖存證於 `proofs/t_97f7f067/` 與 workspace 獨立目錄，不污染其他任務。
- [x] **0-QA15（雜湊唯一性）**：所有 12 張實機全景截圖與 7 張特寫裁切圖之 SHA256 雜湊值均獨立相異，無重複或黑屏偽造。
- [x] **手遊防誤觸與多巴胺視覺規範**：
  - 木人樁多巴胺雙膠囊：最高單擊（#F0F7FF 天藍柔和底）與總命中次數（#F0FAF2 薄荷綠柔和底），加粗深藍紫文字（#1F1A3A），字級 >= 14px。
  - 三欄武器貢獻卡：天藍 #F4F8FD、薄荷綠 #F4FAF5、暖橘 #FFF9EE 柔和底，進度彩條色彩鮮明（天藍 #38A0FF、薄荷綠 #4ED86A、暖橘 #FFA010）。
  - 輪替切換次數膠囊：柔和琥珀底 #FFEED6，圓角 12px，底厚 3px。
  - 大廳武器更換彈窗：750px 橫屏置中，外覆輕透暗色 ModalScrim，圓角 16~22px，邊框 3px。
  - 操作按鈕熱區 >= 48px，立體果凍厚底 5px，點擊回饋明確。
- [x] **0-QA24 / 0-QA25（六語系即時切換）**：
  - 繁中（木人試招數據卡 / 最高單擊 / 總命中次數 / 武器傷害貢獻 / 輪替切換 / 武器庫 · 更換裝備）
  - 英文（Trial Stats / Max Hit / Total Hits / Weapon Damage / Weapon Swaps / Armory · Change Equipment）
  - 日文（試技データ / 最大ダメージ / 総命中数 / 武器ダメージ貢献 / 武器切り替え / 武器庫 · 装備変更）
  - 韓文（연습 결과 / 최대 단타 / 총 적중 수 / 무기 피해 기여 / 무기 교체 / 무기고 · 장비 교체）
  - 西文（Datos de prueba / Golpe máx. / Impactos tot. / Daño por arma / Cambios de arma / Armería · Cambiar equipo）
  - 簡中（木人试招数据卡 / 最高单击 / 总命中数 / 武器伤害贡献 / 轮替切换 / 武器库 · 更换装备）
  - 即時切換無需重啟，無缺漏、無截字、無重疊。
- [x] **100% 零系統原生 Emoji**：所有介面完全使用純文字、自製向量色塊與彩條，零系統原生 Emoji。

---

## 4. 全景實機截圖清單 (1280x720)

| 編號 | 實機截圖檔名 | SHA256 (完整) | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 驗證結論 |
|:---:|:---|:---|:---|:---:|:---:|:---:|
| 01 | `proof_01_dummy_settlement_zh_TW.png` | `da2a7448f434122c5670de3a8998ed254c378180bd2f360bb67b83f859011772` | 繁中木人樁結算全景：最高單擊(142點)、總命中(24次)、三欄武器貢獻卡與輪替切換3次 | ✓ 無 | ✓ 零 | **PASS** |
| 02 | `proof_02_dummy_settlement_en.png` | `3e2a987908cf3196d2e539be3ffc00245671b3471d68aa2420c10ac878249b9d` | 英文結算全景：Max Hit (142 pts)、Total Hits (24)、Weapon Damage、Weapon Swaps (3 hits) | ✓ 無 | ✓ 零 | **PASS** |
| 03 | `proof_03_dummy_settlement_ja.png` | `20a206978d79aafb6aaa4d0a4658712923b61059a3331c0948524e91ca7860e9` | 日文結算全景：最大ダメージ (142 pt)、総命中数 (24 回)、武器ダメージ貢献、武器切り替え (3 回) | ✓ 無 | ✓ 零 | **PASS** |
| 04 | `proof_04_dummy_settlement_ko.png` | `a51f6c03e732099a58ef8d22e574aba43a2fbe554e8c93173a584c99947e1e75` | 韓文結算全景：최대 단타 (142 점)、총 적중 수 (24 회)、무기 피해 기여、무기 교체 (3 회) | ✓ 無 | ✓ 零 | **PASS** |
| 05 | `proof_05_dummy_settlement_es.png` | `6190b0a89abe6ee3cc0e69099210618a5dcf2b8774348ed971564f1451a9a22f` | 西文結算全景：Golpe máx. (142 pts)、Impactos tot. (24 veces)、Daño por arma、Cambios de arma | ✓ 無 | ✓ 零 | **PASS** |
| 06 | `proof_06_dummy_settlement_zh_CN.png` | `6e89088fdf140ced69f69032fda46cd5d446debd72d53f59d66e8bd7cf6e1e4b` | 簡中結算全景：最高单击 (142点)、总命中数 (24次)、武器伤害贡献、轮替切换 (3次) | ✓ 無 | ✓ 零 | **PASS** |
| 07 | `proof_07_dummy_settlement_live_combat.png` | `c7abf4d3567e0fb57991048437fd20d23bc16b60aa316092fa2c4b6e939dbf01` | 真實木人樁戰鬥輪替步進後結算全景（真實累計三欄武器傷害與 2 次輪替） | ✓ 無 | ✓ 零 | **PASS** |
| 08 | `proof_08_lobby_character_before_swap.png` | `31e22c9b196e5028b5cc7b8e1b23d2764c62aaa5c7a12225ee47b06ce53c6140` | 大廳角色頁裝備分頁（未開彈窗，展示首選/副手/絕技槽位與「更換裝備」按鈕） | ✓ 無 | ✓ 零 | **PASS** |
| 09 | `proof_09_lobby_weapon_swap_dialog_750px_zh_TW.png` | `6330b31b7bd477b26e877c4dd37659e697c42e856e6dae85e97a1df0b567b24b` | 750px 置中更換裝備彈窗繁中：三欄 Tab、武器庫候選清單、品質色階、屬性說明與按鈕 | ✓ 無 | ✓ 零 | **PASS** |
| 10 | `proof_10_lobby_weapon_swap_dialog_en.png` | `fe9cc8022ac299e277a3e991b5d1beb1b73adbd619bd82b025e4b2e492b65481` | 更換裝備彈窗英文：Armory · Change Equipment，即時切換無破圖 | ✓ 無 | ✓ 零 | **PASS** |
| 11 | `proof_11_lobby_weapon_swap_dialog_ja.png` | `e454c0be576d395ff55a2285342856451091360d00fa6837ac35a39a3fbecd8a` | 更換裝備彈窗日文：武器庫 · 装備変更，即時切換無破圖 | ✓ 無 | ✓ 零 | **PASS** |
| 12 | `proof_12_lobby_character_after_swap.png` | `9b9e68df7dcc1e7d687f34cdb1a611c087050d74fe50689b14e9868449050cac` | 更換裝備後角色頁：攻擊力數值（61）與戰力（90）即時刷新、紙娃娃即時刷新 | ✓ 無 | ✓ 零 | **PASS** |

---

## 5. 特寫裁切存證清單 (crops/)

| 特寫檔名 | SHA256 (完整) | 尺寸 | 涵蓋重點元素 | 驗證結論 |
|:---|:---|:---:|:---|:---:|
| `crop_01_dummy_double_capsules_zh_TW.png` | `c078d45cc876bf60f2af2a92ae7966d0ad73fdc32cff5100fb5c1f851cc6041d` | 740x80 | 繁中最高單擊與總命中雙膠囊特寫（多巴胺天藍/薄荷綠底色） | **PASS** |
| `crop_02_dummy_weapon_contrib_cards_zh_TW.png` | `081b18b1e5152dfffae53ae8398583b27a5f72ed2f2801e5195543679a2de4df` | 740x135 | 繁中三欄武器貢獻卡與輪替切換 3 次膠囊特寫 | **PASS** |
| `crop_03_dummy_weapon_contrib_cards_en.png` | `5ce6ca61e62d302491c37510fa38928a5cd1c48bd483feb0097f8bb3f345c927` | 740x135 | 英文三欄武器貢獻卡與 Weapon Swaps 3 hits 膠囊特寫 | **PASS** |
| `crop_04_dummy_weapon_contrib_cards_ja.png` | `dfe55208a5e10853a005422d6cc0a6e269425a0a0780a62c7961e92b438f5eab` | 740x135 | 日文三欄武器貢獻卡與 武器切り替え 3 回 膠囊特寫 | **PASS** |
| `crop_05_weapon_swap_dialog_header_and_tabs.png` | `c172475b5a553f75220c1ca9b062b0dd51d7ecf9e9b361e128b407ceb1596084` | 750x120 | 750px 彈窗標題列與三欄位 Tab（首選/副手/絕技）切換按鈕特寫 | **PASS** |
| `crop_06_weapon_swap_candidate_item.png` | `c341fefdac8e4a22bbc21e19ffdcdb05161053f7f8ebb2c5e89beb7ea6b72aa8` | 710x150 | 候選武器卡片品質色階標籤（凡品/秘寶/上品）、打擊數、屬性說明與裝備按鈕特寫 | **PASS** |
| `crop_07_lobby_character_stats_panel.png` | `90c58decff98061e9be0da6749e906330f05fe3da7e12ecac65d17294561925d` | 380x280 | 角色頁更換裝備後屬性面板即時刷新（有效戰力90、物理攻擊61）特寫 | **PASS** |
