class_name SoulSummonFx
extends Control
## 聚魂殿堂召喚動效：中央發條核心上鍊旋轉、金色齒輪解鎖與多巴胺彩糖星芒爆散。

signal animation_finished

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"
const KEY_ASSET := "res://assets/sprites/player/paperdoll/rabbit/winding_key/key_classic_brass_512.png"
const GEAR_ASSET := "res://assets/icons/core_slots/slot_04_transmission_gears.png"

## 多巴胺糖果爆散色盤
const DOPAMINE_COLORS := [
	Color("#FFD028"),  # 金黃
	Color("#FFA010"),  # 暖橘
	Color("#4ED86A"),  # 薄荷綠
	Color("#38A0FF"),  # 晴空藍
	Color("#FF5E8A"),  # 珊瑚粉
	Color("#FFFFFF"),  # 晨曦白
	Color("#A259FF")   # 炫彩紫
]

var _dim_bg: ColorRect
var _center_node: Control
var _glow_ring: Control
var _flash_sphere: Panel
var _left_gear: TextureRect
var _right_gear: TextureRect
var _windup_key: TextureRect
var _shockwave: Control
var _star_layer: Control
var _skip_btn: Button
var _title_hint: Label
var _font: Font = null

var _tween: Tween = null
var _is_playing: bool = false
var _callback: Callable


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_PASS
	_load_font()
	_build_ui()
	visible = false


func _load_font() -> void:
	if _font == null and ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font


func _build_ui() -> void:
	# 1. 聚光暗幕背景（半透明深藍紫，烘托中央發條金色焦點）
	_dim_bg = ColorRect.new()
	_dim_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_dim_bg.color = Color(0.08, 0.06, 0.16, 0.88)
	add_child(_dim_bg)

	# 2. 中央容器
	_center_node = Control.new()
	_center_node.set_anchors_preset(Control.PRESET_CENTER)
	_center_node.position = Vector2(640, 360)
	add_child(_center_node)

	# 3. 儀式標題提示
	_title_hint = Label.new()
	_title_hint.text = "✦ 發條解鎖 · 聚魂召喚 ✦"
	_title_hint.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_title_hint.offset_top = 36
	_title_hint.offset_bottom = 76
	_title_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_title_hint.add_theme_font_size_override("font_size", 28)
	_title_hint.add_theme_color_override("font_color", Color("#FFD028"))
	if _font != null:
		_title_hint.add_theme_font_override("font", _font)
	add_child(_title_hint)

	# 4. 儀式光環底層
	_glow_ring = Control.new()
	_glow_ring.custom_minimum_size = Vector2(340, 340)
	_glow_ring.position = Vector2(-170, -170)
	_glow_ring.pivot_offset = Vector2(170, 170)
	_center_node.add_child(_glow_ring)

	var ring_panel := Panel.new()
	ring_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	var r_style := StyleBoxFlat.new()
	r_style.bg_color = Color(1.0, 0.82, 0.18, 0.15)
	r_style.border_color = Color("#FFD028")
	r_style.set_border_width_all(5)
	r_style.set_corner_radius_all(170)
	r_style.shadow_color = Color(1.0, 0.82, 0.18, 0.65)
	r_style.shadow_size = 28
	ring_panel.add_theme_stylebox_override("panel", r_style)
	_glow_ring.add_child(ring_panel)

	# 4b. 中央高光閃光球
	_flash_sphere = Panel.new()
	_flash_sphere.custom_minimum_size = Vector2(180, 180)
	_flash_sphere.position = Vector2(-90, -90)
	_flash_sphere.pivot_offset = Vector2(90, 90)
	var flash_style := StyleBoxFlat.new()
	flash_style.bg_color = Color(1.0, 0.95, 0.7, 0.35)
	flash_style.border_color = Color("#FFFFFF")
	flash_style.set_border_width_all(2)
	flash_style.set_corner_radius_all(90)
	flash_style.shadow_color = Color(1.0, 0.9, 0.4, 0.8)
	flash_style.shadow_size = 32
	_flash_sphere.add_theme_stylebox_override("panel", flash_style)
	_center_node.add_child(_flash_sphere)

	# 5. 左右傳動解鎖齒輪（乾淨金色齒輪圖示）
	if ResourceLoader.exists(GEAR_ASSET):
		var gear_tex := load(GEAR_ASSET) as Texture2D
		_left_gear = TextureRect.new()
		_left_gear.texture = gear_tex
		_left_gear.custom_minimum_size = Vector2(120, 120)
		_left_gear.size = Vector2(120, 120)
		_left_gear.position = Vector2(-150, -60)
		_left_gear.pivot_offset = Vector2(60, 60)
		_left_gear.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		_left_gear.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_center_node.add_child(_left_gear)

		_right_gear = TextureRect.new()
		_right_gear.texture = gear_tex
		_right_gear.custom_minimum_size = Vector2(120, 120)
		_right_gear.size = Vector2(120, 120)
		_right_gear.position = Vector2(30, -60)
		_right_gear.pivot_offset = Vector2(60, 60)
		_right_gear.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		_right_gear.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_center_node.add_child(_right_gear)

	# 6. 中央發條主鑰匙
	_windup_key = TextureRect.new()
	if ResourceLoader.exists(KEY_ASSET):
		_windup_key.texture = load(KEY_ASSET) as Texture2D
	_windup_key.custom_minimum_size = Vector2(220, 220)
	_windup_key.size = Vector2(220, 220)
	_windup_key.position = Vector2(-110, -110)
	_windup_key.pivot_offset = Vector2(110, 110)
	_windup_key.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_windup_key.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_center_node.add_child(_windup_key)

	# 7. 衝擊波環層
	_shockwave = Control.new()
	_shockwave.position = Vector2.ZERO
	_center_node.add_child(_shockwave)

	# 8. 彩糖星芒粒子層
	_star_layer = Control.new()
	_star_layer.position = Vector2.ZERO
	_center_node.add_child(_star_layer)

	# 9. 右上角快速跳過按鈕
	_skip_btn = Button.new()
	_skip_btn.text = "跳過 >>"
	_skip_btn.custom_minimum_size = Vector2(90, 36)
	_skip_btn.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_skip_btn.offset_left = -110
	_skip_btn.offset_top = 20
	_skip_btn.offset_right = -20
	_skip_btn.offset_bottom = 56
	UiStyle.style_button(_skip_btn, false)
	if _font != null:
		_skip_btn.add_theme_font_override("font", _font)
	_skip_btn.pressed.connect(skip)
	add_child(_skip_btn)


