extends SceneTree

# test_batch_three_shortcuts_t_944c7230.gd
# 驗證 WeaponSwapDialog (t_41078db9)、BattleVictoryDialog (t_567d8611) 與 BattleDefeatDialog (t_0bfa03fb)
# 三大快捷前往背包功能合併至主線之完整性與回歸驗收 (t_944c7230)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _step := 0
var _wait := 0

var _gs: Node = null
var _loc: Node = null
var _eq: Node = null
var _lobby: Control = null

func _initialize() -> void:
	print("=== 開始執行武器更換、關卡勝利、戰敗結算前往背包三快捷合併主線回歸驗收 (t_944c7230) ===")

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq = EqClass.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass:
		_lobby = LobbyClass.new()
		root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 6:
				return false
			_wait = 0
			_test_weapon_swap_shortcut()
			_step = 1
			return false

		1:
			_wait = 0
			_test_battle_victory_shortcut()
			_step = 2
			return false

		2:
			_wait = 0
			_test_battle_defeat_shortcut()
			_step = 3
			return false

		3:
			_wait = 0
			_test_lobby_and_locales()
			print("\n========================================================")
			print("TEST_BATCH_THREE_SHORTCUTS_REGRESSION_OK")
			print("========================================================")
			quit(0)
			return true

	return false

func _test_weapon_swap_shortcut() -> void:
	print("\n--- 1. 驗證 WeaponSwapDialog 前往背包快捷按鈕 (BtnGoInventory, t_41078db9) ---")
	var WeaponSwapClass = load("res://scripts/ui/weapon_swap_dialog.gd")
	assert(WeaponSwapClass != null, "找不到 WeaponSwapDialog 腳本")
	var ws_dialog: Control = WeaponSwapClass.new()
	root.add_child(ws_dialog)
	ws_dialog.call("setup", 0)

	var ws_btn: Button = null
	if ws_dialog.has_method("get_go_inventory_button"):
		ws_btn = ws_dialog.call("get_go_inventory_button") as Button
	if ws_btn == null:
		ws_btn = ws_dialog.find_child("BtnGoInventory", true, false) as Button
	assert(ws_btn != null, "WeaponSwapDialog 找不到 BtnGoInventory 按鈕")
	assert(ws_btn.custom_minimum_size.y >= 48.0, "WeaponSwapDialog BtnGoInventory 高度需 >= 48px")
	assert(ws_btn.custom_minimum_size.x >= 100.0, "WeaponSwapDialog BtnGoInventory 寬度需 >= 100px")
	assert(ws_dialog.has_signal("inventory_requested"), "WeaponSwapDialog 缺少 inventory_requested 信號")

	var sb := ws_btn.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb != null, "BtnGoInventory normal 樣式需為 StyleBoxFlat")
	assert(sb.border_width_bottom == 5, "BtnGoInventory 立體果凍厚底需為 5px")
	assert(sb.corner_radius_top_left >= 14, "BtnGoInventory 圓角需 >= 14px")
	print("  ✓ WeaponSwapDialog BtnGoInventory 存在、熱區 (%.1fx%.1f) 合規且樣式具備立體果凍厚底" % [ws_btn.custom_minimum_size.x, ws_btn.custom_minimum_size.y])
	ws_dialog.queue_free()

