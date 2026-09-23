extends SceneTree
## 《發條之心》開局選族中央舞台 512 合成失敗不准退回 128 測試
## 依據任務規格：
## 1. 成功路徑走 512 高清紙娃娃 (LINEAR)
## 2. 512 合成失敗時，改讀官方立牌或本族 showcase 256 (LINEAR)，不准退回 128 模組切片疊層
## 3. 角色寬度以貼圖像素為準 (scale.x * width == 128.0)
## 4. 九族皆不准借別族圖

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

func _initialize() -> void:
	print("=== 開始測試開局選族中央舞台合成失敗不退 128 ===")
	var demo = DemoScene.instantiate()
	demo.set("creation_mode", true)
	root.add_child(demo)

	var races = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog"]

	# ── 1. 測試成功路徑 (512 高清紙娃娃) ──
	print("\n--- [Phase 1] 成功路徑 512 高清驗證 ---")
	for r in races:
		demo.call("select_race", r)
		var is_512: bool = bool(demo.call("is_stage_512"))
		var tex: Texture2D = demo.call("get_stage_texture")
		var sprite: Sprite2D = demo.call("get_stage_sprite_512")
		assert(tex != null, "種族 %s 舞台貼圖為 null" % r)
		assert(tex.get_width() >= 256, "種族 %s 舞台貼圖寬度小於 256: %d" % [r, tex.get_width()])
		assert(sprite != null and sprite.visible, "種族 %s 512 Sprite 未顯示" % r)
		assert(sprite.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR, "種族 %s 濾鏡非 LINEAR" % r)
		var ch = demo.call("_get_character")
		var layers = ch.get_node_or_null("Layers") as CanvasItem if ch else null
		assert(layers != null and not layers.visible, "種族 %s 128 Layers 疊層未隱藏" % r)
		print("  ✓ 成功路徑 [%-8s]: %dx%d, filter=%d, layers.visible=%s" % [
			r, tex.get_width(), tex.get_height(), sprite.texture_filter, str(layers.visible)
		])

	# ── 2. 測試人為讓 512 合成失敗時的退路 ──
	print("\n--- [Phase 2] 人為讓 512 合成失敗退路驗證 ---")
	demo.set("force_composite_512_fail", true)

	for r in races:
		demo.call("select_race", r)
		var tex: Texture2D = demo.call("get_stage_texture")
		var sprite: Sprite2D = demo.call("get_stage_sprite_512")
		assert(tex != null, "種族 %s 失敗退路貼圖為 null" % r)
		assert(tex.get_width() >= 256, "種族 %s 失敗退路貼圖寬度未達 256: %d" % [r, tex.get_width()])
		assert(sprite != null and sprite.visible, "種族 %s 失敗退路 Sprite 未顯示" % r)
		assert(sprite.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR, "種族 %s 失敗退路濾鏡非 LINEAR" % r)

		# 角色寬度以貼圖像素為準 (換算後寬度為 128px)
		var rendered_w: float = float(tex.get_width()) * sprite.scale.x
		assert(abs(rendered_w - 128.0) < 0.1, "種族 %s 角色縮放寬度非 128: %f" % [r, rendered_w])

		# 嚴禁退回 128 切片疊層
		var ch = demo.call("_get_character")
		var layers = ch.get_node_or_null("Layers") as CanvasItem if ch else null
		assert(layers != null and not layers.visible, "種族 %s 失敗時錯誤退回 128 切片疊層！" % r)

		# 驗證不借別族圖 (路徑必須包含本族名稱)
		var p: String = tex.resource_path
		assert(p.contains(r), "種族 %s 疑似跨族借圖: %s" % [r, p])

		print("  ✓ 失敗退路 [%-8s]: %dx%d (%s), scale=%s, filter=%d, layers.visible=%s" % [
			r, tex.get_width(), tex.get_height(), p.get_file(), str(sprite.scale), sprite.texture_filter, str(layers.visible)
		])

	# ── 3. 恢復正常並切換換裝驗證 ──
	demo.set("force_composite_512_fail", false)
	demo.call("select_race", "rabbit")
	var rab_tex: Texture2D = demo.call("get_stage_texture")
	assert(rab_tex.get_width() == 512 and rab_tex.get_height() == 512, "恢復後兔族非 512 合成")

	demo.queue_free()
	print("\nCREATION_STAGE_NO_128_FALLBACK_OK")
	quit(0)
