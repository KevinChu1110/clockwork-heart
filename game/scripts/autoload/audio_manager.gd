extends Node
## 音效池 + BGM 循環（淡入淡出切曲）

const SFX_DIR := "res://assets/audio/sfx"
const BGM_DIR := "res://assets/audio/bgm"
## 循環起點（秒）。真配樂通常有一段不該重複的前奏，循環要從前奏之後開始。
## 由 tools/import_bgm.py 產生，見 docs/MEDIA.md
const BGM_LOOPS_PATH := "res://assets/audio/bgm/loops.json"
## 任務書 §5：同一回合最多兩個 SFX 疊加。超過時丟掉優先度最低、同優先度丟最舊的。
const MAX_SFX_VOICES := 2
const POOL_SIZE := MAX_SFX_VOICES
const BGM_FADE := 1.1  ## 切曲更柔，少「突然換帶」

## ─── BGM cue（docs/CLOCKWORK_ART_MUSIC_BRIEF.md §5、§6）───
## 檔名只准這八個。其他地區（mist／dojo／coast／tower／wild…）一律在 map_to_bgm 併進來。
const BGM_CUES: Array[String] = [
	"title", "village", "town", "road", "forest", "battle", "boss", "ending",
]
## 只播一次、不循環的 cue（ending＝勝利結算 16 秒）。其餘地區曲循環，免得走路走到沒聲音。
const BGM_ONESHOT: Array[String] = ["ending"]
## 舊曲目 id → 八 cue。main.gd 還有直接 play_bgm("mist") 之類的舊呼叫，在這裡接住。
const BGM_LEGACY_ALIAS := {
	"mist": "forest", "dojo": "town", "coast": "road", "wild": "road", "tower": "forest",
}
## 個別 cue 的音量微調（dB）。任務書：town 音量低於 village。
const BGM_CUE_GAIN_DB := {"town": -2.0}

## ─── SFX ───
## 預載的音效 key。檔案在 sfx/<key>.wav；缺檔不會當，播的時候警告一次。
const SFX_KEYS: Array[String] = [
	"parry", "hit", "slash", "fire", "wind", "rock", "clock",
	"reveal", "break", "stop", "clash", "victory", "defeat",
	"ui", "interact", "step", "warn", "dodge", "battle_start",
	"swap",
	"craft",  ## 可選；缺檔時 play_craft_success 走 ui+reveal
]
## 戰鬥自動回饋一定要有的 key（battle HUD 直接呼叫 AudioManager.play(key)）
const SFX_REQUIRED: Array[String] = ["swap", "break", "warn", "hit", "slash"]
## 還是程式合成的占位音效（要換真錄音）。swap 是 tools/gen_sfx_swap.py 合成的。
const SFX_PLACEHOLDER: Array[String] = [
	"swap", "hit", "slash", "break", "warn", "wind", "parry", "ui", "reveal",
	"victory", "defeat", "clash", "clock", "battle_start",
]
## UI／操作提示只准用這些。parry 不可綁按鈕（任務書 §5），只能當自動彈開演出。
const UI_SFX: Array[String] = ["ui", "interact", "reveal"]
## 按鈕點擊／操作提示走自己的一個 UI 聲道，不算進戰鬥 SFX 的兩聲上限（#63）：
## 戰鬥中破壞、換武、勝利音正響時，按暫停／結算按鈕照樣要有回饋。
## reveal 是演出音（觀星、迷霧揭開），仍走一般池子搶位置。
const UI_VOICE_SFX: Array[String] = ["ui", "interact"]
## 撞上兩聲上限時誰留下：數字大的贏；沒列的＝1
const SFX_PRIORITY := {
	"break": 4, "victory": 4, "defeat": 4,
	"warn": 3, "swap": 3, "wind": 3, "battle_start": 3,
	"hit": 2, "slash": 2, "clash": 2, "reveal": 2,
	"step": 0,
}

var _streams: Dictionary = {}  ## sfx id -> AudioStream
var _bgm_streams: Dictionary = {}  ## bgm id -> AudioStream
var _bgm_loops: Dictionary = {}  ## bgm id -> 循環起點（秒）
var _bgm_sources: Dictionary = {}  ## bgm id -> "ogg" | "wav"
var _pool: Array = []  ## AudioStreamPlayer（數量＝MAX_SFX_VOICES）
var _voice_prio: Array[int] = []  ## 每個 voice 目前播的優先度
var _voice_serial: Array[int] = []  ## 每個 voice 開播序號（越小越舊）
var _serial: int = 0
var _ui_voice: AudioStreamPlayer  ## UI_VOICE_SFX 專用，新的點擊直接接替上一聲
var _missing_sfx_warned: Dictionary = {}  ## 已警告過的缺檔 key，每個只警告一次
var _sfx_db: float = -4.0
var _bgm_db: float = -5.0  ## 悠揚版略抬一點，仍避免蓋過 SFX
var _muted: bool = false
var _bgm_muted: bool = false
var _step_cd: float = 0.0

