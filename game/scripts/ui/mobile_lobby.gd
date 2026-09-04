class_name MobileLobby
extends Control
## 勇者之魂 (Brave Soul) - 現代 Q 萌多巴胺手遊大廳 (Tata Adventure Style)
## 視覺特徵：慶典彩色吊旗 + 飄動陽光粒子 + 白兔多姿態動態呼吸與多動作點擊互動 (無 Emoji)

signal request_battle(mode: String)
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const DEFAULT_HERO_NAME: String = "新人"

enum Tab {
	VILLAGE,     ## 今日村莊大廳 (主城)
	CHARACTER,   ## 角色 / 三欄武器紙娃娃
	ADVENTURE,   ## 四區出征關卡
	SOUL_HALL,   ## 聚魂殿堂 (五色葫蘆跳階)
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

## 角色動態與姿態
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _hero_name_tag: Label
var _rainbow_ring: TextureRect
var _speech_bubble: PanelContainer
var _speech_label: Label
var _particles_root: Control
var _breathe_tween: Tween
var _bubble_tween: Tween
var _idle_action_timer: float = 0.0
var _is_interacting: bool = false

## 動作姿態紋理快取
var _tex_idle: Texture2D
var _tex_attack: Texture2D
var _tex_skill: Texture2D
var _tex_telegraph: Texture2D
var _tex_recover: Texture2D

## 聚魂殿五色葫蘆狀態
var _gourd_lit: Array[bool] = [true, false, false, false, false]
var _gourd_btns: Array[Button] = []

## 四地區出征
var _selected_region: int = 1 # 0: 破曉之原, 1: 聖獅王都, 2: 迷霧雪境, 3: 深淵龍窟
var _stages_container: VBoxContainer

## 慶典飄動彩旗
var _bunting_flags: Control

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

static func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null

func _get_hero_name() -> String:
	var gs := _gs()
	if gs and "player_name" in gs:
		var pname: String = str(gs.player_name).strip_edges()
		if not pname.is_empty():
			return pname
	return DEFAULT_HERO_NAME

func _ready() -> void:
	custom_minimum_size = Vector2(1280, 720)
	size = Vector2(1280, 720)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_load_hero_poses()
	_build_ui()
	refresh_hud()
	_switch_tab(Tab.VILLAGE)

func _load_hero_poses() -> void:
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		_tex_idle = load("res://assets/sprites/player/poses/idle.png")
	if ResourceLoader.exists("res://assets/sprites/player/poses/attack.png"):
		_tex_attack = load("res://assets/sprites/player/poses/attack.png")
	if ResourceLoader.exists("res://assets/sprites/player/poses/skill.png"):
		_tex_skill = load("res://assets/sprites/player/poses/skill.png")
	if ResourceLoader.exists("res://assets/sprites/player/poses/telegraph.png"):
		_tex_telegraph = load("res://assets/sprites/player/poses/telegraph.png")
	if ResourceLoader.exists("res://assets/sprites/player/poses/recover.png"):
		_tex_recover = load("res://assets/sprites/player/poses/recover.png")

func _build_ui() -> void:
	## 1. 背景插畫 (明亮飽和的童話主城)
	var bg := TextureRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/maps/sky_kingdom_bg.png"):
		bg.texture = load("res://assets/sprites/maps/sky_kingdom_bg.png")
	elif ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	elif ResourceLoader.exists("res://assets/sprites/illustrations/title_bg.png"):
		bg.texture = load("res://assets/sprites/illustrations/title_bg.png")
	add_child(bg)

	## 2. 繽紛童話慶典彩旗 (Carnival Bunting Flags)
	_build_carnival_buntings()

	## 3. 飄散的陽光微光金星粒子
	_particles_root = Control.new()
	_particles_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_particles_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_particles_root)
	_spawn_floating_sunlight_particles()

	## 4. 內容掛載層
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

	## 5. 頂部狀態列 (無 Emoji，純淨大氣手遊標籤)
	_build_top_hud()

	## 6. 底部飽滿果凍導航欄 (無 Emoji，超大胖胖字)
	_build_bottom_dock()

## ──────────────────────────────────────────
## 繽紛童話慶典三角旗 (Carnival Pennant Bunting)
## ──────────────────────────────────────────
func _build_carnival_buntings() -> void:
	_bunting_flags = Control.new()
	_bunting_flags.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_bunting_flags.offset_top = 74
	_bunting_flags.offset_bottom = 120
	_bunting_flags.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_bunting_flags)

	var flag_colors: Array[Color] = [
		Color(1.0, 0.40, 0.60),  # 草莓粉
		Color(1.0, 0.82, 0.18),  # 蜜糖黃
		Color(0.28, 0.85, 0.42), # 薄荷綠
		Color(0.24, 0.68, 0.98), # 晴空藍
		Color(1.0, 0.54, 0.12),  # 活力橘
		Color(0.80, 0.50, 1.0),  # 夢幻紫
	]

	var flag_count := 24
	var step_w := 1280.0 / float(flag_count)
	for i in range(flag_count):
		var p := Polygon2D.new()
		var col := flag_colors[i % flag_colors.size()]
		p.color = col
		var x1 := float(i) * step_w
		var x2 := x1 + step_w
		var xc := x1 + step_w * 0.5
		# 自然垂墜弧度
		var curve_y := sin(float(i) / float(flag_count) * PI) * 14.0
		var pts := PackedVector2Array([
			Vector2(x1, curve_y),
			Vector2(x2, curve_y),
			Vector2(xc, curve_y + 24.0)
		])
		p.polygon = pts
		_bunting_flags.add_child(p)

	# 微風輕擺動畫
	var tw := create_tween().set_loops()
	tw.tween_property(_bunting_flags, "position:y", 2.0, 1.6).set_trans(Tween.TRANS_SINE)
	tw.tween_property(_bunting_flags, "position:y", 0.0, 1.6).set_trans(Tween.TRANS_SINE)

## ──────────────────────────────────────────
## 陽光漂浮微粒 (Sunshine Particles)
## ──────────────────────────────────────────
func _spawn_floating_sunlight_particles() -> void:
	for i in range(14):
		var star := Label.new()
		star.text = "✦"
		star.add_theme_font_size_override("font_size", 12 + (i % 3) * 4)
		var c := Color(1.0, 0.90, 0.45, 0.75) if i % 2 == 0 else Color(1.0, 0.60, 0.80, 0.65)
		star.add_theme_color_override("font_color", c)
		star.position = Vector2(randf_range(40.0, 1240.0), randf_range(100.0, 580.0))
		_particles_root.add_child(star)

		# 漂浮與呼吸淡入淡出
		var tw := create_tween().set_loops()
		var dur := randf_range(2.0, 3.5)
		var dy := randf_range(-18.0, -35.0)
		tw.tween_property(star, "position:y", star.position.y + dy, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.2, dur * 0.5)
		tw.tween_property(star, "position:y", star.position.y, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.85, dur * 0.5)

## ──────────────────────────────────────────
## 頂部大尺寸多巴胺 HUD
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
	sb.border_color = UiStyle.TATA_CARD_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.set_corner_radius_all(22)
	sb.shadow_color = Color(0.25, 0.18, 0.10, 0.2)
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
	psb.border_color = UiStyle.TATA_ORANGE
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
	_lv_label.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	_lv_label.add_theme_font_size_override("font_size", 16)
	_lv_label.add_theme_color_override("font_outline_color", Color(1, 1, 1, 0.9))
	_lv_label.add_theme_constant_override("outline_size", 2)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = _get_hero_name()
	_name_label.add_theme_font_size_override("font_size", 17)
	_name_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_name_label.add_theme_color_override("font_outline_color", Color(1, 1, 1, 0.9))
	_name_label.add_theme_constant_override("outline_size", 2)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	_power_label = Label.new()
	_power_label.text = "戰力 482"
	_power_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_power_label.add_theme_font_size_override("font_size", 13)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 多巴胺立體三寶果凍膠囊
	_energy_label = _add_clean_capsule(h, "能量", "15/15", UiStyle.TATA_GREEN)
	_gold_label = _add_clean_capsule(h, "金幣", "12,500", UiStyle.TATA_ORANGE)
	_gem_label = _add_clean_capsule(h, "晶石", "350", UiStyle.TATA_BLUE)

	var set_btn := Button.new()
	set_btn.text = "設置"
	set_btn.custom_minimum_size = Vector2(64, 46)
	set_btn.add_theme_font_size_override("font_size", 16)
	UiStyle.style_button(set_btn, false)
	set_btn.pressed.connect(func():
		var s_scn := load("res://scripts/ui/mobile_settings.gd")
		var s_ui: Control = s_scn.new()
		s_ui.z_index = 80
		add_child(s_ui)
	)
	h.add_child(set_btn)

