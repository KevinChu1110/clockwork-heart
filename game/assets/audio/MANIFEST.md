# Audio Manifest

## SFX (`sfx/`)
Procedural one-shots for combat / UI。**全部都還是程式合成的占位**，要換真錄音。

入口只有一個：`AudioManager.play(key, pitch_scale=1.0, volume_db=0.0)`。
- 缺檔不會當，第一次播到時 `push_warning` 一次。
- 同時最多 **2 聲**（`MAX_SFX_VOICES`）；滿了搶優先度最低、同級最舊的那聲（`SFX_PRIORITY`）。
- 所有 SFX 一律一次性，不循環（`warn` 匯入設定也鎖成 loop disabled）。

| key | 用途（任務書 §5） | 長度 | 備註 |
|-----|------------------|------|------|
| swap | 換欄那一拍的金屬卡榫 | 0.22 s | **占位**，`python3 tools/gen_sfx_swap.py` 合成 |
| hit / slash | 命中／斬擊 | 0.12 / 0.16 s | 規格 < 0.3 s |
| break | 部位碎裂（接 0.4 秒慢動作） | 0.20 s | |
| warn | Boss 部位將破時一聲，一次性 | 0.10 s | 不是格擋窗 |
| wind | **只在戰前上鏈**（`play_wind_up`／`battle_start`） | 0.25 s | 戰鬥中的風刃改用 slash |
| parry | 只可當「彈開」自動演出（`on_battle_event`） | 0.18 s | **不可**綁按鈕或 UI 提示 |
| ui / reveal / victory / defeat | 沿用 | | UI 提示只准 `UI_SFX`（ui／interact／reveal） |

## BGM (`bgm/`) · 八個 cue（2026-10 依任務書收斂）

遊戲只播這八個：**title、village、town、road、forest、battle、boss、ending**。
其他地區在 `AudioManager.map_to_bgm` 併過去（舊 id 呼叫 `play_bgm("mist")` 也會被 `resolve_bgm_cue` 接住）：

| 舊區 | 併到 | 理由 |
|------|------|------|
| dojo* | town | 有人煙的據點 |
| wild*／hunting_grounds | road | 開闊戶外、趕路 |
| coast* | road | 同上 |
| mist* | forest | 霧、神祕地帶 |
| tower*／blackflame_scar | forest | 同上 |

循環：ending 只播一次（勝利結算）；其餘七首都循環，`.mp3.import` 也一律開 loop，loop_offset 與 `loops.json` 相同。
town 在程式裡再壓 −2 dB（任務書：音量低於 village）。

### 2026-10-06 · 佔位曲裁成 brief 長度（issue #31）

重新作曲規格見 [docs/BGM_SPEC.md](../../../docs/BGM_SPEC.md)。現在的八首是**從下面 Suno 佔位曲剪出來的**，
只做裁切、調速不變調（±7 % 內）、檔尾交叉淡化成無縫循環、響度對齊，沒有用付費生成。
重現：`python3 tools/cut_bgm_loops.py --out /tmp/bgm_cut`（原曲從 git blob 取，見工具內 `SOURCE_BLOBS`）。

| cue | 長度 | loop_offset | 響度／true peak | 來源 |
|-----|------|-------------|-----------------|------|
| title | 24.0 s | 6.727 s | −16.00 LUFS／−4.13 dBTP | Suno title 0.00–23.70 s＋程式合成發條棘輪聲（本 repo 自產） |
| village | 45.0 s | 0 | −16.00／−4.64 | Suno village 36.69–80.32 s |
| town | 40.0 s | 0 | −16.00／−1.79 | Suno town 41.63–79.13 s |
| road | 30.0 s | 0 | −16.00／−2.88 | Suno road 110.09–139.42 s |
| forest | 40.0 s | 0 | −15.99／−1.91 | Suno forest 38.01–80.65 s |
| battle | 35.0 s | 0 | −15.99／−1.84 | Suno battle 181.05–218.45 s |
| boss | 40.0 s | 0 | −16.00／−2.70 | Suno boss 206.66–245.81 s |
| ending | 16.0 s | 不循環 | −16.00／−2.34 | Suno ending 255.84 s–結尾 |

授權：沿用原本 Suno 佔位曲（帳號見 `SUNO_SOURCES.json`），沒有引入新的外部音源；發條棘輪聲是 numpy 合成。
分析時用了 librosa（ISC）與 demucs（MIT）做節拍／人聲偵測，兩者都只在本機分析、不進成品，也不是 repo 相依。

`mist`／`dojo`／`coast`／`wild`／`tower` 的 .mp3／.wav 已沒有程式引用，留著待確認後再刪。

### 舊表 · 地區差異化編曲（程式合成 .wav 後備）

每首有獨立 **鼓型／主奏音色／和弦／BPM／EQ**，聽感不該再「全部一個樣」。

| id | 地區感 | BPM | 主奏 | 鼓 | 特徵 |
|----|--------|-----|------|----|------|
| title | 英雄主題 | 118 | brass | drive | 辨識度最高 |
| village | 發條新村 | 92 | flute | 無 | 溫暖、慢、木笛 |
| town | 騎士堡 | 112 | horn | 軍鼓 march | 行進號角 |
| road | 荒路 | 108 | pulse | soft | 趕路步伐 |
| wild | 荒野 | 120 | pulse | drive | 不安 Phrygian |
| mist | 霧隱 | 72 | choir | 無 | 稀疏長音 |
| dojo | 道場 | 126 | pulse | march | 短促打擊 |
| forest | 森林 | 98 | bell | soft | 鐘／琶音 |
| coast | 海岸 | 104 | flute | soft | 浪湧低頻 |
| battle | 雜魚戰 | 148 | power | battle | 最密最快 |
| boss | Boss | 128 | power | battle | 厚重儀式 |
| tower | 塔 | 88 | choir | soft | 低沉 |
| ending | 終章 | 96 | brass | soft | 收束大調 |

重產合成 WAV：`python3 tools/gen_bgm.py`  
烤成可替換壓縮曲＋循環：`python3 tools/bake_placeholder_bgm.py`  
Suno／外部成品：`python3 tools/import_bgm.py <file> --id <曲目>`  

優先順序：`.ogg`／`.mp3`（真配樂槽）→ `.wav`（程式合成後備）。

### 2026-08-21 · Suno 真曲已入庫
帳號 `guanrung1110` 產的 `bravesoul_*` 已下載並 `import_bgm` 覆蓋 13 首。  
來源 uuid 見 `SUNO_SOURCES.json`。多數曲循環相似度偏低（Suno 歌曲結構），若聽得出接縫可再產 loopable 版或手動 `--loop-offset`。
