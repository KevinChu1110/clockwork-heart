class_name GemWorkshopDialog
extends Control
## 《發條之心》手藝工坊寶石彈窗 (GemWorkshopDialog)
## 依手遊人體工學與 review.md 第 28、29 條規範：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 連接既有寶石熔煉／寶石櫃畫面與 GemSystem。
## 4. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const OBSIDIAN_CARD   := Color(0.078, 0.071, 0.094, 0.98)
const OBSIDIAN_WARM   := Color(0.102, 0.090, 0.122, 1.0)
const OBSIDIAN_DEEP   := Color(0.027, 0.024, 0.039, 1.0)
const GOLD_CLASSICAL  := Color(0.831, 0.686, 0.216, 1.0)
const GOLD_HOVER      := Color(0.941, 0.843, 0.549, 1.0)
const INK_IVORY       := Color(0.957, 0.922, 0.831, 1.0)
const INK_MUTED       := Color(0.65, 0.60, 0.52, 1.0)
const LINE_GOLD       := Color(0.831, 0.686, 0.216, 0.5)
const BTN_ACTIVE_BG   := Color(0.20, 0.18, 0.26, 1.0)
const BTN_INACTIVE_BG := Color(0.08, 0.07, 0.10, 1.0)
const BTN_GREEN_BG    := Color(0.20, 0.58, 0.32, 1.0)
const BTN_GREEN_BORDER:= Color(0.35, 0.78, 0.48, 1.0)

enum Tab {
	SMELT,
	CASE_INSPECT,
}

var _current_tab: Tab = Tab.SMELT

var _dialog_card: PanelContainer
var _tab_smelt_btn: Button
var _tab_case_btn: Button

var _smelt_view: VBoxContainer
var _smelt_rich: RichTextLabel
var _actions_container: VBoxContainer

var _case_view: VBoxContainer
var _case_rich: RichTextLabel

var _msg_label: Label
var _cached_font: Font = null