func _add_clean_capsule(parent: Container, title: String, val: String, accent: Color) -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.98, 0.97, 0.94, 0.96)
	csb.border_color = accent
	csb.set_border_width_all(2)
	csb.border_width_bottom = 4
	csb.set_corner_radius_all(16)
	csb.content_margin_left = 12
	csb.content_margin_right = 12
	csb.content_margin_top = 4
	csb.content_margin_bottom = 4
	csb.shadow_color = Color(0.25, 0.18, 0.10, 0.15)
	csb.shadow_size = 5
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 8)
	var il := Label.new()
	il.text = title
	il.add_theme_font_size_override("font_size", 13)
	il.add_theme_color_override("font_color", accent)
	il.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.9))
	il.add_theme_constant_override("outline_size", 2)
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.add_theme_font_size_override("font_size", 16)
	vl.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	vl.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.9))
	vl.add_theme_constant_override("outline_size", 2)
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
	dock.offset_left = 24
	dock.offset_right = -24
	dock.offset_top = -84
	dock.offset_bottom = -12
	
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = UiStyle.TATA_CARD_BG
	dsb.border_color = UiStyle.TATA_CARD_BORDER
	dsb.set_border_width_all(2)
	dsb.border_width_bottom = 6
	dsb.set_corner_radius_all(24)
	dsb.shadow_color = Color(0.25, 0.18, 0.10, 0.25)
	dsb.shadow_size = 12
	dock.add_theme_stylebox_override("panel", dsb)
	add_child(dock)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 16)
	dock.add_child(h)

	var tabs := [
		{"tab": Tab.VILLAGE, "title": "今日村莊"},
		{"tab": Tab.CHARACTER, "title": "角色裝備"},
		{"tab": Tab.ADVENTURE, "title": "四區出征"},
		{"tab": Tab.SOUL_HALL, "title": "聚魂殿堂"},
		{"tab": Tab.BAG, "title": "冒險背包"},
	]

	_dock_buttons.clear()
	for d in tabs:
		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(0, 56)
		btn.text = str(d["title"])
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
## 每幀小動作判定 (動態待機自然活化)
## ──────────────────────────────────────────
func _process(delta: float) -> void:
	if _current_tab != Tab.VILLAGE or _is_interacting:
		return

	_idle_action_timer += delta
	if _idle_action_timer > 5.0:
		_idle_action_timer = 0.0
		_play_random_idle_flavor()

func _play_random_idle_flavor() -> void:
	var roll := randi() % 3
	if roll == 0 and _tex_telegraph:
		## 小伸展站姿
		_hero_avatar.texture = _tex_telegraph
		var tw := create_tween()
		tw.tween_interval(1.2)
		tw.tween_callback(func():
			if not _is_interacting and _tex_idle:
				_hero_avatar.texture = _tex_idle
		)
	elif roll == 1 and _tex_recover:
		## 伸個懶腰
		_hero_avatar.texture = _tex_recover
		var tw := create_tween()
		tw.tween_interval(1.0)
		tw.tween_callback(func():
			if not _is_interacting and _tex_idle:
				_hero_avatar.texture = _tex_idle
		)

