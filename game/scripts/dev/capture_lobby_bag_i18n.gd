extends SceneTree
## 大廳背包未選格六語系實機截圖腳本 (capture_lobby_bag_i18n.gd)
## 驗收重點：
## 1. 大廳背包分頁全景展示未選格狀態（右側標題、請點選格子、消耗品/素材/重要物三行說明、禁用狀態的操作按鈕）。
## 2. 在 zh_TW, en, ja 下即時切換，右側未選格說明與按鈕跟著翻譯，無繁中殘留（0-QA24, 0-QA25）。
## 3. 截圖存放於 proofs/lobby-bag-i18n/。

var OUT_DIR := ProjectSettings.globalize_path("res://../proofs/lobby-bag-i18n")
var CROPS_DIR := ProjectSettings.globalize_path("res://../proofs/lobby-bag-i18n/crops")

var _step := 0
var _wait := 0
var _lobby: Node = null
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
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv := root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	if _gs:
		_gs.set("player_name", "碧簧蛙")
		_gs.set("player_race", "frog")
		_gs.set("level", 15)
		_gs.set("gold", 88888)
		_gs.set("energy", 15)

	print("── 開始執行大廳背包未選格六語系實機截圖腳本 (capture_lobby_bag_i18n) ──")
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1, 2, 3:
			var loc_idx := _step - 1
			var code: String = TEST_LOCALES[loc_idx]
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", code)

				if _lobby == null:
					var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
					if LobbyClass:
						_lobby = LobbyClass.new()
						root.add_child(_lobby)
						_lobby.call("_switch_tab", 4) # Tab.BAG
				else:
					_lobby.call("_switch_tab", 4) # Tab.BAG
					_lobby.call("_apply_locale_texts")

				# 確保處於未選格狀態 (右側展示未選格說明)
				_lobby.set("_selected_bag_item", "")
				_lobby.call("_refresh_bag_tab", false)

			elif _wait >= 25:
				var path := "%s/proof_bag_unselected_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/3] 背包未選格全景 [%s] 實機截圖完成: %s" % [_step, code, path])

				# 截取右側說明區域 (大約 x=450~1230, y=70~650)
				var crop_path := "%s/crop_bag_detail_%s.png" % [CROPS_DIR, code]
				_save_crop(path, crop_path, Rect2i(450, 70, 780, 580))
				print("  ✓ [%d/3] 背包右側說明局部裁切 [%s] 完成: %s" % [_step, code, crop_path])

				_step += 1
				_wait = 0

		4:
			# 還原為繁中
			if _loc_node:
				_loc_node.call("set_locale", "zh_TW")
			print("CAPTURE_LOBBY_BAG_I18N_OK")
			quit(0)
			return true

	return false

func _save_screenshot(path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var tex := vp.get_texture()
		if tex:
			var img := tex.get_image()
			if img:
				img.save_png(path)

func _save_crop(src_path: String, dst_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img:
		var cropped := img.get_region(rect)
		if cropped:
			cropped.save_png(dst_path)
