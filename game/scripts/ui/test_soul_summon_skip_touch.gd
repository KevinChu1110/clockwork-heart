extends SceneTree
## 抽魂演出「跳過」（#93／#101／#102；BENCHMARK M-05、M-13、M-20）
## 1. 六語系下跳過鈕寬高都 ≥ 81px、字級 ≥ 20px 且真的套用（不被共用樣式蓋回 17）、文字放得下、在畫面內。
## 2. 點跳過鈕會結束演出（不受開場保護時間限制）。
## 3. 誤觸不跳過：開場保護時間內的連點、滾輪、右鍵、只有放開。
## 4. 保護時間過後點畫面中央（裝飾層上）會跳過；觸控也會。
## 時間用 fx 自己累加的演出時間判斷，不靠幀數，換 fps 也成立。

const SoulSummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const TOUCH_MIN := 81.0
const FONT_MIN := 20

var _ok := true
var _frame := 0
var _fx: Control
var _done := 0
var _cases: Array = []
var _ci := -1
var _base := 0
var _sent := false
var _wait_after := 0


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
	var guard: float = SoulSummonFx.SKIP_GUARD_SEC
	## [名稱, 送出時的演出時間(秒), 事件種類, 應該跳過?]
	_cases = [
		["跳過鈕（開場第一幀）", 0.0, "button", true],
		["連點：開場第一幀左鍵", 0.0, "left", false],
		["保護時間快結束時左鍵", guard * 0.8, "left", false],
		["滾輪往下", guard + 0.2, "wheel", false],
		["右鍵", guard + 0.2, "right", false],
		["只有放開", guard + 0.2, "release", false],
		["保護時間後左鍵點畫面中央", guard + 0.1, "left", true],
		["保護時間後觸控畫面中央", guard + 0.1, "touch", true],
	]


func _on_done() -> void:
	_done += 1


func _btn() -> Button:
	return _fx.get("_skip_btn") as Button


func _send(kind: String) -> void:
	var pos := Vector2(640, 360)
	if kind == "button":
		pos = _btn().get_global_rect().get_center()
		kind = "left"
	var evs: Array = []
	match kind:
		"left", "right", "wheel":
			var idx := MOUSE_BUTTON_LEFT
			if kind == "right":
				idx = MOUSE_BUTTON_RIGHT
			elif kind == "wheel":
				idx = MOUSE_BUTTON_WHEEL_DOWN
			for p in [true, false]:
				var e := InputEventMouseButton.new()
				e.button_index = idx
				e.pressed = p
				if kind == "wheel":
					e.factor = 1.0
				evs.append(e)
		"release":
			var e := InputEventMouseButton.new()
			e.button_index = MOUSE_BUTTON_LEFT
			e.pressed = false
			evs.append(e)
		"touch":
			for p in [true, false]:
				var t := InputEventScreenTouch.new()
				t.pressed = p
				evs.append(t)
	for e in evs:
		e.position = pos
		if e is InputEventMouseButton:
			e.global_position = pos
		root.push_input(e, true)


func _next_case() -> void:
	_ci += 1
	if _ci >= _cases.size():
		return
	_base = _done
	_sent = false
	_fx.call("play_summon", true, _on_done)


func _process(_d: float) -> bool:
	_frame += 1
	if _frame == 5:
		_check_sizes()
		_next_case()
		return false
	if _ci < 0:
		return false
	if _ci >= _cases.size():
		print("TEST_SOUL_SUMMON_SKIP_TOUCH_OK" if _ok else "TEST_SOUL_SUMMON_SKIP_TOUCH_FAIL")
		quit(0 if _ok else 1)
		return true
	var c: Array = _cases[_ci]
	if not _sent:
		if not bool(_fx.get("_is_playing")):
			_fail("%s：還沒點就自己結束了（上一次演出的排程沒清掉？）" % c[0])
			_fx.call("play_summon", true, _on_done)
			_base = _done
		if float(_fx.get("_play_elapsed")) >= float(c[1]):
			_send(str(c[2]))
			_sent = true
			_wait_after = 3
		return false
	_wait_after -= 1
	if _wait_after > 0:
		return false
	var skipped: bool = _done > _base
	if skipped != bool(c[3]):
		_fail("%s：%s（演出時間 %.2fs）" % [c[0], "被跳過了" if skipped else "沒有跳過", float(c[1])])
	else:
		print("  ok %s → %s" % [c[0], "跳過" if skipped else "不跳過"])
	if not skipped:
		_fx.call("skip")
	_next_case()
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
		var fs: int = b.get_theme_font_size("font_size")
		if r.size.x < TOUCH_MIN or r.size.y < TOUCH_MIN:
			_fail("[%s] 跳過鈕 %s 小於 %dpx 觸控門檻" % [code, str(r.size), int(TOUCH_MIN)])
		if b.custom_minimum_size.y < TOUCH_MIN:
			_fail("[%s] 跳過鈕 custom_minimum_size %s 被蓋掉" % [code, str(b.custom_minimum_size)])
		if fs < FONT_MIN:
			_fail("[%s] 跳過鈕字級 %dpx < %dpx（共用樣式蓋回去了？）" % [code, fs, FONT_MIN])
		if r.size.x + 0.5 < need.x or r.size.y + 0.5 < need.y:
			_fail("[%s] 跳過鈕『%s』放不下文字：%s < %s" % [code, b.text, str(r.size), str(need)])
		var f: Font = b.get_theme_font("font")
		var tw: float = f.get_string_size(b.text, HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x if f else 0.0
		if tw > r.size.x - 16.0:
			_fail("[%s] 跳過鈕文字寬 %.0fpx 貼邊（鈕寬 %.0f）" % [code, tw, r.size.x])
		if not vp.grow(-8.0).encloses(r):
			_fail("[%s] 跳過鈕 %s 超出或貼住畫面邊（需在 safe area 內）" % [code, str(r)])
		print("  ok [%s] 跳過鈕『%s』%s 字級 %dpx 文字寬 %.0fpx" % [code, b.text, str(r.size), fs, tw])
	if loc:
		loc.call("set_locale", "zh_TW")
