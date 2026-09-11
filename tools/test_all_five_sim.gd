extends SceneTree

var _races = [
	{"race": "rabbit", "mode": "road_bandit", "wpn": "dawn_blade", "fury": false},
	{"race": "lion", "mode": "black_ronin", "wpn": "knight_pike", "fury": false},
	{"race": "fox", "mode": "fog_shade", "wpn": "star_rod", "fury": false},
	{"race": "boar", "mode": "coast_raider", "wpn": "anvil_hammer", "fury": false},
	{"race": "macaque", "mode": "bamboo_spirit", "wpn": "hunt_claw", "fury": true},
]
var _idx = 0
var _stage = 0
var _battle = null
var _sim = null
var _t = 0.0

func _process(delta: float) -> bool:
	if _idx >= _races.size():
		print(">>> ALL 5 RACES FINISHED!")
		quit(0)
		return false

	var rinfo = _races[_idx]
	if _stage == 0:
		var gs = root.get_node_or_null("GameState")
		var eq = root.get_node_or_null("EquipmentSystem")
		gs.call("reset_new_game", rinfo.race)
		var inst = eq.call("roll_instance", rinfo.wpn, "rare")
		var uid = str(inst.get("uid", ""))
		gs.set("weapon_loadout", [uid, "", ""])
		gs.set("weapon_loadout_active", 0)
		gs.equip_worn[uid] = inst
		gs.equip_slots["weapon"] = uid
		eq.call("_sync_legacy_weapon")
		gs.set("skill_slash_lv", 3)

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_stage = 1
		return false

	elif _stage == 1:
		_battle.call("setup", rinfo.mode)
		_sim = _battle.get("sim")
		if rinfo.fury and _sim:
			var p = _sim.get_unit("player")
			p.rage = 100.0
			_sim.trigger_fury_awakening()

		_sim.event.connect(func(kind: String, data: Dictionary):
			if kind in ["attack_swing", "hit", "battle_end"]:
				print("  [%s t=%.2f] %s: %s" % [rinfo.race, _sim.time, kind, JSON.stringify(data)])
		)
		_t = 0.0
		_stage = 2
		return false

	elif _stage == 2:
		_t += delta
		if _t >= 6.5:
			_battle.queue_free()
			_battle = null
			_sim = null
			_idx += 1
			_stage = 0
	return false
