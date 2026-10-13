extends SceneTree
## #91：抽魂流程音效。驗：按抽、演出開始、翻卡、十連結算都有呼叫 AudioManager；
## reveal 依框色分 3 級（音高不同）；每個時刻 ≤2 聲；十連只播一聲 reveal。

const Sfx := preload("res://scripts/ui/soul_draw/soul_draw_sfx.gd")
const ResultCard := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const TenPull := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")
const SummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _process(_d: float) -> bool:
	_frame += 1
	if _frame < 3:
		return false
	var am := root.get_node_or_null("AudioManager")
	if am == null:
		_fail("AudioManager autoload missing")
	else:
		am.call("set_muted", false)
		_run(am)
	print("TEST_SOUL_DRAW_SFX_OK" if _ok else "TEST_SOUL_DRAW_SFX_FAIL")
	quit(0 if _ok else 1)
	return true


func _run(am: Node) -> void:
	# 1. 單張翻卡：白／藍／紫三級，都走 AudioManager，音高遞增
	var card: Control = ResultCard.new()
	root.add_child(card)
	var drops := {
		"white": {"kind": "junk", "DropId": "junk_enamel_chip"},
		"blue": {"kind": "part", "DropId": "drop_spring_coil"},
		"purple": {"kind": "outfit", "DropId": "outfit_cream"},
	}
	var pitches: Array[float] = []
	for k in ["white", "blue", "purple"]:
		Sfx.calls.clear()
		am.set("last_sfx", "")
		card.call("show_drop", drops[k])
		var reveals := Sfx.calls.filter(func(c): return c[0] == "reveal")
		if reveals.size() != 1:
			_fail("[%s] 翻卡應播 1 聲 reveal，實際 %s" % [k, str(Sfx.calls)])
			continue
		if Sfx.calls.size() > 2:
			_fail("[%s] 翻卡同時 %d 聲，超過 2" % [k, Sfx.calls.size()])
		if str(am.get("last_sfx")) == "":
			_fail("[%s] 翻卡沒有呼叫 AudioManager" % k)
		pitches.append(float(reveals[0][1]))
	if pitches.size() == 3 and not (pitches[0] < pitches[1] and pitches[1] < pitches[2]):
		_fail("reveal 沒有照稀有度分 3 級：%s" % str(pitches))
	elif pitches.size() == 3:
		print("  ok 翻卡 reveal 分 3 級 %s" % str(pitches))

	# 2. 十連：只播一聲 reveal，取最高框（含紫 → 紫級）
	var ten: Control = TenPull.new()
	root.add_child(ten)
	var ten_drops: Array[Dictionary] = []
	for i in 9:
		ten_drops.append(drops["blue"])
	ten_drops.append(drops["purple"])
	Sfx.calls.clear()
	ten.call("show_drops", ten_drops)
	var r10 := Sfx.calls.filter(func(c): return c[0] == "reveal")
	if r10.size() != 1:
		_fail("十連結算應只播 1 聲 reveal，實際 %d" % r10.size())
	elif not is_equal_approx(float(r10[0][1]), pitches[2] if pitches.size() == 3 else -1.0):
		_fail("十連含紫框，reveal 應為紫級音高，實際 %s" % str(r10[0]))
	elif Sfx.calls.size() > 2:
		_fail("十連結算同時 %d 聲，超過 2" % Sfx.calls.size())
	else:
		print("  ok 十連一聲 reveal（最高框）")

	# 3. 召喚演出開始有聲；跳過後不再追加聲音
	var fx: Control = SummonFx.new()
	root.add_child(fx)
	Sfx.calls.clear()
	fx.call("play_summon", true, func(): pass)
	if Sfx.calls.size() != 1 or Sfx.calls[0][0] != "clock":
		_fail("召喚開始應播 1 聲 clock，實際 %s" % str(Sfx.calls))
	Sfx.calls.clear()
	fx.call("skip")
	if not Sfx.calls.is_empty():
		_fail("跳過演出不該再播聲音：%s" % str(Sfx.calls))
	else:
		print("  ok 召喚開始有聲，跳過不留殘響")

	# 4. 按抽：play_pull 走 play_ui
	Sfx.calls.clear()
	am.set("last_sfx", "")
	Sfx.play_pull()
	if str(am.get("last_sfx")) != "ui":
		_fail("按抽應播 ui，last_sfx=%s" % str(am.get("last_sfx")))
	else:
		print("  ok 按抽有 ui 回饋")
