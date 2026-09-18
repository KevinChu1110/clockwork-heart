# 探索性 QA 第十六輪實機稽核對照表（2026-09-18）

依據世界觀憲章 `docs/world/CANON.md` 與 `review.md` 規範（0-QA9 數值色差檢驗、0-ART28h 對照表、0-QA15 規格查重、31d 零系統 Emoji），針對合入 main 之「六族 head_unit 塗裝變體同步 (t_d11b0432)」與修復單 (t_2247d718 / 3f630388) 及同期項目（衣櫥隨機混搭鈕 t_9265459b、兔族午夜深藍耳色修正 t_7e6cf338）建立逐項對照存證。

截圖存證目錄：`proofs/qa_round16/`

## 逐項稽核對照表（採用平均色板件色距公式 L2 < 60.0）

| 檢查項 | 證據截圖路徑 | 色距與品質量測 (0-QA9 / 0-QA17) | 通過或現象描述 |
|---|---|---|---|
| 1. 烈鬃獅·午夜深藍 (Lion) | `proofs/qa_round16/proof_01_wardrobe_lion_midnight.png`<br>`proofs/qa_round16/comp_01_lion_midnight.png` | Head: (57.0, 78.7, 113.5)<br>Chassis: (83.0, 109.1, 148.8)<br>**ΔE: 53.4** (< 60.0 PASS)<br>色階數: 33,439，平坦比: 0.06% | **通過**：鬃毛面甲與軀幹午夜深藍塗裝同步，雙眼鏤空銜接正常，金屬板件鉚釘清晰，零毛皮，零系統 Emoji。 |
| 2. 靈尾狐·翡翠螢光釉面 (Fox) | `proofs/qa_round16/proof_02_wardrobe_fox_emerald.png`<br>`proofs/qa_round16/comp_02_fox_emerald.png` | Head: (129.8, 205.3, 165.5)<br>Chassis: (133.5, 207.7, 166.3)<br>**ΔE: 4.5** (< 60.0 PASS)<br>色階數: 27,000，平坦比: 1.52% | **通過（瑕疵修復複驗）**：雙眼瞳孔高光與水藍虹膜、黃銅眼眶正常展示，無白色缺塊；畫面左側懸空之發條鑰匙與齒輪碎屑已清理；色距 4.5 高度同步。 |
| 3. 鋼牙豕·赤焰熔爐 (Boar) | `proofs/qa_round16/proof_03_wardrobe_boar_crimson.png`<br>`proofs/qa_round16/comp_03_boar_crimson.png` | Head: (145.5, 80.6, 38.8)<br>Chassis: (137.6, 74.0, 43.1)<br>**ΔE: 11.2** (< 60.0 PASS)<br>色階數: 17,730，平坦比: 0.12% | **通過（附已知底盤記錄）**：胸口已清除未染色之藍灰色塊與除錯線，雙臂巨錘連接完整；下巴頸胸缺口為已知底盤開孔幾何問題（t_239c9c0f 同根因），無新增破圖。 |
| 4. 靈爪猴·天元青古銅 (Macaque) | `proofs/qa_round16/proof_04_wardrobe_macaque_bronze.png`<br>`proofs/qa_round16/comp_04_macaque_bronze.png` | Head: (162.8, 126.8, 51.8)<br>Chassis: (202.4, 159.4, 65.3)<br>**ΔE: 53.1** (< 60.0 PASS)<br>色階數: 30,576，平坦比: 0.01% | **通過**：同軸耳、面甲外圈與機身青古銅塗裝高度同步，金屬質感統一，零毛皮，零系統 Emoji。 |
| 5. 烈焰虎·曜黑烤漆 (Tiger) | `proofs/qa_round16/proof_05_wardrobe_tiger_volcano.png`<br>`proofs/qa_round16/comp_05_tiger_volcano.png` | Head: (62.2, 52.0, 72.4)<br>Chassis: (97.3, 78.0, 72.7)<br>**ΔE: 43.6** (< 60.0 PASS)<br>色階數: 23,109，平坦比: 0.09% | **通過**：虎頭面甲、排氣百葉耳與身體外骨骼曜黑烤漆高度一致，發條短刃與機械尾完整無缺損，零毛皮。 |
| 6. 雲嵐鶴·晴空凌雲湛藍 (Crane) | `proofs/qa_round16/proof_06_wardrobe_crane_azure.png`<br>`proofs/qa_round16/comp_06_crane_azure.png` | Head: (65.4, 109.4, 191.8)<br>Chassis: (102.3, 129.9, 161.2)<br>**ΔE: 52.2** (< 60.0 PASS)<br>色階數: 21,203，平坦比: 0.12% | **通過（瑕疵修復複驗）**：頭部圓球外殼同步為湛藍金屬色，色距由退稿時的 73.7 降至 52.2（< 60.0 門檻），消除青瓷白未換色缺陷。 |
| 7. 兔族午夜深藍耳修正 (t_7e6cf338 回歸) | `proofs/qa_round16/proof_07_wardrobe_rabbit_midnight.png`<br>`proofs/qa_round16/comp_07_rabbit_midnight.png` | 耳色對齊深群青 (54, 100, 182)<br>明度差 0.0，無亮天藍錯色 | **通過**：雙耳外殼與身體主色一致為午夜深藍／深群青，樞軸結構嵌合緊密，零毛皮零破圖。 |
| 8. 衣櫥一鍵隨機混搭鈕 (t_9265459b 回歸) | `proofs/qa_round16/proof_08_wardrobe_random_mix.png`<br>`proofs/qa_round16/comp_08_wardrobe_random_mix.png` | 天藍色多巴胺果凍按鈕<br>高度 >= 48px，即時響應 | **通過**：點擊後即時混搭（象牙白 + 皇家巡遊禮服），預覽動態更新無報錯，UI 100% 零 Emoji。 |
| 9. MD5 切片去重查核 (0-QA15) | 全數 13 組新切片 vs 同族 Stock | MD5 100% 互異獨立 | **通過**：無偽裝複製檔案，Tiger Ember 與 Crane Porcelain 切片均具備獨立 MD5 與色階。 |
| 10. 無頭測試與引擎冒煙 | Godot 引擎無頭執行 | 17/17 全數通過 | **通過**：`godot --headless --quit-after 3` 零 SCRIPT ERROR；`TEST_FILTER=paperdoll ./tools/run_tests.sh` 17/17 跑綠。 |
