extends SceneTree
## 熊與企鵝頭部塗裝同步 512 高清合成與實機存證產生器

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

func _initialize() -> void:
	print("=== 開始生成熊與企鵝頭部塗裝同步 512 存證影像 ===")
	var base := ProjectSettings.globalize_path("res://")
	var out_dir := base.path_join("../proofs/head_sync_proofs")
	DirAccess.make_dir_recursive_absolute(out_dir)

	var targets := [
		{
			"fn": "composite_512_bear_amber.png",
			"race": "bear",
			"slots": {
				"chassis": "paint_bear_amber",
				"head_unit": "paint_bear_amber",
				"costume": "none"
			}
		},
		{
			"fn": "composite_512_bear_quarry.png",
			"race": "bear",
			"slots": {
				"chassis": "paint_iron_quarry",
				"head_unit": "paint_iron_quarry",
				"costume": "none"
			}
		},
		{
			"fn": "composite_512_penguin_polar.png",
			"race": "penguin",
			"slots": {
				"chassis": "paint_polar_frost",
				"head_unit": "paint_polar_frost",
				"costume": "none"
			}
		},
		{
			"fn": "composite_512_penguin_ivory.png",
			"race": "penguin",
			"slots": {
				"chassis": "paint_ivory_stock",
				"head_unit": "paint_ivory_stock",
				"costume": "none"
			}
		}
	]

	for t in targets:
		print("  合成: %s (%s)..." % [t.fn, t.race])
		var tex := PaperdollRenderer.build_composite_texture_512(t.race, t.slots)
		if tex == null:
			push_error("無法合成 512 貼圖: %s" % t.fn)
			continue
		var img := tex.get_image()
		if img == null or img.is_empty():
			push_error("合成影像為空: %s" % t.fn)
			continue
		var save_p := out_dir.path_join(t.fn)
		var err := img.save_png(save_p)
		if err == OK:
			print("    ✓ 成功存證: %s" % save_p)
		else:
			push_error("儲存失敗: %s" % save_p)

	print("=== 512 存證影像生成完畢 ===")
	quit(0)
