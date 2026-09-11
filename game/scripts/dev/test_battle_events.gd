extends SceneTree

var _races := ["rabbit", "lion", "fox", "boar", "macaque"]
var _modes := {
	"rabbit": "road_bandit",
	"lion": "black_ronin",
	"fox": "fog_shade",
	"boar": "coast_raider",
	"macaque": "bamboo_spirit"
}
var _weapons := {
	"rabbit": "dawn_blade",
	"lion": "knight_pike",
	"fox": "star_rod",
	"boar": "anvil_hammer",
	"macaque": "hunt_claw"
}

var _idx := 0
var _battle: Control = null
var _sim: Object = null
var _frame := 0

func _process(_delta: float) -> bool:
	_frame += 1
	if _battle == null:
		if _idx >= _races.size():
			print("ALL RACES TESTED")
			quit(0)
			return false
		var r = _races[_idx]
		print("====================================")
		print("=== TESTING RACE: ", r, " ===")
		print("====================================")
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", r)
			gs.set("player_race", r)
			gs.set("gold", 2000)
			gs.set("weapon_tier", 3)
			gs.set("weapon_atk", 40)
			gs.call("set_flag", "c1_forged", true)
			gs.call("set_flag", "tut_done", true)
		var eq: Node = root.get_node_or_null("EquipmentSystem")
		if eq and gs:
			var inst: Dictionary = eq.call("roll_instance", _weapons[r], "rare")
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_battle.call("setup", _modes[r])
		_sim = _battle.get("sim")
		if r == "macaque" and _sim:
			var p = _sim.call("get_unit", "player")
			if p:
				p.rage = 100.0
			_sim.call("trigger_fury_awakening")

		if _sim:
			_sim.connect("event", func(kind: String, data: Dictionary):
				print("  t=%.2f [%s] %s" % [_sim.get("time"), kind, str(data)])
			)
		return false

	if _sim and _sim.get("has_ended"):
		print("  --> Battle ended at t=%.2f, victory=%s" % [_sim.get("time"), _sim.get("victory")])
		_battle.queue_free()
		_battle = null
		_sim = null
		_idx += 1
		return false

	if _sim and _sim.get("time") > 8.0:
		print("  --> Timeout at t=%.2f" % [_sim.get("time")])
		_battle.queue_free()
		_battle = null
		_sim = null
		_idx += 1
		return false

	return false
