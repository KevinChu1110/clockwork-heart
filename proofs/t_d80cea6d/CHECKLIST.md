# 驗收清單 (CHECKLIST) - t_d80cea6d

## 聚魂殿堂前往心法與心法招式前往聚魂雙分支主線合併與全面回歸驗收

- [x] 分支乾淨合併至 main 主線，衝突完全解決且無代碼遺失 (t_e6e9756b + t_cb73d5ff)
- [x] MobileLobby 聚魂殿堂底欄 BtnGoSkill 前往心法按鈕規格合規（熱區 140x52px >= 48px、多巴胺天藍色 #38A0FF、底厚 5px、圓角 18px、字級 16px、零 Emoji）
- [x] SkillDialog 心法招式底欄 BtnGoSoulHall 前往聚魂按鈕規格合規（熱區 140x50px >= 48px、多巴胺金黃色 #FFD028、底厚 5px、圓角 18px、字級 16px、零 Emoji）
- [x] 大廳 MobileLobby 雙向直通連動與安全關閉閉環驗證（點擊直通呼起對應彈窗/分頁，無遮罩殘留，可順暢雙向來回切換）
- [x] 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換翻譯完全對齊
- [x] 單元與整合自動化測試全數 PASS 綠燈（單元測試、xvfb-run Framebuffer 整合回歸測試、無頭冒煙測試）
- [x] 8 張 1280x720 真實 Framebuffer 實機渲染截圖存證至 proofs/t_d80cea6d/ 與 docs/proofs/t_d80cea6d/，SHA256 均獨立無重複
- [x] clock-check 自動化稽核 100% 零警告通過（缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留）
- [x] docs/PROJECTS.json 專案狀態已更新為已上線
