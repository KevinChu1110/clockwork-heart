extends SceneTree
## 《發條之心》五族走動四幀與待機姿態無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_race_walk_idle.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始五族 walk 四幀與 idle 待機素體無頭驗證 ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("無法取得 GameState 單例")
		_finish(false)
		return

	var races := ["rabbit", "lion", "fox", "boar", "macaque"]

	# 1. 取得兔族基準素材
	gs.set("player_race", "rabbit")
	if "paperdoll_slots" in gs:
		gs.paperdoll_slots = {}

	var rabbit_idle: Texture2D = SpriteDB.player_idle()
	if rabbit_idle == null:
		push_error("無法載入兔族 player_idle")
		ok = false
	else:
		print("  ✓ 兔族基準 idle 載入成功: %s" % rabbit_idle.resource_path)

	var rabbit_walks: Array[Texture2D] = []
	for f in range(4):
		var w: Texture2D = SpriteDB.player_walk(f)
		if w == null:
			push_error("無法載入兔族 player_walk(%d)" % f)
			ok = false
		else:
			print("  ✓ 兔族基準 walk(%d) 載入成功: %s" % [f, w.resource_path])
		rabbit_walks.append(w)

	# 2. 依序測試五族 walk 0..3 與 idle
	for r in races:
		print("\n--- 驗證種族: %s ---" % r)
		gs.set("player_race", r)
		if "paperdoll_slots" in gs:
			gs.paperdoll_slots = {}

		var cur_r := SpriteDB.player_race()
		if cur_r != r:
			push_error("SpriteDB.player_race() 預期 %s，取得 %s" % [r, cur_r])
			ok = false
		else:
			print("  ✓ SpriteDB.player_race() == %s" % cur_r)

		# 檢驗 idle
		var idle: Texture2D = SpriteDB.player_idle()
		if idle == null:
			push_error("種族 %s 之 player_idle() 為 null" % r)
			ok = false
		else:
			var idle_path := idle.resource_path
			print("  ✓ 種族 %s 之 player_idle(): %s" % [r, idle_path])
			if r == "rabbit":
				if idle != rabbit_idle:
					push_error("兔族 player_idle() 應為 rabbit_idle")
					ok = false
				if not idle_path.ends_with("rabbit_idle_x3.png"):
					push_error("兔族 player_idle() 路徑應為 rabbit_idle_x3.png")
					ok = false
			else:
				if idle == rabbit_idle:
					push_error("非兔族 (%s) 之 player_idle() 不應等於兔族 idle 貼圖" % r)
					ok = false
				if idle_path.contains("rabbit"):
					push_error("非兔族 (%s) 之 player_idle() 載到兔族貼圖: %s" % [r, idle_path])
					ok = false
				if not idle_path.contains(r):
					push_error("非兔族 (%s) 之 player_idle() 路徑應包含種族名稱: %s" % [r, idle_path])
					ok = false

		# 檢驗 walk 0..3
		for f in range(4):
			var walk: Texture2D = SpriteDB.player_walk(f)
			if walk == null:
				push_error("種族 %s 之 player_walk(%d) 為 null" % [r, f])
				ok = false
			else:
				var walk_path := walk.resource_path
				print("  ✓ 種族 %s 之 player_walk(%d): %s" % [r, f, walk_path])
				if r == "rabbit":
					if walk != rabbit_walks[f]:
						push_error("兔族 player_walk(%d) 應為 rabbit_walks[%d]" % [f, f])
						ok = false
					if not walk_path.ends_with("rabbit_walk_%d_x3.png" % f):
						push_error("兔族 player_walk(%d) 路徑應為 rabbit_walk_%d_x3.png" % [f, f])
						ok = false
				else:
					if walk == rabbit_walks[f]:
						push_error("非兔族 (%s) 之 player_walk(%d) 不應等於兔族 walk 貼圖" % [r, f])
						ok = false
					if walk_path.contains("rabbit"):
						push_error("非兔族 (%s) 之 player_walk(%d) 載到兔族貼圖: %s" % [r, f, walk_path])
						ok = false
					var expected_suffix := "%s_walk_%d_x3.png" % [r, f]
					if not walk_path.ends_with(expected_suffix):
						push_error("非兔族 (%s) 之 player_walk(%d) 路徑應以 %s 結尾: %s" % [r, f, expected_suffix, walk_path])
						ok = false

	# 3. 驗證未知種族 fallback 機制
	print("\n--- 驗證未知種族 fallback 兔步 ---")
	gs.set("player_race", "unknown_beast")
	for f in range(4):
		var fb_walk: Texture2D = SpriteDB.player_walk(f)
		if fb_walk == null:
			push_error("未知種族 player_walk(%d) fallback 為 null" % f)
			ok = false
		elif fb_walk != rabbit_walks[f]:
			push_error("未知種族 player_walk(%d) 未正確 fallback 到兔步" % f)
			ok = false
		else:
			print("  ✓ 未知種族 player_walk(%d) 正確 fallback 至兔步: %s" % [f, fb_walk.resource_path])

	# 復原回兔族
	gs.set("player_race", "rabbit")

	_finish(ok)

func _finish(ok: bool) -> void:
	if ok:
		print("\nRACE_WALK_IDLE_OK")
		quit(0)
	else:
		push_error("\nRACE_WALK_IDLE_FAIL")
		quit(1)
