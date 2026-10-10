# 《發條之心》背包Tab裝備詳情顯示已鑲寶石並於拆解時安全返還驗收報告 (t_2d2436f1)

- **執行工程師**：阿翔（發條之心·工程師 sideworker2）
- **關聯任務**：`t_2d2436f1`（🎮 遊戲開發｜背包Tab裝備詳情顯示已鑲寶石並於拆解時安全返還）
- **交付存證目錄**：`proofs/t_2d2436f1/`
- **遵循規範**：
  - `review.md` 人因人機工程與多巴胺視覺規範：按鈕高度 >= 52px、立體果凍厚底 5px、圓角 18px、零 Emoji、多巴胺鮮亮高對比色盤（紅 #C2185B、黃 #9A6B00、藍 #1565C0，淺底對比度 > 4.5:1）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異，存證對齊驗收項目與完整互動過程。
    - 詳情面板文字包含完整寶石名稱、星級與屬性加成，避免資訊隱蔽。
    - 裝備拆解（EquipmentSystem.dismantle）完整將鑲嵌寶石返還 GemSystem，防吞寶石。
    - 拆解 Toast 明確提示『返還寶石』。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_bag_weapon_with_gem_selected_zh_TW.png` | `MobileLobby` 背包Tab：選中帶紅寶石之武器【晨光長劍】時，類型顯示為「類型：武器（已鑲寶石）」，詳情面板以高對比色碼清晰顯示「已鑲寶石：紅寶石 · 1 星（凡） · 暴擊 +2.0」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `c3857541e642` | 合格 (PASS) |
| 02 | `proof_02_bag_weapon_without_gem_selected.png` | `MobileLobby` 背包Tab：選中無寶石之普通武器【生鏽鐵劍】時，類型為「類型：武器」，詳情面板不顯示寶石標籤，排版正常無空白溢出 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `2295d426ee1e` | 合格 (PASS) |
| 03 | `proof_03_bag_weapon_with_yellow_gem_en.png` | 英文語系 (en) 背包Tab：選中帶黃寶石之武器【Dawn Blade】時，類型顯示 \"Type: Weapon (Socketed)\"，詳情顯示 \"Socketed Gem: Topaz · 3 Star (Rare) · Attack % +12.0%\"，全英文無 CJK 殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `b6a27b4b0ab4` | 合格 (PASS) |
| 04 | `proof_04_bag_dismantle_toast_refund_gem.png` | 點擊「拆解回收」帶寶石之晨光長劍後，成功呼叫 `EquipmentSystem.dismantle(uid)`，彈出 Toast 提示「拆解【晨光長劍】：獲得鐵屑 ×7、金幣 +100、返還寶石【紅寶石 · 1 級】」 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `955d0304c286` | 合格 (PASS) |
| 05 | `proof_05_gem_safe_in_gem_workshop.png` | 開啟手藝工坊寶石彈窗（GemWorkshopDialog），清楚看見拆解返還之紅寶石安全進駐寶石背包，紅寶石「1階:1」精確入帳且無黑屏破圖 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `7d4b07a5a9b6` | 合格 (PASS) |

- **防作弊與真實性校驗**：5 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），並經 Vision 逐張視覺複檢通過。
- **視覺複檢**：所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **已鑲寶石：** | 已镶宝石： | Socketed Gem:  | 装着宝石： | 장착 보석:  | Gema engarzada:  |
| **已鑲寶石：%s · %d 星（%s） · %s %s** | 已镶宝石：%s · %d 星（%s） · %s %s | Socketed Gem: %s · %d Star (%s) · %s %s | 装着宝石：%s · %d 星（%s） · %s %s | 장착 보석: %s · %d성(%s) · %s %s | Gema engarzada: %s · %d Estrella (%s) · %s %s |
| **類型：%s（已鑲寶石）** | 类型：%s（已镶宝石） | Type: %s (Socketed) | タイプ：%s（宝石装着） | 유형: %s (보석 장착) | Tipo: %s (Engarzada) |
| **拆解【%s】：獲得鐵屑 ×%d、金幣 +%d、返還寶石【%s】** | 拆解【%s】：获得铁屑 ×%d、金币 +%d、返还宝石【%s】 | Dismantled [%s]: Iron Scrap x%d, Gold +%d, Returned Gem [%s] | 【%s】を分解：鉄くず ×%d、ゴールド +%d、宝石返還【%s】 | 【%s】 분해: 고철 ×%d, 골드 +%d, 보석 반환【%s】 | Desmantelado [%s]: Chatarra de hierro x%d, Oro +%d, Gema devuelta [%s] |
| **返還寶石** | 返还宝石 | Returned Gem | 宝石返還 | 보석 반환 | Gema devuelta |
| **返還寶石【%s】** | 返还宝石【%s】 | Returned Gem [%s] | 宝石返還【%s】 | 보석 반환【%s】 | Gema devuelta [%s] |

---

## 三、 單元與無頭測試驗證結論

- 測試腳本：`res://scripts/ui/test_bag_gem_detail_and_dismantle.gd`
- 驗證項：
  1. `GemSystem.get_gem_socket_info`：紅/黃/藍三色寶石於武器與防具六維屬性計算、星級（凡良優精極）、壓明度高對比色碼（#C2185B, #9A6B00, #1565C0）。
  2. 背包選中無寶石武器時正常顯示，不含寶石標籤；選中帶寶石武器時顯示「類型：武器（已鑲寶石）」及完整寶石名稱、星級、加成。
  3. 執行拆解時，`EquipmentSystem.dismantle` 自動退回寶石至 GemSystem（`add_gem`），`GameState.gem_bag` 數量增加，Toast 明確提示『返還寶石』。
  4. 鎖定（is_locked）與穿戴中（is_equipped）防拆保護完整生效，拆解受阻時不扣裝備亦不退寶石。
  5. 六語系字典映射與動態切換，非中文語系無 CJK 中文殘留。
- 測試結果：`TEST_BAG_GEM_DETAIL_AND_DISMANTLE_OK` (100% 綠燈通過，0 SCRIPT ERROR)。
