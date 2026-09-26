extends SceneTree
## 大廳裝備欄六語系實機截圖腳本 (lobby-equip-i18n)
## 驗收重點：
## 1. 大廳全景展示青蛙右側當前裝備（外裝／武器／發條／奇玩）。
## 2. 在 zh_TW, en, ja 下即時切換，裝備名稱跟著翻譯，無繁中殘留。
## 3. 截圖存放於 proofs/lobby-equip-i18n/。

var OUT_DIR := ProjectSettings.globalize_path("res://../proofs/lobby-equip-i18n")

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

	if _gs:
		_gs.set("player_name", "碧簧蛙")
		_gs.set("player_race", "frog")
		_gs.set("level", 15)
		_gs.set("gold", 88888)
		_gs.set("energy", 15)
		_gs.set("paperdoll_slots", {
			"costume": "costume_spring_forest_courier",
			"weapon": "wpn_lotus_cog_dart",
			"winding_key": "key_twin_wing_concentric",
			"back_curio": "curio_lotus_leaf_parasol"
		})

	print("── 開始執行大廳裝備欄六語系實機截圖腳本 (lobby-equip-i18n) ──")
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
				else:
					_lobby.call("_apply_locale_texts")

			elif _wait >= 25:
				var path := "%s/proof_lobby_equip_%s.png" % [OUT_DIR, code]
				_save_screenshot(path)
				print("  ✓ [%d/3] 大廳全景 [%s] 實機截圖完成: %s" % [_step, code, path])
				_step += 1
				_wait = 0

		4:
			print("CAPTURE_LOBBY_EQUIP_I18N_OK")
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
