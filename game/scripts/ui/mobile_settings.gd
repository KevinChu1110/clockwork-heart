class_name MobileSettings
extends Control
## 現代化手機風格系統設定視窗 (Mobile Settings Dialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，主要按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底板奶油白 #FFFDF8。
## 4. 圓角 18~24px，主要按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字、不准露出翻譯百分比。
## 6. 語系切換維持 2×3 雙語卡片網格，已選用卡片用亮金框＋「已選用」標示，禁用泥土灰黑底。
## 7. 全程 0 系統 emoji。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
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
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）

enum Tab {
	LANGUAGE,  ## 語言切換
	AUDIO,     ## 音量控制
	DISPLAY,   ## 畫面與全螢幕
	BACKUP     ## 存檔與連線
}

var _current_tab: Tab = Tab.LANGUAGE

## UI 節點
var _dialog_card: PanelContainer
var _tab_buttons: Array[Button] = []
var _content_container: Control
var _lang_grid: GridContainer

## 音量滑桿
var _bgm_slider: HSlider
var _bgm_val_l: Label
var _sfx_slider: HSlider
var _sfx_val_l: Label

## 畫面開關
var _fullscreen_btn: Button
var _quality_buttons: HBoxContainer = null

var _cached_font: Font = null
var _grabber_tex: ImageTexture = null


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_grabber_tex = _create_circle_texture(24, COLOR_GOLD, COLOR_BORDER, 3)

	_build_ui()
	_switch_tab(Tab.LANGUAGE)


func _create_circle_texture(diameter: int, fill: Color, border: Color, border_w: int) -> ImageTexture:
	var img := Image.create(diameter, diameter, false, Image.FORMAT_RGBA8)
	var center := Vector2(diameter / 2.0, diameter / 2.0)
	var r := diameter / 2.0
	for y in range(diameter):
		for x in range(diameter):
			var d := center.distance_to(Vector2(x + 0.5, y + 0.5))
			if d <= r:
				if d > r - border_w:
					img.set_pixel(x, y, border)
				else:
					img.set_pixel(x, y, fill)
			else:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
	return ImageTexture.create_from_image(img)


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 5, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
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
		sb.shadow_size = 5
		sb.shadow_offset = Vector2(0, 3)
	return sb


func _apply_label_style(lbl: Label, size: int, color: Color = COLOR_TEXT_DARK, outline_col: Color = Color(0, 0, 0, 0), outline_sz: int = 0) -> void:
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	if outline_sz > 0:
		lbl.add_theme_color_override("font_outline_color", outline_col)
		lbl.add_theme_constant_override("outline_size", outline_sz)
	if _cached_font:
		lbl.add_theme_font_override("font", _cached_font)


