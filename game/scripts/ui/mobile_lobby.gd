class_name MobileLobby
extends Control
## 勇者之魂 (Clockwork Heart) - 神殿黑曜石 × 古典黃金齒輪手遊大廳
## 視覺特徵：希臘神殿石柱 + 深邃黑曜石地坪 + 古典黃金齒輪 + 白兔多姿態動態待機 (無 Emoji、無系統字型符號)

signal request_battle(mode: String)
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FootShadowShader = preload("res://shaders/foot_shadow.gdshader")

## ── 希臘神殿 · 黑曜石 × 古典金標準色盤 (對齊 temple.css 與 docs/LOBBY_UI_REDESIGN.md) ──
const OBSIDIAN_BASE      := Color(0.043, 0.039, 0.055, 1.0)  ## #0B0A0E：黑曜石最深底色
const OBSIDIAN_CARD      := Color(0.078, 0.071, 0.094, 1.0)  ## #141218：黑曜石卡片面色
const OBSIDIAN_WARM      := Color(0.102, 0.090, 0.122, 1.0)  ## #1A171F：微溫黑曜石
const OBSIDIAN_DEEP      := Color(0.027, 0.024, 0.039, 1.0)  ## #07060A：黑曜石凹槽

const GOLD_CLASSICAL     := Color(0.831, 0.686, 0.216, 1.0)  ## #D4AF37：古典金
const GOLD_HOVER         := Color(0.941, 0.843, 0.549, 1.0)  ## #F0D78C：黃金亮色
const BRONZE_ANTIQUE     := Color(0.549, 0.416, 0.102, 1.0)  ## #8C6A1A：仿古黃銅
const BRONZE_WARM        := Color(0.769, 0.573, 0.165, 1.0)  ## #C4922A：暖古銅

const TEAL_CORE          := Color(0.243, 0.812, 0.749, 1.0)  ## #3ECFBF：以太青綠核心
const TEAL_CORE_DARK     := Color(0.122, 0.541, 0.502, 1.0)  ## #1F8A80：以太青綠暗底

const INK_IVORY          := Color(0.957, 0.922, 0.831, 1.0)  ## #F4EBD4：象牙白文字
const INK_IVORY_SOFT     := Color(0.788, 0.749, 0.659, 1.0)  ## #C9BFA8：柔和象牙白
const INK_IVORY_MUTED    := Color(0.541, 0.502, 0.439, 1.0)  ## #8A8070：弱化象牙白

const CORAL_RUST         := Color(0.769, 0.361, 0.290, 1.0)  ## #C45C4A：鐵鏽珊瑚紅
const STEEL_BLUE         := Color(0.420, 0.549, 0.682, 1.0)  ## #6B8CAE：淬火精鋼藍

const LINE_GOLD          := Color(0.831, 0.686, 0.216, 0.38) ## 金線微光邊框
const LINE_GOLD_SOFT     := Color(0.831, 0.686, 0.216, 0.18) ## 輔助分界金線

const DEFAULT_HERO_NAME: String = "新人"

enum Tab {
	VILLAGE,     ## 今日村莊大廳 (主城)
	CHARACTER,   ## 角色 / 三欄武器紙娃娃
	ADVENTURE,   ## 四區出征關卡
	SOUL_HALL,   ## 聚魂殿堂 (封靈罐四階)
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
var _char_prev: TextureRect = null

## 角色動態與姿態
var _profile_avatar: TextureRect
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _hero_name_tag: Label
var _speech_bubble: PanelContainer
var _speech_label: Label
var _particles_root: Control
var _breathe_tween: Tween
var _bubble_tween: Tween
var _poke_tween: Tween
var _idle_action_timer: float = 0.0
var _is_interacting: bool = false
var enable_idle_breathing: bool = true
var enable_idle_flavor: bool = true

## 動作姿態紋理快取
var _tex_idle: Texture2D
var _tex_attack: Texture2D
var _tex_skill: Texture2D
var _tex_telegraph: Texture2D
var _tex_recover: Texture2D
var _tex_hit: Texture2D

## 聚魂殿封靈罐四階狀態
var _gourd_lit: Array[bool] = [true, false, false, false]
var _gourd_btns: Array[Button] = []

## 四地區出征
var _selected_region: int = 1 # 0: 破曉之原, 1: 聖獅王都, 2: 迷霧雪境, 3: 深淵龍窟
var _stages_container: VBoxContainer
var _region_buttons: Array[Button] = []

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
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_load_hero_poses()
	_build_ui()
	refresh_hud()
	_switch_tab(Tab.VILLAGE)
	call_deferred("_apply_safe")

func _apply_safe() -> void:
	ResponsiveUi.apply_safe_margins(self)

func _get_hero_portrait(race: String) -> Texture2D:
	var r := race.to_lower().strip_edges()
	var p_path := ""
	match r:
		"rabbit": p_path = "res://assets/sprites/portraits/rabbit.png"
		"fox": p_path = "res://assets/sprites/portraits/fox_mage.png"
		"lion": p_path = "res://assets/sprites/portraits/lion_knight.png"
		"boar": p_path = "res://assets/sprites/portraits/boar_warrior.png"
		"macaque": p_path = "res://assets/sprites/portraits/macaque.png"
		_: p_path = "res://assets/sprites/portraits/rabbit.png"
	if ResourceLoader.exists(p_path):
		return load(p_path) as Texture2D
	return SpriteDB.player_race_composite(r)


func _get_hero_equipped_idle_texture() -> Texture2D:
	var gs := _gs()
	var race := "rabbit"
	var slots: Dictionary = {}
	if gs and "player_race" in gs:
		race = str(gs.player_race).strip_edges().to_lower()
		if race.is_empty():
			race = "rabbit"
	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		slots = (gs.paperdoll_slots as Dictionary).duplicate()
	if not slots.has("weapon") or str(slots["weapon"]).is_empty():
		if gs and "equip_slots" in gs and gs.equip_slots is Dictionary:
			var wuid: String = str(gs.equip_slots.get("weapon", ""))
			if wuid != "" and "equip_worn" in gs and gs.equip_worn is Dictionary and gs.equip_worn.has(wuid):
				var winst: Dictionary = gs.equip_worn[wuid]
				var base_id: String = str(winst.get("base_id", winst.get("id", "")))
				if base_id != "":
					slots["weapon"] = base_id
	var tex: Texture2D = SpriteDB.player_equipped_idle(race, slots)
	if tex == null:
		tex = SpriteDB.player_idle()
	return tex


func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if _hero_avatar:
		_hero_avatar.scale = Vector2.ONE
	if _hero_shadow:
		_hero_shadow.scale = Vector2.ONE
	if not enable_idle_breathing:
		return
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _restore_hero_idle() -> void:
	_tex_idle = _get_hero_equipped_idle_texture()
	if _hero_avatar and _tex_idle:
		_hero_avatar.texture = _tex_idle
		_hero_avatar.position = Vector2(-125, -140)
		_hero_avatar.scale = Vector2.ONE
	if _char_prev and _tex_idle:
		_char_prev.texture = _tex_idle
	if _speech_bubble:
		_speech_bubble.visible = false
	_is_interacting = false
	_start_breathe_tween()


func _load_hero_poses() -> void:
	var gs := _gs()
	var race := "rabbit"
	if gs and "player_race" in gs:
		race = str(gs.player_race).strip_edges().to_lower()
		if race.is_empty():
			race = "rabbit"

