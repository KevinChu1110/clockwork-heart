class_name MobileLobby
extends Control
## 勇者之魂 (Brave Soul) - 現代多巴胺手遊風格大廳 (Tata Adventure Style)
## 視覺標準：超大觸控尺寸 + 飽滿果凍立體按鈕 + 多巴胺鮮亮高飽和配色 + 圓角胖胖字體

signal request_battle(mode: String)
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

enum Tab {
	VILLAGE,     ## 今日村莊大廳 (主城)
	CHARACTER,   ## 角色 / 三欄武器紙娃娃
	ADVENTURE,   ## 出征四地區關卡
	SOUL_HALL,   ## 聚魂殿 (五色葫蘆跳階)
	BAG          ## 冒險背包
}

var _current_tab: Tab = Tab.VILLAGE

## 頂部數值標籤
var _lv_label: Label
var _name_label: Label
var _power_label: Label
var _energy_label: Label
var _gold_label: Label
var _gem_label: Label

## 容器節點
var _content_root: Control
var _village_layer: Control
var _char_layer: Control
var _adventure_layer: Control
var _soul_layer: Control
var _bag_layer: Control
var _dock_buttons: Array[Button] = []

## 角色展台
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _breathe_tween: Tween

## 聚魂殿五色葫蘆狀態
var _gourd_lit: Array[bool] = [true, false, false, false, false]
var _gourd_btns: Array[Button] = []

## 四地區出征
var _selected_region: int = 1 # 0: 破曉之原, 1: 聖獅王都, 2: 迷霧雪境, 3: 深淵龍窟
var _stages_container: VBoxContainer

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func _ready() -> void:
	custom_minimum_size = Vector2(1280, 720)
	size = Vector2(1280, 720)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build_ui()
	refresh_hud()
	_switch_tab(Tab.VILLAGE)

func _build_ui() -> void:
	## 1. 背景插畫 (明亮飽和的童話主城)
	var bg := TextureRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	elif ResourceLoader.exists("res://assets/sprites/illustrations/title_bg.png"):
		bg.texture = load("res://assets/sprites/illustrations/title_bg.png")
	add_child(bg)

	## 頂部與底部通透暗紫漸層遮罩 (消除老舊黑霧)
	var top_v := ColorRect.new()
	top_v.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_v.offset_bottom = 120
	top_v.color = Color(0.10, 0.08, 0.22, 0.40)
	top_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(top_v)

	var bot_v := ColorRect.new()
	bot_v.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bot_v.offset_top = -140
	bot_v.color = Color(0.10, 0.08, 0.22, 0.50)
	bot_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bot_v)

	## 2. 內容掛載層
	_content_root = Control.new()
	_content_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.offset_top = 80
	_content_root.offset_bottom = -90
	add_child(_content_root)

	_build_village_tab()
	_build_character_tab()
	_build_adventure_tab()
	_build_soul_hall_tab()
	_build_bag_tab()

	## 3. 頂部多巴胺大尺寸狀態列
	_build_top_hud()

	## 4. 底部飽滿果凍導航欄
	_build_bottom_dock()

