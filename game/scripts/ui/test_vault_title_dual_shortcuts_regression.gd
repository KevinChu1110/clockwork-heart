extends SceneTree
## 《發條之心》ClockworkVaultDialog 與 TitleWallDialog 雙快捷按鈕合併回歸驗收測試
## (test_vault_title_dual_shortcuts_regression.gd - t_5a1b027c)
##
## 驗收規範：
## 1. ClockworkVaultDialog 前往委託快捷：
##    - BtnGoWindup：暖橘色 (#FFA010)，立體厚底 5px，圓角 18px，高 52px (>= 48px 熱區)。
##    - 點擊發出 go_windup 與 windup_requested，大廳開啟 WindupDailyDialog。
##    - 六語系 i18n 即時切換，零系統 Emoji。
## 2. TitleWallDialog 前往背包快捷：
##    - BtnGoInventory：薄荷綠色 (#4ED86A)，立體厚底 5px，圓角 18px，高 52px (>= 48px 熱區)。
##    - 點擊發出 inventory_requested，大廳開啟 MapleInventory。
##    - 六語系 i18n 即時切換，零系統 Emoji。
## 3. 實機渲染存證：
##    - 擷取真實畫面存證至 proofs/t_5a1b027c/，驗證 SHA256 獨立唯一。
## 4. 哨兵輸出：TEST_VAULT_TITLE_DUAL_SHORTCUTS_REGRESSION_OK。

const ClockworkVaultDialogScn = preload("res://scripts/ui/clockwork_vault_dialog.gd")
const TitleWallDialogScn = preload("res://scripts/ui/title_wall_dialog.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_VAULT_TEXTS: Dictionary = {
	"zh_TW": "前往委託",
	"zh_CN": "前往委托",
	"en": "To Daily",
	"ja": "日課へ",
	"ko": "일일 의뢰로 이동",
	"es": "Ir a Encargos"
}
const EXPECTED_TITLE_INVENTORY_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "To Inventory",
	"ja": "バッグへ",
	"ko": "가방으로 이동",
	"es": "Ir a Mochila"
}

