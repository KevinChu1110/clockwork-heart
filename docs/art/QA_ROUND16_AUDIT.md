# 探索性 QA 第十六輪實機稽核對照表（2026-09-18）

依據世界觀憲章 `docs/world/CANON.md` 與 `review.md` 規範（0-QA9 數值色差檢驗、0-ART28h 對照表、0-QA15 規格查重、31d 零系統 Emoji），針對今日合入 main 之「六族 head_unit 塗裝變體同步 (t_d11b0432 / 68b6f48f)」及同期項目（衣櫥隨機混搭鈕 t_9265459b、兔族午夜深藍耳色修正 t_7e6cf338）建立逐項對照存證。

截圖存證目錄：`proofs/qa_round16/`

## 逐項稽核對照表

| 檢查項 | 證據截圖路徑 | 通過或現象描述 |
|---|---|---|
| 1. 烈鬃獅·午夜深藍烤漆 (Lion) | `proofs/qa_round16/proof_01_wardrobe_lion_midnight.png`<br>`proofs/qa_round16/comp_01_lion_midnight.png` | **通過**：頭部鬃毛板件與軀幹同為深藍色 (70, 100, 145)，色距 0.0，色階數 70,218，平坦比 0.35%。零毛皮、金屬關節完整無破圖，零系統 Emoji。 |
| 2. 靈尾狐·翡翠螢光釉面 (Fox) | `proofs/qa_round16/proof_02_wardrobe_fox_emerald.png`<br>`proofs/qa_round16/comp_02_fox_emerald.png` | **通過**：狐耳雷達與青綠釉面 (183, 255, 225) 同步，色距 0.0，色階數 51,849，平坦比 13.08%。球形關節貼合自然無破圖，零毛皮，零系統 Emoji。 |
| 3. 鋼牙豕·赤焰熔爐烤漆 (Boar) | `proofs/qa_round16/proof_03_wardrobe_boar_crimson.png`<br>`proofs/qa_round16/comp_03_boar_crimson.png` | **通過（附已知底盤記錄）**：鉚釘風帽與機體焦橙/熔金高光 (246, 160, 82) 同步，色距 0.0，色階數 62,576。胸腹處確認為已知底盤開孔幾何問題（t_239c9c0f 同根因），除已知缺口外無新增破圖，零系統 Emoji。 |
| 4. 靈爪猴·天元青古銅 (Macaque) | `proofs/qa_round16/proof_04_wardrobe_macaque_bronze.png`<br>`proofs/qa_round16/comp_04_macaque_bronze.png` | **通過**：同軸耳與面甲、機身青銅 (219, 171, 67) 同步，色距 0.0，色階數 45,832，平坦比 0.40%。各接合處完整零白邊，零毛皮，零系統 Emoji。 |
| 5. 烈焰虎·曜黑烤漆 (Tiger) | `proofs/qa_round16/proof_05_wardrobe_tiger_volcano.png`<br>`proofs/qa_round16/comp_05_tiger_volcano.png` | **通過**：頭部與百葉雙耳同步為曜黑烤漆 (53, 47, 71)，色距 0.0，色階數 44,774，平坦比 2.12%。關節接合完整，發條機關清晰，零毛皮，零系統 Emoji。 |
| 6. 雲嵐鶴·晴空凌雲湛藍 (Crane) | `proofs/qa_round16/proof_06_wardrobe_crane_azure.png`<br>`proofs/qa_round16/comp_06_crane_azure.png` | **通過**：鶴頭冠飾與軀幹湛藍塗裝同步，色階數 48,786，平坦比 0.81%。波紋伸縮環節緊密嵌合，無浮空或斷層，零羽毛零毛皮，零系統 Emoji。 |
| 7. 兔族午夜深藍耳修正 (t_7e6cf338 回歸) | `proofs/qa_round16/proof_07_wardrobe_rabbit_midnight.png`<br>`proofs/qa_round16/comp_07_rabbit_midnight.png` | **通過**：長耳主色對齊深群青 (54, 100, 182)，明度差 0.0，無亮天藍錯色殘留。雙耳基部與頭頂外殼輪廓接合緊密，色階數 24,427，零破圖。 |
| 8. 衣櫥一鍵隨機混搭鈕 (t_9265459b 回歸) | `proofs/qa_round16/proof_08_wardrobe_random_mix.png`<br>`proofs/qa_round16/comp_08_wardrobe_random_mix.png` | **通過**：底部中段正常展示天藍多巴胺果凍隨機按鈕（高度符合手遊規範）。點擊後即時混搭（皇家巡遊禮服 + 象牙白），預覽動態更新，無異常報錯。 |
| 9. 全景截圖規格與查重 (0-QA15) | 全數 8 張全景截圖 | **通過**：全數嚴格符合 1280x720 手遊人體工學標準尺寸，MD5 100% 互異無空畫面重號。 |
| 10. 無頭測試與執行引擎 | Godot 引擎無頭執行 | **通過**：`godot --headless --quit-after 3` 零 SCRIPT ERROR；`TEST_FILTER=paperdoll ./tools/run_tests.sh` 17/17 跑綠。 |
