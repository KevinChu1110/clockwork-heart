extends SceneTree
## 狐族與野豬族戰鬥待機換裝實機截圖產生器
## 依據任務規範：
## 1. 狐族裝備星穹觀測官裝 (costume_astral_observer) 與星穹披肩 (costume_astral_cape)
## 2. 野豬族裝備維京鐵甲 (costume_viking_ironclad) 與維京束帶 (costume_viking_harness)
## 3. 各族提供未縮放 1280x720 完整畫面原圖（待機＋攻擊）
## 4. 各族提供角色區特寫與攻擊抽格武器驗證圖

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


func _setup_equipment(race: String, costume_id: String, weapon_id: String, chassis_id: String, eq_base: String) -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("player_race", race)
		gs.set("player_name", "雷克斯" if race == "fox" else "巴克")
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
			"weapon": weapon_id
		})

	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", eq_base, "rare")
		if inst.is_empty():
			inst = eq.call("roll_instance", "dawn_blade", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid


func _run_captures() -> void:
	await _wait_frames(5)
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")

	# ══════════════════════════════════════
	# 🦊 狐族戰鬥截圖
	# ══════════════════════════════════════
	print(">>> [狐族 場景 1] 狐族換上星穹觀測官裝進戰鬥...")
	_setup_equipment("fox", "costume_astral_observer", "wpn_astral_staff", "paint_fox_orange", "star_rod")

	var battle_fox: Control = b_scn.instantiate()
	root.add_child(battle_fox)
	if battle_fox.has_method("setup"):
		battle_fox.call("setup", "wolf")

	await _wait_frames(18)
	print(">>> 截取未縮放完整狐族戰鬥待機畫面原圖...")
	await _capture_frame("proof_battle_fox_full_screen.png")

	print(">>> 觸發未縮放攻擊動作，截取未縮放完整攻擊畫面原圖...")
	if battle_fox.has_method("_set_player_pose"):
		battle_fox.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_fox_attack_full_screen.png")

	if battle_fox.has_method("_set_player_pose"):
		battle_fox.call("_set_player_pose", "idle", false)
	await _wait_frames(5)

	battle_fox.pivot_offset = Vector2(300, 360)
	battle_fox.scale = Vector2(2.1, 2.1)
	await _wait_frames(6)
	print(">>> 截取第一套外裝（星穹觀測官裝）狐族戰鬥待機畫面...")
	await _capture_frame("proof_battle_fox_equipped_observer.png")

	print(">>> 觸發攻擊動作，截取攻擊抽格畫面...")
	if battle_fox.has_method("_set_player_pose"):
		battle_fox.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_fox_attack_staff.png")

	battle_fox.queue_free()
	await _wait_frames(5)

	# 狐族第二套外裝
	print(">>> [狐族 場景 2] 狐族換上星穹披肩進戰鬥...")
	_setup_equipment("fox", "costume_astral_cape", "wpn_astral_staff", "paint_fox_orange", "star_rod")

	var battle_fox2: Control = b_scn.instantiate()
	root.add_child(battle_fox2)
	if battle_fox2.has_method("setup"):
		battle_fox2.call("setup", "wolf")

	battle_fox2.pivot_offset = Vector2(300, 360)
	battle_fox2.scale = Vector2(2.1, 2.1)
	await _wait_frames(18)
	print(">>> 截取第二套外裝（星穹披肩）狐族戰鬥待機畫面...")
	await _capture_frame("proof_battle_fox_equipped_cape.png")

	battle_fox2.queue_free()
	await _wait_frames(5)

	# ══════════════════════════════════════
	# 🐗 野豬族戰鬥截圖
	# ══════════════════════════════════════
	print(">>> [野豬族 場景 1] 野豬換上維京鐵甲進戰鬥...")
	_setup_equipment("boar", "costume_viking_ironclad", "wpn_anvil_greathammer", "paint_molten_crimson", "anvil_hammer")

	var battle_boar: Control = b_scn.instantiate()
	root.add_child(battle_boar)
	if battle_boar.has_method("setup"):
		battle_boar.call("setup", "wolf")

	await _wait_frames(18)
	print(">>> 截取未縮放完整野豬戰鬥待機畫面原圖...")
	await _capture_frame("proof_battle_boar_full_screen.png")

	print(">>> 觸發未縮放攻擊動作，截取未縮放完整攻擊畫面原圖...")
	if battle_boar.has_method("_set_player_pose"):
		battle_boar.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_boar_attack_full_screen.png")

	if battle_boar.has_method("_set_player_pose"):
		battle_boar.call("_set_player_pose", "idle", false)
	await _wait_frames(5)

	battle_boar.pivot_offset = Vector2(300, 360)
	battle_boar.scale = Vector2(2.1, 2.1)
	await _wait_frames(6)
	print(">>> 截取第一套外裝（維京鐵甲）野豬戰鬥待機畫面...")
	await _capture_frame("proof_battle_boar_equipped_ironclad.png")

	print(">>> 觸發攻擊動作，截取攻擊抽格畫面...")
	if battle_boar.has_method("_set_player_pose"):
		battle_boar.call("_set_player_pose", "attack", true)
	await _wait_frames(5)
	await _capture_frame("proof_battle_boar_attack_hammer.png")

	battle_boar.queue_free()
	await _wait_frames(5)

	# 野豬第二套外裝
	print(">>> [野豬族 場景 2] 野豬換上維京束帶進戰鬥...")
	_setup_equipment("boar", "costume_viking_harness", "wpn_anvil_greathammer", "paint_molten_crimson", "anvil_hammer")

	var battle_boar2: Control = b_scn.instantiate()
	root.add_child(battle_boar2)
	if battle_boar2.has_method("setup"):
		battle_boar2.call("setup", "wolf")

	battle_boar2.pivot_offset = Vector2(300, 360)
	battle_boar2.scale = Vector2(2.1, 2.1)
	await _wait_frames(18)
	print(">>> 截取第二套外裝（維京束帶）野豬戰鬥待機畫面...")
	await _capture_frame("proof_battle_boar_equipped_harness.png")

	battle_boar2.queue_free()
	await _wait_frames(5)

	print(">>> 狐族與野豬族戰鬥截圖存證產生完畢！")
	quit(0)
