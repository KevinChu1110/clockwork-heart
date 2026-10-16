extends SceneTree

# test_batch_four_shortcuts_t_5c9864c0.gd
# 驗證四個快捷功能在 main 主線上的完整性、信號連動與六語系支援 (t_5c9864c0)

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _finished := false
var _exit_code := 0

func _initialize() -> void:
	print("=== 開始執行四快捷主線合併回歸驗收測試 (t_5c9864c0) ===")
	
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

	# 1. ForgeDialog: BtnGoShop
	print("\n--- 1. 驗證 ForgeDialog 前往商城快捷按鈕 (BtnGoShop) ---")
	var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
	var forge = ForgeClass.new()
	root.add_child(forge)
	if not forge.is_node_ready() and forge.has_method("_build_ui"):
		forge.call("_build_ui")

	var forge_btn = forge.get_go_shop_button() if forge.has_method("get_go_shop_button") else null
	if forge_btn == null:
		forge_btn = forge.find_child("BtnGoShop", true, false)
	assert(forge_btn != null, "ForgeDialog 找不到 BtnGoShop")
	assert(forge_btn.custom_minimum_size.y >= 48.0, "ForgeDialog BtnGoShop 高度需 >= 48px")
	assert(forge.has_signal("shop_requested") or forge.has_signal("go_shop"), "ForgeDialog 缺少前往商城信號")
	print("  ✓ ForgeDialog BtnGoShop 存在、熱區合規且信號完備: ", forge_btn.custom_minimum_size)
	forge.queue_free()

	# 2. SkillDialog: BtnGoShop
	print("\n--- 2. 驗證 SkillDialog 前往商城快捷按鈕 (BtnGoShop) ---")
	var SkillClass = load("res://scripts/ui/skill_dialog.gd")
	var skill_dlg = SkillClass.new()
	root.add_child(skill_dlg)
	if not skill_dlg.is_node_ready() and skill_dlg.has_method("_build_ui"):
		skill_dlg.call("_build_ui")

	var skill_btn = skill_dlg.get_go_shop_button() if skill_dlg.has_method("get_go_shop_button") else null
	if skill_btn == null:
		skill_btn = skill_dlg.find_child("BtnGoShop", true, false)
	assert(skill_btn != null, "SkillDialog 找不到 BtnGoShop")
	assert(skill_btn.custom_minimum_size.y >= 48.0, "SkillDialog BtnGoShop 高度需 >= 48px")
	assert(skill_dlg.has_signal("shop_requested") or skill_dlg.has_signal("go_shop"), "SkillDialog 缺少前往商城信號")
	print("  ✓ SkillDialog BtnGoShop 存在、熱區合規且信號完備: ", skill_btn.custom_minimum_size)
	skill_dlg.queue_free()

	# 3. ShopDialog: BtnGoSkill
	print("\n--- 3. 驗證 ShopDialog 前往心法快捷按鈕 (BtnGoSkill) ---")
	var ShopClass = load("res://scripts/ui/shop_dialog.gd")
	var shop = ShopClass.new()
	root.add_child(shop)
	if not shop.is_node_ready() and shop.has_method("_build_ui"):
		shop.call("_build_ui")

	var shop_btn = shop.get_go_skill_button() if shop.has_method("get_go_skill_button") else null
	if shop_btn == null:
		shop_btn = shop.find_child("BtnGoSkill", true, false)
	assert(shop_btn != null, "ShopDialog 找不到 BtnGoSkill")
	assert(shop_btn.custom_minimum_size.y >= 48.0, "ShopDialog BtnGoSkill 高度需 >= 48px")
	assert(shop.has_signal("skill_requested") or shop.has_signal("go_skill"), "ShopDialog 缺少心法跳轉信號")
	print("  ✓ ShopDialog BtnGoSkill 存在、熱區合規且信號完備: ", shop_btn.custom_minimum_size)
	shop.queue_free()

	# 4. ClockworkVaultDialog: BtnGoShop
	print("\n--- 4. 驗證 ClockworkVaultDialog 前往商城快捷按鈕 (BtnGoShop) ---")
	var VaultClass = load("res://scripts/ui/clockwork_vault_dialog.gd")
	var vault = VaultClass.new()
	root.add_child(vault)
	if not vault.is_node_ready() and vault.has_method("_build_ui"):
		vault.call("_build_ui")

	var vault_btn = vault.get_go_shop_button() if vault.has_method("get_go_shop_button") else null
	if vault_btn == null:
		vault_btn = vault.find_child("BtnGoShop", true, false)
	assert(vault_btn != null, "ClockworkVaultDialog 找不到 BtnGoShop")
	assert(vault_btn.custom_minimum_size.y >= 48.0, "ClockworkVaultDialog BtnGoShop 高度需 >= 48px")
	assert(vault.has_signal("shop_requested") or vault.has_signal("go_shop"), "ClockworkVaultDialog 缺少前往商城信號")
	print("  ✓ ClockworkVaultDialog BtnGoShop 存在、熱區合規且信號完備: ", vault_btn.custom_minimum_size)
	vault.queue_free()

	# 5. MobileLobby 大廳連動方法檢驗
	print("\n--- 5. 驗證 MobileLobby 彈窗開啟與連動函式完備性 ---")
	var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = LobbyClass.new()
	assert(lobby.has_method("open_forge"), "MobileLobby 需具備 open_forge")
	assert(lobby.has_method("open_skill_dialog"), "MobileLobby 需具備 open_skill_dialog")
	assert(lobby.has_method("open_shop"), "MobileLobby 需具備 open_shop")
	assert(lobby.has_method("open_clockwork_vault"), "MobileLobby 需具備 open_clockwork_vault")
	print("  ✓ MobileLobby open_forge / open_skill_dialog / open_shop / open_clockwork_vault 全部具備")
	lobby.queue_free()

	# 6. 六語系 key 檢查
	print("\n--- 6. 驗證六語系 i18n 鍵值存在性 ---")
	var required_keys = [
		"forge.btn_go_shop",
		"skill.btn_go_shop",
		"shop.btn_go_skill",
		"vault.btn_go_shop"
	]
	for loc_code in LOCALES:
		if loc != null and loc.has_method("set_locale"):
			loc.call("set_locale", loc_code)
		for k in required_keys:
			var tr_val: String = loc.call("t", k) if loc != null else ""
			assert(tr_val != "" and tr_val != k, "語系 [%s] 缺少 key: %s" % [loc_code, k])
			print("  ✓ [%s] %s => '%s'" % [loc_code, k, tr_val])

	print("\n========================================================")
	print("TEST_BATCH_FOUR_SHORTCUTS_REGRESSION_OK")
	print("========================================================")
	_finished = true
	_exit_code = 0
	quit(0)

func _process(_delta: float) -> bool:
	if _finished:
		quit(_exit_code)
		return true
	return false
