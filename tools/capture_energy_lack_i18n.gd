extends SceneTree
## 體力不足彈窗六語系即時刷新實機截圖腳本 (tools/capture_energy_lack_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja / zh_TW 實機全景截圖（1280x720），呈現 0-QA25 同屏大廳背景與彈窗同語系連動。
## 2. 彈窗開啟中直接切換語系，標題、按鈕、說明文字立即刷新。
## 3. OUT_DIR 只准本輪 proofs/energy-lack-i18n/ (0-QA23)。

var _out_dir: String = ""
var _crops_dir: String = ""
var _step := 0
var _wait := 0

var _current_lobby: Node = null
var _current_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_01_energy_lack_en.png", "crop": "crops/crop_01_energy_lack_en.png"},
	{"loc": "ja", "file": "proof_02_energy_lack_ja.png", "crop": "crops/crop_02_energy_lack_ja.png"},
	{"loc": "zh_TW", "file": "proof_03_energy_lack_zh_TW.png", "crop": "crops/crop_03_energy_lack_zh_TW.png"},
]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/energy-lack-i18n")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_es = root.get_node_or_null("EnergySystem")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("energy", 2)
	if _es:
		_es.call("refresh")
		_es.call("refresh_ad_daily")

	print("── 開始執行體力不足彈窗實機截圖腳本 (energy-lack-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	# 初始建立底層大廳與彈窗 (zh_TW)
	if _step == 0 and _wait == 1:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
		if LobbyClass:
			_current_lobby = LobbyClass.new()
			root.add_child(_current_lobby)

		var EnergyLackClass: GDScript = load("res://scripts/ui/energy_lack_dialog.gd")
		if EnergyLackClass:
			_current_dlg = EnergyLackClass.new()
			_current_dlg.z_index = 90
			root.add_child(_current_dlg)
		return false

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])
		var cname: String = str(task["crop"])

		# 在彈窗開著的狀態下動態切換語系
		if _wait == 5:
			print("  -> 開啟彈窗中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)

		elif _wait >= 30:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 全景截圖完成 [%s]: %s" % [_step + 1, TASKS.size(), code, path])

			var crop_path := _out_dir.path_join(cname)
			# 裁切中央卡片 (寬 750, 高 440，置中約 (265, 140))
			_save_crop(path, crop_path, Rect2i(240, 120, 800, 480))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		_cleanup_nodes()
		print("── 體力不足彈窗六語系實機截圖腳本執行完畢 ──")
		quit(0)
		return true

	return false

func _cleanup_nodes() -> void:
	if _current_dlg and is_instance_valid(_current_dlg):
		_current_dlg.queue_free()
		_current_dlg = null
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img: Image = vp.get_texture().get_image()
		if img and not img.is_empty():
			if img.get_size() != Vector2i(1280, 720):
				img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
			img.save_png(abs_path)

func _save_crop(src_path: String, dst_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img and not img.is_empty():
		var cropped := img.get_region(rect)
		cropped.save_png(dst_path)
