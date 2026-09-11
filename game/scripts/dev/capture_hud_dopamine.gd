extends SceneTree
## 探索與戰鬥狀態板＋快捷欄多巴胺亮色盤實機截圖產生器

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/hud_dopamine")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			# 等待 main.tscn 載入
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var inv: Node = root.get_node_or_null("InventorySystem")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
					gs.set("level", 12)
					gs.set("hp", 350)
					gs.set("gold", 23456)
					gs.set("stardust", 88)
					gs.set("energy", 9)
					gs.set("energy_ts", Time.get_unix_time_from_system())
				if inv:
					inv.call("add_item", "hp_s", 5)
					inv.call("add_item", "mp_s", 3)
					inv.call("ensure_hotbar")
					inv.call("set_hotbar", 0, "hp_s")
					inv.call("set_hotbar", 1, "mp_s")

				# 開啟 village 探索
				var village_screen = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
				_main.call("_open_explore_then", "village", village_screen, Callable())
				_step = 1
				_frame = 0
		1:
			# 確保 HUD 與 Hotbar 可見並刷新
			if _frame >= 20:
				var hud = _main.get("_maple_hud")
				var hotbar = _main.get("_hotbar")
				if hud and is_instance_valid(hud):
					hud.visible = true
					if hud.has_method("refresh"):
						hud.call("refresh")
				if hotbar and is_instance_valid(hotbar):
					hotbar.visible = true
					if hotbar.has_method("refresh"):
						hotbar.call("refresh")

				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p_sc := _out_dir.path_join("proof_explore_hud_hotbar.png")
					var p_pr := _proof_dir.path_join("proof_explore_hud_hotbar.png")
					img.save_png(p_sc)
					img.save_png(p_pr)
					print("SAVED_EXPLORE: ", p_sc, " & ", p_pr)

				# 切換到戰鬥
				_main.call("_start_battle_raw", "road_bandit")
				_step = 2
				_frame = 0
		2:
			# 等待戰鬥畫面載入並穩定渲染
			if _frame >= 25:
				var hotbar = _main.get("_hotbar")
				if hotbar and is_instance_valid(hotbar):
					hotbar.visible = true
					if hotbar.has_method("refresh"):
						hotbar.call("refresh")

				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p_sc := _out_dir.path_join("proof_battle_hud_hotbar.png")
					var p_pr := _proof_dir.path_join("proof_battle_hud_hotbar.png")
					img.save_png(p_sc)
					img.save_png(p_pr)
					print("SAVED_BATTLE: ", p_sc, " & ", p_pr)

				print("HUD_DOPAMINE_CAPTURE_OK")
				quit(0)
				return true
	return false
