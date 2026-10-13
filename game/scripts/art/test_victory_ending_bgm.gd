extends SceneTree
## 勝利結算 ending 測試（#64）：godot --headless -s res://scripts/art/test_victory_ending_bgm.gd
##
## 守這幾件事：
##   1. 勝利 → cue 切到 ending（不循環），淡入落在 0.3–0.5 s，讓開 victory 音效起音
##   2. 輸了 → 不播 ending，維持舊行為（戰鬥曲壓低 8 dB）
##   3. 木人試招（celebrate=false）→ 不播 ending
##   4. ending 自然播完 → 發 bgm_finished("ending")，自動接回開戰前的地區曲
##   5. 播完之前先離開結算（play_bgm_for_map）→ 照新地圖走，舊 ending 播完不會把曲子拉回去
##   6. 結算頁直接再次挑戰 → 開戰前的地區曲不被 ending／battle 蓋掉
##
## 「播完」用直接觸發 player 的 finished 模擬：headless 下等 16 秒太慢，
## 而且要驗的是 AudioManager 收到 finished 後做什麼，不是音訊驅動會不會發 finished。
##
## 注意：用 `-s` 跑時 autoload 的 _ready 在 _initialize 之後才執行，所以等第一個影格。

var _ok := true
var _done := false
var _finished_ids: Array = []


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _expect(cond: bool, msg: String) -> void:
	if cond:
		print("  ok ", msg)
	else:
		_fail(msg)


func _active(am: Node) -> AudioStreamPlayer:
	return am.get("_bgm_active") as AudioStreamPlayer


func _end_oneshot(am: Node) -> void:
	## 模擬目前這軌自然播完
	_active(am).finished.emit()


func _process(_delta: float) -> bool:
	if _done:
		return true
	_done = true
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager autoload missing")
		return _finish()
	am.bgm_finished.connect(func(id: String): _finished_ids.append(id))

	## 0) 規格
	_expect(not am.bgm_loops("ending"), "ending 不循環")
	var fade_in: float = am.ENDING_FADE_IN
	_expect(fade_in >= 0.3 and fade_in <= 0.5, "ending 淡入 %.2f s 落在 0.3–0.5 s" % fade_in)

	## 1) 勝利 → ending
	am.play_bgm("village", 0.01)
	am.battle_start("wolf")
	_expect(am.current_bgm_cue() == "battle", "開戰切 battle")
	am.battle_end(true)
	_expect(am.current_bgm_cue() == "ending", "勝利結算 cue＝ending（實得 %s）" % am.current_bgm_cue())
	_expect(am.resume_bgm_cue() == "village", "ending 播完要接回 village（實得 '%s'）" % am.resume_bgm_cue())
	var st: AudioStream = _active(am).stream
	var looped := true
	if st is AudioStreamMP3:
		looped = (st as AudioStreamMP3).loop
	elif st is AudioStreamOggVorbis:
		looped = (st as AudioStreamOggVorbis).loop
	elif st is AudioStreamWAV:
		looped = (st as AudioStreamWAV).loop_mode != AudioStreamWAV.LOOP_DISABLED
	_expect(st != null and not looped, "ending 串流本身關掉循環")

	## 4) 播完 → 發訊號、接回地區曲
	_end_oneshot(am)
	_expect(_finished_ids == ["ending"], "ending 播完發 bgm_finished(\"ending\")（實得 %s）" % str(_finished_ids))
	_expect(am.current_bgm_cue() == "village", "ending 播完自動接回 village（實得 %s）" % am.current_bgm_cue())

	## 2) 輸了 → 不播 ending，戰鬥曲壓低
	am.battle_start("leo")
	_expect(am.current_bgm_cue() == "boss", "Boss 戰切 boss")
	am.battle_end(false)
	_expect(am.current_bgm_cue() == "boss", "輸了不切 ending（實得 %s）" % am.current_bgm_cue())
	_expect(am.resume_bgm_cue() == "", "輸了沒有接回排程")
	var want_db: float = am._bgm_target_db("boss") - 8.0
	_expect(absf(_active(am).volume_db - want_db) < 0.6, "輸了戰鬥曲壓低 8 dB（%.1f dB）" % _active(am).volume_db)

	## 3) 木人試招 → 不播 ending
	am.play_bgm("town", 0.01)
	am.battle_start("training_dummy")
	am.battle_end(true, false)
	_expect(am.current_bgm_cue() == "battle", "試招贏了不切 ending（實得 %s）" % am.current_bgm_cue())

	## 5) 播完前先離開結算 → 照新地圖，舊 ending 播完不拉回
	am.play_bgm("village", 0.01)
	am.battle_start("wolf")
	am.battle_end(true)
	var ending_player := _active(am)
	am.play_bgm_for_map("forest_1")
	_expect(am.current_bgm_cue() == "forest", "離開結算切回地圖曲 forest")
	_expect(am.resume_bgm_cue() == "", "離開結算後取消接回排程")
	_finished_ids.clear()
	ending_player.finished.emit()
	_expect(am.current_bgm_cue() == "forest" and _finished_ids.is_empty(), "舊 ending 晚到的 finished 不影響新地圖曲")

	## 6) 結算頁再次挑戰 → 地區曲不被蓋掉
	am.play_bgm("road", 0.01)
	am.battle_start("wolf")
	am.battle_end(true)
	am.battle_start("wolf")  ## 結算頁「再次挑戰」
	_expect(am.current_bgm_cue() == "battle", "再次挑戰切回 battle")
	am.battle_end(true)
	_end_oneshot(am)
	_expect(am.current_bgm_cue() == "road", "連打兩場後 ending 播完仍接回 road（實得 %s）" % am.current_bgm_cue())

	return _finish()


func _finish() -> bool:
	if _ok:
		print("VICTORY_ENDING_BGM_OK")
		quit(0)
	else:
		print("VICTORY_ENDING_BGM_FAIL")
		quit(1)
	return true
