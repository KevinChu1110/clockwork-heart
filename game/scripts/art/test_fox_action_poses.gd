extends SceneTree
## 《發條之心》狐族戰鬥六大動作姿態 (Fox Combat Action Poses) 無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_fox_action_poses.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始狐族六大戰鬥姿態無頭驗證 (Fox Action Poses Test) ===")

	var poses := ["idle", "telegraph", "attack", "recover", "skill", "hit"]
	
	# 1. 驗證六大姿態檔案存在且尺寸為 128x128
	print("\n--- 1. 驗證檔案存在性與尺寸 (128x128) ---")
	for p in poses:
		var file_path := "res://assets/sprites/player/poses/fox/%s.png" % p
		var tex: Texture2D = load(file_path)
		if tex == null:
			push_error("無法載入狐族姿態貼圖: %s" % file_path)
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
		var t := SpriteDB.tex("res://assets/sprites/player/poses/fox/%s.png" % p)
		if t == null:
			push_error("SpriteDB.tex 無法載入 poses/fox/%s.png" % p)
			ok = false
		else:
			print("  ✓ SpriteDB 成功索引 poses/fox/%s.png" % p)

	_finish(ok)

func _finish(ok: bool) -> void:
	if ok:
		print("\nFOX_ACTION_POSES_TEST_OK")
		quit(0)
	else:
		push_error("\nFOX_ACTION_POSES_TEST_FAILED")
		quit(1)
