# 驗收證明 · ShopDialog 商城彈窗底欄新增『前往衣櫥』快捷果凍按鈕聯動 WardrobeDialog (t_6e81a1be)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》商城/儲值彈窗（`ShopDialog`，`shop_dialog.gd`）底部操作按鈕列（`FooterBar`）新增『前往衣櫥』立體果凍按鈕（`BtnGoWardrobe`），打通道具商城直通衣櫥換裝彈窗（`WardrobeDialog`）的便捷跳轉：
1. **按鈕規格與樣式**：
   - 位於底部操作按鈕列，與『前往背包』、『前往聚魂』、『前往鍛造』及『前往戰力』並列。
   - 暖橘色盤 `#FFA010`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 140x48px（>= 48px 手機端防誤觸人體工學規範）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），100% 零系統 Emoji。
2. **點擊聯動與安全關閉**：
   - 點擊後發射 `wardrobe_requested` 訊號與 `closed` 訊號。
   - 安全關閉 `ShopDialog`（無遮罩殘留）。
   - 大廳連動開啟 `WardrobeDialog`（`MobileLobby.open_wardrobe()`）。
   - 流暢切換至衣櫥換裝介面。
3. **存取器與訊號**：
   - 提供 `get_go_wardrobe_button() -> Button` 存取器。
   - 提供 `wardrobe_requested` 與 `go_wardrobe` 訊號。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`shop.btn_go_wardrobe`（繁中：前往衣櫥，簡中：前往衣橱，en：Go to Wardrobe，ja：衣装部屋へ，ko：의상실로 이동，es：Ir al Armario）。
   - 已同步更新 `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處檔案。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **快捷按鈕整合測試** | `xvfb-run -a godot --path game -s res://scripts/ui/test_shop_wardrobe_shortcut.gd` | 規格、樣式、訊號、大廳連動、無遮罩殘留、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **商城全套單元測試** | `TEST_FILTER=shop ./tools/run_tests.sh` | 12 個無頭測試全部通過 (12/12 PASS) | **PASS** |
| **程式與素材合規檢查** | `clock-check .` | 零警告，完全通過 | **PASS** |
| **線上官網檢查** | `clock-check --live` | 14 頁皆可存取無舊名詞 | **PASS** |

---

## 3. 實機截圖存證清單 (真實 Framebuffer 渲染)

所有實機截圖存放於 `proofs/t_6e81a1be/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_shop_dialog_with_btn_go_wardrobe.png`
   - SHA256: `cf5217c6917565e6dd72f1d96ca31e171839d0de195d8a2f5d9952e5003cc560`
   - 說明：繁中語系 ShopDialog 底欄展示新增的暖橘立體果凍按鈕『前往衣櫥』。
2. `proof_02_wardrobe_dialog_opened_from_shop.png`
   - SHA256: `7dd9f28ce4abb5db27a307a53202f211f5b89b4b7c5f702c86a0ac61904b5696`
   - 說明：點擊『前往衣櫥』後安全關閉 ShopDialog 並直通連動開啟 WardrobeDialog 衣櫥換裝視窗。
3. `proof_03_zh_CN_shop_wardrobe_btn.png`
   - SHA256: `ebbf1f37049a24206e912d1bef0e6a6e0220b86f88167b881fd1c6b4b66feeaf`
   - 說明：簡中語系即時切換，按鈕正確顯示 `前往衣橱`，無文字溢出或截斷。
4. `proof_04_en_shop_wardrobe_btn.png`
   - SHA256: `7d1e16467e867b93b9738fac5755484ee9c5404e7e7efdfe0e9b56274fe2ba99`
   - 說明：英文語系即時切換，按鈕正確顯示 `Go to Wardrobe`。
5. `proof_05_ja_shop_wardrobe_btn.png`
   - SHA256: `81110150e164bdd5fe539fa2264e91b5c873055bb345bf303303d15943781fb0`
   - 說明：日文語系即時切換，按鈕正確顯示 `衣装部屋へ`。
6. `proof_06_ko_shop_wardrobe_btn.png`
   - SHA256: `a9a76fc49779a5f8887df2334d2b5bc60f167f33c8e8dae698bd66222f944226`
   - 說明：韓文語系即時切換，按鈕正確顯示 `의상실로 이동`。
7. `proof_07_es_shop_wardrobe_btn.png`
   - SHA256: `c849fcfe298e1b32af8ff570b54b88ec0cbc3ec35deb506b2d93aaad2917e427`
   - 說明：西文語系即時切換，按鈕正確顯示 `Ir al Armario`。

---

## 4. 專案狀態更新
- `shop-wardrobe-shortcut`：`開發中` → `測試中`（完成開發、自測與截圖存證，送審 sideqa）
