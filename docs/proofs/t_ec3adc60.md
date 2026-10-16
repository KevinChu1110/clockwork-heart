# 驗收證明 · ShopDialog 商城彈窗底欄新增『前往委託』快捷果凍按鈕連動 WindupDailyDialog (t_ec3adc60)

## 1. 任務背景與驗收目標
依據任務規範，於《發條之心》道具商城彈窗（`ShopDialog`，`shop_dialog.gd`）底部操作快捷列（`FooterBar`）新增『前往委託』多巴胺立體果凍按鈕（`BtnGoWindupDaily`），與已在實作的冒險委託『前往商城』形成完整雙向閉環：
1. **按鈕規格與樣式**：
   - 位於底部操作按鈕列（`FooterBar`），外層具備 `FooterScroll` 橫向滑動支援與結尾間距 `FooterEndSpacer`，確保 10 顆快捷按鈕在手遊與窄螢幕下皆可流暢操作且不撐破 740~760px 彈窗卡片規範。
   - 多巴胺暖橘色盤 `#FFA010`，深藍紫描邊 `#1F1A3A`，文字深藍紫 `#1F1A3A`。
   - 熱區尺寸 150x50px（高度 `>= 50px`，滿足手機端防誤觸人體工學規範 `>= 48px`）。
   - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體（Open Huninn），100% 零系統 Emoji。
2. **點擊聯動與雙向閉環**：
   - 點擊後發射 `windup_daily_requested` 訊號與 `go_windup_daily` 訊號（相容 `windup_requested` / `go_windup`）。
   - 安全關閉 `ShopDialog`（無遮罩殘留）。
   - 大廳連動開啟 `WindupDailyDialog`（`MobileLobby.open_windup_daily()`）。
   - 於 `WindupDailyDialog` 點擊 `BtnGoShop` 可流暢返回 `ShopDialog` 商城彈窗，達成完整無縫雙向跳轉閉環。
3. **存取器與訊號**：
   - 提供 `get_go_windup_daily_button() -> Button` 與 `get_windup_daily_button() -> Button` 存取器（相容 `get_go_daily_button()`、`get_daily_button()`、`get_go_windup_button()`、`get_windup_button()`）。
   - 提供 `windup_daily_requested` 與 `go_windup_daily` 訊號。
   - 提供 `get_footer_scroll()`、`scroll_footer_to_button()`、`scroll_footer_to_end()`。
4. **六語系在地化支援**：
   - 完整支援 `zh_TW`, `zh_CN`, `en`, `ja`, `ko`, `es` 六語系即時切換。
   - 字典鍵值：`shop.btn_go_daily` 與 `shop.btn_go_windup`（繁中：前往委託，簡中：前往委托，en：To Daily，ja：日課へ，ko：일일 의뢰로 이동，es：Ir a Encargos）。
   - 已同步更新 `game/data/i18n/*.json` 與 `game/data/i18n/content/*/ui.json` 共 12 處檔案。

---

## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **商城彈窗單元測試** | `godot --path game --headless -s res://scripts/ui/test_shop_dialog.gd` | 規格、樣式、訊號、IAP品項、去廣告、六語系即時切換全綠 (exit 0) | **PASS** |
| **快捷按鈕整合測試** | `godot --path game --headless -s res://scripts/ui/test_shop_dialog_daily_shortcut.gd` | 規格、樣式、訊號、大廳連動、雙向閉環、六語系即時切換全部 PASS (exit 0) | **PASS** |
| **無頭冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR | **PASS** |
| **程式與素材合規檢查** | `clock-check .` | 零警告，完全通過 | **PASS** |

---

## 3. 實機截圖存證清單 (真實 Framebuffer 渲染)

所有實機截圖存放於 `proofs/t_ec3adc60/` 與 `docs/proofs/t_ec3adc60/` 目錄，經檢驗 SHA256 全部獨立唯一、無黑屏、無遮罩殘留、無文字穿框溢出：

1. `proof_01_zh_TW_shop_dialog_with_btn_go_windup_daily.png`
   - SHA256: `c52eaf795fe4c1fb70fd120af53ca5fef1417d2b901a34a93dcbd2f59b33bb6a`
   - 說明：繁中語系 ShopDialog 底欄展示新增的多巴胺暖橘立體果凍按鈕『前往委託』。
2. `proof_02_windup_daily_dialog_opened_from_shop.png`
   - SHA256: `f26fd13b4f9907bc01d57b82e8c8fca2dca3e780167cd6d3e109c260dbf92eaa`
   - 說明：點擊『前往委託』後安全關閉 ShopDialog 並直通連動開啟 WindupDailyDialog 每日委託視窗，且委託完成時展示『前往商城』按鈕。
3. `proof_03_loop_back_to_shop_dialog.png`
   - SHA256: `d7c1de6bc8d6ea2ec57ca6bad9f4eb6410ae588ff79754ea901f8af6edb82eb1`
   - 說明：於每日委託點擊『前往商城』後安全關閉委託視窗並成功流暢返回 ShopDialog 商城彈窗，達成完整雙向閉環。
4. `proof_04_zh_CN_shop_daily_btn.png`
   - SHA256: `151ff41792fd21cf58cdc38b7f0ef896b559490ecce832a4c5906ad75958e86e`
   - 說明：簡中語系即時切換，按鈕正確顯示 `前往委托`，無文字溢出或截斷。
5. `proof_05_en_shop_daily_btn.png`
   - SHA256: `68e32c91462bbcafb9502c72235787ccc9737022053d800bece584e5cf1d91b4`
   - 說明：英文語系即時切換，按鈕正確顯示 `To Daily`，零 CJK 殘留。
6. `proof_06_ja_shop_daily_btn.png`
   - SHA256: `33e03b13efed6fc29601fb090ad3ce3c3f5df0d2697b003a1c362e655d53dda4`
   - 說明：日文語系即時切換，按鈕正確顯示 `日課へ`。
7. `proof_07_ko_shop_daily_btn.png`
   - SHA256: `f4b7cc258a2ad0bce7fbd48a0390ab707f51893bd91ec124c418f63b42328918`
   - 說明：韓文語系即時切換，按鈕寬度充足（150px）正確顯示 `일일 의뢰로 이동`，無截斷或重疊。
8. `proof_08_es_shop_daily_btn.png`
   - SHA256: `cc379817b0a553d9a779b24f800f933dbe02b82b3d802a2cf8f658ee1e324fc3`
   - 說明：西文語系即時切換，按鈕正確顯示 `Ir a Encargos`，零 CJK 殘留。
