# 大廳戳碰氣泡與聚魂完畢提示六語系 (lobby-poke-toast-i18n) 交付查核清單

依據 `references/review.md` 規範（0-QA15, 0-QA23, 0-QA24, 0-QA25）：

## 一、0-QA23 查 OUT_DIR 獨立性
- 本次截圖輸出目錄嚴格設定為 `proofs/lobby-poke-toast-i18n/`。
- 完全未覆蓋、動到或干擾其他任務的 proof 資料夾。

## 二、0-QA15 截圖 MD5 唯一性與規格
所有實機截圖解析度均為 1280x720，MD5 100% 獨立不重複：
1. `proof_poke_en.png` (d4dfda5d925024baecde09c4d9fd8d83) - 1280x720，大廳點擊主角氣泡英文全景
2. `proof_poke_ja.png` (2a4fad9af34e591e66eeaebf2fffe228) - 1280x720，大廳點擊主角氣泡日文全景
3. `proof_poke_zh_TW.png` (4728a835ac2ad00d6c3d42e03aefccac) - 1280x720，大廳點擊主角氣泡繁中全景
4. `proof_toast_en.png` (cb1e67d1d345f7851d967aa91678f31a) - 1280x720，聚魂殿完成提示英文全景
5. `proof_toast_ja.png` (52ed0b2120c33329ee380fd11217e4a7) - 1280x720，聚魂殿完成提示日文全景
6. `proof_toast_zh_TW.png` (5c193dc678151e0237d7754cdbcd4e6f) - 1280x720，聚魂殿完成提示繁中全景

## 三、0-QA24 語系詞彙與非中文漢字查核
- 遵循詞庫既定用語，日文「聚魂完了」「戦魂の欠片」及英文「Soul gathering complete! Received Soul Shards and Soul EXP!」經回查 `ui.json`，對齊全域翻譯。
- 零系統 emoji（無任何 ⚔、✨、🔥 等業餘 emoji）。

## 四、0-QA25 彈窗／氣泡外全景同步切換查核
- 實機截圖與視覺檢查確認：在切換至 `en` 與 `ja` 時，大廳背景頂部狀態列（能量／金幣／星屑／商城／設置）、四大殿堂按鈕、紙娃娃外觀裝備槽位標籤、右下出征看板與底部五大分頁按鈕均同步切換為對應語言，無任何殘留繁中。
- 當氣泡在畫面上時切換語系，監聽 `locale_changed` 並即時調用 `_update_speech_bubble_text()` 更新當前句台詞。

## 五、輸入與修改對照表（什麼輸入 → 修正什麼）
1. **大廳點擊主角氣泡台詞**：
   - 輸入：五句寫死繁中台詞（看我的旋風斬～喝！／背後的發條上得剛剛好，出發吧！／聽見神殿齒輪的轉動聲了嗎？／神殿的以太核心正在共鳴……／隨時準備好去挑戰大首領！）
   - 修正：改走 `ContentLoc.text("ui", HERO_SPEECH_KEYS[_current_speech_index])`，在六語系字典擴充對應譯文；監聽 `locale_changed`，氣泡開著切換語系時即時動態刷新文字與字型大小（en/es 適配 13px 防止換行溢出）。
2. **聚魂完畢 Toast 提示**：
   - 輸入：`_show_toast("聚魂完畢！獲得了戰魂碎片與戰魂經驗！")` 寫死繁中。
   - 修正：改為 `_show_toast(_t("聚魂完畢！獲得了戰魂碎片與戰魂經驗！"))`，六語系字典補齊對應譯文。
3. **封靈罐初次建立卡片 CostLabel**：
   - 輸入：`cl.text = "金幣 %d" % int(gd["cost"])` 寫死繁中。
   - 修正：改為 `cl.text = "%s %d" % [_t("金幣"), int(gd["cost"])]`，與刷新路徑 `_refresh_gourds_ui` 保持一致，避免初次生成露出繁中再被覆蓋。

## 六、自動化單元測試
- 建立專屬單元測試：`game/scripts/ui/test_lobby_poke_toast_i18n.gd`
- 執行指令：`TEST_FILTER=test_lobby_poke_toast_i18n ./tools/run_tests.sh`
- 結果：全部通過（LOBBY_POKE_TOAST_I18N_OK，exit code 0）。
