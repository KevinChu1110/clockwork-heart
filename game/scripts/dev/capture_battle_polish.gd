extends SceneTree
## 戰鬥畫面換皮截圖：godot --path game --headless --script res://scripts/dev/capture_battle_polish.gd

var _frame: int = 0
var _battle: Control = null
var _out_dir: String = ""
var _out_web: String = ""
var _ws: String = ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	_out_web = base.path_join("../web/media/shots")
	_ws = OS.get_environment("HERMES_KANBAN_WORKSPACE")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_web)
	if _ws != "":
		DirAccess.make_dir_recursive_absolute(_ws)


func _setup_player_loadout() -> void:
	var gs: Node = root.get_node_or_null("GameState")
	if gs:
		gs.call("reset_new_game")
		gs.set("gold", 1500)
		gs.set("weapon_tier", 3)
		gs.set("weapon_atk", 18)
		gs.set("weapon_name", "精煉長劍")
		gs.set("path_style", "sword")
		gs.call("set_flag", "c1_forged", true)
		gs.call("set_flag", "c1_entered_city", true)
		gs.call("set_flag", "tut_done", true)
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	if eq and gs:
		var inst: Dictionary = eq.call("roll_instance", "dawn_blade", "rare")
		if inst.is_empty():
			inst = eq.call("roll_instance", "knight_saber", "rare")
		if not inst.is_empty():
			var uid := str(inst.get("uid", ""))
			gs.set("weapon_loadout", [uid, "", ""])
			gs.set("weapon_loadout_active", 0)
			gs.equip_worn[uid] = inst
			gs.equip_slots["weapon"] = uid
			gs.set("weapon_name", inst.get("name", "晨光長劍"))
			gs.set("weapon_atk", int((inst.get("rolled", {}) as Dictionary).get("atk", 24)))
			gs.set("path_style", "sword")


func _save_image(img: Image, filename: String) -> void:
	if img == null:
		return
	var p_shot := _out_dir.path_join(filename)
	img.save_png(p_shot)
	var p_web := _out_web.path_join(filename)
	img.save_png(p_web)
	if _ws != "":
		img.save_png(ProjectSettings.globalize_path(_ws).path_join(filename))
	print("SAVED_BATTLE_POLISH: ", p_shot, " & ", p_web)


func _dump_shadows(b: Node) -> void:
	for path in ["Arena/PlayerSlot/PlayerBody", "Arena/EnemySlot/EnemyBody"]:
		var body := b.get_node_or_null(path) as TextureRect
		var layer := b.get_node_or_null("ShadowLayer")
		var sh: TextureRect = null
		if layer and body:
			sh = layer.get_node_or_null("FootShadow_%s" % body.name) as TextureRect
		print("SHADOW ", path,
			" body_sz=", body.size if body else Vector2.ZERO,
			" body_pos=", body.global_position if body else Vector2.ZERO,
			" body_tex=", body.texture.resource_path if (body and body.texture) else "null",
			" sh_sz=", sh.size if sh else Vector2.ZERO,
			" sh_pos=", sh.global_position if sh else Vector2.ZERO,
			" vis=", sh.visible if sh else false)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 4:
		_setup_player_loadout()
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "road_bandit")
	elif _frame == 26:
		if _battle:
			_dump_shadows(_battle)
	elif _frame == 28:
		var img := root.get_viewport().get_texture().get_image()
		if img:
			_save_image(img, "proof_battle_polish_bandit.png")
			_save_image(img, "proof_11_battle.png")
		if _battle and is_instance_valid(_battle):
			_battle.queue_free()
			_battle = null
	elif _frame == 32:
		_setup_player_loadout()
		var b_scn2: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn2.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "leo")
	elif _frame == 54:
		if _battle:
			_dump_shadows(_battle)
	elif _frame == 56:
		var img2 := root.get_viewport().get_texture().get_image()
		if img2:
			_save_image(img2, "proof_battle_polish_leo.png")
		print("BATTLE_POLISH_CAPTURE_OK")
		quit(0)
	return false
