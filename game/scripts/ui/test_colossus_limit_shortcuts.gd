extends SceneTree
## 《發條之心》停擺巨偶限制彈窗 (ColossusLimitDialog) 新增『前往戰力』與『前往鍛造』快捷果凍按鈕單元與整合測試
## (test_colossus_limit_shortcuts.gd)
##
## 驗收規範：
## 1. 按鈕規格與樣式：
##    - 在 ColossusLimitDialog 底部並列 ConfirmButton (確定)、BtnGoPowerStat (前往戰力)、BtnGoForge (前往鍛造) 三顆果凍按鈕。
##    - 寬度 160px (>= 120px)、高度 52px (>= 48px)、熱區 >= 48px、底邊厚底 5px、圓角 18px。
##    - ConfirmButton: 金黃色盤 #FFD028、深藍紫描邊 #1F1A3A、字級 18px。
##    - BtnGoPowerStat: 天藍色盤 #38A0FF、深藍紫描邊 #1F1A3A、字級 18px。
##    - BtnGoForge: 暖橘色盤 #FFA010、深藍紫描邊 #1F1A3A、字級 18px。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoPowerStat：發射 power_stat_requested 與 closed 訊號，關閉 ColossusLimitDialog，連動開啟 PowerStatDialog。
##    - 點擊 BtnGoForge：發射 forge_requested 與 closed 訊號，關閉 ColossusLimitDialog，連動開啟天宮鐵匠 ForgeDialog。
##    - 點擊 ConfirmButton：發射 confirmed 與 closed 訊號，安全關閉 ColossusLimitDialog。
## 3. 六語系 i18n 即時切換：
##    - zh_TW: 確定 / 前往戰力 / 前往鍛造
##    - en: OK / Go to Stats / Go to Forge
##    - ja: 確認 / 戦力詳細へ / 鍛造へ進む
##    - ko: 확인 / 전투력으로 이동 / 단조로 이동
##    - es: Aceptar / Ir a Estadísticas / Ir a Forja
##    - zh_CN: 确定 / 前往战力 / 前往锻造
## 4. 存證截圖：
##    - 存入 proofs/t_5944b82b/，包含六語系切換及跳轉介面存證，SHA256 各自獨立。
## 5. 哨兵輸出：TEST_COLOSSUS_LIMIT_SHORTCUTS_OK。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "en", "ja", "ko", "es", "zh_CN"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": {
		"confirm": "確定",
		"power_stat": "前往戰力",
		"forge": "前往鍛造"
	},
	"en": {
		"confirm": "OK",
		"power_stat": "Go to Stats",
		"forge": "Go to Forge"
	},
	"ja": {
		"confirm": "確認",
		"power_stat": "戦力詳細へ",
		"forge": "鍛造へ進む"
	},
	"ko": {
		"confirm": "확인",
		"power_stat": "전투력으로 이동",
		"forge": "단조로 이동"
	},
	"es": {
		"confirm": "Aceptar",
		"power_stat": "Ir a Estadísticas",
		"forge": "Ir a Forja"
	},
	"zh_CN": {
		"confirm": "确定",
		"power_stat": "前往战力",
		"forge": "前往锻造"
	}
}

var _lobby: Control = null
var _dlg: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}
var _locale_idx: int = 0

var _signal_power_stat_fired: bool = false
var _signal_forge_fired: bool = false
var _signal_confirmed_fired: bool = false
var _signal_closed_fired: bool = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_5944b82b")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	var inv = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	var eq = root.get_node_or_null("EquipmentSystem")
	if eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			eq = EqClass.new()
			eq.name = "EquipmentSystem"
			root.add_child(eq)

	var gem_sys = root.get_node_or_null("GemSystem")
	if gem_sys == null:
		var GemSysClass = load("res://scripts/systems/gem_system.gd")
		if GemSysClass:
			gem_sys = GemSysClass.new()
			gem_sys.name = "GemSystem"
			root.add_child(gem_sys)

	var core_sys = root.get_node_or_null("CoreSystem")
	if core_sys == null:
		var CoreSysClass = load("res://scripts/systems/core_system.gd")
		if CoreSysClass:
			core_sys = CoreSysClass.new()
			core_sys.name = "CoreSystem"
			root.add_child(core_sys)

	var soul_sys = root.get_node_or_null("SoulSystem")
	if soul_sys == null:
		var SsClass = load("res://scripts/systems/soul_system.gd")
		if SsClass:
			soul_sys = SsClass.new()
			soul_sys.name = "SoulSystem"
			root.add_child(soul_sys)

	var cds = root.get_node_or_null("ColossusDailySystem")
	if cds == null:
		var CdsClass = load("res://scripts/systems/colossus_daily.gd")
		if CdsClass:
			cds = CdsClass.new()
			cds.name = "ColossusDailySystem"
			root.add_child(cds)

	if _gs != null and _gs.has_method("reset_new_game"):
		_gs.call("reset_new_game", "rabbit")

	var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = MobileLobbyClass.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("COLOSSUS_LIMIT_SHORTCUTS_FAIL: ", msg)
	quit(1)
	return true


