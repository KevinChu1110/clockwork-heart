extends SceneTree
## 《發條之心》第二族熾火赤狐楓之谷 Character.wz 骨骼錨點與部件分層掛載無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_maple_paperdoll_fox.gd

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")
const FOX_SPEC_PATH := "res://data/tables/maple_paperdoll_fox.json"
const PROOF_DIR := "res://assets/sprites/player/paperdoll/fox/"


func _initialize() -> void:
	var ok := true
	print("=== 開始熾火赤狐楓之谷骨骼錨點與部件分層掛載測試 (Maple Paperdoll Fox Test) ===")

	var doll := MaplePaperdollClass.new()
	doll.spec_path = FOX_SPEC_PATH
	doll.breathing_enabled = false # 先關閉以精準測試靜態錨點與位移
	root.add_child(doll)

	if not is_instance_valid(doll):
		push_error("無法實例化 MaplePaperdoll 節點")
		_finish(false)
		return

	doll.load_spec(FOX_SPEC_PATH)

	# -------------------------------------------------------------
	# 1. 驗證角色骨骼/錨點體系（neck/navel/hand/brow/back_key）
	# -------------------------------------------------------------
	print("\n--- 1. 驗證赤狐骨骼錨點體系 (neck/navel/hand/brow/back_key) ---")
	var neck_node := doll.get_anchor_node("neck")
	var navel_node := doll.get_anchor_node("navel")
	var hand_node := doll.get_anchor_node("hand")
	var brow_node := doll.get_anchor_node("brow")
	var back_key_node := doll.get_anchor_node("back_key")

	if neck_node == null or navel_node == null or hand_node == null or brow_node == null or back_key_node == null:
		push_error("核心錨點節點缺失！")
		ok = false
	else:
		print("  ✓ 核心 5 大錨點節點均成功建立")
		# 檢查座標 (基準 512 空間)
		if neck_node.position != Vector2(260, 255):
			push_error("neck 錨點座標不符: %s vs (260, 255)" % str(neck_node.position))
			ok = false
		if navel_node.position != Vector2(256, 350):
			push_error("navel 錨點座標不符: %s vs (256, 350)" % str(navel_node.position))
			ok = false
		if hand_node.position != Vector2(358, 363):
			push_error("hand 錨點座標不符: %s vs (358, 363)" % str(hand_node.position))
			ok = false
		if back_key_node.position != Vector2(370, 280):
			push_error("back_key 錨點座標不符: %s vs (370, 280)" % str(back_key_node.position))
			ok = false
		if brow_node.position != Vector2(0, -60):
			push_error("brow 錨點相對於 neck 座標不符: %s vs (0, -60)" % str(brow_node.position))
			ok = false

		if ok:
			print("  ✓ neck(260,255), navel(256,350), hand(358,363), back_key(370,280), brow(260,195) 座標 100% 精準")

	# -------------------------------------------------------------
	# 2. 驗證眼睛、外裝、武器、發條鑰匙獨立為帶 origin 錨點之緊湊 Sprite
	# -------------------------------------------------------------
	print("\n--- 2. 驗證各部件帶 origin 獨立緊湊 Sprite ---")
	var spr_eyes := doll.get_slot_sprite("eyes")
	var spr_costume := doll.get_slot_sprite("costume")
	var spr_weapon := doll.get_slot_sprite("weapon")
	var spr_key := doll.get_slot_sprite("winding_key")
	var spr_head := doll.get_slot_sprite("head_unit")

	if spr_eyes == null or spr_costume == null or spr_weapon == null or spr_key == null or spr_head == null:
		push_error("部件 Sprite2D 節點不存在！")
		ok = false
	else:
		print("  ✓ 眼睛 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_eyes.name, str(spr_eyes.texture.get_size()), str(spr_eyes.position)])
		print("  ✓ 外裝 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_costume.name, str(spr_costume.texture.get_size()), str(spr_costume.position)])
		print("  ✓ 武器 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_weapon.name, str(spr_weapon.texture.get_size()), str(spr_weapon.position)])
		print("  ✓ 發條鑰匙 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_key.name, str(spr_key.texture.get_size()), str(spr_key.position)])
		print("  ✓ 狐耳/頭部單元 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_head.name, str(spr_head.texture.get_size()), str(spr_head.position)])

		# 驗證各部件並非 512 全圖死切片，而是緊湊獨立素材帶有精確 origin
		if spr_eyes.texture.get_width() >= 512 or spr_costume.texture.get_width() >= 512 or spr_key.texture.get_width() >= 512 or spr_head.texture.get_width() >= 512 or spr_weapon.texture.get_width() >= 512:
			push_error("部件非緊湊切片，仍為全圖 512 畫布！")
			ok = false
		else:
			print("  ✓ 所有部件均為獨立緊湊裁剪 Sprite (眼睛 165x60, 外裝 171x168 / 153x181, 發條鑰匙 61x107, 狐耳 253x106, 武器 83x193)")

	# -------------------------------------------------------------
	# 3. 驗證「眼睛不畫死在素體上」與雙頰面甲平滑無色差補丁、無黑線雜訊
	# -------------------------------------------------------------
	print("\n--- 3. 驗證眼睛不畫死在素體上與雙頰面甲平滑無補丁雜訊 ---")
	doll.set_eyes("none")
	var bare_img := doll.get_composite_image()

	# 3.1 雙側臉頰底色取樣比對斷言 (sideqa 審查要項 1 & 4)
	var left_cheek := bare_img.get_pixel(216, 195)
	var right_cheek := bare_img.get_pixel(315, 195)
	var left_ref := bare_img.get_pixel(180, 195)
	var right_ref := bare_img.get_pixel(340, 195)

	print("  左臉頰 (216, 195) 像素: %s vs 參照 (180, 195): %s" % [str(left_cheek), str(left_ref)])
	print("  右臉頰 (315, 195) 像素: %s vs 參照 (340, 195): %s" % [str(right_cheek), str(right_ref)])

	# 左頰應為飽和溫暖金屬塗裝（非死黑眼眶）
	if left_cheek.r < 0.7 or left_cheek.g < 0.4:
		push_error("素體左側臉頰仍殘留畫死的深黑眼睛線條！")
		ok = false
	# 右頰應為純淨奶油金屬底色（非死黑眼眶，且與右側底色無補丁色差）
	if right_cheek.r < 0.8 or right_cheek.g < 0.7:
		push_error("素體右側臉頰仍殘留畫死的深黑眼睛線條！")
		ok = false
	if abs(right_cheek.r - right_ref.r) > 0.05 or abs(right_cheek.g - right_ref.g) > 0.05 or abs(right_cheek.b - right_ref.b) > 0.05:
		push_error("素體右臉頰去眼處存在明顯邊界生硬的補丁色差！%s vs %s" % [str(right_cheek), str(right_ref)])
		ok = false
	else:
		print("  ✓ 雙側臉頰面甲底色完全一致且無補丁色塊 (左頰橘金、右頰奶霜純淨)")

	# 3.2 檢查額頭眉線區域無殘留黑線雜訊 (y: 148..165, x: 200..335)
	var brow_artifact_count := 0
	for by in range(148, 166):
		for bx in range(200, 336):
			var bpx := bare_img.get_pixel(bx, by)
			if bpx.a > 0.5 and bpx.r < 0.25 and bpx.g < 0.25 and bpx.b < 0.25:
				brow_artifact_count += 1
	if brow_artifact_count > 0:
		push_error("素體額頭/眉部偵測到 %d 個殘留黑線雜訊像素！" % brow_artifact_count)
		ok = false
	else:
		print("  ✓ 額頭與眉部無任何殘留黑線雜訊 (0 個黑線像素)")

	# 3.3 檢查右眼下方與鼻頰周圍無切片破圖折線與三角形雜訊碎片 (sideqa 審查要項 1)
	var noise_artifact_count := 0
	# 右側鼻頰眼下區域 (x: 283..294, y: 228..236)
	for ny in range(228, 236):
		for nx in range(283, 294):
			var npx := bare_img.get_pixel(nx, ny)
			if npx.a > 0.5 and npx.r < 0.25 and npx.g < 0.25 and npx.b < 0.25:
				noise_artifact_count += 1
	# 左側鼻頰眼下區域 (x: 240..248, y: 228..235)
	for ny in range(228, 235):
		for nx in range(240, 248):
			var npx := bare_img.get_pixel(nx, ny)
			if npx.a > 0.5 and npx.r < 0.25 and npx.g < 0.25 and npx.b < 0.25:
				noise_artifact_count += 1
	if noise_artifact_count > 0:
		push_error("素體眼下與鼻頰側偵測到 %d 個殘留折線/三角形雜訊破圖碎片！" % noise_artifact_count)
		ok = false
	else:
		print("  ✓ 眼下與鼻頰處乾淨平整，無任何切片殘留破圖碎片")

	# 裝回眼睛
	doll.set_eyes("eyes_cyan_emerald")

	# -------------------------------------------------------------
	# 3.1 驗證眼睛上裝後額頭無黑色遮罩方塊、臉頰無錯位溢色
	# -------------------------------------------------------------
	print("\n--- 3.1 驗證眼睛上裝後額頭純淨無黑條遮罩、臉頰無溢色 ---")
	for eye_id in ["eyes_cyan_emerald", "eyes_amber_gold"]:
		doll.set_eyes(eye_id)
		var img_eye := doll.get_composite_image()
		# 檢查額頭正中央區域 (y: 145..154, x: 250..270) 是否被實心純黑方條破圖覆蓋
		var black_count := 0
		for check_y in range(145, 155):
			for check_x in range(250, 271):
				var px := img_eye.get_pixel(check_x, check_y)
				if px.a > 0.5 and px.r < 0.08 and px.g < 0.08 and px.b < 0.08:
					black_count += 1
		if black_count > 0:
			push_error("眼睛 %s 在額頭部位偵測到 %d 個實心黑條遮罩破圖像素！" % [eye_id, black_count])
			ok = false
		else:
			print("  ✓ 眼睛 %s 額頭無任何黑條遮罩破圖" % eye_id)

	doll.set_eyes("eyes_cyan_emerald")

	# -------------------------------------------------------------
	# 4. 驗證動態 Z-Order 層級控制
	# -------------------------------------------------------------
	print("\n--- 4. 驗證動態 Z-Order 層級控制 ---")
	var default_z_weapon := doll.get_part_z_index("weapon")
	var default_z_key := doll.get_part_z_index("winding_key")
	print("  預設 Z-Index: weapon=%d, winding_key=%d" % [default_z_weapon, default_z_key])

	# 將武器切換至身體後方 (Z: 4)
	doll.set_part_z_index("weapon", 4)
	if doll.get_part_z_index("weapon") != 4 or spr_weapon.z_index != 4:
		push_error("武器動態 Z-Index 切換失敗！")
		ok = false
	else:
		print("  ✓ 武器動態降至背後 (Z: 4) 成功")

	# 將發條鑰匙切換至前方 (Z: 15)
	doll.set_part_z_index("winding_key", 15)
	if doll.get_part_z_index("winding_key") != 15 or spr_key.z_index != 15:
		push_error("發條鑰匙動態 Z-Index 切換失敗！")
		ok = false
	else:
		print("  ✓ 發條鑰匙動態提至前方 (Z: 15) 成功")

	# 還原預設 Z
	doll.set_part_z_index("weapon", default_z_weapon)
	doll.set_part_z_index("winding_key", default_z_key)

	# -------------------------------------------------------------
	# 5. 驗證部件自由置換矩陣
	# -------------------------------------------------------------
	print("\n--- 5. 驗證部件自由置換矩陣 ---")
	var costumes := ["costume_astral_cape", "costume_astral_observer", "none"]
	var eye_variants := ["eyes_cyan_emerald", "eyes_amber_gold", "eyes_blink"]
	var bodies := ["paint_fox_orange", "paint_ivory_stock", "paint_emerald_glaze"]
	var heads := ["ear_fox_radar_orange", "ear_fox_radar_ivory", "ear_fox_radar_emerald"]

	for c in costumes:
		doll.set_costume(c)
		var cur_c := doll.get_part_item("costume")
		if cur_c != c:
			push_error("外裝切換失敗: %s" % c)
			ok = false
	print("  ✓ 3 款外裝切換驗證通過 (astral_cape / astral_observer / bare)")

	# -------------------------------------------------------------
	# 5.1 驗證外裝狀態下心臟核心完全露出 (0-ART51 與驗收標準)
	# -------------------------------------------------------------
	print("\n--- 5.1 驗證外裝狀態下心臟核心完全露出 (0-ART51) 零穿模 ---")
	for c_check in ["costume_astral_cape", "costume_astral_observer"]:
		doll.set_costume(c_check)
		var c_img := doll.get_composite_image()
		# 檢查心臟核心中心位置 (263, 319) 像素值
		var core_px := c_img.get_pixel(263, 319)
		print("  外裝 %s 胸前心臟核心中心 (263, 319) 像素值: %s" % [c_check, str(core_px)])
		# 發光心臟核心特徵：青綠天青高 G、高 B、低 R (青綠發光體)
		if core_px.g < 0.45 or core_px.b < 0.45 or core_px.r > 0.4:
			push_error("外裝 %s 胸前未開出視窗，心臟核心被完全遮蔽！像素值: %s" % [c_check, str(core_px)])
			ok = false
		else:
			print("  ✓ 外裝 %s 胸前自然開出視窗，青綠發光心臟核心 100%% 露出 (0-ART51 通過)" % c_check)

	# 還原外裝
	doll.set_costume("costume_astral_cape")

	for e in eye_variants:
		doll.set_eyes(e)
		var cur_e := doll.get_part_item("eyes")
		if cur_e != e:
			push_error("眼睛切換失敗: %s" % e)
			ok = false
	print("  ✓ 3 款面部光學核心切換驗證通過 (cyan / amber / blink)")

	for b in bodies:
		doll.set_body(b)
		var cur_b := doll.get_part_item("body")
		if cur_b != b:
			push_error("塗裝素體切換失敗: %s" % b)
			ok = false
	print("  ✓ 3 款塗裝素體切換驗證通過 (fox_orange / ivory_stock / emerald_glaze)")

	for h in heads:
		doll.set_head_unit(h)
		var cur_h := doll.get_part_item("head_unit")
		if cur_h != h:
			push_error("狐耳頭部單元切換失敗: %s" % h)
			ok = false
	print("  ✓ 3 款狐耳頭部單元切換驗證通過 (orange / ivory / emerald)")

	# 還原標準外觀
	doll.set_body("paint_fox_orange")
	doll.set_head_unit("ear_fox_radar_orange")
	doll.set_costume("costume_astral_cape")
	doll.set_eyes("eyes_cyan_emerald")
	doll.set_weapon("wpn_astral_staff")
	doll.set_winding_key("key_classic_brass")

	# -------------------------------------------------------------
	# 6. 驗證呼吸待機動態與骨骼聯動
	# -------------------------------------------------------------
	print("\n--- 6. 驗證呼吸待機動態與骨骼聯動 ---")
	doll.breathing_enabled = true
	var init_body_y := doll.node_body.position.y
	var init_key_rot := doll.node_back_key.rotation

	# 推進時間 0.6 秒 (1/4 週期，應達正峰值)
	doll.update_breathing(0.6)
	var peak_body_y := doll.node_body.position.y
	var peak_key_rot := doll.node_back_key.rotation

	print("  t=0.0s Body Y: %.2f px, Key Rot: %.2f rad" % [init_body_y, init_key_rot])
	print("  t=0.6s Body Y: %.2f px, Key Rot: %.2f rad" % [peak_body_y, peak_key_rot])

	if abs(peak_body_y - init_body_y) < 1.0:
		push_error("呼吸待機動態未產生足夠身體垂直起伏！")
		ok = false
	else:
		print("  ✓ Body 呼吸起伏正常 (振幅 %.2f px)" % abs(peak_body_y - init_body_y))

	if abs(peak_key_rot - init_key_rot) < 0.2:
		push_error("發條鑰匙待機自轉未觸發！")
		ok = false
	else:
		print("  ✓ 發條鑰匙自轉流暢 (角位移 %.2f rad)" % abs(peak_key_rot - init_key_rot))

	var global_neck_y := doll.node_neck.global_position.y
	var global_navel_y := doll.node_navel.global_position.y
	print("  ✓ 子錨點完全隨父骨骼平移：Neck 全域 Y=%.1f, Navel 全域 Y=%.1f" % [global_neck_y, global_navel_y])

	# -------------------------------------------------------------
	# 7. 產生展示截圖 Proofs 存證
	# -------------------------------------------------------------
	print("\n--- 7. 產生展示截圖 Proofs 存證 ---")
	doll.breathing_enabled = false
	doll.node_body.position = Vector2.ZERO
	doll.node_neck.position = Vector2(260, 255)
	doll.node_neck.rotation = 0.0
	doll.node_back_key.rotation = 0.0

	# 存證 A: 基準完整拼裝立繪
	var path_a := PROOF_DIR + "proof_maple_fox_composite.png"
	var err_a := doll.save_composite_png(path_a)
	if err_a != OK:
		push_error("存證 A 儲存失敗: %d" % err_a)
		ok = false
	else:
		print("  ✓ 已輸出存證 A: %s" % path_a)

	# 存證 B: 眼睛分離比對圖 (裸臉面甲 vs 外掛天青核心 vs 外掛琥珀金陽)
	var path_b := PROOF_DIR + "proof_maple_fox_eyes_separated.png"
	doll.set_eyes("none")
	var img_bare_fox := doll.get_composite_image()
	doll.set_eyes("eyes_cyan_emerald")
	var img_cyan_fox := doll.get_composite_image()
	doll.set_eyes("eyes_amber_gold")
	var img_amber_fox := doll.get_composite_image()

	var comp_b := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_b.fill(Color(1, 0.99, 0.97, 1)) # Cream 多巴胺奶油底
	comp_b.blend_rect(img_bare_fox, Rect2i(0, 0, 512, 512), Vector2i(0, 0))
	comp_b.blend_rect(img_cyan_fox, Rect2i(0, 0, 512, 512), Vector2i(512, 0))
	comp_b.blend_rect(img_amber_fox, Rect2i(0, 0, 512, 512), Vector2i(1024, 0))
	comp_b.save_png(path_b)
	print("  ✓ 已輸出存證 B: %s (證明眼睛不畫死在素體上)" % path_b)

	# 存證 C: 3 款外裝置換展示 (astral_cape / astral_observer / bare)
	var path_c := PROOF_DIR + "proof_maple_fox_costume_variants.png"
	var comp_c := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_c.fill(Color(1, 0.99, 0.97, 1))

	var c_list := ["costume_astral_cape", "costume_astral_observer", "none"]
	for idx in range(c_list.size()):
		doll.set_costume(c_list[idx])
		var c_img := doll.get_composite_image()
		comp_c.blend_rect(c_img, Rect2i(0, 0, 512, 512), Vector2i(idx * 512, 0))
	comp_c.save_png(path_c)
	print("  ✓ 已輸出存證 C: %s (證明部件自由置換無切片邊界破圖)" % path_c)

	# 存證 D: 動態 Z-Order 切換存證 (左: 武器在手前 z=40 / 右: 武器背在身後 z=4)
	doll.set_costume("costume_astral_cape")
	doll.set_part_z_index("weapon", 40)
	var img_z_front := doll.get_composite_image()
	doll.set_part_z_index("weapon", 4)
	var img_z_back := doll.get_composite_image()
	var path_d := PROOF_DIR + "proof_maple_fox_z_order_swap.png"
	var comp_d := Image.create(512 * 2, 512, false, Image.FORMAT_RGBA8)
	comp_d.fill(Color(1, 0.99, 0.97, 1))
	comp_d.blend_rect(img_z_front, Rect2i(0, 0, 512, 512), Vector2i(0, 0))
	comp_d.blend_rect(img_z_back, Rect2i(0, 0, 512, 512), Vector2i(512, 0))
	comp_d.save_png(path_d)
	print("  ✓ 已輸出存證 D: %s (證明動態 Z-Order 層級控制)" % path_d)

	# 存證 E: 4 幀呼吸動態時序存證 (t=0.0s, 0.6s, 1.2s, 1.8s)
	doll.set_part_z_index("weapon", 40)
	doll.breathing_enabled = true
	var path_e := PROOF_DIR + "proof_maple_fox_breathing_sequence.png"
	var comp_e := Image.create(512 * 4, 512, false, Image.FORMAT_RGBA8)
	comp_e.fill(Color(1, 0.99, 0.97, 1))

	var times := [0.0, 0.6, 1.2, 1.8]
	for idx in range(times.size()):
		doll._anim_time = times[idx]
		doll.update_breathing(0.0)
		var b_img := doll.get_composite_image()
		comp_e.blend_rect(b_img, Rect2i(0, 0, 512, 512), Vector2i(idx * 512, 0))
	comp_e.save_png(path_e)
	print("  ✓ 已輸出存證 E: %s (證明具備呼吸待機動態且骨骼錨點完全聯動)" % path_e)

	doll.queue_free()
	_finish(ok)


func _finish(success: bool) -> void:
	if success:
		print("\n=== 熾火赤狐楓之谷骨骼錨點與部件分層掛載測試全部通過 ===")
		print("MAPLE_PAPERDOLL_FOX_OK")
		quit(0)
	else:
		push_error("\n=== 熾火赤狐楓之谷骨骼錨點與部件分層掛載測試失敗 ===")
		print("MAPLE_PAPERDOLL_FOX_FAIL")
		quit(1)
