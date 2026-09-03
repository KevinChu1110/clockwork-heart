class_name MobileLobby
extends Control
## 現代化手機風格線上遊戲主大廳 (Modern Mobile Online RPG Lobby)
## 頂部資源列 (Top Bar) + 中央紙娃娃展台 (Main Stage) + 底部五大導航 (Bottom Dock) + 多分頁切換

signal request_explore(map_id: String)
signal request_battle(mode: String)
signal request_quit()
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

enum Tab {
	HOME,       ## 主城大廳
	CHARACTER,  ## 角色 / 紙娃娃
	ADVENTURE,  ## 冒險出征
	GACHA,      ## 聚魂抽卡
	BAG         ## 背包
}

var _current_tab: Tab = Tab.HOME

## UI 核心層
var _bg_rect: TextureRect
var _content_root: Control
var _top_bar: PanelContainer
var _bottom_dock: PanelContainer

## 分頁層
var _stage_layer: Control
var _character_layer: Control
var _adventure_layer: Control
var _gacha_layer: Control
var _bag_layer: Control

## 頂部數值
var _lv_label: Label
var _name_label: Label
var _power_label: Label
var _energy_label: Label
var _gold_label: Label
var _gem_label: Label

## 展台動畫與節點
var _stage_anchor: Control
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _speech_bubble: PanelContainer
var _speech_label: Label
var _bubble_tween: Tween
var _breathe_tween: Tween
var _dock_buttons: Array[Button] = []

## 角色分頁
var _char_preview: TextureRect
var _char_stats_label: RichTextLabel
var _char_equip_grid: GridContainer

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func _ready() -> void:
	custom_minimum_size = Vector2(1280, 720)
	size = Vector2(1280, 720)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build_ui()
	refresh_hud()
	_start_hero_animations()
	_switch_tab(Tab.HOME)

func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		if size.x < 100 or size.y < 100:
			size = Vector2(1280, 720)

func _build_ui() -> void:
	## 1. 全景城鎮插畫背景 (無雜亂角色，純風景)
	_bg_rect = TextureRect.new()
	_bg_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bg_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_bg_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_bg_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		_bg_rect.texture = load("res://assets/sprites/maps/town_bg.webp")
	elif ResourceLoader.exists("res://assets/sprites/maps/forest_bg.webp"):
		_bg_rect.texture = load("res://assets/sprites/maps/forest_bg.webp")
	elif ResourceLoader.exists("res://assets/sprites/illustrations/title_bg.png"):
		_bg_rect.texture = load("res://assets/sprites/illustrations/title_bg.png")
	add_child(_bg_rect)

	## 柔和手遊光暈遮罩 (頂部與底部)
	var top_vignette := ColorRect.new()
	top_vignette.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_vignette.offset_bottom = 120
	top_vignette.color = Color(0.06, 0.05, 0.04, 0.45)
	top_vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(top_vignette)

	var bottom_vignette := ColorRect.new()
	bottom_vignette.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bottom_vignette.offset_top = -140
	bottom_vignette.color = Color(0.06, 0.05, 0.04, 0.55)
	bottom_vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bottom_vignette)

	## 2. 內容層 (分頁掛載處)
	_content_root = Control.new()
	_content_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.offset_top = 75
	_content_root.offset_bottom = -84
	add_child(_content_root)

	_build_stage_tab()
	_build_character_tab()
	_build_adventure_tab()
	_build_gacha_tab()
	_build_bag_tab()

	## 3. 頂部手遊資源條
	_build_top_bar()

	## 4. 底部現代手遊導航列 (Dock)
	_build_bottom_dock()

## ──────────────────────────────────────────
## 頂部資源列 (Top Bar HUD)
## ──────────────────────────────────────────
func _build_top_bar() -> void:
	_top_bar = PanelContainer.new()
	_top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_top_bar.offset_left = 16
	_top_bar.offset_right = -16
	_top_bar.offset_top = 10
	_top_bar.offset_bottom = 68
	
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.12, 0.09, 0.07, 0.92)
	sb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	sb.set_border_width_all(2)
	sb.set_corner_radius_all(14)
	sb.shadow_color = Color(0, 0, 0, 0.35)
	sb.shadow_size = 6
	sb.shadow_offset = Vector2(0, 2)
	sb.content_margin_left = 12
	sb.content_margin_right = 14
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	_top_bar.add_theme_stylebox_override("panel", sb)
	add_child(_top_bar)

	var hbox := HBoxContainer.new()
	hbox.add_theme_constant_override("separation", 16)
	_top_bar.add_child(hbox)

	## 玩家個人檔案塊 (左側)
	var profile_box := HBoxContainer.new()
	profile_box.add_theme_constant_override("separation", 10)
	hbox.add_child(profile_box)

	## 圓形大頭貼
	var portrait_frame := PanelContainer.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.95, 0.88, 0.75, 1.0)
	psb.border_color = Color(0.95, 0.78, 0.25, 1.0)
	psb.set_border_width_all(2)
	psb.set_corner_radius_all(22)
	portrait_frame.custom_minimum_size = Vector2(44, 44)
	portrait_frame.add_theme_stylebox_override("panel", psb)
	
	var portrait_tex := TextureRect.new()
	portrait_tex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait_tex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	portrait_tex.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/portraits/rabbit.png"):
		portrait_tex.texture = load("res://assets/sprites/portraits/rabbit.png")
	portrait_tex.custom_minimum_size = Vector2(38, 38)
	portrait_frame.add_child(portrait_tex)
	profile_box.add_child(portrait_frame)

	## 名字與戰鬥力
	var info_vbox := VBoxContainer.new()
	info_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	info_vbox.add_theme_constant_override("separation", 2)

	var name_row := HBoxContainer.new()
	name_row.add_theme_constant_override("separation", 6)
	_lv_label = Label.new()
	_lv_label.text = "Lv.12"
	_lv_label.add_theme_color_override("font_color", Color(1.0, 0.82, 0.25, 1.0))
	_lv_label.add_theme_font_size_override("font_size", 14)
	_lv_label.add_theme_color_override("font_outline_color", Color(0.2, 0.1, 0.05, 1.0))
	_lv_label.add_theme_constant_override("outline_size", 3)
	name_row.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = "Capoo"
	_name_label.add_theme_color_override("font_color", Color(0.98, 0.95, 0.90, 1.0))
	_name_label.add_theme_font_size_override("font_size", 15)
	name_row.add_child(_name_label)
	info_vbox.add_child(name_row)

	## 戰鬥力標籤 (手遊經典)
	var power_box := HBoxContainer.new()
	power_box.add_theme_constant_override("separation", 4)
	var sword_icon := Label.new()
	sword_icon.text = "⚔️"
	sword_icon.add_theme_font_size_override("font_size", 12)
	power_box.add_child(sword_icon)
	
	_power_label = Label.new()
	_power_label.text = "戰力 482"
	_power_label.add_theme_color_override("font_color", Color(1.0, 0.72, 0.20, 1.0))
	_power_label.add_theme_font_size_override("font_size", 12)
	power_box.add_child(_power_label)
	info_vbox.add_child(power_box)

	profile_box.add_child(info_vbox)

	## 中間空白延伸
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hbox.add_child(spacer)

	## 右側資源膠囊群 (體力 / 金幣 / 鑽石)
	_energy_label = _add_resource_capsule(hbox, "⚡", "15/15", Color(0.3, 0.85, 0.45))
	_gold_label = _add_resource_capsule(hbox, "🪙", "12,500", Color(1.0, 0.85, 0.3))
	_gem_label = _add_resource_capsule(hbox, "💎", "350", Color(0.45, 0.75, 1.0))

	## 齒輪設置按鈕
	var btn_setting := Button.new()
	btn_setting.text = "⚙️"
	btn_setting.custom_minimum_size = Vector2(40, 40)
	btn_setting.add_theme_font_size_override("font_size", 18)
	var set_sb := StyleBoxFlat.new()
	set_sb.bg_color = Color(0.18, 0.14, 0.11, 0.95)
	set_sb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	set_sb.set_border_width_all(2)
	set_sb.set_corner_radius_all(10)
	btn_setting.add_theme_stylebox_override("normal", set_sb)
	btn_setting.add_theme_stylebox_override("hover", set_sb)
	btn_setting.pressed.connect(func(): request_settings.emit())
	hbox.add_child(btn_setting)

