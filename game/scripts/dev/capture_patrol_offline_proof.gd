extends SceneTree
## 發條自動巡邏全自動離線結算大廳側欄實機截圖產生器
## 執行指令：godot --path game --headless -s res://scripts/dev/capture_patrol_offline_proof.gd

var _frame := 0
var _lobby: Control = null
var _out_dir := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	var patrol = root.get_node_or_null("ClockworkPatrolSystem")
	if gs:
		gs.reset_new_game()
		gs.player_name = "小白"
		gs.level = 15
		gs.gold = 3520
		gs.energy = 14
	
	if patrol:
		patrol.clear_patrol_data_for_test()
		# 模擬離線巡邏 1 小時 30 分後登入
		var t0 := 1700000000.0
		patrol.settle_offline_patrol(t0)
		patrol.settle_offline_patrol(t0 + 5400.0)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = LobbyClass.new()
	root.add_child(_lobby)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 30:
		return false
	
	var tex := root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img != null:
		var p1 := _out_dir.path_join("proof_patrol_offline_lobby.png")
		var p2 := ProjectSettings.globalize_path("res://").path_join("../proof_patrol_offline_lobby.png")
		img.save_png(p1)
		img.save_png(p2)
		print("CAPTURE_SAVED: ", p1)
		print("CAPTURE_SAVED: ", p2)
	else:
		push_error("無法獲取 framebuffer 圖像")
	
	quit(0)
	return true