func _gui_input(event: InputEvent) -> void:
	if _is_playing and event is InputEventMouseButton and event.pressed:
		skip()


func play_summon(is_ten: bool, on_finish: Callable) -> void:
	_callback = on_finish
	_is_playing = true
	visible = true
	modulate = Color(1, 1, 1, 1)

	_center_node.position = Vector2(size.x * 0.5 if size.x > 0 else 640.0, size.y * 0.5 if size.y > 0 else 360.0)
	_windup_key.rotation = 0.0
	_windup_key.scale = Vector2(0.9, 0.9)
	_windup_key.modulate = Color(1, 1, 1, 1)
	if _left_gear:
		_left_gear.position = Vector2(-150, -60)
		_left_gear.rotation = 0.0
		_left_gear.modulate = Color(1, 1, 1, 1)
	if _right_gear:
		_right_gear.position = Vector2(30, -60)
		_right_gear.rotation = 0.0
		_right_gear.modulate = Color(1, 1, 1, 1)

	_clear_particles()

	if _tween and _tween.is_valid():
		_tween.kill()

	_tween = create_tween()
	_tween.set_parallel(true)

	var windup_dur: float = 0.5
	var unlock_dur: float = 0.35
	var burst_dur: float = 0.45

	# ── 階段 1：發條上鍊旋轉與蓄力震動 ──
	var spin_turns: float = 5.0 if is_ten else 3.0
	_tween.tween_property(_windup_key, "rotation", TAU * spin_turns, windup_dur)\
		.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	_tween.tween_property(_windup_key, "scale", Vector2(1.25, 1.25), windup_dur)\
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

	if _left_gear:
		_tween.tween_property(_left_gear, "rotation", -TAU * spin_turns * 0.8, windup_dur)
	if _right_gear:
		_tween.tween_property(_right_gear, "rotation", TAU * spin_turns * 0.8, windup_dur)

	# ── 階段 2：齒輪卡榫解鎖彈出 ──
	var t2 := create_tween()
	t2.tween_interval(windup_dur)
	t2.tween_callback(func():
		if not _is_playing: return
		var t_gear := create_tween().set_parallel(true)
		if _left_gear:
			t_gear.tween_property(_left_gear, "position", Vector2(-260, -60), unlock_dur)\
				.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			t_gear.tween_property(_left_gear, "modulate:a", 0.0, unlock_dur + 0.1)
		if _right_gear:
			t_gear.tween_property(_right_gear, "position", Vector2(140, -60), unlock_dur)\
				.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			t_gear.tween_property(_right_gear, "modulate:a", 0.0, unlock_dur + 0.1)
	)

	# ── 階段 3：彩糖星芒爆散與同心圓衝擊波 ──
	var t3 := create_tween()
	t3.tween_interval(windup_dur + unlock_dur)
	t3.tween_callback(func():
		if not _is_playing: return
		_spawn_starburst(48 if is_ten else 32)
		_spawn_shockwave()
		var t_k := create_tween().set_parallel(true)
		t_k.tween_property(_windup_key, "scale", Vector2(1.8, 1.8), burst_dur)\
			.set_trans(Tween.TRANS_EXPO).set_ease(Tween.EASE_OUT)
		t_k.tween_property(_windup_key, "modulate:a", 0.0, burst_dur * 0.8)
	)

	# ── 階段 4：整體平滑過渡至結算卡 ──
	var t_end := create_tween()
	t_end.tween_interval(windup_dur + unlock_dur + burst_dur)
	t_end.tween_property(self, "modulate:a", 0.0, 0.2)
	t_end.tween_callback(func():
		_finish()
	)


