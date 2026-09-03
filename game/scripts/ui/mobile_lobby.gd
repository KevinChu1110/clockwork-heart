class_name MobileLobby
extends Control
## 勇者之魂 (Brave Soul) - 現代手機風格原版架構大廳
## 對齊原作《勇者之魂》(Soul Fighter) 核心 UI/UX：
## 1. 村莊大廳 (四大原創店舖：聚魂殿、鐵匠鋪、演武場、手藝工坊)
## 2. 聚魂殿 (五色葫蘆跳階：白玉、碧綠、青藍、紫霄、澄金 + 十四主星戰魂)
## 3. 四地區出征關卡 (破曉之原、聖獅王都、迷霧雪境、深淵龍窟 + 能量消耗 1/3 點)
## 4. 角色三欄武器與紙娃娃

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
var _speech_bubble: PanelContainer
var _speech_label: Label
var _breathe_tween: Tween

## 聚魂殿五色葫蘆狀態
## 0: 白玉(常駐點亮), 1: 碧綠, 2: 青藍, 3: 紫霄, 4: 澄金
var _gourd_lit: Array[bool] = [true, false, false, false, false]
var _gourd_btns: Array[Button] = []
var _soul_inventory: Array[Dictionary] = []

## 四地區出征
var _selected_region: int = 1 # 0: 破曉之原, 1: 聖獅王都, 2: 迷霧雪境, 3: 深淵龍窟
var _stages_container: VBoxContainer
var _stage_info_card: PanelContainer

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
	## 1. 背景插畫 (王都村莊風景，線性平滑縮放)
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

	## 頂部與底部遮罩
	var top_v := ColorRect.new()
	top_v.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_v.offset_bottom = 120
	top_v.color = Color(0.06, 0.05, 0.04, 0.45)
	top_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(top_v)

	var bot_v := ColorRect.new()
	bot_v.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bot_v.offset_top = -140
	bot_v.color = Color(0.06, 0.05, 0.04, 0.6)
	bot_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bot_v)

	## 2. 內容掛載層
	_content_root = Control.new()
	_content_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.offset_top = 75
	_content_root.offset_bottom = -84
	add_child(_content_root)

	_build_village_tab()
	_build_character_tab()
	_build_adventure_tab()
	_build_soul_hall_tab()
	_build_bag_tab()

	## 3. 頂部手遊狀態條
	_build_top_hud()

	## 4. 底部導航欄
	_build_bottom_dock()

## ──────────────────────────────────────────
## 頂部狀態列 (能量 15點 原作規格)
## ──────────────────────────────────────────
func _build_top_hud() -> void:
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.offset_left = 16
	top_bar.offset_right = -16
	top_bar.offset_top = 10
	top_bar.offset_bottom = 68
	top_bar.add_theme_stylebox_override("panel", UiStyle.panel_style())
	add_child(top_bar)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 14)
	top_bar.add_child(h)

	## 玩家個人檔案
	var p_box := HBoxContainer.new()
	p_box.add_theme_constant_override("separation", 8)
	h.add_child(p_box)

	var p_frame := PanelContainer.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.95, 0.88, 0.75)
	psb.border_color = Color(0.95, 0.78, 0.25)
	psb.set_border_width_all(2)
	psb.set_corner_radius_all(22)
	p_frame.custom_minimum_size = Vector2(44, 44)
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
	row1.add_theme_constant_override("separation", 6)
	_lv_label = Label.new()
	_lv_label.text = "Lv.12"
	_lv_label.add_theme_color_override("font_color", Color(1.0, 0.82, 0.25))
	_lv_label.add_theme_font_size_override("font_size", 14)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = "Capoo"
	_name_label.add_theme_font_size_override("font_size", 15)
	_name_label.add_theme_color_override("font_color", Color.WHITE)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	var sw_icon := Label.new()
	sw_icon.text = "⚔️"
	sw_icon.add_theme_font_size_override("font_size", 12)
	pwr_row.add_child(sw_icon)
	_power_label = Label.new()
	_power_label.text = "戰力 482"
	_power_label.add_theme_color_override("font_color", Color(1.0, 0.75, 0.25))
	_power_label.add_theme_font_size_override("font_size", 12)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 原作資源：能量 (上限 15，30分+1)、金幣、晶石
	_energy_label = _add_capsule(h, "⚡ 能量", "15/15", Color(0.35, 0.9, 0.5))
	_gold_label = _add_capsule(h, "🪙 金幣", "12,500", Color(1.0, 0.85, 0.3))
	_gem_label = _add_capsule(h, "💎 晶石", "350", Color(0.45, 0.8, 1.0))

	## 齒輪設定
	var set_btn := Button.new()
	set_btn.text = "⚙️"
	set_btn.custom_minimum_size = Vector2(40, 40)
	set_btn.add_theme_font_size_override("font_size", 18)
	UiStyle.style_button(set_btn, false)
	set_btn.pressed.connect(func():
		var s_scn := load("res://scripts/ui/mobile_settings.gd")
		var s_ui: Control = s_scn.new()
		s_ui.z_index = 80
		add_child(s_ui)
	)
	h.add_child(set_btn)

