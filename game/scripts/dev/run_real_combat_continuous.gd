extends SceneTree
## 8~12 秒真實連續戰鬥演出錄影腳本

var _frame: int = 0
var _combat_frame: int = 0
var _battle: Control = null
var _ready_flag: String = "/tmp/combat_continuous_ready.flag"
var _is_ready: bool = false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _setup_player() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", "rabbit")
		gs.set("gold", 2000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 55)
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

func _process(_delta: float) -> bool:
	_frame += 1

	if _battle == null and _frame >= 4:
		_setup_player()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
		return false

	if _battle != null and not _is_ready and _frame >= 10:
		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		_is_ready = true
		print(">>> CONTINUOUS COMBAT SCREEN READY")

	if not _is_ready:
		return false

	_combat_frame += 1

	## 第 1 次出招攻擊 (約 1.2s，第 36 幀)
	if _combat_frame == 36:
		print("  [COMBAT] Round 1: Lunge & Attack")
		if _battle and _battle.has_method("_lunge"):
			_battle.call("_lunge", "player")
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)

	## 第 1 次命中與傷害跳字 (約 1.5s，第 45 幀)
	if _combat_frame == 45:
		print("  [COMBAT] Round 1: Damage Hit (188)")
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "188", Color(1.0, 0.4, 0.35))
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "slash_arc")

	## 第 2 次出招攻擊 (約 3.5s，第 105 幀)
	if _combat_frame == 105:
		print("  [COMBAT] Round 2: Lunge & Attack")
		if _battle and _battle.has_method("_lunge"):
			_battle.call("_lunge", "player")
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)

	## 第 2 次命中與暴擊跳字 (約 3.8s，第 114 幀)
	if _combat_frame == 114:
		print("  [COMBAT] Round 2: Critical Hit (256!)")
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "256", Color(1.0, 0.85, 0.2), true)
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "slash_arc")

	## 第 3 次出招 + 部位破壞 BREAK！(約 6.0s，第 180 幀)
	if _combat_frame == 180:
		print("  [COMBAT] Round 3: Lunge & Break")
		if _battle and _battle.has_method("_lunge"):
			_battle.call("_lunge", "player")
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)

	## 部位破壞跳字在身邊爆發 (約 6.3s，第 190 幀)
	if _combat_frame == 190:
		print("  [COMBAT] Round 3: Part Break BREAK!")
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "BREAK！獅衛重盾", Color(1.0, 0.85, 0.15), false, true)
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "parry_flash")

	## 跑滿 300 幀 (約 10 秒)
	if _combat_frame >= 300:
		print(">>> 10-SECOND CONTINUOUS COMBAT COMPLETE!")
		quit(0)

	return false
