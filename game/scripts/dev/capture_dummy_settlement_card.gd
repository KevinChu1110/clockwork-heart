extends SceneTree
## 木人樁試招結算數據卡實機截圖產生器 (t_5e74fb61)

const DummySettlementDialogScript := preload("res://scripts/battle/dummy_settlement_dialog.gd")

var _step := 0
var _wait := 0
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

	var stats := {
		"total_damage": 500,
		"elapsed_time": 12.8,
		"dps": 39.1,
	}
	_dlg = DummySettlementDialogScript.show_dialog(root, stats)


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
			if _wait >= 10:
				_shot("proof_dummy_settlement_card.png")
				_step = 1
		1:
			print("CAPTURE_DUMMY_SETTLEMENT_CARD_OK")
			quit(0)
			return true
	return false