var _bgm_a: AudioStreamPlayer
var _bgm_b: AudioStreamPlayer
var _bgm_active: AudioStreamPlayer
var _current_bgm: String = ""
var _fade_tween: Tween


func _ready() -> void:
	_build_pool()
	_build_bgm_players()
	_preload_sfx()
	_preload_bgm()


func _process(delta: float) -> void:
	if _step_cd > 0.0:
		_step_cd = maxf(0.0, _step_cd - delta)


func _build_pool() -> void:
	for i in POOL_SIZE:
		var p := AudioStreamPlayer.new()
		p.name = "SfxPool_%d" % i
		p.bus = "Master"
		add_child(p)
		_pool.append(p)
		_voice_prio.append(-1)
		_voice_serial.append(0)
	_ui_voice = AudioStreamPlayer.new()
	_ui_voice.name = "SfxUi"
	_ui_voice.bus = "Master"
	add_child(_ui_voice)


func _build_bgm_players() -> void:
	_bgm_a = AudioStreamPlayer.new()
	_bgm_a.name = "BgmA"
	_bgm_a.bus = "Master"
	add_child(_bgm_a)
	_bgm_b = AudioStreamPlayer.new()
	_bgm_b.name = "BgmB"
	_bgm_b.bus = "Master"
	add_child(_bgm_b)
	_bgm_active = _bgm_a


func _preload_sfx() -> void:
	for n in SFX_KEYS:
		var path := "%s/%s.wav" % [SFX_DIR, n]
		if not ResourceLoader.exists(path):
			continue
		var s: Variant = load(path)
		## 音效一律一次性（warn 尤其不能循環）：匯入設定若誤開循環，這裡關掉
		if s is AudioStreamWAV and (s as AudioStreamWAV).loop_mode != AudioStreamWAV.LOOP_DISABLED:
			var w := (s as AudioStreamWAV).duplicate() as AudioStreamWAV
			w.loop_mode = AudioStreamWAV.LOOP_DISABLED
			s = w
		if s is AudioStream:
			_streams[n] = s


## 這個 key 有沒有載到音檔（測試／呼叫端自檢用）
func has_sfx(id: String) -> bool:
	return _streams.has(id)


func sfx_ids() -> Array:
	return _streams.keys()


func sfx_voice_limit() -> int:
	return MAX_SFX_VOICES


## UI 聲道是否正在響（測試／自檢用）
func ui_sfx_playing() -> bool:
	return _ui_voice != null and _ui_voice.playing


## 目前同時在響的戰鬥／演出 SFX 數（≤ MAX_SFX_VOICES；不含 UI 聲道）
func active_sfx_count() -> int:
	var n := 0
	for p in _pool:
		if (p as AudioStreamPlayer).playing:
			n += 1
	return n


func bgm_ids() -> Array:
	return BGM_CUES.duplicate()


## 哪些曲子已經換成真配樂（面板／測試用）
func bgm_source(id: String) -> String:
	return str(_bgm_sources.get(id, ""))


func _load_bgm_loops() -> void:
	_bgm_loops = {}
	if not FileAccess.file_exists(BGM_LOOPS_PATH):
		return
	var f := FileAccess.open(BGM_LOOPS_PATH, FileAccess.READ)
	if f == null:
		return
	var data: Variant = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		push_warning("BGM loops.json 格式不對，忽略")
		return
	for k in (data as Dictionary):
		_bgm_loops[str(k)] = float((data as Dictionary)[k])


func _preload_bgm() -> void:
	_load_bgm_loops()
	for n in bgm_ids():
		var stream := _load_bgm_stream(str(n))
		if stream == null:
			push_warning("BGM missing: %s/%s.(ogg|wav)" % [BGM_DIR, n])
			continue
		_bgm_streams[n] = stream


