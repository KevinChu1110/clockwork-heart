extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)
	
	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)
	
	var lobby = MobileLobby.new()
	root.add_child(lobby)

var _frames := 0
func _process(_delta: float) -> bool:
	_frames += 1
	if _frames == 5:
		var lobby: Control = null
		for c in root.get_children():
			if c is MobileLobby:
				lobby = c
				break
		var eq: Control = lobby.get("_equip_schematic")
		print("BEFORE clip_text:")
		print("EquipSchematic size:", eq.size, " global_pos:", eq.global_position)
		for c in eq.get_children():
			if c is Button:
				c.clip_text = true
		eq.queue_sort()
	elif _frames == 10:
		var lobby: Control = null
		for c in root.get_children():
			if c is MobileLobby:
				lobby = c
				break
		var eq: Control = lobby.get("_equip_schematic")
		print("AFTER clip_text:")
		print("EquipSchematic size:", eq.size, " global_pos:", eq.global_position)
		for c in eq.get_children():
			if c is Control:
				print("Child ", c.name, " size:", c.size, " global_pos:", c.global_position, " custom_min_size:", c.custom_minimum_size)
		quit(0)
		return true
	return false
