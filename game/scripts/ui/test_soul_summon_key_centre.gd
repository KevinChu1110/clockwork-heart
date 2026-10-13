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
## QA 回報雜點的幀（演出開始後第 25、40 幀）
const STRAY_FRAMES := [25, 40]
var _stray_checked := 0


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
		if key.texture == null:
			_fail("鑰匙沒有貼圖")
		_fx.call("play_summon", true, func(): _done = true)
		return false
	if _frame > 3 and not _done and _frame < 2000:
		_check_frame()
		return false
	if _stray_checked < STRAY_FRAMES.size():
		_fail("雜點檢查只跑了 %d／%d 幀" % [_stray_checked, STRAY_FRAMES.size()])
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
	if _frame - 3 in STRAY_FRAMES:
		_check_stray(key, _frame - 3)
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


## 鑰匙當下畫出來的貼圖：所有不透明像素都要跟鑰匙本體相連（不能有會跟著轉的碎片），
## 而且最外圈一圈是透明的（濾波取樣不會把框外的深色像素帶進來）。
func _check_stray(key: TextureRect, at: int) -> void:
	_stray_checked += 1
	var img := key.texture.get_image()
	if img.is_compressed():
		img.decompress()
	img.convert(Image.FORMAT_RGBA8)
	var w := img.get_width()
	var h := img.get_height()
	var border := 0
	for x in w:
		if img.get_pixel(x, 0).a > 0.0 or img.get_pixel(x, h - 1).a > 0.0:
			border += 1
	for y in h:
		if img.get_pixel(0, y).a > 0.0 or img.get_pixel(w - 1, y).a > 0.0:
			border += 1
	if border > 0:
		_fail("第 %d 幀：鑰匙貼圖邊緣有 %d 個不透明像素（會被濾波帶出深色邊）" % [at, border])
	var seen := PackedByteArray()
	seen.resize(w * h)
	var comps: Array[int] = []
	for y in h:
		for x in w:
			if seen[y * w + x] != 0 or img.get_pixel(x, y).a <= 0.0:
				continue
			seen[y * w + x] = 1
			var stack: Array[int] = [y * w + x]
			var n := 0
			while not stack.is_empty():
				var c: int = stack.pop_back()
				n += 1
				for d in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
					var dx: int = d.x
					var dy: int = d.y
					var nx := c % w + dx
					var ny := c / w + dy
					if nx < 0 or ny < 0 or nx >= w or ny >= h:
						continue
					var j := ny * w + nx
					if seen[j] == 0 and img.get_pixel(nx, ny).a > 0.0:
						seen[j] = 1
						stack.append(j)
			comps.append(n)
	comps.sort()
	if comps.size() > 1:
		var stray := 0
		for k in comps.size() - 1:
			stray += comps[k]
		_fail("第 %d 幀：鑰匙旁有 %d 塊不相連碎片共 %d px（會跟著鑰匙轉的雜點）" % [at, comps.size() - 1, stray])
	else:
		print("  ok 第 %d 幀鑰匙貼圖只有本體一塊、四周透明，無雜點" % at)
