extends SceneTree
## QA（PR #98 審查）：抽魂五階翻卡音、summon、跳過收音、同時發聲數。
## 需要 PR #98 的 soul_draw_sfx.gd（main 上還沒有）；把這支複製到 #98 分支或其合併結果上跑。
## 執行（不要加 --fixed-fps，音訊照牆鐘走）：godot --path game --headless -s res://scripts/qa/test_qa_soul_draw_sfx_rarity.gd
## 1. 五個框色各用真實 drop（DROP_TIERS 找得到就用；金／彩不在池裡就用 Catalog 對應的 DropId，再不行走 play_reveal_frame 除錯入口）→ 實際起播的 stream 檔名要對
## 2. 單抽完整演出：summon 有響、演出結束後 reveal 只響一次
## 3. 演出中跳過：summon 立刻停、之後不再有第二次 callback／第二聲 reveal、沒有殘響
## 4. 任何時刻抽魂流程同時發聲 ≤ 2
## 5. 五階實際播出響度（檔案 400 ms 最大均方（近似 M-max）＋volume_db）要由白到彩單調上升（越稀有越響）
## 2026-10-15：#98 42fa1e5f 起白階改播 reveal_white（#107）
const Sfx := preload("res://scripts/ui/soul_draw/soul_draw_sfx.gd")
const Catalog := preload("res://scripts/ui/soul_draw/soul_draw_card_catalog.gd")
const Fx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const WANT := {"white": "reveal_white.wav", "blue": "reveal_blue.wav", "purple": "reveal_purple.wav", "gold": "reveal_gold.wav", "rainbow": "reveal_rainbow.wav"}
var _ok := true
var _am: Node
var _phase := 0
var _f := 0
var _fx: Control
var _cb := 0
var _log: Array = []   # [frame, playing files]
var _maxv := 0
var _drop_for := {}
var _loud: Array = []
func _fail(m: String) -> void:
	print("  FAIL ", m); _ok = false
func _playing() -> Array:
	var out := []
	for p in _am._pool:
		if p.playing and p.stream: out.append(p.stream.resource_path.get_file())
	return out
func _stop_all() -> void:
	for p in _am._pool: p.stop()
func _initialize() -> void:
	## 音訊在牆鐘時間前進：不能用 --fixed-fps（遊戲時間會比聲音快），改成真實 60 fps
	Engine.max_fps = 60
## 讀原始 .wav（匯入後可能是壓縮格式，所以直接讀來源檔的 16-bit PCM data chunk）
func _wav_rms_db(st: AudioStream) -> float:
	var f := FileAccess.open(st.resource_path, FileAccess.READ)
	if f == null: return -999.0
	var b := f.get_buffer(f.get_length())
	var i := 12
	while i + 8 <= b.size():
		var id := b.slice(i, i + 4).get_string_from_ascii()
		var sz := b.decode_u32(i + 4)
		if id == "data":
			## 近似 M-max：400 ms 視窗（檔尾補靜音）、10 ms 步進的最大均方（不含 K 加權）
			var n := int(sz / 2)
			var sq := PackedFloat64Array(); sq.resize(n + 1); sq[0] = 0.0
			for k in n:
				var v := b.decode_s16(i + 8 + k * 2) / 32768.0
				sq[k + 1] = sq[k] + v * v
			var w := 17640; var best := 0.0
			var st_i := 0
			while st_i < n:
				var e := mini(n, st_i + w)
				best = maxf(best, (sq[e] - sq[st_i]) / w)
				st_i += 441
			return 10.0 * log(best + 1e-12) / log(10.0)
		i += 8 + sz + (sz & 1)
	return -999.0


