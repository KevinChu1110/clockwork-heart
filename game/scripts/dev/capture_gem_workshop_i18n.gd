extends SceneTree
## 手藝工坊六語系實機截圖存證 (en / ja 熔煉全景 + 寶石櫃全景)
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_gem_workshop_i18n.gd
##
## 依 review.md 0-QA23、0-QA24、0-QA25 規範：
## 1. OUT_DIR 只准寫入 proofs/gem-workshop-i18n/，絕不覆蓋其它卡片 proof。
## 2. en 與 ja 各截取一張熔煉分頁全景、一張寶石櫃分頁全景，共 4 張全景圖。
## 3. 大廳連動切換語系，確保背景大廳/Dock 同步呈現該語系。

var _step := 0
var _wait := 0
var _main: Node = null
var _lobby: Node = null
var _current_dlg: Control = null
var _loc: Node = null

var OUT_DIR := ""
var CROPS_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/gem-workshop-i18n")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行手藝工坊六語系實機截圖腳本 (gem-workshop-i18n) ──")


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
			# 等待主場景加載穩定並初始化測試環境
			if _wait >= 40:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.set("level", 25)
					gs.set("gold", 8800)
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)

				var gem_sys: Node = root.get_node_or_null("GemSystem")
				if gem_sys and gem_sys.has_method("add_shards"):
					gem_sys.call("add_shards", "red", 5)
					gem_sys.call("add_shards", "yellow", 2)
					gem_sys.call("add_shards", "blue", 4)
					gem_sys.call("add_gem", "red", 1, 2)
					gem_sys.call("add_gem", "red", 2, 1)
					gem_sys.call("add_gem", "blue", 1, 3)

				_loc = root.get_node_or_null("Loc")

				_lobby = root.find_child("MobileLobby", true, false)
				if _lobby == null and _main != null:
					_lobby = _main.find_child("MobileLobby", true, false)

				print("  [截圖] 1. 切換至 en 語系...")
				if _loc:
					_loc.call("set_locale", "en")

				_step = 1
				_wait = 0

		1:
			# 等待大廳切換 en 穩定後開啟手藝工坊
			if _wait >= 25:
				if _lobby and _lobby.has_method("open_gem_workshop"):
					_current_dlg = _lobby.call("open_gem_workshop")
				else:
					var GemClass = load("res://scripts/ui/gem_workshop_dialog.gd")
					_current_dlg = GemClass.new()
					root.add_child(_current_dlg)
				_step = 2
				_wait = 0

		2:
			# 截取 en 熔煉分頁全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_gem_workshop_smelt_en.png"
				_save_screenshot(path)
				print("  ✓ en 熔煉頁完成，切換至 en 寶石櫃頁...")
				var tab_case: Button = _current_dlg.find_child("TabCaseBtn", true, false)
				if tab_case:
					tab_case.pressed.emit()
				_step = 3
				_wait = 0

		3:
			# 截取 en 寶石櫃分頁全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_gem_workshop_case_en.png"
				_save_screenshot(path)
				print("  ✓ en 寶石櫃頁完成，關閉彈窗準備切換 ja...")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
					_current_dlg = null
				_step = 4
				_wait = 0

		4:
			# 切換至 ja 語系
			if _wait >= 25:
				print("  [截圖] 2. 切換至 ja 語系...")
				if _loc:
					_loc.call("set_locale", "ja")
				_step = 5
				_wait = 0

		5:
			# 等待大廳切換 ja 穩定後開啟手藝工坊
			if _wait >= 25:
				if _lobby and _lobby.has_method("open_gem_workshop"):
					_current_dlg = _lobby.call("open_gem_workshop")
				else:
					var GemClass = load("res://scripts/ui/gem_workshop_dialog.gd")
					_current_dlg = GemClass.new()
					root.add_child(_current_dlg)
				_step = 6
				_wait = 0

		6:
			# 截取 ja 熔煉分頁全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_gem_workshop_smelt_ja.png"
				_save_screenshot(path)
				print("  ✓ ja 熔煉頁完成，切換至 ja 寶石櫃頁...")
				var tab_case: Button = _current_dlg.find_child("TabCaseBtn", true, false)
				if tab_case:
					tab_case.pressed.emit()
				_step = 7
				_wait = 0

		7:
			# 截取 ja 寶石櫃分頁全景
			if _wait >= 30:
				var path := OUT_DIR + "/proof_gem_workshop_case_ja.png"
				_save_screenshot(path)
				print("  ✓ ja 寶石櫃頁完成，產生局部特寫 Crops...")
				if _current_dlg and is_instance_valid(_current_dlg):
					_current_dlg.call("_on_close")
					_current_dlg = null
				_generate_crops()
				if _loc:
					_loc.call("set_locale", "zh_TW")
				_step = 8
				_wait = 0

		8:
			print("CAPTURE_GEM_WORKSHOP_I18N_OK")
			quit(0)
			return true

	return false


func _generate_crops() -> void:
	# 裁切重要特寫部位供比對
	# 彈窗區域約 X: 265~1015, Y: 70~650 (750x580)
	for lang in ["en", "ja"]:
		var smelt_path := OUT_DIR + "/proof_gem_workshop_smelt_%s.png" % lang
		if FileAccess.file_exists(smelt_path):
			var img := Image.load_from_file(smelt_path)
			if img:
				# 標題與分頁 (X:265~1015, Y:70~160)
				var crop_head := img.get_region(Rect2i(265, 70, 750, 95))
				crop_head.save_png(CROPS_DIR + "/crop_header_%s.png" % lang)

				# 熔煉卡片與主按鈕 (X:275~1005, Y:220~540)
				var crop_cards := img.get_region(Rect2i(275, 220, 730, 320))
				crop_cards.save_png(CROPS_DIR + "/crop_smelt_cards_%s.png" % lang)

		var case_path := OUT_DIR + "/proof_gem_workshop_case_%s.png" % lang
		if FileAccess.file_exists(case_path):
			var img := Image.load_from_file(case_path)
			if img:
				# 寶石櫃操作按鈕 (X:680~1005, Y:360~430)
				var crop_case_actions := img.get_region(Rect2i(680, 360, 325, 70))
				crop_case_actions.save_png(CROPS_DIR + "/crop_case_actions_%s.png" % lang)

				# 六維總加成面板 (X:275~1005, Y:260~360)
				var crop_bonus := img.get_region(Rect2i(275, 260, 730, 100))
				crop_bonus.save_png(CROPS_DIR + "/crop_case_bonus_%s.png" % lang)
