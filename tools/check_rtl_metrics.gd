extends SceneTree

func _init():
    var rtl = RichTextLabel.new()
    rtl.size = Vector2(600, 116)
    rtl.bbcode_enabled = true
    rtl.scroll_following = true
    rtl.add_theme_font_size_override("normal_font_size", 16)
    rtl.add_theme_font_size_override("bold_font_size", 16)
    root.add_child(rtl)
    
    rtl.append_text("Line 0: 戰鬥開始！遭遇 路霸盜賊\n")
    rtl.append_text("Line 1: 右側拇指：攻擊／技能／換武／鎖定／暫停／逃離。\n")
    rtl.append_text("Line 2: 敵手筋骨結實（防爆高）——爆擊難進，斧鎚硬砸最實在。\n")
    rtl.append_text("Line 3: 部位破壞！【右腕重刃】打破擊暈！\n")
    rtl.append_text("Line 4: 怒氣滿 · 暴怒！（5 秒攻速與傷害提升）\n")
    rtl.append_text("Line 5: 王者斬要擋，擋住就能反擊\n")
    
    # Wait for frame to update
    var line_h = rtl.get_theme_font("normal_font").get_height(16)
    print("Font height at 16px:", line_h)
    quit(0)
