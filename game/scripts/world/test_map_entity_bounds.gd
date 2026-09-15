extends SceneTree
## 檢查全地圖實體座標防呆：
## godot --headless -s res://scripts/world/test_map_entity_bounds.gd
##
## 掃描 MapCatalog 所有地圖的所有實體，
## 斷言任何實體座標不得超出地板矩形左緣/上緣（pos.x >= origin.x 且 pos.y >= origin.y）。

const MapCatalog = preload("res://scripts/world/map_catalog.gd")

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

	var total_checked := 0
	for id in ids:
		var data: Dictionary = MapCatalog.build(id)
		var origin: Vector2 = data.get("origin", Vector2(40, 80))
		var entities: Array = data.get("entities", [])
		for e in entities:
			if typeof(e) != TYPE_DICTIONARY:
				continue
			var eid: String = str(e.get("id", ""))
			var pos: Vector2 = e.get("pos", Vector2.ZERO) as Vector2
			if pos.x < origin.x or pos.y < origin.y:
				_fail("%s 實體 %s 座標 (%s) 小於 origin (%s)，浮出地板上緣/左緣" % [
					id, eid, str(pos), str(origin)
				])
			total_checked += 1

	if total_checked < 50:
		_fail("檢查實體總數過少 (%d)，可能 catalog 遍歷未完全" % total_checked)
	else:
		print("  ok checked %d entities across %d maps" % [total_checked, ids.size()])

	_finish()


func _finish() -> void:
	if _ok:
		print("MAP_ENTITY_BOUNDS_OK")
		quit(0)
	else:
		print("MAP_ENTITY_BOUNDS_FAIL")
		quit(1)