## ──────────────────────────────────────────
## 頂部大尺寸多巴胺 HUD (能量 15 點 原作規格)
## ──────────────────────────────────────────
func _build_top_hud() -> void:
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.offset_left = 16
	top_bar.offset_right = -16
	top_bar.offset_top = 10
	top_bar.offset_bottom = 74
	
	var sb := StyleBoxFlat.new()
	sb.bg_color = UiStyle.TATA_CARD_BG
	sb.border_color = UiStyle.TATA_YELLOW
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.set_corner_radius_all(22)
	sb.shadow_color = Color(0.08, 0.05, 0.18, 0.5)
	sb.shadow_size = 10
	sb.shadow_offset = Vector2(0, 4)
	top_bar.add_theme_stylebox_override("panel", sb)
	add_child(top_bar)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 18)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	top_bar.add_child(h)

	## 玩家個人檔案
	var p_box := HBoxContainer.new()
	p_box.add_theme_constant_override("separation", 10)
	h.add_child(p_box)

	var p_frame := PanelContainer.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(1.0, 0.95, 0.85)
	psb.border_color = UiStyle.TATA_YELLOW
	psb.set_border_width_all(3)
	psb.set_corner_radius_all(26)
	p_frame.custom_minimum_size = Vector2(52, 52)
	p_frame.add_theme_stylebox_override("panel", psb)
	var p_tex := TextureRect.new()
	p_tex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	p_tex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	p_tex.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/portraits/rabbit.png"):
		p_tex.texture = load("res://assets/sprites/portraits/rabbit.png")
	p_frame.add_child(p_tex)
	p_box.add_child(p_frame)

	var info_v := VBoxContainer.new()
	info_v.alignment = BoxContainer.ALIGNMENT_CENTER
	info_v.add_theme_constant_override("separation", 2)
	
	var row1 := HBoxContainer.new()
	row1.add_theme_constant_override("separation", 8)
	_lv_label = Label.new()
	_lv_label.text = "Lv.12"
	_lv_label.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	_lv_label.add_theme_font_size_override("font_size", 16)
	_lv_label.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	_lv_label.add_theme_constant_override("outline_size", 4)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = "Capoo"
	_name_label.add_theme_font_size_override("font_size", 17)
	_name_label.add_theme_color_override("font_color", Color.WHITE)
	_name_label.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	_name_label.add_theme_constant_override("outline_size", 4)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	var sw_icon := Label.new()
	sw_icon.text = "⚔️"
	sw_icon.add_theme_font_size_override("font_size", 13)
	pwr_row.add_child(sw_icon)
	_power_label = Label.new()
	_power_label.text = "戰力 482"
	_power_label.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	_power_label.add_theme_font_size_override("font_size", 14)
	_power_label.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	_power_label.add_theme_constant_override("outline_size", 3)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 多巴胺立體三寶果凍膠囊 (能量 ⚡ 薄荷綠 / 金幣 🪙 金黃 / 晶石 💎 蔚藍)
	_energy_label = _add_tata_capsule(h, "⚡ 能量", "15/15", UiStyle.TATA_GREEN)
	_gold_label = _add_tata_capsule(h, "🪙 金幣", "12,500", UiStyle.TATA_YELLOW)
	_gem_label = _add_tata_capsule(h, "💎 晶石", "350", UiStyle.TATA_BLUE)

	## 齒輪設定按鈕 (立體果凍圓鈕)
	var set_btn := Button.new()
	set_btn.text = "⚙️"
	set_btn.custom_minimum_size = Vector2(46, 46)
	set_btn.add_theme_font_size_override("font_size", 20)
	UiStyle.style_button(set_btn, false)
	set_btn.pressed.connect(func():
		var s_scn := load("res://scripts/ui/mobile_settings.gd")
		var s_ui: Control = s_scn.new()
		s_ui.z_index = 80
		add_child(s_ui)
	)
	h.add_child(set_btn)

func _add_tata_capsule(parent: Container, sym: String, val: String, accent: Color) -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.18, 0.15, 0.32, 0.95)
	csb.border_color = accent
	csb.set_border_width_all(2)
	csb.border_width_bottom = 4
	csb.set_corner_radius_all(16)
	csb.content_margin_left = 12
	csb.content_margin_right = 12
	csb.content_margin_top = 4
	csb.content_margin_bottom = 4
	csb.shadow_color = Color(accent.r, accent.g, accent.b, 0.35)
	csb.shadow_size = 5
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 8)
	var il := Label.new()
	il.text = sym
	il.add_theme_font_size_override("font_size", 14)
	il.add_theme_color_override("font_color", accent)
	il.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	il.add_theme_constant_override("outline_size", 3)
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.add_theme_font_size_override("font_size", 16)
	vl.add_theme_color_override("font_color", Color.WHITE)
	vl.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	vl.add_theme_constant_override("outline_size", 3)
	h.add_child(vl)

	cap.add_child(h)
	parent.add_child(cap)
	return vl