	_tex_idle = _get_hero_equipped_idle_texture()
	_tex_attack = SpriteDB.player_pose("attack", race)
	_tex_skill = SpriteDB.player_pose("skill", race)
	_tex_telegraph = SpriteDB.player_pose("telegraph", race)
	_tex_recover = SpriteDB.player_pose("recover", race)
	_tex_hit = SpriteDB.player_pose("hit", race)

	if _tex_idle == null:
		_tex_idle = SpriteDB.player_idle()
	if _tex_attack == null and ResourceLoader.exists("res://assets/sprites/player/poses/attack.png"):
		_tex_attack = load("res://assets/sprites/player/poses/attack.png")
	if _tex_skill == null and ResourceLoader.exists("res://assets/sprites/player/poses/skill.png"):
		_tex_skill = load("res://assets/sprites/player/poses/skill.png")
	if _tex_telegraph == null and ResourceLoader.exists("res://assets/sprites/player/poses/telegraph.png"):
		_tex_telegraph = load("res://assets/sprites/player/poses/telegraph.png")
	if _tex_recover == null and ResourceLoader.exists("res://assets/sprites/player/poses/recover.png"):
		_tex_recover = load("res://assets/sprites/player/poses/recover.png")
	if _tex_hit == null and ResourceLoader.exists("res://assets/sprites/player/poses/hit.png"):
		_tex_hit = load("res://assets/sprites/player/poses/hit.png")

	if _hero_avatar and _tex_idle and not _is_interacting:
		_hero_avatar.texture = _tex_idle
	if _char_prev and _tex_idle:
		_char_prev.texture = _tex_idle

static var _shadow_tex_cache: Texture2D = null

static func _soft_shadow_tex() -> Texture2D:
	if _shadow_tex_cache != null:
		return _shadow_tex_cache
	## 寬核平台＋柔邊：核接近不透明，邊緣才衰減（review.md 第 16 條 / 腳底軟影）
	var w := 256
	var h := 96
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	var cx := (w - 1) * 0.5
	var cy := (h - 1) * 0.5
	var rx := cx * 0.98
	var ry := cy * 0.96
	for y in h:
		for x in w:
			var dx := (float(x) - cx) / rx
			var dy := (float(y) - cy) / ry
			var d2 := dx * dx + dy * dy
			if d2 >= 1.0:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
			else:
				var d := sqrt(d2)
				var a := 1.0
				if d > 0.40:
					var t := (d - 0.40) / 0.60
					t = t * t * (3.0 - 2.0 * t)
					a = 1.0 - t
				img.set_pixel(x, y, Color(1, 1, 1, a))
	_shadow_tex_cache = ImageTexture.create_from_image(img)
	return _shadow_tex_cache

func _build_ui() -> void:
	## 1. 背景插畫（神殿黑曜石底圖 / LINEAR 平滑採樣）
	var bg := TextureRect.new()
	bg.name = "TempleLobbyBg"
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	
	var temple_path := "res://assets/sprites/maps/temple_lobby_bg.png"
	var abs_temple_path := ProjectSettings.globalize_path(temple_path)
	if FileAccess.file_exists(abs_temple_path):
		var img := Image.load_from_file(abs_temple_path)
		if img and not img.is_empty():
			bg.texture = ImageTexture.create_from_image(img)
	if bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/sky_kingdom_bg.png"):
		bg.texture = load("res://assets/sprites/maps/sky_kingdom_bg.png")
	elif bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	add_child(bg)

	## 2. 飄散的黃金以太塵埃微光粒子 (Golden Ether Motes)
	_particles_root = Control.new()
	_particles_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_particles_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_particles_root)
	_spawn_floating_ether_motes()

	## 3. 內容掛載層
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

	## 4. 頂部狀態列 (神殿黑曜石 HUD，無 Emoji、無符號)
	_build_top_hud()

	## 5. 底部黑曜石神殿導航欄 (無 Emoji、無符號，古典黃金雕飾)
	_build_bottom_dock()

## ──────────────────────────────────────────
## 通用黑曜石神殿風格面板 (Obsidian Temple Panel)
## ──────────────────────────────────────────
func _create_obsidian_panel(accent: Color = LINE_GOLD) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = OBSIDIAN_CARD
	s.border_color = accent
	s.set_border_width_all(1)
	s.border_width_bottom = 3
	s.border_color = BRONZE_ANTIQUE
	s.set_corner_radius_all(8)
	s.content_margin_left = 20
	s.content_margin_right = 20
	s.content_margin_top = 16
	s.content_margin_bottom = 16
	s.shadow_color = Color(0.0, 0.0, 0.0, 0.45)
	s.shadow_size = 10
	s.shadow_offset = Vector2(0, 4)
	return s

## ──────────────────────────────────────────
## 黃金以太塵埃微粒 (Golden Ether Motes)
## ──────────────────────────────────────────
func _spawn_floating_ether_motes() -> void:
	var gp: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		gp = (loop as SceneTree).root.get_node_or_null("GraphicsProfile")
	var n := 14
	if gp != null:
		n = int(gp.particle_count(14))
	if n <= 0:
		return
	for i in range(n):
		var star := ColorRect.new()
		var sz := 4.0 + float((i % 3) * 2)
		star.custom_minimum_size = Vector2(sz, sz)
		star.size = Vector2(sz, sz)
		star.pivot_offset = Vector2(sz * 0.5, sz * 0.5)
		star.rotation = PI * 0.25
		var c := Color(0.831, 0.686, 0.216, 0.70) if i % 2 == 0 else Color(0.243, 0.812, 0.749, 0.60)
		star.color = c
		star.position = Vector2(randf_range(40.0, 1240.0), randf_range(100.0, 580.0))
		_particles_root.add_child(star)

		# 緩慢升騰與呼吸淡入淡出
		var tw := create_tween().set_loops()
		var dur := randf_range(2.5, 4.0)
		var dy := randf_range(-15.0, -30.0)
		tw.tween_property(star, "position:y", star.position.y + dy, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.2, dur * 0.5)
		tw.tween_property(star, "position:y", star.position.y, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.85, dur * 0.5)

