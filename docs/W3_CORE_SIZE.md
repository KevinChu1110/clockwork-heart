# W3-F1 · Core 首包量測（給 Mark 商店文案）

> 分支 `w3/core-export`｜對齊 Product Lock §5.2（首次必要下載 50～80 MB）＋ Ken Base／Pack-A

## 實機 Android PCK 量測（Before → After）

- **瘦身前實測**：100,267,068 bytes（**95.62 MB**）
- **瘦身後實測**：51,407,480 bytes（**49.03 MB**）
- **差距 (Δ)**：**−48,859,588 bytes（−46.59 MB，減幅 48.7%）**
- **目標檢驗**：成功壓回 **85 MB 以下**，首包 PCK 實重為 **49.03 MB**（含完整引擎 arm64-v8a 之 Debug APK 僅 **73.59 MB**，完全落入 50–80 MB 規格目標）。

## 源資產量測（`python3 tools/measure_bundle.py`）

| 包 | Before | After | Δ |
|---|---:|---:|---:|
| **core** | **61.45 MB** | **42.03 MB** | **−19.42 MB** |
| chapter | 63.29 MB | 79.45 MB | +16.16 MB（收下從 core 挪出的 BGM） |
| extra | 54.97 MB | 54.97 MB | — |

## 這次動了什麼（瘦身實作措施）

1. **Core 地圖底圖紋理匯入優化（WebP Lossy 0.85）**：
   - 解決主因：原先 Godot 預設以 `compress/mode=0`（Lossless deflate RGBA8）展開，導致高解析度地圖單張 ctex 膨脹至 2.0～4.5 MB（如 `town_bg` 4.45 MB、`road_bg` 3.88 MB）。
   - 調整設定：18 張 core 地圖與標題底圖全面改用 `compress/mode=1`（WebP Lossy）＋ `compress/lossy_quality=0.85`。
   - 體積成效：單張 ctex 全面壓至 **0.17 MB ～ 0.67 MB**（遠低於 1.5 MB 上限），18 張底圖總計從 ~49 MB 壓至 **7.71 MB**。
   - 畫質驗收：100% 保留原始解析度（如 3600×2025、3200×1800），跑實機截圖（`screenshots/maps_proof/`）檢驗村莊、大路、城鎮三場景，線條與色彩層次完好，無塊狀噪點或色階斷層。
2. **`battle.mp3` 音訊轉碼降位元率**：
   - C0 教學戰 BGM 由 181 kbps 重新壓碼為 96 kbps MP3。
   - 檔案由 7.24 MB 降至 **3.65 MB**，BGM 測試（`test_bgm.gd`）與 loops 循環點（96.8s）驗證全綠。
3. **排除非執行期雜檔**：
   - 在 `tools/measure_bundle.py` 之 `ALWAYS_EXCLUDE` 加入 `extension_api.json` 與 `screenshots/**`，防範 6.96 MB 之 API dump 與除錯截圖誤包入 PCK。

## Android `core.pck` 內前 30 大檔案清單

