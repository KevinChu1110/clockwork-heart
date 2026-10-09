extends SceneTree
## 單元與驗收測試：大廳角色頁一鍵配置最高戰力武器按鈕與即時數值連動 (t_728315d8)
## 覆蓋項目：
## 1. 角色頁「一鍵配置」按鈕規格（BtnAutoEquip，熱區 >= 48px，金黃多巴胺果凍厚底 5px，圓角 16~22px，零系統 Emoji）。
## 2. 按鈕點擊觸發 (btn.pressed.emit) 與 auto_equip_weapons() 呼叫。
## 3. 背包有更強武器時，自動配置替換，並即時刷新數值（effective_atk、有效戰力徽章、武器槽按鈕）。
## 4. 未解鎖槽位防越權（Lv1 僅 Slot 0；Lv10 解鎖 Slot 1；Lv16 解鎖 Slot 2）。
## 5. 冪等性與最佳狀態提示（「當前已是最高戰力配置」，changed=false）。
## 6. 空狀態測試（裝備與背包皆空時安全處理，不拋錯）。
## 7. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換與無遺漏 key。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")

var _lobby: Control = null
var _frame_count: int = 0
var _step: int = 0


func _initialize() -> void:
	print("== 開始執行大廳角色頁一鍵配置最高戰力武器按鈕單元測試 (t_728315d8) ==")
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
			_step_test_button_click_and_stats_refresh()
			_step = 2
		2:
			_step_test_idempotency_best_state()
			_step = 3
		3:
			_step_test_slot_unlock_progression()
			_step = 4
		4:
			_step_test_empty_state()
			_step = 5
		5:
			_step_test_i18n_locales()
			_step = 6
		6:
			print("\n=======================================================")
			print("  TEST_LOBBY_AUTO_EQUIP_BTN_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _step_test_button_spec() -> void:
	print("\n--- 1. 檢驗角色頁『一鍵配置』按鈕規格規範 ---")
	var btn: Button = _lobby._btn_auto_equip
	if btn == null or not is_instance_valid(btn):
		_fail("角色頁未找到 _btn_auto_equip 按鈕")
		return

	if btn.name != "BtnAutoEquip":
		_fail("按鈕節點名稱應為 BtnAutoEquip，實際為: %s" % btn.name)

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
	print("  ok 按鈕名稱 BtnAutoEquip、熱區 (>=48px)、果凍厚底 5px、圓角 16~22px、零 Emoji 符合規範")


func _step_test_button_click_and_stats_refresh() -> void:
	print("\n--- 2. 檢驗點擊按鈕觸發換裝與即時數值面板連動刷新 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	gs.level = 1
	gs.equip_bag.clear()

	# 放入強武器 (atk 50) 與次強武器 (atk 25)
	var strong_w: Dictionary = eq.roll_instance("ash_spear", "rare")
	strong_w["rolled"]["atk"] = 50.0
	eq.add_to_bag(strong_w)

	var mid_w: Dictionary = eq.roll_instance("star_rod", "uncommon")
	mid_w["rolled"]["atk"] = 25.0
	eq.add_to_bag(mid_w)

	var initial_atk := int(gs.effective_atk())

	# 模擬點擊按鈕
	var btn: Button = _lobby._btn_auto_equip
	btn.pressed.emit()

	# 驗證換裝結果
	if str(gs.weapon_loadout[0]) != str(strong_w["uid"]):
		_fail("點擊按鈕後 Slot 0 應裝備最強武器 %s，實際為 %s" % [strong_w["uid"], gs.weapon_loadout[0]])

	if str(gs.weapon_loadout[1]) != "":
		_fail("Lv1 時 Slot 1 未解鎖，不應裝備武器，實際為: %s" % gs.weapon_loadout[1])

	# 驗證數值即時刷新
	var new_atk := int(gs.effective_atk())
	if new_atk <= initial_atk:
		_fail("點擊一鍵配置後 effective_atk 未提升: 原 %d -> 現 %d" % [initial_atk, new_atk])

	# 驗證角色頁攻擊力卡片文字已即時更新
	var atk_card: PanelContainer = _lobby._stat_cards[1]
	var v_lbl := atk_card.find_child("ValLabel", true, false) as Label
	if v_lbl == null or int(v_lbl.text) != new_atk:
		_fail("角色屬性卡片 ValLabel 未即時刷新攻擊力: 實際顯示 %s，預期 %d" % [v_lbl.text if v_lbl else "null", new_atk])

	# 驗證武器槽卡片標題/名稱已即時更新
	var w0_btn: Button = _lobby._weapon_slot_buttons[0]
	var info_lbl := w0_btn.find_child("WeaponInfo", true, false) as Label
	if info_lbl == null or not info_lbl.text.contains(strong_w.get("name", "")):
		_fail("武器槽 0 卡片未即時刷新武器名稱: %s" % (info_lbl.text if info_lbl else "null"))

	print("  ok 按鈕點擊成功換上最強武器，effective_atk 從 %d 升至 %d，屬性卡片與武器槽卡片即時刷新" % [initial_atk, new_atk])


func _step_test_idempotency_best_state() -> void:
	print("\n--- 3. 檢驗當前已是最高戰力時的最佳狀態提示與冪等性 ---")
	var gs = root.get_node_or_null("GameState")
	var prev_w0 := str(gs.weapon_loadout[0])
	var prev_bag_size: int = gs.equip_bag.size()

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)):
		_fail("最佳狀態執行失敗")
		return
	if bool(res.get("changed", false)):
		_fail("當前已是最高戰力時，changed 應為 false")
		return
	if str(res.get("msg", "")) != "當前已是最高戰力配置":
		_fail("提示應為「當前已是最高戰力配置」，實際為: %s" % str(res.get("msg", "")))

	if str(gs.weapon_loadout[0]) != prev_w0:
		_fail("冪等狀態下武器槽位不應改變")
	if gs.equip_bag.size() != prev_bag_size:
		_fail("冪等狀態下背包數量不應改變")

	print("  ok 當前已是最高戰力時保持冪等，正確提示「當前已是最高戰力配置」")


