extends SceneTree
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_elephant_wardrobe_new_costume.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生鋼岳象衣櫥換裝彈窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe_elephant")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "elephant"
		gs.player_name = "鋼岳象"
		gs.paperdoll_slots = {
			"race": "elephant",
			"costume": "costume_colossus_bastion_plate",
			"chassis": "paint_tungsten_iron",
			"costume_id": "costume_colossus_bastion_plate",
			"paint_id": "paint_tungsten_iron",
			"weapon": "wpn_colossus_cleaver_axe"
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
						if _wardrobe.has_method("set_race_filter"):
							_wardrobe.call("set_race_filter", "elephant")
						
						var displayed_c: Array = _wardrobe.get("_displayed_costumes")
						var target_c_idx := 1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_colossus_bastion_plate":
								target_c_idx = idx
								break
						
						var displayed_ch: Array = _wardrobe.get("_displayed_chassis")
						var target_ch_idx := 1
						for idx in range(displayed_ch.size()):
							if displayed_ch[idx].get("id") == "paint_tungsten_iron":
								target_ch_idx = idx
								break

						_wardrobe.set("costume_index", target_c_idx)
						_wardrobe.set("chassis_index", target_ch_idx)
						_wardrobe.set("selected_costume_id", "costume_colossus_bastion_plate")
						_wardrobe.set("selected_chassis_id", "paint_tungsten_iron")

						if _wardrobe.has_method("_update_card_selection_states"):
							_wardrobe.call("_update_card_selection_states")
						if _wardrobe.has_method("_update_ui_texts"):
							_wardrobe.call("_update_ui_texts")
						if _wardrobe.has_method("_update_preview"):
							_wardrobe.call("_update_preview")
						print("  [Wardrobe] 已開啟衣櫥並選中【鋼岳要塞重裝戰鎧】與【高爐鎢鋼淬火黑】")

			elif _wait_frames == 25:
				# 等待佈局穩定後滾動 FilterScroll，確保「象」chip 清晰可見
				if _wardrobe != null:
					var filter_scroll: ScrollContainer = _wardrobe.find_child("FilterScroll", true, false)
					if filter_scroll != null:
						filter_scroll.scroll_horizontal = 9999
						print("  [Wardrobe] FilterScroll 滾動至末端 (scroll_horizontal = 9999)")

			elif _wait_frames >= 40:
				var fn := "proof_wardrobe_elephant_bastion.png"
				_save_screenshot(fn)
				print("  ✓ [1/2] 鋼岳象穿戴【鋼岳要塞重裝戰鎧】衣櫥彈窗截圖完成 -> %s" % fn)

				# 切換至【巨輪工坊厚鋼工裝】對照
				if _wardrobe != null and is_instance_valid(_wardrobe):
					var displayed_c: Array = _wardrobe.get("_displayed_costumes")
					var target_c_idx := 0
					for idx in range(displayed_c.size()):
						if displayed_c[idx].get("id") == "costume_cog_workshop_overalls":
							target_c_idx = idx
							break

					_wardrobe.set("costume_index", target_c_idx)
					_wardrobe.set("selected_costume_id", "costume_cog_workshop_overalls")
					if _wardrobe.has_method("_update_card_selection_states"):
						_wardrobe.call("_update_card_selection_states")
					if _wardrobe.has_method("_update_ui_texts"):
						_wardrobe.call("_update_ui_texts")
					if _wardrobe.has_method("_update_preview"):
						_wardrobe.call("_update_preview")

				_step = 2
				_wait_frames = 0

		2:
			if _wait_frames >= 20:
				var fn := "proof_wardrobe_elephant_overalls.png"
				_save_screenshot(fn)
				print("  ✓ [2/2] 鋼岳象穿戴【巨輪工坊厚鋼工裝】衣櫥彈窗截圖完成 -> %s" % fn)
				_finish()
				return true

	return false

func _save_screenshot(filename: String) -> void:
	var img := root.get_texture().get_image()
	var path := _out_dir.path_join(filename)
	img.save_png(path)
	print("    [Saved] %s (Size: %dx%d)" % [path, img.get_width(), img.get_height()])

func _finish() -> void:
	print("=== 鋼岳象衣櫥實機截圖作業完成 ===")
	quit(0)
