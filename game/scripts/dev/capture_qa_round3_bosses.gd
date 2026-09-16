extends SceneTree
## 全面探索性 QA 第三輪截圖腳本 (t_4dc78d3c)
## 覆蓋：
## 1. 七大首領戰鬥開場與部位破壞（leo, wolf, fog, abo, falcon, boar, demon）
## 2. 七大首領遊戲內對話／過場半身像（leo, wolf, fog, abo, falcon, boar, demon）

var _out_dirs: Array[String] = [
	"/opt/side/bravesoul-game/screenshots/qa_round3",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_4dc78d3c/screenshots"
]

var _main: Node = null
var _phase: int = 0
var _sub_idx: int = 0
var _sub_step: int = 0
var _wait: int = 0
var _saved: Array[String] = []
var _errors: Array[String] = []

var _battle_bosses: Array[Dictionary] = [
	{"id": "leo", "name": "守衛泰坦·雷歐", "has_parts": true},
	{"id": "wolf", "name": "失控的鏽蝕玩具（狼）", "has_parts": false},
	{"id": "fog", "name": "白霧", "has_parts": true},
	{"id": "abo", "name": "阿波", "has_parts": true},
	{"id": "falcon", "name": "疾影", "has_parts": true},
	{"id": "boar", "name": "石拳", "has_parts": true},
	{"id": "demon", "name": "停擺核", "has_parts": true},
]

var _dialogues: Array[Dictionary] = [
	{"id": "leo", "speaker": "雷歐", "text": "渺小的兔子……也想挑戰獅衛之王？"},
	{"id": "wolf", "speaker": "失控的鏽蝕玩具", "text": "喀啦喀啦……（發條劇烈顫動，齒輪咬合聲刺耳，金屬殘肢在荒路拖曳）"},
	{"id": "fog", "speaker": "白霧", "text": "嘻嘻～真的假的，你分得清嗎？"},
	{"id": "abo", "speaker": "阿波", "text": "發條最鬆的。來打我的架勢。打不穿的時候，別急——一下一下，把殼撞鬆。"},
	{"id": "falcon", "speaker": "疾影", "text": "……把發條最鬆的送來了？眼睛，跟得上我嗎？追，會迷路。等，才見我。"},
	{"id": "boar", "speaker": "石拳", "text": "……把發條最鬆的送來了？還站著？那就接下這一拳——力氣該砸向誰？"},
	{"id": "demon", "speaker": "停擺核", "text": "……沉寂的時間……將歸於永恆停擺……你的發條，終將停止旋動。"},
]

func _initialize() -> void:
	print("QA_ROUND3: Initializing Bosses & Dialogues Audit Capture...")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	var err := change_scene_to_file("res://scenes/main.tscn")
	print("QA_ROUND3: change_scene_to_file err=", err)
	_phase = 0
	_sub_idx = 0
	_sub_step = 0
	_wait = 0

func _setup_player_env() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("energy", 30)
		gs.set("gold", 5000)
		gs.set("hp", 80)
		gs.set("max_hp", 80)
		gs.set("weapon_uses_left", 20)
		gs.set("weapon_uses_max", 20)
		gs.set_flag("tut_done", true)
		gs.set_flag("c1_forged", true)
		gs.set_flag("c1_entered_city", true)
		gs.set_flag("c1_soul_intro", true)
	if sk:
		sk.call("ensure_skill_map")
		sk.call("grant_c1_greybeard")

