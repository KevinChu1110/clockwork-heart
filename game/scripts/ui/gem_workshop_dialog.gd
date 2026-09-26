class_name GemWorkshopDialog
extends Control
## 《發條之心》手藝工坊寶石彈窗 (GemWorkshopDialog)
## 依多巴胺亮色盤規範與手遊人體工學果凍化重構：
## 1. 橫屏彈窗寬 750px (符合 740~760px)、高 580px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，分頁鈕與操作主按鈕高均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 14~22px，主要按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零 13px 以下小字。
## 6. 徹底移除 RichTextLabel BBCode 長文牆，全面改為果凍卡片網格與實體拇指按鈕。
## 7. 零系統 Emoji、零字元圖示。
## 8. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換)。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

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

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM   := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_SKY    := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_PINK   := Color("#FFF0F4")  ## 珊瑚粉柔和卡片底
const COLOR_CARD_MUTED  := Color("#EFEBE0")  ## 壓暗奶油底（空卡片專用）
const COLOR_BORDER_MUTED:= Color("#D2CCC0")  ## 壓暗淡邊框

## ── 亮底合規文字色（嚴禁未壓明度之金黃/暖橘/粉紅）──
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK   := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）
const COLOR_TEXT_MUTED  := Color("#6B6680")  ## 次要輔助文字
const COLOR_TEXT_DIM    := Color("#888294")  ## 空庫存標籤文字
const COLOR_TEXT_DIM2   := Color("#A09CA8")  ## 空庫存數量文字

enum Tab {
	SMELT,
	CASE_INSPECT,
}

var _current_tab: Tab = Tab.SMELT

var _dialog_card: PanelContainer
var _title_lbl: Label
var _tab_smelt_btn: Button
var _tab_case_btn: Button

var _smelt_view: VBoxContainer
var _smelt_cards_box: HBoxContainer
var _furnace_bar: PanelContainer

var _case_view: VBoxContainer
var _case_slots_row: HBoxContainer
var _case_bonus_panel: PanelContainer
var _grid_title: Label
var _btn_refresh_case: Button
var _btn_auto_socket: Button
var _case_grid: GridContainer

var _msg_label: Label
var _btn_close: Button
var _cached_font: Font = null


func _enter_tree() -> void:
	_connect_loc_signal()


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
	if _current_tab == Tab.SMELT:
		_refresh_smelt_view()
	else:
		_refresh_case_view()


func _update_ui_texts() -> void:
	if _title_lbl and is_instance_valid(_title_lbl):
		_title_lbl.text = _t("手藝工坊 · 寶石熔煉與寶石櫃")
	if _tab_smelt_btn and is_instance_valid(_tab_smelt_btn):
		_tab_smelt_btn.text = _t("寶石熔煉與合成")
	if _tab_case_btn and is_instance_valid(_tab_case_btn):
		_tab_case_btn.text = _t("寶石櫃盤點檢視")
	if _grid_title and is_instance_valid(_grid_title):
		_grid_title.text = _t("倉庫寶石儲備盤點（各階數量）")
	if _btn_refresh_case and is_instance_valid(_btn_refresh_case):
		_btn_refresh_case.text = _t("重新盤點")
	if _btn_auto_socket and is_instance_valid(_btn_auto_socket):
		_btn_auto_socket.text = _t("一鍵鑲嵌")
	if _btn_close and is_instance_valid(_btn_close):
		_btn_close.text = _t("離開工坊")