## ──────────────────────────────────────────
## 頂部黑曜石 HUD (Top Obsidian HUD)
## ──────────────────────────────────────────
func _build_top_hud() -> void:
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.offset_left = 16
	top_bar.offset_right = -16
	top_bar.offset_top = 10
	top_bar.offset_bottom = 74
	
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.043, 0.039, 0.055, 0.90) # OBSIDIAN_BASE @ 90%
	sb.border_color = BRONZE_ANTIQUE
	sb.set_border_width_all(1)
	sb.border_width_bottom = 2
	sb.set_corner_radius_all(8)
	sb.shadow_color = Color(0.0, 0.0, 0.0, 0.45)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 3)
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
	psb.bg_color = OBSIDIAN_WARM
	psb.border_color = GOLD_CLASSICAL
	psb.set_border_width_all(2)
	psb.set_corner_radius_all(26)
	p_frame.custom_minimum_size = Vector2(52, 52)
	p_frame.add_theme_stylebox_override("panel", psb)
	var p_tex := TextureRect.new()
	p_tex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	p_tex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	p_tex.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	var init_gs := _gs()
	var init_race := str(init_gs.player_race).strip_edges().to_lower() if init_gs and "player_race" in init_gs else "rabbit"
	p_tex.texture = _get_hero_portrait(init_race)
	_profile_avatar = p_tex
	p_frame.add_child(p_tex)
	p_box.add_child(p_frame)

	var info_v := VBoxContainer.new()
	info_v.alignment = BoxContainer.ALIGNMENT_CENTER
	info_v.add_theme_constant_override("separation", 2)
	
	var row1 := HBoxContainer.new()
	row1.add_theme_constant_override("separation", 8)
	_lv_label = Label.new()
	_lv_label.text = "Lv.1"
	_lv_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	_lv_label.add_theme_font_size_override("font_size", 16)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = _get_hero_name()
	_name_label.add_theme_font_size_override("font_size", 17)
	_name_label.add_theme_color_override("font_color", INK_IVORY)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	_power_label = Label.new()
	_power_label.text = "戰力 0"
	_power_label.add_theme_color_override("font_color", BRONZE_WARM)
	_power_label.add_theme_font_size_override("font_size", 13)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 黑曜石凹槽立體三寶膠囊
	_energy_label = _add_clean_capsule(h, "能量", "—", TEAL_CORE)
	_gold_label = _add_clean_capsule(h, "金幣", "—", GOLD_CLASSICAL)
	_gem_label = _add_clean_capsule(h, "星屑", "—", STEEL_BLUE)

	var set_btn := Button.new()
	set_btn.text = "設置"
	set_btn.custom_minimum_size = Vector2(64, 44)
	set_btn.add_theme_font_size_override("font_size", 15)
	var sbs := StyleBoxFlat.new()
	sbs.bg_color = OBSIDIAN_WARM
	sbs.border_color = LINE_GOLD
	sbs.set_border_width_all(1)
	sbs.border_width_bottom = 2
	sbs.set_corner_radius_all(6)
	set_btn.add_theme_stylebox_override("normal", sbs)
	set_btn.add_theme_stylebox_override("hover", sbs)
	set_btn.add_theme_stylebox_override("pressed", sbs)
	set_btn.add_theme_color_override("font_color", INK_IVORY_SOFT)
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
	csb.bg_color = OBSIDIAN_DEEP
	csb.border_color = BRONZE_ANTIQUE
	csb.set_border_width_all(1)
	csb.border_width_bottom = 2
	csb.set_corner_radius_all(8)
	csb.content_margin_left = 12
	csb.content_margin_right = 12
	csb.content_margin_top = 4
	csb.content_margin_bottom = 4
	csb.shadow_color = Color(0.0, 0.0, 0.0, 0.3)
	csb.shadow_size = 4
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 8)
	var il := Label.new()
	il.text = title
	il.add_theme_font_size_override("font_size", 13)
	il.add_theme_color_override("font_color", accent)
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.add_theme_font_size_override("font_size", 15)
	vl.add_theme_color_override("font_color", INK_IVORY)
	h.add_child(vl)

	cap.add_child(h)
	parent.add_child(cap)
	return vl

## ──────────────────────────────────────────
## 底部黑曜石神殿導航欄 (Bottom Dock)
## ──────────────────────────────────────────
func _build_bottom_dock() -> void:
	var dock := PanelContainer.new()
	dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	dock.offset_left = 24
	dock.offset_right = -24
	dock.offset_top = -84
	dock.offset_bottom = -12
	
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = Color(0.043, 0.039, 0.055, 0.95) # OBSIDIAN_BASE @ 95%
	dsb.border_color = GOLD_CLASSICAL
	dsb.border_width_top = 2
	dsb.border_width_bottom = 1
	dsb.border_width_left = 1
	dsb.border_width_right = 1
	dsb.set_corner_radius_all(8)
	dsb.shadow_color = Color(0.0, 0.0, 0.0, 0.5)
	dsb.shadow_size = 12
	dock.add_theme_stylebox_override("panel", dsb)
	add_child(dock)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
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

func _style_dock_button(btn: Button, is_active: bool) -> void:
	var sb := StyleBoxFlat.new()
	if is_active:
		sb.bg_color = GOLD_CLASSICAL
		sb.border_color = TEAL_CORE
		sb.set_border_width_all(1)
		sb.border_width_bottom = 3
		sb.set_corner_radius_all(8)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 14
		sb.content_margin_right = 14
		sb.shadow_color = Color(0.831, 0.686, 0.216, 0.35)
		sb.shadow_size = 8
		btn.add_theme_color_override("font_color", OBSIDIAN_BASE)
		btn.add_theme_color_override("font_hover_color", Color(0.0, 0.0, 0.0, 1.0))
		btn.add_theme_color_override("font_pressed_color", OBSIDIAN_BASE)
	else:
		sb.bg_color = OBSIDIAN_WARM
		sb.border_color = LINE_GOLD_SOFT
		sb.set_border_width_all(1)
		sb.set_corner_radius_all(8)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 14
		sb.content_margin_right = 14
		btn.add_theme_color_override("font_color", INK_IVORY_SOFT)
		btn.add_theme_color_override("font_hover_color", GOLD_HOVER)
		btn.add_theme_color_override("font_pressed_color", INK_IVORY)
	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb)
	btn.add_theme_stylebox_override("pressed", sb)
	btn.add_theme_stylebox_override("focus", sb)

func _switch_tab(target: Tab) -> void:
	_current_tab = target
	if _village_layer:
		_village_layer.visible = (target == Tab.VILLAGE)
	if _char_layer:
		_char_layer.visible = (target == Tab.CHARACTER)
	if _adventure_layer:
		_adventure_layer.visible = (target == Tab.ADVENTURE)
	if _soul_layer:
		_soul_layer.visible = (target == Tab.SOUL_HALL)
	if _bag_layer:
		_bag_layer.visible = (target == Tab.BAG)

	for i in range(_dock_buttons.size()):
		var is_active := (i == int(target))
		_style_dock_button(_dock_buttons[i], is_active)

## ──────────────────────────────────────────
## 每幀小動作判定 (動態待機自然活化)
## ──────────────────────────────────────────
func _process(delta: float) -> void:
	if _current_tab != Tab.VILLAGE or _is_interacting or not enable_idle_flavor:
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
			if not _is_interacting:
				_restore_hero_idle()
		)
	elif roll == 1 and _tex_recover:
		## 伸個懶腰
		_hero_avatar.texture = _tex_recover
		var tw := create_tween()
		tw.tween_interval(1.0)
		tw.tween_callback(func():
			if not _is_interacting:
				_restore_hero_idle()
		)