## ──────────────────────────────────────────
## Tab 1: 今日村莊 (彩虹展台 + 點擊互動 + 粒子爆發)
## ──────────────────────────────────────────
func _build_village_tab() -> void:
	_village_layer = Control.new()
	_village_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_village_layer)

	## 中央英雄展台
	var stage_anchor := Control.new()
	stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	stage_anchor.offset_top = 45
	_village_layer.add_child(stage_anchor)

	## 1. 彩虹多巴胺炫光展台底盤
	_rainbow_ring = TextureRect.new()
	_rainbow_ring.offset_left = -170
	_rainbow_ring.offset_top = 90
	_rainbow_ring.offset_right = 170
	_rainbow_ring.offset_bottom = 185
	var r_grad := Gradient.new()
	r_grad.set_color(0, Color(1.0, 0.85, 0.25, 0.95))
	r_grad.set_color(1, Color(0.28, 0.85, 0.42, 0.0))
	var r_tex := GradientTexture2D.new()
	r_tex.gradient = r_grad
	r_tex.fill = GradientTexture2D.FILL_RADIAL
	r_tex.fill_from = Vector2(0.5, 0.5)
	r_tex.fill_to = Vector2(0.5, 0.0)
	_rainbow_ring.texture = r_tex
	_rainbow_ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage_anchor.add_child(_rainbow_ring)

	## 2. 2.2 頭身白兔主角
	_hero_avatar = TextureRect.new()
	_hero_avatar.offset_left = -125
	_hero_avatar.offset_top = -140
	_hero_avatar.offset_right = 125
	_hero_avatar.offset_bottom = 125
	_hero_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_avatar.pivot_offset = Vector2(125, 240)
	if _tex_idle:
		_hero_avatar.texture = _tex_idle
	stage_anchor.add_child(_hero_avatar)

	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	## 3. 頭頂稱號與名字 (Q 萌粉圓體)
	var tag_v := VBoxContainer.new()
	tag_v.set_anchors_preset(Control.PRESET_CENTER_TOP)
	tag_v.offset_left = -100
	tag_v.offset_top = -52
	tag_v.offset_right = 100
	tag_v.offset_bottom = 0
	tag_v.alignment = BoxContainer.ALIGNMENT_CENTER
	tag_v.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var title_l := Label.new()
	title_l.text = "【初出茅廬】"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 12)
	title_l.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	title_l.add_theme_color_override("font_outline_color", Color(1, 1, 1, 0.9))
	title_l.add_theme_constant_override("outline_size", 2)
	tag_v.add_child(title_l)

	_hero_name_tag = Label.new()
	_hero_name_tag.text = _get_hero_name()
	_hero_name_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hero_name_tag.add_theme_font_size_override("font_size", 16)
	_hero_name_tag.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_hero_name_tag.add_theme_color_override("font_outline_color", Color(1, 1, 1, 0.9))
	_hero_name_tag.add_theme_constant_override("outline_size", 3)
	tag_v.add_child(_hero_name_tag)
	_hero_avatar.add_child(tag_v)

	## 4. 點擊彈出的萌系對話氣泡
	_speech_bubble = PanelContainer.new()
	_speech_bubble.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_speech_bubble.offset_left = -110
	_speech_bubble.offset_top = -110
	_speech_bubble.offset_right = 150
	_speech_bubble.offset_bottom = -60
	_speech_bubble.visible = false
	var bub_sb := StyleBoxFlat.new()
	bub_sb.bg_color = Color(1.0, 0.99, 0.95, 0.98)
	bub_sb.border_color = UiStyle.TATA_ORANGE
	bub_sb.set_border_width_all(2)
	bub_sb.set_corner_radius_all(14)
	bub_sb.shadow_color = Color(0.25, 0.18, 0.10, 0.25)
	bub_sb.shadow_size = 6
	bub_sb.content_margin_left = 12
	bub_sb.content_margin_right = 12
	bub_sb.content_margin_top = 6
	bub_sb.content_margin_bottom = 6
	_speech_bubble.add_theme_stylebox_override("panel", bub_sb)

	_speech_label = Label.new()
	_speech_label.text = "今天也要元氣滿滿出發！"
	_speech_label.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	_speech_label.add_theme_font_size_override("font_size", 14)
	_speech_bubble.add_child(_speech_label)
	_hero_avatar.add_child(_speech_bubble)

	## 呼吸動畫
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)

	## 左側四大殿堂手繪卡牌 (無重複！王都鐵匠、手藝工坊、演武競技、冒險委託)
	var left_shops := VBoxContainer.new()
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 32
	left_shops.offset_top = 16
	left_shops.offset_right = 272
	left_shops.offset_bottom = -16
	left_shops.add_theme_constant_override("separation", 14)
	_village_layer.add_child(left_shops)

	_add_texture_card(left_shops, "res://assets/sprites/ui/mobile/card_hall_forge.png", func():
		_show_toast("進入王都鐵匠：可將裝備品質晉階為紫裝！")
	)
	_add_texture_card(left_shops, "res://assets/sprites/ui/mobile/card_hall_gem.png", func():
		_show_toast("進入手藝工坊：紅黃藍石三合一熔煉！")
	)
	_add_texture_card(left_shops, "res://assets/sprites/ui/mobile/card_hall_arena.png", func():
		request_battle.emit("arena")
	)
	_add_texture_card(left_shops, "res://assets/sprites/ui/mobile/card_hall_quest.png", func():
		_show_toast("已領取今日簽到與冒險委託補給！")
	)

	## 右側：專注於主線推進 (無重複簽到按鈕)
	var right_card := PanelContainer.new()
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -340
	right_card.offset_top = -170
	right_card.offset_right = -32
	right_card.offset_bottom = -16
	right_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_village_layer.add_child(right_card)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 10)
	right_card.add_child(rv)

	var ch_lbl := Label.new()
	ch_lbl.text = "冒險出征 · 當前主線"
	ch_lbl.add_theme_font_size_override("font_size", 14)
	ch_lbl.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	rv.add_child(ch_lbl)

	var s_name := Label.new()
	s_name.text = "第二地區 · 聖獅王城 (2-4 BOSS)"
	s_name.add_theme_font_size_override("font_size", 17)
	s_name.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	rv.add_child(s_name)

	_add_texture_button(rv, "res://assets/sprites/ui/mobile/btn_go_adventure.png", Vector2(280, 68), func():
		_switch_tab(Tab.ADVENTURE)
	)

