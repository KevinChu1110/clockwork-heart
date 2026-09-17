extends SceneTree
## 大廳 PPT 清理後實機截圖（設置圖示／出征圖示／半透明頂底欄）

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/ui_ppt_clean")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_run()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img == null or img.is_empty():
		push_error("截圖失敗: %s" % filename)
		return
	var p := _out_dir.path_join(filename)
	if img.save_png(p) == OK:
		print("CAPTURE_OK ", p)
	else:
		push_error("截圖儲存失敗: %s" % p)


func _run() -> void:
	await _wait_frames(5)
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.gold = 1000
		gs.level = 10
		gs.energy = 15
	var lobby := MobileLobby.new()
	root.add_child(lobby)
	lobby._switch_tab(MobileLobby.Tab.VILLAGE)
	lobby.select_hall_card(-1)
	await _wait_frames(30)
	await _capture_frame("proof_lobby_village.png")
	lobby._switch_tab(MobileLobby.Tab.CHARACTER)
	await _wait_frames(20)
	await _capture_frame("proof_lobby_char.png")
	print("PPT_CLEAN_CAPTURE_DONE")
	quit(0)
