extends SceneTree
## REC-03 聚魂殿四階封靈罐開光與首屏透明保底
## 時長: 5.0s (由握手信號觸發錄製)
## 展示: 去 Emoji 現代 UI、四階金屬封靈罐(綠藍紫橙)、首屏 60/100 虔誠度透明保底進度條、抽魂開光

var _elapsed: float = 0.0
var _step_timer: float = 0.0
var _main: Node = null
var _step: int = 0
var _ready_written: bool = false
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _saved_png: bool = false
var _out_dir: String = ""
var _ready_file: String = ""
var _start_file: String = ""

const ID: String = "rec03_soul_pity"
const TOTAL_DURATION: float = 5.0

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
			if current_scene != null and current_scene.has_method("_go_soul_panel"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var ss: Node = root.get_node_or_null("SoulSystem")
				if gs and ss:
					gs.call("reset_new_game")
					gs.set("gold", 1500)
					gs.set("stardust", 12)
					gs.set("weapon_tier", 2)
					gs.call("set_flag", "soul.piety", 60)
					gs.call("set_flag", "soul.shards", 4)
					ss.call("ensure_slots")
					ss.call("grant_starter_soul")
					_main.call("_go_soul_panel")
					_step = 1
					_step_timer = 0.0
					print("REC03_SOUL_PANEL_OPENED at ", _elapsed)
		1:
			_step_timer += delta
			# 讓聚魂殿畫面繪製並完全穩定
			if _step_timer >= 1.0 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("REC03_READY_FOR_RECORDING written at elapsed=", _elapsed)

			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 2
				_rec_elapsed = 0.0
				print("REC03_RECORDING_STARTED at elapsed=", _elapsed)
		2:
			_rec_elapsed += delta
			# +1.8s: 執行抽魂
			if _rec_elapsed >= 1.8 and _step == 2:
				if _main and _main.has_method("_soul_do_ritual"):
					_main.call("_soul_do_ritual")
				print("REC03_RITUAL_TRIGGERED at rec_elapsed=", _rec_elapsed)
				_step = 3
		3:
			_rec_elapsed += delta
			# +3.5s: 保存關鍵幀截圖
			if _rec_elapsed >= 3.5 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec03_soul_pity.png")
			# +5.0s: 錄影結束
			if _rec_elapsed >= TOTAL_DURATION:
				print("REC03_DONE at rec_elapsed=", _rec_elapsed)
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
