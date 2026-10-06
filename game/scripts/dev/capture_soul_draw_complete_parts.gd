extends SceneTree

var _frame: int = 0
var _step: int = 0
var _view: Control = null
var _ws: String = ""

func _initialize() -> void:
	print("=== 開始截取聚魂十連抽完整零件與五色稀有度實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_ws = OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if _ws == "":
		_ws = ProjectSettings.globalize_path("res://..")

	var view_script = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
	_view = view_script.new()
	_view.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(_view)


func _save_image(filename: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex:
		var img := tex.get_image()
		if img:
			# 儲存於根目錄、proofs/t_77530648 與 screenshots
			var paths := [
				_ws.path_join(filename),
				_ws.path_join("proofs/t_77530648").path_join(filename),
				_ws.path_join("screenshots").path_join(filename)
			]
			for p in paths:
				var dir: String = p.get_base_dir()
				DirAccess.make_dir_recursive_absolute(dir)
				var err := img.save_png(p)
				if err == OK:
					print("  ✓ 成功儲存實機截圖: ", p)
				else:
					push_error("儲存失敗: " + p)
		else:
			push_error("get_image() 回傳 null: " + filename)
	else:
		push_error("get_texture() 回傳 null: " + filename)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_frame = 0
				_step = 1
				_trigger_ten_pull()
		1:
			if _frame >= 10:
				_frame = 0
				_step = 2
				_skip_summon_fx()
		2:
			# 等候十張卡面錯落展開動畫就緒（約 40-50 幀）
			if _frame >= 45:
				_frame = 0
				_step = 3
				_capture_result()
		3:
			pass
	return false


func _trigger_ten_pull() -> void:
	print(">>> [1/3] 充足票數並執行十連抽...")
	if _view != null and _view.get("econ") != null:
		_view.econ.soul_tickets = 50
	if _view != null and _view.has_method("_on_pull_ten"):
		_view.call("_on_pull_ten")


func _skip_summon_fx() -> void:
	print(">>> [2/3] 跳過過場動畫，直接呈現十連結果卡...")
	var fx = _view.get_node_or_null("SoulSummonFx") if _view else null
	if fx and fx.has_method("skip"):
		fx.call("skip")


func _capture_result() -> void:
	print(">>> [3/3] 擷取十連抽結果面板存證...")
	_save_image("proof_soul_draw_complete_parts.png")
	print("=== 完成截圖 ===")
	quit(0)
