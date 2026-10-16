# ForgeDialog 天宮鐵匠底欄新增『前往商城』快捷果凍按鈕驗收存證 (t_5d5f07fd)

## 任務目標
1. 在 `ForgeDialog`（`forge_dialog.gd`）底部操作按鈕列新增『前往商城』（`BtnGoShop`）暖橘色立體果凍按鈕。
2. 按鈕規格：熱區 115x50px（>= 48px 手遊防誤觸標準，高度 50px），多巴胺暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)，立體果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊連動：發射 `shop_requested` 與 `go_shop` 訊號並安全關閉天宮鐵匠（發射 `closed` 訊號、無遮罩殘留），連動大廳開啟 `ShopDialog` 商城視窗（`MobileLobby.open_shop()`）。
4. 雙向閉環：在 `ShopDialog` 點擊『前往鍛造』(`BtnGoForge`) 可順暢返回 `ForgeDialog`。
5. 提供 `get_go_shop_button() -> Button` 存取器與 `shop_requested` / `go_shop` 訊號。
6. 支援六語系 i18n 即時切換（zh_TW, zh_CN, en, ja, ko, es），新增 `forge.btn_go_shop` 鍵值：
   - 繁中：前往商城
   - 簡中：前往商城
   - en：To Shop
   - ja：ショップへ
   - ko：상점으로
   - es：A Tienda
7. 遵守 review.md 與 clock-review-checklist 規範，撰寫單元與整合測試 `test_forge_shop_shortcut.gd` 覆蓋按鈕樣式、點擊訊號、關閉無遮罩殘留、大廳連動開啟商城、雙向閉環返回鍛造與六語系即時切換。
8. 執行 `clock-check` 確保無警告，實機渲染截圖存證送審 sideqa。

---

## 審查常見退回自查表（對照 clock-review-checklist.md）

| 類別 | 檢查項目 | 自查狀態 | 說明 |
|---|---|---|---|
| **畫面與素材** | 實機截圖各語系與窄螢幕無穿模、溢出或遮擋 | ✅ 已檢查 | 實機截圖 1280x720 經 Vision 檢查，底欄 6 顆按鈕寬度與間距適當，文字完整無截斷、邊界留白充裕、零系統 Emoji。 |
| **畫面與素材** | 熱區 >= 48px、節點無坍塌、文字對比足夠 | ✅ 已檢查 | `BtnGoShop` 尺寸 115x50px（熱區高 50px >= 48px），文字採深藍紫 #1F1A3A 搭配暖橘底 #FFA010，厚底 5px，圓角 18px，對比清晰。 |
| **畫面與素材** | 無軟連結、素材無缺失 .import | ✅ 已檢查 | 跑 `clock-check` 確認 0 軟連結、0 缺 .import。 |
| **測試與證據** | 驗證截圖存證完整、連續截圖不重複 (SHA256 互異) | ✅ 已檢查 | 8 張截圖皆由 `xvfb-run` 實機渲染產生，SHA256 雜湊全部獨立唯一。 |
| **測試與證據** | 單元測試防 flaky、狀態重置、語系時序解耦 | ✅ 已檢查 | 測試初始化調用 `reset_new_game("rabbit")`，多語系切換時序等待 5~6 幀重繪，徹底消除時序錯位。 |
| **測試與證據** | 完整執行迴歸測試 | ✅ 已檢查 | `test_forge_shop_shortcut.gd` (PASS)、`test_forge_power_stat_shortcut.gd` (PASS)、`test_forge_i18n.gd` (PASS) 全數通過。 |
| **程式與邏輯** | 彈窗關閉徹底、無遮罩殘留 | ✅ 已檢查 | 點擊 `BtnGoShop` 發射 `shop_requested`、`go_shop` 與 `closed`，`queue_free()` 徹底釋放無殘留。 |
| **程式與邏輯** | 畫面跳轉與雙向連動 | ✅ 已檢查 | 天宮鐵匠點擊『前往商城』開啟商城視窗；商城點擊『前往鍛造』流暢返回天宮鐵匠，雙向閉環完備。 |
| **資料與文案** | 六語系翻譯對齊且零 CJK/零 Emoji | ✅ 已檢查 | 六語系字典齊全，英西語系零 CJK 殘留，全語系 100% 零 Emoji。 |
| **流程與交付** | PROJECTS.json 項目狀態更新 | ✅ 已檢查 | 已將 `forge-shop-shortcut` 更新為「測試中」。 |
| **流程與交付** | 檔案完整 commit、工作區 clean | ✅ 已檢查 | 所有修改與新增檔案完整 commit 至 `agent/20261016-forge-shop-shortcut-t_5d5f07fd` 分支。 |

