extends SceneTree
## 全面探索性 QA 抽查截圖腳本 (t_22571966)
## 覆蓋：大廳、C0~C6 各區開場、戰鬥（兔族/獅族）、聚魂殿、鍛造、衣櫥、設定頁

var _out_dir: String = "/opt/side/bravesoul-game/screenshots/qa_audit"
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []

var _current_dialog: Node = null

func _initialize() -> void:
	print("QA_AUDIT: Initializing full audit capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_AUDIT: load main.tscn err=", err)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待 main.tscn 就緒
			if _wait >= 50:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("QA_AUDIT: main scene ready. Step 1 -> Lobby")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 等待大廳 (Lobby) 渲染完成
			if _wait >= 45:
				_save_viewport("proof_01_lobby.png", "Lobby")
				print("QA_AUDIT: Step 2 -> C0 Village")
				_main.call("proof_jump_explore", "village")
				_step = 2
				_wait = 0

		2:
			# 等待 C0 開場
			if _wait >= 45:
				_save_viewport("proof_02_c0_village.png", "C0 Village")
				print("QA_AUDIT: Step 3 -> C1 Town")
				_main.call("proof_jump_explore", "town")
				_step = 3
				_wait = 0

		3:
			# 等待 C1 開場
			if _wait >= 45:
				_save_viewport("proof_03_c1_town.png", "C1 Town")
				print("QA_AUDIT: Step 4 -> C2 Mist")
				_main.call("proof_jump_explore", "mist_village")
				_step = 4
				_wait = 0

		4:
			# 等待 C2 開場
			if _wait >= 45:
				_save_viewport("proof_04_c2_mist.png", "C2 Mist")
				print("QA_AUDIT: Step 5 -> C3 Dojo")
				_main.call("proof_jump_explore", "dojo")
				_step = 5
				_wait = 0

		5:
			# 等待 C3 開場
			if _wait >= 45:
				_save_viewport("proof_05_c3_dojo.png", "C3 Dojo")
				print("QA_AUDIT: Step 6 -> C4 Forest")
				_main.call("proof_jump_explore", "forest")
				_step = 6
				_wait = 0

		6:
			# 等待 C4 開場
			if _wait >= 45:
				_save_viewport("proof_06_c4_forest.png", "C4 Forest")
				print("QA_AUDIT: Step 7 -> C5 Coast")
				_main.call("proof_jump_explore", "coast")
				_step = 7
				_wait = 0

		7:
			# 等待 C5 開場
			if _wait >= 45:
				_save_viewport("proof_07_c5_coast.png", "C5 Coast")
				print("QA_AUDIT: Step 8 -> C6 Tower")
				_main.call("proof_jump_explore", "tower_foyer")
				_step = 8
				_wait = 0

		8:
			# 等待 C6 開場
			if _wait >= 45:
				_save_viewport("proof_08_c6_tower.png", "C6 Tower")
				print("QA_AUDIT: Step 9 -> Battle Rabbit")
				_main.call("proof_show_battle", "road_bandit")
				_step = 9
				_wait = 0

		9:
			# 等待兔族戰鬥
			if _wait >= 50:
				_save_viewport("proof_09_battle_rabbit.png", "Battle Rabbit")
				print("QA_AUDIT: Step 10 -> Battle Lion")
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "lion")
				_main.call("proof_show_battle", "black_ronin")
				_step = 10
				_wait = 0

		10:
			# 等待獅族戰鬥
			if _wait >= 50:
				_save_viewport("proof_10_battle_lion.png", "Battle Lion")
				print("QA_AUDIT: Step 11 -> Soul Hall")
				_main.call("_go_mobile_lobby")
				_step = 11
				_wait = 0

		11:
			if _wait >= 35:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("_switch_tab"):
					lobby.call("_switch_tab", 3) # Tab.SOUL_HALL
				_step = 12
				_wait = 0

		12:
			# 等待聚魂殿渲染
			if _wait >= 45:
				_save_viewport("proof_11_soul_hall.png", "Soul Hall")
				print("QA_AUDIT: Step 13 -> Forge Dialog")
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_forge"):
					_current_dialog = lobby.call("open_forge")
				_step = 13
				_wait = 0

		13:
			# 等待鍛造彈窗
			if _wait >= 45:
				_save_viewport("proof_12_forge.png", "Forge")
				print("QA_AUDIT: Step 14 -> Wardrobe Dialog")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					lobby.call("open_wardrobe")
					_current_dialog = lobby.get_node_or_null("WardrobeDialog")
				_step = 14
				_wait = 0

		14:
			# 等待衣櫥彈窗
			if _wait >= 45:
				_save_viewport("proof_13_wardrobe.png", "Wardrobe")
				print("QA_AUDIT: Step 15 -> Settings Dialog")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_main.call("_open_mobile_settings")
				_step = 15
				_wait = 0

		15:
			# 等待設定頁
			if _wait >= 45:
				_save_viewport("proof_14_settings.png", "Settings")
				print("QA_AUDIT: ALL CAPTURES FINISHED!")
				_finish()
				return true
	return false

func _find_lobby() -> Node:
	if _main:
		var host = _main.get_node_or_null("ScreenHost")
		if host:
			for c in host.get_children():
				if c.get_script() != null and c.get_script().resource_path.ends_with("mobile_lobby.gd"):
					return c
	return null

func _save_viewport(filename: String, tag: String) -> void:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	if tex == null:
		_errors.append("get_texture is null for %s" % filename)
		return
	var img := tex.get_image()
	if img == null:
		_errors.append("get_image is null for %s" % filename)
		return
	var p := _out_dir.path_join(filename)
	var err := img.save_png(p)
	if err == OK:
		_saved.append(p)
		print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
	else:
		_errors.append("save_png failed code=%d for %s" % [err, filename])

func _finish() -> void:
	print("QA_AUDIT: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
