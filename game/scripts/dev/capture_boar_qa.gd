extends SceneTree
## 驗證與擷取「石拳 (boar)」對話與戰鬥實機畫面證明

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_0fa38966/screenshots"
]

var _main: Node = null
var _phase: int = 0
var _wait: int = 0

func _initialize() -> void:
	print("CAPTURE_BOAR_QA: Initializing...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("CAPTURE_BOAR_QA: change_scene_to_file err=", err)
	_phase = 0
	_wait = 0

func _setup_player_env() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("energy", 30)
		gs.set("gold", 5000)
		gs.set("hp", 80)
		gs.set("max_hp", 80)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
	if sk:
		sk.call("ensure_skill_map")

func _process(_delta: float) -> bool:
	_wait += 1
	match _phase:
		0:
			if _wait >= 40:
				_main = root.get_node_or_null("Main")
				if _main == null:
					_main = root.get_child(root.get_child_count() - 1)
				print("CAPTURE_BOAR_QA: Main scene is ", _main.name if _main else "null")
				_setup_player_env()
				_phase = 1
				_wait = 0
		1:
			if _wait >= 15:
				print("CAPTURE_BOAR_QA: Phase 1 - Playing dialogue for 石拳 (boar)...")
				var lines := [
					{"speaker": "石拳", "text": "……把發條最鬆的送來了？還站著？那就接下這一拳——力氣該砸向誰？"}
				]
				_main.call("_play_dialog", lines)
				_phase = 2
				_wait = 0
		2:
			var dbox: Node = _main.get("_dialogue")
			if dbox and is_instance_valid(dbox):
				if dbox.has_method("_finish_typing"):
					dbox.call("_finish_typing")
			if _wait >= 30:
				_save_viewport("proof_dialogue_boar_current.png", "Dialogue - 石拳")
				if dbox and dbox.has_method("_advance"):
					dbox.call("_advance")
				_phase = 3
				_wait = 0
		3:
			if _wait >= 20:
				print("CAPTURE_BOAR_QA: Phase 2 - Starting battle raw for boar...")
				_setup_player_env()
				_main.call("_start_battle_raw", "boar")
				_phase = 4
				_wait = 0
		4:
			if _wait >= 40:
				_save_viewport("proof_battle_open_boar_current.png", "Battle Open - 石拳")
				_phase = 5
				_wait = 0
		5:
			if _wait >= 10:
				print("CAPTURE_BOAR_QA: Complete, quitting.")
				quit(0)
				return true
	return false

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		print("ERROR: get_texture is null")
		return
	var img := tex.get_image()
	if img == null:
		print("ERROR: get_image is null")
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			print("ERROR: save_png failed for ", p, " err=", err)
