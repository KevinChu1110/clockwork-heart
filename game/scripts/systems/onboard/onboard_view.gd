extends Control
signal finished
## 新手 onb 場景：逐步顯示 onb.n01–n08，N07 可跳過進抽魂結果示意。

const FlowScript := preload("res://scripts/systems/onboard/onboard_flow.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const UiStyle := preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const I18N_PATH := "res://data/i18n/zh_TW.json"

var flow
var card
var force_touch_mode: Variant = null:  ## 測試/截圖強制覆寫觸控模式；null 為自動判定
	set(v):
		force_touch_mode = v
		_update_ui_texts()
var _panel: PanelContainer
var _dialog: Label
var _node_lbl: Label
var _hint: Label
var _btn_next: Button
var _btn_skip: Button
var _i18n: Dictionary = {}


static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res


static func is_touch_device(force_touch: Variant = null) -> bool:
	if force_touch != null:
		return bool(force_touch)
	return DisplayServer.is_touchscreen_available()


static func hint_text(force_touch: Variant = null) -> String:
	if is_touch_device(force_touch):
		return _t("點一下繼續 · 部分步驟可「稍後再說」")
	return _t("空白鍵／下一步 · 部分步驟可「稍後再說」")


func _is_touch() -> bool:
	return is_touch_device(force_touch_mode)


func _hint_text() -> String:
	return hint_text(force_touch_mode)


func _tr(key: String) -> String:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var res = str(loc.call("t", key))
			if res != "" and res != key:
				return res
	return str(_i18n.get(key, key))


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	if FileAccess.file_exists(I18N_PATH):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(I18N_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_i18n = parsed as Dictionary
	_connect_loc_signal()
	_build()
	flow = FlowScript.new()
	flow.load_bingo()
	_show_current()


func _exit_tree() -> void:
	_disconnect_loc_signal()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	_show_current()


func _update_ui_texts() -> void:
	if _btn_next and is_instance_valid(_btn_next):
		_btn_next.text = _t("下一步")
	if _btn_skip and is_instance_valid(_btn_skip):
		_btn_skip.text = _t("稍後再說")
	if _hint and is_instance_valid(_hint):
		_hint.text = _hint_text()


func _build() -> void:
	# 1. 溫暖奶油陽光底，徹底告別 0.10 黑曜石暗底
	var bg := ColorRect.new()
	bg.name = "Background"
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.96, 0.94, 0.90, 1.0)
	add_child(bg)

	# 2. 置中容器與手遊橫屏主卡片（對齊 740~760px 規範，寬 750px）
	var center := CenterContainer.new()
	center.name = "Center"
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_PASS
	add_child(center)

	_panel = PanelContainer.new()
	_panel.name = "OnboardCard"
	_panel.custom_minimum_size = Vector2(750, 500)
	_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	center.add_child(_panel)

	var margin := MarginContainer.new()
	margin.name = "Margin"
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 20)
	margin.add_theme_constant_override("margin_bottom", 20)
	_panel.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.name = "ContentVBox"
	vbox.add_theme_constant_override("separation", 14)
	margin.add_child(vbox)

	# 標題級 (約 24px)
	_node_lbl = Label.new()
	_node_lbl.name = "NodeTitle"
	_node_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_node_lbl.add_theme_font_size_override("font_size", 22)
	_node_lbl.add_theme_color_override("font_color", UiStyle.INK)
	_node_lbl.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.9))
	_node_lbl.add_theme_constant_override("outline_size", 2)
	vbox.add_child(_node_lbl)

	# N07/N08 抽魂結果卡示意（具備足夠高度供 TextureRect 與 Label 居中排列）
	card = CardScript.new()
	card.name = "SoulResultCard"
	card.custom_minimum_size = Vector2(0, 250)
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.size_flags_vertical = Control.SIZE_EXPAND_FILL
	card.visible = false
	vbox.add_child(card)

	# 內文級 (24px)
	_dialog = Label.new()
	_dialog.name = "DialogLabel"
	_dialog.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_dialog.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_dialog.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_dialog.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_dialog.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_dialog.custom_minimum_size = Vector2(0, 80)
	_dialog.add_theme_font_size_override("font_size", 24)
	_dialog.add_theme_color_override("font_color", UiStyle.INK)
	vbox.add_child(_dialog)

	# 按鈕列：高度 >= 50px
	var row := HBoxContainer.new()
	row.name = "ButtonRow"
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 16)
	vbox.add_child(row)

	_btn_next = Button.new()
	_btn_next.name = "BtnNext"
	_btn_next.text = _t("下一步")
	_btn_next.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	UiStyle.style_button(_btn_next, true)
	_btn_next.custom_minimum_size = Vector2(0, 50)
	_btn_next.pressed.connect(func() -> void: _advance(false))
	row.add_child(_btn_next)

	_btn_skip = Button.new()
	_btn_skip.name = "BtnSkip"
	_btn_skip.text = _t("稍後再說")
	_btn_skip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	UiStyle.style_button(_btn_skip, false)
	_btn_skip.custom_minimum_size = Vector2(0, 50)
	_btn_skip.pressed.connect(func() -> void: _advance(true))
	row.add_child(_btn_skip)

	# 輔助級 (>= 16px)
	_hint = Label.new()
	_hint.name = "HintLabel"
	_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hint.text = _hint_text()
	_hint.add_theme_font_size_override("font_size", 16)
	_hint.add_theme_color_override("font_color", UiStyle.INK_DIM)
	vbox.add_child(_hint)


func _show_current() -> void:
	if flow == null:
		return
	if flow.done:
		if _node_lbl and is_instance_valid(_node_lbl):
			_node_lbl.text = _t("新手完成")
		if _dialog and is_instance_valid(_dialog):
			_dialog.text = _tr("onb.n08")
		if _btn_next and is_instance_valid(_btn_next):
			_btn_next.disabled = true
		if _btn_skip and is_instance_valid(_btn_skip):
			_btn_skip.visible = false
		if not has_meta("_emitted_finished"):
			set_meta("_emitted_finished", true)
			finished.emit()
		return
	var cur: Dictionary = flow.current()
	var node: String = str(cur.get("node", ""))
	var key: String = str(cur.get("key", ""))
	if _node_lbl and is_instance_valid(_node_lbl):
		_node_lbl.text = _t("新手引導 · 第 %d／%d 步") % [flow.step_index + 1, flow.steps().size()]
	if _dialog and is_instance_valid(_dialog):
		_dialog.text = _tr(key)
	if _btn_skip and is_instance_valid(_btn_skip):
		_btn_skip.visible = flow.can_skip_current()
	# N07／N08 秀結果卡
	if node in ["N07", "N08"]:
		if card and is_instance_valid(card):
			card.visible = true
			card.show_placeholder(str(cur.get("cue", "soul.pull_start")))
	else:
		if card and is_instance_valid(card):
			card.visible = false


func _advance(skip: bool) -> void:
	flow.advance(skip)
	_show_current()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		_advance(false)
		get_viewport().set_input_as_handled()
