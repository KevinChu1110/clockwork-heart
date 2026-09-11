extends SceneTree
## 聚魂殿首屏保底進度條與戰魂圖鑑截圖
## godot --path game --script res://scripts/dev/capture_soul_simplify.gd

var _step := 0
var _wait := 0
var _main: Node = null
var _out := ""
var _saved: PackedStringArray = PackedStringArray()


func _initialize() -> void:
	_out = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out)
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 40:
				return false
			_main = current_scene
			if _main == null:
				print("CAPTURE fail no main")
				quit(1)
				return true
			var gs: Node = root.get_node_or_null("GameState")
			var ss: Node = root.get_node_or_null("SoulSystem")
			gs.call("reset_new_game")
			gs.set("gold", 1500)
			gs.set("stardust", 12)
			gs.set("weapon_tier", 2)
			gs.call("set_flag", "soul.piety", 60)
			gs.call("set_flag", "soul.shards", 4)
			ss.call("ensure_slots")
			ss.call("grant_starter_soul")
			_main.call("_go_soul_panel")
			_step = 1
			_wait = 0
		1:
			if _wait < 30:
				return false
			_shot("proof_soul_pity.png")
			_shot("soul_panel_pity.png")
			_main.call("_go_astrolabe_panel")
			_step = 2
			_wait = 0
		2:
			if _wait < 30:
				return false
			_shot("soul_codex.png")
			_scroll_panel_down()
			_step = 3
			_wait = 0
		3:
			if _wait < 20:
				return false
			_shot("soul_codex_details.png")
			print("CAPTURE done ", _saved)
			quit(0)
			return true
	return false


func _scroll_panel_down() -> void:
	if _main == null:
		return
	var rtls := _main.find_children("", "RichTextLabel", true, false)
	for rtl in rtls:
		if rtl is RichTextLabel:
			var vsb: VScrollBar = rtl.get_v_scroll_bar()
			if vsb:
				vsb.value = vsb.max_value


func _shot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img == null:
		print("CAPTURE no image ", filename)
		return
	var path := _out.path_join(filename)
	var err := img.save_png(path)
	print("CAPTURE ", path, " err=", err, " ", img.get_width(), "x", img.get_height())
	var base := ProjectSettings.globalize_path("res://")
	var p_web := base.path_join("../web/media/shots").path_join(filename)
	DirAccess.make_dir_recursive_absolute(base.path_join("../web/media/shots"))
	img.save_png(p_web)
	print("CAPTURE web ", p_web)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		DirAccess.make_dir_recursive_absolute(ws)
		var ws_err := img.save_png(ws.path_join(filename))
		print("CAPTURE workspace ", ws.path_join(filename), " err=", ws_err)
	if err == OK:
		_saved.append(path)
