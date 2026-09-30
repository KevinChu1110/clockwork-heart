extends SceneTree
## 戰鬥打擊特效與通透背景截圖驗收腳本
## 執行方式：godot --path game -s res://scripts/dev/capture_combat_hit_fx.gd

var _battle: Control = null
var _frame: int = 0
var _out_dir: String = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/proofs/combat_fx"
var _shots_dir: String = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/screenshots"
var _web_dir: String = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfd4a2e3/web/media/shots"

var _captured_clear_bg := false
var _captured_hit_sparks := false
var _captured_crit_burst := false
var _hit_counter := 0
var _ready_file_written := false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_shots_dir)
	DirAccess.make_dir_recursive_absolute(_web_dir)

func _setup_player() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "rabbit")
		gs.set("gold", 1500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 24)
		gs.set("weapon_name", "晨光長劍")
		gs.set("path_style", "sword")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _save_shot(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p1 := _out_dir.path_join(filename)
		img.save_png(p1)
		var p2 := _shots_dir.path_join(filename)
		img.save_png(p2)
		var p3 := _web_dir.path_join(filename)
		img.save_png(p3)
		print("  [SAVED SHOT] -> %s" % p1)

func _process(_delta: float) -> bool:
	_frame += 1

	if _frame == 2:
		_setup_player()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "road_bandit")
		var f := FileAccess.open("/tmp/fb_lobby_capture.ready", FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
			_ready_file_written = true

	elif _frame == 14 and not _captured_clear_bg:
		print(">>> 捕捉 1: 通透手繪戰鬥背景（無 TileMap 覆蓋、無髒黑濾鏡、柔和藍紫軟影）")
		_save_shot("proof_battle_clear_bg.png")
		_captured_clear_bg = true

	elif _frame == 22:
		print(">>> 觸發 2: 玩家普攻打擊 -> 生成金屬火星與黃銅齒輪爆散")
		if _battle != null:
			_battle.call("_set_player_pose", "attack")
			_battle.call("_set_boss_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "road_bandit", "slash_arc", 0, false)
			_battle.call("_spawn_float", "road_bandit", "-38", Color(1.0, 0.4, 0.35))

	elif _frame == 24 and not _captured_hit_sparks:
		print(">>> 捕捉 2: 普通打擊金屬火星與齒輪爆散中幀")
		_save_shot("proof_battle_hit_sparks_gears.png")
		_captured_hit_sparks = true

	elif _frame == 35:
		print(">>> 觸發 3: 暴擊受擊打擊 -> 劇烈金屬火花與更多齒輪飛散")
		if _battle != null:
			_battle.call("_set_player_pose", "attack")
			_battle.call("_set_boss_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "road_bandit", "slash_arc", 0, true)
			_battle.call("_spawn_float", "road_bandit", "CRIT! -84", Color(1.0, 0.85, 0.2), true)

	elif _frame == 37 and not _captured_crit_burst:
		print(">>> 捕捉 3: 暴擊強烈金屬火花與齒輪爆散中幀")
		_save_shot("proof_battle_crit_burst.png")
		_captured_crit_burst = true

	elif _frame == 45:
		print(">>> 觸發 4: 換場展示雷歐庭院戰鬥背景與我方受擊")
		if _battle and is_instance_valid(_battle):
			_battle.queue_free()
			_battle = null

	elif _frame == 48:
		_setup_player()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")

	elif _frame == 54:
		print(">>> 觸發 4: 雷歐攻擊我方 -> 我方受擊爆出金屬火花與齒輪")
		if _battle != null:
			_battle.call("_set_boss_pose", "attack", true)
			_battle.call("_set_player_pose", "hit", true)
			_battle.call("_spawn_hit_fx", "player", "slash_arc", 0, false)
			_battle.call("_spawn_float", "player", "-24", Color(1.0, 0.3, 0.3))

	elif _frame == 56:
		print(">>> 捕捉 4: 我方受擊爆散金屬火花與齒輪中幀")
		_save_shot("proof_battle_player_hit_fx.png")
		_save_shot("proof_battle_leo_hit_fx.png")
		print("BATTLE_HIT_FX_CAPTURE_OK")
		quit(0)
		return true

	return false
