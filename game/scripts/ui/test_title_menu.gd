extends SceneTree
## 標題主選單：開始遊戲／設置／成就 + 結束遊戲，其餘進子選單。
## godot --headless -s res://scripts/ui/test_title_menu.gd


var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _collect_buttons(n: Node, out: Array) -> void:
	if n is Button:
		out.append((n as Button).text)
	for c in n.get_children():
		_collect_buttons(c, out)


func _host_buttons() -> Array:
	var host: Node = _main.get("host")
	var out: Array = []
	if host:
		_collect_buttons(host, out)
	return out


func _expect_buttons(where: String, want: Array) -> void:
	var got := _host_buttons()
	for w in want:
		var hit := false
		for g in got:
			if str(g).find(str(w)) >= 0:
				hit = true
				break
		if not hit:
			_fail("%s：找不到按鈕「%s」，實際有 %s" % [where, str(w), str(got)])
			return
	print("  ok %s 按鈕 %s" % [where, str(got)])


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
			if not _main.has_method("_go_title"):
				_fail("main.gd 缺少 _go_title()")
				return _finish()
			_main.call("_go_title")
			_step = 1
			_wait = 0
		1:
			if _wait < 8:
				return false
			var got := _host_buttons()
			if got.size() != 4:
				_fail("主選單應剛好 4 顆，實際 %d：%s" % [got.size(), str(got)])
			_expect_buttons("主選單", ["開始遊戲", "設置", "成就", "結束遊戲"])
			for extra in ["新的旅途", "繼續", "連線設定", "顯示設定", "旅途紀錄"]:
				for g in got:
					if str(g).find(extra) >= 0:
						_fail("主選單不該出現「%s」：%s" % [extra, str(got)])
						break
			_main.call("_go_title_start_menu")
			_step = 2
			_wait = 0
		2:
			if _wait < 8:
				return false
			_expect_buttons("開始遊戲子選單", ["新的旅途", "返回"])
			_main.call("_go_title_settings_menu")
			_step = 3
			_wait = 0
		3:
			if _wait < 8:
				return false
			var found_settings := false
			for c in _main.get_children():
				if c.get_script() and str(c.get_script().resource_path).ends_with("mobile_settings.gd"):
					found_settings = true
					break
			if found_settings:
				print("  ok 設置子選單 開啟 MobileSettings 視窗")
			else:
				_expect_buttons("設置子選單", ["連線", "顯示", "返回"])
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("TITLE_MENU_OK")
		quit(0)
	else:
		print("TITLE_MENU_FAIL")
		quit(1)
	return true
