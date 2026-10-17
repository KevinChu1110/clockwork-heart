extends SceneTree

# test_batch_dual_shortcuts_t_22043c6f.gd
# 驗證 ForgeDialog 前往背包 (t_41201712) 與 大廳聚魂殿堂前往商城 (t_9e0be8e9) 雙分支合併主線之完整性 (t_22043c6f)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _finished := false
var _exit_code := 0
var _step := 0
var _wait := 0

var _gs: Node = null
var _loc: Node = null
var _lobby: Control = null
var _forge: Control = null

func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 前往背包 與 聚魂殿堂前往商城 雙快捷主線合併回歸驗收測試 (t_22043c6f) ===")

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	# 1. 驗證 ForgeDialog 前往背包快捷 (t_41201712)
	print("\n--- 1. 驗證 ForgeDialog 前往背包快捷按鈕 (BtnGoInventory, t_41201712) ---")
	var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
	_forge = ForgeClass.new()
	root.add_child(_forge)
	if not _forge.is_node_ready() and _forge.has_method("_build_ui"):
		_forge.call("_build_ui")

	var inv_btn = _forge.get_go_inventory_button() if _forge.has_method("get_go_inventory_button") else null
	if inv_btn == null:
		inv_btn = _forge.find_child("BtnGoInventory", true, false)
	assert(inv_btn != null, "ForgeDialog 找不到 BtnGoInventory")
	assert(inv_btn.custom_minimum_size.y >= 48.0, "ForgeDialog BtnGoInventory 高度需 >= 48px")
	assert(_forge.has_signal("inventory_requested") or _forge.has_signal("go_inventory"), "ForgeDialog 缺少前往背包信號")
	print("  ✓ ForgeDialog BtnGoInventory 存在、熱區合規且信號完備: ", inv_btn.custom_minimum_size)
	_forge.queue_free()

	# 2. 驗證 MobileLobby 聚魂殿堂前往商城快捷 (BtnGoShop, t_9e0be8e9)
	print("\n--- 2. 驗證 MobileLobby 聚魂殿堂前往商城快捷按鈕 (BtnGoShop, t_9e0be8e9) ---")
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = LobbyClass.new()
	root.add_child(_lobby)

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 6:
				return false
			if _lobby.has_method("open_soul_hall"):
				_lobby.call("open_soul_hall")

			var shop_btn = _lobby.get_soul_hall_go_shop_btn() if _lobby.has_method("get_soul_hall_go_shop_btn") else null
			if shop_btn == null:
				shop_btn = _lobby.find_child("BtnGoShop", true, false)
			assert(shop_btn != null, "MobileLobby 聚魂殿堂找不到 BtnGoShop")
			assert(shop_btn.custom_minimum_size.y >= 48.0, "聚魂殿堂 BtnGoShop 高度需 >= 48px")
			print("  ✓ MobileLobby 聚魂殿堂 BtnGoShop 存在且熱區合規: ", shop_btn.custom_minimum_size)

			# 驗證 open_forge / open_maple_inventory / open_shop
			assert(_lobby.has_method("open_forge"), "MobileLobby 需具備 open_forge")
			assert(_lobby.has_method("open_maple_inventory"), "MobileLobby 需具備 open_maple_inventory")
			assert(_lobby.has_method("open_shop"), "MobileLobby 需具備 open_shop")
			print("  ✓ MobileLobby open_forge / open_maple_inventory / open_shop 彈窗連動函式完備")

			# 3. 驗證 ShopDialog 前往聚魂雙向閉環信號與按鈕
			print("\n--- 3. 驗證 ShopDialog 前往聚魂與相關快捷按鈕完備性 ---")
			var ShopClass = load("res://scripts/ui/shop_dialog.gd")
			var shop = ShopClass.new()
			root.add_child(shop)
			if not shop.is_node_ready() and shop.has_method("_build_ui"):
				shop.call("_build_ui")

			var soul_btn = shop.get_go_soul_hall_button() if shop.has_method("get_go_soul_hall_button") else null
			if soul_btn == null and shop.has_method("get_soul_hall_button"):
				soul_btn = shop.get_soul_hall_button()
			if soul_btn == null:
				soul_btn = shop.find_child("BtnGoSoulHall", true, false)
			assert(soul_btn != null, "ShopDialog 找不到 BtnGoSoulHall 閉環按鈕")
			assert(soul_btn.custom_minimum_size.y >= 48.0, "ShopDialog BtnGoSoulHall 高度需 >= 48px")
			print("  ✓ ShopDialog BtnGoSoulHall 存在且熱區合規: ", soul_btn.custom_minimum_size)
			shop.queue_free()

			# 4. 六語系 key 檢查
			print("\n--- 4. 驗證六語系 i18n 鍵值存在性 ---")
			var required_keys = [
				"forge.btn_go_inventory",
				"soul_hall.btn_go_shop",
				"shop.btn_go_soul_hall"
			]
			for loc_code in LOCALES:
				if _loc != null and _loc.has_method("set_locale"):
					_loc.call("set_locale", loc_code)
				for k in required_keys:
					var tr_val: String = _loc.call("t", k) if _loc != null else ""
					assert(tr_val != "" and tr_val != k, "語系 [%s] 缺少 key: %s" % [loc_code, k])
					print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])

			print("\n========================================================")
			print("TEST_BATCH_DUAL_SHORTCUTS_REGRESSION_OK")
			print("========================================================")
			_finished = true
			_exit_code = 0
			quit(0)
			return true

	return false
