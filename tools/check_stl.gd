extends SceneTree

func _init():
    var rtl = RichTextLabel.new()
    rtl.size = Vector2(400, 100)
    root.add_child(rtl)
    for i in range(20):
        rtl.append_text("Line %d: This is a test line\n" % i)
    print("Has scroll_to_line:", rtl.has_method("scroll_to_line"))
    quit(0)