| # | 檔案路徑 | Bytes | MB | 說明 |
|---|---|---:|---:|---|
| 1 | `icudt_godot.dat` | 4,797,472 | 4.58 | Godot 內建 ICU 國際化字元庫 |
| 2 | `.godot/imported/battle.mp3-f37b9f915db4c3f4b74f392ce2c64361.mp3str` | 3,823,975 | 3.65 | C0 教學戰 BGM（96 kbps 壓碼） |
| 3 | `.godot/imported/jf-openhuninn-2.1.ttf-377f09d2af790a8e912350957b0ff552.fontdata` | 3,382,963 | 3.23 | 粉圓體 CJK 核心字型 |
| 4 | `.godot/imported/fox_three_sizes.png-34678dbd870744d49821d0dc54c0015a.ctex` | 1,002,108 | 0.96 | 角色紙娃娃/種族貼圖 |
| 5 | `.godot/imported/soul_result_card.png-c404e62a5a3410f8c49c68084c8bc11b.ctex` | 896,294 | 0.85 | 聚魂抽卡卡片底圖 |
| 6 | `.godot/imported/lion_three_sizes.png-c373336ddc6e557eb6546c0ba0cdd757.ctex` | 863,416 | 0.82 | 角色紙娃娃/種族貼圖 |
| 7 | `.godot/imported/rabbit_base.png-de44c691b4b8b33f312031c69b5b34fa.ctex` | 718,716 | 0.69 | 角色紙娃娃/種族貼圖 |
| 8 | `.godot/imported/xiaobai_base.png-47f08f9433a6b73e78a44acee6b56806.ctex` | 718,716 | 0.69 | 角色紙娃娃/種族貼圖 |
| 9 | `.godot/imported/road_ruins_bg.webp-bdbe5f4dc9cb1ed683b7d31786d34ab7.ctex` | 707,624 | 0.67 | 地圖底圖（ctex Lossy 0.85） |
| 10 | `.godot/imported/pig_three_sizes.png-1e7d87479594f53cb9c46edae5916f1b.ctex` | 686,706 | 0.65 | 角色紙娃娃/種族貼圖 |
| 11 | `.godot/imported/xiaobai_three_sizes.png-8139da1256eec49c952bd12ee1de505e.ctex` | 681,892 | 0.65 | 角色紙娃娃/種族貼圖 |
| 12 | `.godot/imported/town_bg.webp-f0ea3f8c0cc1ba5b756f43d08af870ab.ctex` | 613,952 | 0.59 | 地圖底圖（ctex Lossy 0.85） |
| 13 | `.godot/imported/outfits_x4.png-70abb10f8b3969558a3fa7e5af3b5f6a.ctex` | 577,646 | 0.55 | 外觀服裝圖集 |
| 14 | `.godot/imported/road_bridge_bg.webp-e489a475224eec9b2566998168171c3c.ctex` | 563,066 | 0.54 | 地圖底圖（ctex Lossy 0.85） |
| 15 | `.godot/imported/town_forge_bg.webp-a8b8de66c0498524dab65fa06876b63b.ctex` | 556,584 | 0.53 | 地圖底圖（ctex Lossy 0.85） |
| 16 | `.godot/imported/town_market_bg.webp-778f38aa05db224483244948cb546e0b.ctex` | 536,262 | 0.51 | 地圖底圖（ctex Lossy 0.85） |
| 17 | `.godot/imported/town_tutor_bg.webp-0e6d4d9ca14d5f2faafba6e5b5d4b826.ctex` | 525,036 | 0.50 | 地圖底圖（ctex Lossy 0.85） |
| 18 | `.godot/imported/village_mill_bg.webp-a1267e22b3a07ee4c36da964393d6a91.ctex` | 512,792 | 0.49 | 地圖底圖（ctex Lossy 0.85） |
| 19 | `.godot/imported/codex_icons_x4.png-f0c186bac915dd73774cbc1a529b01fc.ctex` | 508,594 | 0.49 | 圖鑑圖示集 |
| 20 | `.godot/imported/town_gem_bg.webp-979b35f3224e0827f246c5bce05a7d1a.ctex` | 476,860 | 0.45 | 地圖底圖（ctex Lossy 0.85） |
| 21 | `.godot/imported/road_inn_bg.webp-3f24c84b1701891f26a6f0c9f2912aa1.ctex` | 467,962 | 0.45 | 地圖底圖（ctex Lossy 0.85） |
| 22 | `.godot/imported/town_sewers_bg.webp-00aa8aad92f8437aa265d4d91ac4014c.ctex` | 459,394 | 0.44 | 地圖底圖（ctex Lossy 0.85） |
| 23 | `.godot/imported/town_soul_bg.webp-e35bcd96952bebb85e66accec48a2d7a.ctex` | 456,942 | 0.44 | 地圖底圖（ctex Lossy 0.85） |
| 24 | `.godot/imported/village_grave_bg.webp-b4cf09576334839ea81a40de2b63f1e9.ctex` | 412,164 | 0.39 | 地圖底圖（ctex Lossy 0.85） |
| 25 | `.godot/imported/barracks_yard_bg.webp-0ec4e0238c70a0aa6edcdbb48114aaad.ctex` | 375,524 | 0.36 | 地圖底圖（ctex Lossy 0.85） |
| 26 | `.godot/imported/village_cave_bg.webp-124e4d8fea7d92130b4756b75bd66acb.ctex` | 352,308 | 0.34 | 地圖底圖（ctex Lossy 0.85） |
| 27 | `.godot/imported/village_bg.webp-e2e2ce6f0484b9132637c56de2347836.ctex` | 339,184 | 0.32 | 地圖底圖（ctex Lossy 0.85） |
| 28 | `.godot/imported/road_bg.webp-68ef9a9b3d3bad079da55eabfcf21938.ctex` | 329,704 | 0.31 | 地圖底圖（ctex Lossy 0.85） |
| 29 | `.godot/imported/lion_base.png-9e6981aaa948abf7e9f22dce6e5e98d0.ctex` | 308,226 | 0.29 | 角色紙娃娃/種族貼圖 |
| 30 | `.godot/imported/dismantle_pull.png-249e5a3d1747733a965cbe59b4175fb2.ctex` | 276,882 | 0.26 | 拆解部位 UI 特效 |

## 商店可用短句（Mark）

- 首次下載約 **50–75 MB**（包含完整引擎與 C0/大廳內容；之後章節／配樂另載 Chapter Pack）。
- 序章 C0＋大廳可離線開玩；缺外掛包時音效／氛圍曲靜音，不擋流程。
- 完整劇情地圖與村莊／道路／標題 BGM 在後續章節下載包。

## 重跑驗證指令

```bash
python3 tools/measure_bundle.py --apply-presets
python3 tools/build_bundles.py --export
python3 tools/list_pck.py dist/android/core.pck
godot --path game --headless --quit-after 3
godot --path game --headless -s res://scripts/systems/test_bundle.gd
godot --path game --headless -s res://scripts/systems/test_full_bundle_flow.gd
bash tools/run_three_maps_proof.sh
```
