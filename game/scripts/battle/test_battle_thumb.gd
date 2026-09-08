extends SceneTree
## 右手拇指可打完一場：godot --headless -s res://scripts/battle/test_battle_thumb.gd
##
## 守：攻擊／技能／換武／鎖定／暫停／逃離都在右側、熱區 ≥50，
## 不是左上角、不是虛擬搖桿。16:9／19.5:9／20:9／平板／PC 都成立。
## 標籤＝行為：沒有站位 API 就不要左下「前／後」假站位鈕。

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


func _assert_right_thumb(tag: String) -> void:
	var vp: Vector2 = root.get_visible_rect().size
	if vp.x < 8.0:
		vp = Vector2(root.size)
	var need := ["attack", "skill", "switch", "pause", "flee", "lock"]
	for k in need:
		var c := _ctrl(k)
		if c == null or not c.is_visible_in_tree():
			_fail("%s 缺 %s 鈕" % [tag, k])
			continue
		var r: Rect2 = c.get_global_rect()
		if r.size.x + 0.01 < 50.0 or r.size.y + 0.01 < 50.0:
			_fail("%s %s 熱區 %.0fx%.0f < 50" % [tag, k, r.size.x, r.size.y])
		var cx := r.get_center().x
		var cy := r.get_center().y
		if cx < vp.x * 0.50:
			_fail("%s %s 中心 x=%.0f 不在右半（vp.x=%.0f）——單拇指搆不到" % [tag, k, cx, vp.x])
		if cx < 120.0 and cy < 120.0:
			_fail("%s %s 落在左上小角落" % [tag, k])
	var pad := _ctrl("pad")
	if pad == null:
		_fail("%s 沒有 ThumbPad" % tag)
	elif str(pad.name) == "VirtualStick" or pad.find_child("VirtualStick", true, false) != null:
		_fail("%s 塞了虛擬搖桿" % tag)
	var dock: Node = _battle.get("_weapon_dock")
	if dock is Control:
		for child in dock.get_children():
			if child is Control:
				var wr: Rect2 = (child as Control).get_global_rect()
				if wr.size.x + 0.01 < 50.0 or wr.size.y + 0.01 < 50.0:
					_fail("%s 武器格熱區 %.0fx%.0f < 50" % [tag, wr.size.x, wr.size.y])
				if wr.get_center().x < vp.x * 0.50:
					_fail("%s 武器格不在右半" % tag)


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
				"uid": "tw1", "base_id": "test", "name": "測劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common", "quality_label": "凡",
				"rolled": {"atk": 8, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2: Dictionary = w1.duplicate(true)
			w2["uid"] = "tw2"
			w2["line"] = "axe"
			w2["name"] = "測斧"
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
			_assert_right_thumb("16:9")
			_assert_no_fake_stance("16:9")
			if _ok:
				print("  ok 16:9 右側熱區 ≥50，無虛擬搖桿、無假站位")
			var p = _sim.get_unit("player")
			_click(_ctrl("switch"))
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			if int(_sim.weapon_bar_active) != 1:
				_fail("點右側換武沒換到欄 2（作用欄 %d）" % int(_sim.weapon_bar_active))
			else:
				print("  ok 點換武 → 欄 2")
			var p = _sim.get_unit("player")
			p.fury_active = false
			p.fury_timer = 0.0
			p.rage = 100.0
			_click(_ctrl("skill"))
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			var p = _sim.get_unit("player")
			if not bool(p.fury_active):
				_fail("點右側技能沒有進暴怒")
			else:
				print("  ok 點技能 → 暴怒")
			_click(_ctrl("attack"))
			_click(_ctrl("lock"))
			_step = 4
			_wait = 0
		4:
			if _wait < 2:
				return false
			var coach: Label = _battle.get("_coach") as Label
			if coach != null and coach.visible and "站位" in str(coach.text):
				_fail("狼戰點鎖定跳出「%s」——沒有站位就不要講站位" % coach.text)
			else:
				print("  ok 狼戰點鎖定不講站位")
			_battle.call("_ensure_temptation_ui")
			_battle.call("_show_temptation", {
				"title": "測", "text": "右手拇指確認", "stage": 1, "refuse_scale": 0.5,
			})
			_step = 5
			_wait = 0
		5:
			if _wait < 2:
				return false
			var card: Control = _battle.get("_tempt_card")
			var close_b: Control = _battle.get("_tempt_close")
			var refuse: Control = _battle.get("_refuse_btn")
			if card == null:
				_fail("誘惑彈窗沒有 TemptCard")
			else:
				var cw := card.size.x
				if cw < 740.0 or cw > 760.0:
					_fail("誘惑彈窗寬 %.0f，應 740–760" % cw)
				else:
					print("  ok 誘惑彈窗寬 %.0f" % cw)
			if close_b == null:
				_fail("誘惑彈窗沒有右上 ✕")
			else:
				var cr: Rect2 = close_b.get_global_rect()
				if cr.size.x + 0.01 < 50.0 or cr.size.y + 0.01 < 50.0:
					_fail("✕ 熱區 %.0fx%.0f < 50" % [cr.size.x, cr.size.y])
				if close_b.get_index() < (close_b.get_parent().get_child_count() - 1):
					## 最後一個 child＝右側
					pass
				var parent_w := (close_b.get_parent() as Control).size.x
				if close_b.position.x < parent_w * 0.5:
					_fail("✕ 不在彈窗右側")
				else:
					print("  ok 右上 ✕ 熱區 ≥50")
			if refuse == null or refuse.get_global_rect().size.y + 0.01 < 50.0:
				_fail("我拒絕 熱區 < 50")
			else:
				print("  ok 確認鈕熱區 ≥50（refuse_scale 0.5 仍 ≥50）")
			_battle.call("_hide_temptation")
			_ratio_i = 0
			_step = 6
			_wait = 0
		6:
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
			_assert_right_thumb(str(spec["name"]))
			_assert_no_fake_stance(str(spec["name"]))
			if _ok:
				print("  ok %s %s 右側熱區" % [spec["name"], str(spec["size"])])
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
