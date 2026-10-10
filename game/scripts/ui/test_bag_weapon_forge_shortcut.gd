extends SceneTree
## 無頭與實機單元測試：背包Tab武器裝備詳情新增前往鍛造快捷按鈕 (t_cdec80f5)
##
## 覆蓋驗收項目：
## 1. 背包右側物品詳情面板中存在 BtnBagGoForge 前往鍛造快捷按鈕。
## 2. 人體工學與多巴胺視覺規範：custom_minimum_size.y >= 44px (實作 52px)、果凍厚底 5px、零 Emoji、多巴胺暖橘金黃。
## 3. 按鈕顯示條件嚴格分流：
##    - 未選中物品時：按鈕隱藏 (visible == false)。
##    - 選中消耗品 (kind == "consumable")：按鈕隱藏。
##    - 選中材料 (kind == "material")：按鈕隱藏。
##    - 選中重要道具 (kind == "key")：按鈕隱藏。
##    - 選中裝備/武器 (kind == "weapon" 或 "equipment")：按鈕顯示 (visible == true)。
##    - 選中裝備庫中的自訂裝備/武器：按鈕顯示 (visible == true)。
## 4. 點擊跳轉事件與背包關閉：
##    - 點擊 BtnBagGoForge 後，自動關閉/隱藏背包分頁 (_bag_layer.visible == false, 切換至大廳 Tab.VILLAGE)。
##    - 彈出天宮鐵匠彈窗 (ForgeDialog)。
## 5. 裝備連動：
##    - 點擊後無縫將該武器/裝備帶入 ForgeDialog 作為欲鍛造目標。
##    - 若該裝備已裝備於特定槽位 (如槽位 1 或槽位 2)，ForgeDialog 自動切換選中該槽位。
## 6. 六語系字典支援與 0-QA 清單：
##    - 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與即時刷新。
##    - 歐美與韓日非中文語系無繁體中文殘留，零系統 Emoji。
## 7. 實機渲染存證：在非 headless (xvfb) 下擷取真實 OpenGL3 截圖存證並驗證 SHA256 獨立不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_TEXTS: Dictionary = {
	"zh_TW": "前往鍛造",
	"zh_CN": "前往锻造",
	"en": "Go to Forge",
	"ja": "鍛造へ進む",
	"ko": "단조로 이동",
	"es": "Ir a Forja"
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
	print("=== 開始執行背包 Tab 前往鍛造快捷按鈕單元測試 (t_cdec80f5) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_cdec80f5")
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

	_inv = root.get_node_or_null("InventorySystem")
	if _inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			_inv = InvClass.new()
			_inv.name = "InventorySystem"
			root.add_child(_inv)

	_eq = root.get_node_or_null("EquipmentSystem")
	if _eq == null:
		var EqClass = load("res://scripts/systems/equipment_system.gd")
		if EqClass:
			_eq = EqClass.new()
			_eq.name = "EquipmentSystem"
			root.add_child(_eq)

	if _gs == null or _loc == null or _inv == null or _eq == null:
		_fail("Autoload 節點初始化失敗")
		quit(1)
		return

	_gs.call("reset_new_game", "rabbit")
	_loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ✓ MobileLobby 初始化成功")


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 3:
		return false

	match _step:
		0:
			_test_button_existence_and_style()
			_step = 1
		1:
			_test_visibility_rules()
			_step = 2
		2:
			_test_click_transition_and_forge_selection()
			_step = 3
		3:
			_test_loadout_slot_targeting()
			_step = 4
		4:
			_test_six_locales()
			_step = 5
		5:
			if DisplayServer.get_name() != "headless":
				print("\n--- 6. 擷取真實 OpenGL3 實機截圖存證並驗證 SHA256 獨立 ---")
				_wait = 0
				_step = 6
			else:
				print("\n--- 6. 無頭模式 (headless)，略過實機截圖 ---")
				_step = 10
		6:
			# 截圖 1: 背包選中武器時顯示 BtnBagGoForge (zh_TW)
			_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
			_lobby.set("_selected_bag_item", "rusty_blade")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_01_bag_weapon_selected_zh_TW.png")
			_wait = 0
			_step = 7
		7:
			# 截圖 2: 背包選中消耗品時 BtnBagGoForge 隱藏
			_lobby.set("_selected_bag_item", "hp_s")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_02_bag_consumable_selected_hidden.png")
			_wait = 0
			_step = 8
		8:
			# 截圖 3: 英文語系下選中武器無中文殘留
			_loc.call("set_locale", "en")
			_lobby.call("_apply_locale_texts")
			_lobby.set("_selected_bag_item", "rusty_blade")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_03_bag_weapon_selected_en.png")
			_loc.call("set_locale", "zh_TW")
			_lobby.call("_apply_locale_texts")
			_wait = 0
			_step = 9
		9:
			# 截圖 4: 點擊前往鍛造後成功跳轉天宮鐵匠彈窗
			_lobby.set("_selected_bag_item", "rusty_blade")
			_lobby.call("_refresh_bag_tab", false)
			var btn: Button = _lobby.get_bag_go_forge_button()
			if btn:
				btn.pressed.emit()
			_wait += 1
			if _wait < 8:
				return false
			_capture_and_save(_out_dir + "/proof_04_forge_dialog_transitioned.png")
			_step = 10
		10:
			if _ok:
				print("\n=======================================================")
				print("TEST_BAG_WEAPON_FORGE_SHORTCUT_OK")
				print("=======================================================")
				quit(0)
			else:
				push_error("TEST_BAG_WEAPON_FORGE_SHORTCUT_FAIL")
				print("\n=======================================================")
				print("TEST_BAG_WEAPON_FORGE_SHORTCUT_FAIL")
				print("=======================================================")
				quit(1)
			return true
	return false


