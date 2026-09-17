extends SceneTree
## 兔子穿維京裝（跨族）衣櫥實機截圖

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

var _out_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/cross_wear")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_run()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗 %s" % filename)
		return
	var p := _out_dir.path_join(filename)
	if img.save_png(p) == OK:
		print("CAPTURE_OK ", p)


func _run() -> void:
	await _wait_frames(5)
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
	var lobby := MobileLobby.new()
	root.add_child(lobby)
	lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(20)
	lobby.open_wardrobe()
	await _wait_frames(12)
	var dlg = null
	for c in lobby.get_children():
		if c.has_method("set_race_filter") and c.has_method("confirm_selection"):
			dlg = c
			break
	if dlg == null:
		push_error("找不到衣櫥")
		quit(1)
		return
	dlg.set_race_filter("all")
	await _wait_frames(10)
	await _capture("proof_wardrobe_all.png")
	var viking_idx := -1
	for i in range(dlg._displayed_costumes.size()):
		if str(dlg._displayed_costumes[i].get("id", "")) == "costume_viking_harness":
			viking_idx = i
			break
	if viking_idx >= 0:
		dlg.costume_index = viking_idx
		dlg.selected_costume_id = "costume_viking_harness"
		dlg._update_card_selection_states()
		dlg._update_preview()
		await _wait_frames(15)
		await _capture("proof_rabbit_wears_viking.png")

	var astral_idx := -1
	for i in range(dlg._displayed_costumes.size()):
		if str(dlg._displayed_costumes[i].get("id", "")) == "costume_astral_cape":
			astral_idx = i
			break
	if astral_idx >= 0:
		dlg.costume_index = astral_idx
		dlg.selected_costume_id = "costume_astral_cape"
		dlg._update_card_selection_states()
		dlg._update_preview()
		await _wait_frames(15)
		await _capture("proof_rabbit_wears_astral.png")

	var monk_idx := -1
	for i in range(dlg._displayed_costumes.size()):
		if str(dlg._displayed_costumes[i].get("id", "")) == "costume_dawn_monk_tunic":
			monk_idx = i
			break
	if monk_idx >= 0:
		dlg.costume_index = monk_idx
		dlg.selected_costume_id = "costume_dawn_monk_tunic"
		dlg._update_card_selection_states()
		dlg._update_preview()
		await _wait_frames(15)
		await _capture("proof_rabbit_wears_monk.png")
	print("CROSS_WEAR_CAPTURE_DONE")
	quit(0)
