extends SceneTree
## 靈爪猴實機戰鬥展示與錄影同步腳本 (真實戰鬥驅動，30 FPS 精確時鐘同步)

var _frame: int = 0
var _combat_frame: int = 0
var _battle: Control = null
var _sim: Object = null
var _player_unit: Object = null
var _leo_unit: Object = null

var _ready_flag: String = "/opt/side/bravesoul-game/proofs/combat_feel/combat_ready.flag"
var _sync_flag: String = "/opt/side/bravesoul-game/proofs/combat_feel/ffmpeg_started.flag"
var _is_ready: bool = false
var _has_started: bool = false

func _initialize() -> void:
	Engine.max_fps = 30
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	print(">>> INITIALIZING MACAQUE COMBAT SHOWCASE (max_fps=30)")

func _setup_macaque() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "macaque")
		gs.set("player_race", "macaque")
		gs.set("gold", 2000)
		gs.set("hp", 9999)
		gs.set("max_hp", 9999)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 50)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "hunt_claw", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _on_sim_event(kind: String, data: Dictionary) -> void:
	print("  [SIM EVENT @ f", _combat_frame, "] kind=", kind, " data=", data)

func _process(_delta: float) -> bool:
	_frame += 1

	if _battle == null and _frame >= 4:
		_setup_macaque()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
		_sim = _battle.get("sim")
		if _sim:
			_sim.connect("event", _on_sim_event)
			_sim.parts_break_unlocked = true
			_player_unit = _sim.call("get_unit", "player")
			_leo_unit = _sim.call("get_unit", "leo")
			if _player_unit:
				_player_unit.hp = 9999
				_player_unit.max_hp = 9999
				_player_unit.atk = 70
				_player_unit.atb = 0.0
			if _leo_unit:
				_leo_unit.atb = 0.0
				for p in _leo_unit.parts:
					if p.get("id") == "shield":
						p["hp"] = 10
		return false

	if _battle != null and not _is_ready and _frame >= 12:
		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		_is_ready = true
		print(">>> GODOT READY FLAG CREATED, WAITING FOR FFMPEG SYNC")

	if not _is_ready:
		return false

	if not _has_started:
		if FileAccess.file_exists(_sync_flag):
			_has_started = true
			print(">>> FFMPEG SYNC DETECTED, COMMENCING COMBAT TIMELINE")
		else:
			# 等待錄影啟動期間，凍結 ATB，保持待機
			if _player_unit:
				_player_unit.atb = 0.0
			if _leo_unit:
				_leo_unit.atb = 0.0
			return false

	_combat_frame += 1

	# 0 ~ 20 幀 (0.0s ~ 0.67s): 保持待機狀態
	if _combat_frame < 22:
		if _player_unit:
			_player_unit.atb = 0.0
		if _leo_unit:
			_leo_unit.atb = 0.0

	# 幀 22 (~0.73s): 玩家 ATB 蓄滿，自然觸發攻擊 (WINDUP -> attack_swing -> lunge & attack pose)
	if _combat_frame == 22:
		print("  [COMBAT ACTION @ f", _combat_frame, "] Player ATB full -> Trigger attack_swing")
		if _player_unit:
			_player_unit.atb = 100.0

	# 幀 105 (3.5s): 展示結束，退出
	if _combat_frame >= 105:
		print(">>> MACAQUE SHOWCASE FINISHED AT FRAME ", _combat_frame)
		quit(0)

	return false
