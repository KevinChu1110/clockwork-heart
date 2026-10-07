class_name PartBreakChestFx
extends Node2D

## 依據 docs/CLOCKWORK_HEART_GAME_OVERVIEW.md 壹.4 爆點三規範：
## 【破壞特寫與金箱頓挫（Break-Cam Slow-Mo）】
## Boss 部位破壞（part_break）觸發時，在受擊破壞處生成一顆彈跳落地的金色發條寶箱動效
## （Chest Bounce Tween 帶金色流光粒子），並彈出浮字提示掉落對應部位機芯，增加部位擊破爽快感。

signal finished

const ContentLocClass := preload("res://scripts/systems/content_loc.gd")
const CHEST_TEXTURE_PATH := "res://assets/sprites/props/escort_box_goldbox.png"
const KEY_TEXTURE_PATH := "res://assets/icons/items/friendship_key.png"
const FONT_HUNINN_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

var core_name: String = ""
var slot_id: String = ""
var origin: Vector2 = Vector2.ZERO

var chest_sprite: Sprite2D = null
var key_icon: Sprite2D = null
var particles: CPUParticles2D = null
var shadow: Polygon2D = null
var prompt_label: Label = null
var _container: Node2D = null
var _tween: Tween = null

static var _cached_spark_tex: Texture2D = null


static func _get_spark_tex() -> Texture2D:
	if _cached_spark_tex != null:
		return _cached_spark_tex
	var size := 24
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	var c := (size - 1) * 0.5
	for y in size:
		for x in size:
			var dx := absf(float(x) - c) / c
			var dy := absf(float(y) - c) / c
			var star := maxf(0.0, 1.0 - (sqrt(dx) + sqrt(dy)))
			var rad := maxf(0.0, 1.0 - sqrt(dx * dx + dy * dy))
			var val := clampf(star * 0.75 + rad * 0.45, 0.0, 1.0)
			if val <= 0.01:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
			else:
				var col := Color(1.0, 0.95, 0.6, val).lerp(Color(1.0, 0.65, 0.15, val), 1.0 - val)
				img.set_pixel(x, y, col)
	_cached_spark_tex = ImageTexture.create_from_image(img)
	return _cached_spark_tex


static func play(parent: Node, spawn_origin: Vector2, p_core_name: String = "", p_slot_id: String = "") -> PartBreakChestFx:
	var fx := PartBreakChestFx.new()
	fx.name = "BossPartBreakChestFx"
	fx.core_name = p_core_name
	fx.slot_id = p_slot_id
	fx.origin = spawn_origin
	fx.z_index = 55
	parent.add_child(fx)
	fx.global_position = spawn_origin
	fx.start_animation()
	return fx


func _ready() -> void:
	_build_visuals()


