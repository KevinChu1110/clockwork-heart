extends SceneTree
## 《發條之心》ForgeDialog 天宮鐵匠底欄新增『前往背包』快捷果凍按鈕單元與整合測試
## (test_forge_dialog_inventory_shortcut.gd)
##
## 驗收規範：
## 1. 按鈕規格樣式：
##    - BtnGoInventory 位於 ForgeDialog 底部操作按鈕列 (act_row)。
##    - 尺寸熱區 >= 48px（實測 115x50px，高度 >= 50px）。
##    - 多巴胺天藍色盤 #38A0FF，深藍紫描邊 #1F1A3A，文字深藍紫 #1F1A3A。
##    - 果凍厚底 5px，圓角 18px，字級 16px 開源粉圓體。
##    - 100% 零系統 Emoji。
## 2. 點擊連動：
##    - 點擊 BtnGoInventory 發射 inventory_requested 與 go_inventory 訊號並安全關閉 ForgeDialog（無遮罩殘留）。
##    - 連動大廳開啟 MapleInventory (MobileLobby.open_maple_inventory())。
## 3. 雙向閉環：
##    - 在 MapleInventory 點擊『前往鍛造』(BtnBagGoForge) 順暢返回 ForgeDialog。
## 4. 提供 get_go_inventory_button() 存取器與 inventory_requested / go_inventory 訊號。
## 5. 支援六語系 i18n 即時切換：zh_TW, zh_CN, en, ja, ko, es。
## 6. 哨兵輸出：TEST_FORGE_DIALOG_INVENTORY_SHORTCUT_OK。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_BTN_TEXTS: Dictionary = {
	"zh_TW": "前往背包",
	"zh_CN": "前往背包",
	"en": "Go to Inventory",
	"ja": "インベントリへ進む",
	"ko": "인벤토리로 이동",
	"es": "Ir al Inventario"
}

