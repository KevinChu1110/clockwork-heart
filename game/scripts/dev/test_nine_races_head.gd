extends SceneTree

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	print("=== 測試九族 512 合成與頭部截圖 ===")
	var races := ["rabbit", "fox", "lion", "penguin", "bear", "tiger", "crane", "macaque", "boar"]
	var dir := "res://../proofs/qa_round13/head_audit"
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(dir))

	for r in races:
		var tex: Texture2D = PaperdollRenderer.build_composite_texture_512(r, {"costume": "none"})
		if tex == null:
			print("❌ %s 512 合成失敗 (null)" % r)
			continue
		var img := tex.get_image()
		if img == null:
			print("❌ %s 512 取得圖片失敗" % r)
			continue
		var full_path := ProjectSettings.globalize_path(dir.path_join("godot_comp_%s.png" % r))
		img.save_png(full_path)
		# 裁切頭部 (約 x:80..430, y:20..320)
		var head_rect := Rect2i(80, 20, 350, 300)
		var head_img := img.get_region(head_rect)
		var head_path := ProjectSettings.globalize_path(dir.path_join("godot_head_%s.png" % r))
		head_img.save_png(head_path)
		print("✓ %s: 512 合成成功，已存檔至 %s" % [r, head_path])

	quit(0)
