class_name CandyChipVfx
extends Node2D
## Alice W4-A1 / W4-F3 · 拆零件「糖果屑」誇張回饋。
## 粉／紫／奶油琺瑯碎片 + 黃銅齒輪屑；⛔ 不作寫實焊花／黑血。
## 可掛在 §8 smoke 或 battle_view part_broken（不改 battle_sim）。

signal finished

## 琺瑯主色（糖果屑）
const ENAMEL_PINK := Color(1.0, 0.55, 0.78, 1.0)
const ENAMEL_PURPLE := Color(0.72, 0.48, 0.95, 1.0)
const ENAMEL_CREAM := Color(1.0, 0.94, 0.82, 1.0)
## 黃銅齒輪屑
const BRASS_SHARD := Color(0.83, 0.63, 0.22, 1.0)
const BRASS_LIGHT := Color(0.95, 0.82, 0.45, 1.0)

## DropId 專屬偏色（圖鑑短卡對齊）
const DROP_TINTS := {
	"drop_brass_gear": Color(0.92, 0.72, 0.28, 1.0),
	"drop_spring_coil": Color(0.85, 0.78, 0.55, 1.0),
	"drop_core_shard": Color(0.35, 0.85, 0.78, 1.0),
}

const DROP_ICON_PATHS := {
	"drop_brass_gear": "res://assets/sprites/pack_a/vfx_drop_brass_gear.png",
	"drop_spring_coil": "res://assets/sprites/pack_a/vfx_drop_spring_coil.png",
	"drop_core_shard": "res://assets/sprites/pack_a/vfx_drop_core_shard.png",
}


## 在 parent 上於 origin（區域／全域座標視 parent）爆一叢糖果屑。
## drop_id 可空；有則套 tint，並嘗試顯示 Pack-A 掉落圖（缺檔不崩潰）。
static func play(parent: Node, origin: Vector2, drop_id: String = "", chip_count: int = 14) -> CandyChipVfx:
	var fx := CandyChipVfx.new()
	fx.name = "CandyChipVfx"
	fx.z_index = 50
	parent.add_child(fx)
	fx.global_position = origin
	fx._burst(drop_id, chip_count)
	return fx


func _burst(drop_id: String, chip_count: int) -> void:
	var tint: Color = DROP_TINTS.get(drop_id, Color(1, 1, 1, 1)) as Color
	var enamel: Array[Color] = [ENAMEL_PINK, ENAMEL_PURPLE, ENAMEL_CREAM]
	var rng := RandomNumberGenerator.new()
	rng.randomize()

	# 掉落圖示（可選）
	if drop_id != "":
		_spawn_drop_icon(drop_id, tint)

	for i in chip_count:
		var is_brass := (i % 3) == 0
		var col: Color
		if is_brass:
			col = BRASS_SHARD if (i % 6) == 0 else BRASS_LIGHT
		else:
			col = enamel[i % enamel.size()]
		# 掉落偏色：琺瑯略混、黃銅吃更多 tint
		if drop_id != "":
			col = col.lerp(tint, 0.35 if is_brass else 0.18)
		_spawn_chip(col, is_brass, rng)

	# 自動清場
	var tree := get_tree()
	if tree != null:
		tree.create_timer(0.85).timeout.connect(func() -> void:
			finished.emit()
			if is_instance_valid(self):
				queue_free()
		)
	else:
		finished.emit()
		queue_free()


func _spawn_drop_icon(drop_id: String, tint: Color) -> void:
	var path := str(DROP_ICON_PATHS.get(drop_id, ""))
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	var tex: Texture2D = load(path) as Texture2D
	if tex == null:
		return
	var icon := Sprite2D.new()
	icon.texture = tex
	icon.centered = true
	icon.modulate = Color(tint.r, tint.g, tint.b, 0.95)
	icon.scale = Vector2(0.18, 0.18)
	icon.z_index = 2
	add_child(icon)
	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(icon, "position", Vector2(0, -48), 0.55).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.tween_property(icon, "scale", Vector2(0.28, 0.28), 0.25)
	tw.tween_property(icon, "modulate:a", 0.0, 0.35).set_delay(0.4)


func _spawn_chip(col: Color, is_brass: bool, rng: RandomNumberGenerator) -> void:
	var chip := Polygon2D.new()
	# 不規則碎片多邊形（琺瑯小片／黃銅齒輪感菱形）
	if is_brass:
		chip.polygon = PackedVector2Array([
			Vector2(0, -7), Vector2(6, -2), Vector2(5, 5), Vector2(-5, 5), Vector2(-6, -2),
		])
	else:
		var s := rng.randf_range(4.0, 8.0)
		chip.polygon = PackedVector2Array([
			Vector2(-s * 0.4, -s), Vector2(s * 0.7, -s * 0.3),
			Vector2(s * 0.5, s * 0.8), Vector2(-s * 0.6, s * 0.4),
		])
	chip.color = col
	chip.position = Vector2(rng.randf_range(-6, 6), rng.randf_range(-4, 4))
	chip.rotation = rng.randf_range(0.0, TAU)
	add_child(chip)

	var angle := rng.randf_range(-PI, PI)
	var dist := rng.randf_range(48.0, 120.0)
	var target := Vector2(cos(angle), sin(angle)) * dist + Vector2(0, rng.randf_range(10, 40))
	var spin := rng.randf_range(-4.0, 4.0)
	var dur := rng.randf_range(0.45, 0.75)

	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(chip, "position", chip.position + target, dur).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(chip, "rotation", chip.rotation + spin, dur)
	tw.tween_property(chip, "modulate:a", 0.0, dur * 0.55).set_delay(dur * 0.4)
	tw.tween_property(chip, "scale", Vector2(0.35, 0.35), dur)


## 給 battle_view 等 Control 父節點用：把 Control 全域中心轉成 Node2D 子節點座標。
static func play_at_control(parent: CanvasItem, anchor: Control, drop_id: String = "") -> CandyChipVfx:
	if parent == null:
		return null
	var origin := Vector2.ZERO
	if anchor != null and is_instance_valid(anchor):
		origin = anchor.global_position + anchor.size * 0.5
	else:
		origin = parent.get_global_transform_with_canvas().origin
	return play(parent, origin, drop_id)
