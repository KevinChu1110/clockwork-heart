# 《發條之心》BattleDefeatDialog 底欄新增『前往背包』快捷果凍按鈕查驗清單與驗收報告 (t_0bfa03fb)

- **任務編號**：`t_0bfa03fb`
- **任務名稱**：🎮 遊戲開發｜BattleDefeatDialog 戰敗結算新增『前往背包』快捷果凍按鈕連動 MapleInventory
- **執行人**：阿翔 (sideworker2)
- **驗證方式**：真實 OpenGL3 Framebuffer 渲染擷取 (`xvfb-run -a godot --rendering-driver opengl3`)

---

## 驗收項目清單

| 項目 | 規範要求 | 實作與測試現況 | 結論 |
|---|---|---|:---:|
| **按鈕存在性與命名** | BattleDefeatDialog 底欄操作列新增 `BtnGoInventory` 按鈕節點，提供 `get_go_inventory_button()` 存取器 | 底欄成功新增 `BtnGoInventory`，緊鄰『前往戰力』(BtnGoPowerStat)，提供存取器 | **合格 (PASS)** |
| **手遊人體工學與樣式** | 按鈕熱區高度 >= 48px (52px)，寬度 130~150px；天藍色盤 (#38A0FF) 立體果凍厚底 6px、圓角 18~20px、100% 零 Emoji | `custom_minimum_size = Vector2(130, 52)`，`border_width_bottom = 6`，圓角 20px，開源粉圓體字級 17px，無 Emoji | **合格 (PASS)** |
| **訊號發射與平滑關閉** | 點擊發射 `inventory_requested` 與 `go_inventory`，觸發回調並呼叫 `queue_free()` 安全關閉 | 訊號發射與關閉事件驗證通過，無殘留遮罩、無卡死 | **合格 (PASS)** |
| **背包無縫連動** | 連動調用 `open_maple_inventory()` 開啟探索背包彈窗，與關卡勝利結算對稱形成完整閉環 | 連動順暢，正確調起 `MapleInventory` 探索背包節點 | **合格 (PASS)** |
| **六語系在地化** | 支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換，外語無 CJK 中文殘留 | 六語系對齊完整，無任何中文殘留，無文字折行穿框 | **合格 (PASS)** |
| **實機截圖存證** | 真實 Framebuffer 產出 6 張存證，SHA256 皆獨立不重複 | 6 張截圖存證完畢，雜湊比對通過 | **合格 (PASS)** |

---

## 截圖存證清單

| 編號 | 檔案名稱 | 內容說明 | 狀態檢查 | SHA256 前綴 |
|---|---|---|---|---|
| 01 | `proof_01_battle_defeat_dialog_btn_go_inventory_zh_TW.png` | 繁中語系下戰敗結算底欄顯示『前往背包』果凍按鈕 | 零Emoji / 零破圖 / 零截字 | `0e48934dd2f3` |
| 02 | `proof_02_battle_defeat_dialog_en.png` | 英文語系 (en) 下顯示 "Go to Inventory" | 零Emoji / 零破圖 / 零中文殘留 | `2431c935c943` |
| 03 | `proof_03_battle_defeat_dialog_ja.png` | 日文語系 (ja) 下顯示 "インベントリへ進む" | 零Emoji / 零破圖 / 零截字 | `cad5ab6ec5be` |
| 04 | `proof_04_battle_defeat_dialog_ko.png` | 韓文語系 (ko) 下顯示 "인벤토리로 이동" | 零Emoji / 零破圖 / 零截字 | `ac9a1f1b3b82` |
| 05 | `proof_05_battle_defeat_dialog_es.png` | 西文語系 (es) 下顯示 "Ir al Inventario" | 零Emoji / 零破圖 / 零中文殘留 | `2e88227b72e5` |
| 06 | `proof_06_click_btn_go_inventory_opens_maple_inventory.png` | 點擊『前往背包』關閉戰敗彈窗並連動調起 MapleInventory 探索背包 | 零Emoji / 零破圖 / 零遮罩殘留 | `6e2053d02411` |
