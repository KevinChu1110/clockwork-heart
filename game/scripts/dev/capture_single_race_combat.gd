extends SceneTree
## 單種族真實戰鬥錄影驅動腳本
## 由環境變數 TARGET_RACE 指定種族（rabbit/lion/fox/boar/macaque）

var _race: String = "rabbit"
var _battle: Control = null
var _sim = null
var _stage: int = 0
var _ready_flag: String = "/root/tmp_workspace/race_ready.flag"
var _sim_elapsed: float = 0.0
var _ended_timer: float = 0.0
var _is_ended: bool = false

const RACE_CONFIG = {
	"rabbit": {"mode": "road_bandit", "wpn": "dawn_blade", "fury": false},
	"lion": {"mode": "black_ronin", "wpn": "knight_pike", "fury": false},
	"fox": {"mode": "fog_shade", "wpn": "star_rod", "fury": false},
	"boar": {"mode": "coast_raider", "wpn": "anvil_hammer", "fury": false},
	"macaque": {"mode": "bamboo_spirit", "wpn": "hunt_claw", "fury": true},
}

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	Engine.max_fps = 30
	var env_race := OS.get_environment("TARGET_RACE").strip_edges().to_lower()
	if env_race in RACE_CONFIG:
		_race = env_race
	print(">>> [CAPTURE] Initializing combat recording for: ", _race)

func _process(delta: float) -> bool:
	if _stage == 0:
		var cfg = RACE_CONFIG[_race]
		print(">>> [CAPTURE] Setup GameState for %s (wpn=%s, mode=%s)" % [_race, cfg.wpn, cfg.mode])
		var gs: Node = root.get_node_or_null("GameState")
		if gs:
			gs.call("reset_new_game", _race)
			gs.set("player_race", _race)
			gs.set("gold", 2000)
			gs.set("weapon_atk", 0)
			gs.set("skill_slash_lv", 3)

		var eq: Node = root.get_node_or_null("EquipmentSystem")
		if eq and gs:
			var inst: Dictionary = eq.call("roll_instance", cfg.wpn, "rare")
			if inst.is_empty():
				printerr("ERROR: roll_instance failed for: ", cfg.wpn)
			else:
				var uid := str(inst.get("uid", ""))
				gs.set("weapon_loadout", [uid, "", ""])
				gs.set("weapon_loadout_active", 0)
				gs.equip_worn[uid] = inst
				gs.equip_slots["weapon"] = uid
				gs.set("weapon_atk", 0)
				print(">>> [CAPTURE] Equipped %s uid=%s" % [cfg.wpn, uid])

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		_stage = 1
		return false

	elif _stage == 1:
		var cfg = RACE_CONFIG[_race]
		_battle.call("setup", cfg.mode)
		_sim = _battle.get("sim")

		if cfg.fury and _sim:
			var p = _sim.get_unit("player")
			p.rage = 100.0
			_sim.trigger_fury_awakening()
			print(">>> [CAPTURE] Triggered fury awakening for macaque")

		if _sim:
			_sim.event.connect(func(kind: String, data: Dictionary):
				print(">>> [EVENT t=%.2f] kind=%s, data=%s" % [_sim.time, kind, JSON.stringify(data)])
				if kind == "battle_end":
					_is_ended = true
			)

		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		print(">>> [CAPTURE] Ready flag written, combat simulation started!")
		_sim_elapsed = 0.0
		_stage = 2
		return false

	elif _stage == 2:
		_sim_elapsed += delta
		if _is_ended:
			_ended_timer += delta
			if _ended_timer >= 1.5:
				print(">>> [CAPTURE] Finished recording after battle_end at sim_elapsed=%.2f" % _sim_elapsed)
				quit(0)
		elif _sim_elapsed >= 7.0:
			print(">>> [CAPTURE] Finished recording window at sim_elapsed=%.2f" % _sim_elapsed)
			quit(0)
	return false
