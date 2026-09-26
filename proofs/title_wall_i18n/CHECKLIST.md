# 稱號牆標題按鈕與解鎖狀態六語系驗收清單 (t_4326fa9d)

依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25

## 交付內容
1. `game/scripts/ui/title_wall_dialog.gd`：
   - 接入 `Loc.locale_changed` 動態信號監聽
   - 標題（成就 · 稱號牆）、計數（（已解鎖 %d／%d））、新解鎖提示（新解鎖稱號：%s）、返回按鈕（返回標題）、堡壘按鈕（堡壘）全走 `ContentLoc.text("ui", ...)`
   - 稱號卡片解鎖狀態標籤（已解鎖／未解鎖）動態連動，不丟失解鎖狀態
   - 保留手遊多巴胺果凍厚底規範，無系統 emoji，無 AI 腔
2. `game/data/i18n/content/{zh_TW, zh_CN, en, ja, ko, es}/ui.json`：
   - 補齊六語系詞條（成就 · 稱號牆、已解鎖、未解鎖、（已解鎖 %d／%d）、返回標題、回到廣場、堡壘、新解鎖稱號：%s）
3. 具名單元測試 `game/scripts/ui/test_title_wall_i18n.gd`：
   - 驗證六語系詞條字典比對
   - 實例化 TitleWallDialog 進行六語系動態切換（locale_changed）即時刷新驗證
   - 驗證無系統 emoji
4. 實機全景截圖（0-QA23 專屬目錄 `proofs/title_wall_i18n/`）：
   - `proof_title_wall_en.png` (英文全景)
   - `proof_title_wall_ja.png` (日文全景)
   - `proof_title_wall_zh_tw.png` (繁中全景)

## 驗收自檢
- [x] godot headless 冒煙測試無 SCRIPT ERROR
- [x] TEST_FILTER=title_wall_i18n 測試綠燈 (TEST_TITLE_WALL_I18N_OK)
- [x] TEST_FILTER=title_menu 測試綠燈 (TITLE_MENU_OK)
- [x] check_player_text.py 綠燈 (PLAYER_TEXT_OK)
- [x] vision 實機截圖檢核通過，無破圖、無溢出截斷、無 emoji
- [x] 遵守 0-QA23：OUT_DIR 指向獨立目錄 proofs/title_wall_i18n/，無覆蓋他人截圖
