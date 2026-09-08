extends SceneTree
## REC-01 右手拇指操作熱區 (ThumbPad HUD)
## 時長: 4.5s (前置 3.0s 緩衝), 荒路殘兵 setup("road_bandit")
## 操作: 3次普攻揮斬 -> 1次換武(巨錘) -> 1次鎖定切換

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
				var eq: Node = root.get_node_or_null("EquipmentSystem")
				if _main and gs and eq:
					gs.call("reset_new_game")
					gs.call("set_flag", "c0_first_battle", true)
					eq.call("_ensure_state")
					gs.set("level", 16)
					var w1: Dictionary = {
						"uid": "rec_sword", "base_id": "test_sword", "name": "金屬長劍", "slot": "weapon",
						"tier": 1, "line": "sword", "quality": "rare", "quality_label": "靈",
						"rolled": {"atk": 18, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
					}
					var w2: Dictionary = {
						"uid": "rec_hammer", "base_id": "test_hammer", "name": "精鋼重錘", "slot": "weapon",
						"line": "hammer", "tier": 1, "quality": "rare", "quality_label": "靈",
						"rolled": {"atk": 28, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
					}
					gs.set("equip_bag", [w1, w2])
					gs.set("equip_worn", {})
					gs.set("weapon_loadout", ["", "", ""])
					gs.set("weapon_loadout_active", 0)
					eq.call("equip_weapon_to_loadout", "rec_sword", 0)
					eq.call("equip_weapon_to_loadout", "rec_hammer", 1)
					eq.call("switch_weapon_loadout", 0)
					_main.call("_start_battle_raw", "road_bandit")
					_step = 1
					print("REC01_BATTLE_STARTED at ", _elapsed)
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
				print("REC01_RECORDING_WINDOW_START at ", _elapsed)
		3:
			# +1.0s (4.0s): 第 1 次普攻
			if _elapsed >= _start_delay + 1.0 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_1 at ", _elapsed)
				_step = 4
		4:
			# +1.7s (4.7s): 第 2 次普攻
			if _elapsed >= _start_delay + 1.7 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_2 at ", _elapsed)
				_step = 5
		5:
			# +2.4s (5.4s): 第 3 次普攻
			if _elapsed >= _start_delay + 2.4 and _battle:
				_battle.call("_on_thumb_attack")
				print("REC01_ATTACK_3 at ", _elapsed)
				_step = 6
		6:
			# +3.1s (6.1s): 換武 ThumbSwitch
			if _elapsed >= _start_delay + 3.1 and _battle:
				_battle.call("_on_thumb_switch")
				print("REC01_SWITCH_WEAPON at ", _elapsed)
				_step = 7
		7:
			# +3.8s (6.8s): 鎖定切換 ThumbLock
			if _elapsed >= _start_delay + 3.8 and _battle:
				_battle.call("_thumb_cycle_lock", 1)
				print("REC01_CYCLE_LOCK at ", _elapsed)
				_step = 8
		8:
			# +4.1s (7.1s): 保存關鍵幀截圖
			if _elapsed >= _start_delay + 4.1 and not _saved_png:
				_saved_png = true
				_save_screenshot("rec01_thumb_pad.png")
			# +4.5s (7.5s): 錄影結束
			if _elapsed >= _start_delay + 4.5:
				print("REC01_DONE at ", _elapsed)
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