## ──────────────────────────────────────────
## Tab 1: 今日村莊 (神殿日晷展台 + 點擊互動 + 黃金以太粒子)
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

	## 1. 角色腳底接地軟影 (Foot Soft Shadow / review.md 第 16 條)
	_hero_shadow = TextureRect.new()
	_hero_shadow.name = "HeroFootShadow"
	_hero_shadow.add_to_group("soft_shadow")
	_hero_shadow.offset_left = -62
	_hero_shadow.offset_top = 74
	_hero_shadow.offset_right = 98
	_hero_shadow.offset_bottom = 116
	_hero_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	_hero_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hero_shadow.texture = _soft_shadow_tex()
	_hero_shadow.pivot_offset = Vector2(80, 21)

	var shadow_mat := ShaderMaterial.new()
	shadow_mat.shader = FootShadowShader
	shadow_mat.set_shader_parameter("strength", 0.95)
	shadow_mat.set_shader_parameter("shadow_color", Color(0.01, 0.01, 0.02, 1.0))
	_hero_shadow.material = shadow_mat
	stage_anchor.add_child(_hero_shadow)

	## 1.1 緊密接地閉塞陰影 (Contact Occlusion Shadow)
	var contact_shadow := TextureRect.new()
	contact_shadow.name = "HeroContactShadow"
	contact_shadow.add_to_group("soft_shadow")
	contact_shadow.offset_left = -38
	contact_shadow.offset_top = 84
	contact_shadow.offset_right = 74
	contact_shadow.offset_bottom = 104
	contact_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	contact_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	contact_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	contact_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	contact_shadow.texture = _soft_shadow_tex()

	var contact_mat := ShaderMaterial.new()
	contact_mat.shader = FootShadowShader
	contact_mat.set_shader_parameter("strength", 0.98)
	contact_mat.set_shader_parameter("shadow_color", Color(0.005, 0.005, 0.01, 1.0))
	contact_shadow.material = contact_mat
	stage_anchor.add_child(contact_shadow)

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

	## 3. 頭頂稱號與名字（黑曜石半透明膠囊底襯 + 金框 + 深色文字描邊，置於齒輪上方避開核心細節）
	var tag_panel := PanelContainer.new()
	tag_panel.set_anchors_preset(Control.PRESET_CENTER_TOP)
	tag_panel.offset_left = -75
	tag_panel.offset_top = -158
	tag_panel.offset_right = 75
	tag_panel.offset_bottom = -112
	tag_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var tag_sb := StyleBoxFlat.new()
	tag_sb.bg_color = Color(0.027, 0.024, 0.039, 0.88) # OBSIDIAN_DEEP 半透明黑曜石底
	tag_sb.border_color = Color(0.831, 0.686, 0.216, 0.75) # GOLD_CLASSICAL 金屬微光邊框
	tag_sb.set_border_width_all(1)
	tag_sb.border_width_bottom = 2
	tag_sb.set_corner_radius_all(10)
	tag_sb.content_margin_left = 10
	tag_sb.content_margin_right = 10
	tag_sb.content_margin_top = 4
	tag_sb.content_margin_bottom = 4
	tag_sb.shadow_color = Color(0.0, 0.0, 0.0, 0.5)
	tag_sb.shadow_size = 5
	tag_sb.shadow_offset = Vector2(0, 2)
	tag_panel.add_theme_stylebox_override("panel", tag_sb)

	var tag_v := VBoxContainer.new()
	tag_v.alignment = BoxContainer.ALIGNMENT_CENTER
	tag_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tag_v.add_theme_constant_override("separation", 2)

	_hero_name_tag = Label.new()
	_hero_name_tag.text = _get_hero_name()
	_hero_name_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hero_name_tag.add_theme_font_size_override("font_size", 18)
	_hero_name_tag.add_theme_color_override("font_color", GOLD_HOVER)
	_hero_name_tag.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.04, 0.95))
	_hero_name_tag.add_theme_constant_override("outline_size", 3)
	tag_v.add_child(_hero_name_tag)

	var title_l := Label.new()
	title_l.text = "【初出茅廬】"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 12)
	title_l.add_theme_color_override("font_color", INK_IVORY_SOFT)
	title_l.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.04, 0.95))
	title_l.add_theme_constant_override("outline_size", 2)
	tag_v.add_child(title_l)

	tag_panel.add_child(tag_v)
	_hero_avatar.add_child(tag_panel)

	## 4. 點擊彈出的神殿對話氣泡
	_speech_bubble = PanelContainer.new()
	_speech_bubble.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_speech_bubble.offset_left = -110
	_speech_bubble.offset_top = -110
	_speech_bubble.offset_right = 150
	_speech_bubble.offset_bottom = -60
	_speech_bubble.visible = false
	var bub_sb := StyleBoxFlat.new()
	bub_sb.bg_color = Color(0.078, 0.071, 0.094, 0.95) # OBSIDIAN_CARD
	bub_sb.border_color = GOLD_CLASSICAL
	bub_sb.set_border_width_all(1)
	bub_sb.border_width_bottom = 2
	bub_sb.set_corner_radius_all(8)
	bub_sb.shadow_color = Color(0.0, 0.0, 0.0, 0.4)
	bub_sb.shadow_size = 6
	bub_sb.content_margin_left = 12
	bub_sb.content_margin_right = 12
	bub_sb.content_margin_top = 6
	bub_sb.content_margin_bottom = 6
	_speech_bubble.add_theme_stylebox_override("panel", bub_sb)

	_speech_label = Label.new()
	_speech_label.text = "背後的發條上得剛剛好，出發吧！"
	_speech_label.add_theme_color_override("font_color", INK_IVORY)
	_speech_label.add_theme_font_size_override("font_size", 14)
	_speech_bubble.add_child(_speech_label)
	_hero_avatar.add_child(_speech_bubble)

	## 呼吸動畫
	_start_breathe_tween()

	## 左側四大殿堂黑曜石金屬浮雕卡牌 (王都鐵匠、手藝工坊、演武競技、冒險委託)
	var left_shops := VBoxContainer.new()
	left_shops.name = "HallCardsContainer"
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 32
	left_shops.offset_top = 16
	left_shops.offset_right = 272
	left_shops.offset_bottom = -16
	left_shops.add_theme_constant_override("separation", 14)
	_village_layer.add_child(left_shops)

	_add_hall_card(left_shops, "王都鐵匠", "品質轉化 · 裝備鍛造", "鐵", func():
		open_forge()
	)
	_add_hall_card(left_shops, "手藝工坊", "紅黃藍石 · 三合一熔煉", "工", func():
		open_gem_workshop()
	)
	_add_hall_card(left_shops, "演武競技", "挑戰對手 · 雙倍抽獎", "武", func():
		request_battle.emit("arena")
	)
	_add_hall_card(left_shops, "冒險委託", "每日簽到 · 懸賞領獎", "委", func():
		open_windup_daily()
	)

	## 右側：黑曜石戰情報告板 (專注於主線推進)
	var right_card := PanelContainer.new()
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -340
	right_card.offset_top = -170
	right_card.offset_right = -32
	right_card.offset_bottom = -16
	right_card.add_theme_stylebox_override("panel", _create_obsidian_panel(GOLD_CLASSICAL))
	_village_layer.add_child(right_card)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 10)
	right_card.add_child(rv)

	var ch_lbl := Label.new()
	ch_lbl.text = "冒險出征 · 當前主線"
	ch_lbl.add_theme_font_size_override("font_size", 14)
	ch_lbl.add_theme_color_override("font_color", BRONZE_WARM)
	rv.add_child(ch_lbl)

	var s_name := Label.new()
	s_name.text = "第二地區 · 聖獅王城 (2-4 BOSS)"
	s_name.add_theme_font_size_override("font_size", 17)
	s_name.add_theme_color_override("font_color", INK_IVORY)
	rv.add_child(s_name)

	var btn_go := Button.new()
	btn_go.custom_minimum_size = Vector2(280, 68)
	btn_go.text = "前往出征"
	btn_go.add_theme_font_size_override("font_size", 20)
	var gsb := StyleBoxFlat.new()
	gsb.bg_color = GOLD_CLASSICAL
	gsb.border_color = TEAL_CORE
	gsb.set_border_width_all(1)
	gsb.border_width_bottom = 4
	gsb.set_corner_radius_all(8)
	gsb.content_margin_top = 12
	gsb.content_margin_bottom = 12
	gsb.shadow_color = Color(0.831, 0.686, 0.216, 0.35)
	gsb.shadow_size = 8
	gsb.shadow_offset = Vector2(0, 3)
	btn_go.add_theme_stylebox_override("normal", gsb)
	
	var gsb_h := gsb.duplicate() as StyleBoxFlat
	gsb_h.bg_color = GOLD_HOVER
	btn_go.add_theme_stylebox_override("hover", gsb_h)
	btn_go.add_theme_stylebox_override("pressed", gsb)
	btn_go.add_theme_stylebox_override("focus", gsb)
	btn_go.add_theme_color_override("font_color", OBSIDIAN_BASE)
	btn_go.add_theme_color_override("font_hover_color", Color(0.0, 0.0, 0.0, 1.0))
	btn_go.add_theme_color_override("font_pressed_color", OBSIDIAN_BASE)
	btn_go.pressed.connect(func(): _switch_tab(Tab.ADVENTURE))
	rv.add_child(btn_go)

