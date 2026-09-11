class_name GemWorkshopDialog
extends Control
## 《發條之心》手藝工坊寶石彈窗 (GemWorkshopDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 連接既有寶石熔煉／寶石櫃畫面與 GemSystem。
## 7. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_SKY   := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）

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
	# 奶油米白底 + 深藍紫立體邊框 + 22px 大圓角
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
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
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_SKY)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 天藍色粗分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_SKY
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

	var smelt_panel := PanelContainer.new()
	smelt_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_SKY, COLOR_BORDER, 2, 4, 18))
	_smelt_view.add_child(smelt_panel)

	var sp_m := MarginContainer.new()
	sp_m.add_theme_constant_override("margin_left", 14)
	sp_m.add_theme_constant_override("margin_right", 14)
	sp_m.add_theme_constant_override("margin_top", 12)
	sp_m.add_theme_constant_override("margin_bottom", 12)
	smelt_panel.add_child(sp_m)

	_smelt_rich = RichTextLabel.new()
	_smelt_rich.bbcode_enabled = true
	_smelt_rich.fit_content = true
	_smelt_rich.scroll_active = false
	_smelt_rich.custom_minimum_size = Vector2(670, 0)
	_smelt_rich.add_theme_color_override("default_color", COLOR_TEXT_DARK)
	_smelt_rich.add_theme_font_size_override("normal_font_size", 16)
	_smelt_rich.add_theme_font_size_override("bold_font_size", 17)
	if _cached_font:
		_smelt_rich.add_theme_font_override("normal_font", _cached_font)
		_smelt_rich.add_theme_font_override("bold_font", _cached_font)
	sp_m.add_child(_smelt_rich)

	_actions_container = VBoxContainer.new()
	_actions_container.add_theme_constant_override("separation", 8)
	_smelt_view.add_child(_actions_container)

	# 2. 寶石櫃盤點分頁視圖
	_case_view = VBoxContainer.new()
	_case_view.add_theme_constant_override("separation", 10)
	_case_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_child(_case_view)

	var case_panel := PanelContainer.new()
	case_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	_case_view.add_child(case_panel)

	var cp_m := MarginContainer.new()
	cp_m.add_theme_constant_override("margin_left", 14)
	cp_m.add_theme_constant_override("margin_right", 14)
	cp_m.add_theme_constant_override("margin_top", 12)
	cp_m.add_theme_constant_override("margin_bottom", 12)
	case_panel.add_child(cp_m)

	_case_rich = RichTextLabel.new()
	_case_rich.bbcode_enabled = true
	_case_rich.fit_content = true
	_case_rich.scroll_active = false
	_case_rich.custom_minimum_size = Vector2(670, 0)
	_case_rich.add_theme_color_override("default_color", COLOR_TEXT_DARK)
	_case_rich.add_theme_font_size_override("normal_font_size", 16)
	_case_rich.add_theme_font_size_override("bold_font_size", 17)
	if _cached_font:
		_case_rich.add_theme_font_override("normal_font", _cached_font)
		_case_rich.add_theme_font_override("bold_font", _cached_font)
	cp_m.add_child(_case_rich)

	var btn_refresh_case := Button.new()
	btn_refresh_case.name = "BtnRefreshCase"
	btn_refresh_case.text = "重新盤點寶石櫃"
	btn_refresh_case.custom_minimum_size = Vector2(220, 50)
	btn_refresh_case.add_theme_font_size_override("font_size", 16)
	btn_refresh_case.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_refresh_case.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_refresh_case.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		btn_refresh_case.add_theme_font_override("font", _cached_font)
	btn_refresh_case.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 6, 20, 2))
	btn_refresh_case.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 6, 20, 2))
	btn_refresh_case.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
	btn_refresh_case.pressed.connect(_refresh_case_view)
	_case_view.add_child(btn_refresh_case)

	# 底部狀態訊息
	_msg_label = Label.new()
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 16)
	_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_msg_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_msg_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 底部離開按鈕 (按鈕高 >= 50, 金黃立體厚底 5px)
	var foot_row := HBoxContainer.new()
	foot_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(foot_row)

	var btn_close := Button.new()
	btn_close.name = "BtnCloseGemWorkshop"
	btn_close.text = "離開工坊"
	btn_close.custom_minimum_size = Vector2(180, 50)
	btn_close.add_theme_font_size_override("font_size", 18)
	btn_close.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_close.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_close.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		btn_close.add_theme_font_override("font", _cached_font)
	btn_close.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20, 2))
	btn_close.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 20, 2))
	btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
	btn_close.pressed.connect(_on_close)
	foot_row.add_child(btn_close)


