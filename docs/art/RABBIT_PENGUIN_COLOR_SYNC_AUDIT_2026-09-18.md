# 0-ART28q 兔族與蒸氣企鵝族頭部塗裝色距稽核與查重對照表 (t_0345072a)

依據 `review.md` 規範（0-ART28q 嚴格色距量測、0-ART28n 切片查重、0-ART28h 複檢留存對照表），針對兔族（Rabbit）與蒸氣企鵝族（Penguin）head_unit 所有塗裝進行 L2 平均板件色距量測與 MD5 唯一性查核。

## 一、量測標準與方法
1. **平均板件色公式（0-ART28q）**：
   - 採計 $\alpha > 200$ 之不透明像素。
   - 排除深色描邊 $\max(R,G,B) \le 70$ 後取 RGB 平均向量 $\bar{C}$。
2. **合格門檻**：
   - 與同族對應 chassis 塗裝切片之歐幾里得距離 $L_2 = \|\bar{C}_{\text{head}} - \bar{C}_{\text{chassis}}\| < 60.0$。
   - MD5 全目錄查重無非預期重複（0-ART28n）。
   - 角色外觀 100% 零毛皮、金屬板件與發條玩具結構完整。

---

## 二、兔族與蒸氣企鵝族色距與 MD5 對照表

| 族系 | 塗裝變體名稱 | Head 檔案路徑 | Chassis 檔案路徑 | Head 平均色 (RGB) | Chassis 平均色 (RGB) | L2 色距 | MD5 雜湊值 | 判定 |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **兔族 (Rabbit)** | 原廠象牙白 (Ivory Stock) | `ear_rabbit_straight_512.png` | `paint_ivory_stock_512.png` | (217.8, 173.4, 153.9) | (183.8, 177.8, 159.1) | **34.6** | `3f34bb3db9da43a0d02520ef5c901708` | ✅ **PASS** |
| **兔族 (Rabbit)** | 黃銅原金 (Brass Gold) | `ear_rabbit_straight_brass_512.png` | `paint_brass_gold_512.png` | (214.8, 158.1, 109.1) | (188.7, 156.7, 81.0) | **38.4** | `9dfdf3a74bb1efb4da8f3c0ed8172808` | ✅ **PASS** |
| **兔族 (Rabbit)** | 午夜深藍 (Midnight Navy) | `ear_rabbit_straight_midnight_512.png` | `paint_midnight_navy_512.png` | (119.1, 108.2, 148.1) | (84.5, 109.1, 149.0) | **34.6** | `d90f98b89cb528911fc1aeba9995d111` | ✅ **PASS** |
| **蒸氣企鵝 (Penguin)** | 深海鍍鈦藍 (Navy Stock) | `head_steam_penguin_stock_512.png` | `paint_penguin_navy_512.png` | (114.8, 111.8, 128.0) | (129.8, 132.1, 148.7) | **32.7** | `6cfb9d788cd77b14d1af9d3231b087ff` | ✅ **PASS** |
| **蒸氣企鵝 (Penguin)** | 極光冰川白 (Polar Frost) | `head_steam_penguin_polar_512.png` | `paint_polar_frost_512.png` | (194.9, 188.8, 174.8) | (181.3, 185.4, 188.1) | **19.3** | `2905d197ea704ef67131adc9815b299e` | ✅ **PASS** |
| **蒸氣企鵝 (Penguin)** | 原廠象牙白 (Ivory Stock) | `head_steam_penguin_ivory_512.png` | `paint_ivory_stock_512.png` | (188.1, 165.8, 133.2) | (196.9, 185.8, 171.2) | **43.8** | `0e7d5419b67ac7b84229f7db40a92b5f` | ✅ **PASS** |

> 備註：企鵝族別名檔 `head_steam_penguin_navy_512.png` 已同步對齊 stock 切片，符合 `0-ART28n` 已知基底別名規範。

---

## 三、實機衣櫥佐證截圖與 Vision 審核結論

| 族系 | 實機全景截圖 | 512 高清合成角色切片 | Vision 自檢結論 |
| :--- | :--- | :--- | :--- |
| **兔族 (Rabbit)** | `proofs/head_sync_proofs/proof_wardrobe_rabbit_ivory.png` | `proofs/head_sync_proofs/composite_512_rabbit_ivory.png` | **通過**：100% 零毛皮，金屬板件接縫與高光清晰，雙長耳與軀幹原廠象牙白光澤高度協調，關節軸承完整，無斷裂或破圖。 |
| **蒸氣企鵝族 (Penguin)** | `proofs/head_sync_proofs/proof_wardrobe_penguin_navy.png` | `proofs/head_sync_proofs/composite_512_penguin_navy.png` | **通過**：100% 零毛皮，深海鍍鈦藍機殼與黃銅護目鏡層次分明，背部發條鑰匙與蒸氣氣瓶層級正確，無缺口或穿模。 |
