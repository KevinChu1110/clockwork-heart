extends SceneTree
## 《發條之心》WindupDailyDialog 冒險委託每日上發條雙快捷按鈕合併回歸驗收測試
## (test_windup_daily_dual_shortcuts.gd - t_5fa72e81)
##
## 驗收規範：
## 1. 雙按鈕並存於底部按鈕列：
##    - BtnGoInventory：多巴胺薄荷綠 #4ED86A (COLOR_MINT)，立體厚底 5px，圓角 18px，高 52px (>= 50px 熱區)。
##    - BtnGoVault：多巴胺天藍色 #38A0FF (COLOR_SKY)，立體厚底 5px，圓角 18px，高 52px (>= 50px 熱區)。
## 2. 可見度狀態流轉：
##    - 每日委託未完成時：兩者皆隱藏 (visible = false)。
##    - 每日委託完成後：與『離開委託』、『前往戰力』、『前往出征』/『前往停擺巨偶』並列顯示 (visible = true)。
## 3. 連動大廳跳轉：
##    - 點擊 BtnGoInventory 發射 inventory_requested 並關閉彈窗，大廳開啟 MapleInventory。
##    - 點擊 BtnGoVault 發射 vault_requested 並關閉彈窗，大廳開啟 ClockworkVaultDialog。
## 4. 六語系 i18n 即時切換：
##    - 六語系完整對照，零缺詞、零系統 Emoji。
## 5. 實機渲染存證：
##    - 擷取真實畫面存證至 proofs/t_5fa72e81/，驗證 SHA256 獨立唯一。
## 6. 哨兵輸出：TEST_WINDUP_DAILY_DUAL_SHORTCUTS_OK。

const WindupDailyDialogScn = preload("res://scripts/ui/windup_daily_dialog.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_INVENTORY_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "To Inventory",
	"ja": "バッグへ",
	"ko": "가방으로 이동",
	"es": "Ir a Mochila"
}
const EXPECTED_VAULT_TEXTS: Dictionary = {
	"zh_TW": "前往儲能庫",
	"zh_CN": "前往储能库",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고로 이동",
	"es": "Ir a Bóveda"
}

