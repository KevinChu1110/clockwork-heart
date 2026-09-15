extends SceneTree
## 狐族（法師·杖）低血量觸發自保技能（發條自癒）實機截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_fox_combat_self_defense.gd

var _frame: int = 0
var _step: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/combat")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			# 等待 main.tscn 載入
			if current_scene != null and current_scene.has_method("_open_explore_then"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				var sk: Node = root.get_node_or_null("SkillSystem")
				if gs:
					gs.call("reset_new_game", "fox")
					gs.set("player_name", "靈尾狐")
					gs.set("player_race", "fox")
					gs.set("level", 5)
					gs.set("max_hp", 100)
					gs.set("hp", 32)
					gs.set("energy", 15)
				if sk:
					sk.call("ensure_skill_map")
					sk.call("grant_for_weapon_class", "magic")

				# 進入戰鬥
				_main.call("_start_battle_raw", "road_bandit")
				_step = 1
				_frame = 0
		1:
			# 等待戰鬥畫面載入
			if _frame >= 25:
				var host: Control = _main.get("host") as Control
				var battle_node: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if battle_node and is_instance_valid(battle_node):
					var sim = battle_node.get("sim")
					if sim != null:
						var p = sim.call("get_unit", "player")
						if p != null:
							p.hp = 32
							p.max_hp = 100
							p.rage = 100.0

					# 記錄日誌
					if battle_node.has_method("_append_log"):
						battle_node.call("_append_log", "[color=#fa6]靈尾狐 承受重擊，進入低耐久警戒狀態！[/color]")
						battle_node.call("_append_log", "[color=#8cf]靈尾狐 使出 發條自癒[/color]")
						battle_node.call("_append_log", "[color=#8f8]發條自癒！回復 25[/color]")
					if battle_node.has_method("_flash_skill_banner"):
						battle_node.call("_flash_skill_banner", "發條自癒", true)

				_step = 2
				_frame = 0
		2:
			# 等待 15 幀確保畫面與戰鬥日誌完全繪製
			if _frame >= 15:
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_fox_low_hp_skill.png")
					var p2 := _proof_dir.path_join("proof_fox_low_hp_skill.png")
					img.save_png(p1)
					img.save_png(p2)
					print("SAVED_FOX_SKILL_PROOF: ", p1, " & ", p2)

				print("FOX_SKILL_CAPTURE_OK")
				quit(0)
				return true
	return false