func _add_capsule(parent: Container, sym: String, val: String, col: Color) -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.08, 0.06, 0.05, 0.9)
	csb.border_color = Color(0.55, 0.45, 0.32, 0.9)
	csb.set_border_width_all(1)
	csb.set_corner_radius_all(14)
	csb.content_margin_left = 10
	csb.content_margin_right = 10
	csb.content_margin_top = 2
	csb.content_margin_bottom = 2
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 6)
	var il := Label.new()
	il.text = sym
	il.add_theme_font_size_override("font_size", 13)
	il.add_theme_color_override("font_color", col)
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.add_theme_font_size_override("font_size", 14)
	vl.add_theme_color_override("font_color", Color(0.96, 0.95, 0.92))
	h.add_child(vl)

	cap.add_child(h)
	parent.add_child(cap)
	return vl

## ──────────────────────────────────────────
## 底部導航欄
## ──────────────────────────────────────────
func _build_bottom_dock() -> void:
	var dock := PanelContainer.new()
	dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	dock.offset_left = 30
	dock.offset_right = -30
	dock.offset_top = -78
	dock.offset_bottom = -12
	dock.add_theme_stylebox_override("panel", UiStyle.panel_style())
	add_child(dock)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 18)
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
		btn.custom_minimum_size = Vector2(0, 52)
		btn.text = "%s %s" % [d["icon"], d["title"]]
		btn.add_theme_font_size_override("font_size", 16)
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
## Tab 1: 今日村莊 (Village Hub - 四大原作殿堂)
## ──────────────────────────────────────────
func _build_village_tab() -> void:
	_village_layer = Control.new()
	_village_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_village_layer)

	## 中央英雄展台
	var stage_anchor := Control.new()
	stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	stage_anchor.offset_top = 50
	_village_layer.add_child(stage_anchor)

	_hero_shadow = TextureRect.new()
	_hero_shadow.offset_left = -150
	_hero_shadow.offset_top = 100
	_hero_shadow.offset_right = 150
	_hero_shadow.offset_bottom = 170
	var grad := Gradient.new()
	grad.set_color(0, Color(1.0, 0.85, 0.40, 0.85))
	grad.set_color(1, Color(1.0, 0.85, 0.40, 0.0))
	var s_tex := GradientTexture2D.new()
	s_tex.gradient = grad
	s_tex.fill = GradientTexture2D.FILL_RADIAL
	s_tex.fill_from = Vector2(0.5, 0.5)
	s_tex.fill_to = Vector2(0.5, 0.0)
	_hero_shadow.texture = s_tex
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage_anchor.add_child(_hero_shadow)

	_hero_avatar = TextureRect.new()
	_hero_avatar.offset_left = -120
	_hero_avatar.offset_top = -140
	_hero_avatar.offset_right = 120
	_hero_avatar.offset_bottom = 120
	_hero_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_avatar.pivot_offset = Vector2(120, 240)
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		_hero_avatar.texture = load("res://assets/sprites/player/poses/idle.png")
	stage_anchor.add_child(_hero_avatar)

	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	## 呼吸動畫
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.02, 0.98), 1.2).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.99, 1.01), 1.2).set_trans(Tween.TRANS_SINE)

	## 左側原作核心殿堂：聚魂殿、鐵匠鋪、手藝工坊
	var left_shops := VBoxContainer.new()
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 36
	left_shops.offset_top = 20
	left_shops.offset_right = 200
	left_shops.offset_bottom = -20
	left_shops.add_theme_constant_override("separation", 14)
	_village_layer.add_child(left_shops)

	_add_building_entry(left_shops, "🔮", "聚魂殿", "五色葫蘆 · 戰魂入槽", func():
		_switch_tab(Tab.SOUL_HALL)
	)
	_add_building_entry(left_shops, "🔨", "鐵匠鋪", "品質轉化 · 裝備鍛造", func():
		_show_toast("進入王都鐵匠鋪：可將裝備晉階為紫裝！")
	)
	_add_building_entry(left_shops, "💎", "手藝工坊", "紅黃藍寶石 · 3合1熔煉", func():
		_show_toast("進入手藝工坊：寶石鑲嵌必定成功！")
	)
	_add_building_entry(left_shops, "🏆", "演武場", "挑戰對手 · 雙倍經驗抽獎", func():
		request_battle.emit("arena")
	)

	## 右側：今日簽到 & 巨大金色【出征四地區】按鈕
	var right_card := PanelContainer.new()
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -330
	right_card.offset_top = -180
	right_card.offset_right = -36
	right_card.offset_bottom = -20
	right_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_village_layer.add_child(right_card)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 8)
	right_card.add_child(rv)

	var ch_lbl := Label.new()
	ch_lbl.text = "⚔️ 冒險出征 · 當前進度"
	ch_lbl.add_theme_font_size_override("font_size", 13)
	ch_lbl.add_theme_color_override("font_color", Color(1.0, 0.85, 0.4))
	rv.add_child(ch_lbl)

	var s_name := Label.new()
	s_name.text = "第二地區 · 聖獅王城 (2-4 BOSS)"
	s_name.add_theme_font_size_override("font_size", 15)
	s_name.add_theme_color_override("font_color", Color.WHITE)
	rv.add_child(s_name)

	var go_btn := Button.new()
	go_btn.text = "⚔️ 出征四地區 (耗能 1⚡)"
	go_btn.custom_minimum_size = Vector2(0, 46)
	UiStyle.style_button(go_btn, true)
	go_btn.pressed.connect(func(): _switch_tab(Tab.ADVENTURE))
	rv.add_child(go_btn)

	var sign_btn := Button.new()
	sign_btn.text = "🎁 今日簽到與委託"
	sign_btn.custom_minimum_size = Vector2(0, 36)
	UiStyle.style_button(sign_btn, false)
	sign_btn.pressed.connect(func():
		_show_toast("已領取每日補給：金幣+500、能量+5！")
	)
	rv.add_child(sign_btn)

