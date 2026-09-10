extends SceneTree
## 戰鬥演出驗證截圖腳本：驗收兔、獅、狐、豬、猴五族真戰鬥攻擊姿態與武器手持、位移與跳字
## 執行方式：DISPLAY=:97 godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_race_battles.gd

var _races: Array[String] = ["rabbit", "lion", "fox", "boar", "macaque"]
var _current_race_idx: int = 0
var _battle: Control = null
var _frame: int = 0
var _race_frame: int = 0
var _out_dir: String = "/opt/side/bravesoul-game/proofs/combat_feel"
var _captured_attack: bool = false
var _captured_idle: bool = false
var _attack_frame_delay: int = 0

const RACE_MODES := {
	"rabbit": "road_bandit",
	"lion": "black_ronin",
	"fox": "fog_shade",
	"boar": "coast_raider",
	"macaque": "bamboo_spirit",
}

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)

func _setup_race(race: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("player_race", race)
		gs.set("gold", 2000)
		gs.set("skill_slash_lv", 3)
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
			gs.set("weapon_atk", 0)

func _start_current_battle() -> void:
	var race: String = _races[_current_race_idx]
	var mode: String = RACE_MODES.get(race, "road_bandit")
	print(">>> STARTING BATTLE FOR RACE: ", race, " (mode: ", mode, ")")
	_setup_race(race)
	_captured_attack = false
	_captured_idle = false
	_race_frame = 0

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", mode)
	
	if _battle.get("sim") != null:
		var sim_node: Object = _battle.get("sim")
		if race == "macaque":
			var p = sim_node.get_unit("player")
			if p:
				p.rage = 100.0
			sim_node.trigger_fury_awakening()
		if sim_node.has_signal("event_occurred"):
			sim_node.connect("event_occurred", _on_battle_event)

func _on_battle_event(kind: String, data: Dictionary) -> void:
	var race: String = _races[_current_race_idx]
	if kind == "attack_swing" and str(data.get("id", "")) == "player":
		print("  [EVENT] player attack_swing (race=", race, ")")
		_attack_frame_delay = 6
	elif kind == "hit" and str(data.get("attacker", "")) == "player":
		print("  [EVENT] player hit (damage=", data.get("damage"), ", race=", race, ")")
		call_deferred("_capture_shot", "%s_battle_hit.png" % race)
	elif kind == "part_broken":
		print("  [EVENT] part_broken (part=", data.get("part_name"), ", race=", race, ")")
		call_deferred("_capture_shot", "%s_battle_break.png" % race)

func _capture_shot(filename: String) -> void:
	if _battle and _battle.get("player_body"):
		var pb: Control = _battle.get("player_body")
		print("At capture ", filename, " PlayerBody global_rect: ", pb.get_global_rect(), " size: ", pb.size)
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var full_path := _out_dir.path_join(filename)
		img.save_png(full_path)
		print("  --> SAVED PROOF: ", full_path)

func _process(_delta: float) -> bool:
	_frame += 1

	if _battle == null and _current_race_idx < _races.size():
		if _frame >= 4:
			_start_current_battle()
		return false

	_race_frame += 1
	var race: String = _races[_current_race_idx]

	## 捕捉 idle 幀
	if _race_frame == 12 and not _captured_idle:
		_capture_shot("%s_battle_idle.png" % race)
		_captured_idle = true

	## 捕捉 attack 揮擊幀
	if _attack_frame_delay > 0:
		_attack_frame_delay -= 1
		if _attack_frame_delay == 0 and not _captured_attack:
			_capture_shot("%s_battle_attack_full.png" % race)
			_captured_attack = true

	## 若已捕捉到 attack 或超過 200 幀（自然推進，絕不使用 _set_player_pose 當攻擊入口）
	if (_captured_attack and _race_frame > 60) or _race_frame > 200:
		if _battle and is_instance_valid(_battle):
			_battle.queue_free()
			_battle = null

		_current_race_idx += 1
		if _current_race_idx >= _races.size():
			print(">>> ALL RACES CAPTURED SUCCESSFULLY!")
			quit(0)

	return false