func _add_resource_capsule(parent: Container, icon_sym: String, init_val: String, accent_color: Color) -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.08, 0.06, 0.05, 0.90)
	csb.border_color = Color(0.55, 0.45, 0.30, 0.9)
	csb.set_border_width_all(1)
	csb.set_corner_radius_all(15)
	csb.content_margin_left = 10
	csb.content_margin_right = 8
	csb.content_margin_top = 2
	csb.content_margin_bottom = 2
	cap.add_theme_stylebox_override("panel", csb)
	
	var r_box := HBoxContainer.new()
	r_box.add_theme_constant_override("separation", 8)
	r_box.alignment = BoxContainer.ALIGNMENT_CENTER

	var icon_l := Label.new()
	icon_l.text = icon_sym
	icon_l.add_theme_font_size_override("font_size", 15)
	r_box.add_child(icon_l)

	var val_l := Label.new()
	val_l.text = init_val
	val_l.custom_minimum_size = Vector2(58, 0)
	val_l.add_theme_font_size_override("font_size", 14)
	val_l.add_theme_color_override("font_color", Color(0.96, 0.95, 0.92))
	r_box.add_child(val_l)

	var add_btn := Button.new()
	add_btn.text = "+"
	add_btn.custom_minimum_size = Vector2(22, 22)
	add_btn.add_theme_font_size_override("font_size", 13)
	add_btn.add_theme_color_override("font_color", accent_color)
	var asb := StyleBoxFlat.new()
	asb.bg_color = Color(0.24, 0.18, 0.13, 0.9)
	asb.set_corner_radius_all(11)
	add_btn.add_theme_stylebox_override("normal", asb)
	r_box.add_child(add_btn)

	cap.add_child(r_box)
	parent.add_child(cap)
	return val_l

## ──────────────────────────────────────────
## 底部導航列 (Bottom Navigation Dock)
## ──────────────────────────────────────────
func _build_bottom_dock() -> void:
	_bottom_dock = PanelContainer.new()
	_bottom_dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_bottom_dock.offset_left = 30
	_bottom_dock.offset_right = -30
	_bottom_dock.offset_top = -78
	_bottom_dock.offset_bottom = -12
	
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = Color(0.10, 0.08, 0.06, 0.95)
	dsb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	dsb.set_border_width_all(2)
	dsb.set_corner_radius_all(18)
	dsb.shadow_color = Color(0, 0, 0, 0.45)
	dsb.shadow_size = 8
	dsb.shadow_offset = Vector2(0, 3)
	dsb.content_margin_left = 20
	dsb.content_margin_right = 20
	dsb.content_margin_top = 5
	dsb.content_margin_bottom = 5
	_bottom_dock.add_theme_stylebox_override("panel", dsb)
	add_child(_bottom_dock)

	var hbox := HBoxContainer.new()
	hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox.add_theme_constant_override("separation", 18)
	_bottom_dock.add_child(hbox)

	var tabs_data: Array = [
		{"tab": Tab.HOME, "icon": "🏛️", "title": "主城"},
		{"tab": Tab.CHARACTER, "icon": "👤", "title": "角色"},
		{"tab": Tab.ADVENTURE, "icon": "⚔️", "title": "冒險"},
		{"tab": Tab.GACHA, "icon": "🔮", "title": "聚魂"},
		{"tab": Tab.BAG, "icon": "🎒", "title": "背包"},
	]

	_dock_buttons.clear()
	for d in tabs_data:
		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(0, 52)
		btn.text = "%s %s" % [d["icon"], d["title"]]
		btn.add_theme_font_size_override("font_size", 16)
		var t: Tab = d["tab"]
		btn.pressed.connect(func(): _switch_tab(t))
		hbox.add_child(btn)
		_dock_buttons.append(btn)

