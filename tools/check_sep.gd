extends SceneTree

func _init():
    var rtl = RichTextLabel.new()
    rtl.add_theme_font_size_override("normal_font_size", 16)
    rtl.add_theme_font_size_override("bold_font_size", 16)
    root.add_child(rtl)
    print("line_separation:", rtl.get_theme_constant("line_separation"))
    print("font:", rtl.get_theme_font("normal_font"))
    quit(0)
