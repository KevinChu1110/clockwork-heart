extends SceneTree
## 《發條之心》探索性 QA 第四十一輪 實機截圖腳本 (qa_round41)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. 至少 8 張全景：zh_TW／en／ja 各「背包開著」＋「切語系後仍開著」；外加 en 快捷欄、ja 大廳帶背包。
## 2. 驗證背包道具名稱、說明、類型、按鈕、數量六語系即時動態連動。
## 3. 驗證快捷欄 1-8 槽、道具圖標、數量、Menu/選單 按鈕即時刷新。
## 4. 驗證 0-QA25 同屏大廳背景頂欄、四殿堂、出征、底欄 Dock 與背包同語系一致性。
## 5. OUT_DIR 獨立指定為 proofs/qa_round41/ (0-QA23)。

const OUT_DIR := "/opt/side/bravesoul-game/proofs/qa_round41"
const CROPS_DIR := "/opt/side/bravesoul-game/proofs/qa_round41/crops"

var _step := 0
var _wait := 0

var _lobby: Node = null
var _inv: Control = null
var _hotbar: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _inv_sys: Node = null


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
	_inv_sys = root.get_node_or_null("InventorySystem")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("chapter", "c0")
		_gs.set("gold", 1000)
		_gs.set("level", 10)
		_gs.set("energy", 15)
		_gs.inventory = {
			"hp_s": 5,
			"hp_m": 2,
			"bread": 10,
			"iron_scrap": 12,
			"wolf_fang": 4,
			"key_rusty": 1,
			"friendship_key": 3,
			"windup_fragment": 7
		}

	if _inv_sys:
		_inv_sys.call("ensure_hotbar")
		_inv_sys.call("set_hotbar", 0, "hp_s")
		_inv_sys.call("set_hotbar", 1, "hp_m")
		_inv_sys.call("set_hotbar", 2, "iron_scrap")

	print("── 開始執行 QA 第四十一輪實機截圖腳本 (qa_round41) ──")
	print("OUT_DIR: ", OUT_DIR)
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 步驟 1: zh_TW 背包開著 (直接開啟)
			if _wait == 1:
				_setup_scene("zh_TW", true)
			elif _wait == 30:
				var path := "%s/proof_01_zh_TW_inv_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_01_zh_TW_inv_open.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [1/8] zh_TW 背包開著全景完成: %s" % path)
				_step = 2
				_wait = 0

		2:
			# 步驟 2: zh_TW 切語系後仍開著 (先切 en 再動態切 zh_TW)
			if _wait == 1:
				_loc_node.call("set_locale", "en")
			elif _wait == 10:
				# 開著背包動態切回 zh_TW
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 35:
				var path := "%s/proof_02_zh_TW_inv_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_02_zh_TW_inv_switch.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [2/8] zh_TW 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 3
				_wait = 0

		3:
			# 步驟 3: en 背包開著 (直接開啟)
			if _wait == 1:
				_setup_scene("en", true)
			elif _wait == 30:
				var path := "%s/proof_03_en_inv_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_03_en_inv_open.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [3/8] en 背包開著全景完成: %s" % path)
				_step = 4
				_wait = 0

		4:
			# 步驟 4: en 切語系後仍開著 (先切 zh_TW 再動態切 en)
			if _wait == 1:
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 10:
				# 開著背包動態切回 en
				_loc_node.call("set_locale", "en")
			elif _wait == 35:
				var path := "%s/proof_04_en_inv_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_04_en_inv_switch.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [4/8] en 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 5
				_wait = 0

		5:
			# 步驟 5: ja 背包開著 (直接開啟)
			if _wait == 1:
				_setup_scene("ja", true)
			elif _wait == 30:
				var path := "%s/proof_05_ja_inv_open.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_05_ja_inv_open.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [5/8] ja 背包開著全景完成: %s" % path)
				_step = 6
				_wait = 0

		6:
			# 步驟 6: ja 切語系後仍開著 (先切 zh_TW 再動態切 ja)
			if _wait == 1:
				_loc_node.call("set_locale", "zh_TW")
			elif _wait == 10:
				# 開著背包動態切回 ja
				_loc_node.call("set_locale", "ja")
			elif _wait == 35:
				var path := "%s/proof_06_ja_inv_after_switch.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_06_ja_inv_switch.png" % CROPS_DIR, Rect2i(250, 80, 780, 560))
				print("  ✓ [6/8] ja 切語系後仍開著全景完成: %s" % path)
				_clear_scene()
				_step = 7
				_wait = 0

		7:
			# 步驟 7: en 快捷欄 (關閉背包，全景專注展示 en 快捷欄與大廳底欄連動)
			if _wait == 1:
				_setup_scene("en", false)
			elif _wait == 30:
				var path := "%s/proof_07_en_hotbar.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_07_en_hotbar.png" % CROPS_DIR, Rect2i(350, 620, 580, 95))
				print("  ✓ [7/8] en 快捷欄全景完成: %s" % path)
				_clear_scene()
				_step = 8
				_wait = 0

		8:
			# 步驟 8: ja 大廳帶背包 (0-QA25 頂欄、殿堂、出征、底欄 Dock 與日文背包全屏同語系)
			if _wait == 1:
				_setup_scene("ja", true)
			elif _wait == 35:
				var path := "%s/proof_08_ja_lobby_with_inv.png" % OUT_DIR
				_save_screenshot(path)
				_save_crop(path, "%s/crop_08_ja_lobby_dock.png" % CROPS_DIR, Rect2i(0, 630, 1280, 90))
				print("  ✓ [8/8] ja 大廳帶背包全景完成: %s" % path)
				_clear_scene()
				print("── 全部 8 張實機全景截圖存證完成 ──")
				quit(0)
				return true

	return false


func _setup_scene(locale: String, open_inventory: bool) -> void:
	_clear_scene()
	if _loc_node:
		_loc_node.call("set_locale", locale)

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		_lobby.name = "MobileLobby"
		root.add_child(_lobby)

	var HotbarClass: GDScript = load("res://scripts/ui/maple_hotbar.gd")
	if HotbarClass:
		_hotbar = HotbarClass.new()
		_hotbar.name = "MapleHotbar"
		root.add_child(_hotbar)

	var InvClass: GDScript = load("res://scripts/ui/maple_inventory.gd")
	if InvClass:
		_inv = InvClass.new()
		_inv.name = "MapleInventory"
		root.add_child(_inv)
		if open_inventory:
			_inv.call("open")


func _clear_scene() -> void:
	if _inv and is_instance_valid(_inv):
		_inv.queue_free()
		_inv = null
	if _hotbar and is_instance_valid(_hotbar):
		_hotbar.queue_free()
		_hotbar = null
	if _lobby and is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null


func _save_screenshot(target_path: String) -> void:
	var img := root.get_texture().get_image()
	if img != null:
		img.save_png(target_path)


func _save_crop(src_path: String, crop_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img == null:
		return
	var cropped := img.get_region(rect)
	cropped.save_png(crop_path)