func _switch_tab(tab: Tab) -> void:
	_current_tab = tab
	if tab == Tab.SMELT:
		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 20, 2))
		_tab_smelt_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5AB3FF"), COLOR_BORDER, 5, 20, 2))
		_tab_smelt_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#268FE8"), COLOR_BORDER, 2, 20, 2))
		_tab_smelt_btn.add_theme_color_override("font_color", Color.WHITE)
		_tab_smelt_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_smelt_btn.add_theme_constant_override("outline_size", 3)

		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(Color("#F6F1E6"), COLOR_BORDER, 3, 20, 1))
		_tab_case_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#EBE3D0"), COLOR_BORDER, 3, 20, 1))
		_tab_case_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#DFD4BC"), COLOR_BORDER, 1, 20, 1))
		_tab_case_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_case_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_case_btn.add_theme_constant_override("outline_size", 0)

		_smelt_view.visible = true
		_case_view.visible = false
		_refresh_smelt_view()
	else:
		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20, 2))
		_tab_case_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 20, 2))
		_tab_case_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
		_tab_case_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_case_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_case_btn.add_theme_constant_override("outline_size", 2)

		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(Color("#E8F2FC"), COLOR_BORDER, 3, 20, 1))
		_tab_smelt_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#D4E6F8"), COLOR_BORDER, 3, 20, 1))
		_tab_smelt_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#C4DCF4"), COLOR_BORDER, 1, 20, 1))
		_tab_smelt_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_smelt_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_smelt_btn.add_theme_constant_override("outline_size", 0)

		_smelt_view.visible = false
		_case_view.visible = true
		_refresh_case_view()


static func _darken_bbcode(text: String) -> String:
	return text.replace("#FFD028", "#9A6B00").replace("#ffd028", "#9A6B00") \
		.replace("#FFA010", "#C2600A").replace("#ffa010", "#C2600A") \
		.replace("#FF5E8A", "#D62E5C").replace("#ff5e8a", "#D62E5C")


func _refresh_smelt_view() -> void:
	_smelt_rich.text = _darken_bbcode(GemSystem.status_bbcode() + "\n\n" + GemSystem.panel_actions_hint())

	# 清理並重建可執行的熔煉與合成按鈕 (按鈕高 >= 50)
	for c in _actions_container.get_children():
		c.queue_free()

	var count_actions := 0

	# 1. 熔煉按鈕：3 碎片 -> 1 級 (薄荷綠立體果凍厚底 6px)
	for col in GemSystem.COLORS:
		if GemSystem.can_smelt(col):
			var c_str: String = col
			var btn := Button.new()
			btn.text = "熔煉 %s（3 碎片 → 1 級寶石）" % GemSystem.color_label(c_str)
			btn.custom_minimum_size = Vector2(0, 50)
			btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			btn.add_theme_font_size_override("font_size", 16)
			btn.add_theme_color_override("font_color", Color.WHITE)
			btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
			btn.add_theme_constant_override("outline_size", 4)
			if _cached_font:
				btn.add_theme_font_override("font", _cached_font)
			btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 20, 2))
			btn.add_theme_stylebox_override("hover", _create_button_style(Color("#68E882"), COLOR_BORDER, 6, 20, 2))
			btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3BBF55"), COLOR_BORDER, 2, 20, 2))
			btn.pressed.connect(func():
				var res: Dictionary = GemSystem.smelt(c_str)
				_msg_label.text = str(res.get("msg", "熔煉完成！"))
				_msg_label.add_theme_color_override("font_color", COLOR_MINT)
				SaveManager.save_game()
				_refresh_smelt_view()
			)
			_actions_container.add_child(btn)
			count_actions += 1

	# 2. 合成按鈕：3 顆同級 -> 1 顆下一級 (天藍立體果凍厚底 6px)
	for col in GemSystem.COLORS:
		for lv in range(1, GemSystem.MAX_LEVEL):
			if GemSystem.can_fuse(col, lv) and count_actions < 8:
				var c_str: String = col
				var l_val: int = lv
				var btn := Button.new()
				btn.text = "合成 %s（3 顆 %d 級 → 1 顆 %d 級寶石）" % [GemSystem.color_label(c_str), l_val, l_val + 1]
				btn.custom_minimum_size = Vector2(0, 50)
				btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
				btn.add_theme_font_size_override("font_size", 16)
				btn.add_theme_color_override("font_color", Color.WHITE)
				btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
				btn.add_theme_constant_override("outline_size", 4)
				if _cached_font:
					btn.add_theme_font_override("font", _cached_font)
				btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 6, 20, 2))
				btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5AB3FF"), COLOR_BORDER, 6, 20, 2))
				btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#268FE8"), COLOR_BORDER, 2, 20, 2))
				btn.pressed.connect(func():
					var res: Dictionary = GemSystem.fuse(c_str, l_val)
					_msg_label.text = str(res.get("msg", "合成完成！"))
					_msg_label.add_theme_color_override("font_color", COLOR_SKY)
					SaveManager.save_game()
					_refresh_smelt_view()
				)
				_actions_container.add_child(btn)
				count_actions += 1

	if count_actions == 0:
		var empty_lbl := Label.new()
		empty_lbl.text = "目前無可熔煉碎片（需 3 枚同色碎片）或可合成之同級寶石。\n可於主線冒險或獵場中取得寶石碎片。"
		empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		empty_lbl.add_theme_font_size_override("font_size", 16)
		empty_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		empty_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
		empty_lbl.add_theme_constant_override("outline_size", 1)
		if _cached_font:
			empty_lbl.add_theme_font_override("font", _cached_font)
		_actions_container.add_child(empty_lbl)


func _refresh_case_view() -> void:
	_case_rich.text = _darken_bbcode(GemSystem.gem_case_status_bbcode())


func _on_close() -> void:
	closed.emit()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	sb.shadow_size = 10
	sb.shadow_offset = Vector2(0, 5)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.35)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb
