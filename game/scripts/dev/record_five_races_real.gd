extends SceneTree
## 五族實機戰鬥精確抽格錄影腳本 (嚴格遵循 SHORTS_FIVE_RACES_COMBAT_18S.md 第五節與第八節)
## 每一族精準錄製 75 幀 (2.50 秒 @ 30fps)

const RACE_CONFIGS := {
	"rabbit": {
		"mode": "road_bandit",
		"weapon": "dawn_blade",
		"start_time": 2.5,
		"end_time": 5.0,
	},
	"lion": {
		"mode": "black_ronin",
		"weapon": "knight_pike",
		"start_time": 2.5,
		"end_time": 5.0,
	},
	"fox": {
		"mode": "fog_shade",
		"weapon": "star_rod",
		"start_time": 2.5,
		"end_time": 5.0,
	},
	"boar": {
		"mode": "coast_raider",
		"weapon": "anvil_hammer",
		"start_time": 2.5,
		"end_time": 5.0,
	},
	"macaque": {
		"mode": "bamboo_spirit",
		"weapon": "hunt_claw",
		"start_time": 0.8,
		"end_time": 3.3,
	}
}

var _races: Array[String] = ["rabbit", "lion", "fox", "boar", "macaque"]
var _current_idx: int = 0
var _battle: Control = null
var _sim: Object = null
var _out_base: String = "/tmp/five_races_frames"
var _recorded_frames: int = 0
var _recording: bool = false
var _init_done: bool = false

func _initialize() -> void:
	Engine.max_fps = 30
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_base)
	print(">>> INITIALIZING FIVE RACES FRAME RECORDER (1280x720 @ 30fps)")

func _setup_race(race: String, weapon_id: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", race)
		gs.set("player_race", race)
		gs.set("gold", 2000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 40)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", weapon_id, "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _start_battle() -> void:
	var race := _races[_current_idx]
	var conf: Dictionary = RACE_CONFIGS[race]
	var mode: String = conf["mode"]
	var weapon: String = conf["weapon"]
	
	var r_dir := _out_base.path_join(race)
	DirAccess.make_dir_recursive_absolute(r_dir)
	
	_setup_race(race, weapon)
	_recorded_frames = 0
	_recording = false
	
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", mode)
	
	_sim = _battle.get("sim")
	if race == "macaque" and _sim:
		var p = _sim.call("get_unit", "player")
		if p:
			p.rage = 100.0
		_sim.trigger_fury_awakening()
		print("  [MACAQUE] Fury awakening triggered at start!")
	
	print(">>> STARTED BATTLE FOR: ", race, " (mode: ", mode, ", weapon: ", weapon, ")")

func _process(_delta: float) -> bool:
	if not _init_done:
		_init_done = true
		_start_battle()
		return false
	
	if _battle == null or _sim == null:
		return false
	
	var race := _races[_current_idx]
	var conf: Dictionary = RACE_CONFIGS[race]
	var start_t: float = conf["start_time"]
	var cur_sim_t: float = _sim.get("time") if _sim else 0.0
	
	if cur_sim_t >= start_t and not _recording:
		_recording = true
		print("  >>> START RECORDING FOR ", race, " at sim.time = ", cur_sim_t)
	
	if _recording:
		if _recorded_frames < 75:
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var frame_path := _out_base.path_join(race).path_join("frame_%04d.png" % _recorded_frames)
				img.save_png(frame_path)
			_recorded_frames += 1
		else:
			print("  >>> FINISHED RECORDING 75 FRAMES FOR ", race, " at sim.time = ", cur_sim_t)
			_battle.queue_free()
			_battle = null
			_sim = null
			_current_idx += 1
			if _current_idx < _races.size():
				_start_battle()
			else:
				print(">>> ALL 5 RACES RECORDED SUCCESSFULLY (75 frames each)!")
				quit(0)
	
	return false
