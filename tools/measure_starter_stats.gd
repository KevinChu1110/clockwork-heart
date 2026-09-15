extends SceneTree

func _process(_delta: float) -> bool:
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gs == null or eq == null:
		print("Waiting for autoloads...")
		return false

	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	print("=== STARTER WEAPONS & STATS BEFORE/AFTER ===")
	for r in races:
		gs.call("reset_new_game", r)
		var stats: Dictionary = BattleSim.gather_player_stats()
		var wuid: String = str(gs.equip_slots.get("weapon", ""))
		var winst: Dictionary = gs.equip_worn.get(wuid, {})
		var base_id: String = str(winst.get("base_id", ""))
		var tier: int = int(winst.get("tier", 0))
		var w_name: String = str(winst.get("name", ""))
		var w_atk: int = int(winst.get("rolled", {}).get("atk", 0))
		var eff_atk: int = int(stats.get("atk", 0))
		print("%s | weapon=%s (%s, T%d, w_atk=%d) | eff_atk=%d | full_stats: hp=%d def=%d spd=%d" % [
			r, base_id, w_name, tier, w_atk, eff_atk,
			int(stats.get("hp", 0)), int(stats.get("def", 0)), int(stats.get("speed", 0))
		])
	quit(0)
	return false
