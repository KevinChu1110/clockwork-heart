# 稱號牆稱號名與解鎖條件六語系 驗收清單 (title-names-i18n)

## 1. 任務目標
稱號牆標題與按鈕已六語系，但實際稱號名與解鎖條件仍寫死繁中。本任務完成：
1. `title_catalog` 裡玩家看得到的 `name`／`desc` 改走 ContentLoc，資料表繁中當 key，並在各語系 `ui.json` 補齊對照，同時補齊 `zh_TW/title.json`。
2. 接 `Loc.locale_changed`，開著稱號牆切換語系，稱號名稱、解鎖條件、新解鎖橫幅提示、狀態標籤立即刷新。
3. 24 筆稱號全數補齊六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），零系統 emoji。
4. 牆的 chrome（大標題／關閉鈕／已解鎖狀態／計數進度）不重複做，完整保持既有規範。
5. 解鎖規則與已解鎖狀態數值完全不變。

## 2. 交付檔案
- **系統層**：`game/scripts/systems/title_catalog.gd`
  - `entries()` 改走 ContentLoc，支援資料表繁中當 key，回傳各語系在地化名稱與條件
  - 增加 `get_entry(flag)` 查詢輔助函式
- **UI 彈窗**：`game/scripts/ui/title_wall_dialog.gd`
  - `_create_title_card()` 記錄 `flag`、`raw_name`、`raw_desc` metadata
  - `_update_ui_texts()` 在收到 `locale_changed` 時，即時遍歷所有卡片，將每張卡片的 `NameLabel` 與 `DescLabel` 刷新為當前語系
  - `_banner_lbl` 新解鎖稱號提示橫幅支援元素個別在地化翻譯
  - 增加 `get_card_by_flag()`、`get_card_name_text()`、`get_card_desc_text()`
- **六語系詞條檔**：
  - `game/data/i18n/content/zh_TW/title.json`（補齊繁中基準 24 筆稱號定義）
  - `game/data/i18n/content/{zh_TW,zh_CN,en,ja,ko,es}/ui.json`（全數寫入 24 筆稱號名稱與解鎖條件，繁中為 key）
- **具名單元測試**：`game/scripts/ui/test_title_wall_i18n.gd`
  - 抽驗至少 4 個稱號名與條件（`title.claw_parry`, `title.cleared`, `title.star_wisher`, `title.wood_mentor`）在六語系動態切換下的即時刷新與準確性
- **實機截圖腳本**：`tools/capture_title_names_i18n.gd`
- **實機截圖存證（0-QA23 獨立目錄）**：
  - `proofs/title-names-i18n/proof_01_title_names_en.png`（英文全景實機，背後大廳同步切換 en，0-QA25）
  - `proofs/title-names-i18n/crops/crop_01_title_names_en.png`（英文稱號牆局部裁切）
  - `proofs/title-names-i18n/proof_02_title_names_ja.png`（日文全景實機，背後大廳同步切換 ja，0-QA25）
  - `proofs/title-names-i18n/crops/crop_02_title_names_ja.png`（日文稱號牆局部裁切）
  - `proofs/title-names-i18n/proof_03_title_names_zh_TW.png`（繁中全景基準對照）
  - `proofs/title-names-i18n/crops/crop_03_title_names_zh_TW.png`（繁中稱號牆局部裁切）

## 3. 抽樣稱號多語系對照表

