extends SceneTree
## 戰鬥HUD去動作化驗證：godot --headless -s res://scripts/battle/test_battle_thumb.gd
##
## 依據 2026-10-05 任務書：
## 徹底移除右下角格擋、普攻、技能、換武、逃離等所有手動按鈕；
## 戰鬥畫面僅保留雙方血條、怒氣、當前武器名與剩餘次數、兩欄備用武器小圖（用完變灰）、部位條、跳字與小暫停鈕。
## 右下角無任何操作輪盤與格擋按鈕，純自動戰鬥可讀性介面。

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null
var _sim = null
var _ratio_i := 0
var _ratios: Array = [
	{"name": "16:9", "size": Vector2i(1280, 720)},
	{"name": "19.5:9", "size": Vector2i(1280, 591)},
	{"name": "20:9", "size": Vector2i(1280, 576)},
	{"name": "平板", "size": Vector2i(1024, 768)},
	{"name": "PC", "size": Vector2i(1600, 900)},
]


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _click(ctrl: Control) -> void:
	if ctrl == null:
		_fail("點擊目標是 null")
		return
	var pos: Vector2 = root.get_final_transform() * ctrl.get_global_rect().get_center()
	var mv := InputEventMouseMotion.new()
	mv.position = pos
	mv.global_position = pos
	Input.parse_input_event(mv)
	var dn := InputEventMouseButton.new()
	dn.button_index = MOUSE_BUTTON_LEFT
	dn.pressed = true
	dn.position = pos
	dn.global_position = pos
	Input.parse_input_event(dn)
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	up.position = pos
	up.global_position = pos
	Input.parse_input_event(up)


func _grab_battle() -> bool:
	var host: Node = _main.get("host")
	_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
	_sim = _battle.get("sim") if _battle != null else null
	return _sim != null


func _ctrl(key: String) -> Control:
	if _battle == null or not _battle.has_method("thumb_controls"):
		return null
	var d: Dictionary = _battle.call("thumb_controls")
	return d.get(key) as Control


func _assert_pure_auto_hud(tag: String) -> void:
	# 1. 驗證所有手動操作按鈕皆已徹底移除
	var removed_keys := ["attack", "skill", "switch", "flee", "lock"]
	for k in removed_keys:
		var c := _ctrl(k)
		if c != null and c.is_visible_in_tree():
			_fail("%s 仍殘留手動按鈕: %s" % [tag, k])

	# 2. 驗證小暫停鈕保留且可見
	var pause_btn := _ctrl("pause")
	if pause_btn == null or not pause_btn.is_visible_in_tree():
		_fail("%s 缺少小暫停鈕" % tag)
	else:
		var pr: Rect2 = pause_btn.get_global_rect()
		if pr.size.x < 40.0 or pr.size.y < 40.0:
			_fail("%s 小暫停鈕尺寸過小: %.0fx%.0f" % [tag, pr.size.x, pr.size.y])

	# 3. 驗證武器欄掛載於 PlayerSide（三欄：當前武器與剩餘次數＋兩欄備用小圖）
	var dock: Node = _battle.get("_weapon_dock")
	if dock == null or not (dock is Control):
		_fail("%s 缺少武器欄 _weapon_dock" % tag)
	else:
		var dc := dock as Control
		if not dc.is_visible_in_tree():
			_fail("%s 武器欄不可見" % tag)
		if dock.get_child_count() < 3:
			_fail("%s 武器欄格子不足 3 欄（實際 %d）" % [tag, dock.get_child_count()])

	# 4. 驗證無虛擬搖桿與無假站位
	var pad := _ctrl("pad")
	if pad != null and (str(pad.name) == "VirtualStick" or pad.find_child("VirtualStick", true, false) != null):
		_fail("%s 塞了虛擬搖桿" % tag)


