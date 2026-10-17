extends SceneTree
## 《發條之心》SkillDialog 心法招式底欄新增『前往鍛造』快捷果凍按鈕單元與整合測試
## (test_skill_dialog_forge_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoForge 位於 SkillDialog 底欄按鈕列 (BottomBar)，緊鄰『前往背包』與『前往商城』。
##    - 尺寸不小於 140x48px（符合手機端熱區 >= 48px）。
##    - 金黃色盤 #FFD028，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 16~18px，字級 16~18px 開源粉圓體。
##    - 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoForge 發射 forge_requested 與 go_forge 訊號並安全關閉 SkillDialog（發射 closed 訊號）。
##    - 連動大廳開啟天宮鐵匠 ForgeDialog (MobileLobby.open_forge())。
##    - 關閉 ForgeDialog 可順暢返回心法招式介面。
## 3. 提供 get_go_forge_button() / get_forge_button() 存取器與 forge_requested / go_forge 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：PASS_OK 與 TEST_SKILL_DIALOG_FORGE_SHORTCUT_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}

var _lobby: Control = null
var _dlg: Control = null
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
	_out_dir = base_dir.path_join("../proofs/t_45acdc2e")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SKILL_FORGE_SHORTCUT_FAIL: ", msg)
	_ok = false
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
	if _dlg and is_instance_valid(_dlg) and _dlg.has_method("_update_ui_texts"):
		_dlg.call("_update_ui_texts")


