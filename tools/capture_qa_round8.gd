extends SceneTree
## 探索性 QA 盤點第八輪實機截圖抽查腳本 (t_c46b102c)
## 覆蓋受近期合併影響之四族：玄軸熊、蒸氣企鵝、烈焰虎、雲嵐鶴
## 抽查項目：
## 1. 大廳待機 (Lobby Idle): 4族 (熊/企鵝/虎/鶴)
## 2. 戰鬥待機 (Battle Idle): 4族 (熊/企鵝/虎/鶴)
## 3. 衣櫥換裝 (Wardrobe Dialog): 4族 (熊/企鵝/虎/鶴)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/qa_round8",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c46b102c/proofs/qa_round8"
]
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _current_dialog: Node = null

func _initialize() -> void:
	print("QA_ROUND8: Initializing Round 8 in-game core scenes capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND8: load main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main.tscn 就緒
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("QA_ROUND8: Step 1 -> Lobby Bear")
				_setup_player_env("bear", "costume_berserker_cuirass", "paint_iron_quarry", "wpn_eccentric_gyro_sledge")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 大廳 1：玄軸熊
			if _wait >= 45:
				_save_viewport("proof_01_lobby_bear.png", "Lobby Bear")
				print("QA_ROUND8: Step 2 -> Lobby Penguin")
				_setup_player_env("penguin", "costume_abyssal_diver_cuirass", "paint_polar_frost", "wpn_twin_harpoon_gun")
				_main.call("_go_mobile_lobby")
				_step = 2
				_wait = 0

		2:
			# 大廳 2：蒸氣企鵝
			if _wait >= 45:
				_save_viewport("proof_02_lobby_penguin.png", "Lobby Penguin")
				print("QA_ROUND8: Step 3 -> Lobby Tiger")
				_setup_player_env("tiger", "costume_ash_ninja_garb", "paint_volcano_black", "wpn_twin_ember_sabers")
				_main.call("_go_mobile_lobby")
				_step = 3
				_wait = 0

		3:
			# 大廳 3：烈焰虎
			if _wait >= 45:
				_save_viewport("proof_03_lobby_tiger.png", "Lobby Tiger")
				print("QA_ROUND8: Step 4 -> Lobby Crane")
				_setup_player_env("crane", "costume_sky_hunter_mail", "paint_ivory_stock", "wpn_zephyr_wing_bow")
				_main.call("_go_mobile_lobby")
				_step = 4
				_wait = 0

		4:
			# 大廳 4：雲嵐鶴
			if _wait >= 45:
				_save_viewport("proof_04_lobby_crane.png", "Lobby Crane")
				print("QA_ROUND8: Step 5 -> Battle Bear")
				_setup_player_env("bear", "costume_berserker_cuirass", "paint_iron_quarry", "wpn_eccentric_gyro_sledge")
				_main.call("proof_show_battle", "black_ronin")
				_step = 5
				_wait = 0

		5:
			# 戰鬥 1：玄軸熊
			if _wait >= 50:
				_save_viewport("proof_05_battle_bear.png", "Battle Bear")
				print("QA_ROUND8: Step 6 -> Battle Penguin")
				_setup_player_env("penguin", "costume_abyssal_diver_cuirass", "paint_polar_frost", "wpn_twin_harpoon_gun")
				_main.call("proof_show_battle", "road_bandit")
				_step = 6
				_wait = 0

		6:
			# 戰鬥 2：蒸氣企鵝
			if _wait >= 35:
				_save_viewport("proof_06_battle_penguin.png", "Battle Penguin")
				print("QA_ROUND8: Step 7 -> Battle Tiger")
				_setup_player_env("tiger", "costume_ash_ninja_garb", "paint_volcano_black", "wpn_twin_ember_sabers")
				_main.call("proof_show_battle", "black_ronin")
				_step = 7
				_wait = 0

		7:
			# 戰鬥 3：烈焰虎
			if _wait >= 35:
				_save_viewport("proof_07_battle_tiger.png", "Battle Tiger")
				print("QA_ROUND8: Step 8 -> Battle Crane")
				_setup_player_env("crane", "costume_sky_hunter_mail", "paint_ivory_stock", "wpn_zephyr_wing_bow")
				_main.call("proof_show_battle", "road_bandit")
				_step = 8
				_wait = 0

		8:
			# 戰鬥 4：雲嵐鶴
			if _wait >= 35:
				_save_viewport("proof_08_battle_crane.png", "Battle Crane")
				print("QA_ROUND8: Step 9 -> Wardrobe Bear")
				_setup_player_env("bear", "costume_berserker_cuirass", "paint_iron_quarry", "wpn_eccentric_gyro_sledge")
				_main.call("_go_mobile_lobby")
				_step = 9
				_wait = 0

		9:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "bear")
			elif _wait >= 65:
				# 衣櫥 1：玄軸熊
				_save_viewport("proof_09_wardrobe_bear.png", "Wardrobe Bear")
				print("QA_ROUND8: Step 10 -> Wardrobe Penguin")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("penguin", "costume_abyssal_diver_cuirass", "paint_polar_frost", "wpn_twin_harpoon_gun")
				_main.call("_go_mobile_lobby")
				_step = 10
				_wait = 0

		10:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "penguin")
			elif _wait >= 65:
				# 衣櫥 2：蒸氣企鵝
				_save_viewport("proof_10_wardrobe_penguin.png", "Wardrobe Penguin")
				print("QA_ROUND8: Step 11 -> Wardrobe Tiger")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("tiger", "costume_ash_ninja_garb", "paint_volcano_black", "wpn_twin_ember_sabers")
				_main.call("_go_mobile_lobby")
				_step = 11
				_wait = 0

		11:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "tiger")
			elif _wait >= 65:
				# 衣櫥 3：烈焰虎
				_save_viewport("proof_11_wardrobe_tiger.png", "Wardrobe Tiger")
				print("QA_ROUND8: Step 12 -> Wardrobe Crane")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("crane", "costume_sky_hunter_mail", "paint_ivory_stock", "wpn_zephyr_wing_bow")
				_main.call("_go_mobile_lobby")
				_step = 12
				_wait = 0

		12:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "crane")
			elif _wait >= 65:
				# 衣櫥 4：雲嵐鶴
				_save_viewport("proof_12_wardrobe_crane.png", "Wardrobe Crane")
				print("QA_ROUND8: ALL IN-GAME CAPTURES FINISHED SUCCESSFULLY!")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_finish()
				return true

	return false

