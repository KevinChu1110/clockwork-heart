# 驗收清單 (CHECKLIST) - t_353ac700

## 稱號前往工坊與工坊前往稱號雙分支主線合併與全面回歸驗收

- [x] 分支乾淨合併至 main 主線，衝突完全解決且無代碼遺失 (t_23216484 + t_5be26512)
- [x] TitleWallDialog 底欄 BtnGoWorkshop 前往工坊按鈕規格合規（熱區 150x52px >= 48px、多巴胺薄荷綠 #4ED86A、底厚 5px、圓角 18px、字級 18px、零 Emoji）
- [x] GemWorkshopDialog 底欄 BtnGoTitleWall 前往稱號按鈕規格合規（熱區 130x50px >= 48px、多巴胺金黃色 #FFD028、底厚 5px、圓角 18px、字級 16px、零 Emoji）
- [x] 大廳 MobileLobby 雙向直通連動與安全關閉閉環驗證（點擊直通呼起對應彈窗，無遮罩殘留，可順暢雙向來回切換）
- [x] 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換翻譯完全對齊
- [x] 單元與整合自動化測試全數 PASS 綠燈（單元測試、xvfb-run Framebuffer 整合回歸測試、無頭冒煙測試）
- [x] 8 張 1280x720 真實 Framebuffer 實機渲染截圖存證至 proofs/t_353ac700/ 與 docs/proofs/t_353ac700/，SHA256 均獨立無重複
- [x] clock-check 自動化稽核 100% 零警告通過（缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留）
- [x] docs/PROJECTS.json 專案狀態已完成更新
