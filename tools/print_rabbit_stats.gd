extends SceneTree

func _process(_delta: float) -> bool:
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	gs.call("reset_new_game", "rabbit")
	var inst = eq.call("roll_instance", "dawn_blade", "rare")
	var uid = str(inst.get("uid", ""))
	gs.set("weapon_loadout", [uid, "", ""])
	gs.set("weapon_loadout_active", 0)
	gs.equip_worn[uid] = inst
	gs.equip_slots["weapon"] = uid
	eq.call("_sync_legacy_weapon")
	gs.set("skill_slash_lv", 3)

	var stats = BattleSim.gather_player_stats()
	print("Gathered stats for rabbit: ", stats)
	print("inst: ", inst)
	quit(0)
	return false
