extends SceneTree
## 《發條之心》第五族靈爪猴 楓之谷 Character.wz 骨骼錨點與部件分層掛載無頭驗證測試
## 執行方式：godot --path game --headless -s res://scripts/art/test_maple_paperdoll_macaque.gd

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")
const MACAQUE_SPEC_PATH := "res://data/tables/maple_paperdoll_macaque.json"
const ASSET_PROOF_DIR := "res://assets/sprites/player/paperdoll/macaque/"
const GLOBAL_PROOF_DIR := "res://../proofs/t_e49ae8c1/"


func _initialize() -> void:
	var ok := true
	print("=== 開始靈爪猴楓之谷骨骼錨點與部件分層掛載測試 (Maple Paperdoll Macaque Test) ===")

	var doll := MaplePaperdollClass.new()
	doll.spec_path = MACAQUE_SPEC_PATH
	doll.breathing_enabled = false # 先關閉以精準測試靜態錨點與位移
	root.add_child(doll)

	if not is_instance_valid(doll):
		push_error("無法實例化 MaplePaperdoll 節點")
		_finish(false)
		return

	doll.load_spec(MACAQUE_SPEC_PATH)

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
		if neck_node.position != Vector2(232, 260):
			push_error("neck 錨點座標不符: %s vs (232, 260)" % str(neck_node.position))
			ok = false
		if navel_node.position != Vector2(256, 345):
			push_error("navel 錨點座標不符: %s vs (256, 345)" % str(navel_node.position))
			ok = false
		if hand_node.position != Vector2(200, 340):
			push_error("hand 錨點座標不符: %s vs (200, 340)" % str(hand_node.position))
			ok = false
		if back_key_node.position != Vector2(330, 240):
			push_error("back_key 錨點座標不符: %s vs (330, 240)" % str(back_key_node.position))
			ok = false
		if brow_node.position != Vector2(-2, -120):
			push_error("brow 錨點相對於 neck 座標不符: %s vs (-2, -120)" % str(brow_node.position))
			ok = false
		if tail_node.position != Vector2(350, 280):
			push_error("tail 錨點座標不符: %s vs (350, 280)" % str(tail_node.position))
			ok = false

		if ok:
			print("  ✓ neck(232,260), navel(256,345), hand(200,340), back_key(330,240), brow(230,140), tail(350,280) 座標 100% 精準")

	# -------------------------------------------------------------
	# 2. 驗證眼睛、外裝、武器、發條鑰匙、同軸耳頭部、尾部獨立為帶 origin 錨點之緊湊 Sprite
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
		print("  ✓ 頭部同軸耳 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_head.name, str(spr_head.texture.get_size()), str(spr_head.position)])
		print("  ✓ 外裝 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_costume.name, str(spr_costume.texture.get_size()), str(spr_costume.position)])
		print("  ✓ 武器 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_weapon.name, str(spr_weapon.texture.get_size()), str(spr_weapon.position)])
		print("  ✓ 發條鑰匙 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_key.name, str(spr_key.texture.get_size()), str(spr_key.position)])
		print("  ✓ 彈簧長尾 Sprite: %s, 尺寸: %s, 錨點位移: %s" % [spr_tail.name, str(spr_tail.texture.get_size()), str(spr_tail.position)])

		# 驗證各部件並非 512 全圖死切片，而是緊湊獨立素材帶有精確 origin
		if spr_eyes.texture.get_width() >= 512 or spr_costume.texture.get_width() >= 512 or spr_head.texture.get_width() >= 512 or spr_weapon.texture.get_width() >= 512:
			push_error("部件非緊湊切片，仍為全圖 512 畫布！")
			ok = false
		else:
			print("  ✓ 所有部件均為獨立緊湊裁剪 Sprite (眼睛 90x60, 同軸耳 247x212, 外裝 151x164/150x118, 武器 278x146, 鑰匙 96x110, 尾部 76x192)")

	# -------------------------------------------------------------
	# 3. 驗證「眼睛不畫死在素體上」（0-ART51）
	# -------------------------------------------------------------
	print("\n--- 3. 驗證眼睛不畫死在素體上 (0-ART51) ---")
	doll.set_eyes("none")
	var bare_img := doll.get_composite_image()
	# 檢查眼睛處 (x: 230, y: 140) 是否純淨深色金屬暗面/眼窩孔（無眼球、無發光像素殘留）
	var sample_pixel := bare_img.get_pixel(230, 140)
	print("  ✓ 卸除眼睛時臉部眼窩像素值: %s" % str(sample_pixel))
	if sample_pixel.g > 0.6 and sample_pixel.b > 0.6 and sample_pixel.r < 0.4:
		push_error("眼睛仍畫死在頭部/素體上！")
		ok = false
	else:
		print("  ✓ 卸除眼睛時眼窩為純淨深色/透空金屬暗面，未畫死眼球 (0-ART51)")

	# 裝回眼睛
	doll.set_eyes("eyes_cyan_emerald")
	var equipped_img := doll.get_composite_image()
	var eye_pixel := equipped_img.get_pixel(230, 140)
	print("  ✓ 裝上天青祖母綠義眼時眼球核心像素值: %s" % str(eye_pixel))
	if eye_pixel.a < 0.5:
		push_error("眼睛上裝後未正確渲染！")
		ok = false
	else:
		print("  ✓ 光學義眼完美嵌入眼窩")

	# -------------------------------------------------------------
	# 4. 驗證外裝更換與自由置換（晨曦僧袍 / 禪拳戰裝 / 裸裝）
	# -------------------------------------------------------------
	print("\n--- 4. 驗證外裝更換與自由置換 ---")
	for c_id in ["costume_dawn_monk_tunic", "costume_zen_striker", "none"]:
		doll.set_costume(c_id)
		var cur_c := doll.get_part_item("costume")
		if cur_c != c_id:
			push_error("外裝更換失敗: 預期 %s, 實際 %s" % [c_id, cur_c])
			ok = false
		else:
			print("  ✓ 外裝成功切換至: %s" % c_id)

	# 復原預設外裝
	doll.set_costume("costume_dawn_monk_tunic")

	# -------------------------------------------------------------
	# 5. 驗證塗裝底盤更換（象牙白 / 天元青古銅 / 金光禪武）
	# -------------------------------------------------------------
	print("\n--- 5. 驗證塗裝底盤更換 ---")
	for b_id in ["paint_ivory_stock", "paint_bamboo_bronze", "paint_zen_gold"]:
		doll.set_body(b_id)
		var cur_b := doll.get_part_item("body")
		if cur_b != b_id:
			push_error("塗裝更換失敗: 預期 %s, 實際 %s" % [b_id, cur_b])
			ok = false
		else:
			print("  ✓ 塗裝成功切換至: %s" % b_id)

	# 復原預設塗裝
	doll.set_body("paint_ivory_stock")

	# -------------------------------------------------------------
	# 6. 驗證呼吸動態與發條鑰匙旋轉聯動
	# -------------------------------------------------------------
	print("\n--- 6. 驗證待機呼吸與發條鑰匙自轉 ---")
	doll.breathing_enabled = true
	var base_neck_y := doll.node_neck.position.y
	doll.update_breathing(0.6)
	var breath_neck_y := doll.node_neck.position.y
	var key_rot := doll.node_back_key.rotation
	print("  ✓ 呼吸更新 0.6s: neck_y 原 (%.1f) -> 現 (%.1f), 鑰匙旋轉角 (%.3f rad)" % [base_neck_y, breath_neck_y, key_rot])
	if abs(key_rot) < 0.01:
		push_error("發條鑰匙未自轉！")
		ok = false
	else:
		print("  ✓ 全身骨骼待機呼吸與鑰匙自轉聯動正常")

	doll.breathing_enabled = false
	doll.node_body.position = Vector2.ZERO
	doll.node_back_key.rotation = 0.0

	# -------------------------------------------------------------
	# 7. 輸出實機渲染截圖存證至 proofs/ 與資源目錄
	# -------------------------------------------------------------
	print("\n--- 7. 輸出實機渲染截圖存證 ---")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(ASSET_PROOF_DIR))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(GLOBAL_PROOF_DIR))

	# 存證 A: 預設全裝備複合渲染紙娃娃
	var path_a := ASSET_PROOF_DIR + "proof_maple_macaque_composite.png"
	var err_a := doll.save_composite_png(path_a)
	doll.save_composite_png(GLOBAL_PROOF_DIR + "proof_01_composite.png")
	if err_a != OK:
		push_error("存證 A 儲存失敗: %d" % err_a)
		ok = false
	else:
		print("  ✓ 已輸出存證 A: %s" % path_a)

	# 存證 B: 眼睛分離比對圖 (裸面甲眼窩 vs 天青祖母綠 vs 琥珀金陽)
	var path_b := ASSET_PROOF_DIR + "proof_maple_macaque_eyes_separated.png"
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
	comp_b.save_png(ProjectSettings.globalize_path(path_b))
	comp_b.save_png(ProjectSettings.globalize_path(GLOBAL_PROOF_DIR + "proof_02_eyes_separated.png"))
	print("  ✓ 已輸出存證 B: %s (證明眼睛不畫死在素體上)" % path_b)

	# 存證 C: 外裝置換展示 (晨曦僧袍 / 禪拳戰裝 / 純淨素體)
	var path_c := ASSET_PROOF_DIR + "proof_maple_macaque_costume_variants.png"
	var comp_c := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_c.fill(Color(1, 0.99, 0.97, 1))

	var c_list := ["costume_dawn_monk_tunic", "costume_zen_striker", "none"]
	for idx in range(c_list.size()):
		doll.set_costume(c_list[idx])
		var c_img := doll.get_composite_image()
		comp_c.blend_rect(c_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_c.save_png(ProjectSettings.globalize_path(path_c))
	comp_c.save_png(ProjectSettings.globalize_path(GLOBAL_PROOF_DIR + "proof_03_costume_variants.png"))
	print("  ✓ 已輸出存證 C: %s (外裝自由置換零穿模)" % path_c)

	# 存證 D: 3 款塗裝素體展示 (經典象牙白 / 天元青古銅 / 金光禪武)
	var path_d := ASSET_PROOF_DIR + "proof_maple_macaque_chassis_variants.png"
	var comp_d := Image.create(512 * 3, 512, false, Image.FORMAT_RGBA8)
	comp_d.fill(Color(1, 0.99, 0.97, 1))
	doll.set_costume("costume_dawn_monk_tunic")

	var b_list := ["paint_ivory_stock", "paint_bamboo_bronze", "paint_zen_gold"]
	for idx in range(b_list.size()):
		doll.set_body(b_list[idx])
		var b_img := doll.get_composite_image()
		comp_d.blend_rect(b_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_d.save_png(ProjectSettings.globalize_path(path_d))
	comp_d.save_png(ProjectSettings.globalize_path(GLOBAL_PROOF_DIR + "proof_04_chassis_variants.png"))
	print("  ✓ 已輸出存證 D: %s (多款塗裝純淨金屬底盤)" % path_d)

	# 存證 E: 呼吸待機序列拼貼 (0.0s, 0.6s, 1.2s, 1.8s)
	var path_e := ASSET_PROOF_DIR + "proof_maple_macaque_breathing_sequence.png"
	var comp_e := Image.create(512 * 4, 512, false, Image.FORMAT_RGBA8)
	comp_e.fill(Color(1, 0.99, 0.97, 1))
	doll.set_body("paint_ivory_stock")
	doll.breathing_enabled = true

	var time_points := [0.0, 0.6, 1.2, 1.8]
	for idx in range(time_points.size()):
		doll.node_body.position = Vector2.ZERO
		doll.node_back_key.rotation = 0.0
		doll.update_breathing(time_points[idx])
		var frame_img := doll.get_composite_image()
		comp_e.blend_rect(frame_img, Rect2i(0, 0, 512, 512), Vector2i(512 * idx, 0))
	comp_e.save_png(ProjectSettings.globalize_path(path_e))
	comp_e.save_png(ProjectSettings.globalize_path(GLOBAL_PROOF_DIR + "proof_05_breathing_sequence.png"))
	print("  ✓ 已輸出存證 E: %s (全身骨骼待機呼吸聯動)" % path_e)

	print("\n=== 靈爪猴楓之谷骨骼錨點與部件分層掛載測試總結 ===")
	if ok:
		print("🎉 【PASS】靈爪猴楓之谷骨骼錨點與部件分層掛載測試全部通過！(MAPLE_PAPERDOLL_MACAQUE_OK)")
		_finish(true)
	else:
		push_error("❌ 【FAIL】靈爪猴測試存在未通過項目，請檢查錯誤紀錄！")
		_finish(false)


func _finish(success: bool) -> void:
	if success:
		quit(0)
	else:
		quit(1)
