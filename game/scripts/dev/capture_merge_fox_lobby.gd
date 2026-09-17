extends SceneTree
## 實機重拍狐族大廳截圖腳本 (Xvfb 1280x720)
## 3. 狐族大廳 (Lobby): proof_fox_lobby_512.png

var _out_dir: String = ""
var _main: Node = null
var _step: int = 0
var _wait: int = 0

func _initialize() -> void:
	print("CAPTURE_FOX_LOBBY: Initializing...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/merge_battle_fox_512")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("CAPTURE_FOX_LOBBY: load main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					print("ERROR: main scene is null")
					quit(1)
					return false
				print("CAPTURE_FOX_LOBBY: Setup Fox and go to mobile lobby")
				_setup_player_fox()
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0
		1:
			if _wait >= 60:
				_save_viewport("proof_fox_lobby_512.png")
				print("CAPTURE_FOX_LOBBY_OK")
				quit(0)
	return false

func _setup_player_fox() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		return
	gs.call("reset_new_game", "fox")
	gs.set("player_name", "靈尾狐")
	gs.set("player_race", "fox")
	gs.set("max_hp", 999)
	gs.set("energy", 15)
	gs.set("gold", 8888)
	gs.set("stardust", 30)
	if gs.has_method("set_flag"):
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
	gs.set("paperdoll_slots", {
		"race": "fox",
		"costume": "costume_astral_cape",
		"costume_id": "costume_astral_cape",
		"chassis": "paint_fox_orange",
		"chassis_id": "paint_fox_orange",
		"head_unit": "ear_fox_radar",
		"head_unit_id": "ear_fox_radar",
		"weapon": "wpn_astral_staff",
		"weapon_id": "wpn_astral_staff"
	})
	var tut: Node = root.get_node_or_null("TutorialSystem")
	if tut and tut.has_method("mark"):
		for k in ["boot", "explore", "battle_auto", "battle_parry", "battle_fog", "forge", "paths", "soul", "fort", "flag_hint", "ng"]:
			tut.call("mark", k)

func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		print("ERROR: get_texture is null")
		return
	var img := tex.get_image()
	if img == null:
		print("ERROR: get_image is null")
		return
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  ✓ Saved %s (%dx%d)" % [p, img.get_width(), img.get_height()])
	else:
		print("ERROR: save_png failed error %d" % err)