func _build_visuals() -> void:
	if _container != null:
		return

	# 1. 地面接觸軟陰影 (Dual Floor Shadow 原則之軟影)
	shadow = Polygon2D.new()
	shadow.name = "ChestShadow"
	var shadow_pts: PackedVector2Array = []
	var r_x := 28.0
	var r_y := 10.0
	for i in 16:
		var rad := float(i) * TAU / 16.0
		shadow_pts.append(Vector2(cos(rad) * r_x, sin(rad) * r_y))
	shadow.polygon = shadow_pts
	shadow.color = Color(0.08, 0.05, 0.12, 0.45)
	shadow.position = Vector2(0, 75)
	shadow.scale = Vector2(0.3, 0.3)
	shadow.modulate.a = 0.2
	add_child(shadow)

	# 2. 金色流光粒子 (CPUParticles2D)
	particles = CPUParticles2D.new()
	particles.name = "GoldParticles"
	particles.texture = _get_spark_tex()
	particles.emitting = false
	particles.one_shot = false
	particles.explosiveness = 0.75
	particles.amount = 32
	particles.lifetime = 0.65
	particles.direction = Vector2(0, -1)
	particles.spread = 180.0
	particles.gravity = Vector2(0, 240)
	particles.initial_velocity_min = 100.0
	particles.initial_velocity_max = 260.0
	particles.scale_amount_min = 1.0
	particles.scale_amount_max = 2.4
	var grad := Gradient.new()
	grad.set_color(0, Color(1.0, 0.98, 0.7, 1.0))
	grad.add_point(0.35, Color(1.0, 0.82, 0.25, 1.0))
	grad.add_point(0.75, Color(0.95, 0.55, 0.1, 0.75))
	grad.add_point(1.0, Color(0.85, 0.35, 0.05, 0.0))
	particles.color_ramp = grad
	particles.z_index = 2
	add_child(particles)

	# 3. 寶箱與裝飾主容器
	_container = Node2D.new()
	_container.name = "ChestContainer"
	add_child(_container)

	# 3.1 寶箱主體 Sprite (Q 版玩具金色發條寶箱)
	chest_sprite = Sprite2D.new()
	chest_sprite.name = "ChestSprite"
	if ResourceLoader.exists(CHEST_TEXTURE_PATH):
		chest_sprite.texture = load(CHEST_TEXTURE_PATH) as Texture2D
	chest_sprite.centered = true
	chest_sprite.modulate = Color(1.12, 1.06, 0.92, 1.0)
	_container.add_child(chest_sprite)

	# 3.2 發條鑰匙裝飾 (背後/箱頂發條鑰匙)
	if ResourceLoader.exists(KEY_TEXTURE_PATH):
		key_icon = Sprite2D.new()
		key_icon.name = "WindingKeyIcon"
		key_icon.texture = load(KEY_TEXTURE_PATH) as Texture2D
		key_icon.centered = true
		key_icon.position = Vector2(0, -26)
		key_icon.scale = Vector2(0.55, 0.55)
		key_icon.modulate = Color(1.15, 1.0, 0.65, 0.95)
		_container.add_child(key_icon)

	# 4. 浮字提示掉落對應部位機芯 (CorePromptLabel)
	prompt_label = Label.new()
	prompt_label.name = "CorePromptLabel"
	if ResourceLoader.exists(FONT_HUNINN_PATH):
		var f := load(FONT_HUNINN_PATH) as Font
		if f != null:
			prompt_label.add_theme_font_override("font", f)
	prompt_label.add_theme_font_size_override("font_size", 22)
	prompt_label.add_theme_color_override("font_color", Color(1.0, 0.92, 0.32, 1.0))
	prompt_label.add_theme_color_override("font_outline_color", Color(0.12, 0.08, 0.22, 1.0))
	prompt_label.add_theme_constant_override("outline_size", 4)
	prompt_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.85))
	prompt_label.add_theme_constant_override("shadow_offset_x", 2)
	prompt_label.add_theme_constant_override("shadow_offset_y", 2)
	prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	var display_txt := core_name
	if display_txt.is_empty():
		display_txt = ContentLocClass.text("ui", "共鳴核心")
	var t_tpl: String = ContentLocClass.text("ui", "掉落部位機芯：%s")
	if "%s" in t_tpl:
		prompt_label.text = t_tpl % display_txt
	else:
		prompt_label.text = "【" + ContentLocClass.text("ui", "機芯") + "】" + display_txt
	prompt_label.size = Vector2(260, 36)
	prompt_label.position = Vector2(-130, 20)
	prompt_label.scale = Vector2(0.5, 0.5)
	prompt_label.pivot_offset = Vector2(130, 18)
	prompt_label.modulate.a = 0.0
	prompt_label.z_index = 10
	add_child(prompt_label)


