extends SceneTree
## 回歸驗收截圖腳本 (t_0d3accdd)
## 覆蓋四項合併修復驗收點：
## 1. 大廳 (HUD 與快捷欄不穿透遮蓋 Dock 文字)
## 2. C2 白霧之地 (無矩形遮罩硬邊/斷層)
## 3. C3 試煉山門 (無矩形遮罩硬邊/斷層)
## 4. C4 疾影森林 (無矩形遮罩硬邊/斷層)
## 5. 兔族戰鬥 (滿怒起手技能 [橫斬] 施放)
## 6. 獅族戰鬥 (滿怒起手技能 [一線突刺] 施放)
## 7. 衣櫥彈窗切獅族 (蒸氣工匠與午夜深藍兩張卡有圖不全白，且 HUD 不遮蓋標題)

var _out_dir: String = "/opt/side/bravesoul-game/screenshots/regression_four_fixes"
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []

func _initialize() -> void:
	print("REGRESSION_CAPTURE: Initializing...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("REGRESSION_CAPTURE: load main.tscn err=", err)
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
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "rabbit")
				print("REGRESSION_CAPTURE: Step 1 -> Lobby")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 1. 大廳截圖
			if _wait >= 45:
				_save_viewport("proof_01_lobby.png", "Lobby")
				print("REGRESSION_CAPTURE: Step 2 -> C2 Mist")
				_main.call("proof_jump_explore", "mist_village")
				_step = 2
				_wait = 0

		2:
			# 2. C2 白霧之地
			if _wait >= 45:
				_save_viewport("proof_02_c2_mist.png", "C2 Mist")
				print("REGRESSION_CAPTURE: Step 3 -> C3 Dojo")
				_main.call("proof_jump_explore", "dojo")
				_step = 3
				_wait = 0

		3:
			# 3. C3 試煉山門
			if _wait >= 45:
				_save_viewport("proof_03_c3_dojo.png", "C3 Dojo")
				print("REGRESSION_CAPTURE: Step 4 -> C4 Forest")
				_main.call("proof_jump_explore", "forest")
				_step = 4
				_wait = 0

		4:
			# 4. C4 疾影森林
			if _wait >= 45:
				_save_viewport("proof_04_c4_forest.png", "C4 Forest")
				print("REGRESSION_CAPTURE: Step 5 -> Battle Rabbit (road_bandit)")
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "rabbit")
				_main.call("proof_show_battle", "road_bandit")
				_step = 5
				_wait = 0

		5:
			# 5. 兔族戰鬥：設置滿怒並觸發技能
			if _wait == 25:
				var battle := _find_battle()
				if battle:
					var sim = battle.get("sim")
					if sim:
						var pu = sim.get_unit("player")
						if pu:
							pu.rage = 100.0
							print("  --> Rabbit player unit rage set to 100, can_skill=", pu.can_skill)
			elif _wait >= 50:
				_save_viewport("proof_05_battle_rabbit.png", "Battle Rabbit")
				print("REGRESSION_CAPTURE: Step 6 -> Battle Lion (black_ronin)")
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "lion")
				_main.call("proof_show_battle", "black_ronin")
				_step = 6
				_wait = 0

		6:
			# 6. 獅族戰鬥：設置滿怒並觸發技能
			if _wait == 25:
				var battle := _find_battle()
				if battle:
					var sim = battle.get("sim")
					if sim:
						var pu = sim.get_unit("player")
						if pu:
							pu.rage = 100.0
							print("  --> Lion player unit rage set to 100, can_skill=", pu.can_skill)
			elif _wait >= 50:
				_save_viewport("proof_06_battle_lion.png", "Battle Lion")
				print("REGRESSION_CAPTURE: Step 7 -> Wardrobe Lion")
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "lion")
				_main.call("_go_mobile_lobby")
				_step = 7
				_wait = 0

		7:
			# 等待大廳切換完成，開啟獅族換裝衣櫥
			if _wait >= 35:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					lobby.call("open_wardrobe")
					var dlg = lobby.get_node_or_null("WardrobeDialog")
					if dlg:
						if "current_race" in dlg:
							dlg.current_race = "lion"
						if dlg.has_method("_rebuild_cards"):
							dlg.call("_rebuild_cards")
						if dlg.has_method("_update_preview"):
							dlg.call("_update_preview")
						if dlg.has_method("_update_ui_texts"):
							dlg.call("_update_ui_texts")
						print("  --> WardrobeDialog opened for lion")
				_step = 8
				_wait = 0

		8:
			# 7. 獅族衣櫥截圖
			if _wait >= 45:
				_save_viewport("proof_07_wardrobe_lion.png", "Wardrobe Lion")
				print("REGRESSION_CAPTURE: ALL 7 CAPTURES FINISHED!")
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

func _find_battle() -> Node:
	if _main:
		var host = _main.get_node_or_null("ScreenHost")
		if host:
			for c in host.get_children():
				if c.get_script() != null and c.get_script().resource_path.ends_with("battle_view.gd"):
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
	print("REGRESSION_CAPTURE: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