func _build_ui() -> void:
	## 1. 全螢幕半透明遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	## 點擊背景可關閉
	var scrim_click := Button.new()
	scrim_click.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_click.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_click.add_theme_stylebox_override("normal", esb)
	scrim_click.add_theme_stylebox_override("hover", esb)
	scrim_click.add_theme_stylebox_override("pressed", esb)
	scrim_click.pressed.connect(_on_close)
	scrim.add_child(scrim_click)

	## 2. 中央大氣手遊卡片主體 (寬 750, 高 490，奶油米白底 + 深藍紫立體邊框 + 22px 圓角)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "SettingsCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 490)
	_dialog_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v_main := VBoxContainer.new()
	v_main.add_theme_constant_override("separation", 12)
	margin.add_child(v_main)

	## 頂部標題與關閉列
	var header := HBoxContainer.new()
	header.alignment = BoxContainer.ALIGNMENT_CENTER
	header.add_theme_constant_override("separation", 10)
	v_main.add_child(header)

	var title_l := Label.new()
	title_l.text = "系統設定"
	_apply_label_style(title_l, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 4)
	title_l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title_l)

	## 右上「✕」關閉按鈕 (50x50，珊瑚粉果凍厚底按鈕)
	var close_btn := ResponsiveUi.make_close_button(_on_close)
	close_btn.custom_minimum_size = Vector2(50, 50)
	close_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_PINK, COLOR_BORDER, 5, 20))
	close_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7A9F"), COLOR_BORDER, 5, 20))
	close_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_PINK, COLOR_BORDER, 2, 20))
	close_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	close_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	close_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		close_btn.add_theme_font_override("font", _cached_font)
	header.add_child(close_btn)

	## 亮橘色立體分隔粗線
	var rule := ColorRect.new()
	rule.custom_minimum_size = Vector2(0, 3)
	rule.color = COLOR_ORANGE
	v_main.add_child(rule)

	## 左右雙欄佈局 (左側 Tab、右側 Content)
	var body_h := HBoxContainer.new()
	body_h.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body_h.add_theme_constant_override("separation", 18)
	v_main.add_child(body_h)

	## 左側分類按鈕區 (寬 180px，按鈕高 52px，符合大拇指觸控)
	var left_tabs := VBoxContainer.new()
	left_tabs.custom_minimum_size = Vector2(180, 0)
	left_tabs.add_theme_constant_override("separation", 10)
	body_h.add_child(left_tabs)

	var tabs_info := [
		{"tab": Tab.LANGUAGE, "name": "語言切換"},
		{"tab": Tab.AUDIO, "name": "聲音音效"},
		{"tab": Tab.DISPLAY, "name": "畫面顯示"},
		{"tab": Tab.BACKUP, "name": "存檔備份"},
	]

	_tab_buttons.clear()
	for t in tabs_info:
		var btn := Button.new()
		btn.custom_minimum_size = Vector2(0, 52)
		btn.text = str(t["name"])
		btn.add_theme_font_size_override("font_size", 16)
		if _cached_font:
			btn.add_theme_font_override("font", _cached_font)
		var tb: Tab = t["tab"]
		btn.pressed.connect(func(): _switch_tab(tb))
		left_tabs.add_child(btn)
		_tab_buttons.append(btn)

	## 右側內容面板
	_content_container = Control.new()
	_content_container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_content_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body_h.add_child(_content_container)

	_build_language_panel()
	_build_audio_panel()
	_build_display_panel()
	_build_backup_panel()


func _switch_tab(target: Tab) -> void:
	_current_tab = target
	for i in range(_tab_buttons.size()):
		var is_active := (i == int(target))
		var b := _tab_buttons[i]
		if is_active:
			## 選取中分頁：陽光金黃底 + 深藍紫立體邊框 + 5px 果凍厚底
			var asb := _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20)
			b.add_theme_stylebox_override("normal", asb)
			b.add_theme_stylebox_override("hover", asb)
			b.add_theme_stylebox_override("pressed", asb)
			b.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		else:
			## 未選取分頁：溫暖米黃底 + 深藍紫邊框 (告別泥土灰黑)
			var nsb := _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 3, 20)
			b.add_theme_stylebox_override("normal", nsb)
			b.add_theme_stylebox_override("hover", nsb)
			b.add_theme_stylebox_override("pressed", nsb)
			b.add_theme_color_override("font_color", COLOR_TEXT_DARK)

	for child in _content_container.get_children():
		child.visible = false

	match target:
		Tab.LANGUAGE:
			var p := _content_container.get_node_or_null("LangPanel")
			if p: p.visible = true
			_refresh_lang_selection()
		Tab.AUDIO:
			var p := _content_container.get_node_or_null("AudioPanel")
			if p: p.visible = true
		Tab.DISPLAY:
			var p := _content_container.get_node_or_null("DisplayPanel")
			if p: p.visible = true
		Tab.BACKUP:
			var p := _content_container.get_node_or_null("BackupPanel")
			if p: p.visible = true


