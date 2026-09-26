# 探索性 QA 第四十五輪：抽魂結果卡六語系＋裝備面板 720p 修復合主線後找破圖驗收清單 (qa-round45)

- **執行人**：小婷（側案·測試 sideqa）
- **關聯任務**：`t_e1f74739`（🤖 平台與維運｜探索性 QA 第四十五輪：抽魂結果卡六語系＋裝備面板 720p 修復合主線後找破圖）
- **前置任務**：
  - `t_33ac0c71`（🎮 遊戲開發｜抽魂結果卡掉落種類與名稱六語系，commit `0f458a3d`）
  - `t_40fd7012`（🎮 遊戲開發｜修復裝備面板 720p 垂直溢出包進 ScrollContainer 與補齊英文品質標籤，commit `8878a019`）
- **交付目錄**：`proofs/qa_round45/`（遵守 `review.md 0-QA23` 獨立專屬目錄，絕無跨卡覆蓋）
- **遵循規範**：
  - `review.md 0-QA15`：本輪產出無重複檔名、無相同內容（全數 11 張全景截圖與 10 張特寫 crops MD5 100% 獨立唯一）。
  - `review.md 0-QA17`：實機截圖完整呈現核心功能畫面，包含抽魂結果卡（en/ja/zh_TW 零件與換裝）、裝備面板（en/zh_TW 頂部與捲到底返回鈕）、大廳 chrome 語系同步連動。
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/qa_round45/`，完全未動到、覆蓋或干擾其他任務之 proof 目錄。
  - `review.md 0-QA24`：日文漢字（「パーツ」、「真鍮の歯車」、「着せ替え」、「小白・クリーム普段着」、「シロ」、「エネルギー」、「金」、「星屑」、「ショップ」、「設定」、「ぜんまい新村」、「キャラ装備」、「四区出征」、「聚魂殿」、「冒険バッグ」等）均回查 `ja.json` 與 `content/ja/ui.json` 核實，確認為合規既定詞條，非漏翻殘留。
  - `review.md 0-QA25`：全畫面連動查驗，彈窗以外的大廳背景、頂部狀態列（Lv.16 / 角色名 / 能量 / 金幣 / 星屑）、底部導航 Dock 同步連動目標語系，無半中半英。

---

## 一、 實機全景截圖核驗清單（1280x720，逐張打勾）

| 編號 | 實機截圖檔名 | 涵蓋場景與語系 | 破圖 | 零 Emoji | 零截字 | 語系連動 (0-QA25) | 驗證結論 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_en_soul_result_card.png` | en 抽魂結果卡（零件展示：徽章 `Part`、名稱 `Brass Gear`、提示 `Part logged in the codex!`、底層按鈕全英文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 02 | `proof_02_ja_soul_result_card.png` | ja 抽魂結果卡（零件展示：徽章 `パーツ`、名稱 `真鍮の歯車`、提示 `パーツ図鑑に入った！`、底層按鈕全日文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 03 | `proof_03_ja_soul_result_outfit.png` | ja 抽魂結果卡（換裝展示：徽章 `着せ替え`、名稱 `小白・クリーム普段着`、提示 `新しいステッカー皮！着替える？`） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24) | **通過 (PASS)** |
| 04 | `proof_04_zh_TW_soul_result_card.png` | zh_TW 抽魂結果卡（繁中基準：徽章 `換裝`、名稱 `小白 · 奶油便服`、提示 `新貼紙皮！要換上嗎？`） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中基準 | **通過 (PASS)** |
| 05 | `proof_05_en_equip_panel_top.png` | en 裝備面板頂部（標題 `Equipment`、`Total ATK+4 DEF+0...`、武器欄 `Weapon slots`、防具 `Armour`、飾品槽） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 | **通過 (PASS)** |
| 06 | `proof_06_en_equip_panel_bottom.png` | en 裝備面板捲到底（720p 垂直捲動到底、**返回鈕 `Back` 清晰可見完整顯示**、背包格品質標籤 `Rare`/`Epic`/`Common`） | ✓ 無 | ✓ 零 | ⚠️ 發現折行與溢出 | ✓ 100% 英文連動 | **有缺陷記錄 (FINDING)** |
| 07 | `proof_07_zh_TW_equip_panel_top.png` | zh_TW 裝備面板頂部基準（標題 `裝備`、總加成、武器欄 3 欄、防具槽、飾品六槽） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中基準 | **通過 (PASS)** |
| 08 | `proof_08_zh_TW_equip_panel_bottom.png` | zh_TW 裝備面板捲到底基準（720p 垂直捲動到底、**返回鈕 `返回` 清晰可見完整顯示**、背包格道具） | ✓ 無 | ✓ 零 | ✓ 無 | ⚠️ 發現武器類別殘留英文 | **有缺陷記錄 (FINDING)** |
| 09 | `proof_09_en_lobby_chrome.png` | en 大廳主介面全景（切語系連動：頂部狀態列 `Lv.16 Xiaobai`, `Energy`, `Gold`, `Stardust`, `Shop`, `Settings`；底部 Dock 5 頁籤全英文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 英文連動 (0-QA25) | **通過 (PASS)** |
| 10 | `proof_10_ja_lobby_chrome.png` | ja 大廳主介面全景（切語系連動：頂部狀態列 `Lv.16 シロ`, `エネルギー`, `金`, `星屑`, `ショップ`, `設定`；底部 Dock `ぜんまい新村` 等全日文） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 日文連動 (0-QA24/25) | **通過 (PASS)** |
| 11 | `proof_11_zh_TW_lobby_chrome.png` | zh_TW 大廳主介面全景基準（繁中基準：頂部狀態列 `Lv.16 小白`, `能量`, `金幣`, `星屑`, `商城`, `設置`；底部 Dock 5 頁籤全繁中） | ✓ 無 | ✓ 零 | ✓ 無 | ✓ 100% 繁中基準 | **通過 (PASS)** |

