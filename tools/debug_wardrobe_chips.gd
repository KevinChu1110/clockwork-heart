extends SceneTree

const WardrobeDialog = preload("res://scripts/ui/wardrobe_dialog.gd")

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var dlg := WardrobeDialog.new()
	root.add_child(dlg)
	
	# wait 10 frames
	for i in range(10):
		await process_frame
		
	print("--- Debugging Wardrobe Chips ---")
	print("current_filter_race: ", dlg.current_filter_race)
	print("_filter_chips keys: ", dlg._filter_chips.keys())
	for rid in dlg._filter_chips.keys():
		var btn: Button = dlg._filter_chips[rid]
		print("  Chip %-10s pos.x=%.1f size.x=%.1f visible=%s" % [rid, btn.position.x, btn.size.x, btn.visible])
		
	var scroll := dlg.find_child("FilterScroll", true, false) as ScrollContainer
	if scroll:
		var hbar := scroll.get_h_scroll_bar()
		print("FilterScroll size: ", scroll.size, " scroll_h: ", scroll.scroll_horizontal)
		if hbar:
			print("hbar min: ", hbar.min_value, " max: ", hbar.max_value, " page: ", hbar.page)
			
	print("\nCalling set_race_filter('fawn')...")
	dlg.set_race_filter("fawn")
	
	for i in range(10):
		await process_frame
		
	print("After set_race_filter('fawn'):")
	print("FilterScroll scroll_h: ", scroll.scroll_horizontal if scroll else "null")
	if scroll and scroll.get_h_scroll_bar():
		var hbar := scroll.get_h_scroll_bar()
		print("hbar max: ", hbar.max_value, " page: ", hbar.page)
		
	quit(0)
