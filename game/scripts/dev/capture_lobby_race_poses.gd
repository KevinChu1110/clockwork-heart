extends SceneTree

var _frame: int = 0
var _lobby: Control = null
var _out_dir: String = ""
var _gs: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.reset_new_game()
		_gs.player_name = "聖獅騎士"
		_gs.player_race = "lion"

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 8:
		# 1. 截取獅子大廳待機
		var img1 := root.get_viewport().get_texture().get_image()
		if img1:
			var p1 := _out_dir.path_join("proof_lobby_lion_idle.png")
			img1.save_png(p1)
			print("SAVED: ", p1)
		# 觸發戳碰：切到攻擊幀
		var avatar := _lobby.get("_hero_avatar") as TextureRect
		var tex_atk: Texture2D = _lobby.get("_tex_attack")
		if avatar and tex_atk:
			avatar.texture = tex_atk
	elif _frame == 12:
		# 2. 截取獅子大廳揮槍姿態
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			var p2 := _out_dir.path_join("proof_lobby_lion_attack.png")
			img2.save_png(p2)
			print("SAVED: ", p2)
		# 切換為狐狸
		if _gs:
			_gs.player_name = "靈狐術士"
			_gs.player_race = "fox"
		if _lobby and _lobby.has_method("_load_hero_poses"):
			_lobby.call("_load_hero_poses")
		if _lobby and _lobby.has_method("refresh_hud"):
			_lobby.call("refresh_hud")
		var avatar := _lobby.get("_hero_avatar") as TextureRect
		var tex_idle: Texture2D = _lobby.get("_tex_idle")
		if avatar and tex_idle:
			avatar.texture = tex_idle
	elif _frame == 18:
		# 3. 截取狐狸大廳待機
		var img3 := root.get_viewport().get_texture().get_image()
		if img3:
			var p3 := _out_dir.path_join("proof_lobby_fox_idle.png")
			img3.save_png(p3)
			print("SAVED: ", p3)
		var avatar := _lobby.get("_hero_avatar") as TextureRect
		var tex_atk: Texture2D = _lobby.get("_tex_attack")
		if avatar and tex_atk:
			avatar.texture = tex_atk
	elif _frame == 24:
		# 4. 截取狐狸大廳法術攻擊姿態
		var img4 := root.get_viewport().get_texture().get_image()
		if img4:
			var p4 := _out_dir.path_join("proof_lobby_fox_attack.png")
			img4.save_png(p4)
			print("SAVED: ", p4)
		print("PROOF_LOBBY_RACE_POSES_OK")
		quit(0)
	return false
