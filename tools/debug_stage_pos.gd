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
		var st: Control = lobby.get("_stage_anchor")
		print("stage_anchor position:", st.position, " global_pos:", st.global_position, " offset_top:", st.offset_top, " anchor_top:", st.anchor_top)
		var av: Control = lobby.get("_hero_avatar")
		print("hero_avatar position:", av.position, " global_pos:", av.global_position, " size:", av.size)
		quit(0)
		return true
	return false