func _add_hall_card(parent: Container, title: String, subtitle: String, icon_symbol: String, cb: Callable) -> void:
	var btn := Button.new()
	btn.name = "HallCard_" + title
	btn.add_to_group("hall_cards")
	btn.set_meta("hall_title", title)
	btn.set_meta("hall_subtitle", subtitle)
	btn.set_meta("hall_icon", icon_symbol)
	btn.custom_minimum_size = Vector2(240, 72)
	
	var sb := StyleBoxFlat.new()
	sb.bg_color = OBSIDIAN_CARD
	sb.border_color = BRONZE_ANTIQUE
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(8)
	sb.content_margin_left = 14
	sb.content_margin_right = 14
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	sb.shadow_color = Color(0.0, 0.0, 0.0, 0.4)
	sb.shadow_size = 6
	sb.shadow_offset = Vector2(0, 2)
	btn.add_theme_stylebox_override("normal", sb)
	
	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = OBSIDIAN_WARM
	sb_h.border_color = GOLD_CLASSICAL
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb)
	btn.add_theme_stylebox_override("focus", sb)
	
	var h := HBoxContainer.new()
	h.set_anchors_preset(Control.PRESET_FULL_RECT)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 12)
	h.mouse_filter = Control.MOUSE_FILTER_IGNORE
	btn.add_child(h)
	
	var icon_box := PanelContainer.new()
	icon_box.custom_minimum_size = Vector2(42, 42)
	var isb := StyleBoxFlat.new()
	isb.bg_color = OBSIDIAN_DEEP
	isb.border_color = GOLD_CLASSICAL
	isb.set_border_width_all(1)
	isb.set_corner_radius_all(6)
	icon_box.add_theme_stylebox_override("panel", isb)
	icon_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	
	var icon_lbl := Label.new()
	icon_lbl.text = icon_symbol
	icon_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	icon_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	icon_lbl.add_theme_font_size_override("font_size", 18)
	icon_lbl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	icon_box.add_child(icon_lbl)
	h.add_child(icon_box)
	
	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	
	var tl := Label.new()
	tl.text = title
	tl.add_theme_font_size_override("font_size", 15)
	tl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	v.add_child(tl)
	
	var sl := Label.new()
	sl.text = subtitle
	sl.add_theme_font_size_override("font_size", 12)
	sl.add_theme_color_override("font_color", INK_IVORY_SOFT)
	v.add_child(sl)
	
	h.add_child(v)
	btn.pressed.connect(cb)
	parent.add_child(btn)

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
## 點擊主角：切換動態姿態 + 爆發黃金以太粒子 + 氣泡
## ──────────────────────────────────────────
func _on_hero_clicked(forced_act: int = -1) -> void:
	_is_interacting = true
	var act_type := forced_act if forced_act >= 0 else (randi() % 3)

	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()

	var speech_lines := [
		"看我的旋風斬～喝！",
		"背後的發條上得剛剛好，出發吧！",
		"聽見神殿齒輪的轉動聲了嗎？",
		"神殿的以太核心正在共鳴……",
		"隨時準備好去挑戰大首領！"
	]
	if _speech_label:
		_speech_label.text = speech_lines[randi() % speech_lines.size()]
	if _speech_bubble:
		_speech_bubble.visible = true
		_speech_bubble.modulate.a = 0.0

		if _bubble_tween and _bubble_tween.is_valid():
			_bubble_tween.kill()
		_bubble_tween = create_tween()
		_bubble_tween.tween_property(_speech_bubble, "modulate:a", 1.0, 0.15)
		_bubble_tween.tween_interval(0.7)
		_bubble_tween.tween_property(_speech_bubble, "modulate:a", 0.0, 0.15)
		_bubble_tween.tween_callback(func(): _speech_bubble.visible = false)

	## 噴散 8 顆黃金以太星芒微粒
	if _hero_avatar:
		_burst_click_particles(_hero_avatar.global_position + Vector2(125, 120))

	if _poke_tween and _poke_tween.is_valid():
		_poke_tween.kill()
	var tw := create_tween()
	_poke_tween = tw
	match act_type:
		0:
			## 揮劍劈砍姿態 (attack -> recover -> equipped idle)
			if _tex_attack and _hero_avatar: _hero_avatar.texture = _tex_attack
			tw.tween_property(_hero_avatar, "position", Vector2(-110, -165), 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "position", Vector2(-125, -140), 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.tween_interval(0.4)
			tw.tween_callback(func():
				if _tex_recover and _hero_avatar: _hero_avatar.texture = _tex_recover
			)
			tw.tween_interval(0.3)
			tw.tween_callback(_restore_hero_idle)
		1:
			## 聚氣勝利姿態 (skill -> equipped idle)
			if _tex_skill and _hero_avatar: _hero_avatar.texture = _tex_skill
			tw.tween_property(_hero_avatar, "scale", Vector2(1.15, 1.15), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "scale", Vector2(1.0, 1.0), 0.2).set_trans(Tween.TRANS_SINE)
			tw.tween_interval(0.6)
			tw.tween_callback(_restore_hero_idle)
		2:
			## 靈巧後翻大跳躍 (telegraph -> equipped idle)
			if _tex_telegraph and _hero_avatar: _hero_avatar.texture = _tex_telegraph
			tw.tween_property(_hero_avatar, "position:y", -175.0, 0.15).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", -1.0, 0.15)
			tw.tween_property(_hero_avatar, "position:y", -140.0, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", 1.0, 0.18)
			tw.tween_interval(0.2)
			tw.tween_callback(_restore_hero_idle)

func _burst_click_particles(center_pos: Vector2) -> void:
	var gp := get_node_or_null("/root/GraphicsProfile")
	var n := 8
	if gp != null:
		n = int(gp.particle_count(8))
	if n <= 0:
		return
	var cols: Array[Color] = [
		GOLD_CLASSICAL,
		GOLD_HOVER,
		TEAL_CORE,
		BRONZE_WARM
	]
	for i in range(n):
		var star := ColorRect.new()
		star.name = "BurstParticle_%d" % i
		star.add_to_group("burst_particles")
		star.custom_minimum_size = Vector2(6, 6)
		star.size = Vector2(6, 6)
		star.pivot_offset = Vector2(3, 3)
		star.rotation = PI * 0.25
		star.color = cols[i % cols.size()]
		star.global_position = center_pos - Vector2(3, 3)
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(star)

		var angle := float(i) * (PI * 2.0 / float(n))
		var dist := randf_range(40.0, 80.0)
		var target := center_pos + Vector2(cos(angle), sin(angle)) * dist

		var tw := create_tween()
		tw.tween_property(star, "global_position", target, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(star, "modulate:a", 0.0, 0.35).set_delay(0.15)
		tw.tween_callback(star.queue_free)

## ──────────────────────────────────────────
## Tab 4: 聚魂殿堂 (以太祭壇封靈罐四階)
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
	panel.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD))
	_soul_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = _t("聚魂殿 · 封靈罐四階")
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 24)
	t.add_theme_color_override("font_color", GOLD_CLASSICAL)
	v.add_child(t)

	var desc := Label.new()
	desc.text = _t("聚引四大共鳴核心之魂：銳齒(攻) · 固甲(防) · 旋簧(血) · 全衡(衡)。點擊點亮更高階封靈罐！")
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 13)
	desc.add_theme_color_override("font_color", INK_IVORY_SOFT)
	v.add_child(desc)

	var gourd_row := HBoxContainer.new()
	gourd_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gourd_row.add_theme_constant_override("separation", 14)
	v.add_child(gourd_row)

	var gourds_data := [
		{"name": _t("綠階封靈罐"), "cost": 80, "color": TEAL_CORE},
		{"name": _t("藍階封靈罐"), "cost": 200, "color": STEEL_BLUE},
		{"name": _t("紫階封靈罐"), "cost": 500, "color": Color(0.68, 0.45, 0.90)},
		{"name": _t("橙階封靈罐"), "cost": 1000, "color": GOLD_CLASSICAL}
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
	var asb := StyleBoxFlat.new()
	asb.bg_color = OBSIDIAN_WARM
	asb.border_color = BRONZE_WARM
	asb.set_border_width_all(1)
	asb.border_width_bottom = 3
	asb.set_corner_radius_all(8)
	btn_absorb.add_theme_stylebox_override("normal", asb)
	btn_absorb.add_theme_stylebox_override("hover", asb)
	btn_absorb.add_theme_stylebox_override("pressed", asb)
	btn_absorb.add_theme_color_override("font_color", INK_IVORY)
	btn_absorb.pressed.connect(func():
		_show_toast("已將廢魂轉化為 480 戰魂經驗值！")
	)
	bot_h.add_child(btn_absorb)

	var btn_draw := Button.new()
	btn_draw.text = "聚魂十連"
	btn_draw.custom_minimum_size = Vector2(220, 56)
	btn_draw.add_theme_font_size_override("font_size", 18)
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = GOLD_CLASSICAL
	dsb.border_color = TEAL_CORE
	dsb.set_border_width_all(1)
	dsb.border_width_bottom = 4
	dsb.set_corner_radius_all(8)
	dsb.shadow_color = Color(0.831, 0.686, 0.216, 0.35)
	dsb.shadow_size = 8
	btn_draw.add_theme_stylebox_override("normal", dsb)
	var dsb_h := dsb.duplicate() as StyleBoxFlat
	dsb_h.bg_color = GOLD_HOVER
	btn_draw.add_theme_stylebox_override("hover", dsb_h)
	btn_draw.add_theme_stylebox_override("pressed", dsb)
	btn_draw.add_theme_color_override("font_color", OBSIDIAN_BASE)
	btn_draw.add_theme_color_override("font_hover_color", Color(0.0, 0.0, 0.0, 1.0))
	btn_draw.pressed.connect(func(): _do_gourd_draw(0, true))
	bot_h.add_child(btn_draw)

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
	csb.border_color = GOLD_HOVER
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
	cl.add_theme_color_override("font_color", BRONZE_WARM)
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
		var is_lit := _gourd_lit[i]
		var sb := StyleBoxFlat.new()
		if is_lit:
			sb.bg_color = OBSIDIAN_CARD
			sb.border_color = GOLD_CLASSICAL
			sb.set_border_width_all(2)
			sb.border_width_bottom = 4
			sb.set_corner_radius_all(8)
			sb.shadow_color = Color(0.831, 0.686, 0.216, 0.25)
			sb.shadow_size = 8
			b.disabled = false
		else:
			sb.bg_color = OBSIDIAN_DEEP
			sb.border_color = LINE_GOLD_SOFT
			sb.set_border_width_all(1)
			sb.border_width_bottom = 2
			sb.set_corner_radius_all(8)
			b.disabled = true
		b.add_theme_stylebox_override("normal", sb)
		b.add_theme_stylebox_override("hover", sb)
		b.add_theme_stylebox_override("disabled", sb)

func _do_gourd_draw(idx: int, is_ten: bool) -> void:
	if not _gourd_lit[idx] and not is_ten:
		return

	var roll := randf()
	if roll < 0.35 and idx < 3:
		_gourd_lit[idx + 1] = true
		_show_toast(_t("靈光閃爍！成功點亮更高階的封靈罐！"))
	else:
		for i in range(1, 4):
			_gourd_lit[i] = false
		_show_toast("聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
	
	_refresh_gourds_ui()

## ──────────────────────────────────────────
## Tab 3: 四地區出征 (神殿戰情報告板)
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
	panel.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD))
	_adventure_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	panel.add_child(v)

	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)

	_region_buttons.clear()
	var regions: Array[String] = ["第一地區 · 破曉之原", "第二地區 · 聖獅王都", "第三地區 · 迷霧雪境", "第四地區 · 深淵龍窟"]
	for i in range(regions.size()):
		var rb := Button.new()
		rb.text = regions[i]
		rb.custom_minimum_size = Vector2(175, 46)
		rb.add_theme_font_size_override("font_size", 16)
		_style_region_button(rb, i == _selected_region)
		var r_idx := i
		rb.pressed.connect(func(): _select_region(r_idx))
		reg_bar.add_child(rb)
		_region_buttons.append(rb)

	_stages_container = VBoxContainer.new()
	_stages_container.add_theme_constant_override("separation", 14)
	_stages_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_stages_container)

	_refresh_region_stages()