func _add_building_entry(parent: Container, icon: String, title: String, desc: String, cb: Callable) -> void:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(180, 60)
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.14, 0.11, 0.08, 0.92)
	csb.border_color = Color(0.85, 0.70, 0.35, 0.9)
	csb.set_border_width_all(2)
	csb.set_corner_radius_all(14)
	csb.content_margin_left = 12
	csb.content_margin_right = 12
	btn.add_theme_stylebox_override("normal", csb)
	btn.add_theme_stylebox_override("hover", csb)
	btn.pressed.connect(cb)

	var h := HBoxContainer.new()
	h.set_anchors_preset(Control.PRESET_FULL_RECT)
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	h.add_theme_constant_override("separation", 10)
	btn.add_child(h)

	var il := Label.new()
	il.text = icon
	il.add_theme_font_size_override("font_size", 24)
	h.add_child(il)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	h.add_child(v)

	var tl := Label.new()
	tl.text = title
	tl.add_theme_font_size_override("font_size", 14)
	tl.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	v.add_child(tl)

	var dl := Label.new()
	dl.text = desc
	dl.add_theme_font_size_override("font_size", 10)
	dl.add_theme_color_override("font_color", Color(0.80, 0.75, 0.70))
	v.add_child(dl)

	parent.add_child(btn)

