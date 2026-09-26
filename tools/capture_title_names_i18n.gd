extends SceneTree
## 稱號名與解鎖條件六語系實機全景截圖腳本 (tools/capture_title_names_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja / zh_TW 實機全景截圖（1280x720），呈現 0-QA25 同屏大廳背景與稱號牆彈窗同語系連動。
## 2. 稱號牆開啟中直接切換語系，稱號名、解鎖條件、按鈕、狀態立即刷新。
## 3. OUT_DIR 嚴格限定本輪 proofs/title-names-i18n/ (0-QA23)。

var _out_dir: String = ""
var _crops_dir: String = ""
var _step := 0
var _wait := 0

var _current_lobby: Node = null
var _current_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _tc: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_01_title_names_en.png", "crop": "crops/crop_01_title_names_en.png"},
	{"loc": "ja", "file": "proof_02_title_names_ja.png", "crop": "crops/crop_02_title_names_ja.png"},
	{"loc": "zh_TW", "file": "proof_03_title_names_zh_TW.png", "crop": "crops/crop_03_title_names_zh_TW.png"},
]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/title-names-i18n")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_tc = root.get_node_or_null("TitleCatalog")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		# 預先設置部分解鎖條件，使畫面上同時呈現已解鎖（金黃/暖橘果凍底）與未解鎖（壓暗奶油底）卡片
		_gs.call("set_flag", "c1_perfect_parry_once", true)
		_gs.call("set_flag", "boss.white_fog_cleared", true)
		_gs.call("set_flag", "game_cleared", true)
		_gs.call("set_flag", "c1_sprout_done", true)

	print("── 開始執行稱號牆六語系實機截圖腳本 (title-names-i18n) ──")
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
			_current_lobby.name = "MobileLobby"
			root.add_child(_current_lobby)

		var newly: Array[String] = _tc.call("evaluate_all") if _tc and _tc.has_method("evaluate_all") else []
		var TitleWallClass: GDScript = load("res://scripts/ui/title_wall_dialog.gd")
		if TitleWallClass:
			_current_dlg = TitleWallClass.new()
			_current_dlg.z_index = 90
			_current_dlg.call("setup", newly, Callable(), Callable(), "回到廣場")
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
			# 裁切中央卡片網格與標題 (寬 750, 高 520，置中約 (265, 100))
			_save_crop(path, crop_path, Rect2i(250, 90, 780, 540))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		print("── 稱號牆實機截圖存證完成 ──")
		quit(0)
		return true

	return false


func _save_screenshot(path: String) -> void:
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		if img.get_size() != Vector2i(1280, 720):
			img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
		img.save_png(path)


func _save_crop(src_path: String, dst_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img != null:
		var cropped := img.get_region(rect)
		cropped.save_png(dst_path)
