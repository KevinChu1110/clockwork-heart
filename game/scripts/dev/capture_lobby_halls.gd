extends SceneTree
## 《發條之心》大廳三殿堂彈窗（王都鐵匠、手藝工坊、冒險委託）實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_lobby_halls.gd

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _lobby: MobileLobby = null
var _current_dlg: Control = null


func _initialize() -> void:
	print("=== 開始產生大廳三殿堂實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/lobby_halls")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.gold = 1000
		gs.level = 10

	var ws = root.get_node_or_null("WindupDailySystem")
	if ws:
		ws.debug_day = 20260911
		ws.refresh()

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_step = 1


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		1:
			# 等待大廳載入完畢，開啟鐵匠
			if _frame_count >= 10:
				print("  開啟王都鐵匠彈窗...")
				_current_dlg = _lobby.open_forge()
				_step = 2
				_frame_count = 0
		2:
			# 等待渲染穩定，截取鐵匠畫面
			if _frame_count >= 15:
				_save_shot("proof_lobby_hall_forge.png")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
				_step = 3
				_frame_count = 0
		3:
			# 等待關閉過渡，開啟手藝工坊
			if _frame_count >= 10:
				print("  開啟手藝工坊彈窗...")
				_current_dlg = _lobby.open_gem_workshop()
				_step = 4
				_frame_count = 0
		4:
			# 等待渲染穩定，截取工坊畫面
			if _frame_count >= 15:
				_save_shot("proof_lobby_hall_gem.png")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
				_step = 5
				_frame_count = 0
		5:
			# 等待關閉過渡，開啟冒險委託
			if _frame_count >= 10:
				print("  開啟冒險委託彈窗...")
				_current_dlg = _lobby.open_windup_daily()
				_step = 6
				_frame_count = 0
		6:
			# 等待渲染穩定，截取冒險委託畫面
			if _frame_count >= 15:
				_save_shot("proof_lobby_hall_windup.png")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
				_step = 7
				_frame_count = 0
		7:
			print("CAPTURE_LOBBY_HALLS_OK")
			quit(0)
			return true
	return false


func _save_shot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p := _out_dir.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			print("  ✓ 成功存證截圖: ", p)
		else:
			push_error("截圖儲存失敗: %s" % p)
		if filename == "proof_lobby_hall_forge.png":
			var base := ProjectSettings.globalize_path("res://")
			var p_web := base.path_join("../web/media/shots/proof_forge_panel.png")
			var p_shots := base.path_join("../screenshots/proof_forge_panel.png")
			DirAccess.make_dir_recursive_absolute(base.path_join("../web/media/shots"))
			DirAccess.make_dir_recursive_absolute(base.path_join("../screenshots"))
			img.save_png(p_web)
			img.save_png(p_shots)
			print("  ✓ 同步官網鍛造圖: ", p_web)
