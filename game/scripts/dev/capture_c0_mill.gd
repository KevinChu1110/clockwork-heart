extends SceneTree

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _explore: Control = null
var _proof_dir: String = ""

func _initialize() -> void:
	print("=== 開始截取 C0 風車積木田玩具化實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/c0_mill_toy")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _save_image(filename: String, crop_rect: Rect2i = Rect2i()) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex:
		var img := tex.get_image()
		if img:
			if crop_rect.size.x > 0 and crop_rect.size.y > 0:
				img = img.get_region(crop_rect)
			var p1 := _proof_dir.path_join(filename)
			img.save_png(p1)
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
						gs.set("paperdoll_slots", {
							"race": "rabbit",
							"costume": "costume_nutcracker_guard",
							"chassis": "paint_ivory_stock",
							"costume_id": "costume_nutcracker_guard",
							"paint_id": "paint_ivory_stock"
						})
					print(">>> 開啟 C0 風車積木田 (village_mill)...")
					var screen_v = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
					_main.call("_open_explore", "village_mill", screen_v)
					_step = 1
					_frame = 0

		1:
			# 等待轉場完成 (50 幀)
			if _frame == 50:
				_explore = _main.get("_explore")
				_step_capture_overview()
				return false

		2:
			# 截取 scare_b (第二哨兵偶)
			if _frame == 20:
				_step_capture_scare_b()
				return false

		3:
			# 截取 big_mill (巨型發條風車)
			if _frame == 20:
				_step_capture_big_mill()
				return false

		4:
			# 截取 back_from_mill (回玩具堆邊緣)
			if _frame == 20:
				_step_capture_back_from_mill()
				return false

		5:
			# 截取 mill_to_road (捷徑·外緣)
			if _frame == 20:
				_step_capture_mill_to_road()
				return false

	return false


func _step_capture_overview() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_c0_mill_overview.png")

	# 移動玩家至 scare_b 附近 (744, 1026)
	if _explore:
		_explore.player_pos = Vector2(744, 1046)
		_explore._update_near()
		_explore._update_camera()

	_step = 2
	_frame = 0


func _step_capture_scare_b() -> void:
	await RenderingServer.frame_post_draw
	var node: Control = _explore._entity_nodes.get("scare_b")
	var chip: Control = node.get_meta("name_chip") if node and node.has_meta("name_chip") else null
	if chip:
		chip.visible = true
	await RenderingServer.frame_post_draw

	var pt: Vector2 = chip.global_position if chip else (node.global_position if node else Vector2(640, 360))
	var r := Rect2i(int(pt.x - 50), int(pt.y - 70), 220, 160)
	_save_image("crop_scare_b.png", r)

	# 移動玩家至 big_mill 附近 (864, 891)
	if _explore:
		_explore.player_pos = Vector2(864, 915)
		_explore._update_near()
		_explore._update_camera()

	_step = 3
	_frame = 0


func _step_capture_big_mill() -> void:
	await RenderingServer.frame_post_draw
	var node: Control = _explore._entity_nodes.get("big_mill")
	var chip: Control = node.get_meta("name_chip") if node and node.has_meta("name_chip") else null
	if chip:
		chip.visible = true
	await RenderingServer.frame_post_draw

	var pt: Vector2 = chip.global_position if chip else (node.global_position if node else Vector2(640, 360))
	var r := Rect2i(int(pt.x - 50), int(pt.y - 70), 240, 160)
	_save_image("crop_big_mill.png", r)

	# 移動玩家至 back_from_mill 附近 (840, 1215)
	if _explore:
		_explore.player_pos = Vector2(840, 1235)
		_explore._update_near()
		_explore._update_camera()

	_step = 4
	_frame = 0


func _step_capture_back_from_mill() -> void:
	await RenderingServer.frame_post_draw
	var node: Control = _explore._entity_nodes.get("back_from_mill")
	var chip: Control = node.get_meta("name_chip") if node and node.has_meta("name_chip") else null
	if chip:
		chip.visible = true
	await RenderingServer.frame_post_draw

	var pt: Vector2 = chip.global_position if chip else (node.global_position if node else Vector2(640, 360))
	var r := Rect2i(int(pt.x - 50), int(pt.y - 70), 240, 160)
	_save_image("crop_back_from_mill.png", r)

	# 移動玩家至 mill_to_road 附近 (2208, 1080)
	if _explore:
		_explore.player_pos = Vector2(2208, 1100)
		_explore._update_near()
		_explore._update_camera()

	_step = 5
	_frame = 0


func _step_capture_mill_to_road() -> void:
	await RenderingServer.frame_post_draw
	var node: Control = _explore._entity_nodes.get("mill_to_road")
	var chip: Control = node.get_meta("name_chip") if node and node.has_meta("name_chip") else null
	if chip:
		chip.visible = true
	await RenderingServer.frame_post_draw

	var pt: Vector2 = chip.global_position if chip else (node.global_position if node else Vector2(640, 360))
	var r := Rect2i(int(pt.x - 50), int(pt.y - 70), 220, 160)
	_save_image("crop_mill_to_road.png", r)

	print("=== 全部實機截圖完成 ===")
	quit(0)
