extends SceneTree
## 側案·程式 阿宏 - 探索走路非兔族改走 512 合成實機驗證截圖 (t_1464d6b7)
## 產出三張實機截圖（md5 不可重複）：
## 1. proof_explore_fox_walk_512.png (狐族探索換裝走動 512)
## 2. proof_explore_lion_walk_512.png (獅族探索換裝走動 512)
## 3. proof_compare_idle_vs_walk_512.png (同一角色站著 vs 走動並排 512 解析度一致)

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _gs: Node = null
var _host: Control = null
var _compare_screen: Control = null

func _initialize() -> void:
	print("=== 開始產生非兔族探索走動 512 合成實機截圖 (t_1464d6b7) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.call("reset_new_game", "fox")
		_gs.set("player_name", "靈狐")
		_gs.set("chapter", "c0")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# ── 步驟 1/3：狐族探索走動 (costume_astral_cape 512 合成) ──
			if _wait == 1:
				print(">>> [步驟 1/3] 設定狐族探索換裝走動 (costume_astral_cape)...")
				if _gs:
					_gs.set("player_race", "fox")
					_gs.set("paperdoll_slots", {
						"race": "fox",
						"costume": "costume_astral_cape",
						"chassis": "paint_fox_orange",
						"costume_id": "costume_astral_cape",
						"paint_id": "paint_fox_orange"
					})
				SpriteDB.clear_equipped_cache()
				var Host = load("res://scripts/world/explore_host.gd")
				_host = Host.new()
				root.add_child(_host)
				_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				_host.setup("village")
			if _wait == 15:
				var pl: Node = _host.get_player()
				if pl and pl.has_method("go_to"):
					pl.call("go_to", pl.get("global_position") + Vector2(240, 0))
					print("  已觸發狐族探索走動路徑...")
			if _wait >= 40:
				var pl: CanvasItem = _host.get_player() as CanvasItem
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 200)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 200)
				_save_full_and_crop(
					"proof_explore_fox_walk_512.png",
					"proof_explore_fox_walk_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 200, 200)
				)
				if _host:
					_host.queue_free()
					_host = null
				_step = 1
				_wait = 0
			return false

		1:
			# ── 步驟 2/3：獅族探索走動 (costume_nutcracker_guard 512 合成) ──
			if _wait == 5:
				print(">>> [步驟 2/3] 設定獅族探索換裝走動 (costume_nutcracker_guard)...")
				if _gs:
					_gs.set("player_race", "lion")
					_gs.set("paperdoll_slots", {
						"race": "lion",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_brass_gold",
						"costume_id": "costume_nutcracker_guard",
						"paint_id": "paint_brass_gold"
					})
				SpriteDB.clear_equipped_cache()
				var Host = load("res://scripts/world/explore_host.gd")
				_host = Host.new()
				root.add_child(_host)
				_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
				_host.setup("village")
			if _wait == 20:
				var pl: Node = _host.get_player()
				if pl and pl.has_method("go_to"):
					pl.call("go_to", pl.get("global_position") + Vector2(240, 0))
					print("  已觸發獅族探索走動路徑...")
			if _wait >= 45:
				var pl: CanvasItem = _host.get_player() as CanvasItem
				var crop_pos := Vector2i(540, 260)
				if pl:
					var screen_pos: Vector2 = pl.get_global_transform_with_canvas().origin
					crop_pos = Vector2i(int(screen_pos.x - 100), int(screen_pos.y - 120))
					crop_pos.x = clampi(crop_pos.x, 0, 1280 - 200)
					crop_pos.y = clampi(crop_pos.y, 0, 720 - 200)
				_save_full_and_crop(
					"proof_explore_lion_walk_512.png",
					"proof_explore_lion_walk_crop.png",
					Rect2i(crop_pos.x, crop_pos.y, 200, 200)
				)
				if _host:
					_host.queue_free()
					_host = null
				_step = 2
				_wait = 0
			return false

		2:
			# ── 步驟 3/3：同一角色站著 vs 走動並排 (512 解析度一致) ──
			if _wait == 5:
				print(">>> [步驟 3/3] 構建同一角色站著 vs 走動並排展示畫面 (512 解析度一致)...")
				SpriteDB.clear_equipped_cache()
				var fox_slots := {
					"costume": "costume_astral_cape",
					"chassis": "paint_fox_orange"
				}
				var idle_tex: Texture2D = SpriteDB.player_equipped_idle("fox", fox_slots)
				var walk_tex: Texture2D = SpriteDB.player_equipped_walk(0, "fox", fox_slots)

				_compare_screen = Control.new()
				_compare_screen.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_compare_screen)

				# 背景
				var bg := ColorRect.new()
				bg.set_anchors_preset(Control.PRESET_FULL_RECT)
				bg.color = Color("#FFFDF8") # 陽光童話·奶油米白底
				_compare_screen.add_child(bg)

				# 頂部標題
				var title_lbl := Label.new()
				title_lbl.text = "發條之心 512 高清合成對照：站立待機 (Idle) vs 探索走動 (Walk)"
				title_lbl.set_anchors_preset(Control.PRESET_TOP_WIDE)
				title_lbl.offset_top = 28
				title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
				title_lbl.add_theme_font_size_override("font_size", 24)
				title_lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
				_compare_screen.add_child(title_lbl)

				# 左側卡片：站立待機
				var left_box := PanelContainer.new()
				left_box.position = Vector2(160, 90)
				left_box.size = Vector2(440, 560)
				left_box.add_theme_stylebox_override("panel", _create_card_style())
				_compare_screen.add_child(left_box)

				var left_vbox := VBoxContainer.new()
				left_box.add_child(left_vbox)

				var left_hdr := Label.new()
				left_hdr.text = "站立待機 (Idle 512x512)"
				left_hdr.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
				left_hdr.add_theme_font_size_override("font_size", 20)
				left_hdr.add_theme_color_override("font_color", Color("#1F1A3A"))
				left_vbox.add_child(left_hdr)

				var left_rect := TextureRect.new()
				left_rect.custom_minimum_size = Vector2(400, 480)
				left_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				left_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
				left_rect.texture = idle_tex
				left_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				left_vbox.add_child(left_rect)

				# 右側卡片：探索走動
				var right_box := PanelContainer.new()
				right_box.position = Vector2(680, 90)
				right_box.size = Vector2(440, 560)
				right_box.add_theme_stylebox_override("panel", _create_card_style())
				_compare_screen.add_child(right_box)

				var right_vbox := VBoxContainer.new()
				right_box.add_child(right_vbox)

				var right_hdr := Label.new()
				right_hdr.text = "探索走動 (Walk Frame 0 512x512)"
				right_hdr.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
				right_hdr.add_theme_font_size_override("font_size", 20)
				right_hdr.add_theme_color_override("font_color", Color("#1F1A3A"))
				right_vbox.add_child(right_hdr)

				var right_rect := TextureRect.new()
				right_rect.custom_minimum_size = Vector2(400, 480)
				right_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				right_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
				right_rect.texture = walk_tex
				right_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				right_vbox.add_child(right_rect)

			if _wait >= 25:
				_save_full_and_crop(
					"proof_compare_idle_vs_walk_512.png",
					"proof_compare_idle_vs_walk_crop.png",
					Rect2i(800, 260, 200, 200)
				)
				if _compare_screen:
					_compare_screen.queue_free()
					_compare_screen = null
				print("=== 3 張實機截圖擷取完成 ===")
				quit(0)
				return true

	return false

func _save_full_and_crop(full_name: String, crop_name: String, crop_rect: Rect2i) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var full_p := _out_dir.path_join(full_name)
	img.save_png(full_p)
	print("  ✓ 儲存實機全景截圖: %s (1280x720)" % full_p)

	if not crop_name.is_empty():
		var crop_img := img.get_region(crop_rect)
		var crop_p := _out_dir.path_join(crop_name)
		crop_img.save_png(crop_p)
		print("  ✓ 儲存特寫裁切截圖: %s (%dx%d)" % [crop_p, crop_rect.size.x, crop_rect.size.y])

func _create_card_style() -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color("#FFFFFF")
	sb.border_color = Color("#1F1A3A")
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5 # 果凍厚底
	sb.set_corner_radius_all(20) # 圓角 18~24px
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 16
	sb.content_margin_bottom = 16
	return sb