func _ready() -> void:
	name = "GemWorkshopDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_connect_loc_signal()
	_build_ui()
	_update_ui_texts()
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

	# 2. 置中卡片 (寬 750px，高 580px，符合 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "GemWorkshopCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 580)
	_dialog_card.clip_contents = true
	# 奶油米白底 + 深藍紫立體邊框 + 22px 大圓角
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 14)
	margin.add_theme_constant_override("margin_bottom", 14)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	margin.add_child(v)

	# 標題列 + 右上「✕」關閉按鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("手藝工坊 · 寶石熔煉與寶石櫃")
	_title_lbl.add_theme_font_size_override("font_size", 22)
	_title_lbl.add_theme_color_override("font_color", COLOR_SKY)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_title_lbl.add_theme_font_override("font", _cached_font)
	_title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(_title_lbl)

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
	_tab_smelt_btn.text = _t("寶石熔煉與合成")
	_tab_smelt_btn.custom_minimum_size = Vector2(220, 50)
	_tab_smelt_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_tab_smelt_btn.add_theme_font_override("font", _cached_font)
	_tab_smelt_btn.pressed.connect(func(): _switch_tab(Tab.SMELT))
	tab_row.add_child(_tab_smelt_btn)

	_tab_case_btn = Button.new()
	_tab_case_btn.name = "TabCaseBtn"
	_tab_case_btn.text = _t("寶石櫃盤點檢視")
	_tab_case_btn.custom_minimum_size = Vector2(220, 50)
	_tab_case_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_tab_case_btn.add_theme_font_override("font", _cached_font)
	_tab_case_btn.pressed.connect(func(): _switch_tab(Tab.CASE_INSPECT))
	tab_row.add_child(_tab_case_btn)

	# 內容捲動區 (高 355px，完美納入全視圖，無多餘捲動)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(710, 355)
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	v.add_child(scroll)

	var content_box := VBoxContainer.new()
	content_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_theme_constant_override("separation", 8)
	scroll.add_child(content_box)

	# 1. 熔煉分頁視圖
	_smelt_view = VBoxContainer.new()
	_smelt_view.add_theme_constant_override("separation", 8)
	_smelt_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_child(_smelt_view)

	_furnace_bar = PanelContainer.new()
	_furnace_bar.name = "FurnaceBar"
	_furnace_bar.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 14))
	_smelt_view.add_child(_furnace_bar)

	_smelt_cards_box = HBoxContainer.new()
	_smelt_cards_box.name = "SmeltCardsBox"
	_smelt_cards_box.add_theme_constant_override("separation", 10)
	_smelt_cards_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_smelt_view.add_child(_smelt_cards_box)

	# 2. 寶石櫃盤點分頁視圖
	_case_view = VBoxContainer.new()
	_case_view.add_theme_constant_override("separation", 6)
	_case_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_child(_case_view)

	_case_slots_row = HBoxContainer.new()
	_case_slots_row.name = "CaseSlotsRow"
	_case_slots_row.add_theme_constant_override("separation", 10)
	_case_slots_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_case_view.add_child(_case_slots_row)

	_case_bonus_panel = PanelContainer.new()
	_case_bonus_panel.name = "CaseBonusPanel"
	_case_bonus_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_SKY, COLOR_BORDER, 2, 3, 14))
	_case_view.add_child(_case_bonus_panel)

	var case_grid_wrap := PanelContainer.new()
	case_grid_wrap.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 2, 3, 14))
	_case_view.add_child(case_grid_wrap)

	var cgw_m := MarginContainer.new()
	cgw_m.add_theme_constant_override("margin_left", 10)
	cgw_m.add_theme_constant_override("margin_right", 10)
	cgw_m.add_theme_constant_override("margin_top", 6)
	cgw_m.add_theme_constant_override("margin_bottom", 6)
	case_grid_wrap.add_child(cgw_m)

	var cgw_v := VBoxContainer.new()
	cgw_v.add_theme_constant_override("separation", 4)
	cgw_m.add_child(cgw_v)

	var grid_head := HBoxContainer.new()
	cgw_v.add_child(grid_head)

	_grid_title = _create_label(_t("倉庫寶石儲備盤點（各階數量）"), 18, COLOR_TEXT_DARK, true)
	_grid_title.name = "GridTitle"
	_grid_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_grid_title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	grid_head.add_child(_grid_title)

	_btn_refresh_case = Button.new()
	_btn_refresh_case.name = "BtnRefreshCase"
	_btn_refresh_case.text = _t("重新盤點")
	_btn_refresh_case.custom_minimum_size = Vector2(130, 50)
	_btn_refresh_case.add_theme_font_size_override("font_size", 16)
	_btn_refresh_case.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_refresh_case.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_refresh_case.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_refresh_case.add_theme_font_override("font", _cached_font)
	_btn_refresh_case.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 16, 2))
	_btn_refresh_case.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 16, 2))
	_btn_refresh_case.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 16, 2))
	_btn_refresh_case.pressed.connect(_refresh_case_view)
	grid_head.add_child(_btn_refresh_case)

	_btn_auto_socket = Button.new()
	_btn_auto_socket.name = "BtnAutoSocket"
	_btn_auto_socket.text = _t("一鍵鑲嵌")
	_btn_auto_socket.custom_minimum_size = Vector2(130, 50)
	_btn_auto_socket.add_theme_font_size_override("font_size", 16)
	_btn_auto_socket.add_theme_color_override("font_color", Color.WHITE)
	_btn_auto_socket.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_auto_socket.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_btn_auto_socket.add_theme_font_override("font", _cached_font)
	_btn_auto_socket.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 16, 2))
	_btn_auto_socket.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE584"), COLOR_BORDER, 5, 16, 2))
	_btn_auto_socket.add_theme_stylebox_override("pressed", _create_button_style(Color("#36B850"), COLOR_BORDER, 2, 16, 2))
	_btn_auto_socket.pressed.connect(func():
		var res: Dictionary = GemSystem.auto_socket()
		_msg_label.text = _t(str(res.get("msg", "")))
		if bool(res.get("ok", false)):
			_msg_label.add_theme_color_override("font_color", COLOR_MINT)
		else:
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
		SaveManager.save_game()
		_refresh_case_view()
	)
	grid_head.add_child(_btn_auto_socket)

	_case_grid = GridContainer.new()
	_case_grid.name = "CaseGrid"
	_case_grid.columns = 5
	_case_grid.add_theme_constant_override("h_separation", 6)
	_case_grid.add_theme_constant_override("v_separation", 4)
	_case_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	cgw_v.add_child(_case_grid)

	# 底部狀態訊息
	_msg_label = Label.new()
	_msg_label.name = "MsgLabel"
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 16)
	_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_msg_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_msg_label.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 底部離開按鈕 (按鈕高 >= 50, 金黃立體厚底 5px)
	var foot_row := HBoxContainer.new()
	foot_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(foot_row)

	_btn_close = Button.new()
	_btn_close.name = "BtnCloseGemWorkshop"
	_btn_close.text = _t("離開工坊")
	_btn_close.custom_minimum_size = Vector2(180, 50)
	_btn_close.add_theme_font_size_override("font_size", 18)
	_btn_close.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_close.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_close.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_close.add_theme_font_override("font", _cached_font)
	_btn_close.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
	_btn_close.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
	_btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
	_btn_close.pressed.connect(_on_close)
	foot_row.add_child(_btn_close)