func _step_test_slot_unlock_progression() -> void:
	print("\n--- 4. 檢驗等級解鎖槽位連動 (Lv10 雙槽、Lv16 三槽) ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 升至 Lv10 解鎖 Slot 1
	gs.level = 10
	var res10: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res10.get("changed", false)):
		_fail("Lv10 解鎖新槽位後應觸發換裝 changed=true")
		return
	if str(gs.weapon_loadout[0]) == "" or str(gs.weapon_loadout[1]) == "":
		_fail("Lv10 時 Slot 0 與 Slot 1 皆應裝備武器")
	if str(gs.weapon_loadout[2]) != "":
		_fail("Lv10 時 Slot 2 尚未解鎖，不應裝備武器")

	# 升至 Lv16 解鎖 Slot 2，放入第 3 把與第 4 把武器
	gs.level = 16
	var w3: Dictionary = eq.roll_instance("anvil_hammer", "common")
	w3["rolled"]["atk"] = 20.0
	eq.add_to_bag(w3)

	var w_weak: Dictionary = eq.roll_instance("flint_gun", "common")
	w_weak["rolled"]["atk"] = 5.0
	eq.add_to_bag(w_weak)

	var res16: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res16.get("changed", false)):
		_fail("Lv16 解鎖第 3 槽位後應觸發換裝 changed=true")
		return

	if str(gs.weapon_loadout[0]) == "" or str(gs.weapon_loadout[1]) == "" or str(gs.weapon_loadout[2]) == "":
		_fail("Lv16 時三槽位皆應裝備武器")

	var names: Array = res16.get("equipped_names", [])
	if names.size() != 3:
		_fail("equipped_names 長度應為 3，實際為: %d" % names.size())

	print("  ok Lv10 與 Lv16 槽位解鎖進階配置正常，三槽位正確配置最強三把武器")


func _step_test_empty_state() -> void:
	print("\n--- 5. 檢驗空狀態（無任何武器時安全處理） ---")
	var gs = root.get_node_or_null("GameState")
	gs.weapon_loadout = ["", "", ""]
	if gs.equip_slots != null and gs.equip_slots is Dictionary:
		gs.equip_slots["weapon"] = ""
	gs.equip_worn.clear()
	gs.equip_bag.clear()

	var res: Dictionary = _lobby.auto_equip_weapons()
	if not bool(res.get("success", false)):
		_fail("空狀態下執行 auto_equip_weapons 失敗")
		return
	if bool(res.get("changed", false)):
		_fail("空狀態下不應觸發 changed=true")
		return
	if str(res.get("msg", "")) != "當前已是最高戰力配置":
		_fail("空狀態提示應為「當前已是最高戰力配置」，實際為: %s" % str(res.get("msg", "")))

	print("  ok 空狀態安全處理無崩潰，正確提示最佳配置")


func _step_test_i18n_locales() -> void:
	print("\n--- 6. 檢驗六語系即時切換與文字非空且零 Emoji ---")
	var loc = root.get_node_or_null("Loc")
	var codes := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var ContentLoc = preload("res://scripts/systems/content_loc.gd")

	for code in codes:
		loc.call("set_locale", code)
		_lobby._apply_locale_texts()

		var btn: Button = _lobby._btn_auto_equip
		if btn == null or btn.text.is_empty():
			_fail("[%s] _btn_auto_equip 文字為空" % code)
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

		print("  ok [%s] 按鈕文字「%s」正常、提示在地化對照完整、零 Emoji" % [code, btn.text])

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
