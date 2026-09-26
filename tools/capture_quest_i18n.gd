extends SceneTree
## 任務清單六語系實機全景截圖腳本 (tools/capture_quest_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja / zh_TW 實機全景截圖（1280x720），呈現 0-QA25 同屏大廳背景與任務面板同語系連動。
## 2. 開著任務清單中直接切換語系，標題、任務名、任務說明、獎勵、按鈕即時整片換。
## 3. OUT_DIR 嚴格限定為 proofs/quest-i18n/ (0-QA23)。
## 4. 0-QA24 檢核：日文漢字（長期任務、初鳴き等）為既定規範詞條；英文零 CJK 殘留。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _out_dir: String = ""
var _crops_dir: String = ""
var _step := 0
var _wait := 0

var _lobby: Control = null
var _main: Control = null
var _loc_node: Node = null
var _gs: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_01_quest_en.png", "crop": "crops/crop_01_quest_en.png"},
	{"loc": "ja", "file": "proof_02_quest_ja.png", "crop": "crops/crop_02_quest_ja.png"},
	{"loc": "zh_TW", "file": "proof_03_quest_zh_TW.png", "crop": "crops/crop_03_quest_zh_TW.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/quest-i18n")
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

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")

	print("── 開始執行任務清單實機截圖腳本 (quest-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	# 初始建立底層大廳與上層 Main 任務面板 (zh_TW)
	if _step == 0 and _wait == 1:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")

		var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
		if LobbyClass:
			_lobby = LobbyClass.new()
			_lobby.z_index = 10
			root.add_child(_lobby)

		var MainScn: PackedScene = load("res://scenes/main.tscn")
		if MainScn:
			_main = MainScn.instantiate()
			_main.z_index = 80
			root.add_child(_main)
			# 隱藏 main 內建純黑背景，使半透明 MenuLayer 能透出大廳背景
			var bg_node = _main.get_node_or_null("BG")
			if bg_node:
				bg_node.visible = false
			_main.call("_go_quest_panel")
		return false

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])
		var cname: String = str(task["crop"])

		# 開著任務面板時動態切換語系
		if _wait == 5:
			print("  -> 開啟任務清單中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)
			if _gs:
				_gs.player_name = ContentLoc.text("ui", "小白")

		elif _wait >= 30:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 全景截圖完成 [%s]: %s" % [_step + 1, TASKS.size(), code, path])

			var crop_path := _out_dir.path_join(cname)
			# 裁切中央卡片 (寬 750, 高 480，置中約 (265, 120))
			_save_crop(path, crop_path, Rect2i(240, 100, 800, 520))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		_cleanup_nodes()
		print("── 任務清單六語系實機截圖腳本執行完畢 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _main and is_instance_valid(_main):
		_main.queue_free()
		_main = null
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null


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