## ──────────────────────────────────────────
## 底部多巴胺果凍導航欄 (超大胖胖按鈕)
## ──────────────────────────────────────────
func _build_bottom_dock() -> void:
	var dock := PanelContainer.new()
	dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	dock.offset_left = 24
	dock.offset_right = -24
	dock.offset_top = -84
	dock.offset_bottom = -12
	
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = UiStyle.TATA_CARD_BG
	dsb.border_color = UiStyle.TATA_YELLOW
	dsb.set_border_width_all(2)
	dsb.border_width_bottom = 6
	dsb.set_corner_radius_all(24)
	dsb.shadow_color = Color(0.08, 0.05, 0.18, 0.6)
	dsb.shadow_size = 12
	dock.add_theme_stylebox_override("panel", dsb)
	add_child(dock)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 16)
	dock.add_child(h)

	var tabs := [
		{"tab": Tab.VILLAGE, "icon": "🏛️", "title": "今日村莊"},
		{"tab": Tab.CHARACTER, "icon": "👤", "title": "角色裝備"},
		{"tab": Tab.ADVENTURE, "icon": "⚔️", "title": "四地區出征"},
		{"tab": Tab.SOUL_HALL, "icon": "🔮", "title": "聚魂殿"},
		{"tab": Tab.BAG, "icon": "🎒", "title": "冒險背包"},
	]

	_dock_buttons.clear()
	for d in tabs:
		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(0, 56)
		btn.text = "%s %s" % [d["icon"], d["title"]]
		btn.add_theme_font_size_override("font_size", 18)
		var t: Tab = d["tab"]
		btn.pressed.connect(func(): _switch_tab(t))
		h.add_child(btn)
		_dock_buttons.append(btn)

func _switch_tab(target: Tab) -> void:
	_current_tab = target
	_village_layer.visible = (target == Tab.VILLAGE)
	_char_layer.visible = (target == Tab.CHARACTER)
	_adventure_layer.visible = (target == Tab.ADVENTURE)
	_soul_layer.visible = (target == Tab.SOUL_HALL)
	_bag_layer.visible = (target == Tab.BAG)

	for i in range(_dock_buttons.size()):
		var is_active := (i == int(target))
		UiStyle.style_button(_dock_buttons[i], is_active)

