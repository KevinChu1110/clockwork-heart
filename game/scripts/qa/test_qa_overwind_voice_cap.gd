extends SceneTree
## QA：發條超載爆裂（overwind burst）不得超過 SFX 同時發聲上限
## TEST_FILTER=qa_overwind ./tools/run_tests.sh
##
## 背景：PR #16 把 SFX 收成「同時最多 MAX_SFX_VOICES 聲」；main 合入的
## play_overwind_burst() 在缺 overwind.wav 時一次疊 clash＋break＋clock 三聲。
## 這支測試量實際同時在響的 SFX 數，並印出哪一層被丟掉／被搶走。
## main（沒有 MAX_SFX_VOICES）只印資訊、不判失敗。
## 2026-10-15：有 #68 UI 專屬聲道（SfxUi）時，上限只算戰鬥池；並檢查 ui 有響、沒擠掉戰鬥音（#63）。

var _done := false
var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _playing(am: Node) -> Array[String]:
	var out: Array[String] = []
	for c in am.find_children("*", "AudioStreamPlayer", true, false):
		var p := c as AudioStreamPlayer
		if p.playing and p.stream != null:
			out.append(p.stream.resource_path.get_file().get_basename())
	return out


## 戰鬥 SFX 池（不含 #68 的 UI 專屬聲道 SfxUi；UI 聲道依 #63 驗收不算進兩聲上限）
func _playing_pool(am: Node) -> Array[String]:
	var out: Array[String] = []
	for c in am.find_children("*", "AudioStreamPlayer", true, false):
		var p := c as AudioStreamPlayer
		if p.name == "SfxUi":
			continue
		if p.playing and p.stream != null and p.stream.resource_path.contains("/sfx/"):
			out.append(p.stream.resource_path.get_file().get_basename())
	return out


func _stop_all(am: Node) -> void:
	for c in am.find_children("*", "AudioStreamPlayer", true, false):
		var p := c as AudioStreamPlayer
		if p.stream != null and p.stream.resource_path.contains("/sfx/"):
			p.stop()


func _process(_delta: float) -> bool:
	if _done:
		return true
	_done = true
	var am := root.get_node_or_null("AudioManager")
	if am == null or not am.has_method("play_overwind_burst"):
		print("  SKIP AudioManager 沒有 play_overwind_burst")
		print("QA_OVERWIND_VOICE_CAP_OK")
		quit(0)
		return true
	var cap_v = am.get("MAX_SFX_VOICES")
	var cap: int = int(cap_v) if cap_v != null else -1
	var has_file: bool = am.get("_streams") is Dictionary and (am.get("_streams") as Dictionary).has("overwind")
	print("  MAX_SFX_VOICES=%s  overwind.wav=%s" % [str(cap), str(has_file)])

	# 情境 A：安靜時觸發
	_stop_all(am)
	am.call("play_overwind_burst")
	var a := _playing(am)
	print("  A 安靜時爆裂 → 同時在響 %d 聲：%s" % [a.size(), str(a)])
	if cap > 0 and a.size() > cap:
		_fail("情境 A 同時 %d 聲，超過上限 %d" % [a.size(), cap])

	# 情境 B：部位破壞（break）＋普通命中（hit）正在響時觸發
	_stop_all(am)
	am.call("play", "break")
	am.call("play", "hit")
	am.call("play_overwind_burst")
	var b := _playing(am)
	print("  B break+hit 進行中爆裂 → 同時在響 %d 聲：%s" % [b.size(), str(b)])
	if cap > 0 and b.size() > cap:
		_fail("情境 B 同時 %d 聲，超過上限 %d" % [b.size(), cap])

	# 情境 C：爆裂後立刻點 UI
	am.call("play", "ui")
	var c := _playing(am)
	var cp := _playing_pool(am)
	var ui_voice: bool = am.get("_ui_voice") != null
	print("  C 爆裂後點 UI → 全部 %d 聲：%s；戰鬥池 %d 聲：%s（ui 在不在：%s；UI 專屬聲道：%s）" % [c.size(), str(c), cp.size(), str(cp), str(c.has("ui")), str(ui_voice)])
	if cap > 0 and cp.size() > cap:
		_fail("情境 C 戰鬥池同時 %d 聲，超過上限 %d" % [cp.size(), cap])
	if ui_voice and not c.has("ui"):
		_fail("情境 C 有 UI 專屬聲道（#68）但 ui 點擊沒響（#63 回歸）")
	if ui_voice and cp != b:
		_fail("情境 C UI 點擊擠掉了戰鬥音：%s → %s" % [str(b), str(cp)])

	print("QA_OVERWIND_VOICE_CAP_OK" if _ok else "QA_OVERWIND_VOICE_CAP_FAIL")
	quit(0 if _ok else 1)
	return true
