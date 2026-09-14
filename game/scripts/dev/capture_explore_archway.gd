extends SceneTree
## C0 閣樓探索場拱門／牌樓修正驗證截圖產生器
## 依據任務規範：
## 1. 截圖存 proofs/explore_archway_fix/：改前、改後同一機位全景各一張，外加該區裁剪放大四倍各一張。
## 2. 切完 await RenderingServer.frame_post_draw 再 save_png。

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _proof_dir: String = ""
var _out_dir: String = ""
var _mode: String = "before"


func _initialize() -> void:
	print("=== 開始截取 C0 閣樓牌樓截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/explore_archway_fix")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--mode="):
			_mode = a.trim_prefix("--mode=")
	print("模式: ", _mode)

	change_scene_to_file("res://scenes/main.tscn")


func _save_image(filename: String, crop_rect: Rect2i = Rect2i(), scale_mult: int = 1) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex:
		var img := tex.get_image()
		if img:
			if crop_rect.size.x > 0 and crop_rect.size.y > 0:
				img = img.get_region(crop_rect)
			if scale_mult > 1:
				img.resize(img.get_width() * scale_mult, img.get_height() * scale_mult, Image.INTERPOLATE_NEAREST)
			var p1 := _proof_dir.path_join(filename)
			var p2 := _out_dir.path_join(filename)
			img.save_png(p1)
			img.save_png(p2)
			print("  ✓ 成功儲存截圖: ", p1)
		else:
			push_error("get_image() 回傳 null: " + filename)
	else:
		push_error("get_texture() 回傳 null: " + filename)


func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		0:
			if _frame >= 15:
				_main = current_scene
				if _main and _main.has_method("_open_explore"):
					var gs: Node = root.get_node_or_null("GameState")
					if gs:
						gs.call("reset_new_game")
						gs.set("player_name", "小白")
						gs.set("player_race", "rabbit")
						gs.set("chapter", "c0")
						gs.set("gold", 1234)
						gs.set("paperdoll_slots", {
							"race": "rabbit",
							"costume": "costume_nutcracker_guard",
							"chassis": "paint_ivory_stock",
							"costume_id": "costume_nutcracker_guard",
							"paint_id": "paint_ivory_stock"
						})
					print(">>> 開啟 C0 閣樓探索場 (village)...")
					var screen_v = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
					_main.call("_open_explore", "village", screen_v)
					_step = 1
					_frame = 0
				else:
					print("等待 main.tscn 就緒...")

		1:
			if _frame == 50:
				_async_capture()
				return false

	return false


func _async_capture() -> void:
	await RenderingServer.frame_post_draw
	# 1. 全景截圖
	var full_name := "%s.png" % _mode
	_save_image(full_name)

	# 2. 該區裁剪放大四倍（約 X 120-380, Y 200-400 區域，寬 260 高 200）
	var crop_box := Rect2i(120, 200, 260, 200)
	var crop_name := "%s_crop_4x.png" % _mode
	_save_image(crop_name, crop_box, 4)

	print("=== 實機截圖完成 (%s) ===" % _mode)
	print("CAPTURE_OK")
	quit(0)
