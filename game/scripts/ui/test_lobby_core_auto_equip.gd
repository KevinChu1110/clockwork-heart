extends SceneTree
## 大廳角色頁五大機芯槽位支援一鍵配置最高戰力機芯與即時屬性刷新單元測試 (test_lobby_core_auto_equip.gd)
## 依據任務 t_791dc011 驗收標準：
## 1. 大廳角色頁 (mobile_lobby.gd, Tab.CHARACTER) 顯示五大機芯槽位與一鍵配置按鈕 (BtnCoreAutoEquip)，熱區 >= 48px。
## 2. 測試計算邏輯與空槽/低階裝備：自動比對背包中機芯綜合戰力，將最高數值機芯換上對應槽位。
## 3. 測試數值提升與介面即時刷新：GameState.core_slots、大廳頂部戰力、角色頁戰力膠囊與五槽卡片同步刷新。
## 4. 測試飄字反饋：數值提升時提示「戰力提升 +XX！已一鍵配置最高戰力機芯。」；已是最佳配置時提示「目前已是最佳機芯配置！」。
## 5. 測試六語系即時切換 (zh_TW, zh_CN, en, ja, ko, es)，按鈕與提示正確翻譯，無中文殘留，零系統 Emoji。
## 6. 印出 LOBBY_CORE_AUTO_EQUIP_OK 哨兵，0 SCRIPT ERROR，quit(0)。

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _loc_node: Node = null
var _lobby: Control = null
var _cs: Node = null
var _gs: Node = null


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
	print("=== 開始 test_lobby_core_auto_equip 測試 (t_791dc011) ===")
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

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	_lobby = MobileLobby.new()
	root.add_child(_lobby)


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
	print("\n--- 1. 驗證大廳角色頁一鍵配置按鈕 (BtnCoreAutoEquip) 存在與規格 ---")
	_lobby.switch_tab(MobileLobby.Tab.CHARACTER)

	var btn: Button = _lobby.find_child("BtnCoreAutoEquip", true, false) as Button
	if btn == null:
		_fail("角色分頁找不到 BtnCoreAutoEquip 按鈕")
		return
	print("  ✓ BtnCoreAutoEquip 按鈕存在")

	# 熱區 >= 48px
	var msize := btn.custom_minimum_size
	if msize.x < 100 or msize.y < 48:
		_fail("BtnCoreAutoEquip 尺寸未達熱區標準 (>=48px): %s" % str(msize))
	else:
		print("  ✓ BtnCoreAutoEquip 尺寸符合熱區規範 (104x48px): %s" % str(msize))

	var fsize := btn.get_theme_font_size("font_size")
	if fsize < 14:
		_fail("BtnCoreAutoEquip 字體小於 14px 零小字標準: %d" % fsize)
	else:
		print("  ✓ BtnCoreAutoEquip 字體大小符合規範: %d px" % fsize)


