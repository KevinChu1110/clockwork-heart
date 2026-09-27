extends SceneTree

func _init() -> void:
	var btn := Button.new()
	UiStyle.style_button(btn, true)
	btn.text = "Attack"
	btn.add_theme_font_size_override("font_size", 17)
	var font = btn.get_theme_font("font")
	var font_size = btn.get_theme_font_size("font_size")
	var text_width = font.get_string_size("Attack", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	print("Font size: ", font_size)
	print("Text width of 'Attack': ", text_width)
	print("Button min size: ", btn.custom_minimum_size)
	quit()
