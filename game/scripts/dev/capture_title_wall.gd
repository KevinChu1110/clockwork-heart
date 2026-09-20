extends SceneTree
## 截取成就稱號牆實機截圖
## 1. proof_title_wall_locked.png (預設未解鎖為主)
## 2. proof_title_wall_unlocked.png (多個稱號已解鎖高亮 + 金黃提示條 + 堡壘鈕)

var _wait := 0
var _step := 0
var _main: Node = null
var _gs: Node = null
var _tc: Node = null
var _out_dir := "res://proofs/title_wall"


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var dir := DirAccess.open("res://")
	if dir and not dir.dir_exists("proofs/title_wall"):
		dir.make_dir_recursive("proofs/title_wall")
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			_gs = root.get_node_or_null("GameState")
			_tc = root.get_node_or_null("TitleCatalog")
			if _main == null or _gs == null or _tc == null:
				push_error("初始化節點失敗")
				quit(1)
				return true
			_gs.call("reset_new_game")
			_main.call("_go_title")
			_step = 1
			_wait = 0
		1:
			if _wait < 8:
				return false
			_main.call("_go_title_wall")
			_step = 2
			_wait = 0
		2:
			if _wait < 20:
				return false
			_capture("proof_title_wall_locked.png")
			# 設置解鎖條件
			_gs.call("set_flag", "c1_perfect_parry_once", true)
			_gs.call("set_flag", "boss.white_fog_cleared", true)
			_gs.call("set_flag", "game_cleared", true)
			_gs.call("set_flag", "c1_sprout_done", true)
			_gs.call("set_flag", "boss.scar_lord_cleared", true)
			_step = 3
			_wait = 0
		3:
			if _wait < 8:
				return false
			_main.call("_go_title_wall")
			_step = 4
			_wait = 0
		4:
			if _wait < 20:
				return false
			_capture("proof_title_wall_unlocked.png")
			print("CAPTURE_ALL_OK")
			quit(0)
			return true
	return false


func _capture(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		push_error("無法取得 ViewportTexture: " + filename)
		return
	var save_path := "proofs/title_wall/" + filename
	var abs_path := ProjectSettings.globalize_path(save_path)
	var err := img.save_png(abs_path)
	print("SAVED: ", abs_path, " err=", err, " size=", img.get_width(), "x", img.get_height())
