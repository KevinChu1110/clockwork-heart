extends SceneTree
## 探索畫面任務「！」徽章多巴胺亮色盤實機截圖產生器

var _frame: int = 0
var _ev: Control = null
var _out_dir: String = ""
var _proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = ProjectSettings.globalize_path("res://").path_join("../proofs/explore_badge")
	DirAccess.make_dir_recursive_absolute(_proof_dir)


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
		print("EXPLORE_VIEW_VILLAGE_SETUP_DONE")

	elif _frame == 40:
		var tex: ViewportTexture = root.get_viewport().get_texture()
		var img: Image = tex.get_image() if tex else null
		if img:
			var p_full := _proof_dir.path_join("proof_explore_quest_badge_fullscreen.png")
			img.save_png(p_full)
			var p_sc := _out_dir.path_join("proof_explore_quest_badge_fullscreen.png")
			img.save_png(p_sc)
			print("SAVED_FULL: ", p_full)

			# 尋找畫面上可見的 badge_panel
			var entity_nodes: Dictionary = _ev.get("_entity_nodes")
			var target_bp: PanelContainer = null
			for eid in ["sign_east", "maisui", "sword"]:
				if entity_nodes.has(eid):
					var node: Control = entity_nodes[eid]
					if node and node.has_meta("badge_panel"):
						var bp: PanelContainer = node.get_meta("badge_panel") as PanelContainer
						if bp and bp.is_visible_in_tree():
							target_bp = bp
							print("FOUND_VISIBLE_BADGE on ", eid)
							break

			if target_bp:
				var gpos := target_bp.global_position
				var gsize := target_bp.size
				print("BADGE_GPOS: ", gpos, " SIZE: ", gsize)
				var pad_x := 30
				var pad_y := 24
				var rx := clampi(int(gpos.x) - pad_x, 0, img.get_width() - 1)
				var ry := clampi(int(gpos.y) - pad_y, 0, img.get_height() - 1)
				var rw := clampi(int(gsize.x) + pad_x * 2, 20, img.get_width() - rx)
				var rh := clampi(int(gsize.y) + pad_y * 2, 20, img.get_height() - ry)
				var crop_rect := Rect2i(rx, ry, rw, rh)
				var cropped := img.get_region(crop_rect)
				var p_crop := _proof_dir.path_join("proof_explore_quest_badge_crop.png")
				cropped.save_png(p_crop)
				print("SAVED_CROP: ", p_crop)

				# 4x 放大圖（使用 NEAREST 縮放）
				var scaled := Image.create(cropped.get_width() * 4, cropped.get_height() * 4, false, cropped.get_format())
				scaled.resize(cropped.get_width() * 4, cropped.get_height() * 4, Image.INTERPOLATE_NEAREST)
				var p_crop4x := _proof_dir.path_join("proof_explore_quest_badge_crop_4x.png")
				# 用 blit 做精確 4x 放大
				for y in cropped.get_height():
					for x in cropped.get_width():
						var col := cropped.get_pixel(x, y)
						for dy in 4:
							for dx in 4:
								scaled.set_pixel(x * 4 + dx, y * 4 + dy, col)
				scaled.save_png(p_crop4x)
				print("SAVED_CROP_4X: ", p_crop4x)
			else:
				print("TARGET_BP_NOT_FOUND")
		else:
			print("NO_IMAGE_CAPTURED")

		print("EXPLORE_BADGE_CAPTURE_OK")
		quit(0)
	return false
