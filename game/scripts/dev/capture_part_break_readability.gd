extends SceneTree

var _wait := 0
var _step := 0
var _main: Node = null
var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/combat",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_406bef6f/screenshots"
]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)
	change_scene_to_file("res://scenes/main.tscn")

func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null:
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("SAVED PROOF: ", p)

func _setup_player_env(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("energy", 15)
		gs.set("gold", 2500)
		gs.set("hp", 13)
		gs.set("max_hp", 50)
		gs.set("weapon_uses_left", 15)
		gs.set("weapon_uses_max", 16)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
	if sk:
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			print("Starting Battle 1: Leo (Dark Stone Wall background)")
			_setup_player_env("rabbit")
			if _main:
				_main.call("_start_battle_raw", "leo")
			_step = 1
			_wait = 0

		1:
			# 等待戰鬥載入並設置部位破壞
			if _wait == 25:
				var host: Control = _main.get("host") as Control
				if host and host.get_child_count() > 0:
					var bnode = host.get_child(0)
					var sim = bnode.get("sim")
					if sim:
						var boss = sim.call("_primary_boss_unit")
						if boss:
							boss.hp = 235
							boss.max_hp = 420
							sim.parts_break_unlocked = true
							sim.parts_break_stage = 1
							sim.focus_part_id = "body"
							# 破壞圓盾以展示未破壞(盔)與已破壞(盾/甲)對比
							if boss.parts.size() > 1:
								boss.parts[1]["hp"] = 0
								boss.parts[1]["broken"] = true
							if bnode.has_method("_refresh_part_bars"):
								bnode.call("_refresh_part_bars", boss)
							if bnode.has_method("_refresh_part_focus_hint"):
								bnode.call("_refresh_part_focus_hint")
							if bnode.has_method("_refresh_hud"):
								bnode.call("_refresh_hud")
			elif _wait >= 50:
				_save_viewport("proof_battle_part_break.png")
				print("Saved proof_battle_part_break.png (Leo - dark background)")
				_step = 2
				_wait = 0

		2:
			# 切換鎖定部位至盔，展示聚焦狀態
			if _wait == 10:
				var host: Control = _main.get("host") as Control
				if host and host.get_child_count() > 0:
					var bnode = host.get_child(0)
					var sim = bnode.get("sim")
					if sim:
						var boss = sim.call("_primary_boss_unit")
						if boss:
							sim.focus_part_id = "helmet"
							if bnode.has_method("_refresh_part_bars"):
								bnode.call("_refresh_part_bars", boss)
							if bnode.has_method("_refresh_part_focus_hint"):
								bnode.call("_refresh_part_focus_hint")
			elif _wait >= 30:
				_save_viewport("proof_battle_part_break_helm_focus.png")
				print("Saved proof_battle_part_break_helm_focus.png")
				print("Starting Battle 2: Bamboo Spirit (Bright / Light green background)")
				_step = 3
				_wait = 0

		3:
			# 啟動淺色/明亮背景戰鬥（falcon 巨鷹，森林明亮綠底），驗證明亮背景下的部位破壞卡片可讀性
			_setup_player_env("rabbit")
			if _main:
				_main.call("_start_battle_raw", "falcon")
			_step = 4
			_wait = 0

		4:
			if _wait == 25:
				var host: Control = _main.get("host") as Control
				if host and host.get_child_count() > 0:
					var bnode = host.get_child(0)
					var sim = bnode.get("sim")
					if sim:
						var boss = sim.call("_primary_boss_unit")
						if boss and boss.parts.size() > 0:
							sim.parts_break_unlocked = true
							sim.parts_break_stage = 1
							sim.focus_part_id = boss.parts[0].get("id", "")
							if bnode.has_method("_refresh_part_bars"):
								bnode.call("_refresh_part_bars", boss)
							if bnode.has_method("_refresh_part_focus_hint"):
								bnode.call("_refresh_part_focus_hint")
							if bnode.has_method("_refresh_hud"):
								bnode.call("_refresh_hud")
			elif _wait >= 50:
				_save_viewport("proof_battle_part_break_bright_bg.png")
				print("Saved proof_battle_part_break_bright_bg.png (Falcon - bright forest background)")
				print("ALL PROOFS CAPTURED SUCCESSFULLY")
				quit(0)
				return true
	return false
