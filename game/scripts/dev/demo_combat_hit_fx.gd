extends SceneTree
## 戰鬥實機打擊錄影展示腳本（6 秒戰鬥循環，包含普攻打擊、我方受擊、暴擊爆散與格擋火花）
## 執行方式：DISPLAY=:97 godot --path game --rendering-driver opengl3 -s res://scripts/dev/demo_combat_hit_fx.gd

var _battle: Control = null
var _frame: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _setup_player() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("gold", 1500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 24)
		gs.set("weapon_name", "晨光長劍")
		gs.set("path_style", "sword")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _process(_delta: float) -> bool:
	_frame += 1

	if _frame == 2:
		_setup_player()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "road_bandit")

	elif _frame == 10:
		var f := FileAccess.open("/tmp/combat_ready_run", FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()

	# 第 1.0 秒：普攻打擊（刀光＋金屬火星＋齒輪）
	elif _frame == 35:
		if _battle != null:
			_battle.call("_set_player_pose", "attack")
			_battle.call("_set_boss_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "road_bandit", "slash_arc", 0, false)
			_battle.call("_spawn_float", "road_bandit", "-38", Color(1.0, 0.4, 0.35))

	# 第 2.5 秒：敵方還擊（我方受擊＋金屬火星＋齒輪）
	elif _frame == 80:
		if _battle != null:
			_battle.call("_set_boss_pose", "attack", true)
			_battle.call("_set_player_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "player", "slash_arc", 0, false)
			_battle.call("_spawn_float", "player", "-18", Color(1.0, 0.3, 0.3))

	# 第 4.0 秒：玩家暴擊（巨額暴擊傷害＋強烈星芒衝擊＋大量金屬火星與齒輪爆散）
	elif _frame == 130:
		if _battle != null:
			_battle.call("_set_player_pose", "attack")
			_battle.call("_set_boss_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "road_bandit", "slash_arc", 0, true)
			_battle.call("_spawn_float", "road_bandit", "CRIT! -84", Color(1.0, 0.85, 0.2), true)

	# 第 5.2 秒：格擋反擊
	elif _frame == 175:
		if _battle != null:
			_battle.call("_spawn_hit_fx", "road_bandit", "parry_flash", 0, false)
			_battle.call("_spawn_float", "road_bandit", "PARRY! -52", Color(0.3, 0.85, 1.0), true)

	# 第 6.5 秒：錄製完成退出
	elif _frame == 210:
		print("DEMO_COMBAT_HIT_FX_FINISHED")
		quit(0)
		return true

	return false