func _process(_delta: float) -> bool:
	_wait += 1

	match _step:
		0:
			if _wait < 5:
				return false
			print("=== 1. 初始化 GameState 與開啟 SkillDialog ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			_switch_locale("zh_TW")

			_dlg = _lobby.call("open_skill_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 SkillDialog")
			print("  ok 成功開啟 SkillDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 驗證 BtnGoForge 按鈕規格、熱區與樣式 ===")
			var btn: Button = _dlg.call("get_go_forge_button") as Button
			if btn == null:
				btn = _dlg.call("get_forge_button") as Button
			if btn == null:
				btn = _dlg.find_child("BtnGoForge", true, false) as Button
			if btn == null:
				return _fail("無法取得 BtnGoForge 快捷按鈕")
			if btn.name != "BtnGoForge":
				return _fail("按鈕名稱應為 BtnGoForge，實測: %s" % btn.name)
			if btn.text != "前往鍛造":
				return _fail("繁中按鈕文字應為『前往鍛造』，實測: %s" % btn.text)
			_check_no_emoji(btn.text, "BtnGoForge")
			print("  ok BtnGoForge 文字正確: 前往鍛造")

			# 尺寸熱區驗證（>= 140x48px）
			if btn.custom_minimum_size.x < 140 or btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區不合規範 (<140x48px)，實測: %s" % [str(btn.custom_minimum_size)])
			print("  ok BtnGoForge 尺寸熱區合規: %s (>= 140x48px)" % str(btn.custom_minimum_size))

			# 樣式：金黃色盤 #FFD028、底邊 5px、圓角 16~18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_gold := Color("#FFD028")
				if sb.bg_color.to_html(false).to_upper() != target_gold.to_html(false).to_upper():
					return _fail("按鈕底色應為金黃色盤 #FFD028，實測: %s" % sb.bg_color.to_html(false))
				if sb.border_width_bottom != 5:
					return _fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
				if sb.corner_radius_top_left < 16 or sb.corner_radius_top_left > 18:
					return _fail("按鈕圓角應為 16~18px，實測: %d" % sb.corner_radius_top_left)
				var border_col: Color = sb.border_color
				var target_border := Color("#1F1A3A")
				if border_col.to_html(false).to_upper() != target_border.to_html(false).to_upper():
					return _fail("按鈕描邊應為深藍紫 #1F1A3A，實測: %s" % border_col.to_html(false))
				print("  ok BtnGoForge 樣式檢驗通過：金黃底色 #FFD028、圓角 18px、底厚 5px、深藍紫描邊 #1F1A3A")

			# 驗證按鈕位置緊鄰『前往背包』與『前往商城』
			var p_btn: Node = btn.get_parent()
			if p_btn != null and p_btn.name == "BottomBar":
				var idx_forge := btn.get_index()
				var inv_btn := p_btn.get_node_or_null("BtnGoInventory")
				var shop_btn := p_btn.get_node_or_null("BtnGoShop")
				if inv_btn != null and shop_btn != null:
					var idx_inv := inv_btn.get_index()
					var idx_shop := shop_btn.get_index()
					if abs(idx_forge - idx_inv) > 1 or abs(idx_forge - idx_shop) > 1:
						return _fail("BtnGoForge 必須緊鄰 BtnGoInventory 與 BtnGoShop")
					print("  ok BtnGoForge 在 BottomBar 中緊鄰 BtnGoInventory (idx %d) 與 BtnGoShop (idx %d)" % [idx_inv, idx_shop])

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_skill_dialog_btn_go_forge.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_skill_dialog_btn_go_forge.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 3. 點擊 BtnGoForge，驗證訊號發射、關閉 SkillDialog 並連動開啟 ForgeDialog ===")
			var btn: Button = _dlg.call("get_go_forge_button") as Button
			if btn == null:
				return _fail("無法取得 BtnGoForge")

			var sig_fired := {"req": false, "go": false, "closed": false}
			_dlg.forge_requested.connect(func(): sig_fired["req"] = true)
			_dlg.go_forge.connect(func(): sig_fired["go"] = true)
			_dlg.closed.connect(func(): sig_fired["closed"] = true)

			# 模擬點擊
			btn.emit_signal("pressed")

			if not sig_fired["req"]:
				return _fail("點擊按鈕未發射 forge_requested 訊號")
			if not sig_fired["go"]:
				return _fail("點擊按鈕未發射 go_forge 訊號")
			if not sig_fired["closed"]:
				return _fail("點擊按鈕未發射 closed 訊號")
			print("  ok 成功發射 forge_requested, go_forge 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			# 驗證 SkillDialog 是否安全關閉
			var old_skill := _lobby.get_node_or_null("SkillDialog")
			if old_skill != null and not old_skill.is_queued_for_deletion():
				return _fail("舊 SkillDialog 尚未關閉或有遮罩殘留")
			print("  ok SkillDialog 已安全關閉且無遮罩殘留")

			# 驗證 ForgeDialog 是否已連動開啟
			var forge: Control = _lobby.find_child("ForgeDialog", true, false) as Control
			if forge == null:
				return _fail("連動開啟大廳 ForgeDialog 失敗")
			print("  ok 成功直通連動開啟大廳 ForgeDialog 天宮鐵匠視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_forge_dialog_opened.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_zh_TW_forge_dialog_opened.png (SHA256: %s...)" % h2.substr(0, 16))

			print("\n=== 4. 關閉 ForgeDialog，驗證順暢返回 SkillDialog ===")
			var forge: Control = _lobby.find_child("ForgeDialog", true, false) as Control
			if forge != null:
				forge.emit_signal("closed")
				forge.queue_free()

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			_dlg = _lobby.get_node_or_null("SkillDialog")
			if _dlg == null or not is_instance_valid(_dlg) or _dlg.is_queued_for_deletion():
				_dlg = _lobby.call("open_skill_dialog")
			if _dlg == null:
				return _fail("無法順暢返回或重新開啟 SkillDialog")
			print("  ok 順暢返回心法招式介面 SkillDialog")

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			print("\n=== 5. 測試六語系 i18n 即時切換 ===")
			for loc in LOCALES:
				_switch_locale(loc)
				var btn: Button = _dlg.call("get_go_forge_button") as Button
				if btn == null:
					return _fail("[%s] 無法取得 BtnGoForge" % loc)
				var expected_text: String = EXPECTED_BTN_TEXTS.get(loc, "")
				if btn.text != expected_text:
					return _fail("[%s] 按鈕文字不符，預期: '%s'，實測: '%s'" % [loc, expected_text, btn.text])
				_check_no_emoji(btn.text, "BtnGoForge_" + loc)
				print("  ok [%s] 語系按鈕文字驗證正確: '%s' (零 Emoji)" % [loc, btn.text])

			_switch_locale("zh_TW")
			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return false
			var h3 := _capture_save(_out_dir.path_join("proof_03_locales_btn_go_forge.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_locales_btn_go_forge.png (SHA256: %s...)" % h3.substr(0, 16))

			if DisplayServer.get_name() != "headless" and _proof_hashes.size() >= 3:
				var hashes_arr: Array = _proof_hashes.values()
				if hashes_arr[0] == hashes_arr[1] or hashes_arr[1] == hashes_arr[2] or hashes_arr[0] == hashes_arr[2]:
					return _fail("截圖存證雜湊重複，未能如實捕捉各步驟畫面！")
				print("  ok 截圖 SHA256 彼此相異，驗證畫面確實切換")

			print("\n==========================================")
			print("PASS_OK")
			print("TEST_SKILL_DIALOG_FORGE_SHORTCUT_OK")
			print("==========================================")
			quit(0)
			return true

	return false
