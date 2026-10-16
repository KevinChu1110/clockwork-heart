# EnergyLackDialog 能量不足彈窗新增『前往儲能庫』快捷果凍按鈕連動 ClockworkVaultDialog 驗收存證 (t_f267916e)

## 任務目標
1. 在 `EnergyLackDialog` (`game/scripts/ui/energy_lack_dialog.gd`) 能量不足彈窗底部操作按鈕列新增前往發條儲能庫果凍按鈕（`BtnGoVault`）。
2. 點擊後發射 `vault_requested` 與 `closed` 訊號並自動關閉彈窗 (`queue_free()`)，大廳 `MobileLobby` (`game/scripts/ui/mobile_lobby.gd`) 接到後平滑連動開啟 `ClockworkVaultDialog` 發條儲能庫放置收益彈窗。
3. 按鈕尺寸與視覺規範：
   - 位於 `btn_h` 底部按鈕列，與『觀看廣告回復能量』、『前往商城』、『前往戰力』、『稍後再來』五顆按鈕並列。
   - 按鈕高度 52px (>= 50px 手機端熱區)，熱區寬度 125px (>= 48px 手機端熱區)。
   - 多巴胺金黃色盤 (`COLOR_GOLD` `#FFD028`)，立體果凍厚底 6px，圓角 20px，深藍紫描邊 (`#1F1A3A`)，文字採深藍紫文字 `#1F1A3A` 帶高對比白色細描邊，100% 零系統 Emoji。
4. 提供存取器：`get_go_vault_btn()`, `get_btn_go_vault()`, `get_go_vault_button()`, `get_vault_button()`。
5. 支援六語系 i18n 即時刷新（`zh_TW`: 「前往儲能庫」, `zh_CN`: 「前往储能库」, `en`: 「To Vault」, `ja`: 「貯蔵庫へ」, `ko`: 「저장고로 이동」, `es`: 「Ir a Bóveda」），歐美語系零 CJK 殘留。
6. 撰寫單元與整合測試 `test_energy_lack_vault_shortcut.gd`，在非 headless (xvfb) 下產出實機截圖存證，執行 `clock-check` 確認無警告。
7. 使用 `project_status.py` 同步更新 `docs/PROJECTS.json` 狀態為「測試中」。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision Analyze 複驗，彈窗底部按鈕列五按鈕『看廣告』、『前往儲能庫』、『前往商城』、『前往戰力』、『稍後再來』並列間距均勻，文字完整無穿框，邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoVault` 尺寸 125x52px（寬 125px >= 48px，高 52px >= 50px 符合熱區規範），文字採深藍紫字 #1F1A3A 加白輪廓搭配多巴胺金黃底 #FFD028，立體厚底 6px，圓角 20px，高對比易讀。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 執行 `clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f267916e/bravesoul-game` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 6 張截圖皆由 `xvfb-run` 實機渲染產生，SHA256 雜湊全部獨立唯一（0 重複），經 Vision 驗證無黑屏、無遮擋殘留。 |
| **測試與證據** | 單元測試防 flaky、狀態重置 | ✅ 已檢查 | 測試初始化調用 `gs.reset_new_game("rabbit")`，等待幀數充分保留，無頭與實機測試皆穩定綠燈通過。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_energy_lack_vault_shortcut`、`test_energy_lack_i18n` 等相關測試全數跑綠。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoVault` 發射 `closed` 與 `vault_requested` 訊號並關閉 EnergyLackDialog 彈窗，大廳平滑連動開啟 `ClockworkVaultDialog`，無遮罩殘留。 |
| **程式與邏輯** | 畫面跳轉與連動順暢 | ✅ 已檢查 | 能量不足彈窗點擊『前往儲能庫』直達發條儲能庫放置收益彈窗，放置金幣與零件鐵屑收益狀態齊全，無卡死、無破圖。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系 ui.json 字典齊全（zh_TW: 前往儲能庫, zh_CN: 前往储能库, en: To Vault, ja: 貯蔵庫へ, ko: 저장고로 이동, es: Ir a Bóveda），英西語系零 CJK 殘留，全語系 100% 零系統 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | `energy-lack-vault-shortcut` 狀態更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與新增檔案已 commit 至 `agent/20261016-energy-lack-vault-shortcut-t_f267916e` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720 OpenGL3)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_energy_lack_five_buttons_zh_TW.png` | 繁中能量不足彈窗：底欄五按鈕並列，金黃果凍按鈕『前往儲能庫』(125x52px) 正常顯示 | 1280x720 | `f077f11c6ea5bdf6fd9ae74162a20c42bf9d0d7f238fcefc75abe4af5a3f7f3c` |
| 02 | `proof_02_energy_lack_btn_go_vault_en.png` | 英文語系切換刷新：\"To Vault\"，零 CJK 殘留 | 1280x720 | `07c7199e43b8727d843694a76db98ccba7e59f13d493f410304096058db4224a` |
| 03 | `proof_03_energy_lack_btn_go_vault_ja.png` | 日文語系切換刷新：『貯蔵庫へ』 | 1280x720 | `5a8c3b85629b1e924d20bbc14067c2c64a4409efd32c57e4649665a4b2d82579` |
| 04 | `proof_04_energy_lack_btn_go_vault_ko.png` | 韓文語系切換刷新：『저장고로 이동』 | 1280x720 | `bfefee72a9fe843990dbb9510d7843afa92a7c0c90e49746d050ada9146a5976` |
| 05 | `proof_05_energy_lack_btn_go_vault_es.png` | 西文語系切換刷新：\"Ir a Bóveda\"，零 CJK 殘留 | 1280x720 | `abf1075fe663c91fb6b02681115c53ece1c110db92b33e7f798d6acfb7218062` |
| 06 | `proof_06_click_btn_go_vault_opens_clockwork_vault_dialog.png` | 點擊前往儲能庫：直通開啟 ClockworkVaultDialog 放置收益彈窗，底層無遮罩殘留 | 1280x720 | `852034b536edcdc5a069e69a0e307fc669a218fccfb882c07c914979d1428942` |

---

## 測試執行驗證記錄

```bash
# 1. 自動檢查
clock-check /root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f267916e/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞

# 2. 功能單元測試
godot --path game --headless --script scripts/ui/test_energy_lack_vault_shortcut.gd
# 輸出：TEST_ENERGY_LACK_VAULT_SHORTCUT_OK (Exit 0)

# 3. 語系測試迴歸
godot --path game --headless --script scripts/ui/test_energy_lack_i18n.gd
# 輸出：TEST_ENERGY_LACK_I18N_OK (Exit 0)
```
