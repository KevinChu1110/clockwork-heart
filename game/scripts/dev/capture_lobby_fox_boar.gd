extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _gs: Node = null

func _initialize() -> void:
	print("=== 開始產生狐族與野豬族大廳換裝待機實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "fox"
		_gs.player_name = "雷克斯"
		_gs.chapter = "c0"
		_gs.paperdoll_slots = {
			"race": "fox",
			"costume": "costume_astral_observer",
			"chassis": "paint_fox_orange",
			"costume_id": "costume_astral_observer",
			"paint_id": "paint_fox_orange",
			"weapon": "wpn_astral_staff"
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
				_save_screenshot("proof_lobby_fox_observer.png")
				print("  ✓ 成功截取 [狐族第一套外裝: 星穹觀測官裝] 大廳待機畫面")
				if _gs:
					_gs.paperdoll_slots = {
						"race": "fox",
						"costume": "costume_astral_cape",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_astral_cape",
						"paint_id": "paint_fox_orange",
						"weapon": "wpn_astral_staff"
					}
				if _lobby:
					_lobby._load_hero_poses()
				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_fox_cape.png")
				print("  ✓ 成功截取 [狐族第二套外裝: 星穹披肩] 大廳待機畫面")
				if _gs:
					_gs.player_race = "boar"
					_gs.player_name = "巴克"
					_gs.paperdoll_slots = {
						"race": "boar",
						"costume": "costume_viking_ironclad",
						"chassis": "paint_molten_crimson",
						"costume_id": "costume_viking_ironclad",
						"paint_id": "paint_molten_crimson",
						"weapon": "wpn_anvil_greathammer"
					}
				if _lobby:
					_lobby._load_hero_poses()
				_step = 3
				_wait_frames = 0
		3:
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_boar_ironclad.png")
				print("  ✓ 成功截取 [野豬第一套外裝: 維京鐵甲] 大廳待機畫面")
				if _gs:
					_gs.paperdoll_slots = {
						"race": "boar",
						"costume": "costume_viking_harness",
						"chassis": "paint_molten_crimson",
						"costume_id": "costume_viking_harness",
						"paint_id": "paint_molten_crimson",
						"weapon": "wpn_anvil_greathammer"
					}
				if _lobby:
					_lobby._load_hero_poses()
				_step = 4
				_wait_frames = 0
		4:
			if _wait_frames >= 30:
				_save_screenshot("proof_lobby_boar_harness.png")
				print("  ✓ 成功截取 [野豬第二套外裝: 維京束帶] 大廳待機畫面")
				print("=== 狐族與野豬族大廳截圖全部完成 ===")
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
