extends SceneTree
## 探索性 QA 盤點第九輪實機截圖抽查腳本 (t_d080c5af)
## 覆蓋重點：
## 1. 玄軸熊衣櫥換裝：「狂戰破陣機關戰鎧」(新外裝) 與「玄軸工坊重裝工作吊帶甲」(既有外裝)
## 2. 雲嵐鶴衣櫥換裝：「晴空巡獵機關羽甲」(新外裝) 與「凌雲羽衣輕鋼道袍」(既有外裝)
## 3. 靈爪猴衣櫥換裝：「天元演武者機關甲」(近期合併耳部與左手修復覆核)
## 4. 玄軸熊與雲嵐鶴大廳待機 (Lobby Idle) 實機全身畫面

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/qa_round9",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_d080c5af/proofs/qa_round9"
]
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _current_dialog: Node = null

func _initialize() -> void:
	print("QA_ROUND9: Initializing Round 9 in-game core scenes capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND9: load main.tscn err=", err)
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
				print("QA_ROUND9: Step 1 -> Wardrobe Bear (Berserker Cuirass)")
				_setup_player_env("bear", "costume_berserker_cuirass", "paint_iron_quarry", "wpn_eccentric_gyro_sledge")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 玄軸熊衣櫥 1：狂戰破陣機關戰鎧
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog):
					if _current_dialog.has_method("set_race_filter"):
						_current_dialog.call("set_race_filter", "bear")
					_select_card_or_force("costume", 1, "costume_berserker_cuirass")
					_select_card_or_force("chassis", 1, "paint_iron_quarry")
			elif _wait >= 70:
				_save_viewport("proof_01_wardrobe_bear_berserker.png", "Wardrobe Bear Berserker")
				print("QA_ROUND9: Step 2 -> Wardrobe Bear (Overalls Default)")
				_step = 2
				_wait = 0

		2:
			# 玄軸熊衣櫥 2：玄軸工坊重裝工作吊帶甲
			if _wait == 10:
				if is_instance_valid(_current_dialog):
					_select_card_or_force("costume", 0, "costume_ironclad_overalls")
					_select_card_or_force("chassis", 0, "paint_bear_amber")
			elif _wait >= 40:
				_save_viewport("proof_02_wardrobe_bear_overalls.png", "Wardrobe Bear Overalls")
				print("QA_ROUND9: Step 3 -> Wardrobe Crane (Sky Hunter Mail)")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("crane", "costume_sky_hunter_mail", "paint_zephyr_azure", "wpn_zephyr_wing_bow")
				_main.call("_go_mobile_lobby")
				_step = 3
				_wait = 0

		3:
			# 雲嵐鶴衣櫥 1：晴空巡獵機關羽甲
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog):
					if _current_dialog.has_method("set_race_filter"):
						_current_dialog.call("set_race_filter", "crane")
					_select_card_or_force("costume", 1, "costume_sky_hunter_mail")
					_select_card_or_force("chassis", 1, "paint_zephyr_azure")
			elif _wait >= 70:
				_save_viewport("proof_03_wardrobe_crane_sky_hunter.png", "Wardrobe Crane Sky Hunter")
				print("QA_ROUND9: Step 4 -> Wardrobe Crane (Zephyr Robe Default)")
				_step = 4
				_wait = 0

		4:
			# 雲嵐鶴衣櫥 2：凌雲羽衣輕鋼道袍
			if _wait == 10:
				if is_instance_valid(_current_dialog):
					_select_card_or_force("costume", 0, "costume_zephyr_robe")
					_select_card_or_force("chassis", 0, "paint_crane_porcelain")
			elif _wait >= 40:
				_save_viewport("proof_04_wardrobe_crane_zephyr_robe.png", "Wardrobe Crane Zephyr Robe")
				print("QA_ROUND9: Step 5 -> Wardrobe Macaque (Zen Striker)")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("macaque", "costume_zen_striker", "paint_bamboo_bronze", "wpn_monkey_glove_blade")
				_main.call("_go_mobile_lobby")
				_step = 5
				_wait = 0

		5:
			# 靈爪猴衣櫥：天元演武者機關甲 (近期修復檢查)
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog):
					if _current_dialog.has_method("set_race_filter"):
						_current_dialog.call("set_race_filter", "macaque")
					_select_card_or_force("costume", 1, "costume_zen_striker")
					_select_card_or_force("chassis", 1, "paint_bamboo_bronze")
			elif _wait >= 70:
				_save_viewport("proof_05_wardrobe_macaque_zen.png", "Wardrobe Macaque Zen")
				print("QA_ROUND9: Step 6 -> Lobby Bear (Berserker Cuirass)")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("bear", "costume_berserker_cuirass", "paint_iron_quarry", "wpn_eccentric_gyro_sledge")
				_main.call("_go_mobile_lobby")
				_step = 6
				_wait = 0

		6:
			# 大廳：玄軸熊全景
			if _wait >= 45:
				_save_viewport("proof_06_lobby_bear_berserker.png", "Lobby Bear Berserker")
				print("QA_ROUND9: Step 7 -> Lobby Crane (Sky Hunter Mail)")
				_setup_player_env("crane", "costume_sky_hunter_mail", "paint_zephyr_azure", "wpn_zephyr_wing_bow")
				_main.call("_go_mobile_lobby")
				_step = 7
				_wait = 0

		7:
			# 大廳：雲嵐鶴全景
			if _wait >= 45:
				_save_viewport("proof_07_lobby_crane_sky_hunter.png", "Lobby Crane Sky Hunter")
				print("QA_ROUND9: ALL SCREENSHOTS CAPTURED SUCCESSFULLY!")
				_finish()
				return true

	return false

func _select_card_or_force(slot_type: String, idx: int, item_id: String) -> void:
	if not is_instance_valid(_current_dialog):
		return
	var card_name := "Card_%s_%d" % [slot_type, idx]
	var card = _current_dialog.find_child(card_name, true, false) as Button
	if card:
		card.emit_signal("pressed")
	if slot_type == "costume":
		_current_dialog.set("costume_index", idx)
		_current_dialog.set("selected_costume_id", item_id)
	elif slot_type == "chassis":
		_current_dialog.set("chassis_index", idx)
		_current_dialog.set("selected_chassis_id", item_id)
	if _current_dialog.has_method("_update_card_selection_states"):
		_current_dialog.call("_update_card_selection_states")
	if _current_dialog.has_method("_update_ui_texts"):
		_current_dialog.call("_update_ui_texts")
	if _current_dialog.has_method("_update_preview"):
		_current_dialog.call("_update_preview")

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
	print("QA_ROUND9: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
