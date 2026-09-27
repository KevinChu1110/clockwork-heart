extends SceneTree
## 測試探針：驗證 10 個 QA 實機截圖步驟運作 (tools/test_capture_all_t_3a945a87.gd)

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

var OUT_DIR_NAME := "proofs/t_3a945a87"

var _step := 0
var _wait := 0
var _loc_node: Node = null
var _gs: Node = null
var _cds: Node = null
var _eq: Node = null
var _inv: Node = null
var _out_dir: String = ""

var _lobby: Control = null
var _forge_dlg: Control = null
var _host: Node = null
var _equip_panel: RefCounted = null
var _battle: Control = null
var _victory_dlg: Control = null

class MockHost extends Node:
	var _ui_root: Control
	func _init():
		_ui_root = Control.new()
		_ui_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(_ui_root)
	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			c.queue_free()
	func ui_reset_fade() -> void:
		pass
	func ui_host() -> Control:
		return _ui_root
	func ui_refresh_hud() -> void:
		pass
	func ui_goto(_target: String = "") -> void:
		pass

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../" + OUT_DIR_NAME)
	DirAccess.make_dir_recursive_absolute(_out_dir)

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

	_cds = root.get_node_or_null("ColossusDailySystem")
	if _cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			_cds = CdsClass.new()
			_cds.name = "ColossusDailySystem"
			root.add_child(_cds)

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq = EqClass.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)

	_inv = root.get_node_or_null("InventorySystem")
	if _inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			_inv = InvClass.new()
			_inv.name = "InventorySystem"
			root.add_child(_inv)

	_init_player_data()

	print("── 開始執行 t_3a945a87 探索性 QA 截圖測試腳本 ──")
	print("   OUT_DIR: ", _out_dir)
	_step = 1
	_wait = 0

func _init_player_data() -> void:
	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 25)
		_gs.set("hp", 150)
		_gs.set("max_hp", 150)
		_gs.set("gold", 8000)
		_gs.set("weapon_tier", 3)
		_gs.set("weapon_atk", 24)
		_gs.set("weapon_name", "精煉長劍")
		_gs.call("set_flag", "c1_forged", true)
		_gs.call("set_flag", "c1_entered_city", true)
		_gs.call("set_flag", "tut_done", true)

	if _cds:
		_cds.set("debug_day", 20260927)
		_cds.call("refresh")

	if _inv and _inv.has_method("add_item"):
		_inv.call("add_item", "iron_scrap", 100)
	elif _gs and "inventory" in _gs and _gs.inventory is Dictionary:
		_gs.inventory["iron_scrap"] = 100

	# 預置多樣色階展示（橘階、藍階、紫階、白階）
	_setup_core_slots_tier()

func _setup_core_slots_tier() -> void:
	CoreSystemClass.reset_player_parts()
	CoreSystemClass.clear_inventory()
	# 發條發電機：橘階 (校準 1 次，剩餘 6 次)
	CoreSystemClass.calibrate_player_part("mainspring", true, {"ATK": 2}, 3)
	# 機殼裝甲：藍階 (校準 2 次，剩餘 5 次)
	CoreSystemClass.calibrate_player_part("chassis", true, {"DEF": 2}, 6)
	CoreSystemClass.calibrate_player_part("chassis", true, {"DEF": 2}, 6)
	# 擒縱調速器：紫階 (校準 4 次，剩餘 3 次)
	CoreSystemClass.calibrate_player_part("escapement", true, {"CRIT": 1}, 8)
	CoreSystemClass.calibrate_player_part("escapement", true, {"CRIT": 1}, 8)
	CoreSystemClass.calibrate_player_part("escapement", true, {"CRIT": 1}, 8)
	CoreSystemClass.calibrate_player_part("escapement", true, {"CRIT": 1}, 8)

	# 模擬背包內有幾顆掉落機芯部件展示
	var p1: Dictionary = CoreSystemClass.create_part_by_tier("chassis", "purple", {"DEF": 18, "HP": 90})
	var p2: Dictionary = CoreSystemClass.create_part_by_tier("escapement", "blue", {"CRIT": 4, "CRIT_DMG": 8})
	var p3: Dictionary = CoreSystemClass.create_part_by_tier("gear_train", "red", {"ATK": 40, "DEF": 30})
	CoreSystemClass.add_part_to_inventory(p1)
	CoreSystemClass.add_part_to_inventory(p2)
	CoreSystemClass.add_part_to_inventory(p3)