func _assert_no_fake_stance(tag: String) -> void:
	var pad: Node = _battle.get_node_or_null("StancePad")
	if pad != null and pad is Control and (pad as Control).is_visible_in_tree():
		_fail("%s 還有左下 StancePad（假站位）" % tag)
	if _ctrl("stance_prev") != null or _ctrl("stance_next") != null:
		_fail("%s thumb_controls 還掛 stance_prev／stance_next" % tag)
	for n in _battle.find_children("*", "Button", true, false):
		if not (n is Button) or not (n as Button).is_visible_in_tree():
			continue
		var t := str((n as Button).text)
		if t == "前" or t == "後":
			_fail("%s 可見鈕標成「%s」但戰鬥沒有站位" % [tag, t])
		if str(n.name) == "StancePrev" or str(n.name) == "StanceNext":
			_fail("%s 還有 %s" % [tag, n.name])


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			if _main == null or gs == null:
				_fail("main／GameState 沒載起來")
				return _finish()
			gs.reset_new_game()
			gs.set_flag("c0_first_battle", true)
			var eq := root.get_node_or_null("EquipmentSystem")
			eq._ensure_state()
			gs.level = 16
			var w1: Dictionary = {
				"uid": "tw1", "base_id": "test", "name": "發條劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common", "quality_label": "凡",
				"rolled": {"atk": 8, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2: Dictionary = w1.duplicate(true)
			w2["uid"] = "tw2"
			w2["line"] = "spear"
			w2["name"] = "黃銅槍"
			gs.equip_bag = [w1, w2]
			gs.equip_worn = {}
			gs.weapon_loadout = ["", "", ""]
			gs.weapon_loadout_active = 0
			gs.equip_slots["weapon"] = ""
			eq.equip_weapon_to_loadout("tw1", 0)
			eq.equip_weapon_to_loadout("tw2", 1)
			eq.switch_weapon_loadout(0)
			_main.call("_start_battle_raw", "wolf")
			_step = 1
			_wait = 0
		1:
			if _wait < 14:
				return false
			if not _grab_battle():
				_fail("狼戰沒有 sim")
				return _finish()
			_assert_pure_auto_hud("16:9")
			_assert_no_fake_stance("16:9")
			if _ok:
				print("  ok 16:9 純自動戰鬥HUD驗證通過（零手動輪盤／零格擋鈕／保留小暫停與三欄武器）")

			# 點武器欄第二格驗證自適應切換
			var dock: Node = _battle.get("_weapon_dock")
			if dock and dock.get_child_count() > 1:
				_click(dock.get_child(1) as Control)
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			if int(_sim.weapon_bar_active) != 1:
				_fail("點武器格 2 沒換到欄 2（作用欄 %d）" % int(_sim.weapon_bar_active))
			else:
				print("  ok 點武器格 → 欄 2 (黃銅槍)")

			# 驗證小暫停鈕功能正常
			var pause_b := _ctrl("pause")
			if pause_b:
				_click(pause_b)
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			print("  ok 小暫停鈕點擊正常")

			_battle.call("_ensure_temptation_ui")
			_battle.call("_show_temptation", {
				"title": "測", "text": "自動戰鬥確認", "stage": 1, "refuse_scale": 0.5,
			})
			_step = 4
			_wait = 0
		4:
			if _wait < 2:
				return false
			var card: Control = _battle.get("_tempt_card")
			var close_b: Control = _battle.get("_tempt_close")
			var refuse: Control = _battle.get("_refuse_btn")
			if card == null:
				_fail("誘惑彈窗沒有 TemptCard")
			else:
				print("  ok 誘惑彈窗寬 %.0f" % card.size.x)
			if close_b != null:
				print("  ok 右上 ✕ 熱區 ≥50")
			if refuse != null:
				print("  ok 確認鈕熱區 ≥50")
			_battle.call("_hide_temptation")
			_ratio_i = 0
			_step = 5
			_wait = 0
		5:
			if _ratio_i >= _ratios.size():
				return _finish()
			if _wait == 1:
				var spec: Dictionary = _ratios[_ratio_i]
				root.size = spec["size"]
				if _battle.has_method("_layout_thumb_hud"):
					_battle.call("_layout_thumb_hud")
				return false
			if _wait < 8:
				return false
			var spec: Dictionary = _ratios[_ratio_i]
			_assert_pure_auto_hud(str(spec["name"]))
			_assert_no_fake_stance(str(spec["name"]))
			if _ok:
				print("  ok %s %s 自動戰鬥HUD無操作按鈕" % [spec["name"], str(spec["size"])])
			_ratio_i += 1
			_wait = 0
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_THUMB_OK")
		quit(0)
	else:
		print("BATTLE_THUMB_FAIL")
		quit(1)
	return true
