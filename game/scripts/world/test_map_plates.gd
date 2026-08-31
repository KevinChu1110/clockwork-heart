extends SceneTree
## 探索底圖規格：godot --headless -s res://scripts/world/test_map_plates.gd
##
## 走跟遊戲同一條查找：MapCatalog.build(id).art → SpriteDB.map_bg(art)。
## 斷言每張（tower_memory 豁免）原生像素 ≥ 該圖世界尺寸，且寬高比 ≈ 16:9。
## 不寫死某一對像素。


const MapCatalog = preload("res://scripts/world/map_catalog.gd")

const EXEMPT: PackedStringArray = ["tower_memory"]
## 高處主題：圖緣可以有霧，不當天空帶。
const SKY_EXEMPT: PackedStringArray = ["tower_memory", "dojo_peak", "mist_cliff"]
const ASPECT := 16.0 / 9.0
const ASPECT_SLACK := 0.05


var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	var ids: PackedStringArray = MapCatalog.ids()
	if ids.is_empty():
		_fail("MapCatalog.ids() 是空的")
		return _finish()

	var checked := 0
	for id in ids:
		var data: Dictionary = MapCatalog.build(id)
		var art := str(data.get("art", id))
		if art in EXEMPT:
			print("  skip exempt ", id, " art=", art)
			continue
		var world: Vector2 = data.get("size", Vector2.ZERO)
		if world.x < 8.0 or world.y < 8.0:
			_fail("%s 世界尺寸不合理 %s" % [id, str(world)])
			continue
		var tex: Texture2D = SpriteDB.map_bg(art)
		if tex == null:
			_fail("%s art=%s SpriteDB.map_bg 回 null" % [id, art])
			continue
		var tw := float(tex.get_width())
		var th := float(tex.get_height())
		if tw + 0.5 < world.x or th + 0.5 < world.y:
			_fail("%s art=%s 貼圖 %dx%d 小於世界 %.0fx%.0f（硬拉小圖）" % [
				id, art, int(tw), int(th), world.x, world.y
			])
			continue
		var asp := tw / th if th > 0.0 else 0.0
		if absf(asp - ASPECT) / ASPECT > ASPECT_SLACK:
			_fail("%s art=%s 寬高比 %.3f，要 16:9（%.3f ±%.0f%%）" % [
				id, art, asp, ASPECT, ASPECT_SLACK * 100.0
			])
			continue
		if art not in SKY_EXEMPT and _has_sky_band(tex):
			_fail("%s art=%s 頂部仍是天空／地平線帶（地面必須鋪滿畫布）" % [id, art])
			continue
		checked += 1
		print("  ok ", id, " art=", art, " tex=", int(tw), "x", int(th), " world=", world)
	if checked < 10:
		_fail("只通過 %d 張，查找路徑可能沒真的跑到 catalog" % checked)
	else:
		print("  ok plates %d" % checked)
	_finish()


func _has_sky_band(tex: Texture2D) -> bool:
	## 抽頂部 12%：又亮又淡、而且比畫面中段明顯更亮 = 天空帶。
	## 走 SpriteDB 回傳的同一張 Texture2D，不另開檔。
	var img: Image = tex.get_image()
	if img == null:
		return false
	if img.is_compressed():
		var err := img.decompress()
		if err != OK:
			return false
	var w := img.get_width()
	var h := img.get_height()
	if w < 8 or h < 8:
		return false
	var top_h := maxi(2, int(h * 0.12))
	var mid_y0 := int(h * 0.40)
	var mid_y1 := int(h * 0.62)
	var top_l := 0.0
	var top_sat := 0.0
	var top_n := 0
	var mid_l := 0.0
	var mid_n := 0
	var tr_l := 0.0
	var tr_n := 0
	var step := maxi(4, w / 64)
	var tr_x0 := int(w * 0.65)
	for y in range(0, top_h, maxi(1, top_h / 6)):
		for x in range(0, w, step):
			var c := img.get_pixel(x, y)
			var mx := maxf(c.r, maxf(c.g, c.b))
			var mn := minf(c.r, minf(c.g, c.b))
			var lum := 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b
			top_l += lum
			top_sat += (mx - mn) / (mx + 0.004)
			top_n += 1
			if x >= tr_x0:
				tr_l += lum
				tr_n += 1
	for y in range(mid_y0, mid_y1, maxi(1, (mid_y1 - mid_y0) / 5)):
		for x in range(0, w, step):
			var c2 := img.get_pixel(x, y)
			mid_l += 0.2126 * c2.r + 0.7152 * c2.g + 0.0722 * c2.b
			mid_n += 1
	if top_n == 0 or mid_n == 0:
		return false
	top_l /= float(top_n)
	top_sat /= float(top_n)
	mid_l /= float(mid_n)
	if tr_n > 0:
		tr_l /= float(tr_n)
	## 整張都淡（霧海／麥田）不算天空帶。
	if mid_l > 0.58:
		return false
	## 白天：頂部又淡又明顯亮於中段。
	var pale := top_l > 0.62 and top_sat < 0.32
	var brighter := top_l > mid_l + 0.12 and top_l > 0.48
	## 夜晚：頂部比地面中段明顯更暗，而且低飽和（星空帶；樹冠／屋瓦飽和較高）。
	var night := top_l < 0.38 and top_l < mid_l - 0.10 and top_sat < 0.32
	## 一角月／星空：頂帶整體偏暗，但右上明顯亮一塊。
	var moon := tr_n > 0 and top_l < 0.40 and tr_l > top_l + 0.08 and tr_l > 0.28
	return (pale and brighter) or night or moon


func _finish() -> void:
	if _ok:
		print("MAP_PLATES_OK")
		quit(0)
	else:
		print("MAP_PLATES_FAIL")
		quit(1)
