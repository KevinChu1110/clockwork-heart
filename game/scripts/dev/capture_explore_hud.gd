extends SceneTree
## 探索場景 HUD 疊層實機截圖產生器
## 依據任務規範：
## 1. 玩具堆邊緣 (village_outskirts)：地標膠囊全文露出、不被角色卡壓住
## 2. 荒路朝向世界大鐘 (road)：地標標籤全文露出、不被角色卡壓住前段
## 3. 小地圖完整圖例：小地圖圖例末端完整露出、不被容器 clip
## 4. 存 proofs/explore_hud/，檔名不跟既有撞。
## 5. 切完圖 await RenderingServer.frame_post_draw 再 save_png。

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _proof_dir: String = ""
var _out_dir: String = ""


func _initialize() -> void:
	print("=== 開始截取探索 HUD 疊層實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_proof_dir = base.path_join("../proofs/explore_hud")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_proof_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir)

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
			# 等待 main.tscn 載入完成
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
					print(">>> [1/3] 開啟 C0 玩具堆邊緣 (village_outskirts)...")
					var screen_v = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
					_main.call("_open_explore", "village_outskirts", screen_v)
					_step = 1
					_frame = 0
				else:
					print("等待 main.tscn 就緒...")

		1:
			# 等待轉場結束 (約 50 幀)
			if _frame == 50:
				_async_capture_step_1()
				return false

		2:
			# 等待第二張地圖 (荒路) 轉場完成
			if _frame == 50:
				_async_capture_step_2()
				return false

		3:
			# 等待第三張地圖 (十字路口 explore 小地圖) 轉場完成
			if _frame == 50:
				_async_capture_step_3()
				return false

	return false


func _async_capture_step_1() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_c0_outskirts_hud.png")
	print(">>> [2/3] 開啟 C0 荒路朝向世界大鐘 (road)...")
	var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
	_main.call("_open_explore", "road", screen_r)
	_step = 2
	_frame = 0


func _async_capture_step_2() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_c0_road_clock_hud.png")
	print(">>> [3/3] 開啟 C0 荒路交界小地圖完整圖例 (crossroads)...")
	var screen_r = _main.Screen.C0_ROAD if "Screen" in _main else 3
	_main.call("_open_explore", "crossroads", screen_r)
	_step = 3
	_frame = 0


func _async_capture_step_3() -> void:
	await RenderingServer.frame_post_draw
	_save_image("proof_c0_minimap_legend_full.png")
	_save_image("proof_c0_minimap_legend_crop.png", Rect2i(1040, 0, 240, 260))
	print("=== 全部實機截圖完成 ===")
	print("EXPLORE_HUD_CAPTURE_OK")
	quit(0)
