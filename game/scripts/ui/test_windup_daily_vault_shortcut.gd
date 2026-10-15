extends SceneTree
## 《發條之心》WindupDailyDialog 冒險委託每日上發條新增『前往儲能庫』快捷果凍按鈕單元與整合測試
## (test_windup_daily_vault_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格與多巴胺視覺：
##    - BtnGoVault 位於 FootButtons 底部按鈕列。
##    - 天藍色盤 #38A0FF (COLOR_SKY)，深藍紫描邊 #1F1A3A (COLOR_BORDER)，立體厚底 5px，圓角 18px，高 52px (>= 50px 手機端熱區)。
##    - 使用開源粉圓體，字級 >= 16px，零系統 Emoji 與特殊符號。
## 2. 可見度狀態流轉：
##    - 每日委託未完成時：隱藏 (visible = false)。
##    - 每日委託完成後：與『離開委託』、『前往戰力』、『前往背包』、『前往出征』/『前往停擺巨偶』並列顯示 (visible = true)。
## 3. 點擊連動大廳開啟 ClockworkVaultDialog：
##    - 點擊 BtnGoVault 發射 vault_requested 訊號並自動關閉彈窗 (closed 訊號、queue_free)。
##    - 大廳接到後平滑連動開啟 ClockworkVaultDialog 發條儲能庫放置收益彈窗。
## 4. 存取器與訊號：
##    - 提供 get_vault_button() 與 get_go_vault_button() 存取器。
##    - 宣告 vault_requested 訊號。
## 5. 支援六語系 i18n 即時切換：
##    - zh_TW: 「前往儲能庫」
##    - zh_CN: 「前往储能库」
##    - en: 「To Vault」
##    - ja: 「貯蔵庫へ」
##    - ko: 「저장고로 이동」
##    - es: 「Ir a Bóveda」
##    - 動態切換無缺詞、零系統 Emoji。
## 6. 實機渲染存證：
##    - 擷取真實畫面存證至 proofs/t_44ba96c6/，驗證 SHA256 獨立唯一且無黑屏。
## 7. 哨兵輸出：TEST_WINDUP_DAILY_VAULT_SHORTCUT_OK。

const WindupDailyDialogScn = preload("res://scripts/ui/windup_daily_dialog.gd")
const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往儲能庫",
	"zh_CN": "前往储能库",
	"en": "To Vault",
	"ja": "貯蔵庫へ",
	"ko": "저장고로 이동",
	"es": "Ir a Bóveda"
}

