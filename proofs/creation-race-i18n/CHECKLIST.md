# 創角種族卡與欄位標題六語系落地驗收清單 (creation-race-i18n)

卡號：t_61561279
執行人：阿翔（側案·工程師 sideworker2）
日期：2026-09-26

## 一、 驗收要求達成盤點

1. **種族顯示名各語系既有譯名補齊與對齊（遵守 0-QA24）：**
   - 13 大已上線種族在六語系（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`）下之譯名全數補齊至 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`。
   - 既有種族嚴格沿用 `ui.json` 既有 key：
     - `瓷韻熊貓` -> en: `The Porcelain Panda` / ja: `磁韻パンダ` / ko: `도운 판다` / es: `Panda de Porcelana`
     - `碧箸蛙` -> en: `The Spring-Leg Frog` / ja: `碧箸蛙` / ko: `벽저와` / es: `Rana de Resorte de Jade`
     - `鋼岳象` -> en: `The Colossus Elephant` / ja: `鋼岳象` / ko: `강악상` / es: `El Elefante Colosal`
     - `玄機龜` -> en: `The Xuanji Tortoise` / ja: `玄機龜` / ko: `현기귀` / es: `La Tortuga Xuanji`
   - 其他種族依據規格書 `paperdoll_slots.json` 既定英文名及日韓漢字標準譯名落定：
     - `白金兔` -> en: `Clockwork Rabbit` / ja: `白金兎` / ko: `백금토끼` / es: `Conejo de Platino`
     - `靈尾狐` -> en: `Astral Fox` / ja: `霊尾狐` / ko: `영미호` / es: `Zorro Astral`
     - `烈鬃獅` -> en: `Gilded Lion` / ja: `烈鬃獅子` / ko: `열기사자` / es: `León Dorado`
     - `鋼牙豕` -> en: `Forge Boar` / ja: `鋼牙猪` / ko: `강아저` / es: `Jabalí de la Forja`
     - `靈爪猴` -> en: `Spring Macaque` / ja: `霊爪猿` / ko: `영조원` / es: `Mono Resorte`
     - `烈焰虎` -> en: `The Ember Tiger` / ja: `烈焔虎` / ko: `열염호` / es: `El Tigre de Fuego`
     - `雲嵐鶴` -> en: `The Cloud Crane` / ja: `雲嵐鶴` / ko: `운람학` / es: `La Grulla de las Nubes`
     - `玄軸熊` -> en: `The Iron Bear` / ja: `玄軸熊` / ko: `현축웅` / es: `El Oso de Hierro`
     - `蒸氣企鵝` -> en: `The Steam Penguin` / ja: `蒸気ペンギン` / ko: `증기 펭귄` / es: `El Pingüino de Vapor`

2. **欄位標題與狀態列接入 Loc.t()，六語系補詞：**
   - 面板標題：`即時換裝控制項 · 模組槽位調配` (Live Outfit Controls · Modular Slot Tuning / リアルタイム着替え操作 · モジュールスロット調整 等)
   - 外裝服飾槽：`• 外裝服飾槽 (Costume Slot - Z:25)` (• Costume Slot (Costume Slot - Z:25) / • 衣装スロット (Costume Slot - Z:25) 等)
   - 軀體塗裝槽：`• 軀體塗裝槽 (Chassis Shell - Z:10)` (• Chassis Shell Slot (Chassis Shell - Z:10) / • 機体塗装スロット (Chassis Shell - Z:10) 等)
   - 手持武器槽：`• 手持武器槽 (Weapon Slot - Z:40)` (• Handheld Weapon Slot (Weapon Slot - Z:40) / • 手持ち武器スロット (Weapon Slot - Z:40) 等)
   - 狀態列格式字串：
     - `7 大槽位狀態：512 高清合成就緒 (渲染: %d/%d)` (7 Slot Status: 512 HD Composite Ready (Rendered: %d/%d) / 7スロット状態：512 HD合成完了 (描画: %d/%d) 等)
     - `7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)` (7 Slot Status: All %d Slots Ready (Loaded: %d/%d) / 7スロット状態：全 %d スロット準備完了 (読込: %d/%d) 等)
   - 操作按鈕：`重設預設`、`儲存驗證截圖`。

