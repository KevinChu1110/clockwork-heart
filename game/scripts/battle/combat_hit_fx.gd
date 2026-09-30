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
static func spawn_hit_particles(parent: Node, hit_pos: Vector2, is_crit: bool = false, intensity: float = 1.0) -> Node2D:
	if parent == null or not is_instance_valid(parent):
		return null
	var gp = Engine.get_main_loop().root.get_node_or_null("GraphicsProfile") if Engine.get_main_loop() is SceneTree else null
	if gp != null and gp.has_method("vfx_enabled") and not gp.vfx_enabled():
		return null

	var script: GDScript = load("res://scripts/battle/combat_hit_fx.gd") as GDScript
	var fx: Node2D = script.new() as Node2D
	fx.name = "CombatHitFx"
	fx.z_index = 45
	parent.add_child(fx)
	fx.global_position = hit_pos
	fx.call("_play", is_crit, intensity)
	return fx


## 在指定父節點生成部位破壞特寫特效（慢動作齒輪噴發、衝擊光環、大量火花）
static func spawn_part_break_fx(parent: Node, hit_pos: Vector2, part_name: String = "") -> Node2D:
	if parent == null or not is_instance_valid(parent):
		return null
	var gp = Engine.get_main_loop().root.get_node_or_null("GraphicsProfile") if Engine.get_main_loop() is SceneTree else null
	if gp != null and gp.has_method("vfx_enabled") and not gp.vfx_enabled():
		return null

	var script: GDScript = load("res://scripts/battle/combat_hit_fx.gd") as GDScript
	var fx: Node2D = script.new() as Node2D
	fx.name = "CombatPartBreakFx"
	fx.z_index = 50
	parent.add_child(fx)
	fx.global_position = hit_pos
	fx.call("_play_part_break", part_name)
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


## ── 部位破壞特寫特效（慢動作齒輪噴發、衝擊光環、大量火花） ──
func _play_part_break(part_name: String = "") -> void:
	var gp = Engine.get_main_loop().root.get_node_or_null("GraphicsProfile") if Engine.get_main_loop() is SceneTree else null
	var rng := RandomNumberGenerator.new()
	rng.randomize()

	var spark_count := 28
	var gear_count := 10
	var screw_count := 6
	if gp != null and gp.has_method("particle_count"):
		spark_count = int(gp.particle_count(spark_count))
		gear_count = int(gp.particle_count(gear_count))
		screw_count = int(gp.particle_count(screw_count))

	# 1. 巨大破裂衝擊星芒與金藍衝擊光環 (Shockwave Ring & Burst Star)
	_spawn_break_shockwave()
	_spawn_break_starburst()

	# 2. 全方位高密度多巴胺金屬火花 (360度爆散)
	_spawn_break_sparks(spark_count, rng)

	# 3. 零件齒輪慢動作噴發 (Slow-Mo Flying Brass Gears, 1.5s)
	_spawn_break_gears_slowmo(gear_count, rng)

	# 4. 飛散發條螺絲與彈簧零件 (Clockwork Screws & Springs)
	_spawn_break_screws_and_springs(screw_count, rng)

	# 5. 自動回收（慢動作持續時間 1.65 秒）
	var max_dur := 1.65
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


## 衝擊光環 (Shockwave Ring)
func _spawn_break_shockwave() -> void:
	var ring := Node2D.new()
	ring.name = "BreakShockwave"
	ring.add_to_group("combat_break_shockwave")
	add_child(ring)

	var poly := Polygon2D.new()
	var add_mat := CanvasItemMaterial.new()
	add_mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	poly.material = add_mat
	var pts := PackedVector2Array()
	var segs := 36
	var r_outer := 70.0
	var r_inner := 54.0
	for i in range(segs + 1):
		var a := float(i) * TAU / float(segs)
		pts.append(Vector2(cos(a) * r_outer, sin(a) * r_outer))
	for i in range(segs, -1, -1):
		var a := float(i) * TAU / float(segs)
		pts.append(Vector2(cos(a) * r_inner, sin(a) * r_inner))
	poly.polygon = pts
	poly.color = GOLD_CORE
	ring.add_child(poly)

	ring.scale = Vector2(0.2, 0.2)
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(ring, "scale", Vector2(2.8, 2.8), 0.42).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(poly, "color", CYAN_CORE, 0.35)
	tw.tween_property(ring, "modulate:a", 0.0, 0.42).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_callback(ring.queue_free).set_delay(0.45)


## 破裂星芒 (12-Point Burst Star)
func _spawn_break_starburst() -> void:
	var star := Polygon2D.new()
	star.name = "BreakStarburst"
	star.add_to_group("combat_break_starburst")
	var add_mat := CanvasItemMaterial.new()
	add_mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	star.material = add_mat

	var pts := PackedVector2Array()
	var n_pts := 12
	var r_outer := 96.0
	var r_inner := 28.0
	for i in range(n_pts * 2):
		var a := float(i) * PI / float(n_pts)
		var r := r_outer if (i % 2 == 0) else r_inner
		pts.append(Vector2(cos(a) * r, sin(a) * r))
	star.polygon = pts
	star.color = WHITE_HOT
	star.scale = Vector2(0.3, 0.3)
	add_child(star)

	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(star, "scale", Vector2(2.5, 2.5), 0.22).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(star, "color", GOLD_CORE, 0.18)
	tw.tween_property(star, "modulate:a", 0.0, 0.24).set_delay(0.12)
	tw.tween_callback(star.queue_free).set_delay(0.38)