## ──────────────────────────────────────────
## Tab 1: 今日村莊 (四大鮮亮糖果建築卡片)
## ──────────────────────────────────────────
func _build_village_tab() -> void:
	_village_layer = Control.new()
	_village_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_village_layer)

	## 中央英雄展台 (帶彩虹星芒投影)
	var stage_anchor := Control.new()
	stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	stage_anchor.offset_top = 45
	_village_layer.add_child(stage_anchor)

	_hero_shadow = TextureRect.new()
	_hero_shadow.offset_left = -160
	_hero_shadow.offset_top = 100
	_hero_shadow.offset_right = 160
	_hero_shadow.offset_bottom = 175
	var grad := Gradient.new()
	grad.set_color(0, Color(1.0, 0.85, 0.35, 0.9))
	grad.set_color(1, Color(1.0, 0.85, 0.35, 0.0))
	var s_tex := GradientTexture2D.new()
	s_tex.gradient = grad
	s_tex.fill = GradientTexture2D.FILL_RADIAL
	s_tex.fill_from = Vector2(0.5, 0.5)
	s_tex.fill_to = Vector2(0.5, 0.0)
	_hero_shadow.texture = s_tex
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage_anchor.add_child(_hero_shadow)

	_hero_avatar = TextureRect.new()
	_hero_avatar.offset_left = -125
	_hero_avatar.offset_top = -140
	_hero_avatar.offset_right = 125
	_hero_avatar.offset_bottom = 125
	_hero_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_avatar.pivot_offset = Vector2(125, 240)
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		_hero_avatar.texture = load("res://assets/sprites/player/poses/idle.png")
	stage_anchor.add_child(_hero_avatar)

	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)

	## 左側四大糖果色殿堂卡片 (紫粉 / 暖橘 / 天藍 / 亮金)
	var left_shops := VBoxContainer.new()
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 32
	left_shops.offset_top = 16
	left_shops.offset_right = 252
	left_shops.offset_bottom = -16
	left_shops.add_theme_constant_override("separation", 14)
	_village_layer.add_child(left_shops)

	_add_candy_building_entry(left_shops, "🔮", "聚魂殿", "五色葫蘆 · 戰魂入槽", UiStyle.TATA_PINK, func():
		_switch_tab(Tab.SOUL_HALL)
	)
	_add_candy_building_entry(left_shops, "🔨", "鐵匠鋪", "品質晉階 · 裝備鍛造", UiStyle.TATA_ORANGE, func():
		_show_toast("進入王都鐵匠鋪：可將裝備晉階為紫裝！")
	)
	_add_candy_building_entry(left_shops, "💎", "手藝工坊", "紅黃藍寶石 · 3合1熔煉", UiStyle.TATA_BLUE, func():
		_show_toast("進入手藝工坊：寶石鑲嵌必定成功！")
	)
	_add_candy_building_entry(left_shops, "🏆", "演武場", "挑戰對手 · 雙倍抽獎", UiStyle.TATA_YELLOW, func():
		request_battle.emit("arena")
	)

	## 右側：今日簽到 & 巨大金色【出征四地區】果凍按鈕
	var right_card := PanelContainer.new()
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -360
	right_card.offset_top = -200
	right_card.offset_right = -32
	right_card.offset_bottom = -16
	right_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_village_layer.add_child(right_card)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 10)
	right_card.add_child(rv)

	var ch_lbl := Label.new()
	ch_lbl.text = "⚔️ 冒險出征 · 當前主線"
	ch_lbl.add_theme_font_size_override("font_size", 14)
	ch_lbl.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	ch_lbl.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	ch_lbl.add_theme_constant_override("outline_size", 3)
	rv.add_child(ch_lbl)

	var s_name := Label.new()
	s_name.text = "第二地區 · 聖獅王城 (2-4 BOSS)"
	s_name.add_theme_font_size_override("font_size", 17)
	s_name.add_theme_color_override("font_color", Color.WHITE)
	s_name.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	s_name.add_theme_constant_override("outline_size", 4)
	rv.add_child(s_name)

	## 巨大塔塔風出征按鈕
	var go_btn := Button.new()
	go_btn.text = "⚔️ 出征冒險！ (耗能 1⚡)"
	go_btn.custom_minimum_size = Vector2(0, 56)
	go_btn.add_theme_font_size_override("font_size", 20)
	UiStyle.style_button(go_btn, true)
	go_btn.pressed.connect(func(): _switch_tab(Tab.ADVENTURE))
	rv.add_child(go_btn)

	var sign_btn := Button.new()
	sign_btn.text = "🎁 今日簽到與每日委託"
	sign_btn.custom_minimum_size = Vector2(0, 44)
	UiStyle.style_button(sign_btn, false)
	sign_btn.pressed.connect(func():
		_show_toast("已領取每日補給：金幣+500、能量+5！")
	)
	rv.add_child(sign_btn)

func _add_candy_building_entry(parent: Container, icon: String, title: String, desc: String, accent: Color, cb: Callable) -> void:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(220, 68)
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.18, 0.15, 0.32, 0.95)
	csb.border_color = accent
	csb.set_border_width_all(2)
	csb.border_width_bottom = 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 14
	csb.content_margin_right = 14
	csb.shadow_color = Color(accent.r, accent.g, accent.b, 0.4)
	csb.shadow_size = 6
	btn.add_theme_stylebox_override("normal", csb)
	btn.add_theme_stylebox_override("hover", csb)
	btn.pressed.connect(cb)

	var h := HBoxContainer.new()
	h.set_anchors_preset(Control.PRESET_FULL_RECT)
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_theme_constant_override("separation", 12)
	btn.add_child(h)

	var il := Label.new()
	il.text = icon
	il.add_theme_font_size_override("font_size", 30)
	h.add_child(il)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	h.add_child(v)

	var tl := Label.new()
	tl.text = title
	tl.add_theme_font_size_override("font_size", 16)
	tl.add_theme_color_override("font_color", Color.WHITE)
	tl.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	tl.add_theme_constant_override("outline_size", 3)
	v.add_child(tl)

	var dl := Label.new()
	dl.text = desc
	dl.add_theme_font_size_override("font_size", 11)
	dl.add_theme_color_override("font_color", accent)
	v.add_child(dl)

	parent.add_child(btn)

