extends SceneTree
## 背包物品欄六語系落地實機截圖腳本 (inventory-i18n)
## 依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
## 驗收重點：
## 1. en / ja 背包物品欄全景共 2 張。
## 2. 標題／主按鈕／操作提示／類型說明已翻；零破圖、零截字、零系統 emoji、零舊 IP。
## 3. 大廳背景與底部 Dock 連動同步切換語系 (0-QA25)。
## 4. OUT_DIR 只准 proofs/inventory-i18n/ (0-QA23)。

var _out_dir: String = ""
var _step := 0
var _wait := 0
var _current_lobby: Node = null
var _current_inv: Control = null
var _loc_node: Node = null
var _gs: Node = null
var _inv_sys: Node = null

const TASKS := [
	{"loc": "en", "file": "proof_inventory_en.png"},
	{"loc": "ja", "file": "proof_inventory_ja.png"},
]


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/inventory-i18n")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc_node = root.get_node_or_null("Loc")
	_gs = root.get_node_or_null("GameState")
	_inv_sys = root.get_node_or_null("InventorySystem")

	print("── 開始執行背包物品欄實機截圖腳本 (inventory-i18n) ──")
	print("OUT_DIR: ", _out_dir)
	_step = 0
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1

	if _step < TASKS.size():
		var task: Dictionary = TASKS[_step]
		var code: String = str(task["loc"])
		var fname: String = str(task["file"])

		if _wait == 1:
			if _loc_node:
				_loc_node.call("set_locale", code)
			if _gs:
				_gs.call("reset_new_game", "rabbit")
				_gs.set("player_name", "小白")

			if _inv_sys:
				_inv_sys.call("add_item", "hp_m", 3)
				_inv_sys.call("add_item", "iron_scrap", 5)
				_inv_sys.call("add_item", "bread", 2)
				_inv_sys.call("add_item", "friendship_key", 1)

			# 建立底層大廳，使彈窗背後之大廳與 Dock 一併呈現同語系 (0-QA25)
			var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
			if LobbyClass:
				_current_lobby = LobbyClass.new()
				root.add_child(_current_lobby)

			var MapleInvClass: GDScript = load("res://scripts/ui/maple_inventory.gd")
			if MapleInvClass:
				_current_inv = MapleInvClass.new()
				_current_inv.z_index = 80
				root.add_child(_current_inv)
				_current_inv.call("open")
				# 選取 iron_scrap 呈現素材類型翻譯
				_current_inv.set("_selected", "iron_scrap")
				_current_inv.call("refresh")

		elif _wait >= 25:
			var path := _out_dir.path_join(fname)
			_save_screenshot(path)
			print("  ✓ [%d/2] 背包物品欄 [%s] 實機截圖完成: %s" % [_step + 1, code, path])

			_cleanup_nodes()
			_step += 1
			_wait = 0
	else:
		if _loc_node:
			_loc_node.call("set_locale", "zh_TW")
		print("── 背包物品欄 2 張全景截圖全數完成 ──")
		quit(0)
		return true

	return false


func _cleanup_nodes() -> void:
	if _current_inv and is_instance_valid(_current_inv):
		_current_inv.queue_free()
		_current_inv = null
	if _current_lobby and is_instance_valid(_current_lobby):
		_current_lobby.queue_free()
		_current_lobby = null


func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_viewport().get_texture().get_image()
	if img:
		if img.get_size() != Vector2i(1280, 720):
			img.resize(1280, 720, Image.INTERPOLATE_LANCZOS)
		img.save_png(abs_path)
