extends SceneTree
## SFX 把關測試：godot --headless -s res://scripts/art/test_sfx.gd
##
## 守任務書 §5 的音效規則：
##   1. 戰鬥自動回饋要用的 key（swap／break／warn／hit／slash）都載得到
##   2. hit、slash、swap 都短於 0.3 秒；所有 SFX 都不循環（warn 是一次性）
##   3. 缺檔的 key 不會當，只警告一次
##   4. 同時最多兩聲 SFX
##   5. parry 不在 UI 提示音清單裡
##   6. AudioManager 自己不播 warn（危險預警、王斬蓄力、Boss 開戰都不行）；
##      warn 只由戰鬥端在「Boss 部位將破」時 play("warn") 一次
##
## 同 test_bgm：autoload 的 _ready 在 _initialize 之後，檢查放第一個影格。

const REQUIRED: Array[String] = ["swap", "break", "warn", "hit", "slash"]
const SHORT_KEYS: Array[String] = ["hit", "slash", "swap"]
const MAX_SHORT_SEC := 0.3

var _ok := true
var _done := false


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _process(_delta: float) -> bool:
	if _done:
		return true
	_done = true
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager autoload missing")
	else:
		_check_required(am)
		_check_lengths_and_loop(am)
		_check_missing_key(am)
		_check_voice_limit(am)
		_check_parry_not_ui(am)
		_check_warn_only_explicit(am)
		_check_weapon_swap_event(am)
	if _ok:
		print("SFX_OK")
		quit(0)
	else:
		print("SFX_FAIL")
		quit(1)
	return true


func _check_required(am: Node) -> void:
	## 先釘清單：AudioManager 自己宣告的必備 key 要和這裡一致
	for k in REQUIRED:
		if not _const(am, "SFX_REQUIRED").has(k):
			_fail("AudioManager.SFX_REQUIRED 少了 %s" % k)
		if not am.has_sfx(k):
			_fail("必備音效 %s 沒載到（game/assets/audio/sfx/%s.wav）" % [k, k])
	if _ok:
		print("  ok 必備 key 都在：%s" % str(REQUIRED))


func _check_lengths_and_loop(am: Node) -> void:
	for k in SHORT_KEYS:
		var s: Variant = load("res://assets/audio/sfx/%s.wav" % k)
		if not (s is AudioStream):
			_fail("%s.wav 載不到" % k)
			continue
		var dur: float = (s as AudioStream).get_length()
		if dur <= 0.0 or dur >= MAX_SHORT_SEC:
			_fail("%s 長 %.3f 秒，規格要 < %.1f 秒" % [k, dur, MAX_SHORT_SEC])
	var n := 0
	for k in am.sfx_ids():
		var st: Variant = am._streams.get(k)
		if st is AudioStreamWAV and (st as AudioStreamWAV).loop_mode != AudioStreamWAV.LOOP_DISABLED:
			_fail("SFX %s 會循環（音效一律一次性）" % k)
		n += 1
	if n < REQUIRED.size():
		_fail("只載到 %d 個 SFX，清單空轉？" % n)
	print("  ok hit／slash／swap < %.1f 秒，%d 個 SFX 都不循環" % [MAX_SHORT_SEC, n])


func _check_missing_key(am: Node) -> void:
	var key := "__no_such_sfx__"
	am.play(key)
	am.play(key)
	if not am._missing_sfx_warned.has(key):
		_fail("缺檔 key 沒有記下警告")
	elif am._missing_sfx_warned.size() < 1:
		_fail("缺檔警告表是空的")
	else:
		print("  ok 缺檔 key 不會當，只警告一次")


func _check_voice_limit(am: Node) -> void:
	if am.sfx_voice_limit() != 2:
		_fail("SFX 同時上限應為 2，實際 %d" % am.sfx_voice_limit())
		return
	if am._pool.size() > 2:
		_fail("SFX voice 池有 %d 個，超過兩聲上限" % am._pool.size())
		return
	var was_muted: bool = am._muted
	am._muted = false
	for k in ["hit", "slash", "swap", "break", "hit"]:
		am.play(k)
		if am.active_sfx_count() > 2:
			_fail("同時響了 %d 聲（上限 2）" % am.active_sfx_count())
			break
	## 高優先度（break）要搶得到位置，低優先度（step）在滿載時要被丟掉
	am.play("break")
	am.play("break")
	if am.active_sfx_count() != 2:
		_fail("連播兩聲 break 後應有 2 聲在響，實際 %d（voice 檢查會空轉）" % am.active_sfx_count())
	var before := _playing_keys(am)
	am.play("step")
	var after := _playing_keys(am)
	if before.size() == 2 and before != after:
		_fail("滿載時低優先度 step 不該擠掉 %s（變成 %s）" % [str(before), str(after)])
	for p in am._pool:
		(p as AudioStreamPlayer).stop()
	am._muted = was_muted
	if _ok:
		print("  ok 同時最多 2 聲，低優先度滿載時被丟掉")


