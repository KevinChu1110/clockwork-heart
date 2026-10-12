extends SceneTree
## 《發條之心》雙分支合併主線全面回歸驗收截圖存證腳本 (t_eac1c7dc)
## 驗收對象：
## 1. agent/20261012-maple-inventory-core-replace-t_ba3e60c1 (探索背包機芯頁籤與替換彈窗)
## 2. agent/20261012-lobby-core-auto-equip-t_791dc011 (大廳角色頁機芯一鍵配置)
## 執行指令：xvfb-run -a godot --path game --rendering-driver opengl3 -s res://../tools/capture_regression_t_eac1c7dc.gd

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const MapleInventoryScript = preload("res://scripts/ui/maple_inventory.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const OUT_PATHS: Array[String] = [
	"/opt/side/bravesoul-game/proofs/t_eac1c7dc",
	"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_eac1c7dc/bravesoul-game/proofs/t_eac1c7dc"
]

var _step: int = 0
var _frame: int = 0
var _wait: int = 0
var _gs: Node = null
var _loc: Node = null
var _cs: Node = null
var _lobby: Control = null
var _inv: Control = null
var _hashes: Dictionary = {}


func _initialize() -> void:
	print("== 開始執行 t_eac1c7dc 雙分支合併主線全面回歸實機截圖驗收 ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	for p in OUT_PATHS:
		DirAccess.make_dir_recursive_absolute(p)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv_sys = root.get_node_or_null("InventorySystem")
	if inv_sys == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv_sys = InvClass.new()
			inv_sys.name = "InventorySystem"
			root.add_child(inv_sys)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	_step = 1
	_frame = 0


func _save_viewport(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return
	for p in OUT_PATHS:
		var target := p.path_join(filename)
		img.save_png(target)
		var h := FileAccess.get_sha256(target)
		_hashes[filename] = h
		print("  [CAPTURE] 已儲存: %s (SHA256: %s)" % [target, h.substr(0, 16)])


func _process(_delta: float) -> bool:
	_frame += 1
	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		1:
			# 初始化大廳角色頁與機芯部件
			print("\n--- 階段 1: 大廳角色頁展示五大機芯槽位與一鍵配置按鈕 ---")
			CoreSystemClass.clear_inventory()
			_gs.ensure_core_slots("white")

			var p_mainspring := CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 20, "CRIT": 3.0})
			var p_chassis := CoreSystemClass.create_part_by_tier("chassis", "blue", {"DEF": 15, "HP": 50})
			var p_escapement := CoreSystemClass.create_part_by_tier("escapement", "purple", {"ATK": 15, "DEF": 10})
			var p_gear := CoreSystemClass.create_part_by_tier("gear_train", "green", {"ATK": 35, "CRIT": 5.0})
			var p_soul := CoreSystemClass.create_part_by_tier("soul_core", "red", {"ATK": 50, "DEF": 30})

			CoreSystemClass.add_part_to_inventory(p_mainspring)
			CoreSystemClass.add_part_to_inventory(p_chassis)
			CoreSystemClass.add_part_to_inventory(p_escapement)
			CoreSystemClass.add_part_to_inventory(p_gear)
			CoreSystemClass.add_part_to_inventory(p_soul)

			_lobby = MobileLobbyScript.new()
			root.add_child(_lobby)
			_lobby.call("_switch_tab", 1) # Tab.CHARACTER
			_lobby.call("_refresh_char_core_slots")
			_lobby.call("refresh_hud")
			_wait = 15
			_step = 2

		2:
			# 截圖 1: 大廳角色頁五大機芯槽位與一鍵配置按鈕
			_save_viewport("proof_01_char_core_slots_auto_equip_btn_zh_tw.png")
			# 執行一鍵配置
			_lobby.auto_equip_cores()
			_wait = 3
			_step = 3

		3:
			# 截圖 2: 一鍵配置後高階機芯全數換上、飄字戰力提升提示
			_save_viewport("proof_02_char_core_auto_equipped_power_boost_zh_tw.png")
			_lobby.queue_free()
			_lobby = null
			_wait = 10
			_step = 4

		4:
			# 階段 3: 探索背包 MapleInventory 點選機芯分類 Chip 與選取機芯
			print("\n--- 階段 2: MapleInventory 探索背包機芯頁籤與替換機芯按鈕 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys:
				inv_sys.call("register_item", "test_core_part_1", {"name": "測試發條", "kind": "core"})
				inv_sys.call("add_item", "test_core_part_1", 1)

			_inv = MapleInventoryScript.new()
			root.add_child(_inv)
			_inv.open()
			_inv.call("set_category", "core")
			_inv.call("_on_cell", 0, MOUSE_BUTTON_LEFT)
			_wait = 15
			_step = 5

		5:
			# 截圖 3: MapleInventory 機芯 Chip 列、部件卡片與替換機芯按鈕
			_save_viewport("proof_03_maple_inventory_core_chip_filtered_zh_tw.png")
			# 點擊替換機芯彈出 CoreReplaceDialog
			var replace_btn: Button = _inv.call("get_replace_core_button")
			if replace_btn:
				replace_btn.pressed.emit()
			_wait = 10
			_step = 6

		6:
			# 截圖 4: 直通連動 CoreReplaceDialog 比較確認彈窗
			_save_viewport("proof_04_maple_inventory_core_replace_dialog_zh_tw.png")
			# 切換至英文語系
			print("\n--- 階段 3: 英文 (en) 多語系驗證 ---")
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_inv.call("_on_locale_changed", "en")
			_inv.call("refresh")
			_wait = 10
			_step = 7

		7:
			# 截圖 5: 英文語系 MapleInventory Core 頁籤與替換彈窗
			_save_viewport("proof_05_maple_inventory_core_en.png")
			_inv.queue_free()
			_inv = null
			# 切換至日文語系並開啟大廳
			print("\n--- 階段 4: 日文 (ja) 多語系驗證 ---")
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "ja")
			_lobby = MobileLobbyScript.new()
			root.add_child(_lobby)
			_lobby.call("_switch_tab", 1) # Tab.CHARACTER
			_lobby.call("_on_locale_changed", "ja")
			_wait = 15
			_step = 8

		8:
			# 點擊機芯槽位彈出 CoreReplaceDialog (日文)
			_lobby.call("_on_char_core_slot_clicked", "mainspring")
			_wait = 10
			_step = 9

		9:
			# 截圖 6: 日文語系 CoreReplaceDialog 比較確認彈窗
			_save_viewport("proof_06_lobby_core_replace_dialog_ja.png")
			print("\n=== 全部 6 張主線全面回歸截圖存證完成 ===")
			print("截圖 SHA256 清單:")
			for k in _hashes:
				print("  - %s: %s" % [k, _hashes[k]])
			quit(0)
			return true

	return false
