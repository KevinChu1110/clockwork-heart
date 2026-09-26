# 《發條之心》大廳 Dock 頁籤與頂欄能量金幣星屑六語系 查驗清單與驗收報告 (t_a93ad08c)

- **執行人**：阿翔（側案·工程師 sideworker2）
- **關聯任務**：`t_a93ad08c`（🎮 遊戲開發｜大廳 Dock 頁籤與頂欄能量金幣星屑六語系）
- **交付目錄**：`proofs/lobby-dock-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/lobby-dock-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準（如「金」、「星屑」、「ぜんまい新村」、「四区出征」、「聚魂殿」），確認為合規譯名，非中文殘留。
  - `review.md 0-QA25`：同張截圖全景查驗，頂欄三資源名、商城/設置鈕、左側殿堂、中央主角、右側裝備/出征與底部 Dock 全數呈現同語系。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_lobby_dock_en.png` | 大廳村莊全景（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_lobby_dock_ja.png` | 大廳村莊全景（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |

---

## 二、 語系對照與詞條清單

所有玩家可見文字均透過 `_t()` / `ContentLoc.text("ui", ...)` 對接 `game/data/i18n/content/<locale>/ui.json`：

| 來源原文 (zh_TW) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) | 簡體中文 (zh_CN) |
|---|---|---|---|---|---|
| **能量** | Energy | エネルギー | 에너지 | Energía | 能量 |
| **金幣** | Gold | 金 | 골드 | Oro | 金币 |
| **星屑** | Stardust | 星屑 | 별가루 | Polvo estelar | 星屑 |
| **發條新村** | Cogwheel Hamlet | ぜんまい新村 | 태엽 신촌 | Aldea Mecánica | 发条新村 |
| **角色裝備** | Hero Gear | キャラ装備 | 캐릭터 장비 | Equipo de héroe | 角色装备 |
| **四區出征** | Four Regions | 四区出征 | 4구역 출정 | Cuatro Regiones | 四区出征 |
| **聚魂殿堂** | Soul Hall | 聚魂殿 | 영혼의 전당 | Salón del Alma | 聚魂殿堂 |
| **冒險背包** | Adventure Bag | 冒険バッグ | 모험 배낭 | Bolsa de aventura | 冒险背包 |

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元測試**：
   - `test_mobile_lobby.gd`：新增 `_test_dock_and_topbar_i18n()` 測試，涵蓋六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）動態即時切換 `Loc.set_locale()` 時，頂欄三寶標籤（`_energy_title_label`、`_gold_title_label`、`_gem_title_label`）與底部五頁籤（`_dock_buttons`）的文字完全對齊語系表。
   - 執行 `TEST_FILTER=lobby ./tools/run_tests.sh`：2 個測試全數綠燈通過（`MOBILE_LOBBY_OK`、`LOBBY_EQUIP_I18N_OK`）。
3. **Vision 模型審查**：
   - `proof_lobby_dock_en.png` 與 `proof_lobby_dock_ja.png` 親自開圖審查。
   - 頂欄三資源（Energy / Gold / Stardust 與 エネルギー / 金 / 星屑）與底部五頁籤（Cogwheel Hamlet 等與 ぜんまい新村 等）皆準確翻譯。
   - 畫面無破圖、無溢出截字、無系統 Emoji、無舊版 IP 名詞殘留。
   - 符合 0-QA23（獨立 OUT_DIR）、0-QA24（日文漢字依語系檔為準）、0-QA25（全畫面 UI 語系一致）。
