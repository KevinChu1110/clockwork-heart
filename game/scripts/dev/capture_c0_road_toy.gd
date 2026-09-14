extends SceneTree
## 截取 C0 荒路四張地圖改名後的實機畫面與戰鬥敵名
## 輸出至 proofs/c0_road_toy/

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _battle: Node = null
var _proof_dir: String = ""

func _initialize() -> void:
	print("=== 開始截取 C0 玩具堆外緣地圖與戰鬥實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/c0_road_toy")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _save_image(filename: String, crop: Rect2i = Rect2i(), scale_mult: int = 1) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex:
		var img := tex.get_image()
		if img:
			if crop.size.x > 0 and crop.size.y > 0:
				img = img.get_region(crop)
			if scale_mult > 1:
				img.resize(img.get_width() * scale_mult, img.get_height() * scale_mult, Image.INTERPOLATE_NEAREST)
			var p := _proof_dir.path_join(filename)
			img.save_png(p)
			print("  ✓ 成功儲存: ", p)
		else:
			push_error("get_image() null: " + filename)
	else:
		push_error("get_texture() null: " + filename)


func _process(_delta: float) -> bool:
	_frame += 1

	match _step:
		0:
			if _frame >= 20:
				_main = current_scene
				if _main and _main.has_method("_open_explore"):
					var gs: Node = root.get_node_or_null("GameState")
					if gs:
						gs.call("reset_new_game")
						gs.set("player_name", "小白")
						gs.set("player_race", "rabbit")
						gs.set("chapter", "c0")
					print(">>> [1/5] 開啟 road: 玩具堆外緣 · 朝向世界大鐘...")
					var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
					_main.call("_open_explore", "road", screen_r)
					_step = 1
					_frame = 0

		1:
			if _frame == 45:
				_save_image("proof_01_road.png")
				_save_image("crop_01_road_title.png", Rect2i(310, 8, 380, 50), 2)
				print(">>> [2/5] 開啟 road_bridge: 玩具堆外緣 · 積木斷橋...")
				var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
				_main.call("_open_explore", "road_bridge", screen_r)
				_step = 2
				_frame = 0

		2:
			if _frame == 45:
				_save_image("proof_02_road_bridge.png")
				_save_image("crop_02_road_bridge_title.png", Rect2i(310, 8, 380, 50), 2)
				print(">>> [3/5] 開啟 road_inn: 玩具堆外緣 · 停擺旅舍...")
				var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
				_main.call("_open_explore", "road_inn", screen_r)
				_step = 3
				_frame = 0

		3:
			if _frame == 45:
				_save_image("proof_03_road_inn.png")
				_save_image("crop_03_road_inn_title.png", Rect2i(310, 8, 380, 50), 2)
				print(">>> [4/5] 開啟 road_ruins: 玩具堆外緣 · 舊上鍊站...")
				var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
				_main.call("_open_explore", "road_ruins", screen_r)
				_step = 4
				_frame = 0

		4:
			if _frame == 45:
				_save_image("proof_04_road_ruins.png")
				_save_image("crop_04_road_ruins_title.png", Rect2i(310, 8, 380, 50), 2)
				print(">>> [5/5] 開啟戰鬥畫面: road_bandit (銹蝕哨兵偶)...")
				_main.queue_free()
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "road_bandit")
				_step = 5
				_frame = 0

		5:
			if _frame == 45:
				_save_image("proof_05_battle_road_bandit.png")
				# 敵方血條與名字區域大約在右上角 (X 800-1260, Y 10-100)
				_save_image("crop_05_enemy_name.png", Rect2i(800, 10, 460, 90), 2)
				print("=== 全部實機截圖完成 (共 5 張全景 + 5 張局部) ===")
				print("ROAD_MAPS_CAPTURE_OK")
				quit(0)

	return false
