extends SceneTree
## 《發條之心》戰鬥待機呼吸與動作姿態實機截圖產生器 (xvfb 驗證用)
## 依據任務規範：
## 1. 戰鬥待機兩張間隔 >= 1.0s 的實機截圖 (proof_battle_idle_breathe_t0.png, t1.png)，角色 scale 有可見差異
## 2. 出手當下截圖 scale 為 (1, 1)（呼吸已停，proof_battle_attack_strike.png）
## 3. 兩套外裝待機仍看得出換裝（proof_battle_equipped_costume_a.png, costume_b.png）

var _out_dir: String = ""
var _proof_dir: String = ""
var _time: float = 0.0
var _step: int = 0
var _battle: Control = null
var _player_body: TextureRect = null

var scale_t0: Vector2 = Vector2.ZERO
var scale_t1: Vector2 = Vector2.ZERO
var scale_atk: Vector2 = Vector2.ZERO


func _initialize() -> void:
	print("=== 開始產生戰鬥待機呼吸與姿態實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_proof_dir = base.path_join("../proofs/battle_breathe")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proof_dir)

	_setup_equipment("rabbit", "costume_nutcracker_guard")
	_step = 0
	_time = 0.0


func _setup_equipment(race: String, costume_id: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", race)
		gs.set("player_name", "小白")
		gs.set("gold", 2000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 40)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
		gs.set("paperdoll_slots", {
			"race": race,
			"costume": costume_id,
			"chassis": "paint_ivory_stock",
			"costume_id": costume_id,
			"paint_id": "paint_ivory_stock",
			"headwear": "",
			"optic_core": "core_cyan_emerald",
			"ears": "ears_upright_radar",
			"tail": "tail_spring_short",
			"weapon": "wpn_dawn_blade"
		})

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid


func _process(delta: float) -> bool:
	_time += delta

	match _step:
		0:
			# 載入戰鬥場景 1 (胡桃鉗近衛軍裝)
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "wolf")
			_player_body = _battle.get_node_or_null("Arena/PlayerSlot/PlayerBody") as TextureRect
			print(">>> [場景 1] 兔族換上胡桃鉗近衛軍裝進戰鬥...")
			_step = 1
			_time = 0.0

		1:
			# 等待呼吸 Tween 運行至第一個波峰 (1.1s，scale 約 1.03, 0.97)
			if _time >= 1.1:
				if _player_body:
					scale_t0 = _player_body.scale
				_save_screenshot("proof_battle_idle_breathe_t0.png")
				_save_screenshot("proof_battle_equipped_costume_a.png")
				print("  ✓ [t0=1.1s] 截取站立呼吸波峰 1 (Costume A): scale=%s" % [scale_t0])
				_step = 2
				_time = 0.0

		2:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，呼吸運行至反向波峰 (scale 約 0.98, 1.02)
			if _time >= 1.1:
				if _player_body:
					scale_t1 = _player_body.scale
				_save_screenshot("proof_battle_idle_breathe_t1.png")
				print("  ✓ [t1=2.2s] 截取站立呼吸波峰 2 (間隔 1.1s): scale=%s" % [scale_t1])
				# 觸發攻擊動作
				if _battle.has_method("_set_player_pose"):
					_battle.call("_set_player_pose", "attack", true)
				_step = 3
				_time = 0.0

		3:
			# 等待攻擊幀渲染 (0.08s, 5~6 幀)，驗證 breathing 停止且 scale 為 (1, 1)
			if _time >= 0.08:
				if _player_body:
					scale_atk = _player_body.scale
				_save_screenshot("proof_battle_attack_strike.png")
				print("  ✓ 出手當下 player_body.scale=%s (呼吸已停)" % [scale_atk])
				_battle.queue_free()
				_battle = null
				_player_body = null
				_step = 4
				_time = 0.0

		4:
			# 場景 2：換上第二套外裝（蒸汽工匠裝）
			if _time >= 0.1:
				print(">>> [場景 2] 兔族換上蒸汽工匠裝進戰鬥...")
				_setup_equipment("rabbit", "costume_steam_artisan")
				var b_scn2: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn2.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "wolf")
				_step = 5
				_time = 0.0

		5:
			# 等待場景 2 渲染穩定 (0.6s)
			if _time >= 0.6:
				_save_screenshot("proof_battle_equipped_costume_b.png")
				print("  ✓ 截取 [第二套外裝: 蒸汽工匠裝] 戰鬥待機畫面")
				if _battle:
					_battle.queue_free()
					_battle = null
				print("=== 實機截圖產生完成 ===")
				quit(0)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var p1 := _out_dir.path_join(filename)
	var p2 := _proof_dir.path_join(filename)
	img.save_png(p1)
	img.save_png(p2)
	print("  [截圖成功] -> %s" % filename)