func _on_hero_clicked() -> void:
	var tw := create_tween()
	tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y - 18, 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	_show_toast("保護王國與夥伴，是小白的榮耀！")

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
	panel.offset_left = 60
	panel.offset_right = -60
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_soul_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = "✦ 聚魂殿 · 五色葫蘆跳階 ✦"
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 20)
	t.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	v.add_child(t)

	var desc := Label.new()
	desc.text = "聚引十四主星之魂：七煞(攻) · 武曲(防) · 天機(血) · 貪狼(命) · 紫微(閃) · 破軍(爆)。點擊點亮更高階葫蘆！"
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 12)
	desc.add_theme_color_override("font_color", Color(0.85, 0.80, 0.75))
	v.add_child(desc)

	## 五色葫蘆行 (白玉、碧綠、青藍、紫霄、澄金)
	var gourd_row := HBoxContainer.new()
	gourd_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gourd_row.add_theme_constant_override("separation", 18)
	v.add_child(gourd_row)

	var gourds_data := [
		{"name": "白玉葫蘆", "cost": 100, "color": Color(0.95, 0.95, 0.95), "icon": "🍶"},
		{"name": "碧綠葫蘆", "cost": 300, "color": Color(0.4, 0.9, 0.5), "icon": "🧪"},
		{"name": "青藍葫蘆", "cost": 800, "color": Color(0.4, 0.7, 1.0), "icon": "🏺"},
		{"name": "紫霄葫蘆", "cost": 2000, "color": Color(0.8, 0.5, 1.0), "icon": "🔮"},
		{"name": "澄金葫蘆", "cost": 5000, "color": Color(1.0, 0.85, 0.3), "icon": "⭐"}
	]

	_gourd_btns.clear()
	for i in range(gourds_data.size()):
		var gd: Dictionary = gourds_data[i]
		var gb := _build_gourd_card(gd, i)
		gourd_row.add_child(gb)
		_gourd_btns.append(gb)

	_refresh_gourds_ui()

	## 一鍵煉魂與十連聚魂按鈕列
	var bot_h := HBoxContainer.new()
	bot_h.alignment = BoxContainer.ALIGNMENT_CENTER
	bot_h.add_theme_constant_override("separation", 24)
	v.add_child(bot_h)

	var btn_absorb := Button.new()
	btn_absorb.text = "⚡ 一鍵吸收灰魂 (換經驗)"
	btn_absorb.custom_minimum_size = Vector2(180, 44)
	UiStyle.style_button(btn_absorb, false)
	btn_absorb.pressed.connect(func():
		_show_toast("已將廢魂轉化為 480 戰魂經驗值！")
	)
	bot_h.add_child(btn_absorb)

	var btn_ten := Button.new()
	btn_ten.text = "✨ 聚魂十次 (直接點擊)"
	btn_ten.custom_minimum_size = Vector2(180, 44)
	UiStyle.style_button(btn_ten, true)
	btn_ten.pressed.connect(func():
		_do_gourd_draw(0, true)
	)
	bot_h.add_child(btn_ten)

func _build_gourd_card(gd: Dictionary, idx: int) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(130, 150)
	btn.name = "GourdBtn_%d" % idx

	var v := VBoxContainer.new()
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 6)
	btn.add_child(v)

	var ic := Label.new()
	ic.text = str(gd["icon"])
	ic.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ic.add_theme_font_size_override("font_size", 36)
	v.add_child(ic)

	var nl := Label.new()
	nl.text = str(gd["name"])
	nl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nl.add_theme_font_size_override("font_size", 13)
	nl.add_theme_color_override("font_color", gd["color"] as Color)
	v.add_child(nl)

	var cl := Label.new()
	cl.text = "🪙 %d" % int(gd["cost"])
	cl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cl.add_theme_font_size_override("font_size", 11)
	cl.add_theme_color_override("font_color", Color(0.85, 0.8, 0.75))
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
		var is_lit := _gourd_lit[i]
		var sb := StyleBoxFlat.new()
		if is_lit:
			sb.bg_color = Color(0.22, 0.16, 0.10, 0.95)
			sb.border_color = Color(1.0, 0.85, 0.35, 1.0)
			sb.set_border_width_all(2)
			sb.set_corner_radius_all(12)
			sb.shadow_color = Color(1.0, 0.85, 0.35, 0.4)
			sb.shadow_size = 6
			b.disabled = false
		else:
			sb.bg_color = Color(0.12, 0.10, 0.08, 0.6)
			sb.border_color = Color(0.35, 0.28, 0.20, 0.5)
			sb.set_border_width_all(1)
			sb.set_corner_radius_all(12)
			b.disabled = true
		b.add_theme_stylebox_override("normal", sb)
		b.add_theme_stylebox_override("hover", sb)
		b.add_theme_stylebox_override("disabled", sb)

