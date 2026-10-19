# 大廳聚魂殿堂新增『前往心法』快捷果凍按鈕驗收存證 (t_cb73d5ff)

## 任務目標
1. 在 `mobile_lobby.gd` 的聚魂殿堂分頁（`_build_soul_hall_tab`）底部操作列 (`bot_h`)，新增『前往心法』（`BtnGoSkill`）天藍色立體果凍按鈕。
2. 按鈕規格：熱區 140x52px（>= 50px 高度，>= 48px 寬度），多巴胺天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，100% 零系統 Emoji、零特殊字元圖示。
3. 點擊聯動：播放 UI 音效，發射 `skill_requested` 訊號並調用 `open_skill_dialog()` 直通 SkillDialog 心法彈窗，與心法彈窗底部的『前往聚魂』形成完整雙向閉環。
4. 提供 `get_soul_hall_go_skill_btn()`、`get_btn_soul_go_skill()`、`get_soul_hall_skill_btn()` 存取器。
5. 支援六語系 i18n 即時切換（`zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es`），新增 `soul_hall.btn_go_skill` 鍵值：
   - 繁中：前往心法
   - 簡中：前往心法
   - en：To Skills
   - ja：心法へ
   - ko：심법으로
   - es：A Habilidades
6. 遵守 review.md 規範，撰寫單元與整合測試 `test_soul_hall_skill_shortcut.gd` 覆蓋樣式、點擊聯動、六語系即時切換。
7. 執行 `clock-check` 確保無警告，非 headless (OpenGL3) 截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，底欄按鈕排版間距合理無穿模，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoSkill` 尺寸 140x52px（熱區 >= 50px 高度，>= 48px 寬度），文字採深藍紫 #1F1A3A 搭配天藍底 #38A0FF，對比清晰立體。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複）。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game()`，時序等待幀數控制在 5~6 幀，無頭與視窗模式皆穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_soul_hall_skill_shortcut`、`test_skill_dialog_soul_hall_shortcut`、`test_soul_hall_shop_shortcut`、`test_soul_hall_inventory_shortcut`、`test_soul_hall_power_stat_shortcut`、`test_soul_hall_unequip_all`、`test_shop_shortcuts` 等測試全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoSkill` 發射訊號並開啟 `SkillDialog`，心法彈窗點擊『前往聚魂』安全關閉釋放無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與雙向閉環 | ✅ 已檢查 | 聚魂殿底欄點擊『前往心法』開啟心法彈窗；心法彈窗點擊『前往聚魂』切換回聚魂殿，雙向閉環完整順暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已更新 `soul-hall-skill-shortcut` 狀態為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與新增檔案完整 commit 到 `agent/20261019-soul-hall-skill-shortcut-t_cb73d5ff` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_soul_hall_btn_go_skill.png` | 繁中聚魂殿分頁：底欄展示天藍色立體果凍按鈕『前往心法』(140x52px) | 1280x720 | `b3627f01eddb55321ef25178ae9b7dd6a62f3e465d297453446162e26ca5cbf7` |
| 02 | `proof_02_zh_TW_skill_dialog_opened.png` | 點擊前往心法：連動開啟 SkillDialog 心法招式彈窗，底部展示『前往聚魂』按鈕 | 1280x720 | `0e429507d8f2d9623e047cd7a12ed5cd4ac33de209e02c54d1aec5467ce03112` |
| 03 | `proof_03_zh_TW_loop_back_to_soul_hall.png` | 雙向閉環：從心法彈窗點擊『前往聚魂』安全關閉心法彈窗返回聚魂殿堂 | 1280x720 | `0622a7badad5d830eaace673d3d4fb513bdd04ff107fc4d134e1d03d95170ca3` |
| 04 | `proof_04_zh_CN_soul_hall_skill_btn.png` | 簡中 (zh_CN) 即時切換：按鈕文字「前往心法」，零 Emoji | 1280x720 | `6dced41c37df6fbeb3b7d075574a76bcfe6e2d0039437f6b698d7d1c8070f4d5` |
| 05 | `proof_05_en_soul_hall_skill_btn.png` | 英文 (en) 即時切換：按鈕文字 "To Skills"，零 CJK 殘留 | 1280x720 | `9d3f89a0e1004c370c07f56ae21422ac508ed6e3ee4811b99b719fd5ed7c677a` |
| 06 | `proof_06_ja_soul_hall_skill_btn.png` | 日文 (ja) 即時切換：按鈕文字「心法へ」 | 1280x720 | `1f2074c9ca5ef8e92d05bf630dad0bcd7b40ca5bf359d25d436e3037f6144d59` |
| 07 | `proof_07_ko_soul_hall_skill_btn.png` | 韓文 (ko) 即時切換：按鈕文字「심법으로」 | 1280x720 | `9df53ac3c946f81ff85f4b3d4c8eb162ae4cdd259ccf397e82a32184349bf659` |
| 08 | `proof_08_es_soul_hall_skill_btn.png` | 西文 (es) 即時切換：按鈕文字 "A Habilidades"，零 CJK 殘留 | 1280x720 | `369e60f20224868c3537fd938edf21f08f72b271b7e7b8202b94fa887c3bdc52` |
