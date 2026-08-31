extends SceneTree
## godot --headless -s res://scripts/world/test_objective.gd
## 主線指引哨兵：「下一站」隨旗標推進、秘境不擋主線、全清有收尾語。

func _initialize() -> void:
	var ok := true
	## 不能 preload：region_catalog 引用 GameState autoload，
	## -s 模式 preload 時 autoload 尚未註冊會編譯失敗；runtime load 才行
	var RegionCatalog = load("res://scripts/world/region_catalog.gd")
	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("GameState missing")
		quit(1)
		return
	gs.reset_new_game()

	## 1) 新局：指向關卡 1
	var o1: Dictionary = RegionCatalog.next_objective()
	if o1.is_empty() or str(o1.get("id", "")) != "r1_s1":
		push_error("fresh game should point to r1_s1, got %s" % str(o1.get("id", "?")))
		ok = false
	else:
		print("fresh objective OK ", RegionCatalog.next_objective_line())

	## 2) 通過首戰：指向雷歐
	gs.set_flag("c0_first_battle", true)
	var o2: Dictionary = RegionCatalog.next_objective()
	if str(o2.get("id", "")) != "r1_s2":
		push_error("after c0 should point to r1_s2, got %s" % str(o2.get("id", "?")))
		ok = false
	else:
		print("leo objective OK")

	## 3) 清雷歐：指向白霧主線關（r2_s1），秘境 r2_s2 不插隊
	gs.set_flag("boss.leo_cleared", true)
	var o3: Dictionary = RegionCatalog.next_objective()
	if str(o3.get("id", "")) != "r2_s1":
		push_error("after leo should point to r2_s1, got %s" % str(o3.get("id", "?")))
		ok = false
	else:
		print("fog objective OK")

	## 4) 主線全清：收尾語或指向秘境備選，但不能空字串
	for f in ["boss.white_fog_cleared", "boss.abo_cleared", "boss.shadowwind_cleared",
			"boss.stonefist_cleared", "boss.demon_cleared"]:
		gs.set_flag(f, true)
	var line: String = RegionCatalog.next_objective_line()
	if line.strip_edges() == "":
		push_error("endgame objective line should not be empty")
		ok = false
	else:
		print("endgame line OK: ", line)

	## 4b) 每一關的「前往」都指向真的存在的地圖；魔王那關要開塔下營地，
	##     不是疤地（魔王在塔裡，疤地那張圖上根本沒有塔門）
	var WorldTravel = load("res://scripts/world/world_travel.gd")
	var map_ids: PackedStringArray = WorldTravel.list_map_ids()
	for r in RegionCatalog.regions():
		for s in r.get("stages", []):
			var goto: Dictionary = s.get("goto", {})
			var mid := str(goto.get("map", ""))
			if not (mid in map_ids):
				push_error("stage %s goto map %s not in list_map_ids" % [str(s.get("id", "")), mid])
				ok = false
			if str(s.get("id", "")) == "r4_s2" and mid != "tower_camp":
				push_error("r4_s2（魔王）goto 應為 tower_camp，得 %s" % mid)
				ok = false
	if ok:
		print("stage goto maps OK")

	## 5) 一鍵領取：沒完成的委託 → 明確回報不可領
	var qs = root.get_node_or_null("QuestSystem")
	if qs != null:
		var r: Dictionary = qs.claim_all_ready()
		if bool(r.get("ok", false)) and int(r.get("n", 0)) == 0:
			push_error("claim_all_ready with nothing done should be ok=false")
			ok = false
		else:
			print("claim_all empty OK: ", r.get("msg"))

	if ok:
		print("OBJECTIVE_OK")
		quit(0)
	else:
		print("OBJECTIVE_FAIL")
		quit(1)
