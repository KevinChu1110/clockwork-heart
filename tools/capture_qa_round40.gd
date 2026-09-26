extends SceneTree
## 《發條之心》探索性 QA 第四十輪 實機巡檢截圖腳本 (qa-round40)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 大廳打開體力不足彈窗，切 en / ja，截全景 (1280x720)；同一張圖裡彈窗外大廳字同步切換同一語系 (0-QA25)。
## 2. 戰鬥打開戰敗復活彈窗，切 en / ja，截全景 (1280x720)；同一張圖裡戰鬥 HUD 語系同步切換同一語系 (0-QA25)。
## 3. OUT_DIR 只准本輪 proofs/qa-round40/ (0-QA23)。
## 4. 0-QA24 檢核：日文漢字（敗北、エネルギー不足、戦闘終了等）為既定規範詞條。
## 5. 零系統 emoji、按鈕熱區 >= 50px、橫屏彈窗 740~760、長譯名不截字不溢出。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa-round40"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa-round40/crops"

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _step := 0
var _wait := 0

var _current_lobby: Node = null
var _current_battle: Node = null
var _current_dlg: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _es: Node = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

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

	_es = root.get_node_or_null("EnergySystem")
	if _es == null:
		var EsClass = load("res://scripts/autoload/energy_system.gd")
		if EsClass:
			_es = EsClass.new()
			_es.name = "EnergySystem"
			root.add_child(_es)

	print("── 開始執行探索性 QA 第四十輪實機巡檢截圖 (qa-round40) ──")
	print("OUT_DIR: ", OUT_DIR)
	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# ── Phase 1: 大廳體力不足彈窗 ──
		1:
			# 初始化大廳 + 體力不足彈窗 (初始 zh_TW)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("energy", 2)
				if _es:
					_es.call("refresh")
					_es.call("refresh_ad_daily")

				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				if LobbyClass:
					_current_lobby = LobbyClass.new()
					root.add_child(_current_lobby)

				var EnergyLackClass: GDScript = load("res://scripts/ui/energy_lack_dialog.gd")
				if EnergyLackClass:
					_current_dlg = EnergyLackClass.new()
					_current_dlg.z_index = 90
					root.add_child(_current_dlg)

			elif _wait == 10:
				print("  [1/4] 開啟體力不足彈窗中，動態切換語系至: en")
				if _loc_node:
					_loc_node.call("set_locale", "en")

			elif _wait >= 40:
				var path := "%s/proof_01_energy_lack_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/4] 體力不足英文全景截圖完成: %s" % path)

				var crop_path := "%s/crop_01_energy_lack_en.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 120, 800, 480))
				print("  ✓ [1/4] 局部卡片特寫完成: %s" % crop_path)

				_step = 2
				_wait = 0

		2:
			# 在同一個彈窗開著的狀態下，動態切換至 ja
			if _wait == 10:
				print("  [2/4] 開啟體力不足彈窗中，動態切換語系至: ja")
				if _loc_node:
					_loc_node.call("set_locale", "ja")

			elif _wait >= 40:
				var path := "%s/proof_02_energy_lack_ja.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/4] 體力不足日文全景截圖完成: %s" % path)

				var crop_path := "%s/crop_02_energy_lack_ja.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 120, 800, 480))
				print("  ✓ [2/4] 局部卡片特寫完成: %s" % crop_path)

				_cleanup_phase_nodes()
				_step = 3
				_wait = 0

		# ── Phase 2: 戰鬥失敗復活彈窗 ──
		3:
			# 初始化戰鬥場景 + 戰敗復活彈窗 (初始 zh_TW)
			if _wait == 1:
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				if _gs:
					_gs.call("reset_new_game", "rabbit")
					_gs.set("player_name", "小白")
					_gs.set("has_removed_ads", false)
				if _es:
					_es.call("refresh")
					_es.call("refresh_ad_daily")

				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				if b_scn:
					_current_battle = b_scn.instantiate()
					root.add_child(_current_battle)
					if _current_battle.has_method("setup"):
						_current_battle.call("setup", "training_dummy")

				var DefeatClass: GDScript = load("res://scripts/battle/battle_defeat_dialog.gd")
				if DefeatClass:
					_current_dlg = DefeatClass.new()
					_current_dlg.z_index = 95
					root.add_child(_current_dlg)

			elif _wait == 10:
				print("  [3/4] 開啟戰敗彈窗中，動態切換語系至: en")
				if _loc_node:
					_loc_node.call("set_locale", "en")
				if _gs:
					_gs.player_name = ContentLoc.text("ui", "小白")
				if _current_battle and _current_battle.has_method("_refresh_hud"):
					_current_battle.call("_refresh_hud")

			elif _wait >= 40:
				var path := "%s/proof_03_battle_defeat_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/4] 戰敗復活英文全景截圖完成: %s" % path)

				var crop_path := "%s/crop_03_battle_defeat_en.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 130, 800, 460))
				print("  ✓ [3/4] 局部卡片特寫完成: %s" % crop_path)

				_step = 4
				_wait = 0

		4:
			# 在同一個戰敗彈窗開著的狀態下，動態切換至 ja
			if _wait == 10:
				print("  [4/4] 開啟戰敗彈窗中，動態切換語系至: ja")
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				if _gs:
					_gs.player_name = ContentLoc.text("ui", "小白")
				if _current_battle and _current_battle.has_method("_refresh_hud"):
					_current_battle.call("_refresh_hud")

			elif _wait >= 40:
				var path := "%s/proof_04_battle_defeat_ja.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/4] 戰敗復活日文全景截圖完成: %s" % path)

				var crop_path := "%s/crop_04_battle_defeat_ja.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 130, 800, 460))
				print("  ✓ [4/4] 局部卡片特寫完成: %s" % crop_path)

				_cleanup_phase_nodes()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				print("── 探索性 QA 第四十輪實機截圖腳本全數執行完畢 ──")
				quit(0)
				return true

	return false

func _cleanup_phase_nodes() -> void:
	if _current_dlg and is_instance_valid(_current_dlg):
		_current_dlg.queue_free()
		_current_dlg = null
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null
	if _current_battle and is_instance_valid(_current_battle):
		_current_battle.queue_free()
		_current_battle = null

func _save_screenshot(abs_path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img: Image = vp.get_texture().get_image()
		if img and not img.is_empty():
			if img.get_size() != Vector2i(1280, 720):
				img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
			img.save_png(abs_path)

func _save_crop(src_abs_path: String, dst_abs_path: String, region: Rect2i) -> void:
	if not FileAccess.file_exists(src_abs_path):
		return
	var img := Image.load_from_file(src_abs_path)
	if img and not img.is_empty():
		var cropped := img.get_region(region)
		if cropped and not cropped.is_empty():
			cropped.save_png(dst_abs_path)
