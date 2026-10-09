# 大廳三欄武器槽聯動與寶箱道具轉譯全面回歸驗收清單 (t_1c9863a0)

## 1. 任務背景與目標
針對 `sideworker2` 將「大廳三欄武器槽聯動真實裝備與即時預覽」（`agent/20261007-lobby-weapon-slots-live-t7e5cfb4b`）與 `sideworker` 之「探索寶箱消耗品與材料專有名詞玩具世界化轉譯」（`agent/20261007-toy-items-tb3a73db2`）合併至 `main` 後，由測試員小婷（`sideqa`）執行全面自動化回歸驗收與實機截圖存證：
1. **無頭冒煙測試**：`godot --path game --headless --quit-after 3` 達成 0 SCRIPT ERROR。
2. **單元測試全綠**：包含 `test_lobby_weapon_loadout_live`、`test_toy_chest_items`、`test_mobile_lobby`、`test_inventory_item_i18n`、`test_maple_inventory` 全數 PASS。
3. **自動化檢查**：`clock-check --live`（14 頁全開、零舊詞）與 `clock-check`（0 缺 .import、0 斷鏈）全數合規。
4. **實機截圖存證**：依據 `review.md` 規範（0-QA15, 0-QA23, 0-QA24, 0-QA25）產出 1280x720 實機截圖與局部裁切特寫，並以 Vision 工具嚴格審查確認零穿模、零舊奇幻詞、零 CJK 殘留、零系統 Emoji。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，正常載入所有資料表與 DisplaySettings | **PASS** |
| **大廳武器槽與紙娃娃連動** | `TEST_FILTER=lobby ./tools/run_tests.sh` | 10/10 全部通過（`LOBBY_WEAPON_LOADOUT_LIVE_OK` 等） | **PASS** |
| **玩具世界化寶箱道具測試** | `TEST_FILTER=toy ./tools/run_tests.sh` | 1/1 通過（`TOY_CHEST_ITEMS_OK`） | **PASS** |
| **道具多語系與消耗品測試** | `TEST_FILTER=item ./tools/run_tests.sh` | 3/3 全部通過（`BATTLE_ITEMS_OK`, `INVENTORY_ITEM_I18N_OK` 等） | **PASS** |
| **背包與快捷欄即時連動** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 2/2 全部通過（`MAPLE_INVENTORY_OK` 等） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/忍者村 零殘留） | **PASS** |
| **資產匯入與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改的素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 規範查核與審驗結論 (review.md)

- [x] **0-QA23（獨立 Proof 目錄）**：所有截圖嚴格產出於 `proofs/t_1c9863a0/` 與 workspace 獨立目錄，不覆寫任何歷史任務存證檔。
- [x] **0-QA15（MD5 雜湊唯一性）**：所有實機全景圖與局部裁切圖 MD5 均獨立相異，絕無重複存檔或黑畫面假過。
- [x] **0-QA24（日韓漢字核實、英文 0 CJK 殘留）**：
  - 日文實機截圖（`放熱冷却剤`、`使う / 売却`、`ショートカットに登録`）經 Vision 審查確認 100% 符合日本新字體（Jōyō Kanji）標準。
  - 英文實機截圖中之道具名稱（`Cooling Coolant`）、說明、按鈕與佔位 glyph（`A` 為 Axle, `P` 為 Plate）經 Vision 審查確認 100% 純英文字元，零 CJK 中文字殘留。
- [x] **0-QA25（同屏即時多語系連動）**：
  - 背包彈窗開著時切換語系，背包彈窗（標題、副標題、道具名、說明、操作鈕、提示語）與底層大廳背景（Gold、Stardust、Shop、Settings、Set Out to Battle、Cogwheel Hamlet、Adventure Bag）100% 同步即時切換。
- [x] **零穿模與紙娃娃防護（0-QA31 / 0-ART 規範）**：
  - 首選武器長劍正確手持 `wpn_dawn_blade_512`，握柄與角色身形層級正確；
  - 副手長槍與絕技鐵拳切換時，安全降級為 `none`，避免低解析度戰鬥小圖示被暴力放大 8 倍覆蓋角色穿模。
