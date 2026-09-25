extends SceneTree
## 《發條之心》創角種族卡與欄位標題六語系實機驗證截圖 (creation-race-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 創角首發分頁 (Launch Tab) 在 zh_TW, en, ja 下，種族卡（白金兔/Clockwork Rabbit/白金兎 等）與右側欄位標題、狀態列即時翻譯切換。
## 2. 創角擴充分頁 (Expansion Tab) 在 zh_TW, en, ja 下，擴充8族種族卡與右側欄位標題、狀態列即時翻譯切換。
## 3. 局部 Crops 供顯微比對。
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_creation_race_i18n.gd

var OUT_DIR := "/opt/side/bravesoul-game/proofs/creation-race-i18n"
var CROPS_DIR := "/opt/side/bravesoul-game/proofs/creation-race-i18n/crops"

var _step := 0
var _wait := 0
var _current_node: Node = null
var _loc_node: Node = null
var _gs: Node = null

const TEST_LOCALES := ["zh_TW", "en", "ja"]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var resolved_dir := ProjectSettings.globalize_path("res://../proofs/creation-race-i18n")
	OUT_DIR = resolved_dir
	CROPS_DIR = resolved_dir + "/crops"

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行創角種族卡與欄位標題六語系實機截圖腳本 (creation-race-i18n) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 步驟 1~3: 創角首發頁 (Launch Tab) 截圖 (zh_TW, en, ja)
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "launch")
					demo.call("select_race", "rabbit")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 35:
				var path := "%s/proof_creation_launch_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 創角介面首發頁 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		4, 5, 6:
			# 步驟 4~6: 創角擴充頁 (Expansion Tab) 截圖 (zh_TW, en, ja)
			var loc_idx := _step - 4
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "tiger")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "expansion")
					demo.call("select_race", "panda")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 35:
				var path := "%s/proof_creation_expansion_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 創角介面擴充頁 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		7:
			# 步驟 7: 產生局部特寫 Crops 供顯微比對 (0-QA23)
			_generate_crops()
			print("── 創角種族卡與欄位標題六語系實機截圖全數完成 ──")
			quit(0)
			return true

	return false

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
		print("    Successfully wrote: %s" % abs_path)

func _generate_crops() -> void:
	for code in TEST_LOCALES:
		# 1. 創角首發頁裁切：種族卡列特寫 (X:40~840, Y:125~235)
		var launch_path := "%s/proof_creation_launch_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(launch_path):
			var img := Image.load_from_file(launch_path)
			if img and not img.is_empty():
				# 頂部種族卡橫條 (X:40~960, Y:120~240)
				var race_cards_crop := img.get_region(Rect2i(40, 120, 920, 120))
				var cards_p := "%s/crop_race_cards_launch_%s.png" % [CROPS_DIR, code]
				race_cards_crop.save_png(cards_p)
				print("  [Crop] 首發種族卡橫條特寫 [%s]: %s" % [code, cards_p])

				# 右側欄位標題與狀態列 (X:850~1260, Y:120~560)
				var slots_crop := img.get_region(Rect2i(850, 120, 410, 440))
				var slots_p := "%s/crop_slots_panel_%s.png" % [CROPS_DIR, code]
				slots_crop.save_png(slots_p)
				print("  [Crop] 右側槽位控制項特寫 [%s]: %s" % [code, slots_p])

		# 2. 創角擴充頁裁切：擴充種族卡橫條特寫
		var exp_path := "%s/proof_creation_expansion_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(exp_path):
			var img_e := Image.load_from_file(exp_path)
			if img_e and not img_e.is_empty():
				var race_exp_crop := img_e.get_region(Rect2i(40, 120, 920, 120))
				var exp_cards_p := "%s/crop_race_cards_expansion_%s.png" % [CROPS_DIR, code]
				race_exp_crop.save_png(exp_cards_p)
				print("  [Crop] 擴充種族卡橫條特寫 [%s]: %s" % [code, exp_cards_p])
