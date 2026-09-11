extends SceneTree

const MobileLobby = preload("res://scripts/ui/mobile_lobby.gd")

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var lobby = MobileLobby.new()
	root.add_child(lobby)
	lobby._ready()
	lobby.open_wardrobe()
	var dlg = lobby.get_node_or_null("WardrobeDialog")
	print("WardrobeDialog:", dlg)
	if dlg:
		var btn = dlg.find_child("CloseBtn", true, false)
		print("CloseBtn node:", btn)
		if btn:
			print("CloseBtn custom_min_size:", btn.custom_minimum_size)
			print("CloseBtn size:", btn.size)
			print("CloseBtn global_rect:", btn.get_global_rect())
			var csb = btn.get_theme_stylebox("normal")
			print("CloseBtn csb:", csb)
			if csb is StyleBoxFlat:
				print("csb bg_color:", csb.bg_color.to_html(), "border_color:", csb.border_color.to_html(), "border_bottom:", csb.border_width_bottom, "radius:", csb.corner_radius_top_left)
	quit(0)
