extends SceneTree

var _race := "lion"

func _initialize() -> void:
	var env_race := OS.get_environment("TARGET_RACE")
	if env_race != "":
		_race = env_race
	print("=== TESTING RACE: ", _race, " ===")

var _battle: Control = null
var _sim: Object = null
var _frame := 0

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

func _process(_delta: float) -> bool:
	_frame += 1
	if _battle == null and _frame >= 3:
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", _race)
			gs.set("player_race", _race)
			gs.set("gold", 2000)
			gs.set("weapon_tier", 3)
			gs.set("weapon_atk", 40)
			gs.call("set_flag", "c1_forged", true)
			gs.call("set_flag", "tut_done", true)
		var eq: Node = root.get_node_or_null("EquipmentSystem")
		if eq and gs:
			var inst: Dictionary = eq.call("roll_instance", _weapons[_race], "rare")
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_battle.call("setup", _modes[_race])
		_sim = _battle.get("sim")
		if _race == "macaque" and _sim:
			var p = _sim.call("get_unit", "player")
			if p:
				p.rage = 100.0
			_sim.call("trigger_fury_awakening")

		if _sim:
			_sim.connect("event", func(kind: String, data: Dictionary):
				print("  t=%.2f [%s] %s" % [_sim.get("time"), kind, str(data)])
			)
		return false

	if _sim:
		if _sim.get("has_ended") or _sim.get("time") >= 6.0:
			print("FINISHED at t=%.2f, ended=%s, victory=%s" % [_sim.get("time"), _sim.get("has_ended"), _sim.get("victory")])
			quit(0)
			return false

	return false
