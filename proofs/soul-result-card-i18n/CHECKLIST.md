# 《發條之心》抽魂結果卡掉落種類與名稱六語系 查驗清單與驗收報告 (t_33ac0c71)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_33ac0c71`（🎮 遊戲開發｜抽魂結果卡掉落種類與名稱六語系）
- **交付目錄**：`proofs/soul-result-card-i18n/`（0-QA23 獨立專屬目錄，絕無跨卡覆蓋）
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/soul-result-card-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名，非中文殘留。
  - `review.md 0-QA25`：查驗全景畫面背景與全屏 UI 語系狀態（同圖內標題、按鈕、狀態列皆連動切換至目標語言）。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 | MD5 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| 01 | `proof_01_result_card_en.png` | 抽魂結果卡零件展示（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) | `a32ada9c920da3811fdc56d2e5654baf` |
| 02 | `proof_02_result_card_ja.png` | 抽魂結果卡零件展示（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) | `092c766ef14c4287bba9be4b345bd045` |
| 03 | `proof_03_result_card_zh_TW.png` | 抽魂結果卡換裝展示（zh_TW 繁中全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 繁中 | 合格 (PASS) | `b662129932c95156fc02377d4c8271ff` |

---

## 二、 局部特寫 Crops 驗證清單（`proofs/soul-result-card-i18n/crops/`）

- `crop_01_result_card_en.png`：英文結果卡徽章 `Part`、提示 `Part logged in the codex!` 與明細 `【Part】 Brass Gear` 特寫（MD5: `9857b40a9b71f233a959756f49a6f911`）。
- `crop_02_result_card_ja.png`：日文結果卡徽章 `パーツ`、提示 `パーツ図鑑に入った！` 與明細 `【パーツ】 真鍮の歯車` 特寫（MD5: `97405287700dc156f6ee6dabe4e132a3`）。
- `crop_03_result_card_zh_TW.png`：繁中結果卡徽章 `換裝`、提示 `新貼紙皮！要換上嗎？` 與明細 `【換裝】 小白 · 奶油便服` 特寫（MD5: `4a84bae23fef04a365b40b1c5c4555dd`）。

---

## 三、 六語系詞條對齊表（種類 3 個 + 掉落名 8 個）

| 種類／掉落項 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|---|
| **種類 1** | 換裝 | 换装 | Outfit | 着せ替え | 의상 | Atuendo |
| **種類 2** | 零件 | 零件 | Part | パーツ | 부품 | Pieza |
| **種類 3** | 雜件 | 杂件 | Junk | ジャンク | 잡동사니 | Chatarra |
| **掉落 1** | 黃銅齒輪 | 黄铜齿轮 | Brass Gear | 真鍮の歯車 | 황동 톱니바퀴 | Engranaje de latón |
| **掉落 2** | 發條游絲 | 发条游丝 | Balance Spring | ヒゲゼンマイ | 태엽 헤어스프링 | Espiral de cuerda |
| **掉落 3** | 核心碎片 | 核心碎片 | Core Shard | コアの破片 | 코어 조각 | Fragmento de núcleo |
| **掉落 4** | 小白 · 奶油便服 | 小白 · 奶油便服 | Shiro · Cream Casual | 小白・クリーム普段着 | 시로 · 크림 일상복 | Blanco · Atuendo Crema |
| **掉落 5** | 獅 · 黃銅背心 | 狮 · 黄铜背心 | Lion · Brass Vest | 獅子・真鍮ベスト | 사자 · 황동 조끼 | León · Chaleco de latón |
| **掉落 6** | 狐 · 圍巾長衫 | 狐 · 围巾长衫 | Fox · Scarf Tunic | 狐・マフラー長羽織 | 여우 · 목도리 긴옷 | Zorro · Túnica con bufanda |
| **掉落 7** | 野豬 · 工匠工裙 | 野猪 · 工匠工裙 | Boar · Artisan Apron | 猪・職人エプロン | 멧돼지 · 장인 작업치마 | Jabalí · Delantal de artesano |
| **掉落 8** | 搪瓷碎屑 | 搪瓷碎屑 | Enamel Chips | エナメル片 | 에ナ멜 조각 | Fragmento de esmalte |

---

## 四、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：完全無 SCRIPT ERROR，編譯與加載 100% 正常。
2. **單元測試**：
   - 執行 `godot --path game --headless -s scripts/ui/test_soul_draw_i18n.gd`：
     - 抽魂主畫面六語系詞條解析通過。
     - View 節點 `locale_changed` 動態連動刷新通過。
     - **SoulResultCard 結果卡即時切換六語系**：全部 8 個掉落物、3 個種類在六語系下的徽章文字與明細文字切換全數通過（`TEST_SOUL_DRAW_I18N_OK`）。
3. **vision_analyze 審查結論**：
   - `proof_01_result_card_en.png`：徽章（`Part`）、提示（`Part logged in the codex!`）、明細（`【Part】 Brass Gear`）與頂部標題、按鈕全屏 100% 英文，符合 0-QA25，無截字破圖，零系統 emoji。
   - `proof_02_result_card_ja.png`：徽章（`パーツ`）、提示（`パーツ図鑑に入った！`）、明細（`【パーツ】 真鍮の歯車`）與全屏 UI 均為日文，漢字名詞遵守 0-QA24 規範，零系統 emoji。
   - `crop_01_result_card_en.png` 與 `crop_02_result_card_ja.png`：文字置中對齊，字體渲染正常無截字。
