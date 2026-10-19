# 驗收清單 (CHECKLIST) - t_d50fd787

## 楓之谷紙娃娃架構與首發三族展示切換主線合併與全面回歸驗收

- [x] 分支乾淨合併至 main 主線，衝突完全解決且無代碼遺失 (t_e425d379 + t_924d3928 + t_dd5fc16a + t_d7d5ff53)
- [x] MaplePaperdoll 重構核心組件 (Character.wz 骨骼錨點 neck/navel/hand/brow/back_key/tail 與部件分層掛載) 功能完整
- [x] 第二族熾火赤狐專屬骨骼錨點與 7 大部件分層切片規格建置完備，外裝胸前自然開出心臟視窗 (0-ART51)
- [x] 第三族烈金雄獅專屬骨骼錨點與 7 大部件分層切片規格建置完備，純淨金屬底盤與動態 Z-Order 控制 (0-ART51)
- [x] MaplePaperdollShowcase 展示場景支援白兔、赤狐、雄獅首發三族即時切換與骨骼錨點聯動，無縫復原且零狀態殘留
- [x] 全套單元與實機自動化測試 100% 通過：
  - `test_maple_paperdoll_showcase_multirace.gd` -> MAPLE_SHOWCASE_MULTIRACE_OK
  - `test_maple_paperdoll.gd` -> MAPLE_PAPERDOLL_OK
  - `test_maple_paperdoll_fox.gd` -> MAPLE_PAPERDOLL_FOX_OK
  - `test_maple_paperdoll_lion.gd` -> MAPLE_PAPERDOLL_LION_OK
- [x] 5 張 1280x720 真實 Framebuffer 實機渲染截圖存證至 proofs/t_d50fd787/ 與 docs/proofs/t_d50fd787/，SHA256 均獨立無重複
- [x] clock-check 自動化稽核 100% 零警告通過（新增/修改 64 個素材，缺 .import 0 個、0 軟連結、語系 key 齊全、0 舊名詞殘留）
- [x] docs/PROJECTS.json 專案狀態已由 project_status.py 更新推進
