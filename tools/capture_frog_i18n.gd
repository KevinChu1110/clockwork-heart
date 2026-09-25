extends SceneTree
## 碧箸蛙玩家可見名稱六語系落地實機截圖腳本 (frog-i18n)
## 驗收重點：
## 1. 創角擴充分頁選碧箸蛙，展示【碧箸蛙】、【忍者】、【碧箸巡林客工裝】、【原廠薄荷翡翠綠】在 zh_TW, en, ja 下即時切換。
## 2. 衣櫥選用碧箸蛙外裝／塗裝標籤，在大廳背景與底部 Dock 連動下（0-QA25），在 zh_TW, en, ja 下即時切換。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/frog-i18n"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/frog-i18n/crops"

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

	print("── 開始執行碧箸蛙六語系落地實機截圖腳本 (frog-i18n) ──")
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			# 步驟 1~3: 創角介面 (PaperdollSelectDemo) 擴充分頁選碧箸蛙 (zh_TW, en, ja)
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
				var demo_packed: PackedScene = load("res://scenes/ui/paperdoll_select_demo.tscn")
				if demo_packed:
					var demo = demo_packed.instantiate()
					demo.set("creation_mode", true)
					root.add_child(demo)
					demo.call("switch_tab", "expansion")
					demo.call("select_race", "frog")
					demo.call("reset_to_default")
					_current_node = demo
			elif _wait >= 35:
				var path := "%s/proof_creation_frog_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 創角介面選碧箸蛙 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		4, 5, 6:
			# 步驟 4~6: 大廳開啟衣櫥 (WardrobeDialog)，篩選「蛙」展示工裝與塗裝標籤，背景大廳與 Dock 同步切換語系 (0-QA25)
			var loc_idx := _step - 4
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)
				if _gs:
					_gs.call("reset_new_game", "frog")
					_gs.set("player_name", "碧箸蛙")
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					var lobby = LobbyClass.new()
					root.add_child(lobby)
					_current_node = lobby
			elif _wait == 15:
				if _current_node and _current_node.has_method("open_wardrobe"):
					_current_node.call("open_wardrobe")
					var wardrobe = _current_node.find_child("WardrobeDialog", true, false)
					if wardrobe and wardrobe.has_method("set_race_filter"):
						wardrobe.call("set_race_filter", "frog")
			elif _wait >= 40:
				var path := "%s/proof_wardrobe_frog_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/6] 大廳連動衣櫥蛙族標籤 [%s] 實機截圖完成: %s" % [_step, code, path])
				if _current_node:
					_current_node.queue_free()
					_current_node = null
				_step += 1
				_wait = 0

		7:
			# 截圖全部完成，產生局部 Crops 供顯微比對
			_generate_crops()
			print("── 碧箸蛙六語系落地實機截圖全數完成 ──")
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
	# 裁切創角右側資訊面板文字區 (X:760~1260, Y:120~550) 驗證四詞
	for code in TEST_LOCALES:
		var c_path := "%s/proof_creation_frog_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(c_path):
			var img := Image.load_from_file(c_path)
			if img and not img.is_empty():
				var crop := img.get_region(Rect2i(760, 100, 500, 480))
				var crop_p := "%s/crop_creation_info_%s.png" % [CROPS_DIR, code]
				crop.save_png(crop_p)
				print("  [Crop] 創角文字特寫 [%s]: %s" % [code, crop_p])

		# 裁切衣櫥卡片標籤與左側徽章區 (X:180~700, Y:180~560)
		var w_path := "%s/proof_wardrobe_frog_%s.png" % [OUT_DIR, code]
		if FileAccess.file_exists(w_path):
			var img := Image.load_from_file(w_path)
			if img and not img.is_empty():
				var crop := img.get_region(Rect2i(220, 150, 700, 450))
				var crop_p := "%s/crop_wardrobe_cards_%s.png" % [CROPS_DIR, code]
				crop.save_png(crop_p)
				print("  [Crop] 衣櫥卡片特寫 [%s]: %s" % [code, crop_p])
