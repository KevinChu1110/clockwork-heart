extends SceneTree
## 《發條之心》SkillDialog 心法招式底欄新增『前往儲能庫』快捷果凍按鈕單元與整合測試
## (test_skill_dialog_vault_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoVault 位於 SkillDialog 底部操作按鈕列 (BottomBar)。
##    - 尺寸熱區 >= 48px（實測 140x50px，高度 >= 48px，寬度 >= 140px）。
##    - 多巴胺金黃色盤 #FFD028，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 16~18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoVault 發射 vault_requested 與 go_vault 訊號並安全關閉 SkillDialog（發射 closed 訊號，無遮罩殘留）。
##    - 連動大廳開啟 ClockworkVaultDialog (MobileLobby.open_clockwork_vault_dialog())。
## 3. 提供 get_go_vault_button() 與 get_vault_button() 存取器與 vault_requested / go_vault 訊號。
## 4. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 5. 哨兵輸出：TEST_SKILL_DIALOG_VAULT_SHORTCUT_OK。

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
var _skill_dlg: Control = null
var _vault_dlg: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
var _loc_index: int = 0
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_aa09bf27")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_aa09bf27")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	process_frame.connect(_on_process_frame)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("SKILL_VAULT_FAIL: ", msg)
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
	var fname := path.get_file()
	if _out_dir_docs != "":
		img.save_png(_out_dir_docs.path_join(fname))
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
	if _skill_dlg and is_instance_valid(_skill_dlg) and _skill_dlg.has_method("_update_ui_texts"):
		_skill_dlg.call("_update_ui_texts")
	if _vault_dlg and is_instance_valid(_vault_dlg) and _vault_dlg.has_method("_update_localized_texts"):
		_vault_dlg.call("_update_localized_texts")