func _on_hero_clicked() -> void:
	var tw := create_tween()
	tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y - 20, 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	_show_toast("出發！和夥伴們一起守護王國！")

## ──────────────────────────────────────────
## Tab 4: 聚魂殿 (五色葫蘆跳階 原作招牌)
## ──────────────────────────────────────────
func _build_soul_hall_tab() -> void:
	_soul_layer = Control.new()
	_soul_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_soul_layer.visible = false
	_content_root.add_child(_soul_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_soul_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = "✦ 聚魂殿 · 五色葫蘆跳階 ✦"
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 24)
	t.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	t.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	t.add_theme_constant_override("outline_size", 4)
	v.add_child(t)

	var desc := Label.new()
	desc.text = "聚引十四主星之魂：七煞(攻) · 武曲(防) · 天機(血) · 貪狼(命) · 紫微(閃) · 破軍(爆)。點擊點亮更高階葫蘆！"
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 13)
	desc.add_theme_color_override("font_color", Color(0.90, 0.88, 0.95))
	v.add_child(desc)

	## 五色葫蘆行 (白玉、碧綠、青藍、紫霄、澄金)
	var gourd_row := HBoxContainer.new()
	gourd_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gourd_row.add_theme_constant_override("separation", 20)
	v.add_child(gourd_row)

	var gourds_data := [
		{"name": "白玉葫蘆", "cost": 100, "color": Color(0.95, 0.95, 0.95), "icon": "🍶"},
		{"name": "碧綠葫蘆", "cost": 300, "color": UiStyle.TATA_GREEN, "icon": "🧪"},
		{"name": "青藍葫蘆", "cost": 800, "color": UiStyle.TATA_BLUE, "icon": "🏺"},
		{"name": "紫霄葫蘆", "cost": 2000, "color": UiStyle.TATA_PINK, "icon": "🔮"},
		{"name": "澄金葫蘆", "cost": 5000, "color": UiStyle.TATA_YELLOW, "icon": "⭐"}
	]

	_gourd_btns.clear()
	for i in range(gourds_data.size()):
		var gd: Dictionary = gourds_data[i]
		var gb := _build_gourd_card(gd, i)
		gourd_row.add_child(gb)
		_gourd_btns.append(gb)

	_refresh_gourds_ui()

	## 一鍵煉魂與十連聚魂按鈕列 (大尺寸果凍)
	var bot_h := HBoxContainer.new()
	bot_h.alignment = BoxContainer.ALIGNMENT_CENTER
	bot_h.add_theme_constant_override("separation", 28)
	v.add_child(bot_h)

	var btn_absorb := Button.new()
	btn_absorb.text = "⚡ 一鍵吸收灰魂 (換經驗)"
	btn_absorb.custom_minimum_size = Vector2(210, 50)
	UiStyle.style_button(btn_absorb, false)
	btn_absorb.pressed.connect(func():
		_show_toast("已將廢魂轉化為 480 戰魂經驗值！")
	)
	bot_h.add_child(btn_absorb)

	var btn_ten := Button.new()
	btn_ten.text = "✨ 聚魂十次 (直接點擊)"
	btn_ten.custom_minimum_size = Vector2(210, 50)
	UiStyle.style_button(btn_ten, true)
	btn_ten.pressed.connect(func():
		_do_gourd_draw(0, true)
	)
	bot_h.add_child(btn_ten)

