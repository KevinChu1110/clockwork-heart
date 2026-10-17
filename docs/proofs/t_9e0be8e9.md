# 大廳聚魂殿堂新增『前往商城』快捷果凍按鈕驗收證明 (t_9e0be8e9)

- **卡號**：`t_9e0be8e9`
- **分支**：`agent/20261017-soul-hall-shop-shortcut-t_9e0be8e9`
- **實作內容**：在大廳聚魂殿堂（`mobile_lobby.gd` 之 `_build_soul_hall_tab`）底欄新增『前往商城』（`BtnGoShop`）暖橘色立體果凍按鈕（140x52px），點擊直通調用 `open_shop()` 開啟 `ShopDialog` 商城彈窗，與商城彈窗底欄的『前往聚魂』形成完整雙向閉環。
- **UI 規範落實**：多巴胺暖橘色盤 #FFA010、深藍紫描邊與文字 #1F1A3A、圓角 18px、底厚 5px、熱區 52px（>= 48px）、開源粉圓體 16px、100% 零系統 Emoji。
- **六語系支援**：`soul_hall.btn_go_shop` 完整登錄至繁中、簡中、英文、日文、韓文、西文。

## 實機截圖存證清單 (1280x720 OpenGL3)

| 序號 | 截圖檔案 | 說明 | SHA256 雜湊 |
|---|---|---|---|
| 01 | `proof_01_zh_TW_soul_hall_btn_go_shop.png` | 繁中聚魂殿底欄展示『前往商城』果凍按鈕 (140x52px) | `1a29e9adc82596c65b9ed934633c93bf90eaff59f1b936ac582ff53101f72a23` |
| 02 | `proof_02_zh_TW_shop_dialog_opened.png` | 點擊前往商城：直通開啟 ShopDialog 道具商城彈窗 | `5036d37a2a1e2cca9edbb379c9d385c3fc83eb5f5451254892231c6d62490f35` |
| 03 | `proof_03_zh_TW_loop_back_to_soul_hall.png` | 雙向閉環：從商城點擊『前往聚魂』安全返回聚魂殿堂 | `09c8ed543274e1df0e10b8d8898bc99e5fb0568332d10aa629016f14b918dda5` |
| 04 | `proof_04_zh_CN_soul_hall_shop_btn.png` | 簡中語系按鈕呈現「前往商城」 | `1ab4925dcbb18de7917b756d9b48276c67b177a2c1253ab23f1e20e21d9643f3` |
| 05 | `proof_05_en_soul_hall_shop_btn.png` | 英文語系按鈕呈現 "To Shop"，零 CJK 殘留 | `8fb7918a561da95dd137b50a494379811cbf8b0f4bf1687b5e76228b52c2636e` |
| 06 | `proof_06_ja_soul_hall_shop_btn.png` | 日文語系按鈕呈現「ショップへ」 | `6dd85e876e9bf329130f1482daf259dbef7007063dc27bbdc2d84bd3f6817838` |
| 07 | `proof_07_ko_soul_hall_shop_btn.png` | 韓文語系按鈕呈現「상점으로」 | `b384b9016321f1a0e41e7f35cb4f03c31c297dcf3bbc8149b525fcf3b0bd2f6f` |
| 08 | `proof_08_es_soul_hall_shop_btn.png` | 西文語系按鈕呈現 "A Tienda"，零 CJK 殘留 | `d566b9a5865671a1896e27f1b78cc008a0144b10cf73678fd6b6047b40b84be6` |

## 驗證結果
- `clock-check t_9e0be8e9`：✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞
- `test_soul_hall_shop_shortcut.gd`：PASS（TEST_SOUL_HALL_SHOP_SHORTCUT_OK）
- 迴歸測試（`test_soul_hall_power_stat_shortcut`、`test_soul_hall_inventory_shortcut`、`test_soul_hall_unequip_all`、`test_shop_shortcuts`）：全數 PASS
- 無頭冒煙測試：0 SCRIPT ERROR
