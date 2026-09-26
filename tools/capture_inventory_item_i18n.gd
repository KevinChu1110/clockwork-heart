extends SceneTree
## 背包道具名稱與說明六語系實機全景截圖腳本 (tools/capture_inventory_item_i18n.gd)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja / zh_TW 實機全景截圖（1280x720），呈現 0-QA25 同屏大廳背景、快捷欄與背包彈窗同語系連動。
## 2. 背包彈窗開啟中直接切換語系，格子名稱 tooltip、選中明細名稱與說明、類型標籤、操作按鈕立即刷新。
## 3. OUT_DIR 嚴格限定本輪 proofs/inventory-item-i18n/ (0-QA23)。

var _out_dir: String = ""
var _crops_dir: String = ""
var _step := 0
var _wait := 0

var _current_lobby: Node = null
var _current_inv: Control = null
var _current_hotbar: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _inv_sys: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_01_inventory_item_en.png", "crop": "crops/crop_01_inventory_item_en.png"},
	{"loc": "ja", "file": "proof_02_inventory_item_ja.png", "crop": "crops/crop_02_inventory_item_ja.png"},
	{"loc": "zh_TW", "file": "proof_03_inventory_item_zh_TW.png", "crop": "crops/crop_03_inventory_item_zh_TW.png"},
]

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/inventory-item-i18n")
	_crops_dir = _out_dir.path_join("crops")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_crops_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_inv_sys = root.get_node_or_null("InventorySystem")

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		# 預先設置背包道具，展示不同類型（消耗品、素材、重要物）
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

	print("── 開始執行背包道具名稱與說明六語系實機截圖腳本 (inventory-item-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	# 初始建立底層大廳、快捷欄與背包彈窗 (zh_TW)
	if _step == 0 and _wait == 1:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")

		var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
		if LobbyClass:
			_current_lobby = LobbyClass.new()
			_current_lobby.name = "MobileLobby"
			root.add_child(_current_lobby)

		var HotbarClass: GDScript = load("res://scripts/ui/maple_hotbar.gd")
		if HotbarClass:
			_current_hotbar = HotbarClass.new()
			_current_hotbar.name = "MapleHotbar"
			root.add_child(_current_hotbar)

		var InvClass: GDScript = load("res://scripts/ui/maple_inventory.gd")
		if InvClass:
			_current_inv = InvClass.new()
			_current_inv.name = "MapleInventory"
			root.add_child(_current_inv)
			_current_inv.call("open")
		return false

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])
		var cname: String = str(task["crop"])

		# 在背包開著的狀態下動態切換語系
		if _wait == 5:
			print("  -> 開啟背包中切換語系至: ", code)
			if _loc_node:
				_loc_node.call("set_locale", code)

		elif _wait >= 35:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/%d] 全景截圖完成 [%s]: %s" % [_step + 1, TASKS.size(), code, path])

			var crop_path := _out_dir.path_join(cname)
			# 裁切中央背包彈窗與明細區 (寬 750, 高 540，置中約 (265, 90))
			_save_crop(path, crop_path, Rect2i(250, 80, 780, 560))
			print("  ✓ [%d/%d] 局部裁切完成 [%s]: %s" % [_step + 1, TASKS.size(), code, crop_path])

			_step += 1
			_wait = 0
		return false

	print("── 全部實機截圖存證完成 ──")
	quit(0)
	return true


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