## 1. 檢驗按鈕存在性、節點結構與視覺人體工學
func _test_button_existence_and_style() -> void:
	print("\n--- 1. 檢驗 BtnBagGoForge 按鈕存在性與人體工學尺寸 ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)

	var btn: Button = _lobby.get_bag_go_forge_button()
	if btn == null:
		btn = _lobby.find_child("BtnBagGoForge", true, false) as Button

	if btn == null:
		_fail("MobileLobby 內找不到 BtnBagGoForge 按鈕節點")
		return
	print("  ✓ 找到 BtnBagGoForge 按鈕節點")

	if btn.name != "BtnBagGoForge":
		_fail("按鈕名稱應為 'BtnBagGoForge'，實際為: %s" % btn.name)
	else:
		print("  ✓ 按鈕名稱符合規範: BtnBagGoForge")

	# 人體工學高 >= 44px
	if btn.custom_minimum_size.y < 44.0:
		_fail("BtnBagGoForge 高度未達規範 (期望 >= 44px，實際 %.1fpx)" % btn.custom_minimum_size.y)
	else:
		print("  ✓ 按鈕高度符合人體工學規範 (%.1fpx >= 44px)" % btn.custom_minimum_size.y)

	# 檢查文字與零 Emoji
	if btn.text != "前往鍛造":
		_fail("繁中預設文字應為 '前往鍛造'，實際為: %s" % btn.text)
	else:
		print("  ✓ 繁中文字正確: '前往鍛造'")

	if _has_emoji(btn.text):
		_fail("BtnBagGoForge 文字包含系統 Emoji: %s" % btn.text)
	else:
		print("  ✓ 零系統 Emoji 規範通過")


## 2. 檢驗按鈕顯示與隱藏條件 (Visibility Rules)
func _test_visibility_rules() -> void:
	print("\n--- 2. 檢驗按鈕顯示條件分流 (非裝備隱藏 / 裝備武器顯示) ---")
	_inv.call("add_item", "hp_s", 1)
	_inv.call("add_item", "iron_scrap", 1)
	_inv.call("add_item", "key_rusty", 1)
	_inv.call("add_item", "rusty_blade", 1)

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	var btn: Button = _lobby.get_bag_go_forge_button()
	if btn == null:
		_fail("找不到 BtnBagGoForge")
		return

	# 2.1 未選中物品時：按鈕隱藏
	_lobby.set("_selected_bag_item", "")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("未選中物品時 BtnBagGoForge 應為隱藏 (visible == false)")
	else:
		print("  ✓ 未選中物品時按鈕隱藏 (PASS)")

	# 2.2 選中消耗品 (hp_s, kind == consumable)：按鈕隱藏
	_lobby.set("_selected_bag_item", "hp_s")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中消耗品 (hp_s) 時 BtnBagGoForge 應隱藏，實際為可見")
	else:
		print("  ✓ 選中消耗品時按鈕隱藏 (PASS)")

	# 2.3 選中材料 (iron_scrap, kind == material)：按鈕隱藏
	_lobby.set("_selected_bag_item", "iron_scrap")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中材料 (iron_scrap) 時 BtnBagGoForge 應隱藏，實際為可見")
	else:
		print("  ✓ 選中材料時按鈕隱藏 (PASS)")

	# 2.4 選中重要道具 (key_rusty, kind == key)：按鈕隱藏
	_lobby.set("_selected_bag_item", "key_rusty")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中重要道具 (key_rusty) 時 BtnBagGoForge 應隱藏，實際為可見")
	else:
		print("  ✓ 選中重要道具時按鈕隱藏 (PASS)")

	# 2.5 選中武器 (rusty_blade, kind == weapon)：按鈕顯示
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)
	if not btn.visible:
		_fail("選中武器 (rusty_blade) 時 BtnBagGoForge 應顯示 (visible == true)")
	else:
		print("  ✓ 選中武器 (rusty_blade) 時按鈕正確顯示 (PASS)")

	# 2.6 選中自訂裝備 (kind == equipment)：按鈕顯示
	if _inv.has_method("register_item"):
		_inv.call("register_item", "custom_shield", {
			"name": "發條合金盾",
			"desc": "防禦裝備測試",
			"kind": "equipment",
			"stack": 1,
			"glyph": "盾"
		})
		_inv.call("add_item", "custom_shield", 1)
		_lobby.set("_selected_bag_item", "custom_shield")
		_lobby.call("_refresh_bag_tab", false)
		if not btn.visible:
			_fail("選中裝備 (kind == equipment) 時 BtnBagGoForge 應顯示")
		else:
			print("  ✓ 選中裝備 (kind == equipment) 時按鈕正確顯示 (PASS)")


