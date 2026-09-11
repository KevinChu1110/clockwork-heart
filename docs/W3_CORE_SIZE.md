# W3-F1 · Core 首包量測（給 Mark 商店文案）

> 分支 `w3/core-export`｜對齊 Product Lock §5.2（首次必要下載 50～80 MB）＋ Ken Base／Pack-A

## Before → After（源資產，`python3 tools/measure_bundle.py`）

| 包 | Before | After | Δ |
|---|---:|---:|---:|
| **core** | **61.45 MB** | **45.29 MB** | **−16.16 MB** |
| chapter | 63.29 MB | 79.45 MB | +16.16（收下從 core 挪出的 BGM） |
| extra | 54.97 MB | 54.97 MB | — |

**首包估計（源資產 + Godot 引擎 25–40 MB）：**

| | Before | After |
|---|---|---|
| 區間 | 86–101 MB | **70–85 MB** |

貼圖 import／壓縮後實裝 PCK 通常再低一截；本機無 export templates，未打 APK／.app 實重。

## 這次動了什麼

1. **`bundle_manifest.json`**
   - core BGM：**只留 `battle`**（C0 教學戰；缺檔會靜音警告，不擋流程）
   - `title`／`village`／`town`／`road` → **chapter**（兼 Ken **Pack-A** 氛圍曲）
   - 新增 `packs.pack_a`：Xiaobai 三態／找碴圖／sfx+bgm 路徑約定（`ships_via: chapter`）
2. **`export_presets.cfg`**（`measure_bundle.py --apply-presets`）
   - **macOS + Android + iOS** → CORE exclude（含上述 BGM + chapter 地圖 + Noto）
   - Windows／Linux → 仍為完整可玩包（只剝 extra 重複檔）
3. **驗收**
   - `test_s8_smoke.gd` → `S8_SMOKE_SUCCESS`（無 Pack-A，cue 靜音占位）
   - `test_bundle.gd` → `BUNDLE_OK`

## Core 現在最大項（下一刀給 Kevin／音質）

| 檔 | MB | 備註 |
|---|---:|---|
| `battle.mp3` | 6.91 | 留 core；壓到 ~96 kbps 約再省 3–4 MB |
| `jf-openhuninn-2.1.ttf` | 4.68 | CJK 主字，暫留 |
| `sky_kingdom_bg.png` | 2.52 | 大廳殿堂；可轉 webp |
| `title_bg_clockwork.png` | 1.78 | 標題；可再壓 |

把 `battle` 壓碼後，含引擎高檔估計有機會進 **≤80 MB** 硬上限。

## 商店可用短句（Mark）

- 首次下載約 **70–85 MB**（引擎視平台；之後章節／配樂另載 Pack-A）。
- 序章 C0＋大廳可離線開玩；缺外掛包時音效／氛圍曲靜音，不擋流程。
- 完整劇情地圖與村莊／道路／標題 BGM 在後續下載包。

## 重跑

```bash
python3 tools/measure_bundle.py
python3 tools/measure_bundle.py --apply-presets
godot --path game --headless -s res://scripts/systems/standard_scene_s8/test_s8_smoke.gd
godot --path game --headless -s res://scripts/systems/test_bundle.gd
```
