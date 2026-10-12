# 探索背包消耗品即時使用效果結算與恢復浮動提示驗收清單 (t_3bb0fb3b)

## 驗收重點
1. **多巴胺按鈕規格與樣式**：
   - 薄荷綠果凍厚底按鈕 (COLOR_MINT #4ED86A, 深藍紫描邊 #1F1A3A, 2px border, 5px bottom border)
   - 按鈕熱區高度 52px (>= 48px)，圓角 18px，粉圓體字級 18px (>= 16px)
   - 零系統原生 Emoji

2. **消耗品即時使用結算閉環**：
   - 選取消耗品 (hp_s 微光潤滑油 x3) 並點擊『使用』
   - 數量正確扣除 1 (變為 2)，玩家 HP 即時恢復 +25 (20 -> 45)
   - 右側詳情面板即時刷新為 '×2'

3. **多巴胺恢復浮動提示 (ConsumableFloatingToast)**：
   - 彈出 ConsumableFloatingToast 浮動面板與 '+25 HP' 飄字
   - 綠色多巴胺高對比字體 #1E7538、18px 圓角、4px 果凍厚底
   - 播放使用音效，動效流暢無需退出背包

4. **生命已滿安全防護 (防無效浪費)**：
   - 角色生命已滿 (HP 50/50) 時，恢復類消耗品 (hp_s) 按鈕適應性置灰 (disabled=true)
   - 按鈕文案切換為『生命已滿』，阻擋使用並防扣數量
   - 非恢復類消耗品 (dust_crumb 星屑碎) 滿血不受限制，依然可使用

5. **六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態在地化**：
   - zh_TW: 生命已滿 / 使用
   - zh_CN: 生命已满 / 使用
   - en: HP Full / Use
   - ja: HP満タン / 使う
   - ko: HP 가득 참 / 사용
   - es: Salud llena / Usar

## 實機截圖存證清單
- `proof_01_consumable_selected_damaged_hp_ready_zh_tw.png`: 受傷狀態選取 hp_s，按鈕『使用』薄荷綠厚底啟用
- `proof_02_consumable_use_floating_toast_heal_green.png`: 點擊使用，彈出多巴胺「+25 HP」綠色浮動飄字與詳情更新
- `proof_03_consumable_selected_full_hp_disabled_zh_tw.png`: 滿血狀態選取 hp_s，按鈕適應性置灰顯示『生命已滿』
- `proof_04_consumable_non_heal_dust_crumb_usable.png`: 星屑碎非恢復消耗品，滿血仍可使用
- `proof_05_consumable_full_hp_en.png`: 英文語系 HP Full
- `proof_06_consumable_full_hp_ja.png`: 日文語系 HP満タン
- `proof_07_consumable_full_hp_ko.png`: 韓文語系 HP 가득 참
- `proof_08_consumable_full_hp_es.png`: 西班牙文語系 Salud llena
