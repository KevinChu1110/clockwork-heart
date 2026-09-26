extends SceneTree
## W8 Hub 殼玩家可見字六語系實機截圖腳本 (tools/capture_w8_hub_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
##
## 驗收重點：
## 1. en / ja 實機全景各一張，且 proof 目錄只用本輪資料夾 proofs/w8-hub-i18n/ (0-QA23)。
## 2. 開著 W8 Hub 畫面切換語系，橫幅、章節資訊、按鈕、提示即時刷新 (0-QA25)。
## 3. 日文漢字（玩具の山の縁、初回クリアと掃討等）對齊既定譯名 (0-QA24)。
## 4. 零系統 emoji。

var _step := 0
var _wait := 0
var _hub: Control = null
var _loc: Node = null

var OUT_DIR := ""
var CROPS_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/w8-hub-i18n")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行 W8 Hub 六語系實機截圖腳本 (w8-hub-i18n) ──")
	print("OUT_DIR: ", OUT_DIR)


func _save_screenshot_and_crop(full_path: String, crop_path: String, crop_rect: Rect2i) -> void:
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

	var err := img.save_png(full_path)
	if err != OK:
		push_error("save_png failed err=%d: %s" % [err, full_path])
	else:
		print("    [Saved Full] %s (%dx%d)" % [full_path, img.get_width(), img.get_height()])

	var cropped := img.get_region(crop_rect)
	if cropped and not cropped.is_empty():
		var cerr := cropped.save_png(crop_path)
		if cerr != OK:
			push_error("save crop failed err=%d: %s" % [cerr, crop_path])
		else:
			print("    [Saved Crop] %s (%dx%d)" % [crop_path, cropped.get_width(), cropped.get_height()])


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			# 等待主場景初始化完畢
			if _wait >= 40:
				_loc = root.get_node_or_null("Loc")
				print("  [截圖] 1. 切換至 en 語系...")
				if _loc:
					_loc.call("set_locale", "en")

				var HubClass = load("res://scripts/systems/wave8/w8_hub_view.gd")
				_hub = HubClass.new()
				_hub.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_hub)
				_hub.call("_goto", 2) # Phase.CHAPTER

				_step = 1
				_wait = 0

		1:
			# 等待 en 畫面穩定
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_01_w8_hub_chapter_en.png"
				var crop_path := CROPS_DIR + "/crop_01_w8_hub_chapter_en.png"
				# 裁切聚焦在橫幅與主要按鈕區域
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(20, 10, 1240, 680))
				print("  ✓ en 全景截圖完成。準備在畫面上切換至 ja...")
				_step = 2
				_wait = 0

		2:
			# 動態切換至 ja (locale_changed)
			print("  [截圖] 2. 動態切換至 ja 語系...")
			if _loc:
				_loc.call("set_locale", "ja")
			_step = 3
			_wait = 0

		3:
			# 等待 ja 畫面連動刷新穩定
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_02_w8_hub_chapter_ja.png"
				var crop_path := CROPS_DIR + "/crop_02_w8_hub_chapter_ja.png"
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(20, 10, 1240, 680))
				print("  ✓ ja 全景截圖完成。準備切換回 zh_TW 對照...")
				_step = 4
				_wait = 0

		4:
			# 動態切回 zh_TW
			print("  [截圖] 3. 動態切換回 zh_TW 繁中...")
			if _loc:
				_loc.call("set_locale", "zh_TW")
			_step = 5
			_wait = 0

		5:
			# 等待 zh_TW 畫面還原穩定
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_03_w8_hub_chapter_zh_TW.png"
				var crop_path := CROPS_DIR + "/crop_03_w8_hub_chapter_zh_TW.png"
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(20, 10, 1240, 680))
				print("  ✓ zh_TW 對照截圖完成。全部截圖流程完畢！")

				print("\n=======================================================")
				print("W8_HUB_I18N_CAPTURE_SUCCESS")
				quit(0)
				return true

	return false
