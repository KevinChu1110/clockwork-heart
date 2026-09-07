extends SceneTree
## 輸入抽象層把關：godot --headless -s res://scripts/autoload/test_game_input.gd
##
## 守：七個語意動作有單一入口；戰鬥／探索／對話不再直接讀鍵碼或滑鼠來驅動它們。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _key(code: Key) -> InputEventKey:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = true
	return ev


func _initialize() -> void:
	var gi: Node = root.get_node_or_null("GameInput")
	if gi == null:
		_fail("GameInput autoload 沒載起來")
		return _finish()
	if gi.ALL.size() != 7:
		_fail("語意動作應為 7 個，得 %d" % gi.ALL.size())
	for a in ["move", "attack", "interact", "skill", "switch_weapon", "confirm", "cancel"]:
		if a not in gi.ALL:
			_fail("缺動作 %s" % a)

	var atk := _key(KEY_J)
	if not gi.matches(atk, gi.ATTACK):
		_fail("J 應是 Attack（舊 parry）")
	else:
		print("  ok J → Attack")

	var skill := _key(KEY_F)
	if not gi.matches(skill, gi.SKILL):
		_fail("F 應是 Skill")
	else:
		print("  ok F → Skill")

	var sw := _key(KEY_X)
	if not gi.matches(sw, gi.SWITCH_WEAPON):
		_fail("X 應是 SwitchWeapon")
	elif int(gi.weapon_slot(sw)) != 1:
		_fail("X 應是武器欄 2（slot 1），得 %d" % int(gi.weapon_slot(sw)))
	else:
		print("  ok X → SwitchWeapon slot 1")

	var enter := _key(KEY_ENTER)
	if not gi.matches(enter, gi.CONFIRM):
		_fail("Enter 應是 Confirm")
	else:
		print("  ok Enter → Confirm")

	var esc := _key(KEY_ESCAPE)
	if not gi.matches(esc, gi.CANCEL):
		_fail("Esc 應是 Cancel")
	else:
		print("  ok Esc → Cancel")

	var space := _key(KEY_SPACE)
	if not gi.matches(space, gi.INTERACT):
		_fail("Space 應是 Interact")
	else:
		print("  ok Space → Interact")

	var mb := InputEventMouseButton.new()
	mb.button_index = MOUSE_BUTTON_LEFT
	mb.pressed = true
	if not gi.primary_pointer_pressed(mb):
		_fail("滑鼠左應由 GameInput 認成主指標")
	else:
		print("  ok 主指標在 GameInput")

	_scan_sources()
	_finish()


func _scan_sources() -> void:
	## 戰鬥／探索／對話／過場不得再直接用鍵碼或滑鼠驅動七個動作。
	var files := {
		"res://scripts/battle/battle_view.gd": ["InputEventMouseButton", "KEY_Z", "KEY_X", "KEY_C", "KEY_F", "is_action_pressed(\"parry\")"],
		"res://scripts/world/explore_view.gd": ["InputEventMouseButton"],
		"res://scripts/world/explore_host.gd": ["InputEventMouseButton"],
		"res://scripts/ui/dialogue_box.gd": ["InputEventMouseButton", "is_action_pressed(\"ui_accept\")"],
		"res://scripts/ui/cutscene_player.gd": ["InputEventMouseButton", "is_action_pressed(\"ui_accept\")"],
		"res://scripts/main.gd": ["is_action_pressed(\"ui_cancel\")"],
	}
	for path in files:
		if not FileAccess.file_exists(path):
			_fail("找不到 %s" % path)
			continue
		var txt := FileAccess.get_file_as_string(path)
		for needle in files[path]:
			if txt.contains(needle):
				_fail("%s 仍直接判斷 %s" % [path, needle])
	if _ok:
		print("  ok 戰鬥／探索／對話／選單路徑已不直接讀鍵鼠驅動七動作")


func _finish() -> void:
	if _ok:
		print("GAME_INPUT_OK")
		quit(0)
	else:
		print("GAME_INPUT_FAIL")
		quit(1)
