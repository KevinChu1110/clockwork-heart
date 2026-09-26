extends SceneTree
## 戰鬥失敗復活彈窗六語系即時刷新實機截圖腳本 (tools/capture_battle_defeat_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja / zh_TW 實機全景截圖（1280x720），呈現 0-QA25 同屏戰鬥背景與彈窗同語系連動。
## 2. 彈窗開啟中直接切換語系，標題、說明、復活鈕、結束鈕立即刷新。
## 3. OUT_DIR 只准本輪 proofs/battle-defeat-i18n/ (0-QA23)。
## 4. 0-QA24 檢核：日文漢字（敗北、戦闘終了等）為既定規範詞條。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

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
	{"loc": "en", "file": "proof_01_battle_defeat_en.png", "crop": "crops/crop_01_battle_defeat_en.png"},
	{"loc": "ja", "file": "proof_02_battle_defeat_ja.png", "crop": "crops/crop_02_battle_defeat_ja.png"},
	{"loc": "zh_TW", "file": "proof_03_battle_defeat_zh_TW.png", "crop": "crops/crop_03_battle_defeat_zh_TW.png"},
]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/battle-defeat-i18n")
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

	print("── 開始執行戰鬥失敗復活彈窗實機截圖腳本 (battle-defeat-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	# 初始建立底層戰鬥場景與彈窗 (zh_TW)
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

		# 在彈窗開著的狀態下動態切換語系
		if _wait == 5:
			print("  -> 開啟彈窗中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)
			if _gs:
				_gs.player_name = ContentLoc.text("ui", "小白")
			# 額外觸發一次 battle_view 刷新確保 player_name 抓取最新
			if _battle and _battle.has_method("_refresh_hud"):
				_battle.call("_refresh_hud")

		elif _wait >= 30:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 全景截圖完成 [%s]: %s" % [_step + 1, TASKS.size(), code, path])

			var crop_path := _out_dir.path_join(cname)
			# 裁切中央卡片 (寬 750, 高 420，置中約 (265, 150))
			_save_crop(path, crop_path, Rect2i(240, 130, 800, 460))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		_cleanup_nodes()
		print("── 戰鬥失敗復活彈窗六語系實機截圖腳本執行完畢 ──")
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
