# 《發條之心》天宮鐵匠與手藝工坊雙向直通快捷按鈕驗收報告 (t_2e67527c)

- **執行工程師**：阿宏（發條之心·程式 sideworker）
- **關聯任務**：`t_2e67527c`（🎮 遊戲開發｜天宮鐵匠與手藝工坊支援雙向直通快捷按鈕（forge與workshop閉環））
- **交付存證目錄**：`proofs/t_2e67527c/`
- **遵循規範**：
  - `review.md` 人因人機工程與多巴胺視覺規範：按鈕高度 >= 48px（實作 50~52px）、立體果凍厚底 5px、圓角 16~20px、粉圓體 (Open-Huninn)、零系統 Emoji、零 13px 以下小字、多巴胺鮮亮色盤（#4ED86A 薄荷綠 / #FFA010 暖橘 / #1F1A3A 深藍紫描邊）。
  - `clock-review-checklist.md`：
    - 實機截圖 100% 走 `xvfb-run -a godot` 真實 Framebuffer 渲染（1280x720），嚴禁假圖。
    - 連續截圖 SHA256 完全獨立互異（5/5 獨立無重複冒充），存證對齊驗收項目與完整互動過程。
    - 雙向直通切換時舊彈窗確實銷毀關閉、新彈窗乾淨掛載，無殘留、無漏譯、無破圖。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）完整在地化支援，歐美非中文語系無繁中殘留。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720 OpenGL3 真實 Framebuffer 渲染）

| 編號 | 實機截圖檔名 | 涵蓋內容與驗收重點 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_forge_btn_go_workshop_zh_TW.png` | `ForgeDialog`（天宮鐵匠）：底部操作列中央配置暖橘立體厚底「前往工坊」按鈕（`BtnGoWorkshop`，高度 52px >= 48px，厚底 5px，圓角 20px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `fe6c56768ed6` | 合格 (PASS) |
| 02 | `proof_02_gem_workshop_btn_go_forge_zh_TW.png` | `GemWorkshopDialog`（手藝工坊）：底部操作列左側配置薄荷綠立體厚底「前往鐵匠」按鈕（`BtnGoForge`，高度 50px >= 48px，厚底 5px，圓角 18px） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `56434e25cbf5` | 合格 (PASS) |
| 03 | `proof_03_forge_btn_go_workshop_en.png` | 英文語系 (en) 天宮鐵匠：按鈕顯示 "Go to Workshop"，字級 18px，全英文無 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `056cd9de13fc` | 合格 (PASS) |
| 04 | `proof_04_gem_workshop_btn_go_forge_en.png` | 英文語系 (en) 手藝工坊：按鈕顯示 "Go to Smithy"，字級 18px，全英文無 CJK 中文殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `153ec6572ae8` | 合格 (PASS) |
| 05 | `proof_05_bidirectional_switch_verified.png` | 雙向切換閉環存證：在工坊點擊「前往鐵匠」後平滑銷毀工坊，乾淨切換回天宮鐵匠彈窗，無畫面閃爍與節點殘留 | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `a2e0c8851515` | 合格 (PASS) |

- **防作弊與真實性校驗**：5 張全景實機截圖 SHA256 完全獨立互異（無重複冒充）。
- **視覺複檢**：所有按鈕尺寸大於觸控人因下限（>= 48px）、多巴胺高對比鮮亮色盤、粉圓體粗描邊、零 Emoji、零文字截斷。

---

## 二、 六大語系在地化校對清單

所有文字均已嚴格對齊 `game/data/i18n/content/<locale>/ui.json` 與 `game/data/i18n/<locale>.json`：

| 來源原文 (zh_TW) | 簡體中文 (zh_CN) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) |
|---|---|---|---|---|---|
| **前往工坊** | 前往工坊 | Go to Workshop | 工房へ進む | 공방으로 이동 | Ir al Taller |
| **前往鐵匠** | 前往铁匠 | Go to Smithy | 鍛冶屋へ進む | 대장간으로 이동 | Ir a la Herrería |

---

## 三、 單元與無頭測試驗證結論

- 測試腳本：`res://scripts/ui/test_forge_workshop_shortcut.gd`
- 驗證項：
  1. ForgeDialog 包含 `BtnGoWorkshop`，高度 52px >= 48px、立體厚底 5px、圓角 20px、多巴胺暖橘色盤、粉圓體、零系統 Emoji，點擊觸發 `workshop_requested` 信號。
  2. GemWorkshopDialog 包含 `BtnGoForge`，高度 50px >= 48px、立體厚底 5px、圓角 18px、多巴胺薄荷綠色盤、粉圓體、零系統 Emoji，點擊觸發 `forge_requested` 信號。
  3. MobileLobby 雙向平滑切換邏輯：open_forge 與 open_gem_workshop 相互關閉銷毀舊彈窗實體、乾淨掛載新彈窗。
  4. 六語系字典映射與動態即時切換，非繁中無 CJK 中文殘留。
  5. 實機 OpenGL3 全景截圖存證 5/5 SHA256 獨立合格。
- 測試結果：`TEST_FORGE_WORKSHOP_SHORTCUT_OK` (100% 綠燈通過，0 SCRIPT ERROR)。
- 冒煙測試：`godot --path game --headless --quit-after 3` (0 SCRIPT ERROR)。
- 靜態檢查：`clock-check` 全部通過（✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞）。
