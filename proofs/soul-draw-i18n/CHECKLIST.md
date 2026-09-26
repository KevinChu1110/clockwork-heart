# 《發條之心》聚魂殿抽魂畫面標題按鈕票數六語系 查驗清單與驗收報告 (t_f73d9f45)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_f73d9f45`（🎮 遊戲開發｜聚魂殿抽魂畫面標題按鈕票數六語系）
- **交付目錄**：`proofs/soul-draw-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/soul-draw-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名，非中文殘留。
  - `review.md 0-QA25`：查驗全景畫面背景語系狀態，並記錄於驗收說明中。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_soul_draw_en.png` | 抽魂主畫面（en 英文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_soul_draw_ja.png` | 抽魂主畫面（ja 日文全景） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |

---

## 二、 局部特寫 Crops 驗證清單（`proofs/soul-draw-i18n/crops/`）

- `crop_header_en.png` / `crop_header_ja.png`：抽魂主標題與票數列即時切換特寫。
- `crop_buttons_en.png` / `crop_buttons_ja.png`：主按鈕（Wind Up — Draw 1 / 巻き上げ——一回引く）與次按鈕（To the Toy-pile Edge / 玩具の山の縁へ）特寫。

---

## 三、 六語系詞條對齊表

| 項目 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|---|
| 主標題 | 抽魂 · 封靈罐 | 抽魂 · 封灵罐 | Soul Draw · Soul Canister | 抽魂 · 封霊缶 | 추혼 · 봉령캔 | Extracción de Almas · Recipiente de Almas |
| 抽一格按鈕 | 上緊——抽一格 | 上紧——抽一格 | Wind Up — Draw 1 | 巻き上げ——一回引く | 태엽 감기——1칸 뽑기 | Dar Cuerda — Extraer 1 |
| 次按鈕 | 去玩具堆邊緣 | 去玩具堆边缘 | To the Toy-pile Edge | 玩具の山の縁へ | 장난감 더미 가장자리로 | Ir a la orilla del montón |
| 票數資訊格式 | 封靈票 ×%d · 今日已抽 %d | 封灵票 ×%d · 今日已抽 %d | Soul Tickets ×%d · Pulled Today: %d | 封霊券 ×%d · 本日抽選 %d | 봉령 티켓 ×%d · 오늘 뽑기 %d | Boletos de Alma ×%d · Extraídas Hoy: %d |
| 票數不足提示 | 封靈票不足 | 封灵票不足 | Not enough Soul Tickets | 封霊券が不足しています | 봉령 티켓 부족 | Boletos de alma insuficientes |

---

## 四、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR，編譯與加載完全正常。
2. **單元測試**：
   - `test_soul_draw_v2.gd`：既有抽魂隨機池與保底邏輯通過（SOUL_DRAW_V2_OK）。
   - `test_soul_draw_i18n.gd`：六語系字典解析、動態切換 `Loc.locale_changed` 即時刷新連動測試通過（TEST_SOUL_DRAW_I18N_OK）。
3. **vision_analyze 審查結論**：
   - `proof_soul_draw_en.png`：標題（Soul Draw · Soul Canister）、票數狀態（Soul Tickets ×3 · Pulled Today: 0）、抽一格按鈕（Wind Up — Draw 1）、去玩具堆邊緣按鈕（To the Toy-pile Edge）均正確顯示為英文，排版工整無截字破圖，零系統 emoji。
   - `proof_soul_draw_ja.png`：標題（抽魂 · 封霊缶）、票數狀態（封霊券 ×3 · 本日抽選 0）、抽一格按鈕（巻き上げ——一回引く）、去玩具堆邊緣按鈕（玩具の山の縁へ）均正確顯示為日文，漢字名詞遵守 0-QA24 規範，零系統 emoji。
   - 0-QA25 背景狀態備註：soul_draw_play_view 本身設計為全屏視圖（UiStyle.TATA_CARD_BG 溫潤奶油全屏底板），底板覆蓋 1280x720，大廳未外露。內層結果卡既有 `tr_key` 邏輯依照任務要求「結果卡既有 tr_key 的不要重做」維持原樣。
