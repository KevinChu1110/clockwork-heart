extends SceneTree
## 《發條之心》探索性 QA 第四十二輪 實機截圖腳本 (qa_round42)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 至少 6 張全景：zh_TW／en／ja 各「商城開著」＋「切語系後仍開著」；外加 en/ja 背景大廳連動全景。
## 2. 驗證商城 3 個 IAP 佔位品項名稱、說明、按鈕六語系即時動態連動。
## 3. 驗證 +15、×10、金幣 500、NT$ 標不變，TODO 定價待定佔位符符合規範保留。
## 4. 驗證 0-QA25 同屏大廳背景頂欄、四殿堂、出征、底欄 Dock 與商城同語系一致性，無半中半英。
## 5. OUT_DIR 獨立指定為 proofs/qa_round42/ (0-QA23)。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round42"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round42/crops"

var _step := 0
var _wait := 0

var _lobby: Control = null
var _shop: Control = null
var _loc_node: Node = null
var _gs: Node = null


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute(CROPS_DIR)

	# 清理舊檔確保 0-QA23 獨立目錄
	_clean_dir(CROPS_DIR)
	_clean_dir(OUT_DIR)

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
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c0")
		_gs.set("gold", 1000)
		_gs.set("level", 10)
		_gs.set("energy", 8)
		_gs.set("has_removed_ads", false)

	print("── 開始執行 QA 第四十二輪實機截圖腳本 (qa_round42) ──")
	print("OUT_DIR: ", OUT_DIR)
	_step = 1
	_wait = 0


func _clean_dir(path: String) -> void:
	var dir := DirAccess.open(path)
	if dir != null:
		dir.list_dir_begin()
		var file_name := dir.get_next()
		while file_name != "":
			if not dir.current_is_dir():
				dir.remove(file_name)
			file_name = dir.get_next()


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: zh_TW 商城開著 (直接開啟)
			if _wait == 1:
				_setup_scene("zh_TW", true)
			elif _wait == 30:
				var path := "%s/proof_01_zh_TW_shop_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_01_zh_TW_shop_open.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [1/8] zh_TW 商城開著全景完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: zh_TW 切語系後仍開著 (先切 en 再動態切 zh_TW)
			if _wait == 1:
				_loc_node.call("set_locale", "en")
			elif _wait == 10:
				# 開著商城動態切回 zh_TW
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 35:
				var path := "%s/proof_02_zh_TW_shop_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_02_zh_TW_shop_switch.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [2/8] zh_TW 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 3
				_wait = 0

		3:
			# 步驟 3: en 商城開著 (直接開啟)
			if _wait == 1:
				_setup_scene("en", true)
			elif _wait == 30:
				var path := "%s/proof_03_en_shop_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_03_en_shop_open.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [3/8] en 商城開著全景完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: en 切語系後仍開著 (先切 zh_TW 再動態切 en)
			if _wait == 1:
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 10:
				# 開著商城動態切回 en
				_loc_node.call("set_locale", "en")
			elif _wait == 35:
				var path := "%s/proof_04_en_shop_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_04_en_shop_switch.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [4/8] en 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 5
				_wait = 0

		5:
			# 步驟 5: ja 商城開著 (直接開啟)
			if _wait == 1:
				_setup_scene("ja", true)
			elif _wait == 30:
				var path := "%s/proof_05_ja_shop_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_05_ja_shop_open.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [5/8] ja 商城開著全景完成: %s" % path)
				_step = 6
				_wait = 0

		6:
			# 步驟 6: ja 切語系後仍開著 (先切 zh_TW 再動態切 ja)
			if _wait == 1:
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 10:
				# 開著商城動態切回 ja
				_loc_node.call("set_locale", "ja")
			elif _wait == 35:
				var path := "%s/proof_06_ja_shop_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_06_ja_shop_switch.png" % CROPS_DIR, Rect2i(160, 60, 960, 600))
				print("  ✓ [6/8] ja 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 7
				_wait = 0

		7:
			# 步驟 7: en 大廳頂欄與商城連動特寫檢驗
			if _wait == 1:
				_setup_scene("en", true)
			elif _wait == 30:
				var path := "%s/proof_07_en_shop_detail.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_07_en_lobby_top_dock.png" % CROPS_DIR, Rect2i(0, 0, 1280, 90))
				print("  ✓ [7/8] en 大廳頂欄與商城連動全景完成: %s" % path)
				_clear_scene()
				_step = 8
				_wait = 0

		8:
			# 步驟 8: ja 大廳帶商城全景 (0-QA25 頂欄、出征、底欄ぜんまい新村與日文商城全屏同語系)
			if _wait == 1:
				_setup_scene("ja", true)
			elif _wait == 30:
				var path := "%s/proof_08_ja_lobby_with_shop.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_08_ja_lobby_dock.png" % CROPS_DIR, Rect2i(0, 630, 1280, 90))
				print("  ✓ [8/8] ja 大廳帶商城全景完成: %s" % path)
				_clear_scene()
				print("── 全部 8 張實機全景截圖存證完成 ──")
				quit(0)
				return true

	return false


func _setup_scene(locale: String, open_shop_now: bool) -> void:
	_clear_scene()
	if _loc_node:
		_loc_node.call("set_locale", locale)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)

	if open_shop_now and _lobby:
		_shop = _lobby.open_shop()


func _clear_scene() -> void:
	if _shop and is_instance_valid(_shop):
		_shop.queue_free()
		_shop = null
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null


func _save_screenshot(target_path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		var err := img.save_png(target_path)
		if err != OK:
			push_error("save_png failed err=%d: %s" % [err, target_path])
	else:
		push_error("root texture is null for %s" % target_path)


func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null:
		push_error("load_from_file failed for %s" % src_path)
		return
	var cropped := img.get_region(rect)
	var err := cropped.save_png(crop_path)
	if err != OK:
		push_error("save_crop failed err=%d: %s" % [err, crop_path])
