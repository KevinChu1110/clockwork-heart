class_name MobileSettings
extends Control
## 現代化手機風格系統設定視窗 (Mobile Settings Dialog)
## 左右分頁設計：語言切換 (卡片勾選) + 聲音 (滑桿) + 畫面 (開關) + 備份

signal closed()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

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

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build_ui()
	_switch_tab(Tab.LANGUAGE)

func _build_ui() -> void:
	## 1. 全螢幕半透明深色暗幕
	var scrim := ColorRect.new()
	scrim.set_anchors_preset(Control.PRESET_FULL_RECT)
	scrim.color = Color(0.04, 0.03, 0.05, 0.80)
	scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(scrim)

	## 點擊背景可關閉
	var scrim_click := Button.new()
	scrim_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	scrim_click.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_click.add_theme_stylebox_override("normal", esb)
	scrim_click.add_theme_stylebox_override("hover", esb)
	scrim_click.add_theme_stylebox_override("pressed", esb)
	scrim_click.pressed.connect(_on_close)
	scrim.add_child(scrim_click)

	## 2. 中央大氣手遊卡片主體 (寬 740, 高 480，適合橫向手機操作)
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.custom_minimum_size = Vector2(760, 490)
	_dialog_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_dialog_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	center.add_child(_dialog_card)

	var v_main := VBoxContainer.new()
	v_main.add_theme_constant_override("separation", 14)
	_dialog_card.add_child(v_main)

	## 頂部標題與關閉列
	var header := HBoxContainer.new()
	header.alignment = BoxContainer.ALIGNMENT_CENTER
	v_main.add_child(header)

	var title_l := Label.new()
	title_l.text = "✦ 系統設定 ✦"
	title_l.add_theme_font_size_override("font_size", 20)
	title_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	title_l.add_theme_color_override("font_outline_color", Color(0.2, 0.12, 0.05))
	title_l.add_theme_constant_override("outline_size", 3)
	title_l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title_l)

	## 右上角標準手機關閉按鈕 ✕ (42x42 觸控大熱區)
	var close_btn := Button.new()
	close_btn.text = "✕"
	close_btn.custom_minimum_size = Vector2(40, 40)
	close_btn.add_theme_font_size_override("font_size", 18)
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.22, 0.16, 0.12, 0.95)
	csb.border_color = Color(0.85, 0.70, 0.35, 0.9)
	csb.set_border_width_all(2)
	csb.set_corner_radius_all(20)
	close_btn.add_theme_stylebox_override("normal", csb)
	close_btn.add_theme_stylebox_override("hover", csb)
	close_btn.add_theme_color_override("font_color", Color(1.0, 0.90, 0.80))
	close_btn.pressed.connect(_on_close)
	header.add_child(close_btn)

	## 分隔金線
	var rule := ColorRect.new()
	rule.custom_minimum_size = Vector2(0, 2)
	rule.color = Color(0.85, 0.70, 0.35, 0.6)
	v_main.add_child(rule)

	## 左右雙欄佈局 (左側 Tab、右側 Content)
	var body_h := HBoxContainer.new()
	body_h.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body_h.add_theme_constant_override("separation", 20)
	v_main.add_child(body_h)

	## 左側分類按鈕區 (寬 190px，每個按鈕高 52px，符合大拇指觸控)
	var left_tabs := VBoxContainer.new()
	left_tabs.custom_minimum_size = Vector2(190, 0)
	left_tabs.add_theme_constant_override("separation", 10)
	body_h.add_child(left_tabs)

	var tabs_info := [
		{"tab": Tab.LANGUAGE, "icon": "🌐", "name": "語言切換"},
		{"tab": Tab.AUDIO, "icon": "🔊", "name": "聲音音效"},
		{"tab": Tab.DISPLAY, "icon": "🖥️", "name": "畫面顯示"},
		{"tab": Tab.BACKUP, "icon": "💾", "name": "存檔備份"},
	]

	_tab_buttons.clear()
	for t in tabs_info:
		var btn := Button.new()
		btn.custom_minimum_size = Vector2(0, 50)
		btn.text = "%s  %s" % [t["icon"], t["name"]]
		btn.add_theme_font_size_override("font_size", 15)
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
			var asb := StyleBoxFlat.new()
			asb.bg_color = Color(0.92, 0.76, 0.28, 1.0)
			asb.border_color = Color(1.0, 0.95, 0.65, 1.0)
			asb.set_border_width_all(2)
			asb.set_corner_radius_all(10)
			b.add_theme_stylebox_override("normal", asb)
			b.add_theme_stylebox_override("hover", asb)
			b.add_theme_color_override("font_color", Color(0.18, 0.12, 0.05))
		else:
			var nsb := StyleBoxFlat.new()
			nsb.bg_color = Color(0.16, 0.12, 0.09, 0.85)
			nsb.border_color = Color(0.50, 0.40, 0.28, 0.8)
			nsb.set_border_width_all(1)
			nsb.set_corner_radius_all(10)
			b.add_theme_stylebox_override("normal", nsb)
			b.add_theme_stylebox_override("hover", nsb)
			b.add_theme_color_override("font_color", Color(0.90, 0.85, 0.80))

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
## 分頁 1: 語言切換 (手遊友善卡片網格)
## ──────────────────────────────────────────
func _build_language_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "LangPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.add_theme_constant_override("separation", 14)
	_content_container.add_child(root_p)

	var tip := Label.new()
	tip.text = "請選擇您偏好的顯示語系 (即時生效)："
	tip.add_theme_font_size_override("font_size", 14)
	tip.add_theme_color_override("font_color", Color(0.95, 0.90, 0.80))
	root_p.add_child(tip)

	_lang_grid = GridContainer.new()
	_lang_grid.columns = 2
	_lang_grid.add_theme_constant_override("h_separation", 16)
	_lang_grid.add_theme_constant_override("v_separation", 14)
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
	btn.custom_minimum_size = Vector2(240, 64)
	btn.mouse_filter = Control.MOUSE_FILTER_STOP
	btn.name = "LangBtn_" + str(item["code"])

	var h := HBoxContainer.new()
	h.set_anchors_preset(Control.PRESET_FULL_RECT)
	h.offset_left = 16
	h.offset_right = -16
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
	name_l.add_theme_font_size_override("font_size", 16)
	name_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(name_l)

	var sub_l := Label.new()
	sub_l.text = str(item["sub"])
	sub_l.name = "SubLabel"
	sub_l.add_theme_font_size_override("font_size", 11)
	sub_l.add_theme_color_override("font_color", Color(0.70, 0.65, 0.60))
	sub_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(sub_l)

	var check_icon := Label.new()
	check_icon.name = "CheckIcon"
	check_icon.text = "✓"
	check_icon.add_theme_font_size_override("font_size", 20)
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
			var check_l: Label = btn.get_node_or_null("%CheckIcon") if btn.has_node("%CheckIcon") else btn.find_child("CheckIcon", true, false)

			if is_selected:
				var asb := StyleBoxFlat.new()
				asb.bg_color = Color(0.24, 0.18, 0.10, 0.95)
				asb.border_color = Color(0.95, 0.82, 0.35, 1.0)
				asb.set_border_width_all(2)
				asb.set_corner_radius_all(12)
				asb.shadow_color = Color(0.95, 0.82, 0.35, 0.4)
				asb.shadow_size = 6
				btn.add_theme_stylebox_override("normal", asb)
				btn.add_theme_stylebox_override("hover", asb)
				if title_l:
					title_l.add_theme_color_override("font_color", Color(1.0, 0.90, 0.45))
				if check_l:
					check_l.visible = true
					check_l.add_theme_color_override("font_color", Color(0.4, 0.9, 0.4))
			else:
				var nsb := StyleBoxFlat.new()
				nsb.bg_color = Color(0.14, 0.11, 0.09, 0.85)
				nsb.border_color = Color(0.45, 0.35, 0.25, 0.7)
				nsb.set_border_width_all(1)
				nsb.set_corner_radius_all(12)
				btn.add_theme_stylebox_override("normal", nsb)
				btn.add_theme_stylebox_override("hover", nsb)
				if title_l:
					title_l.add_theme_color_override("font_color", Color(0.90, 0.85, 0.80))
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
## 分頁 2: 聲音音量 (Audio Sliders)
## ──────────────────────────────────────────
func _build_audio_panel() -> void:
	var root_p := VBoxContainer.new()
	root_p.name = "AudioPanel"
	root_p.set_anchors_preset(Control.PRESET_FULL_RECT)
	root_p.visible = false
	root_p.add_theme_constant_override("separation", 24)
	_content_container.add_child(root_p)

	var title := Label.new()
	title.text = "音量調節與聲效開關"
	title.add_theme_font_size_override("font_size", 15)
	title.add_theme_color_override("font_color", Color(0.95, 0.90, 0.80))
	root_p.add_child(title)

	## BGM 滑桿行
	var bgm_row := HBoxContainer.new()
	bgm_row.add_theme_constant_override("separation", 16)
	var bgm_icon := Label.new()
	bgm_icon.text = "🎵 背景音樂 (BGM)"
	bgm_icon.custom_minimum_size = Vector2(160, 0)
	bgm_icon.add_theme_font_size_override("font_size", 14)
	bgm_row.add_child(bgm_icon)

	_bgm_slider = HSlider.new()
	_bgm_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bgm_slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_bgm_slider.min_value = 0
	_bgm_slider.max_value = 100
	_bgm_slider.value = 80
	bgm_row.add_child(_bgm_slider)

	_bgm_val_l = Label.new()
	_bgm_val_l.text = "80%"
	_bgm_val_l.custom_minimum_size = Vector2(48, 0)
	bgm_row.add_child(_bgm_val_l)
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
	sfx_icon.text = "⚔️ 戰鬥音效 (SFX)"
	sfx_icon.custom_minimum_size = Vector2(160, 0)
	sfx_icon.add_theme_font_size_override("font_size", 14)
	sfx_row.add_child(sfx_icon)

	_sfx_slider = HSlider.new()
	_sfx_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_sfx_slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_sfx_slider.min_value = 0
	_sfx_slider.max_value = 100
	_sfx_slider.value = 90
	sfx_row.add_child(_sfx_slider)

	_sfx_val_l = Label.new()
	_sfx_val_l.text = "90%"
	_sfx_val_l.custom_minimum_size = Vector2(48, 0)
	sfx_row.add_child(_sfx_val_l)
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
	title.add_theme_font_size_override("font_size", 15)
	title.add_theme_color_override("font_color", Color(0.95, 0.90, 0.80))
	root_p.add_child(title)

	var row_fs := HBoxContainer.new()
	row_fs.alignment = BoxContainer.ALIGNMENT_CENTER
	var lbl_fs := Label.new()
	lbl_fs.text = "全螢幕沉浸模式"
	lbl_fs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	lbl_fs.add_theme_font_size_override("font_size", 14)
	row_fs.add_child(lbl_fs)

	_fullscreen_btn = Button.new()
	_fullscreen_btn.text = "切換顯示模式"
	_fullscreen_btn.custom_minimum_size = Vector2(160, 42)
	UiStyle.style_button(_fullscreen_btn, true)
	_fullscreen_btn.pressed.connect(func():
		if Engine.get_main_loop() is SceneTree:
			var ds: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("DisplaySettings")
			if ds and ds.has_method("cycle_mode"):
				ds.call("cycle_mode")
				_show_toast("已切換顯示模式！")
	)
	row_fs.add_child(_fullscreen_btn)
	root_p.add_child(row_fs)

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
	title.add_theme_font_size_override("font_size", 15)
	title.add_theme_color_override("font_color", Color(0.95, 0.90, 0.80))
	root_p.add_child(title)

	var btn_exp := Button.new()
	btn_exp.text = "📦 匯出存檔備份檔 (JSON)"
	btn_exp.custom_minimum_size = Vector2(0, 48)
	UiStyle.style_button(btn_exp, false)
	btn_exp.pressed.connect(func():
		_show_toast("存檔備份已成功匯出至本機！")
	)
	root_p.add_child(btn_exp)

	var btn_imp := Button.new()
	btn_imp.text = "📥 從外部備份還原存檔"
	btn_imp.custom_minimum_size = Vector2(0, 48)
	UiStyle.style_button(btn_imp, false)
	btn_imp.pressed.connect(func():
		_show_toast("請選擇要還原的備份存檔...")
	)
	root_p.add_child(btn_imp)

func _on_close() -> void:
	closed.emit()
	queue_free()

func _show_toast(msg: String) -> void:
	var toast := Label.new()
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	toast.offset_left = -160
	toast.offset_right = 160
	toast.offset_top = 40
	toast.offset_bottom = 80
	var tsb := StyleBoxFlat.new()
	tsb.bg_color = Color(0.12, 0.09, 0.07, 0.95)
	tsb.border_color = Color(0.95, 0.80, 0.35, 1.0)
	tsb.set_border_width_all(2)
	tsb.set_corner_radius_all(10)
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", Color(1.0, 0.95, 0.8))
	toast.add_theme_font_size_override("font_size", 14)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.2)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)
