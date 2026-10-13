extends SceneTree
## 無頭與實機單元測試：背包Tab寶石素材與裝備詳情新增『前往工坊』快捷按鈕連動 GemWorkshopDialog (t_b3545e1b)
##
## 覆蓋驗收項目：
## 1. 背包右側物品詳情面板中存在 BtnBagGoWorkshop 前往工坊快捷按鈕。
## 2. 人體工學與多巴胺視覺規範：custom_minimum_size.y >= 52px、果凍厚底 5px、圓角 18px、零 Emoji、多巴胺薄荷綠 (#4ED86A) 底色與深藍紫描邊 (#1F1A3A)。
## 3. 按鈕顯示條件嚴格分流：
##    - 未選中物品時：按鈕隱藏 (visible == false)。
##    - 選中消耗品 (kind == "consumable")：按鈕隱藏。
##    - 選中材料 (kind == "material")：按鈕隱藏。
##    - 選中重要道具 (kind == "key")：按鈕隱藏。
##    - 選中星屑素材 (id 含 dust / kind == gem)：按鈕顯示 (visible == true)。
##    - 選中寶石素材 (id 含 gem)：按鈕顯示 (visible == true)。
##    - 選中裝備/武器 (kind == "weapon" 或 "equipment")：按鈕顯示 (visible == true)。
## 4. 點擊跳轉事件、自動關閉背包與開啟 GemWorkshopDialog：
##    - 點擊 BtnBagGoWorkshop 後，自動關閉/隱藏背包分頁 (_bag_layer.visible == false，切換至大廳 Tab.VILLAGE)。
##    - 彈出手藝工坊寶石彈窗 (GemWorkshopDialog)。
## 5. 分頁自動連動：
##    - 選中星屑/寶石素材點擊時：自動切換至手藝工坊「熔煉分頁」 (Tab.SMELT = 0)。
##    - 選中武器/裝備點擊時：自動切換至手藝工坊「寶石櫃鑲嵌分頁」 (Tab.CASE_INSPECT = 1)。
## 6. 六語系字典支援與 0-QA 規範：
##    - 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與即時刷新。
##    - 歐美與韓日非中文語系無繁體中文殘留，零系統 Emoji。
## 7. 實機渲染存證：在非 headless (xvfb) 下擷取真實 OpenGL3 截圖存證並驗證 SHA256 獨立不重複。

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往工坊",
	"zh_CN": "前往工坊",
	"en": "Go to Workshop",
	"ja": "工房へ進む",
	"ko": "공방으로 이동",
	"es": "Ir al Taller"
}

var _ok := true
var _frame := 0
var _step := 0
var _wait := 0
var _lobby: Control = null
var _gs: Node = null
var _eq: Node = null
var _inv: Node = null
var _loc: Node = null
var _gem_sys: Node = null
var _out_dir: String = ""
var _proof_hashes: Array[String] = []


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			return true
	return false


