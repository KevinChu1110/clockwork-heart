# 驗收證明 · SkillDialog 心法招式底欄新增『前往戰力』快捷果凍按鈕聯動 PowerStatDialog (t_d703bf0e)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》招式與技能體系彈窗（`SkillDialog`，`skill_dialog.gd`）底欄按鈕列（`BottomBar` / `bot_h`）新增『前往戰力』立體果凍按鈕（`BtnGoPowerStat`），打通心法升級/出招設定直通戰力屬性總覽（`PowerStatDialog`）的雙向閉環：
1. **按鈕規格與樣式**：
   - 位於底欄『前往木人樁試招』與『關閉』按鈕旁。
   - 金黃色盤 `#FFD028`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 160x50px（>= 48px 手機端防誤觸人體工學規範）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），零系統 Emoji。
2. **點擊聯動與安全關閉**：
   - 點擊後發射 `power_stat_requested` 訊號與 `closed` 訊號。
   - 安全關閉 `SkillDialog`（無遮罩殘留）。
   - 大廳連動開啟 `PowerStatDialog`（`MobileLobby.open_power_stat_dialog()`）。
   - 與 `PowerStatDialog` 內招式卡片的『前往心法』形成雙向閉環。
3. **存取器與訊號**：
   - 提供 `get_go_power_stat_button() -> Button` 存取器。
   - 提供 `power_stat_requested` 訊號。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`skill.btn_go_power_stat`（繁中：前往戰力，簡中：前往战力，en：Go to Stats，ja：戦力詳細へ，ko：전투력으로 이동，es：Ir a Estadísticas）。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **快捷按鈕整合測試** | `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_skill_power_stat_shortcut.gd` | 規格、樣式、訊號、大廳連動、雙向閉環、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **程式與素材合規檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | ✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞 | **PASS** |

---

## 3. 實機截圖存證清單 (OpenGL3 真實 Framebuffer 渲染)

所有實機截圖存放於 `proofs/t_d703bf0e/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_skill_dialog_bottom_bar.png`
   - SHA256: `fd738af625cbf7007558a6f704e4b6f97943b2c81edfc40ffc9d165fbbc3a888`
   - 說明：繁中語系 SkillDialog 底欄展示新增的金黃色立體果凍按鈕『前往戰力』。
2. `proof_02_zh_TW_power_stat_opened_from_skill.png`
   - SHA256: `b369e53e54ff6a2d19c1cc861408db61aa42ad7a5c16f07527d0dc4de8c5f653`
   - 說明：點擊『前往戰力』後安全關閉 SkillDialog 並直通開啟 PowerStatDialog 戰力屬性總覽。
3. `proof_03_en_skill_dialog_bottom_bar.png`
   - SHA256: `11c8d395d9178f0d0c10f296635d5614173e21b918bec8fc58a48d5031320ab0`
   - 說明：英文語系即時切換，按鈕正確顯示 `Go to Stats`，無文字溢出或截斷。
4. `proof_04_ja_skill_dialog_bottom_bar.png`
   - SHA256: `70167bdc63a65512ee804ebe65868789ba337353cdb0f32644b00b246d712212`
   - 說明：日文語系即時切換，按鈕正確顯示 `戦力詳細へ`。
5. `proof_05_ko_skill_dialog_bottom_bar.png`
   - SHA256: `57656cffb8c23ab5a7a505b7eaa36ed3cf8a68c2588a2c0565a89777f779af61`
   - 說明：韓文語系即時切換，按鈕正確顯示 `전투력으로 이동`。
6. `proof_06_es_skill_dialog_bottom_bar.png`
   - SHA256: `f5b6f6033d8ca690b08fae368162360526d4d177499a1650271ed79d690ccc7f`
   - 說明：西班牙文語系即時切換，按鈕正確顯示 `Ir a Estadísticas`。

---

## 4. 專案狀態更新
- `skill-power-stat-shortcut`：`開發中` → `測試中`（完成開發、自測與截圖存證，送審 sideqa）