func _update_dock_styling() -> void:
	for i in range(_dock_buttons.size()):
		var btn: Button = _dock_buttons[i]
		var is_active := (i == int(_current_tab))
		if is_active:
			## 選中態：亮金高光手遊膠囊
			var asb := StyleBoxFlat.new()
			asb.bg_color = Color(0.92, 0.76, 0.28, 1.0)
			asb.border_color = Color(1.0, 0.95, 0.65, 1.0)
			asb.set_border_width_all(2)
			asb.set_corner_radius_all(14)
			asb.shadow_color = Color(0.92, 0.76, 0.28, 0.4)
			asb.shadow_size = 6
			btn.add_theme_stylebox_override("normal", asb)
			btn.add_theme_stylebox_override("hover", asb)
			btn.add_theme_color_override("font_color", Color(0.18, 0.12, 0.05, 1.0))
			btn.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.8))
			btn.add_theme_constant_override("outline_size", 1)
		else:
			## 未選中態：深色內斂手遊膠囊
			var nsb := StyleBoxFlat.new()
			nsb.bg_color = Color(0.16, 0.12, 0.09, 0.85)
			nsb.border_color = Color(0.40, 0.32, 0.24, 0.8)
			nsb.set_border_width_all(1)
			nsb.set_corner_radius_all(14)
			btn.add_theme_stylebox_override("normal", nsb)
			btn.add_theme_stylebox_override("hover", nsb)
			btn.add_theme_color_override("font_color", Color(0.85, 0.80, 0.75, 1.0))
			btn.add_theme_constant_override("outline_size", 0)

## ──────────────────────────────────────────
## 分頁切換 (Tabs Logic)
## ──────────────────────────────────────────
func _switch_tab(target_tab: Tab) -> void:
	_current_tab = target_tab
	_stage_layer.visible = (target_tab == Tab.HOME)
	_character_layer.visible = (target_tab == Tab.CHARACTER)
	_adventure_layer.visible = (target_tab == Tab.ADVENTURE)
	_gacha_layer.visible = (target_tab == Tab.GACHA)
	_bag_layer.visible = (target_tab == Tab.BAG)
	_update_dock_styling()

	if target_tab == Tab.CHARACTER:
		_refresh_character_stats()

## ──────────────────────────────────────────
## Tab 1: 主城舞台 (Home Stage)
## ──────────────────────────────────────────
func _build_stage_tab() -> void:
	_stage_layer = Control.new()
	_stage_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_stage_layer)

	## 展台錨定容器 (中央偏下)
	_stage_anchor = Control.new()
	_stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	_stage_anchor.offset_left = 0
	_stage_anchor.offset_top = 40
	_stage_layer.add_child(_stage_anchor)

	## 舞台發光底盤 (圓形光環投影)
	_hero_shadow = TextureRect.new()
	_hero_shadow.offset_left = -150
	_hero_shadow.offset_top = 100
	_hero_shadow.offset_right = 150
	_hero_shadow.offset_bottom = 170
	var s_grad := Gradient.new()
	s_grad.set_color(0, Color(1.0, 0.85, 0.40, 0.85))
	s_grad.set_color(1, Color(1.0, 0.85, 0.40, 0.0))
	var s_tex := GradientTexture2D.new()
	s_tex.gradient = s_grad
	s_tex.fill = GradientTexture2D.FILL_RADIAL
	s_tex.fill_from = Vector2(0.5, 0.5)
	s_tex.fill_to = Vector2(0.5, 0.0)
	_hero_shadow.texture = s_tex
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage_anchor.add_child(_hero_shadow)

	## 中央 2.2 頭身 Q 版兔子紙娃娃展台
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
	elif ResourceLoader.exists("res://assets/sprites/player/rabbit_idle.png"):
		_hero_avatar.texture = load("res://assets/sprites/player/rabbit_idle.png")
	
	_stage_anchor.add_child(_hero_avatar)

	## 點擊角色觸發互動 (跳躍 + 說話泡泡)
	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	var empty_sb := StyleBoxEmpty.new()
	hero_click.add_theme_stylebox_override("normal", empty_sb)
	hero_click.add_theme_stylebox_override("hover", empty_sb)
	hero_click.add_theme_stylebox_override("pressed", empty_sb)
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	## 頭頂稱號與名字
	var tag_vbox := VBoxContainer.new()
	tag_vbox.set_anchors_preset(Control.PRESET_CENTER_TOP)
	tag_vbox.offset_left = -110
	tag_vbox.offset_top = -52
	tag_vbox.offset_right = 110
	tag_vbox.offset_bottom = 0
	tag_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	tag_vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var title_l := Label.new()
	title_l.text = "【初出茅廬的勇者】"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	title_l.add_theme_font_size_override("font_size", 13)
	title_l.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	title_l.add_theme_constant_override("outline_size", 3)
	tag_vbox.add_child(title_l)

	var name_tag := Label.new()
	name_tag.text = "Capoo"
	name_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_tag.add_theme_color_override("font_color", Color.WHITE)
	name_tag.add_theme_font_size_override("font_size", 16)
	name_tag.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	name_tag.add_theme_constant_override("outline_size", 4)
	tag_vbox.add_child(name_tag)
	_hero_avatar.add_child(tag_vbox)

	## 說話對話氣泡
	_speech_bubble = PanelContainer.new()
	_speech_bubble.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_speech_bubble.offset_left = -90
	_speech_bubble.offset_top = -105
	_speech_bubble.offset_right = 140
	_speech_bubble.offset_bottom = -60
	_speech_bubble.visible = false
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = Color(1.0, 0.98, 0.92, 0.96)
	bsb.border_color = Color(0.25, 0.18, 0.12, 1.0)
	bsb.set_border_width_all(2)
	bsb.set_corner_radius_all(12)
	bsb.content_margin_left = 12
	bsb.content_margin_right = 12
	bsb.content_margin_top = 4
	bsb.content_margin_bottom = 4
	_speech_bubble.add_theme_stylebox_override("panel", bsb)

	_speech_label = Label.new()
	_speech_label.text = "今天也要拯救世界喵！"
	_speech_label.add_theme_color_override("font_color", Color(0.2, 0.15, 0.1))
	_speech_label.add_theme_font_size_override("font_size", 13)
	_speech_bubble.add_child(_speech_label)
	_hero_avatar.add_child(_speech_bubble)

	## 左側手遊活動圓鈕欄
	var left_acts := VBoxContainer.new()
	left_acts.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_acts.offset_left = 30
	left_acts.offset_top = 20
	left_acts.offset_right = 110
	left_acts.offset_bottom = -20
	left_acts.add_theme_constant_override("separation", 14)
	_stage_layer.add_child(left_acts)

	_add_circle_act_btn(left_acts, "🎁", "簽到", func():
		_show_act_toast("已領取今日簽到補給！")
	)
	_add_circle_act_btn(left_acts, "📜", "委託", func():
		_show_act_toast("冒險者每日委託已刷新！")
	)
	_add_circle_act_btn(left_acts, "🏆", "演武場", func():
		request_battle.emit("arena")
	)
	_add_circle_act_btn(left_acts, "🌌", "裂縫", func():
		request_battle.emit("rift")
	)

	## 右側：快速出征主線卡片 (手遊經典出發按鈕)
	var quick_card := PanelContainer.new()
	quick_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	quick_card.offset_left = -310
	quick_card.offset_top = -150
	quick_card.offset_right = -40
	quick_card.offset_bottom = -20
	var qsb := StyleBoxFlat.new()
	qsb.bg_color = Color(0.12, 0.09, 0.07, 0.90)
	qsb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	qsb.set_border_width_all(2)
	qsb.set_corner_radius_all(16)
	qsb.content_margin_left = 16
	qsb.content_margin_right = 16
	qsb.content_margin_top = 12
	qsb.content_margin_bottom = 12
	quick_card.add_theme_stylebox_override("panel", qsb)
	_stage_layer.add_child(quick_card)

	var q_vbox := VBoxContainer.new()
	q_vbox.add_theme_constant_override("separation", 8)
	quick_card.add_child(q_vbox)

	var chapter_title := Label.new()
	chapter_title.text = "當前主線：第一章"
	chapter_title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	chapter_title.add_theme_font_size_override("font_size", 13)
	q_vbox.add_child(chapter_title)

	var stage_name := Label.new()
	stage_name.text = "聖獅城 · 守望者之牆"
	stage_name.add_theme_color_override("font_color", Color(0.96, 0.94, 0.90))
	stage_name.add_theme_font_size_override("font_size", 16)
	q_vbox.add_child(stage_name)

	var go_btn := Button.new()
	go_btn.text = "⚔️ 立即出征"
	go_btn.custom_minimum_size = Vector2(0, 44)
	UiStyle.style_button(go_btn, true)
	go_btn.pressed.connect(func():
		request_explore.emit("town")
	)
	q_vbox.add_child(go_btn)

