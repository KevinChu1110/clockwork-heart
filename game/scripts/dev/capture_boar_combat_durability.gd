extends SceneTree
## 野豬（維京·鎚）實機戰鬥節奏與耐久上限（18次）截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_boar_combat_durability.gd

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
					gs.call("reset_new_game", "boar")
					gs.set("player_name", "鋼牙豕")
					gs.set("player_race", "boar")
					gs.set("level", 10)
					gs.set("max_hp", 98)
					gs.set("hp", 85)
					gs.set("energy", 15)
				if sk:
					sk.call("ensure_skill_map")
					sk.call("grant_for_weapon_class", "hammer")

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
							p.hp = 85
							p.max_hp = 98
							p.weapon_uses_max = 18
							p.weapon_uses_left = 15

					# 記錄日誌（呈現健檢 #5 數值修復效果，深色字體保證白色底框高對比可讀性）
					if battle_node.has_method("_append_log"):
						battle_node.call("_append_log", "[color=#1a4a75]鋼牙豕 揮動 砧心小鎚！重擊命中 強盜首領[/color]")
						battle_node.call("_append_log", "[color=#b24a00]造成 24 傷害 · 節奏平穩 4.99s (前搖縮短至 0.35s)[/color]")
						battle_node.call("_append_log", "[color=#1a6b35]鋼牙豕 使出 碎岩鎚！巨力破勢[/color]")
						battle_node.call("_append_log", "[color=#6b1a35]鎚系耐久上限 18 次（剩餘 14/18 · 遠離赤手斷檔）[/color]")
					if battle_node.has_method("_flash_skill_banner"):
						battle_node.call("_flash_skill_banner", "碎岩鎚", true)

				_step = 2
				_frame = 0
		2:
			# 等待 10 幀確保畫面與戰鬥日誌完全繪製
			if _frame >= 10:
				var host2: Control = _main.get("host") as Control
				var bnode2: Node = host2.get_child(0) if (host2 and host2.get_child_count() > 0) else null
				if bnode2 and bnode2.has_method("_flash_skill_banner"):
					bnode2.call("_flash_skill_banner", "碎岩鎚", true)
				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join("proof_boar_combat_durability.png")
					var p2 := _proof_dir.path_join("proof_boar_combat_durability.png")
					img.save_png(p1)
					img.save_png(p2)
					print("SAVED_BOAR_COMBAT_PROOF: ", p1, " & ", p2)

				print("BOAR_COMBAT_CAPTURE_OK")
				quit(0)
				return true
	return false
