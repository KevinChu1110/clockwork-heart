extends SceneTree
## 探索性 QA 盤點第六輪實機截圖抽查腳本 (t_6e6d887d)
## 覆蓋核心畫面：
## 1. 大廳 (Lobby)：白金兔、蒸汽企鵝、雲嵐鶴 (3張)
## 2. 戰鬥 (Battle)：白金兔、烈陽獅、蒸汽企鵝 (3張)
## 3. 聚魂殿 (Soul Hall)：分頁、抽卡面板 (2張)
## 4. 衣櫥 (Wardrobe)：白金兔、蒸汽企鵝(淵海深潛耐壓機關鎧)、玄軸熊 (3張)
## 5. C6 結局分支 (C6 Ending)：繁中普通結局、繁中三拒結局、英文三拒結局 (3張)

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/proofs/qa_round6",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6e6d887d/proofs"
]
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _current_dialog: Node = null

func _initialize() -> void:
	print("QA_ROUND6: Initializing Round 6 full audit capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND6: load main.tscn err=", err)
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
				print("QA_ROUND6: Step 1 -> Lobby Rabbit")
				_setup_player_env("rabbit")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 大廳 1：白金兔
			if _wait >= 45:
				_save_viewport("proof_01_lobby_rabbit.png", "Lobby Rabbit")
				print("QA_ROUND6: Step 2 -> Lobby Penguin")
				_setup_player_env("penguin")
				_main.call("_go_mobile_lobby")
				_step = 2
				_wait = 0

		2:
			# 大廳 2：蒸汽企鵝
			if _wait >= 45:
				_save_viewport("proof_02_lobby_penguin.png", "Lobby Penguin")
				print("QA_ROUND6: Step 3 -> Lobby Crane")
				_setup_player_env("crane")
				_main.call("_go_mobile_lobby")
				_step = 3
				_wait = 0

		3:
			# 大廳 3：雲嵐鶴
			if _wait >= 45:
				_save_viewport("proof_03_lobby_crane.png", "Lobby Crane")
				print("QA_ROUND6: Step 4 -> Battle Rabbit")
				_setup_player_env("rabbit")
				_main.call("proof_show_battle", "road_bandit")
				_step = 4
				_wait = 0

		4:
			# 戰鬥 1：白金兔
			if _wait >= 50:
				_save_viewport("proof_04_battle_rabbit.png", "Battle Rabbit")
				print("QA_ROUND6: Step 5 -> Battle Lion")
				_setup_player_env("lion")
				_main.call("proof_show_battle", "black_ronin")
				_step = 5
				_wait = 0

		5:
			# 戰鬥 2：烈陽獅
			if _wait >= 50:
				_save_viewport("proof_05_battle_lion.png", "Battle Lion")
				print("QA_ROUND6: Step 6 -> Battle Penguin")
				_setup_player_env("penguin")
				_main.call("proof_show_battle", "fog_shade")
				_step = 6
				_wait = 0

		6:
			# 戰鬥 3：蒸汽企鵝
			if _wait >= 50:
				_save_viewport("proof_06_battle_penguin.png", "Battle Penguin")
				print("QA_ROUND6: Step 7 -> Soul Hall Tab")
				_setup_player_env("rabbit")
				_main.call("_go_mobile_lobby")
				_step = 7
				_wait = 0

		7:
			if _wait >= 35:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("_switch_tab"):
					lobby.call("_switch_tab", MobileLobby.Tab.SOUL_HALL)
				_step = 8
				_wait = 0

		8:
			# 聚魂殿 1：分頁總覽
			if _wait >= 45:
				_save_viewport("proof_07_soul_hall_tab.png", "Soul Hall Tab")
				print("QA_ROUND6: Step 9 -> Soul Hall Panel (Draw)")
				_main.call("proof_show_soul")
				_step = 9
				_wait = 0

		9:
			# 聚魂殿 2：抽卡/魂石介面
			if _wait >= 50:
				_save_viewport("proof_08_soul_hall_panel.png", "Soul Hall Panel")
				print("QA_ROUND6: Step 10 -> Wardrobe Rabbit")
				_setup_player_env("rabbit")
				_main.call("_go_mobile_lobby")
				_step = 10
				_wait = 0

		10:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait >= 60:
				# 衣櫥 1：白金兔
				_save_viewport("proof_09_wardrobe_rabbit.png", "Wardrobe Rabbit")
				print("QA_ROUND6: Step 11 -> Wardrobe Penguin Abyssal")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("penguin")
				_main.call("_go_mobile_lobby")
				_step = 11
				_wait = 0

		11:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "penguin")
			elif _wait >= 65:
				# 衣櫥 2：蒸汽企鵝（淵海深潛耐壓機關鎧與海軍藍塗裝）
				_save_viewport("proof_10_wardrobe_penguin_abyssal.png", "Wardrobe Penguin")
				print("QA_ROUND6: Step 12 -> Wardrobe Bear")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_setup_player_env("bear")
				_main.call("_go_mobile_lobby")
				_step = 12
				_wait = 0

		12:
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait == 40:
				if is_instance_valid(_current_dialog) and _current_dialog.has_method("set_race_filter"):
					_current_dialog.call("set_race_filter", "bear")
			elif _wait >= 65:
				# 衣櫥 3：玄軸熊
				_save_viewport("proof_11_wardrobe_bear.png", "Wardrobe Bear")
				print("QA_ROUND6: Step 13 -> C6 Ending Default (zh_TW)")
				if is_instance_valid(_current_dialog):
					_current_dialog.queue_free()
					_current_dialog = null
				_main.call("proof_jump_explore", "tower_foyer")
				_step = 13
				_wait = 0

		13:
			# 等待地圖載入後播放 C6 普通結局對白
			if _wait >= 35:
				_set_locale("zh_TW")
				var lines := DialogLines.lines("c6.demon_win")
				_main.call("_play_dialog", lines, Callable())
				_step = 14
				_wait = 0

		14:
			if _wait >= 10:
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox) and dbox.has_method("_finish_typing"):
					dbox.call("_finish_typing")
				_step = 15
				_wait = 0

		15:
			# C6 結局 1：繁中普通結局
			if _wait >= 25:
				_save_viewport("proof_12_c6_demon_win_zh.png", "C6 Ending demon_win zh_TW")
				print("QA_ROUND6: Step 16 -> C6 Ending Refuse All (zh_TW)")
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox):
					dbox.visible = false
				_step = 16
				_wait = 0

		16:
			if _wait >= 15:
				_set_locale("zh_TW")
				var lines := DialogLines.lines("c6.demon_win_refuse_all")
				_main.call("_play_dialog", lines, Callable())
				_step = 17
				_wait = 0

		17:
			if _wait >= 10:
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox) and dbox.has_method("_finish_typing"):
					dbox.call("_finish_typing")
				_step = 18
				_wait = 0

		18:
			# C6 結局 2：繁中三拒結局
			if _wait >= 25:
				_save_viewport("proof_13_c6_refuse_all_zh.png", "C6 Ending refuse_all zh_TW")
				print("QA_ROUND6: Step 19 -> C6 Ending Refuse All (en)")
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox):
					dbox.visible = false
				_step = 19
				_wait = 0

		19:
			if _wait >= 15:
				_set_locale("en")
				var lines := DialogLines.lines("c6.demon_win_refuse_all")
				_main.call("_play_dialog", lines, Callable())
				_step = 20
				_wait = 0

		20:
			if _wait >= 10:
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox) and dbox.has_method("_finish_typing"):
					dbox.call("_finish_typing")
				_step = 21
				_wait = 0

		21:
			# C6 結局 3：英文三拒結局
			if _wait >= 25:
				_save_viewport("proof_14_c6_refuse_all_en.png", "C6 Ending refuse_all en")
				print("QA_ROUND6: ALL 14 CAPTURES FINISHED SUCCESSFULLY!")
				_finish()
				return true

	return false

func _setup_player_env(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("energy", 15)
		gs.set("gold", 8888)
		gs.set("stardust", 30)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
	var tut: Node = root.get_node_or_null("TutorialSystem")
	if tut and tut.has_method("mark"):
		for k in ["boot", "explore", "battle_auto", "battle_parry", "battle_fog", "forge", "paths", "soul", "fort", "flag_hint", "ng"]:
			tut.call("mark", k)
	if sk and sk.has_method("ensure_skill_map"):
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")

func _set_locale(loc: String) -> void:
	var loc_node = root.get_node_or_null("Loc")
	if loc_node:
		loc_node.set("locale", loc)
	TranslationServer.set_locale(loc)
	DialogLines.reload()

func _find_lobby() -> Node:
	if _main:
		var host = _main.get("host") as Control
		if host:
			for c in host.get_children():
				if c is MobileLobby:
					return c
		var host_node = _main.get_node_or_null("Host")
		if host_node:
			for c in host_node.get_children():
				if c is MobileLobby:
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
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])

func _finish() -> void:
	print("QA_ROUND6: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
