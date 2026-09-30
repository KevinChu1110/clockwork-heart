class_name CombatHitFx
extends Node2D
## 戰鬥打擊回饋與受擊特效：金屬火星、飛散小齒輪、打擊衝擊光芒。
## 契合發條玩具主題（零毛皮、金屬板件、黃銅齒輪、多巴胺鮮亮高飽和色盤）。

signal finished

## 多巴胺糖果與黃銅金屬配色
const GOLD_CORE := Color("#FFD028")       ## 金黃核心
const GOLD_HOVER := Color("#FFE066")      ## 亮金反光
const ORANGE_SPARK := Color("#FFA010")    ## 暖橘火花
const WHITE_HOT := Color("#FFFFFF")       ## 白熱亮點
const STRAWBERRY_POP := Color("#FF5E8A")  ## 多巴胺粉紅火星
const CYAN_CORE := Color("#38A0FF")       ## 機芯天藍亮星
const DARK_OUTLINE := Color("#1F1A3A")    ## 深藍紫描邊

static var _gear_tex: Texture2D = null

static func get_gear_texture() -> Texture2D:
	if _gear_tex != null:
		return _gear_tex
	const path := "res://assets/sprites/fx/fx_gear_brass.png"
	if ResourceLoader.exists(path):
		_gear_tex = load(path) as Texture2D
	if _gear_tex == null:
		var global_p := ProjectSettings.globalize_path(path)
		if FileAccess.file_exists(global_p):
			var img := Image.load_from_file(global_p)
			if img != null:
				_gear_tex = ImageTexture.create_from_image(img)
	return _gear_tex


## 在指定父節點的全域位置生成打擊粒子
static func spawn_hit_particles(parent: Node, hit_pos: Vector2, is_crit: bool = false, intensity: float = 1.0) -> CombatHitFx:
	if parent == null or not is_instance_valid(parent):
		return null
	var gp = Engine.get_main_loop().root.get_node_or_null("GraphicsProfile") if Engine.get_main_loop() is SceneTree else null
	if gp != null and gp.has_method("vfx_enabled") and not gp.vfx_enabled():
		return null

	var fx := CombatHitFx.new()
	fx.name = "CombatHitFx"
	fx.z_index = 45
	parent.add_child(fx)
	fx.global_position = hit_pos
	fx._play(is_crit, intensity)
	return fx


func _play(is_crit: bool, intensity: float) -> void:
	var gp = Engine.get_main_loop().root.get_node_or_null("GraphicsProfile") if Engine.get_main_loop() is SceneTree else null
	var rng := RandomNumberGenerator.new()
	rng.randomize()

	var spark_count := 14 if is_crit else 9
	var gear_count := 6 if is_crit else 3
	if gp != null and gp.has_method("particle_count"):
		spark_count = int(gp.particle_count(spark_count))
		gear_count = int(gp.particle_count(gear_count))

	# 1. 核心衝擊星芒閃光
	_spawn_impact_flash(is_crit, intensity)

	# 2. 金屬火星噴射
	_spawn_sparks(spark_count, is_crit, intensity, rng)

	# 3. 飛散小齒輪
	_spawn_gears(gear_count, is_crit, intensity, rng)

	# 4. 自動回收
	var max_dur := 0.95
	var tree: SceneTree = null
	if is_inside_tree():
		tree = get_tree()
	if tree == null and Engine.get_main_loop() is SceneTree:
		tree = Engine.get_main_loop() as SceneTree
	if tree != null:
		tree.create_timer(max_dur).timeout.connect(func():
			finished.emit()
			if is_instance_valid(self):
				queue_free()
		)
	else:
		finished.emit()
		queue_free()


## 1. 核心衝擊星芒閃光
func _spawn_impact_flash(is_crit: bool, intensity: float) -> void:
	var flash := Polygon2D.new()
	flash.name = "ImpactFlash"
	var add_mat := CanvasItemMaterial.new()
	add_mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	flash.material = add_mat

	# 八角星形衝擊光
	var pts := PackedVector2Array()
	var n_pts := 8
	var r_outer := 56.0 * (1.5 if is_crit else 1.0) * intensity
	var r_inner := 18.0 * (1.5 if is_crit else 1.0) * intensity
	for i in range(n_pts * 2):
		var a := float(i) * PI / float(n_pts)
		var r := r_outer if (i % 2 == 0) else r_inner
		pts.append(Vector2(cos(a) * r, sin(a) * r))
	flash.polygon = pts
	flash.color = WHITE_HOT
	flash.scale = Vector2(0.4, 0.4)
	add_child(flash)

	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(flash, "scale", Vector2(2.2, 2.2), 0.16).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(flash, "color", GOLD_CORE, 0.12)
	tw.tween_property(flash, "modulate:a", 0.0, 0.20).set_delay(0.08)
	tw.tween_callback(flash.queue_free).set_delay(0.28)