func _add_circle_act_btn(parent: Container, icon_sym: String, label_text: String, cb: Callable) -> void:
	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 3)

	var b := Button.new()
	b.text = icon_sym
	b.custom_minimum_size = Vector2(52, 52)
	b.add_theme_font_size_override("font_size", 22)
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = Color(0.14, 0.11, 0.08, 0.94)
	bsb.border_color = Color(0.85, 0.72, 0.35, 1.0)
	bsb.set_border_width_all(2)
	bsb.set_corner_radius_all(26)
	bsb.shadow_color = Color(0, 0, 0, 0.4)
	bsb.shadow_size = 5
	b.add_theme_stylebox_override("normal", bsb)
	b.add_theme_stylebox_override("hover", bsb)
	b.pressed.connect(cb)
	v.add_child(b)

	var l := Label.new()
	l.text = label_text
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", 12)
	l.add_theme_color_override("font_color", Color(0.98, 0.95, 0.90))
	l.add_theme_color_override("font_outline_color", Color(0.15, 0.10, 0.05))
	l.add_theme_constant_override("outline_size", 3)
	v.add_child(l)

	parent.add_child(v)

func _start_hero_animations() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.02, 0.98), 1.2).set_trans(Tween.TRANS_SINE)
	_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(1.05, 1.05), 1.2).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.99, 1.01), 1.2).set_trans(Tween.TRANS_SINE)
	_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(0.98, 0.98), 1.2).set_trans(Tween.TRANS_SINE)

func _on_hero_clicked() -> void:
	var jump_tween := create_tween()
	jump_tween.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y - 18, 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	jump_tween.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)

	var lines: Array[String] = [
		"準備好迎接下一場戰鬥了嗎！",
		"這套裝備看起來真帥氣～",
		"聽說聚魂殿今天運氣很好喔！",
		"保護王國是我們的責任！"
	]
	var pick: String = lines[randi() % lines.size()]
	_speech_label.text = pick
	_speech_bubble.visible = true
	_speech_bubble.modulate.a = 0.0

	if _bubble_tween and _bubble_tween.is_valid():
		_bubble_tween.kill()
	_bubble_tween = create_tween()
	_bubble_tween.tween_property(_speech_bubble, "modulate:a", 1.0, 0.2)
	_bubble_tween.tween_interval(2.5)
	_bubble_tween.tween_property(_speech_bubble, "modulate:a", 0.0, 0.4)
	_bubble_tween.tween_callback(func(): _speech_bubble.visible = false)

