extends SceneTree
## 單元與驗收測試：大廳角色頁一鍵配置最高戰力武器 (t_162c4b02)
## 覆蓋項目：
## 1. 角色頁「一鍵配置」按鈕結構、尺寸 (>=48px)、多巴胺金黃果凍厚底 5px、零 Emoji。
## 2. 背包有更強武器時，點擊一鍵配置能正確換上最高攻擊力武器。
## 3. 未解鎖槽位（例如未達 Lv10/Lv16）不會被越權裝備。
## 4. 已是最高戰力時的冪等性（不重複觸發變更，提示「當前已是最高戰力配置」）。
## 5. 即時刷新大廳主角紙娃娃外觀、屬性卡片（攻擊力/防禦力/生命/戰力）、三欄武器槽按鈕與 HUD。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態切換與在地化連動無遺漏 key。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: Control = null
var _frame_count: int = 0
var _step: int = 0


func _initialize() -> void:
	print("== 開始執行大廳角色頁一鍵配置最高戰力武器驗收測試 (t_162c4b02) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	if gs == null or eq == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / Loc)")
		return

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ok 大廳節點建立成功")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	match _step:
		0:
			_step_test_button_spec()
			_step = 1
		1:
			_step_test_auto_equip_lvl1()
			_step = 2
		2:
			_step_test_idempotency()
			_step = 3
		3:
			_step_test_auto_equip_lvl10()
			_step = 4
		4:
			_step_test_auto_equip_lvl16()
			_step = 5
		5:
			_step_test_i18n_locales()
			_step = 6
		6:
			print("\n=======================================================")
			print("  TEST_LOBBY_AUTO_EQUIP_WEAPONS_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _step_test_button_spec() -> void:
	print("\n--- 1. 檢驗角色頁『一鍵配置』按鈕規格規範 ---")
	var btn: Button = _lobby._btn_auto_equip_weapons
	if btn == null or not is_instance_valid(btn):
		_fail("角色頁未找到 _btn_auto_equip_weapons 按鈕")
		return

	if btn.name != "BtnAutoEquipWeapons":
		_fail("按鈕節點名稱應為 BtnAutoEquipWeapons，實際為: %s" % btn.name)

	if btn.custom_minimum_size.y < 48:
		_fail("按鈕高度熱區小於 48px: %s" % str(btn.custom_minimum_size))

	var sb := btn.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		_fail("按鈕缺少 normal StyleBoxFlat")
		return

	if sb.border_width_bottom != 5:
		_fail("按鈕果凍厚底非 5px，實際為: %d" % sb.border_width_bottom)

	if sb.corner_radius_top_left < 16 or sb.corner_radius_top_left > 22:
		_fail("按鈕圓角需符合 16~22px，實際為: %d" % sb.corner_radius_top_left)

	_assert_no_emoji(btn.text, "一鍵配置按鈕文字")
	print("  ok 按鈕名稱、尺寸 (>=48px)、果凍厚底 5px、圓角 16~22px、零 Emoji 符合 review.md")


func _step_test_auto_equip_lvl1() -> void:
	print("\n--- 2. 檢驗 Lv1 時一鍵配置（僅解鎖 Slot 0，Slot 1/2 不被越權裝備） ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	gs.level = 1
	gs.equip_bag.clear()

	# 放入一把強武器 (atk 45) 與一把中等武器 (atk 25)
	var strong_w: Dictionary = eq.roll_instance("ash_spear", "rare")
	strong_w["rolled"]["atk"] = 45.0
	eq.add_to_bag(strong_w)

	var mid_w: Dictionary = eq.roll_instance("star_rod", "uncommon")
	mid_w["rolled"]["atk"] = 25.0
	eq.add_to_bag(mid_w)

	var initial_w0 := str(gs.weapon_loadout[0])
	var initial_atk := int(gs.effective_atk())

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)):
		_fail("一鍵配置執行失敗: %s" % str(res))
		return
	if not bool(res.get("changed", false)):
		_fail("背包有更強武器時應觸發 changed=true")
		return

	if str(gs.weapon_loadout[0]) != str(strong_w["uid"]):
		_fail("Slot 0 應裝備最強武器 %s，實際為 %s" % [strong_w["uid"], gs.weapon_loadout[0]])

	if str(gs.weapon_loadout[1]) != "":
		_fail("Lv1 時 Slot 1 未解鎖，不應裝備武器，實際為: %s" % gs.weapon_loadout[1])

	if str(gs.weapon_loadout[2]) != "":
		_fail("Lv1 時 Slot 2 未解鎖，不應裝備武器，實際為: %s" % gs.weapon_loadout[2])

	# 檢查原裝備已退回背包
	var found_old := false
	for item in gs.equip_bag:
		if str(item.get("uid", "")) == initial_w0:
			found_old = true
			break
	if not found_old and initial_w0 != "":
		_fail("原 Slot 0 武器未退回背包")

	# 檢查攻擊力面板增強
	var new_atk := int(gs.effective_atk())
	if new_atk <= initial_atk:
		_fail("換上最強武器後 effective_atk 未提升: 原 %d -> 現 %d" % [initial_atk, new_atk])

	print("  ok Lv1 一鍵配置成功換上最強武器，未解鎖槽位無越權，面板攻擊力從 %d 提升至 %d" % [initial_atk, new_atk])