func _initialize() -> void:
	print("=== 開始執行背包 Tab 前往工坊快捷按鈕單元測試 (t_b3545e1b) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var env_dir := OS.get_environment("PROOF_DIR")
	if env_dir != "":
		_out_dir = env_dir
	else:
		_out_dir = ProjectSettings.globalize_path("res://../proofs/t_b3545e1b")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	change_scene_to_file("res://scenes/main.tscn")


func _setup_lobby_and_data() -> void:
	_gs = root.get_node_or_null("GameState")
	_loc = root.get_node_or_null("Loc")
	_inv = root.get_node_or_null("InventorySystem")
	_eq = root.get_node_or_null("EquipmentSystem")
	_gem_sys = root.get_node_or_null("GemSystem")

	if _gs == null or _loc == null or _inv == null or _eq == null or _gem_sys == null:
		_fail("Autoload 節點初始化失敗 (main.tscn 載入不完全)")
		quit(1)
		return

	_gs.call("reset_new_game", "rabbit")
	_loc.call("set_locale", "zh_TW")

	if _inv.has_method("add_item"):
		_inv.call("add_item", "hp_s", 5)
		_inv.call("add_item", "iron_scrap", 10)
		_inv.call("add_item", "dust_crumb", 3)
		_inv.call("add_item", "key_rusty", 1)
		_inv.call("add_item", "rusty_blade", 1)

	var MobileLobbyScript = load("res://scripts/ui/mobile_lobby.gd")
	if MobileLobbyScript == null:
		_fail("無法載入 mobile_lobby.gd")
		quit(1)
		return

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ✓ MobileLobby 初始化成功")


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 15:
		return false

	if _frame == 15:
		_setup_lobby_and_data()
		return false

	match _step:
		0:
			_test_button_existence_and_style()
			_step = 1
		1:
			_test_visibility_rules()
			_step = 2
		2:
			_test_click_transition_and_tab_sync()
			_step = 3
		3:
			_test_six_locales()
			_step = 4
		4:
			if DisplayServer.get_name() != "headless":
				print("\n--- 5. 擷取真實 OpenGL3 實機截圖存證並驗證 SHA256 獨立 ---")
				_wait = 0
				_step = 5
			else:
				print("\n--- 5. 無頭模式 (headless)，略過實機截圖 ---")
				_step = 10
		5:
			# 截圖 1: 背包選中星屑素材時顯示 BtnBagGoWorkshop (zh_TW)
			_lobby.call("_switch_tab", 4) # Tab.BAG
			_lobby.set("_selected_bag_item", "dust_crumb")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_01_bag_dust_selected_zh_TW.png")
			_wait = 0
			_step = 6
		6:
			# 截圖 2: 點擊前往工坊直達 GemWorkshopDialog 熔煉分頁
			var btn := _lobby.call("get_bag_go_workshop_button") as Button
			if btn != null:
				btn.pressed.emit()
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_02_workshop_smelt_opened.png")
			var dlg = _lobby.get_node_or_null("GemWorkshopDialog")
			if dlg:
				dlg.queue_free()
			_wait = 0
			_step = 7
		7:
			# 截圖 3: 背包選中武器時顯示 BtnBagGoWorkshop (zh_TW)
			_lobby.call("_switch_tab", 4) # Tab.BAG
			_lobby.set("_selected_bag_item", "rusty_blade")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_03_bag_weapon_selected_zh_TW.png")
			_wait = 0
			_step = 8
		8:
			# 截圖 4: 點擊前往工坊直達 GemWorkshopDialog 寶石櫃分頁
			var btn2 := _lobby.call("get_bag_go_workshop_button") as Button
			if btn2 != null:
				btn2.pressed.emit()
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_04_workshop_case_opened.png")
			var dlg2 = _lobby.get_node_or_null("GemWorkshopDialog")
			if dlg2:
				dlg2.queue_free()
			_wait = 0
			_step = 9
		9:
			# 截圖 5: 背包選中普通消耗品時 BtnBagGoWorkshop 隱藏
			_lobby.call("_switch_tab", 4) # Tab.BAG
			_lobby.set("_selected_bag_item", "hp_s")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_05_bag_consumable_hidden.png")
			_step = 10
		10:
			_finish()
			return true

	return false


func _test_button_existence_and_style() -> void:
	print("\n--- 1. 檢驗 BtnBagGoWorkshop 按鈕存在性與多巴胺視覺規範 ---")
	var btn: Button = null
	if _lobby.has_method("get_bag_go_workshop_button"):
		btn = _lobby.call("get_bag_go_workshop_button") as Button
	if btn == null:
		btn = _lobby.find_child("BtnBagGoWorkshop", true, false) as Button
	if btn == null:
		_fail("MobileLobby 內找不到 BtnBagGoWorkshop 按鈕節點")
		return
	print("  ✓ 找到 BtnBagGoWorkshop 按鈕節點")

	if btn.name != "BtnBagGoWorkshop":
		_fail("按鈕名稱應為 'BtnBagGoWorkshop'，實際為: %s" % btn.name)
	else:
		print("  ✓ 按鈕名稱符合規範: BtnBagGoWorkshop")

	if btn.custom_minimum_size.y < 52.0:
		_fail("BtnBagGoWorkshop 高度未達手遊規範 (期望 >= 52px，實際 %.1fpx)" % btn.custom_minimum_size.y)
	else:
		print("  ✓ 按鈕高度符合人體工學規範 (%.1fpx >= 52px)" % btn.custom_minimum_size.y)

	var sb_normal = btn.get_theme_stylebox("normal")
	if sb_normal is StyleBoxFlat:
		var bg_hex = sb_normal.bg_color.to_html(false).to_upper()
		if bg_hex != "4ED86A":
			_fail("BtnBagGoWorkshop 底色非多巴胺薄荷綠 #4ED86A (實際 #%s)" % bg_hex)
		else:
			print("  ✓ 按鈕底色符合多巴胺薄荷綠 (#4ED86A)")

		if sb_normal.border_width_bottom < 5:
			_fail("BtnBagGoWorkshop 果凍厚底未達 5px (實際 %dpx)" % sb_normal.border_width_bottom)
		else:
			print("  ✓ 按鈕果凍厚底達標: %dpx" % sb_normal.border_width_bottom)

		if sb_normal.corner_radius_top_left != 18:
			_fail("BtnBagGoWorkshop 圓角非 18px (實際 %dpx)" % sb_normal.corner_radius_top_left)
		else:
			print("  ✓ 按鈕圓角規範達標: %dpx" % sb_normal.corner_radius_top_left)
	else:
		_fail("BtnBagGoWorkshop normal stylebox 未設定或型別錯誤")

	if btn.text != "前往工坊":
		_fail("繁體中文預設文字不符預期！期望 '前往工坊'，實際: '%s'" % btn.text)
	else:
		print("  ✓ 繁中文字正確: '前往工坊'")

	if _has_emoji(btn.text):
		_fail("BtnBagGoWorkshop 文字包含系統 Emoji: %s" % btn.text)
	else:
		print("  ✓ 零系統 Emoji 規範通過")


func _test_visibility_rules() -> void:
	print("\n--- 2. 檢驗按鈕顯示條件分流 (非裝備素材隱藏 / 寶石星屑裝備顯示) ---")
	_lobby.call("_switch_tab", 4) # Tab.BAG
	var btn := _lobby.call("get_bag_go_workshop_button") as Button
	if btn == null:
		_fail("找不到 BtnBagGoWorkshop")
		return

	# 1. 未選中任何物品
	_lobby.set("_selected_bag_item", "")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("未選中物品時 BtnBagGoWorkshop 應為隱藏 (visible == false)")
	else:
		print("  ✓ 未選中物品時按鈕隱藏 (PASS)")

	# 2. 選中普通消耗品 (hp_s)
	_lobby.set("_selected_bag_item", "hp_s")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中普通消耗品 (hp_s) 時 BtnBagGoWorkshop 應隱藏，實際為可見")
	else:
		print("  ✓ 選中消耗品時按鈕隱藏 (PASS)")

	# 3. 選中普通材料 (iron_scrap)
	_lobby.set("_selected_bag_item", "iron_scrap")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中普通材料 (iron_scrap) 時 BtnBagGoWorkshop 應隱藏，實際為可見")
	else:
		print("  ✓ 選中普通材料時按鈕隱藏 (PASS)")

	# 4. 選中重要道具 (key_rusty)
	_lobby.set("_selected_bag_item", "key_rusty")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中重要道具 (key_rusty) 時 BtnBagGoWorkshop 應隱藏，實際為可見")
	else:
		print("  ✓ 選中重要道具時按鈕隱藏 (PASS)")

	# 5. 選中星屑素材 (dust_crumb) -> 應顯示
	_lobby.set("_selected_bag_item", "dust_crumb")
	_lobby.call("_refresh_bag_tab", false)
	if not btn.visible:
		_fail("選中星屑素材 (dust_crumb) 時 BtnBagGoWorkshop 應顯示 (visible == true)")
	else:
		print("  ✓ 選中星屑素材 (dust_crumb) 時按鈕正確顯示 (PASS)")

	# 6. 選中自訂寶石素材 (gem_red) -> 應顯示
	_lobby.set("_selected_bag_item", "gem_red")
	_lobby.call("_refresh_bag_tab", false)
	if not btn.visible:
		_fail("選中寶石素材 (gem_red) 時 BtnBagGoWorkshop 應顯示 (visible == true)")
	else:
		print("  ✓ 選中寶石素材 (gem_red) 時按鈕正確顯示 (PASS)")

	# 7. 選中武器裝備 (rusty_blade) -> 應顯示
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)
	if not btn.visible:
		_fail("選中武器 (rusty_blade) 時 BtnBagGoWorkshop 應顯示 (visible == true)")
	else:
		print("  ✓ 選中武器 (rusty_blade) 時按鈕正確顯示 (PASS)")

	# 8. 選中裝備系統生成的自訂裝備 -> 應顯示
	var eq_uid := ""
	if _eq.has_method("grant_item"):
		var inst: Dictionary = _eq.call("grant_item", "wpn_dawn_blade", 1, 1)
		eq_uid = str(inst.get("uid", ""))
	if not eq_uid.is_empty():
		_lobby.set("_selected_bag_item", eq_uid)
		_lobby.call("_refresh_bag_tab", false)
		if not btn.visible:
			_fail("選中裝備系統實例時 BtnBagGoWorkshop 應顯示")
		else:
			print("  ✓ 選中裝備庫實例裝備時按鈕正確顯示 (PASS)")


