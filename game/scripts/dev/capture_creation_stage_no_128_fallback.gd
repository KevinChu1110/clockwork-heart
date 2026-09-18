extends SceneTree
## 《發條之心》開局選族中央舞台無 128 退路實機截圖產生器 (xvfb 1280x720)
## 依據任務規格：
## 1. 開局選族兔族舞台成功路徑是高清 (512 高清紙娃娃，LINEAR)
## 2. 人為讓 512 合成失敗時舞台改讀立牌／showcase (LINEAR)，臉不是馬賽克，角色寬度以貼圖像素為準
## 3. 截圖為全景實機畫面 (1280x720)，有場景有 HUD，放 proofs/，過 0-QA18

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _demo: Node = null

func _initialize() -> void:
	print("=== 開始產生開局選族中央舞台無 128 退路實機截圖 (xvfb 1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/creation_stage_no_128_fallback")
	_proofs_dir = base.path_join("../proofs")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	DirAccess.make_dir_recursive_absolute(_proofs_dir)

	_run_captures()


func _wait_frames(n: int) -> void:
	for i in range(n):
		await process_frame


func _capture_frame(filename: String) -> void:
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	if img:
		var p1 := _out_dir.path_join(filename)
		var err1 := img.save_png(p1)
		var p2 := _proofs_dir.path_join(filename)
		var err2 := img.save_png(p2)
		if err1 == OK and err2 == OK:
			print("  ✓ 成功存證截圖至: %s 與 %s" % [p1, p2])
		else:
			push_error("截圖儲存失敗: %s" % filename)


func _run_captures() -> void:
	await _wait_frames(5)

	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)

	await _wait_frames(10)

	# ── 1. 兔族舞台成功路徑 (512 高清紙娃娃) ──
	print("\n>>> [1/2 成功路徑] 開局選族兔族中央舞台 512 高清紙娃娃...")
	_demo.call("select_race", "rabbit")
	_demo.call("reset_to_default")
	await _wait_frames(15)

	var is_rab_512: bool = bool(_demo.call("is_stage_512"))
	var rab_tex: Texture2D = _demo.call("get_stage_texture")
	var rab_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	var ch1 = _demo.call("_get_character")
	var layers1 = ch1.get_node_or_null("Layers") as CanvasItem if ch1 else null

	print("  [成功路徑] is_stage_512: %s, 貼圖路徑: %s, 尺寸: %s, 濾鏡: %d (2=LINEAR), layers.visible: %s" % [
		str(is_rab_512),
		rab_tex.resource_path if rab_tex else "null",
		str(rab_tex.get_size()) if rab_tex else "null",
		rab_sprite.texture_filter if rab_sprite else -1,
		str(layers1.visible) if layers1 else "null"
	])
	assert(is_rab_512, "兔族舞台未正確走 512 高清合成")
	assert(rab_tex.get_width() == 512 and rab_tex.get_height() == 512, "兔族成功路徑貼圖尺寸非 512x512")
	assert(rab_sprite.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR, "濾鏡非 LINEAR")
	assert(layers1 != null and not layers1.visible, "128 Layers 疊層未隱藏")

	await _capture_frame("proof_creation_rabbit_stage_512_hd.png")

	# ── 2. 人為讓 512 合成失敗時，改讀官方立牌／showcase ──
	print("\n>>> [2/2 失敗退路] 人為讓 512 合成失敗，改讀官方立牌／showcase (LINEAR)...")
	_demo.set("force_composite_512_fail", true)
	_demo.call("select_race", "rabbit")
	_demo.call("reset_to_default")
	await _wait_frames(15)

	var is_fail_fallback: bool = bool(_demo.call("is_stage_512"))
	var fb_tex: Texture2D = _demo.call("get_stage_texture")
	var fb_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	var ch2 = _demo.call("_get_character")
	var layers2 = ch2.get_node_or_null("Layers") as CanvasItem if ch2 else null

	var fb_rendered_w: float = float(fb_tex.get_width()) * fb_sprite.scale.x if fb_tex and fb_sprite else 0.0

	print("  [失敗退路] 貼圖路徑: %s, 尺寸: %s, 濾鏡: %d (2=LINEAR), scale: %s, 換算角色寬度: %f, layers.visible: %s" % [
		fb_tex.resource_path if fb_tex else "null",
		str(fb_tex.get_size()) if fb_tex else "null",
		fb_sprite.texture_filter if fb_sprite else -1,
		str(fb_sprite.scale) if fb_sprite else "null",
		fb_rendered_w,
		str(layers2.visible) if layers2 else "null"
	])
	assert(fb_tex != null and fb_tex.get_width() >= 256, "失敗退路貼圖為空或寬度小於 256")
	assert(fb_sprite.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR, "失敗退路濾鏡非 LINEAR")
	assert(abs(fb_rendered_w - 128.0) < 0.1, "角色縮放寬度未按貼圖像素精確換算為 128: %f" % fb_rendered_w)
	assert(layers2 != null and not layers2.visible, "失敗時錯誤退回 128 切片疊層！")

	await _capture_frame("proof_creation_rabbit_stage_fallback_hd.png")

	print("\n=== 開局選族中央舞台無 128 退路截圖產生完畢 ===")
	_demo.queue_free()
	quit(0)
