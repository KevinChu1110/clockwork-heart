extends SceneTree

var _frame: int = 0
var _step: int = 0
var _proof_dir: String = ""
var _out_dir: String = ""
var _view: Control = null


func _initialize() -> void:
	print("=== 開始截取抽魂與結果卡實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/soul_draw")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir)

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
			var p1 := _proof_dir.path_join(filename)
			var p2 := _out_dir.path_join(filename)
			img.save_png(p1)
			img.save_png(p2)
			print("  ✓ 成功儲存實機截圖: ", p1)
		else:
			push_error("get_image() 回傳 null: " + filename)
	else:
		push_error("get_texture() 回傳 null: " + filename)


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_async_capture_idle()
		1:
			pass
		2:
			if _frame >= 25:
				_step = 3
				_async_capture_pulled()
		3:
			pass
	return false


func _async_capture_idle() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_soul_draw_idle.png")
	print(">>> [1/2] 已截取未抽畫面，執行抽卡...")
	if _view and _view.has_method("_on_pull"):
		_view.call("_on_pull")
	_frame = 0
	_step = 2


func _async_capture_pulled() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_soul_draw_pulled.png")
	print(">>> [2/2] 已截取抽完畫面，完成！")
	quit(0)