func start_animation() -> void:
	_build_visuals()

	# 檢查繪圖設定
	var vfx_on := true
	if is_inside_tree():
		var gp := get_node_or_null("/root/GraphicsProfile")
		if gp != null and gp.has_method("vfx_enabled"):
			vfx_on = gp.vfx_enabled()

	if vfx_on and particles != null:
		particles.emitting = true

	var target_landing := Vector2(0, 75)
	var peak_pos := Vector2(0, -48)

	_container.position = Vector2.ZERO
	_container.scale = Vector2(0.4, 0.4)
	_container.rotation = deg_to_rad(-12.0)

	_tween = create_tween()

	# ── 第一階段：破壞瞬間向上彈躍與放大 (Pop Arc: 0.18s) ──
	_tween.tween_property(_container, "position", peak_pos, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	_tween.parallel().tween_property(_container, "scale", Vector2(1.2, 1.2), 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_tween.parallel().tween_property(_container, "rotation", deg_to_rad(8.0), 0.18)

	# ── 第二階段：落體下墜至地面 (Fall: 0.20s) ──
	_tween.tween_property(_container, "position", target_landing, 0.20).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	_tween.parallel().tween_property(shadow, "scale", Vector2(1.0, 1.0), 0.20)
	_tween.parallel().tween_property(shadow, "modulate:a", 0.65, 0.20)
	_tween.parallel().tween_property(_container, "rotation", 0.0, 0.20)

	# ── 第三階段：第一下強力著地回彈與擠壓 (Squash & Bounce 1: 0.22s) ──
	_tween.tween_property(_container, "scale", Vector2(1.35, 0.68), 0.06).set_trans(Tween.TRANS_QUAD)
	_tween.tween_property(_container, "position", target_landing + Vector2(0, -28), 0.10).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	_tween.parallel().tween_property(_container, "scale", Vector2(0.88, 1.15), 0.10)
	_tween.tween_property(_container, "position", target_landing, 0.06).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	_tween.parallel().tween_property(_container, "scale", Vector2(1.15, 0.88), 0.06)

	# ── 機芯浮字提示於寶箱著地瞬間彈出 (0.4s 處同步觸發) ──
	_tween.parallel().tween_property(prompt_label, "modulate:a", 1.0, 0.12)
	_tween.parallel().tween_property(prompt_label, "scale", Vector2(1.15, 1.15), 0.12).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_tween.parallel().tween_property(prompt_label, "position:y", 15.0, 0.12)

	# ── 第四階段：第二下微小緩衝彈跳 (Bounce 2: 0.16s) ──
	_tween.tween_property(_container, "position", target_landing + Vector2(0, -10), 0.08).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	_tween.parallel().tween_property(_container, "scale", Vector2(0.95, 1.05), 0.08)
	_tween.tween_property(_container, "position", target_landing, 0.08).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	_tween.parallel().tween_property(_container, "scale", Vector2.ONE, 0.08)

	# 浮字回穩與緩慢上浮
	_tween.parallel().tween_property(prompt_label, "scale", Vector2.ONE, 0.12)
	_tween.parallel().tween_property(prompt_label, "position:y", -10.0, 0.65).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)

	# ── 第五階段：金光微動與收尾 (Settle & Fade: 0.8s) ──
	if key_icon != null:
		_tween.parallel().tween_property(key_icon, "rotation", deg_to_rad(25.0), 0.4).set_trans(Tween.TRANS_SINE)
		_tween.parallel().tween_property(key_icon, "rotation", deg_to_rad(-10.0), 0.4).set_delay(0.4).set_trans(Tween.TRANS_SINE)

	_tween.tween_property(_container, "modulate", Color(1.3, 1.25, 1.0, 1.0), 0.25).set_trans(Tween.TRANS_SINE)
	_tween.tween_property(_container, "modulate", Color(1.0, 1.0, 1.0, 0.0), 0.45).set_delay(0.35)
	_tween.parallel().tween_property(shadow, "modulate:a", 0.0, 0.45).set_delay(0.35)
	_tween.parallel().tween_property(prompt_label, "modulate:a", 0.0, 0.40).set_delay(0.40)

	_tween.tween_callback(func():
		finished.emit()
		if is_instance_valid(self):
			queue_free()
	)
