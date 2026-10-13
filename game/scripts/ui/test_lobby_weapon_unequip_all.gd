extends SceneTree
## 大廳角色頁武器輪替配置新增『一鍵卸下』按鈕與安全防護單元測試 (test_lobby_weapon_unequip_all.gd)
## 依據任務 t_3c98e3bb 驗收標準：
## 1. 大廳角色頁 (mobile_lobby.gd, Tab.CHARACTER) 顯示武器輪替配置標題列中，於現有『一鍵配置』按鈕旁新增『一鍵卸下』按鈕 (BtnWeaponUnequipAll)。
##    按鈕規範：尺寸 >= 104x48px，熱區 >= 48px，珊瑚粉 #FF5E8A 果凍厚底 5px，圓角 16px，深藍紫描邊 2px，字級 16px 開源粉圓體，零 Emoji。
## 2. 連動邏輯：點擊時遍歷武器欄位，調用 EquipmentSystem.unequip_loadout_slot() 將副武器或多餘武器卸下歸還背包；具備安全防護（保留初始武器）。
## 3. 空手防呆：若全卸下則切換至空手拳套防呆 (weapon_name='空手', path_style='fist', weapon_atk=0)，即時刷新三欄卡片、頂部戰力與屬性面板。
## 4. 飄字反饋：成功卸下時提示「已將副武器卸下歸還背包！」；若當前已無可卸下武器，提示「當前無可卸下的武器！」。
## 5. 支援六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，按鈕與提示文字零 hardcode。
## 6. 印出 TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK 哨兵，0 SCRIPT ERROR，quit(0)。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null
var _lobby: Control = null
var _es: Node = null
var _gs: Node = null
var _signal_received := false
var _signal_payload: Dictionary = {}


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _initialize() -> void:
	print("=== 開始 test_lobby_weapon_unequip_all 測試 (t_3c98e3bb) ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	_es = root.get_node_or_null("EquipmentSystem")
	if _es == null:
		var EsClass = load("res://scripts/systems/equipment_system.gd")
		if EsClass:
			_es = EsClass.new()
			_es.name = "EquipmentSystem"
			root.add_child(_es)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)

	if _lobby.has_signal("weapons_unequipped"):
		_lobby.connect("weapons_unequipped", func(res: Dictionary):
			_signal_received = true
			_signal_payload = res
		)


func _process(_delta: float) -> bool:
	_frame += 1

	if _step == 0 and _frame >= 5:
		_step = 1
		_test_btn_exists_and_specs()

	elif _step == 1 and _frame >= 10:
		_step = 2
		_test_unequip_secondary_weapons()

	elif _step == 2 and _frame >= 15:
		_step = 3
		_test_repeat_unequip_no_weapons()

	elif _step == 3 and _frame >= 20:
		_step = 4
		_test_all_unequip_bare_handed_failsafe()

	elif _step == 4 and _frame >= 25:
		_step = 5
		_test_locales_and_no_emoji()

	elif _step == 5 and _frame >= 30:
		_step = 6
		_finish_test()

	return false


