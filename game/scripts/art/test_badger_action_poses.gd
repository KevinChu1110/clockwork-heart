extends SceneTree
## 《發條之心》第四十六族破星蜜獾戰鬥六大動作姿態 (The Starbreaker Honey Badger Combat Action Poses) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_badger_action_poses.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始破星蜜獾族六大戰鬥姿態無頭驗證 (Badger Action Poses Test) ===")

	var poses := ["idle", "telegraph", "attack", "recover", "skill", "hit"]

	# 1. 驗證六大姿態檔案存在且尺寸為 128x128
	print("\n--- 1. 驗證檔案存在性與尺寸 (128x128) ---")
	for p in poses:
		var file_path := "res://assets/sprites/player/poses/badger/%s.png" % p
		var tex: Texture2D = load(file_path)
		if tex == null:
			push_error("無法載入破星蜜獾族姿態貼圖: %s" % file_path)
			ok = false
		else:
			var sz := tex.get_size()
			print("  ✓ %s: %s, 尺寸: %s" % [p, file_path, str(sz)])
			if int(sz.x) != 128 or int(sz.y) != 128:
				push_error("姿態 %s 尺寸不為 128x128，取得: %s" % [p, str(sz)])
				ok = false

	# 2. 驗證 SpriteDB 讀取專用姿態
	print("\n--- 2. 驗證 SpriteDB.tex 專用姿態讀取 ---")
	for p in poses:
		var t := SpriteDB.tex("res://assets/sprites/player/poses/badger/%s.png" % p)
		if t == null:
			push_error("SpriteDB.tex 無法載入 poses/badger/%s.png" % p)
			ok = false
		else:
			print("  ✓ SpriteDB 成功索引 poses/badger/%s.png" % p)

	# 3. 驗證 SpriteDB.player_pose("...", "badger") 正確調用 512 高清貼圖 (寬邊 >= 256)
	print("\n--- 3. 驗證 SpriteDB.player_pose 專用姿態分支 (512 高清貼圖，無 128 退路) ---")
	for p in poses:
		var pt := SpriteDB.player_pose(p, "badger")
		if pt == null:
			push_error("SpriteDB.player_pose('%s', 'badger') 回傳 null" % p)
			ok = false
		else:
			var sz := pt.get_size()
			if int(sz.x) < 256 or int(sz.y) < 256:
				push_error("SpriteDB.player_pose('%s', 'badger') 寬度小於 256 (退回了 128 糊圖): %s" % [p, str(sz)])
				ok = false
			else:
				print("  ✓ SpriteDB.player_pose('%s', 'badger') 成功載入: %dx%d (%s)" % [p, int(sz.x), int(sz.y), pt.resource_path])

	# 4. 驗證無效動作姿態安全回傳 null，⛔ 絕不退回 128 糊圖
	print("\n--- 4. 驗證無效動作姿態無 128 退路 (0-QA22 防護) ---")
	var invalid_pt := SpriteDB.player_pose("invalid_pose_name", "badger")
	if invalid_pt != null:
		push_error("0-QA22 違反: 破星蜜獾族無效姿態退回了非空貼圖: %s" % invalid_pt.resource_path)
		ok = false
	else:
		print("  ✓ 破星蜜獾族無效動作姿態安全回傳 null，無 128 退路")

	_finish(ok)

func _finish(ok: bool) -> void:
	if ok:
		print("\nBADGER_ACTION_POSES_TEST_OK")
		quit(0)
	else:
		push_error("\nBADGER_ACTION_POSES_TEST_FAILED")
		quit(1)
