extends SceneTree
## 全面探索性 QA 抽查截圖腳本第二輪 (t_02d07272)
## 覆蓋：大廳、冒險分頁、戰鬥（五族開局各打一場：兔/狐/獅/豬/猴）、部位破壞、聚魂殿（分頁＋彈窗）、武術館（導師＋兵器架）、衣櫥、設定頁

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/qa_round2",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5180b4c2/screenshots"
]
var _main: Node = null
var _step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []
var _current_dialog: Node = null

var _races = [
	{"race": "rabbit", "name": "星芒兔", "skill": "橫斬", "mode": "road_bandit", "file": "proof_03_battle_rabbit.png", "tag": "Battle Rabbit"},
	{"race": "fox", "name": "靈尾狐", "skill": "魔彈", "mode": "fog_shade", "file": "proof_04_battle_fox.png", "tag": "Battle Fox"},
	{"race": "lion", "name": "烈鬃獅", "skill": "一線突刺", "mode": "black_ronin", "file": "proof_05_battle_lion.png", "tag": "Battle Lion"},
	{"race": "boar", "name": "鋼牙豕", "skill": "碎岩鎚", "mode": "coast_raider", "file": "proof_06_battle_boar.png", "tag": "Battle Boar"},
	{"race": "macaque", "name": "金毛猴", "skill": "連環拳", "mode": "bamboo_spirit", "file": "proof_07_battle_macaque.png", "tag": "Battle Macaque"},
]
var _race_idx: int = 0