func _switch_tab(tab: Tab) -> void:
	_current_tab = tab
	if tab == Tab.SMELT:
		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18, 2))
		_tab_smelt_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5AB3FF"), COLOR_BORDER, 5, 18, 2))
		_tab_smelt_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#268FE8"), COLOR_BORDER, 2, 18, 2))
		_tab_smelt_btn.add_theme_color_override("font_color", Color.WHITE)
		_tab_smelt_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_smelt_btn.add_theme_constant_override("outline_size", 3)

		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(Color("#F6F1E6"), COLOR_BORDER, 3, 18, 1))
		_tab_case_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#EBE3D0"), COLOR_BORDER, 3, 18, 1))
		_tab_case_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#DFD4BC"), COLOR_BORDER, 1, 18, 1))
		_tab_case_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_case_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_case_btn.add_theme_constant_override("outline_size", 0)

		_smelt_view.visible = true
		_case_view.visible = false
		_refresh_smelt_view()
	else:
		_tab_case_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18, 2))
		_tab_case_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18, 2))
		_tab_case_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 18, 2))
		_tab_case_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_case_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_case_btn.add_theme_constant_override("outline_size", 2)

		_tab_smelt_btn.add_theme_stylebox_override("normal", _create_button_style(Color("#E8F2FC"), COLOR_BORDER, 3, 18, 1))
		_tab_smelt_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#D4E6F8"), COLOR_BORDER, 3, 18, 1))
		_tab_smelt_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#C4DCF4"), COLOR_BORDER, 1, 18, 1))
		_tab_smelt_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		_tab_smelt_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_tab_smelt_btn.add_theme_constant_override("outline_size", 0)

		_smelt_view.visible = false
		_case_view.visible = true
		_refresh_case_view()