func _style_region_button(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	if is_selected:
		sb.bg_color = GOLD_CLASSICAL
		sb.border_color = TEAL_CORE
		sb.set_border_width_all(1)
		sb.border_width_bottom = 3
		sb.set_corner_radius_all(8)
		btn.add_theme_color_override("font_color", OBSIDIAN_BASE)
		btn.add_theme_color_override("font_hover_color", Color(0.0, 0.0, 0.0, 1.0))
		btn.add_theme_color_override("font_pressed_color", OBSIDIAN_BASE)
	else:
		sb.bg_color = OBSIDIAN_WARM
		sb.border_color = LINE_GOLD_SOFT
		sb.set_border_width_all(1)
		sb.set_corner_radius_all(8)
		btn.add_theme_color_override("font_color", INK_IVORY_MUTED)
		btn.add_theme_color_override("font_hover_color", INK_IVORY)
		btn.add_theme_color_override("font_pressed_color", INK_IVORY_SOFT)
	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb)
	btn.add_theme_stylebox_override("pressed", sb)
	btn.add_theme_stylebox_override("focus", sb)

func _select_region(r: int) -> void:
	_selected_region = r
	for i in range(_region_buttons.size()):
		_style_region_button(_region_buttons[i], i == _selected_region)
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
	csb.bg_color = OBSIDIAN_CARD
	csb.border_color = CORAL_RUST if is_boss else LINE_GOLD
	csb.set_border_width_all(2 if is_boss else 1)
	csb.border_width_bottom = 4 if is_boss else 2
	csb.set_corner_radius_all(8)
	csb.content_margin_left = 16
	csb.content_margin_right = 16
	csb.content_margin_top = 12
	csb.content_margin_bottom = 12
	csb.shadow_color = Color(0.0, 0.0, 0.0, 0.35)
	csb.shadow_size = 6
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
	num_l.add_theme_color_override("font_color", GOLD_CLASSICAL)
	t_row.add_child(num_l)

	var name_l := Label.new()
	name_l.text = str(s["name"])
	name_l.add_theme_font_size_override("font_size", 16)
	name_l.add_theme_color_override("font_color", INK_IVORY)
	t_row.add_child(name_l)
	v.add_child(t_row)

	var inf_row := HBoxContainer.new()
	inf_row.add_theme_constant_override("separation", 14)
	var typ_l := Label.new()
	typ_l.text = str(s["type"])
	typ_l.add_theme_font_size_override("font_size", 13)
	typ_l.add_theme_color_override("font_color", CORAL_RUST if is_boss else INK_IVORY_SOFT)
	inf_row.add_child(typ_l)

	var pwr_l := Label.new()
	pwr_l.text = "推薦戰力: %d" % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 13)
	pwr_l.add_theme_color_override("font_color", INK_IVORY_MUTED)
	inf_row.add_child(pwr_l)
	v.add_child(inf_row)

	var btn_battle := Button.new()
	btn_battle.custom_minimum_size = Vector2(145, 48)
	btn_battle.text = "挑戰首領" if is_boss else "出征"
	btn_battle.add_theme_font_size_override("font_size", 16)
	var bsb := StyleBoxFlat.new()
	if is_boss:
		bsb.bg_color = GOLD_CLASSICAL
		bsb.border_color = CORAL_RUST
		bsb.set_border_width_all(1)
		bsb.border_width_bottom = 3
		bsb.set_corner_radius_all(8)
		btn_battle.add_theme_color_override("font_color", OBSIDIAN_BASE)
		btn_battle.add_theme_color_override("font_hover_color", Color(0.0, 0.0, 0.0, 1.0))
	else:
		bsb.bg_color = OBSIDIAN_WARM
		bsb.border_color = BRONZE_WARM
		bsb.set_border_width_all(1)
		bsb.border_width_bottom = 3
		bsb.set_corner_radius_all(8)
		btn_battle.add_theme_color_override("font_color", INK_IVORY)
		btn_battle.add_theme_color_override("font_hover_color", GOLD_HOVER)
	btn_battle.add_theme_stylebox_override("normal", bsb)
	btn_battle.add_theme_stylebox_override("hover", bsb)
	btn_battle.add_theme_stylebox_override("pressed", bsb)
	var m: String = str(s["mode"])
	btn_battle.pressed.connect(func(): request_battle.emit(m))
	h.add_child(btn_battle)

	return c

