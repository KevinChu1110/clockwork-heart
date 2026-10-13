extends SceneTree
## 《發條之心》TitleWallDialog 稱號牆新增『卸下稱號』果凍按鈕與連動安全防護單元與整合測試
## (test_title_unequip.gd)
##
## 驗收規範：
## 1. 按鈕屬性與樣式：BtnUnequipTitle 高度 >= 50px（160x52px），珊瑚粉色盤 #FF5E8A，圓角 18px，底邊 5px，字級 18px >= 16px，零 Emoji。
## 2. 安全防呆：當玩家當前未佩戴特殊稱號（即為初出茅廬或空）時，按鈕安全置灰（disabled == true），防止無效操作。
## 3. 點擊卸下邏輯：佩戴特殊稱號後按鈕啟用，點擊後安全卸下稱號，觸發 title_unequipped 訊號，GameState.set_equipped_title("") 重設為預設『初出茅廬』。
## 4. 大廳名牌即時同步：大廳頭頂稱號名牌即時同步刷新回歸預設『初出茅廬』。
## 5. 六語系 i18n 字典支援：zh_TW, zh_CN, en, ja, ko, es 均正確翻譯且無系統 Emoji。
## 6. 哨兵輸出：TEST_TITLE_UNEQUIP_OK。

const MobileLobbyScn = preload("res://scripts/ui/mobile_lobby.gd")
const TitleWallDialogScn = preload("res://scripts/ui/title_wall_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_UNEQUIP_BTN_TEXTS: Dictionary = {
	"zh_TW": "卸下稱號",
	"zh_CN": "卸下称号",
	"en": "Unequip Title",
	"ja": "称号を外す",
	"ko": "칭호 해제",
	"es": "Desequipar título"
}
const EXPECTED_DEFAULT_TITLES: Dictionary = {
	"zh_TW": "初出茅廬",
	"zh_CN": "初出茅庐",
	"en": "Fledgling Novice",
	"ja": "駆け出し",
	"ko": "풋내기 모험가",
	"es": "Novato Principiante"
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
	_out_dir = base_dir.path_join("../proofs/t_71a3c58d")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_lobby = MobileLobbyScn.new()
	_lobby.name = "MobileLobby"
	root.add_child(_lobby)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("TITLE_UNEQUIP_FAIL: ", msg)
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
			print("=== 1. 驗證 GameState 持久化保存、重設與 set_equipped_title(\"\") ===")
			var gs: Node = root.get_node_or_null("GameState")
			if gs == null:
				return _fail("無法取得 GameState 單例")

			gs.reset_new_game()
			if gs.get_equipped_title() != "初出茅廬":
				return _fail("GameState 預設稱號應為『初出茅廬』")

			# 佩戴特殊稱號
			gs.set_equipped_title("看破者")
			if gs.get_equipped_title() != "看破者":
				return _fail("GameState 佩戴稱號未更新為『看破者』")

			# 測試重設為空字串安全回歸預設
			var sig_state := {"fired": false, "title": ""}
			var change_cb := func(new_t: String):
				sig_state["fired"] = true
				sig_state["title"] = new_t
			gs.equipped_title_changed.connect(change_cb)
			gs.set_equipped_title("")
			gs.equipped_title_changed.disconnect(change_cb)

			if gs.get_equipped_title() != "初出茅廬":
				return _fail("GameState.set_equipped_title(\"\") 未正確回歸預設『初出茅廬』")
			if not sig_state["fired"]:
				return _fail("GameState.set_equipped_title(\"\") 未觸發 equipped_title_changed 訊號")
			print("  ok GameState.set_equipped_title(\"\") 安全重設為『初出茅廬』並觸發訊號")

			_switch_locale("zh_TW")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return false
			print("\n=== 2. 開啟 TitleWallDialog，驗證 BtnUnequipTitle 按鈕屬性、樣式與預設置灰防呆 ===")
			_dlg = _lobby.call("open_title_wall_dialog")
			if _dlg == null:
				return _fail("無法透過大廳開啟 TitleWallDialog 稱號牆視窗")
			print("  ok 成功開啟 TitleWallDialog 稱號牆視窗")

			var unequip_btn := _dlg.call("get_unequip_button") as Button
			if unequip_btn == null:
				unequip_btn = _dlg.find_child("BtnUnequipTitle", true, false) as Button
			if unequip_btn == null:
				return _fail("TitleWallDialog 找不到 BtnUnequipTitle 按鈕")

			# 驗證尺寸：高 >= 50px（160x52px）
			if unequip_btn.custom_minimum_size.y < 50:
				return _fail("BtnUnequipTitle 尺寸高度需 >= 50px，實際為: %f" % unequip_btn.custom_minimum_size.y)
			if unequip_btn.custom_minimum_size.x < 140:
				return _fail("BtnUnequipTitle 尺寸寬度需 >= 140px，實際為: %f" % unequip_btn.custom_minimum_size.x)
			print("  ok 按鈕尺寸合格: %s (寬 %d, 高 %d >= 50px)" % [unequip_btn.name, unequip_btn.custom_minimum_size.x, unequip_btn.custom_minimum_size.y])

			# 驗證字級 >= 16px
			var font_sz: int = unequip_btn.get_theme_font_size("font_size")
			if font_sz < 16:
				return _fail("BtnUnequipTitle 字級需 >= 16px，實際為: %d" % font_sz)
			print("  ok 按鈕字級合格: %dpx >= 16px" % font_sz)

			# 驗證多巴胺珊瑚粉 #FF5E8A 樣式與立體厚底規範
			var normal_sb = unequip_btn.get_theme_stylebox("normal") as StyleBoxFlat
			if normal_sb == null:
				return _fail("BtnUnequipTitle normal 樣式應為 StyleBoxFlat")
			if normal_sb.bg_color != Color("#FF5E8A"):
				return _fail("BtnUnequipTitle 底色應為珊瑚粉 #FF5E8A，實際為: %s" % str(normal_sb.bg_color))
			if normal_sb.border_width_bottom != 5:
				return _fail("BtnUnequipTitle 底邊厚底應為 5px，實際為: %d" % normal_sb.border_width_bottom)
			if normal_sb.corner_radius_top_left != 18:
				return _fail("BtnUnequipTitle 圓角應為 18px，實際為: %d" % normal_sb.corner_radius_top_left)
			print("  ok 按鈕外觀完全符合多巴胺珊瑚粉 (#FF5E8A)、圓角 18px、底邊 5px 立體厚底規範")

			# 驗證預設置灰防呆（當玩家當前為初出茅廬或空時，按鈕置灰 disabled）
			if not unequip_btn.disabled:
				return _fail("玩家佩戴預設稱號時，BtnUnequipTitle 應安全置灰（disabled == true）")
			if not _dlg.call("is_unequip_button_disabled"):
				return _fail("is_unequip_button_disabled() 應回傳 true")
			print("  ok 預設防呆成功：未佩戴特殊稱號時按鈕正確置灰（disabled 樣式）防止無效操作")

			_check_no_emoji(unequip_btn.text, "BtnUnequipTitle")

			# 存證 01: 預設狀態按鈕置灰防呆
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_zh_TW_title_wall_disabled_default.png"))

			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return false
			print("\n=== 3. 佩戴特殊稱號『以劍抵爪』，驗證按鈕啟用高亮與大廳同步 ===")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set_flag("title.claw_parry", true)
			gs.set_flag("title.fog_seer", true)
			_dlg.call("_update_ui_texts")

			# 點擊佩戴以劍抵爪
			var card_claw := _dlg.call("get_card_by_flag", "title.claw_parry") as PanelContainer
			if card_claw == null:
				return _fail("稱號牆找不到『title.claw_parry』卡片")
			_dlg.call("_on_card_clicked", card_claw)

			if gs.get_equipped_title() != "以劍抵爪":
				return _fail("佩戴以劍抵爪失敗，當前: %s" % gs.get_equipped_title())

			var unequip_btn := _dlg.call("get_unequip_button") as Button
			if unequip_btn.disabled:
				return _fail("佩戴特殊稱號後，BtnUnequipTitle 應解除置灰（disabled == false）")
			print("  ok 佩戴特殊稱號『以劍抵爪』後，按鈕成功解除置灰，呈現可點擊立體珊瑚粉樣式！")

			# 驗證卡片顯示 ✓ 佩戴中
			var badge_claw: Label = card_claw.find_child("BadgeLabel", true, false) as Label
			if badge_claw == null or badge_claw.text != "✓ 佩戴中":
				return _fail("卡片標籤應為『✓ 佩戴中』")

			# 存證 02: 佩戴特殊稱號，按鈕亮粉色啟用
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_zh_TW_title_wall_equipped_special.png"))

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			print("\n=== 4. 點擊『卸下稱號』，驗證卸下邏輯、訊號發射、卡片復原與按鈕重新置灰 ===")
			var gs: Node = root.get_node_or_null("GameState")
			var unequip_sig := {"fired": false}
			var sig_cb := func():
				unequip_sig["fired"] = true
			_dlg.title_unequipped.connect(sig_cb)

			# 模擬點擊卸下按鈕
			var unequip_btn := _dlg.call("get_unequip_button") as Button
			_dlg.call("_on_unequip_pressed")
			_dlg.title_unequipped.disconnect(sig_cb)

			if not unequip_sig["fired"]:
				return _fail("點擊卸下稱號未觸發 title_unequipped 訊號")
			print("  ok 成功觸發 title_unequipped 訊號")

			if gs.get_equipped_title() != "初出茅廬":
				return _fail("點擊卸下稱號後，GameState 稱號未重設為『初出茅廬』，當前: %s" % gs.get_equipped_title())
			print("  ok GameState.get_equipped_title() 成功恢復為『初出茅廬』")

			# 驗證稱號卡片恢復為已解鎖，光框消失
			var card_claw := _dlg.call("get_card_by_flag", "title.claw_parry") as PanelContainer
			var badge_claw: Label = card_claw.find_child("BadgeLabel", true, false) as Label
			if badge_claw == null or badge_claw.text != "已解鎖":
				return _fail("卸下後以劍抵爪標籤應恢復為『已解鎖』，實際為: %s" % (badge_claw.text if badge_claw else "null"))
			var is_claw_eq: bool = _dlg.call("is_card_equipped", "title.claw_parry")
			if is_claw_eq:
				return _fail("以劍抵爪卡片不應為已佩戴狀態")

			# 驗證按鈕重新置灰防呆
			if not unequip_btn.disabled:
				return _fail("卸下稱號後，BtnUnequipTitle 應重新安全置灰（disabled == true）")
			print("  ok 卸下完成後，卡片恢復『已解鎖』，按鈕重新安全置灰（disabled 樣式）！")

			# 存證 03: 卸下後稱號牆
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_zh_TW_title_wall_after_unequip.png"))

			# 關閉彈窗回到大廳驗證大廳頭頂名牌連動
			_dlg.queue_free()
			_dlg = null
			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n=== 5. 驗證大廳頭頂稱號名牌即時同步刷新回歸預設『【初出茅廬】』 ===")
			var lobby_title: String = _lobby.call("get_hero_title_text")
			if lobby_title != "【初出茅廬】":
				return _fail("大廳頭頂名牌未即時刷新為『【初出茅廬】』，實際為: %s" % lobby_title)
			print("  ok 大廳頭頂稱號名牌即時連動刷新回歸預設: %s" % lobby_title)

			# 存證 04: 大廳名牌回歸預設
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_zh_TW_lobby_after_unequip.png"))

			# 重新開啟彈窗並佩戴特殊稱號，切換英文進行六語系驗證
			_dlg = _lobby.call("open_title_wall_dialog")
			var gs: Node = root.get_node_or_null("GameState")
			gs.set_flag("title.claw_parry", true)
			_dlg.call("equip_title", "title.claw_parry")
			_switch_locale("en")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			print("\n=== 6. 驗證英文 (en) 語系：BtnUnequipTitle 與多語系即時切換 ===")
			var unequip_btn := _dlg.call("get_unequip_button") as Button
			if unequip_btn.text != "Unequip Title":
				return _fail("英文語系按鈕文字應為『Unequip Title』，實際為: %s" % unequip_btn.text)
			print("  ok 英文按鈕文字正確: %s" % unequip_btn.text)
			_check_no_emoji(unequip_btn.text, "BtnUnequipTitle_en")

			# 英文語系下執行卸下
			_dlg.call("unequip_title")
			if not unequip_btn.disabled:
				return _fail("英文語系卸下後按鈕應置灰")
			print("  ok 英文語系卸下功能正常且置灰防呆有效")

			# 存證 05: 英文語系稱號牆
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_en_title_wall_unequip.png"))

			# 重新佩戴並切換日文語系
			_dlg.call("equip_title", "title.claw_parry")
			_switch_locale("ja")

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n=== 7. 驗證日語 (ja) 語系：BtnUnequipTitle 與多語系即時切換 ===")
			var unequip_btn := _dlg.call("get_unequip_button") as Button
			if unequip_btn.text != "称号を外す":
				return _fail("日語語系按鈕文字應為『称号を外す』，實際為: %s" % unequip_btn.text)
			print("  ok 日語按鈕文字正確: %s" % unequip_btn.text)
			_check_no_emoji(unequip_btn.text, "BtnUnequipTitle_ja")

			# 日語語系下執行卸下
			_dlg.call("unequip_title")
			if not unequip_btn.disabled:
				return _fail("日語語系卸下後按鈕應置灰")
			print("  ok 日語語系卸下功能正常且置灰防呆有效")

			# 存證 06: 日文語系稱號牆
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_ja_title_wall_unequip.png"))

			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			print("\n=== 8. 驗證六語系完整切換無遺漏、無 Emoji ===")
			var unequip_btn := _dlg.call("get_unequip_button") as Button
			for loc in LOCALES:
				_switch_locale(loc)
				var expected_btn: String = str(EXPECTED_UNEQUIP_BTN_TEXTS.get(loc, ""))
				if unequip_btn.text != expected_btn:
					return _fail("語系 %s 按鈕文字不符，預期: %s，實際: %s" % [loc, expected_btn, unequip_btn.text])
				_check_no_emoji(unequip_btn.text, "BtnUnequipTitle_" + loc)
				print("  ok [%s] 語系字典驗證通過: 『%s』" % [loc, unequip_btn.text])

			if DisplayServer.get_name() != "headless":
				print("\n=== 9. 驗證實機截圖完整產出且 SHA256 不重複 ===")
				var seen_hashes := {}
				for key in _proof_hashes.keys():
					var h: String = _proof_hashes[key]
					if h.is_empty():
						return _fail("截圖 %s 雜湊為空" % key)
					if seen_hashes.has(h):
						return _fail("截圖 %s 與 %s SHA256 重複: %s" % [key, seen_hashes[h], h])
					seen_hashes[h] = key
					print("  ok 截圖存證 %s 通過: %s" % [key, h.substr(0, 16)])

			print("\n==========================================")
			print("🎉 全部單元與整合測試通過！")
			print("TEST_TITLE_UNEQUIP_OK")
			print("==========================================")
			quit(0)
			return true

	return false
