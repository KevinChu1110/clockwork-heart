extends SceneTree

var _elapsed: float = 0.0
var _step: int = 0
var _lobby: Control = null
var _rec_started: bool = false
var _rec_elapsed: float = 0.0
var _ready_written: bool = false
var _ready_file: String = "/tmp/fb_lobby_capture.ready"
var _start_file: String = "/tmp/fb_lobby_capture.start"

var _click_times: Array[float] = [1.5, 5.0, 8.5, 12.0, 15.5]
var _click_done: Array[bool] = [false, false, false, false, false]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		if "player_name" in gs:
			gs.player_name = "小白"
		if "level" in gs:
			gs.level = 15
		if "gold" in gs:
			gs.gold = 3850
		if "stardust" in gs:
			gs.stardust = 240

	change_scene_to_file("res://scenes/ui/mobile_lobby_standalone.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			if current_scene != null:
				_lobby = current_scene as Control
				if _lobby and _lobby.is_inside_tree():
					_step = 1
					print("STANDALONE_LOBBY_LOADED at elapsed=", _elapsed)
		1:
			if not _ready_written and _elapsed >= 0.5:
				_ready_written = true
				var f := FileAccess.open(_ready_file, FileAccess.WRITE)
				if f:
					f.store_string("ready")
					f.close()
				print("FB_LOBBY_READY at elapsed=", _elapsed)

			if not _rec_started:
				if FileAccess.file_exists(_start_file) or _elapsed >= 3.0:
					_rec_started = true
					print("FB_LOBBY_REC_STARTED at elapsed=", _elapsed)

			if _rec_started:
				_rec_elapsed += delta
				for i in range(_click_times.size()):
					if not _click_done[i] and _rec_elapsed >= _click_times[i]:
						_click_done[i] = true
						if _lobby and _lobby.has_method("_on_hero_clicked"):
							_lobby.call("_on_hero_clicked")
							print("HERO_CLICKED #", i + 1, " at rec_elapsed=", _rec_elapsed)

				if _rec_elapsed >= 20.5:
					print("FB_LOBBY_CAPTURE_DONE at rec_elapsed=", _rec_elapsed)
					quit(0)

	return false
