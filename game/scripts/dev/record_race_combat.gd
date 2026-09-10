extends SceneTree
## 單族實機戰鬥精確抽格錄影腳本 (接收 TARGET_RACE 環境變數)
## 嚴格遵循 SHORTS_FIVE_RACES_COMBAT_18S.md 與 review.md 規範
## 配合 --fixed-fps 30 確保逐幀物理時間 100% 穩定，精準對齊打擊幀

const RACE_CONFIGS := {
	"rabbit": {
		"mode": "road_bandit",
		"weapon": "dawn_blade",
		"start_time": 3.067,
	},
	"lion": {
		"mode": "black_ronin",
		"weapon": "knight_pike",
		"start_time": 3.000,
	},
	"fox": {
		"mode": "fog_shade",
		"weapon": "star_rod",
		"start_time": 3.033,
	},
	"boar": {
		"mode": "coast_raider",
		"weapon": "anvil_hammer",
		"start_time": 3.300,
	},
	"macaque": {
		"mode": "bamboo_spirit",
		"weapon": "hunt_claw",
		"start_time": 1.400,
	}
}

var _race: String = "rabbit"
var _battle: Control = null
var _sim: Object = null
var _out_dir: String = ""
var _recorded_frames: int = 0
var _recording: bool = false
var _init_done: bool = false
var _frame_count: int = 0

func _initialize() -> void:
	Engine.max_fps = 30
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	
	var env_race := OS.get_environment("TARGET_RACE")
	if env_race in RACE_CONFIGS:
		_race = env_race
	
	var env_out := OS.get_environment("OUT_FRAMES_DIR")
	if env_out != "":
		_out_dir = env_out.path_join(_race)
	else:
		_out_dir = ProjectSettings.globalize_path("res://../proofs/five_races_frames").path_join(_race)
	DirAccess.make_dir_recursive_absolute(_out_dir)
	print(">>> INITIALIZING FRAME RECORDER FOR RACE: ", _race, " -> ", _out_dir)

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
	var conf: Dictionary = RACE_CONFIGS[_race]
	var mode: String = conf["mode"]
	var weapon: String = conf["weapon"]
	
	_setup_race(_race, weapon)
	_recorded_frames = 0
	_recording = false
	
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	if _battle.has_method("setup"):
		_battle.call("setup", mode)
	
	_sim = _battle.get("sim")
	if _sim:
		# 關鍵改進：確保敵方生命值充沛 (500 HP)，防止 1 擊秒殺導致跳入勝利結算畫面 (勝 利)！
		# 遵守 review.md 第 19i 條與總監退稿意見：「不准用勝利結算畫面充當打擊鏡頭」
		var enemy = _sim.call("get_unit", mode)
		if enemy:
			enemy.hp = 500
			enemy.max_hp = 500
	
	if _race == "macaque" and _sim:
		var p = _sim.call("get_unit", "player")
		if p:
			p.rage = 100.0
		_sim.call("trigger_fury_awakening")
		print("  [MACAQUE] Fury awakening triggered!")
	
	print(">>> BATTLE STARTED FOR: ", _race, " (mode: ", mode, ", weapon: ", weapon, ")")

func _process(_delta: float) -> bool:
	_frame_count += 1
	if not _init_done:
		if _frame_count >= 3:
			_init_done = true
			_start_battle()
		return false
	
	if _battle == null or _sim == null:
		return false
	
	var conf: Dictionary = RACE_CONFIGS[_race]
	var start_t: float = conf["start_time"]
	var cur_sim_t: float = _sim.get("time") if _sim else 0.0
	
	if cur_sim_t >= start_t and not _recording:
		_recording = true
		print("  >>> START RECORDING FOR ", _race, " at sim.time = ", cur_sim_t, " (frame ", _frame_count, ")")
	
	if _recording:
		if _recorded_frames < 75:
			var img := root.get_viewport().get_texture().get_image()
			if img and not img.is_empty():
				var frame_path := _out_dir.path_join("frame_%04d.png" % _recorded_frames)
				var err := img.save_png(frame_path)
				if err != OK:
					printerr("save_png failed: ", err)
			_recorded_frames += 1
		else:
			print("  >>> FINISHED RECORDING 75 FRAMES FOR ", _race, " at sim.time = ", cur_sim_t)
			quit(0)
	
	return false
