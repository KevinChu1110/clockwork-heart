extends SceneTree

var _battle: Control = null
var _elapsed: float = 0.0
var _real_start: float = 0.0
var _ready_flag: String = "/tmp/combat_verified_ready.flag"
var _flag_written: bool = false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	Engine.max_fps = 30

func _process(delta: float) -> bool:
	if _real_start == 0.0:
		_real_start = Time.get_ticks_msec() / 1000.0
	_elapsed += delta

	if _battle == null and _elapsed >= 0.1:
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game")
			gs.set("player_race", "rabbit")
			gs.set("gold", 2000)
			gs.set("weapon_tier", 3)
			gs.set("weapon_atk", 65)
			gs.set("speed", 25)
			gs.set("max_hp", 300)
			gs.set("hp", 300)
			gs.call("set_flag", "c1_forged", true)
			gs.call("set_flag", "tut_done", true)

		var eq: Node = root.get_node_or_null("EquipmentSystem")
		if eq and gs:
			var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
			if not inst.is_empty():
				var uid := str(inst.get("uid", ""))
				gs.set("weapon_loadout", [uid, "", ""])
				gs.set("weapon_loadout_active", 0)
				gs.equip_worn[uid] = inst
				gs.equip_slots["weapon"] = uid

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")

		if _battle.get("sim"):
			var sim = _battle.get("sim")
			sim.event.connect(func(kind: String, data: Dictionary):
				var r_now := (Time.get_ticks_msec() / 1000.0) - _real_start
				print("[COMBAT_EVENT] Game %5.2fs / Real %5.2fs: %s -> %s" % [_elapsed, r_now, kind, JSON.stringify(data)])
			)

	if _battle != null and not _flag_written and _elapsed >= 0.3:
		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		_flag_written = true
		print(">>> COMBAT SCREEN INITIALIZED AND READY")

	if _elapsed >= 10.5:
		print(">>> 10.5s COMBAT FINISHED")
		quit(0)

	return false
