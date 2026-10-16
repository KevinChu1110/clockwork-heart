# ClockworkVaultDialog 發條儲能庫放置收益彈窗底欄新增『前往商城』快捷果凍按鈕驗收存證 (t_fb74722c)

## 任務目標
1. 在 `ClockworkVaultDialog`（`clockwork_vault_dialog.gd`）底部操作按鈕列新增『前往商城』（`BtnGoShop`）暖橘色立體果凍按鈕。
2. 按鈕規格：熱區 105x52px（>= 48px 手遊防誤觸標準，高度 52px），多巴胺暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)，立體果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊連動：發射 `shop_requested` 與 `go_shop` 訊號並安全關閉發條儲能庫（發射 `closed` 訊號、無遮罩殘留），連動大廳開啟 `ShopDialog` 商城視窗（`MobileLobby.open_shop()`）。
4. 提供 `get_go_shop_button() -> Button` 與 `get_shop_button() -> Button` 存取器與 `shop_requested` / `go_shop` 訊號。
5. 支援六語系 i18n 即時切換（zh_TW, zh_CN, en, ja, ko, es），新增 `vault.btn_go_shop` 鍵值：
   - 繁中：前往商城
   - 簡中：前往商城
   - en：To Shop
   - ja：ショップへ
   - ko：상점으로
   - es：A Tienda
6. 遵守 review.md 與 clock-review-checklist 規範，撰寫單元與整合測試 `test_clockwork_vault_shop_shortcut.gd` 覆蓋按鈕樣式、點擊訊號、關閉無遮罩殘留、大廳連動開啟商城、多語系重開回到儲能庫與六語系即時切換。
7. 執行 `clock-check` 確保無警告，實機渲染截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經檢查，彈窗寬度適度拓寬至 820px，底欄 7 顆按鈕並列整齊，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoShop` 尺寸 105x52px（熱區高 52px >= 48px），文字採深藍紫 #1F1A3A 搭配暖橘底 #FFA010，厚底 5px，圓角 18px，對比清晰。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run` 實機渲染產生，SHA256 雜湊全部獨立唯一。 |
| **測試與證據** | 單元測試防 flaky、狀態重置、語系時序解耦 | ✅ 已檢查 | 測試初始化調用 `reset_new_game("rabbit")`，多語系切換時序等待 5~6 幀重繪，徹底消除時序錯位。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_clockwork_vault_shop_shortcut.gd` (PASS)、`test_clockwork_vault_windup_shortcut.gd` (PASS)、`test_clockwork_vault_inventory_shortcut.gd` (PASS)、`test_clockwork_vault_power_stat_shortcut.gd` (PASS)、`test_vault_forge_shortcut.gd` (PASS) 全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoShop` 發射 `shop_requested`、`go_shop` 與 `closed`，`queue_free()` 徹底釋放無殘留。 |
| **程式與邏輯** | 畫面跳轉與大廳連動 | ✅ 已檢查 | 發條儲能庫點擊『前往商城』安全關閉儲能庫並直通開啟大廳商城視窗，無遮罩殘留。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系 100% 零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已將 `vault-shop-shortcut` 更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與新增檔案完整 commit 至 `agent/20261016-clockwork-vault-shop-shortcut-t_fb74722c` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_clockwork_vault_dialog_btn_go_shop.png` | 繁中發條儲能庫：底欄展示『前往商城』暖橘果凍厚底按鈕 (105x52px) | 1280x720 | `d0ed3b4d4f06d9518d22c5b44c1705651b5dd46648dd575fc09709d24e33ccdd` |
| 02 | `proof_02_click_btn_go_shop_opens_shop_dialog.png` | 點擊前往商城：儲能庫安全關閉，大廳連動開啟 ShopDialog 商城彈窗 | 1280x720 | `045d61f865b0e4207f4107b6be050d5e00c2ee1ba7d73a5d0cbf0a8109862c8f` |
| 03 | `proof_03_loop_back_to_vault.png` | 關閉商城並重新開啟儲能庫：無遮罩殘留，進入多語系檢測階段 | 1280x720 | `66248f01261e57fb51350ce420070eda6b599a7cd53eb1706cdeb1ab9c00b3c1` |
| 04 | `proof_04_zh_CN_clockwork_vault_dialog_btn_go_shop.png` | 簡中語系：按鈕文字『前往商城』 | 1280x720 | `88640670d3526a4e047e8f3407dc5e8a049a613686ff6232a539462ec94fd60c` |
| 05 | `proof_05_en_clockwork_vault_dialog_btn_go_shop.png` | 英文語系：按鈕文字 "To Shop"，文字排版居中留白充裕、零 CJK 殘留 | 1280x720 | `a50ae299f568ab9ae2b8162aff093d108dc88357d17da453e368b171cbe9292d` |
| 06 | `proof_06_ja_clockwork_vault_dialog_btn_go_shop.png` | 日文語系：按鈕文字 "ショップへ" | 1280x720 | `5c026f28ad23587b7714d0b7e3f101483d915c852ff718c15fb0d1bd05787c91` |
| 07 | `proof_07_ko_clockwork_vault_dialog_btn_go_shop.png` | 韓文語系：按鈕文字 "상점으로"，零 CJK 殘留 | 1280x720 | `83c42e17d8aa9c45cab6adc7002e7ec68725fb51d28c867d8ab66c3df54f10a3` |
| 08 | `proof_08_es_clockwork_vault_dialog_btn_go_shop.png` | 西文語系：按鈕文字 "A Tienda"，零 CJK 殘留 | 1280x720 | `f54122c388c5a41f652b08d53fdaf8f1ecfbe9f7695cc28d6b45a7bee933a9fc` |

---

## 測試執行驗證記錄

```bash
# 1. 執行單元與整合測試及截圖存證
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_clockwork_vault_shop_shortcut.gd
# 輸出：TEST_CLOCKWORK_VAULT_SHOP_SHORTCUT_OK

# 2. 執行關聯快捷回歸測試
xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_clockwork_vault_windup_shortcut.gd
# 輸出：TEST_CLOCKWORK_VAULT_WINDUP_SHORTCUT_OK

xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_clockwork_vault_inventory_shortcut.gd
# 輸出：TEST_CLOCKWORK_VAULT_INVENTORY_SHORTCUT_OK

xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_clockwork_vault_power_stat_shortcut.gd
# 輸出：TEST_CLOCKWORK_VAULT_POWER_STAT_SHORTCUT_OK

xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_vault_forge_shortcut.gd
# 輸出：TEST_VAULT_FORGE_SHORTCUT_OK

# 3. clock-check 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞
```
