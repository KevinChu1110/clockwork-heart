# 驗收證明 · 大廳聚魂殿堂底欄新增『前往戰力』快捷果凍按鈕聯動 PowerStatDialog (t_deb8486e)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》大廳聚魂殿堂分頁（`mobile_lobby.gd`，`_build_soul_hall_tab()`）底欄按鈕列，在既有一鍵吸收、一鍵配置、一鍵卸下、前往背包旁，新增『前往戰力』（`BtnGoPowerStat`）金黃色立體果凍按鈕，打通聚魂殿堂直通戰力屬性總覽（`PowerStatDialog`）的雙向閉環：
1. **按鈕規格與樣式**：
   - 位於底部操作按鈕列，在前往背包旁。
   - 金黃色盤 `#FFD028`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 140x52px（>= 50px 手機端防誤觸人體工學規範）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），零系統 Emoji。
2. **點擊聯動與雙向閉環**：
   - 點擊後調用 `open_power_stat_dialog()` 直通戰力屬性總覽。
   - 戰力總覽（`PowerStatDialog`）點擊『前往聚魂』（`BtnGoSoul`）可安全關閉總覽並返回聚魂殿堂，形成完整雙向閉環。
3. **存取器**：
   - 提供 `get_soul_hall_go_power_stat_btn() -> Button` 存取器（以及相容別名 `get_btn_soul_go_power_stat()`）。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`soul_hall.btn_go_power_stat`（繁中：前往戰力，簡中：前往战力，en：Go to Stats，ja：戦力詳細へ，ko：전투력으로 이동，es：Ir a Estadísticas）。
5. **合規與自動化測試**：
   - 遵守 review.md 規範，撰寫單元與整合測試 `test_soul_hall_power_stat_shortcut.gd` 覆蓋樣式、點擊聯動、六語系即時切換。
   - 執行 `clock-check` 確保零警告，OpenGL3 真實渲染截圖存證完備。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **快捷按鈕整合測試** | `xvfb-run -a godot --path game --rendering-driver opengl3 --audio-driver Dummy -s res://scripts/ui/test_soul_hall_power_stat_shortcut.gd` | 規格、樣式、大廳連動、雙向閉環、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **聚魂殿一鍵卸下迴歸測試** | `godot --path game --headless -s res://scripts/ui/test_soul_hall_unequip_all.gd` | 0 SCRIPT ERROR，全語系與雙向操作全部通過 (exit 0) | **PASS** |
| **戰力屬性快捷迴歸測試** | `godot --path game --headless -s res://scripts/ui/test_power_stat_shortcuts.gd` | 0 SCRIPT ERROR，快捷按鈕與大廳連動全部通過 (exit 0) | **PASS** |
| **程式與素材合規檢查** | `clock-check t_deb8486e` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 實機截圖存證清單 (OpenGL3 真實 Framebuffer 渲染)

所有實機截圖存放於 `proofs/t_deb8486e/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_soul_hall_btn_go_power_stat.png`
   - SHA256: `972a4cef06d452a6ee0a62a6a0aa6f881abf4729815a6f3d065098ea87785800`
   - 說明：繁中語系聚魂殿堂分頁底欄展示金黃色立體果凍按鈕『前往戰力』(140x52px)。
2. `proof_02_zh_TW_power_stat_dialog_opened.png`
   - SHA256: `3f0807a42530e4b752aee1a6bec216b22fc138a52edfc2ff5fc79c01a8430308`
   - 說明：點擊『前往戰力』後直通開啟 PowerStatDialog 戰力屬性總覽彈窗。
3. `proof_03_zh_TW_loop_back_to_soul_hall.png`
   - SHA256: `0c64a28f7589b5e085625b9ad4f4a381a064c8e783e24adbc2b309ffa81b5db8`
   - 說明：從戰力屬性總覽點擊『前往聚魂』安全關閉總覽並返回聚魂殿堂，形成完整雙向閉環。
4. `proof_04_zh_CN_soul_hall_power_stat_btn.png`
   - SHA256: `e4363be215882a4536d505260cf5b41db54999af53346a78f787f5de47f47122`
   - 說明：簡中語系即時切換，按鈕正確顯示「前往战力」，零 Emoji。
5. `proof_05_en_soul_hall_power_stat_btn.png`
   - SHA256: `6fab5a9516b1da645ed2ccaf2981a968c06d4e03465db893f4c3e96a2aec9a8b`
   - 說明：英文語系即時切換，按鈕正確顯示 "Go to Stats"，零 CJK 殘留。
6. `proof_06_ja_soul_hall_power_stat_btn.png`
   - SHA256: `6027aaf8492a020506dfbcdf39a2289fad6ff04cef240f2eea88bf0063553601`
   - 說明：日文語系即時切換，按鈕正確顯示「戦力詳細へ」。
7. `proof_07_ko_soul_hall_power_stat_btn.png`
   - SHA256: `9abb04e2dd3440d1ead46ffbe8104d61e1bb9bf39a468cc1153e6ce1c23a731b`
   - 說明：韓文語系即時切換，按鈕正確顯示「전투력으로 이동」。
8. `proof_08_es_soul_hall_power_stat_btn.png`
   - SHA256: `d584dead476b0b734a8874aa7cc4ffcf76b76deeb50492bcb6fc4bb90d5335d6`
   - 說明：西文語系即時切換，按鈕正確顯示 "Ir a Estadísticas"，零 CJK 殘留。

---

## 4. 專案狀態更新
- `soul-hall-power-stat-shortcut`：`開發中` → `測試中`（完成開發、自測與截圖存證，送審 sideqa）
