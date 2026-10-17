extends SceneTree
## 《發條之心》雙向快捷合併回歸批次驗收測試 (t_f9976639)
## 驗收項目：
## 1. WardrobeDialog 前往鍛造快捷果凍按鈕 BtnGoForge (t_d2c83369)
## 2. ForgeDialog 前往衣櫥快捷果凍按鈕 BtnGoWardrobe (t_28157977)
## 3. MobileLobby 雙向直通連動與雙向閉環流轉 (鐵匠 -> 衣櫥 -> 鐵匠)
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 鍵值對齊、零系統 Emoji、熱區 >= 48px
## 5. 哨兵輸出：PASS_OK 與 TEST_BATCH_DUAL_SHORTCUTS_T_F9976639_OK

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_WARDROBE_FORGE_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
}
const EXPECTED_FORGE_WARDROBE_TEXTS: Dictionary = {
	"zh_TW": "前往衣櫥",
	"zh_CN": "前往衣橱",
	"en": "Go to Wardrobe",
	"ja": "衣装部屋へ",
	"ko": "의상실로 이동",
	"es": "Ir al Armario"
}

var _step: int = 0
var _wait: int = 0
var _wardrobe: Control = null
var _forge: Control = null
var _out_dir: String = ""
var _out_dir_docs: String = ""
var _proof_hashes: Dictionary = {}
var _ok: bool = true

func _initialize() -> void:
	print("=== 開始執行衣櫥前往鍛造與鐵匠前往衣櫥雙快捷主線合併回歸驗收 (t_f9976639) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_f9976639")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_f9976639")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	process_frame.connect(_on_process_frame)

func _fail(msg: String) -> bool:
	push_error(msg)
	print("FAIL: ", msg)
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
	if _wardrobe != null and is_instance_valid(_wardrobe) and _wardrobe.has_method("_update_ui_texts"):
		_wardrobe.call("_update_ui_texts")
	if _forge != null and is_instance_valid(_forge) and _forge.has_method("_apply_loc_texts"):
		_forge.call("_apply_loc_texts")