func _test_click_transition_and_tab_sync() -> void:
	print("\n--- 3. 檢驗點擊跳轉事件、收合背包與開啟手藝工坊分頁連動 ---")
	var btn := _lobby.call("get_bag_go_workshop_button") as Button
	if btn == null:
		_fail("找不到 BtnBagGoWorkshop")
		return

	# Case A: 選中星屑素材 (dust_crumb) -> 應進入熔煉分頁 (Tab.SMELT = 0)
	_lobby.call("_switch_tab", 4) # Tab.BAG
	_lobby.set("_selected_bag_item", "dust_crumb")
	_lobby.call("_refresh_bag_tab", false)

	btn.pressed.emit()

	var bag_layer = _lobby.get("_bag_layer") as Control
	if bag_layer != null and bag_layer.visible:
		_fail("點擊前往工坊後背包圖層未關閉 (bag_layer.visible 仍為 true)")
	else:
		print("  ✓ 點擊後背包面板平滑收合/隱藏 (PASS)")

	var dlg = _lobby.get_node_or_null("GemWorkshopDialog")
	if dlg == null:
		_fail("點擊後未成功彈出 GemWorkshopDialog")
	else:
		print("  ✓ 成功開啟 GemWorkshopDialog")
		if dlg.has_method("get_current_tab"):
			var cur_tab: int = int(dlg.call("get_current_tab"))
			if cur_tab != 0: # 0: SMELT
				_fail("選中星屑素材時應切換至熔煉分頁 (Tab.SMELT = 0)，實際為: %d" % cur_tab)
			else:
				print("  ✓ 選中星屑素材時，手藝工坊精確連動至「熔煉分頁」 (PASS)")
		dlg.queue_free()

	# Case B: 選中武器裝備 (rusty_blade) -> 應進入寶石櫃鑲嵌分頁 (Tab.CASE_INSPECT = 1)
	_lobby.call("_switch_tab", 4) # Tab.BAG
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)

	btn.pressed.emit()

	var dlg2 = _lobby.get_node_or_null("GemWorkshopDialog")
	if dlg2 == null:
		_fail("選中裝備點擊後未彈出 GemWorkshopDialog")
	else:
		print("  ✓ 成功開啟 GemWorkshopDialog (裝備測試)")
		if dlg2.has_method("get_current_tab"):
			var cur_tab2: int = int(dlg2.call("get_current_tab"))
			if cur_tab2 != 1: # 1: CASE_INSPECT
				_fail("選中裝備時應切換至寶石櫃分頁 (Tab.CASE_INSPECT = 1)，實際為: %d" % cur_tab2)
			else:
				print("  ✓ 選中裝備時，手藝工坊精確連動至「寶石櫃鑲嵌分頁」 (PASS)")
		dlg2.queue_free()


