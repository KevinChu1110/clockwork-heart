extends SceneTree
## 猴族戰鬥待機換裝實機截圖產生器
## 依據任務規範：
## 1. 猴族換上破曉行僧袍 (costume_dawn_monk_tunic) 進戰鬥 (proof_battle_macaque_equipped_dawn_monk.png)
## 2. 猴族換上天元演武者機關甲 (costume_zen_striker) 進戰鬥 (proof_battle_macaque_equipped_zen_striker.png)
## 3. 攻擊幀抽格驗證武器持握 (proof_battle_macaque_attack_claws.png)
## 4. 完整未縮放待機畫面 (proof_battle_macaque_full_screen.png)
## 5. 完整未縮放攻擊畫面 (proof_battle_macaque_attack_full_screen.png)

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


func _setup_equipment(race: String, costume_id: String, chassis_id: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", race)
		gs.set("player_name", "悟空")
		gs.set("gold", 2000)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 40)
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "tut_done", true)
		gs.set("paperdoll_slots", {
			"race": race,
			"costume": costume_id,
			"chassis": chassis_id,
			"costume_id": costume_id,
			"paint_id": chassis_id,
			"weapon": "wpn_spring_claws"
		})

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "hunt_claw", "rare")
		if inst.is_empty():
			inst = eq.call("roll_instance", "hunt_claw", "uncommon")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid


func _run_captures() -> void:
	await _wait_frames(5)

	# ── 第一場：猴族裝備破曉行僧袍 (costume_dawn_monk_tunic) ──
	print(">>> [場景 1] 猴族換上破曉行僧袍進戰鬥...")
	_setup_equipment("macaque", "costume_dawn_monk_tunic", "paint_ivory_stock")

	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	var battle: Control = b_scn.instantiate()
	root.add_child(battle)
	if battle.has_method("setup"):
		battle.call("setup", "wolf")

	await _wait_frames(18)
	print(">>> 截取未縮放完整猴族戰鬥待機畫面原圖（含敵方、我方、全景與接地影）...")
	await _capture_frame("proof_battle_macaque_full_screen.png")

	# 抽格未縮放攻擊畫面原圖
	print(">>> 觸發未縮放攻擊動作，截取未縮放完整攻擊畫面原圖...")
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_macaque_attack_full_screen.png")

	# 切回待機準備特寫
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "idle", false)
	await _wait_frames(5)

	# 縮放焦點對準玩家角色區
	battle.pivot_offset = Vector2(300, 360)
	battle.scale = Vector2(2.1, 2.1)

	await _wait_frames(6)
	print(">>> 截取第一套外裝（破曉行僧袍）猴族戰鬥待機畫面...")
	await _capture_frame("proof_battle_macaque_equipped_dawn_monk.png")

	# 抽格攻擊動作
	print(">>> 觸發攻擊動作，截取攻擊抽格畫面...")
	if battle.has_method("_set_player_pose"):
		battle.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_macaque_attack_claws.png")

	battle.queue_free()
	await _wait_frames(5)

	# ── 第二場：猴族換裝天元演武者 (costume_zen_striker) ──
	print(">>> [場景 2] 猴族換上天元演武者進戰鬥...")
	_setup_equipment("macaque", "costume_zen_striker", "paint_bamboo_bronze")

	var battle2: Control = b_scn.instantiate()
	root.add_child(battle2)
	if battle2.has_method("setup"):
		battle2.call("setup", "wolf")

	battle2.pivot_offset = Vector2(300, 360)
	battle2.scale = Vector2(2.1, 2.1)

	await _wait_frames(18)
	print(">>> 截取第二套外裝（天元演武者）猴族戰鬥待機畫面...")
	await _capture_frame("proof_battle_macaque_equipped_zen_striker.png")

	battle2.queue_free()
	await _wait_frames(5)

	print(">>> 猴族戰鬥截圖存證產生完畢！")
	quit(0)
