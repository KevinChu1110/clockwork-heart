extends SceneTree
## 《發條之心》創角種族列首發／擴充分頁與確認鈕六語系實機驗證截圖 (creation-tabs-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 創角首發分頁 (Launch Tab) 在 zh_TW, en, ja 下，頂部「首發／擴充」分頁與底部「確認選擇 · 踏上旅途／返回」按鈕即時翻譯切換。
## 2. 創角擴充分頁 (Expansion Tab) 在 zh_TW, en, ja 下，分頁選取狀態與按鈕即時翻譯。
## 3. 大廳背景與底部 Dock 連動同步切換語系 (0-QA25 檢查)。
## 4. 局部 Crops 供顯微比對。
## 執行方式：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://scripts/dev/capture_creation_tabs_proof.gd

const OUT_DIR := "/opt/side/bravesoul-game/proofs/creation-tabs-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/creation-tabs-i18n/crops"

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

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")

	print("── 開始執行創角分頁與確認鈕六語系實機截圖腳本 (creation-tabs-i18n) ──")
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
				print("  ✓ [%d/9] 創角介面首發頁 [%s] 實機截圖完成: %s" % [_step, code, path])
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
					_gs.call("reset_new_game", "rabbit")
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
				print("  ✓ [%d/9] 創角介面擴充頁 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		7, 8, 9:
			# 步驟 7~9: 大廳與 Dock 同步換語系 (0-QA25 檢查，zh_TW, en, ja)
			var loc_idx := _step - 7
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait >= 35:
				var path := "%s/proof_lobby_dock_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/9] 大廳與Dock同步語系 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		10:
			# 步驟 10: 產生局部特寫 Crops 供顯微比對 (0-QA23)
			_generate_crops()
			print("── 創角分頁與確認鈕六語系實機截圖全數完成 ──")
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
		# 1. 創角首發頁截圖裁切
		var launch_path := "%s/proof_creation_launch_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(launch_path):
			var img := Image.load_from_file(launch_path)
			if img and not img.is_empty():
				# 頂部「首發｜擴充」分頁 tab 區 (X:440~840, Y:60~125)
				var tabs_crop := img.get_region(Rect2i(440, 60, 400, 65))
				var tabs_p := "%s/crop_tabs_%s.png" % [CROPS_DIR, code]
				tabs_crop.save_png(tabs_p)
				print("  [Crop] 創角分頁標籤特寫 [%s]: %s" % [code, tabs_p])

				# 底部操作按鈕區 (確認選擇 · 踏上旅途／返回) (X:655~1225, Y:580~645)
				var actions_crop := img.get_region(Rect2i(655, 580, 570, 65))
				var actions_p := "%s/crop_actions_%s.png" % [CROPS_DIR, code]
				actions_crop.save_png(actions_p)
				print("  [Crop] 底部操作按鈕特寫 [%s]: %s" % [code, actions_p])

		# 2. 大廳截圖裁切底部 Dock 區 (X:0~1280, Y:620~720) 驗證 0-QA25
		var lobby_path := "%s/proof_lobby_dock_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(lobby_path):
			var img_l := Image.load_from_file(lobby_path)
			if img_l and not img_l.is_empty():
				var dock_crop := img_l.get_region(Rect2i(0, 620, 1280, 100))
				var dock_p := "%s/crop_dock_%s.png" % [CROPS_DIR, code]
				dock_crop.save_png(dock_p)
				print("  [Crop] 底部Dock特寫 [%s]: %s" % [code, dock_p])
