extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始產生猴族大廳換裝待機實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "macaque"
		_gs.player_name = "悟空"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": "macaque",
			"costume": "costume_dawn_monk_tunic",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_dawn_monk_tunic",
			"paint_id": "paint_ivory_stock",
			"weapon": "wpn_spring_claws"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_step = 1
	_wait_frames = 0


func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_macaque_dawn_monk.png")
				print("  ✓ 成功截取 [第一套外裝: 破曉行僧袍] 猴族大廳待機畫面")
				if _gs:
					_gs.paperdoll_slots = {
						"race": "macaque",
						"costume": "costume_zen_striker",
						"chassis": "paint_bamboo_bronze",
						"costume_id": "costume_zen_striker",
						"paint_id": "paint_bamboo_bronze",
						"weapon": "wpn_spring_claws"
					}
				if _lobby:
					_lobby._load_hero_poses()
				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_macaque_zen_striker.png")
				print("  ✓ 成功截取 [第二套外裝: 天元演武者] 猴族大廳待機畫面")
				print("=== 猴族大廳截圖全部完成 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> %s" % file_path)
	else:
		push_error("截圖失敗: %s" % file_path)