## ──────────────────────────────────────────
## Tab 2: 角色 / 紙娃娃換裝 (Character View)
## ──────────────────────────────────────────
func _build_character_tab() -> void:
	_character_layer = Control.new()
	_character_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_character_layer.visible = false
	_content_root.add_child(_character_layer)

	var hbox := HBoxContainer.new()
	hbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	hbox.offset_left = 50
	hbox.offset_right = -50
	hbox.offset_top = 20
	hbox.offset_bottom = -20
	hbox.add_theme_constant_override("separation", 28)
	_character_layer.add_child(hbox)

	## 左側：全身紙娃娃展示卡片
	var left_card := PanelContainer.new()
	left_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	left_card.size_flags_stretch_ratio = 1.0
	left_card.add_theme_stylebox_override("panel", UiStyle.panel_style_dark())
	hbox.add_child(left_card)

	var left_v := VBoxContainer.new()
	left_v.alignment = BoxContainer.ALIGNMENT_CENTER
	left_v.add_theme_constant_override("separation", 16)
	left_card.add_child(left_v)

	_char_preview = TextureRect.new()
	_char_preview.custom_minimum_size = Vector2(280, 320)
	_char_preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_char_preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_char_preview.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		_char_preview.texture = load("res://assets/sprites/player/poses/idle.png")
	left_v.add_child(_char_preview)

	var act_row := HBoxContainer.new()
	act_row.alignment = BoxContainer.ALIGNMENT_CENTER
	act_row.add_theme_constant_override("separation", 14)
	var btn_idle := Button.new()
	btn_idle.text = "待機姿態"
	UiStyle.style_button(btn_idle, true)
	btn_idle.pressed.connect(func(): _set_preview_pose("idle"))
	act_row.add_child(btn_idle)

	var btn_atk := Button.new()
	btn_atk.text = "攻擊姿態"
	UiStyle.style_button(btn_atk, false)
	btn_atk.pressed.connect(func(): _set_preview_pose("attack"))
	act_row.add_child(btn_atk)

	var btn_skill := Button.new()
	btn_skill.text = "施法姿態"
	UiStyle.style_button(btn_skill, false)
	btn_skill.pressed.connect(func(): _set_preview_pose("skill"))
	act_row.add_child(btn_skill)
	left_v.add_child(act_row)

	## 右側：裝備格與詳細屬性卡片
	var right_card := PanelContainer.new()
	right_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right_card.size_flags_stretch_ratio = 1.4
	right_card.add_theme_stylebox_override("panel", UiStyle.panel_style_dark())
	hbox.add_child(right_card)

	var right_v := VBoxContainer.new()
	right_v.add_theme_constant_override("separation", 16)
	right_card.add_child(right_v)

	var eq_title := Label.new()
	eq_title.text = "獨立部位紙娃娃裝備 (Paperdoll)"
	eq_title.add_theme_font_size_override("font_size", 16)
	eq_title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	right_v.add_child(eq_title)

	_char_equip_grid = GridContainer.new()
	_char_equip_grid.columns = 5
	_char_equip_grid.add_theme_constant_override("h_separation", 12)
	right_v.add_child(_char_equip_grid)

	var slots := ["武器", "上衣", "頭飾", "飾品", "靈魂"]
	for s in slots:
		var slot_p := PanelContainer.new()
		slot_p.custom_minimum_size = Vector2(72, 72)
		var sp_sb := StyleBoxFlat.new()
		sp_sb.bg_color = Color(0.16, 0.13, 0.10, 0.92)
		sp_sb.border_color = Color(0.75, 0.60, 0.40, 0.9)
		sp_sb.set_border_width_all(2)
		sp_sb.set_corner_radius_all(10)
		slot_p.add_theme_stylebox_override("panel", sp_sb)
		
		var sl := Label.new()
		sl.text = s
		sl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sl.add_theme_font_size_override("font_size", 13)
		sl.add_theme_color_override("font_color", Color(0.90, 0.85, 0.80))
		slot_p.add_child(sl)
		_char_equip_grid.add_child(slot_p)

	_char_stats_label = RichTextLabel.new()
	_char_stats_label.bbcode_enabled = true
	_char_stats_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_char_stats_label.add_theme_font_size_override("normal_font_size", 15)
	right_v.add_child(_char_stats_label)

	var equip_btn_row := HBoxContainer.new()
	equip_btn_row.alignment = BoxContainer.ALIGNMENT_END
	var one_click_btn := Button.new()
	one_click_btn.text = "⚡ 一鍵適配最高戰力"
	one_click_btn.custom_minimum_size = Vector2(180, 42)
	UiStyle.style_button(one_click_btn, true)
	one_click_btn.pressed.connect(func():
		_show_act_toast("已一鍵裝備最高評級套裝！")
		_refresh_character_stats()
	)
	equip_btn_row.add_child(one_click_btn)
	right_v.add_child(equip_btn_row)

func _set_preview_pose(pose: String) -> void:
	var path := "res://assets/sprites/player/poses/%s.png" % pose
	if ResourceLoader.exists(path):
		_char_preview.texture = load(path)

func _refresh_character_stats() -> void:
	if not _char_stats_label:
		return
	var hp := 100
	var atk := 25
	var def := 15
	var crit := 5
	var speed := 10
	var power := 482

	if Engine.get_main_loop() is SceneTree:
		var gs: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if gs.has_method("effective_max_hp"): hp = gs.call("effective_max_hp")
			if gs.has_method("effective_atk"): atk = gs.call("effective_atk")
			if gs.has_method("effective_def"): def = gs.call("effective_def")
			if gs.has_method("effective_crit"): crit = gs.call("effective_crit")
			if gs.has_method("effective_speed"): speed = gs.call("effective_speed")
			if gs.has_method("power_score"): power = gs.call("power_score")

	var text := "[color=#ffd700][b]角色戰鬥屬性面板[/b][/color]\n\n"
	text += "綜合戰鬥力：[color=#ffa500][b]%d[/b][/color]\n" % power
	text += "生命上限 (HP)：[color=#ff6b6b]%d[/color]\n" % hp
	text += "物理攻擊 (ATK)：[color=#4dabf7]%d[/color]\n" % atk
	text += "物理防禦 (DEF)：[color=#51cf66]%d[/color]\n" % def
	text += "暴擊率 (CRIT)：[color=#fcc419]%d%%[/color]\n" % crit
	text += "攻擊速度 (SPD)：[color=#cc5de8]%d[/color]\n" % speed
	_char_stats_label.text = text

