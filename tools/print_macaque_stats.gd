extends SceneTree

var _stage = 0
var _battle = null
var _sim = null

func _process(delta: float) -> bool:
	if _stage == 0:
		var gs = root.get_node_or_null("GameState")
		var eq = root.get_node_or_null("EquipmentSystem")
		gs.call("reset_new_game", "macaque")
		var inst = eq.call("roll_instance", "hunt_claw", "rare")
		var uid = str(inst.get("uid", ""))
		gs.set("weapon_loadout", [uid, "", ""])
		gs.set("weapon_loadout_active", 0)
		gs.equip_worn[uid] = inst
		gs.equip_slots["weapon"] = uid
		gs.set("skill_slash_lv", 3)

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_stage = 1
		return false
	elif _stage == 1:
		_battle.call("setup", "bamboo_spirit")
		_sim = _battle.get("sim")
		var p = _sim.get_unit("player")
		var b = _sim.get_unit("bamboo_spirit")
		print("Player atk:", p.atk, " armed_atk:", p.armed_atk, " weapon_class:", p.weapon_class)
		print("Bamboo spirit hp:", b.max_hp, " def:", b.defense, " atk:", b.atk)
		p.rage = 100.0
		_sim.trigger_fury_awakening()
		print("After fury awakening: player atk:", p.atk, " atk_buff_mult:", p.atk_buff_mult)
		quit(0)
	return false
