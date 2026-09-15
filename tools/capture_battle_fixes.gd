extends SceneTree

var _step := 0
var _wait := 0
var _main: Node = null
var _out_dir := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9e1b0b57/repo/screenshots/battle_qa_fixed"

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	DirAccess.make_dir_recursive_absolute(_out_dir)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 40:
				_main = current_scene
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "rabbit")
				print("CAPTURE: Step 1 -> Rabbit battle (road_bandit)")
				_main.call("proof_show_battle", "road_bandit")
				_step = 1
				_wait = 0
		1:
			if _wait >= 65:
				_save_viewport("%s/proof_rabbit_fixed.png" % _out_dir)
				print("CAPTURE: Rabbit battle screenshot saved.")
				var gs: Node = root.get_node_or_null("GameState")
				if gs:
					gs.call("reset_new_game", "lion")
				print("CAPTURE: Step 2 -> Lion battle (black_ronin)")
				_main.call("proof_show_battle", "black_ronin")
				_step = 2
				_wait = 0
		2:
			if _wait >= 65:
				print("=== SEARCHING NODES FOR '烈鬃獅' ===")
				_find_text_nodes(root, "烈鬃獅")
				print("=== SEARCHING NODES FOR '黑鏽浪人' ===")
				_find_text_nodes(root, "黑鏽浪人")
				_save_viewport("%s/proof_lion_fixed.png" % _out_dir)
				print("CAPTURE: Lion battle screenshot saved.")
				print("CAPTURE_ALL_COMPLETE")
				quit(0)
				return true
	return false

func _find_text_nodes(n: Node, query: String) -> void:
	if "text" in n and query in str(n.text):
		var gpos = n.global_position if n is Control else "N/A"
		var vis = n.is_visible_in_tree() if n is CanvasItem else "N/A"
		var z = n.z_index if n is CanvasItem else "N/A"
		print("  NODE: %s | class=%s | text='%s' | gpos=%s | vis=%s | z=%s" % [
			n.get_path(), n.get_class(), n.text, gpos, vis, z
		])
	for c in n.get_children():
		_find_text_nodes(c, query)

func _save_viewport(path: String) -> void:
	var vp := root.get_viewport()
	if vp:
		var img := vp.get_texture().get_image()
		if img:
			img.save_png(path)
			print("  [OK] Saved image to ", path)