## ──────────────────────────────────────────
## Tab 2 & Tab 5: 角色紙娃娃與背包 (神殿陳列匣)
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
	panel.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD))
	_char_layer.add_child(panel)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 28)
	panel.add_child(h)

	var l_card := PanelContainer.new()
	l_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	l_card.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD_SOFT))
	h.add_child(l_card)

	var l_margin := MarginContainer.new()
	l_margin.add_theme_constant_override("margin_left", 12)
	l_margin.add_theme_constant_override("margin_top", 12)
	l_margin.add_theme_constant_override("margin_right", 12)
	l_margin.add_theme_constant_override("margin_bottom", 12)
	l_card.add_child(l_margin)

	var l_vbox := VBoxContainer.new()
	l_vbox.add_theme_constant_override("separation", 10)
	l_margin.add_child(l_vbox)

	_char_prev = TextureRect.new()
	_char_prev.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_char_prev.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_char_prev.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_char_prev.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_char_prev.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if _tex_idle:
		_char_prev.texture = _tex_idle
	_char_prev.mouse_filter = Control.MOUSE_FILTER_PASS
	l_vbox.add_child(_char_prev)

	# 點擊預覽卡可直接開啟更衣
	var click_card_btn := Button.new()
	click_card_btn.flat = true
	click_card_btn.set_anchors_preset(Control.PRESET_FULL_RECT)
	click_card_btn.mouse_filter = Control.MOUSE_FILTER_PASS
	click_card_btn.pressed.connect(open_wardrobe)
	_char_prev.add_child(click_card_btn)

	# 正式更衣按鈕 (手遊防誤觸標準：高度 50px，熱區 >= 50px)
	var btn_wardrobe := Button.new()
	btn_wardrobe.name = "BtnWardrobe"
	btn_wardrobe.text = _t("更衣 · 發條衣櫥")
	btn_wardrobe.custom_minimum_size = Vector2(0, 50)
	btn_wardrobe.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn_wardrobe.add_theme_font_size_override("font_size", 16)
	var wsb := StyleBoxFlat.new()
	wsb.bg_color = OBSIDIAN_WARM
	wsb.border_color = GOLD_CLASSICAL
	wsb.set_border_width_all(2)
	wsb.border_width_bottom = 5
	wsb.set_corner_radius_all(14)
	btn_wardrobe.add_theme_stylebox_override("normal", wsb)
	var wsb_h := wsb.duplicate()
	wsb_h.bg_color = Color(0.18, 0.15, 0.22, 1.0)
	wsb_h.border_color = GOLD_HOVER
	btn_wardrobe.add_theme_stylebox_override("hover", wsb_h)
	btn_wardrobe.add_theme_stylebox_override("pressed", wsb_h)
	btn_wardrobe.add_theme_color_override("font_color", GOLD_CLASSICAL)
	btn_wardrobe.add_theme_color_override("font_hover_color", GOLD_HOVER)
	btn_wardrobe.pressed.connect(open_wardrobe)
	l_vbox.add_child(btn_wardrobe)

	var r_v := VBoxContainer.new()
	r_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	r_v.add_theme_constant_override("separation", 14)
	h.add_child(r_v)

	var title := Label.new()
	title.text = "三欄武器輪替系統 (原作節奏)"
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", GOLD_CLASSICAL)
	r_v.add_child(title)

	var w_row := HBoxContainer.new()
	w_row.add_theme_constant_override("separation", 12)
	r_v.add_child(w_row)

	var w_slots := ["首選: 鐵劍 (4次)", "副手: 獵弓 (4次)", "絕技: 拳套 (5連擊)"]
	for ws in w_slots:
		var p := PanelContainer.new()
		p.custom_minimum_size = Vector2(130, 68)
		var psb := StyleBoxFlat.new()
		psb.bg_color = OBSIDIAN_DEEP
		psb.border_color = BRONZE_WARM
		psb.set_border_width_all(1)
		psb.border_width_bottom = 3
		psb.set_corner_radius_all(8)
		p.add_theme_stylebox_override("panel", psb)
		var l := Label.new()
		l.text = ws
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 13)
		l.add_theme_color_override("font_color", INK_IVORY)
		p.add_child(l)
		w_row.add_child(p)

	var stats := RichTextLabel.new()
	stats.bbcode_enabled = true
	stats.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stats.add_theme_font_size_override("normal_font_size", 15)
	stats.text = "\n[color=#D4AF37][b]機體戰鬥屬性 (有效戰力 482)[/b][/color]\n\n"
	stats.text += "生命力 (HP): [color=#3ECFBF]520[/color]   物理攻擊: [color=#D4AF37]95[/color]\n"
	stats.text += "物理防禦: [color=#6B8CAE]48[/color]   暴擊率: [color=#F0D78C]22%[/color]\n"
	stats.text += "怒氣量表: [color=#C45C4A]20 點 (滿怒超頻運轉 +25% 性能)[/color]\n"
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
	panel.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD))
	_bag_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = "冒險者背包 (道具與戰魂倉庫)"
	t.add_theme_font_size_override("font_size", 20)
	t.add_theme_color_override("font_color", GOLD_CLASSICAL)
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
		ssb.bg_color = OBSIDIAN_DEEP
		ssb.border_color = LINE_GOLD_SOFT
		ssb.set_border_width_all(1)
		ssb.border_width_bottom = 2
		ssb.set_corner_radius_all(6)
		sp.add_theme_stylebox_override("panel", ssb)
		var l := Label.new()
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		l.add_theme_font_size_override("font_size", 12)
		l.add_theme_color_override("font_color", INK_IVORY)
		if i == 0: l.text = "鐵劍"
		elif i == 1: l.text = "紅藥水x10"
		elif i == 2: l.text = "紅寶石"
		elif i == 3: l.text = "全衡之魂"
		sp.add_child(l)
		grid.add_child(sp)

