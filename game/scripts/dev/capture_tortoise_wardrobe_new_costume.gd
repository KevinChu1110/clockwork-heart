extends SceneTree
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_tortoise_wardrobe_new_costume.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""
var _wait_frames: int = 0
var _step: int = 0
var _lobby: MobileLobby = null
var _wardrobe: Control = null

func _initialize() -> void:
	print("=== 開始產生玄機龜衣櫥換裝彈窗實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/wardrobe_tortoise")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "tortoise"
		gs.player_name = "玄機龜"
		gs.paperdoll_slots = {
			"race": "tortoise",
			"costume": "costume_bagua_master_robe",
			"chassis": "paint_basalt_black",
			"costume_id": "costume_bagua_master_robe",
			"paint_id": "paint_basalt_black",
			"weapon": "wpn_bagua_astrolabe"
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
						# Filter to tortoise if needed, or find index of costume_bagua_master_robe
						if _wardrobe.has_method("filter_by_race"):
							_wardrobe.call("filter_by_race", "tortoise")
						
						var displayed_c: Array = _wardrobe.get("_displayed_costumes")
						var target_c_idx := 1
						for idx in range(displayed_c.size()):
							if displayed_c[idx].get("id") == "costume_bagua_master_robe":
								target_c_idx = idx
								break
						
						var displayed_ch: Array = _wardrobe.get("_displayed_chassis")
						var target_ch_idx := 1
						for idx in range(displayed_ch.size()):
							if displayed_ch[idx].get("id") == "paint_basalt_black":
								target_ch_idx = idx
								break

						_wardrobe.set("costume_index", target_c_idx)
						_wardrobe.set("chassis_index", target_ch_idx)
						_wardrobe.set("selected_costume_id", "costume_bagua_master_robe")
						_wardrobe.set("selected_chassis_id", "paint_basalt_black")

						if _wardrobe.has_method("_update_card_selection_states"):
							_wardrobe.call("_update_card_selection_states")
						if _wardrobe.has_method("_update_ui_texts"):
							_wardrobe.call("_update_ui_texts")
						if _wardrobe.has_method("_update_preview"):
							_wardrobe.call("_update_preview")
						print("  [Wardrobe] 已開啟衣櫥並選中【乾坤八卦宗師道鎧】與【玄武黑曜淬火黑】")

			if _wait_frames >= 40:
				var fn := "proof_wardrobe_tortoise_bagua.png"
				_save_screenshot(fn)
				print("  ✓ [1/2] 玄機龜穿戴【乾坤八卦宗師道鎧】衣櫥彈窗截圖完成 -> %s" % fn)

				# 切換至【天元道場玄機護甲】對照
				if _wardrobe != null and is_instance_valid(_wardrobe):
					var displayed_c: Array = _wardrobe.get("_displayed_costumes")
					var target_c_idx := 0
					for idx in range(displayed_c.size()):
						if displayed_c[idx].get("id") == "costume_zen_dojo_harness":
							target_c_idx = idx
							break

					_wardrobe.set("costume_index", target_c_idx)
					_wardrobe.set("selected_costume_id", "costume_zen_dojo_harness")
					if _wardrobe.has_method("_update_card_selection_states"):
						_wardrobe.call("_update_card_selection_states")
					if _wardrobe.has_method("_update_ui_texts"):
						_wardrobe.call("_update_ui_texts")
					if _wardrobe.has_method("_update_preview"):
						_wardrobe.call("_update_preview")
					print("  [Wardrobe] 已切換回【天元道場玄機護甲】")
				_step = 2
				_wait_frames = 0
		2:
			if _wait_frames >= 30:
				var fn2 := "proof_wardrobe_tortoise_harness.png"
				_save_screenshot(fn2)
				print("  ✓ [2/2] 玄機龜穿戴【天元道場玄機護甲】衣櫥彈窗截圖完成 -> %s" % fn2)
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
		push_error("無法取得 Viewport")
		return
	var img := vp.get_texture().get_image()
	if img == null or img.is_empty():
		push_error("無法自 Viewport 取得影像")
		return
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		print("  [Screenshot] 已成功儲存截圖至: %s" % p)
	else:
		push_error("截圖儲存失敗，錯誤碼: %d" % err)

func _finish() -> void:
	print("=== 玄機龜衣櫥換裝彈窗實機截圖流程結束 ===")
	quit(0)
