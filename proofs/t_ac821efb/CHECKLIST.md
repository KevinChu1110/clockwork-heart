# 衣櫥前往背包與背包前往衣櫥雙快捷按鈕合併回歸驗收存證 (t_ac821efb)

## 1. 驗收標準檢驗
- [x] 雙分支乾淨合併至 main 主線，解決 i18n 字典與 PROJECTS.json 衝突
- [x] `WardrobeDialog` 底欄新增『前往背包』果凍按鈕（`BtnGoInventory`，暖橘色 `#FFA010`，尺寸 105x50px >= 48px）
- [x] `MapleInventory` 底欄新增『前往衣櫥』果凍按鈕（`BtnGoWardrobe`，暖橘色 `#FFA010`，尺寸 120x48px >= 48px）
- [x] 100% 零系統 Emoji，使用粉圓體 (Open-Huninn) 與立體厚底 5px 描邊設計
- [x] 點擊 WardrobeDialog 前往背包直通開啟 MapleInventory 並安全關閉衣櫥彈窗
- [x] 點擊 MapleInventory 前往衣櫥直通開啟 WardrobeDialog 並安全關閉背包視窗（雙向閉環互通）
- [x] 支援六語系 i18n 即時切換：繁中、簡中、en、ja、ko、es，字典 12 處全數齊全
- [x] 無頭引擎冒煙測試（exit 0）、相關單元測試（PASS）與雙快捷合併回歸測試（PASS）全綠

## 2. 實機截圖存證清單
- `proof_01_wardrobe_dialog_with_btn_go_inventory.png`: SHA256 `74dae0b81222cf6b1b2fcb6855ed80cbaa4718b2c5e3366e691372a9722da887`
- `proof_02_wardrobe_click_go_inventory_opens_maple_inventory.png`: SHA256 `833e477e7ab778b7bc69aa328b48f8e8570c89bb3bed51a808d191f20732ce69`
- `proof_03_maple_inventory_with_btn_go_wardrobe.png`: SHA256 `4109d15e86be6215ed89faf2109c62af1929cfc4e24c5497f428a934bdfeb42f`
- `proof_04_inventory_click_go_wardrobe_opens_wardrobe_dialog.png`: SHA256 `9d4be712334a26da68abd71f4259d749d013546f61adeae0debd0496ab48ce08`
- `proof_05_wardrobe_inventory_locale_ja.png`: SHA256 `2fdb8562db12168f8fea2b94781369c8a72652bc6367b4e0897deb79ff057dcf`
- `proof_06_inventory_wardrobe_locale_en.png`: SHA256 `b9b5bb968719025e1af379fcd94f7d1c92577b9a944cc23e6a476ad7f9cb6120`