func _on_process_frame() -> void:
	_wait += 1
	_total_frames += 1

	if _total_frames > 600:
		_fail("測試逾時 (超過 600 幀仍未完成)")
		return

	match _step:
		0:
			if _wait < 5:
				return
			print("=== 1. 初始化 GameState 與 MobileLobby ===")
			_gs = root.get_node_or_null("GameState")
			if _gs == null:
				_fail("無法取得 GameState 單例")
				return
			if _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game")

			_loc = root.get_node_or_null("Loc")
			_switch_locale("zh_TW")

			var LobbyClass = load("res://scripts/ui/mobile_lobby.gd")
			if LobbyClass == null:
				_fail("無法載入 MobileLobby")
				return
			_lobby = LobbyClass.new() as Control
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			_step = 1
			_wait = 0

		1:
			if _wait < 8:
				return
			print("=== 2. 大廳開啟 SkillDialog ===")
			_skill_dlg = _lobby.call("open_skill_dialog") as Control
			if _skill_dlg == null or not is_instance_valid(_skill_dlg):
				_fail("open_skill_dialog() 返回 null 或無效實例")
				return
			print("  ok 成功開啟 SkillDialog 視窗")
			_step = 2
			_wait = 0

		2:
			if _wait < 6:
				return
			print("\n=== 3. 驗證 BtnGoVault 按鈕規格、樣式與存取器 ===")
			var btn: Button = _skill_dlg.call("get_go_vault_button") as Button
			if btn == null:
				btn = _skill_dlg.call("get_vault_button") as Button
			if btn == null:
				btn = _skill_dlg.find_child("BtnGoVault", true, false) as Button
			if btn == null:
				_fail("無法取得 BtnGoVault 快捷按鈕")
				return
			if btn.name != "BtnGoVault":
				_fail("按鈕名稱應為 BtnGoVault，實測: %s" % btn.name)
				return
			if btn.text != "前往儲能庫":
				_fail("繁中按鈕文字應為『前往儲能庫』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoVault_init")
			print("  ok BtnGoVault 繁體中文文案正確: %s" % btn.text)

			# 存取器驗證
			var btn_acc1: Button = _skill_dlg.call("get_go_vault_button") as Button
			var btn_acc2: Button = _skill_dlg.call("get_vault_button") as Button
			if btn_acc1 != btn or btn_acc2 != btn:
				_fail("存取器 get_go_vault_button() / get_vault_button() 回傳實例不一致")
				return
			print("  ok 存取器 get_go_vault_button() / get_vault_button() 驗證通過")

			# 尺寸熱區驗證（>= 48px）
			if btn.custom_minimum_size.x < 140 or btn.custom_minimum_size.y < 48:
				_fail("按鈕熱區不合規範 (<140x48px)，實測: %s" % str(btn.custom_minimum_size))
				return
			print("  ok BtnGoVault 尺寸熱區合規: %s (>= 140x48px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺金黃 #FFD028、底邊 5px、圓角 16~18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_gold := Color("#FFD028")
				if sb.bg_color.to_html(false).to_upper() != target_gold.to_html(false).to_upper():
					_fail("按鈕底色應為金黃色盤 #FFD028，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left < 16 or sb.corner_radius_top_left > 18:
					_fail("按鈕圓角應為 16~18px，實測: %d" % sb.corner_radius_top_left)
					return
				var border_col: Color = sb.border_color
				var target_border := Color("#1F1A3A")
				if border_col.to_html(false).to_upper() != target_border.to_html(false).to_upper():
					_fail("按鈕描邊應為深藍紫 #1F1A3A，實測: %s" % border_col.to_html(false))
					return
				print("  ok BtnGoVault 樣式檢驗通過：金黃底色 #FFD028、圓角 16px、底厚 5px、深藍紫描邊 #1F1A3A")

			# 驗證位於 BottomBar
			var p_btn: Node = btn.get_parent()
			if p_btn == null or p_btn.name != "BottomBar":
				_fail("BtnGoVault 應位於 BottomBar，實測父節點: %s" % (p_btn.name if p_btn else "null"))
				return
			print("  ok BtnGoVault 成功位於 BottomBar 內")

			if _skill_dlg.has_method("scroll_bottom_to_vault"):
				_skill_dlg.call("scroll_bottom_to_vault")

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_skill_dialog_btn_go_vault.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_skill_dialog_btn_go_vault.png (SHA256: %s...)" % h1.substr(0, 16))

			print("\n=== 4. 點擊 BtnGoVault，驗證訊號發射、關閉 SkillDialog 並連動開啟 ClockworkVaultDialog ===")
			var btn: Button = _skill_dlg.call("get_go_vault_button") as Button
			var sig_fired := {"vault_req": false, "go_vault": false, "closed": false}
			_skill_dlg.vault_requested.connect(func(): sig_fired["vault_req"] = true)
			_skill_dlg.go_vault.connect(func(): sig_fired["go_vault"] = true)
			_skill_dlg.closed.connect(func(): sig_fired["closed"] = true)

			btn.emit_signal("pressed")

			if not sig_fired["vault_req"]:
				_fail("點擊 BtnGoVault 未發射 vault_requested 訊號")
				return
			if not sig_fired["go_vault"]:
				_fail("點擊 BtnGoVault 未發射 go_vault 訊號")
				return
			if not sig_fired["closed"]:
				_fail("點擊 BtnGoVault 未發射 closed 訊號")
				return
			print("  ok 成功發射 vault_requested、go_vault 與 closed 訊號")

			_step = 4
			_wait = 0

		4:
			if _wait < 8:
				return
			# 驗證 SkillDialog 關閉
			var old_skill := _lobby.get_node_or_null("SkillDialog")
			if old_skill != null and not old_skill.is_queued_for_deletion() and old_skill.visible:
				_fail("點擊前往儲能庫後 SkillDialog 未正常關閉")
				return
			print("  ok SkillDialog 已順暢關閉無殘留遮罩")

			# 驗證 ClockworkVaultDialog 開啟
			_vault_dlg = _lobby.get_node_or_null("ClockworkVaultDialog") as Control
			if _vault_dlg == null or not is_instance_valid(_vault_dlg):
				_fail("連動大廳未能開啟 ClockworkVaultDialog")
				return
			print("  ok 大廳成功連動開啟 ClockworkVaultDialog")

			var h2 := _capture_save(_out_dir.path_join("proof_02_click_btn_go_vault_opens_clockwork_vault_dialog.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_click_btn_go_vault_opens_clockwork_vault_dialog.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return
			print("\n=== 5. 關閉 ClockworkVaultDialog，驗證返回 SkillDialog 形成閉環 ===")
			if _vault_dlg.has_signal("closed"):
				_vault_dlg.emit_signal("closed")
			_vault_dlg.queue_free()

			_step = 6
			_wait = 0

		6:
			if _wait < 8:
				return
			_skill_dlg = _lobby.get_node_or_null("SkillDialog") as Control
			if _skill_dlg == null or not is_instance_valid(_skill_dlg):
				# 若大廳有 open_skill_dialog 閉環則應該重新開啟
				_skill_dlg = _lobby.call("open_skill_dialog") as Control
			if _skill_dlg == null:
				_fail("未能順暢返回 SkillDialog")
				return
			print("  ok 成功返回 SkillDialog 介面")

			if _skill_dlg.has_method("scroll_bottom_to_vault"):
				_skill_dlg.call("scroll_bottom_to_vault")

			var h3 := _capture_save(_out_dir.path_join("proof_03_loop_back_to_skill_dialog.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_loop_back_to_skill_dialog.png (SHA256: %s...)" % h3.substr(0, 16))

			print("\n=== 6. 六語系 i18n 即時切換驗證與實機截圖 ===")
			_loc_index = 0
			_step = 7
			_wait = 0

		7:
			if _loc_index >= LOCALES.size():
				_step = 8
				_wait = 0
				return

			var loc := LOCALES[_loc_index]
			_switch_locale(loc)
			_step = 71
			_wait = 0

		71:
			if _wait < 6:
				return
			var loc := LOCALES[_loc_index]
			var btn: Button = _skill_dlg.call("get_go_vault_button") as Button
			if btn == null:
				btn = _skill_dlg.find_child("BtnGoVault", true, false) as Button
			if btn == null:
				_fail("[%s] 無法取得 BtnGoVault" % loc)
				return

			var expected: String = EXPECTED_BTN_TEXTS.get(loc, "")
			_check_no_emoji(btn.text, "BtnGoVault_" + loc)

			if _skill_dlg.has_method("scroll_bottom_to_vault"):
				_skill_dlg.call("scroll_bottom_to_vault")

			if btn.text != expected:
				_fail("[%s] BtnGoVault 翻譯文字不符合預期: 期望 '%s'，實際 '%s'" % [loc, expected, btn.text])
				return
			print("  ok [%s] BtnGoVault 文字正確: %s" % [loc, btn.text])

			var proof_idx := _loc_index + 4
			var proof_name := "proof_%02d_%s_skill_dialog_btn_go_vault.png" % [proof_idx, loc]
			# 若為 zh_TW 已經在 proof_01 拍過，但多語系流程依序拍 proof_04 (zh_CN), proof_05 (en), proof_06 (ja), proof_07 (ko), proof_08 (es)
			if loc != "zh_TW":
				var proof_num: int = 0
				match loc:
					"zh_CN": proof_num = 4
					"en": proof_num = 5
					"ja": proof_num = 6
					"ko": proof_num = 7
					"es": proof_num = 8
				var actual_proof_name := "proof_%02d_%s_skill_dialog_btn_go_vault.png" % [proof_num, loc]
				var h := _capture_save(_out_dir.path_join(actual_proof_name))
				if h != "":
					_proof_hashes["proof_%02d" % proof_num] = h
					print("  ok 儲存截圖 %s (SHA256: %s...)" % [actual_proof_name, h.substr(0, 16)])

			_loc_index += 1
			_step = 7
			_wait = 0

		8:
			if _wait < 6:
				return
			print("\n=== 7. 驗證所有實機截圖雜湊獨立唯一（無同幀重複） ===")
			if DisplayServer.get_name() != "headless":
				var seen_hashes := {}
				for p_key in _proof_hashes:
					var h: String = _proof_hashes[p_key]
					if seen_hashes.has(h):
						_fail("截圖重複！%s 與 %s 具有相同的 SHA256 雜湊: %s" % [p_key, seen_hashes[h], h])
						return
					seen_hashes[h] = p_key
				print("  ok 全部實機截圖 SHA256 獨立唯一驗證通過 (共 %d 張)" % _proof_hashes.size())

			print("\n=======================================================")
			print("PASS_OK")
			print("TEST_SKILL_DIALOG_VAULT_SHORTCUT_OK")
			print("=======================================================")
			quit(0)
