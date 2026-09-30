extends SceneTree
## 驗證戰鬥受擊金屬火星與齒輪爆散粒子特效
## 執行方式：godot --path game --headless -s res://scripts/battle/test_combat_hit_fx.gd

const CombatHitFx := preload("res://scripts/battle/combat_hit_fx.gd")

var _frame := 0
var _fx_normal: CombatHitFx = null
var _fx_crit: CombatHitFx = null
var _root_node: Node2D = null

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		root.size = Vector2i(1280, 720)
		_root_node = Node2D.new()
		_root_node.name = "TestRoot"
		root.add_child(_root_node)
		print("=== 開始驗證戰鬥打擊金屬火花與齒輪爆散特效 ===")
		_fx_normal = CombatHitFx.spawn_hit_particles(_root_node, Vector2(640, 360), false, 1.0)
		_fx_crit = CombatHitFx.spawn_hit_particles(_root_node, Vector2(400, 300), true, 1.2)
		var flash := _fx_normal.get_node_or_null("ImpactFlash")
		if flash == null:
			push_error("TEST_COMBAT_HIT_FX_FAIL: 缺少 ImpactFlash")
			quit(1)
			return true
		print("  ✓ ImpactFlash 衝擊光芒存在")
	elif _frame == 3:
		var sparks := get_nodes_in_group("combat_hit_sparks")
		var gears := get_nodes_in_group("combat_hit_gears")
		print("全場打擊粒子數 - 火星: %d, 齒輪: %d" % [sparks.size(), gears.size()])

		var normal_sparks := 0
		var normal_gears := 0
		for c in _fx_normal.get_children():
			if c.is_in_group("combat_hit_sparks"):
				normal_sparks += 1
			elif c.is_in_group("combat_hit_gears"):
				normal_gears += 1
		print("普通受擊 - 火星: %d, 齒輪: %d" % [normal_sparks, normal_gears])

		var crit_sparks := 0
		var crit_gears := 0
		for c in _fx_crit.get_children():
			if c.is_in_group("combat_hit_sparks"):
				crit_sparks += 1
			elif c.is_in_group("combat_hit_gears"):
				crit_gears += 1
		print("暴擊受擊 - 火星: %d, 齒輪: %d" % [crit_sparks, crit_gears])

		if normal_sparks < 5:
			push_error("TEST_COMBAT_HIT_FX_FAIL: 普通火星不足 (%d < 5)" % normal_sparks)
			quit(1)
			return true
		if normal_gears < 2:
			push_error("TEST_COMBAT_HIT_FX_FAIL: 普通齒輪不足 (%d < 2)" % normal_gears)
			quit(1)
			return true
		if crit_sparks <= normal_sparks:
			push_error("TEST_COMBAT_HIT_FX_FAIL: 暴擊火星應多於普通 (%d <= %d)" % [crit_sparks, normal_sparks])
			quit(1)
			return true
		if crit_gears <= normal_gears:
			push_error("TEST_COMBAT_HIT_FX_FAIL: 暴擊齒輪應多於普通 (%d <= %d)" % [crit_gears, normal_gears])
			quit(1)
			return true

		# 驗證黃銅齒輪貼圖
		var g_tex := CombatHitFx.get_gear_texture()
		print("黃銅齒輪貼圖尺寸: ", g_tex.get_size() if g_tex else "無")

		print("TEST_COMBAT_HIT_FX_OK")
		quit(0)
		return true
	return false
