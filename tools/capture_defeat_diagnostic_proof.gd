extends SceneTree
## 戰敗結算戰力診斷卡與前往整頓按鈕實機截圖存證 (tools/capture_defeat_diagnostic_proof.gd)

var _out_dir: String = ""
var _crops_dir: String = ""
var _step := 0
var _wait := 0

var _battle: Control = null
var _current_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

const TASKS := [
	{"loc": "zh_TW", "file": "proof_01_defeat_diagnostic_zh_TW.png", "crop": "crops/crop_01_defeat_diagnostic_zh_TW.png"},
	{"loc": "en", "file": "proof_02_defeat_diagnostic_en.png", "crop": "crops/crop_02_defeat_diagnostic_en.png"},
	{"loc": "ja", "file": "proof_03_defeat_diagnostic_ja.png", "crop": "crops/crop_03_defeat_diagnostic_ja.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/t_39d5fc6c")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_es = root.get_node_or_null("EnergySystem")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("has_removed_ads", false)
	if _es:
		_es.call("refresh")
		_es.call("refresh_ad_daily")

	print("── 開始執行戰敗結算戰力診斷存證截圖腳本 (t_39d5fc6c) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step == 0 and _wait == 1:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")

		var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
		if b_scn:
			_battle = b_scn.instantiate()
			root.add_child(_battle)
			if _battle.has_method("setup"):
				_battle.call("setup", "training_dummy")

		var DefeatClass: GDScript = load("res://scripts/battle/battle_defeat_dialog.gd")
		if DefeatClass:
			_current_dlg = DefeatClass.new()
			_current_dlg.z_index = 95
			root.add_child(_current_dlg)
		return false

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])
		var cname: String = str(task["crop"])

		if _wait == 5:
			print("  -> 開啟彈窗中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)

		elif _wait >= 30:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 全景截圖完成 [%s]: %s" % [_step + 1, TASKS.size(), code, path])

			var crop_path := _out_dir.path_join(cname)
			_save_crop(path, crop_path, Rect2i(240, 100, 800, 520))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		_cleanup_nodes()
		print("── 戰敗結算戰力診斷存證截圖腳本執行完畢 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_dlg and is_instance_valid(_current_dlg):
		_current_dlg.queue_free()
		_current_dlg = null
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img: Image = vp.get_texture().get_image()
		if img and not img.is_empty():
			img.save_png(abs_path)


func _save_crop(src_abs_path: String, dst_abs_path: String, region: Rect2i) -> void:
	if not FileAccess.file_exists(src_abs_path):
		return
	var img := Image.load_from_file(src_abs_path)
	if img and not img.is_empty():
		var cropped := img.get_region(region)
		if cropped and not cropped.is_empty():
			cropped.save_png(dst_abs_path)
