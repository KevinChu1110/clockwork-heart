extends SceneTree
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_wardrobe_shared_costume.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _crops_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null
var _explore_view: Control = null

func _initialize() -> void:
	print("=== 開始產生瓷韻熊貓與碧簧蛙第二套共用外裝實機驗收截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe-shared-costume")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	_step = 1
	_wait_frames = 0
	_setup_panda_lobby()

func _setup_panda_lobby() -> void:
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "panda")
		gs.player_race = "panda"
		gs.player_name = "瓷韻熊貓"
		gs.paperdoll_slots = {
			"race": "panda",
			"costume": "costume_dawn_monk_tunic",
			"costume_id": "costume_dawn_monk_tunic",
			"chassis": "paint_panda_porcelain",
			"paint_id": "paint_panda_porcelain",
			"weapon": "wpn_panda_taiji_cestus",
			"head_unit": "head_panda_brass_socket_ears",
			"optic_core": "core_obsidian_amber_quartz",
			"winding_key": "key_panda_taiji_ruyi_brass",
			"back_curio": "curio_panda_floating_taiji_box"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)

func _setup_frog_lobby() -> void:
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "frog")
		gs.player_race = "frog"
		gs.player_name = "碧簧蛙"
		gs.paperdoll_slots = {
			"race": "frog",
			"costume": "costume_astral_cape",
			"costume_id": "costume_astral_cape",
			"chassis": "paint_frog_emerald",
			"paint_id": "paint_frog_emerald",
			"weapon": "wpn_lotus_cog_dart",
			"head_unit": "head_spring_frog_stock",
			"optic_core": "core_azure_aperture",
			"winding_key": "key_twin_wing_concentric",
			"back_curio": "curio_lotus_leaf_parasol"
		}

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_lobby._ready()
	_lobby._switch_tab(MobileLobby.Tab.CHARACTER)

func _process(_delta: float) -> bool:
	_wait_frames += 1

	match _step:
		1:
			# 步驟 1: 熊貓衣櫥
			if _wait_frames == 10:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
					if _wardrobe != null:
						if _wardrobe.has_method("set_race_filter"):
							_wardrobe.call("set_race_filter", "panda")
						
						var displayed_c: Array = _wardrobe.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_dawn_monk_tunic":
								target_c_idx = idx
								break
						
						if target_c_idx >= 0:
							_wardrobe.set("costume_index", target_c_idx)
							_wardrobe.set("selected_costume_id", "costume_dawn_monk_tunic")
						
						if _wardrobe.has_method("_update_card_selection_states"):
							_wardrobe.call("_update_card_selection_states")
						if _wardrobe.has_method("_update_ui_texts"):
							_wardrobe.call("_update_ui_texts")
						if _wardrobe.has_method("_update_preview"):
							_wardrobe.call("_update_preview")
						print("  [Wardrobe] 已開啟衣櫥並選中熊貓第二套【晨曦武道短裋】")

			elif _wait_frames == 25:
				if _wardrobe != null:
					var filter_scroll: ScrollContainer = _wardrobe.find_child("FilterScroll", true, false)
					if filter_scroll != null:
						filter_scroll.scroll_horizontal = 9999

			elif _wait_frames >= 40:
				var fn := _out_dir.path_join("proof_01_wardrobe_panda_dawn_tunic.png")
				_save_screenshot(fn)
				print("  ✓ [1/4] 熊貓穿戴第二套【晨曦武道短裋】衣櫥彈窗截圖完成 -> %s" % fn)

				# 關閉並清理 lobby
				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.queue_free()
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				# 進入步驟 2: 熊貓探索待機
				_step = 2
				_wait_frames = 0
				var ExploreViewScn = load("res://scripts/world/explore_view.gd")
				if ExploreViewScn:
					var ev = ExploreViewScn.new()
					ev.set_anchors_preset(Control.PRESET_FULL_RECT)
					root.add_child(ev)
					ev.setup("village")
					_explore_view = ev

		2:
			# 步驟 2: 熊貓探索待機截圖
			if _wait_frames >= 40:
				var fn := _out_dir.path_join("proof_02_explore_panda_dawn_tunic.png")
				_save_screenshot(fn)
				print("  ✓ [2/4] 熊貓穿戴第二套【晨曦武道短裋】探索待機截圖完成 -> %s" % fn)

				if _explore_view != null and is_instance_valid(_explore_view):
					_explore_view.queue_free()
					_explore_view = null

				# 進入步驟 3: 蛙衣櫥
				_step = 3
				_wait_frames = 0
				_setup_frog_lobby()

		3:
			# 步驟 3: 蛙衣櫥
			if _wait_frames == 10:
				if _lobby != null:
					_lobby.open_wardrobe()
					_wardrobe = _lobby.find_child("WardrobeDialog", true, false)
					if _wardrobe != null:
						if _wardrobe.has_method("set_race_filter"):
							_wardrobe.call("set_race_filter", "frog")
						
						var displayed_c: Array = _wardrobe.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_astral_cape":
								target_c_idx = idx
								break
						
						if target_c_idx >= 0:
							_wardrobe.set("costume_index", target_c_idx)
							_wardrobe.set("selected_costume_id", "costume_astral_cape")
						
						if _wardrobe.has_method("_update_card_selection_states"):
							_wardrobe.call("_update_card_selection_states")
						if _wardrobe.has_method("_update_ui_texts"):
							_wardrobe.call("_update_ui_texts")
						if _wardrobe.has_method("_update_preview"):
							_wardrobe.call("_update_preview")
						print("  [Wardrobe] 已開啟衣櫥並選中蛙第二套【星紋斗篷】")

			elif _wait_frames == 25:
				if _wardrobe != null:
					var filter_scroll: ScrollContainer = _wardrobe.find_child("FilterScroll", true, false)
					if filter_scroll != null:
						filter_scroll.scroll_horizontal = 9999

			elif _wait_frames >= 40:
				var fn := _out_dir.path_join("proof_03_wardrobe_frog_astral_cape.png")
				_save_screenshot(fn)
				print("  ✓ [3/4] 蛙穿戴第二套【星紋斗篷】衣櫥彈窗截圖完成 -> %s" % fn)

				if _wardrobe != null and is_instance_valid(_wardrobe):
					_wardrobe.queue_free()
					_wardrobe = null
				if _lobby != null and is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null

				# 進入步驟 4: 蛙探索待機
				_step = 4
				_wait_frames = 0
				var ExploreViewScn = load("res://scripts/world/explore_view.gd")
				if ExploreViewScn:
					var ev = ExploreViewScn.new()
					ev.set_anchors_preset(Control.PRESET_FULL_RECT)
					root.add_child(ev)
					ev.setup("village")
					_explore_view = ev

		4:
			# 步驟 4: 蛙探索待機截圖
			if _wait_frames >= 40:
				var fn := _out_dir.path_join("proof_04_explore_frog_astral_cape.png")
				_save_screenshot(fn)
				print("  ✓ [4/4] 蛙穿戴第二套【星紋斗篷】探索待機截圖完成 -> %s" % fn)

				if _explore_view != null and is_instance_valid(_explore_view):
					_explore_view.queue_free()
					_explore_view = null

				_step = 5
				_generate_crops()
				print("=== 瓷韻熊貓與碧簧蛙第二套外裝實機截圖完成 ===")
				quit(0)

	return false

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    Successfully wrote: %s" % abs_path)

