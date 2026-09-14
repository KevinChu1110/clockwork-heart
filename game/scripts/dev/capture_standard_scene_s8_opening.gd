extends SceneTree
## §8 標準場開場 S1 (shot_01.png) 實機截圖產生器

var _elapsed: float = 0.0
var _step: int = 0
var _step_timer: float = 0.0
var _main: Node = null
var _target_path: String = ""

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	Engine.max_fps = 30

	var base := ProjectSettings.globalize_path("res://")
	_target_path = base.path_join("../proofs/standard_scene_s8/shot_01.png")

	change_scene_to_file("res://scenes/main.tscn")

func _process(delta: float) -> bool:
	_elapsed += delta
	_step_timer += delta

	match _step:
		0:
			if current_scene != null and current_scene.has_method("proof_jump_explore"):
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game")
					gs.set("player_race", "rabbit")
					gs.set("player_name", "小白")
					gs.set("level", 12)
					gs.set("gold", 1200)
					gs.set("weapon_name", "微末之刃")
					gs.set("weapon_tier", 2)
					gs.set("weapon_atk", 45)
					gs.set("hp", 200)
					gs.set("max_hp", 200)
					gs.set("energy", 15)
					gs.set("paperdoll_slots", {
						"race": "rabbit",
						"costume": "costume_nutcracker_guard",
						"chassis": "paint_ivory_stock",
						"costume_id": "costume_nutcracker_guard",
						"paint_id": "paint_ivory_stock"
					})
					gs.call("set_flag", "tut_done", true)
					gs.call("set_flag", "c1_entered_city", true)
				var es: Node = root.get_node_or_null("EnergySystem")
				if es and es.has_method("grant"):
					es.call("grant", 15)

				_main.call("proof_jump_explore", "village")

				if _step_timer >= 0.5:
					_step = 1
					_step_timer = 0.0
					print("[S8_SCENE] S1: 探索開始 (village, t=%.2fs)" % _elapsed)
					var exp_v: Node = _main.get("_explore") if _main else null
					if exp_v and exp_v.has_method("_start_tap_move"):
						var cur_pos: Vector2 = exp_v.get("player_pos")
						exp_v.call("_start_tap_move", cur_pos + Vector2(220, 0))

		1:
			var exp_v: Node = _main.get("_explore") if _main else null
			if exp_v:
				if _step_timer >= 2.4 and _step_timer < 4.2:
					var pbody = exp_v.get("_player")
					if pbody and is_instance_valid(pbody):
						var breathe := sin(_step_timer * 4.0) * 0.03
						pbody.scale = Vector2(1.0 + breathe, 1.0 - breathe)

			if _step_timer >= 3.2:
				_step = 2
				_do_capture()

	return false

func _do_capture() -> void:
	await RenderingServer.frame_post_draw
	var vp := root.get_viewport()
	if vp:
		var img := vp.get_texture().get_image()
		if img and not img.is_empty():
			img.save_png(_target_path)
			print("[S8_SCENE] SAVED shot_01.png to %s" % _target_path)
			quit(0)