func _do_gourd_draw(idx: int, is_ten: bool) -> void:
	if not _gourd_lit[idx] and not is_ten:
		return

	var roll := randf()
	if roll < 0.35 and idx < 4:
		## 成功點亮更高階葫蘆！
		_gourd_lit[idx + 1] = true
		_show_toast("🔮 靈光閃爍！成功點亮更高階的葫蘆！")
	else:
		## 摔回白玉葫蘆 (原作經典跳階機制)
		for i in range(1, 5):
			_gourd_lit[i] = false
		_show_toast("聚魂完畢！獲得了【戰魂碎片】與戰魂經驗！")
	
	_refresh_gourds_ui()

## ──────────────────────────────────────────
## Tab 3: 四地區出征關卡 (原作四地區)
## ──────────────────────────────────────────
func _build_adventure_tab() -> void:
	_adventure_layer = Control.new()
	_adventure_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_adventure_layer.visible = false
	_content_root.add_child(_adventure_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_adventure_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 12)
	panel.add_child(v)

	## 四地區標籤選擇列 (第一～四地區)
	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)

	var regions: Array[String] = ["第一地區 · 破曉之原", "第二地區 · 聖獅王都", "第三地區 · 迷霧雪境", "第四地區 · 深淵龍窟"]
	for i in range(regions.size()):
		var rb := Button.new()
		rb.text = regions[i]
		rb.custom_minimum_size = Vector2(160, 42)
		UiStyle.style_button(rb, i == _selected_region)
		var r_idx := i
		rb.pressed.connect(func(): _select_region(r_idx))
		reg_bar.add_child(rb)

	## 關卡列表容器
	_stages_container = VBoxContainer.new()
	_stages_container.add_theme_constant_override("separation", 12)
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
		{"num": "2-1", "name": "王城外郭 · 守望關隘", "type": "雜魚", "cost": 1, "power": 380, "mode": "road_bandit"},
		{"num": "2-2", "name": "市集街道 · 潛伏暗哨", "type": "菁英", "cost": 1, "power": 420, "mode": "road_bandit"},
		{"num": "2-3", "name": "下水道口 · 腐化黏怪", "type": "菁英", "cost": 1, "power": 450, "mode": "road_bandit"},
		{"num": "2-4", "name": "聖獅王宮 · 狂暴守護者", "type": "👑 BOSS部位破壞", "cost": 3, "power": 520, "mode": "leo"},
	]

	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 18)
	grid.add_theme_constant_override("v_separation", 14)
	_stages_container.add_child(grid)

	for s in stages_data:
		var sc := _build_stage_card(s)
		grid.add_child(sc)

