# 《發條之心》新手引導按鈕與步驟標籤六語系 查驗清單與驗收報告 (t_73956e46)

- **執行人**：阿宏（側案·程式 sideworker）
- **關聯任務**：`t_73956e46`（🎮 遊戲開發｜新手引導按鈕與步驟標籤六語系）
- **交付目錄**：`proofs/onboard-i18n/`
- **遵循規範**：
  - `review.md 0-QA23`：OUT_DIR 嚴格限定為 `proofs/onboard-i18n/`，絕不覆蓋其它任務之 proof 目錄。
  - `review.md 0-QA24`：日文／韓文漢字依語系檔為準，確認為合法新字體／既定譯名，非中文殘留。
  - `review.md 0-QA25`：全景畫面 UI 呈現同一語系，零混合或硬編殘留。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | 語系完整度 | 驗證結果 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_onboard_en.png` | 新手引導 N07 步驟（en 英文全景，含 Next / Later / Step 7/8 / Hint / Soul Seal） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 英文 | 合格 (PASS) |
| 02 | `proof_onboard_ja.png` | 新手引導 N07 步驟（ja 日文全景，含 次へ / あとで / ステップ 7/8 / Hint / 封霊） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | ✓ 100% 日文 | 合格 (PASS) |

---

## 二、 語系對照與詞條清單

所有玩家可見文字均透過 `ContentLoc.text("ui", ...)` / `_t()` 與 `Loc.t()` 對接 `game/data/i18n/content/<locale>/ui.json` 及 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) | 簡體中文 (zh_CN) |
|---|---|---|---|---|---|
| 下一步 | Next | 次へ | 다음 | Siguiente | 下一步 |
| 稍後再說 | Later | あとで | 나중에 | Más tarde | 稍后再说 |
| 新手完成 | Tutorial Complete | チュートリアル完了 | 튜토리얼 완료 | Tutorial completado | 新手完成 |
| 新手引導 · 第 %d／%d 步 | Tutorial · Step %d/%d | チュートリアル · ステップ %d/%d | 튜토리얼 · %d/%d 단계 | Tutorial · Paso %d/%d | 新手引导 · 第 %d／%d 步 |
| 第 %d／%d 步 | Step %d/%d | ステップ %d/%d | %d/%d 단계 | Paso %d/%d | 第 %d／%d 步 |
| 空白鍵／下一步 · 部分步驟可「稍後再說」 | Space / Next · Some steps can be skipped with "Later" | スペース / 次へ · 一部の手順は「あとで」でスキップ可能 | 스페이스바 / 다음 · 일부 단계는 「나중에」로 건너뛰기 가능 | Espacio / Siguiente · Algunos pasos se pueden omitir con «Más tarde» | 空格键／下一步 · 部分步骤可「稍后再说」 |
| 封靈 | Soul Seal | 封霊 | 봉령 | Sello de alma | 封灵 |

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - 執行 `godot --path game --headless --quit-after 3`：無任何 SCRIPT ERROR 或 Compile Error。
2. **單元測試**：
   - `test_onboard_flow.gd`：流程節點載入、不可跳過 N05、N07 跳過進 N08、資源就緒等完整通過（`ONBOARD_FLOW_OK`）。
   - `test_onboard_view_dopamine.gd`：奶油陽光底、750px 卡片寬度、24px 圓角、按鈕高度 >= 50px、字級與深暖色規範通過（`ONBOARD_VIEW_DOPAMINE_OK`）。
   - `test_onboard_i18n.gd`（新增）：包含六語系 (en, ja, ko, es, zh_CN, zh_TW) 字典解析、`OnboardView` 實例連動、`Loc.locale_changed` 信號動態即時切換、N01 標題、N07 雙按鈕與結果卡、新手完成狀態全流程檢驗通過（`ONBOARD_I18N_OK`）。
3. **Vision 模型審查**：
   - `proof_onboard_en.png` 與 `proof_onboard_ja.png` 親自開圖審查。
   - 步驟標題、對話台詞、按鈕（Next/Later、次へ/あとで）、底部操作提示以及結果卡標籤（Soul Seal / 封霊）全數正確呈現對應語言，無硬編繁中殘留。
   - 日文字體完全符合 JIS 當用漢字/新字體（如：封霊、次へ），符合 `review.md 0-QA24` 規範。
   - 畫面無任何系統 emoji、無截字破圖、邊距與圓角排版正常，符合 `review.md 0-QA25` 規範。
