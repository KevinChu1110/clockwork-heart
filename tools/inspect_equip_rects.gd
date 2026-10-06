extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

var _vp_sizes: Array[Vector2i] = [Vector2i(1280, 720), Vector2i(1600, 720)]
var _idx: int = 0
var _frames: int = 0
var _lobby: Control = null

func _initialize() -> void:
	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.reset_new_game()
		gs.player_name = "測試白兔"
		gs.player_race = "rabbit"

	_setup_current()

func _setup_current() -> void:
	var vp_size: Vector2i = _vp_sizes[_idx]
	root.size = vp_size
	var win := root.get_window()
	if win != null:
		win.size = vp_size

	if _lobby:
		_lobby.free()

	_lobby = MobileLobby.new()
	root.add_child(_lobby)
	_frames = 0

func _process(_delta: float) -> bool:
	_frames += 1
	if _frames == 8:
		var vp_size: Vector2i = _vp_sizes[_idx]
		var eq: Control = _lobby.get("_equip_schematic") as Control
		print("\n=== Viewport: ", vp_size, " ===")
		if eq == null:
			print("EquipSchematic is null!")
		else:
			print("EquipSchematic global_pos: ", eq.global_position, " size: ", eq.size, " end: ", eq.global_position + eq.size)
			for c in eq.get_children():
				if c is Control:
					var r: Rect2 = Rect2(c.global_position, c.size)
					var in_vp: bool = (r.position.x >= 0.0 and r.position.y >= 0.0 and r.end.x <= float(vp_size.x) and r.end.y <= float(vp_size.y))
					var margin_right: float = float(vp_size.x) - r.end.x
					var margin_left: float = r.position.x
					var margin_top: float = r.position.y
					var margin_bottom: float = float(vp_size.y) - r.end.y
					print("  Child ", c.name, ": rect=", r, " | in_vp=", in_vp, " | margins: L=", margin_left, " R=", margin_right, " T=", margin_top, " B=", margin_bottom)

		_idx += 1
		if _idx < _vp_sizes.size():
			_setup_current()
			return false
		else:
			quit(0)
			return true
	return false