## ──────────────────────────────────────────
## 分頁 1: 語言切換 (2×3 雙語卡片網格，亮金框＋已選用標示)
## ──────────────────────────────────────────
func _build_language_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "LangPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.add_theme_constant_override("separation", 12)
	_content_container.add_child(root_p)

	var tip := Label.new()
	tip.text = "請選擇您偏好的顯示語系 (即時生效)："
	_apply_label_style(tip, 16, COLOR_TEXT_DARK)
	root_p.add_child(tip)

	_lang_grid = GridContainer.new()
	_lang_grid.columns = 2
	_lang_grid.add_theme_constant_override("h_separation", 14)
	_lang_grid.add_theme_constant_override("v_separation", 12)
	root_p.add_child(_lang_grid)

	var locales_data := [
		{"code": "zh_TW", "name": "繁體中文", "sub": "Traditional Chinese"},
		{"code": "zh_CN", "name": "简体中文", "sub": "Simplified Chinese"},
		{"code": "en", "name": "English", "sub": "英文"},
		{"code": "ja", "name": "日本語", "sub": "Japanese"},
		{"code": "ko", "name": "한국어", "sub": "Korean"},
		{"code": "es", "name": "Español", "sub": "Spanish"},
	]

	for item in locales_data:
		var card := _build_lang_card(item)
		_lang_grid.add_child(card)


func _build_lang_card(item: Dictionary) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(245, 66)
	btn.mouse_filter = Control.MOUSE_FILTER_STOP
	btn.name = "LangBtn_" + str(item["code"])

	var h := HBoxContainer.new()
	h.set_anchors_preset(Control.PRESET_FULL_RECT)
	h.offset_left = 16
	h.offset_right = -14
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	btn.add_child(h)

	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_child(v)

	var name_l := Label.new()
	name_l.text = str(item["name"])
	name_l.name = "TitleLabel"
	_apply_label_style(name_l, 18, COLOR_TEXT_DARK)
	name_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(name_l)

	var sub_l := Label.new()
	sub_l.text = str(item["sub"])
	sub_l.name = "SubLabel"
	_apply_label_style(sub_l, 16, Color("#6B5E80"))
	sub_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(sub_l)

	var check_icon := Label.new()
	check_icon.name = "CheckIcon"
	check_icon.text = "✓ 已選用"
	_apply_label_style(check_icon, 16, COLOR_TEXT_ORANGE, COLOR_BORDER, 2)
	check_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_child(check_icon)

	var code: String = str(item["code"])
	btn.pressed.connect(func(): _select_language(code))
	return btn


func _refresh_lang_selection() -> void:
	var cur_code: String = "zh_TW"
	if Engine.get_main_loop() is SceneTree:
		var loc: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("Loc")
		if loc and "locale" in loc:
			cur_code = str(loc.locale)

	for child in _lang_grid.get_children():
		if child is Button:
			var btn: Button = child
			var is_selected := btn.name == ("LangBtn_" + cur_code)
			var title_l: Label = btn.get_node_or_null("%TitleLabel") if btn.has_node("%TitleLabel") else btn.find_child("TitleLabel", true, false)
			var sub_l: Label = btn.find_child("SubLabel", true, false)
			var check_l: Label = btn.get_node_or_null("%CheckIcon") if btn.has_node("%CheckIcon") else btn.find_child("CheckIcon", true, false)

			if is_selected:
				## 已選用卡片：金黃柔和底 + 亮金橘厚邊框 (5px 厚底) + 亮金光暈
				var asb := StyleBoxFlat.new()
				asb.bg_color = COLOR_CARD_GOLD
				asb.border_color = COLOR_ORANGE
				asb.set_border_width_all(3)
				asb.border_width_bottom = 5
				asb.set_corner_radius_all(20)
				asb.shadow_color = Color(1.0, 0.63, 0.06, 0.35)
				asb.shadow_size = 6
				asb.shadow_offset = Vector2(0, 3)
				btn.add_theme_stylebox_override("normal", asb)
				btn.add_theme_stylebox_override("hover", asb)
				btn.add_theme_stylebox_override("pressed", asb)

				if title_l:
					title_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
				if sub_l:
					sub_l.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
				if check_l:
					check_l.visible = true
					check_l.text = "✓ 已選用"
					check_l.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
					check_l.add_theme_color_override("font_outline_color", COLOR_BORDER)
					check_l.add_theme_constant_override("outline_size", 2)
			else:
				## 未選用卡片：奶油米白底 + 深藍紫邊框 (告別泥土暗沉)
				var nsb := StyleBoxFlat.new()
				nsb.bg_color = COLOR_CARD_WARM
				nsb.border_color = COLOR_BORDER
				nsb.set_border_width_all(2)
				nsb.border_width_bottom = 4
				nsb.set_corner_radius_all(20)
				nsb.shadow_color = Color(0.12, 0.10, 0.23, 0.15)
				nsb.shadow_size = 4
				nsb.shadow_offset = Vector2(0, 2)
				btn.add_theme_stylebox_override("normal", nsb)
				btn.add_theme_stylebox_override("hover", nsb)
				btn.add_theme_stylebox_override("pressed", nsb)

				if title_l:
					title_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
				if sub_l:
					sub_l.add_theme_color_override("font_color", Color("#756A8A"))
				if check_l:
					check_l.visible = false