## ──────────────────────────────────────────
## Tab 3: 冒險出征 (Adventure View)
## ──────────────────────────────────────────
func _build_adventure_tab() -> void:
	_adventure_layer = Control.new()
	_adventure_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_adventure_layer.visible = false
	_content_root.add_child(_adventure_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 60
	panel.offset_right = -60
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style_dark())
	_adventure_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var title := Label.new()
	title.text = "冒險出征 · 章節選擇"
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	v.add_child(title)

	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(scroll)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.add_theme_constant_override("h_separation", 18)
	grid.add_theme_constant_override("v_separation", 18)
	scroll.add_child(grid)

	var chapters: Array = [
		{"name": "第零章 · 破曉之村", "desc": "燃燒的故鄉與最初的覺醒", "map": "village", "star": "⭐⭐⭐"},
		{"name": "第一章 · 王都聖獅", "desc": "繁華王城與狂暴的守護獅", "map": "town", "star": "⭐⭐⭐"},
		{"name": "第二章 · 迷霧之谷", "desc": "籠罩在白霧中的幻影古蹟", "map": "mist_village", "star": "⭐⭐"},
		{"name": "第三章 · 試煉道場", "desc": "隱士武者的極限挑戰", "map": "dojo", "star": "⭐"},
		{"name": "第四章 · 巨木之森", "desc": "遠古精靈與受詛咒的魔獸", "map": "forest", "star": "未解鎖"},
		{"name": "第五章 · 咆哮之海", "desc": "神秘沉船與深海狂濤", "map": "coast", "star": "未解鎖"},
	]

	for c in chapters:
		var c_card := PanelContainer.new()
		c_card.custom_minimum_size = Vector2(250, 115)
		var csb := StyleBoxFlat.new()
		csb.bg_color = Color(0.15, 0.12, 0.09, 0.95)
		csb.border_color = Color(0.70, 0.55, 0.35, 0.9)
		csb.set_border_width_all(2)
		csb.set_corner_radius_all(10)
		csb.content_margin_left = 14
		csb.content_margin_right = 14
		csb.content_margin_top = 10
		csb.content_margin_bottom = 10
		c_card.add_theme_stylebox_override("panel", csb)

		var cv := VBoxContainer.new()
		cv.add_theme_constant_override("separation", 4)
		c_card.add_child(cv)

		var cn := Label.new()
		cn.text = str(c.get("name", ""))
		cn.add_theme_font_size_override("font_size", 14)
		cn.add_theme_color_override("font_color", Color(1.0, 0.88, 0.50))
		cv.add_child(cn)

		var cd := Label.new()
		cd.text = str(c.get("desc", ""))
		cd.add_theme_font_size_override("font_size", 11)
		cd.add_theme_color_override("font_color", Color(0.85, 0.80, 0.75))
		cv.add_child(cd)

		var cs := Label.new()
		cs.text = str(c.get("star", ""))
		cs.add_theme_font_size_override("font_size", 12)
		cv.add_child(cs)

		var btn := Button.new()
		btn.text = "出發探索"
		btn.custom_minimum_size = Vector2(0, 30)
		UiStyle.style_button(btn, true)
		var m_id: String = str(c.get("map", ""))
		btn.pressed.connect(func(): request_explore.emit(m_id))
		cv.add_child(btn)

		grid.add_child(c_card)

## ──────────────────────────────────────────
## Tab 4: 聚魂抽卡 (Gacha View)
## ──────────────────────────────────────────
func _build_gacha_tab() -> void:
	_gacha_layer = Control.new()
	_gacha_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_gacha_layer.visible = false
	_content_root.add_child(_gacha_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 80
	panel.offset_right = -80
	panel.offset_top = 20
	panel.offset_bottom = -20
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style_dark())
	_gacha_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 20)
	panel.add_child(v)

	var title := Label.new()
	title.text = "🔮 萬魂召喚祭壇 · 傳說戰魂降臨"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 22)
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	v.add_child(title)

	var hint := Label.new()
	hint.text = "聚引十四主星之魂 · SSR【紫微星君】機率限時 UP！"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_font_size_override("font_size", 14)
	hint.add_theme_color_override("font_color", Color(0.92, 0.88, 0.82))
	v.add_child(hint)

	var btn_row := HBoxContainer.new()
	btn_row.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_row.add_theme_constant_override("separation", 24)

	var btn_1 := Button.new()
	btn_1.text = "聚魂一次 (💎 100)"
	btn_1.custom_minimum_size = Vector2(180, 52)
	UiStyle.style_button(btn_1, false)
	btn_1.pressed.connect(func(): _do_summon(1))
	btn_row.add_child(btn_1)

	var btn_10 := Button.new()
	btn_10.text = "十連聚魂 (💎 900)"
	btn_10.custom_minimum_size = Vector2(180, 52)
	UiStyle.style_button(btn_10, true)
	btn_10.pressed.connect(func(): _do_summon(10))
	btn_row.add_child(btn_10)

	v.add_child(btn_row)

