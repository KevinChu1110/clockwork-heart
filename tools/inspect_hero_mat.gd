extends SceneTree

func _initialize() -> void:
	var ml_cls = load("res://scripts/ui/mobile_lobby.gd")
	var lobby = ml_cls.new()
	root.add_child(lobby)
	for i in range(5):
		await process_frame

	var hero := lobby.find_child("HeroAvatar", true, false) as TextureRect
	print("HeroAvatar:", hero)
	if hero:
		print("Material:", hero.material)
		if hero.material is ShaderMaterial:
			var sm: ShaderMaterial = hero.material
			print("Shader:", sm.shader.resource_path if sm.shader else "null")
			print("rim_enabled:", sm.get_shader_parameter("rim_enabled"))
			print("rim_color:", sm.get_shader_parameter("rim_color"))
			print("rim_intensity:", sm.get_shader_parameter("rim_intensity"))
			print("rim_width:", sm.get_shader_parameter("rim_width"))
			print("rim_direction:", sm.get_shader_parameter("rim_direction"))
			print("outline_color:", sm.get_shader_parameter("outline_color"))
			print("outline_width:", sm.get_shader_parameter("outline_width"))
			print("outline_enabled:", sm.get_shader_parameter("outline_enabled"))
	quit(0)
