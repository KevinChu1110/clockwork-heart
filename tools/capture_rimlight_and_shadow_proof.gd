extends SceneTree
## 截取大廳與戰鬥場景之角色動態光影與雙層接地陰影驗證圖

var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null
var _lobby: Control = null

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	
	if not root.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root.add_child(gf)

	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 25:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			if _main == null or gs == null:
				quit(1)
				return true
			gs.call("reset_new_game")
			gs.set("player_name", "小白")
			gs.set("player_race", "rabbit")
			
			# 1. 截取大廳實機圖
			var ml_cls = load("res://scripts/ui/mobile_lobby.gd")
			_lobby = ml_cls.new()
			_lobby.name = "ProofLobby"
			root.add_child(_lobby)
			_step = 1
			_wait = 0
		1:
			if _wait < 35:
				return false
			var img: Image = root.get_texture().get_image()
			if img == null:
				var vp := root.get_viewport()
				if vp and vp.get_texture():
					img = vp.get_texture().get_image()
			if img != null:
				img.save_png("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_lobby_rimlight_shadow.png")
				img.save_png("/opt/side/bravesoul-game/proofs/t_5b8dc14c/proof_lobby_rimlight_shadow.png")
				print("CAPTURE_LOBBY_DONE")
			else:
				push_error("LOBBY_IMAGE_NULL")
			
			if _lobby:
				_lobby.queue_free()
				_lobby = null
			
			# 2. 開啟戰鬥場景 (巨偶停擺戰)
			_main.call("_start_battle_raw", "colossus_lion")
			_step = 2
			_wait = 0
		2:
			if _wait < 40:
				return false
			var host: Control = _main.get("host") as Control
			if host and host.get_child_count() > 0:
				_battle = host.get_child(0) as Control
			if _battle == null or not is_instance_valid(_battle):
				quit(1)
				return true
			var sim = _battle.get("sim")
			if sim:
				sim.sim_paused = true
			_battle.call("_refresh_hud")
			_step = 3
			_wait = 0
		3:
			if _wait < 30:
				return false
			var img: Image = root.get_texture().get_image()
			if img == null:
				var vp := root.get_viewport()
				if vp and vp.get_texture():
					img = vp.get_texture().get_image()
			if img != null:
				img.save_png("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_5b8dc14c/proofs/proof_battle_rimlight_shadow.png")
				img.save_png("/opt/side/bravesoul-game/proofs/t_5b8dc14c/proof_battle_rimlight_shadow.png")
				print("CAPTURE_BATTLE_DONE")
			else:
				push_error("BATTLE_IMAGE_NULL")
			print("ALL_PROOFS_CAPTURED_OK")
			quit(0)
			return true
	return false
