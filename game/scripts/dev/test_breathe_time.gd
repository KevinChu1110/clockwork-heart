extends SceneTree

var _host: Control = null
var _p: CharacterBody2D = null
var _time: float = 0.0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var Host = load("res://scripts/world/explore_host.gd")
	_host = Host.new()
	root.add_child(_host)
	_host.setup("village")

func _process(delta: float) -> bool:
	_time += delta
	if _p == null:
		_p = _host.call("get_player")
	if _p:
		var b = _p.get("body")
		if b:
			print("Time: %.3fs, scale: %s" % [_time, b.scale])
	if _time >= 2.4:
		quit(0)
		return true
	return false
