extends SceneTree
## 實機重拍狐族大廳／創角／探索三張截圖腳本 (Xvfb 1280x720)
## 覆蓋：
## 1. 狐族大廳 (Lobby): proof_01_lobby_fox.png
## 2. 狐族創角 (Creation): proof_02_creation_fox.png
## 3. 狐族探索 (Explore): proof_03_explore_fox_walk.png

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dir: String = "/opt/side/bravesoul-game/proofs/fox_fix"
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _demo: Control = null

func _initialize() -> void:
	print("CAPTURE_FOX_PROOFS: Initializing...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("CAPTURE_FOX_PROOFS: load main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main 就緒
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("CAPTURE_FOX_PROOFS: Step 1 -> Lobby Fox")
				_setup_player_fox()
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 大廳：等待 50 frames 渲染完畢
			if _wait >= 50:
				_save_viewport("proof_01_lobby_fox.png", "Lobby Fox")
				print("CAPTURE_FOX_PROOFS: Step 2 -> Creation Fox")
				_setup_creation_fox()
				_step = 2
				_wait = 0

		2:
			# 創角：等待 40 frames 渲染完畢
			if _wait >= 40:
				_save_viewport("proof_02_creation_fox.png", "Creation Fox")
				print("CAPTURE_FOX_PROOFS: Step 3 -> Explore Fox Walk")
				if is_instance_valid(_demo):
					_demo.queue_free()
					_demo = null
				_setup_player_fox()
				# Open explore outdoor hunting_grounds (C1_WILD = 1)
				_main.call("_open_explore", "hunting_grounds", 1)
				_step = 3
				_wait = 0

		3:
			# 探索：等待 60 frames 讓地圖、小地圖與狐族角色完全就緒
			if _wait >= 60:
				_save_viewport("proof_03_explore_fox_walk.png", "Explore Fox Walk")
				_step = 4
				_finish()

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

func _setup_creation_fox() -> void:
	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)
	if _demo.has_method("select_race"):
		_demo.call("select_race", "fox")

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
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		_saved.append(p)
		print("  ✓ [%s] Saved %s (%dx%d)" % [tag, p, img.get_width(), img.get_height()])
	else:
		_errors.append("save_png failed with error %d for %s" % [err, p])

func _finish() -> void:
	print("\n=== CAPTURE_FOX_PROOFS COMPLETED ===")
	print("Saved files (%d):" % _saved.size())
	for s in _saved:
		print("  - ", s)
	if not _errors.is_empty():
		print("Errors (%d):" % _errors.size())
		for e in _errors:
			print("  ! ", e)
		quit(1)
	else:
		print("CAPTURE_FOX_PROOFS_OK")
		quit(0)