func _setup_player_env(race: String, costume: String = "", chassis: String = "", weapon: String = "") -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("player_race", race)
		gs.set("hp", 999)
		gs.set("max_hp", 999)
		gs.set("energy", 15)
		gs.set("gold", 8888)
		gs.set("stardust", 30)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
		var slots: Dictionary = gs.get("paperdoll_slots")
		if slots == null:
			slots = {}
		slots["race"] = race
		if costume != "":
			slots["costume"] = costume
			slots["costume_id"] = costume
		if chassis != "":
			slots["chassis"] = chassis
			slots["chassis_id"] = chassis
		if weapon != "":
			slots["weapon"] = weapon
			slots["weapon_id"] = weapon
		gs.set("paperdoll_slots", slots)

	var tut: Node = root.get_node_or_null("TutorialSystem")
	if tut and tut.has_method("mark"):
		for k in ["boot", "explore", "battle_auto", "battle_parry", "battle_fog", "forge", "paths", "soul", "fort", "flag_hint", "ng"]:
			tut.call("mark", k)
	if sk and sk.has_method("ensure_skill_map"):
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")

func _find_lobby() -> Node:
	if _main:
		var host = _main.get("host") as Control
		if host:
			for c in host.get_children():
				if c is MobileLobby:
					return c
		var host_node = _main.get_node_or_null("Host")
		if host_node:
			for c in host_node.get_children():
				if c is MobileLobby:
					return c
	return null

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])

func _finish() -> void:
	print("QA_ROUND8: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
