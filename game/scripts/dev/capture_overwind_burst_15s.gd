extends SceneTree
## 《發條之心》短影音 15 秒實機錄影驅動腳本：發條超載爆裂（Overwind Burst）
## 時長：精確 15.0 秒（由握手信號觸發錄影）
## 內容：第 0 秒開局直接滿怒爆發「發條超載爆裂」暗角＋齒輪噴發＋金色星芒火花＋連續疾速斬擊

var _elapsed: float = 0.0
var _battle: Control = null
var _sim = null
var _step: int = 0
var _ready_written: bool = false
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _ready_file: String = ""
var _start_file: String = ""

const ID: String = "overwind_burst_15s"
const TOTAL_DURATION: float = 15.2

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws == "":
		ws = "/tmp"
	_ready_file = ws.path_join(ID + ".ready")
	_start_file = ws.path_join(ID + ".start")

	var loc := root.get_node_or_null("Loc")
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.call("set_flag", "c0_first_battle", true)
		gs.set("player_name", "小白")
		gs.set("player_race", "rabbit")
		gs.set("level", 20)

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)
	_step = 0

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			# 初始化戰鬥（對陣合規合金玩具狼 wolf）
			_battle.call("setup", "wolf")
			_sim = _battle.get("sim")
			if _sim:
				_sim.set("hazard_kind", "")
				var p = _sim.call("get_unit", "player")
				if p:
					p.set("rage", 100.0)
					p.set("crit", 80.0)
			_step = 1
		1:
			# 等待渲染平穩
			if _elapsed >= 0.8 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("OVERWIND_15S_READY written at ", _elapsed)

			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 2
				_rec_elapsed = 0.0
				print("OVERWIND_15S_RECORDING_STARTED at ", _elapsed)
		2:
			_rec_elapsed += delta

			# 0.0s~0.1s: 開局第 0 秒直接引爆「發條超載爆裂」
			if _rec_elapsed >= 0.05 and _step == 2:
				_battle.set("_last_overwind_burst_msec", -99999)
				_battle.call("trigger_overwind_burst", "hook_opener")
				print("--> 0.05s: Overwind Burst Hook Triggered!")
				_step = 3
		3:
			_rec_elapsed += delta

			# 1.5s: 連斬第 1 擊（暴擊斬擊）
			if _rec_elapsed >= 1.5 and _step == 3:
				if _battle.has_method("_flash"):
					_battle.call("_flash", _battle.get("player_body"), Color(2.5, 2.0, 1.0))
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "enemy", "CRIT 48", Color(1.0, 0.85, 0.1), true)
				_battle.set("_shake", 0.25)
				_step = 4
		4:
			_rec_elapsed += delta

			# 3.2s: 連斬第 2 擊（高速破甲）
			if _rec_elapsed >= 3.2 and _step == 4:
				if _battle.has_method("_flash"):
					_battle.call("_flash", _battle.get("enemy_body"), Color(2.0, 1.5, 1.0))
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "enemy", "CRIT 52", Color(1.0, 0.85, 0.1), true)
				_battle.set("_shake", 0.3)
				_step = 5
		5:
			_rec_elapsed += delta

			# 5.5s: 蓄力迴轉斬＋齒輪火花次波噴射
			if _rec_elapsed >= 5.5 and _step == 5:
				_battle.set("_last_overwind_burst_msec", -99999)
				_battle.call("trigger_overwind_burst", "combo_surge")
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "player", "轉數極限！", Color(0.2, 0.9, 1.0), true)
					_battle.call("_spawn_float", "enemy", "CRIT 68", Color(1.0, 0.85, 0.1), true)
				_step = 6
		6:
			_rec_elapsed += delta

			# 8.0s: 第三連擊爆散
			if _rec_elapsed >= 8.0 and _step == 6:
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "enemy", "BREAK!", Color(1.0, 0.4, 0.2), true)
				_battle.set("_shake", 0.35)
				_step = 7
		7:
			_rec_elapsed += delta

			# 10.5s: 終結重擊，數值狂飆
			if _rec_elapsed >= 10.5 and _step == 7:
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "enemy", "OVERWIND CRIT 99", Color(1.0, 0.9, 0.1), true)
				_battle.set("_shake", 0.4)
				_step = 8
		8:
			_rec_elapsed += delta

			# 13.0s: 勝利定格，戰意結算
			if _rec_elapsed >= 13.0 and _step == 8:
				if _battle.has_method("_spawn_float"):
					_battle.call("_spawn_float", "player", "戰鬥完勝", Color(0.3, 1.0, 0.4), true)
				_step = 9
		9:
			_rec_elapsed += delta
			if _rec_elapsed >= TOTAL_DURATION:
				print("OVERWIND_15S_COMPLETED at rec_elapsed=", _rec_elapsed)
				quit(0)
				return true

	return false