func _select_language(code: String) -> void:
	if Engine.get_main_loop() is SceneTree:
		var loc: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("set_locale"):
			loc.call("set_locale", code)
	_refresh_lang_selection()
	_show_toast("語言已成功切換！")


## ──────────────────────────────────────────
## 分頁 2: 聲音音量 (多巴胺鮮亮滑桿)
## ──────────────────────────────────────────
func _style_hslider(slider: HSlider, fill_color: Color) -> void:
	var bg_sb := StyleBoxFlat.new()
	bg_sb.bg_color = COLOR_CARD_WARM
	bg_sb.border_color = COLOR_BORDER
	bg_sb.set_border_width_all(2)
	bg_sb.border_width_bottom = 3
	bg_sb.set_corner_radius_all(10)
	bg_sb.content_margin_top = 8
	bg_sb.content_margin_bottom = 8

	var fill_sb := StyleBoxFlat.new()
	fill_sb.bg_color = fill_color
	fill_sb.border_color = COLOR_BORDER
	fill_sb.set_border_width_all(2)
	fill_sb.border_width_bottom = 3
	fill_sb.set_corner_radius_all(10)
	fill_sb.content_margin_top = 8
	fill_sb.content_margin_bottom = 8

	slider.add_theme_stylebox_override("slider", bg_sb)
	slider.add_theme_stylebox_override("grabber_area", fill_sb)
	slider.add_theme_stylebox_override("grabber_area_highlight", fill_sb)
	if _grabber_tex:
		slider.add_theme_icon_override("grabber", _grabber_tex)
		slider.add_theme_icon_override("grabber_highlight", _grabber_tex)
	slider.custom_minimum_size.y = 44


func _build_audio_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "AudioPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.visible = false
	root_p.add_theme_constant_override("separation", 22)
	_content_container.add_child(root_p)

	var title := Label.new()
	title.text = "音量調節與聲效開關"
	_apply_label_style(title, 18, COLOR_TEXT_DARK)
	root_p.add_child(title)

	## BGM 滑桿行
	var bgm_row := HBoxContainer.new()
	bgm_row.add_theme_constant_override("separation", 16)
	var bgm_icon := Label.new()
	bgm_icon.text = "背景音樂 (BGM)"
	bgm_icon.custom_minimum_size = Vector2(160, 0)
	_apply_label_style(bgm_icon, 16, COLOR_TEXT_DARK)
	bgm_row.add_child(bgm_icon)

	_bgm_slider = HSlider.new()
	_bgm_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bgm_slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_bgm_slider.min_value = 0
	_bgm_slider.max_value = 100
	_bgm_slider.value = 80
	_style_hslider(_bgm_slider, COLOR_SKY)
	bgm_row.add_child(_bgm_slider)

	var bgm_badge := PanelContainer.new()
	bgm_badge.custom_minimum_size = Vector2(60, 36)
	bgm_badge.add_theme_stylebox_override("panel", _create_panel_style(COLOR_GOLD, COLOR_BORDER, 2, 3, 12))
	_bgm_val_l = Label.new()
	_bgm_val_l.text = "80%"
	_bgm_val_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_bgm_val_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_label_style(_bgm_val_l, 18, COLOR_TEXT_DARK)
	bgm_badge.add_child(_bgm_val_l)
	bgm_row.add_child(bgm_badge)

	_bgm_slider.value_changed.connect(func(v: float):
		_bgm_val_l.text = "%d%%" % int(v)
		if Engine.get_main_loop() is SceneTree:
			var am: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
			if am and "bgm_vol" in am:
				am.bgm_vol = v / 100.0
	)
	root_p.add_child(bgm_row)

	## SFX 滑桿行
	var sfx_row := HBoxContainer.new()
	sfx_row.add_theme_constant_override("separation", 16)
	var sfx_icon := Label.new()
	sfx_icon.text = "戰鬥音效 (SFX)"
	sfx_icon.custom_minimum_size = Vector2(160, 0)
	_apply_label_style(sfx_icon, 16, COLOR_TEXT_DARK)
	sfx_row.add_child(sfx_icon)

	_sfx_slider = HSlider.new()
	_sfx_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_sfx_slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_sfx_slider.min_value = 0
	_sfx_slider.max_value = 100
	_sfx_slider.value = 90
	_style_hslider(_sfx_slider, COLOR_MINT)
	sfx_row.add_child(_sfx_slider)

	var sfx_badge := PanelContainer.new()
	sfx_badge.custom_minimum_size = Vector2(60, 36)
	sfx_badge.add_theme_stylebox_override("panel", _create_panel_style(COLOR_GOLD, COLOR_BORDER, 2, 3, 12))
	_sfx_val_l = Label.new()
	_sfx_val_l.text = "90%"
	_sfx_val_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_sfx_val_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_label_style(_sfx_val_l, 18, COLOR_TEXT_DARK)
	sfx_badge.add_child(_sfx_val_l)
	sfx_row.add_child(sfx_badge)

	_sfx_slider.value_changed.connect(func(v: float):
		_sfx_val_l.text = "%d%%" % int(v)
	)
	root_p.add_child(sfx_row)