func _test_btn_exists_and_specs() -> void:
	print("\n--- 1. 驗證大廳角色頁一鍵卸下按鈕 (BtnWeaponUnequipAll) 存在與規格 ---")
	_lobby.switch_tab(MobileLobby.Tab.CHARACTER)

	var btn: Button = _lobby.find_child("BtnWeaponUnequipAll", true, false) as Button
	if btn == null:
		_fail("角色分頁找不到 BtnWeaponUnequipAll 按鈕")
		return
	print("  ✓ BtnWeaponUnequipAll 按鈕存在")

	var btn_auto: Button = _lobby.find_child("BtnWeaponAutoEquip", true, false) as Button
	if btn_auto == null:
		_fail("角色分頁未見相鄰之 BtnWeaponAutoEquip 按鈕")
	else:
		print("  ✓ BtnWeaponAutoEquip 與 BtnWeaponUnequipAll 均在武器輪替配置標題列中")

	# 熱區 >= 48px，尺寸 >= 104x48
	var msize := btn.custom_minimum_size
	if msize.x < 104 or msize.y < 48:
		_fail("BtnWeaponUnequipAll 尺寸未達標準 (>=104x48px): %s" % str(msize))
	else:
		print("  ✓ BtnWeaponUnequipAll 尺寸符合熱區規範 (>=104x48px): %s" % str(msize))

	var fsize := btn.get_theme_font_size("font_size")
	if fsize != 16:
		_fail("BtnWeaponUnequipAll 字體非 16px 開源粉圓體: %d" % fsize)
	else:
		print("  ✓ BtnWeaponUnequipAll 字體大小符合 16px 規範: %d px" % fsize)

	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if sb is StyleBoxFlat:
		var sbf := sb as StyleBoxFlat
		# 珊瑚粉 #FF5E8A
		var col_hex := sbf.bg_color.to_html(false).to_upper()
		if col_hex != "FF5E8A":
			_fail("BtnWeaponUnequipAll 背景色非珊瑚粉 #FF5E8A: #%s" % col_hex)
		else:
			print("  ✓ BtnWeaponUnequipAll 底色符合珊瑚粉色盤: #%s" % col_hex)

		if sbf.border_width_bottom < 5:
			_fail("BtnWeaponUnequipAll 果凍厚底底部描邊小於 5px: %d" % sbf.border_width_bottom)
		else:
			print("  ✓ BtnWeaponUnequipAll 具備立體果凍厚底 (border_bottom: %d px)" % sbf.border_width_bottom)

		if sbf.corner_radius_top_left != 16:
			_fail("BtnWeaponUnequipAll 圓角非 16px: %d" % sbf.corner_radius_top_left)
		else:
			print("  ✓ BtnWeaponUnequipAll 圓角符合規範 (16px)")

		if sbf.border_width_left != 2:
			_fail("BtnWeaponUnequipAll 描邊寬度非 2px: %d" % sbf.border_width_left)
		else:
			print("  ✓ BtnWeaponUnequipAll 深藍紫描邊符合規範 (2px)")

	if _has_emoji(btn.text):
		_fail("BtnWeaponUnequipAll 含有違規 Emoji: %s" % btn.text)
	else:
		print("  ✓ BtnWeaponUnequipAll 零系統 Emoji 檢查通過")


func _test_unequip_secondary_weapons() -> void:
	print("\n--- 2. 驗證遍歷武器欄位卸下副武器與多餘武器、歸還背包與保留初始武器 ---")
	_gs.level = 20
	_gs.weapon_loadout = ["", "", ""]
	_gs.equip_worn = {}
	_gs.equip_bag = []

	var w1 := {
		"uid": "test_w_primary_sword",
		"base_id": "star_fang",
		"name": "星紋龍牙",
		"slot": "weapon",
		"tier": 3,
		"line": "sword",
		"quality": "epic",
		"rolled": {"atk": 90, "crit": 8.0}
	}
	var w2 := {
		"uid": "test_w_secondary_spear",
		"base_id": "ash_spear",
		"name": "燼木銳矛",
		"slot": "weapon",
		"tier": 2,
		"line": "spear",
		"quality": "rare",
		"rolled": {"atk": 70, "crit": 5.0}
	}
	var w3 := {
		"uid": "test_w_skill_bow",
		"base_id": "reed_bow",
		"name": "風葦輕弓",
		"slot": "weapon",
		"tier": 2,
		"line": "bow",
		"quality": "uncommon",
		"rolled": {"atk": 50, "crit": 3.0}
	}

	_gs.equip_worn[w1.uid] = w1
	_gs.equip_worn[w2.uid] = w2
	_gs.equip_worn[w3.uid] = w3

	_gs.weapon_loadout = [w1.uid, w2.uid, w3.uid]
	_gs.weapon_loadout_active = 0
	_gs.equip_slots["weapon"] = w1.uid
	_gs.weapon_name = w1.name
	_gs.weapon_atk = 90
	_gs.path_style = "sword"

	_lobby.refresh_weapon_slots()
	_lobby.refresh_hud()

	var power_before: int = int(_gs.power_score())
	print("  卸下前戰力: %d，槽位: %s" % [power_before, str(_gs.weapon_loadout)])
	print("  卸下前背包裝備數: %d" % _gs.equip_bag.size())

	_signal_received = false
	var res: Dictionary = _lobby.unequip_all_weapons(true)

	if not bool(res.get("ok", false)) or not bool(res.get("changed", false)):
		_fail("一鍵卸下執行失敗或未觸發變更: %s" % str(res))
		return
	print("  ✓ 一鍵卸下執行成功: %s" % str(res.get("unequipped_slots", [])))

	if not _signal_received:
		_fail("未收到 weapons_unequipped 信號")
	else:
		print("  ✓ 成功接收 weapons_unequipped 信號")

	# 驗證保留初始武器（首選武器 slot 0），副武器 slot 1 與多餘武器 slot 2 卸下
	if str(_gs.weapon_loadout[0]) != w1.uid:
		_fail("初始首選武器 (slot 0) 未保留: %s" % str(_gs.weapon_loadout[0]))
	else:
		print("  ✓ 初始武器安全保留在 slot 0: %s (%s)" % [w1.name, w1.uid])

	if str(_gs.weapon_loadout[1]) != "" or str(_gs.weapon_loadout[2]) != "":
		_fail("副武器或多餘武器未完全卸下: %s" % str(_gs.weapon_loadout))
	else:
		print("  ✓ 副武器 (slot 1) 與多餘武器 (slot 2) 已正確清空卸下")

	# 驗證卸下的武器安全歸還背包
	var bag_uids: Array[String] = []
	for item in _gs.equip_bag:
		bag_uids.append(str(item.get("uid", "")))

	if not bag_uids.has(w2.uid) or not bag_uids.has(w3.uid):
		_fail("副武器未歸還至冒險背包: %s" % str(bag_uids))
	else:
		print("  ✓ 卸下之副武器與絕技武器已全數安全歸還至冒險背包 (背包裝備數: %d)" % _gs.equip_bag.size())

	# 驗證飄字反饋
	var toast_node: Label = _lobby._current_toast
	if toast_node == null or not is_instance_valid(toast_node):
		_fail("一鍵卸下成功後未彈出 Toast 飄字")
	else:
		var exp_toast := "已將副武器卸下歸還背包！"
		if toast_node.text != exp_toast:
			_fail("Toast 飄字文字不符: 期望 '%s'，實際 '%s'" % [exp_toast, toast_node.text])
		else:
			print("  ✓ 飄字反饋正確: '%s'" % toast_node.text)