func _build_gourd_card(gd: Dictionary, idx: int) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(145, 170)
	btn.name = "GourdBtn_%d" % idx

	var v := VBoxContainer.new()
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 8)
	btn.add_child(v)

	var ic := Label.new()
	ic.text = str(gd["icon"])
	ic.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ic.add_theme_font_size_override("font_size", 44)
	v.add_child(ic)

	var nl := Label.new()
	nl.text = str(gd["name"])
	nl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nl.add_theme_font_size_override("font_size", 15)
	nl.add_theme_color_override("font_color", gd["color"] as Color)
	nl.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	nl.add_theme_constant_override("outline_size", 3)
	v.add_child(nl)

	var cl := Label.new()
	cl.text = "🪙 %d" % int(gd["cost"])
	cl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cl.add_theme_font_size_override("font_size", 13)
	cl.add_theme_color_override("font_color", Color(1.0, 0.95, 0.85))
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
		var is_lit := _gourd_lit[i]
		var sb := StyleBoxFlat.new()
		if is_lit:
			sb.bg_color = Color(0.24, 0.18, 0.42, 0.98)
			sb.border_color = UiStyle.TATA_YELLOW
			sb.set_border_width_all(3)
			sb.border_width_bottom = 6
			sb.set_corner_radius_all(20)
			sb.shadow_color = Color(1.0, 0.82, 0.18, 0.5)
			sb.shadow_size = 10
			b.disabled = false
		else:
			sb.bg_color = Color(0.14, 0.12, 0.24, 0.6)
			sb.border_color = Color(0.35, 0.30, 0.50, 0.5)
			sb.set_border_width_all(1)
			sb.border_width_bottom = 3
			sb.set_corner_radius_all(18)
			b.disabled = true
		b.add_theme_stylebox_override("normal", sb)
		b.add_theme_stylebox_override("hover", sb)
		b.add_theme_stylebox_override("disabled", sb)

func _do_gourd_draw(idx: int, is_ten: bool) -> void:
	if not _gourd_lit[idx] and not is_ten:
		return

	var roll := randf()
	if roll < 0.35 and idx < 4:
		_gourd_lit[idx + 1] = true
		_show_toast("🔮 靈光閃爍！成功點亮更高階的葫蘆！")
	else:
		for i in range(1, 5):
			_gourd_lit[i] = false
		_show_toast("聚魂完畢！獲得了【戰魂碎片】與戰魂經驗！")
	
	_refresh_gourds_ui()

## ──────────────────────────────────────────
## Tab 3: 四地區出征關卡 (超大關卡卡片)
## ──────────────────────────────────────────
func _build_adventure_tab() -> void:
	_adventure_layer = Control.new()
	_adventure_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_adventure_layer.visible = false
	_content_root.add_child(_adventure_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 40
	panel.offset_right = -40
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_adventure_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	panel.add_child(v)

	## 四地區分頁按鈕 (大尺寸膠囊)
	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)

	var regions: Array[String] = ["第一地區 · 破曉之原", "第二地區 · 聖獅王都", "第三地區 · 迷霧雪境", "第四地區 · 深淵龍窟"]
	for i in range(regions.size()):
		var rb := Button.new()
		rb.text = regions[i]
		rb.custom_minimum_size = Vector2(175, 46)
		UiStyle.style_button(rb, i == _selected_region)
		var r_idx := i
		rb.pressed.connect(func(): _select_region(r_idx))
		reg_bar.add_child(rb)

	_stages_container = VBoxContainer.new()
	_stages_container.add_theme_constant_override("separation", 14)
	_stages_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_stages_container)

	_refresh_region_stages()

func _select_region(r: int) -> void:
	_selected_region = r
	_refresh_region_stages()

func _refresh_region_stages() -> void:
	for c in _stages_container.get_children():
		c.queue_free()

	var stages_data := [
		{"num": "2-1", "name": "王城外郭 · 守望關隘", "type": "雜魚關卡", "cost": 1, "power": 380, "mode": "road_bandit"},
		{"num": "2-2", "name": "市集街道 · 潛伏暗哨", "type": "菁英戰鬥", "cost": 1, "power": 420, "mode": "road_bandit"},
		{"num": "2-3", "name": "下水道口 · 腐化黏怪", "type": "菁英戰鬥", "cost": 1, "power": 450, "mode": "road_bandit"},
		{"num": "2-4", "name": "聖獅王宮 · 狂暴守護者", "type": "👑 BOSS部位破壞", "cost": 3, "power": 520, "mode": "leo"},
	]

	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 20)
	grid.add_theme_constant_override("v_separation", 16)
	_stages_container.add_child(grid)

	for s in stages_data:
		var sc := _build_stage_card(s)
		grid.add_child(sc)