## 真配樂（.ogg／.mp3）優先；程式合成的 .wav 是後備，所以換曲只要丟檔案不用改程式。
## 兩種壓縮格式都收，是因為不是每台機器的 ffmpeg 都編得出 Vorbis。
func _load_bgm_stream(id: String) -> AudioStream:
	for ext in ["ogg", "mp3"]:
		var path := "%s/%s.%s" % [BGM_DIR, id, ext]
		if not ResourceLoader.exists(path):
			continue
		var s: Variant = load(path)
		if s == null:
			continue
		_bgm_sources[id] = ext
		var off := maxf(0.0, float(_bgm_loops.get(id, 0.0)))
		var looped := bgm_loops(id)
		## duplicate：避免改到匯入快取本體，循環設定才穩定
		if s is AudioStreamOggVorbis:
			var v := (s as AudioStreamOggVorbis).duplicate() as AudioStreamOggVorbis
			v.loop = looped
			v.loop_offset = off
			return v
		if s is AudioStreamMP3:
			var m := (s as AudioStreamMP3).duplicate() as AudioStreamMP3
			m.loop = looped
			m.loop_offset = off
			return m
		if s is AudioStream:
			return s

	var wav_path := "%s/%s.wav" % [BGM_DIR, id]
	if not ResourceLoader.exists(wav_path):
		return null
	var stream: Variant = load(wav_path)
	if stream is AudioStreamWAV:
		var w := (stream as AudioStreamWAV).duplicate() as AudioStreamWAV
		w.loop_mode = AudioStreamWAV.LOOP_FORWARD if bgm_loops(id) else AudioStreamWAV.LOOP_DISABLED
		w.loop_begin = 0
		var bytes_per := 2  ## 16-bit PCM
		if w.format == AudioStreamWAV.FORMAT_8_BITS:
			bytes_per = 1
		elif w.format == AudioStreamWAV.FORMAT_IMA_ADPCM:
			bytes_per = 1
		var ch := 2 if w.stereo else 1
		var frames := 0
		if bytes_per * ch > 0 and w.data.size() > 0:
			frames = int(w.data.size() / (bytes_per * ch))
		w.loop_end = maxi(1, frames)
		_bgm_sources[id] = "wav"
		return w
	if stream is AudioStream:
		_bgm_sources[id] = "wav"
		return stream
	return null


## 這個 cue 要不要循環（ending 只播一次）
func bgm_loops(id: String) -> bool:
	return not BGM_ONESHOT.has(id)


func _bgm_target_db(id: String) -> float:
	return _bgm_db + float(BGM_CUE_GAIN_DB.get(id, 0.0))


func set_muted(v: bool) -> void:
	_muted = v
	if v:
		stop_bgm(0.2)


func set_bgm_muted(v: bool) -> void:
	_bgm_muted = v
	if v:
		stop_bgm(0.3)
	elif _current_bgm != "":
		var id := _current_bgm
		_current_bgm = ""
		play_bgm(id)


## SFX 唯一入口：AudioManager.play(key, pitch_scale, volume_db)
## 缺檔不會當，只在第一次播到時 push_warning 一次。
## 同時最多 MAX_SFX_VOICES 聲；滿了就搶優先度最低（同級搶最舊）的那聲，搶不到就丟掉新的。
## UI_VOICE_SFX（ui／interact）例外：走專屬 UI 聲道，不搶也不被搶。
func play(id: String, pitch_scale: float = 1.0, volume_db: float = 0.0) -> void:
	if _muted:
		return
	var stream: AudioStream = _streams.get(id)
	if stream == null:
		if not _missing_sfx_warned.has(id):
			_missing_sfx_warned[id] = true
			push_warning("SFX missing: %s/%s.wav（之後不再提示）" % [SFX_DIR, id])
		return
	if UI_VOICE_SFX.has(id) and _ui_voice != null:
		_ui_voice.stop()
		_ui_voice.stream = stream
		_ui_voice.pitch_scale = clampf(pitch_scale, 0.5, 2.0)
		_ui_voice.volume_db = _sfx_db + volume_db
		_ui_voice.play()
		return
	if _pool.is_empty():
		return
	var prio := int(SFX_PRIORITY.get(id, 1))
	var slot := _pick_voice(prio)
	if slot < 0:
		return
	var p: AudioStreamPlayer = _pool[slot]
	p.stop()
	p.stream = stream
	p.pitch_scale = clampf(pitch_scale, 0.5, 2.0)
	p.volume_db = _sfx_db + volume_db
	p.play()
	_serial += 1
	_voice_prio[slot] = prio
	_voice_serial[slot] = _serial


## 空的 voice 優先；全滿就挑「優先度最低、同級最舊」的；新的優先度更低就回 -1（丟掉）
func _pick_voice(prio: int) -> int:
	var victim := -1
	for i in _pool.size():
		var p: AudioStreamPlayer = _pool[i]
		if not p.playing:
			return i
		if victim < 0 or _voice_prio[i] < _voice_prio[victim] \
				or (_voice_prio[i] == _voice_prio[victim] and _voice_serial[i] < _voice_serial[victim]):
			victim = i
	if victim >= 0 and prio >= _voice_prio[victim]:
		return victim
	return -1


