# GemWorkshopDialog 手藝工坊新增『前往商城』快捷果凍按鈕驗收存證 (t_db6b3973)

## 任務目標
1. 在 `GemWorkshopDialog`（`gem_workshop_dialog.gd`）底部操作按鈕列新增『前往商城』（`BtnGoShop`）暖橘色立體果凍按鈕。
2. 按鈕規格：熱區 130x50px（>= 48px），暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)，立體果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊連動：發射 `shop_requested` 與 `go_shop` 訊號並安全關閉手藝工坊（發射 `closed` 訊號、無遮罩殘留），連動大廳開啟 `ShopDialog` 商城視窗（`MobileLobby.open_shop()`）。
4. 提供 `get_go_shop_button()` 存取器與 `shop_requested` / `go_shop` 訊號。
5. 支援六語系 i18n 即時切換（zh_TW, zh_CN, en, ja, ko, es），新增 `gem_workshop.btn_go_shop` 鍵值：
   - 繁中：前往商城
   - 簡中：前往商城
   - en：To Shop
   - ja：ショップへ
   - ko：상점으로
   - es：A Tienda
6. 遵守 review.md 0-UI1、0-QA26、0-QA28 規範，撰寫單元與整合測試 `test_gem_workshop_shop_shortcut.gd` 覆蓋按鈕樣式、點擊訊號、關閉無遮罩殘留、六語系即時切換（等待 6 幀解耦重繪避免時序錯位）。
7. 執行 `clock-check` 確保無警告，實機渲染截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經檢驗，底欄 5 顆按鈕寬度與間距適當，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoShop` 尺寸 130x50px（熱區高 50px >= 48px），文字採深藍紫 #1F1A3A 搭配暖橘底 #FFA010，厚底 5px，圓角 18px，對比清晰。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run` 實機渲染產生，SHA256 雜湊全部獨立唯一。 |
| **測試與證據** | 單元測試防 flaky、狀態重置、語系時序解耦 | ✅ 已檢查 | 測試初始化先調用 `gs.reset_new_game()`，多語系切換時序等待 6 幀重繪，徹底消除時序錯位。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_gem_workshop_shop_shortcut`、`test_gem_workshop_power_stat_shortcut`、`test_gem_workshop`、`test_gem_workshop_i18n`、`test_wardrobe_shop_shortcut` 全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoShop` 發射 `shop_requested`、`go_shop` 與 `closed`，`queue_free()` 徹底釋放無殘留。 |
| **程式與邏輯** | 畫面跳轉與連動 | ✅ 已檢查 | 手藝工坊點擊『前往商城』開啟商城視窗；大廳正確監聽連動，跳轉流暢。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已新增 `workshop-shop-shortcut` 並更新狀態為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與新增檔案完整 commit 至 `agent/20261016-gem-workshop-shop-shortcut-t_db6b3973` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_gem_workshop_btn_go_shop_zh_TW.png` | 繁中熔煉分頁：展示『前往商城』暖橘果凍厚底按鈕 (130x50px) | 1280x720 | `6059e02d7db2c06f1b8eb0e059e13f8e56b800a6c4f00ea41e188fe701b93fab` |
| 02 | `proof_02_gem_workshop_case_tab_zh_TW.png` | 繁中寶石櫃分頁：確認『前往商城』按鈕常駐顯示可見 | 1280x720 | `21dc9f92d3f86bdbbc357fb495a823da2318896917458d4752ccb05eceb0e324` |
| 03 | `proof_03_click_btn_go_shop_opens_shop_dialog.png` | 點擊前往商城：工坊安全關閉，大廳連動開啟 ShopDialog 商城彈窗 | 1280x720 | `c8183a128b95e41a059d1a44c1d50c5e4d3a7dfbcbebbef9648fbf85886b7ada` |
| 04 | `proof_04_gem_workshop_btn_go_shop_zh_CN.png` | 簡中語系：按鈕文字『前往商城』 | 1280x720 | `dbb8d7eed9352f11feba65664bac296dc261244d20c67a3c4a3bd1c1f330d503` |
| 05 | `proof_05_gem_workshop_btn_go_shop_en.png` | 英文語系：按鈕文字 \"To Shop\"，零 CJK 殘留 | 1280x720 | `80c38db3568fc9c2ce261ae746138379486f70ce036c0644f86146b7c6afa7a8` |
| 06 | `proof_06_gem_workshop_btn_go_shop_ja.png` | 日文語系：按鈕文字 \"ショップへ\" | 1280x720 | `611a00d44b2cef1492668dffdbe095082f044ca88bd238a5db360a1a9e32c76b` |
| 07 | `proof_07_gem_workshop_btn_go_shop_ko.png` | 韓文語系：按鈕文字 \"상점으로\"，零 CJK 殘留 | 1280x720 | `6ea8f2c50201608cb9a43ddaa3c84c59a072940c2ac9d437992daf1e5a5e3b9e` |
| 08 | `proof_08_gem_workshop_btn_go_shop_es.png` | 西文語系：按鈕文字 \"A Tienda\"，零 CJK 殘留 | 1280x720 | `13274480197eb8c0de5df88362fcd03c5f1e895d72c72f3abc2105c01bf13cee` |

---

## 測試執行驗證記錄

```bash
# 1. 執行單元與整合測試及截圖存證
xvfb-run -a godot --path game --script res://scripts/ui/test_gem_workshop_shop_shortcut.gd
# 輸出：TEST_GEM_WORKSHOP_SHOP_SHORTCUT_OK

# 2. 執行回歸測試
godot --path game --headless --script res://scripts/ui/test_gem_workshop.gd
# 輸出：TEST_GEM_WORKSHOP_OK

godot --path game --headless --script res://scripts/ui/test_gem_workshop_power_stat_shortcut.gd
# 輸出：TEST_GEM_WORKSHOP_POWER_STAT_SHORTCUT_OK

godot --path game --headless --script res://scripts/ui/test_gem_workshop_i18n.gd
# 輸出：TEST_GEM_WORKSHOP_I18N_OK

# 3. clock-check 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞
```