func _build_stage_card(s: Dictionary) -> PanelContainer:
	var c := PanelContainer.new()
	c.custom_minimum_size = Vector2(420, 105)
	var csb := StyleBoxFlat.new()
	var is_boss: bool = str(s["type"]).find("BOSS") >= 0
	csb.bg_color = Color(0.24, 0.18, 0.40, 0.98) if is_boss else Color(0.18, 0.15, 0.32, 0.95)
	csb.border_color = UiStyle.TATA_YELLOW if is_boss else Color(0.50, 0.44, 0.72, 0.9)
	csb.set_border_width_all(2)
	csb.border_width_bottom = 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 16
	csb.content_margin_right = 16
	csb.content_margin_top = 12
	csb.content_margin_bottom = 12
	csb.shadow_color = Color(1.0, 0.82, 0.18, 0.4) if is_boss else Color(0.08, 0.05, 0.16, 0.4)
	csb.shadow_size = 8
	c.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	c.add_child(h)

	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.add_theme_constant_override("separation", 6)
	h.add_child(v)

	var t_row := HBoxContainer.new()
	t_row.add_theme_constant_override("separation", 8)
	var num_l := Label.new()
	num_l.text = str(s["num"])
	num_l.add_theme_font_size_override("font_size", 17)
	num_l.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	num_l.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	num_l.add_theme_constant_override("outline_size", 3)
	t_row.add_child(num_l)

	var name_l := Label.new()
	name_l.text = str(s["name"])
	name_l.add_theme_font_size_override("font_size", 16)
	name_l.add_theme_color_override("font_color", Color.WHITE)
	name_l.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	name_l.add_theme_constant_override("outline_size", 3)
	t_row.add_child(name_l)
	v.add_child(t_row)

	var inf_row := HBoxContainer.new()
	inf_row.add_theme_constant_override("separation", 14)
	var typ_l := Label.new()
	typ_l.text = str(s["type"])
	typ_l.add_theme_font_size_override("font_size", 13)
	typ_l.add_theme_color_override("font_color", UiStyle.TATA_ORANGE if is_boss else Color(0.85, 0.85, 0.95))
	inf_row.add_child(typ_l)

	var pwr_l := Label.new()
	pwr_l.text = "推薦戰力: %d" % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 13)
	pwr_l.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	inf_row.add_child(pwr_l)
	v.add_child(inf_row)

	var btn := Button.new()
	btn.text = "⚔️ 開戰 (⚡%d)" % int(s["cost"])
	btn.custom_minimum_size = Vector2(130, 48)
	btn.add_theme_font_size_override("font_size", 16)
	UiStyle.style_button(btn, is_boss)
	var m: String = str(s["mode"])
	btn.pressed.connect(func(): request_battle.emit(m))
	h.add_child(btn)

	return c

