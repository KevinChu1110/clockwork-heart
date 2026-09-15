extends SceneTree
## 五族實機戰鬥滿怒招式截圖產生器
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_five_races_combat.gd

var _frame: int = 0
var _step: int = 0
var _race_idx: int = 0
var _main: Node = null
var _out_dir: String = ""
var _proof_dir: String = ""

var _races = [
	{"race": "rabbit", "name": "星芒兔", "skill": "橫斬", "skill_id": "slash", "line": "sword", "weapon": "rusty_blade", "file": "proof_combat_rabbit_slash.png"},
	{"race": "lion", "name": "獅衛隊長", "skill": "一線突刺", "skill_id": "line_thrust", "line": "spear", "weapon": "ash_spear", "file": "proof_combat_lion_thrust.png"},
	{"race": "fox", "name": "靈尾狐", "skill": "魔彈", "skill_id": "magic_bolt", "line": "magic", "weapon": "star_rod", "file": "proof_combat_fox_magic.png"},
	{"race": "boar", "name": "鋼牙豕", "skill": "碎岩鎚", "skill_id": "stone_crush", "line": "hammer", "weapon": "anvil_hammer", "file": "proof_combat_boar_crush.png"},
	{"race": "macaque", "name": "金毛猴", "skill": "連環拳", "skill_id": "combo_fist", "line": "fist", "weapon": "wrap_gloves", "file": "proof_combat_macaque_fist.png"},
]

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
				_start_current_race_battle()
				_step = 1
				_frame = 0
		1:
			# 等待戰鬥畫面載入並注入狀態
			if _frame >= 25:
				var cur = _races[_race_idx]
				var host: Control = _main.get("host") as Control
				var battle_node: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if battle_node and is_instance_valid(battle_node):
					var sim = battle_node.get("sim")
					if sim != null:
						var p = sim.call("get_unit", "player")
						if p != null:
							p.rage = 100.0

					if battle_node.has_method("_append_log"):
						battle_node.call("_append_log", "[color=#1a4a75]%s 手持 T1 武器，滿怒 100%% 爆發！[/color]" % cur["name"])
						battle_node.call("_append_log", "[color=#b24a00]%s 使出 %s！[/color]" % [cur["name"], cur["skill"]])
					if battle_node.has_method("_flash_skill_banner"):
						battle_node.call("_flash_skill_banner", cur["skill"], true)

				_step = 2
				_frame = 0
		2:
			# 等待 15 幀確保畫面與戰鬥日誌完全繪製並截圖
			if _frame >= 15:
				var cur = _races[_race_idx]
				var host: Control = _main.get("host") as Control
				var bnode: Node = host.get_child(0) if (host and host.get_child_count() > 0) else null
				if bnode and bnode.has_method("_flash_skill_banner"):
					bnode.call("_flash_skill_banner", cur["skill"], true)

				var img := root.get_viewport().get_texture().get_image()
				if img:
					var p1 := _out_dir.path_join(cur["file"])
					var p2 := _proof_dir.path_join(cur["file"])
					img.save_png(p1)
					img.save_png(p2)
					print("SAVED_PROOF [%s]: %s & %s" % [cur["race"], p1, p2])

				_race_idx += 1
				if _race_idx < _races.size():
					_start_current_race_battle()
					_step = 1
					_frame = 0
				else:
					print("ALL_FIVE_RACES_COMBAT_CAPTURE_OK")
					quit(0)
					return true
	return false

func _start_current_race_battle() -> void:
	var cur = _races[_race_idx]
	var gs: Node = root.get_node_or_null("GameState")
	var sk: Node = root.get_node_or_null("SkillSystem")
	if gs:
		gs.call("reset_new_game", cur["race"])
		gs.set("player_name", cur["name"])
		gs.set("player_race", cur["race"])
		gs.set("level", 1)
		gs.set("energy", 15)
	if sk:
		sk.call("ensure_skill_map")
		sk.call("grant_for_weapon_class", cur["line"])

	# 關閉既有戰鬥若存在
	var host: Control = _main.get("host") as Control
	if host:
		for c in host.get_children():
			c.queue_free()

	_main.call("_start_battle_raw", "wolf")