func _test_battle_victory_shortcut() -> void:
	print("\n--- 2. 驗證 BattleVictoryDialog 前往背包快捷按鈕 (BtnGoInventory, t_567d8611) ---")
	var VictoryClass = load("res://scripts/battle/battle_victory_dialog.gd")
	assert(VictoryClass != null, "找不到 BattleVictoryDialog 腳本")
	var vic_dialog = VictoryClass.new()
	vic_dialog.setup({})
	root.add_child(vic_dialog)

	var vic_btn: Button = null
	if vic_dialog.has_method("get_go_inventory_button"):
		vic_btn = vic_dialog.call("get_go_inventory_button") as Button
	if vic_btn == null:
		vic_btn = vic_dialog.find_child("BtnGoInventory", true, false) as Button
	assert(vic_btn != null, "BattleVictoryDialog 找不到 BtnGoInventory 按鈕")
	assert(vic_btn.custom_minimum_size.y >= 48.0, "BattleVictoryDialog BtnGoInventory 高度需 >= 48px")
	assert(vic_btn.custom_minimum_size.x >= 120.0, "BattleVictoryDialog BtnGoInventory 寬度需 >= 120px")
	assert(vic_dialog.has_signal("inventory_requested"), "BattleVictoryDialog 缺少 inventory_requested 信號")

	var sb := vic_btn.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb != null, "BtnGoInventory normal 樣式需為 StyleBoxFlat")
	assert(sb.border_width_bottom == 5, "BtnGoInventory 立體果凍厚底需為 5px")
	assert(sb.corner_radius_top_left >= 14, "BtnGoInventory 圓角需 >= 14px")
	print("  ✓ BattleVictoryDialog BtnGoInventory 存在、熱區 (%.1fx%.1f) 合規且信號完備" % [vic_btn.custom_minimum_size.x, vic_btn.custom_minimum_size.y])
	vic_dialog.queue_free()

func _test_battle_defeat_shortcut() -> void:
	print("\n--- 3. 驗證 BattleDefeatDialog 前往背包快捷按鈕 (BtnGoInventory, t_0bfa03fb) ---")
	var DefeatClass = load("res://scripts/battle/battle_defeat_dialog.gd")
	assert(DefeatClass != null, "找不到 BattleDefeatDialog 腳本")
	var def_dialog = DefeatClass.new()
	def_dialog.setup()
	root.add_child(def_dialog)

	var def_btn: Button = null
	if def_dialog.has_method("get_go_inventory_button"):
		def_btn = def_dialog.call("get_go_inventory_button") as Button
	if def_btn == null:
		def_btn = def_dialog.find_child("BtnGoInventory", true, false) as Button
	assert(def_btn != null, "BattleDefeatDialog 找不到 BtnGoInventory 按鈕")
	assert(def_btn.custom_minimum_size.y >= 48.0, "BattleDefeatDialog BtnGoInventory 高度需 >= 48px")
	assert(def_btn.custom_minimum_size.x >= 120.0, "BattleDefeatDialog BtnGoInventory 寬度需 >= 120px")
	assert(def_dialog.has_signal("inventory_requested"), "BattleDefeatDialog 缺少 inventory_requested 信號")

	var sb := def_btn.get_theme_stylebox("normal") as StyleBoxFlat
	assert(sb != null, "BtnGoInventory normal 樣式需為 StyleBoxFlat")
	assert(sb.border_width_bottom >= 5, "BtnGoInventory 立體果凍厚底需 >= 5px")
	assert(sb.corner_radius_top_left >= 14, "BtnGoInventory 圓角需 >= 14px")
	print("  ✓ BattleDefeatDialog BtnGoInventory 存在、熱區 (%.1fx%.1f) 合規且信號完備" % [def_btn.custom_minimum_size.x, def_btn.custom_minimum_size.y])
	def_dialog.queue_free()

func _test_lobby_and_locales() -> void:
	print("\n--- 4. 驗證 MobileLobby 支援 open_maple_inventory ---")
	assert(_lobby.has_method("open_maple_inventory"), "MobileLobby 需提供 open_maple_inventory 函式")
	_lobby.call("open_maple_inventory")
	var maple_inv = _lobby.find_child("MapleInventory", true, false)
	assert(maple_inv != null, "MobileLobby 未成功開啟 MapleInventory")
	print("  ✓ MobileLobby open_maple_inventory 驗證成功，順利呼起探索背包")

	print("\n--- 5. 驗證三功能在六語系中鍵值齊備且無缺漏 ---")
	var required_keys = [
		"weapon_swap.btn_go_inventory",
		"victory.btn_go_inventory",
		"defeat.btn_go_inventory"
	]
	for loc_code in LOCALES:
		if _loc != null and _loc.has_method("set_locale"):
			_loc.call("set_locale", loc_code)
		for k in required_keys:
			var tr_val: String = _loc.call("t", k) if _loc != null else ""
			assert(tr_val != "" and tr_val != k, "語系 [%s] 缺少 key: %s" % [loc_code, k])
			print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])
