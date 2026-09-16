extends SceneTree
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_bear_wardrobe_new_costume.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生玄軸熊衣櫥換裝彈窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe_bear")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "bear"
		gs.player_name = "玄軸熊"
		gs.paperdoll_slots = {
			"race": "bear",
			"costume": "costume_berserker_cuirass",
			"chassis": "paint_iron_quarry",
			"costume_id": "costume_berserker_cuirass",
			"paint_id": "paint_iron_quarry",
			"weapon": "wpn_eccentric_gyro_sledge"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)

	_step = 1
	_wait_frames = 0

func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			if _wait_frames == 10:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
					if _wardrobe != null:
						# Select Berserker Cuirass & Quarry Grey
						_wardrobe.set("costume_index", 1)
						_wardrobe.set("chassis_index", 1)
						if _wardrobe.has_method("_update_card_selection_states"):
							_wardrobe.call("_update_card_selection_states")
						if _wardrobe.has_method("_update_ui_texts"):
							_wardrobe.call("_update_ui_texts")
						if _wardrobe.has_method("_update_preview"):
							_wardrobe.call("_update_preview")
						print("  [Wardrobe] 已開啟衣櫥並選中【狂戰破陣機關戰鎧】與【重裝礦山玄鐵灰】")
			if _wait_frames >= 40:
				var fn := "proof_wardrobe_bear_berserker.png"
				_save_screenshot(fn)
				print("  ✓ [1/2] 玄軸熊穿戴【狂戰破陣機關戰鎧】衣櫥彈窗截圖完成 -> %s" % fn)

				# 切換至【玄軸工坊重裝工作吊帶甲】對照
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.set("costume_index", 0)
					_wardrobe.set("chassis_index", 0)
					if _wardrobe.has_method("_update_card_selection_states"):
						_wardrobe.call("_update_card_selection_states")
					if _wardrobe.has_method("_update_ui_texts"):
						_wardrobe.call("_update_ui_texts")
					if _wardrobe.has_method("_update_preview"):
						_wardrobe.call("_update_preview")
					print("  [Wardrobe] 已切換回【玄軸工坊重裝工作吊帶甲】與【原廠玄軸琥珀棕】")
				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 30:
				var fn2 := "proof_wardrobe_bear_overalls.png"
				_save_screenshot(fn2)
				print("  ✓ [2/2] 玄軸熊穿戴【玄軸工坊重裝工作吊帶甲】衣櫥彈窗截圖完成 -> %s" % fn2)
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.call("close")
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_finish()
				return true

	return false

func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		return
	var path := _out_dir.path_join(filename)
	var err := img.save_png(path)
	if err == OK:
		print("    [Screenshot] 已存檔至: %s" % path)
	else:
		push_error("存檔失敗: %s, code: %d" % [path, err])

func _finish() -> void:
	print("=== 玄軸熊衣櫥換裝彈窗截圖全數完成 ===")
	quit(0)