| Flag | zh_TW | zh_CN | en | ja | ko | es |
|---|---|---|---|---|---|---|
| `title.claw_parry` | 以劍抵爪 | 以剑抵爪 | Sword Against Claw | 剣もて爪を受く | 검으로 발톱을 받다 | Espada contra zarpa |
| `title.claw_parry` (desc) | 對雷歐完美格擋至少一次。 | 对雷欧完美格挡至少一次。 | Land at least one perfect parry on Leo. | レオに完璧なパリィを一度以上。 | 레오에게 완벽한 패링을 한 번 이상. | Para a Leo a la perfección al menos una vez. |
| `title.cleared` | 晨光中的兔子 | 晨光中的兔子 | Rabbit in the Morning Light | 朝光の中の兎 | 아침빛 속의 토끼 | El conejo del amanecer |
| `title.cleared` (desc) | 通關終章。 | 通关终章。 | Clear the final chapter. | 終章をクリア。 | 종장 클리어. | Termina el capítulo final. |
| `title.star_wisher` | 許願兔 | 许愿兔 | Wishing Rabbit | 願う兎 | 소원 비는 토끼 | Conejo que pide deseos |
| `title.star_wisher` (desc) | 在星落淺池許下一願——不必說出口。 | 在星落浅池许下一愿——不必说出口。 | Make a wish at the Starfall shallows — no need to say it aloud. | 星落の浅池でひとつ願った——口に出さなくていい。 | 성락 얕은 못에서 한 가지 빌었다——입 밖에 낼 필요는 없다. | Pide un deseo en las aguas de Estrellas Caídas; no hace falta decirlo en voz alta. |
| `title.wood_mentor` | 木劍之約 | 木剑之约 | Promise of the Wooden Sword | 木剣の約束 | 목검의 약속 | Promesa de la espada de madera |
| `title.wood_mentor` (desc) | 把練習的夢想交到小芽手裡。 | 把练习的梦想交到小芽手里。 | Put the dream of practice into Sprout's hands. | 稽古という夢を芽の手に渡した。 | 연습이라는 꿈을 새싹의 손에 쥐여 주었다. | Pon el sueño de practicar en manos de Brote. |

## 4. 驗收規範審核結果 (review.md)

- [x] **0-QA23（獨立 proof 目錄）**：所有實機截圖與裁切圖嚴格存放在 `proofs/title-names-i18n/`，無修改或覆蓋其他任務之 proof（如 `proofs/title_wall/`、`proofs/title_wall_i18n/` 等舊檔案均完整保留未更動）。
- [x] **0-QA24（日／韓漢字核實、英文無 CJK 殘留）**：
  - 英文全景中，彈窗標題為 `Achievements · Title Wall (Unlocked 4/24)`、橫幅提示為 `Newly unlocked titles: Sword Against Claw、One Who Sees Through、Rabbit in the Morning Light、Promise of the Wooden Sword`、卡片名稱如 `Sword Against Claw`、`Guardbreaker`、`Windchaser`、`Last One Standing`、`I Bow to No Power` 等，解鎖條件均為英文句子，零 CJK 漢字殘留。
  - 日文全景中，漢字（実績・称号の壁、解放済み、未解放、広場へ戻る、剣もて爪を受く、看破せし者、構えを崩す者、風を追う者、岸に最後まで、我、強権を慕わず、朝光の中の兎、木剣の約束等）均核實回查語系檔，確認為日文常用漢字/新字體。
- [x] **0-QA25（彈窗以外同屏同步換語系）**：
  - 實機截圖中，背後大廳頂部 Header（Energy, Gold, Stardust / エネルギー, 金, 星屑）、左側四入口（Celestial Blacksmith, Craft Workshop, Martial Arena, Adventure Bounties / 天宮の鍛冶屋, 工芸工房, 演武競技, 冒険依頼）、底部 Dock（Cogwheel Hamlet, Hero Gear, Four Regions, Soul Hall, Adventure Bag / ぜんまい新村, キャラ装備, 四区出征, 聚魂殿, 冒険バッグ）均同步切換為該語系。
- [x] **零系統 Emoji**：所有稱號名、條件說明、按鈕與標籤皆 100% 零系統 emoji。
- [x] **解鎖規則與狀態不變**：解鎖旗標判定邏輯、條件計算全數維持不變。

## 5. 測試驗證記錄

```bash
# 1. 冒煙測試（無 SCRIPT ERROR）
godot --path game --headless --quit-after 3

# 2. 稱號目錄測試
godot --path game --headless -s res://scripts/systems/test_title_catalog.gd

# 3. 稱號選單測試
godot --path game --headless -s res://scripts/ui/test_title_menu.gd

# 4. 六語系稱號牆即時刷新單元測試（抽驗 4 個稱號名與條件）
godot --path game --headless -s res://scripts/ui/test_title_wall_i18n.gd
```
