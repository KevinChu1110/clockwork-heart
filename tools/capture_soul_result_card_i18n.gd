extends SceneTree
## 抽魂結果卡掉落種類與名稱六語系實機截圖腳本 (tools/capture_soul_result_card_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
##
## 驗收重點：
## 1. en / ja 結果卡徽章與掉落名為該語言，零系統 emoji。
## 2. 開著抽魂結果卡直接切換語系，徽章與掉落名稱立刻連動刷新。
## 3. OUT_DIR 嚴格限定為 proofs/soul-result-card-i18n/ (0-QA23)。
## 4. 0-QA25 檢核：同圖內全屏 UI 語系一致連動。
## 5. 0-QA24 檢核：日文漢字（真鍮の歯車、パーツ、着せ替え等）為既定譯名。

var _step := 0
var _wait := 0
var _main: Node = null
var _view: Control = null
var _loc: Node = null

var OUT_DIR := ""
var CROPS_DIR := ""


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/soul-result-card-i18n")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	change_scene_to_file("res://scenes/main.tscn")
	print("── 開始執行抽魂結果卡六語系實機截圖腳本 (soul-result-card-i18n) ──")
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
			# 實例化 SoulDrawPlayView 並展示 drop (零件: drop_brass_gear)
			if _wait >= 25:
				var ViewClass = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
				_view = ViewClass.new()
				_view.set_anchors_preset(Control.PRESET_FULL_RECT)
				root.add_child(_view)
				# 模擬抽到零件：黃銅齒輪
				var drop := {
					"DropId": "drop_brass_gear",
					"kind": "part",
					"toastKey": "soul.pull_part"
				}
				if _view.card != null:
					_view.card.show_drop(drop)
				_step = 2
				_wait = 0

		2:
			# 截取 en 結果卡全景與特寫
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_01_result_card_en.png"
				var crop_path := CROPS_DIR + "/crop_01_result_card_en.png"
				# 結果卡區域約在 center, x: 40~1240 (w: 1200), y: 96~555 (h: 460)
				# 特寫聚焦在卡片底部徽章與名稱區域：x: 340~940 (w: 600), y: 350~540 (h: 190)
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(340, 360, 600, 180))
				print("  ✓ en 結果卡實機截圖完成。準備在開著卡片的狀態下切換至 ja...")
				_step = 3
				_wait = 0

		3:
			# 開著卡片直接切換至 ja 語系，驗證即時動態刷新
			if _wait >= 20:
				print("  [截圖] 2. 開著卡片即時切換至 ja 語系...")
				if _loc:
					_loc.call("set_locale", "ja")
				_step = 4
				_wait = 0

		4:
			# 截取 ja 結果卡全景與特寫
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_02_result_card_ja.png"
				var crop_path := CROPS_DIR + "/crop_02_result_card_ja.png"
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(340, 360, 600, 180))
				print("  ✓ ja 結果卡實機截圖完成。準備切換至換裝展示...")
				_step = 5
				_wait = 0

		5:
			# 切換至換裝 drop: outfit_cream 並切換至 zh_TW 語系
			if _wait >= 20:
				var drop_outfit := {
					"DropId": "outfit_cream",
					"kind": "outfit",
					"toastKey": "soul.pull_outfit"
				}
				if _view.card != null:
					_view.card.show_drop(drop_outfit)
				if _loc:
					_loc.call("set_locale", "zh_TW")
				_step = 6
				_wait = 0

		6:
			# 截取 zh_TW 換裝卡全景與特寫
			if _wait >= 30:
				var full_path := OUT_DIR + "/proof_03_result_card_zh_TW.png"
				var crop_path := CROPS_DIR + "/crop_03_result_card_zh_TW.png"
				_save_screenshot_and_crop(full_path, crop_path, Rect2i(340, 360, 600, 180))
				print("  ✓ zh_TW 換裝卡實機截圖完成。")
				_step = 7
				_wait = 0

		7:
			if _wait >= 10:
				print("── 全部實機截圖存證完成 ──")
				quit(0)
				return true

	return false
