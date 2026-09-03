extends SceneTree

var _frame: int = 0
var _lobby: Control = null
var _battle: Control = null
var _out_dir: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://").path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 8:
		## 觸發聚魂十連抽
		if _lobby and _lobby.has_method("_do_summon"):
			_lobby.call("_do_summon", 10)
	elif _frame == 20:
		## 截取聚魂十連抽結算畫面
		var img := root.get_viewport().get_texture().get_image()
		if img:
			var p := _out_dir.path_join("proof_mobile_gacha_showcase.png")
			img.save_png(p)
			print("SAVED_GACHA: ", p)
		
		## 移除 lobby，載入戰鬥視圖進行戰鬥飄字截圖
		if _lobby and is_instance_valid(_lobby):
			_lobby.queue_free()
		
		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		_battle = b_scn.instantiate()
		root.add_child(_battle)
		if _battle.has_method("setup"):
			_battle.call("setup", "road_bandit")
	elif _frame == 35:
		## 在戰鬥視圖觸發手遊暴擊與破防飄字
		if _battle and _battle.has_method("_spawn_float"):
			_battle.call("_spawn_float", "enemy", "4,820", Color(1.0, 0.85, 0.2), true, false)
			_battle.call("_spawn_float", "enemy", "BREAK", Color(1.0, 0.35, 0.1), false, true)
			_battle.call("_spawn_float", "player", "+850", Color(0.4, 1.0, 0.6), false, false)
	elif _frame == 45:
		## 截取戰鬥傷害飄字
		var img_b := root.get_viewport().get_texture().get_image()
		if img_b:
			var pb := _out_dir.path_join("proof_mobile_battle_damage.png")
			img_b.save_png(pb)
			print("SAVED_BATTLE_DAMAGE: ", pb)
		print("STEP2_CAPTURE_OK")
		quit(0)
	return false
