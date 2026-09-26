# 《發條之心》探索性 QA 第三十五輪 查驗清單與缺陷報告 (Round 35 Checklist)

- **測試日期**：2026-09-26
- **測試員**：小婷（側案·測試 sideqa）
- **關聯卡號**：`t_66544bf2`
- **關聯前置任務**：
  - `t_64ef4f3d`（大廳裝備欄武器／發條／奇玩名稱六語系落地與切換即時刷新，來源分支 `wt/t_4e7681e8`）
  - `t_27f1d695`（創角種族卡與槽位標題六語系改動合進主線，來源分支 `wt/t_61561279`）
- **存檔目錄**：`/opt/side/bravesoul-game/proofs/qa_round35/`

---

## 一、 實機截圖核驗清單（每張全景圖：破圖／emoji／截字／模糊／語系一致性）

依據規範（review.md 0-QA15、0-QA17、0-QA23、0-QA24、0-QA25），全數實機截圖規格為 1280x720，MD5 經查核 100% 獨立無覆蓋：

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零系統Emoji | 零截字 | 高清立繪 | 審核結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_lobby_zh_TW.png` | 大廳全景（zh_TW 繁中基準：外裝／武器／發條／奇玩） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 02 | `proof_02_lobby_en.png` | 大廳全景（en 英文：Outfit/Weapon/Clockwork/Curio） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 03 | `proof_03_lobby_ja.png` | 大廳全景（ja 日文：衣装／武器／ゼンマイ／骨董品） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 04 | `proof_04_lobby_ko.png` | 大廳全景（ko 韓文：외형／무기／태엽／진기품） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 05 | `proof_05_creation_launch_zh_TW.png` | 創角首發分頁（zh_TW 白金兔全景基準） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 06 | `proof_06_creation_launch_en.png` | 創角首發分頁（en 英文：種族卡＋槽位標題＋狀態列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 07 | `proof_07_creation_launch_ja.png` | 創角首發分頁（ja 日文：種族卡＋槽位標題＋狀態列） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 08 | `proof_08_creation_expansion_zh_TW.png` | 創角擴充分頁（zh_TW 瓷韻熊貓全景基準） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 09 | `proof_09_creation_expansion_en.png` | 創角擴充分頁（en 英文：擴充8族＋Colossus Elephant） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |
| 10 | `proof_10_creation_expansion_ja.png` | 創角擴充分頁（ja 日文：擴充8族＋磁韻パンダ立繪） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 512高清 | 合格 (PASS) |

### 局部特寫 Crops 驗證清單（`proofs/qa_round35/crops/`）
- `crop_lobby_equip_{zh_TW,en,ja}.png`：大廳右側裝備欄四槽位（外裝、武器、發條、奇玩）多語系特寫。
- `crop_lobby_dock_{zh_TW,en,ja}.png`：大廳底部 Dock 五大入口多語系連動特寫。
- `crop_race_cards_launch_{zh_TW,en,ja}.png`：創角首發 5 族種族卡橫條特寫。
- `crop_race_cards_expansion_{zh_TW,en,ja}.png`：創角擴充 8 族種族卡橫條特寫（驗證 The Colossus Elephant 自適應雙行置中）。
- `crop_slots_panel_{zh_TW,en,ja}.png`：創角右側模組槽位標題與 512 高清狀態列特寫。
- `crop_creation_actions_{zh_TW,en,ja}.png`：創角底部操作按鈕（確認選擇 · 踏上旅途／返回）特寫。

---

## 二、 專項查核重點結果

### 1. 大廳右側裝備欄四槽位六語系驗證（proof_01 ~ proof_04）
- **前置缺陷複驗（Round 34 發現之裝備名漏翻）**：
  - **zh_TW 基準**：
    - 外裝：`碧簧巡林客工裝`
    - 武器：`碧葉旋刃機關鏢`
    - 發條：`雙蝶翼同心圓黃銅發條鑰匙`
    - 奇玩：`微型發條荷葉浮空傘`
  - **en 英文環境**：
    - `Outfit  Spring Forest Courier Overalls`
    - `Weapon  Lotus Cog Dart`
    - `Clockwork  Twin-Wing Concentric Brass Key`
    - `Curio  Floating Lotus Leaf Parasol`
    - **核驗結論**：四部件名稱與標題 100% 完整英文化，零繁中殘留，字體大小依長度自動縮放（10~13px），無溢出與無省略截斷。
  - **ja 日文環境**：
    - `衣装  碧箸巡林客作業着`
    - `武器  碧葉旋刃からくり鏢`
    - `ゼンマイ  双蝶翼同心円黄銅ゼンマイキー`
    - `骨董品  超小型ゼンマイ蓮葉浮空傘`
    - **核驗結論**：四部件標題與名稱已完全在地化，採用日文新字體（双、円、着、業），零繁中殘留。
  - **ko 韓文環境**：
    - `외형  벽저 순림객 작업복`
    - `무기  벽엽선인 기관 표창`
    - `태엽  쌍접익 동심원 황동 태엽 열쇠`
    - `진기품  초소형 태엽 연잎 부유 우산`
    - **核驗結論**：四部件類別標題與道具全名均已完整翻譯為流暢正確的韓文。
- **大廳頂欄與 Dock 語系連動（0-QA25 規範）**：
  - 頂欄（能量/金幣/星屑/商城/設置）與底欄 Dock（發條新村/角色裝備/四區出征/聚魂殿堂/冒險背包）與右側裝備欄同時處於同一語系，切換語言即時刷新，無語系脫節。

### 2. 創角首發分頁種族卡與槽位標題驗證（proof_05 ~ proof_07）
- **頂部分頁**：
  - zh_TW:「首發」「擴充」
  - en:「Launch」「Expansion」
  - ja:「初期」「拡張」
- **首發 5 族種族卡**：
  - zh_TW: 白金兔、靈尾狐、烈鬃獅、鋼牙豕、靈爪猴
  - en: Clockwork Rabbit、Astral Fox、Gilded Lion、Forge Boar、Spring Macaque
  - ja: 白金兎、霊尾狐、烈鬃獅子、鋼牙猪、霊爪猿
  - **核驗結論**：卡片標籤 100% 接入 i18n，點擊即時高亮，無破圖或空卡。
- **右側槽位標題與狀態列**：
  - zh_TW:
    - `• 外裝服飾槽 (Costume Slot - Z:25)`
    - `• 軀體塗裝槽 (Chassis Shell - Z:10)`
    - `• 手持武器槽 (Weapon Slot - Z:40)`
    - 狀態列：`7 大槽位狀態：512 高清合成就緒 (渲染: 7/7)`
  - en:
    - `• Costume Slot (Costume Slot - Z:25)`
    - `• Chassis Shell Slot (Chassis Shell - Z:10)`
    - `• Handheld Weapon Slot (Weapon Slot - Z:40)`
    - 狀態列：`7 Slot Status: 512 HD Composite Ready (Rendered: 7/7)`
  - ja:
    - `• 衣装スロット (Costume Slot - Z:25)`
    - `• 機体塗装スロット (Chassis Shell - Z:10)`
    - `• 手持ち武器スロット (Weapon Slot - Z:40)`
    - 狀態列：`7スロット状態：512 HD合成完了 (描画: 7/7)`
- **底部操作按鈕**：
  - zh_TW: 還原預設／確認選擇 · 踏上旅途／返回
  - en: Reset Defaults／Confirm Selection · Begin Journey／Back
  - ja: デフォルトに戻す／選択確認 · 旅立ち／戻る

### 3. 創角擴充分頁種族卡長譯名與排版查核（proof_08 ~ proof_10）
- **擴充 8 族種族卡**：
  - 涵蓋：烈焰虎、雲嵐鶴、玄軸熊、蒸氣企鵝、玄機龜、鋼岳象、碧簧蛙、瓷韻熊貓。
  - **The Colossus Elephant 長譯名排版**：經 Vision 顯微核查，卡片名稱成功啟用 `WORD_SMART` 自適應折行為雙行居中（第一行 `The Colossus`，第二行 `Elephant`），左右邊距保留 10px，徹底消除向外溢出與鄰近卡片重疊碰撞瑕疵。
- **角色立繪**：
  - 瓷韻熊貓（The Porcelain Panda / 磁韻パンダ）512 高清合成完整，各部件圖層拼合無裂紋、無色偏、無系統 Emoji。

### 4. 日／韓漢字翻譯規範核實（0-QA24 規範）
- 日文環境下：
  - 「鋼岳象」在 `ui.json` 中本即以日文漢字收錄（`"鋼岳象": "鋼岳象"`），屬於合法漢字沿用，不誤判為漏翻。
  - 「白金兎」、「霊尾狐」、「雙」轉「双」、「圓」轉「円」均正確遵循日文新字體規範。

### 5. 截圖目錄獨立性核驗（0-QA23 規範）
- 截圖腳本 `tools/capture_qa_round35.gd` 將輸出嚴格限定於 `proofs/qa_round35/` 與 `proofs/qa_round35/crops/`，完全未寫入或覆蓋其他任務的 proof 目錄。

---

## 三、 探索性發現之缺陷報告（什麼輸入 → 什麼壞掉）
*註：依任務規範「若還有玩家可見漏翻，CHECKLIST 寫『什麼輸入→什麼壞掉』；本單不修，由製作人另開單」。*

### 【缺陷 1】創角展示介面內部資料層文字（選項副標說明與風味敘述）在非繁中語系下未翻譯
- **觸發輸入**：
  1. 切換語言至英文（en）或日文（ja）。
  2. 進入創角紙娃娃選擇介面（`paperdoll_select_demo`）。
- **壞掉現象**：
  - 頂部分頁、種族卡、槽位大標題、狀態列與底部按鈕均已正確翻譯。
  - 但**槽位選中項目的副標說明**與**左側立繪底部風味描述**仍顯示為繁體中文（見 `proof_06`、`proof_07`、`proof_09`、`proof_10` 及 `crop_slots_panel_en.png`）：
    - 服裝槽副標：仍顯示「`經典紅藍胡桃鉗金屬禮服與黃銅肩章`」或「`高溫黑白生漆陶瓷板件與天元道場武道長袍`」。
    - 塗裝槽項目與副標：仍顯示「`原廠象牙白`」及「`溫潤微光象牙白高光琺瑯塗層`」。
    - 左側立繪底層說明：仍顯示「`發條之心的守護象徵，身形輕巧，搭載高響應晨曦核心與剛性長耳。`」或「`自天元竹林悟道的發條陶瓷熊貓，黑白高溫生漆陶瓷板件...`」。
    - 頂部展示標題橫幅：仍為「`發條之心 · 紙娃娃試衣間`」。
- **根本原因**：
  `t_61561279` 任務範圍聚焦於種族卡與槽位控制項標題（Slot Title）；`paperdoll_select_demo.gd` 中各外裝、塗裝字典裡的 `desc` 欄位與 `RACES_DATA` 內的 `desc`、頂部標題標籤尚未呼叫 `Loc.t()` 進行六語系翻譯。
- **修復建議**：
  建議製作人開單補充 `paperdoll_select_demo.gd` 的 `desc` 欄位與展示標題的多語系詞條映射。

### 【缺陷 2】日文擴充種族卡中少數漢字未轉換為日文新字體
- **觸發輸入**：
  1. 切換語言至日文（ja）。
  2. 進入創角擴充分頁。
- **壞掉現象**：
  - 「玄機龜」卡片顯示繁體「龜」（日文規範漢字為「亀」）。
  - 「烈焰虎」顯示「烈焰虎」（日文一般習慣用「烈火の虎」或「烈焔虎」）。
- **根本原因**：
  `ui.json` 中 ja 語系對應詞條未細化為日文新字體。
- **修復建議**：
  於 `game/data/i18n/content/ja/ui.json` 將「玄機龜」調整為「玄機亀」。

---

## 四、 驗收指令執行紀錄

- `godot --path game --headless --quit-after 3`：**0 SCRIPT ERROR**（通過）。
- `TEST_FILTER=lobby ./tools/run_tests.sh`：**2/2 PASSED**（含 `test_lobby_equip_i18n`、`test_mobile_lobby`）。
- `TEST_FILTER=creation ./tools/run_tests.sh`：**6/6 PASSED**（含 `test_paperdoll_creation_breathe`、`test_character_creation_flow`、`test_creation_race_i18n`、`test_creation_race_tabs`、`test_creation_stage_no_128_fallback`、`test_creation_tabs_i18n`）。
- `TEST_FILTER=i18n ./tools/run_tests.sh`：**6/6 PASSED**（含 `test_i18n`、`test_creation_race_i18n`、`test_creation_tabs_i18n`、`test_lobby_equip_i18n`、`test_wardrobe_i18n`、`test_windup_daily_i18n`）。
- **Vision 逐張審查**：全數 10 張實機全景截圖與 6 組特寫裁剪均已親自由 Vision 模型完成視覺審驗與缺陷定位。