func _fmt_int(n: int) -> String:
	var neg := n < 0
	var s := str(absi(n))
	var out := ""
	while s.length() > 3:
		out = "," + s.substr(s.length() - 3, 3) + out
		s = s.substr(0, s.length() - 3)
	return ("-" if neg else "") + s + out

func _energy_hud_text() -> String:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")
	var cur := 0
	var mx := 15
	if es:
		if es.has_method("current"):
			cur = int(es.call("current"))
		if es.get("MAX_ENERGY") != null:
			mx = int(es.get("MAX_ENERGY"))
	var s := "%d/%d" % [cur, mx]
	if cur < mx and es and es.has_method("seconds_to_next"):
		var m := int(ceil(float(es.call("seconds_to_next")) / 60.0))
		s += " %d分" % maxi(1, m)
	return s

func refresh_hud() -> void:
	var gs := _gs()
	var lv := 1
	var gold := 0
	var dust := 0
	var pow := 0
	if gs:
		lv = maxi(1, int(gs.level))
		gold = int(gs.gold)
		dust = int(gs.stardust)
		if gs.has_method("power_score"):
			pow = int(gs.call("power_score"))
	if _lv_label:
		_lv_label.text = "Lv.%d" % lv
	if _name_label:
		_name_label.text = _get_hero_name()
	if _hero_name_tag:
		_hero_name_tag.text = _get_hero_name()
	if _profile_avatar:
		var cur_r := str(gs.player_race).strip_edges().to_lower() if gs and "player_race" in gs else "rabbit"
		_profile_avatar.texture = _get_hero_portrait(cur_r)
	if _hero_avatar:
		_load_hero_poses()
		if not _is_interacting and _tex_idle:
			_hero_avatar.texture = _tex_idle
	if _char_prev and _tex_idle:
		_char_prev.texture = _tex_idle
	if _power_label:
		_power_label.text = "戰力 %d" % pow
	if _energy_label:
		_energy_label.text = _energy_hud_text()
	if _gold_label:
		_gold_label.text = _fmt_int(gold)
	if _gem_label:
		_gem_label.text = _fmt_int(dust)

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
	tsb.bg_color = Color(0.043, 0.039, 0.055, 0.95)
	tsb.border_color = GOLD_CLASSICAL
	tsb.set_border_width_all(1)
	tsb.border_width_bottom = 3
	tsb.set_corner_radius_all(8)
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", INK_IVORY)
	toast.add_theme_font_size_override("font_size", 15)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.5)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)


## 開啟換裝衣櫥彈窗 (非開局選角，是隨時可重複開合的衣櫥)
func open_wardrobe() -> void:
	var existing = get_node_or_null("WardrobeDialog")
	if existing != null:
		return

	var wardrobe_scn := load("res://scenes/ui/wardrobe_dialog.tscn")
	var dlg: Control = null
	if wardrobe_scn != null:
		dlg = wardrobe_scn.instantiate() as Control
	else:
		var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
		if WardrobeClass != null:
			dlg = WardrobeClass.new() as Control

	if dlg == null:
		push_error("無法載入 WardrobeDialog")
		return

	if "creation_mode" in dlg:
		dlg.creation_mode = false

	if dlg.has_signal("outfit_saved"):
		dlg.connect("outfit_saved", func(_race: String, _selections: Dictionary):
			_load_hero_poses()
			refresh_hud()
			if _hero_avatar and _tex_idle and not _is_interacting:
				_hero_avatar.texture = _tex_idle
			if _char_prev and _tex_idle:
				_char_prev.texture = _tex_idle
			_show_toast(_t("換裝完成！新外裝已生效"))
		)

	# 開啟衣櫥時隱藏底層角色預覽，避免高亮剪影穿透全螢幕半透明遮罩 (review.md / 視覺品質標準)
	if _char_prev:
		_char_prev.visible = false
	var restore_prev := func():
		_load_hero_poses()
		if _hero_avatar and _tex_idle and not _is_interacting:
			_hero_avatar.texture = _tex_idle
		if _char_prev and _tex_idle:
			_char_prev.texture = _tex_idle
		if _char_prev:
			_char_prev.visible = true
	dlg.tree_exited.connect(restore_prev)

	add_child(dlg)


## 開啟王都鐵匠彈窗
func open_forge() -> Control:
	var existing = get_node_or_null("ForgeDialog")
	if existing != null:
		return existing
	var ForgeClass: GDScript = load("res://scripts/ui/forge_dialog.gd")
	if ForgeClass == null:
		push_error("無法載入 ForgeDialog")
		return null
	var dlg: Control = ForgeClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


## 開啟手藝工坊寶石彈窗
func open_gem_workshop() -> Control:
	var existing = get_node_or_null("GemWorkshopDialog")
	if existing != null:
		return existing
	var GemClass: GDScript = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemClass == null:
		push_error("無法載入 GemWorkshopDialog")
		return null
	var dlg: Control = GemClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


## 開啟冒險委託每日上發條彈窗
func open_windup_daily() -> Control:
	var existing = get_node_or_null("WindupDailyDialog")
	if existing != null:
		return existing
	var WindupClass: GDScript = load("res://scripts/ui/windup_daily_dialog.gd")
	if WindupClass == null:
		push_error("無法載入 WindupDailyDialog")
		return null
	var dlg: Control = WindupClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


