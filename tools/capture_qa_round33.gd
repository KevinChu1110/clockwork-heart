extends SceneTree
## QA Round 33 探索性驗證實機截圖腳本
## 涵蓋：
## 1. 創角首發頁抽查（五卡一屏，確認沒被擴充改壞）
## 2. 創角擴充分頁整頁（選中蛙或貓，舞台角色完好無空白人偶）
## 3. 創角擴充頁向右滾動至最末端（確認無翠角鹿空卡，結束於瓷韻熊貓）
## 4. 衣櫥種族列滾動至末端（確認有象、蛙、貓，無鹿篩選 chip）
## 5. 熊貓換第二套外裝前（衣櫥選中第一套【禪道學徒生漆長袍】）
## 6. 熊貓換第二套外裝後（衣櫥選中第二套【晨曦武道短裋】）
## 7. 蛙換第二套外裝前（衣櫥選中第一套【碧箐巡林客工裝】）
## 8. 蛙換第二套外裝後（衣櫥選中第二套【星紋斗篷】）
## 9. 蛙衣櫥標籤 en（大廳連動下，Dock、大廳、衣櫥標籤同步為 en，0-QA25）
## 10. 蛙衣櫥標籤 ja（大廳連動下，Dock、大廳、衣櫥標籤同步為 ja，0-QA25）

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round33"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round33/crops"

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")
const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	if _loc_node:
		_loc_node.call("set_locale", "zh_TW")

	print("=== 開始執行 QA Round 33 探索性實機截圖流程 ===")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: 創角首發頁抽查（五卡一屏）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo = DemoScene.instantiate()
				demo.set("creation_mode", true)
				root.add_child(demo)
				demo.call("switch_tab", "launch")
				demo.call("select_race", "rabbit")
				demo.call("reset_to_default")
				_current_node = demo
			elif _wait >= 30:
				var path := "%s/proof_01_creation_launch.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/10] 創角首發頁抽查: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: 創角擴充分頁整頁
			if _wait == 1:
				if _current_node:
					_current_node.call("switch_tab", "expansion")
					_current_node.call("select_race", "frog")
					_current_node.call("reset_to_default")
			elif _wait >= 30:
				var path := "%s/proof_02_creation_expansion.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/10] 創角擴充分頁整頁: %s" % path)
				_step = 3
				_wait = 0

		3:
			# 步驟 3: 創角擴充頁向右滾動至最末端（確認無鹿空卡）
			if _wait == 1:
				if _current_node:
					_current_node.call("select_race", "panda")
					_current_node.call("reset_to_default")
					var scroll := _current_node.get_node_or_null("TopRaceBar") as ScrollContainer
					if scroll:
						scroll.scroll_horizontal = 9999
			elif _wait >= 30:
				var path := "%s/proof_03_creation_expansion_scroll_end.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/10] 創角擴充頁滾動至最末端: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 4
				_wait = 0

		4:
			# 步驟 4: 衣櫥種族列滾動至末端（確認無鹿晶片，有象/蛙/貓）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var wd := WardrobeDialog.new()
				root.add_child(wd)
				wd.set_race_filter("all")
				_current_node = wd
			elif _wait == 15:
				if _current_node:
					var filter_scroll: ScrollContainer = null
					for node in _current_node.find_children("*", "ScrollContainer", true, false):
						if "Filter" in node.name:
							filter_scroll = node as ScrollContainer
							break
					if filter_scroll:
						filter_scroll.scroll_horizontal = 9999
			elif _wait >= 35:
				var path := "%s/proof_04_wardrobe_filter_chips_end.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/10] 衣櫥種族篩選列滾動至末端: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 5
				_wait = 0

		5:
			# 步驟 5: 熊貓換第二套外裝前（衣櫥選中第一套【禪道學徒生漆長袍】）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "panda")
					_gs.set("player_race", "panda")
					_gs.set("player_name", "瓷韻熊貓")
					_gs.set("paperdoll_slots", {
						"race": "panda",
						"costume": "costume_panda_zen_apprentice_robe",
						"costume_id": "costume_panda_zen_apprentice_robe",
						"chassis": "paint_panda_porcelain",
						"paint_id": "paint_panda_porcelain",
						"weapon": "wpn_panda_taiji_cestus",
						"head_unit": "head_panda_brass_socket_ears",
						"optic_core": "core_obsidian_amber_quartz",
						"winding_key": "key_panda_taiji_ruyi_brass",
						"back_curio": "curio_panda_floating_taiji_box"
					})
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				lobby._ready()
				lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_current_node = lobby
			elif _wait == 10:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd:
						if wd.has_method("set_race_filter"):
							wd.call("set_race_filter", "panda")
						var displayed_c: Array = wd.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_panda_zen_apprentice_robe":
								target_c_idx = idx
								break
						if target_c_idx >= 0:
							wd.set("costume_index", target_c_idx)
							wd.set("selected_costume_id", "costume_panda_zen_apprentice_robe")
							if wd.has_method("_update_card_selection_states"):
								wd.call("_update_card_selection_states")
							if wd.has_method("_update_ui_texts"):
								wd.call("_update_ui_texts")
							if wd.has_method("_update_preview"):
								wd.call("_update_preview")
			elif _wait >= 40:
				var path := "%s/proof_05_wardrobe_panda_costume_default.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/10] 熊貓換第二套外裝前（第一套【禪道學徒生漆長袍】）: %s" % path)
				_step = 6
				_wait = 0

		6:
			# 步驟 6: 熊貓換第二套外裝後（第二套【晨曦武道短裋】）
			if _wait == 1:
				if _current_node:
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd:
						var displayed_c: Array = wd.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_dawn_monk_tunic":
								target_c_idx = idx
								break
						if target_c_idx >= 0:
							wd.set("costume_index", target_c_idx)
							wd.set("selected_costume_id", "costume_dawn_monk_tunic")
							if wd.has_method("_update_card_selection_states"):
								wd.call("_update_card_selection_states")
							if wd.has_method("_update_ui_texts"):
								wd.call("_update_ui_texts")
							if wd.has_method("_update_preview"):
								wd.call("_update_preview")
			elif _wait >= 40:
				var path := "%s/proof_06_wardrobe_panda_costume_second.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [6/10] 熊貓換第二套外裝後（第二套【晨曦武道短裋】）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 7
				_wait = 0

		7:
			# 步驟 7: 蛙換第二套外裝前（第一套【碧箐巡林客工裝】）
			if _wait == 1:
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "碧箸蛙")
					_gs.set("paperdoll_slots", {
						"race": "frog",
						"costume": "costume_spring_forest_courier",
						"costume_id": "costume_spring_forest_courier",
						"chassis": "paint_frog_emerald",
						"paint_id": "paint_frog_emerald",
						"weapon": "wpn_lotus_cog_dart",
						"head_unit": "head_spring_frog_stock",
						"optic_core": "core_azure_aperture",
						"winding_key": "key_twin_wing_concentric",
						"back_curio": "curio_lotus_leaf_parasol"
					})
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				lobby._ready()
				lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_current_node = lobby
			elif _wait == 10:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd:
						if wd.has_method("set_race_filter"):
							wd.call("set_race_filter", "frog")
						var displayed_c: Array = wd.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_spring_forest_courier":
								target_c_idx = idx
								break
						if target_c_idx >= 0:
							wd.set("costume_index", target_c_idx)
							wd.set("selected_costume_id", "costume_spring_forest_courier")
							if wd.has_method("_update_card_selection_states"):
								wd.call("_update_card_selection_states")
							if wd.has_method("_update_ui_texts"):
								wd.call("_update_ui_texts")
							if wd.has_method("_update_preview"):
								wd.call("_update_preview")
			elif _wait >= 40:
				var path := "%s/proof_07_wardrobe_frog_costume_default.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [7/10] 蛙換第二套外裝前（第一套【碧箐巡林客工裝】）: %s" % path)
				_step = 8
				_wait = 0

		8:
			# 步驟 8: 蛙換第二套外裝後（第二套【星紋斗篷】）
			if _wait == 1:
				if _current_node:
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd:
						var displayed_c: Array = wd.get("_displayed_costumes")
						var target_c_idx := -1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_astral_cape":
								target_c_idx = idx
								break
						if target_c_idx >= 0:
							wd.set("costume_index", target_c_idx)
							wd.set("selected_costume_id", "costume_astral_cape")
							if wd.has_method("_update_card_selection_states"):
								wd.call("_update_card_selection_states")
							if wd.has_method("_update_ui_texts"):
								wd.call("_update_ui_texts")
							if wd.has_method("_update_preview"):
								wd.call("_update_preview")
			elif _wait >= 40:
				var path := "%s/proof_08_wardrobe_frog_costume_second.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [8/10] 蛙換第二套外裝後（第二套【星紋斗篷】）: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 9
				_wait = 0

		9:
			# 步驟 9: 蛙衣櫥標籤 en（大廳連動下，Dock、大廳、衣櫥標籤全切換至 en，0-QA25）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "The Spring-Leg Frog")
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				lobby._ready()
				lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd and wd.has_method("set_race_filter"):
						wd.call("set_race_filter", "frog")
			elif _wait >= 45:
				var path := "%s/proof_09_wardrobe_frog_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [9/10] 蛙衣櫥標籤 en 連動截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step = 10
				_wait = 0

		10:
			# 步驟 10: 蛙衣櫥標籤 ja（大廳連動下，Dock、大廳、衣櫥標籤全切換至 ja，0-QA25）
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_race", "frog")
					_gs.set("player_name", "碧箸蛙")
				var lobby = MobileLobby.new()
				root.add_child(lobby)
				lobby._ready()
				lobby._switch_tab(MobileLobby.Tab.CHARACTER)
				_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wd = _current_node.find_child("WardrobeDialog", true, false)
					if wd and wd.has_method("set_race_filter"):
						wd.call("set_race_filter", "frog")
			elif _wait >= 45:
				var path := "%s/proof_10_wardrobe_frog_ja.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [10/10] 蛙衣櫥標籤 ja 連動截圖完成: %s" % path)
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_step = 11
				_wait = 0

		11:
			_generate_crops()
			print("=== QA Round 33 實機截圖與 Crops 產出全數完成 ===")
			quit(0)
			return true

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
	var img := tex.get_image()
	if img == null or img.is_empty():
		push_error("Cannot get image")
		return
	img.save_png(abs_path)


