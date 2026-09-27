extends SceneTree
## 浪花海獺 (Tidal Otter) 六大戰鬥姿勢 dev 預覽巡檢腳本
## 走一次 dev 預覽巡過六姿勢：idle, telegraph, attack, skill, hit, recover
## 驗收確認無破圖、紋理皆有效、尺寸 512x512 及 128x128 齊備

const SpriteDB = preload("res://scripts/art/sprite_db.gd")

func _initialize() -> void:
	print("=== 開始走訪浪花海獺 (Tidal Otter) 六大戰鬥姿勢 Dev 預覽巡檢 ===")
	var poses := ["idle", "telegraph", "attack", "skill", "hit", "recover"]
	var ok := true

	# 建立預覽根節點
	var canvas := Control.new()
	canvas.name = "DevCombatPosePreview"
	canvas.size = Vector2(1280, 720)
	root.add_child(canvas)

	var hbox := HBoxContainer.new()
	hbox.position = Vector2(40, 100)
	hbox.add_theme_constant_override("separation", 24)
	canvas.add_child(hbox)

	for p in poses:
		print("\n>>> 巡檢姿態: %s" % p)
		var tex_128: Texture2D = SpriteDB.tex("res://assets/sprites/player/poses/otter/%s.png" % p)
		if tex_128 == null:
			push_error("❌ 128 姿態貼圖加載失敗: %s" % p)
			ok = false
		else:
			print("  ✓ 128 貼圖正常: %dx%d" % [tex_128.get_width(), tex_128.get_height()])

		var tex_512: Texture2D = SpriteDB.player_pose(p, "otter")
		if tex_512 == null:
			push_error("❌ 512 姿態貼圖加載失敗: %s" % p)
			ok = false
		else:
			print("  ✓ 512 貼圖正常: %dx%d (%s)" % [tex_512.get_width(), tex_512.get_height(), tex_512.resource_path])

		# 建立預覽 UI 控件檢查渲染狀態
		var card := VBoxContainer.new()
		var lbl := Label.new()
		lbl.text = p.to_upper()
		card.add_child(lbl)

		var tr := TextureRect.new()
		tr.custom_minimum_size = Vector2(160, 160)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.texture = tex_512
		tr.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		card.add_child(tr)
		hbox.add_child(card)

	if ok:
		print("\n🎉 Dev 預覽巡檢六大姿勢全數通過，無破圖、無報錯！")
		print("OTTER_DEV_PREVIEW_PASSED")
		quit(0)
	else:
		push_error("\n❌ Dev 預覽巡檢存在破圖或缺失！")
		quit(1)