func _add_texture_card(parent: Container, tex_path: String, cb: Callable) -> void:
	var tb := TextureButton.new()
	tb.custom_minimum_size = Vector2(240, 72)
	tb.ignore_texture_size = true
	tb.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	if ResourceLoader.exists(tex_path):
		tb.texture_normal = load(tex_path)
	tb.pressed.connect(cb)
	parent.add_child(tb)

func _add_texture_button(parent: Container, tex_path: String, sz: Vector2, cb: Callable) -> void:
	var tb := TextureButton.new()
	tb.custom_minimum_size = sz
	tb.ignore_texture_size = true
	tb.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	if ResourceLoader.exists(tex_path):
		tb.texture_normal = load(tex_path)
	tb.pressed.connect(cb)
	parent.add_child(tb)

## ──────────────────────────────────────────
## 點擊主角：切換動態姿態 + 爆發彩色粒子 + 氣泡
## ──────────────────────────────────────────
func _on_hero_clicked() -> void:
	_is_interacting = true
	var act_type := randi() % 3

	var speech_lines := [
		"看我的旋風斬～呀！",
		"今天也要元氣滿滿出發！",
		"我的短劍已經磨得亮晶晶啦～",
		"哇！不要一直戳人家的長耳朵啦～",
		"隨時準備好去挑戰大首領！"
	]
	_speech_label.text = speech_lines[randi() % speech_lines.size()]
	_speech_bubble.visible = true
	_speech_bubble.modulate.a = 0.0

	if _bubble_tween and _bubble_tween.is_valid():
		_bubble_tween.kill()
	_bubble_tween = create_tween()
	_bubble_tween.tween_property(_speech_bubble, "modulate:a", 1.0, 0.15)
	_bubble_tween.tween_interval(2.2)
	_bubble_tween.tween_property(_speech_bubble, "modulate:a", 0.0, 0.3)
	_bubble_tween.tween_callback(func(): _speech_bubble.visible = false)

	## 噴散 8 顆彩色糖果星芒粒子
	_burst_click_particles(_hero_avatar.global_position + Vector2(125, 120))

	var tw := create_tween()
	match act_type:
		0:
			## 揮劍劈砍姿態
			if _tex_attack: _hero_avatar.texture = _tex_attack
			tw.tween_property(_hero_avatar, "position", Vector2(-110, -165), 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "position", Vector2(-125, -140), 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.tween_interval(0.4)
			tw.tween_callback(func():
				if _tex_recover: _hero_avatar.texture = _tex_recover
			)
			tw.tween_interval(0.3)
			tw.tween_callback(func():
				if _tex_idle: _hero_avatar.texture = _tex_idle
				_is_interacting = false
			)
		1:
			## 聚氣勝利姿態
			if _tex_skill: _hero_avatar.texture = _tex_skill
			tw.tween_property(_hero_avatar, "scale", Vector2(1.15, 1.15), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "scale", Vector2(1.0, 1.0), 0.2).set_trans(Tween.TRANS_SINE)
			tw.tween_interval(0.6)
			tw.tween_callback(func():
				if _tex_idle: _hero_avatar.texture = _tex_idle
				_is_interacting = false
			)
		2:
			## 開心翻轉大跳躍
			tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y - 35, 0.15).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", -1.0, 0.15)
			tw.tween_property(_hero_avatar, "position:y", _hero_avatar.position.y, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", 1.0, 0.18)
			tw.tween_callback(func():
				_is_interacting = false
			)

func _burst_click_particles(center_pos: Vector2) -> void:
	var cols: Array[Color] = [
		Color(1.0, 0.85, 0.25),  # 金黃
		Color(1.0, 0.40, 0.60),  # 草莓粉
		Color(0.28, 0.85, 0.42), # 薄荷綠
		Color(0.24, 0.68, 0.98), # 晴空藍
	]
	for i in range(8):
		var star := Label.new()
		star.text = "✦"
		star.add_theme_font_size_override("font_size", 16)
		star.add_theme_color_override("font_color", cols[i % cols.size()])
		star.global_position = center_pos
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(star)

		var angle := float(i) * (PI * 2.0 / 8.0)
		var dist := randf_range(40.0, 80.0)
		var target := center_pos + Vector2(cos(angle), sin(angle)) * dist

		var tw := create_tween()
		tw.tween_property(star, "global_position", target, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(star, "modulate:a", 0.0, 0.35).set_delay(0.15)
		tw.tween_callback(star.queue_free)

## ──────────────────────────────────────────
## Tab 4: 聚魂殿堂 (藝術圖片十連鈕)
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
	t.text = "✦ 聚魂殿堂 · 五色葫蘆跳階 ✦"
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 24)
	t.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	v.add_child(t)

	var desc := Label.new()
	desc.text = "聚引十四主星之魂：七煞(攻) · 武曲(防) · 天機(血) · 貪狼(命) · 紫微(閃) · 破軍(爆)。點擊點亮更高階葫蘆！"
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 13)
	desc.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	v.add_child(desc)

	var gourd_row := HBoxContainer.new()
	gourd_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gourd_row.add_theme_constant_override("separation", 20)
	v.add_child(gourd_row)

	var gourds_data := [
		{"name": "白玉葫蘆", "cost": 100, "color": Color(0.85, 0.85, 0.85)},
		{"name": "碧綠葫蘆", "cost": 300, "color": UiStyle.TATA_GREEN},
		{"name": "青藍葫蘆", "cost": 800, "color": UiStyle.TATA_BLUE},
		{"name": "紫霄葫蘆", "cost": 2000, "color": UiStyle.TATA_PINK},
		{"name": "澄金葫蘆", "cost": 5000, "color": UiStyle.TATA_YELLOW}
	]

	_gourd_btns.clear()
	for i in range(gourds_data.size()):
		var gd: Dictionary = gourds_data[i]
		var gb := _build_gourd_card(gd, i)
		gourd_row.add_child(gb)
		_gourd_btns.append(gb)

	_refresh_gourds_ui()

	var bot_h := HBoxContainer.new()
	bot_h.alignment = BoxContainer.ALIGNMENT_CENTER
	bot_h.add_theme_constant_override("separation", 28)
	v.add_child(bot_h)

	var btn_absorb := Button.new()
	btn_absorb.text = "一鍵吸收灰魂 (換經驗)"
	btn_absorb.custom_minimum_size = Vector2(210, 52)
	btn_absorb.add_theme_font_size_override("font_size", 16)
	UiStyle.style_button(btn_absorb, false)
	btn_absorb.pressed.connect(func():
		_show_toast("已將廢魂轉化為 480 戰魂經驗值！")
	)
	bot_h.add_child(btn_absorb)

	_add_texture_button(bot_h, "res://assets/sprites/ui/mobile/btn_draw_10.png", Vector2(220, 56), func():
		_do_gourd_draw(0, true)
	)

