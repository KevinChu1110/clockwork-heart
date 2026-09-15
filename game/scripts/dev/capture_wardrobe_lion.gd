extends SceneTree
## 截取獅族 (lion) 與其他族群衣櫥彈窗卡片圖示實機截圖
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_lion.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null

var _test_races := ["lion", "rabbit", "macaque", "fox", "boar"]
var _current_race_idx := 0

func _initialize() -> void:
	print("=== 開始產生衣櫥彈窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)

	_setup_race(_test_races[_current_race_idx])
	_step = 1
	_wait_frames = 0

func _setup_race(race_id: String) -> void:
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = race_id
		gs.player_name = "英雄"
		if race_id == "lion":
			gs.paperdoll_slots = {
				"race": "lion",
				"costume": "costume_steam_artisan",
				"chassis": "paint_midnight_navy",
				"costume_id": "costume_steam_artisan",
				"paint_id": "paint_midnight_navy"
			}
		else:
			gs.paperdoll_slots = {
				"race": race_id
			}
	print("Setup race: ", race_id)

func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 打開衣櫥
			if _wait_frames == 10:
				if _lobby != null:
					_lobby.open_wardrobe()
					# 找到產生的 WardrobeDialog
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
			if _wait_frames >= 35:
				var cur_race = _test_races[_current_race_idx]
				var filename = "proof_wardrobe_%s.png" % cur_race
				_save_screenshot(filename)
				print("  ✓ 成功截取 [%s] 衣櫥彈窗 -> %s" % [cur_race, filename])
				
				# 關閉目前的 wardrobe
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				
				_current_race_idx += 1
				if _current_race_idx < _test_races.size():
					_setup_race(_test_races[_current_race_idx])
					_wait_frames = 0
					_step = 1
				else:
					print("=== 所有種族衣櫥截圖完成 ===")
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
