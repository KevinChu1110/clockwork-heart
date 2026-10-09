extends SceneTree
## 發條鑰匙轉速跟時間走、不跟渲染幀率走（#61）：
##   godot --headless -s res://scripts/art/test_winding_key_time.gd
## 守：
##   1. 30／60／120／144Hz 與不規則 delta，跑 2 秒都轉 15 格（一格 8/60 秒，一秒 7.5 格）。
##   2. 60Hz 下仍是第 8／16／24 幀換格（跟任務書「每 8 幀」一致）。
##   3. 卡頓一大段（切背景回來）最多補一圈，不狂轉。
##   4. 大廳用的 WindingKeyAnim.accumulate 同一套規則。

const WindingKeyAnim = preload("res://scripts/art/winding_key_anim.gd")
const WindingKeyTicker = preload("res://scripts/art/winding_key_ticker.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _new_ticker() -> Array:
	var rect := TextureRect.new()
	root.add_child(rect)
	rect.texture = PaperdollRenderer.build_composite_texture_512("rabbit", {})
	var t = WindingKeyTicker.new()
	rect.add_child(t)
	t.attach(rect, func(): return {"race": "rabbit", "sel": {}})
	t.set_process(false)
	return [rect, t]


func _initialize() -> void:
	var made := _new_ticker()
	var rect: TextureRect = made[0]
	var t = made[1]

	## 1. 不同刷新率跑 2 秒
	for hz in [30, 60, 120, 144]:
		t.attach(rect, func(): return {"race": "rabbit", "sel": {}})
		t.set_process(false)
		var before: int = t.steps_taken
		for i in range(hz * 2):
			t.tick_time(1.0 / float(hz))
		var got: int = t.steps_taken - before
		if got != 15:
			_fail("%dHz 跑 2 秒應轉 15 格，實際 %d" % [hz, got])
		else:
			print("  ok  %3dHz × 2 秒 → %d 格" % [hz, got])

	## 不規則 delta（掉幀、忽快忽慢），總長 2 秒
	t.attach(rect, func(): return {"race": "rabbit", "sel": {}})
	t.set_process(false)
	var rng := RandomNumberGenerator.new()
	rng.seed = 61
	var before_j: int = t.steps_taken
	var total := 0.0
	while total < 2.0 - 0.000001:
		var d := minf(rng.randf_range(0.004, 0.05), 2.0 - total)
		total += d
		t.tick_time(d)
	var got_j: int = t.steps_taken - before_j
	if got_j != 15:
		_fail("不規則 delta 跑 2 秒應轉 15 格，實際 %d" % got_j)
	else:
		print("  ok  不規則 delta × 2 秒 → %d 格" % got_j)

	## 2. 60Hz 仍是第 8／16／24 幀
	t.attach(rect, func(): return {"race": "rabbit", "sel": {}})
	t.set_process(false)
	var changed_at: Array = []
	for i in range(1, 25):
		if t.tick():
			changed_at.append(i)
	if changed_at != [8, 16, 24]:
		_fail("60Hz 應在第 8／16／24 幀換格，實際 %s" % [changed_at])
	else:
		print("  ok  60Hz 換格幀 %s" % [changed_at])

	## 3. 卡 5 秒：最多補一圈
	var before_s: int = t.steps_taken
	t.tick_time(5.0)
	var got_s: int = t.steps_taken - before_s
	if got_s > WindingKeyAnim.STEPS_PER_TURN:
		_fail("卡頓 5 秒補了 %d 格，應最多一圈（%d）" % [got_s, WindingKeyAnim.STEPS_PER_TURN])
	else:
		print("  ok  卡頓 5 秒補 %d 格（上限一圈）" % got_s)

	## 4. 大廳用的累加器：144Hz 跑 2 秒
	var acc := 0.0
	var steps := 0
	for i in range(288):
		var r: Array = WindingKeyAnim.accumulate(acc, 1.0 / 144.0)
		acc = float(r[1])
		steps += int(r[0])
	if steps != 15:
		_fail("accumulate 144Hz × 2 秒應 15 格，實際 %d" % steps)
	else:
		print("  ok  accumulate 144Hz × 2 秒 → %d 格" % steps)

	rect.queue_free()
	if _ok:
		print("WINDING_KEY_TIME_OK")
	quit(0 if _ok else 1)
