extends SceneTree
## 《發條之心》碧簧蛙族戰鬥六大動作姿態 (Spring-Leg Frog Combat Action Poses) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_frog_action_poses.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始碧簧蛙族六大戰鬥姿態無頭驗證 (Frog Action Poses Test) ===")

	var poses := ["idle", "telegraph", "attack", "recover", "skill", "hit"]

	# 1. 驗證六大姿態檔案存在且尺寸為 128x128
	print("\n--- 1. 驗證檔案存在性與尺寸 (128x128) ---")
	for p in poses:
		var file_path := "res://assets/sprites/player/poses/frog/%s.png" % p
		var tex: Texture2D = load(file_path)
		if tex == null:
			push_error("無法載入碧簧蛙族姿態貼圖: %s" % file_path)
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
		var t := SpriteDB.tex("res://assets/sprites/player/poses/frog/%s.png" % p)
		if t == null:
			push_error("SpriteDB.tex 無法載入 poses/frog/%s.png" % p)
			ok = false
		else:
			print("  ✓ SpriteDB 成功索引 poses/frog/%s.png" % p)

	# 3. 驗證 SpriteDB.player_pose("...", "frog") 正確調用 512 高清貼圖
	print("\n--- 3. 驗證 SpriteDB.player_pose 專用姿態分支 ---")
	for p in poses:
		var pt := SpriteDB.player_pose(p, "frog")
		if pt == null:
			push_error("SpriteDB.player_pose('%s', 'frog') 回傳 null" % p)
			ok = false
		else:
			print("  ✓ SpriteDB.player_pose('%s', 'frog') 成功載入: %dx%d (%s)" % [p, int(pt.get_size().x), int(pt.get_size().y), pt.resource_path])

	_finish(ok)

func _finish(ok: bool) -> void:
	if ok:
		print("\nFROG_ACTION_POSES_TEST_OK")
		quit(0)
	else:
		push_error("\nFROG_ACTION_POSES_TEST_FAILED")
		quit(1)