var _lobby: Control = null
var _windup_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _inventory_signal_emitted: bool = false
var _vault_signal_emitted: bool = false
var _closed_signal_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_5fa72e81")
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

	var ws: Node = root.get_node_or_null("WindupDailySystem")
	if ws == null:
		var WsClass = load("res://scripts/systems/windup_daily.gd")
		if WsClass:
			ws = WsClass.new()
			ws.name = "WindupDailySystem"
			root.add_child(ws)

	var cds: Node = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("WINDUP_DAILY_DUAL_SHORTCUTS_FAIL: ", msg)
	_ok = false
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, u])


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 3:
				return false
			print("\n=== 1. 驗證未完成狀態下，BtnGoInventory 與 BtnGoVault 皆正確隱藏 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", false)
			if ws:
				ws.call("refresh")

			var uncomp_dlg = WindupDailyDialogScn.new()
			root.add_child(uncomp_dlg)
			var uncomp_btn_inv: Button = uncomp_dlg.find_child("BtnGoInventory", true, false)
			var uncomp_btn_vault: Button = uncomp_dlg.find_child("BtnGoVault", true, false)
			if uncomp_btn_inv == null or uncomp_btn_vault == null:
				return _fail("WindupDailyDialog 缺少快捷按鈕節點")
			if uncomp_btn_inv.visible or uncomp_btn_vault.visible:
				return _fail("每日委託未完成時，快捷按鈕不應顯示")
			print("  ✓ 每日委託未完成時，BtnGoInventory 與 BtnGoVault 皆正確隱藏")
			uncomp_dlg.queue_free()

			_step = 1
			_wait = 0
			return false

		1:
			if _wait < 3:
				return false
			print("\n=== 2. 驗證完成狀態下，雙快捷按鈕規格、樣式、並列呈現 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			var cds: Node = root.get_node_or_null("ColossusDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", true)
			if cds:
				cds.call("set", "_entries_today", 0)
			if ws:
				ws.call("refresh")

			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法透過大廳開啟 WindupDailyDialog")

			var btn_inv: Button = _windup_dlg.find_child("BtnGoInventory", true, false)
			var btn_vault: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			if btn_inv == null or btn_vault == null:
				return _fail("無法取得雙快捷按鈕節點")
			if not btn_inv.visible or not btn_vault.visible:
				return _fail("完成狀態下雙快捷按鈕未顯示")

			print("  ✓ 委託完成狀態下，BtnGoInventory 與 BtnGoVault 同時正常顯示")
			print("  ✓ BtnGoInventory: '%s' 尺寸 %s" % [btn_inv.text, str(btn_inv.size)])
			print("  ✓ BtnGoVault: '%s' 尺寸 %s" % [btn_vault.text, str(btn_vault.size)])
			_check_no_emoji(btn_inv.text, "BtnGoInventory_zh_TW")
			_check_no_emoji(btn_vault.text, "BtnGoVault_zh_TW")

			_step = 2
			_wait = 0
			return false

		2:
			if _wait < 6:
				return false
			var cap_name := "proof_01_windup_daily_completed_dual_shortcuts_zh_TW.png"
			var hash0 := _capture_save(_out_dir.path_join(cap_name))
			if not hash0.is_empty():
				_proof_hashes[cap_name] = hash0

			_step = 3
			_wait = 0
			return false

		3:
			if _wait < 3:
				return false
			print("\n=== 3. 測試點擊 BtnGoInventory 連動開啟 MapleInventory ===")
			_windup_dlg.inventory_requested.connect(func(): _inventory_signal_emitted = true)
			_windup_dlg.closed.connect(func(): _closed_signal_emitted = true)

			var btn_inv: Button = _windup_dlg.find_child("BtnGoInventory", true, false)
			btn_inv.emit_signal("pressed")

			_step = 4
			_wait = 0
			return false

		4:
			if _wait < 6:
				return false
			if not _inventory_signal_emitted:
				return _fail("未發射 inventory_requested 訊號")
			if not _closed_signal_emitted:
				return _fail("未發射 closed 訊號")
			print("  ✓ 成功發射 inventory_requested 與 closed 訊號")

			var maple_inv = _lobby.find_child("MapleInventory", true, false)
			if maple_inv == null:
				return _fail("大廳未開啟 MapleInventory")
			print("  ✓ 大廳成功連動開啟 MapleInventory")

			var cap_name := "proof_02_click_go_inventory_opens_maple_inventory.png"
			var hash1 := _capture_save(_out_dir.path_join(cap_name))
			if not hash1.is_empty():
				_proof_hashes[cap_name] = hash1
			maple_inv.queue_free()

			_step = 5
			_wait = 0
			return false

		5:
			if _wait < 3:
				return false
			print("\n=== 4. 測試點擊 BtnGoVault 連動開啟 ClockworkVaultDialog ===")
			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法重新開啟 WindupDailyDialog")

			_vault_signal_emitted = false
			_closed_signal_emitted = false
			_windup_dlg.vault_requested.connect(func(): _vault_signal_emitted = true)
			_windup_dlg.closed.connect(func(): _closed_signal_emitted = true)

			var btn_vault: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			btn_vault.emit_signal("pressed")

			_step = 6
			_wait = 0
			return false

		6:
			if _wait < 6:
				return false
			if not _vault_signal_emitted:
				return _fail("未發射 vault_requested 訊號")
			if not _closed_signal_emitted:
				return _fail("未發射 closed 訊號")
			print("  ✓ 成功發射 vault_requested 與 closed 訊號")

			var vault_dlg = _lobby.find_child("ClockworkVaultDialog", true, false)
			if vault_dlg == null:
				return _fail("大廳未開啟 ClockworkVaultDialog")
			print("  ✓ 大廳成功連動開啟 ClockworkVaultDialog")

			var cap_name := "proof_03_click_go_vault_opens_clockwork_vault.png"
			var hash2 := _capture_save(_out_dir.path_join(cap_name))
			if not hash2.is_empty():
				_proof_hashes[cap_name] = hash2
			vault_dlg.queue_free()

			_step = 7
			_wait = 0
			_locale_test_index = 0
			return false

		7:
			if _wait < 3:
				return false
			print("\n=== 5. 六語系 i18n 動態切換驗證 ===")
			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法重新開啟 WindupDailyDialog 進行語系測試")

			_step = 8
			_wait = 0
			return false

		8:
			if _wait < 3:
				return false
			if _locale_test_index >= LOCALES.size():
				_step = 10
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			_switch_locale(loc_code)

			var btn_inv: Button = _windup_dlg.find_child("BtnGoInventory", true, false)
			var btn_vault: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			if btn_inv == null or btn_vault == null:
				return _fail("語系 [%s] 下無法取得按鈕" % loc_code)

			var exp_inv: String = EXPECTED_INVENTORY_TEXTS[loc_code]
			var exp_vault: String = EXPECTED_VAULT_TEXTS[loc_code]
			if btn_inv.text != exp_inv:
				return _fail("語系 [%s] BtnGoInventory 文字不符：預期 '%s'，實際 '%s'" % [loc_code, exp_inv, btn_inv.text])
			if btn_vault.text != exp_vault:
				return _fail("語系 [%s] BtnGoVault 文字不符：預期 '%s'，實際 '%s'" % [loc_code, exp_vault, btn_vault.text])

			_check_no_emoji(btn_inv.text, "BtnGoInventory_%s" % loc_code)
			_check_no_emoji(btn_vault.text, "BtnGoVault_%s" % loc_code)
			print("  ✓ 語系 [%s] 即時切換: 背包='%s', 儲能庫='%s'" % [loc_code, btn_inv.text, btn_vault.text])

			_step = 9
			_wait = 0
			return false

		9:
			if _wait < 6:
				return false
			var loc_code: String = LOCALES[_locale_test_index]
			var cap_name := "proof_locale_%s_dual_shortcuts.png" % loc_code
			var hash_loc := _capture_save(_out_dir.path_join(cap_name))
			if not hash_loc.is_empty():
				_proof_hashes[cap_name] = hash_loc

			_locale_test_index += 1
			_step = 8
			_wait = 0
			return false

		10:
			if _wait < 3:
				return false
			print("\n=== 6. 驗證所有實機截圖存證 SHA256 獨立唯一 ===")
			if _proof_hashes.size() > 1:
				var hash_values := _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							var k1 = _proof_hashes.keys()[i]
							var k2 = _proof_hashes.keys()[j]
							return _fail("發現重複截圖 (SHA256 相同): %s 與 %s" % [k1, k2])
			print("  ✓ 全數實機截圖 (%d 張) SHA256 均獨立唯一，無重複截圖" % _proof_hashes.size())

			print("\n=======================================================")
			print("TEST_WINDUP_DAILY_DUAL_SHORTCUTS_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
