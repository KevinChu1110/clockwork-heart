extends SceneTree
## REC-04 怒氣滿額超轉速過載 (Overdrive) 與部位 BREAK
## 時長: 6.5s (前置 3.0s 緩衝), 雷歐戰 setup("leo")
## 展示: 怒氣滿額覺醒、齒輪超轉速狂暴連斬、部位擊破金字 BREAK 爆散

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
					gs.set("level", 30)
					_main.call("_start_battle_raw", "leo")
					_step = 1
					print("REC04_BATTLE_STARTED at ", _elapsed)
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
				print("REC04_RECORDING_WINDOW_START at ", _elapsed)
		3:
			# +1.2s: 怒氣滿 100% 並觸發暴怒覺醒
			if _elapsed >= _start_delay + 1.2 and _sim:
				var p = _sim.call("get_unit", "player")
				if p:
					p.set("rage", 100.0)
					_sim.call("trigger_fury_awakening")
					print("REC04_FURY_AWAKENING_TRIGGERED at ", _elapsed)
				_step = 4
		4:
			# +2.2s: 狂暴高速普攻
			if _elapsed >= _start_delay + 2.2 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC04_FURY_ATTACK_1 at ", _elapsed)
				_step = 5
		5:
			# +3.5s: 觸發部位 BREAK（壓低部位血量並攻擊破壞）
			if _elapsed >= _start_delay + 3.5 and _sim and _battle:
				var boss = _sim.call("_primary_boss_unit")
				if boss and boss.get("parts") and boss.parts.size() > 1:
					boss.parts[1]["hp"] = 1
					_sim.set("focus_part_id", boss.parts[1].get("id", ""))
				_battle.call("_on_thumb_attack")
				print("REC04_BREAK_ATTACK at ", _elapsed)
				_step = 6
		6:
			# +5.0s: 保存關鍵幀截圖
			if _elapsed >= _start_delay + 5.0 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec04_overdrive_break.png")
			# +6.5s: 錄影結束
			if _elapsed >= _start_delay + 6.5:
				print("REC04_DONE at ", _elapsed)
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