func trigger_burst_instant() -> void:
	## 立即展示解鎖爆散的高峰狀態（供視覺展示與精確截圖）
	visible = true
	modulate = Color(1, 1, 1, 1)
	_center_node.position = Vector2(640, 360)
	_windup_key.rotation = PI * 0.8
	_windup_key.scale = Vector2(1.35, 1.35)
	_windup_key.modulate = Color(1, 1, 1, 0.95)
	if _left_gear:
		_left_gear.position = Vector2(-240, -60)
		_left_gear.rotation = -PI * 0.65
		_left_gear.modulate = Color(1, 1, 1, 0.85)
	if _right_gear:
		_right_gear.position = Vector2(120, -60)
		_right_gear.rotation = PI * 0.65
		_right_gear.modulate = Color(1, 1, 1, 0.85)
	_clear_particles()
	_spawn_starburst_static(48)
	_spawn_shockwave_static()


func _spawn_starburst_static(count: int) -> void:
	for i in range(count):
		var star := Control.new()
		var col: Color = DOPAMINE_COLORS[i % DOPAMINE_COLORS.size()]
		var angle: float = (float(i) / float(count)) * TAU + sin(float(i)) * 0.15
		var dist: float = 140.0 + (i % 4) * 65.0
		var pos := Vector2(cos(angle), sin(angle)) * dist
		var star_size: float = 20.0 + (i % 3) * 10.0

		var rect := ColorRect.new()
		rect.size = Vector2(star_size, star_size)
		rect.position = Vector2(-star_size * 0.5, -star_size * 0.5)
		rect.color = col
		rect.rotation = PI * 0.25
		rect.pivot_offset = Vector2(star_size * 0.5, star_size * 0.5)
		star.add_child(rect)

		# 交叉雙芒星（讓星芒更華麗）
		if i % 2 == 0:
			var cross := ColorRect.new()
			cross.size = Vector2(star_size * 1.5, star_size * 0.4)
			cross.position = Vector2(-star_size * 0.75, -star_size * 0.2)
			cross.color = Color(1, 1, 1, 0.9)
			star.add_child(cross)

		star.position = pos
		_star_layer.add_child(star)