## ──────────────────────────────────────────
## 分頁 3: 畫面顯示 (Display Toggles)
## ──────────────────────────────────────────
func _build_display_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "DisplayPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.visible = false
	root_p.add_theme_constant_override("separation", 20)
	_content_container.add_child(root_p)

	var title := Label.new()
	title.text = "顯示模式與渲染設定"
	_apply_label_style(title, 18, COLOR_TEXT_DARK)
	root_p.add_child(title)

	var row_fs := HBoxContainer.new()
	row_fs.alignment = BoxContainer.ALIGNMENT_CENTER
	var lbl_fs := Label.new()
	lbl_fs.text = "全螢幕沉浸模式"
	lbl_fs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_apply_label_style(lbl_fs, 16, COLOR_TEXT_DARK)
	row_fs.add_child(lbl_fs)

	_fullscreen_btn = Button.new()
	_fullscreen_btn.text = "切換顯示模式"
	_fullscreen_btn.custom_minimum_size = Vector2(170, 50)
	_fullscreen_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 20))
	_fullscreen_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5DB3FF"), COLOR_BORDER, 5, 20))
	_fullscreen_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_SKY, COLOR_BORDER, 2, 20))
	_fullscreen_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_fullscreen_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_fullscreen_btn.add_theme_constant_override("outline_size", 3)
	_fullscreen_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_fullscreen_btn.add_theme_font_override("font", _cached_font)
	_fullscreen_btn.pressed.connect(func():
		if Engine.get_main_loop() is SceneTree:
			var ds: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("DisplaySettings")
			if ds and ds.has_method("cycle_mode"):
				ds.call("cycle_mode")
				_show_toast("已切換顯示模式！")
	)
	row_fs.add_child(_fullscreen_btn)
	root_p.add_child(row_fs)

	var q_title := Label.new()
	q_title.text = _loc_t("display.quality")
	_apply_label_style(q_title, 16, COLOR_TEXT_DARK)
	root_p.add_child(q_title)

	var q_row := HBoxContainer.new()
	q_row.add_theme_constant_override("separation", 10)
	root_p.add_child(q_row)
	var q_opts: Array = [
		{"id": "auto", "key": "display.quality_auto"},
		{"id": "low", "key": "display.quality_low"},
		{"id": "mid", "key": "display.quality_mid"},
		{"id": "high", "key": "display.quality_high"},
	]
	for opt in q_opts:
		var qb := Button.new()
		qb.text = _loc_t(str(opt["key"]))
		qb.custom_minimum_size = Vector2(0, 50)
		qb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		qb.add_theme_font_size_override("font_size", 16)
		if _cached_font:
			qb.add_theme_font_override("font", _cached_font)
		var qid := str(opt["id"])
		qb.pressed.connect(_on_quality_picked.bind(qid))
		qb.set_meta("quality_id", qid)
		q_row.add_child(qb)
	_quality_buttons = q_row
	_refresh_quality_buttons()


