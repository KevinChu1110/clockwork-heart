extends SceneTree

var _frame := 0
var _view: Control

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var view_script = load("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
	_view = view_script.new()
	_view.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(_view)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 2:
		print("Frame 2 - View size: ", _view.size)
		var fx = _view.get_node_or_null("SoulSummonFx")
		if fx:
			print("SoulSummonFx size: ", fx.size, " pos: ", fx.position)
			var skip = fx.get_node_or_null("Button") # _skip_btn
			for c in fx.get_children():
				if c is Button:
					print("Skip btn pos: ", c.position, " size: ", c.size, " global_pos: ", c.global_position)
		var ten = _view.get_node_or_null("SoulTenPullView")
		if ten:
			print("SoulTenPullView size: ", ten.size, " pos: ", ten.position)
			for c in ten.get_children():
				if c is HBoxContainer:
					print("HBoxContainer pos: ", c.position, " size: ", c.size, " global_pos: ", c.global_position)
		quit(0)
		return true
	return false
