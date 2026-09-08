extends SceneTree
## REC-02 視覺換血（粗描邊、落地軟影與 0.15s 打擊停頓）
## 時長: 8.0s (由握手信號觸發錄製)
## 展示: 去像素平滑插畫感、outline.gdshader 深暖褐描邊、foot_shadow.gdshader 落地柔化軟影、0.15s Hitstop

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

const ID: String = "rec02_battle_polish"
const TOTAL_DURATION: float = 8.0

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
					gs.set("level", 25)
					_main.call("_start_battle_raw", "leo")
					_step = 1
					print("REC02_LEO_BATTLE_STARTED at ", _elapsed)
		1:
			var host: Node = _main.get("host") if _main else null
			if host and host.get_child_count() > 0:
				_battle = host.get_child(host.get_child_count() - 1) as Control
				if _battle and _battle.is_inside_tree():
					_sim = _battle.get("sim")
					_step = 2
					_step_timer = 0.0
					print("REC02_BATTLE_NODE_READY at ", _elapsed)
		2:
			_step_timer += delta
			if _step_timer >= 1.0 and not _ready_written:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("REC02_READY_FOR_RECORDING written at elapsed=", _elapsed)

			if _ready_written and FileAccess.file_exists(_start_file):
				_rec_started = true
				_step = 3
				_rec_elapsed = 0.0
				print("REC02_RECORDING_STARTED at elapsed=", _elapsed)
		3:
			_rec_elapsed += delta
			# +1.5s: 普攻第 1 次
			if _rec_elapsed >= 1.5 and _step == 3:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_1 at rec_elapsed=", _rec_elapsed)
				_step = 4
		4:
			_rec_elapsed += delta
			# +3.5s: 普攻第 2 次
			if _rec_elapsed >= 3.5 and _step == 4:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_2 at rec_elapsed=", _rec_elapsed)
				_step = 5
		5:
			_rec_elapsed += delta
			# +5.5s: 普攻第 3 次（0.15s 打擊停頓與金色跳字）
			if _rec_elapsed >= 5.5 and _step == 5:
				if _battle:
					_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_3_HITSTOP at rec_elapsed=", _rec_elapsed)
				_step = 6
		6:
			_rec_elapsed += delta
			# +6.5s: 保存關鍵幀截圖
			if _rec_elapsed >= 6.5 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec02_battle_polish.png")
			# +8.0s: 錄影結束
			if _rec_elapsed >= TOTAL_DURATION:
				print("REC02_DONE at rec_elapsed=", _rec_elapsed)
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