func _process(_delta: float) -> bool:
	_wait += 1
	match _phase:
		0:
			# 等待 main.tscn 就緒
			if _wait >= 40:
				_main = current_scene
				if _main == null:
					_errors.append("main scene is null")
					_finish()
					return false
				print("QA_ROUND3: main ready. Moving to Phase 1: Battles")
				_phase = 1
				_sub_idx = 0
				_sub_step = 0
				_wait = 0

		1:
			# Phase 1: 戰鬥場景巡檢 (開場 + 部位破壞)
			var bdata: Dictionary = _battle_bosses[_sub_idx]
			var boss_id: String = bdata["id"]
			match _sub_step:
				0:
					print("QA_ROUND3: Starting Battle [%d/%d] id=%s (%s)" % [_sub_idx + 1, _battle_bosses.size(), boss_id, bdata["name"]])
					_setup_player_env()
					_main.call("_start_battle_raw", boss_id)
					_sub_step = 1
					_wait = 0
				1:
					# 等待開場畫面穩定
					if _wait >= 35:
						var filename := "proof_battle_open_%s.png" % boss_id
						_save_viewport(filename, "Battle Open - " + bdata["name"])
						if bdata["has_parts"]:
							_sub_step = 2
							_wait = 0
						else:
							# 無部位破壞（例如狼），直接進入下一隻
							_sub_idx += 1
							if _sub_idx >= _battle_bosses.size():
								print("QA_ROUND3: All battles completed. Moving to Phase 2: Dialogues")
								_phase = 2
								_sub_idx = 0
								_sub_step = 0
								_wait = 0
							else:
								_sub_step = 0
								_wait = 0
				2:
					# 觸發部位破壞
					var host: Control = _main.get("host") as Control
					var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
					if bnode and is_instance_valid(bnode):
						var sim = bnode.get("sim")
						if sim != null:
							var boss = sim.call("_primary_boss_unit")
							if boss and not boss.parts.is_empty():
								sim.parts_break_unlocked = true
								boss.hp = int(boss.max_hp * 0.6)
								var part = boss.parts[0]
								sim.focus_part_id = str(part.get("id", ""))
								var p_max = int(part.get("max_hp", 60))
								sim.call("_process_part_damage", boss, p_max + 20, true)
								if bnode.has_method("_append_log"):
									bnode.call("_append_log", "[color=#fc0]QA測試：部位破壞觸發【%s】！[/color]" % str(part.get("name", "部位")))
								if bnode.has_method("_refresh_part_bars"):
									bnode.call("_refresh_part_bars", boss)
								if bnode.has_method("_refresh_part_focus_hint"):
									bnode.call("_refresh_part_focus_hint")
								if bnode.has_method("_refresh_hud"):
									bnode.call("_refresh_hud")
					_sub_step = 3
					_wait = 0
				3:
					# 等待部位破壞視覺渲染
					if _wait >= 25:
						var filename := "proof_battle_part_break_%s.png" % boss_id
						_save_viewport(filename, "Battle Part Break - " + bdata["name"])
						_sub_idx += 1
						if _sub_idx >= _battle_bosses.size():
							print("QA_ROUND3: All battles completed. Moving to Phase 2: Dialogues")
							_phase = 2
							_sub_idx = 0
							_sub_step = 0
							_wait = 0
						else:
							_sub_step = 0
							_wait = 0

		2:
			# Phase 2: 對話／過場半身像巡檢
			var ddata: Dictionary = _dialogues[_sub_idx]
			match _sub_step:
				0:
					print("QA_ROUND3: Playing Dialogue [%d/%d] speaker=%s" % [_sub_idx + 1, _dialogues.size(), ddata["speaker"]])
					var lines := [
						{"speaker": ddata["speaker"], "text": ddata["text"]}
					]
					_main.call("_play_dialog", lines)
					_sub_step = 1
					_wait = 0
				1:
					# 等待打字機完成或快進
					var dbox: Node = _main.get("_dialogue")
					if dbox and is_instance_valid(dbox):
						if dbox.has_method("_finish_typing"):
							dbox.call("_finish_typing")
					if _wait >= 25:
						var filename := "proof_dialogue_%s.png" % ddata["id"]
						_save_viewport(filename, "Dialogue - " + ddata["speaker"])
						if dbox and dbox.has_method("_advance"):
							dbox.call("_advance")
						_sub_idx += 1
						if _sub_idx >= _dialogues.size():
							print("QA_ROUND3: All dialogues completed!")
							_phase = 3
							_wait = 0
						else:
							_sub_step = 0
							_wait = 0

		3:
			if _wait >= 10:
				_finish()
				return false

	return false

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
	print("QA_ROUND3: Finished execution. total_saved=%d errors=%d" % [_saved.size(), _errors.size()])
	for s in _saved:
		print("  SAVED: ", s)
	for e in _errors:
		print("  ERROR: ", e)
	quit(0 if _errors.is_empty() else 1)
