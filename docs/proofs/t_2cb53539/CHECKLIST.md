# 審查常見退回自查清單 (t_2cb53539)

對照 `~/.hermes/shared/clock-review-checklist.md` 逐項自查：

- [x] **測試與證據**：單元測試 `test_clockwork_vault_dialog_skill_shortcut.gd`、`test_skill_dialog_vault_shortcut.gd` 與主線批次回歸測試 `test_batch_vault_skill_shortcuts_t_2cb53539.gd` 100% 全綠通過；產出 8 張 1280x720 實機截圖，SHA256 全部獨立唯一，無黑屏無重複。
- [x] **畫面與素材**：按鈕熱區合規（BtnGoSkill: 102x52px >= 48px, BtnGoVault: 140x50px >= 48px），多巴胺鮮亮配色（珊瑚粉 #FF5E8A / 金黃 #FFD028）、果凍厚底 5px、圓角 16~18px、深藍紫描邊 #1F1A3A、開源粉圓體字型、100% 零系統 Emoji。
- [x] **程式與邏輯**：點擊觸發音效、發射訊號、彈窗安全關閉無遮罩殘留，大廳順暢連動並達成雙向閉環流轉。
- [x] **資料與文案**：六語系字典檔完整補齊（繁中、簡中、英文、日文、韓文、西文），無殘留舊名詞或未翻譯鍵值。
- [x] **流程與交付**：雙分支無衝突乾淨合併至 main 主線，clock-check 檢查通過無警告，PROJECTS.json 狀態推進至已上線。
