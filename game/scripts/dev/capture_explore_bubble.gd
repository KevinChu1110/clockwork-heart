extends SceneTree
## 探索畫面對話泡泡實機截圖產生器

var _frame: int = 0
var _ev: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 2:
		var ExploreViewScn = load("res://scripts/world/explore_view.gd")
		if ExploreViewScn == null:
			push_error("無法載入 explore_view.gd")
			quit(1)
			return true

		_ev = ExploreViewScn.new()
		_ev.set_anchors_preset(Control.PRESET_FULL_RECT)
		root.add_child(_ev)
		_ev.setup("village")
		print("EXPLORE_VIEW_SETUP_DONE")

	elif _frame == 10:
		if _ev:
			# 觸發玩家泡泡與實體泡泡
			_ev.show_player_bubble("發條運轉正常！出發探索！", 10.0)

	elif _frame == 45:
		var tex: ViewportTexture = root.get_viewport().get_texture()
		var img: Image = tex.get_image() if tex else null
		if img:
			var p_full := _out_dir.path_join("proof_explore_bubble_fullscreen.png")
			img.save_png(p_full)
			print("SAVED_FULL: ", p_full)

			# 截取中央玩家泡泡區域
			# 玩家在中央偏下位置，泡泡通常在中央
			var rx := clampi(int(img.get_width() * 0.35), 0, img.get_width() - 1)
			var ry := clampi(int(img.get_height() * 0.4), 0, img.get_height() - 1)
			var rw := clampi(int(img.get_width() * 0.3), 100, img.get_width() - rx)
			var rh := clampi(int(img.get_height() * 0.3), 100, img.get_height() - ry)
			var crop_rect := Rect2i(rx, ry, rw, rh)
			var crop_img := img.get_region(crop_rect)
			var p_crop := _out_dir.path_join("proof_explore_bubble_crop.png")
			crop_img.save_png(p_crop)
			print("SAVED_CROP: ", p_crop)

		print("EXPLORE_BUBBLE_CAPTURE_OK")
		quit(0)
		return true

	return false