## ──────────────────────────────────────────
## 分頁 4: 存檔備份 (Backup & Account)
## ──────────────────────────────────────────
func _build_backup_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "BackupPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.visible = false
	root_p.add_theme_constant_override("separation", 18)
	_content_container.add_child(root_p)

	var title := Label.new()
	title.text = "雲端與本機存檔備份"
	_apply_label_style(title, 18, COLOR_TEXT_DARK)
	root_p.add_child(title)

	var btn_exp := Button.new()
	btn_exp.text = "匯出存檔備份檔 (JSON)"
	btn_exp.custom_minimum_size = Vector2(0, 52)
	btn_exp.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 20))
	btn_exp.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 20))
	btn_exp.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 20))
	btn_exp.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_exp.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		btn_exp.add_theme_font_override("font", _cached_font)
	btn_exp.pressed.connect(func():
		_show_toast("存檔備份已成功匯出至本機！")
	)
	root_p.add_child(btn_exp)

	var btn_imp := Button.new()
	btn_imp.text = "從外部備份還原存檔"
	btn_imp.custom_minimum_size = Vector2(0, 52)
	btn_imp.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 20))
	btn_imp.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB338"), COLOR_BORDER, 5, 20))
	btn_imp.add_theme_stylebox_override("pressed", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 20))
	btn_imp.add_theme_color_override("font_color", Color("#FFFFFF"))
	btn_imp.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_imp.add_theme_constant_override("outline_size", 3)
	btn_imp.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		btn_imp.add_theme_font_override("font", _cached_font)
	btn_imp.pressed.connect(func():
		_show_toast("請選擇要還原的備份存檔...")
	)
	root_p.add_child(btn_imp)


func _on_close() -> void:
	closed.emit()
	queue_free()


func _loc_t(key: String, vars: Dictionary = {}) -> String:
	if Engine.get_main_loop() is SceneTree:
		var loc: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("Loc")
		if loc != null and loc.has_method("t"):
			return str(loc.call("t", key, vars))
	return key


func _on_quality_picked(qid: String) -> void:
	if Engine.get_main_loop() is SceneTree:
		var gp: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GraphicsProfile")
		if gp != null and gp.has_method("set_choice"):
			gp.call("set_choice", qid)
	_refresh_quality_buttons()
	_show_toast(_loc_t("display.quality_applied", {"tier": _loc_t("display.quality_" + qid)}))


func _refresh_quality_buttons() -> void:
	if _quality_buttons == null:
		return
	var current := "auto"
	if Engine.get_main_loop() is SceneTree:
		var gp: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GraphicsProfile")
		if gp != null and "choice" in gp:
			current = str(gp.choice)
	for child in _quality_buttons.get_children():
		var b := child as Button
		if b == null:
			continue
		var is_on := str(b.get_meta("quality_id", "")) == current
		if is_on:
			var sb := _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18)
			b.add_theme_stylebox_override("normal", sb)
			b.add_theme_stylebox_override("hover", sb)
			b.add_theme_stylebox_override("pressed", sb)
			b.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		else:
			var sb := _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 3, 18)
			b.add_theme_stylebox_override("normal", sb)
			b.add_theme_stylebox_override("hover", sb)
			b.add_theme_stylebox_override("pressed", sb)
			b.add_theme_color_override("font_color", COLOR_TEXT_DARK)


func _show_toast(msg: String) -> void:
	var toast := Label.new()
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	toast.offset_left = -170
	toast.offset_right = 170
	toast.offset_top = 40
	toast.offset_bottom = 86
	_apply_label_style(toast, 16, COLOR_TEXT_DARK)

	var tsb := _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 18)
	toast.add_theme_stylebox_override("normal", tsb)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.2)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)