func _build_stage_card(s: Dictionary) -> PanelContainer:
	var c := PanelContainer.new()
	c.custom_minimum_size = Vector2(360, 96)
	var csb := StyleBoxFlat.new()
	var is_boss: bool = str(s["type"]).find("BOSS") >= 0
	csb.bg_color = Color(0.20, 0.14, 0.10, 0.95) if is_boss else Color(0.14, 0.11, 0.08, 0.92)
	csb.border_color = Color(1.0, 0.85, 0.35, 1.0) if is_boss else Color(0.65, 0.52, 0.35, 0.8)
	csb.set_border_width_all(2)
	csb.set_corner_radius_all(12)
	csb.content_margin_left = 14
	csb.content_margin_right = 14
	csb.content_margin_top = 10
	csb.content_margin_bottom = 10
	c.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 12)
	c.add_child(h)

	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.add_theme_constant_override("separation", 4)
	h.add_child(v)

	var t_row := HBoxContainer.new()
	t_row.add_theme_constant_override("separation", 8)
	var num_l := Label.new()
	num_l.text = str(s["num"])
	num_l.add_theme_font_size_override("font_size", 15)
	num_l.add_theme_color_override("font_color", Color(1.0, 0.85, 0.35))
	t_row.add_child(num_l)

	var name_l := Label.new()
	name_l.text = str(s["name"])
	name_l.add_theme_font_size_override("font_size", 14)
	name_l.add_theme_color_override("font_color", Color.WHITE)
	t_row.add_child(name_l)
	v.add_child(t_row)

	var inf_row := HBoxContainer.new()
	inf_row.add_theme_constant_override("separation", 12)
	var typ_l := Label.new()
	typ_l.text = str(s["type"])
	typ_l.add_theme_font_size_override("font_size", 11)
	typ_l.add_theme_color_override("font_color", Color(1.0, 0.6, 0.4) if is_boss else Color(0.8, 0.8, 0.8))
	inf_row.add_child(typ_l)

	var pwr_l := Label.new()
	pwr_l.text = "推薦戰力: %d" % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 11)
	pwr_l.add_theme_color_override("font_color", Color(0.9, 0.85, 0.6))
	inf_row.add_child(pwr_l)
	v.add_child(inf_row)

	var btn := Button.new()
	btn.text = "⚔️ 開戰 (⚡%d)" % int(s["cost"])
	btn.custom_minimum_size = Vector2(110, 42)
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
	panel.offset_left = 60
	panel.offset_right = -60
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_char_layer.add_child(panel)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 24)
	panel.add_child(h)

	## 左側立繪
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

	## 右側三欄武器與數值
	var r_v := VBoxContainer.new()
	r_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	r_v.add_theme_constant_override("separation", 12)
	h.add_child(r_v)

	var title := Label.new()
	title.text = "✦ 三欄武器輪替系統 (原作節奏) ✦"
	title.add_theme_font_size_override("font_size", 16)
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.35))
	r_v.add_child(title)

	var w_row := HBoxContainer.new()
	w_row.add_theme_constant_override("separation", 10)
	r_v.add_child(w_row)

	var w_slots := ["首選: 鐵劍 (每場4次)", "副手: 獵弓 (每場4次)", "絕技: 拳套 (每次5連擊)"]
	for ws in w_slots:
		var p := PanelContainer.new()
		p.custom_minimum_size = Vector2(120, 60)
		var psb := StyleBoxFlat.new()
		psb.bg_color = Color(0.16, 0.12, 0.09, 0.9)
		psb.border_color = Color(0.85, 0.70, 0.35, 0.9)
		psb.set_border_width_all(1)
		psb.set_corner_radius_all(8)
		p.add_theme_stylebox_override("panel", psb)
		var l := Label.new()
		l.text = ws
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 11)
		p.add_child(l)
		w_row.add_child(p)

	var stats := RichTextLabel.new()
	stats.bbcode_enabled = true
	stats.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stats.text = "\n[color=#ffd700]角色戰鬥屬性 (有效戰力 482)[/color]\n\n"
	stats.text += "生命力 (HP): [color=#ff6b6b]520[/color]   物理攻擊: [color=#4dabf7]95[/color]\n"
	stats.text += "物理防禦: [color=#51cf66]48[/color]   暴擊率: [color=#fcc419]22%[/color]\n"
	stats.text += "怒氣量表: [color=#ffa500]20 點 (滿怒自動觸發暴怒 +25% 攻防暴)[/color]\n"
	r_v.add_child(stats)

func _build_bag_tab() -> void:
	_bag_layer = Control.new()
	_bag_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bag_layer.visible = false
	_content_root.add_child(_bag_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 80
	panel.offset_right = -80
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_bag_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	panel.add_child(v)

	var t := Label.new()
	t.text = "🎒 冒險者背包 (道具與戰魂倉庫)"
	t.add_theme_font_size_override("font_size", 18)
	t.add_theme_color_override("font_color", Color(1.0, 0.85, 0.4))
	v.add_child(t)

	var grid := GridContainer.new()
	grid.columns = 8
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 10)
	v.add_child(grid)

	for i in range(24):
		var sp := PanelContainer.new()
		sp.custom_minimum_size = Vector2(64, 64)
		var ssb := StyleBoxFlat.new()
		ssb.bg_color = Color(0.14, 0.11, 0.08, 0.9)
		ssb.border_color = Color(0.55, 0.42, 0.28, 0.8)
		ssb.set_border_width_all(1)
		ssb.set_corner_radius_all(8)
		sp.add_theme_stylebox_override("panel", ssb)
		var l := Label.new()
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 11)
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
	toast.offset_left = -180
	toast.offset_right = 180
	toast.offset_top = 80
	toast.offset_bottom = 120
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
	tw.tween_interval(1.5)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)
