# 雙快捷主線合併回歸驗收清單 (t_f9976639)

- [x] WardrobeDialog 前往鍛造快捷果凍按鈕 `BtnGoForge` (t_d2c83369)
- [x] ForgeDialog 前往衣櫥快捷果凍按鈕 `BtnGoWardrobe` (t_28157977)
- [x] MobileLobby 雙向直通連動與雙向閉環流轉 (鐵匠 -> 衣櫥 -> 鐵匠)
- [x] 六語系 (zh_TW, zh_CN, en, ja, ko, es) 鍵值對齊、零系統 Emoji、熱區 >= 48px
- [x] 實機截圖 5 張 SHA256 獨立完整存證於 proofs/t_f9976639/ 與 docs/proofs/t_f9976639/
- [x] 單元測試 test_wardrobe_forge_shortcut.gd PASS_OK
- [x] 單元測試 test_forge_dialog_wardrobe_shortcut.gd PASS_OK
- [x] 批次回歸測試 test_batch_dual_shortcuts_t_f9976639.gd PASS_OK
- [x] clock-check 規範檢查通過（素材皆有 .import，無軟連結，語系鍵對齊）
- [x] docs/PROJECTS.json 狀態推進為「已上線」
