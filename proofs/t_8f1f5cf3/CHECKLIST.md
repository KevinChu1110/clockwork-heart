# 審查常見退回自查清單 (t_8f1f5cf3)

- [x] 畫面與素材：實機截圖完整覆蓋 EnergyLackDialog 前往儲能庫快捷按鈕（BtnGoVault）與連動開啟 ClockworkVaultDialog，五顆按鈕並列排版正常無穿模或遮擋
- [x] 畫面與素材：熱區 >= 48px（實測 125px × 52px）、金黃色盤 #FFD028、深藍紫描邊 #1F1A3A、底邊厚 6px、圓角 20px、開源粉圓體字型、文字對比足夠
- [x] 畫面與素材：無軟連結、素材無缺失 .import、100% 零系統 Emoji
- [x] 測試與證據：驗證截圖存證完整、連續截圖不重複（SHA256 互異）
- [x] 測試與證據：單元測試防 flaky、狀態重置、語系時序解耦、無頭模式防護
- [x] 測試與證據：完整執行專屬單元測試 test_energy_lack_vault_shortcut.gd 與關聯測試（全部 PASS）
- [x] 程式與邏輯：彈窗關閉徹底、無遮罩殘留、發射 vault_requested 與 closed 訊號連動大廳開啟儲能庫
- [x] 程式與邏輯：畫面跳轉與大廳連動順暢、雙向閉環正常
- [x] 資料與文案：六語系翻譯對齊（繁中、簡中、英文、日文、韓文、西文）且零 CJK / 零 Emoji
- [x] 流程與交付：PROJECTS.json 項目狀態更新（energy-lack-vault-shortcut 與 merge-energy-lack-vault-shortcut 皆切為已上線）
- [x] 流程與交付：檔案完整 commit、工作區 clean、推送到 origin/main