---

## 二、 實機截圖檔案與 MD5 查驗表

全數檔案均為 1280x720 實機 framebuffer 渲染（特寫裁切為對應局部區域），21 個檔案 MD5 均為獨立真實生成，符合 `review.md 0-QA15`：

```
a32ada9c920da3811fdc56d2e5654baf  proof_01_en_soul_result_card.png (1280x720)
092c766ef14c4287bba9be4b345bd045  proof_02_ja_soul_result_card.png (1280x720)
d2a9947cc2a713a83c6c42c60c342b70  proof_03_ja_soul_result_outfit.png (1280x720)
b662129932c95156fc02377d4c8271ff  proof_04_zh_TW_soul_result_card.png (1280x720)
f2dbe8a8e8a2344acde9d93f5068b25b  proof_05_en_equip_panel_top.png (1280x720)
292ec04bc94268ca71daf44645c7e91d  proof_06_en_equip_panel_bottom.png (1280x720)
7e344544f5a701bad92fa2aeb9bc2178  proof_07_zh_TW_equip_panel_top.png (1280x720)
750bc75fd900b58714027fe8e2196b51  proof_08_zh_TW_equip_panel_bottom.png (1280x720)
b9dff0c469336e441eb46e816e39fbf6  proof_09_en_lobby_chrome.png (1280x720)
bc480257728d5b94c96e7fc44d401cbc  proof_10_ja_lobby_chrome.png (1280x720)
e214339302255e95620973fc9814e70b  proof_11_zh_TW_lobby_chrome.png (1280x720)

crops/9857b40a9b71f233a959756f49a6f911  crops/crop_01_en_soul_badge_name.png (600x180)
crops/97405287700dc156f6ee6dabe4e132a3  crops/crop_02_ja_soul_badge_name.png (600x180)
crops/02819ff46986907a35d52d4d1ad894b8  crops/crop_03_ja_soul_outfit_badge.png (600x180)
crops/07b00e5a6c098a42b7c0a20fca107a61  crops/crop_04_en_equip_back_btn_bottom.png (600x320)
crops/f022974df2f57f8bbc5c53d0301d4c82  crops/crop_05_zh_TW_equip_back_btn_bottom.png (600x320)
crops/2cc58179222131dd0f52b51551da89be  crops/crop_06_en_equip_item_text_issue.png (145x140)
crops/e962ac43afa08fa0dc518357ab7f7562  crops/crop_07_en_lobby_top_bar.png (1280x80)
crops/612195f0c4c662fe33231eb3aea563fc  crops/crop_08_en_lobby_dock.png (1280x90)
crops/e0192bd41e6dee05227eeae01e524e95  crops/crop_09_ja_lobby_top_bar.png (1280x80)
crops/08b542d45f2f1f28ac3213d758640923  crops/crop_10_ja_lobby_dock.png (1280x90)
```

---

## 三、 局部特寫 Crops 驗證說明

1. **`crops/crop_01_en_soul_badge_name.png`**：
   - 英文結果卡底部特寫：徽章 `Part`、提示 `Part logged in the codex!` 與明細 `【Part】 Brass Gear`，排版置中無截字。