func _ready() -> void:
	name = "GemWorkshopDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build_ui()
	_switch_tab(Tab.SMELT)


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	var scrim_btn := Button.new()
	scrim_btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_btn.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_btn.add_theme_stylebox_override("normal", esb)
	scrim_btn.add_theme_stylebox_override("hover", esb)
	scrim_btn.add_theme_stylebox_override("pressed", esb)
	scrim_btn.pressed.connect(_on_close)
	scrim.add_child(scrim_btn)

	# 2. 置中卡片 (寬 750px，符合 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "GemWorkshopCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 500)
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(OBSIDIAN_CARD, GOLD_CLASSICAL, 1, 4, 14))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 10)
	margin.add_child(v)

	# 標題列 + 右上「✕」關閉按鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.text = "手藝工坊 · 寶石熔煉與寶石櫃"
	title_lbl.add_theme_font_size_override("font_size", 20)
	title_lbl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 金色分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 2)
	sep.color = LINE_GOLD
	v.add_child(sep)

	# 分頁標籤切換列 (按鈕高 >= 50)
	var tab_row := HBoxContainer.new()
	tab_row.add_theme_constant_override("separation", 12)
	v.add_child(tab_row)

	_tab_smelt_btn = Button.new()
	_tab_smelt_btn.name = "TabSmeltBtn"
	_tab_smelt_btn.text = "寶石熔煉與合成"
	_tab_smelt_btn.custom_minimum_size = Vector2(220, 50)
	_tab_smelt_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_tab_smelt_btn.add_theme_font_override("font", _cached_font)
	_tab_smelt_btn.pressed.connect(func(): _switch_tab(Tab.SMELT))
	tab_row.add_child(_tab_smelt_btn)

	_tab_case_btn = Button.new()
	_tab_case_btn.name = "TabCaseBtn"
	_tab_case_btn.text = "寶石櫃盤點檢視"
	_tab_case_btn.custom_minimum_size = Vector2(220, 50)
	_tab_case_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_tab_case_btn.add_theme_font_override("font", _cached_font)
	_tab_case_btn.pressed.connect(func(): _switch_tab(Tab.CASE_INSPECT))
	tab_row.add_child(_tab_case_btn)

	# 內容捲動區 (高 270px)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(710, 260)
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	v.add_child(scroll)

	var content_box := VBoxContainer.new()
	content_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(content_box)

	# 1. 熔煉分頁視圖
	_smelt_view = VBoxContainer.new()
	_smelt_view.add_theme_constant_override("separation", 10)
	_smelt_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_child(_smelt_view)

	_smelt_rich = RichTextLabel.new()
	_smelt_rich.bbcode_enabled = true
	_smelt_rich.fit_content = true
	_smelt_rich.scroll_active = false
	_smelt_rich.custom_minimum_size = Vector2(700, 0)
	if _cached_font:
		_smelt_rich.add_theme_font_override("normal_font", _cached_font)
	_smelt_view.add_child(_smelt_rich)

	_actions_container = VBoxContainer.new()
	_actions_container.add_theme_constant_override("separation", 8)
	_smelt_view.add_child(_actions_container)

	# 2. 寶石櫃盤點分頁視圖
	_case_view = VBoxContainer.new()
	_case_view.add_theme_constant_override("separation", 10)
	_case_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_child(_case_view)

	_case_rich = RichTextLabel.new()
	_case_rich.bbcode_enabled = true
	_case_rich.fit_content = true
	_case_rich.scroll_active = false
	_case_rich.custom_minimum_size = Vector2(700, 0)
	if _cached_font:
		_case_rich.add_theme_font_override("normal_font", _cached_font)
	_case_view.add_child(_case_rich)

	var btn_refresh_case := Button.new()
	btn_refresh_case.name = "BtnRefreshCase"
	btn_refresh_case.text = "重新盤點寶石櫃"
	btn_refresh_case.custom_minimum_size = Vector2(220, 50)
	btn_refresh_case.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		btn_refresh_case.add_theme_font_override("font", _cached_font)
	btn_refresh_case.add_theme_stylebox_override("normal", _create_button_style(OBSIDIAN_WARM, LINE_GOLD, 4))
	btn_refresh_case.add_theme_stylebox_override("hover", _create_button_style(Color(0.15, 0.13, 0.18), GOLD_HOVER, 4))
	btn_refresh_case.add_theme_stylebox_override("pressed", _create_button_style(Color(0.08, 0.07, 0.10), LINE_GOLD, 2))
	btn_refresh_case.add_theme_color_override("font_color", INK_IVORY)
	btn_refresh_case.pressed.connect(_refresh_case_view)
	_case_view.add_child(btn_refresh_case)

	# 底部狀態訊息
	_msg_label = Label.new()
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 14)
	_msg_label.add_theme_color_override("font_color", GOLD_HOVER)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 底部離開按鈕 (按鈕高 >= 50)
	var foot_row := HBoxContainer.new()
	foot_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(foot_row)

	var btn_close := Button.new()
	btn_close.name = "BtnCloseGemWorkshop"
	btn_close.text = "離開工坊"
	btn_close.custom_minimum_size = Vector2(180, 50)
	btn_close.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		btn_close.add_theme_font_override("font", _cached_font)
	btn_close.add_theme_stylebox_override("normal", _create_button_style(OBSIDIAN_WARM, LINE_GOLD, 4))
	btn_close.add_theme_stylebox_override("hover", _create_button_style(Color(0.15, 0.13, 0.18), GOLD_HOVER, 4))
	btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color(0.08, 0.07, 0.10), LINE_GOLD, 2))
	btn_close.add_theme_color_override("font_color", INK_IVORY)
	btn_close.pressed.connect(_on_close)
	foot_row.add_child(btn_close)


func _switch_tab(tab: Tab) -> void:
	_current_tab = tab
	if tab == Tab.SMELT:
		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(BTN_ACTIVE_BG, GOLD_CLASSICAL, 4))
		_tab_smelt_btn.add_theme_color_override("font_color", GOLD_CLASSICAL)
		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(BTN_INACTIVE_BG, LINE_GOLD, 2))
		_tab_case_btn.add_theme_color_override("font_color", INK_MUTED)
		_smelt_view.visible = true
		_case_view.visible = false
		_refresh_smelt_view()
	else:
		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(BTN_ACTIVE_BG, GOLD_CLASSICAL, 4))
		_tab_case_btn.add_theme_color_override("font_color", GOLD_CLASSICAL)
		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(BTN_INACTIVE_BG, LINE_GOLD, 2))
		_tab_smelt_btn.add_theme_color_override("font_color", INK_MUTED)
		_smelt_view.visible = false
		_case_view.visible = true
		_refresh_case_view()


