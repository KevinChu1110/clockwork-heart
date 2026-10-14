# GemWorkshopDialog 手藝工坊新增『前往戰力』快捷果凍按鈕驗收存證 (t_69e139d8)

## 任務目標
1. 在 `GemWorkshopDialog`（`gem_workshop_dialog.gd`）底部操作按鈕列，在既有『前往鍛造』與『前往背包』按鈕旁新增『前往戰力』（`BtnGoPowerStat`）天藍色立體果凍按鈕。
2. 按鈕規格：熱區 140x50px（>= 48px），天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A，果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊連動：發射 `power_stat_requested` 訊號並安全關閉手藝工坊（無遮罩殘留），連動大廳開啟 `PowerStatDialog`（`MobileLobby.open_power_stat_dialog()`），與戰力總覽的『前往工坊』形成完整雙向閉環。
4. 提供 `get_go_power_stat_button()` 存取器與 `power_stat_requested` 訊號。
5. 支援六語系 i18n 即時切換（zh_TW, zh_CN, en, ja, ko, es），新增 `gem_workshop.btn_go_power_stat` 鍵值：
   - 繁中：前往戰力
   - 簡中：前往战力
   - en：Go to Stats
   - ja：戦力詳細へ
   - ko：전투력으로 이동
   - es：Ir a Estadísticas
6. 遵守 review.md 規範，撰寫單元與整合測試 `test_gem_workshop_power_stat_shortcut.gd` 覆蓋按鈕樣式、點擊訊號、關閉無遮罩殘留、六語系即時切換。
7. 執行 `clock-check` 確保無警告，非 headless 截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，按鈕文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoPowerStat` 尺寸 140x50px（熱區 >= 48px），文字採深藍紫 #1F1A3A 搭配天藍色底 #38A0FF，對比清晰。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run opengl3` 實機渲染產生，SHA256 雜湊全部獨立唯一。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game()`，時序等待幀數控制在 5~6 幀，穩定綠燈。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_gem_workshop_power_stat_shortcut`、`test_gem_workshop_go_inventory`、`test_title_wall_power_stat_shortcut`、`test_skill_power_stat_shortcut`、`test_power_stat_shortcuts` 全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoPowerStat` 發射 `power_stat_requested` 與 `closed`，`queue_free()` 徹底釋放無殘留。 |
| **程式與邏輯** | 畫面跳轉與雙向閉環 | ✅ 已檢查 | 手藝工坊點擊『前往戰力』開啟戰力總覽；戰力總覽點擊『前往工坊』返回手藝工坊，閉環流暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已新增 `gem-workshop-power-stat-shortcut` 並更新狀態為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有檔案已 commit 至 `agent/20261014-gem-workshop-power-stat-shortcut-t_69e139d8` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_gem_workshop_btn_go_power_stat_zh_TW.png` | 繁中熔煉分頁：展示『前往戰力』天藍果凍厚底按鈕 (140x50px) | 1280x720 | `4f9248504854b3a9c584a095e2a2ef7c659e9cc21d953122cec318cd647d0283` |
| 02 | `proof_02_gem_workshop_case_tab_zh_TW.png` | 繁中寶石櫃分頁：確認按鈕常駐顯示可見 | 1280x720 | `f7b8eb8ccb52cdcc4fac4c29cd3e9ca58a89440c81cc46ebc9dfff92a70534f1` |
| 03 | `proof_03_lobby_power_stat_dialog_opened.png` | 點擊前往戰力：工坊安全關閉，大廳開啟 PowerStatDialog 戰力總覽 | 1280x720 | `46c88c1c395d60fe1e0be5ee1ff1a69b65168f139d40a3c7d35f5d26430b792b` |
| 04 | `proof_04_gem_workshop_btn_go_power_stat_en.png` | 英文語系：按鈕文字 "Go to Stats"，零 CJK 殘留 | 1280x720 | `c62ccfa529e5435c19b8109d78c62ca0b4689ca5a8c681aacdd2dd1242d8bcae` |
| 05 | `proof_05_gem_workshop_btn_go_power_stat_ja.png` | 日文語系：按鈕文字 "戦力詳細へ" | 1280x720 | `cd0295b99b3b4f8a34f1745f262e70c867c1f60d412bd156b027a6686efabf73` |
| 06 | `proof_06_gem_workshop_btn_go_power_stat_ko.png` | 韓文語系：按鈕文字 "전투력으로 이동" | 1280x720 | `573e66e537add1577ca2490fcd4f744a3a828ad27e7a0ec4d06fe7b9de153c6a` |
| 07 | `proof_07_gem_workshop_btn_go_power_stat_es.png` | 西文語系：按鈕文字 "Ir a Estadísticas"，零 CJK 殘留 | 1280x720 | `8ef6839bea0868f65e93c133baf9f8fd833ce37c4479c653454a8523f3685888` |
| 08 | `proof_08_power_stat_back_to_gem_workshop.png` | 雙向閉環：從戰力總覽點擊『前往工坊』返回手藝工坊 | 1280x720 | `f43cee4e55160f48fa22d442d69aaa79c98e7fc7fe26d5a120bad2ad05a3eaeb` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 無頭冒煙測試
godot --path game --headless --quit-after 3
# 輸出：Exit 0

# 3. 功能單元與整合測試
godot --path game --headless -s scripts/ui/test_gem_workshop_power_stat_shortcut.gd
# 輸出：TEST_GEM_WORKSHOP_POWER_STAT_SHORTCUT_OK (Exit 0)

# 4. 關聯單元與雙向迴歸測試
godot --path game --headless -s scripts/ui/test_gem_workshop_go_inventory.gd
godot --path game --headless -s scripts/ui/test_title_wall_power_stat_shortcut.gd
godot --path game --headless -s scripts/ui/test_skill_power_stat_shortcut.gd
godot --path game --headless -s scripts/ui/test_power_stat_shortcuts.gd
# 輸出：全數 PASS (Exit 0)

# 5. 實機渲染截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_gem_workshop_power_stat_shortcut.gd
# 輸出：8 張獨立唯一截圖成功產出，雜湊無碰撞
```