func _refresh_smelt_view() -> void:
	# 1. 刷新頂部產線橫幅
	for c in _furnace_bar.get_children():
		c.queue_free()

	var fb_m := MarginContainer.new()
	fb_m.add_theme_constant_override("margin_left", 12)
	fb_m.add_theme_constant_override("margin_right", 12)
	fb_m.add_theme_constant_override("margin_top", 6)
	fb_m.add_theme_constant_override("margin_bottom", 6)
	_furnace_bar.add_child(fb_m)

	var row1 := HBoxContainer.new()
	row1.add_theme_constant_override("separation", 10)
	fb_m.add_child(row1)

	var left_lines: int = GemSystem.smelt_left_today()
	var total_lines: int = GemSystem.smelt_lines_per_day()
	var line_info := _create_label(_t("今日熔煉產線：%d / %d 線") % [left_lines, total_lines], 18, COLOR_TEXT_DARK, true)
	row1.add_child(line_info)

	if GemSystem.furnace_unlocked():
		var furnace_tag := _create_label(_t("· 熔爐已點燃（雙線並行）"), 16, COLOR_SKY, true)
		row1.add_child(furnace_tag)
	elif GemSystem.furnace_can_unlock():
		var btn_unlock := Button.new()
		btn_unlock.text = _t("點燃熔爐")
		btn_unlock.custom_minimum_size = Vector2(100, 36)
		btn_unlock.add_theme_font_size_override("font_size", 16)
		btn_unlock.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn_unlock.add_theme_color_override("font_outline_color", COLOR_BORDER)
		btn_unlock.add_theme_constant_override("outline_size", 1)
		if _cached_font:
			btn_unlock.add_theme_font_override("font", _cached_font)
		btn_unlock.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 3, 14, 2))
		btn_unlock.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 3, 14, 2))
		btn_unlock.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 1, 14, 2))
		btn_unlock.pressed.connect(func():
			var u_res: Dictionary = GemSystem.unlock_furnace("auto")
			_msg_label.text = _t(str(u_res.get("msg", "")))
			_refresh_smelt_view()
		)
		row1.add_child(btn_unlock)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row1.add_child(spacer)

	var rule_lbl := _create_label(_t("3碎片→1級 · 3顆同級可合成"), 16, COLOR_TEXT_MUTED)
	row1.add_child(rule_lbl)

	# 2. 刷新三色寶石果凍卡片
	for c in _smelt_cards_box.get_children():
		c.queue_free()

	for col in GemSystem.COLORS:
		var card := _build_single_smelt_card(col)
		_smelt_cards_box.add_child(card)


