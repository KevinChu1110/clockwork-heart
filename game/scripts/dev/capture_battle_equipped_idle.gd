extends SceneTree
## 戰鬥待機換裝實機截圖產生器
## 依據任務規範：
## 1. 兔族換上皇家巡遊禮服進戰鬥 (proof_battle_equipped_royal_parade.png)
## 2. 換蒸汽工匠裝再進戰鬥 (proof_battle_equipped_steam_artisan.png)
## 3. 攻擊幀抽格驗證武器持握 (proof_battle_attack_sword.png)
## 門檻：待機幀與大廳 equipped_idle 同座標同色像素比 <= 2%，兩套外裝 diff > 10000 px

var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p := _out_dir.path_join(filename)
		img.save_png(p)
		print("  ✓ 成功存證截圖: ", p)


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
			"weapon": "dawn_blade"
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


func _run_captures() -> void:
	await _wait_frames(5)

	# ── 第一場：兔族裝備皇家巡遊禮服 (costume_royal_parade) ──
	print(">>> [場景 1] 兔族換上皇家巡遊禮服進戰鬥...")
	_setup_equipment("rabbit", "costume_royal_parade")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	if battle.has_method("setup"):
		battle.call("setup", "wolf")

	# 縮放焦點對準玩家角色區（類似探索模式 cam.zoom），讓 1280x720 畫布清晰呈現紙娃娃細節
	battle.pivot_offset = Vector2(300, 360)
	battle.scale = Vector2(2.1, 2.1)

	await _wait_frames(18)
	print(">>> 截取第一套外裝（皇家巡遊禮服）戰鬥待機畫面...")
	await _capture_frame("proof_battle_equipped_royal_parade.png")

	# 抽格攻擊動作
	print(">>> 觸發攻擊動作，截取攻擊抽格畫面...")
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_attack_sword.png")

	battle.queue_free()
	await _wait_frames(5)

	# ── 第二場：兔族換裝蒸汽工匠裝 (costume_steam_artisan) ──
	print(">>> [場景 2] 兔族換上蒸汽工匠裝進戰鬥...")
	_setup_equipment("rabbit", "costume_steam_artisan")

	var battle2: Control = b_scn.instantiate()
	root.add_child(battle2)
	if battle2.has_method("setup"):
		battle2.call("setup", "wolf")

	battle2.pivot_offset = Vector2(300, 360)
	battle2.scale = Vector2(2.1, 2.1)

	await _wait_frames(18)
	print(">>> 截取第二套外裝（蒸汽工匠裝）戰鬥待機畫面...")
	await _capture_frame("proof_battle_equipped_steam_artisan.png")

	battle2.queue_free()
	await _wait_frames(5)

	print(">>> 全數截圖存證產生完畢！")
	quit(0)