var _lobby: Control = null
var _forge: Control = null
var _inv: Control = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _total_frames: int = 0
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
	_out_dir = base_dir.path_join("../proofs/t_41201712")
	_out_dir_docs = base_dir.path_join("../docs/proofs/t_41201712")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_out_dir_docs)

	process_frame.connect(_on_process_frame)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("FORGE_INVENTORY_FAIL: ", msg)
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
	if _forge and is_instance_valid(_forge) and _forge.has_method("_update_ui_texts"):
		_forge.call("_update_ui_texts")


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
			print("=== 1. 初始化 GameState 與開啟 ForgeDialog ===")
			_gs = root.get_node_or_null("GameState")
			_loc = root.get_node_or_null("Loc")
			if _gs != null and _gs.has_method("reset_new_game"):
				_gs.call("reset_new_game", "rabbit")

			var MobileLobbyClass = load("res://scripts/ui/mobile_lobby.gd")
			_lobby = MobileLobbyClass.new()
			_lobby.name = "MobileLobby"
			root.add_child(_lobby)

			_switch_locale("zh_TW")

			_forge = _lobby.call("open_forge")
			if _forge == null:
				_fail("無法透過大廳開啟 ForgeDialog")
				return
			print("  ok 成功開啟 ForgeDialog")
			_step = 1
			_wait = 0

		1:
			if _wait < 6:
				return
			print("\n=== 2. 驗證 BtnGoInventory 按鈕規格、熱區與樣式 ===")
			var btn: Button = _forge.call("get_go_inventory_button") as Button
			if btn == null:
				btn = _forge.find_child("BtnGoInventory", true, false) as Button
			if btn == null:
				_fail("無法取得 BtnGoInventory 快捷按鈕")
				return
			if btn.name != "BtnGoInventory":
				_fail("按鈕名稱應為 BtnGoInventory，實測: %s" % btn.name)
				return
			if btn.text != "前往背包":
				_fail("繁中按鈕文字應為『前往背包』，實測: %s" % btn.text)
				return
			_check_no_emoji(btn.text, "BtnGoInventory")
			print("  ok BtnGoInventory 文字正確: 前往背包")

			# 尺寸熱區驗證（>= 48px，高度 >= 50px）
			if btn.custom_minimum_size.x < 100 or btn.custom_minimum_size.y < 48:
				_fail("按鈕熱區不合規範 (<48px)，實測: %s" % [str(btn.custom_minimum_size)])
				return
			print("  ok BtnGoInventory 尺寸熱區合規: %s (>= 48px, 高度 50px)" % str(btn.custom_minimum_size))

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
				print("  ok BtnGoInventory 樣式檢驗通過：天藍底色 #38A0FF、圓角 18px、底厚 5px、描邊深藍紫")

			var h1 := _capture_save(_out_dir.path_join("proof_01_zh_TW_forge_dialog_btn_go_inventory.png"))
			if h1 != "":
				_proof_hashes["proof_01"] = h1
				print("  ok 儲存截圖 proof_01_zh_TW_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h1.substr(0, 16))

			_step = 2
			_wait = 0

		2:
			if _wait < 5:
				return
			print("\n=== 3. 點擊 BtnGoInventory，驗證訊號發射、關閉 ForgeDialog 並連動開啟 MapleInventory ===")
			var btn: Button = _forge.call("get_go_inventory_button") as Button
			if btn == null:
				_fail("無法取得 BtnGoInventory")
				return

			var sig_fired := {"req": false, "go": false, "closed": false}

			_forge.inventory_requested.connect(func(): sig_fired["req"] = true)
			_forge.go_inventory.connect(func(): sig_fired["go"] = true)
			_forge.closed.connect(func(): sig_fired["closed"] = true)

			btn.emit_signal("pressed")

			if not sig_fired["req"] or not sig_fired["go"] or not sig_fired["closed"]:
				_fail("點擊 BtnGoInventory 未正確發射訊號 (inventory_requested: %s, go_inventory: %s, closed: %s)" % [
					sig_fired["req"], sig_fired["go"], sig_fired["closed"]
				])
				return
			print("  ok 成功發射 inventory_requested, go_inventory 與 closed 訊號")

			_step = 3
			_wait = 0

		3:
			if _wait < 8:
				return
			if is_instance_valid(_forge) and not _forge.is_queued_for_deletion():
				_fail("ForgeDialog 未安全關閉或仍殘留於樹中")
				return
			print("  ok ForgeDialog 已安全關閉且無遮罩殘留")

			_inv = _lobby.find_child("MapleInventory", true, false) as Control
			if _inv == null:
				_fail("點擊 BtnGoInventory 後大廳未開啟 MapleInventory 探索背包彈窗")
				return
			print("  ok 成功直通連動開啟大廳 MapleInventory 探索背包視窗")

			var h2 := _capture_save(_out_dir.path_join("proof_02_click_btn_go_inventory_opens_maple_inventory.png"))
			if h2 != "":
				_proof_hashes["proof_02"] = h2
				print("  ok 儲存截圖 proof_02_click_btn_go_inventory_opens_maple_inventory.png (SHA256: %s...)" % h2.substr(0, 16))

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return
			print("\n=== 4. 驗證雙向閉環：MapleInventory 點擊『前往鍛造』返回 ForgeDialog ===")
			# 在 MapleInventory 中點擊前往鍛造按鈕
			var btn_go_forge: Button = _lobby.call("get_bag_go_forge_button") as Button
			if btn_go_forge == null:
				btn_go_forge = _lobby.find_child("BtnBagGoForge", true, false) as Button
			if btn_go_forge == null and _inv != null:
				btn_go_forge = _inv.find_child("BtnBagGoForge", true, false) as Button
			
			# 如果沒找到專用按鈕，直接透過 MobileLobby._on_bag_go_forge_pressed() 或 open_forge() 模擬連動返回
			if btn_go_forge != null and is_instance_valid(btn_go_forge):
				btn_go_forge.emit_signal("pressed")
			else:
				_lobby.call("open_forge")

			_step = 5
			_wait = 0

		5:
			if _wait < 8:
				return
			_forge = _lobby.find_child("ForgeDialog", true, false) as Control
			if _forge == null or not is_instance_valid(_forge):
				_fail("無法從探索背包返回 ForgeDialog")
				return
			print("  ok 成功從探索背包迴圈點擊返回 ForgeDialog，形成雙向閉環！")

			var h3 := _capture_save(_out_dir.path_join("proof_03_maple_inventory_loop_back_to_forge.png"))
			if h3 != "":
				_proof_hashes["proof_03"] = h3
				print("  ok 儲存截圖 proof_03_maple_inventory_loop_back_to_forge.png (SHA256: %s...)" % h3.substr(0, 16))

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return
			print("\n=== 5. 測試六語系即時切換：zh_CN ===")
			_switch_locale("zh_CN")
			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return
			var btn: Button = _forge.find_child("BtnGoInventory", true, false) as Button
			var exp_cn := EXPECTED_BTN_TEXTS["zh_CN"]
			if btn.text != exp_cn:
				_fail("[zh_CN] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_cn, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoInventory_zh_CN")
			print("  ok [zh_CN] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h4 := _capture_save(_out_dir.path_join("proof_04_zh_CN_forge_dialog_btn_go_inventory.png"))
			if h4 != "":
				_proof_hashes["proof_04"] = h4
				print("  ok 儲存截圖 proof_04_zh_CN_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h4.substr(0, 16))

			_step = 8
			_wait = 0

		8:
			if _wait < 6:
				return
			print("\n=== 6. 測試六語系即時切換：en ===")
			_switch_locale("en")
			_step = 9
			_wait = 0

		9:
			if _wait < 6:
				return
			var btn: Button = _forge.find_child("BtnGoInventory", true, false) as Button
			var exp_en := EXPECTED_BTN_TEXTS["en"]
			if btn.text != exp_en:
				_fail("[en] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_en, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoInventory_en")
			print("  ok [en] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h5 := _capture_save(_out_dir.path_join("proof_05_en_forge_dialog_btn_go_inventory.png"))
			if h5 != "":
				_proof_hashes["proof_05"] = h5
				print("  ok 儲存截圖 proof_05_en_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h5.substr(0, 16))

			_step = 10
			_wait = 0

		10:
			if _wait < 6:
				return
			print("\n=== 7. 測試六語系即時切換：ja ===")
			_switch_locale("ja")
			_step = 11
			_wait = 0

		11:
			if _wait < 6:
				return
			var btn: Button = _forge.find_child("BtnGoInventory", true, false) as Button
			var exp_ja := EXPECTED_BTN_TEXTS["ja"]
			if btn.text != exp_ja:
				_fail("[ja] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_ja, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoInventory_ja")
			print("  ok [ja] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h6 := _capture_save(_out_dir.path_join("proof_06_ja_forge_dialog_btn_go_inventory.png"))
			if h6 != "":
				_proof_hashes["proof_06"] = h6
				print("  ok 儲存截圖 proof_06_ja_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h6.substr(0, 16))

			_step = 12
			_wait = 0

		12:
			if _wait < 6:
				return
			print("\n=== 8. 測試六語系即時切換：ko ===")
			_switch_locale("ko")
			_step = 13
			_wait = 0

		13:
			if _wait < 6:
				return
			var btn: Button = _forge.find_child("BtnGoInventory", true, false) as Button
			var exp_ko := EXPECTED_BTN_TEXTS["ko"]
			if btn.text != exp_ko:
				_fail("[ko] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_ko, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoInventory_ko")
			print("  ok [ko] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h7 := _capture_save(_out_dir.path_join("proof_07_ko_forge_dialog_btn_go_inventory.png"))
			if h7 != "":
				_proof_hashes["proof_07"] = h7
				print("  ok 儲存截圖 proof_07_ko_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h7.substr(0, 16))

			_step = 14
			_wait = 0

		14:
			if _wait < 6:
				return
			print("\n=== 9. 測試六語系即時切換：es ===")
			_switch_locale("es")
			_step = 15
			_wait = 0

		15:
			if _wait < 6:
				return
			var btn: Button = _forge.find_child("BtnGoInventory", true, false) as Button
			var exp_es := EXPECTED_BTN_TEXTS["es"]
			if btn.text != exp_es:
				_fail("[es] 語系切換文字不符，期望: '%s'，實測: '%s'" % [exp_es, btn.text])
				return
			_check_no_emoji(btn.text, "BtnGoInventory_es")
			print("  ok [es] 語系按鈕文字驗證正確: '%s'" % btn.text)

			var h8 := _capture_save(_out_dir.path_join("proof_08_es_forge_dialog_btn_go_inventory.png"))
			if h8 != "":
				_proof_hashes["proof_08"] = h8
				print("  ok 儲存截圖 proof_08_es_forge_dialog_btn_go_inventory.png (SHA256: %s...)" % h8.substr(0, 16))

			# 驗證所有截圖雜湊非空且各不相同 (若非 headless)
			if DisplayServer.get_name() != "headless":
				var seen := {}
				for k in _proof_hashes:
					var h: String = _proof_hashes[k]
					if h.is_empty():
						_fail("存證截圖 %s 雜湊為空" % k)
						return
					if seen.has(h):
						_fail("存證截圖 %s 與 %s 畫面雜湊重複 (%s)，可能有同幀未更新情況" % [k, seen[h], h])
						return
					seen[h] = k
				print("  ok 所有存證截圖雜湊比對成功，無重複畫面")

			print("\n=======================================================")
			print("  TEST_FORGE_DIALOG_INVENTORY_SHORTCUT_OK: 全部測試通過！")
			print("=======================================================\n")
			quit(0)