## 破裂多巴胺火花 (360度爆散)
func _spawn_break_sparks(count: int, rng: RandomNumberGenerator) -> void:
	var spark_colors: Array[Color] = [WHITE_HOT, GOLD_CORE, GOLD_HOVER, ORANGE_SPARK, STRAWBERRY_POP, CYAN_CORE]
	for i in range(count):
		var spark := Polygon2D.new()
		spark.name = "BreakSpark_%d" % i
		spark.add_to_group("combat_hit_sparks")
		spark.add_to_group("combat_break_sparks")
		var add_mat := CanvasItemMaterial.new()
		add_mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
		spark.material = add_mat

		var len_s := rng.randf_range(44.0, 72.0)
		var w_s := rng.randf_range(10.0, 16.0)
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
		var dist := rng.randf_range(140.0, 320.0)
		var target := Vector2(cos(angle), sin(angle)) * dist
		var dur := rng.randf_range(0.45, 0.70)

		var tw := create_tween()
		tw.set_parallel(true)
		tw.tween_property(spark, "position", target, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(spark, "scale", Vector2(0.15, 0.15), dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.tween_property(spark, "modulate:a", 0.0, dur * 0.45).set_delay(dur * 0.55)
		tw.tween_callback(spark.queue_free).set_delay(dur)


## 慢動作拋物線零件齒輪噴發 (Slow-Mo Flying Brass Gears)
func _spawn_break_gears_slowmo(count: int, rng: RandomNumberGenerator) -> void:
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

		gear.name = "BreakGear_%d" % i
		gear.add_to_group("combat_hit_gears")
		gear.add_to_group("combat_break_gears")
		add_child(gear)

		# 寬角度扇形噴射 (-165度 到 -15度)
		var angle := rng.randf_range(-PI * 0.92, -PI * 0.08)
		var speed_x := cos(angle) * rng.randf_range(110.0, 280.0)
		var peak_y := -rng.randf_range(130.0, 240.0)
		var fall_y := rng.randf_range(120.0, 260.0)
		var dur := rng.randf_range(1.35, 1.55)  ## 慢動作拉長至 ~1.5 秒
		var spin := rng.randf_range(-PI * 6.0, PI * 6.0)

		var target_scale := Vector2(1.25, 1.25) * rng.randf_range(0.9, 1.3)
		gear.scale = Vector2(0.4, 0.4)
		gear.modulate = Color(1.0, rng.randf_range(0.85, 1.0), rng.randf_range(0.35, 0.75), 1.0)

		var tw := create_tween()
		tw.set_parallel(true)
		# 彈跳縮放 (TRANS_BACK 慢動作彈跳)
		tw.tween_property(gear, "scale", target_scale, 0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		tw.tween_property(gear, "scale", target_scale * 0.65, dur - 0.16).set_delay(0.16)
		# X 軸水平飛行（緩慢飄散）
		tw.tween_property(gear, "position:x", speed_x, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		# Y 軸慢動作拋物線 (先優雅上升，再飄散落下)
		tw.tween_property(gear, "position:y", peak_y, dur * 0.42).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(gear, "position:y", peak_y + fall_y, dur * 0.58).set_delay(dur * 0.42).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		# 旋轉
		tw.tween_property(gear, "rotation", spin, dur)
		# 尾端平滑淡出
		tw.tween_property(gear, "modulate:a", 0.0, dur * 0.32).set_delay(dur * 0.68)
		tw.tween_callback(gear.queue_free).set_delay(dur)


## 飛散發條螺絲與彈簧零件 (Clockwork Screws & Springs)
func _spawn_break_screws_and_springs(count: int, rng: RandomNumberGenerator) -> void:
	for i in range(count):
		var part := Polygon2D.new()
		part.name = "BreakPart_%d" % i
		part.add_to_group("combat_break_parts")

		var is_spring := (i % 2 == 0)
		if is_spring:
			# 彈簧線條多邊形
			var s_pts := PackedVector2Array([
				Vector2(-12, -4), Vector2(-4, -8), Vector2(4, -4),
				Vector2(12, -8), Vector2(8, 0), Vector2(0, 4),
				Vector2(-8, 0), Vector2(-12, -4)
			])
			part.polygon = s_pts
			part.color = Color("#FFA010")  ## 亮橘黃銅彈簧
		else:
			# 六角螺絲多邊形
			var sc_pts := PackedVector2Array()
			for s in range(6):
				var a := float(s) * TAU / 6.0
				sc_pts.append(Vector2(cos(a) * 8.0, sin(a) * 8.0))
			part.polygon = sc_pts
			part.color = Color("#FFE066")  ## 鍍金螺絲
		add_child(part)

		var angle := rng.randf_range(-PI * 0.95, -PI * 0.05)
		var speed_x := cos(angle) * rng.randf_range(90.0, 250.0)
		var peak_y := -rng.randf_range(110.0, 200.0)
		var fall_y := rng.randf_range(100.0, 230.0)
		var dur := rng.randf_range(1.20, 1.45)
		var spin := rng.randf_range(-PI * 7.0, PI * 7.0)

		part.scale = Vector2(0.5, 0.5)
		var tw := create_tween()
		tw.set_parallel(true)
		tw.tween_property(part, "scale", Vector2(1.2, 1.2), 0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		tw.tween_property(part, "scale", Vector2(0.6, 0.6), dur - 0.14).set_delay(0.14)
		tw.tween_property(part, "position:x", speed_x, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(part, "position:y", peak_y, dur * 0.40).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(part, "position:y", peak_y + fall_y, dur * 0.60).set_delay(dur * 0.40).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.tween_property(part, "rotation", spin, dur)
		tw.tween_property(part, "modulate:a", 0.0, dur * 0.30).set_delay(dur * 0.70)
		tw.tween_callback(part.queue_free).set_delay(dur)
