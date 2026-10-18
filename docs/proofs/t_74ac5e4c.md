# TitleWallDialog 稱號牆底欄新增『前往心法』快捷果凍按鈕連動 SkillDialog 驗收報告

- **任務 ID**：t_74ac5e4c
- **執行人**：發條之心·程式 阿宏 (sideworker)
- **完成時間**：2026-10-18
- **對應專案**：`title-wall-skill-shortcut`

## 驗收結果概述
1. **按鈕與樣式**：`BtnGoSkill` 成功置入 `TitleWallDialog` 底部 `ButtonRow`，具備多巴胺暖橘色盤（#FFA010）、深藍紫描邊（#1F1A3A）、底厚 5px、圓角 18px、粉圓字體 18px，觸控熱區 150x52px（>= 48px），100% 零系統 Emoji。
2. **存取器與訊號**：提供 `get_go_skill_button()` 與 `get_skill_button()` 存取器，發射 `skill_requested` 與 `go_skill` 訊號。
3. **連動與安全關閉**：點擊 `BtnGoSkill` 後發射 `closed` 訊號安全關閉稱號牆，無遮罩與元件殘留；大廳 `MobileLobby` 監聽並安全呼叫 `open_skill_dialog()` 開啟招式心法彈窗。
4. **六語系完整支援**：六語系字典已同步補齊 `title_wall.btn_go_skill` 與 `title_wall.go_skill`，支援繁中、簡中、英文、日文、韓文、西文即時切換。
5. **自動化驗證**：專屬整合測試 `test_title_wall_dialog_skill_shortcut.gd` 與 `clock-check t_74ac5e4c` 100% 全數通過，產出 8 張真實 Framebuffer 截圖（SHA256 全部獨立唯一）。
