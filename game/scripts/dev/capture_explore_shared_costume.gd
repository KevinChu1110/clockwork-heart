extends SceneTree
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_explore_shared_costume.gd

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _out_dir: String = ""
var _crops_dir: String = ""

func _initialize() -> void:
	print("=== 開始截取瓷韻熊貓與碧簧蛙探索待機實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe-shared-costume")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	change_scene_to_file("res://scenes/main.tscn")

func _save_image(filename: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex:
		var img := tex.get_image()
		if img:
			var p := _out_dir.path_join(filename)
			img.save_png(p)
			print("  ✓ 成功儲存實機截圖: ", p)
		else:
			push_error("get_image() 回傳 null: " + filename)
	else:
		push_error("get_texture() 回傳 null: " + filename)

func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		0:
			# 等待 main.tscn 載入完成並切換熊貓探索
			if _frame >= 15:
				_main = current_scene
				if _main and _main.has_method("_open_explore"):
					var gs: Node = root.get_node_or_null("GameState")
					if gs:
						gs.call("reset_new_game", "panda")
						gs.set("player_name", "瓷韻熊貓")
						gs.set("player_race", "panda")
						gs.set("chapter", "c0")
						gs.set("paperdoll_slots", {
							"race": "panda",
							"costume": "costume_dawn_monk_tunic",
							"costume_id": "costume_dawn_monk_tunic",
							"chassis": "paint_panda_porcelain",
							"paint_id": "paint_panda_porcelain",
							"weapon": "wpn_panda_taiji_cestus",
							"head_unit": "head_panda_brass_socket_ears",
							"optic_core": "core_obsidian_amber_quartz",
							"winding_key": "key_panda_taiji_ruyi_brass",
							"back_curio": "curio_panda_floating_taiji_box"
						})
					print(">>> [1/2] 開啟瓷韻熊貓 C0 探索場 (village)...")
					var screen_v = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
					_main.call("_open_explore", "village", screen_v)
					_step = 1
					_frame = 0

		1:
			# 等待熊貓探索轉場完成
			if _frame == 45:
				_async_capture_panda()
				return false

		2:
			# 等待切換蛙探索
			if _frame >= 15:
				if _main and _main.has_method("_open_explore"):
					var gs: Node = root.get_node_or_null("GameState")
					if gs:
						gs.call("reset_new_game", "frog")
						gs.set("player_name", "碧簧蛙")
						gs.set("player_race", "frog")
						gs.set("chapter", "c0")
						gs.set("paperdoll_slots", {
							"race": "frog",
							"costume": "costume_astral_cape",
							"costume_id": "costume_astral_cape",
							"chassis": "paint_frog_emerald",
							"paint_id": "paint_frog_emerald",
							"weapon": "wpn_lotus_cog_dart",
							"head_unit": "head_spring_frog_stock",
							"optic_core": "core_azure_aperture",
							"winding_key": "key_twin_wing_concentric",
							"back_curio": "curio_lotus_leaf_parasol"
						})
					print(">>> [2/2] 開啟碧簧蛙 C0 探索場 (village)...")
					var screen_v = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
					_main.call("_open_explore", "village", screen_v)
					_step = 3
					_frame = 0

		3:
			# 等待蛙探索轉場完成
			if _frame == 45:
				_async_capture_frog()
				return false

	return false

func _async_capture_panda() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_02_explore_panda_dawn_tunic.png")
	
	# 特寫
	var p := _out_dir.path_join("proof_02_explore_panda_dawn_tunic.png")
	if FileAccess.file_exists(p):
		var img := Image.load_from_file(p)
		if img and not img.is_empty():
			# 角色通常在中心偏左 (X: 450~650, Y: 280~520)
			var crop := img.get_region(Rect2i(450, 280, 220, 240))
			crop.save_png(_crops_dir.path_join("crop_explore_panda_character.png"))
	
	_step = 2
	_frame = 0

func _async_capture_frog() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_04_explore_frog_astral_cape.png")
	
	# 特寫
	var p := _out_dir.path_join("proof_04_explore_frog_astral_cape.png")
	if FileAccess.file_exists(p):
		var img := Image.load_from_file(p)
		if img and not img.is_empty():
			var crop := img.get_region(Rect2i(450, 280, 220, 240))
			crop.save_png(_crops_dir.path_join("crop_explore_frog_character.png"))

	print("=== 探索實機截圖完成 ===")
	quit(0)