func _test_repeat_unequip_no_weapons() -> void:
	print("\n--- 3. 驗證當前已無可卸下武器時之防呆判定與提示 ---")
	_signal_received = false
	var res: Dictionary = _lobby.unequip_all_weapons(true)

	if bool(res.get("changed", true)):
		_fail("已無副武器狀態下一鍵卸下仍觸發變更")
	else:
		print("  ✓ 無副武器可卸下時正確判定 changed=false")

	var toast_node: Label = _lobby._current_toast
	if toast_node == null or not is_instance_valid(toast_node):
		_fail("無副武器時未彈出防呆 Toast")
	else:
		var exp_toast := "當前無可卸下的武器！"
		if toast_node.text != exp_toast:
			_fail("防呆 Toast 文字不符: 期望 '%s'，實際 '%s'" % [exp_toast, toast_node.text])
		else:
			print("  ✓ 無可卸下武器防呆飄字反饋正確: '%s'" % toast_node.text)


func _test_all_unequip_bare_handed_failsafe() -> void:
	print("\n--- 4. 驗證全卸下切換至空手拳套防呆安全防護 ---")
	# 執行強制全卸下 (keep_primary = false)
	var res: Dictionary = _lobby.unequip_all_weapons(false)
	if not bool(res.get("ok", false)) or not bool(res.get("changed", false)):
		_fail("強制全卸下執行失敗: %s" % str(res))
		return

	print("  ✓ 全卸下執行完畢，所有槽位: %s" % str(_gs.weapon_loadout))
	if _gs.weapon_loadout[0] != "" or _gs.weapon_loadout[1] != "" or _gs.weapon_loadout[2] != "":
		_fail("全卸下後武器欄位未清空: %s" % str(_gs.weapon_loadout))

	# 驗證空手防呆切換
	if str(_gs.weapon_name) != "空手":
		_fail("全卸下後 weapon_name 未切換為『空手』: %s" % str(_gs.weapon_name))
	else:
		print("  ✓ weapon_name 正確防呆切換為『空手』")

	if int(_gs.weapon_atk) != 0:
		_fail("全卸下後 weapon_atk 未歸零: %d" % _gs.weapon_atk)
	else:
		print("  ✓ weapon_atk 正確歸零")

	if str(_gs.path_style) != "fist":
		_fail("全卸下後 path_style 未切換為拳套防呆 'fist': %s" % str(_gs.path_style))
	else:
		print("  ✓ path_style 正確切換為拳套防呆 'fist'")

	if str(_gs.equip_slots.get("weapon", "")) != "":
		_fail("equip_slots['weapon'] 未清空: %s" % str(_gs.equip_slots.get("weapon", "")))
	else:
		print("  ✓ equip_slots['weapon'] 正確清空")

	# 再次點擊一鍵卸下，驗證全空狀態防呆
	var res_empty: Dictionary = _lobby.unequip_all_weapons(true)
	if bool(res_empty.get("changed", true)):
		_fail("全空狀態下一鍵卸下仍觸發變更")
	else:
		print("  ✓ 全空狀態下一鍵卸下回傳 changed=false")

	var toast_node: Label = _lobby._current_toast
	if toast_node != null and is_instance_valid(toast_node):
		print("  ✓ 全空狀態下飄字提示正常: '%s'" % toast_node.text)


