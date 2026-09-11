extends SceneTree

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var tests = [
		{"race": "rabbit", "wpn": "dawn_blade"},
		{"race": "lion", "wpn": "knight_pike"},
		{"race": "fox", "wpn": "star_rod"},
		{"race": "boar", "wpn": "anvil_hammer"},
		{"race": "macaque", "wpn": "hunt_claw"},
	]
	for t in tests:
		var p = PaperdollRenderer.resolve_slot_texture_path(t.race, "weapon", t.wpn)
		print(t.race, " (", t.wpn, ") -> ", p, " [exists: ", ResourceLoader.exists(p) or FileAccess.file_exists(p), "]")
	quit(0)