func _initialize() -> void:
	print("QA_ROUND2: Initializing round 2 full audit capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND2: load main.tscn err=", err)
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
				print("QA_ROUND2: main scene ready. Step 1 -> Lobby")
				_setup_player_env("rabbit")
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0

		1:
			# 等待大廳 (Lobby) 渲染完成
			if _wait >= 50:
				_save_viewport("proof_01_lobby.png", "Lobby")
				print("QA_ROUND2: Step 2 -> Adventure Tab")
				var lobby = _find_lobby()
				if lobby and lobby.has_method("_switch_tab"):
					lobby.call("_switch_tab", MobileLobby.Tab.ADVENTURE)
				_step = 2
				_wait = 0

		2:
			# 等待冒險分頁渲染完成
			if _wait >= 50:
				_save_viewport("proof_02_adventure_tab.png", "Adventure Tab")
				print("QA_ROUND2: Step 3 -> Five Races Battles")
				_race_idx = 0
				_start_race_battle(_race_idx)
				_step = 3
				_wait = 0

		3:
			# 等待各族戰鬥載入並注入技能/滿怒
			if _wait == 25:
				var cur = _races[_race_idx]
				var host: Control = _main.get("host") as Control
				var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if bnode and is_instance_valid(bnode):
					var sim = bnode.get("sim")
					if sim != null:
						var p = sim.call("get_unit", "player")
						if p != null:
							p.rage = 100.0
					if bnode.has_method("_append_log"):
						bnode.call("_append_log", "[color=#1a4a75]%s 開局 T1 武器整備，滿怒 100%% 爆發！[/color]" % cur["name"])
						bnode.call("_append_log", "[color=#b24a00]%s 使出 %s！[/color]" % [cur["name"], cur["skill"]])
					if bnode.has_method("_flash_skill_banner"):
						bnode.call("_flash_skill_banner", cur["skill"], true)
			elif _wait >= 50:
				var cur = _races[_race_idx]
				_save_viewport(cur["file"], cur["tag"])
				_race_idx += 1
				if _race_idx < _races.size():
					_start_race_battle(_race_idx)
					_wait = 0
				else:
					print("QA_ROUND2: Step 4 -> Part Destruction Battle")
					_start_part_break_battle()
					_step = 4
					_wait = 0

		4:
			# 等待部位破壞戰鬥載入並注入部位破壞
			if _wait == 30:
				var host: Control = _main.get("host") as Control
				var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if bnode and is_instance_valid(bnode):
					var sim = bnode.get("sim")
					if sim != null:
						var boss = sim.call("_primary_boss_unit")
						if boss and not boss.parts.is_empty():
							sim.parts_break_unlocked = true
							boss.hp = int(boss.max_hp * 0.6) # 降至 60% 開啟部位破壞
							sim.focus_part_id = "shield"
							var shield_max = int(boss.parts[1].get("max_hp", 80))
							sim.call("_process_part_damage", boss, shield_max + 10, true)
							if bnode.has_method("_append_log"):
								bnode.call("_append_log", "[color=#fc0]部位破壞測試：鎖定【盾·鋼爪圓盾】，破甲降防！[/color]")
							if bnode.has_method("_refresh_part_bars"):
								bnode.call("_refresh_part_bars", boss)
							if bnode.has_method("_refresh_part_focus_hint"):
								bnode.call("_refresh_part_focus_hint")
							if bnode.has_method("_refresh_hud"):
								bnode.call("_refresh_hud")
			elif _wait >= 55:
				_save_viewport("proof_08_battle_part_break.png", "Part Break Battle")
				print("QA_ROUND2: Step 5 -> Soul Hall Tab")
				_setup_player_env("rabbit")
				_main.call("_go_mobile_lobby")
				_step = 5
				_wait = 0

		5:
			# 等待大廳切換至聚魂殿分頁
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("_switch_tab"):
					lobby.call("_switch_tab", MobileLobby.Tab.SOUL_HALL)
			elif _wait >= 55:
				_save_viewport("proof_09_soul_hall_tab.png", "Soul Hall Tab")
				print("QA_ROUND2: Step 6 -> Soul Hall Panel (Dialog)")
				_main.call("_go_soul_panel")
				_step = 6
				_wait = 0

		6:
			# 等待聚魂殿彈窗 (武器魂槽資訊與保底)
			if _wait >= 50:
				_save_viewport("proof_10_soul_hall_panel.png", "Soul Hall Panel")
				print("QA_ROUND2: Step 7 -> Tutor Hall (Martial Arts)")
				_main.call("proof_show_tutor")
				_step = 7
				_wait = 0

		7:
			# 等待武術館 · 導師指點
			if _wait >= 50:
				_save_viewport("proof_11_tutor_hall.png", "Tutor Hall")
				print("QA_ROUND2: Step 8 -> Weapon Wall (Martial Arts)")
				_main.call("_go_weapon_wall_panel")
				_step = 8
				_wait = 0

		8:
			# 等待武術館 · 兵器架整備
			if _wait >= 50:
				_save_viewport("proof_12_weapon_wall.png", "Weapon Wall")
				print("QA_ROUND2: Step 9 -> Wardrobe Dialog")
				_setup_player_env("lion") # 用獅族打開衣櫥，同時複驗獅族外裝塗裝
				_main.call("_go_mobile_lobby")
				_step = 9
				_wait = 0

		9:
			# 等待大廳並打開衣櫥彈窗
			if _wait == 25:
				var lobby = _find_lobby()
				if lobby and lobby.has_method("open_wardrobe"):
					_current_dialog = lobby.call("open_wardrobe")
			elif _wait >= 60:
				_save_viewport("proof_13_wardrobe.png", "Wardrobe")
				print("QA_ROUND2: Step 10 -> Settings Dialog")
				var lobby = _find_lobby()
				if lobby:
					var wd = lobby.get_node_or_null("WardrobeDialog")
					if wd and is_instance_valid(wd):
						wd.queue_free()
				_main.call("_open_mobile_settings")
				_step = 10
				_wait = 0

		10:
			# 等待設定頁
			if _wait >= 50:
				_save_viewport("proof_14_settings.png", "Settings")
				print("QA_ROUND2: ALL 14 CAPTURES FINISHED SUCCESSFULLY!")
				_finish()
				return true
	return false

func _setup_player_env(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("energy", 15)
		gs.set("gold", 2500)
		gs.set("stardust", 10)
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

func _start_race_battle(idx: int) -> void:
	var cur = _races[idx]
	print("QA_ROUND2: Starting race battle [%s] mode=%s" % [cur["race"], cur["mode"]])
	_setup_player_env(cur["race"])
	if _main:
		_main.call("_start_battle_raw", cur["mode"])

func _start_part_break_battle() -> void:
	print("QA_ROUND2: Starting part break battle mode=leo")
	_setup_player_env("rabbit")
	if _main:
		_main.call("_start_battle_raw", "leo")

func _find_lobby() -> Node:
	if _main:
		var host = _main.get("host") as Control
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
	for d in _out_dirs:
		var p := d.path_join(filename)
		var err := img.save_png(p)
		if err == OK:
			_saved.append(p)
			print("  ✓ SAVED [%s] (%dx%d) -> %s" % [tag, img.get_width(), img.get_height(), p])
		else:
			_errors.append("save_png failed code=%d for %s" % [err, p])

func _finish() -> void:
	print("QA_ROUND2: Done. saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  FILE: ", s)
	for e in _errors:
		print("  ERR: ", e)
	quit(0 if _errors.is_empty() else 1)
