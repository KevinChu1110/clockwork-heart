# 《發條之心》EnergyLackDialog 能量不足彈窗新增『前往商城』果凍按鈕聯動 ShopDialog 驗收報告 (t_f25c0492)

- **關聯任務**：`t_f25c0492`（🎮 遊戲開發｜EnergyLackDialog 能量不足彈窗新增『前往商城』果凍按鈕聯動 ShopDialog）
- **實作者**：阿宏（`sideworker`）
- **審查者**：小婷（`sideqa`）
- **分支**：`agent/20261013-energy-lack-shop-shortcut-t_f25c0492`

---

## 1. 任務背景與驗收目標
在能量不足彈窗 `EnergyLackDialog`（`game/scripts/ui/energy_lack_dialog.gd`）操作按鈕區中，補齊商業化閉環導流：
1. **新增『前往商城』果凍按鈕（BtnGoShop）**：
   - 暖橘色 `#FFA010`，深藍紫描邊 `#1F1A3A`，厚底 5~6px（6px），圓角 18~24px（20px），按鈕高度 52px（>= 50px），熱區寬度 180px（>= 48px），字級 17px。
2. **操作按鈕區佈局規格**：
   - 與看廣告拿體力（`WatchAdBtn`，寬 300px）、稍後再來（`BackBtn`，寬 160px）並列居中排列，間距 12px，總寬 664px，在 750px 彈窗卡片（扣除左右 24px 邊距為 702px）內完美居中且無穿框或溢出。
3. **訊號發射與大廳連動跳轉**：
   - 點擊發射 `shop_requested` 訊號並支援 `open_shop()` 直通大廳商城彈窗（`ShopDialog`），平滑關閉能量不足彈窗，導流至商城選購『發條能量補給箱』。
4. **六語系支援**：
   - 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 即時動態切換，更新六語系 `ui.json` 與全域字典檔，歐美語系零 CJK 殘留，零系統 Emoji。
5. **實機驗證與存證**：
   - 通過 `test_energy_lack_shop_shortcut.gd` 自動化單元測試，印出 `TEST_ENERGY_LACK_SHOP_SHORTCUT_OK` 哨兵。
   - 通過 `test_energy_lack_i18n.gd` 六語系單元測試，印出 `TEST_ENERGY_LACK_I18N_OK` 哨兵。
   - 實機 OpenGL3 渲染存證至 `proofs/t_f25c0492/`，6 張截圖 SHA256 獨立不重複。
   - `clock-check` 審查零警告。

---

## 2. 實機存證截圖清單 (proofs/t_f25c0492/)

| 編號 | 存證檔案名 | 驗收項目與畫面說明 | 無破圖 | 零 Emoji | 零截字 | SHA256 前綴 | 判定 |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|
| 01 | `proof_01_energy_lack_dialog_three_buttons_zh_TW.png` | 繁中 (zh_TW) 能量不足彈窗操作區並列三顆果凍按鈕（`WatchAdBtn` 綠底、`BtnGoShop` 暖橘底、`BackBtn` 米黃底），規格完整置中 | ✓ | ✓ | ✓ | `24d0d2ce18d2` | **PASS** |
| 02 | `proof_02_energy_lack_btn_go_shop_en.png` | 英文語系 (en) 彈窗展示：按鈕文字為『Go to Shop』，標題為『Insufficient Energy』，零 CJK 殘留 | ✓ | ✓ | ✓ | `db15a91c6fb9` | **PASS** |
| 03 | `proof_03_energy_lack_btn_go_shop_ja.png` | 日文語系 (ja) 彈窗展示：按鈕文字為『ショップへ』，標題為『エネルギー不足』，排版工整無溢出 | ✓ | ✓ | ✓ | `50f9354a8c2a` | **PASS** |
| 04 | `proof_04_energy_lack_btn_go_shop_ko.png` | 韓文語系 (ko) 彈窗展示：按鈕文字為『상점으로』，標題為『에너지 부족』，排版工整無溢出 | ✓ | ✓ | ✓ | `f03e1562954b` | **PASS** |
| 05 | `proof_05_energy_lack_btn_go_shop_es.png` | 西文語系 (es) 彈窗展示：按鈕文字為『Ir a la tienda』，標題為『Energía insuficiente』，零 CJK 殘留 | ✓ | ✓ | ✓ | `1ac0416ba657` | **PASS** |
| 06 | `proof_06_click_btn_go_shop_opens_shop_dialog.png` | 點擊『前往商城』後發射 `shop_requested` 訊號，無縫開啟大廳商城彈窗 `ShopDialog`，並展示『發條能量補給箱』(NT$ 30) | ✓ | ✓ | ✓ | `1852f20326ec` | **PASS** |

---

## 3. 六語系字典對齊驗證

| 鍵值 / 按鈕 | 繁中 (zh_TW) | 簡中 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西文 (es) |
|---|---|---|---|---|---|---|
| **BtnGoShop** | 前往商城 | 前往商城 | Go to Shop | ショップへ | 상점으로 | Ir a la tienda |
| **TitleLbl** | 能量不足 | 能量不足 | Insufficient Energy | エネルギー不足 | 에너지 부족 | Energía insuficiente |
| **BackBtn** | 稍後再來 | 稍后再来 | Come Back Later | 後で来る | 나중에 오기 | Volver más tarde |

---

## 4. 自動化測試執行紀錄

| 測試腳本 / 指令 | 驗證項目 | 結果 | 報錯數 |
|---|---|:---:|:---:|
| `godot --path game --headless --quit-after 3` | 無頭引擎冒煙測試 | **PASS** | 0 SCRIPT ERROR |
| `godot --path game --headless -s res://scripts/ui/test_energy_lack_shop_shortcut.gd` | 專用單元測試（按鈕規格、果凍樣式、訊號發送、連動大廳商城、六語系、零 Emoji） | **PASS** | 0 SCRIPT ERROR |
| `godot --path game --headless -s res://scripts/ui/test_energy_lack_i18n.gd` | 原有六語系即時切換與廣告狀態迴歸測試 | **PASS** | 0 SCRIPT ERROR |
| `clock-check t_f25c0492` | 素材、路徑、語系 key、舊名詞自動審查工具 | **PASS** | 0 警告 |
| `xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/ui/test_energy_lack_shop_shortcut.gd` | 真實 OpenGL3 實機渲染存證截圖與 SHA256 驗證 | **PASS** | 6 獨立截圖 |
