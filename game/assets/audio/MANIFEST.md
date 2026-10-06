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

循環：ending 只播一次（勝利結算）；其餘循環，village／battle 的匯入設定也開了 loop。
town 在程式裡再壓 −2 dB（任務書：音量低於 village）。
響度：八首 mp3 都在 −16 LUFS 附近（2026-10-06 量測 −16.4～−15.9）；battle、ending 重做 loudnorm 到 −16 LUFS／−1.5 dBTP。

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
