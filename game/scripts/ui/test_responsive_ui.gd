extends SceneTree
## 響應式 UI：Safe Area、彈窗寬、核心熱區、2 列網格、✕ 不被裁。
## godot --headless -s res://scripts/ui/test_responsive_ui.gd

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")

const ASPECTS: Array = [
	{"name": "16:9", "size": Vector2i(1280, 720)},
	{"name": "19.5:9", "size": Vector2i(1560, 720)},
	{"name": "20:9", "size": Vector2i(1600, 720)},
	{"name": "tablet", "size": Vector2i(1024, 768)},
	{"name": "PC", "size": Vector2i(1920, 1080)},
]

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _aspect_i := 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _min_btn_h(n: Node, floor_h: float = 50.0) -> void:
	if n is Button:
		var b := n as Button
		var h: float = maxf(b.custom_minimum_size.y, b.size.y)
		if h + 0.5 < floor_h:
			_fail("按鈕「%s」高 %.1f < %.0f" % [b.text, h, floor_h])
	for c in n.get_children():
		_min_btn_h(c, floor_h)


func _find_named(n: Node, name: String) -> Node:
	if n.name == name:
		return n
	for c in n.get_children():
		var hit := _find_named(c, name)
		if hit:
			return hit
	return null


func _assert_card_width(card: Control, where: String) -> void:
	if card == null:
		_fail("%s：找不到彈窗卡" % where)
		return
	var w: float = maxf(card.custom_minimum_size.x, card.size.x)
	if w < 739.0 or w > 761.0:
		_fail("%s：寬 %.1f 不在 740–760" % [where, w])
	else:
		print("  ok %s 寬 %.0f" % [where, w])
	if w <= 420.5:
		_fail("%s：窄欄 %.1f" % [where, w])


func _assert_title_grid(host: Node) -> void:
	var grid := _find_named(host, "TitleMenuGrid") as GridContainer
	if grid == null:
		_fail("標題沒有 TitleMenuGrid")
		return
	if grid.columns > 2:
		_fail("標題網格 %d 列 > 2" % grid.columns)
	var n_btn := 0
	for c in grid.get_children():
		if c is Button:
			n_btn += 1
			var b := c as Button
			if b.size.x > 500.0:
				_fail("標題鈕「%s」寬 %.0f 仍是全寬長條" % [b.text, b.size.x])
	if n_btn < 1:
		_fail("標題網格沒有按鈕")
	else:
		print("  ok 標題 2 列網格 columns=%d buttons=%d" % [grid.columns, n_btn])


func _assert_close_visible(n: Node, where: String) -> void:
	var btn := _find_named(n, "CloseBtn") as Button
	if btn == null:
		_fail("%s：沒有 CloseBtn" % where)
		return
	if btn.text != "✕":
		_fail("%s：關閉鈕是「%s」不是 ✕" % [where, btn.text])
	var sz := Vector2(
		maxf(btn.custom_minimum_size.x, btn.size.x),
		maxf(btn.custom_minimum_size.y, btn.size.y)
	)
	if sz.x + 0.5 < 50.0 or sz.y + 0.5 < 50.0:
		_fail("%s：關閉熱區 %s < 50" % [where, str(sz)])
	var r := btn.get_global_rect()
	var vp := root.get_visible_rect()
	if r.size.x < 1.0 or r.size.y < 1.0:
		_fail("%s：關閉鈕尚未排版 r=%s" % [where, str(r)])
		return
	if r.position.x < vp.position.x - 1.0 or r.position.y < vp.position.y - 1.0 \
			or r.end.x > vp.end.x + 1.0 or r.end.y > vp.end.y + 1.0:
		_fail("%s：關閉鈕被裁 r=%s vp=%s" % [where, str(r), str(vp)])
	else:
		print("  ok %s 關閉鈕可見 r=%s" % [where, str(r)])


func _build_aspect() -> void:
	if _main == null:
		_fail("main 沒載起來")
		return
	_main.call("_go_title")
	_main.call("_open_pause")


func _check_aspect(tag: String) -> void:
	print("== ", tag, " vp=", root.size, " visible=", root.get_visible_rect().size)
	var dummy := Control.new()
	root.add_child(dummy)
	var w := ResponsiveUi.dialog_width(dummy)
	if w < 739.0 or w > 761.0:
		_fail("%s dialog_width=%.1f" % [tag, w])
	else:
		print("  ok dialog_width %.0f" % w)
	dummy.queue_free()

	if _main == null:
		_fail("main 沒載起來")
		return
	var host: Node = _main.get("host")
	if host == null:
		_fail("沒有 host")
		return
	_min_btn_h(host)
	var title_card := _find_named(host, "TitleMenuCard") as Control
	_assert_card_width(title_card, "標題選單")
	_assert_title_grid(host)
	_assert_close_visible(host, "標題")

	var pause: Node = _main.get("_pause_layer")
	if pause == null:
		_fail("暫停層沒建起來")
	else:
		_min_btn_h(pause)
		var pcard := _find_named(pause, "PauseCard") as Control
		_assert_card_width(pcard, "暫停")
		_assert_close_visible(pause, "暫停")
	_main.call("_close_pause")
	print("  ok 核心熱區 ≥50")


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			if _main == null:
				_fail("main scene 沒載起來")
				return _finish()
			_step = 1
			_wait = 0
			_aspect_i = 0
		1:
			if _aspect_i >= ASPECTS.size():
				return _finish()
			var a: Dictionary = ASPECTS[_aspect_i]
			root.size = a["size"]
			_wait = 0
			_step = 2
		2:
			if _wait < 6:
				return false
			_build_aspect()
			_wait = 0
			_step = 3
		3:
			if _wait < 8:
				return false
			var a: Dictionary = ASPECTS[_aspect_i]
			_check_aspect(str(a["name"]))
			_aspect_i += 1
			_step = 1
			_wait = 0
	return false


func _finish() -> bool:
	if _ok:
		print("RESPONSIVE_UI_OK")
		quit(0)
	else:
		print("RESPONSIVE_UI_FAIL")
		quit(1)
	return true
