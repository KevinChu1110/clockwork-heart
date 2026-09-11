extends SceneTree

var _races = [
	{"race": "rabbit", "mode": "road_bandit", "wpn": "dawn_blade", "fury": false},
	{"race": "lion", "mode": "black_ronin", "wpn": "knight_pike", "fury": false},
	{"race": "fox", "mode": "fog_shade", "wpn": "star_rod", "fury": false},
	{"race": "boar", "mode": "coast_raider", "wpn": "anvil_hammer", "fury": false},
	{"race": "macaque", "mode": "bamboo_spirit", "wpn": "hunt_claw", "fury": true},
]
var _idx = 0
var _battle: Control = null
var _sim = null
var _stage = 0
var _time = 0.0

func _initialize() -> void:
	print(">>> STARTING FIVE RACES SIM TEST")

func _process(delta: float) -> bool:
	if _idx >= _races.size():
		print(">>> ALL RACES SIM TEST COMPLETED")
		quit(0)
		return false

	var rinfo = _races[_idx]
	if _stage == 0:
		print("\n--- Testing: %s (%s, %s) ---" % [rinfo.race, rinfo.mode, rinfo.wpn])
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game")
			gs.set("player_race", rinfo.race)
			gs.set("gold", 2000)
			gs.set("weapon_tier", 3)
			gs.set("weapon_atk", 40)
			gs.call("set_flag", "c1_forged", true)
			gs.call("set_flag", "tut_done", true)
			gs.set("skill_slash_lv", 3)
		
		var eq: Node = root.get_node_or_null("EquipmentSystem")
		if eq and gs:
			var inst: Dictionary = eq.call("roll_instance", rinfo.wpn, "rare")
			if inst.is_empty():
				print("ERROR: roll_instance returned empty for ", rinfo.wpn)
			else:
				var uid := str(inst.get("uid", ""))
				gs.set("weapon_loadout", [uid, "", ""])
				gs.set("weapon_loadout_active", 0)
				gs.equip_worn[uid] = inst
				gs.equip_slots["weapon"] = uid
				print("Equipped %s (uid=%s)" % [rinfo.wpn, uid])

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_stage = 1
		return false

	elif _stage == 1:
		# Now battle is in tree and _ready has run
		_battle.call("setup", rinfo.mode)
		_sim = _battle.get("sim")
		if rinfo.fury and _sim:
			var p = _sim.get_unit("player")
			p.rage = 100.0
			_sim.trigger_fury_awakening()
			print("Triggered fury awakening for macaque")
		
		if _sim:
			_sim.event.connect(func(kind: String, data: Dictionary):
				print("  [SIM EVENT t=%.2f] kind=%s, data=%s" % [_sim.time, kind, JSON.stringify(data)])
			)
		_time = 0.0
		_stage = 2
		return false

	elif _stage == 2:
		_time += delta
		if _time >= 5.5:
			if _battle:
				_battle.queue_free()
				_battle = null
			_sim = null
			_idx += 1
			_stage = 0
	return false
