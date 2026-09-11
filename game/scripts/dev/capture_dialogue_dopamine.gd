extends SceneTree
## 探索對話框與過場字幕多巴胺亮色盤實機截圖產生器
## 執行方式：
## xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_dialogue_dopamine.gd

var _out_dir: String = ""
var _proof_dir: String = ""
var _step: int = 0
var _frame_count: int = 0
var _main: Node = null


func _initialize() -> void:
	print("=== 開始產生對話框與過場字幕多巴胺實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	_proof_dir = base.path_join("../proofs/dialogue_dopamine")
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _save_shot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p_sc := _out_dir.path_join(filename)
		var p_pr := _proof_dir.path_join(filename)
		img.save_png(p_sc)
		img.save_png(p_pr)
		print("  SAVED: ", p_pr)


func _process(_delta: float) -> bool:
	_frame_count += 1
	match _step:
		0:
			# 等待 main.tscn 載入完成
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_name", "小白")
					gs.set("player_race", "rabbit")
					gs.set("level", 10)
					gs.set("gold", 8888)

				var village_screen = _main.Screen.C0_VILLAGE if "Screen" in _main else 2
				_main.call("_open_explore_then", "village", village_screen, Callable())
				_step = 1
				_frame_count = 0

		1:
			# 等待地圖載入，開啟對話框
			if _frame_count >= 20:
				print("  開啟探索對話框...")
				var lines := [
					{
						"speaker": "麥穗",
						"text": "指揮官，發條核心的能量指針已經校準完畢！準備好踏出城門探索荒野了嗎？",
					}
				]
				_main.call("_play_dialog", lines, Callable())
				_step = 2
				_frame_count = 0

		2:
			# 確保打字機完成並呈現人名+內文+繼續提示
			if _frame_count >= 10:
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox):
					dbox.call("_finish_typing")
				_step = 3
				_frame_count = 0

		3:
			# 等待對話框完全渲染穩定後截圖
			if _frame_count >= 15:
				_save_shot("proof_dialogue_playing.png")
				var dbox = _main.get("_dialogue")
				if dbox and is_instance_valid(dbox):
					dbox.visible = false
				_step = 4
				_frame_count = 0

		4:
			# 開啟全屏過場字幕
			if _frame_count >= 10:
				print("  開啟過場字幕...")
				var cutscene = _main.get("_cutscene")
				if cutscene and is_instance_valid(cutscene):
					var slides := [
						{
							"bg": "village",
							"portrait": "maisui",
							"speaker": "麥穗",
							"text": "在這個被齒輪與發條運轉的世界裡，每一顆心臟都有它甦醒的時刻。",
							"hold": 0.0,
						}
					]
					cutscene.call("play", slides, Callable())
				_step = 5
				_frame_count = 0

		5:
			# 等待過場動畫完全淡入（tween 需要約 0.4s = 24 幀）
			if _frame_count >= 30:
				_save_shot("proof_cutscene_caption.png")
				print("DIALOGUE_DOPAMINE_CAPTURE_OK")
				quit(0)
				return true

	return false
