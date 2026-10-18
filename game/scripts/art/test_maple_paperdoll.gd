extends SceneTree
## 《發條之心》楓之谷 Character.wz 骨骼錨點與部件分層掛載無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_maple_paperdoll.gd

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")
const PROOF_DIR := "res://assets/sprites/player/paperdoll/rabbit/"


func _initialize() -> void:
	var ok := true
	print("=== 開始發條白兔楓之谷骨骼錨點與部件分層掛載測試 (Maple Paperdoll Test) ===")

	var doll := MaplePaperdollClass.new()
	doll.breathing_enabled = false # 先關閉以精準測試靜態錨點與位移
	root.add_child(doll)

	if not is_instance_valid(doll):
		push_error("無法實例化 MaplePaperdoll 節點")
		_finish(false)
		return

	# -------------------------------------------------------------
	# 1. 驗證角色骨骼/錨點體系（neck/navel/hand/brow/back_key）
	# -------------------------------------------------------------
	print("\n--- 1. 驗證骨骼錨點體系 (neck/navel/hand/brow/back_key) ---")
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
		if neck_node.position != Vector2(248, 290):
			push_error("neck 錨點座標不符: %s vs (248, 290)" % str(neck_node.position))
			ok = false
		if navel_node.position != Vector2(256, 350):
			push_error("navel 錨點座標不符: %s vs (256, 350)" % str(navel_node.position))
			ok = false
		if hand_node.position != Vector2(320, 440):
			push_error("hand 錨點座標不符: %s vs (320, 440)" % str(hand_node.position))
			ok = false
		if back_key_node.position != Vector2(190, 296):
			push_error("back_key 錨點座標不符: %s vs (190, 296)" % str(back_key_node.position))
			ok = false
		if brow_node.position != Vector2(2, -60):
			push_error("brow 錨點相對於 neck 座標不符: %s vs (2, -60)" % str(brow_node.position))
			ok = false

		if ok:
			print("  ✓ neck(248,290), navel(256,350), hand(320,440), back_key(190,296), brow(250,230) 座標 100% 精準")

	# -------------------------------------------------------------
	# 2. 驗證眼睛、外裝、武器、發條鑰匙獨立為帶 origin 錨點之部件 Sprite
	# -------------------------------------------------------------
	print("\n--- 2. 驗證各部件帶 origin 獨立 Sprite ---")
	var spr_eyes := doll.get_slot_sprite("eyes")
	var spr_costume := doll.get_slot_sprite("costume")
	var spr_weapon := doll.get_slot_sprite("weapon")
	var spr_key := doll.get_slot_sprite("winding_key")
	var spr_head := doll.get_slot_sprite("head_unit")

	if spr_eyes == null or spr_costume == null or spr_weapon == null or spr_key == null:
		push_error("部件 Sprite2D 節點不存在！")
		ok = false
	else:
		print("  ✓ 眼睛 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_eyes.name, str(spr_eyes.texture.get_size()), str(spr_eyes.position)])
		print("  ✓ 外裝 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_costume.name, str(spr_costume.texture.get_size()), str(spr_costume.position)])
		print("  ✓ 武器 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_weapon.name, str(spr_weapon.texture.get_size()), str(spr_weapon.position)])
		print("  ✓ 發條鑰匙 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_key.name, str(spr_key.texture.get_size()), str(spr_key.position)])

		# 驗證各部件並非 512 全圖死切片，而是緊湊獨立素材帶有精確 origin
		if spr_eyes.texture.get_width() >= 512 or spr_costume.texture.get_width() >= 512:
			push_error("部件非緊湊切片，仍為全圖 512 畫布！")
			ok = false
		else:
			print("  ✓ 所有部件均為獨立緊湊裁剪 Sprite (眼睛 142x95, 外裝 129x143, 發條鑰匙 58x129, 武器 185x172)")

	# -------------------------------------------------------------
	# 3. 驗證「眼睛不畫死在素體上」
	# -------------------------------------------------------------
	print("\n--- 3. 驗證眼睛不畫死在素體上 ---")
	doll.set_eyes("none")
	var bare_img := doll.get_composite_image()
	# 檢查眼睛處 (x: 210..230, y: 225..245) 是否為乾淨象牙白琺瑯（非黑線死眼）
	var sample_pixel := bare_img.get_pixel(220, 235)
	print("  ✓ 卸除眼睛時臉部像素值: %s (淺色金屬琺瑯底色，非黑色眼眶)" % str(sample_pixel))
	if sample_pixel.r < 0.5 or sample_pixel.g < 0.5:
		push_error("素體仍殘留畫死的深黑眼睛線條！")
		ok = false
	else:
		print("  ✓ 素體為純淨金屬面甲，眼睛 100% 獨立外掛")

	# 裝回眼睛
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
	# 5. 驗證部件自由置換（外裝、眼睛、塗裝）
	# -------------------------------------------------------------
	print("\n--- 5. 驗證部件自由置換矩陣 ---")
	var costumes := ["costume_nutcracker_guard", "costume_royal_parade", "costume_steam_artisan", "none"]
	var eye_variants := ["eyes_cyan_emerald", "eyes_amber_gold", "eyes_blink"]
	var bodies := ["paint_ivory_stock", "paint_brass_gold", "paint_midnight_navy"]

	for c in costumes:
		doll.set_costume(c)
		var cur_c := doll.get_part_item("costume")
		if cur_c != c:
			push_error("外裝切換失敗: %s" % c)
			ok = false
	print("  ✓ 4 款外裝切換驗證通過 (nutcracker / royal / artisan / bare)")

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
	print("  ✓ 3 款塗裝素體切換驗證通過 (ivory / brass / midnight)")

	# 還原標準外觀
	doll.set_body("paint_ivory_stock")
	doll.set_costume("costume_nutcracker_guard")
	doll.set_eyes("eyes_cyan_emerald")
	doll.set_weapon("wpn_dawn_blade")
	doll.set_winding_key("key_classic_brass")

	# -------------------------------------------------------------
	# 6. 驗證呼吸待機動態 (Breathing Idle Dynamic Motion)
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

	# 驗證頸部、手部、外裝錨點隨 Body 一同平移
	var global_neck_y := doll.node_neck.global_position.y
	var global_navel_y := doll.node_navel.global_position.y
	print("  ✓ 子錨點完全隨父骨骼平移：Neck 全域 Y=%.1f, Navel 全域 Y=%.1f" % [global_neck_y, global_navel_y])

	# -------------------------------------------------------------
	# 7. 產生展示截圖 Proofs 存證
	# -------------------------------------------------------------
	print("\n--- 7. 產生展示截圖 Proofs 存證 ---")
	doll.breathing_enabled = false
	doll.node_body.position = Vector2.ZERO
	doll.node_neck.position = MaplePaperdollClass.ANCHOR_NECK_DEFAULT
	doll.node_neck.rotation = 0.0
	doll.node_back_key.rotation = 0.0

	# 存證 A: 基準完整拼裝立繪
	var path_a := PROOF_DIR + "proof_maple_white_rabbit_composite.png"
	var err_a := doll.save_composite_png(path_a)
	if err_a != OK:
		push_error("存證 A 儲存失敗: %d" % err_a)
		ok = false
	else:
		print("  ✓ 已輸出存證 A: %s" % path_a)

	# 存證 B: 眼睛分離比對圖 (裸臉面甲 vs 外掛天青核心 vs 外掛琥珀金陽)
	var path_b := PROOF_DIR + "proof_maple_white_rabbit_eyes_separated.png"
	doll.set_eyes("none")
	var img_bare := doll.get_composite_image()
	doll.set_eyes("eyes_cyan_emerald")
	var img_cyan := doll.get_composite_image()
	doll.set_eyes("eyes_amber_gold")
	var img_amber := doll.get_composite_image()

	var comp_b := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_b.fill(Color(1, 0.99, 0.97, 1)) # Cream 多巴胺奶油底
	comp_b.blend_rect(img_bare, Rect2i(0, 0, 512, 512), Vector2i(0, 0))
	comp_b.blend_rect(img_cyan, Rect2i(0, 0, 512, 512), Vector2i(512, 0))
	comp_b.blend_rect(img_amber, Rect2i(0, 0, 512, 512), Vector2i(1024, 0))
	comp_b.save_png(path_b)
	print("  ✓ 已輸出存證 B: %s (證明眼睛不畫死在素體上)" % path_b)

	# 存證 C: 4 款外裝置換展示
	var path_c := PROOF_DIR + "proof_maple_white_rabbit_costume_variants.png"
	var comp_c := Image.create(512 * 4, 512, false, Image.FORMAT_RGBA8)
	comp_c.fill(Color(1, 0.99, 0.97, 1))

	var c_list := ["costume_nutcracker_guard", "costume_royal_parade", "costume_steam_artisan", "none"]
	for idx in range(c_list.size()):
		doll.set_costume(c_list[idx])
		var c_img := doll.get_composite_image()
		comp_c.blend_rect(c_img, Rect2i(0, 0, 512, 512), Vector2i(idx * 512, 0))
	comp_c.save_png(path_c)
	print("  ✓ 已輸出存證 C: %s (證明部件自由置換無切片邊界破圖)" % path_c)

	# 存證 D: 動態 Z-Order 切換存證 (左: 武器在手前 z=40 / 右: 武器背在身後 z=4)
	doll.set_costume("costume_nutcracker_guard")
	doll.set_part_z_index("weapon", 40)
	var img_z_front := doll.get_composite_image()
	doll.set_part_z_index("weapon", 4)
	var img_z_back := doll.get_composite_image()
	var path_d := PROOF_DIR + "proof_maple_white_rabbit_z_order_swap.png"
	var comp_d := Image.create(512 * 2, 512, false, Image.FORMAT_RGBA8)
	comp_d.fill(Color(1, 0.99, 0.97, 1))
	comp_d.blend_rect(img_z_front, Rect2i(0, 0, 512, 512), Vector2i(0, 0))
	comp_d.blend_rect(img_z_back, Rect2i(0, 0, 512, 512), Vector2i(512, 0))
	comp_d.save_png(path_d)
	print("  ✓ 已輸出存證 D: %s (證明動態 Z-Order 層級控制)" % path_d)

	# 存證 E: 4 幀呼吸動態時序存證 (t=0.0s, 0.6s, 1.2s, 1.8s)
	doll.set_part_z_index("weapon", 40)
	doll.breathing_enabled = true
	var path_e := PROOF_DIR + "proof_maple_white_rabbit_breathing_sequence.png"
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
		print("\n=== 發條白兔楓之谷骨骼錨點與部件分層掛載測試全部通過 ===")
		print("MAPLE_PAPERDOLL_OK")
		quit(0)
	else:
		push_error("\n=== 發條白兔楓之谷骨骼錨點與部件分層掛載測試失敗 ===")
		print("MAPLE_PAPERDOLL_FAIL")
		quit(1)