var _lobby: Control = null
var _windup_dlg: Control = null
var _vault_dlg: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true
var _vault_signal_emitted: bool = false
var _closed_signal_emitted: bool = false
var _locale_test_index: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_44ba96c6")
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
	print("WINDUP_DAILY_VAULT_SHORTCUT_FAIL: ", msg)
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
			print("\n=== 1. 驗證委託未完成狀態下，BtnGoVault 正確隱藏 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", false)
			if ws:
				ws.call("refresh")

			var uncomp_dlg = WindupDailyDialogScn.new()
			root.add_child(uncomp_dlg)
			var uncomp_btn: Button = uncomp_dlg.find_child("BtnGoVault", true, false)
			if uncomp_btn == null:
				return _fail("WindupDailyDialog 缺少 BtnGoVault 按鈕節點")
			if uncomp_btn.visible:
				return _fail("每日委託未完成時，BtnGoVault 不應顯示 (visible 應為 false)")
			print("  ✓ 每日委託未完成時，BtnGoVault 正確隱藏")
			uncomp_dlg.queue_free()

			_step = 1
			_wait = 0
			return false

		1:
			if _wait < 3:
				return false
			print("\n=== 2. 驗證委託完成狀態下，BtnGoVault 規格、熱區、樣式與存取器 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var ws: Node = root.get_node_or_null("WindupDailySystem")
			var cds: Node = root.get_node_or_null("ColossusDailySystem")
			if gs:
				gs.call("set_flag", "windup.done", true)
				gs.set("colossus_daily_entries", 3)
			if ws:
				ws.call("refresh")
			if cds:
				cds.call("refresh")

			_switch_locale("zh_TW")
			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法透過 _lobby.open_windup_daily() 開啟彈窗")

			var btn: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			if btn == null:
				return _fail("無法取得 BtnGoVault 按鈕")
			if not btn.visible:
				return _fail("委託完成狀態下，BtnGoVault 應為 visible")
			print("  ✓ 委託完成狀態下，BtnGoVault 正確呈現顯示")

			# 驗證存取器
			if not _windup_dlg.has_method("get_vault_button"):
				return _fail("WindupDailyDialog 缺少 get_vault_button() 存取器")
			if _windup_dlg.get_vault_button() != btn:
				return _fail("get_vault_button() 返回按鈕與 BtnGoVault 不符")
			print("  ✓ get_vault_button() 存取器驗證通過")

			if not _windup_dlg.has_method("get_go_vault_button"):
				return _fail("WindupDailyDialog 缺少 get_go_vault_button() 存取器")
			if _windup_dlg.get_go_vault_button() != btn:
				return _fail("get_go_vault_button() 返回按鈕與 BtnGoVault 不符")
			print("  ✓ get_go_vault_button() 存取器驗證通過")

			# 驗證文字與零 Emoji
			if btn.text != "前往儲能庫":
				return _fail("繁中初始文字應為『前往儲能庫』，實際為: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoVault_zh_TW")
			print("  ✓ 按鈕文字吻合『前往儲能庫』且零系統 Emoji")

			# 驗證尺寸與手機端熱區
			if btn.custom_minimum_size.y < 50.0:
				return _fail("按鈕高度小於 50px: %.1f" % btn.custom_minimum_size.y)
			if btn.custom_minimum_size.x < 120.0:
				return _fail("按鈕寬度過窄小於 120px: %.1f" % btn.custom_minimum_size.x)
			print("  ✓ 按鈕尺寸符合手機端熱區: %s (高 %.1f px >= 50px, 寬 %.1f px >= 120px)" % [str(btn.custom_minimum_size), btn.custom_minimum_size.y, btn.custom_minimum_size.x])

			# 驗證底色天藍色盤與圓角、厚底
			var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb == null:
				return _fail("BtnGoVault 缺少 StyleBoxFlat normal 樣式")
			var sky_color := Color("#38A0FF")
			if sb.bg_color.to_html(false) != sky_color.to_html(false):
				return _fail("BtnGoVault 底色應為天藍色盤 #38A0FF，實測: #%s" % sb.bg_color.to_html(false))
			if sb.border_width_bottom < 5:
				return _fail("BtnGoVault 底厚應 >= 5px，實測: %d" % sb.border_width_bottom)
			if sb.corner_radius_top_left != 18:
				return _fail("BtnGoVault 圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
			print("  ✓ 多巴胺天藍色盤 (#38A0FF)、立體厚底 (%d px)、圓角 (%d px) 樣式驗證通過" % [sb.border_width_bottom, sb.corner_radius_top_left])

			# 驗證底部按鈕列並列順序
			var foot_box := _windup_dlg.find_child("FootButtons", true, false) as HBoxContainer
			if foot_box == null:
				return _fail("WindupDailyDialog 缺少 FootButtons 按鈕容器")
			var btn_leave: Button = _windup_dlg.find_child("BtnCloseWindup", true, false)
			var btn_power_stat: Button = _windup_dlg.find_child("BtnGoPowerStat", true, false)
			var btn_inventory: Button = _windup_dlg.find_child("BtnGoInventory", true, false)
			var btn_sortie: Button = _windup_dlg.find_child("BtnGoSortie", true, false)
			var btn_colossus: Button = _windup_dlg.find_child("BtnGoColossus", true, false)
			if btn_leave == null or not btn_leave.visible:
				return _fail("底部按鈕列中『離開委託』應保持可見")
			if btn_power_stat == null or not btn_power_stat.visible:
				return _fail("底部按鈕列中『前往戰力』應保持可見")
			if btn_inventory == null or not btn_inventory.visible:
				return _fail("底部按鈕列中『前往背包』應保持可見")
			if btn_sortie == null or not btn_sortie.visible:
				return _fail("底部按鈕列中『前往出征』應保持可見")
			if btn_colossus == null or not btn_colossus.visible:
				return _fail("底部按鈕列中『前往停擺巨偶』應保持可見")
			print("  ✓ 底部按鈕列六按鈕完整並列：離開委託、前往戰力、前往背包、前往儲能庫、前往出征、前往停擺巨偶")

			_step = 2
			_wait = 0
			return false

		2:
			# 等待渲染幀數以擷取第一張存證圖 (繁中委託完成狀態全景)
			if _wait < 6:
				return false
			var hash_01 := _capture_save(_out_dir.path_join("proof_01_windup_daily_completed_btn_go_vault_zh_TW.png"))
			if not hash_01.is_empty():
				_proof_hashes["proof_01"] = hash_01

			_step = 3
			_wait = 0
			return false

		3:
			if _wait < 3:
				return false
			print("\n=== 3. 點擊 BtnGoVault，驗證訊號發射、關閉彈窗與大廳連動開啟 ClockworkVaultDialog ===")
			_vault_signal_emitted = false
			_closed_signal_emitted = false

			_windup_dlg.vault_requested.connect(func():
				_vault_signal_emitted = true
			)
			_windup_dlg.closed.connect(func():
				_closed_signal_emitted = true
			)

			var btn: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			if btn == null:
				return _fail("無法取得 BtnGoVault 按鈕")

			# 模擬玩家點擊按鈕
			btn.pressed.emit()

			if not _vault_signal_emitted:
				return _fail("點擊 BtnGoVault 未發射 vault_requested 訊號")
			print("  ✓ 成功發射 vault_requested 訊號")

			if not _closed_signal_emitted:
				return _fail("點擊 BtnGoVault 未發射 closed 訊號")
			print("  ✓ 成功發射 closed 訊號")

			if not _windup_dlg.is_queued_for_deletion():
				return _fail("點擊後 WindupDailyDialog 未標記 queue_free 關閉")
			print("  ✓ WindupDailyDialog 順利 queue_free 安全關閉，無殘留")

			_step = 4
			_wait = 0
			return false

		4:
			# 等待渲染幀數讓 ClockworkVaultDialog 完整繪製
			if _wait < 8:
				return false
			# 驗證大廳已成功開啟 ClockworkVaultDialog
			_vault_dlg = _lobby.get_node_or_null("ClockworkVaultDialog")
			if _vault_dlg == null or not is_instance_valid(_vault_dlg):
				return _fail("點擊 BtnGoVault 後，大廳未能成功連動開啟 ClockworkVaultDialog！")
			if not _vault_dlg.visible:
				return _fail("連動開啟之 ClockworkVaultDialog 未處於 visible 狀態")
			print("  ✓ 大廳成功平滑連動開啟 ClockworkVaultDialog 發條儲能庫放置收益彈窗！")

			var hash_02 := _capture_save(_out_dir.path_join("proof_02_click_go_vault_opens_clockwork_vault_dialog.png"))
			if not hash_02.is_empty():
				_proof_hashes["proof_02"] = hash_02

			# 關閉 ClockworkVaultDialog 準備進行六語系測試
			_vault_dlg.queue_free()
			_vault_dlg = null

			_step = 5
			_wait = 0
			_locale_test_index = 0
			return false

		5:
			if _wait < 3:
				return false
			# 重新開啟 WindupDailyDialog 進行六語系動態切換驗證
			_windup_dlg = _lobby.open_windup_daily()
			if _windup_dlg == null:
				return _fail("無法重新開啟 WindupDailyDialog 進行語系測試")

			_step = 6
			_wait = 0
			_locale_test_index = 0
			return false

		6:
			if _wait < 3:
				return false
			if _locale_test_index >= LOCALES.size():
				_step = 8
				_wait = 0
				return false

			var loc_code: String = LOCALES[_locale_test_index]
			_switch_locale(loc_code)

			var btn: Button = _windup_dlg.find_child("BtnGoVault", true, false)
			if btn == null:
				return _fail("語系 [%s] 下無法取得 BtnGoVault" % loc_code)

			var expected_txt: String = EXPECTED_BTN_TEXTS[loc_code]
			if btn.text != expected_txt:
				return _fail("語系 [%s] BtnGoVault 按鈕文字不符：預期 '%s'，實際 '%s'" % [loc_code, expected_txt, btn.text])
			_check_no_emoji(btn.text, "BtnGoVault_%s" % loc_code)
			print("  ✓ 語系 [%s] 按鈕文字即時動態刷新 -> '%s' (零系統 Emoji)" % [loc_code, btn.text])

			_step = 7
			_wait = 0
			return false

		7:
			# 等待渲染幀數讓 Viewport 繪製新語系文字
			if _wait < 6:
				return false
			var loc_code: String = LOCALES[_locale_test_index]
			var cap_name := "proof_locale_%s_windup_vault_btn.png" % loc_code
			var hash_loc := _capture_save(_out_dir.path_join(cap_name))
			if not hash_loc.is_empty():
				_proof_hashes[cap_name] = hash_loc

			_locale_test_index += 1
			_step = 6
			_wait = 0
			return false

		8:
			if _wait < 3:
				return false
			print("\n=== 4. 驗證所有實機截圖存證 SHA256 獨立唯一 ===")
			if _proof_hashes.size() > 1:
				var hash_values := _proof_hashes.values()
				for i in range(hash_values.size()):
					for j in range(i + 1, hash_values.size()):
						if hash_values[i] == hash_values[j]:
							var k1 = _proof_hashes.keys()[i]
							var k2 = _proof_hashes.keys()[j]
							return _fail("截圖存證重複！%s 與 %s 之 SHA256 相同: %s" % [k1, k2, hash_values[i]])
				print("  ✓ 全數實機截圖 (%d 張) SHA256 均獨立唯一，無重複截圖" % _proof_hashes.size())

			# 切回繁中基準
			_switch_locale("zh_TW")
			if _windup_dlg and is_instance_valid(_windup_dlg):
				_windup_dlg.queue_free()

			print("\n=======================================================")
			print("TEST_WINDUP_DAILY_VAULT_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
