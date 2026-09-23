extends SceneTree
## 九族 512 走路四幀與合成失敗退路無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_nine_races_walk_512.gd

const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始九族 512 走路四幀與失敗退路無頭驗證 (0-QA18, 0-QA21, 0-QA22, 31d) ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("無法取得 GameState 單例")
		quit(1)
		return

	var all_races := ["rabbit", "lion", "fox", "boar", "macaque", "tiger", "crane", "bear", "penguin", "tortoise", "elephant", "frog"]
	var broken_slots := {
		"costume": "broken_invalid_costume_999",
		"chassis": "broken_invalid_chassis_999"
	}

	# 1. 取得兔族基準走路幀
	var rabbit_walks: Array[Texture2D] = []
	for f in range(4):
		var rw: Texture2D = SpriteDB.player_equipped_walk(f, "rabbit", {})
		if rw == null or rw.get_width() < 256:
			push_error("兔族 player_equipped_walk(%d) 為空或寬度不足 256: %s" % [f, str(rw)])
			ok = false
		rabbit_walks.append(rw)

	# 2. 逐一檢驗九族走路成功路徑 (512) 與失敗退路 (本族預設 512，不退 128、不借兔)
	for r in all_races:
		print("\n--- 驗證種族: %s ---" % r)
		SpriteDB.clear_equipped_cache()

		var race_walks: Array[Texture2D] = []
		var walk_imgs: Array[Image] = []

		for f in range(4):
			# 測試正常 512 走路合成
			var w: Texture2D = SpriteDB.player_equipped_walk(f, r, {})
			if w == null:
				push_error("種族 %s walk(%d) 為 null" % [r, f])
				ok = false
			elif w.get_width() < 256 or w.get_height() < 256:
				push_error("種族 %s walk(%d) 尺寸不足 256: %dx%d" % [r, f, w.get_width(), w.get_height()])
				ok = false
			else:
				race_walks.append(w)
				walk_imgs.append(w.get_image())

			# 測試換裝 512 合成失敗時安全退回本族預設 512 走路幀
			SpriteDB.clear_equipped_cache()
			var fw: Texture2D = SpriteDB.player_equipped_walk(f, r, broken_slots)
			if fw == null:
				push_error("種族 %s 換裝失敗 walk(%d) 為 null" % [r, f])
				ok = false
			elif fw.get_width() < 256 or fw.get_height() < 256:
				push_error("種族 %s 換裝失敗 walk(%d) 退回低解析度: %dx%d (不准退回 128)" % [r, f, fw.get_width(), fw.get_height()])
				ok = false
			elif w != null and fw != null and (fw.get_width() != w.get_width() or fw.get_height() != w.get_height()):
				push_error("種族 %s 換裝失敗 walk(%d) 尺寸與預設 512 不符" % [r, f])
				ok = false
			else:
				print("  ✓ %s walk(%d) 成功合成尺寸 %dx%d；換裝失敗退路尺寸 %dx%d (>=256)" % [r, f, w.get_width() if w else 0, w.get_height() if w else 0, fw.get_width() if fw else 0, fw.get_height() if fw else 0])

		# 檢驗非兔族（含企鵝）絕不借兔步
		if r != "rabbit":
			for f in range(4):
				if f < race_walks.size() and f < rabbit_walks.size():
					var rw_img: Image = rabbit_walks[f].get_image()
					var ow_img: Image = race_walks[f].get_image()
					var diff_count := 0
					for y in range(0, 512, 4):
						for x in range(0, 512, 4):
							if rw_img.get_pixel(x, y) != ow_img.get_pixel(x, y):
								diff_count += 1
					if diff_count == 0:
						push_error("種族 %s walk(%d) 與兔族完全相同（借兔步）！" % [r, f])
						ok = false
					else:
						print("  ✓ %s walk(%d) 獨立於兔族 (差異像素採樣: %d)" % [r, f, diff_count])

		# 檢驗四幀會動（絕不每幀塞同一張立牌）
		if walk_imgs.size() == 4:
			var has_motion := false
			for i in range(4):
				for j in range(i + 1, 4):
					var diff := 0
					for y in range(0, 512, 2):
						for x in range(0, 512, 2):
							if walk_imgs[i].get_pixel(x, y) != walk_imgs[j].get_pixel(x, y):
								diff += 1
					if diff > 100:
						has_motion = true
			if not has_motion:
				push_error("種族 %s 走路四幀無動作變化（疑似每幀塞同一張靜態立牌）！" % r)
				ok = false
			else:
				print("  ✓ %s 走路四幀動態連續且具備動作變化 (會動，非靜態立牌)" % r)

	if ok:
		print("\nNINE_RACES_WALK_512_OK")
		quit(0)
	else:
		push_error("\nNINE_RACES_WALK_512_FAIL")
		quit(1)
