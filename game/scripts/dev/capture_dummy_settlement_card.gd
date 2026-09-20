extends SceneTree
## 木人樁試招結算數據卡實機截圖產生器 (t_f761d9e4)
## 背景包含木人樁戰鬥場景，前景為半透明遮罩與浮空數據結算卡

const DummySettlementDialogScript := preload("res://scripts/battle/dummy_settlement_dialog.gd")

var _step := 0
var _wait := 0
var _battle: Control = null
var _dlg: Control = null
var _out_dirs: Array[String] = []


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	var repo_proofs := base.path_join("../proofs")
	_out_dirs.append(repo_proofs)

	var ws := OS.get_environment("HERMES_KANBAN_WORKSPACE")
	if ws != "":
		_out_dirs.append(ws.path_join("proofs"))

	for d in _out_dirs:
		DirAccess.make_dir_recursive_absolute(d)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.player_race = "rabbit"
		gs.player_name = "小白"
		gs.chapter = "c0"
		gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	# 建立戰鬥節點
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	root.add_child(_battle)


func _shot(filename: String) -> void:
	RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null:
		return
	for d in _out_dirs:
		var p := d.path_join(filename)
		img.save_png(p)
		print("  -> 已存檔: %s" % p)


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 5:
				if _battle.has_method("setup"):
					_battle.call("setup", "training_dummy")
				var stats := {
					"total_damage": 500,
					"elapsed_time": 12.8,
					"dps": 39.1,
				}
				_dlg = DummySettlementDialogScript.show_dialog(root, stats)
				_step = 1
				_wait = 0
		1:
			if _wait >= 25:
				_shot("proof_dummy_settlement_card.png")
				_step = 2
		2:
			print("CAPTURE_DUMMY_SETTLEMENT_CARD_OK")
			quit(0)
			return true
	return false