func _generate_crops() -> void:
	# 1. 創角擴充頁最右端按鈕列特寫
	_crop_and_save(
		"%s/proof_03_creation_expansion_scroll_end.png" % OUT_DIR,
		"%s/crop_01_expansion_scroll_end.png" % CROPS_DIR,
		Rect2i(500, 15, 760, 140)
	)
	# 2. 衣櫥篩選晶片列末端特寫（象/蛙/貓，無鹿）
	_crop_and_save(
		"%s/proof_04_wardrobe_filter_chips_end.png" % OUT_DIR,
		"%s/crop_02_wardrobe_filter_chips_end.png" % CROPS_DIR,
		Rect2i(400, 70, 850, 80)
	)
	# 3. 熊貓第一套衣服預覽特寫
	_crop_and_save(
		"%s/proof_05_wardrobe_panda_costume_default.png" % OUT_DIR,
		"%s/crop_03_panda_costume_default.png" % CROPS_DIR,
		Rect2i(80, 140, 360, 420)
	)
	# 4. 熊貓第二套衣服預覽特寫
	_crop_and_save(
		"%s/proof_06_wardrobe_panda_costume_second.png" % OUT_DIR,
		"%s/crop_04_panda_costume_second.png" % CROPS_DIR,
		Rect2i(80, 140, 360, 420)
	)
	# 5. 蛙第一套衣服預覽特寫
	_crop_and_save(
		"%s/proof_07_wardrobe_frog_costume_default.png" % OUT_DIR,
		"%s/crop_05_frog_costume_default.png" % CROPS_DIR,
		Rect2i(80, 140, 360, 420)
	)
	# 6. 蛙第二套衣服預覽特寫
	_crop_and_save(
		"%s/proof_08_wardrobe_frog_costume_second.png" % OUT_DIR,
		"%s/crop_06_frog_costume_second.png" % CROPS_DIR,
		Rect2i(80, 140, 360, 420)
	)
	# 7. 蛙衣櫥 en 卡片與標籤特寫
	_crop_and_save(
		"%s/proof_09_wardrobe_frog_en.png" % OUT_DIR,
		"%s/crop_07_wardrobe_frog_en.png" % CROPS_DIR,
		Rect2i(450, 150, 800, 350)
	)
	# 8. 蛙衣櫥 ja 卡片與標籤特寫
	_crop_and_save(
		"%s/proof_10_wardrobe_frog_ja.png" % OUT_DIR,
		"%s/crop_08_wardrobe_frog_ja.png" % CROPS_DIR,
		Rect2i(450, 150, 800, 350)
	)


func _crop_and_save(src_path: String, dst_path: String, rect: Rect2i) -> void:
	if not FileAccess.file_exists(src_path):
		return
	var img := Image.load_from_file(src_path)
	if img == null or img.is_empty():
		return
	var cropped := img.get_region(rect)
	if cropped != null and not cropped.is_empty():
		cropped.save_png(dst_path)
