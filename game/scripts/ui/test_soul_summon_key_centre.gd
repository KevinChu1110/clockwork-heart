extends SceneTree
## #103：抽魂召喚演出中，發條主鑰匙要一直在光環中心，不能壓到標題；貼圖只取鑰匙本體（不帶切圖殘片）。
## 整段演出（開場、蓄力、爆發）每一幀都檢查。

const SoulSummonFx := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")

var _ok := true
var _frame := 0
var _fx: Control
var _done := false
var _checked := 0
var _max_off := 0.0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)
	_fx = SoulSummonFx.new()
	root.add_child(_fx)


func _process(_d: float) -> bool:
	_frame += 1
	if _frame < 3:
		return false
	if _frame == 3:
		var key: TextureRect = _fx.get("_windup_key")
		if key.size.x > SoulSummonFx.KEY_BOX + 0.5 or key.size.y > SoulSummonFx.KEY_BOX + 0.5:
			_fail("鑰匙 TextureRect 被撐成 %s（應為 %s）" % [str(key.size), str(SoulSummonFx.KEY_BOX)])
		var tex := key.texture
		if not (tex is AtlasTexture):
			_fail("鑰匙貼圖應只取本體區塊（AtlasTexture），實際 %s" % str(tex))
		_fx.call("play_summon", true, func(): _done = true)
		return false
	if _frame > 3 and not _done and _frame < 2000:
		_check_frame()
		return false
	if _checked < 30:
		_fail("只檢查到 %d 幀，演出太短或沒有播" % _checked)
	if _ok:
		print("  ok %d 幀鑰匙都在中心（最大偏移 %.1fpx），不壓標題" % [_checked, _max_off])
	print("TEST_SOUL_SUMMON_KEY_CENTRE_OK" if _ok else "TEST_SOUL_SUMMON_KEY_CENTRE_FAIL")
	quit(0 if _ok else 1)
	return true


func _check_frame() -> void:
	var key: TextureRect = _fx.get("_windup_key")
	if not key.visible or key.modulate.a < 0.05:
		return
	_checked += 1
	var centre: Vector2 = (_fx.get("_center_node") as Control).get_global_transform().origin
	var xf := key.get_global_transform()
	var key_centre := xf * (key.size * 0.5)
	var off := key_centre.distance_to(centre)
	_max_off = maxf(_max_off, off)
	if off > 4.0:
		_fail("第 %d 幀鑰匙中心 %s 離光環中心 %s 有 %.0fpx" % [_frame, str(key_centre), str(centre), off])
		_done = true
		return
	## 鑰匙圖案實際範圍：box 內保持比例置中
	var tex_sz: Vector2 = key.texture.get_size()
	var k := minf(key.size.x / tex_sz.x, key.size.y / tex_sz.y)
	var half := tex_sz * k * 0.5
	var top := INF
	for c in [Vector2(-half.x, -half.y), Vector2(half.x, -half.y), Vector2(-half.x, half.y), Vector2(half.x, half.y)]:
		top = minf(top, (xf * (key.size * 0.5 + c)).y)
	var title: Control = _fx.get("_title_hint")
	var title_bottom := title.get_global_rect().end.y
	if top < title_bottom:
		_fail("第 %d 幀鑰匙頂端 y=%.0f 壓到標題（標題底 y=%.0f）" % [_frame, top, title_bottom])
		_done = true
