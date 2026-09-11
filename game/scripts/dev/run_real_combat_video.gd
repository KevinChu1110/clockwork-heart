extends SceneTree
## 錄製 10 秒真戰鬥
var _frame: int = 0
var _battle: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 4:
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game")
			gs.set("player_race", "rabbit")
			gs.set("gold", 2000)
			gs.set("weapon_tier", 3)
			gs.set("weapon_atk", 35)
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

	## 跑約 360 幀（約 12 秒）
	if _frame > 380:
		print("REAL_COMBAT_VIDEO_FINISHED")
		quit(0)

	return false
