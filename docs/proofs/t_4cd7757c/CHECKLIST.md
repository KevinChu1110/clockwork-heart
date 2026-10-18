# 審查常見退回自查清單 (t_4cd7757c)

對照 `~/.hermes/shared/clock-review-checklist.md` 逐項自查：

- [x] **測試與證據**：單元測試 `test_clockwork_vault_dialog_workshop_shortcut.gd`、`test_gem_workshop_dialog_vault_shortcut.gd` 與主線批次回歸測試 `test_batch_vault_workshop_shortcuts_t_4cd7757c.gd` 100% 全綠通過；產出 8 張 1280x720 實機截圖，SHA256 全部獨立唯一，無黑屏無重複。
- [x] **畫面與素材**：按鈕熱區合規（BtnGoWorkshop: 102x52px >= 48px, BtnGoVault: 130x50px >= 48px），多巴胺鮮亮配色（薄荷綠 #4ED86A / 金黃 #FFD028）、果凍厚底 5px、圓角 18px、深藍紫描邊 #1F1A3A、開源粉圓體字型、100% 零系統 Emoji。
- [x] **程式與邏輯**：點擊觸發音效、發射訊號、彈窗安全關閉無遮罩殘留，大廳順暢連動並達成雙向閉環流轉。
- [x] **資料與文案**：六語系字典檔完整補齊（繁中、簡中、英文、日文、韓文、西文），無殘留舊名詞或未翻譯鍵值。
- [x] **流程與交付**：雙分支無衝突乾淨合併至 main 主線，clock-check 檢查通過，PROJECTS.json 狀態推進至已上線。
