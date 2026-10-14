extends SceneTree
## 戰鬥立繪腳底要一直貼著接地軟影（#59）：
##   godot --headless -s res://scripts/battle/test_battle_shadow_anchor.gd
## 守：
##   1. 震屏結束後 Arena 回到原本的版面位置（以前歸零，整排角色往左上跳約 48,70）。
##   2. 震屏中、震屏後、Boss 突進時，主角與 Boss 的軟影中心都在腳底附近。

const TOL := 6.0

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null
var _home := Vector2.ZERO


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _feet(body: TextureRect) -> Vector2:
	var dr: Rect2 = _battle.call("_body_drawn_rect", body)
	var frac: float = _battle.call("_content_bottom_frac", body.texture)
	return body.get_global_transform() * Vector2(dr.position.x + dr.size.x * 0.5, dr.position.y + dr.size.y * frac)


func _check_shadows(tag: String) -> void:
	var layer: Control = _battle.get_node_or_null("ShadowLayer")
	if layer == null:
		_fail("%s：沒有 ShadowLayer" % tag)
		return
	for body in [_battle.get("player_body"), _battle.get("enemy_body")]:
		var sh := layer.get_node_or_null("ContactShadow_%s" % body.name) as TextureRect
		if sh == null:
			_fail("%s：%s 沒有接觸軟影" % [tag, body.name])
			continue
		var c: Vector2 = sh.global_position + sh.size * sh.get_global_transform().get_scale() * 0.5
		var d := c - _feet(body)
		if absf(d.x) > TOL or absf(d.y) > TOL:
			_fail("%s：%s 軟影離腳底 %s（容許 %.0fpx）" % [tag, body.name, d, TOL])
		else:
			print("  ok  %s %s 軟影偏差 %s" % [tag, body.name, d])


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			root.get_node("GameState").call("reset_new_game", "rabbit")
			_main.call("_start_battle_raw", "leo")
			_step = 1
			_wait = 0
		1:
			if _wait < 40:
				return false
			var host: Node = _main.get("host")
			_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
			if _battle == null or _battle.get("arena") == null:
				_fail("戰鬥場景沒載起來")
				return _finish()
			## 停住模擬，免得 Boss 自己出招干擾量測
			var sim = _battle.get("sim")
			if sim != null:
				sim.set("sim_paused", true)
			_home = (_battle.get("arena") as Control).position
			_check_shadows("開場")
			_battle.set("_shake", 0.5)
			_step = 2
			_wait = 0
		2:
			if _wait == 5:
				_check_shadows("震屏中")
			## 無頭跑的 delta 不固定：等震屏真的結束（最多 900 幀）
			if float(_battle.get("_shake")) > 0.0 and _wait < 900:
				return false
			var now: Vector2 = (_battle.get("arena") as Control).position
			if now.distance_to(_home) > 0.01:
				_fail("震屏後 Arena 位置 %s ≠ 原位 %s" % [now, _home])
			else:
				print("  ok  震屏後 Arena 回到原位 %s" % now)
			_check_shadows("震屏後")
			_battle.call("_lunge", "enemy")
			_step = 3
			_wait = 0
		3:
			if _wait == 6:
				_check_shadows("Boss 突進中")
			if _wait < 30:
				return false
			_check_shadows("Boss 突進後")
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_SHADOW_ANCHOR_OK")
	quit(0 if _ok else 1)
	return true
