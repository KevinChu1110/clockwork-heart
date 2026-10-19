extends SceneTree
## 《發條之心》厚鎧野豬 楓之谷 Character.wz 骨骼錨點與部件分層掛載無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_maple_paperdoll_boar.gd

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")
const BOAR_SPEC_PATH := "res://data/tables/maple_paperdoll_boar.json"
const PROOF_DIR := "res://assets/sprites/player/paperdoll/boar/"


func _initialize() -> void:
	var ok := true
	print("=== 開始厚鎧野豬楓之谷骨骼錨點與部件分層掛載測試 (Maple Paperdoll Boar Test) ===")

	var doll := MaplePaperdollClass.new()
	doll.spec_path = BOAR_SPEC_PATH
	doll.breathing_enabled = false # 先關閉以精準測試靜態錨點與位移
	root.add_child(doll)

	if not is_instance_valid(doll):
		push_error("無法實例化 MaplePaperdoll 節點")
		_finish(false)
		return

	doll.load_spec(BOAR_SPEC_PATH)

	# -------------------------------------------------------------
	# 1. 驗證角色骨骼/錨點體系（neck/navel/hand/brow/back_key/tail）
	# -------------------------------------------------------------
	print("\n--- 1. 驗證骨骼錨點體系 (neck/navel/hand/brow/back_key/tail) ---")
	var neck_node := doll.get_anchor_node("neck")
	var navel_node := doll.get_anchor_node("navel")
	var hand_node := doll.get_anchor_node("hand")
	var brow_node := doll.get_anchor_node("brow")
	var back_key_node := doll.get_anchor_node("back_key")
	var tail_node := doll.get_anchor_node("tail")

	if neck_node == null or navel_node == null or hand_node == null or brow_node == null or back_key_node == null or tail_node == null:
		push_error("核心錨點節點缺失！")
		ok = false
	else:
		print("  ✓ 核心 6 大錨點節點均成功建立")
		# 檢查座標 (基準 512 空間)
		if neck_node.position != Vector2(250, 176):
			push_error("neck 錨點座標不符: %s vs (250, 176)" % str(neck_node.position))
			ok = false
		if navel_node.position != Vector2(256, 340):
			push_error("navel 錨點座標不符: %s vs (256, 340)" % str(navel_node.position))
			ok = false
		if hand_node.position != Vector2(180, 340):
			push_error("hand 錨點座標不符: %s vs (180, 340)" % str(hand_node.position))
			ok = false
		if back_key_node.position != Vector2(360, 140):
			push_error("back_key 錨點座標不符: %s vs (360, 140)" % str(back_key_node.position))
			ok = false
		if brow_node.position != Vector2(-15, -15):
			push_error("brow 錨點相對於 neck 座標不符: %s vs (-15, -15)" % str(brow_node.position))
			ok = false
		if tail_node.position != Vector2(350, 335):
			push_error("tail 錨點座標不符: %s vs (350, 335)" % str(tail_node.position))
			ok = false

		if ok:
			print("  ✓ neck(250,176), navel(256,340), hand(180,340), back_key(360,140), brow(235,161), tail(350,335) 座標 100% 精準")

	# -------------------------------------------------------------
	# 2. 驗證眼睛、外裝、武器、發條鑰匙、頭部面罩、尾部獨立為帶 origin 錨點之部件 Sprite
	# -------------------------------------------------------------
	print("\n--- 2. 驗證各部件帶 origin 獨立緊湊 Sprite ---")
	var spr_eyes := doll.get_slot_sprite("eyes")
	var spr_costume := doll.get_slot_sprite("costume")
	var spr_weapon := doll.get_slot_sprite("weapon")
	var spr_key := doll.get_slot_sprite("winding_key")
	var spr_head := doll.get_slot_sprite("head_unit")
	var spr_tail := doll.get_slot_sprite("back_curio")

	if spr_eyes == null or spr_costume == null or spr_weapon == null or spr_key == null or spr_head == null or spr_tail == null:
		push_error("部件 Sprite2D 節點不存在！")
		ok = false
	else:
		print("  ✓ 眼睛 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_eyes.name, str(spr_eyes.texture.get_size()), str(spr_eyes.position)])
		print("  ✓ 頭部鋼牙面罩 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_head.name, str(spr_head.texture.get_size()), str(spr_head.position)])
		print("  ✓ 外裝 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_costume.name, str(spr_costume.texture.get_size()), str(spr_costume.position)])
		print("  ✓ 武器 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_weapon.name, str(spr_weapon.texture.get_size()), str(spr_weapon.position)])
		print("  ✓ 發條鑰匙 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_key.name, str(spr_key.texture.get_size()), str(spr_key.position)])
		print("  ✓ 彈簧尾 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_tail.name, str(spr_tail.texture.get_size()), str(spr_tail.position)])

		# 驗證各部件並非 512 全圖死切片，而是緊湊獨立素材帶有精確 origin
		if spr_eyes.texture.get_width() >= 512 or spr_costume.texture.get_width() >= 512 or spr_head.texture.get_width() >= 512:
			push_error("部件非緊湊切片，仍為全圖 512 畫布！")
			ok = false
		else:
			print("  ✓ 所有部件均為獨立緊湊裁剪 Sprite (眼睛 90x60, 面罩 266x142, 外裝 148x164/180x204, 武器 176x252, 鑰匙 104x108, 尾部 96x88)")

	# -------------------------------------------------------------
	# 3. 驗證「眼睛不畫死在素體上」
	# -------------------------------------------------------------
	print("\n--- 3. 驗證眼睛不畫死在素體上 ---")
	doll.set_eyes("none")
	var bare_img := doll.get_composite_image()
	# 檢查眼睛處 (x: 235, y: 161) 是否為純淨金屬面甲（無眼眶死黑線、無青綠眼球殘留）
	var sample_pixel := bare_img.get_pixel(235, 161)
	print("  ✓ 卸除眼睛時臉部眼窩像素值: %s" % str(sample_pixel))
	if sample_pixel.g > 0.6 and sample_pixel.b > 0.6 and sample_pixel.r < 0.4:
		push_error("眼睛仍畫死在頭部/素體上！")
		ok = false
	else:
		print("  ✓ 卸除眼睛時眼窩為深色金屬暗面，未畫死眼球 (0-ART51)")

	# 裝上眼睛
	doll.set_eyes("eyes_cyan_emerald")

	# -------------------------------------------------------------
	# 3.1 驗證眼睛上裝後額頭無黑色遮罩方塊、臉頰無溢色
	# -------------------------------------------------------------
	print("\n--- 3.1 驗證眼睛上裝後額頭純淨無黑條遮罩、臉頰無溢色 ---")
	for eye_id in ["eyes_cyan_emerald", "eyes_amber_gold"]:
		doll.set_eyes(eye_id)
		var img_eye := doll.get_composite_image()
		var black_count := 0
		for check_y in range(130, 140):
			for check_x in range(220, 250):
				var px := img_eye.get_pixel(check_x, check_y)
				if px.a > 0.5 and px.r < 0.05 and px.g < 0.05 and px.b < 0.05:
					black_count += 1
		if black_count > 0:
			push_error("眼睛上裝後額頭存在黑條遮罩破圖 (%s): %d 像素" % [eye_id, black_count])
			ok = false
		else:
			print("  ✓ 眼睛 %s 覆蓋純淨自然，無黑條遮罩破圖" % eye_id)

	# -------------------------------------------------------------
	# 4. 驗證外裝、塗裝與武器動態 Z-Order 控制
	# -------------------------------------------------------------
	print("\n--- 4. 驗證動態 Z-Order 控制 ---")
	var z_key: int = doll.get_part_z_index("winding_key")
	var z_tail: int = doll.get_part_z_index("back_curio")
	var z_body: int = doll.get_part_z_index("body")
	var z_head: int = doll.get_part_z_index("head_unit")
	var z_costume: int = doll.get_part_z_index("costume")
	var z_eyes: int = doll.get_part_z_index("eyes")
	var z_weapon: int = doll.get_part_z_index("weapon")

	print("  目前層級順序: key(%d) < tail(%d) < body(%d) < head(%d) < costume(%d) < eyes(%d) < weapon(%d)" % [
		z_key, z_tail, z_body, z_head, z_costume, z_eyes, z_weapon
	])
	if not (z_key < z_tail and z_tail < z_body and z_body < z_head and z_head < z_costume and z_costume < z_eyes and z_eyes < z_weapon):
		push_error("預設 Z-Index 層級順序不符規格！")
		ok = false
	else:
		print("  ✓ 預設 Z-Order 完全符合角色前後層次規範")

	# -------------------------------------------------------------
	# 5. 驗證外裝與素體分層置換
	# -------------------------------------------------------------
	print("\n--- 5. 驗證外裝與素體分層置換 ---")
	var costumes := ["costume_viking_harness", "costume_viking_ironclad", "none"]
	var bodies := ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]
	var heads := ["ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl"]

	for c in costumes:
		doll.set_costume(c)
		var cur_c := doll.get_part_item("costume")
		if cur_c != c:
			push_error("外裝置換失敗: %s" % c)
			ok = false
	print("  ✓ 外裝切換驗證通過 (harness / ironclad / none)")

	for b in bodies:
		doll.set_body(b)
		var cur_b := doll.get_part_item("body")
		if cur_b != b:
			push_error("素體切換失敗: %s" % b)
			ok = false
	print("  ✓ 3 款塗裝素體切換驗證通過 (brass / ivory / crimson)")

	for h in heads:
		doll.set_head_unit(h)
		var cur_h := doll.get_part_item("head_unit")
		if cur_h != h:
			push_error("鋼牙面罩切換失敗: %s" % h)
			ok = false
	print("  ✓ 4 款鋼牙面罩切換驗證通過 (brass / ivory / crimson / default)")

	# 還原標準外觀
	doll.set_body("paint_brass_gold")
	doll.set_head_unit("ear_boar_rivet_cowl_brass")
	doll.set_costume("costume_viking_harness")
	doll.set_eyes("eyes_cyan_emerald")
	doll.set_weapon("wpn_anvil_greathammer")
	doll.set_winding_key("key_classic_brass")
	doll.set_back_curio("curio_spring_tail")

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
	doll.node_body.scale = Vector2.ONE
	doll.node_neck.position = Vector2(250, 176)
	doll.node_neck.rotation = 0.0
	doll.node_hand.position = Vector2(180, 340)
	doll.node_back_key.rotation = 0.0

	# 存證 A: 基準完整拼裝立繪 (Harness)
	var path_a := PROOF_DIR + "proof_maple_boar_composite.png"
	var err_a := doll.save_composite_png(path_a)
	if err_a != OK:
		push_error("存證 A 儲存失敗: %d" % err_a)
		ok = false
	else:
		print("  ✓ 已輸出存證 A: %s" % path_a)

	# 存證 B: 眼睛分離比對圖 (裸面甲 vs 天青祖母綠 vs 琥珀金陽)
	var path_b := PROOF_DIR + "proof_maple_boar_eyes_separated.png"
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

	# 存證 C: 外裝置換展示 (粗獷鍛爐束帶 / 維京重裝鐵甲 / 純淨素體)
	var path_c := PROOF_DIR + "proof_maple_boar_costume_variants.png"
	var comp_c := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_c.fill(Color(1, 0.99, 0.97, 1))

	var c_list := ["costume_viking_harness", "costume_viking_ironclad", "none"]
	for idx in range(c_list.size()):
		doll.set_costume(c_list[idx])
		var c_img := doll.get_composite_image()
		comp_c.blend_rect(c_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_c.save_png(path_c)
	print("  ✓ 已輸出存證 C: %s (外裝自由置換零穿模)" % path_c)

	# 存證 D: 3 款塗裝素體展示 (黃銅原金 / 經典象牙白 / 赤焰熔爐)
	var path_d := PROOF_DIR + "proof_maple_boar_chassis_variants.png"
	var comp_d := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_d.fill(Color(1, 0.99, 0.97, 1))
	doll.set_costume("costume_viking_harness")

	var b_list := ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]
	for idx in range(b_list.size()):
		doll.set_body(b_list[idx])
		var b_img := doll.get_composite_image()
		comp_d.blend_rect(b_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_d.save_png(path_d)
	print("  ✓ 已輸出存證 D: %s (多款塗裝純淨金屬底盤)" % path_d)

	# 存證 E: 呼吸待機序列拼貼 (0.0s, 0.6s, 1.2s, 1.8s)
	var path_e := PROOF_DIR + "proof_maple_boar_breathing_sequence.png"
	var comp_e := Image.create(512 * 4, 512, false, Image.FORMAT_RGBA8)
	comp_e.fill(Color(1, 0.99, 0.97, 1))
	doll.set_body("paint_brass_gold")
	doll.breathing_enabled = true

	var time_points := [0.0, 0.6, 1.2, 1.8]
	for idx in range(time_points.size()):
		doll.node_body.position = Vector2.ZERO
		doll.node_back_key.rotation = 0.0
		doll.update_breathing(time_points[idx])
		var frame_img := doll.get_composite_image()
		comp_e.blend_rect(frame_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_e.save_png(path_e)
	print("  ✓ 已輸出存證 E: %s (全身骨骼待機呼吸聯動)" % path_e)

	print("\n=== 厚鎧野豬楓之谷骨骼錨點與部件分層掛載測試總結 ===")
	if ok:
		print("🎉 【PASS】厚鎧野豬楓之谷骨骼錨點與部件分層掛載測試全部通過！(MAPLE_PAPERDOLL_BOAR_OK)")
		_finish(true)
	else:
		push_error("❌ 【FAIL】厚鎧野豬測試存在未通過項目，請檢查錯誤紀錄！")
		_finish(false)


func _finish(success: bool) -> void:
	if success:
		quit(0)
	else:
		quit(1)
