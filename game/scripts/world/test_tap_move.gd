extends SceneTree
## godot --headless -s res://scripts/world/test_tap_move.gd
## 點擊移動哨兵：尋路建得起來、跟路走得到、點實體會走過去並互動。


func _initialize() -> void:
	var ok := true
	var Ex = load("res://scripts/world/explore_view.gd")
	if Ex == null:
		push_error("no explore")
		quit(1)
		return
	var ex = Ex.new()
	root.add_child(ex)
	ex.setup("town")

	if ex._astar == null:
		push_error("astar not built")
		quit(1)
		return
	print("astar built OK")

	## 1) 找一個離出生點夠遠、可達的可走格，規劃過去
	var spawn_cell: Vector2i = ex._world_to_cell(ex.player_pos + ex.FOOT_OFFSET)
	var target_cell := Vector2i(-1, -1)
	var best_d := 0
	for y in ex._map_rows:
		if best_d >= 30:
			break
		for x in ex._map_cols:
			var c := Vector2i(x, y)
			if ex._is_solid_cell(c):
				continue
			var d: int = absi(c.x - spawn_cell.x) + absi(c.y - spawn_cell.y)
			if d <= best_d or d < 8:
				continue
			var cells: Array[Vector2i] = ex._astar.get_id_path(spawn_cell, c)
			if cells.size() >= 2:
				best_d = d
				target_cell = c
	if target_cell.x < 0:
		push_error("no reachable far cell")
		ok = false
	else:
		var target_pos: Vector2 = ex._cell_to_stand_pos(target_cell)
		## 點擊點是「地面上的點」（格心），不是玩家站位左上角
		if not ex._start_tap_move(target_pos + ex.FOOT_OFFSET):
			push_error("tap move refused")
			ok = false
		elif ex._path.is_empty():
			push_error("no path produced")
			ok = false
		else:
			print("path len ", ex._path.size(), " OK")
			var steps := 0
			while not ex._path.is_empty() and steps < 6000:
				ex._follow_path(1.0 / 60.0)
				steps += 1
			if not ex._path.is_empty():
				push_error("path not finished in %d steps" % steps)
				ok = false
			elif ex.player_pos.distance_to(target_pos) > 48.0:
				push_error("stopped far from target: %s vs %s" % [ex.player_pos, target_pos])
				ok = false
			else:
				print("walk arrive OK (", steps, " steps)")

	## 2) 點實體：應該走過去並發 interacted
	var hits: Array = []
	ex.interacted.connect(func(id: String) -> void: hits.append(id))
	## 挑離玩家最近的實體，最不容易搆不到
	var pick: Dictionary = {}
	var pick_d := INF
	for e in ex._entities:
		var ec: Vector2 = e.pos + e.size * 0.5
		var d2: float = (ex.player_pos + ex.PLAYER_SIZE * 0.5).distance_to(ec)
		if d2 < pick_d:
			pick_d = d2
			pick = e
	if pick.is_empty():
		push_error("no entities on map")
		ok = false
	else:
		var ec2: Vector2 = pick.pos + pick.size * 0.5
		ex._on_tap(ec2)
		var steps2 := 0
		while not ex._path.is_empty() and steps2 < 6000:
			ex._follow_path(1.0 / 60.0)
			steps2 += 1
		if hits.is_empty():
			push_error("tap entity did not interact (target=%s)" % str(pick.get("id", "?")))
			ok = false
		else:
			print("tap interact OK -> ", hits[0])

	## 3) 凍結時收指令：不能留殘路徑
	ex._start_tap_move(ex.player_pos + Vector2(96, 0))
	ex.set_frozen(true)
	if not ex._path.is_empty() or ex._tap_interact_id != "":
		push_error("frozen should clear path")
		ok = false
	else:
		print("frozen clears OK")

	if ok:
		print("TAP_MOVE_OK")
		quit(0)
	else:
		print("TAP_MOVE_FAIL")
		quit(1)
