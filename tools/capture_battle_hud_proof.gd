extends SceneTree

var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			if _main == null or gs == null:
				quit(1)
				return true
			gs.call("reset_new_game")
			gs.set("player_name", "小白")
			gs.set("player_race", "rabbit")
			_main.call("_start_battle_raw", "road_bandit")
			_step = 1
			_wait = 0
		1:
			if _wait < 25:
				return false
			var host: Control = _main.get("host") as Control
			if host and host.get_child_count() > 0:
				_battle = host.get_child(0) as Control
			if _battle == null or not is_instance_valid(_battle):
				quit(1)
				return true
			
			var sim = _battle.get("sim")
			if sim:
				sim.sim_paused = true
				var p = sim.get_unit("player")
				if p:
					p.can_skill = true
					p.bare_fisted = false
					p.weapon_class = "sword"
					p.rage = 100.0
			_battle.call("_refresh_hud")
			_step = 2
			_wait = 0
		2:
			if _wait < 8:
				return false
			
			var eb: Control = _battle.get("enemy_body") as Control
			if eb:
				print("ENEMY_BODY_RECT: ", eb.get_global_rect())
			var tp: Control = _battle.get("_thumb_pad") as Control
			if tp:
				print("THUMB_PAD_RECT: ", tp.get_global_rect())
			var wd: Control = _battle.get("_weapon_dock") as Control
			if wd:
				print("WEAPON_DOCK_RECT: ", wd.get_global_rect())
			var tc: Dictionary = _battle.call("thumb_controls")
			for k in tc:
				if tc[k] is Control:
					print("CTRL ", k, ": ", (tc[k] as Control).get_global_rect())

			var dir := ProjectSettings.globalize_path("res://").path_join("../screenshots")
			DirAccess.make_dir_recursive_absolute(dir)
			
			var img: Image = root.get_viewport().get_texture().get_image()
			if img:
				var path1 := dir.path_join("proof_battle_hud_dopamine.png")
				img.save_png(path1)
				print("PROOF_BATTLE_SAVED: ", path1, " size=", img.get_width(), "x", img.get_height())
			
			# Now simulate telegraphing for windup parry button check
			_battle.call("_update_thumb_attack_text", "發條格擋")
			_step = 3
			_wait = 0
		3:
			if _wait < 8:
				return false
			var dir2 := ProjectSettings.globalize_path("res://").path_join("../screenshots")
			var img2: Image = root.get_viewport().get_texture().get_image()
			if img2:
				var path2 := dir2.path_join("proof_battle_hud_parry.png")
				img2.save_png(path2)
				print("PROOF_PARRY_SAVED: ", path2, " size=", img2.get_width(), "x", img2.get_height())
			
			print("CAPTURE_ALL_SUCCESS")
			quit(0)
			return true
	return false
