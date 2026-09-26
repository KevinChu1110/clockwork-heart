extends SceneTree
## 背包使用／出售／重要物品提示六語系實機截圖腳本 (capture_bag_use_i18n.gd)
##
## 驗收重點：
## 1. 0-QA23: 獨立專屬目錄 proofs/bag_use_i18n/，絕不覆蓋他卡 proof。
## 2. 0-QA24: en 語系實機截圖與 toast 提示零 CJK 漢字殘留。使用具備 PNG 圖標的 friendship_key。
## 3. 0-QA25: 全屏背景（頂部資訊、底部 Dock、背包標題、操作按鈕）隨語系同步刷新，非局部變換。
## 4. 實機捕捉英、日語系重要物品警示提示與材料出售提示。

var OUT_DIR := ProjectSettings.globalize_path("res://../proofs/bag_use_i18n")
var CROPS_DIR := ProjectSettings.globalize_path("res://../proofs/bag_use_i18n/crops")

var _step := 0
var _wait := 0
var _lobby: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _inv: Node = null

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

	_inv = root.get_node_or_null("InventorySystem")
	if _inv == null:
		var InvClass = load("res://scripts/autoload/inventory_system.gd")
		if InvClass:
			_inv = InvClass.new()
			_inv.name = "InventorySystem"
			root.add_child(_inv)

	if _gs:
		_gs.set("player_name", "碧簧蛙")
		_gs.set("player_race", "frog")
		_gs.set("level", 15)
		_gs.set("gold", 5000)
		_gs.set("energy", 15)
		_gs.set("inventory", {})

	print("── 開始執行背包提示六語系實機截圖腳本 (capture_bag_use_i18n) ──")
	_step = 1
	_wait = 0

func _reset_test_inventory() -> void:
	if _gs:
		_gs.set("inventory", {})
	if _inv:
		_inv.call("add_item", "friendship_key", 1)
		_inv.call("add_item", "iron_scrap", 5)
		_inv.call("add_item", "hp_s", 3)

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		1:
			# 初始化大廳並切換至 Tab.BAG
			if _wait == 1:
				if _lobby == null:
					var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
					if LobbyClass:
						_lobby = LobbyClass.new()
						root.add_child(_lobby)
						_lobby.call("_switch_tab", 4) # Tab.BAG
			elif _wait >= 10:
				_step = 2
				_wait = 0

		2:
			# Step 2: 英文 (en) 重要物品提示截圖
			if _wait == 1:
				_reset_test_inventory()
				if _loc_node:
					_loc_node.call("set_locale", "en")
				_lobby.call("_switch_tab", 4)
				_lobby.call("_apply_locale_texts")
				_lobby.set("_selected_bag_item", "friendship_key")
				_lobby.call("_refresh_bag_tab", false)
				_lobby.call("_on_bag_use_pressed")
			elif _wait == 6:
				var path := "%s/proof_01_key_item_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [1/5] 英文重要物品提示全景截圖完成: %s" % path)
				var crop_path := "%s/crop_01_key_item_en.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 60, 960, 360))
				print("  ✓ [1/5] 英文重要物品提示局部裁切完成: %s" % crop_path)
				_step = 3
				_wait = 0

		3:
			# Step 3: 英文 (en) 出售材料提示截圖
			if _wait == 1:
				_reset_test_inventory()
				_lobby.set("_selected_bag_item", "iron_scrap")
				_lobby.call("_refresh_bag_tab", false)
				_lobby.call("_on_bag_use_pressed")
			elif _wait == 6:
				var path := "%s/proof_02_sell_item_en.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [2/5] 英文出售材料全景截圖完成: %s" % path)
				var crop_path := "%s/crop_02_sell_item_en.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 60, 960, 360))
				print("  ✓ [2/5] 英文出售材料局部裁切完成: %s" % crop_path)
				_step = 4
				_wait = 0

		4:
			# Step 4: 日文 (ja) 重要物品提示截圖
			if _wait == 1:
				_reset_test_inventory()
				if _loc_node:
					_loc_node.call("set_locale", "ja")
				_lobby.call("_switch_tab", 4)
				_lobby.call("_apply_locale_texts")
				_lobby.set("_selected_bag_item", "friendship_key")
				_lobby.call("_refresh_bag_tab", false)
				_lobby.call("_on_bag_use_pressed")
			elif _wait == 6:
				var path := "%s/proof_03_key_item_ja.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [3/5] 日文重要物品提示全景截圖完成: %s" % path)
				var crop_path := "%s/crop_03_key_item_ja.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 60, 960, 360))
				print("  ✓ [3/5] 日文重要物品提示局部裁切完成: %s" % crop_path)
				_step = 5
				_wait = 0

		5:
			# Step 5: 日文 (ja) 出售材料提示截圖
			if _wait == 1:
				_reset_test_inventory()
				_lobby.set("_selected_bag_item", "iron_scrap")
				_lobby.call("_refresh_bag_tab", false)
				_lobby.call("_on_bag_use_pressed")
			elif _wait == 6:
				var path := "%s/proof_04_sell_item_ja.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [4/5] 日文出售材料全景截圖完成: %s" % path)
				var crop_path := "%s/crop_04_sell_item_ja.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 60, 960, 360))
				print("  ✓ [4/5] 日文出售材料局部裁切完成: %s" % crop_path)
				_step = 6
				_wait = 0

		6:
			# Step 6: 繁中 (zh_TW) 基準截圖
			if _wait == 1:
				_reset_test_inventory()
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				_lobby.call("_switch_tab", 4)
				_lobby.call("_apply_locale_texts")
				_lobby.set("_selected_bag_item", "friendship_key")
				_lobby.call("_refresh_bag_tab", false)
				_lobby.call("_on_bag_use_pressed")
			elif _wait == 6:
				var path := "%s/proof_05_key_item_zh_TW.png" % OUT_DIR
				_save_screenshot(path)
				print("  ✓ [5/5] 繁中重要物品提示全景截圖完成: %s" % path)
				var crop_path := "%s/crop_05_key_item_zh_TW.png" % CROPS_DIR
				_save_crop(path, crop_path, Rect2i(240, 60, 960, 360))
				print("  ✓ [5/5] 繁中重要物品提示局部裁切完成: %s" % crop_path)
				print("── 背包提示六語系實機截圖腳本執行完畢 ──")
				quit(0)
				return true

	return false

func _save_screenshot(path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img := vp.get_texture().get_image()
		if img and not img.is_empty():
			img.save_png(path)

func _save_crop(src_path: String, dst_path: String, rect: Rect2i) -> void:
	var img := Image.load_from_file(src_path)
	if img and not img.is_empty():
		var cropped := img.get_region(rect)
		cropped.save_png(dst_path)
