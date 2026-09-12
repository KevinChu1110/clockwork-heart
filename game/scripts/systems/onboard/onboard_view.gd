extends Control
signal finished
## 新手 onb 場景：逐步顯示 onb.n01–n08，N07 可跳過進抽魂結果示意。

const FlowScript := preload("res://scripts/systems/onboard/onboard_flow.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const I18N_PATH := "res://data/i18n/zh_TW.json"

var flow
var card
var _dialog: Label
var _node_lbl: Label
var _hint: Label
var _btn_next: Button
var _btn_skip: Button
var _i18n: Dictionary = {}


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	if FileAccess.file_exists(I18N_PATH):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(I18N_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_i18n = parsed as Dictionary
	_build()
	flow = FlowScript.new()
	flow.load_bingo()
	_show_current()


func _tr(key: String) -> String:
	return str(_i18n.get(key, key))


func _build() -> void:
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.10, 0.09, 0.12, 1)
	add_child(bg)

	_node_lbl = Label.new()
	_node_lbl.position = Vector2(40, 24)
	_node_lbl.add_theme_font_size_override("font_size", 20)
	_node_lbl.add_theme_color_override("font_color", Color(0.85, 0.8, 0.65))
	add_child(_node_lbl)

	card = CardScript.new()
	card.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.offset_left = 60
	card.offset_top = 70
	card.offset_right = -60
	card.offset_bottom = -200
	card.visible = false
	add_child(card)

	_dialog = Label.new()
	_dialog.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dialog.offset_top = -190
	_dialog.offset_left = 48
	_dialog.offset_right = -48
	_dialog.offset_bottom = -110
	_dialog.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dialog.add_theme_font_size_override("font_size", 24)
	_dialog.add_theme_color_override("font_color", Color(0.95, 0.93, 0.88))
	add_child(_dialog)

	_hint = Label.new()
	_hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_hint.offset_top = -48
	_hint.offset_bottom = -16
	_hint.offset_left = 48
	_hint.text = "空白鍵／下一步 · N07 可「稍後再說」"
	_hint.add_theme_font_size_override("font_size", 14)
	_hint.add_theme_color_override("font_color", Color(0.65, 0.62, 0.55))
	add_child(_hint)

	var row := HBoxContainer.new()
	row.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	row.offset_top = -100
	row.offset_bottom = -52
	row.offset_left = 48
	row.offset_right = -48
	row.add_theme_constant_override("separation", 16)
	add_child(row)

	_btn_next = Button.new()
	_btn_next.text = "下一步"
	_btn_next.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_next.custom_minimum_size = Vector2(0, 48)
	_btn_next.pressed.connect(func() -> void: _advance(false))
	row.add_child(_btn_next)

	_btn_skip = Button.new()
	_btn_skip.text = "稍後再說"
	_btn_skip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_skip.custom_minimum_size = Vector2(0, 48)
	_btn_skip.pressed.connect(func() -> void: _advance(true))
	row.add_child(_btn_skip)


func _show_current() -> void:
	if flow.done:
		_node_lbl.text = "新手完成"
		_dialog.text = _tr("onb.n08")
		_btn_next.disabled = true
		_btn_skip.visible = false
		if not has_meta("_emitted_finished"):
			set_meta("_emitted_finished", true)
			finished.emit()
		return
	var cur: Dictionary = flow.current()
	var node: String = str(cur.get("node", ""))
	var key: String = str(cur.get("key", ""))
	_node_lbl.text = "新手 · %s · cue %s" % [node, str(cur.get("cue", ""))]
	_dialog.text = _tr(key)
	_btn_skip.visible = flow.can_skip_current()
	# N07／N08 秀結果卡
	if node in ["N07", "N08"]:
		card.visible = true
		card.show_placeholder(str(cur.get("cue", "soul.pull_start")))
	else:
		card.visible = false


func _advance(skip: bool) -> void:
	flow.advance(skip)
	_show_current()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		_advance(false)
		get_viewport().set_input_as_handled()
