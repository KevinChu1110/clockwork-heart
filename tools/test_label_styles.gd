extends SceneTree

func _init():
    root.size = Vector2i(1280, 720)
    var win := root.get_window()
    if win: win.size = Vector2i(1280, 720)

var _frame = 0

func _process(delta):
    _frame += 1
    if _frame == 1:
        change_scene_to_file("res://scenes/main.tscn")
    elif _frame == 25:
        var main = current_scene
        var gs = root.get_node_or_null("GameState")
        if gs:
            gs.call("reset_new_game")
            gs.set("player_name", "小白")
            gs.set("player_race", "rabbit")
        main.call("_start_battle_raw", "road_bandit")
    elif _frame == 45:
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        
        # Test Approach A: outline
        var prl: Label = battle_node.get_node_or_null("SideBars/PlayerSide/PlayerRageLabel")
        if prl:
            prl.add_theme_font_size_override("font_size", 16)
            prl.add_theme_constant_override("outline_size", 4)
            prl.add_theme_color_override("font_outline_color", Color("#FFFDF8"))
            prl.add_theme_color_override("font_color", Color("#B85600")) # dark amber on white outline, or light?
            
        var ptag: Label = battle_node.get_node_or_null("Arena/PlayerSlot/PlayerTag")
        if ptag:
            ptag.add_theme_font_size_override("font_size", 16)
            ptag.add_theme_constant_override("outline_size", 4)
            ptag.add_theme_color_override("font_outline_color", Color("#FFFDF8"))
            ptag.add_theme_color_override("font_color", Color("#1F5EA8"))
            
        var etag: Label = battle_node.get_node_or_null("Arena/EnemySlot/EnemyTag")
        if etag:
            etag.add_theme_font_size_override("font_size", 16)
            etag.add_theme_constant_override("outline_size", 4)
            etag.add_theme_color_override("font_outline_color", Color("#FFFDF8"))
            etag.add_theme_color_override("font_color", Color("#C22B55"))
    elif _frame == 55:
        var img := root.get_viewport().get_texture().get_image()
        img.save_png("/tmp/test_labels_outline.png")
        
        # Now switch to Approach B: mini card
        var host = current_scene.get("host")
        var battle_node = host.get_child(0)
        
        var make_mini_card := func(lbl: Label, text_col: Color = Color("#1F1A3A")) -> void:
            var sb := StyleBoxFlat.new()
            sb.bg_color = Color("#FFFDF8")
            sb.border_color = Color("#1F1A3A")
            sb.set_border_width_all(2)
            sb.border_width_bottom = 3
            sb.set_corner_radius_all(10)
            sb.content_margin_left = 8
            sb.content_margin_right = 8
            sb.content_margin_top = 2
            sb.content_margin_bottom = 2
            sb.shadow_color = Color(0.12, 0.1, 0.23, 0.25)
            sb.shadow_size = 4
            sb.shadow_offset = Vector2(0, 2)
            lbl.add_theme_stylebox_override("normal", sb)
            lbl.add_theme_font_size_override("font_size", 16)
            lbl.add_theme_color_override("font_color", text_col)
            lbl.add_theme_constant_override("outline_size", 0)
            lbl.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
            
        var prl: Label = battle_node.get_node_or_null("SideBars/PlayerSide/PlayerRageLabel")
        if prl:
            make_mini_card.call(prl)
            # For rage label in VBoxContainer, if size_flags_horizontal is shrink center or shrink begin:
            prl.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
            
        var ptag: Label = battle_node.get_node_or_null("Arena/PlayerSlot/PlayerTag")
        if ptag:
            make_mini_card.call(ptag, Color("#1F5EA8")) # deep ally blue on cream white
            
        var etag: Label = battle_node.get_node_or_null("Arena/EnemySlot/EnemyTag")
        if etag:
            make_mini_card.call(etag, Color("#C22B55")) # deep enemy berry red on cream white
    elif _frame == 65:
        var img := root.get_viewport().get_texture().get_image()
        img.save_png("/tmp/test_labels_minicard.png")
        print("Saved both test images.")
        quit(0)
    return false