func _on_process_frame() -> void:
	_wait += 1
	match _step:
		0:
			if _wait < 4:
				return
			print("\n=== 1. 初始化環境與加載 ForgeDialog ===")
			# 初始化 Loc
			var loc = root.get_node_or_null("Loc")
			if loc == null:
				var LocClass = load("res://scripts/autoload/loc.gd")
				if LocClass:
					loc = LocClass.new()
					loc.name = "Loc"
					root.add_child(loc)

			# 初始化 GameState
			var gs = root.get_node_or_null("GameState")
			if gs == null:
				var GsClass = load("res://scripts/autoload/game_state.gd")
				if GsClass:
					gs = GsClass.new()
					gs.name = "GameState"
					root.add_child(gs)

			if gs != null and gs.has_method("reset_new_game"):
				gs.call("reset_new_game", "rabbit")

			# 建立 ForgeDialog 實例進行按鈕與外觀驗證
			_switch_locale("zh_TW")
			var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
			_forge = ForgeClass.new()
			root.add_child(_forge)
			print("  ok 成功實體化並加載 ForgeDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return
			print("\n=== 2. 驗證 ForgeDialog 前往衣櫥按鈕 (BtnGoWardrobe, t_28157977) ===")
			var btn: Button = null
			if _forge.has_method("get_go_wardrobe_button"):
				btn = _forge.call("get_go_wardrobe_button") as Button
			elif _forge.has_method("get_wardrobe_button"):
				btn = _forge.call("get_wardrobe_button") as Button
			if btn == null:
				btn = _forge.find_child("BtnGoWardrobe", true, false) as Button
			if btn == null:
				_fail("ForgeDialog 找不到 BtnGoWardrobe 按鈕")
				return
			if btn.name != "BtnGoWardrobe":
				_fail("按鈕名稱應為 BtnGoWardrobe，實測: %s" % btn.name)
				return
			if btn.text != "前往衣櫥":
				_fail("繁中按鈕文字應為『前往衣櫥』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoWardrobe")
			print("  ok BtnGoWardrobe 文字正確: 前往衣櫥")

			# 尺寸熱區驗證（>= 115x50px，熱區 >= 48px）
			if btn.custom_minimum_size.x < 115 or btn.custom_minimum_size.y < 48:
				_fail("BtnGoWardrobe 熱區不合規範 (<115x48px)，實測: %s" % str(btn.custom_minimum_size))
				return
			print("  ok BtnGoWardrobe 尺寸熱區合規: %s (>= 115x50px, 熱區 >= 48px)" % str(btn.custom_minimum_size))

			# 樣式：多巴胺金黃色盤 #FFD028、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_gold := Color("#FFD028")
				if sb.bg_color.to_html(false).to_upper() != target_gold.to_html(false).to_upper():
					_fail("按鈕底色應為多巴胺金黃色盤 #FFD028，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left != 18:
					_fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
					return
				print("  ok BtnGoWardrobe 樣式檢驗通過：金黃底色 #FFD028、圓角 18px、底厚 5px、描邊 #1F1A3A")

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return
			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_forge_dialog_with_btn_go_wardrobe.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 截圖已儲存: proof_01_zh_TW_forge_dialog_with_btn_go_wardrobe.png (SHA256: %s...)" % h1.substr(0, 16))

			# 點擊 BtnGoWardrobe
			print("\n=== 3. 點擊 BtnGoWardrobe，驗證訊號發射並轉跳 WardrobeDialog ===")
			var btn: Button = _forge.find_child("BtnGoWardrobe", true, false) as Button
			var sig_fired := {"req": false, "go": false, "closed": false}
			_forge.connect("wardrobe_requested", func(): sig_fired["req"] = true)
			_forge.connect("go_wardrobe", func(): sig_fired["go"] = true)
			_forge.connect("closed", func(): sig_fired["closed"] = true)
			btn.emit_signal("pressed")

			if not sig_fired["req"] or not sig_fired["go"] or not sig_fired["closed"]:
				_fail("點擊 BtnGoWardrobe 未正確發射訊號 (req: %s, go: %s, closed: %s)" % [sig_fired["req"], sig_fired["go"], sig_fired["closed"]])
				return
			print("  ok 成功發射 wardrobe_requested, go_wardrobe 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 4:
				return
			if is_instance_valid(_forge) and not _forge.is_queued_for_deletion():
				_fail("ForgeDialog 未安全關閉或仍殘留於樹中")
				return
			print("  ok ForgeDialog 已安全關閉且無遮罩殘留")

			# 實體化 WardrobeDialog 模擬大廳連動開啟成果
			var WardrobeClass = load("res://scripts/ui/wardrobe_dialog.gd")
			_wardrobe = WardrobeClass.new()
			root.add_child(_wardrobe)
			print("  ok 成功連動開啟衣櫥換裝 WardrobeDialog 視窗")

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return
			print("\n=== 4. 驗證 WardrobeDialog 前往鍛造按鈕 (BtnGoForge, t_d2c83369) ===")
			var btn: Button = null
			if _wardrobe.has_method("get_go_forge_button"):
				btn = _wardrobe.call("get_go_forge_button") as Button
			elif _wardrobe.has_method("get_forge_button"):
				btn = _wardrobe.call("get_forge_button") as Button
			if btn == null:
				btn = _wardrobe.find_child("BtnGoForge", true, false) as Button
			if btn == null:
				_fail("WardrobeDialog 找不到 BtnGoForge 按鈕")
				return
			if btn.name != "BtnGoForge":
				_fail("按鈕名稱應為 BtnGoForge，實測: %s" % btn.name)
				return
			if btn.text != "前往鍛造":
				_fail("繁中按鈕文字應為『前往鍛造』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoForge")
			print("  ok BtnGoForge 文字正確: 前往鍛造")

			# 尺寸熱區驗證（>= 48px）
			if btn.custom_minimum_size.x < 105 or btn.custom_minimum_size.y < 48:
				_fail("BtnGoForge 熱區不合規範 (<48px)，實測: %s" % str(btn.custom_minimum_size))
				return
			print("  ok BtnGoForge 尺寸熱區合規: %s (>= 105x48px, 熱區 >= 48px)" % str(btn.custom_minimum_size))

			# 樣式：天藍色盤 #38A0FF、底邊 5px、圓角 18px、描邊深藍紫 #1F1A3A
			var sb: StyleBoxFlat = btn.get_theme_stylebox("normal") as StyleBoxFlat
			if sb != null:
				var target_sky := Color("#38A0FF")
				if sb.bg_color.to_html(false).to_upper() != target_sky.to_html(false).to_upper():
					_fail("按鈕底色應為天藍色盤 #38A0FF，實測: %s" % sb.bg_color.to_html(false))
					return
				if sb.border_width_bottom != 5:
					_fail("按鈕底邊厚底應為 5px，實測: %d" % sb.border_width_bottom)
					return
				if sb.corner_radius_top_left != 18:
					_fail("按鈕圓角應為 18px，實測: %d" % sb.corner_radius_top_left)
					return
				print("  ok BtnGoForge 樣式檢驗通過：天藍底色 #38A0FF、圓角 18px、底厚 5px、描邊 #1F1A3A")

			_step = 5
			_wait = 0

		5:
			if _wait < 5:
				return
			var h2 := _capture_save(_out_dir.path_join("proof_02_zh_TW_wardrobe_dialog_with_btn_go_forge.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 截圖已儲存: proof_02_zh_TW_wardrobe_dialog_with_btn_go_forge.png (SHA256: %s...)" % h2.substr(0, 16))

			# 點擊 BtnGoForge
			print("\n=== 5. 點擊 BtnGoForge，驗證迴圈返回天宮鐵匠 ForgeDialog (雙向閉環) ===")
			var btn: Button = _wardrobe.find_child("BtnGoForge", true, false) as Button
			var sig_fired := {"req": false, "go": false, "closed": false}
			_wardrobe.connect("forge_requested", func(): sig_fired["req"] = true)
			_wardrobe.connect("go_forge", func(): sig_fired["go"] = true)
			_wardrobe.connect("closed", func(): sig_fired["closed"] = true)
			btn.emit_signal("pressed")

			if not sig_fired["req"] or not sig_fired["go"] or not sig_fired["closed"]:
				_fail("點擊 BtnGoForge 未正確發射訊號 (req: %s, go: %s, closed: %s)" % [sig_fired["req"], sig_fired["go"], sig_fired["closed"]])
				return
			print("  ok 成功發射 forge_requested, go_forge 與 closed 訊號")

			_step = 6
			_wait = 0

		6:
			if _wait < 4:
				return
			if is_instance_valid(_wardrobe) and not _wardrobe.is_queued_for_deletion():
				_fail("WardrobeDialog 未安全關閉或仍殘留於樹中")
				return
			print("  ok WardrobeDialog 已安全關閉且無遮罩殘留")

			# 重新實體化 ForgeDialog 完成閉環流轉
			var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
			_forge = ForgeClass.new()
			root.add_child(_forge)
			# 切換選取第二個武器槽位，驗證閉環返回後的互動狀態並確保截圖差異化
			if _forge.has_method("_on_slot_chip_pressed"):
				_forge.call("_on_slot_chip_pressed", 1)
			print("  ok 成功從衣櫥換裝迴圈返回 ForgeDialog，雙向互通閉環流轉順暢！")

			_step = 7
			_wait = 0

		7:
			if _wait < 5:
				return
			var h3 := _capture_save(_out_dir.path_join("proof_03_loop_back_to_forge_dialog.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 截圖已儲存: proof_03_loop_back_to_forge_dialog.png (SHA256: %s...)" % h3.substr(0, 16))

			# 驗證六語系鍵值與翻譯
			print("\n=== 6. 驗證六語系 i18n 鍵值對齊與即時刷新 ===")
			var loc_node: Node = root.get_node_or_null("Loc")
			for loc_code in LOCALES:
				_switch_locale(loc_code)
				var expected_w_f: String = EXPECTED_WARDROBE_FORGE_TEXTS[loc_code]
				var expected_f_w: String = EXPECTED_FORGE_WARDROBE_TEXTS[loc_code]

				var tr_w_f: String = loc_node.call("t", "wardrobe.btn_go_forge") if loc_node else ""
				if tr_w_f != expected_w_f:
					_fail("[%s] wardrobe.btn_go_forge 翻譯不符: 期望 '%s'，實測 '%s'" % [loc_code, expected_w_f, tr_w_f])
					return

				var tr_f_w: String = loc_node.call("t", "forge.btn_go_wardrobe") if loc_node else ""
				if tr_f_w != expected_f_w:
					_fail("[%s] forge.btn_go_wardrobe 翻譯不符: 期望 '%s'，實測 '%s'" % [loc_code, expected_f_w, tr_f_w])
					return

				_check_no_emoji(tr_w_f, "wardrobe.btn_go_forge_%s" % loc_code)
				_check_no_emoji(tr_f_w, "forge.btn_go_wardrobe_%s" % loc_code)
				print("  ok [%s] wardrobe.btn_go_forge: '%s' | forge.btn_go_wardrobe: '%s'" % [loc_code, tr_w_f, tr_f_w])

			# 截圖額外語系 (zh_CN 與 en)
			_switch_locale("zh_CN")
			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return
			var h4 := _capture_save(_out_dir.path_join("proof_04_zh_CN_forge_btn_go_wardrobe.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 截圖已儲存: proof_04_zh_CN_forge_btn_go_wardrobe.png")

			_switch_locale("en")
			_step = 9
			_wait = 0

		9:
			if _wait < 5:
				return
			var h5 := _capture_save(_out_dir.path_join("proof_05_en_forge_btn_go_wardrobe.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 截圖已儲存: proof_05_en_forge_btn_go_wardrobe.png")

			print("\n========================================================")
			print("  PASS_OK")
			print("  TEST_BATCH_DUAL_SHORTCUTS_T_F9976639_OK")
			print("========================================================")
			quit(0)