func _build_single_smelt_card(col: String) -> PanelContainer:
	var card := PanelContainer.new()
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(225, 0)

	var bg_col := COLOR_CARD_WARM
	var title_col := COLOR_TEXT_DARK
	var sub_text := ""
	match col:
		"red":
			bg_col = COLOR_CARD_PINK
			title_col = COLOR_TEXT_PINK
			sub_text = _t("暴擊·生命")
		"yellow":
			bg_col = COLOR_CARD_GOLD
			title_col = COLOR_TEXT_GOLD
			sub_text = _t("攻擊·防禦")
		"blue":
			bg_col = COLOR_CARD_SKY
			title_col = COLOR_SKY
			sub_text = _t("命中·迴避")

	card.add_theme_stylebox_override("panel", _create_panel_style(bg_col, COLOR_BORDER, 2, 4, 16))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 10)
	m.add_theme_constant_override("margin_right", 10)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	m.add_child(v)

	# 標題與特性（單行緊湊）
	var top_row := HBoxContainer.new()
	v.add_child(top_row)

	var name_lbl := _create_label(_t(GemSystem.color_label(col)), 20, title_col, true)
	top_row.add_child(name_lbl)

	var sub_lbl := _create_label("（%s）" % sub_text, 16, COLOR_TEXT_MUTED)
	top_row.add_child(sub_lbl)

	# 碎片資訊
	var shards := GemSystem.shard_count(col)
	var shard_box := PanelContainer.new()
	shard_box.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 1, 2, 10))
	v.add_child(shard_box)

	var sm := MarginContainer.new()
	sm.add_theme_constant_override("margin_left", 8)
	sm.add_theme_constant_override("margin_right", 8)
	sm.add_theme_constant_override("margin_top", 4)
	sm.add_theme_constant_override("margin_bottom", 4)
	shard_box.add_child(sm)

	var s_row := HBoxContainer.new()
	sm.add_child(s_row)

	var s_title := _create_label(_t("碎片儲備"), 16, COLOR_TEXT_DARK)
	s_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	s_row.add_child(s_title)

	var s_num_col := COLOR_TEXT_ORANGE if shards >= 3 else COLOR_TEXT_MUTED
	var s_val := _create_label("%d / 3" % shards, 18, s_num_col, true)
	s_row.add_child(s_val)

	# 各階寶石存量摘要（單行 5 欄緊湊排版）
	var stock_row := HBoxContainer.new()
	stock_row.alignment = BoxContainer.ALIGNMENT_CENTER
	stock_row.add_theme_constant_override("separation", 4)
	v.add_child(stock_row)

	for lv in range(1, GemSystem.MAX_LEVEL + 1):
		var num: int = GemSystem.count_of(col, lv)
		var num_col := COLOR_TEXT_DARK if num > 0 else COLOR_TEXT_DIM
		var lv_lbl := _create_label(_t("%d階:%d") % [lv, num], 16, num_col, num > 0)
		stock_row.add_child(lv_lbl)

	# 操作按鈕區 (高度 >= 50px)
	var can_s: bool = GemSystem.can_smelt(col)
	var btn_smelt := Button.new()
	btn_smelt.name = "BtnSmelt_" + col
	btn_smelt.custom_minimum_size = Vector2(0, 50)
	btn_smelt.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		btn_smelt.add_theme_font_override("font", _cached_font)

	if can_s:
		# 可熔煉時主按鈕暖橘果凍厚底 5~6px
		btn_smelt.text = _t("熔煉 1 級寶石")
		btn_smelt.add_theme_color_override("font_color", Color.WHITE)
		btn_smelt.add_theme_color_override("font_outline_color", COLOR_BORDER)
		btn_smelt.add_theme_constant_override("outline_size", 4)
		btn_smelt.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 6, 16, 2))
		btn_smelt.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB030"), COLOR_BORDER, 6, 16, 2))
		btn_smelt.add_theme_stylebox_override("pressed", _create_button_style(Color("#E58A05"), COLOR_BORDER, 2, 16, 2))
		btn_smelt.pressed.connect(func():
			var res: Dictionary = GemSystem.smelt(col)
			_msg_label.text = _t(str(res.get("msg", "熔煉完成！")))
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
			SaveManager.save_game()
			_refresh_smelt_view()
		)
	else:
		btn_smelt.disabled = true
		if GemSystem.smelt_left_today() <= 0:
			btn_smelt.text = _t("今日產線已盡")
		else:
			btn_smelt.text = _t("碎片不足(需3)")
		btn_smelt.add_theme_color_override("font_color", COLOR_TEXT_DIM)
		btn_smelt.add_theme_stylebox_override("disabled", _create_disabled_button_style(16))
	v.add_child(btn_smelt)

	# 合成按鈕 (高度 >= 50px)
	var fuse_target_lv := -1
	for lv in range(1, GemSystem.MAX_LEVEL):
		if GemSystem.can_fuse(col, lv):
			fuse_target_lv = lv
			break

	var btn_fuse := Button.new()
	btn_fuse.name = "BtnFuse_" + col
	btn_fuse.custom_minimum_size = Vector2(0, 50)
	btn_fuse.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		btn_fuse.add_theme_font_override("font", _cached_font)

	if fuse_target_lv != -1:
		btn_fuse.text = _t("合成 %d 級 → %d 級") % [fuse_target_lv, fuse_target_lv + 1]
		btn_fuse.add_theme_color_override("font_color", Color.WHITE)
		btn_fuse.add_theme_color_override("font_outline_color", COLOR_BORDER)
		btn_fuse.add_theme_constant_override("outline_size", 4)
		btn_fuse.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 16, 2))
		btn_fuse.add_theme_stylebox_override("hover", _create_button_style(Color("#5AB3FF"), COLOR_BORDER, 5, 16, 2))
		btn_fuse.add_theme_stylebox_override("pressed", _create_button_style(Color("#268FE8"), COLOR_BORDER, 2, 16, 2))
		btn_fuse.pressed.connect(func():
			var res: Dictionary = GemSystem.fuse(col, fuse_target_lv)
			_msg_label.text = _t(str(res.get("msg", "合成完成！")))
			_msg_label.add_theme_color_override("font_color", COLOR_SKY)
			SaveManager.save_game()
			_refresh_smelt_view()
		)
	else:
		btn_fuse.disabled = true
		btn_fuse.text = _t("合成(需3同級)")
		btn_fuse.add_theme_color_override("font_color", COLOR_TEXT_DIM)
		btn_fuse.add_theme_stylebox_override("disabled", _create_disabled_button_style(16))
	v.add_child(btn_fuse)

	return card


