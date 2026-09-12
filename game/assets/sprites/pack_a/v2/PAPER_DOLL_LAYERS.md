# Art Pivot v2 — 紙娃娃層切表（Xiaobai）

風格鎖：手機扁平賽璐璐＋貼紙粗黑線；禁電影 3D；身份色 米白／青綠心／黃銅背鑰／單手劍。

## Slot 層（由下到上 draw order）

| z | SlotId | 說明 | 預設資產 | 可換 |
|---|--------|------|----------|------|
| 0 | `body` | 米白主體＋四肢 | `layer_body.png` | 皮膚色變體 |
| 1 | `ears` | 金屬立耳 | `layer_ears.png` | 耳飾 |
| 2 | `face` | 眼／頰紅／嘴 | `layer_face.png` | 表情 |
| 3 | `chest_heart` | 青綠心（HUD 錨點） | `layer_chest_heart.png` | 心外殼 |
| 4 | `back_key` | 黃銅背鑰（必須在背） | `layer_back_key.png` | 鑰造型 |
| 5 | `weapon_main` | 單手長劍（僅 B 相） | `layer_sword.png` | 武器 |
| 6 | `vfx_candy` | 糖果屑（part_break） | `vfx_candy_*.png` | 依 DropId |

## 三相對應

| Phase | 顯示層 | 備註 |
|-------|--------|------|
| E03 探索 | body+ears+face+chest_heart+back_key | 無武器 |
| B02 戰鬥 | 同上＋weapon_main＋可選受擊屑 | **單手**握劍 |
| D02 拆部位 | 同上無武器；手部 pose 拉齒輪 | 鑰仍在背 |

## 禁則

- 頭上螺旋槳、鑰在手上、雙手握劍、藍 mana 條、寫實電焊火花、電影級打光

## 檔案

- `xiaobai_e03.png` / `xiaobai_b02.png` / `xiaobai_d02.png`
- 樣張：`../style_pivot_xiaobai_v1.png`


> 完整開發分解見 `PAPER_DOLL_SYSTEM.md`（裝備槽＋單手/雙手/遠程動作1–3＋受擊/準備/待機）。
