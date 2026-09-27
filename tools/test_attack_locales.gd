extends SceneTree

func _init() -> void:
	var words = {
		"zh_TW": "攻擊",
		"zh_CN": "攻击",
		"en": "Attack",
		"ja": "攻撃",
		"ko": "공격",
		"es": "Ataque"
	}
	for loc in words:
		var txt: String = words[loc]
		var btn := Button.new()
		UiStyle.style_button(btn, true)
		btn.custom_minimum_size = Vector2(108, 72)
		btn.text = txt
		btn.add_theme_font_size_override("font_size", 16)
		var font = btn.get_theme_font("font")
		var font_size = btn.get_theme_font_size("font_size")
		var w = font.get_string_size(txt, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
		print(loc, " '", txt, "': text_width=", w, ", btn_width=108, content_avail=", 108 - 44)
	quit()