func _refresh_case_view() -> void:
	var survey: Dictionary = GemSystem.inspect_gem_case()

	# 1. 孔位狀態卡片
	for c in _case_slots_row.get_children():
		c.queue_free()

	var slots: Array = survey.get("slots", [])
	for s in slots:
		var slot_card := _build_slot_card(s)
		_case_slots_row.add_child(slot_card)

	# 2. 全身加成總計
	for c in _case_bonus_panel.get_children():
		c.queue_free()

	var bm := MarginContainer.new()
	bm.add_theme_constant_override("margin_left", 12)
	bm.add_theme_constant_override("margin_right", 12)
	bm.add_theme_constant_override("margin_top", 6)
	bm.add_theme_constant_override("margin_bottom", 6)
	_case_bonus_panel.add_child(bm)

	var bv := VBoxContainer.new()
	bv.add_theme_constant_override("separation", 4)
	bm.add_child(bv)

	var bonus_title := _create_label(_t("全身穿戴寶石六維總加成"), 18, COLOR_TEXT_DARK, true)
	bv.add_child(bonus_title)

	var wb: Dictionary = survey.get("worn_bonuses", {})
	var crit_v: float = float(wb.get("crit", 0.0))
	var atk_pct_v: float = float(wb.get("atk_pct", 0.0)) * 100.0
	var hit_v: float = float(wb.get("hit", 0.0))
	var hp_pct_v: float = float(wb.get("hp_pct", 0.0)) * 100.0
	var def_pct_v: float = float(wb.get("def_pct", 0.0)) * 100.0
	var eva_v: float = float(wb.get("eva", 0.0))

	var b_grid := GridContainer.new()
	b_grid.columns = 3
	b_grid.add_theme_constant_override("h_separation", 16)
	b_grid.add_theme_constant_override("v_separation", 2)
	bv.add_child(b_grid)

	b_grid.add_child(_create_label(_t("暴擊：+%.1f") % crit_v, 16, COLOR_TEXT_PINK if crit_v > 0 else COLOR_TEXT_DARK, crit_v > 0))
	b_grid.add_child(_create_label(_t("攻擊加成：+%.1f%%") % atk_pct_v, 16, COLOR_TEXT_GOLD if atk_pct_v > 0 else COLOR_TEXT_DARK, atk_pct_v > 0))
	b_grid.add_child(_create_label(_t("命中：+%.1f") % hit_v, 16, COLOR_SKY if hit_v > 0 else COLOR_TEXT_DARK, hit_v > 0))
	b_grid.add_child(_create_label(_t("生命加成：+%.1f%%") % hp_pct_v, 16, COLOR_TEXT_PINK if hp_pct_v > 0 else COLOR_TEXT_DARK, hp_pct_v > 0))
	b_grid.add_child(_create_label(_t("防禦加成：+%.1f%%") % def_pct_v, 16, COLOR_TEXT_GOLD if def_pct_v > 0 else COLOR_TEXT_DARK, def_pct_v > 0))
	b_grid.add_child(_create_label(_t("迴避：+%.1f") % eva_v, 16, COLOR_SKY if eva_v > 0 else COLOR_TEXT_DARK, eva_v > 0))

	# 3. 寶石庫存網格 (15 種寶石小卡)
	for c in _case_grid.get_children():
		c.queue_free()

	for col in GemSystem.COLORS:
		for lv in range(1, GemSystem.MAX_LEVEL + 1):
			var num: int = GemSystem.count_of(col, lv)
			var item_card := _build_gem_inventory_cell(col, lv, num)
			_case_grid.add_child(item_card)


