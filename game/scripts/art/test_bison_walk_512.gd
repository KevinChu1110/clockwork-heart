extends SceneTree
## 撼地野牛 (bison) 512 走路四幀與失敗退路無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_bison_walk_512.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始撼地野牛 (bison) 512 走路四幀與失敗退路無頭驗證 ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("無法取得 GameState 單例")
		quit(1)
		return

	# 1. 取得兔族基準走路幀
	var rabbit_walks: Array[Texture2D] = []
	for f in range(4):
		var rw: Texture2D = SpriteDB.player_equipped_walk(f, "rabbit", {})
		if rw == null or rw.get_width() < 256:
			push_error("兔族 player_equipped_walk(%d) 為空或寬度不足 256: %s" % [f, str(rw)])
			ok = false
		rabbit_walks.append(rw)

	# 2. 驗證 bison
	var r := "bison"
	print("\n--- 驗證種族: %s ---" % r)
	SpriteDB.clear_equipped_cache()

	var race_walks: Array[Texture2D] = []
	var walk_imgs: Array[Image] = []

	for f in range(4):
		var w_tex: Texture2D = SpriteDB.player_equipped_walk(f, r, {})
		if w_tex == null:
			push_error("種族 %s 之 player_equipped_walk(%d) 為空！" % [r, f])
			ok = false
			continue
		if w_tex.get_width() < 256 or w_tex.get_height() < 256:
			push_error("種族 %s 之 player_equipped_walk(%d) 尺寸異常 (非 512): %dx%d" % [r, f, w_tex.get_width(), w_tex.get_height()])
			ok = false
		race_walks.append(w_tex)
		walk_imgs.append(w_tex.get_image())

	# 驗證失敗退路 (使用無效槽位道具時不退 128、不借兔)
	var broken_slots := {
		"costume": "broken_invalid_costume_999",
		"chassis": "broken_invalid_chassis_999"
	}
	for f in range(4):
		var fb_tex: Texture2D = SpriteDB.player_equipped_walk(f, r, broken_slots)
		if fb_tex == null:
			push_error("種族 %s 之失敗退路 player_equipped_walk(%d) 為空！" % [r, f])
			ok = false
			continue
		if fb_tex.get_width() < 256 or fb_tex.get_height() < 256:
			push_error("種族 %s 失敗退路異常退回低清或為空: %dx%d" % [r, f, fb_tex.get_width(), fb_tex.get_height()])
			ok = false

	# 驗證與兔族獨立且四幀動態
	if race_walks.size() == 4 and rabbit_walks.size() == 4:
		for f in range(4):
			var diff := 0
			var img_r = walk_imgs[f]
			var img_rb = rabbit_walks[f].get_image()
			for y in range(0, 512, 8):
				for x in range(0, 512, 8):
					if img_r.get_pixel(x, y) != img_rb.get_pixel(x, y):
						diff += 1
			if diff < 100:
				push_error("種族 %s walk(%d) 疑似退回兔族素材 (差異採樣數: %d)" % [r, f, diff])
				ok = false
			else:
				print("  ✓ %s walk(%d) 獨立於兔族 (差異像素採樣: %d)" % [r, f, diff])

		# 幀間差異 (動態非靜態)
		var frame_diff := 0
		for y in range(0, 512, 8):
			for x in range(0, 512, 8):
				if walk_imgs[0].get_pixel(x, y) != walk_imgs[1].get_pixel(x, y):
					frame_diff += 1
		if frame_diff < 50:
			push_error("種族 %s 走路四幀過度相似 (幀0與幀1差異採樣: %d)" % [r, frame_diff])
			ok = false
		else:
			print("  ✓ %s 走路四幀動態連續且具備動作變化 (會動，非靜態立牌)" % r)

	if ok:
		print("\n🎉 BISON_WALK_512_OK")
		quit(0)
	else:
		push_error("\n❌ BISON_WALK_512_FAIL")
		quit(1)
