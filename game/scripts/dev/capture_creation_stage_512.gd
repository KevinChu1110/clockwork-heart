extends SceneTree
## 《發條之心》開局選族中央舞台 512 高清合成實機截圖產生器 (xvfb 1280x720)
## 依據任務規格：
## 實機 xvfb 1280×720 三張：兔、狐、鶴（或任一非兔）舞台全景，有場景有 HUD，放 proofs/，過 0-QA18。貼圖寬高 512。

const DemoScene = preload("res://scenes/ui/paperdoll_select_demo.tscn")

var _out_dir: String = ""
var _proofs_dir: String = ""
var _demo: Node = null


func _initialize() -> void:
	print("=== 開始產生開局選族中央舞台 512 實機截圖 (xvfb 1280x720) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../proofs/creation_stage_512")
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
			print("  ✓ 成功存證截圖至 proofs: ", filename)
		else:
			push_error("截圖儲存失敗: %s" % filename)


func _run_captures() -> void:
	await _wait_frames(5)

	_demo = DemoScene.instantiate()
	_demo.set("creation_mode", true)
	root.add_child(_demo)

	await _wait_frames(10)

	# ── 1. 兔族 (rabbit) 512 中央舞台 ──
	print("\n>>> [1/4 兔族] 選取兔族 (costume_nutcracker_guard + paint_ivory_stock)...")
	_demo.call("select_race", "rabbit")
	_demo.call("reset_to_default")
	await _wait_frames(12)

	var is_rab_512: bool = bool(_demo.call("is_stage_512"))
	var rab_tex: Texture2D = _demo.call("get_stage_texture")
	var rab_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	print("  [兔族舞台] is_stage_512: %s, 貼圖尺寸: %s, 濾鏡: %d" % [
		str(is_rab_512),
		str(rab_tex.get_size()) if rab_tex else "null",
		rab_sprite.texture_filter if rab_sprite else -1
	])
	assert(is_rab_512, "兔族舞台未正確走 512 合成")
	assert(rab_tex.get_width() == 512 and rab_tex.get_height() == 512, "兔族貼圖尺寸非 512x512")
	await _capture_frame("proof_creation_stage_rabbit_512.png")

	# ── 2. 狐族 (fox) 512 中央舞台 ──
	print("\n>>> [2/4 狐族] 選取靈尾狐 (costume_astral_cape + paint_fox_orange)...")
	_demo.call("select_race", "fox")
	await _wait_frames(12)

	var is_fox_512: bool = bool(_demo.call("is_stage_512"))
	var fox_tex: Texture2D = _demo.call("get_stage_texture")
	var fox_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	print("  [狐族舞台] is_stage_512: %s, 貼圖尺寸: %s, 濾鏡: %d" % [
		str(is_fox_512),
		str(fox_tex.get_size()) if fox_tex else "null",
		fox_sprite.texture_filter if fox_sprite else -1
	])
	assert(is_fox_512, "狐族舞台未正確走 512 合成")
	assert(fox_tex.get_width() == 512 and fox_tex.get_height() == 512, "狐族貼圖尺寸非 512x512")
	await _capture_frame("proof_creation_stage_fox_512.png")

	# ── 3. 鶴族 (crane) 512 中央舞台 (切換至 512 裸機素體) ──
	print("\n>>> [3/4 鶴族] 選取雲嵐鶴並切換至無外裝裸機素體 (512 完整高光板件)...")
	_demo.call("select_race", "crane")
	# 點兩次切換外裝至 none (0: zephyr_robe -> 1: sky_hunter -> 2: none)
	_demo.call("_on_costume_next_pressed")
	_demo.call("_on_costume_next_pressed")
	await _wait_frames(12)

	var is_crane_512: bool = bool(_demo.call("is_stage_512"))
	var crane_tex: Texture2D = _demo.call("get_stage_texture")
	var crane_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	print("  [鶴族舞台] is_stage_512: %s, 貼圖尺寸: %s, 濾鏡: %d" % [
		str(is_crane_512),
		str(crane_tex.get_size()) if crane_tex else "null",
		crane_sprite.texture_filter if crane_sprite else -1
	])
	assert(is_crane_512, "鶴族舞台未正確走 512 合成")
	assert(crane_tex.get_width() == 512 and crane_tex.get_height() == 512, "鶴族貼圖尺寸非 512x512")
	await _capture_frame("proof_creation_stage_crane_512.png")

	# ── 4. 獅族 (lion) 512 中央舞台 (備援非兔族驗證：胡桃鉗軍裝) ──
	print("\n>>> [4/4 獅族] 選取烈鬃獅 (costume_nutcracker_guard + paint_brass_gold)...")
	_demo.call("select_race", "lion")
	_demo.call("reset_to_default")
	await _wait_frames(12)

	var is_lion_512: bool = bool(_demo.call("is_stage_512"))
	var lion_tex: Texture2D = _demo.call("get_stage_texture")
	var lion_sprite: Sprite2D = _demo.call("get_stage_sprite_512")
	print("  [獅族舞台] is_stage_512: %s, 貼圖尺寸: %s, 濾鏡: %d" % [
		str(is_lion_512),
		str(lion_tex.get_size()) if lion_tex else "null",
		lion_sprite.texture_filter if lion_sprite else -1
	])
	assert(is_lion_512, "獅族舞台未正確走 512 合成")
	assert(lion_tex.get_width() == 512 and lion_tex.get_height() == 512, "獅族貼圖尺寸非 512x512")
	await _capture_frame("proof_creation_stage_lion_512.png")

	print("\n=== 開局選族中央舞台 512 截圖生成完畢 ===")
	_demo.queue_free()
	quit(0)
