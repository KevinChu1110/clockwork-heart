# 《發條之心》WeaponSwapDialog 底欄新增『前往背包』快捷果凍按鈕查驗清單與驗收報告 (t_41078db9)

- **任務編號**：`t_41078db9`
- **任務名稱**：🎮 遊戲開發｜WeaponSwapDialog 武器更換彈窗底欄新增『前往背包』快捷果凍按鈕聯動 MapleInventory
- **執行人**：阿翔 (sideworker2)
- **驗證方式**：真實 OpenGL3 Framebuffer 渲染擷取 (`xvfb-run -a godot --rendering-driver opengl3`)

---

## 驗收項目清單

| 項目 | 規範要求 | 實作與測試現況 | 結論 |
|---|---|---|---|
| **按鈕存在性與命名** | WeaponSwapDialog 底欄操作列新增 `BtnGoInventory` 按鈕節點，提供 `get_go_inventory_button()` 存取器 | 底欄成功新增 `BtnGoInventory`，並提供相應存取器，熱區高寬合規 | **合格 (PASS)** |
| **手遊人體工學與樣式** | 按鈕熱區高度 >= 48px，寬度 >= 100px；多巴胺薄荷綠 (#4ED86A) 立體果凍厚底 5px、圓角 16px、100% 零 Emoji | `custom_minimum_size = Vector2(115, 48)`，`border_width_bottom = 5`，開源粉圓體字級 14px，無 Emoji | **合格 (PASS)** |
| **訊號發射與平滑關閉** | 點擊發射 `inventory_requested` 與 `go_inventory`，觸發 `closed` 並呼叫 `queue_free()` 安全關閉 | 訊號發射與關閉事件驗證通過，無殘留遮罩 | **合格 (PASS)** |
| **大廳無縫連動** | `MobileLobby` 接收訊號並調用 `open_maple_inventory()` 開啟探索背包彈窗 | 連動順暢，正確開啟 `MapleInventory` 節點 | **合格 (PASS)** |
| **六語系在地化** | 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換，外語無中文殘留 | 六語系對齊完整，無任何中文殘留 | **合格 (PASS)** |
| **實機截圖存證** | 真實 Framebuffer 產出 4 張存證，SHA256 皆獨立不重複 | 4 張截圖存證完畢，雜湊比對通過 | **合格 (PASS)** |

---

## 截圖存證清單

| 編號 | 檔案名稱 | 內容說明 | 狀態檢查 | SHA256 前綴 |
|---|---|---|---|---|
| 01 | `proof_01_weapon_swap_dialog_btn_go_inventory.png` | WeaponSwapDialog 武器更換彈窗底欄顯示『前往背包』果凍按鈕 | 零Emoji / 零破圖 / 零截字 | 5e2b362dfd88 |
| 02 | `proof_02_maple_inventory_dialog_opened.png` | 點擊『前往背包』關閉更換彈窗並連動開啟 MapleInventory 探索背包 | 零Emoji / 零破圖 / 零截字 | 30282462afd1 |
| 03 | `proof_03_weapon_swap_inventory_en.png` | 英文語系 (en) 下顯示 "Go to Inventory" | 零Emoji / 零破圖 / 零中文殘留 | c2de9af676e4 |
| 04 | `proof_04_weapon_swap_inventory_ja.png` | 日文語系 (ja) 下顯示 "インベントリへ進む" | 零Emoji / 零破圖 / 零截字 | d4d5c4e9e5dd |
