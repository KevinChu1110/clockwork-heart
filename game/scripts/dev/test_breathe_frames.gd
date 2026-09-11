extends SceneTree

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var Host = load("res://scripts/world/explore_host.gd")
	var host = Host.new()
	root.add_child(host)
	host.setup("village")

var _f: int = 0

func _process(delta: float) -> bool:
	_f += 1
	var host = root.get_child(root.get_child_count() - 1)
	var p = host.call("get_player") if host and host.has_method("get_player") else null
	if p:
		var b = p.get("body")
		if b and _f % 10 == 0:
			print("Frame %d (time ~%.2fs): scale=%s" % [_f, _f * delta, b.scale])
	if _f >= 180:
		quit(0)
		return true
	return false