---

## 實機渲染截圖存證清單 (1280x720)

| 序號 | 檔案名 | 內容描述 | 解析度 | SHA256 雜湊 |
|---|---|---|---|---|
| 01 | `proof_01_zh_TW_forge_dialog_btn_go_shop.png` | 繁中天宮鐵匠：底欄展示『前往商城』暖橘果凍厚底按鈕 (115x50px) | 1280x720 | `44cda052bc2eb11cc6a30a817ae83ed8e710c6294d558d49a27233d169cdaf0b` |
| 02 | `proof_02_click_btn_go_shop_opens_shop_dialog.png` | 點擊前往商城：鐵匠安全關閉，大廳連動開啟 ShopDialog 商城彈窗 | 1280x720 | `ebf02c2dcda715ff41b57084e584249b6361b69c910c73e70cc66bd255ad7216` |
| 03 | `proof_03_loop_back_to_forge.png` | 雙向閉環：在 ShopDialog 點擊『前往鍛造』成功返回 ForgeDialog | 1280x720 | `5e1a9ea1b6811738881d617269eda5d33efcbb4e82ac5967f04350e83c2d7123` |
| 04 | `proof_04_zh_CN_forge_dialog_btn_go_shop.png` | 簡中語系：按鈕文字『前往商城』 | 1280x720 | `818eb5f2bdf983b347df0ef7ce36e42fb11d976ad3191a386dbe4c8b13ff87e4` |
| 05 | `proof_05_en_forge_dialog_btn_go_shop.png` | 英文語系：按鈕文字 "To Shop"，文字排版居中留白充裕、零 CJK 殘留 | 1280x720 | `9d77b81d8eff886fb3005c65a0d95b6ed78a24960ac16e3c90c39e0692dd8fcf` |
| 06 | `proof_06_ja_forge_dialog_btn_go_shop.png` | 日文語系：按鈕文字 "ショップへ" | 1280x720 | `bc79d83541680ecb459736cbed330696e78d5365ee403613060f3c3f327ef929` |
| 07 | `proof_07_ko_forge_dialog_btn_go_shop.png` | 韓文語系：按鈕文字 "상점으로"，零 CJK 殘留 | 1280x720 | `c7db2e7f9613c40f5e972311161f5f93d78b967328cca7808ad34c01f94944c6` |
| 08 | `proof_08_es_forge_dialog_btn_go_shop.png` | 西文語系：按鈕文字 "A Tienda"，零 CJK 殘留 | 1280x720 | `cd76c6c306ee46156710ae4c660a5313baf932e579d90de1d366a69e3b792751` |

---

## 測試執行驗證記錄

```bash
# 1. 執行單元與整合測試及截圖存證
xvfb-run -a -s "-screen 0 1280x720x24" godot --audio-driver Dummy --path game -s scripts/ui/test_forge_shop_shortcut.gd
# 輸出：TEST_FORGE_SHOP_SHORTCUT_OK: 全部測試通過！

# 2. 執行無頭單元與整合測試
godot --audio-driver Dummy --headless --path game -s scripts/ui/test_forge_shop_shortcut.gd
# 輸出：TEST_FORGE_SHOP_SHORTCUT_OK: 全部測試通過！

# 3. 執行關聯快捷回歸測試
godot --headless --path game -s scripts/ui/test_forge_power_stat_shortcut.gd
# 輸出：TEST_FORGE_POWER_STAT_SHORTCUT_OK: 全部測試通過！

# 4. clock-check 自動檢查
clock-check /opt/side/bravesoul-game
# 輸出：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞
```
