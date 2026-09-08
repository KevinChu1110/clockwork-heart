extends SceneTree
## REC-04 怒氣滿額暴怒覺醒與高速連斬
## 時長: 6.5s (由握手信號觸發錄製)
## 展示: 怒氣滿額觸發「暴怒覺醒！」跳字＋三連斬擊命中雷歐（受擊閃紅與傷害跳字）

var _elapsed: float = 0.0
var _step_timer: float = 0.0
var _main: Node = null
var _battle: Control = null
var _sim = null
var _step: int = 0
var _ready_written: bool = false
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _saved_png: bool = false
var _out_dir: String = ""
var _ready_file: String = ""
var _start_file: String = ""

const ID: String = "rec04_overdrive_break"
const TOTAL_DURATION: float = 6.5

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws == "":
		ws = "/tmp"
	_ready_file = ws.path_join(ID + ".ready")
	_start_file = ws.path_join(ID + ".start")
	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			if current_scene != null and current_scene.has_method("_start_battle_raw"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.call("set_flag", "c0_first_battle", true)
					gs.set("level", 30)
					_main.call("_start_battle_raw", "leo")
					_step = 1
					print("REC04_BATTLE_STARTED at ", _elapsed)
		1:
			var host: Node = _main.get("host") if _main else null
			if host and host.get_child_count() > 0:
				_battle = host.get_child(host.get_child_count() - 1) as Control
				if _battle and _battle.is_inside_tree():
					_sim = _battle.get("sim")
					if _sim:
						_sim.set("hazard_kind", "")
					_step = 2
					_step_timer = 0.0
					print("REC04_BATTLE_NODE_READY at ", _elapsed)
		2:
			_step_timer += delta
			# 讓畫面渲染幾幀穩定
			if _step_timer >= 1.0 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("REC04_READY_FOR_RECORDING written at elapsed=", _elapsed)

			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 3
				_rec_elapsed = 0.0
				print("REC04_RECORDING_STARTED at elapsed=", _elapsed)
		3:
			_rec_elapsed += delta
			# +1.0s: 怒氣滿 100% 並觸發暴怒覺醒
			if _rec_elapsed >= 1.0 and _step == 3:
				if _sim:
					var p = _sim.call("get_unit", "player")
					if p:
						p.set("rage", 100.0)
						p.set("crit", 100.0)
						_sim.call("trigger_fury_awakening")
						print("REC04_FURY_AWAKENING_TRIGGERED at rec_elapsed=", _rec_elapsed)
				_step = 4
		4:
			_rec_elapsed += delta
			# +2.0s: 暴怒連斬第 1 擊
			if _rec_elapsed >= 2.0 and _step == 4:
				if _sim:
					var p = _sim.call("get_unit", "player")
					var leo = _sim.call("get_unit", "leo")
					if leo:
						leo.set("atb", 0.0)
					if p:
						p.set("state", 0)
						_sim.call("_begin_attack", p)
						print("REC04_ATTACK_1 at rec_elapsed=", _rec_elapsed)
				_step = 5
		5:
			_rec_elapsed += delta
			# +3.2s: 暴怒連斬第 2 擊
			if _rec_elapsed >= 3.2 and _step == 5:
				if _sim:
					var p = _sim.call("get_unit", "player")
					var leo = _sim.call("get_unit", "leo")
					if leo:
						leo.set("atb", 0.0)
					if p:
						p.set("state", 0)
						_sim.call("_begin_attack", p)
						print("REC04_ATTACK_2 at rec_elapsed=", _rec_elapsed)
				_step = 6
		6:
			_rec_elapsed += delta
			# +4.4s: 暴怒連斬第 3 擊
			if _rec_elapsed >= 4.4 and _step == 6:
				if _sim:
					var p = _sim.call("get_unit", "player")
					var leo = _sim.call("get_unit", "leo")
					if leo:
						leo.set("atb", 0.0)
					if p:
						p.set("state", 0)
						_sim.call("_begin_attack", p)
						print("REC04_ATTACK_3 at rec_elapsed=", _rec_elapsed)
				_step = 7
		7:
			_rec_elapsed += delta
			# +5.2s: 保存關鍵幀截圖
			if _rec_elapsed >= 5.2 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec04_overdrive_break.png")
			# +6.5s: 錄影結束
			if _rec_elapsed >= TOTAL_DURATION:
				print("REC04_DONE at rec_elapsed=", _rec_elapsed)
				quit(0)
				return true
	return false

func _save_screenshot(filename: String) -> void:
	var tex: ViewportTexture = root.get_texture()
	var img: Image = tex.get_image() if tex else null
	if img:
		var p1 := _out_dir.path_join(filename)
		img.save_png(p1)
		print("SAVED_SCREENSHOT: ", p1)
		var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
		if ws != "":
			DirAccess.make_dir_recursive_absolute(ws)
			img.save_png(ws.path_join(filename))
			print("SAVED_WORKSPACE: ", ws.path_join(filename))