- [x] **零系統原生 Emoji**：
  - 畫面中所有資源（發條鑰匙、齒輪金幣、星屑、寶箱、板手、導航圖示等）皆為專用手繪/向量 Sprite 素材，完全零 Unicode 系統原生 Emoji。

---

## 4. 實機截圖清單與 MD5 存證

| 編號 | 截圖檔名 | 測試場景與驗收焦點 | 破圖/穿模 | 零 Emoji | 語系連動 | 驗收結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|
| 01 | `proof_01_lobby_weapon_slot0_sword.png` | 大廳角色頁：首選武器「晨曦長劍」（上品藍階），紙娃娃持劍正常無穿模，戰力與屬性連動 | ✓ 無 | ✓ 零 | ✓ 繁中基準 | **PASS** |
| 02 | `proof_02_lobby_weapon_slot1_spear.png` | 大廳角色頁：副手武器「破浪長槍」（良品綠階），亮橙選中態，3 次打擊，面板攻擊連動更新 (27) | ✓ 無 | ✓ 零 | ✓ 即時連動 | **PASS** |
| 03 | `proof_03_lobby_weapon_slot2_fist.png` | 大廳角色頁：絕技武器「熔火鐵拳」（秘寶紫階），5 連擊，面板攻擊連動更新 (35)，零穿模 | ✓ 無 | ✓ 零 | ✓ 即時連動 | **PASS** |
| 04 | `proof_04_inventory_toy_items_zh_TW.png` | 背包道具繁中全景：散熱冷卻劑等 100% 玩具世界化詞彙，零舊奇幻詞（小紅水/乾糧/焰骨/狼牙） | ✓ 無 | ✓ 零 | ✓ 繁中基準 | **PASS** |
| 05 | `proof_05_inventory_toy_items_en.png` | 背包道具英文全景：Cooling Coolant，大廳與背包同屏全英連動，無 CJK 殘留 (0-QA24, 0-QA25) | ✓ 無 | ✓ 零 | ✓ 100% 英文 | **PASS** |
| 06 | `proof_06_inventory_toy_items_ja.png` | 背包道具日文全景：放熱冷却剤，常用漢字與新字體對齊，大廳同屏日文連動 (0-QA24, 0-QA25) | ✓ 無 | ✓ 零 | ✓ 100% 日文 | **PASS** |

### 實機局部裁切特寫 (crops/)
- `crop_01_weapon_slots_sword.png` (MD5: `ae2b4b9883de56aaff8346b981522448`)
- `crop_02_weapon_slots_spear.png` (MD5: `2e2fae29aa2844d891e3a79f58d08c9e`)
- `crop_03_weapon_slots_fist.png` (MD5: `757d1a4c51539e985b74f500535e5fea`)
- `crop_04_inventory_toy_items_zh_TW.png` (MD5: `69b09cb007643f303180f3acdbd5acff`)
- `crop_05_inventory_toy_items_en.png` (MD5: `18fa9ca6d066a7f1f5978744958d62bc`)
- `crop_06_inventory_toy_items_ja.png` (MD5: `f825a6d616e1470528813cd513ada1f3`)

### 實機全景 MD5 雜湊表
- `proof_01_lobby_weapon_slot0_sword.png`: `11e1de61e2716d3a28596c1cfef2e74c`
- `proof_02_lobby_weapon_slot1_spear.png`: `50b7ae9e150db9626469e7e816e9d0b5`
- `proof_03_lobby_weapon_slot2_fist.png`: `64b862843920a690964730c49c196288`
- `proof_04_inventory_toy_items_zh_TW.png`: `4209b9451321ee53267f74dbf970df7f`
- `proof_05_inventory_toy_items_en.png`: `68a1d932e18df3f74508ee6f00ec7146`
- `proof_06_inventory_toy_items_ja.png`: `801255b6bd16fa5fb852797843db3834`
