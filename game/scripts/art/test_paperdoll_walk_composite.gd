extends SceneTree
## 《發條之心》探索走路執行期紙娃娃合成無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_paperdoll_walk_composite.gd

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	var ok := true
	print("=== 開始探索走路執行期紙娃娃分部位合成驗證 (PaperdollRenderer Walk) ===")

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		push_error("無法取得 GameState 單例")
		quit(1)
		return

	# 1. 測試空槽位時 fallback 回烘烤素體
	print("\n--- 檢查斷言 ①：未換裝時 fallback 至基準 walk 貼圖 ---")
	gs.set("player_race", "rabbit")
	gs.paperdoll_slots = {}
	SpriteDB.clear_equipped_cache()

	for f in range(4):
		var w_empty: Texture2D = SpriteDB.player_walk(f)
		if w_empty == null:
			push_error("未換裝時 player_walk(%d) 為 null" % f)
			ok = false
		elif not w_empty.resource_path.ends_with("rabbit_walk_%d_x3.png" % f):
			push_error("未換裝時 player_walk(%d) 未回傳基準烘烤圖: %s" % [f, w_empty.resource_path])
			ok = false
		else:
			print("  ✓ 空槽位 walk(%d) 正確回傳烘烤圖: %s" % [f, w_empty.resource_path])

	# 2. 測試換裝時動態合成 (PaperdollRenderer)
	print("\n--- 檢查斷言 ②：換裝後執行期分部位動態合成 512 (nutcracker_guard + dawn_blade) ---")
	var custom_slots := {
		"costume": "costume_nutcracker_guard",
		"weapon": "wpn_dawn_blade"
	}
	gs.paperdoll_slots = custom_slots.duplicate()
	SpriteDB.clear_equipped_cache()

	var idle_tex: Texture2D = SpriteDB.player_equipped_idle("rabbit", custom_slots)
	if idle_tex == null:
		push_error("換裝待機圖 player_equipped_idle 為 null")
		ok = false
	elif idle_tex.get_width() < 512 or idle_tex.get_height() < 512:
		push_error("換裝待機圖尺寸不足 512: %s" % str(idle_tex.get_size()))
		ok = false
	else:
		print("  ✓ 成功合成換裝待機圖: 尺寸 = %s" % str(idle_tex.get_size()))

	var walk_textures: Array[Texture2D] = []
	for f in range(4):
		var w_tex: Texture2D = SpriteDB.player_equipped_walk(f, "rabbit", custom_slots)
		if w_tex == null:
			push_error("換裝走路幀 player_equipped_walk(%d) 為 null" % f)
			ok = false
		elif w_tex.get_width() < 512 or w_tex.get_height() < 512:
			push_error("換裝走路幀 (%d) 尺寸不足 512: %s" % [f, str(w_tex.get_size())])
			ok = false
		else:
			print("  ✓ 成功合成換裝走路幀 (%d): 尺寸 = %s" % [f, str(w_tex.get_size())])
			walk_textures.append(w_tex)

		# 檢驗 SpriteDB.player_walk(f) 在有換裝時亦自動回傳即時合成貼圖
		var p_walk: Texture2D = SpriteDB.player_walk(f)
		if p_walk != w_tex:
			push_error("player_walk(%d) 未回傳當前換裝合成圖" % f)
			ok = false

	# 測試非兔族（狐族／獅族）換裝後走動亦為 512 合成
	print("\n--- 檢查斷言 ②-B：非兔族換裝走路 512 合成 ---")
	for nr in ["fox", "lion"]:
		var nr_slots := {"costume": "costume_astral_cape"}
		for f in range(4):
			var nr_walk := SpriteDB.player_equipped_walk(f, nr, nr_slots)
			if nr_walk == null:
				push_error("種族 %s 換裝走路幀 (%d) 為 null" % [nr, f])
				ok = false
			elif nr_walk.get_width() < 512 or nr_walk.get_height() < 512:
				push_error("種族 %s 換裝走路幀 (%d) 尺寸不足 512: %s" % [nr, f, str(nr_walk.get_size())])
				ok = false
			else:
				print("  ✓ 種族 %s 換裝走路幀 (%d) 成功合成 512: %s" % [nr, f, str(nr_walk.get_size())])

	if not ok:
		push_error("紙娃娃走路幀合成基礎檢查失敗")
		quit(1)
		return

	# 3. 像素級尺度與骨骼量測 (512x512)
	print("\n--- 檢查斷言 ③：尺度、腳底 y 與腿部動作幅度 (Rule 4b-7 / 4b-9 / 4b-9-2) ---")
	var idle_img: Image = idle_tex.get_image()
	var idle_foot_y := -1
	var idle_body_min_y := 999
	var idle_body_max_y := -1
	for y in range(512):
		for x in range(512):
			var c := idle_img.get_pixel(x, y)
			if c.a > 0.08:
				if y < 472:
					idle_body_min_y = mini(idle_body_min_y, y)
					idle_body_max_y = maxi(idle_body_max_y, y)
				if y >= 440 and y < 512 and x >= 160 and x <= 380 and c.a > 0.78:
					idle_foot_y = maxi(idle_foot_y, y)

	var idle_h: int = idle_body_max_y - idle_body_min_y + 1
	print("  待機: 本體高度 = %d px (y=[%d, %d]), 腳底 y = %d" % [idle_h, idle_body_min_y, idle_body_max_y, idle_foot_y])

	var walk_imgs: Array[Image] = []
	var heights: Array[int] = [idle_h]
	var foot_ys: Array[int] = [idle_foot_y]

	for f in range(4):
		var w_img: Image = walk_textures[f].get_image()
		walk_imgs.append(w_img)
		var f_foot_y := -1
		var f_min_y := 999
		var f_max_y := -1
		for y in range(512):
			for x in range(512):
				var c := w_img.get_pixel(x, y)
				if c.a > 0.08:
					if y < 472:
						f_min_y = mini(f_min_y, y)
						f_max_y = maxi(f_max_y, y)
					if y >= 440 and y < 512 and x >= 160 and x <= 380 and c.a > 0.78:
						f_foot_y = maxi(f_foot_y, y)

		var h: int = f_max_y - f_min_y + 1
		heights.append(h)
		foot_ys.append(f_foot_y)
		var diff_pct: float = abs(float(h - idle_h)) / float(idle_h) * 100.0
		print("  walk_%d: 本體高度 = %d px (y=[%d, %d]), 腳底 y = %d, 與待機高差 = %.2f%%" % [f, h, f_min_y, f_max_y, f_foot_y, diff_pct])

		if diff_pct > 5.0:
			push_error("walk_%d 身高差 %.2f%% > 5.0%% (違反 Rule 4b-9)" % [f, diff_pct])
			ok = false
		if abs(f_foot_y - idle_foot_y) > 12:
			push_error("walk_%d 腳底 y %d 與待機 %d 差距 > 12" % [f, f_foot_y, idle_foot_y])
			ok = false

	# 檢驗腿部區 (y=368..472) 幀間差 >= 2000px
	print("\n--- 檢查斷言 ④：腿部區幀間差 (Rule 4b-7 >= 2000px) ---")
	for i in range(4):
		for j in range(i + 1, 4):
			var leg_diff := 0
			for y in range(368, 472):
				for x in range(512):
					if walk_imgs[i].get_pixel(x, y) != walk_imgs[j].get_pixel(x, y):
						leg_diff += 1
			print("  Frames %d vs %d 腿部區差異: %d px (>=2000: %s)" % [i, j, leg_diff, str(leg_diff >= 2000)])
			if leg_diff < 2000:
				push_error("Frames %d vs %d 腿部區差異 %d px < 2000 px (違反 Rule 4b-7)" % [i, j, leg_diff])
				ok = false

	if ok:
		print("\n=======================================================")
		print("PAPERDOLL_WALK_COMPOSITE_OK")
		quit(0)
	else:
		push_error("驗證失敗")
		quit(1)
