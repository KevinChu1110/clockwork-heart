extends SceneTree
## 聚魂殿抽魂畫面六語系實機截圖存證 (en / ja 全景)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_soul_draw_i18n.gd
##
## 依 review.md 0-QA23、0-QA24、0-QA25 規範：
## 1. OUT_DIR 只准寫入 proofs/soul-draw-i18n/，絕不覆蓋其它卡片 proof。
## 2. en 與 ja 各截取一張抽魂主畫面全景，共 2 張全景圖。
## 3. 大廳環境連動切換語系。

var _step := 0
var _wait := 0
var _main: Node = null
var _current_view: Control = null
var _loc: Node = null

var OUT_DIR := ""
var CROPS_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/soul-draw-i18n")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行抽魂畫面六語系實機截圖腳本 (soul-draw-i18n) ──")


func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		push_error("Cannot get viewport")
		return
	var tex := vp.get_texture()
	if tex == null:
		push_error("Cannot get texture")
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		push_error("Image is empty")
		return
	var err := img.save_png(abs_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, abs_path])
	else:
		print("    [Saved] %s (%dx%d)" % [abs_path, img.get_width(), img.get_height()])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待主場景加載穩定
			if _wait >= 40:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 8800)
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)

				_loc = root.get_node_or_null("Loc")

				print("  [截圖] 1. 切換至 en 語系...")
				if _loc:
					_loc.call("set_locale", "en")

				_step = 1
				_wait = 0

		1:
			# 切換 en 穩定後開啟 SoulDrawPlayView
			if _wait >= 25:
				var ViewClass = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
				_current_view = ViewClass.new()
				_current_view.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_current_view)
				_step = 2
				_wait = 0

		2:
			# 截取 en 抽魂畫面全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_soul_draw_en.png"
				_save_screenshot(path)
				print("  ✓ en 抽魂畫面全景完成，準備切換 ja...")
				if _current_view and is_instance_valid(_current_view):
					_current_view.queue_free()
					_current_view = null
				_step = 3
				_wait = 0

		3:
			# 切換至 ja 語系
			if _wait >= 25:
				print("  [截圖] 2. 切換至 ja 語系...")
				if _loc:
					_loc.call("set_locale", "ja")
				_step = 4
				_wait = 0

		4:
			# 切換 ja 穩定後開啟 SoulDrawPlayView
			if _wait >= 25:
				var ViewClass = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
				_current_view = ViewClass.new()
				_current_view.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_current_view)
				_step = 5
				_wait = 0

		5:
			# 截取 ja 抽魂畫面全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_soul_draw_ja.png"
				_save_screenshot(path)
				print("  ✓ ja 抽魂畫面全景完成，產生特寫 Crops...")
				if _current_view and is_instance_valid(_current_view):
					_current_view.queue_free()
					_current_view = null
				_generate_crops()
				if _loc:
					_loc.call("set_locale", "zh_TW")
				_step = 6
				_wait = 0

		6:
			print("CAPTURE_SOUL_DRAW_I18N_OK")
			quit(0)
			return true

	return false


func _generate_crops() -> void:
	for lang in ["en", "ja"]:
		var full_path := OUT_DIR + "/proof_soul_draw_%s.png" % lang
		if FileAccess.file_exists(full_path):
			var img := Image.load_from_file(full_path)
			if img:
				# 標題與票數列 (X:30~680, Y:15~95)
				var crop_head := img.get_region(Rect2i(30, 15, 650, 80))
				crop_head.save_png(CROPS_DIR + "/crop_header_%s.png" % lang)

				# 底部操作按鈕區 (X:440~840, Y:550~715)
				var crop_btns := img.get_region(Rect2i(440, 550, 400, 165))
				crop_btns.save_png(CROPS_DIR + "/crop_buttons_%s.png" % lang)