func play_step() -> void:
	if _step_cd > 0.0:
		return
	_step_cd = 0.28
	play("step", randf_range(0.92, 1.08), -6.0)


func play_ui() -> void:
	play("ui", 1.0, -2.0)


## 戰前上鏈。wind 只在這裡用（任務書 §5），戰鬥中不要拿來當風刃。
func play_wind_up() -> void:
	if _streams.has("wind"):
		play("wind")
	else:
		play("battle_start")


func play_interact() -> void:
	play("interact")


## 鍛造成功記憶點：有 craft.wav 用專檔，否則 ui + reveal 疊層
func play_craft_success() -> void:
	if _streams.has("craft"):
		play("craft")
	else:
		play("ui", 1.05, -1.0)
		play("reveal", 1.12, -2.0)


## 觀星成功：reveal 為主、輕 ui 點綴
func play_ritual_success() -> void:
	play("reveal", 0.95)
	play("ui", 1.18, -5.0)


## ─── BGM ───

func play_bgm(id: String, fade: float = BGM_FADE) -> void:
	if id == "":
		return
	id = resolve_bgm_cue(id)
	var target_db := _bgm_target_db(id)
	if _bgm_muted or _muted:
		_current_bgm = id
		return
	## 同曲且已在播 → 不重切（避免選單重建時靜音）
	## 例外：戰鬥結束會把音量壓低，回探索同曲時要拉回，否則會一直「悶聲」
	if id == _current_bgm and _bgm_active and _bgm_active.playing:
		if _bgm_active.volume_db < target_db - 1.0:
			if _fade_tween and is_instance_valid(_fade_tween):
				_fade_tween.kill()
			_fade_tween = create_tween()
			_fade_tween.tween_property(_bgm_active, "volume_db", target_db, maxf(0.35, fade * 0.55))
		return
	var stream: AudioStream = _bgm_streams.get(id)
	if stream == null:
		## 熱載一次，避免第一次進遊戲表尚未就緒
		stream = _load_bgm_stream(id)
		if stream != null:
			_bgm_streams[id] = stream
	if stream == null:
		push_warning("BGM not loaded: %s" % id)
		return
	var incoming: AudioStreamPlayer = _bgm_b if _bgm_active == _bgm_a else _bgm_a
	var outgoing: AudioStreamPlayer = _bgm_active

	if _fade_tween and is_instance_valid(_fade_tween):
		_fade_tween.kill()

	incoming.stop()
	incoming.stream = stream
	incoming.volume_db = -40.0
	incoming.play()
	## 下一幀再確認；若仍未播則硬啟
	if not incoming.playing:
		incoming.volume_db = target_db
		incoming.play()
	call_deferred("_ensure_bgm_playing", incoming)

	_fade_tween = create_tween()
	_fade_tween.set_parallel(true)
	_fade_tween.tween_property(incoming, "volume_db", target_db, fade)
	if outgoing and outgoing != incoming and outgoing.playing:
		_fade_tween.tween_property(outgoing, "volume_db", -40.0, fade)
		_fade_tween.chain().tween_callback(func():
			if is_instance_valid(outgoing):
				outgoing.stop()
		)
	_bgm_active = incoming
	_current_bgm = id


func _ensure_bgm_playing(p: AudioStreamPlayer) -> void:
	if p == null or not is_instance_valid(p):
		return
	if not p.playing and p.stream != null and not _muted and not _bgm_muted:
		p.volume_db = _bgm_target_db(_current_bgm)
		p.play()


func stop_bgm(fade: float = BGM_FADE) -> void:
	if _fade_tween and _fade_tween.is_valid():
		_fade_tween.kill()
	var out := _bgm_active
	if out == null or not out.playing:
		_current_bgm = ""
		return
	_fade_tween = create_tween()
	_fade_tween.tween_property(out, "volume_db", -40.0, fade)
	_fade_tween.tween_callback(func():
		if is_instance_valid(out):
			out.stop()
	)
	_current_bgm = ""


func play_bgm_for_map(map_id: String) -> void:
	var id := map_to_bgm(map_id)
	play_bgm(id)


func play_bgm_for_battle(mode: String) -> void:
	if is_boss_battle(mode):
		play_bgm("boss")
	else:
		play_bgm("battle")