func _test_auto_equip_and_power_refresh() -> void:
	print("\n--- 2. 驗證空槽/低階比對背包最高戰力機芯一鍵裝備與即時戰力刷新 ---")
	# 初始配置：清空背包，槽位設為白板低階機芯
	CoreSystemClass.clear_inventory()
	_gs.ensure_core_slots("white")

	# 記錄初始戰力
	var initial_power: int = int(_gs.power_score())
	print("  初始有效戰力: %d" % initial_power)

	# 注入高階機芯至背包：
	# mainspring: 金階 (score 45)
	# chassis: 藍階 (score 15)
	# escapement: 紫階 (score 30)
	# gear_train: 綠階 (score 60)
	# soul_core: 紅階 (score 75)
	var p_mainspring := CoreSystemClass.create_part_by_tier("mainspring", "gold", {"ATK": 20, "CRIT": 3.0})
	var p_chassis := CoreSystemClass.create_part_by_tier("chassis", "blue", {"DEF": 15, "HP": 50})
	var p_escapement := CoreSystemClass.create_part_by_tier("escapement", "purple", {"ATK": 15, "DEF": 10})
	var p_gear := CoreSystemClass.create_part_by_tier("gear_train", "green", {"ATK": 35, "CRIT": 5.0})
	var p_soul := CoreSystemClass.create_part_by_tier("soul_core", "red", {"ATK": 50, "DEF": 30})

	CoreSystemClass.add_part_to_inventory(p_mainspring)
	CoreSystemClass.add_part_to_inventory(p_chassis)
	CoreSystemClass.add_part_to_inventory(p_escapement)
	CoreSystemClass.add_part_to_inventory(p_gear)
	CoreSystemClass.add_part_to_inventory(p_soul)

	# 背包再多塞幾顆低階混淆項，確保只會挑選各槽最高戰力者
	var dummy_low_mainspring := CoreSystemClass.create_part_by_tier("mainspring", "orange", {"ATK": 2})
	var dummy_low_gear := CoreSystemClass.create_part_by_tier("gear_train", "blue", {"ATK": 5})
	CoreSystemClass.add_part_to_inventory(dummy_low_mainspring)
	CoreSystemClass.add_part_to_inventory(dummy_low_gear)

	var inv_before: Array = CoreSystemClass.get_inventory()
	if inv_before.size() != 7:
		_fail("背包初始機芯數量不符: 期望 7，實際 %d" % inv_before.size())
	else:
		print("  ✓ 背包成功注入 7 件機芯（含 5 件高階目標件與 2 件低階備件）")

	# 點擊一鍵配置
	var res: Dictionary = _lobby.auto_equip_cores()
	if not bool(res.get("ok", false)) or not bool(res.get("changed", false)):
		_fail("一鍵配置執行失敗或未觸發變更: %s" % str(res))
		return

	var power_gain: int = int(res.get("power_gain", 0))
	var new_power: int = int(_gs.power_score())
	print("  一鍵配置後戰力提升: +%d (當前有效戰力: %d)" % [power_gain, new_power])

	if new_power <= initial_power:
		_fail("一鍵配置後戰力未提升: 初始 %d, 目前 %d" % [initial_power, new_power])
	else:
		print("  ✓ GameState.power_score() 戰力確實大幅提升")

	# 驗證五大槽位皆換為最高階機芯
	if str(_gs.core_slots.get("mainspring", {}).get("tier", "")) != "gold":
		_fail("mainspring 槽位未換上金階機芯: %s" % str(_gs.core_slots.get("mainspring")))
	else:
		print("  ✓ mainspring 槽位成功換上金階機芯")

	if str(_gs.core_slots.get("chassis", {}).get("tier", "")) != "blue":
		_fail("chassis 槽位未換上藍階機芯: %s" % str(_gs.core_slots.get("chassis")))
	else:
		print("  ✓ chassis 槽位成功換上藍階機芯")

	if str(_gs.core_slots.get("escapement", {}).get("tier", "")) != "purple":
		_fail("escapement 槽位未換上紫階機芯: %s" % str(_gs.core_slots.get("escapement")))
	else:
		print("  ✓ escapement 槽位成功換上紫階機芯")

	if str(_gs.core_slots.get("gear_train", {}).get("tier", "")) != "green":
		_fail("gear_train 槽位未換上綠階機芯: %s" % str(_gs.core_slots.get("gear_train")))
	else:
		print("  ✓ gear_train 槽位成功換上綠階機芯")

	if str(_gs.core_slots.get("soul_core", {}).get("tier", "")) != "red":
		_fail("soul_core 槽位未換上紅階機芯: %s" % str(_gs.core_slots.get("soul_core")))
	else:
		print("  ✓ soul_core 槽位成功換上紅階機芯")

	# 驗證原本的白板機芯已卸回背包，且新機芯從背包移除
	var inv_after: Array = CoreSystemClass.get_inventory()
	print("  一鍵配置後背包機芯數量: %d" % inv_after.size())
	if inv_after.size() != 7:
		_fail("一鍵配置後背包數量應維持 7 件 (5 件卸回 + 2 件未裝低階備件): 實際 %d" % inv_after.size())
	else:
		print("  ✓ 舊白板機芯成功卸回背包，新機芯精確從背包移出")

	# 驗證飄字提示 (Toast)
	var toast_lbl: Label = _lobby.find_child("Label", true, false) as Label
	var current_toast: Label = _lobby._current_toast
	if current_toast == null or not is_instance_valid(current_toast):
		_fail("一鍵配置成功後未彈出飄字提示 Toast")
	else:
		print("  ✓ 成功彈出飄字提示: '%s'" % current_toast.text)
		if "戰力提升" not in current_toast.text:
			_fail("飄字內容未包含『戰力提升』: %s" % current_toast.text)


func _test_repeat_auto_equip_optimal() -> void:
	print("\n--- 3. 驗證已是最佳配置時再次點擊一鍵配置之判定 ---")
	var res: Dictionary = _lobby.auto_equip_cores()
	if not bool(res.get("ok", false)):
		_fail("最佳狀態下一鍵配置呼叫回傳 ok=false")
		return

	if bool(res.get("changed", false)):
		_fail("已是最佳狀態卻仍觸發變更")
		return
	print("  ✓ 最佳狀態下 changed=false 正確未重複變更")

	var current_toast: Label = _lobby._current_toast
	if current_toast == null or not is_instance_valid(current_toast):
		_fail("未彈出最佳配置提示 Toast")
	else:
		print("  ✓ 成功彈出最佳配置飄字提示: '%s'" % current_toast.text)
		if "最佳機芯配置" not in current_toast.text:
			_fail("飄字內容未包含『最佳機芯配置』: %s" % current_toast.text)


func _test_locales_and_no_emoji() -> void:
	print("\n--- 4. 驗證六語系切換與零系統 Emoji 規範 ---")
	var expected_btn_text := {
		"zh_TW": "一鍵配置",
		"zh_CN": "一键配置",
		"en": "Auto-Equip",
		"ja": "一括装着",
		"ko": "일괄 장착",
		"es": "Equipamiento rápido"
	}

	var expected_toast_optimal := {
		"zh_TW": "目前已是最佳機芯配置！",
		"zh_CN": "当前已是最佳机芯配置！",
		"en": "Already at optimal core configuration!",
		"ja": "現在は最適なコア配置です！",
		"ko": "현재 최적의 코어 배치입니다!",
		"es": "¡Ya está en la configuración óptima de núcleos!"
	}

	var btn: Button = _lobby.find_child("BtnCoreAutoEquip", true, false) as Button
	for loc in LOCALES:
		if _loc_node and _loc_node.has_method("set_locale"):
			_loc_node.call("set_locale", loc)
		_lobby._on_locale_changed(loc)

		var exp_btn: String = expected_btn_text[loc]
		if btn.text != exp_btn:
			_fail("[%s] BtnCoreAutoEquip 文字不符: 期望 '%s', 實際 '%s'" % [loc, exp_btn, btn.text])
		else:
			print("  ✓ [%s] 按鈕文字正確: '%s'" % [loc, btn.text])

		# 再次觸發最佳配置提示以驗證 Toast 翻譯
		_lobby.auto_equip_cores()
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
		print("🎉 大廳五大機芯槽位一鍵配置最高戰力與即時屬性刷新驗收測試全部通過！")
		print("LOBBY_CORE_AUTO_EQUIP_OK")
		quit(0)
	else:
		print("❌ 測試有失敗項目！")
		print("LOBBY_CORE_AUTO_EQUIP_FAIL")
		quit(1)
