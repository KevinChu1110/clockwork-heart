extends SceneTree

func _init() -> void:
	var parent := TextureRect.new()
	var child := TextureRect.new()
	child.show_behind_parent = true
	parent.add_child(child)
	print("child.show_behind_parent: ", child.show_behind_parent)
	quit()
