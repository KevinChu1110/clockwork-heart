extends SceneTree
## 九族戰鬥五大動作姿態 512 驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_nine_races_combat_poses_512.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

const RACES := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda"]
const POSES := ["attack", "hit", "skill", "telegraph", "recover"]

func _initialize() -> void:
	var ok := true
	print("=== 開始九族戰鬥五大動作姿態 512 驗證測試 ===")

	for r in RACES:
		print("\n--- 檢查種族: %s ---" % r)
		for p in POSES:
			var tex: Texture2D = SpriteDB.player_pose(p, r)
			if tex == null:
				push_error("SpriteDB.player_pose('%s', '%s') 回傳 null" % [p, r])
				ok = false
			else:
				var sz := tex.get_size()
				if int(sz.x) != 512 or int(sz.y) != 512:
					push_error("SpriteDB.player_pose('%s', '%s') 尺寸不為 512x512，取得: %s" % [p, r, str(sz)])
					ok = false
				else:
					print("  ✓ %s: %s (512x512)" % [p, tex.resource_path])

	# 驗證 0-ART26 防護：不存在的假種族不可借用兔族姿態
	print("\n--- 驗證 0-ART26 防護（跨族借圖防護） ---")
	var fake_tex: Texture2D = SpriteDB.player_pose("attack", "non_existent_race")
	if fake_tex != null:
		push_error("0-ART26 違反: 不存在種族 fallback 到了兔族或其他姿態: %s" % fake_tex.resource_path)
		ok = false
	else:
		print("  ✓ 0-ART26 守護成功: 不存在種族安全回傳 null，無借圖行為")

	# 驗證 0-QA22 防護：無 512 或無效動作姿態安全回傳 null，絕不退回 128 糊圖
	print("\n--- 驗證 0-QA22 防護（無 128 糊圖退路） ---")
	for r in ["rabbit", "lion", "fox"]:
		var invalid_tex: Texture2D = SpriteDB.player_pose("invalid_test_pose", r)
		if invalid_tex != null:
			push_error("0-QA22 違反: 種族 %s 無效姿態退回了非空貼圖: %s (寬度: %d)" % [r, invalid_tex.resource_path, invalid_tex.get_width()])
			ok = false
		else:
			print("  ✓ 種族 %s 無效姿態安全回傳 null，無 128 退路" % r)

	if ok:
		print("\nNINE_RACES_COMBAT_POSES_512_OK")
		quit(0)
	else:
		push_error("\nNINE_RACES_COMBAT_POSES_512_FAIL")
		quit(1)