## 2. 金屬火星噴射
func _spawn_sparks(count: int, is_crit: bool, intensity: float, rng: RandomNumberGenerator) -> void:
	var spark_colors: Array[Color] = [WHITE_HOT, GOLD_CORE, GOLD_HOVER, ORANGE_SPARK, STRAWBERRY_POP, CYAN_CORE]
	for i in range(count):
		var spark := Polygon2D.new()
		spark.name = "HitSpark_%d" % i
		spark.add_to_group("combat_hit_sparks")
		var add_mat := CanvasItemMaterial.new()
		add_mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
		spark.material = add_mat

		var len_s := rng.randf_range(32.0, 56.0) * (1.3 if is_crit else 1.0) * intensity
		var w_s := rng.randf_range(8.0, 14.0) * intensity
		# 菱形火星光斑
		spark.polygon = PackedVector2Array([
			Vector2(0, -len_s * 0.5),
			Vector2(w_s * 0.5, 0),
			Vector2(0, len_s * 0.5),
			Vector2(-w_s * 0.5, 0),
		])
		spark.color = spark_colors[i % spark_colors.size()]
		add_child(spark)

		var angle := rng.randf_range(0.0, TAU)
		spark.rotation = angle + PI * 0.5
		var dist := rng.randf_range(90.0, 220.0) * (1.35 if is_crit else 1.0) * intensity
		var target := Vector2(cos(angle), sin(angle)) * dist
		var dur := rng.randf_range(0.35, 0.55)

		var tw := create_tween()
		tw.set_parallel(true)
		tw.tween_property(spark, "position", target, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(spark, "scale", Vector2(0.2, 0.2), dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.tween_property(spark, "modulate:a", 0.0, dur * 0.5).set_delay(dur * 0.5)
		tw.tween_callback(spark.queue_free).set_delay(dur)


## 3. 飛散小齒輪
func _spawn_gears(count: int, is_crit: bool, intensity: float, rng: RandomNumberGenerator) -> void:
	var g_tex := get_gear_texture()
	for i in range(count):
		var gear: Node2D
		if g_tex != null:
			var spr := Sprite2D.new()
			spr.texture = g_tex
			spr.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			gear = spr
		else:
			gear = _create_fallback_gear_polygon(rng)

		gear.name = "HitGear_%d" % i
		gear.add_to_group("combat_hit_gears")
		add_child(gear)

		# 往上方散射拋物線弧度 (-150度 到 -30度)
		var angle := rng.randf_range(-PI * 0.85, -PI * 0.15)
		var speed_x := cos(angle) * rng.randf_range(80.0, 220.0) * intensity
		var peak_y := -rng.randf_range(70.0, 140.0) * intensity
		var fall_y := rng.randf_range(50.0, 120.0) * intensity
		var dur := rng.randf_range(0.60, 0.85)
		var spin := rng.randf_range(-PI * 5.0, PI * 5.0)

		var target_scale := Vector2(0.95, 0.95) * (1.3 if is_crit else 1.0)
		gear.scale = Vector2(0.4, 0.4)
		gear.modulate = Color(1.0, rng.randf_range(0.85, 1.0), rng.randf_range(0.4, 0.8), 1.0)

		var tw := create_tween()
		tw.set_parallel(true)
		# 縮放彈出
		tw.tween_property(gear, "scale", target_scale, 0.10).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		tw.tween_property(gear, "scale", target_scale * 0.70, dur - 0.10).set_delay(0.10)
		# X 軸水平飛行
		tw.tween_property(gear, "position:x", speed_x, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		# Y 軸先向上再落下重力弧線
		tw.tween_property(gear, "position:y", peak_y, dur * 0.45).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(gear, "position:y", peak_y + fall_y, dur * 0.55).set_delay(dur * 0.45).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		# 旋轉
		tw.tween_property(gear, "rotation", spin, dur)
		# 淡出
		tw.tween_property(gear, "modulate:a", 0.0, dur * 0.35).set_delay(dur * 0.65)
		tw.tween_callback(gear.queue_free).set_delay(dur)


func _create_fallback_gear_polygon(rng: RandomNumberGenerator) -> Polygon2D:
	var poly := Polygon2D.new()
	var pts := PackedVector2Array()
	var teeth := 8
	var r_out := 24.0
	var r_in := 16.0
	for i in range(teeth):
		var a0 := (float(i) * TAU) / float(teeth)
		var a1 := a0 + 0.25 * (TAU / float(teeth))
		var a2 := a0 + 0.75 * (TAU / float(teeth))
		var a3 := a0 + (TAU / float(teeth))
		pts.append(Vector2(cos(a0) * r_in, sin(a0) * r_in))
		pts.append(Vector2(cos(a1) * r_out, sin(a1) * r_out))
		pts.append(Vector2(cos(a2) * r_out, sin(a2) * r_out))
		pts.append(Vector2(cos(a3) * r_in, sin(a3) * r_in))
	poly.polygon = pts
	poly.color = GOLD_CORE
	return poly