## 主線聖獸／魔王／秘境小 Boss 等「有記憶點」的戰
func is_boss_battle(mode: String) -> bool:
	return mode in [
		"leo", "fog", "abo", "demon", "falcon", "boar", "wrath", "tide",
		"statue", "chrono", "scar_lord", "mirror_wraith", "wreck_captain",
	]


## 地圖 id → 八 cue 之一。任務書只留八個名字，舊地區併到最接近的那首：
##   village*                                  → village（八音盒＋雙簧管）
##   town* / barracks_yard / dojo*             → town（有人煙的據點；道場也算聚落）
##   road* / cross* / 商隊／星落原 / wild* / 獵場 / coast* → road（趕路、開闊戶外）
##   forest* / mist* / tower* / 疤地             → forest（豎琴；霧、塔這類神祕地帶）
## 沒對到的（裂縫入口掛在 postgame hub 等）回 town。
static func map_to_bgm(map_id: String) -> String:
	if map_id.begins_with("village"):
		return "village"
	if map_id.begins_with("town") or map_id == "barracks_yard" or map_id.begins_with("dojo"):
		return "town"
	if map_id.begins_with("road") or map_id.begins_with("cross") \
			or map_id in ["caravan_camp", "starfall_plain", "hunting_grounds"] \
			or map_id.begins_with("wild") or map_id.begins_with("coast"):
		return "road"
	if map_id.begins_with("forest") or map_id.begins_with("mist") \
			or map_id.begins_with("tower") or map_id == "blackflame_scar" or map_id.begins_with("scar"):
		return "forest"
	return "town"


## 任何曲目名（八 cue、舊地區 id、地圖 id）→ 八 cue 之一。play_bgm 進來先過這關。
static func resolve_bgm_cue(id: String) -> String:
	if BGM_CUES.has(id):
		return id
	if BGM_LEGACY_ALIAS.has(id):
		return str(BGM_LEGACY_ALIAS[id])
	return map_to_bgm(id)


## 戰鬥事件 → 音效
func on_battle_event(kind: String, data: Dictionary = {}) -> void:
	match kind:
		"perfect_parry":
			play("parry")
		"hit":
			if data.get("king_slash", false):
				play("clash", 0.9)
			else:
				play("hit", randf_range(0.95, 1.05), -2.0)
		"skill_hit":
			if data.get("parry_followup", false):
				play("parry", 1.05)
			else:
				play("slash")
		"skill_cast":
			play("slash", 1.1, -4.0)
		"hazard_warn":
			## warn 只留給「Boss 部位將破」（任務書 §5，由戰鬥端直接 play("warn")）；
			## 這裡改成低一點的發條滴答，聽得出有事但不搶 warn
			var hk := str(data.get("kind", ""))
			play("clock", 1.0 if hk == "time_clock" else 0.85, -6.0)
		"hazard_window":
			play("clock", 1.2)
		"hazard_resolve":
			if bool(data.get("success", false)):
				play("dodge")
			else:
				var hk2 := str(data.get("kind", ""))
				match hk2:
					"fire_ring":
						play("fire")
					"wind_cut":
						## wind 留給戰前上鏈；風刃改用 slash 壓低音高
						play("slash", 0.8, -3.0)
					"rockfall":
						play("rock")
					"bomb":
						play("clash", 0.85)
					"time_clock":
						play("clock", 0.7)
					_:
						play("hit")
		"fog_reveal":
			play("reveal")
		"fog_phantom_hit":
			play("hit", 0.85)
		"abo_guard_break":
			play("break")
		"falcon_stop":
			play("stop")
		"boar_armor_break":
			if data.get("regrow", false):
				play("rock", 0.8)
			else:
				play("clash")
		"king_slash_start":
			## 蓄力同理不用 warn，改低沉滴答
			play("clock", 0.75, -6.0)
		"temptation":
			play("reveal", 0.7, -4.0)
		## 自動戰鬥回饋（任務書 §5）：換欄卡榫、部位碎裂。
		## 「Boss 部位將破」的 warn 不在這裡：戰鬥端自己 play("warn") 一次，AudioManager 不另外播
		"weapon_swap":
			play("swap")
		"part_break":
			play("break")
		_:
			pass


func battle_start(mode: String = "wolf") -> void:
	## 戰前上鏈（wind）。Boss 不再疊 warn——warn 只給部位將破；Boss 感由 boss BGM 負責
	play_wind_up()
	play_bgm_for_battle(mode)


func battle_end(won: bool) -> void:
	if won:
		play("victory")
	else:
		play("defeat")
	## 暫時壓低 BGM，回探索時會由 map 切回
	if _bgm_active and _bgm_active.playing:
		_bgm_active.volume_db = _bgm_target_db(_current_bgm) - 8.0