func _build_slot_card(s: Dictionary) -> PanelContainer:
	var card := PanelContainer.new()
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 10)
	m.add_theme_constant_override("margin_right", 10)
	m.add_theme_constant_override("margin_top", 6)
	m.add_theme_constant_override("margin_bottom", 6)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 2)
	m.add_child(v)

	var s_name := str(s.get("slot_name", ""))
	var is_eq := bool(s.get("is_equipped", false))
	var eq_name := str(s.get("equip_name", ""))
	var has_g := bool(s.get("has_gem", false))

	var head_txt := _t("%s孔位") % _t(s_name)
	if is_eq and not eq_name.is_empty():
		head_txt += "【%s】" % _t(eq_name)
	var head_lbl := _create_label(head_txt, 18, COLOR_TEXT_DARK, true)
	v.add_child(head_lbl)

	if not is_eq:
		var status_lbl := _create_label(_t("未穿戴裝備"), 16, COLOR_TEXT_MUTED)
		v.add_child(status_lbl)
	elif not has_g:
		var status_lbl := _create_label(_t("孔位閒置 · 未鑲嵌寶石"), 16, COLOR_TEXT_MUTED)
		v.add_child(status_lbl)
	else:
		var g: Dictionary = s.get("gem", {})
		var c_str := str(g.get("color", ""))
		var glabel := str(g.get("label", ""))
		var stars := str(g.get("stars", ""))
		var bname := str(g.get("bonus_name", ""))
		var btext := str(g.get("bonus_text", ""))

		var col_t := COLOR_TEXT_DARK
		match c_str:
			"red":
				col_t = COLOR_TEXT_PINK
			"yellow":
				col_t = COLOR_TEXT_GOLD
			"blue":
				col_t = COLOR_SKY

		var gem_lbl := _create_label(_t("已鑲嵌：%s (%s) · %s %s") % [glabel, _t(stars), _t(bname), btext], 16, col_t, true)
		v.add_child(gem_lbl)

	return card


func _build_gem_inventory_cell(col: String, lv: int, qty: int) -> PanelContainer:
	var cell := PanelContainer.new()
	cell.custom_minimum_size = Vector2(130, 46)
	cell.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var is_empty := qty <= 0
	var bg_col := COLOR_CARD_MUTED if is_empty else COLOR_CARD_WARM
	var border_col := COLOR_BORDER_MUTED if is_empty else COLOR_BORDER
	var text_col := COLOR_TEXT_DIM if is_empty else COLOR_TEXT_DARK
	var qty_col := COLOR_TEXT_DIM2 if is_empty else COLOR_TEXT_DARK

	if not is_empty:
		match col:
			"red":
				bg_col = COLOR_CARD_PINK
				text_col = COLOR_TEXT_PINK
			"yellow":
				bg_col = COLOR_CARD_GOLD
				text_col = COLOR_TEXT_GOLD
			"blue":
				bg_col = COLOR_CARD_SKY
				text_col = COLOR_SKY

	cell.add_theme_stylebox_override("panel", _create_panel_style(bg_col, border_col, 2, 2, 10))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 4)
	m.add_theme_constant_override("margin_right", 4)
	m.add_theme_constant_override("margin_top", 4)
	m.add_theme_constant_override("margin_bottom", 4)
	cell.add_child(m)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 1)
	m.add_child(v)

	var name_txt := _t("%s %d級") % [_t(GemSystem.color_label(col)), lv]
	var n_lbl := _create_label(name_txt, 16, text_col, not is_empty, HORIZONTAL_ALIGNMENT_CENTER)
	v.add_child(n_lbl)

	var q_txt := _t("持有 %d 顆") % qty if not is_empty else _t("0 顆")
	var q_lbl := _create_label(q_txt, 16, qty_col, not is_empty, HORIZONTAL_ALIGNMENT_CENTER)
	v.add_child(q_lbl)

	return cell


func _create_label(text: String, font_size: int = 16, color: Color = COLOR_TEXT_DARK, bold: bool = false, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> Label:
	var lbl := Label.new()
	lbl.text = text
	lbl.horizontal_alignment = align
	lbl.add_theme_font_size_override("font_size", font_size)
	lbl.add_theme_color_override("font_color", color)
	if bold:
		lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
		lbl.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		lbl.add_theme_font_override("font", _cached_font)
	return lbl


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 16) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	sb.shadow_size = 6
	sb.shadow_offset = Vector2(0, 3)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 18, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 10
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
	return sb


func _create_disabled_button_style(radius: int = 18) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_MUTED
	sb.border_color = COLOR_BORDER_MUTED
	sb.set_border_width_all(2)
	sb.border_width_bottom = 2
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 10
	return sb


func _on_close() -> void:
	closed.emit()
	queue_free()
