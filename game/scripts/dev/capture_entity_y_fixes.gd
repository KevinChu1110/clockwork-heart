extends SceneTree

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/entity_y_fixes",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_3f8c9f05/screenshots"
]

var _main: Node = null
var _step: int = 0
var _frame: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []


func _initialize() -> void:
	var main_res: PackedScene = load("res://scenes/main.tscn")
	if main_res == null:
		push_error("無法載入 main.tscn")
		quit(1)
		return
	var m := main_res.instantiate()
	root.add_child(m)
	current_scene = m
	_main = m


func _process(_delta: float) -> bool:
	_frame += 1
	_wait += 1

	match _step:
		0:
			# 等待 main.tscn 載入就緒
			if _wait >= 20:
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
					gs.set("chapter", "c1")
				print(">>> [Step 1] 開啟 crossroads (六域岔路)...")
				var screen_w = _main.Screen.C1_WILD if "Screen" in _main else 5
				_main.call("_open_explore", "crossroads", screen_w)
				_step = 1
				_wait = 0

		1:
			# 等待 crossroads 載入並移動相機到北部出口群
			if _wait >= 30:
				var exp_view: Node = _find_explore()
				if exp_view and is_instance_valid(exp_view):
					# 站於北山道與北道場下方，相機居中拍攝上緣邊界
					exp_view.set("player_pos", Vector2(1150, 220))
					if exp_view.has_method("_update_camera"):
						exp_view.call("_update_camera")
					if exp_view.has_method("_ysort_world"):
						exp_view.call("_ysort_world")
				_step = 2
				_wait = 0

		2:
			# 截圖 1: crossroads 北部出口（北山道 + 北·道場）
			if _wait >= 25:
				_save_viewport("proof_crossroads_north_exits.png", "crossroads north exits")
				# 移往東北·森林出口 (1640, 100)
				var exp_view: Node = _find_explore()
				if exp_view and is_instance_valid(exp_view):
					exp_view.set("player_pos", Vector2(1640, 220))
					if exp_view.has_method("_update_camera"):
						exp_view.call("_update_camera")
					if exp_view.has_method("_ysort_world"):
						exp_view.call("_ysort_world")
				_step = 3
				_wait = 0

		3:
			# 截圖 2: crossroads 東北·森林出口
			if _wait >= 25:
				_save_viewport("proof_crossroads_forest_exit.png", "crossroads northeast forest")
				print(">>> [Step 2] 開啟 coast_wreck (海岸·沉船灣)...")
				var screen_c = _main.Screen.C5_COAST if "Screen" in _main else 9
				_main.call("_open_explore", "coast_wreck", screen_c)
				_step = 4
				_wait = 0

		4:
			# 等待 coast_wreck 載入並移動玩家至斷桅 (1016, 100) 互動距離內 (1016, 125)
			if _wait >= 30:
				var exp_view: Node = _find_explore()
				if exp_view and is_instance_valid(exp_view):
					exp_view.set("player_pos", Vector2(1016, 125))
					if exp_view.has_method("_update_camera"):
						exp_view.call("_update_camera")
					if exp_view.has_method("_ysort_world"):
						exp_view.call("_ysort_world")
				_step = 5
				_wait = 0

		5:
			# 截圖 3: coast_wreck 斷桅與沉船殘骸
			if _wait >= 25:
				_save_viewport("proof_coast_wreck_mast.png", "coast_wreck mast")
				_finish()
				return false

	return false


func _find_explore() -> Node:
	if _main == null:
		return null
	return _main.get("_explore")


func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])


func _finish() -> void:
	print("=== 實體 Y 軸修正截圖完成 ===")
	print("total_saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  SAVED: ", s)
	for e in _errors:
		print("  ERROR: ", e)
	if _errors.is_empty() and not _saved.is_empty():
		print("ENTITY_Y_FIXES_CAPTURE_OK")
		quit(0)
	else:
		print("ENTITY_Y_FIXES_CAPTURE_FAIL")
		quit(1)