func _test_locales_and_no_emoji() -> void:
	print("\n--- 5. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換與零 Emoji ---")
	var btn: Button = _lobby.find_child("BtnWeaponUnequipAll", true, false) as Button
	if btn == null:
		_fail("找不到 BtnWeaponUnequipAll 按鈕")
		return

	var expected_btn_text: Dictionary = {
		"zh_TW": "一鍵卸下",
		"zh_CN": "一键卸下",
		"en": "Quick Unsocket",
		"ja": "一括解除",
		"ko": "일괄 해제",
		"es": "Desengarzar Todo"
	}

	var expected_success_toast: Dictionary = {
		"zh_TW": "已將副武器卸下歸還背包！",
		"zh_CN": "已将副武器卸下归还背包！",
		"en": "Secondary weapons unequipped and returned to bag!",
		"ja": "副武器を外してバッグに戻しました！",
		"ko": "보조 무기를 해제하여 가방에 보관했습니다!",
		"es": "¡Armas secundarias desequipadas y devueltas a la bolsa!"
	}

	var expected_empty_toast: Dictionary = {
		"zh_TW": "當前無可卸下的武器！",
		"zh_CN": "当前无可卸下的武器！",
		"en": "No weapons to unequip currently!",
		"ja": "現在外せる武器がありません！",
		"ko": "현재 해제할 수 있는 무기가 없습니다!",
		"es": "¡No hay armas para desequipar actualmente!"
	}

	for code in LOCALES:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", code)

		_lobby._on_locale_changed(code)

		var actual_btn := btn.text
		var exp_btn: String = expected_btn_text[code]
		if actual_btn != exp_btn:
			_fail("[%s] 按鈕文字翻譯不符: 期望 '%s'，實際 '%s'" % [code, exp_btn, actual_btn])
		else:
			print("  ✓ [%s] 按鈕文字符合: '%s'" % [code, actual_btn])

		if _has_emoji(actual_btn):
			_fail("[%s] 按鈕文字含有違規 Emoji: %s" % [code, actual_btn])

		var actual_succ := MobileLobby._t("已將副武器卸下歸還背包！")
		var exp_succ: String = expected_success_toast[code]
		if actual_succ != exp_succ:
			_fail("[%s] 成功飄字翻譯不符: 期望 '%s'，實際 '%s'" % [code, exp_succ, actual_succ])
		else:
			print("  ✓ [%s] 成功飄字符合: '%s'" % [code, actual_succ])

		var actual_emp := MobileLobby._t("當前無可卸下的武器！")
		var exp_emp: String = expected_empty_toast[code]
		if actual_emp != exp_emp:
			_fail("[%s] 防呆飄字翻譯不符: 期望 '%s'，實際 '%s'" % [code, exp_emp, actual_emp])
		else:
			print("  ✓ [%s] 防呆飄字符合: '%s'" % [code, actual_emp])

		if code in ["en", "es"] and (_has_cjk(actual_succ) or _has_cjk(actual_emp)):
			_fail("[%s] 英文/西文語系殘留 CJK 中文字元" % code)

	# 切回繁中預設
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")
	_lobby._on_locale_changed("zh_TW")


func _finish_test() -> void:
	print("\n=======================================================")
	if _ok:
		print("TEST_LOBBY_WEAPON_UNEQUIP_ALL_OK")
		quit(0)
	else:
		print("TEST_LOBBY_WEAPON_UNEQUIP_ALL_FAILED")
		quit(1)