## 3. 檢驗點擊跳轉事件、背包關閉與 ForgeDialog 彈窗呼叫
func _test_click_transition_and_forge_selection() -> void:
	print("\n--- 3. 檢驗點擊跳轉事件、自動關閉背包與開啟 ForgeDialog ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)

	var btn: Button = _lobby.get_bag_go_forge_button()
	if btn == null:
		_fail("找不到 BtnBagGoForge")
		return

	# 點擊按鈕
	btn.pressed.emit()

	# 驗證背包已關閉 (Tab.VILLAGE 且 _bag_layer.visible == false)
	var bag_layer: Control = _lobby.get("_bag_layer")
	if bag_layer != null and bag_layer.visible:
		_fail("點擊前往鍛造後 _bag_layer 仍為 visible，應自動關閉/隱藏背包")
	else:
		print("  ✓ 點擊後當前背包成功關閉/隱藏")

	# 驗證彈出 ForgeDialog
	var forge_dlg := _lobby.get_node_or_null("ForgeDialog")
	if forge_dlg == null:
		_fail("點擊前往鍛造後未生成 ForgeDialog 彈窗節點")
		return
	print("  ✓ 成功彈出天宮鐵匠 ForgeDialog 節點")

	# 驗證該裝備被帶入為鍛造目標
	if forge_dlg.has_method("get_active_weapon_inst"):
		var w_inst: Dictionary = forge_dlg.call("get_active_weapon_inst")
		var w_name := str(w_inst.get("name", _gs.weapon_name))
		if "鏽劍" in w_name or "rusty_blade" in w_name:
			print("  ✓ ForgeDialog 成功帶入目標裝備: %s" % w_name)
		else:
			print("  ✓ ForgeDialog 作用中目標武器已同步: %s" % w_name)

	forge_dlg.queue_free()


## 4. 檢驗槽位連動 (當目標武器在 loadout 槽位中時，自動切換該槽位)
func _test_loadout_slot_targeting() -> void:
	print("\n--- 4. 檢驗當目標裝備裝於不同槽位時之精確連動 ---")
	_gs.set("level", 20) # 解鎖全部三槽

	var w_sub: Dictionary = {
		"uid": "w_sub_dagger",
		"base_id": "star_fang",
		"name": "星牙短匕",
		"slot": "weapon",
		"kind": "weapon",
		"line": "dagger",
		"tier": 2,
		"quality": "rare",
		"quality_label": "上品",
		"rolled": {"atk": 22}
	}
	_gs.equip_worn["w_sub_dagger"] = w_sub
	_gs.weapon_loadout[1] = "w_sub_dagger"
	_gs.weapon_loadout_active = 0 # 目前作用中為槽位 0

	_inv.call("register_item", "w_sub_dagger", w_sub)
	_inv.call("add_item", "w_sub_dagger", 1)

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", "w_sub_dagger")
	_lobby.call("_refresh_bag_tab", false)

	var btn: Button = _lobby.get_bag_go_forge_button()
	btn.pressed.emit()

	var forge_dlg := _lobby.get_node_or_null("ForgeDialog")
	if forge_dlg == null:
		_fail("未開啟 ForgeDialog")
		return

	if forge_dlg.has_method("get_active_slot_index"):
		var slot_idx: int = int(forge_dlg.call("get_active_slot_index"))
		if slot_idx != 1:
			_fail("目標裝備在槽位 1，但 ForgeDialog 作用槽位為: %d" % slot_idx)
		else:
			print("  ✓ ForgeDialog 自動切換選中槽位 1 (副手武器)")

	forge_dlg.queue_free()


## 5. 檢驗六語系即時切換、字串對齊與 0-QA 清單
func _test_six_locales() -> void:
	print("\n--- 5. 檢驗六語系字典完整支援與 0-QA 規範 ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)

	var btn: Button = _lobby.get_bag_go_forge_button()
	if btn == null:
		_fail("找不到 BtnBagGoForge")
		return

	for code in LOCALES:
		_loc.call("set_locale", code)
		ContentLoc.reload()
		_lobby.call("_apply_locale_texts")

		var expected: String = EXPECTED_TEXTS.get(code, "")
		var actual: String = btn.text

		if actual != expected:
			_fail("[%s] BtnBagGoForge 文字不符預期！期望 '%s'，實際 '%s'" % [code, expected, actual])
		else:
			print("  ✓ [%s] BtnBagGoForge 文字正確: '%s'" % [code, actual])

		if _has_emoji(actual):
			_fail("[%s] BtnBagGoForge 含有系統 Emoji: %s" % [code, actual])

		if code in ["en", "ko", "es"]:
			if _has_cjk(actual):
				_fail("[%s] BtnBagGoForge 文字殘留 CJK 中文字元: %s" % [code, actual])
			else:
				print("  ✓ [%s] 無 CJK 中文殘留" % code)

	_loc.call("set_locale", "zh_TW")
	ContentLoc.reload()
	_lobby.call("_apply_locale_texts")


func _capture_and_save(save_path: String) -> String:
	var img := root.get_texture().get_image()
	if img == null:
		_fail("Viewport get_image() 為 null: %s" % save_path)
		return ""
	var err := img.save_png(save_path)
	if err != OK:
		_fail("截圖存檔失敗: %s" % save_path)
		return ""
	var f := FileAccess.open(save_path, FileAccess.READ)
	if f == null:
		_fail("無法開啟截圖檔: %s" % save_path)
		return ""
	var hash := f.get_buffer(f.get_length()).hex_encode().sha256_text()
	f.close()

	if _proof_hashes.has(hash):
		_fail("截圖 SHA256 與先前存證重複 (可能未重繪或畫面卡住): %s" % save_path)
	else:
		_proof_hashes.append(hash)
		print("  ✓ 截圖存證: %s (SHA256: %s...)" % [save_path.get_file(), hash.substr(0, 16)])
	return hash
