extends SceneTree
## REC-02 視覺換血（粗描邊、落地軟影與 0.15s 打擊停頓）
## 時長: 8.0s (前置 3.0s 緩衝), 雷歐戰 setup("leo")
## 展示: 去像素平滑插畫感、outline.gdshader 深暖褐描邊、foot_shadow.gdshader 落地柔化軟影、0.15s Hitstop

var _elapsed: float = 0.0
var _start_delay: float = 3.0
var _main: Node = null
var _battle: Control = null
var _sim = null
var _step: int = 0
var _saved_png: bool = false
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	match _step:
		0:
			if _elapsed >= 0.5:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if _main and gs:
					gs.call("reset_new_game")
					gs.call("set_flag", "c0_first_battle", true)
					gs.set("level", 25)
					_main.call("_start_battle_raw", "leo")
					_step = 1
					print("REC02_LEO_BATTLE_STARTED at ", _elapsed)
		1:
			if _elapsed >= 1.2:
				var host: Node = _main.get("host") if _main else null
				if host and host.get_child_count() > 0:
					_battle = host.get_child(host.get_child_count() - 1) as Control
					if _battle:
						_sim = _battle.get("sim")
				_step = 2
		2:
			# 等待錄影開始點 (elapsed >= 3.0)
			if _elapsed >= _start_delay:
				_step = 3
				print("REC02_RECORDING_WINDOW_START at ", _elapsed)
		3:
			# +1.2s: 普攻觸發打擊
			if _elapsed >= _start_delay + 1.2 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_1 at ", _elapsed)
				_step = 4
		4:
			# +3.0s: 連續出招
			if _elapsed >= _start_delay + 3.0 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_2 at ", _elapsed)
				_step = 5
		5:
			# +4.8s: 普攻命中觸發 0.15s 打擊停頓與金色跳字
			if _elapsed >= _start_delay + 4.8 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC02_ATTACK_3_HITSTOP at ", _elapsed)
				_step = 6
		6:
			# +6.5s: 保存關鍵幀截圖
			if _elapsed >= _start_delay + 6.5 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec02_battle_polish.png")
			# +8.0s: 錄影結束
			if _elapsed >= _start_delay + 8.0:
				print("REC02_DONE at ", _elapsed)
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