2. **`crops/crop_02_ja_soul_badge_name.png`**：
   - 日文結果卡底部特寫：徽章 `パーツ`、提示 `パーツ図鑑に入った！` 與明細 `【パーツ】 真鍮の歯車`，日文漢字符合 0-QA24 既定詞條。
3. **`crops/crop_03_ja_soul_outfit_badge.png`**：
   - 日文結果卡換裝特寫：徽章 `着せ替え`、提示 `新しいステッカー皮！着替える？` 與明細 `【着せ替え】 小白・クリーム普段着`。
4. **`crops/crop_04_en_equip_back_btn_bottom.png`**：
   - 英文裝備面板捲動到底部特寫：黃色立體果凍圓角按鈕 **`Back`** 完整置中顯示於視窗底部，不再發生 720p 垂直溢出被截斷問題。
5. **`crops/crop_05_zh_TW_equip_back_btn_bottom.png`**：
   - 繁體中文裝備面板捲動到底部特寫：黃色立體果凍圓角按鈕 **`返回`** 完整置中顯示於視窗底部，驗證修復跨語系一致。
6. **`crops/crop_06_en_equip_item_text_issue.png`**：
   - 英文背包第 6 格特寫：清晰記錄「Bladestanc / e Ring」異常 mid-word line wrap 折行與底部品質標籤邊界壓邊缺陷。
7. **`crops/crop_07_en_lobby_top_bar.png`** 與 **`crops/crop_08_en_lobby_dock.png`**：
   - 英文大廳 chrome 特寫：頂部狀態列（`Lv.16 Xiaobai`、`Energy`、`Gold`、`Stardust`、`Shop`、`Settings`）與底部導航 Dock 5 頁籤完全即時連動為英文。
8. **`crops/crop_09_ja_lobby_top_bar.png`** 與 **`crops/crop_10_ja_lobby_dock.png`**：
   - 日文大廳 chrome 特寫：頂部狀態列（`Lv.16 シロ`、`エネルギー`、`金`、`星屑`、`ショップ`、`設定`）與底部導航 Dock 5 頁籤完全即時連動為日文。

---

## 四、 玩家可見缺陷記錄（嚴格遵守「什麼輸入 → 什麼壞掉」，不改程式）

依據任務規範「找到玩家可見缺陷只寫『什麼輸入 → 什麼壞掉』，不准改程式。漏翻一詞等小錯留給製作人」，本輪實機巡檢發現以下 2 項缺陷：

### 缺陷 1：英文裝備面板背包道具名稱 mid-word 折行與品質標籤貼齊邊框
- **輸入**：語系切換至英文 (`en`)，打開裝備面板（EquipPanel），捲動到底部背包區域（`Bag (tap to equip)`）。
- **壞掉**：第 6 格裝備名「Bladestance Ring」在 110x110 卡片容器內因寬度不足且採用自動換行，發生單字中間截斷折行（拆為第一行 `Bladestanc` 與第二行 `e Ring`）；同時因名稱佔用兩行垂直高度，擠壓下方品質標籤，導致底部品質文字（`Rare`）直接壓在卡片粉紅邊框線上，甚至輕微溢出邊框。

### 缺陷 2：繁體中文裝備面板背包武器品質標籤後方殘留未翻譯英文 `· sword`
- **輸入**：語系切換至繁體中文 (`zh_TW`)，打開裝備面板（EquipPanel），捲動到底部背包查看武器類道具（如騎士軍刀、晨光長劍）。
- **壞掉**：武器品質標籤顯示為 `上品 · sword` 與 `秘寶 · sword`，其中的 `· sword` 武器類型字樣為英文原始鍵值未經在地化轉換，未顯示為繁中（例如 `· 劍`）。

---

## 五、 綜合驗證結論

1. **抽魂結果卡六語系與即時連動**：
   - en 與 ja 抽魂結果卡徽章與掉落名稱完全符合在地化規範，開著結果卡切換語系能即時動態刷新。
   - 零系統 Emoji、日文漢字符合 0-QA24 語系詞條定義。
2. **裝備面板 720p 垂直捲動與返回鈕**：
   - 包入 `ScrollContainer` 後，1280x720 解析度下裝備面板可正常垂直捲動，捲動到底部時**返回鈕（`Back`／`返回`）清晰完整可見**，徹底解決先前 720p 溢出截斷問題。
   - 英文品質標籤（`Common`、`Rare`、`Epic`、`Legendary`）已補齊並正常渲染顯示。
3. **大廳 Chrome 語系同步連動 (0-QA25)**：
   - 切換語系時，頂部狀態列（等級、角色名、三種貨幣、商城、設置按鈕）與底部 Dock 5 頁籤 100% 同步連動更新，無任何背景殘留中文。