func _generate_crops() -> void:
	# 熊貓衣櫥卡片網格與 512 預覽特寫
	var p_wd := _out_dir.path_join("proof_01_wardrobe_panda_dawn_tunic.png")
	if FileAccess.file_exists(p_wd):
		var img := Image.load_from_file(p_wd)
		if img and not img.is_empty():
			var crop_cards := img.get_region(Rect2i(540, 130, 470, 470))
			crop_cards.save_png(_crops_dir.path_join("crop_wardrobe_panda_cards.png"))
			var crop_prev := img.get_region(Rect2i(270, 140, 260, 380))
			crop_prev.save_png(_crops_dir.path_join("crop_wardrobe_panda_preview.png"))

	# 熊貓探索待機角色特寫
	var p_ex := _out_dir.path_join("proof_02_explore_panda_dawn_tunic.png")
	if FileAccess.file_exists(p_ex):
		var img := Image.load_from_file(p_ex)
		if img and not img.is_empty():
			var crop_char := img.get_region(Rect2i(540, 260, 200, 260))
			crop_char.save_png(_crops_dir.path_join("crop_explore_panda_character.png"))

	# 蛙衣櫥卡片網格與 512 預覽特寫
	var f_wd := _out_dir.path_join("proof_03_wardrobe_frog_astral_cape.png")
	if FileAccess.file_exists(f_wd):
		var img := Image.load_from_file(f_wd)
		if img and not img.is_empty():
			var crop_cards := img.get_region(Rect2i(540, 130, 470, 470))
			crop_cards.save_png(_crops_dir.path_join("crop_wardrobe_frog_cards.png"))
			var crop_prev := img.get_region(Rect2i(270, 140, 260, 380))
			crop_prev.save_png(_crops_dir.path_join("crop_wardrobe_frog_preview.png"))

	# 蛙探索待機角色特寫
	var f_ex := _out_dir.path_join("proof_04_explore_frog_astral_cape.png")
	if FileAccess.file_exists(f_ex):
		var img := Image.load_from_file(f_ex)
		if img and not img.is_empty():
			var crop_char := img.get_region(Rect2i(540, 260, 200, 260))
			crop_char.save_png(_crops_dir.path_join("crop_explore_frog_character.png"))
