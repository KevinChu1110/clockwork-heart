# 探索性 QA 第十四輪實機稽核對照表（2026-09-18）

依據 0-ART28h / 0-QA 規範，針對兔族紙娃娃四項視覺修復與全景實機表現建立逐項對照存證。
截圖來源：`proofs/qa_round14/`

## 逐項稽核對照表

| 檢查項 | 證據截圖路徑 | 通過或現象描述 |
|---|---|---|
| 開局選族兔族舞台 | `proofs/qa_round14/proof_01_creation_rabbit_stage.png` | 通過：512 舞台高清展示，無純白矩形破圖，無毛皮殘留，零系統 Emoji。 |
| 大廳中央角色（村莊分頁） | `proofs/qa_round14/proof_02_lobby_village_rabbit.png` | 通過：高清 512 立繪，非 128 放大，浮空島背景與 HUD 完整，無系統 Emoji。 |
| 大廳中央角色（角色分頁待機） | `proofs/qa_round14/proof_03_lobby_char_rabbit.png` | 通過：角色待機動態呈現清晰，Dock 與選單齊全，色彩豐富度檢驗通過。 |
| 衣櫥無外裝·象牙白 | `proofs/qa_round14/proof_04_wardrobe_none_ivory.png` | 通過：光潔素體與鉚釘接縫正常，耳朵 (251,245,223) 與機體 (255,255,255) 明度差 10.7，同色系一致。 |
| 衣櫥無外裝·黃銅塗裝 | `proofs/qa_round14/proof_05_wardrobe_none_brass.png` | 通過：耳朵 (207,167,88) 與機體 (233,181,62) 明度差 13.0，同色系無脫節。 |
| 衣櫥無外裝·午夜深藍 | `proofs/qa_round14/proof_06_wardrobe_none_midnight.png` | ❌ 不合格：耳朵外緣亮天藍 (120,190,222) vs 機體深群青 (54,100,182)，明度差 77.1。現象：頭頂與耳外緣像戴了另一套淺藍機體的帽子，與「午夜」深邃感不成立。已立案修復卡。 |
| 衣櫥胡桃鉗·象牙白 | `proofs/qa_round14/proof_07_wardrobe_nutcracker_ivory.png` | 通過：外裝層次分明，肩章金邊貼合，無切片邊界或浮空。 |
| 衣櫥胡桃鉗·黃銅塗裝 | `proofs/qa_round14/proof_08_wardrobe_nutcracker_brass.png` | 通過：外裝與塗裝底層正確混搭，無色塊衝突與黑雜邊。 |
| 衣櫥胡桃鉗·午夜深藍 | `proofs/qa_round14/proof_09_wardrobe_nutcracker_midnight.png` | 通過（除耳色差外）：外裝部件與金邊裝飾正常套用。 |
| 蒸氣工匠·象牙白（修復項） | `proofs/qa_round14/proof_10_wardrobe_steam_ivory.png`、`proof_17_steam_artisan_detail.png` | 通過：胸腹深褐吊帶與皮革工裝圍裙剪影清晰（有描邊有弧度有層次，像素差 25358 px > 500 px），非光潔素體，非貼圖錯位。 |
| 蒸氣工匠·黃銅塗裝 | `proofs/qa_round14/proof_11_wardrobe_steam_brass.png` | 通過：金屬扣件與工裝圍兜正常疊加於黃銅機體。 |
| 蒸氣工匠·午夜深藍 | `proofs/qa_round14/proof_12_wardrobe_steam_midnight.png` | 通過（除耳色差外）：工匠外裝正常覆蓋於深藍素體。 |
| 皇家巡遊·象牙白（修復項） | `proofs/qa_round14/proof_13_wardrobe_royal_ivory.png`、`proof_18_royal_neckline_detail.png` | 通過：領口隨頸胸起伏轉折呈圓弧貼合，無生硬水平切口，頸部接合完整無白色缺口斷層。 |
| 皇家巡遊·黃銅塗裝 | `proofs/qa_round14/proof_14_wardrobe_royal_brass.png` | 通過：圓弧領口與金邊隨形走，無邊界生硬橫切。 |
| 皇家巡遊·午夜深藍 | `proofs/qa_round14/proof_15_wardrobe_royal_midnight.png` | 通過（除耳色差外）：圓弧領口貼合頸部，無接縫斷裂。 |
| 衣櫥縮圖卡片規格（修復項） | `proofs/qa_round14/proof_16_wardrobe_cards_overview.png`、`crop_wardrobe_cards_all.png` | 通過：符合 0-ART28i 例外基準（無外裝縮圖為無武器素體部件視角），外裝卡片規格視覺一致。 |
| 兔族午夜深藍耳特寫（修復項） | `proofs/qa_round14/proof_19_midnight_ears_detail.png`、`crop_detail_midnight_ears.png` | ❌ 不合格：alpha bbox (169,25,334,216) 雖完整無雜邊，但耳外緣最大不透明主色 (120,190,222) 亮天藍與 chassis (54,100,182) 深群青明度差 77.1，色相與明度顯著脫節。 |
| 全景規格與防重號 | `proofs/qa_round14/proof_01` ~ `19` | 通過：全數 1280x720 實機全景截圖，主要 15 張畫面 MD5 100% 互異。 |
| 系統 Emoji 與規範 | 遊戲 UI 與腳本掃描 | 通過：100% 零系統 Emoji、按鈕熱區 >= 48px、粉圓體正常渲染。 |

## 待修項目（已開看板卡）

1. **兔族午夜深藍塗裝耳朵色票修正**
   - **問題**：`head_unit/ear_rabbit_straight_midnight_512.png` 耳外緣亮天藍 (120, 190, 222) 與 `chassis/paint_midnight_navy_512.png` 機體深群青 (54, 100, 182) 色差過大（明度差 77.1，合格基準 brass/ivory 為 10~13）。
   - **現象**：頭頂與耳外緣像戴了另一套淺藍機體的帽子，與「午夜」的深邃感不成立。這是玩家在衣櫥第一眼就會看到的。
   - **修復要求**：把兔族 midnight 耳外緣主色調到與 chassis (54, 100, 182) 同族，明度差控制在 brass 量級（明度差 <= 20.0），保持 bbox (169,25,334,216) 不縮水。
   - **追蹤卡號**：`t_7e6cf338`（[Art] 兔族午夜深藍塗裝耳朵色票修正：耳外緣主色對齊 chassis 深群青，指派 sideart）。
