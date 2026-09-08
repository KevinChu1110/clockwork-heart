extends SceneTree
## ART-02 程式配合：主城／C0 村關掉 TileMap 覆蓋，底圖走 LINEAR。
## godot --headless -s res://scripts/world/test_no_tile_overlay.gd


func _fail(ok: Array, msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	ok[0] = false


func _file_has(path: String, needle: String) -> bool:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return false
	return f.get_as_text().find(needle) >= 0


func _initialize() -> void:
	var ok := [true]
	root.size = Vector2i(1280, 720)

	for id in ["town", "village"]:
		var path := "res://scenes/maps/%s.tscn" % id
		var ps := load(path) as PackedScene
		if ps == null:
			_fail(ok, "load fail %s" % path)
			continue
		var n: Node = ps.instantiate()
		root.add_child(n)
		var tiles: Node = n.get_node_or_null("Tiles")
		if tiles == null:
			_fail(ok, "%s 沒有 Tiles 節點" % id)
		elif (tiles as CanvasItem).visible:
			_fail(ok, "%s Tiles 仍可見" % id)
		else:
			print("  ok %s Tiles hidden" % id)
		var ground: Node = n.get_node_or_null("Ground")
		if ground is CanvasItem:
			var filt: int = (ground as CanvasItem).texture_filter
			if filt != CanvasItem.TEXTURE_FILTER_LINEAR:
				_fail(ok, "%s Ground filter=%d 不是 LINEAR" % [id, filt])
			else:
				print("  ok %s Ground LINEAR" % id)
		else:
			_fail(ok, "%s 沒有 Ground Sprite" % id)
		n.free()

	if not _file_has("res://scripts/world/explore_view.gd", "NO_TILE_OVERLAY_ART"):
		_fail(ok, "explore_view.gd 缺 NO_TILE_OVERLAY_ART")
	elif not _file_has("res://scripts/world/explore_view.gd", "\"town\", \"village\""):
		_fail(ok, "explore_view.gd NO_TILE_OVERLAY_ART 沒含 town/village")
	else:
		print("  ok explore_view NO_TILE_OVERLAY_ART")

	if not _file_has("res://scripts/world/map_stage.gd", "NO_TILE_OVERLAY_ART"):
		_fail(ok, "map_stage.gd 缺 NO_TILE_OVERLAY_ART")
	else:
		print("  ok map_stage NO_TILE_OVERLAY_ART")

	if not _file_has("res://scripts/ui/mobile_lobby.gd", "TEXTURE_FILTER_LINEAR"):
		_fail(ok, "mobile_lobby 底圖不是 LINEAR")
	else:
		print("  ok lobby LINEAR")

	if ok[0]:
		print("NO_TILE_OVERLAY_OK")
		quit(0)
		return
	print("NO_TILE_OVERLAY_FAIL")
	quit(1)
