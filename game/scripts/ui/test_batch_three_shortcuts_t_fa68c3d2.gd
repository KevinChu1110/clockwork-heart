extends SceneTree

# test_batch_three_shortcuts_t_fa68c3d2.gd
# 驗證商城前往儲能庫(t_53a8b616)、委託前往商城(t_18b92637)與商城前往委託(t_ec3adc60)三分支合併主線之完整性 (t_fa68c3d2)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _finished := false
var _exit_code := 0

func _initialize() -> void:
	print("=== 開始執行三快捷主線合併回歸驗收測試 (t_fa68c3d2) ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
			if gs.has_method("reset_new_game"):
				gs.call("reset_new_game", "rabbit")

	var loc = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

	# 1. ShopDialog: BtnGoVault (前往儲能庫快捷)
	print("\n--- 1. 驗證 ShopDialog 前往儲能庫快捷按鈕 (BtnGoVault, t_53a8b616) ---")
	var ShopClass = load("res://scripts/ui/shop_dialog.gd")
	var shop = ShopClass.new()
	root.add_child(shop)
	if not shop.is_node_ready() and shop.has_method("_build_ui"):
		shop.call("_build_ui")

	var vault_btn = shop.get_go_vault_button() if shop.has_method("get_go_vault_button") else null
	if vault_btn == null and shop.has_method("get_vault_button"):
		vault_btn = shop.get_vault_button()
	if vault_btn == null:
		vault_btn = shop.find_child("BtnGoVault", true, false)
	assert(vault_btn != null, "ShopDialog 找不到 BtnGoVault")
	assert(vault_btn.custom_minimum_size.y >= 48.0, "ShopDialog BtnGoVault 高度需 >= 48px")
	assert(shop.has_signal("vault_requested") or shop.has_signal("go_vault"), "ShopDialog 缺少儲能庫跳轉信號")
	print("  ✓ ShopDialog BtnGoVault 存在、熱區合規且信號完備: ", vault_btn.custom_minimum_size)

	# 2. ShopDialog: BtnGoWindupDaily (前往委託快捷)
	print("\n--- 2. 驗證 ShopDialog 前往委託快捷按鈕 (BtnGoWindupDaily, t_ec3adc60) ---")
	var windup_btn = shop.get_go_windup_daily_button() if shop.has_method("get_go_windup_daily_button") else null
	if windup_btn == null and shop.has_method("get_go_daily_button"):
		windup_btn = shop.get_go_daily_button()
	if windup_btn == null:
		windup_btn = shop.find_child("BtnGoWindupDaily", true, false)
	assert(windup_btn != null, "ShopDialog 找不到 BtnGoWindupDaily")
	assert(windup_btn.custom_minimum_size.y >= 48.0, "ShopDialog BtnGoWindupDaily 高度需 >= 48px")
	assert(shop.has_signal("windup_daily_requested") or shop.has_signal("go_windup_daily"), "ShopDialog 缺少每日委託跳轉信號")
	print("  ✓ ShopDialog BtnGoWindupDaily 存在、熱區合規且信號完備: ", windup_btn.custom_minimum_size)
	shop.queue_free()

	# 3. WindupDailyDialog: BtnGoShop (前往商城快捷)
	print("\n--- 3. 驗證 WindupDailyDialog 前往商城快捷按鈕 (BtnGoShop, t_18b92637) ---")
	var WindupClass = load("res://scripts/ui/windup_daily_dialog.gd")
	var windup_dlg = WindupClass.new()
	root.add_child(windup_dlg)
	if not windup_dlg.is_node_ready() and windup_dlg.has_method("_build_ui"):
		windup_dlg.call("_build_ui")

	var shop_btn = windup_dlg.get_go_shop_button() if windup_dlg.has_method("get_go_shop_button") else null
	if shop_btn == null and windup_dlg.has_method("get_shop_button"):
		shop_btn = windup_dlg.get_shop_button()
	if shop_btn == null:
		shop_btn = windup_dlg.find_child("BtnGoShop", true, false)
	assert(shop_btn != null, "WindupDailyDialog 找不到 BtnGoShop")
	assert(shop_btn.custom_minimum_size.y >= 48.0, "WindupDailyDialog BtnGoShop 高度需 >= 48px")
	assert(windup_dlg.has_signal("shop_requested") or windup_dlg.has_signal("go_shop"), "WindupDailyDialog 缺少前往商城信號")
	print("  ✓ WindupDailyDialog BtnGoShop 存在、熱區合規且信號完備: ", shop_btn.custom_minimum_size)
	windup_dlg.queue_free()

	# 4. MobileLobby 大廳連動方法檢驗
	print("\n--- 4. 驗證 MobileLobby 彈窗開啟與連動函式完備性 ---")
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	assert(lobby.has_method("open_shop"), "MobileLobby 需具備 open_shop")
	assert(lobby.has_method("open_clockwork_vault"), "MobileLobby 需具備 open_clockwork_vault")
	assert(lobby.has_method("open_windup_daily"), "MobileLobby 需具備 open_windup_daily")
	print("  ✓ MobileLobby open_shop / open_clockwork_vault / open_windup_daily 全部具備")
	lobby.queue_free()

	# 5. 六語系 key 檢查
	print("\n--- 5. 驗證六語系 i18n 鍵值存在性 ---")
	var required_keys = [
		"shop.btn_go_vault",
		"windup_daily.btn_go_shop",
		"shop.btn_go_daily"
	]
	for loc_code in LOCALES:
		if loc != null and loc.has_method("set_locale"):
			loc.call("set_locale", loc_code)
		for k in required_keys:
			var tr_val: String = loc.call("t", k) if loc != null else ""
			assert(tr_val != "" and tr_val != k, "語系 [%s] 缺少 key: %s" % [loc_code, k])
			print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])

	print("\n========================================================")
	print("TEST_BATCH_THREE_SHORTCUTS_REGRESSION_OK")
	print("========================================================")
	_finished = true
	_exit_code = 0
	quit(0)

func _process(_delta: float) -> bool:
	if _finished:
		quit(_exit_code)
		return true
	return false
