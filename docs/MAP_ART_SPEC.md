# 地圖底圖統一規格（2026-08-27 Kevin 拍板）

> 起因：底圖各自生成，視角與比例尺失控——有 ¾ 俯視村莊、有帶天空的遠景山水、
> 有平視鏡頭、甚至有帶畫框的卷軸圖。角色疊上去比例錯亂、像漂浮在畫上。
> 本檔是**唯一**的產圖規格；重生成與新圖一律照此，不要憑感覺寫 prompt。

## 硬規則（違反任一條就重生成）

| 規則 | 說明 |
|------|------|
| 視角 | **45° ¾ 俯視等角**（以 town／village 為基準），全圖同一相機高度 |
| 禁止 | 天空、地平線、雲海、畫框／邊框、文字、星座連線、暗角 |
| 地面鋪滿 | 地形鋪滿整張畫布，圖緣就是地面（出口做在圖緣），不留「遠方」 |
| 比例尺 | 單層屋高 ≈ 畫面高 **1/4**；門高 ≈ 畫面高 **1/12**（＝角色兩倍身高）；樹冠 ≈ 屋高 |
| 路 | 至少一條主路，寬 ≈ 門寬 1.5–2 倍，清楚連到圖緣（接 walkmask 與出口） |
| 開闊度 | ≥ 40% 是可走地面；物件沿邊與節點擺，不塞滿 |
| 規格 | 16:9；**原生像素 ≥ 該 art 的世界／FLOOR 尺寸**（禁止小圖硬拉）。新圖用 Gemini 2K／4K，裝進 runtime 前按世界尺寸縮，再過 `tools/pixelize_env.py`（96 色主色盤） |


## Prompt 模板（tools/regen_map_bgs.py 用這個，不要另起爐灶）

```
top-down 3/4 isometric RPG map background, camera looking down at 45 degrees,
consistent scale: a single-story house is about 1/4 of image height and a doorway
about 1/12 of image height, ground terrain fills the entire canvas edge to edge,
no sky, no horizon, no clouds, no border, no frame, no text, clear walkable dirt
paths about twice door width connecting to the edges, at least forty percent open
walkable ground, warm muted painted game art, {每圖一句 content brief}
```

## 產後三件事（缺一不可）

1. 已有 4K 原檔時用 `tools/install_hd_native.py` 裝成「原生 ≥ 世界」的 16:9 webp（不要再縮死 2633×1469）
2. `tools/pixelize_env.py`（會自動備份原圖到 `_backup_prepixel_*`）
3. **重描 walkmask**（`data/walkmask.json`）——圖換了 mask 一定要跟著換，
   跑 `tools/check_walkmask.py` 到全綠（出生點＋每個互動實體可站可達）
4. `dev/verify_capture.gd` 實拍確認角色可見、走在路上

## 特例備忘

- `tower_memory`（塔內記憶幻境）刻意抽象，**豁免**本規格。
- 室內店舖（`town_forge`／`town_soul`／`town_gem`／`town_tutor`）同樣 ¾ 俯視房間、地面鋪滿；禁止眼平室內＋窗外天空。
- 「高處」主題（dojo_peak、mist_cliff）：雲霧只能當**圖緣邊界**處理，不得出現天空視角。
- 開放式建築（棚屋、涼亭）不得當場景遮擋切片——矩形切片表達不了（road_inn 教訓）。