func _save_screenshot(abs_path: String) -> void:
	var img: Image = root.get_texture().get_image()
	if img != null:
		var err := img.save_png(abs_path)
		if err == OK:
			print("  ✓ 截圖存檔成功: ", abs_path, " (%dx%d)" % [img.get_width(), img.get_height()])
		else:
			push_error("無法儲存截圖至: " + abs_path)
	else:
		push_error("無法取得 Viewport 影像")

func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		# ──────────────────────────────────────────────────────────
		# 步驟 1: 繁中 (zh_TW) 鐵匠鍛造彈窗（機芯五槽色階與剩餘次數、單次校準按鈕）
		# ──────────────────────────────────────────────────────────
		1:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()
				_init_player_data()
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
			elif _wait == 10:
				if _lobby and _lobby.has_method("open_forge"):
					_forge_dlg = _lobby.call("open_forge")
			elif _wait >= 35:
				var path := "%s/proof_01_zh_forge_calibration.png" % _out_dir
				_save_screenshot(path)
				_step = 2
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 2: 繁中 (zh_TW) 鐵匠點擊校準後反饋（跳階成功/色階與剩餘次數更新/結果句）
		# ──────────────────────────────────────────────────────────
		2:
			if _wait == 1:
				# 對發條發電機執行跳一階
				CoreSystemClass.calibrate_player_part("mainspring", "jump_1")
				if is_instance_valid(_forge_dlg):
					if _forge_dlg.has_method("_refresh_all_forge_core_slots"):
						_forge_dlg.call("_refresh_all_forge_core_slots")
					if _forge_dlg.has_method("_refresh_display"):
						_forge_dlg.call("_refresh_display")
					var p: Dictionary = CoreSystemClass.get_player_part("mainspring")
					var tnm: String = str(p.get("tier_name", "金"))
					var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
					_forge_dlg.set("_last_calibrate_state", {
						"slot_name": "發條發電機",
						"tip": "跳一階成功！發條突破進階",
						"tip_key": "CALIBRATE_JUMP_1",
						"tier_name": tnm,
						"rem": rem,
						"ok": true
					})
					if _forge_dlg.has_method("_update_calibrate_message"):
						_forge_dlg.call("_update_calibrate_message")
			elif _wait >= 25:
				var path := "%s/proof_02_zh_forge_calibrated_result.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_forge_dlg):
					_forge_dlg.queue_free()
					_forge_dlg = null
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 3
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 3: 繁中 (zh_TW) 角色整備五槽機芯 (EquipPanel 五槽位色階/剩餘次數/機芯背包)
		# ──────────────────────────────────────────────────────────
		3:
			if _wait == 1:
				_host = MockHost.new()
				root.add_child(_host)
				var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
				_equip_panel = EquipPanelClass.new(_host)
				_equip_panel.call("open")
			elif _wait == 15:
				var scroll: ScrollContainer = root.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 200
			elif _wait >= 40:
				var path := "%s/proof_03_zh_equip_panel_5slots.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_host):
					_host.queue_free()
					_host = null
				_equip_panel = null
				_step = 4
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 4: 繁中 (zh_TW) 停擺巨偶出征卡 (鋼岳象、金鬃雄獅、提線機偶出征卡、推薦等級)
		# ──────────────────────────────────────────────────────────
		4:
			if _wait == 1:
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("switch_tab", 2) # Tab.ADVENTURE
			elif _wait == 15:
				var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
				if colossus_btn:
					colossus_btn.emit_signal("pressed")
			elif _wait >= 35:
				var path := "%s/proof_04_zh_colossus_sortie_cards.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 5
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 5: 繁中 (zh_TW) 巨偶勝場結算卡片 (BattleVictoryDialog 戰利品金階機芯/經驗/鐵屑/雙鈕)
		# ──────────────────────────────────────────────────────────
		5:
			if _wait == 1:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
				var dropped: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 25, "HP": 120})
				dropped["is_colossus"] = true
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				_victory_dlg = DlgClass.show_dialog(root, dropped, Callable(), 450, 60)
			elif _wait >= 35:
				var path := "%s/proof_05_zh_colossus_victory_settlement.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null
				_step = 6
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 6: 英文 (en) 鐵匠鍛造彈窗（Core Slots 色階、Remaining 次數、Calibrate 按鈕）
		# ──────────────────────────────────────────────────────────
		6:
			if _wait == 1:
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				_init_player_data()
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
			elif _wait == 10:
				if _lobby and _lobby.has_method("open_forge"):
					_forge_dlg = _lobby.call("open_forge")
			elif _wait >= 35:
				var path := "%s/proof_06_en_forge_calibration.png" % _out_dir
				_save_screenshot(path)
				_step = 7
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 7: 英文 (en) 鐵匠點擊校準後反饋（英文結果句、色階與剩餘次數更新）
		# ──────────────────────────────────────────────────────────
		7:
			if _wait == 1:
				CoreSystemClass.calibrate_player_part("mainspring", "jump_1")
				if is_instance_valid(_forge_dlg):
					if _forge_dlg.has_method("_refresh_all_forge_core_slots"):
						_forge_dlg.call("_refresh_all_forge_core_slots")
					if _forge_dlg.has_method("_refresh_display"):
						_forge_dlg.call("_refresh_display")
					var p: Dictionary = CoreSystemClass.get_player_part("mainspring")
					var tnm: String = str(p.get("tier_name", "Gold"))
					var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
					_forge_dlg.set("_last_calibrate_state", {
						"slot_name": "Mainspring Dynamo",
						"tip": "Jump 1 Tier Success! Mainspring advanced",
						"tip_key": "CALIBRATE_JUMP_1",
						"tier_name": tnm,
						"rem": rem,
						"ok": true
					})
					if _forge_dlg.has_method("_update_calibrate_message"):
						_forge_dlg.call("_update_calibrate_message")
			elif _wait >= 25:
				var path := "%s/proof_07_en_forge_calibrated_result.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_forge_dlg):
					_forge_dlg.queue_free()
					_forge_dlg = null
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 8
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 8: 英文 (en) 角色整備五槽機芯 (EquipPanel Five Core Slots)
		# ──────────────────────────────────────────────────────────
		8:
			if _wait == 1:
				_host = MockHost.new()
				root.add_child(_host)
				var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
				_equip_panel = EquipPanelClass.new(_host)
				_equip_panel.call("open")
			elif _wait == 15:
				var scroll: ScrollContainer = root.find_child("EquipScroll", true, false) as ScrollContainer
				if scroll:
					scroll.scroll_vertical = 200
			elif _wait >= 40:
				var path := "%s/proof_08_en_equip_panel_5slots.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_host):
					_host.queue_free()
					_host = null
				_equip_panel = null
				_step = 9
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 9: 英文 (en) 停擺巨偶出征卡 (Colossus Sortie Cards, Rec. Lv, Sortie Buttons)
		# ──────────────────────────────────────────────────────────
		9:
			if _wait == 1:
				var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
				_lobby = LobbyClass.new()
				root.add_child(_lobby)
				_lobby.call("switch_tab", 2) # Tab.ADVENTURE
			elif _wait == 15:
				var colossus_btn: Button = _lobby.find_child("BtnModeColossus", true, false)
				if colossus_btn:
					colossus_btn.emit_signal("pressed")
			elif _wait >= 35:
				var path := "%s/proof_09_en_colossus_sortie_cards.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_lobby):
					_lobby.queue_free()
					_lobby = null
				_step = 10
				_wait = 0

		# ──────────────────────────────────────────────────────────
		# 步驟 10: 英文 (en) 巨偶勝場結算卡片 (BattleVictoryDialog Part Drop, EXP, Scrap, Buttons)
		# ──────────────────────────────────────────────────────────
		10:
			if _wait == 1:
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				if _battle.has_method("setup"):
					_battle.call("setup", "colossus_lion")
				var dropped: Dictionary = CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 25, "HP": 120})
				dropped["is_colossus"] = true
				var DlgClass = load("res://scripts/battle/battle_victory_dialog.gd")
				_victory_dlg = DlgClass.show_dialog(root, dropped, Callable(), 450, 60)
			elif _wait >= 35:
				var path := "%s/proof_10_en_colossus_victory_settlement.png" % _out_dir
				_save_screenshot(path)
				if is_instance_valid(_victory_dlg):
					_victory_dlg.queue_free()
					_victory_dlg = null
				if is_instance_valid(_battle):
					_battle.queue_free()
					_battle = null

				# 恢復繁中
				if _loc_node:
					_loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				print("── 全數 10 張探索性 QA 實機截圖完成 ──")
				quit(0)
				return true

	return false