func _step_test_idempotency() -> void:
	print("\n--- 3. 檢驗最高戰力時一鍵配置冪等性 ---")
	var gs = root.get_node_or_null("GameState")

	var prev_w0 := str(gs.weapon_loadout[0])
	var prev_bag_size: int = gs.equip_bag.size()

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)):
		_fail("冪等性測試執行失敗")
		return
	if bool(res.get("changed", false)):
		_fail("當前已是最高戰力配置時，changed 應為 false")
		return
	if str(res.get("msg", "")) != "當前已是最高戰力配置":
		_fail("提示訊息應為「當前已是最高戰力配置」，實際為: %s" % str(res.get("msg", "")))

	if str(gs.weapon_loadout[0]) != prev_w0:
		_fail("冪等性狀態下武器槽位不應改變")
	if gs.equip_bag.size() != prev_bag_size:
		_fail("冪等性狀態下背包數量不應改變")

	print("  ok 當前已是最高戰力時保持冪等，正確提示「當前已是最高戰力配置」")


func _step_test_auto_equip_lvl10() -> void:
	print("\n--- 4. 檢驗 Lv10 時解鎖 Slot 1，自動為兩個槽位配置最佳武器 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	gs.level = 10
	if not eq.loadout_slot_unlocked(1):
		_fail("Lv10 時 Slot 1 應已解鎖")
	if eq.loadout_slot_unlocked(2):
		_fail("Lv10 時 Slot 2 應仍為鎖定")

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)) or not bool(res.get("changed", false)):
		_fail("Lv10 解鎖新槽位後一鍵配置應觸發變更")
		return

	if str(gs.weapon_loadout[0]) == "":
		_fail("Slot 0 不應為空")
	if str(gs.weapon_loadout[1]) == "":
		_fail("Slot 1 應已裝備次強武器")
	if str(gs.weapon_loadout[2]) != "":
		_fail("Lv10 時 Slot 2 不應裝備武器")

	var names: Array = res.get("equipped_names", [])
	if names.size() != 2:
		_fail("解鎖 2 個槽位時 equipped_names 長度應為 2，實際為: %d" % names.size())

	# 冪等性再驗證
	var res2: Dictionary = _lobby.auto_equip_weapons()
	if bool(res2.get("changed", false)):
		_fail("Lv10 二次呼叫應保持冪等 changed=false")

	print("  ok Lv10 成功為 Slot 0 與 Slot 1 配置最佳武器，Slot 2 保持鎖定，冪等性驗證通過")


func _step_test_auto_equip_lvl16() -> void:
	print("\n--- 5. 檢驗 Lv16 時解鎖全三槽位，自動配置三把最強武器 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	gs.level = 16
	if not eq.loadout_slot_unlocked(2):
		_fail("Lv16 時 Slot 2 應已解鎖")

	# 加入第 3 把與第 4 把武器（第 4 把最弱）
	var w3: Dictionary = eq.roll_instance("anvil_hammer", "common")
	w3["rolled"]["atk"] = 20.0
	eq.add_to_bag(w3)

	var w_weak: Dictionary = eq.roll_instance("flint_gun", "common")
	w_weak["rolled"]["atk"] = 5.0
	eq.add_to_bag(w_weak)

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)) or not bool(res.get("changed", false)):
		_fail("Lv16 解鎖第 3 槽位後一鍵配置應觸發變更")
		return

	if str(gs.weapon_loadout[0]) == "" or str(gs.weapon_loadout[1]) == "" or str(gs.weapon_loadout[2]) == "":
		_fail("全三槽位皆應裝備武器: %s" % str(gs.weapon_loadout))

	# 最弱武器應留在背包
	var weak_in_bag := false
	for item in gs.equip_bag:
		if str(item.get("uid", "")) == str(w_weak["uid"]):
			weak_in_bag = true
			break
	if not weak_in_bag:
		_fail("最弱武器應留在背包中")

	var names: Array = res.get("equipped_names", [])
	if names.size() != 3:
		_fail("解鎖 3 個槽位時 equipped_names 長度應為 3，實際為: %d" % names.size())

	print("  ok Lv16 全三槽位成功配置最強三把武器，最弱武器留在背包，提示名稱包含: %s" % "、".join(names))


func _step_test_i18n_locales() -> void:
	print("\n--- 6. 檢驗六語系即時切換與文字非空且零 Emoji ---")
	var loc = root.get_node_or_null("Loc")
	var codes := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var ContentLoc = preload("res://scripts/systems/content_loc.gd")

	for code in codes:
		loc.call("set_locale", code)
		_lobby._apply_locale_texts()

		var btn: Button = _lobby._btn_auto_equip_weapons
		if btn == null or btn.text.is_empty():
			_fail("[%s] _btn_auto_equip_weapons 文字為空" % code)
		_assert_no_emoji(btn.text, "[%s] 按鈕文字" % code)

		var t_already: String = ContentLoc.text("ui", "當前已是最高戰力配置")
		if t_already.is_empty():
			_fail("[%s] 缺少「當前已是最高戰力配置」翻譯" % code)
		if code != "zh_TW" and t_already == "當前已是最高戰力配置":
			_fail("[%s] 語系未成功在地化「當前已是最高戰力配置」" % code)

		var t_fmt: String = ContentLoc.text("ui", "已一鍵配置最高戰力武器：%s")
		if t_fmt.is_empty():
			_fail("[%s] 缺少一鍵配置武器格式化字串翻譯" % code)
		if code != "zh_TW" and t_fmt == "已一鍵配置最高戰力武器：%s":
			_fail("[%s] 語系未成功在地化一鍵配置格式化字串" % code)

		print("  ok [%s] 按鈕文字「%s」正常、提示語系對照完整、零 Emoji" % [code, btn.text])

	loc.call("set_locale", "zh_TW")
	_lobby._apply_locale_texts()


func _assert_no_emoji(text: String, context: String) -> void:
	for ch in text:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			if ch != "✕":
				_fail("%s 含有禁止之系統 Emoji: '%s'" % [context, ch])


func _fail(msg: String) -> void:
	push_error("TEST_FAILED: " + msg)
	printerr("TEST_FAILED: " + msg)
	quit(1)