func _build_gourd_card(gd: Dictionary, idx: int) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(145, 170)
	btn.name = "GourdBtn_%d" % idx

	var v := VBoxContainer.new()
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 10)
	btn.add_child(v)

	var circle := PanelContainer.new()
	circle.custom_minimum_size = Vector2(56, 56)
	var csb := StyleBoxFlat.new()
	csb.bg_color = gd["color"] as Color
	csb.set_corner_radius_all(28)
	csb.border_color = Color(1, 1, 1, 0.9)
	csb.set_border_width_all(2)
	circle.add_theme_stylebox_override("panel", csb)
	v.add_child(circle)

	var nl := Label.new()
	nl.text = str(gd["name"])
	nl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nl.add_theme_font_size_override("font_size", 16)
	nl.add_theme_color_override("font_color", gd["color"] as Color)
	v.add_child(nl)

	var cl := Label.new()
	cl.text = "金幣 %d" % int(gd["cost"])
	cl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cl.add_theme_font_size_override("font_size", 13)
	cl.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
		var is_lit := _gourd_lit[i]
		var sb := StyleBoxFlat.new()
		if is_lit:
			sb.bg_color = Color(1.0, 0.98, 0.92, 0.98)
			sb.border_color = UiStyle.TATA_ORANGE
			sb.set_border_width_all(3)
			sb.border_width_bottom = 6
			sb.set_corner_radius_all(20)
			sb.shadow_color = Color(0.25, 0.18, 0.10, 0.25)
			sb.shadow_size = 10
			b.disabled = false
		else:
			sb.bg_color = Color(0.95, 0.93, 0.90, 0.7)
			sb.border_color = Color(0.70, 0.65, 0.60, 0.5)
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
		_show_toast("靈光閃爍！成功點亮更高階的葫蘆！")
	else:
		for i in range(1, 5):
			_gourd_lit[i] = false
		_show_toast("聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
	
	_refresh_gourds_ui()

## ──────────────────────────────────────────
## Tab 3: 四地區出征 (藝術圖片開戰鈕)
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

	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)

	var regions: Array[String] = ["第一地區 · 破曉之原", "第二地區 · 聖獅王都", "第三地區 · 迷霧雪境", "第四地區 · 深淵龍窟"]
	for i in range(regions.size()):
		var rb := Button.new()
		rb.text = regions[i]
		rb.custom_minimum_size = Vector2(175, 46)
		rb.add_theme_font_size_override("font_size", 16)
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
		{"num": "2-1", "name": "王城外郭 · 守望關隘", "type": "前哨雜魚", "cost": 1, "power": 380, "mode": "road_bandit"},
		{"num": "2-2", "name": "市集街道 · 潛伏暗哨", "type": "精英戰鬥", "cost": 1, "power": 420, "mode": "road_bandit"},
		{"num": "2-3", "name": "下水道口 · 腐化黏怪", "type": "精英戰鬥", "cost": 1, "power": 450, "mode": "road_bandit"},
		{"num": "2-4", "name": "聖獅王宮 · 狂暴守護者", "type": "首領部位破壞", "cost": 3, "power": 520, "mode": "leo"},
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
	c.custom_minimum_size = Vector2(430, 105)
	var csb := StyleBoxFlat.new()
	var is_boss: bool = str(s["type"]).find("首領") >= 0
	csb.bg_color = Color(1.0, 0.98, 0.92, 0.98) if is_boss else Color(0.98, 0.97, 0.94, 0.96)
	csb.border_color = UiStyle.TATA_ORANGE if is_boss else UiStyle.TATA_CARD_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 16
	csb.content_margin_right = 16
	csb.content_margin_top = 12
	csb.content_margin_bottom = 12
	csb.shadow_color = Color(0.25, 0.18, 0.10, 0.2)
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
	num_l.add_theme_font_size_override("font_size", 18)
	num_l.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	t_row.add_child(num_l)

	var name_l := Label.new()
	name_l.text = str(s["name"])
	name_l.add_theme_font_size_override("font_size", 16)
	name_l.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	t_row.add_child(name_l)
	v.add_child(t_row)

	var inf_row := HBoxContainer.new()
	inf_row.add_theme_constant_override("separation", 14)
	var typ_l := Label.new()
	typ_l.text = str(s["type"])
	typ_l.add_theme_font_size_override("font_size", 13)
	typ_l.add_theme_color_override("font_color", UiStyle.TATA_ORANGE if is_boss else Color(0.45, 0.38, 0.30))
	inf_row.add_child(typ_l)

	var pwr_l := Label.new()
	pwr_l.text = "推薦戰力: %d" % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 13)
	pwr_l.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	inf_row.add_child(pwr_l)
	v.add_child(inf_row)

	var btn_img := "res://assets/sprites/ui/mobile/btn_boss_battle.png" if is_boss else "res://assets/sprites/ui/mobile/btn_normal_battle.png"
	var m: String = str(s["mode"])
	_add_texture_button(h, btn_img, Vector2(160, 52) if is_boss else Vector2(145, 50), func():
		request_battle.emit(m)
	)

	return c