const SOUL_CARDS: Array[Dictionary] = [
	{"name": "紫微星君", "rarity": "SSR", "title": "帝星之魂", "tex": "res://assets/sprites/souls/star_ziwei.png", "desc": "全隊傷害 +25%"},
	{"name": "天府星君", "rarity": "SSR", "title": "令星之魂", "tex": "res://assets/sprites/souls/star_tianfu.png", "desc": "生命上限 +30%"},
	{"name": "武曲星君", "rarity": "SR", "title": "剛金之魂", "tex": "res://assets/sprites/souls/star_wuqu.png", "desc": "物理暴擊 +15%"},
	{"name": "七殺星君", "rarity": "SR", "title": "肅殺之魂", "tex": "res://assets/sprites/souls/star_qisha.png", "desc": "攻擊穿透 +18%"},
	{"name": "破軍星君", "rarity": "SR", "title": "先鋒之魂", "tex": "res://assets/sprites/souls/star_pojun.png", "desc": "技能急速 +12%"},
	{"name": "天梁星君", "rarity": "SR", "title": "福蔭之魂", "tex": "res://assets/sprites/souls/star_tianliang.png", "desc": "受到傷害 -15%"},
	{"name": "天童星君", "rarity": "R", "title": "純真之魂", "tex": "res://assets/sprites/souls/star_tiantong.png", "desc": "自然回血 +10%"},
	{"name": "太陽星君", "rarity": "R", "title": "光耀之魂", "tex": "res://assets/sprites/souls/star_taiyang.png", "desc": "命中率 +8%"},
	{"name": "太陰星君", "rarity": "R", "title": "清輝之魂", "tex": "res://assets/sprites/souls/star_taiyin.png", "desc": "暴擊抵抗 +8%"},
	{"name": "貪狼星君", "rarity": "R", "title": "機變之魂", "tex": "res://assets/sprites/souls/star_tanlang.png", "desc": "移動速度 +5%"},
]

func _do_summon(count: int) -> void:
	var results: Array[Dictionary] = []
	var has_ssr := false
	for i in range(count):
		var pick_idx := 0
		var r := randf()
		if i == count - 1 and not has_ssr:
			## 保底機制：最後一抽保底 SR 以上
			pick_idx = randi() % 6
		elif r < 0.15:
			pick_idx = randi() % 2 # SSR
			has_ssr = true
		elif r < 0.55:
			pick_idx = 2 + (randi() % 4) # SR
		else:
			pick_idx = 6 + (randi() % 4) # R
		results.append(SOUL_CARDS[pick_idx])
	
	_play_gacha_showcase(results, count)

func _play_gacha_showcase(results: Array[Dictionary], count: int) -> void:
	var has_ssr := false
	for card in results:
		if str(card.get("rarity", "")) == "SSR":
			has_ssr = true
			break

	var overlay := Control.new()
	overlay.name = "GachaShowcaseOverlay"
	overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	overlay.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(overlay)

	## 1. 召喚背景 (深邃星空暗夜)
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.05, 0.04, 0.08, 0.95)
	overlay.add_child(bg)

	## 2. 金光 / 紫光衝天光暈
	var beam := TextureRect.new()
	beam.set_anchors_preset(Control.PRESET_CENTER)
	beam.offset_left = -300
	beam.offset_top = -300
	beam.offset_right = 300
	beam.offset_bottom = 300
	var grad := Gradient.new()
	if has_ssr:
		grad.set_color(0, Color(1.0, 0.85, 0.35, 0.9))
		grad.set_color(1, Color(1.0, 0.70, 0.20, 0.0))
	else:
		grad.set_color(0, Color(0.75, 0.45, 1.0, 0.85))
		grad.set_color(1, Color(0.55, 0.25, 0.90, 0.0))
	var beam_tex := GradientTexture2D.new()
	beam_tex.gradient = grad
	beam_tex.fill = GradientTexture2D.FILL_RADIAL
	beam_tex.fill_from = Vector2(0.5, 0.5)
	beam_tex.fill_to = Vector2(0.5, 0.0)
	beam.texture = beam_tex
	beam.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(beam)

	## 頂部結算標題
	var title_box := VBoxContainer.new()
	title_box.set_anchors_preset(Control.PRESET_TOP_WIDE)
	title_box.offset_top = 22
	title_box.alignment = BoxContainer.ALIGNMENT_CENTER
	title_box.add_theme_constant_override("separation", 4)
	overlay.add_child(title_box)

	var title_l := Label.new()
	title_l.text = "✦ 聚魂召喚結果 ✦"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 24)
	title_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	title_l.add_theme_color_override("font_outline_color", Color(0.2, 0.12, 0.05))
	title_l.add_theme_constant_override("outline_size", 4)
	title_box.add_child(title_l)

	var sub_l := Label.new()
	sub_l.text = "獲得了傳說戰魂的眷顧！" if has_ssr else "群星戰魂已響應您的召喚"
	sub_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub_l.add_theme_font_size_override("font_size", 13)
	sub_l.add_theme_color_override("font_color", Color(0.9, 0.85, 0.8))
	title_box.add_child(sub_l)

	## 中央卡牌網格
	var card_container := GridContainer.new()
	card_container.set_anchors_preset(Control.PRESET_CENTER)
	card_container.columns = 5 if count > 1 else 1
	card_container.add_theme_constant_override("h_separation", 16)
	card_container.add_theme_constant_override("v_separation", 16)
	
	if count > 1:
		card_container.offset_left = -480
		card_container.offset_top = -180
		card_container.offset_right = 480
		card_container.offset_bottom = 180
	else:
		card_container.offset_left = -110
		card_container.offset_top = -140
		card_container.offset_right = 110
		card_container.offset_bottom = 140
	overlay.add_child(card_container)

	for card_data in results:
		var card_card := _build_soul_card_item(card_data)
		card_container.add_child(card_card)

	## 底部確認操作列
	var bot_box := HBoxContainer.new()
	bot_box.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bot_box.offset_bottom = -24
	bot_box.alignment = BoxContainer.ALIGNMENT_CENTER
	bot_box.add_theme_constant_override("separation", 24)
	overlay.add_child(bot_box)

	var again_btn := Button.new()
	again_btn.text = "🔄 再抽十連 (💎 900)" if count > 1 else "🔄 再抽一次 (💎 100)"
	again_btn.custom_minimum_size = Vector2(180, 46)
	UiStyle.style_button(again_btn, false)
	again_btn.pressed.connect(func():
		overlay.queue_free()
		_do_summon(count)
	)
	bot_box.add_child(again_btn)

	var ok_btn := Button.new()
	ok_btn.text = "✨ 收入聚魂閣"
	ok_btn.custom_minimum_size = Vector2(180, 46)
	UiStyle.style_button(ok_btn, true)
	ok_btn.pressed.connect(func():
		overlay.queue_free()
	)
	bot_box.add_child(ok_btn)

	## 全屏金色/光芒微閃動畫
	var flash := ColorRect.new()
	flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	flash.color = Color(1.0, 0.95, 0.85, 0.9) if has_ssr else Color(0.85, 0.70, 1.0, 0.7)
	flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(flash)

	var tw := create_tween()
	tw.tween_property(flash, "modulate:a", 0.0, 0.28).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_callback(flash.queue_free)