func _rarity_check() -> void:
	for k in Catalog.DROP_TIERS.keys():
		var fr := Catalog.frame_key_for_drop({"DropId": k, "kind": "part"})
		if not _drop_for.has(fr): _drop_for[fr] = k
	print("  drop per frame: ", _drop_for)
	for fr in WANT.keys():
		_stop_all()
		var via := ""
		if _drop_for.has(fr):
			Sfx.play_reveal_for_drop({"DropId": _drop_for[fr], "kind": "part"}); via = "drop " + str(_drop_for[fr])
		else:
			Sfx.play_reveal_frame(fr); via = "debug play_reveal_frame"
		var pl := _playing()
		var okk: bool = pl.size() == 1 and pl[0] == WANT[fr]
		print("  %s %-7s via %-30s → %s" % ["ok" if okk else "FAIL", fr, via, str(pl)])
		if not okk: _fail("%s 應只播 %s，實際 %s" % [fr, WANT[fr], str(pl)])
		for p in _am._pool:
			if p.playing and p.stream:
				var eff: float = _wav_rms_db(p.stream) + p.volume_db - _am._sfx_db
				_loud.append([fr, eff, p.volume_db - _am._sfx_db])
	var prev := -999.0
	for e in _loud:
		print("  loud %-7s 400ms最大均方+增益=%.1f dB（volume_db %+.1f）" % [e[0], e[1], e[2]])
		if e[1] < prev - 0.05: _fail("%s 播出響度 %.1f 低於前一階 %.1f：稀有度響度沒有單調上升" % [e[0], e[1], prev])
		prev = maxf(prev, e[1])
	# 十連取最高
	_stop_all()
	var drops := []
	for fr in ["white", "blue", "purple"]:
		if _drop_for.has(fr): drops.append({"DropId": _drop_for[fr], "kind": "part"})
	Sfx.play_reveal_for_drops(drops)
	print("  ten-pull(white,blue,purple) → ", _playing())
	_stop_all()
func _start_fx() -> void:
	_cb = 0; _log.clear()
	if _fx: _fx.queue_free()
	_fx = Fx.new(); _fx.size = Vector2(1280, 720)
	root.add_child(_fx)
	Sfx.play_pull()
	_fx.play_summon(false, func():
		_cb += 1
		Sfx.play_reveal_for_drop({"DropId": _drop_for.get("purple", ""), "kind": "part"}))
func _process(_d: float) -> bool:
	_f += 1
	if _phase == 0 and _f == 3:
		_am = root.get_node("AudioManager"); _am._muted = false
		print("  pool=%d" % _am._pool.size())
		_rarity_check()
		_phase = 1; _f = 0
		_start_fx()
		return false
	if _phase in [1, 2]:
		var pl := _playing()
		_maxv = maxi(_maxv, pl.size())
		if _log.is_empty() or _log[-1][1] != pl: _log.append([_f, pl])
		if _phase == 2 and _f == 18:
			print("  SKIP at f18, playing before: ", pl)
			_fx.skip()
			print("  after skip same frame: ", _playing(), " cb=", _cb)
		if _f == 300:
			var name := "natural" if _phase == 1 else "skip"
			print("  [%s] timeline: %s  callbacks=%d maxVoices=%d" % [name, str(_log), _cb, _maxv])
			var summon_seen := false
			for e in _log:
				if "summon.wav" in e[1]: summon_seen = true
			if not summon_seen: _fail("[%s] summon 沒有響" % name)
			if _cb != 1: _fail("[%s] 結束 callback 被呼叫 %d 次（應 1）→ reveal 會重播" % [name, _cb])
			if _maxv > 2: _fail("[%s] 同時 %d 聲 > 2" % [name, _maxv])
			if _phase == 2:
				for e in _log:
					if e[0] > 18 and "summon.wav" in e[1]: _fail("[skip] 跳過後 f%d 仍有 summon" % e[0])
			if _phase == 1:
				_phase = 2; _f = 0; _maxv = 0; _stop_all(); _start_fx()
			else:
				print("QA_SOUL_DRAW_SFX_RARITY_OK" if _ok else "QA_SOUL_DRAW_SFX_RARITY_FAIL")
				quit(0 if _ok else 1)
	return false
