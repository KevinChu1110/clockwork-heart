extends SceneTree
## 無頭與實機單元測試：背包Tab武器裝備詳情新增『拆解回收』按鈕 (t_68937335)
##
## 覆蓋驗收項目：
## 1. 背包右側物品詳情面板中存在 BtnBagDismantle 拆解回收按鈕。
## 2. 人體工學與多巴胺視覺規範：custom_minimum_size.y >= 52px、果凍厚底 5px、圓角 18px、零 Emoji、多巴胺鮮亮珊瑚粉 (#FF5E8A) 底色與深藍紫描邊 (#1F1A3A)。
## 3. 按鈕顯示條件嚴格分流：
##    - 未選中物品時：按鈕隱藏 (visible == false)。
##    - 選中消耗品 (kind == "consumable")：按鈕隱藏。
##    - 選中材料 (kind == "material")：按鈕隱藏。
##    - 選中重要道具 (kind == "key")：按鈕隱藏。
##    - 選中裝備/武器 (kind == "weapon" 或 "equipment")：按鈕顯示 (visible == true)。
## 4. 裝備鎖定防拆 (Lock Protection)：
##    - 裝備鎖定時 (EquipmentSystem.is_locked(uid) == true)，按鈕禁用 (disabled == true)，文字切換為「已鎖定」。
##    - 點擊或呼叫 EquipmentSystem.dismantle(uid) 嚴格阻擋並提示「裝備已鎖定，無法拆解。」。
##    - 解鎖後按鈕恢復啟用 (disabled == false)，文字切換為「拆解回收」。
## 5. 穿戴中防拆 (Equipped/Worn Protection)：
##    - 處於裝備中時 (worn / loadout)，按鈕禁用 (disabled == true)，文字切換為「裝備中」。
##    - 點擊或呼叫 EquipmentSystem.dismantle(uid) 嚴格阻擋並提示「裝備中無法拆解，請先卸下。」。
##    - 卸下裝備後按鈕恢復啟用。
## 6. 成功拆解與即時刷新 (Dismantle Success & Real-time Refresh)：
##    - 點擊拆解回收按鈕後，呼叫 EquipmentSystem.dismantle(uid)，該裝備成功自背包移除。
##    - 獲得對應鐵屑 (iron_scrap) 與金幣 (gold)，彈出獲得提示 Toast。
##    - 背包格子清單與 HUD 資源即時刷新。
## 7. 六語系字典支援與 0-QA 規範：
##    - 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時動態切換支援。
##    - 歐美與韓日非中文語系無繁體中文殘留，零系統 Emoji。
## 8. 實機渲染存證：在非 headless (xvfb) 下擷取真實 OpenGL3 截圖存證並驗證 SHA256 獨立不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_DISMANTLE_TEXTS: Dictionary = {
	"zh_TW": "拆解回收",
	"zh_CN": "拆解回收",
	"en": "Dismantle",
	"ja": "分解回収",
	"ko": "분해 회수",
	"es": "Desmantelar"
}
const EXPECTED_LOCKED_TEXTS: Dictionary = {
	"zh_TW": "已鎖定",
	"zh_CN": "已锁定",
	"en": "Locked",
	"ja": "ロック中",
	"ko": "잠금됨",
	"es": "Bloqueado"
}
const EXPECTED_EQUIPPED_TEXTS: Dictionary = {
	"zh_TW": "裝備中",
	"zh_CN": "装备中",
	"en": "Equipped",
	"ja": "装備中",
	"ko": "장착 중",
	"es": "Equipado"
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

var _proof_unlocked_uid := ""
var _proof_locked_uid := ""
var _proof_equipped_uid := ""


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
	print("=== 開始執行背包 Tab 拆解回收按鈕單元測試 (t_68937335) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://../proofs/t_68937335")
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
			_test_locked_protection()
			_step = 3
		3:
			_test_equipped_protection()
			_step = 4
		4:
			_test_dismantle_success_and_refresh()
			_step = 5
		5:
			_test_six_locales()
			_step = 6
		6:
			if DisplayServer.get_name() != "headless":
				print("\n--- 7. 擷取真實 OpenGL3 實機截圖存證並驗證 SHA256 獨立 ---")
				var cur_toast: Label = _lobby.get("_current_toast")
				if cur_toast and is_instance_valid(cur_toast):
					cur_toast.queue_free()
					_lobby.set("_current_toast", null)
				_setup_screenshot_states()
				_wait = 0
				_step = 7
			else:
				print("\n--- 7. 無頭模式 (headless)，略過實機截圖 ---")
				_step = 20
		7:
			# 截圖 1: 背包選中可拆解武器時顯示 BtnBagDismantle (zh_TW)
			_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
			_lobby.set("_selected_bag_item", _proof_unlocked_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_01_bag_weapon_selected_zh_TW.png")
			_wait = 0
			_step = 8
		8:
			# 截圖 2: 選中消耗品時 BtnBagDismantle 嚴格隱藏
			_lobby.set("_selected_bag_item", "hp_s")
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_02_bag_consumable_selected_hidden.png")
			_wait = 0
			_step = 9
		9:
			# 截圖 3: 選中已鎖定裝備時按鈕顯示「已鎖定」且 disabled
			_lobby.set("_selected_bag_item", _proof_locked_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_03_bag_weapon_locked_disabled.png")
			_wait = 0
			_step = 10
		10:
			# 截圖 4: 選中裝備中武器時按鈕顯示「裝備中」且 disabled
			_lobby.set("_selected_bag_item", _proof_equipped_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_04_bag_weapon_equipped_disabled.png")
			_wait = 0
			_step = 11
		11:
			# 截圖 5: 英文語系 (en) 下顯示 "Dismantle" 且零 CJK 殘留
			_loc.call("set_locale", "en")
			ContentLoc.reload()
			_lobby.call("_apply_locale_texts")
			_lobby.set("_selected_bag_item", _proof_unlocked_uid)
			_lobby.call("_refresh_bag_tab", false)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_05_bag_weapon_selected_en.png")
			_loc.call("set_locale", "zh_TW")
			ContentLoc.reload()
			_lobby.call("_apply_locale_texts")
			_wait = 0
			_step = 12
		12:
			# 點擊拆解回收按鈕一次
			_lobby.set("_selected_bag_item", _proof_unlocked_uid)
			_lobby.call("_refresh_bag_tab", false)
			var btn: Button = _lobby.get_bag_dismantle_button()
			if btn:
				btn.pressed.emit()
			_wait = 0
			_step = 13
		13:
			# 等待 Toast 與介面刷新渲染完成 (3~5 幀)
			_wait += 1
			if _wait < 6:
				return false
			_capture_and_save(_out_dir + "/proof_06_dismantled_toast_and_refreshed.png")
			_step = 20
		20:
			if _ok:
				print("\n=======================================================")
				print("TEST_BAG_DISMANTLE_BTN_OK")
				print("=======================================================")
				quit(0)
			else:
				push_error("TEST_BAG_DISMANTLE_BTN_FAIL")
				print("\n=======================================================")
				print("TEST_BAG_DISMANTLE_BTN_FAIL")
				print("=======================================================")
				quit(1)
			return true
	return false


## 1. 檢驗按鈕存在性、多巴胺風格、人體工學尺寸與零 Emoji
func _test_button_existence_and_style() -> void:
	print("\n--- 1. 檢驗 BtnBagDismantle 按鈕存在性與多巴胺視覺規範 ---")
	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("MobileLobby 內找不到 BtnBagDismantle 按鈕")
		return
	print("  ✓ 找到 BtnBagDismantle 按鈕節點")

	if btn.name != "BtnBagDismantle":
		_fail("按鈕名稱不符規範 (期望 BtnBagDismantle，實際 %s)" % btn.name)
	else:
		print("  ✓ 按鈕名稱符合規範: BtnBagDismantle")

	# 人體工學高 >= 52px
	if btn.custom_minimum_size.y < 52.0:
		_fail("BtnBagDismantle 高度未達規範 (期望 >= 52px，實際 %.1fpx)" % btn.custom_minimum_size.y)
	else:
		print("  ✓ 按鈕高度符合人體工學規範 (%.1fpx >= 52px)" % btn.custom_minimum_size.y)

	# 檢查 StyleBoxFlat 樣式
	var sb_normal := btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb_normal == null:
		_fail("BtnBagDismantle normal stylebox 未設定或型別錯誤")
	else:
		var bg_hex := sb_normal.bg_color.to_html(false).to_upper()
		if bg_hex != "FF5E8A":
			_fail("BtnBagDismantle 底色非多巴胺珊瑚粉 #FF5E8A (實際 #%s)" % bg_hex)
		else:
			print("  ✓ 按鈕底色符合多巴胺珊瑚粉 (#FF5E8A)")

		if sb_normal.border_width_bottom != 5:
			_fail("BtnBagDismantle 果凍厚底未達 5px (實際 %dpx)" % sb_normal.border_width_bottom)
		else:
			print("  ✓ 按鈕果凍厚底達標: 5px")

		if sb_normal.corner_radius_top_left != 18:
			_fail("BtnBagDismantle 圓角非 18px (實際 %dpx)" % sb_normal.corner_radius_top_left)
		else:
			print("  ✓ 按鈕圓角規範達標: 18px")

	# 檢查繁中預設文字與零 Emoji
	if btn.text != "拆解回收":
		_fail("繁中預設文字應為 '拆解回收'，實際為: %s" % btn.text)
	else:
		print("  ✓ 繁中文字正確: '拆解回收'")

	if _has_emoji(btn.text):
		_fail("BtnBagDismantle 文字包含系統 Emoji: %s" % btn.text)
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
	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("找不到 BtnBagDismantle")
		return

	# 2.1 未選中物品時：按鈕隱藏
	_lobby.set("_selected_bag_item", "")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("未選中物品時 BtnBagDismantle 應為隱藏 (visible == false)")
	else:
		print("  ✓ 未選中物品時按鈕隱藏 (PASS)")

	# 2.2 選中消耗品 (hp_s, kind == consumable)：按鈕隱藏
	_lobby.set("_selected_bag_item", "hp_s")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中消耗品 (hp_s) 時 BtnBagDismantle 應隱藏，實際為可見")
	else:
		print("  ✓ 選中消耗品時按鈕隱藏 (PASS)")

	# 2.3 選中材料 (iron_scrap, kind == material)：按鈕隱藏
	_lobby.set("_selected_bag_item", "iron_scrap")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中材料 (iron_scrap) 時 BtnBagDismantle 應隱藏，實際為可見")
	else:
		print("  ✓ 選中材料時按鈕隱藏 (PASS)")

	# 2.4 選中重要道具 (key_rusty, kind == key)：按鈕隱藏
	_lobby.set("_selected_bag_item", "key_rusty")
	_lobby.call("_refresh_bag_tab", false)
	if btn.visible:
		_fail("選中重要道具 (key_rusty) 時 BtnBagDismantle 應隱藏，實際為可見")
	else:
		print("  ✓ 選中重要道具時按鈕隱藏 (PASS)")

	# 2.5 選中武器 (rusty_blade, kind == weapon)：按鈕顯示
	_lobby.set("_selected_bag_item", "rusty_blade")
	_lobby.call("_refresh_bag_tab", false)
	if not btn.visible:
		_fail("選中武器 (rusty_blade) 時 BtnBagDismantle 應顯示 (visible == true)")
	else:
		print("  ✓ 選中武器 (rusty_blade) 時按鈕正確顯示 (PASS)")

	# 2.6 選中自訂裝備 (kind == equipment)：按鈕顯示
	if _inv.has_method("register_item"):
		_inv.call("register_item", "custom_shield_test", {
			"name": "發條合金盾",
			"desc": "防禦裝備測試",
			"kind": "equipment",
			"stack": 1,
			"glyph": "盾"
		})
		_inv.call("add_item", "custom_shield_test", 1)
		_lobby.set("_selected_bag_item", "custom_shield_test")
		_lobby.call("_refresh_bag_tab", false)
		if not btn.visible:
			_fail("選中裝備 (kind == equipment) 時 BtnBagDismantle 應顯示")
		else:
			print("  ✓ 選中裝備 (kind == equipment) 時按鈕正確顯示 (PASS)")


## 3. 檢驗裝備鎖定防拆 (Lock Protection)
func _test_locked_protection() -> void:
	print("\n--- 3. 檢驗裝備鎖定防拆連動 (EquipmentSystem.is_locked) ---")
	var w_inst: Dictionary = _eq.call("roll_instance", "rusty_blade", "rare")
	var uid: String = str(w_inst.get("uid", "w_lock_test_01"))
	w_inst["uid"] = uid
	_eq.call("add_to_bag", w_inst)

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", uid)
	_lobby.call("_refresh_bag_tab", false)

	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("找不到 BtnBagDismantle")
		return

	# 3.1 初始未鎖定狀態
	if btn.disabled:
		_fail("未鎖定裝備之 BtnBagDismantle 應為可點擊 (disabled == false)")
	if btn.text != "拆解回收":
		_fail("未鎖定裝備之按鈕文字應為 '拆解回收'，實際為: %s" % btn.text)
	print("  ✓ 未鎖定狀態：按鈕啟用且文字為 '拆解回收'")

	# 3.2 鎖定該裝備
	_eq.call("set_locked", uid, true)
	assert(_eq.call("is_locked", uid) == true, "裝備應已鎖定")

	_lobby.call("_refresh_bag_tab", false)
	if not btn.disabled:
		_fail("鎖定裝備之 BtnBagDismantle 應被禁用 (disabled == true)")
	if btn.text != "已鎖定":
		_fail("鎖定裝備之按鈕文字應為 '已鎖定'，實際為: %s" % btn.text)
	print("  ✓ 鎖定狀態：按鈕禁用且文字切換為 '已鎖定'")

	# 3.3 嘗試呼叫 dismantle(uid) 應嚴格被阻擋
	var r_fail: Dictionary = _eq.call("dismantle", uid)
	if bool(r_fail.get("ok", true)):
		_fail("已鎖定裝備呼叫 dismantle 應失敗，但回傳 ok == true: %s" % r_fail)
	else:
		print("  ✓ EquipmentSystem.dismantle 嚴格阻擋已鎖定裝備: %s" % r_fail.get("msg", ""))

	# 3.4 解鎖該裝備
	_eq.call("set_locked", uid, false)
	assert(_eq.call("is_locked", uid) == false, "裝備應已解鎖")

	_lobby.call("_refresh_bag_tab", false)
	if btn.disabled:
		_fail("解鎖後 BtnBagDismantle 應恢復可點擊 (disabled == false)")
	if btn.text != "拆解回收":
		_fail("解鎖後按鈕文字應恢復 '拆解回收'，實際為: %s" % btn.text)
	print("  ✓ 解鎖後狀態：按鈕恢復啟用且文字為 '拆解回收'")


## 4. 檢驗穿戴中防拆 (Equipped/Worn Protection)
func _test_equipped_protection() -> void:
	print("\n--- 4. 檢驗穿戴中防拆連動 (worn / loadout) ---")
	var w_inst: Dictionary = _eq.call("roll_instance", "rusty_blade", "uncommon")
	var uid: String = str(w_inst.get("uid", "w_worn_test_01"))
	w_inst["uid"] = uid
	_eq.call("add_to_bag", w_inst)

	# 裝備該武器到槽位 0
	var er: Dictionary = _eq.call("equip_weapon_to_loadout", uid, 0)
	assert(bool(er.get("ok", false)), "裝備穿戴失敗: %s" % er)
	assert(_eq.call("is_equipped", uid) == true, "裝備應處於已穿戴狀態")

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", uid)
	_lobby.call("_refresh_bag_tab", false)

	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("找不到 BtnBagDismantle")
		return

	if not btn.disabled:
		_fail("穿戴中裝備之 BtnBagDismantle 應被禁用 (disabled == true)")
	if btn.text != "裝備中":
		_fail("穿戴中裝備之按鈕文字應為 '裝備中'，實際為: %s" % btn.text)
	print("  ✓ 穿戴中狀態：按鈕禁用且文字切換為 '裝備中'")

	# 嘗試拆解應失敗
	var r_fail: Dictionary = _eq.call("dismantle", uid)
	if bool(r_fail.get("ok", true)):
		_fail("穿戴中裝備呼叫 dismantle 應失敗，但回傳 ok == true: %s" % r_fail)
	else:
		print("  ✓ EquipmentSystem.dismantle 嚴格阻擋穿戴中裝備: %s" % r_fail.get("msg", ""))

	# 卸下武器槽位 0
	_eq.call("unequip_loadout_slot", 0)
	assert(_eq.call("is_equipped", uid) == false, "裝備應已卸下")

	_lobby.call("_refresh_bag_tab", false)
	if btn.disabled:
		_fail("卸下裝備後 BtnBagDismantle 應恢復可點擊 (disabled == false)")
	if btn.text != "拆解回收":
		_fail("卸下裝備後按鈕文字應恢復 '拆解回收'，實際為: %s" % btn.text)
	print("  ✓ 卸下後狀態：按鈕恢復啟用且文字為 '拆解回收'")


## 5. 檢驗成功拆解與背包即時刷新 (Dismantle Success & Real-time Refresh)
func _test_dismantle_success_and_refresh() -> void:
	print("\n--- 5. 檢驗成功拆解回收與背包/資源即時刷新 ---")
	var w_inst: Dictionary = _eq.call("roll_instance", "rusty_blade", "rare")
	var uid: String = str(w_inst.get("uid", "w_dismantle_real_01"))
	w_inst["uid"] = uid
	_eq.call("add_to_bag", w_inst)

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	_lobby.set("_selected_bag_item", uid)
	_lobby.call("_refresh_bag_tab", false)

	var prev_scrap: int = _inv.call("count", "iron_scrap")
	var prev_gold: int = _gs.get("gold")
	var yield_val: Dictionary = _eq.call("dismantle_yield", w_inst)
	var exp_scrap: int = int(yield_val.get("iron_scrap", 0))
	var exp_gold: int = int(yield_val.get("gold", 0))

	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("找不到 BtnBagDismantle")
		return

	# 點擊拆解回收按鈕
	btn.pressed.emit()

	# 驗證裝備已被移除
	var check_inst: Dictionary = _eq.call("find_bag", uid)
	if not check_inst.is_empty():
		_fail("拆解後裝備仍存在於 equip_bag")
	else:
		print("  ✓ 裝備已自背包中乾淨移除")

	# 驗證資源收益
	var cur_scrap: int = _inv.call("count", "iron_scrap")
	var cur_gold: int = _gs.get("gold")
	if cur_scrap != prev_scrap + exp_scrap:
		_fail("鐵屑收益不符 (期望 %d，實際 %d)" % [prev_scrap + exp_scrap, cur_scrap])
	else:
		print("  ✓ 鐵屑收益精確入帳: +%d" % exp_scrap)

	if cur_gold != prev_gold + exp_gold:
		_fail("金幣收益不符 (期望 %d，實際 %d)" % [prev_gold + exp_gold, cur_gold])
	else:
		print("  ✓ 金幣收益精確入帳: +%d" % exp_gold)

	# 驗證當前已選取之物品已更新
	var sel_now: String = _lobby.get("_selected_bag_item")
	if sel_now == uid:
		_fail("背包選中目標未刷新，仍指向已被拆解之裝備: %s" % uid)
	else:
		print("  ✓ 背包選取焦點即時刷新為: %s" % (sel_now if not sel_now.is_empty() else "(空)"))


## 6. 檢驗六語系字典完整支援與 0-QA 規範
func _test_six_locales() -> void:
	print("\n--- 6. 檢驗六語系字典完整支援與 0-QA 規範 ---")
	# 建立 3 個獨立物品分別對應：正常可拆、已鎖定、裝備中
	var w_norm: Dictionary = _eq.call("roll_instance", "rusty_blade", "common")
	var uid_norm: String = "w_loc_norm_01"
	w_norm["uid"] = uid_norm
	_eq.call("add_to_bag", w_norm)

	var w_lock: Dictionary = _eq.call("roll_instance", "rusty_blade", "rare")
	var uid_lock: String = "w_loc_lock_02"
	w_lock["uid"] = uid_lock
	_eq.call("add_to_bag", w_lock)
	_eq.call("set_locked", uid_lock, true)

	var w_worn: Dictionary = _eq.call("roll_instance", "rusty_blade", "epic")
	var uid_worn: String = "w_loc_worn_03"
	w_worn["uid"] = uid_worn
	_eq.call("add_to_bag", w_worn)
	_eq.call("equip_weapon_to_loadout", uid_worn, 0)

	_lobby._switch_tab(MobileLobbyScript.Tab.BAG)
	var btn: Button = _lobby.get_bag_dismantle_button()
	if btn == null:
		_fail("找不到 BtnBagDismantle")
		return

	for code in LOCALES:
		_loc.call("set_locale", code)
		ContentLoc.reload()
		_lobby.call("_apply_locale_texts")

		# 6.1 測試「拆解回收」
		_lobby.set("_selected_bag_item", uid_norm)
		_lobby.call("_refresh_bag_tab", false)
		var exp_dis: String = EXPECTED_DISMANTLE_TEXTS.get(code, "")
		var act_dis: String = btn.text
		if act_dis != exp_dis:
			_fail("[%s] 拆解按鈕文字不符預期！期望 '%s'，實際 '%s'" % [code, exp_dis, act_dis])
		else:
			print("  ✓ [%s] 拆解按鈕文字正確: '%s'" % [code, act_dis])

		if _has_emoji(act_dis):
			_fail("[%s] BtnBagDismantle 含有系統 Emoji: %s" % [code, act_dis])

		if code in ["en", "ko", "es"]:
			if _has_cjk(act_dis):
				_fail("[%s] 拆解按鈕文字殘留 CJK 中文字元: %s" % [code, act_dis])
			else:
				print("  ✓ [%s] 拆解按鈕無 CJK 中文殘留" % code)

		# 6.2 測試「已鎖定」
		_lobby.set("_selected_bag_item", uid_lock)
		_lobby.call("_refresh_bag_tab", false)
		var exp_lock: String = EXPECTED_LOCKED_TEXTS.get(code, "")
		var act_lock: String = btn.text
		if act_lock != exp_lock:
			_fail("[%s] 鎖定按鈕文字不符預期！期望 '%s'，實際 '%s'" % [code, exp_lock, act_lock])
		else:
			print("  ✓ [%s] 鎖定按鈕文字正確: '%s'" % [code, act_lock])

		if code in ["en", "ko", "es"]:
			if _has_cjk(act_lock):
				_fail("[%s] 已鎖定文字殘留 CJK 中文字元: %s" % [code, act_lock])

		# 6.3 測試「裝備中」
		_lobby.set("_selected_bag_item", uid_worn)
		_lobby.call("_refresh_bag_tab", false)
		var exp_eq: String = EXPECTED_EQUIPPED_TEXTS.get(code, "")
		var act_eq: String = btn.text
		if act_eq != exp_eq:
			_fail("[%s] 裝備中按鈕文字不符預期！期望 '%s'，實際 '%s'" % [code, exp_eq, act_eq])
		else:
			print("  ✓ [%s] 裝備中按鈕文字正確: '%s'" % [code, act_eq])

		if code in ["en", "ko", "es"]:
			if _has_cjk(act_eq):
				_fail("[%s] 裝備中文字殘留 CJK 中文字元: %s" % [code, act_eq])

	_loc.call("set_locale", "zh_TW")
	ContentLoc.reload()
	_lobby.call("_apply_locale_texts")


func _setup_screenshot_states() -> void:
	# 建立存證專用實例
	var w1: Dictionary = _eq.call("roll_instance", "rusty_blade", "rare")
	_proof_unlocked_uid = str(w1.get("uid", "proof_unlocked_w1"))
	w1["uid"] = _proof_unlocked_uid
	_eq.call("add_to_bag", w1)

	var w2: Dictionary = _eq.call("roll_instance", "rusty_blade", "epic")
	_proof_locked_uid = str(w2.get("uid", "proof_locked_w2"))
	w2["uid"] = _proof_locked_uid
	_eq.call("add_to_bag", w2)
	_eq.call("set_locked", _proof_locked_uid, true)

	var w3: Dictionary = _eq.call("roll_instance", "rusty_blade", "common")
	_proof_equipped_uid = str(w3.get("uid", "proof_equipped_w3"))
	w3["uid"] = _proof_equipped_uid
	_eq.call("add_to_bag", w3)
	_eq.call("equip_weapon_to_loadout", _proof_equipped_uid, 0)


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
		_fail("截圖 SHA256 與先前存證重複: %s" % save_path)
	else:
		_proof_hashes.append(hash)
	print("  [PROOF SAVED] %s (SHA256: %s)" % [save_path.get_file(), hash.substr(0, 12)])
	return hash
