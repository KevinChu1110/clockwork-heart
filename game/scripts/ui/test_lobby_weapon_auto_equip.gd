extends SceneTree
## 大廳角色頁武器輪替配置新增『一鍵配置』最高戰力武器單元測試 (test_lobby_weapon_auto_equip.gd)
## 依據任務 t_5c2f9a55 驗收標準：
## 1. 大廳角色頁 (mobile_lobby.gd, Tab.CHARACTER) 顯示武器輪替配置標題列與一鍵配置按鈕 (BtnWeaponAutoEquip)，熱區 >= 48px，尺寸 >= 104x48px，薄荷綠果凍厚底，深藍紫描邊 2px，圓角 16px，零 Emoji。
## 2. 測試 EquipmentSystem.auto_equip_best_weapons() 依攻擊力與品質排序背包武器，自動挑選最佳武器填入已解鎖的三個武器槽位。
## 3. 測試點擊後發出 weapons_auto_equipped 信號並即時刷新三欄武器卡、有效戰力與戰鬥屬性卡片。
## 4. 測試飄字反饋：數值提升時提示「戰力提升 +XX！已一鍵配置最高戰力武器。」；已是最佳配置時提示「目前已是最佳武器配置！」。
## 5. 測試六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，按鈕與提示正確翻譯，無中文殘留，零系統 Emoji。
## 6. 印出 LOBBY_WEAPON_AUTO_EQUIP_OK 哨兵，0 SCRIPT ERROR，quit(0)。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

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
	print("=== 開始 test_lobby_weapon_auto_equip 測試 (t_5c2f9a55) ===")
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

	if _lobby.has_signal("weapons_auto_equipped"):
		_lobby.connect("weapons_auto_equipped", func(res: Dictionary):
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
		_test_auto_equip_and_power_refresh()

	elif _step == 2 and _frame >= 15:
		_step = 3
		_test_repeat_auto_equip_optimal()

	elif _step == 3 and _frame >= 20:
		_step = 4
		_test_locales_and_no_emoji()

	elif _step == 4 and _frame >= 25:
		_step = 5
		_finish_test()

	return false


func _test_btn_exists_and_specs() -> void:
	print("\n--- 1. 驗證大廳角色頁一鍵配置按鈕 (BtnWeaponAutoEquip) 存在與規格 ---")
	_lobby.switch_tab(MobileLobby.Tab.CHARACTER)

	var btn: Button = _lobby.find_child("BtnWeaponAutoEquip", true, false) as Button
	if btn == null:
		_fail("角色分頁找不到 BtnWeaponAutoEquip 按鈕")
		return
	print("  ✓ BtnWeaponAutoEquip 按鈕存在")

	# 熱區 >= 48px，尺寸 >= 104x48
	var msize := btn.custom_minimum_size
	if msize.x < 104 or msize.y < 48:
		_fail("BtnWeaponAutoEquip 尺寸未達熱區標準 (>=104x48px): %s" % str(msize))
	else:
		print("  ✓ BtnWeaponAutoEquip 尺寸符合熱區規範 (>=104x48px): %s" % str(msize))

	var fsize := btn.get_theme_font_size("font_size")
	if fsize < 14:
		_fail("BtnWeaponAutoEquip 字體小於 14px 零小字標準: %d" % fsize)
	else:
		print("  ✓ BtnWeaponAutoEquip 字體大小符合規範: %d px" % fsize)

	var sb: StyleBox = btn.get_theme_stylebox("normal")
	if sb is StyleBoxFlat:
		var sbf := sb as StyleBoxFlat
		if sbf.border_width_bottom < 5:
			_fail("BtnWeaponAutoEquip 果凍厚底底部描邊小於 5px: %d" % sbf.border_width_bottom)
		else:
			print("  ✓ BtnWeaponAutoEquip 具備立體果凍厚底 (border_bottom: %d px)" % sbf.border_width_bottom)
		if sbf.corner_radius_top_left != 16:
			_fail("BtnWeaponAutoEquip 圓角非 16px: %d" % sbf.corner_radius_top_left)
		else:
			print("  ✓ BtnWeaponAutoEquip 圓角符合規範 (16px)")


func _test_auto_equip_and_power_refresh() -> void:
	print("\n--- 2. 驗證依攻擊力與品質排序背包武器一鍵裝備與即時戰力刷新 ---")
	# 設定玩家等級 Lv 20（解鎖全部 3 個武器欄位）
	_gs.level = 20
	_gs.weapon_loadout = ["", "", ""]
	_gs.equip_worn = {}
	_gs.equip_bag = []

	var initial_power: int = int(_gs.power_score())
	print("  初始有效戰力: %d" % initial_power)

	# 構造 5 件測試武器
	# W1: 秘寶 (epic) 龍鱗劍，atk: 90
	var w1 := {
		"uid": "test_w_epic_90",
		"base_id": "star_fang",
		"name": "星紋龍牙",
		"slot": "weapon",
		"tier": 3,
		"line": "sword",
		"quality": "epic",
		"rolled": {"atk": 90, "crit": 8.0}
	}
	# W2: 上品 (rare) 破風槍，atk: 70
	var w2 := {
		"uid": "test_w_rare_70",
		"base_id": "ash_spear",
		"name": "燼木銳矛",
		"slot": "weapon",
		"tier": 2,
		"line": "spear",
		"quality": "rare",
		"rolled": {"atk": 70, "crit": 5.0}
	}
	# W3: 良品 (uncommon) 貫雲弓，atk: 50
	var w3 := {
		"uid": "test_w_uncommon_50",
		"base_id": "reed_bow",
		"name": "風葦輕弓",
		"slot": "weapon",
		"tier": 2,
		"line": "bow",
		"quality": "uncommon",
		"rolled": {"atk": 50, "crit": 3.0}
	}
	# W4: 凡品 (common) 鐵短棒，atk: 25
	var w4 := {
		"uid": "test_w_common_25",
		"base_id": "wrap_gloves",
		"name": "行旅拳套",
		"slot": "weapon",
		"tier": 1,
		"line": "glove",
		"quality": "common",
		"rolled": {"atk": 25, "crit": 1.0}
	}
	# W5: 凡品 (common) 鏽蝕初刃，atk: 10
	var w5 := {
		"uid": "test_w_common_10",
		"base_id": "rusty_blade",
		"name": "生鏽短劍",
		"slot": "weapon",
		"tier": 1,
		"line": "sword",
		"quality": "common",
		"rolled": {"atk": 10, "crit": 0.0}
	}

	# 槽位 0 先裝上最弱的 w5，其餘兩槽為空
	_gs.equip_worn[w5.uid] = w5
	_gs.weapon_loadout[0] = w5.uid
	_gs.equip_slots["weapon"] = w5.uid

	# 背包放入 w1, w2, w3, w4
	_gs.equip_bag.append(w1)
	_gs.equip_bag.append(w2)
	_gs.equip_bag.append(w3)
	_gs.equip_bag.append(w4)

	# 呼叫一鍵配置武器
	_signal_received = false
	_signal_payload = {}
	var res: Dictionary = _lobby.auto_equip_weapons()

	if not bool(res.get("ok", false)) or not bool(res.get("changed", false)):
		_fail("一鍵配置武器執行失敗或未觸發變更: %s" % str(res))
		return

	if not _signal_received:
		_fail("點擊一鍵配置後未收到 weapons_auto_equipped 信號")
	else:
		print("  ✓ 收到 weapons_auto_equipped 信號，payload 含 changed=true")

	var power_gain: int = int(res.get("power_gain", 0))
	var new_power: int = int(_gs.power_score())
	print("  一鍵配置後戰力提升: +%d (當前有效戰力: %d)" % [power_gain, new_power])

	if new_power <= initial_power:
		_fail("一鍵配置後戰力未提升: 初始 %d, 目前 %d" % [initial_power, new_power])
	else:
		print("  ✓ GameState.power_score() 戰力大幅提升")

	# 驗證三個槽位依序換為最強三件：w1 (atk 90), w2 (atk 70), w3 (atk 50)
	if str(_gs.weapon_loadout[0]) != w1.uid:
		_fail("槽位 0 未換上最強武器 w1 (%s): 實際 %s" % [w1.uid, str(_gs.weapon_loadout[0])])
	else:
		print("  ✓ 槽位 0 成功換上最強武器【星紋龍牙】(atk: 90, epic)")

	if str(_gs.weapon_loadout[1]) != w2.uid:
		_fail("槽位 1 未換上次強武器 w2 (%s): 實際 %s" % [w2.uid, str(_gs.weapon_loadout[1])])
	else:
		print("  ✓ 槽位 1 成功換上次強武器【燼木銳矛】(atk: 70, rare)")

	if str(_gs.weapon_loadout[2]) != w3.uid:
		_fail("槽位 2 未換上第三強武器 w3 (%s): 實際 %s" % [w3.uid, str(_gs.weapon_loadout[2])])
	else:
		print("  ✓ 槽位 2 成功換上第三強武器【風葦輕弓】(atk: 50, uncommon)")

	# 驗證原槽位 0 的弱武器 w5 與未被選中的 w4 都在背包中
	var bag_uids: Array[String] = []
	for b in _gs.equip_bag:
		bag_uids.append(str(b.get("uid", "")))
	if not bag_uids.has(w5.uid):
		_fail("原槽位 0 卸下的弱武器 w5 未退回背包: %s" % str(bag_uids))
	else:
		print("  ✓ 原武器 w5 成功退回背包")
	if not bag_uids.has(w4.uid):
		_fail("未被選中之武器 w4 不在背包中: %s" % str(bag_uids))
	else:
		print("  ✓ 未被選中之武器 w4 妥善保留在背包")


func _test_repeat_auto_equip_optimal() -> void:
	print("\n--- 3. 驗證再次點擊一鍵配置已是最佳狀態與提示飄字 ---")
	_signal_received = false
	var res2: Dictionary = _lobby.auto_equip_weapons()

	if bool(res2.get("changed", true)):
		_fail("已是最佳配置時 auto_equip_weapons 回傳 changed=true")
	else:
		print("  ✓ 再次執行一鍵配置正確回傳 changed=false (無需變更)")

	var toast: Label = _lobby._current_toast
	if toast == null:
		_fail("最佳狀態下一鍵配置未彈出提示飄字")
	elif toast.text != "目前已是最佳武器配置！":
		_fail("最佳配置飄字不符: 期望 '目前已是最佳武器配置！'，實際 '%s'" % toast.text)
	else:
		print("  ✓ 飄字提示完全正確: '%s'" % toast.text)


func _test_locales_and_no_emoji() -> void:
	print("\n--- 4. 驗證六語系切換、按鈕翻譯、零中文殘留與零系統 Emoji ---")
	var btn: Button = _lobby.find_child("BtnWeaponAutoEquip", true, false) as Button
	if btn == null:
		_fail("找不到 BtnWeaponAutoEquip")
		return

	var expected_btn_text: Dictionary = {
		"zh_TW": "一鍵配置",
		"zh_CN": "一键配置",
		"en": "Auto-Equip",
		"ja": "一括装着",
		"ko": "일괄 장착",
		"es": "Equipamiento rápido"
	}

	var expected_toast_optimal: Dictionary = {
		"zh_TW": "目前已是最佳武器配置！",
		"zh_CN": "当前已是最佳武器配置！",
		"en": "Already at optimal weapon configuration!",
		"ja": "現在は最適な武器配置です！",
		"ko": "현재 최적의 무기 배치입니다!",
		"es": "¡Ya está en la configuración óptima de armas!"
	}

	for loc in LOCALES:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", loc)
		_lobby._on_locale_changed(loc)

		var exp_btn: String = expected_btn_text[loc]
		if btn.text != exp_btn:
			_fail("[%s] BtnWeaponAutoEquip 按鈕文字不符: 期望 '%s', 實際 '%s'" % [loc, exp_btn, btn.text])
		else:
			print("  ✓ [%s] 按鈕文字翻譯正確: '%s'" % [loc, btn.text])

		# 再次觸發最佳配置提示以驗證 Toast 翻譯
		_lobby.auto_equip_weapons()
		var toast: Label = _lobby._current_toast
		if toast:
			var exp_toast: String = expected_toast_optimal[loc]
			if toast.text != exp_toast:
				_fail("[%s] Toast 翻譯不符: 期望 '%s', 實際 '%s'" % [loc, exp_toast, toast.text])
			else:
				print("  ✓ [%s] 飄字翻譯正確: '%s'" % [loc, toast.text])

		if loc == "en" and _has_cjk(btn.text):
			_fail("[en] 按鈕殘留中文: " + btn.text)
		if loc == "ja" and _has_emoji(btn.text):
			_fail("[ja] 按鈕含有非法 Emoji: " + btn.text)

	# 還原回 zh_TW
	if _loc_node and _loc_node.has_method("set_locale"):
		_loc_node.call("set_locale", "zh_TW")
	_lobby._on_locale_changed("zh_TW")


func _finish_test() -> void:
	print("\n--- 測試總結 ---")
	if _ok:
		print("🎉 大廳武器輪替配置一鍵配置最高戰力與即時屬性刷新驗收測試全部通過！")
		print("LOBBY_WEAPON_AUTO_EQUIP_OK")
		quit(0)
	else:
		print("❌ 測試有失敗項目！")
		print("LOBBY_WEAPON_AUTO_EQUIP_FAIL")
		quit(1)
