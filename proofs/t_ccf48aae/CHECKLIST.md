# 《發條之心》四大背包與工坊閉環功能主線合併後全面回歸驗收報告 (t_ccf48aae)

- **執行測試**：小婷（發條之心·測試 sideqa）
- **關聯任務**：`t_ccf48aae`（🤖 平台與維運｜四大背包與工坊閉環功能合併後的全全面回歸驗收（實機截圖存證））
- **前置主線合併**：`t_0d64864a`（HEAD: f8bea03c）已乾淨合併以下 4 條功能分支：
  1. `agent/20261010-bag-tab-dismantle-t_68937335` (commit 37e53d92 / 7d58b54d)
  2. `agent/20261010-bag-gem-detail-dismantle-t_2d2436f1` (commit 97a47cb0)
  3. `agent/20261010-forge-workshop-shortcut-t_2e67527c` (commit 156571b1)
  4. `agent/20261010-bag-workshop-shortcut-t_b3545e1b` (commit 1eda34e7 / c3c6d237)
- **交付存證目錄**：`proofs/t_ccf48aae/`
- **遵循規範**：
  - `review.md` 人體工學與多巴胺視覺規範：按鈕高度 >= 48px（實作 50~52px）、立體果凍厚底 5px、圓角 16~18px、零系統 Emoji、多巴胺鮮亮高飽和色盤（珊瑚粉 #FF5E8A、薄荷綠 #4ED86A、金黃 #FFD028、深藍紫描邊 #1F1A3A）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot --rendering-driver opengl3` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 4 張連續截圖 SHA256 完全獨立互異（無重複冒充），無黑屏/破圖。
    - 元件佈局高度 >= 48px，非裝備類消耗品/材料嚴格隱藏按鈕防誤觸，零折行、零溢出、零重疊。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援，非中文語系無中文殘留（依 review.md 0-QA28 驗證）。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_bag_dismantle_btn_visible.png` | `MobileLobby` 背包Tab：選中武器【生鏽短劍】時，右側詳情面板顯示多巴胺珊瑚粉 (#FF5E8A) 果凍厚底「拆解回收」按鈕（`BtnBagDismantle`，高度 52px >= 48px，底邊 5px 厚底、圓角 18px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `897798e13e0b` | 合格 (PASS) |
| 02 | `proof_02_bag_gem_detail_and_refund.png` | `MobileLobby` 背包Tab：選中已鑲嵌紅寶石之【晨曦之刃】，面板清晰標註寶石名稱、星級（凡階）、暴擊加成 (+2.0) 標籤與拆解返還機制 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `bde6f7078f1d` | 合格 (PASS) |
| 03 | `proof_03_forge_workshop_bidirectional_link.png` | 天宮鐵匠 `ForgeDialog`：頂部面板清晰顯示多巴胺薄荷綠 (#4ED86A)「前往工坊」按鈕（`BtnGoWorkshop`，高度 52px >= 48px），支援雙向平滑直通手藝工坊 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `9e2381e6dfdd` | 合格 (PASS) |
| 04 | `proof_04_bag_workshop_shortcut_btn.png` | `MobileLobby` 背包Tab：選中星屑素材【微光星屑】時，右側面板顯示多巴胺薄荷綠果凍厚底「前往工坊」按鈕（`BtnBagGoWorkshop`，高度 52px >= 48px），點擊直達工坊熔煉分頁 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `bfd9d6174726` | 合格 (PASS) |

- **防作弊與真實性校驗**：4 張全景實機截圖 SHA256 完全獨立互異（無重複冒充），通道均方差與像素極值校驗均正常（非黑屏、非純色）。
- **視覺複檢**：所有元素比例正確、無黑屏、無穿模、無截字、無任何違規 Emoji。

---

## 二、 4 項功能自動化測試 100% 通過清單

| 測試腳本 | 測試目標與覆蓋項 | 執行結果 | SCRIPT ERROR |
|---|---|:---:|:---:|
| `res://scripts/ui/test_bag_dismantle_btn.gd` | 背包武器拆解按鈕樣式、裝備/非裝備顯示分流、鎖定/穿戴防拆保護、拆解收益入帳、六語系即時切換 | **PASS** (`TEST_BAG_DISMANTLE_BTN_OK`) | 0 |
| `res://scripts/ui/test_bag_gem_detail_and_dismantle.gd` | 背包裝備詳情顯示已鑲寶石資訊、星級屬性加成、拆解安全返還至 GemSystem（防吞寶石）、防拆保護、六語系即時切換 | **PASS** (`TEST_BAG_GEM_DETAIL_AND_DISMANTLE_OK`) | 0 |
| `res://scripts/ui/test_forge_workshop_shortcut.gd` | 天宮鐵匠與手藝工坊雙向直通按鈕存在性、高度 >= 48px、雙向信號發射、彈窗乾淨掛載與銷毀、六語系即時切換 | **PASS** (`TEST_FORGE_WORKSHOP_SHORTCUT_OK`) | 0 |
| `res://scripts/ui/test_bag_workshop_shortcut.gd` | 背包星屑/寶石/裝備選中顯示前往工坊按鈕、普通材料/消耗品隱藏、收合背包並開啟工坊指定分頁、六語系即時切換 | **PASS** (`TEST_BAG_WORKSHOP_SHORTCUT_OK`) | 0 |
| `godot --headless --quit-after 3` | 全專案無頭冒煙測試與場景資源完整性 | **PASS** | 0 |

---

## 三、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **拆解回收** | 拆解回收 | Dismantle | 分解回収 | 분해 회수 | Desmantelar |
| **前往工坊** | 前往工坊 | Go to Workshop | 工房へ進む | 공방으로 이동 | Ir al Taller |
| **前往鐵匠** | 前往铁匠 | Go to Smithy | 鍛冶屋へ進む | 대장간으로 이동 | Ir a la Herrería |
| **已鑲寶石：%s · %s (%s) · %s** | 已镶宝石：%s · %s (%s) · %s | Socketed Gem: %s · %s (%s) · %s | 装着宝石：%s · %s (%s) · %s | 장착 보석: %s · %s (%s) · %s | Gema engarzada: %s · %s (%s) · %s |
| **拆解將全額返還已鑲嵌之寶石** | 拆解将全额返还已镶嵌之宝石 | Dismantling will fully refund socketed gems | 分解時に装着中の宝石は全額返還されます | 분해 시 장착된 보석이 전액 반환됩니다 | Desmantelar devolverá todas las gemas engarzadas |

---

## 四、 回歸驗收總結

經小婷（sideqa）獨立複驗：
1. 合併至 main 後之 4 大背包與工坊閉環功能（拆解回收、已鑲寶石返還、鐵匠工坊雙向直通、背包前往工坊）各項行為邏輯完全符合規格。
2. 4 支自動化單元測試 100% 綠燈，無頭冒煙 0 SCRIPT ERROR。
3. 4 張 1280x720 OpenGL3 實機截圖已落地存證，SHA256 均獨立互異，無黑屏、無破圖。
4. `clock-check` 自動化檢查無 warning，`clock-check --live` 官網頁面全部正常。
5. `docs/PROJECTS.json` 對應 4 項項目狀態更新為「已上線」。