## ──────────────────────────────────────────
## Tab 2 & Tab 5: 角色紙娃娃與背包 (無 Emoji)
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
	if _tex_idle:
		prev.texture = _tex_idle
	l_card.add_child(prev)

	var r_v := VBoxContainer.new()
	r_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	r_v.add_theme_constant_override("separation", 14)
	h.add_child(r_v)

	var title := Label.new()
	title.text = "✦ 三欄武器輪替系統 (原作節奏) ✦"
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
	r_v.add_child(title)

	var w_row := HBoxContainer.new()
	w_row.add_theme_constant_override("separation", 12)
	r_v.add_child(w_row)

	var w_slots := ["首選: 鐵劍 (4次)", "副手: 獵弓 (4次)", "絕技: 拳套 (5連擊)"]
	for ws in w_slots:
		var p := PanelContainer.new()
		p.custom_minimum_size = Vector2(130, 68)
		var psb := StyleBoxFlat.new()
		psb.bg_color = Color(0.98, 0.97, 0.94, 0.96)
		psb.border_color = UiStyle.TATA_ORANGE
		psb.set_border_width_all(2)
		psb.border_width_bottom = 4
		psb.set_corner_radius_all(12)
		p.add_theme_stylebox_override("panel", psb)
		var l := Label.new()
		l.text = ws
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 13)
		l.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
		p.add_child(l)
		w_row.add_child(p)

	var stats := RichTextLabel.new()
	stats.bbcode_enabled = true
	stats.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stats.add_theme_font_size_override("normal_font_size", 15)
	stats.text = "\n[color=#e06010][b]角色戰鬥屬性 (有效戰力 482)[/b][/color]\n\n"
	stats.text += "生命力 (HP): [color=#e03060]520[/color]   物理攻擊: [color=#1080d0]95[/color]\n"
	stats.text += "物理防禦: [color=#20a040]48[/color]   暴擊率: [color=#e08010]22%[/color]\n"
	stats.text += "怒氣量表: [color=#e06010]20 點 (滿怒自動觸發暴怒 +25% 攻防暴)[/color]\n"
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
	t.text = "冒險者背包 (道具與戰魂倉庫)"
	t.add_theme_font_size_override("font_size", 20)
	t.add_theme_color_override("font_color", UiStyle.TATA_ORANGE)
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
		ssb.bg_color = Color(0.98, 0.97, 0.94, 0.96)
		ssb.border_color = UiStyle.TATA_CARD_BORDER
		ssb.set_border_width_all(2)
		ssb.border_width_bottom = 4
		ssb.set_corner_radius_all(14)
		sp.add_theme_stylebox_override("panel", ssb)
		var l := Label.new()
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 12)
		l.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
		if i == 0: l.text = "鐵劍"
		elif i == 1: l.text = "紅藥水x10"
		elif i == 2: l.text = "紅寶石"
		elif i == 3: l.text = "紫微星魂"
		sp.add_child(l)
		grid.add_child(sp)

func refresh_hud() -> void:
	if _lv_label: _lv_label.text = "Lv.12"
	if _name_label: _name_label.text = _get_hero_name()
	if _hero_name_tag: _hero_name_tag.text = _get_hero_name()
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
	tsb.bg_color = UiStyle.TATA_CARD_BG
	tsb.border_color = UiStyle.TATA_ORANGE
	tsb.set_border_width_all(2)
	tsb.border_width_bottom = 4
	tsb.set_corner_radius_all(14)
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", UiStyle.TATA_BROWN)
	toast.add_theme_font_size_override("font_size", 15)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.5)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)