3. **切換語系後畫面上已在節點即時連動刷新（遵守 0-QA25）：**
   - `paperdoll_select_demo.gd` 中實作 `_update_right_panel_labels()`，並於 `_on_locale_changed` 完整更新右側所有欄位標題與狀態。
   - `_update_race_buttons_text()` 與 `_update_race_buttons_visual()` 均呼叫 `_t(...)`，選中切換種族卡高亮時文字不退回繁中。
   - 武器名稱欄位接入 `_t(...)`。

4. **翠角鹿防護守衛生效：**
   - 第十四族翠角鹿（fawn）未齊全套立繪資源，前端保持 `has_race_assets("fawn") == false` 防護，畫面上完全隱藏，不露出空卡。

5. **實機截圖存證（proofs/creation-race-i18n/，遵守 0-QA23）：**
   - 創角首發頁（Launch Tab 全景）：
     - `proof_creation_launch_zh_TW.png`
     - `proof_creation_launch_en.png`
     - `proof_creation_launch_ja.png`
   - 創角擴充頁（Expansion Tab 全景）：
     - `proof_creation_expansion_zh_TW.png`
     - `proof_creation_expansion_en.png`
     - `proof_creation_expansion_ja.png`
   - 顯微特寫 Crops（`crops/`）：
     - `crop_race_cards_launch_{zh_TW,en,ja}.png`
     - `crop_slots_panel_{zh_TW,en,ja}.png`
     - `crop_race_cards_expansion_{zh_TW,en,ja}.png`
   - 全數截圖與特寫經 MD5 檢驗 100% 獨立，嚴格存放於 `proofs/creation-race-i18n/`。

6. **親身視覺審查（Vision Check）與 QA Rework 修正（0-QA23）：**
   - en 全景：種族卡（Clockwork Rabbit, Astral Fox 等）、右側欄位（Costume Slot 等）、狀態列（7 Slot Status: 512 HD Ready）均為純淨英文，零破圖零截字零 emoji。
   - ja 全景：種族卡（白金兎、霊尾狐、烈鬃獅子 等）、右側欄位（衣装スロット 等）、狀態列（7スロット状態：512 HD合成完了）均為正確日文與漢字，合規 0-QA24。
   - 擴充分頁：8 族完整展示無橫向溢出，瓷韻熊貓 512 高清合成正確渲染，翠角鹿無空卡。
   - **【Attempt 2 修正項】：針對審查員 sideqa 提出長譯名溢出之要求**：
     - 為所有種族按鈕之 `NameLabel` 全面開啟智慧折行 `autowrap_mode = TextServer.AUTOWRAP_WORD_SMART`，並在 `.tscn` 靜態設置 `autowrap_mode = 3` 與 `size_flags_horizontal = 3`。
     - 實作字級動態調適 `_format_race_name_label`：長名（長度 > 10，如 `The Colossus Elephant`、`Clockwork Rabbit`）自動調節字級（12px）並安全折行收納於 136px 卡框內。
     - 按鈕內縮邊距加寬至 `margin_left = 10` / `margin_right = 10`，首發頁 `Clockwork Rabbit` 具備充裕舒適邊距，不再貼死兩側邊框。
     - 擴充頁長譯名（如 `The Colossus Elephant`）自然拆為雙行居中展示，與相鄰按鈕文字徹底歸零碰撞，絕無破圖或貫穿邊框。
     - 單元測試 `test_creation_race_i18n.gd` 加入 `autowrap_mode`、字級調適與邊距防護之斷言查核。

---

## 二、 驗收指令執行紀錄

- `godot --path game --headless --quit-after 3`：**0 SCRIPT ERROR**。
- `TEST_FILTER=creation ./tools/run_tests.sh`：**6/6 PASSED**（含新增之 `test_creation_race_i18n` autowrap 與邊距斷言）。
- `TEST_FILTER=i18n ./tools/run_tests.sh`：**5/5 PASSED**。
