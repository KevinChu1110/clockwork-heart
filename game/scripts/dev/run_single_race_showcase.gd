extends SceneTree
## 單種族真實戰鬥展示腳本（支援 ready 訊號）

var _frame: int = 0
var _combat_frame: int = 0
var _battle: Control = null
var _race: String = "rabbit"
var _ready_flag: String = "/tmp/combat_ready.flag"
var _is_ready: bool = false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var env_race := OS.get_environment("TARGET_RACE")
	if env_race != "":
		_race = env_race
	print(">>> INITIALIZING COMBAT SHOWCASE FOR: ", _race)

func _setup_race(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", race)
		gs.set("gold", 2000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 50)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var wpn_id := "dawn_blade"
		match race:
			"rabbit": wpn_id = "dawn_blade"
			"lion": wpn_id = "knight_pike"
			"fox": wpn_id = "star_rod"
			"boar": wpn_id = "anvil_hammer"
			"macaque": wpn_id = "hunt_claw"
		var inst: Dictionary = eq.call("roll_instance", wpn_id, "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _process(_delta: float) -> bool:
	_frame += 1

	if _battle == null and _frame >= 4:
		_setup_race(_race)
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
		return false

	if _battle != null and not _is_ready and _frame >= 10:
		## 戰鬥畫面已完全就緒，發出 ready 訊號
		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		_is_ready = true
		print(">>> COMBAT SCREEN READY: ", _race)

	if not _is_ready:
		return false

	_combat_frame += 1

	## 0.0s ~ 1.0s: 靜態待機 (Idle)
	## 1.0s (第 30 幀): 觸發攻擊位移與攻擊姿態 (Lunge + Attack Pose)
	if _combat_frame == 30:
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)
		if _battle and _battle.has_method("_lunge"):
			_battle.call("_lunge", "player")
		print("  [COMBAT ACTION] Player Lunge & Attack Pose triggered")

	## 1.5s (第 45 幀): 突進到最前線命中，跳出傷害數字與打擊特效
	if _combat_frame == 45:
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "188", Color(1.0, 0.4, 0.35))
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "slash_arc")
		print("  [COMBAT ACTION] Hit damage float & FX triggered")

	## 2.2s (第 66 幀): 部位破壞 BREAK 在敵人身邊跳出
	if _combat_frame == 66:
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "BREAK！獅衛重盾", Color(1.0, 0.85, 0.15), false, true)
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "parry_flash")
		print("  [COMBAT ACTION] Part Break BREAK triggered")

	## 3.2s (第 96 幀): 完成展示
	if _combat_frame >= 105:
		print("SHOWCASE_FINISHED_FOR: ", _race)
		quit(0)

	return false