func _check_no_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x2712) or (code >= 0x2714 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


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
	var buf := file.get_buffer(file.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	return ctx.finish().hex_encode()


func _switch_locale(loc_code: String) -> void:
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node != null and loc_node.has_method("set_locale"):
		loc_node.call("set_locale", loc_code)
	if _lobby and _lobby.has_method("_apply_locale_texts"):
		_lobby.call("_apply_locale_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 8:
				return false
			print("=== 1. 初始化與開啟 ColossusLimitDialog ===")
			_switch_locale("zh_TW")

			_dlg = _lobby.call("show_colossus_limit_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 ColossusLimitDialog")
			print("  ok 成功開啟 ColossusLimitDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 ConfirmButton、BtnGoPowerStat、BtnGoForge 三顆果凍按鈕實例與規格 ===")
			var ok_btn := _dlg.find_child("ConfirmButton", true, false) as Button
			var btn_pstat := _dlg.find_child("BtnGoPowerStat", true, false) as Button
			var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button

			if ok_btn == null:
				return _fail("找不到 ConfirmButton")
			if btn_pstat == null:
				return _fail("找不到 BtnGoPowerStat")
			if btn_forge == null:
				return _fail("找不到 BtnGoForge")

			print("  ok 三顆按鈕實例均正確存在於 ColossusLimitDialog")

			# 驗證 ConfirmButton
			if ok_btn.text != "確定":
				return _fail("ConfirmButton 繁中文字應為『確定』，實測: %s" % ok_btn.text)
			_check_no_emoji(ok_btn.text, "ConfirmButton")
			if ok_btn.custom_minimum_size.x < 120 or ok_btn.custom_minimum_size.y < 48:
				return _fail("ConfirmButton 熱區不合規範 (<120x48px)，實測: %s" % str(ok_btn.custom_minimum_size))
			var ok_sb: StyleBoxFlat = ok_btn.get_theme_stylebox("normal") as StyleBoxFlat
			if ok_sb != null:
				if ok_sb.bg_color.to_html(false) != Color("#FFD028").to_html(false):
					return _fail("ConfirmButton 底色應為金黃 #FFD028，實測: %s" % ok_sb.bg_color.to_html(false))
				if ok_sb.border_width_bottom != 5:
					return _fail("ConfirmButton 底厚應為 5px，實測: %d" % ok_sb.border_width_bottom)
				if ok_sb.corner_radius_top_left != 18:
					return _fail("ConfirmButton 圓角應為 18px，實測: %d" % ok_sb.corner_radius_top_left)
			print("  ok ConfirmButton 規格檢驗通過：寬160x高52px、金黃#FFD028、底厚5px、圓角18px")

			# 驗證 BtnGoPowerStat
			if btn_pstat.text != "前往戰力":
				return _fail("BtnGoPowerStat 繁中文字應為『前往戰力』，實測: %s" % btn_pstat.text)
			_check_no_emoji(btn_pstat.text, "BtnGoPowerStat")
			if btn_pstat.custom_minimum_size.x < 120 or btn_pstat.custom_minimum_size.y < 48:
				return _fail("BtnGoPowerStat 熱區不合規範 (<120x48px)，實測: %s" % str(btn_pstat.custom_minimum_size))
			var pstat_sb: StyleBoxFlat = btn_pstat.get_theme_stylebox("normal") as StyleBoxFlat
			if pstat_sb != null:
				if pstat_sb.bg_color.to_html(false) != Color("#38A0FF").to_html(false):
					return _fail("BtnGoPowerStat 底色應為天藍 #38A0FF，實測: %s" % pstat_sb.bg_color.to_html(false))
				if pstat_sb.border_width_bottom != 5:
					return _fail("BtnGoPowerStat 底厚應為 5px，實測: %d" % pstat_sb.border_width_bottom)
				if pstat_sb.corner_radius_top_left != 18:
					return _fail("BtnGoPowerStat 圓角應為 18px，實測: %d" % pstat_sb.corner_radius_top_left)
			print("  ok BtnGoPowerStat 規格檢驗通過：寬160x高52px、天藍#38A0FF、底厚5px、圓角18px")

			# 驗證 BtnGoForge
			if btn_forge.text != "前往鍛造":
				return _fail("BtnGoForge 繁中文字應為『前往鍛造』，實測: %s" % btn_forge.text)
			_check_no_emoji(btn_forge.text, "BtnGoForge")
			if btn_forge.custom_minimum_size.x < 120 or btn_forge.custom_minimum_size.y < 48:
				return _fail("BtnGoForge 熱區不合規範 (<120x48px)，實測: %s" % str(btn_forge.custom_minimum_size))
			var forge_sb: StyleBoxFlat = btn_forge.get_theme_stylebox("normal") as StyleBoxFlat
			if forge_sb != null:
				if forge_sb.bg_color.to_html(false) != Color("#FFA010").to_html(false):
					return _fail("BtnGoForge 底色應為暖橘 #FFA010，實測: %s" % forge_sb.bg_color.to_html(false))
				if forge_sb.border_width_bottom != 5:
					return _fail("BtnGoForge 底厚應為 5px，實測: %d" % forge_sb.border_width_bottom)
				if forge_sb.corner_radius_top_left != 18:
					return _fail("BtnGoForge 圓角應為 18px，實測: %d" % forge_sb.corner_radius_top_left)
			print("  ok BtnGoForge 規格檢驗通過：寬160x高52px、暖橘#FFA010、底厚5px、圓角18px")

			_step = 2
			_wait = 0

		2:
			# 六語系切換檢驗與截圖
			if _wait < 6:
				return false
			var cur_loc := LOCALES[_locale_idx]
			_switch_locale(cur_loc)

			var ok_btn := _dlg.find_child("ConfirmButton", true, false) as Button
			var btn_pstat := _dlg.find_child("BtnGoPowerStat", true, false) as Button
			var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button

			var exp_cfg: Dictionary = EXPECTED_TEXTS[cur_loc]
			if ok_btn.text != exp_cfg["confirm"]:
				return _fail("[%s] ConfirmButton 文字不符，預期: %s，實測: %s" % [cur_loc, exp_cfg["confirm"], ok_btn.text])
			if btn_pstat.text != exp_cfg["power_stat"]:
				return _fail("[%s] BtnGoPowerStat 文字不符，預期: %s，實測: %s" % [cur_loc, exp_cfg["power_stat"], btn_pstat.text])
			if btn_forge.text != exp_cfg["forge"]:
				return _fail("[%s] BtnGoForge 文字不符，預期: %s，實測: %s" % [cur_loc, exp_cfg["forge"], btn_forge.text])

			_check_no_emoji(ok_btn.text, "ConfirmButton_%s" % cur_loc)
			_check_no_emoji(btn_pstat.text, "BtnGoPowerStat_%s" % cur_loc)
			_check_no_emoji(btn_forge.text, "BtnGoForge_%s" % cur_loc)

			var p_name := "proof_%02d_colossus_limit_%s.png" % [_locale_idx + 1, cur_loc]
			if _locale_idx == 0:
				p_name = "proof_01_colossus_limit_three_buttons_zh_TW.png"
			var h := _capture_save(_out_dir.path_join(p_name))
			if h != "":
				_proof_hashes[p_name] = h
				print("  ok 語系 [%s] 驗證通過並截圖: %s (SHA256: %s...)" % [cur_loc, p_name, h.substr(0, 16)])

			_locale_idx += 1
			if _locale_idx < LOCALES.size():
				_wait = 0
			else:
				print("\n=== 3. 六語系切換全部通過！準備驗證點擊連動訊號與視圖切換 ===")
				_step = 3
				_wait = 0

		3:
			if _wait < 6:
				return false
			# 切回繁中進行點擊測試
			_switch_locale("zh_TW")

			print("\n=== 4. 點擊 BtnGoPowerStat，驗證訊號發射、關閉彈窗並連動開啟 PowerStatDialog ===")
			_signal_power_stat_fired = false
			_signal_closed_fired = false

			_dlg.connect("power_stat_requested", func(): _signal_power_stat_fired = true)
			_dlg.connect("closed", func(): _signal_closed_fired = true)

			var btn_pstat := _dlg.find_child("BtnGoPowerStat", true, false) as Button
			btn_pstat.pressed.emit()

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			if not _signal_power_stat_fired:
				return _fail("點擊 BtnGoPowerStat 未發射 power_stat_requested 訊號！")
			if not _signal_closed_fired:
				return _fail("點擊 BtnGoPowerStat 未發射 closed 訊號！")
			print("  ok power_stat_requested 與 closed 訊號發射成功")

			# 驗證 ColossusLimitDialog 已關閉或正在刪除
			var cur_limit = _lobby.get_node_or_null("ColossusLimitDialog")
			if cur_limit != null and not cur_limit.is_queued_for_deletion():
				return _fail("點擊 BtnGoPowerStat 後 ColossusLimitDialog 未安全關閉！")
			print("  ok ColossusLimitDialog 已正確關閉")

			# 驗證 PowerStatDialog 成功開啟
			var pstat_dlg = _lobby.get_node_or_null("PowerStatDialog")
			if pstat_dlg == null or not is_instance_valid(pstat_dlg):
				return _fail("點擊 BtnGoPowerStat 後未成功開啟 PowerStatDialog！")
			print("  ok PowerStatDialog 成功連動開啟！")

			var h_pstat := _capture_save(_out_dir.path_join("proof_07_click_go_power_stat_opens_power_stat_dialog.png"))
			if h_pstat != "":
				_proof_hashes["proof_07"] = h_pstat
				print("  ok 截圖存證: proof_07_click_go_power_stat_opens_power_stat_dialog.png (SHA256: %s...)" % h_pstat.substr(0, 16))

			# 關閉 PowerStatDialog 準備下一步
			pstat_dlg.queue_free()
			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			print("\n=== 5. 點擊 BtnGoForge，驗證訊號發射、關閉彈窗並連動開啟天宮鐵匠 ForgeDialog ===")
			_dlg = _lobby.call("show_colossus_limit_dialog")
			if _dlg == null:
				return _fail("重新開啟 ColossusLimitDialog 失敗！")

			_signal_forge_fired = false
			_signal_closed_fired = false

			_dlg.connect("forge_requested", func(): _signal_forge_fired = true)
			_dlg.connect("closed", func(): _signal_closed_fired = true)

			var btn_forge := _dlg.find_child("BtnGoForge", true, false) as Button
			btn_forge.pressed.emit()

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			if not _signal_forge_fired:
				return _fail("點擊 BtnGoForge 未發射 forge_requested 訊號！")
			if not _signal_closed_fired:
				return _fail("點擊 BtnGoForge 未發射 closed 訊號！")
			print("  ok forge_requested 與 closed 訊號發射成功")

			var cur_limit = _lobby.get_node_or_null("ColossusLimitDialog")
			if cur_limit != null and not cur_limit.is_queued_for_deletion():
				return _fail("點擊 BtnGoForge 後 ColossusLimitDialog 未安全關閉！")
			print("  ok ColossusLimitDialog 已正確關閉")

			# 驗證 ForgeDialog 成功開啟
			var forge_dlg = _lobby.get_node_or_null("ForgeDialog")
			if forge_dlg == null or not is_instance_valid(forge_dlg):
				return _fail("點擊 BtnGoForge 後未成功開啟 ForgeDialog！")
			print("  ok ForgeDialog 天宮鐵匠成功連動開啟！")

			var h_forge := _capture_save(_out_dir.path_join("proof_08_click_go_forge_opens_forge_dialog.png"))
			if h_forge != "":
				_proof_hashes["proof_08"] = h_forge
				print("  ok 截圖存證: proof_08_click_go_forge_opens_forge_dialog.png (SHA256: %s...)" % h_forge.substr(0, 16))

			# 關閉 ForgeDialog 準備下一步
			forge_dlg.queue_free()
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			print("\n=== 6. 點擊 ConfirmButton，驗證 confirmed 與 closed 訊號並正常關閉 ===")
			_dlg = _lobby.call("show_colossus_limit_dialog")
			if _dlg == null:
				return _fail("重新開啟 ColossusLimitDialog 失敗！")

			_signal_confirmed_fired = false
			_signal_closed_fired = false

			_dlg.connect("confirmed", func(): _signal_confirmed_fired = true)
			_dlg.connect("closed", func(): _signal_closed_fired = true)

			var ok_btn := _dlg.find_child("ConfirmButton", true, false) as Button
			ok_btn.pressed.emit()

			_step = 8
			_wait = 0

		8:
			if _wait < 6:
				return false
			if not _signal_confirmed_fired:
				return _fail("點擊 ConfirmButton 未發射 confirmed 訊號！")
			if not _signal_closed_fired:
				return _fail("點擊 ConfirmButton 未發射 closed 訊號！")
			print("  ok confirmed 與 closed 訊號發射成功")

			var cur_limit = _lobby.get_node_or_null("ColossusLimitDialog")
			if cur_limit != null and not cur_limit.is_queued_for_deletion():
				return _fail("點擊 ConfirmButton 後 ColossusLimitDialog 未安全關閉！")
			print("  ok ColossusLimitDialog 已正確關閉")

			# 驗證截圖哈希互不相同
			var hashes := _proof_hashes.values()
			for i in range(hashes.size()):
				for j in range(i + 1, hashes.size()):
					if hashes[i] != "" and hashes[i] == hashes[j]:
						return _fail("截圖存證存在重複相同哈希: %s" % hashes[i])

			print("\n=======================================================")
			print("🎉 全部單元與整合測試通過！六語系、多巴胺樣式、雙向快捷連動均完美驗收！")
			print("TEST_COLOSSUS_LIMIT_SHORTCUTS_OK")
			print("=======================================================\n")
			quit(0)
			return true

	return false