var _lobby: Control = null
var _vault_dlg: Control = null
var _title_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_5a1b027c")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	var gs: Node = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)
	if gs and gs.has_method("reset_new_game"):
		gs.call("reset_new_game", "rabbit")

	var loc: Node = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("VAULT_TITLE_DUAL_SHORTCUTS_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, u])


func _capture_save(filename: String) -> String:
	var img := root.get_viewport().get_texture().get_image()
	var full_path := _out_dir.path_join(filename)
	img.save_png(full_path)
	var f := FileAccess.open(full_path, FileAccess.READ)
	var sha := ""
	if f != null:
		var data := f.get_buffer(f.get_length())
		var ctx := HashingContext.new()
		ctx.start(HashingContext.HASH_SHA256)
		ctx.update(data)
		sha = ctx.finish().hex_encode()
		f.close()
	if _proof_hashes.has(sha):
		_fail("截圖重複（SHA256 碰撞）：%s 與 %s" % [filename, _proof_hashes[sha]])
	_proof_hashes[sha] = filename
	print("  [CAPTURE] %s (SHA256: %s)" % [filename, sha])
	return sha


func _process(_delta: float) -> bool:
	if not _ok:
		return false
	if _wait > 0:
		_wait -= 1
		return false

	match _step:
		0:
			print("Step 0: 打開發條儲能庫 ClockworkVaultDialog")
			_vault_dlg = _lobby.open_clockwork_vault()
			if _vault_dlg == null:
				return _fail("未能透過 _lobby.open_clockwork_vault() 開啟彈窗")
			_wait = 15
			_step = 1

		1:
			print("Step 1: 檢查 ClockworkVaultDialog 前往委託快捷按鈕規格")
			var btn: Button = _vault_dlg.get_node_or_null("MarginContainer/Panel/VBox/Footer/BtnGoWindup")
			if btn == null and _vault_dlg.has_method("get_go_windup_button"):
				btn = _vault_dlg.call("get_go_windup_button")
			if btn == null:
				return _fail("ClockworkVaultDialog 未找到 BtnGoWindup 按鈕")

			if btn.size.y < 48 and btn.custom_minimum_size.y < 48:
				return _fail("BtnGoWindup 高度未達 48px 熱區規範: %s" % str(btn.size))
			_check_no_emoji(btn.text, "BtnGoWindup")
			if btn.text != "前往委託":
				return _fail("BtnGoWindup 預設繁中文字不符，預期「前往委託」，實際: %s" % btn.text)

			_capture_save("proof_01_clockwork_vault_with_btn_go_windup.png")
			_wait = 10
			_step = 2

		2:
			print("Step 2: 點擊 BtnGoWindup，驗證大廳開啟 WindupDailyDialog")
			var btn: Button = _vault_dlg.get_node_or_null("MarginContainer/Panel/VBox/Footer/BtnGoWindup")
			if btn == null and _vault_dlg.has_method("get_go_windup_button"):
				btn = _vault_dlg.call("get_go_windup_button")
			btn.emit_signal("pressed")
			_wait = 20
			_step = 3

		3:
			print("Step 3: 驗證 WindupDailyDialog 成功開啟且 ClockworkVaultDialog 關閉")
			var windup = _lobby.get_node_or_null("WindupDailyDialog")
			if windup == null:
				return _fail("點擊 BtnGoWindup 後大廳未開啟 WindupDailyDialog")
			var vault = _lobby.get_node_or_null("ClockworkVaultDialog")
			if vault != null and vault.visible:
				return _fail("開啟委託後 ClockworkVaultDialog 未正常關閉或遮罩殘留")

			_capture_save("proof_02_vault_click_go_windup_opens_windup_daily.png")
			if windup.has_method("close"):
				windup.call("close")
			elif windup.has_method("_on_close"):
				windup.call("_on_close")
			else:
				windup.queue_free()
			_wait = 15
			_step = 4

		4:
			print("Step 4: 打開稱號牆 TitleWallDialog")
			_title_dlg = _lobby.open_title_wall_dialog()
			if _title_dlg == null:
				return _fail("未能透過 _lobby.open_title_wall_dialog() 開啟彈窗")
			_wait = 15
			_step = 5

		5:
			print("Step 5: 檢查 TitleWallDialog 前往背包快捷按鈕規格")
			var btn: Button = _title_dlg.get_node_or_null("ModalRoot/Panel/VBox/FooterHBox/BtnGoInventory")
			if btn == null and _title_dlg.has_method("get_go_inventory_button"):
				btn = _title_dlg.call("get_go_inventory_button")
			if btn == null:
				return _fail("TitleWallDialog 未找到 BtnGoInventory 按鈕")

			if btn.size.y < 48 and btn.custom_minimum_size.y < 48:
				return _fail("BtnGoInventory 高度未達 48px 熱區規範: %s" % str(btn.size))
			_check_no_emoji(btn.text, "BtnGoInventory")
			if btn.text != "前往背包":
				return _fail("BtnGoInventory 預設繁中文字不符，預期「前往背包」，實際: %s" % btn.text)

			_capture_save("proof_03_title_wall_with_btn_go_inventory.png")
			_wait = 10
			_step = 6

		6:
			print("Step 6: 點擊 BtnGoInventory，驗證大廳開啟 MapleInventory")
			var btn: Button = _title_dlg.get_node_or_null("ModalRoot/Panel/VBox/FooterHBox/BtnGoInventory")
			if btn == null and _title_dlg.has_method("get_go_inventory_button"):
				btn = _title_dlg.call("get_go_inventory_button")
			btn.emit_signal("pressed")
			_wait = 20
			_step = 7

		7:
			print("Step 7: 驗證 MapleInventory 成功開啟且 TitleWallDialog 關閉")
			var inv = _lobby.get_node_or_null("MapleInventory")
			if inv == null:
				return _fail("點擊 BtnGoInventory 後大廳未開啟 MapleInventory")
			var title_wall = _lobby.get_node_or_null("TitleWallDialog")
			if title_wall != null and title_wall.visible:
				return _fail("開啟背包後 TitleWallDialog 未正常關閉或遮罩殘留")

			_capture_save("proof_04_title_wall_click_go_inventory_opens_maple_inventory.png")
			inv.queue_free()
			_wait = 15
			_step = 8

		8:
			print("Step 8: 驗證六語系切換支援")
			var loc_node: Node = root.get_node_or_null("Loc")
			for loc_code in LOCALES:
				if loc_node and loc_node.has_method("set_locale"):
					loc_node.call("set_locale", loc_code)
				var v_dlg: Control = _lobby.open_clockwork_vault()
				var v_btn: Button = v_dlg.call("get_go_windup_button")
				var expected_v: String = EXPECTED_VAULT_TEXTS[loc_code]
				if v_btn.text != expected_v:
					return _fail("儲能庫按鈕在語系 [%s] 文本不符: 預期 '%s', 實際 '%s'" % [loc_code, expected_v, v_btn.text])
				_check_no_emoji(v_btn.text, "VaultWindup_" + loc_code)
				v_dlg.queue_free()

				var t_dlg: Control = _lobby.open_title_wall_dialog()
				var t_btn: Button = t_dlg.call("get_go_inventory_button")
				var expected_t: String = EXPECTED_TITLE_INVENTORY_TEXTS[loc_code]
				if t_btn.text != expected_t:
					return _fail("稱號牆按鈕在語系 [%s] 文本不符: 預期 '%s', 實際 '%s'" % [loc_code, expected_t, t_btn.text])
				_check_no_emoji(t_btn.text, "TitleInventory_" + loc_code)
				t_dlg.queue_free()

			if loc_node and loc_node.has_method("set_locale"):
				loc_node.call("set_locale", "ja")
			var vault_ja = _lobby.open_clockwork_vault()
			_wait = 15
			_step = 9

		9:
			_capture_save("proof_05_vault_windup_locale_ja.png")
			var vault_ja = _lobby.get_node_or_null("ClockworkVaultDialog")
			if vault_ja:
				vault_ja.queue_free()
			var loc_node: Node = root.get_node_or_null("Loc")
			if loc_node and loc_node.has_method("set_locale"):
				loc_node.call("set_locale", "en")
			var title_en = _lobby.open_title_wall_dialog()
			_wait = 15
			_step = 10

		10:
			_capture_save("proof_06_title_wall_inventory_locale_en.png")
			var title_en = _lobby.get_node_or_null("TitleWallDialog")
			if title_en:
				title_en.queue_free()

			print("==================================================")
			print("TEST_VAULT_TITLE_DUAL_SHORTCUTS_REGRESSION_OK")
			print("==================================================")
			quit(0)
			return true

	return false
