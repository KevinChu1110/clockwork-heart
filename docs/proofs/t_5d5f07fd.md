# ForgeDialog 天宮鐵匠底欄新增『前往商城』快捷果凍按鈕驗收存證 (t_5d5f07fd)

- 卡號：t_5d5f07fd
- 分支：`agent/20261016-forge-shop-shortcut-t_5d5f07fd`
- 執行者：sideworker2（阿翔）
- 審查者：sideqa（小婷）

## 實作內容
1. 在 `ForgeDialog`（`forge_dialog.gd`）底部操作按鈕列新增『前往商城』（`BtnGoShop`）暖橘色立體果凍按鈕。
2. 樣式規格：熱區 115x50px（>= 48px），暖橘色盤 #FFA010 (COLOR_ORANGE)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，文字深藍紫 #1F1A3A (COLOR_TEXT_DARK)，果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體，零系統 Emoji。
3. 點擊連動：點擊發射 `shop_requested` 與 `go_shop` 訊號並安全關閉天宮鐵匠（發射 `closed` 訊號、無遮罩殘留），連動大廳開啟 `ShopDialog` 商城視窗（`MobileLobby.open_shop()`）。
4. 雙向閉環：在 `ShopDialog` 點擊『前往鍛造』(`BtnGoForge`) 可順暢返回 `ForgeDialog`。
5. 存取器與訊號：提供 `get_go_shop_button() -> Button` 存取器與 `shop_requested` / `go_shop` 訊號。
6. 六語系支援：`forge.btn_go_shop`（繁中『前往商城』、簡中『前往商城』、en『To Shop』、ja『ショップへ』、ko『상점으로』、es『A Tienda』）。
7. 單元測試：撰寫 `test_forge_shop_shortcut.gd` 驗證按鈕規格、樣式、訊號、連動開啟商城、雙向閉環與六語系即時切換。

## 驗收證明
- 截圖目錄：`proofs/t_5d5f07fd/` 與 `docs/proofs/t_5d5f07fd/`（共 8 張 1280x720 實機截圖，SHA256 全部獨立唯一）。
- 自動檢查：`clock-check /opt/side/bravesoul-game` 結論為 `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。
- 測試執行：`test_forge_shop_shortcut.gd` 全數通過，SCRIPT ERROR = 0。
