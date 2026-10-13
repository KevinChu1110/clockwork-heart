# 全面回歸驗收清單 · ForgeDialog 機芯一鍵校準分支合進主線 (t_1028c4a6)

## 1. 任務背景與驗收目標
將已由 sideqa 審查通過的分支 `agent/20261012-forge-core-auto-calibrate-t_4f136f47` 乾淨合併至 `main` 分支，解決潛在衝突，更新 `docs/PROJECTS.json` 將 `forge-core-auto-calibrate` 標記為已上線。執行全站無頭冒煙測試、單元測試 `test_forge_dialog_auto_calibrate.gd` 與 `clock-check`，產出合併後的回歸驗收證明文件至 `docs/proofs/` 並推送到 `origin/main`。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **機芯一鍵校準單元測試** | `godot --path game --headless -s scripts/ui/test_forge_dialog_auto_calibrate.gd` | 全部測試通過（按鈕規格、熱區、鐵屑扣除、五槽刷新、戰力提升、Toast、六語系） | **PASS** |
| **一鍵鍛造回歸單元測試** | `godot --path game --headless -s scripts/ui/test_forge_dialog_auto_forge.gd` | 全部測試通過（批次鍛造、金幣鐵屑消耗、三欄切換、六語系） | **PASS** |
| **戰力機芯快捷回歸測試** | `godot --path game --headless -s scripts/ui/test_power_stat_core_shortcut.gd` | 全部測試通過（機芯部件卡片、大廳連動開啟 ForgeDialog） | **PASS** |
| **機芯拆解回收回歸測試** | `godot --path game --headless -s scripts/ui/test_maple_inventory_core_dismantle.gd` | 全部測試通過（八色階鐵屑計算、已裝備防誤拆、容量刷新） | **PASS** |
| **公開官網與舊名詞檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞（霧隱村/今日村莊/白霧村 零殘留） | **PASS** |
| **素材與軟連結檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個，零軟連結 | **PASS** |

---

## 3. 實機截圖存證與 SHA256 雜湊表

| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_forge_core_slots_before_auto_calibrate_zh_TW.png` | 繁中鐵匠五槽白板態與 BtnAutoCalibrateCore 金黃果凍按鈕（130x48px） | 1280×720 | `843508748dac7cc9ba9f149d088da63134bcdc79b5aa4326d92ab822a8fcb4e6` |
| `proof_02_auto_calibrate_clicked_toast_power_boost_zh_TW.png` | 點擊一鍵校準後五槽升階、戰力成長與 Toast 提示 (一鍵校準完成！共校準 X 次 · 戰力提升 +XX · 消耗 XX 鐵屑) | 1280×720 | `fc973d316b130a3aa6d3d990f654da512d8fa5274e545fcdb9d4d2c435012f32` |
| `proof_03_auto_calibrate_insufficient_scrap_toast_zh_TW.png` | 鐵屑不足時點擊一鍵校準之阻擋 Toast (鐵屑不足！無法進行一鍵校準。) | 1280×720 | `545a18d6eecbec54f7d4866be904b9070866bfce3fa8665bbab1c9b56a6e1c7c` |
| `proof_04_auto_calibrate_all_maxed_toast_zh_TW.png` | 部位全部滿階/達上限時之阻擋 Toast (所有部位均已達上限或已滿色階！) | 1280×720 | `5a6b1a13ba7168960a92b1c1af67cba0cb6f0b4595062d8c8d8ee04180ba62ee` |
| `proof_05_forge_auto_calibrate_en.png` | 英文語系 (en) 一鍵校準 Auto Calibrate 按鈕與 UI，零 CJK 殘留 | 1280×720 | `dad55df9be40fc6cc99a2da9d2109539bc00b844aee26d2d5a9c0acbd1c11208` |
| `proof_06_forge_auto_calibrate_ja.png` | 日文語系 (ja) 一鍵校準 一括校正 按鈕與 UI | 1280×720 | `4af3ce999d66bd4ef32df60c5649ebff5f1b7d3dabf0d509c502728c05c56630` |

*註：6 張截圖 SHA256 互不相同，零重複，各語系渲染及時序等待皆符合手遊人因與視覺規範。*

---

## 4. 規範查核結論
- [x] **main 分支無衝突合併**：Merge commit `6da71b1dc` 乾淨整併。
- [x] **零系統 Emoji**：清除系統 emoji，採用粉圓體與質感金黃果凍厚底按鈕。
- [x] **按鈕熱區與尺寸規格**：按鈕高 48px（>= 48px），寬 130px，圓角 14px，厚底 5px。
- [x] **安全防護機制**：鐵屑不足、未裝備與滿階上限三重安全防護。
- [x] **六語系在地化切換**：zh_TW, zh_CN, en, ja, ko, es 完整對齊。
- [x] **專案狀態同步**：`forge-core-auto-calibrate` 於 `PROJECTS.json` 更新為「已上線」。
