extends SceneTree

# test_batch_shortcuts_regression.gd
# 驗證四個快捷功能在 main 上的完整性與無衝突運作

const Locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _frame := 0

func _init() -> void:
	print("=== 開始執行四快捷主線合併回歸驗收測試 (t_aa791e10) ===")

func _initialize() -> void:
	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
			gs.call("reset_new_game", "rabbit")

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	var inv_sys = root.get_node_or_null("InventorySystem")
	if inv_sys == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv_sys = InvClass.new()
			inv_sys.name = "InventorySystem"
			root.add_child(inv_sys)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 2:
		return false

	var loc = root.get_node_or_null("Loc")

	# 1. 測試 MapleInventory 中的 BtnGoShop 與 BtnGoTitleWall
	print("\n--- 1. 驗證 MapleInventory 雙快捷按鈕規格與信號 ---")
	var MapleInvClass = load("res://scripts/ui/maple_inventory.gd")
	var inv = MapleInvClass.new()
	root.add_child(inv)
	if inv.has_method("open"):
		inv.call("open")

	var btn_shop = inv.get_go_shop_button() if inv.has_method("get_go_shop_button") else null
	if btn_shop == null:
		btn_shop = inv.find_child("BtnGoShop", true, false)
	assert(btn_shop != null, "MapleInventory 找不到 BtnGoShop")
	assert(btn_shop.custom_minimum_size.y >= 48.0, "BtnGoShop 高度需 >= 48px")
	print("  ✓ MapleInventory BtnGoShop 存在且熱區合規: ", btn_shop.custom_minimum_size)

	var btn_tw = inv.get_go_title_wall_button() if inv.has_method("get_go_title_wall_button") else null
	if btn_tw == null:
		btn_tw = inv.find_child("BtnGoTitleWall", true, false)
	assert(btn_tw != null, "MapleInventory 找不到 BtnGoTitleWall")
	assert(btn_tw.custom_minimum_size.y >= 48.0, "BtnGoTitleWall 高度需 >= 48px")
	print("  ✓ MapleInventory BtnGoTitleWall 存在且熱區合規: ", btn_tw.custom_minimum_size)

	assert(inv.has_signal("go_shop"), "MapleInventory 缺少 go_shop 信號")
	assert(inv.has_signal("go_title_wall"), "MapleInventory 缺少 go_title_wall 信號")
	print("  ✓ MapleInventory 具備 go_shop 與 go_title_wall 信號")
	inv.queue_free()

	# 2. 測試 ShopDialog 中的 BtnGoWorkshop
	print("\n--- 2. 驗證 ShopDialog 前往工坊快捷按鈕規格與信號 ---")
	var ShopClass = load("res://scripts/ui/shop_dialog.gd")
	var shop = ShopClass.new()
	root.add_child(shop)
	# 手動確保 _build_ui 已執行
	if not shop.is_node_ready() and shop.has_method("_build_ui"):
		shop.call("_build_ui")

	var btn_ws = shop.get_go_workshop_button() if shop.has_method("get_go_workshop_button") else null
	if btn_ws == null:
		btn_ws = shop.find_child("BtnGoWorkshop", true, false)
	assert(btn_ws != null, "ShopDialog 找不到 BtnGoWorkshop")
	assert(btn_ws.custom_minimum_size.y >= 48.0, "BtnGoWorkshop 高度需 >= 48px")
	assert(shop.has_signal("workshop_requested") or shop.has_signal("go_workshop"), "ShopDialog 缺少工坊跳轉信號")
	print("  ✓ ShopDialog BtnGoWorkshop 存在、熱區合規且信號完備: ", btn_ws.custom_minimum_size)
	shop.queue_free()

	# 3. 測試 GemWorkshopDialog 中的 BtnGoShop
	print("\n--- 3. 驗證 GemWorkshopDialog 前往商城快捷按鈕規格與信號 ---")
	var WorkshopClass = load("res://scripts/ui/gem_workshop_dialog.gd")
	var ws = WorkshopClass.new()
	root.add_child(ws)
	if not ws.is_node_ready() and ws.has_method("_build_ui"):
		ws.call("_build_ui")

	var ws_btn_shop = ws.get_go_shop_button() if ws.has_method("get_go_shop_button") else null
	if ws_btn_shop == null:
		ws_btn_shop = ws.find_child("BtnGoShop", true, false)
	assert(ws_btn_shop != null, "GemWorkshopDialog 找不到 BtnGoShop")
	assert(ws_btn_shop.custom_minimum_size.y >= 48.0, "GemWorkshopDialog BtnGoShop 高度需 >= 48px")
	assert(ws.has_signal("shop_requested") or ws.has_signal("go_shop"), "GemWorkshopDialog 缺少商城跳轉信號")
	print("  ✓ GemWorkshopDialog BtnGoShop 存在、熱區合規且信號完備: ", ws_btn_shop.custom_minimum_size)
	ws.queue_free()

	# 4. 測試六語系翻譯鍵值
	print("\n--- 4. 驗證六語系字典翻譯鍵值完整性 ---")
	for lang in Locales:
		if loc and loc.has_method("set_locale"):
			loc.call("set_locale", lang)
		var t_inv_shop = loc.call("t", "inventory.btn_go_shop") if loc else ""
		var t_inv_tw = loc.call("t", "inventory.btn_go_title_wall") if loc else ""
		var t_shop_ws = loc.call("t", "shop.btn_go_workshop") if loc else ""
		var t_ws_shop = loc.call("t", "gem_workshop.btn_go_shop") if loc else ""

		assert(not t_inv_shop.is_empty() and t_inv_shop != "inventory.btn_go_shop", "語系 %s 缺 inventory.btn_go_shop" % lang)
		assert(not t_inv_tw.is_empty() and t_inv_tw != "inventory.btn_go_title_wall", "語系 %s 缺 inventory.btn_go_title_wall" % lang)
		assert(not t_shop_ws.is_empty() and t_shop_ws != "shop.btn_go_workshop", "語系 %s 缺 shop.btn_go_workshop" % lang)
		assert(not t_ws_shop.is_empty() and t_ws_shop != "gem_workshop.btn_go_shop", "語系 %s 缺 gem_workshop.btn_go_shop" % lang)
		print("  ✓ [%s] 六語系鍵值檢驗通過: %s / %s / %s / %s" % [lang, t_inv_shop, t_inv_tw, t_shop_ws, t_ws_shop])

	print("\n=======================================================")
	print("TEST_BATCH_SHORTCUTS_REGRESSION_OK")
	print("=======================================================")
	quit(0)
	return true
