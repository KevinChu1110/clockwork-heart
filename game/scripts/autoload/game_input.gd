extends Node
## 輸入抽象層（Product Lock §5.1 第 2 項）
##
## 遊戲邏輯只讀七個語意動作：
##   Move / Attack / Interact / Skill / SwitchWeapon / Confirm / Cancel
## PC 綁鍵鼠／手把，手機綁觸控／虛擬按鍵。裝置判斷只准出現在這一檔。

const MOVE := "move"
const ATTACK := "attack"
const INTERACT := "interact"
const SKILL := "skill"
const SWITCH_WEAPON := "switch_weapon"
const CONFIRM := "confirm"
const CANCEL := "cancel"

const ALL: PackedStringArray = [
	MOVE, ATTACK, INTERACT, SKILL, SWITCH_WEAPON, CONFIRM, CANCEL,
]

## 語意動作 → InputMap 名稱（含舊名，避免一次拆光既有綁定）
var _aliases := {
	ATTACK: PackedStringArray(["attack", "parry"]),
	INTERACT: PackedStringArray(["interact"]),
	SKILL: PackedStringArray(["skill"]),
	SWITCH_WEAPON: PackedStringArray([
		"switch_weapon", "switch_weapon_1", "switch_weapon_2", "switch_weapon_3",
	]),
	CONFIRM: PackedStringArray(["confirm", "ui_accept"]),
	CANCEL: PackedStringArray(["cancel", "ui_cancel"]),
	MOVE: PackedStringArray(["ui_left", "ui_right", "ui_up", "ui_down"]),
}

const _SLOT_ACTIONS: PackedStringArray = [
	"switch_weapon_1", "switch_weapon_2", "switch_weapon_3",
]


var _bound := false


func _ready() -> void:
	_ensure_bindings()


func _ensure_bindings() -> void:
	if _bound:
		return
	_bound = true
	## Attack：沿用既有 parry（J／K／滑鼠左／手把 B）
	_ensure_action("attack")
	_copy_events("parry", "attack")
	## Skill：F、手把 Y
	_bind_key("skill", KEY_F)
	_bind_joy("skill", JOY_BUTTON_Y)
	## SwitchWeapon：Z／X／C 對欄 1／2／3；手把 RB 循環（slot = -1）
	_bind_key("switch_weapon_1", KEY_Z)
	_bind_key("switch_weapon_2", KEY_X)
	_bind_key("switch_weapon_3", KEY_C)
	_bind_joy("switch_weapon", JOY_BUTTON_RIGHT_SHOULDER)
	_ensure_action("confirm")
	_copy_events("ui_accept", "confirm")
	_ensure_action("cancel")
	_copy_events("ui_cancel", "cancel")


func names(action: String) -> PackedStringArray:
	_ensure_bindings()
	return _aliases.get(action, PackedStringArray([action]))


func just_pressed(action: String) -> bool:
	for n in names(action):
		if InputMap.has_action(n) and Input.is_action_just_pressed(n):
			return true
	return false


func pressed(action: String) -> bool:
	if action == MOVE:
		return move_vector().length() > 0.2
	for n in names(action):
		if InputMap.has_action(n) and Input.is_action_pressed(n):
			return true
	return false


func matches(event: InputEvent, action: String) -> bool:
	if event == null or action == MOVE:
		return false
	if event.is_echo():
		return false
	for n in names(action):
		if InputMap.has_action(n) and event.is_action_pressed(n):
			return true
	return false


func move_vector() -> Vector2:
	return Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")


func weapon_slot(event: InputEvent) -> int:
	_ensure_bindings()
	if event == null:
		return -1
	for i in _SLOT_ACTIONS.size():
		var n := _SLOT_ACTIONS[i]
		if InputMap.has_action(n) and event.is_action_pressed(n):
			return i
	return -1


## 觸控／滑鼠主鍵按下。只有這一層可以認裝置。
## 給「這個 widget 就是某語意動作的虛擬鍵」用，遊戲邏輯不要拿去當 Attack。
func primary_pointer_pressed(event: InputEvent) -> bool:
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		return mb.pressed and mb.button_index == MOUSE_BUTTON_LEFT
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).pressed
	return false


func pointer_position(event: InputEvent) -> Vector2:
	if event is InputEventMouseButton:
		return (event as InputEventMouseButton).position
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).position
	return Vector2.ZERO


func inject(action: String, down: bool = true) -> void:
	## 用別名清單最後一個（舊 InputMap 名），既有 listener 才接得到。
	var picked := ""
	for n in names(action):
		if InputMap.has_action(n):
			picked = n
	if picked == "":
		return
	var ev := InputEventAction.new()
	ev.action = picked
	ev.pressed = down
	Input.parse_input_event(ev)


func _ensure_action(action: String) -> void:
	if not InputMap.has_action(action):
		InputMap.add_action(action)


func _bind_key(action: String, physical: Key) -> void:
	_ensure_action(action)
	for existing in InputMap.action_get_events(action):
		if existing is InputEventKey and (existing as InputEventKey).physical_keycode == physical:
			return
	var ev := InputEventKey.new()
	ev.physical_keycode = physical
	ev.device = -1
	InputMap.action_add_event(action, ev)


func _bind_joy(action: String, button: JoyButton) -> void:
	_ensure_action(action)
	for existing in InputMap.action_get_events(action):
		if existing is InputEventJoypadButton \
				and (existing as InputEventJoypadButton).button_index == button:
			return
	var ev := InputEventJoypadButton.new()
	ev.button_index = button
	ev.device = -1
	InputMap.action_add_event(action, ev)


func _copy_events(from_action: String, to_action: String) -> void:
	if not InputMap.has_action(from_action):
		return
	_ensure_action(to_action)
	for ev in InputMap.action_get_events(from_action):
		if not InputMap.action_has_event(to_action, ev):
			InputMap.action_add_event(to_action, ev)
