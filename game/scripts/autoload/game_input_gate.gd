extends RefCounted
## 給會被 `godot --headless -s` 測試 preload 的腳本用。
## 不可寫 autoload 識別字 GameInput：那種測試編譯早於 autoload 註冊，
## 會 Identifier not found，連帶所有 preload 此腳本的測試全滅。
## 遊戲正常跑時走 /root/GameInput；取不到時退回 InputMap 舊名。

const MOVE := "move"
const ATTACK := "attack"
const INTERACT := "interact"
const SKILL := "skill"
const SWITCH_WEAPON := "switch_weapon"
const CONFIRM := "confirm"
const CANCEL := "cancel"


static func lookup() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("/root/GameInput")
	return null


static func matches(event: InputEvent, action: String) -> bool:
	var gi := lookup()
	if gi != null:
		return gi.matches(event, action)
	if event == null or action == MOVE:
		return false
	if event.is_echo():
		return false
	for n in _fallback_names(action):
		if InputMap.has_action(n) and event.is_action_pressed(n):
			return true
	return false


static func primary_pointer_pressed(event: InputEvent) -> bool:
	var gi := lookup()
	if gi != null:
		return gi.primary_pointer_pressed(event)
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		return mb.pressed and mb.button_index == MOUSE_BUTTON_LEFT
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).pressed
	return false


static func pointer_position(event: InputEvent) -> Vector2:
	var gi := lookup()
	if gi != null:
		return gi.pointer_position(event)
	if event is InputEventMouseButton:
		return (event as InputEventMouseButton).position
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).position
	return Vector2.ZERO


static func weapon_slot(event: InputEvent) -> int:
	var gi := lookup()
	if gi != null:
		return int(gi.weapon_slot(event))
	if event == null:
		return -1
	var slots := PackedStringArray(["switch_weapon_1", "switch_weapon_2", "switch_weapon_3"])
	for i in slots.size():
		var n := slots[i]
		if InputMap.has_action(n) and event.is_action_pressed(n):
			return i
	return -1


static func inject(action: String, down: bool = true) -> void:
	var gi := lookup()
	if gi != null:
		gi.inject(action, down)
		return
	var picked := ""
	for n in _fallback_names(action):
		if InputMap.has_action(n):
			picked = n
	if picked == "":
		return
	var ev := InputEventAction.new()
	ev.action = picked
	ev.pressed = down
	Input.parse_input_event(ev)


static func _fallback_names(action: String) -> PackedStringArray:
	match action:
		ATTACK:
			return PackedStringArray(["attack", "parry"])
		INTERACT:
			return PackedStringArray(["interact"])
		SKILL:
			return PackedStringArray(["skill"])
		SWITCH_WEAPON:
			return PackedStringArray([
				"switch_weapon", "switch_weapon_1", "switch_weapon_2", "switch_weapon_3",
			])
		CONFIRM:
			return PackedStringArray(["confirm", "ui_accept"])
		CANCEL:
			return PackedStringArray(["cancel", "ui_cancel"])
		MOVE:
			return PackedStringArray(["ui_left", "ui_right", "ui_up", "ui_down"])
		_:
			return PackedStringArray([action])
