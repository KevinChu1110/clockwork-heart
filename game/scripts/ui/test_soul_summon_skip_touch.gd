extends SceneTree
## 抽魂演出「跳過」鈕觸控目標（#93／BENCHMARK M-05、M-13、M-20）
## 1. 六語系下跳過鈕寬高都 ≥ 81px（T-01 標準檔），文字不被裁。
## 2. 跳過鈕完整在畫面內、不貼邊（safe area 之內）。
## 3. 真的送點擊事件：點跳過鈕會結束演出；點畫面中央（裝飾層上）也會結束演出。

const SoulSummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const TOUCH_MIN := 81.0

var _ok := true
var _frame := 0
var _step := 0
var _fx: Control
var _done_count := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)  ## headless 預設 64×64，點擊會落在畫面外
	_fx = SoulSummonFx.new()
	root.add_child(_fx)


func _on_done() -> void:
	_done_count += 1


func _btn() -> Button:
	return _fx.get("_skip_btn") as Button


func _tap(pos: Vector2) -> void:
	for pressed in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = pos
		ev.global_position = pos
		root.push_input(ev, true)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_check_sizes()
				_fx.call("play_summon", false, _on_done)
				_step = 1
				_frame = 0
		1:
			if _frame == 3:
				var b := _btn()
				_tap(b.get_global_rect().get_center())
			elif _frame == 6:
				if _done_count != 1:
					_fail("點跳過鈕後演出沒結束（callback %d 次）" % _done_count)
				else:
					print("  ok 點跳過鈕結束演出")
				_fx.call("play_summon", true, _on_done)
				_step = 2
				_frame = 0
		2:
			if _frame == 10:
				## 中央是發條鑰匙／光環／星芒等裝飾層，不能吃掉點擊
				_tap(Vector2(640, 360))
			elif _frame == 13:
				if _done_count != 2:
					_fail("點畫面中央（裝飾層上）沒有跳過演出（callback %d 次）" % _done_count)
				else:
					print("  ok 點畫面任何地方都能跳過")
				if _ok:
					print("TEST_SOUL_SUMMON_SKIP_TOUCH_OK")
					quit(0)
				else:
					print("TEST_SOUL_SUMMON_SKIP_TOUCH_FAIL")
					quit(1)
				return true
	return false


func _check_sizes() -> void:
	var loc: Node = root.get_node_or_null("Loc")
	var vp := Rect2(Vector2.ZERO, Vector2(1280, 720))
	for code in LOCALES:
		if loc:
			loc.call("set_locale", code)
		var b := _btn()
		var r := b.get_global_rect()
		var need := b.get_combined_minimum_size()
		if r.size.x < TOUCH_MIN or r.size.y < TOUCH_MIN:
			_fail("[%s] 跳過鈕 %s 小於 %dpx 觸控門檻" % [code, str(r.size), int(TOUCH_MIN)])
		if r.size.x + 0.5 < need.x or r.size.y + 0.5 < need.y:
			_fail("[%s] 跳過鈕『%s』放不下文字：%s < %s" % [code, b.text, str(r.size), str(need)])
		if not vp.grow(-8.0).encloses(r):
			_fail("[%s] 跳過鈕 %s 超出或貼住畫面邊（需在 safe area 內）" % [code, str(r)])
		print("  ok [%s] 跳過鈕『%s』%s" % [code, b.text, str(r.size)])
	if loc:
		loc.call("set_locale", "zh_TW")