func _build_soul_card_item(data: Dictionary) -> PanelContainer:
	var rarity: String = str(data.get("rarity", "R"))
	var is_ssr := (rarity == "SSR")
	var is_sr := (rarity == "SR")

	var card := PanelContainer.new()
	card.custom_minimum_size = Vector2(170, 160)
	var csb := StyleBoxFlat.new()
	if is_ssr:
		csb.bg_color = Color(0.24, 0.18, 0.08, 0.95)
		csb.border_color = Color(1.0, 0.85, 0.35, 1.0)
		csb.shadow_color = Color(1.0, 0.80, 0.25, 0.5)
		csb.shadow_size = 8
	elif is_sr:
		csb.bg_color = Color(0.18, 0.12, 0.24, 0.95)
		csb.border_color = Color(0.80, 0.55, 1.0, 1.0)
		csb.shadow_color = Color(0.70, 0.40, 0.95, 0.4)
		csb.shadow_size = 6
	else:
		csb.bg_color = Color(0.10, 0.14, 0.20, 0.95)
		csb.border_color = Color(0.45, 0.70, 0.95, 0.9)
		csb.shadow_size = 3

	csb.set_border_width_all(2)
	csb.set_corner_radius_all(12)
	csb.content_margin_left = 10
	csb.content_margin_right = 10
	csb.content_margin_top = 8
	csb.content_margin_bottom = 8
	card.add_theme_stylebox_override("panel", csb)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 6)
	card.add_child(v)

	## 稀有度角標
	var r_label := Label.new()
	r_label.text = "✦ %s ✦" % rarity
	r_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	r_label.add_theme_font_size_override("font_size", 14)
	if is_ssr:
		r_label.add_theme_color_override("font_color", Color(1.0, 0.90, 0.35))
	elif is_sr:
		r_label.add_theme_color_override("font_color", Color(0.85, 0.65, 1.0))
	else:
		r_label.add_theme_color_override("font_color", Color(0.55, 0.80, 1.0))
	v.add_child(r_label)

	## 戰魂圖示
	var icon_rect := TextureRect.new()
	icon_rect.custom_minimum_size = Vector2(56, 56)
	icon_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	var t_path: String = str(data.get("tex", ""))
	if ResourceLoader.exists(t_path):
		icon_rect.texture = load(t_path)
	v.add_child(icon_rect)

	## 戰魂名稱
	var name_l := Label.new()
	name_l.text = str(data.get("name", ""))
	name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_l.add_theme_font_size_override("font_size", 13)
	name_l.add_theme_color_override("font_color", Color(0.98, 0.95, 0.90))
	v.add_child(name_l)

	## 加成說明
	var desc_l := Label.new()
	desc_l.text = str(data.get("desc", ""))
	desc_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc_l.add_theme_font_size_override("font_size", 11)
	desc_l.add_theme_color_override("font_color", Color(0.85, 0.80, 0.75))
	v.add_child(desc_l)

	return card

## ──────────────────────────────────────────
## Tab 5: 背包 (Bag View)
## ──────────────────────────────────────────
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
	panel.add_theme_stylebox_override("panel", UiStyle.panel_style_dark())
	_bag_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	panel.add_child(v)

	var title := Label.new()
	title.text = "🎒 冒險者背包"
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.40))
	v.add_child(title)

	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(scroll)

	var grid := GridContainer.new()
	grid.columns = 8
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 12)
	scroll.add_child(grid)

	for i in range(32):
		var slot := PanelContainer.new()
		slot.custom_minimum_size = Vector2(64, 64)
		var ssb := StyleBoxFlat.new()
		ssb.bg_color = Color(0.16, 0.13, 0.10, 0.92)
		ssb.border_color = Color(0.55, 0.45, 0.32, 0.8)
		ssb.set_border_width_all(1)
		ssb.set_corner_radius_all(8)
		slot.add_theme_stylebox_override("panel", ssb)
		
		var l := Label.new()
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 12)
		if i == 0:
			l.text = "木劍"
			l.add_theme_color_override("font_color", Color(1.0, 0.85, 0.4))
		elif i == 1:
			l.text = "紅藥水x5"
		elif i == 2:
			l.text = "靈魂晶石"
		else:
			l.text = ""
		slot.add_child(l)
		grid.add_child(slot)

## ──────────────────────────────────────────
## 外部狀態刷新
## ──────────────────────────────────────────
func refresh_hud() -> void:
	var lv := 12
	var hero_name := "Capoo"
	var power := 482
	var gold := 12500
	var energy := 15
	var gems := 350

	if Engine.get_main_loop() is SceneTree:
		var gs: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if "level" in gs and int(gs.level) > 0: lv = int(gs.level)
			if "player_name" in gs and str(gs.player_name) != "": hero_name = str(gs.player_name)
			if gs.has_method("power_score"): power = gs.call("power_score")
			if "gold" in gs and int(gs.gold) > 0: gold = int(gs.gold)

		var es: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EnergySystem")
		if es and es.has_method("current"):
			energy = es.call("current")

	if _lv_label: _lv_label.text = "Lv.%d" % lv
	if _name_label: _name_label.text = hero_name
	if _power_label: _power_label.text = "戰力 %d" % power
	if _energy_label: _energy_label.text = "%d/15" % energy
	if _gold_label: _gold_label.text = str(gold)
	if _gem_label: _gem_label.text = str(gems)

func _show_act_toast(msg: String) -> void:
	var toast := Label.new()
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	toast.offset_left = -160
	toast.offset_right = 160
	toast.offset_top = 100
	toast.offset_bottom = 140
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
