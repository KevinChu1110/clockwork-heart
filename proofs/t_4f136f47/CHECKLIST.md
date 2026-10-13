# 驗收清單：ForgeDialog 天宮鐵匠機芯五槽新增『一鍵校準』果凍按鈕與連動 CoreSystem (t_4f136f47)

## 1. 任務核心驗收標準對齊
- [x] **ForgeDialog 機芯五槽部位面板一鍵校準果凍按鈕 (BtnAutoCalibrateCore)**：
  - 在 `game/scripts/ui/forge_dialog.gd` 之 `ForgeCoreSlotsPanel` 面板標題列（`core_head`）新增「一鍵校準」果凍按鈕（`BtnAutoCalibrateCore`）。
  - 熱區尺寸嚴格符合手機端防誤觸規範（`custom_minimum_size = Vector2(130, 48)`，高度 >= 48px）。
  - 配色採多巴胺金黃果凍厚底風格（`COLOR_GOLD` `#FFD028`、深藍紫描邊 `COLOR_BORDER` `#1F1A3A`、底部立體厚底 5px、圓角 14px、陰影 6px），文字採深藍紫加粗加白描邊（14px），達成零系統 Emoji。
- [x] **檢查鐵屑與循環校準連動 CoreSystem**：
  - 點擊後依序檢查 `GameState.iron_scrap` 與 `CoreSystem.has_enough_scrap_to_calibrate()`。
  - 鐵屑充足時，依順序（可校準、剩餘次數 > 0、未達紅階 TIER_RED）循環對已裝備機芯執行 `CoreSystem.calibrate_player_part()`。
  - 當鐵屑不足或所有部位校準次數耗盡/達到滿階時，安全退出迴圈。
- [x] **即時數值、五槽外觀、頂部戰力與飄字提示 (Toast)**：
  - 執行後即時調用 `_refresh_all_forge_core_slots()` 與 `_refresh_display()`。
  - 五槽卡片之 `TierLabel`（色階）、`CountLabel`（剩餘次數）、`SlotIcon.modulate`（色階光暈）即時刷新。
  - 頂部戰力 `TopPowerLabel`（`战力 %d`）即時增長。
  - 彈出獨立 Toast（`ForgeToast`）與更新 `MsgLabel`，提示「一鍵校準完成！共校準 X 次 · 戰力提升 +XX · 消耗 XX 鐵屑」。
- [x] **完整安全邊界防護**：
  - 鐵屑不足時點擊：正確阻擋並彈出「鐵屑不足！無法進行一鍵校準。」Toast。
  - 未裝備機芯時點擊：正確阻擋並彈出「未裝備任何可校準的機芯部位！」Toast。
  - 部位全滿階/次數達上限時點擊：正確阻擋並彈出「所有部位均已達上限或已滿色階！」Toast。
- [x] **六語系即時在地化切換**：
  - 支援 zh_TW, zh_CN, en, ja, ko, es 六大語系即時切換。
  - 各語系按鈕文字精確對齊（zh_TW="一鍵校準", zh_CN="一键校准", en="Auto Calibrate", ja="一括校正", ko="일괄 보정", es="Calibración Rápida"）。
  - 歐美語系 (en, es) 零 CJK 漢字殘留，全語系零系統 Emoji。

---

## 2. 測試與驗證結果
- **專屬單元測試**：
  - `TEST_FILTER=test_forge_dialog_auto_calibrate ./tools/run_tests.sh`：1/1 PASS（100% 全綠，TEST_FORGE_DIALOG_AUTO_CALIBRATE_OK，exit code 0）。
  - 覆蓋點：按鈕熱區與尺寸規格、鐵屑不足防護、未裝備與滿階上限防護、充足資源下循環校準迴圈、鐵屑扣除、五槽即時刷新、頂部戰力增長、Toast 飄字提示、六語系即時切換與零 Emoji。
- **既有回歸測試**：
  - `TEST_FILTER=test_forge ./tools/run_tests.sh`：6/6 PASS（全數通過，無任何回歸破壞）。
- **冒煙測試**：
  - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR（exit code 0）。
- **clock-check 自動檢查**：
  - `/root/bin/clock-check /opt/side/bravesoul-game`
  - 結論：`✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。

---

## 3. 實機 Framebuffer 截圖存證 (proofs/t_4f136f47/)
所有截圖皆以 OpenGL3 渲染驅動於 1280x720 解析度下透過真實 Viewport Framebuffer 產生，零 PIL 假圖，SHA256 各自獨立：

| 檔案名稱 | 說明 | SHA256 |
|---|---|---|
| `proof_01_forge_core_slots_before_auto_calibrate_zh_TW.png` | 繁中鐵匠五槽白板態與 BtnAutoCalibrateCore 金黃果凍按鈕（130x48px） | `843508748dac7cc9ba9f149d088da63134bcdc79b5aa4326d92ab822a8fcb4e6` |
| `proof_02_auto_calibrate_clicked_toast_power_boost_zh_TW.png` | 點擊一鍵校準後五槽升階、戰力成長與 Toast 提示 (一鍵校準完成！共校準 X 次 · 戰力提升 +XX · 消耗 XX 鐵屑) | `fc973d316b130a3aa6d3d990f654da512d8fa5274e545fcdb9d4d2c435012f32` |
| `proof_03_auto_calibrate_insufficient_scrap_toast_zh_TW.png` | 鐵屑不足時點擊一鍵校準之阻擋 Toast (鐵屑不足！無法進行一鍵校準。) | `545a18d6eecbec54f7d4866be904b9070866bfce3fa8665bbab1c9b56a6e1c7c` |
| `proof_04_auto_calibrate_all_maxed_toast_zh_TW.png` | 部位全部滿階/達上限時之阻擋 Toast (所有部位均已達上限或已滿色階！) | `5a6b1a13ba7168960a92b1c1af67cba0cb6f0b4595062d8c8d8ee04180ba62ee` |
| `proof_05_forge_auto_calibrate_en.png` | 英文語系 (en) 一鍵校準 Auto Calibrate 按鈕與 UI，零 CJK 殘留 | `dad55df9be40fc6cc99a2da9d2109539bc00b844aee26d2d5a9c0acbd1c11208` |
| `proof_06_forge_auto_calibrate_ja.png` | 日文語系 (ja) 一鍵校準 一括校正 按鈕與 UI | `4af3ce999d66bd4ef32df60c5649ebff5f1b7d3dabf0d509c502728c05c56630` |

---

## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **截圖存證確實對齊驗收項目與完整互動過程**：繁中、英文、日文各情境截圖齊全，包含校準前、校準後戰力提升飄字、鐵屑不足阻擋、全部滿階阻擋、語系切換，SHA256 皆獨立無重複。
- [x] **單元測試穩定防 flaky**：等待幀數充足（20~25 幀），無時序競爭，無頭測試 `1/1 PASS`。
- [x] **UI 排版邊界與圖層順序 (Z-index)**：按鈕位於 `core_head` 標題列右端，彈出之 Toast 設為 z-index=100，層次分明無穿透。
- [x] **互動元件佈局尺寸與熱區**：`BtnAutoCalibrateCore` 尺寸設為 130x48px，熱區符合手遊規範（>= 48px），避免節點坍塌。
- [x] **字級規範**：字體大小 14px 加粗，深藍紫加深描邊，達成零小字。
- [x] **零系統 Emoji**：按鈕與飄字全域無系統 Unicode Emoji。
- [x] **名稱與用詞規範**：五大槽位名稱與八色階名稱嚴格對齊既有定義，無任何已淘汰用詞。