func _test_six_locales() -> void:
	print("\n--- 4. 檢驗六語系字典完整支援與 0-QA 規範 ---")
	var btn := _lobby.call("get_bag_go_workshop_button") as Button
	if btn == null:
		_fail("找不到 BtnBagGoWorkshop")
		return

	# 選中裝備以維持按鈕可見
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)

	for code in LOCALES:
		_loc.call("set_locale", code)
		_lobby.call("_on_locale_changed", code)

		var expected: String = EXPECTED_TEXTS.get(code, "")
		var actual: String = btn.text
		if actual != expected:
			_fail("[%s] BtnBagGoWorkshop 文字不符預期！期望 '%s'，實際 '%s'" % [code, expected, actual])
		else:
			print("  ✓ [%s] BtnBagGoWorkshop 文字正確: '%s'" % [code, actual])

		if _has_emoji(actual):
			_fail("[%s] BtnBagGoWorkshop 含有系統 Emoji: %s" % [code, actual])

		if code in ["en", "ko", "es"]:
			if _has_cjk(actual):
				_fail("[%s] BtnBagGoWorkshop 文字殘留 CJK 中文字元: %s" % [code, actual])
			else:
				print("  ✓ [%s] 無 CJK 中文殘留" % code)

	# 恢復繁中
	_loc.call("set_locale", "zh_TW")
	_lobby.call("_on_locale_changed", "zh_TW")


func _capture_and_save(path: String) -> void:
	var img := root.get_texture().get_image()
	if img == null:
		_fail("無法自 root 取得視窗圖像: " + path)
		return
	var err := img.save_png(path)
	if err != OK:
		_fail("存檔失敗 (代碼 %d): %s" % [err, path])
		return

	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		_fail("無法讀取已儲存之截圖: " + path)
		return
	var buf := f.get_buffer(f.get_length())
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	var hash_bytes := ctx.finish()
	var hash_str := hash_bytes.hex_encode()

	if _proof_hashes.has(hash_str):
		_fail("截圖存證發現重複雜湊 (SHA256: %s): %s" % [hash_str, path])
	else:
		_proof_hashes.append(hash_str)
		print("  [截圖存證] %s (SHA256: %s)" % [path.get_file(), hash_str.substr(0, 12)])


func _finish() -> void:
	print("\n=======================================================")
	if _ok:
		print("TEST_BAG_WORKSHOP_SHORTCUT_OK")
	else:
		print("TEST_BAG_WORKSHOP_SHORTCUT_FAILED")
	print("=======================================================")
	quit(0 if _ok else 1)
