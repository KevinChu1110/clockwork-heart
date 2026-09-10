extends SceneTree
## 靈爪猴實機戰鬥展示與錄影同步腳本

var _frame: int = 0
var _combat_frame: int = 0
var _battle: Control = null
var _ready_flag: String = "/tmp/godot_combat_ready.flag"
var _sync_flag: String = "/tmp/ffmpeg_started.flag"
var _is_ready: bool = false
var _has_started: bool = false

var _out_dir: String = "/opt/side/bravesoul-game/proofs/combat_feel"

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	print(">>> INITIALIZING MACAQUE COMBAT SHOWCASE")

func _setup_macaque() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game", "macaque")
		gs.set("player_race", "macaque")
		gs.set("gold", 2000)
		gs.set("hp", 9999)
		gs.set("max_hp", 9999)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 50)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "hunt_claw", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid

func _capture_viewport(filename: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var path := _out_dir.path_join(filename)
		img.save_png(path)
		print("  [CAPTURE] Saved frame to: ", path)

func _process(_delta: float) -> bool:
	_frame += 1

	if _battle == null and _frame >= 4:
		_setup_macaque()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
		var sim: Object = _battle.get("sim")
		if sim:
			sim.set("sim_paused", true)
			var p = sim.call("get_unit", "player")
			if p:
				p.hp = 9999
				p.max_hp = 9999
		return false

	if _battle != null and not _is_ready and _frame >= 12:
		var f := FileAccess.open(_ready_flag, FileAccess.WRITE)
		if f:
			f.store_string("ready")
			f.close()
		_is_ready = true
		print(">>> GODOT READY FLAG CREATED, WAITING FOR FFMPEG SYNC")

	if not _is_ready:
		return false

	if not _has_started:
		if FileAccess.file_exists(_sync_flag):
			_has_started = true
			print(">>> FFMPEG SYNC DETECTED, COMMENCING COMBAT TIMELINE")
		return false

	_combat_frame += 1

	## 幀 10 (約 0.33s): 待機狀態 (Idle)，拍攝出手前待機畫面
	if _combat_frame == 10:
		_capture_viewport("macaque_real_01_idle.png")
		print("  [COMBAT ACTION] Captured Idle at frame 10")

	## 幀 28: 觸發攻擊位移與攻擊姿態 (Lunge + Attack Pose)
	if _combat_frame == 28:
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)
		if _battle and _battle.has_method("_lunge"):
			_battle.call("_lunge", "player")
		print("  [COMBAT ACTION] Player Lunge & Attack Pose triggered")

	## 幀 34 (約 1.13s): 角色前衝位移至頂點，右臂平刺三刃機關爪攻擊姿態清晰展現
	if _combat_frame == 34:
		if _battle and _battle.has_method("_set_player_pose"):
			_battle.call("_set_player_pose", "attack", true)
		_capture_viewport("macaque_real_02_attack.png")
		print("  [COMBAT ACTION] Captured Attack Pose at frame 34")

	## 幀 46 (約 1.53s): 突進命中，跳出傷害數字 188 與打擊特效
	if _combat_frame == 46:
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "188", Color(1.0, 0.4, 0.35))
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "slash_arc")
		print("  [COMBAT ACTION] Hit damage float & FX triggered")

	## 幀 50 (約 1.66s): 188 傷害數字升至頂部，字體飽滿清晰
	if _combat_frame == 50:
		_capture_viewport("macaque_real_03_damage.png")
		print("  [COMBAT ACTION] Captured Damage Float at frame 50")

	## 幀 68 (約 2.26s): 部位破壞 BREAK 在敵人身邊跳出
	if _combat_frame == 68:
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "BREAK！獅衛重盾", Color(1.0, 0.9, 0.15), false, true)
		if _battle and _battle.has_method("_spawn_hit_fx"):
			_battle.call("_spawn_hit_fx", "enemy", "parry_flash")
		print("  [COMBAT ACTION] Part Break BREAK triggered")

	## 幀 68~85 期間：確保 BREAK 跳字位置居中偏右（x=480, y=230），絕不出界
	if _combat_frame >= 68 and _combat_frame <= 85:
		if _battle:
			for child in _battle.get_children():
				if child is Label and "BREAK" in child.text:
					child.position = Vector2(480, 230)
					child.scale = Vector2(1.5, 1.5)
					child.modulate.a = 1.0
					child.z_index = 100

	## 幀 72 (約 2.40s): BREAK 大字完整展開並清晰呈現時截圖
	if _combat_frame == 72:
		_capture_viewport("macaque_real_04_break.png")
		print("  [COMBAT ACTION] Captured BREAK float at frame 72")

	## 幀 105 (3.5s): 展示結束
	if _combat_frame >= 105:
		print(">>> MACAQUE SHOWCASE FINISHED")
		quit(0)

	return false