func _refresh_smelt_view() -> void:
	_smelt_rich.text = GemSystem.status_bbcode() + "\n\n" + GemSystem.panel_actions_hint()

	# 清理並重建可執行的熔煉與合成按鈕 (按鈕高 >= 50)
	for c in _actions_container.get_children():
		c.queue_free()

	var count_actions := 0

	# 1. 熔煉按鈕：3 碎片 -> 1 級
	for col in GemSystem.COLORS:
		if GemSystem.can_smelt(col):
			var c_str: String = col
			var btn := Button.new()
			btn.text = "熔煉 %s（3 碎片 → 1 級寶石）" % GemSystem.color_label(c_str)
			btn.custom_minimum_size = Vector2(0, 50)
			btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			btn.add_theme_font_size_override("font_size", 15)
			if _cached_font:
				btn.add_theme_font_override("font", _cached_font)
			btn.add_theme_stylebox_override("normal", _create_button_style(BTN_GREEN_BG, BTN_GREEN_BORDER, 4))
			btn.add_theme_stylebox_override("hover", _create_button_style(Color(0.25, 0.68, 0.38), BTN_GREEN_BORDER, 4))
			btn.add_theme_color_override("font_color", Color.WHITE)
			btn.pressed.connect(func():
				var res: Dictionary = GemSystem.smelt(c_str)
				_msg_label.text = str(res.get("msg", "熔煉完成！"))
				_msg_label.add_theme_color_override("font_color", Color(0.4, 0.95, 0.5))
				SaveManager.save_game()
				_refresh_smelt_view()
			)
			_actions_container.add_child(btn)
			count_actions += 1

	# 2. 合成按鈕：3 顆同級 -> 1 顆下一級
	for col in GemSystem.COLORS:
		for lv in range(1, GemSystem.MAX_LEVEL):
			if GemSystem.can_fuse(col, lv) and count_actions < 8:
				var c_str: String = col
				var l_val: int = lv
				var btn := Button.new()
				btn.text = "合成 %s（3 顆 %d 級 → 1 顆 %d 級寶石）" % [GemSystem.color_label(c_str), l_val, l_val + 1]
				btn.custom_minimum_size = Vector2(0, 50)
				btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
				btn.add_theme_font_size_override("font_size", 15)
				if _cached_font:
					btn.add_theme_font_override("font", _cached_font)
				btn.add_theme_stylebox_override("normal", _create_button_style(Color(0.18, 0.32, 0.58), Color(0.35, 0.55, 0.88), 4))
				btn.add_theme_stylebox_override("hover", _create_button_style(Color(0.25, 0.42, 0.72), Color(0.45, 0.65, 0.98), 4))
				btn.add_theme_color_override("font_color", Color.WHITE)
				btn.pressed.connect(func():
					var res: Dictionary = GemSystem.fuse(c_str, l_val)
					_msg_label.text = str(res.get("msg", "合成完成！"))
					_msg_label.add_theme_color_override("font_color", Color(0.4, 0.8, 1.0))
					SaveManager.save_game()
					_refresh_smelt_view()
				)
				_actions_container.add_child(btn)
				count_actions += 1

	if count_actions == 0:
		var empty_lbl := Label.new()
		empty_lbl.text = "目前無可熔煉碎片（需 3 枚同色碎片）或可合成之同級寶石。\n可於主線冒險或獵場中取得寶石碎片。"
		empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		empty_lbl.add_theme_font_size_override("font_size", 14)
		empty_lbl.add_theme_color_override("font_color", INK_MUTED)
		if _cached_font:
			empty_lbl.add_theme_font_override("font", _cached_font)
		_actions_container.add_child(empty_lbl)


func _refresh_case_view() -> void:
	_case_rich.text = GemSystem.gem_case_status_bbcode()


func _on_close() -> void:
	closed.emit()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 1, bottom_w: int = 3, radius: int = 12) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	return sb


func _create_button_style(bg: Color, border: Color, bottom_border: int = 4) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(1)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	return sb