## ──────────────────────────────────────────
## Tab 2 & Tab 5: 角色紙娃娃與背包
## ──────────────────────────────────────────
func _build_character_tab() -> void:
	_char_layer = Control.new()
	_char_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_char_layer.visible = false
	_content_root.add_child(_char_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_char_layer.add_child(panel)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 28)
	panel.add_child(h)

	var l_card := PanelContainer.new()
	l_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	l_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	h.add_child(l_card)

	var prev := TextureRect.new()
	prev.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	prev.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	prev.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		prev.texture = load("res://assets/sprites/player/poses/idle.png")
	l_card.add_child(prev)

	var r_v := VBoxContainer.new()
	r_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	r_v.add_theme_constant_override("separation", 14)
	h.add_child(r_v)

	var title := Label.new()
	title.text = "✦ 三欄武器輪替系統 (原作節奏) ✦"
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	title.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	title.add_theme_constant_override("outline_size", 3)
	r_v.add_child(title)

	var w_row := HBoxContainer.new()
	w_row.add_theme_constant_override("separation", 12)
	r_v.add_child(w_row)

	var w_slots := ["首選: 鐵劍 (4次)", "副手: 獵弓 (4次)", "絕技: 拳套 (5連擊)"]
	for ws in w_slots:
		var p := PanelContainer.new()
		p.custom_minimum_size = Vector2(130, 68)
		var psb := StyleBoxFlat.new()
		psb.bg_color = Color(0.20, 0.16, 0.35, 0.95)
		psb.border_color = UiStyle.TATA_YELLOW
		psb.set_border_width_all(2)
		psb.border_width_bottom = 4
		psb.set_corner_radius_all(12)
		p.add_theme_stylebox_override("panel", psb)
		var l := Label.new()
		l.text = ws
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 13)
		l.add_theme_color_override("font_color", Color.WHITE)
		p.add_child(l)
		w_row.add_child(p)

	var stats := RichTextLabel.new()
	stats.bbcode_enabled = true
	stats.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stats.add_theme_font_size_override("normal_font_size", 15)
	stats.text = "\n[color=#ffd028][b]角色戰鬥屬性 (有效戰力 482)[/b][/color]\n\n"
	stats.text += "生命力 (HP): [color=#ff5e8a]520[/color]   物理攻擊: [color=#38a0ff]95[/color]\n"
	stats.text += "物理防禦: [color=#4ed86a]48[/color]   暴擊率: [color=#ffd028]22%[/color]\n"
	stats.text += "怒氣量表: [color=#ffa010]20 點 (滿怒自動觸發暴怒 +25% 攻防暴)[/color]\n"
	r_v.add_child(stats)

func _build_bag_tab() -> void:
	_bag_layer = Control.new()
	_bag_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bag_layer.visible = false
	_content_root.add_child(_bag_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 60
	panel.offset_right = -60
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_bag_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = "🎒 冒險者背包 (道具與戰魂倉庫)"
	t.add_theme_font_size_override("font_size", 20)
	t.add_theme_color_override("font_color", UiStyle.TATA_YELLOW)
	t.add_theme_color_override("font_outline_color", UiStyle.TATA_NAVY)
	t.add_theme_constant_override("outline_size", 3)
	v.add_child(t)

	var grid := GridContainer.new()
	grid.columns = 8
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 12)
	v.add_child(grid)

	for i in range(24):
		var sp := PanelContainer.new()
		sp.custom_minimum_size = Vector2(72, 72)
		var ssb := StyleBoxFlat.new()
		ssb.bg_color = Color(0.18, 0.15, 0.32, 0.95)
		ssb.border_color = Color(0.50, 0.44, 0.72, 0.8)
		ssb.set_border_width_all(2)
		ssb.border_width_bottom = 4
		ssb.set_corner_radius_all(14)
		sp.add_theme_stylebox_override("panel", ssb)
		var l := Label.new()
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 12)
		if i == 0: l.text = "鐵劍"
		elif i == 1: l.text = "紅藥水x10"
		elif i == 2: l.text = "紅寶石"
		elif i == 3: l.text = "紫微星魂"
		sp.add_child(l)
		grid.add_child(sp)

func refresh_hud() -> void:
	if _lv_label: _lv_label.text = "Lv.12"
	if _name_label: _name_label.text = "Capoo"
	if _power_label: _power_label.text = "戰力 482"
	if _energy_label: _energy_label.text = "15/15"
	if _gold_label: _gold_label.text = "12,500"
	if _gem_label: _gem_label.text = "350"

func _show_toast(msg: String) -> void:
	var toast := Label.new()
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	toast.offset_left = -200
	toast.offset_right = 200
	toast.offset_top = 80
	toast.offset_bottom = 126
	var tsb := StyleBoxFlat.new()
	tsb.bg_color = UiStyle.TATA_NAVY
	tsb.border_color = UiStyle.TATA_YELLOW
	tsb.set_border_width_all(2)
	tsb.border_width_bottom = 4
	tsb.set_corner_radius_all(14)
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", Color.WHITE)
	toast.add_theme_font_size_override("font_size", 15)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.5)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)
