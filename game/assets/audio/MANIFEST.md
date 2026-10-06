# Audio Manifest

## SFX (`sfx/`) · 錄製／重做清單（issue #32）

依據：`docs/CLOCKWORK_ART_MUSIC_BRIEF.md` §5。世界是**發條八音盒＋輕管弦**，不是動作遊戲；
音效只負責「看懂自動戰鬥」，**不做成「請玩家按」的提示**。

入口只有一個：`AudioManager.play(key, pitch_scale=1.0, volume_db=0.0)`（介面不變）。
- 缺檔不會當，第一次播到時 `push_warning` 一次。
- 同時最多 **2 聲**（`MAX_SFX_VOICES`）；滿了搶優先度最低、同級最舊的那聲（`SFX_PRIORITY`）。
- 所有 SFX 一律一次性，**不循環**（`warn` 匯入設定也鎖成 loop disabled）。
- 檔案：`game/assets/audio/sfx/<key>.wav`，snake_case 英文、沿用既有 key 檔名，mono 16-bit PCM。

### 響度規格（SFX 一體）

短音效（多數 < 0.4 秒）量不到 EBU R128 的 integrated（閘門要 400 ms 區塊，量出來都是 −70），
所以 SFX 統一用 **最大瞬時響度 M-max（400 ms 視窗）**，量之前在檔尾補 1 秒靜音，
讓短於 400 ms 的音也有完整視窗（等於把能量平均到 400 ms，越短越小聲，正好符合「短促不搶戲」）。
峰值一律用 **true peak（4× 超取樣）≤ −1 dBTP**。

| 層級 | key | M-max 目標 | 理由 |
|------|-----|-----------|------|
| 事件 cue | swap、break、warn | −18 LUFS（±1） | 一場只響幾次、要聽得出「發生事了」 |
| 頻繁回饋 | hit、slash | −21 LUFS（±1） | 每次命中都會響、和跳字同一瞬間，比事件 cue 低 3 LU，不蓋過跳字 |
| 戰前 | wind | −20 LUFS（±1） | 戰前上鏈，和 battle BGM 起頭疊在一起，不要搶 |

對照：BGM 檔是 −16 LUFS integrated，遊戲內 BGM 匯流排 −5 dB、SFX 匯流排 −4 dB
（`_bgm_db`／`_sfx_db`），所以事件 cue 在遊戲裡約 −22 LUFS M-max、BGM 約 −21 LUFS，同一個量級。

量測指令（每個檔都要過）：

```bash
ffmpeg -nostats -i x.wav -af "apad=pad_dur=1,ebur128=peak=true" -f null - 2>&1 \
  | awk '/M:/{for(i=1;i<=NF;i++) if($i=="M:" && $(i+1)+0>m) m=$(i+1)} END{print "M-max",m}'
#  summary 的 Peak: 就是 true peak（dBTP）
```

### 清單（每個 key）

來源：**合成**＝本 repo 的免費 numpy 合成腳本；**舊占位**＝`tools/gen_sfx_and_tiles.py` 早期純 python 合成（遊戲感方波，待重做）；
**授權**＝外部免費音源（目前沒有）。優先順序：P0 本 issue 先做、P1 下一輪、P2 有空再做。