func _spawn_shockwave_static() -> void:
	for i in range(2):
		var p := Panel.new()
		var rad: float = 240.0 if i == 0 else 380.0
		p.size = Vector2(rad, rad)
		p.position = Vector2(-rad * 0.5, -rad * 0.5)
		p.pivot_offset = Vector2(rad * 0.5, rad * 0.5)
		var style := StyleBoxFlat.new()
		style.bg_color = Color(1, 1, 1, 0.0)
		style.border_color = Color("#FFD028") if i == 0 else Color("#FFA010")
		style.set_border_width_all(5)
		style.set_corner_radius_all(int(rad * 0.5))
		style.shadow_color = Color(1, 0.8, 0.2, 0.6)
		style.shadow_size = 20
		p.add_theme_stylebox_override("panel", style)
		_shockwave.add_child(p)


func _spawn_starburst(count: int) -> void:
	for i in range(count):
		var star := Control.new()
		var col: Color = DOPAMINE_COLORS[i % DOPAMINE_COLORS.size()]
		var angle: float = (float(i) / float(count)) * TAU + randf_range(-0.1, 0.1)
		var dist: float = randf_range(180.0, 390.0)
		var target_pos := Vector2(cos(angle), sin(angle)) * dist
		var star_size: float = randf_range(18.0, 34.0)

		var rect := ColorRect.new()
		rect.size = Vector2(star_size, star_size)
		rect.position = Vector2(-star_size * 0.5, -star_size * 0.5)
		rect.color = col
		rect.rotation = PI * 0.25
		rect.pivot_offset = Vector2(star_size * 0.5, star_size * 0.5)
		star.add_child(rect)

		if i % 2 == 0:
			var cross := ColorRect.new()
			cross.size = Vector2(star_size * 1.5, star_size * 0.4)
			cross.position = Vector2(-star_size * 0.75, -star_size * 0.2)
			cross.color = Color(1, 1, 1, 0.9)
			star.add_child(cross)

		_star_layer.add_child(star)

		var tw := create_tween().set_parallel(true)
		tw.tween_property(star, "position", target_pos, 0.5)\
			.set_trans(Tween.TRANS_EXPO).set_ease(Tween.EASE_OUT)
		tw.tween_property(star, "scale", Vector2(0.3, 0.3), 0.5)
		tw.tween_property(star, "modulate:a", 0.0, 0.5)
		tw.chain().tween_callback(star.queue_free)


func _spawn_shockwave() -> void:
	for i in range(2):
		var p := Panel.new()
		p.size = Vector2(60, 60)
		p.position = Vector2(-30, -30)
		p.pivot_offset = Vector2(30, 30)
		var style := StyleBoxFlat.new()
		style.bg_color = Color(1, 1, 1, 0.0)
		style.border_color = Color("#FFD028") if i == 0 else Color("#FFA010")
		style.set_border_width_all(5)
		style.set_corner_radius_all(30)
		style.shadow_color = Color(1, 0.8, 0.2, 0.7)
		style.shadow_size = 18
		p.add_theme_stylebox_override("panel", style)
		_shockwave.add_child(p)

		var tw := create_tween().set_parallel(true)
		tw.tween_interval(i * 0.08)
		tw.tween_property(p, "scale", Vector2(16.0, 16.0), 0.45)\
			.set_trans(Tween.TRANS_EXPO).set_ease(Tween.EASE_OUT)
		tw.tween_property(p, "modulate:a", 0.0, 0.45)
		tw.chain().tween_callback(p.queue_free)


func _clear_particles() -> void:
	for c in _star_layer.get_children():
		c.queue_free()
	for c in _shockwave.get_children():
		c.queue_free()


func skip() -> void:
	if not _is_playing:
		return
	if _tween and _tween.is_valid():
		_tween.kill()
	_clear_particles()
	_finish()


func _finish() -> void:
	_is_playing = false
	visible = false
	animation_finished.emit()
	if _callback.is_valid():
		_callback.call()