func _playing_keys(am: Node) -> Array:
	var out: Array = []
	for p in am._pool:
		var ap := p as AudioStreamPlayer
		if ap.playing and ap.stream:
			out.append(ap.stream.resource_path)
	return out


func _check_parry_not_ui(am: Node) -> void:
	if _const(am, "UI_SFX").has("parry"):
		_fail("parry 不可當 UI／操作提示音")
	else:
		print("  ok parry 不在 UI 提示音清單")


func _const(am: Node, name: String) -> Array:
	var m: Dictionary = am.get_script().get_script_constant_map()
	return m.get(name, [])


## 行為面：觸發以前會帶 warn 的事件，確認沒有任何 voice 在播 warn。
## 原始碼面：audio_manager.gd 裡不能再有 play("warn"…)，免得之後又被加回某個事件。
func _check_warn_only_explicit(am: Node) -> void:
	var warn_stream: Variant = am._streams.get("warn")
	if warn_stream == null:
		_fail("warn 沒載到，無法檢查")
		return
	var was_muted: bool = am._muted
	am._muted = false
	var cases := [
		["hazard_warn", {"kind": "fire_ring"}],
		["hazard_warn", {"kind": "time_clock"}],
		["king_slash_start", {}],
	]
	for c in cases:
		_stop_all(am)
		am.on_battle_event(c[0], c[1])
		if _warn_playing(am, warn_stream):
			_fail("on_battle_event(%s) 不該播 warn" % c[0])
	_stop_all(am)
	am.battle_start("leo")  ## leo 是 Boss 戰
	if _warn_playing(am, warn_stream):
		_fail("Boss 開戰 battle_start 不該播 warn")
	am.stop_bgm(0.01)
	## 明確呼叫還是要播得出來（戰鬥端靠這個）
	_stop_all(am)
	am.play("warn")
	if not _warn_playing(am, warn_stream):
		_fail("play(\"warn\") 明確呼叫卻沒播")
	_stop_all(am)
	am._muted = was_muted

	var f := FileAccess.open("res://scripts/autoload/audio_manager.gd", FileAccess.READ)
	if f == null:
		_fail("讀不到 audio_manager.gd")
		return
	var re := RegEx.new()
	re.compile("play\\(\\s*\"warn\"")
	var hits := 0
	for line in f.get_as_text().split("\n"):
		if re.search(line.split("#")[0]) != null:  ## 註解裡提到 play("warn") 不算
			hits += 1
	if hits > 0:
		_fail("audio_manager.gd 還有 %d 處自動 play(\"warn\")" % hits)
	if _ok:
		print("  ok AudioManager 不自動播 warn（預警／蓄力／Boss 開戰），明確 play(\"warn\") 仍可播")


func _warn_playing(am: Node, warn_stream: Variant) -> bool:
	for p in am._pool:
		var ap := p as AudioStreamPlayer
		if ap.playing and ap.stream == warn_stream:
			return true
	return false


func _stop_all(am: Node) -> void:
	for p in am._pool:
		(p as AudioStreamPlayer).stop()


func _check_weapon_swap_event(am: Node) -> void:
	var swap_stream: Variant = am._streams.get("swap")
	if swap_stream == null:
		_fail("swap 沒載到，無法檢查")
		return
	var was_muted: bool = am._muted
	am._muted = false
	for ev in ["weapon_swap", "weapon_slot_switched"]:
		_stop_all(am)
		am.on_battle_event(ev, {"auto": true})
		if not _warn_playing(am, swap_stream):
			_fail("on_battle_event(%s) 應該播放 swap.wav" % ev)
	_stop_all(am)
	am._muted = was_muted
	if _ok:
		print("  ok on_battle_event(weapon_swap / weapon_slot_switched) 觸發 swap.wav 金屬卡榫音效")