| key | 用途（誰觸發） | 目標長度 | 質感描述 | 目前來源 | 優先 |
|-----|---------------|---------|---------|---------|-----|
| swap | 換欄那一拍（`weapon_swap`）：次數用完自動換下一欄 | 0.20–0.28 s（< 0.3） | 黃銅卡榫：兩下棘輪「喀喀」＋一聲扣入的「卡」，帶一點機身低頻，乾、不拖尾 | 合成占位 `tools/gen_sfx_swap.py`（#16）→ 重做中 | P0 |
| hit | 一般命中（`hit`、幻影命中） | 0.12–0.20 s（< 0.3） | 錫皮玩具被敲：短「咚」機身＋錫片非諧波「噹」，不要肉擊、不要爆炸 | 舊占位 → 重做中 | P0 |
| slash | 斬擊／技能命中（`skill_hit`、`skill_cast`、風刃） | 0.18–0.26 s（< 0.3） | 黃銅刃劃過：快掃的空氣聲＋細細一聲「鏘」金屬尾音 | 舊占位 → 重做中 | P0 |
| break | 部位碎裂（`part_break`、熊貓破防、鍛造摔錘），接 0.4 秒慢動作 | 0.55–0.70 s | 先一聲脆裂（板件崩開），再接齒輪／螺絲散落的叮噹與一聲鬆掉的彈簧，尾巴在 0.4 秒慢動作裡收乾淨 | 舊占位 → 重做中 | P0 |
| warn | Boss 部位將破時一聲（戰鬥端直接 `play("warn")`，AudioManager 不自動播） | 0.35–0.50 s | 發條繃緊的金屬吱一聲＋一記玻璃鐘「叮」，一次就好，不是倒數、不是嗶嗶警報、不是格擋窗 | 舊占位 → 重做中 | P0 |
| wind | **只在戰前上鏈**（`battle_start` → `play_wind_up`） | 0.80–1.00 s | 發條鑰匙轉三四格：棘輪喀喀一格比一格緊、音高微升，最後一聲到位 | 舊占位 → 重做中 | P0 |
| parry | **只可當「彈開」自動演出**（`perfect_parry` 等），**不可綁按鈕或 UI 提示** | 0.15–0.25 s | 金屬彈開的一聲「叮」，短 | 舊占位 | P1 |
| victory | 勝利（`battle_end(true)`），後面接 ending BGM | 0.6–1.2 s | 八音盒三音上行，溫暖、不浮誇 | 舊占位 | P1 |
| defeat | 落敗（`battle_end(false)`） | 0.6–1.2 s | 發條停擺：音盒走慢、音高下滑 | 舊占位 | P1 |
| reveal | 抽魂／聚魂揭曉、霧中現形、UI 揭曉 | 0.3–0.6 s | 鐘琴閃一下，亮 | 舊占位 | P1 |
| ui | UI 點擊（`play_ui`） | 0.04–0.08 s | 木質小按鍵「嗒」，很輕 | 舊占位 | P1 |
| battle_start | `wind` 缺檔時的上鏈後備 | 0.2–0.4 s | 同 wind 但短 | 舊占位 | P2 |
| clash | 王斬命中、野豬破甲、炸彈 | 0.12–0.20 s | 厚重金屬對撞 | 舊占位 | P1 |
| interact | 探索互動 | 0.06–0.10 s | 木盒開扣 | 舊占位 | P2 |
| clock | 環境危險預警／蓄力（刻意不用 warn） | 0.05–0.10 s | 低一點的發條滴答 | 舊占位 | P2 |
| stop | 隼停時 | 0.15–0.25 s | 指針卡住 | 舊占位 | P2 |
| rock | 落石、野豬甲再生 | 0.15–0.25 s | 木石碰撞 | 舊占位 | P2 |
| fire | 火環命中 | 0.3–0.4 s | 小火苗噗 | 舊占位 | P2 |
| dodge | 危險閃過 | 0.08–0.12 s | 輕掃 | 舊占位 | P2 |
| step | 探索腳步（優先度 0） | 0.04–0.06 s | 木地板輕踏 | 舊占位 | P2 |
| craft | 鍛造成功（可選，缺檔走 ui＋reveal） | 0.3–0.5 s | 小錘敲黃銅 | **缺檔** | P2 |
| miss | `battle_view.gd` 揮空時 `play("miss")`，但不在 `SFX_KEYS`，目前只會警告 | — | 舊格擋流程用；任務書已拿掉格擋，建議跟著刪呼叫 | **缺檔** | — |

### 重產（重做完成後生效）

```bash
python3 tools/gen_sfx_clockwork.py            # 重產 P0 六個（swap hit slash break warn wind）
python3 tools/gen_sfx_clockwork.py hit warn   # 只重產指定的
python3 tools/gen_sfx_clockwork.py --measure  # 只量，不寫檔
godot --path game --headless --import         # 換了音檔後匯入一次（只 commit 對應的 .wav.import）
```

`tools/gen_sfx_and_tiles.py` 會跳過上面六個 key，不會把它們蓋回舊占位。
付費生成（錄音室、AI 音效）一律先問 KC；目前全部是免費合成。

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
