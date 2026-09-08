extends SceneTree
## 截取武術館招式熟練度果凍進度條畫面
## godot --path game -s res://scripts/dev/capture_tutor_progress.gd

enum Step { BOOT, SETUP, WAIT, CAP, DONE }

var _step: Step = Step.BOOT
var _wait: int = 0
var _out_dir: String = ""
var _main: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

func _process(_delta: float) -> bool:
	match _step:
		Step.BOOT:
			change_scene_to_file("res://scenes/main.tscn")
			_step = Step.SETUP
		Step.SETUP:
			_main = current_scene
			if _main == null:
				return false
			var gs = root.get_node_or_null("GameState")
			var sk = root.get_node_or_null("SkillSystem")
			if gs and sk:
				gs.reset_new_game()
				gs.set_flag("c1_forged", true)
				gs.set_flag("c1_entered_city", true)
				gs.gold = 120
				sk.ensure_skill_map()
				# 習得橫斬 Lv.1，具有 8 點熟練度
				sk.grant_c1_greybeard()
				# 解鎖旋風斬
				sk.try_unlock("blade_dance")
				# 習得破星突刺並升至 Lv.3 滿階（展示滿條與推階提示）
				sk.learn("star_pierce", 3)
			if _main.has_method("_go_skill_panel"):
				_main.call("_go_skill_panel")
			_step = Step.WAIT
			_wait = 0
		Step.WAIT:
			_wait += 1
			if _wait >= 50:
				_step = Step.CAP
		Step.CAP:
			var img := root.get_viewport().get_texture().get_image()
			if img:
				var path := _out_dir.path_join("proof_tutor_skill_progress.png")
				img.save_png(path)
				print("SAVED: ", path)
			print("CAPTURE_TUTOR_PROGRESS_OK")
			_step = Step.DONE
			quit(0)
			return true
	return false
